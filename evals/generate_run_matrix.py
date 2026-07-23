#!/usr/bin/env python3
"""Generate a with-skill / baseline behavior-run matrix for the twelve fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"
MATRIX = ROOT / "evals" / "matrix"
DEFAULT_HOSTS = ("codex", "claude")
DEFAULT_CONDITIONS = ("with-skill", "baseline")


def git_revision() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return "0" * 40
    return completed.stdout.strip()


def load_fixtures() -> list[tuple[Path, dict]]:
    items: list[tuple[Path, dict]] = []
    for path in sorted(FIXTURES.glob("*.json")):
        items.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return items


def build_prompt(fixture: dict, condition: str) -> str:
    evidence = "; ".join(fixture["input_evidence"])
    mode = fixture["mode"]
    platform = fixture["platform"]
    task = fixture["task"]
    assertions = "\n".join(f"- {item}" for item in fixture["required_assertions"])
    forbidden = "\n".join(f"- {item}" for item in fixture["forbidden_claims"])
    skill_line = (
        "Use $material3-design for this task.\n"
        if condition == "with-skill"
        else "Do not use the material3-design skill. Answer from general knowledge only.\n"
    )
    return (
        f"{skill_line}"
        f"Mode: {mode}\n"
        f"Platform: {platform}\n"
        f"Task: {task}\n"
        f"Input evidence: {evidence}\n\n"
        f"Satisfy these assertions:\n{assertions}\n\n"
        f"Do not make these claims:\n{forbidden}\n"
    )


def blank_record(fixture_path: Path, fixture: dict, host: str, condition: str, repetition: int, revision: str) -> dict:
    digest = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    run_id = f"{host}-{fixture['id']}-{condition}-r{repetition}"
    return {
        "schema_version": 2,
        "run_id": run_id,
        "fixture_id": fixture["id"],
        "fixture_sha256": digest,
        "git_revision": revision,
        "working_tree_clean": True,
        "host": host,
        "host_version": "FILL",
        "model": "FILL",
        "condition": condition,
        "repetition": repetition,
        "metrics": {
            "input_tokens": None,
            "output_tokens": None,
            "duration_seconds": None,
        },
        "started_at": "FILL-UTC-Z",
        "completed_at": "FILL-UTC-Z",
        "prompt_artifact": f"evals/runs/artifacts/{run_id}/prompt.md",
        "response_artifact": f"evals/runs/artifacts/{run_id}/response.md",
        "assertions": [
            {
                "index": index,
                "assertion": assertion,
                "critical": index in fixture["critical_assertion_indexes"],
                "passed": False,
                "evidence": ["FILL"],
            }
            for index, assertion in enumerate(fixture["required_assertions"])
        ],
        "forbidden_claims": [
            {"claim": claim, "observed": False, "evidence": []}
            for claim in fixture["forbidden_claims"]
        ],
        "generated_files": [],
        "test_output": [],
        "human_deviations": [],
        "reviewer": "FILL",
        "result": "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Material 3 behavior-run matrix prompts and blank records.")
    parser.add_argument("--hosts", default=",".join(DEFAULT_HOSTS), help="Comma-separated hosts (default: codex,claude).")
    parser.add_argument(
        "--conditions",
        default=",".join(DEFAULT_CONDITIONS),
        help="Comma-separated conditions (default: with-skill,baseline).",
    )
    parser.add_argument("--repetitions", type=int, default=1, help="Repetitions per cell (default: 1).")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without writing files.")
    parser.add_argument("--out", type=Path, default=MATRIX, help="Output directory (default: evals/matrix).")
    args = parser.parse_args()
    if args.repetitions < 1:
        print("ERROR: --repetitions must be >= 1", file=sys.stderr)
        return 1

    hosts = [item.strip().lower() for item in args.hosts.split(",") if item.strip()]
    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]
    if not hosts or not conditions:
        print("ERROR: hosts and conditions must be non-empty", file=sys.stderr)
        return 1
    for condition in conditions:
        if condition not in DEFAULT_CONDITIONS:
            print(f"ERROR: unknown condition {condition}", file=sys.stderr)
            return 1

    fixtures = load_fixtures()
    if len(fixtures) != 12:
        print(f"ERROR: expected 12 fixtures, found {len(fixtures)}", file=sys.stderr)
        return 1

    revision = git_revision()
    cells: list[dict] = []
    for fixture_path, fixture in fixtures:
        for host in hosts:
            for condition in conditions:
                for repetition in range(1, args.repetitions + 1):
                    run_id = f"{host}-{fixture['id']}-{condition}-r{repetition}"
                    cells.append(
                        {
                            "run_id": run_id,
                            "fixture_id": fixture["id"],
                            "fixture_file": fixture_path.name,
                            "fixture_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
                            "host": host,
                            "condition": condition,
                            "repetition": repetition,
                            "git_revision": revision,
                            "prompt": build_prompt(fixture, condition),
                            "blank_record": blank_record(
                                fixture_path, fixture, host, condition, repetition, revision
                            ),
                        }
                    )

    print(
        f"Matrix plan: {len(fixtures)} fixtures × {len(hosts)} hosts × "
        f"{len(conditions)} conditions × {args.repetitions} reps = {len(cells)} runs"
    )
    if args.dry_run:
        for cell in cells:
            print(f"- {cell['run_id']}")
        return 0

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "git_revision": revision,
        "hosts": hosts,
        "conditions": conditions,
        "repetitions": args.repetitions,
        "run_count": len(cells),
        "runs": [
            {
                "run_id": cell["run_id"],
                "fixture_id": cell["fixture_id"],
                "fixture_file": cell["fixture_file"],
                "fixture_sha256": cell["fixture_sha256"],
                "host": cell["host"],
                "condition": cell["condition"],
                "repetition": cell["repetition"],
                "prompt_path": f"prompts/{cell['run_id']}.md",
                "blank_record_path": f"blank-records/{cell['run_id']}.json",
            }
            for cell in cells
        ],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    prompts_dir = out / "prompts"
    blanks_dir = out / "blank-records"
    prompts_dir.mkdir(exist_ok=True)
    blanks_dir.mkdir(exist_ok=True)
    for cell in cells:
        (prompts_dir / f"{cell['run_id']}.md").write_text(cell["prompt"], encoding="utf-8")
        (blanks_dir / f"{cell['run_id']}.json").write_text(
            json.dumps(cell["blank_record"], indent=2) + "\n",
            encoding="utf-8",
        )
    readme = out / "README.md"
    readme.write_text(
        "# Behavior run matrix\n\n"
        "Generated by `python evals/generate_run_matrix.py`.\n\n"
        "1. Open each prompt under `prompts/`.\n"
        "2. Run it on the named host under the named condition.\n"
        "3. Copy the matching blank record from `blank-records/` into `evals/runs/` after filling results.\n"
        "4. Store prompt/response artifacts at the paths listed in the record.\n"
        "5. Validate with `python tests/validate_eval_runs.py`.\n"
        "6. Aggregate with `python evals/benchmark_report.py`.\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(cells)} prompts and blank records under {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
