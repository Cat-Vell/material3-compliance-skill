from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"
RUNS = ROOT / "evals" / "runs"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_FIELDS = {
    "schema_version", "run_id", "fixture_id", "fixture_sha256", "git_revision",
    "working_tree_clean", "host", "host_version", "model", "condition",
    "repetition", "metrics", "started_at", "completed_at", "prompt_artifact",
    "response_artifact", "assertions", "forbidden_claims", "generated_files",
    "test_output", "human_deviations", "reviewer", "result",
}
CONDITIONS = {"with-skill", "baseline"}
METRIC_KEYS = {"input_tokens", "output_tokens", "duration_seconds"}


def parse_utc(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def load_fixtures(errors: list[str]) -> dict[str, tuple[Path, dict]]:
    fixtures: dict[str, tuple[Path, dict]] = {}
    for path in sorted(FIXTURES.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        fixtures[data["id"]] = (path, data)
    if len(fixtures) != 12:
        errors.append(f"expected 12 fixtures, found {len(fixtures)}")
    return fixtures


def revision_exists(revision: str) -> bool:
    try:
        completed = subprocess.run(
            ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return completed.returncode == 0


def validate_artifact_path(label: Path, field: str, value: object, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: {field} must be a non-empty repository-relative path")
        return
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append(f"{label}: {field} must stay inside the repository")
        return
    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f"{label}: {field} must stay inside the repository")
        return
    if not resolved.is_file():
        errors.append(f"{label}: {field} does not exist: {value}")


def validate_metrics(label: Path, metrics: object, errors: list[str]) -> None:
    if not isinstance(metrics, dict):
        errors.append(f"{label}: metrics must be an object")
        return
    if set(metrics) != METRIC_KEYS:
        errors.append(f"{label}: metrics must contain exactly {sorted(METRIC_KEYS)}")
        return
    for key in ("input_tokens", "output_tokens"):
        value = metrics[key]
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            errors.append(f"{label}: metrics.{key} must be a non-negative integer or null")
    duration = metrics["duration_seconds"]
    if duration is not None and (not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration < 0):
        errors.append(f"{label}: metrics.duration_seconds must be a non-negative number or null")


def validate_run(
    path: Path,
    run: object,
    fixtures: dict[str, tuple[Path, dict]],
    errors: list[str],
) -> tuple[int, int] | None:
    label = path.relative_to(ROOT)
    if not isinstance(run, dict):
        errors.append(f"{label}: record must be a JSON object")
        return None
    missing = REQUIRED_FIELDS - run.keys()
    extra = run.keys() - REQUIRED_FIELDS
    if missing:
        errors.append(f"{label}: missing fields {sorted(missing)}")
    if extra:
        errors.append(f"{label}: unexpected fields {sorted(extra)}")
    if missing:
        return None

    fixture_entry = fixtures.get(run["fixture_id"])
    if fixture_entry is None:
        errors.append(f"{label}: unknown fixture_id {run['fixture_id']}")
        return None
    fixture_path, fixture = fixture_entry
    digest = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    if run["fixture_sha256"] != digest or not SHA64.fullmatch(str(run["fixture_sha256"])):
        errors.append(f"{label}: fixture_sha256 does not match {fixture_path.name}")
    if run["schema_version"] != 2:
        errors.append(f"{label}: schema_version must be 2")
    if not SHA40.fullmatch(str(run["git_revision"])):
        errors.append(f"{label}: git_revision must be a full lowercase 40-character SHA")
    if run["working_tree_clean"] is not True:
        errors.append(f"{label}: working_tree_clean must be true for archived evidence")
    for field in ("run_id", "host", "host_version", "model", "reviewer"):
        if not isinstance(run[field], str) or not run[field].strip():
            errors.append(f"{label}: {field} must be a non-empty string")
    if run["condition"] not in CONDITIONS:
        errors.append(f"{label}: condition must be one of {sorted(CONDITIONS)}")
    if not isinstance(run["repetition"], int) or isinstance(run["repetition"], bool) or run["repetition"] < 1:
        errors.append(f"{label}: repetition must be an integer >= 1")
    validate_metrics(label, run["metrics"], errors)
    for field in ("prompt_artifact", "response_artifact"):
        validate_artifact_path(label, field, run[field], errors)
    for field in ("started_at", "completed_at"):
        if not parse_utc(run[field]):
            errors.append(f"{label}: {field} must be an ISO-8601 UTC timestamp ending in Z")
    for field in ("generated_files", "test_output", "human_deviations"):
        if not isinstance(run[field], list) or not all(isinstance(item, str) for item in run[field]):
            errors.append(f"{label}: {field} must be a string array")

    expected_assertions = fixture["required_assertions"]
    critical = set(fixture["critical_assertion_indexes"])
    assertions = run["assertions"]
    if not isinstance(assertions, list) or len(assertions) != len(expected_assertions):
        errors.append(f"{label}: assertion result count must equal fixture assertions")
        assertions = []
    passed_count = 0
    critical_pass = True
    for index, assertion in enumerate(assertions):
        expected_keys = {"index", "assertion", "critical", "passed", "evidence"}
        if not isinstance(assertion, dict) or set(assertion) != expected_keys:
            errors.append(f"{label}: assertion {index} has invalid fields")
            continue
        if assertion["index"] != index or assertion["assertion"] != expected_assertions[index]:
            errors.append(f"{label}: assertion {index} does not match fixture")
        if assertion["critical"] != (index in critical):
            errors.append(f"{label}: assertion {index} critical flag does not match fixture")
        if not isinstance(assertion["passed"], bool):
            errors.append(f"{label}: assertion {index} passed must be boolean")
        elif assertion["passed"]:
            passed_count += 1
        elif index in critical:
            critical_pass = False
        if not isinstance(assertion["evidence"], list) or not all(
            isinstance(item, str) and item for item in assertion["evidence"]
        ):
            errors.append(f"{label}: assertion {index} evidence must be a non-empty-string array")

    expected_forbidden = fixture["forbidden_claims"]
    forbidden = run["forbidden_claims"]
    no_forbidden = True
    if not isinstance(forbidden, list) or len(forbidden) != len(expected_forbidden):
        errors.append(f"{label}: forbidden-claim result count must equal fixture")
        forbidden = []
    for index, claim in enumerate(forbidden):
        expected_keys = {"claim", "observed", "evidence"}
        if not isinstance(claim, dict) or set(claim) != expected_keys:
            errors.append(f"{label}: forbidden claim {index} has invalid fields")
            continue
        if claim["claim"] != expected_forbidden[index]:
            errors.append(f"{label}: forbidden claim {index} does not match fixture")
        if not isinstance(claim["observed"], bool):
            errors.append(f"{label}: forbidden claim {index} observed must be boolean")
        elif claim["observed"]:
            no_forbidden = False
        if not isinstance(claim["evidence"], list) or not all(isinstance(item, str) for item in claim["evidence"]):
            errors.append(f"{label}: forbidden claim {index} evidence must be a string array")

    calculated = "pass" if critical_pass and no_forbidden else "fail"
    if run["result"] != calculated:
        errors.append(f"{label}: result must be {calculated} from critical and forbidden-claim results")
    return passed_count, len(expected_assertions)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate archived Material 3 behavior run records.")
    parser.add_argument("--require-host", action="append", default=[], help="Require records for this host.")
    parser.add_argument(
        "--require-all-fixtures",
        action="store_true",
        help="Require every fixture×condition for each required host.",
    )
    parser.add_argument(
        "--min-repetitions",
        type=int,
        default=1,
        help="Minimum archived repetitions per host×fixture×condition (default: 1).",
    )
    parser.add_argument(
        "--conditions",
        default="with-skill,baseline",
        help="Comma-separated conditions required under --require-all-fixtures (default: with-skill,baseline).",
    )
    args = parser.parse_args()
    if args.min_repetitions < 1:
        print("ERROR: --min-repetitions must be >= 1")
        return 1
    required_conditions = {item.strip() for item in args.conditions.split(",") if item.strip()}
    if not required_conditions or not required_conditions.issubset(CONDITIONS):
        print(f"ERROR: --conditions must be a non-empty subset of {sorted(CONDITIONS)}")
        return 1

    errors: list[str] = []
    fixtures = load_fixtures(errors)
    records: list[dict] = []
    run_ids: set[str] = set()
    coverage: Counter[tuple[str, str, str]] = Counter()
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    failed_runs: Counter[str] = Counter()
    for path in sorted(RUNS.glob("*.json")):
        try:
            run = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        result = validate_run(path, run, fixtures, errors)
        if not isinstance(run, dict):
            continue
        run_id = run.get("run_id")
        if run_id in run_ids:
            errors.append(f"{path.relative_to(ROOT)}: duplicate run_id {run_id}")
        run_ids.add(run_id)
        host = run.get("host")
        fixture_id = run.get("fixture_id")
        condition = run.get("condition")
        if isinstance(host, str) and isinstance(fixture_id, str) and isinstance(condition, str):
            host = host.lower()
            coverage[(host, fixture_id, condition)] += 1
            # Release gates apply only to with-skill runs; baseline is contrast evidence.
            if condition == "with-skill":
                if result:
                    totals[host][0] += result[0]
                    totals[host][1] += result[1]
                if run.get("result") != "pass":
                    failed_runs[host] += 1
        revision = run.get("git_revision")
        if isinstance(revision, str) and SHA40.fullmatch(revision) and not revision_exists(revision):
            errors.append(f"{path.relative_to(ROOT)}: git_revision is not present in repository history")
        records.append(run)

    required_hosts = {host.lower() for host in args.require_host}
    present_hosts = {host for host, _fixture, _condition in coverage}
    missing_hosts = required_hosts - present_hosts
    for host in sorted(missing_hosts):
        errors.append(f"required host has no archived records: {host}")
    if args.require_all_fixtures:
        if not required_hosts:
            errors.append("--require-all-fixtures requires at least one --require-host")
        for host in sorted(required_hosts - missing_hosts):
            for fixture_id in fixtures:
                for condition in sorted(required_conditions):
                    count = coverage[(host, fixture_id, condition)]
                    if count < args.min_repetitions:
                        errors.append(
                            f"expected at least {args.min_repetitions} {host}/{fixture_id}/{condition} "
                            f"record(s), found {count}"
                        )
            passed, total = totals[host]
            if total == 0 or passed / total < 0.9:
                errors.append(f"{host}: with-skill overall assertion pass rate is below 90% ({passed}/{total})")
            if failed_runs[host]:
                errors.append(
                    f"{host}: {failed_runs[host]} with-skill run(s) failed a critical or forbidden-claim gate"
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if records:
        print(f"Behavior run-record validation passed ({len(records)} archived records).")
    else:
        print("Behavior run-record validation passed (0 archived records; no host behavior evidence).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
