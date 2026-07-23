#!/usr/bin/env python3
"""Validate trigger cases and score archived trigger run results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).resolve().parent / "cases.json"
EXPECTED_COUNTS = {
    "should-trigger": 25,
    "should-not-trigger": 15,
    "near-miss": 10,
}
VALID_EXPECTED = {"trigger", "no-trigger"}
VALID_OBSERVED = {"trigger", "no-trigger"}


def load_cases() -> dict:
    return json.loads(CASES.read_text(encoding="utf-8"))


def validate_cases(data: dict) -> list[str]:
    errors: list[str] = []
    cases = data.get("cases")
    if not isinstance(cases, list):
        return ["cases must be an array"]
    if len(cases) != 50:
        errors.append(f"expected 50 cases, found {len(cases)}")
    ids: set[str] = set()
    counts = {key: 0 for key in EXPECTED_COUNTS}
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"case {index}: must be an object")
            continue
        for field in ("id", "category", "expected", "prompt"):
            if field not in case or not isinstance(case[field], str) or not case[field].strip():
                errors.append(f"case {index}: missing non-empty {field}")
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in ids:
                errors.append(f"duplicate case id: {case_id}")
            ids.add(case_id)
        category = case.get("category")
        if category in counts:
            counts[category] += 1
        elif category is not None:
            errors.append(f"case {case_id}: unknown category {category}")
        if case.get("expected") not in VALID_EXPECTED:
            errors.append(f"case {case_id}: expected must be trigger or no-trigger")
        if category == "should-trigger" and case.get("expected") != "trigger":
            errors.append(f"case {case_id}: should-trigger must expect trigger")
        if category in {"should-not-trigger", "near-miss"} and case.get("expected") != "no-trigger":
            errors.append(f"case {case_id}: {category} must expect no-trigger")
    for category, expected_count in EXPECTED_COUNTS.items():
        if counts[category] != expected_count:
            errors.append(f"{category}: expected {expected_count}, found {counts[category]}")
    targets = data.get("targets") or {}
    for key in ("precision_min", "recall_min", "near_miss_false_trigger_max"):
        if key not in targets:
            errors.append(f"targets missing {key}")
    return errors


def score(cases: list[dict], results: list[dict]) -> tuple[dict, list[str]]:
    errors: list[str] = []
    by_id = {case["id"]: case for case in cases}
    seen: set[str] = set()
    tp = fp = tn = fn = 0
    near_miss_total = 0
    near_miss_false = 0
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            errors.append(f"result {index}: must be an object")
            continue
        case_id = result.get("id")
        observed = result.get("observed")
        if case_id not in by_id:
            errors.append(f"result {index}: unknown id {case_id}")
            continue
        if case_id in seen:
            errors.append(f"duplicate result for {case_id}")
            continue
        seen.add(case_id)
        if observed not in VALID_OBSERVED:
            errors.append(f"result {case_id}: observed must be trigger or no-trigger")
            continue
        expected = by_id[case_id]["expected"]
        category = by_id[case_id]["category"]
        if expected == "trigger" and observed == "trigger":
            tp += 1
        elif expected == "no-trigger" and observed == "trigger":
            fp += 1
        elif expected == "no-trigger" and observed == "no-trigger":
            tn += 1
        elif expected == "trigger" and observed == "no-trigger":
            fn += 1
        if category == "near-miss":
            near_miss_total += 1
            if observed == "trigger":
                near_miss_false += 1
    missing = sorted(set(by_id) - seen)
    if missing:
        errors.append(f"missing results for: {', '.join(missing)}")
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    near_miss_rate = near_miss_false / near_miss_total if near_miss_total else 0.0
    return {
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "near_miss_false_trigger_rate": round(near_miss_rate, 4),
        "scored_cases": len(seen),
    }, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and score Material 3 skill trigger evaluations.")
    parser.add_argument(
        "--results",
        type=Path,
        help="JSON file with [{id, observed}] for each case. Omit to validate cases only.",
    )
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Exit non-zero if precision/recall/near-miss targets are missed.",
    )
    args = parser.parse_args()

    data = load_cases()
    errors = validate_cases(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Trigger case validation passed ({len(data['cases'])} cases).")

    if args.results is None:
        return 0

    try:
        payload = json.loads(args.results.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read results: {exc}")
        return 1
    results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
    if not isinstance(results, list):
        print("ERROR: results must be a JSON array or {\"results\": [...]}")
        return 1

    metrics, score_errors = score(data["cases"], results)
    if score_errors:
        for error in score_errors:
            print(f"ERROR: {error}")
        return 1

    targets = data["targets"]
    print(json.dumps(metrics, indent=2))
    failed = False
    if metrics["precision"] < targets["precision_min"]:
        print(f"FAIL: precision {metrics['precision']} < {targets['precision_min']}")
        failed = True
    if metrics["recall"] < targets["recall_min"]:
        print(f"FAIL: recall {metrics['recall']} < {targets['recall_min']}")
        failed = True
    if metrics["near_miss_false_trigger_rate"] > targets["near_miss_false_trigger_max"]:
        print(
            f"FAIL: near-miss false trigger rate {metrics['near_miss_false_trigger_rate']} "
            f"> {targets['near_miss_false_trigger_max']}"
        )
        failed = True
    if failed and args.require_pass:
        return 1
    if not failed:
        print("Trigger score targets met.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
