#!/usr/bin/env python3
"""Aggregate archived behavior runs into BENCHMARK.md and benchmark.json."""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "evals" / "runs"
OUT_MD = ROOT / "BENCHMARK.md"
OUT_JSON = ROOT / "benchmark.json"


def mean_or_none(values: list[float]) -> float | None:
    return round(statistics.mean(values), 2) if values else None


def pct(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(100.0 * numerator / denominator, 1)


def load_runs() -> list[dict]:
    records: list[dict] = []
    for path in sorted(RUNS.glob("*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    return records


def aggregate(records: list[dict]) -> dict:
    buckets: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for run in records:
        host = str(run.get("host", "")).lower()
        condition = str(run.get("condition", ""))
        buckets[(host, condition)].append(run)

    groups = []
    for (host, condition), runs in sorted(buckets.items()):
        assertion_pass = 0
        assertion_total = 0
        critical_pass = 0
        critical_total = 0
        forbidden_observed = 0
        result_pass = 0
        input_tokens: list[float] = []
        output_tokens: list[float] = []
        durations: list[float] = []
        for run in runs:
            if run.get("result") == "pass":
                result_pass += 1
            for assertion in run.get("assertions", []):
                assertion_total += 1
                if assertion.get("passed"):
                    assertion_pass += 1
                if assertion.get("critical"):
                    critical_total += 1
                    if assertion.get("passed"):
                        critical_pass += 1
            for claim in run.get("forbidden_claims", []):
                if claim.get("observed"):
                    forbidden_observed += 1
            metrics = run.get("metrics") or {}
            if isinstance(metrics.get("input_tokens"), (int, float)):
                input_tokens.append(float(metrics["input_tokens"]))
            if isinstance(metrics.get("output_tokens"), (int, float)):
                output_tokens.append(float(metrics["output_tokens"]))
            if isinstance(metrics.get("duration_seconds"), (int, float)):
                durations.append(float(metrics["duration_seconds"]))
        groups.append(
            {
                "host": host,
                "condition": condition,
                "run_count": len(runs),
                "result_pass_rate": pct(result_pass, len(runs)),
                "critical_assertion_pass_rate": pct(critical_pass, critical_total),
                "all_assertion_pass_rate": pct(assertion_pass, assertion_total),
                "forbidden_claim_count": forbidden_observed,
                "mean_input_tokens": mean_or_none(input_tokens),
                "mean_output_tokens": mean_or_none(output_tokens),
                "mean_duration_seconds": mean_or_none(durations),
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "archived_run_count": len(records),
        "groups": groups,
    }


def fmt(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value}"
    return str(value)


def render_markdown(report: dict) -> str:
    lines = [
        "# Behavior benchmark",
        "",
        f"Generated at `{report['generated_at']}` from `evals/runs/`.",
        "",
        f"**Archived host behavior runs: {report['archived_run_count']}**",
        "",
    ]
    if report["archived_run_count"] == 0:
        lines.extend(
            [
                "No archived runs yet. This table is a placeholder until with-skill and baseline records exist.",
                "",
                "| Host | Condition | Runs | Critical assertion % | All assertion % | Forbidden claims | Mean input tokens | Mean duration (s) |",
                "|---|---|---:|---:|---:|---:|---:|---:|",
                "| — | — | 0 | — | — | — | — | — |",
                "",
                "Produce prompts with `python evals/generate_run_matrix.py`, archive records under `evals/runs/`, then re-run this script.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "| Host | Condition | Runs | Critical assertion % | All assertion % | Forbidden claims | Mean input tokens | Mean duration (s) |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for group in report["groups"]:
        lines.append(
            "| {host} | {condition} | {run_count} | {critical} | {all_a} | {forbidden} | {tokens} | {duration} |".format(
                host=group["host"],
                condition=group["condition"],
                run_count=group["run_count"],
                critical=fmt(group["critical_assertion_pass_rate"]),
                all_a=fmt(group["all_assertion_pass_rate"]),
                forbidden=group["forbidden_claim_count"],
                tokens=fmt(group["mean_input_tokens"]),
                duration=fmt(group["mean_duration_seconds"]),
            )
        )
    lines.extend(
        [
            "",
            "## With-skill vs baseline (same host)",
            "",
            "| Host | Critical Δ (pp) | All assertion Δ (pp) | Forbidden Δ | Token Δ |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    by_host: dict[str, dict[str, dict]] = defaultdict(dict)
    for group in report["groups"]:
        by_host[group["host"]][group["condition"]] = group
    for host, conditions in sorted(by_host.items()):
        skill = conditions.get("with-skill")
        base = conditions.get("baseline")
        if not skill or not base:
            lines.append(f"| {host} | — | — | — | — |")
            continue
        crit_delta = None
        all_delta = None
        if skill["critical_assertion_pass_rate"] is not None and base["critical_assertion_pass_rate"] is not None:
            crit_delta = round(skill["critical_assertion_pass_rate"] - base["critical_assertion_pass_rate"], 1)
        if skill["all_assertion_pass_rate"] is not None and base["all_assertion_pass_rate"] is not None:
            all_delta = round(skill["all_assertion_pass_rate"] - base["all_assertion_pass_rate"], 1)
        forbidden_delta = skill["forbidden_claim_count"] - base["forbidden_claim_count"]
        token_delta = None
        if skill["mean_input_tokens"] is not None and base["mean_input_tokens"] is not None:
            token_delta = round(skill["mean_input_tokens"] - base["mean_input_tokens"], 1)
        lines.append(
            f"| {host} | {fmt(crit_delta)} | {fmt(all_delta)} | {forbidden_delta} | {fmt(token_delta)} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    records = load_runs()
    report = aggregate(records)
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)} and {OUT_JSON.relative_to(ROOT)} ({report['archived_run_count']} runs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
