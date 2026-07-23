from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tests" / "validate_eval_runs.py"
SPEC = importlib.util.spec_from_file_location("validate_eval_runs", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class EvalRunValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_path = ROOT / "evals" / "fixtures" / "01-compose-theme.json"
        self.fixture = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        critical = set(self.fixture["critical_assertion_indexes"])
        self.run = {
            "schema_version": 2,
            "run_id": "test-codex-compose-theme",
            "fixture_id": self.fixture["id"],
            "fixture_sha256": hashlib.sha256(self.fixture_path.read_bytes()).hexdigest(),
            "git_revision": "a" * 40,
            "working_tree_clean": True,
            "host": "codex",
            "host_version": "test-host",
            "model": "test-model",
            "condition": "with-skill",
            "repetition": 1,
            "metrics": {
                "input_tokens": 100,
                "output_tokens": 200,
                "duration_seconds": 12.5,
            },
            "started_at": "2026-07-22T12:00:00Z",
            "completed_at": "2026-07-22T12:05:00Z",
            "prompt_artifact": "README.md",
            "response_artifact": "CHANGELOG.md",
            "assertions": [
                {
                    "index": index,
                    "assertion": assertion,
                    "critical": index in critical,
                    "passed": True,
                    "evidence": [f"response line {index + 1}"],
                }
                for index, assertion in enumerate(self.fixture["required_assertions"])
            ],
            "forbidden_claims": [
                {"claim": claim, "observed": False, "evidence": []}
                for claim in self.fixture["forbidden_claims"]
            ],
            "generated_files": [],
            "test_output": [],
            "human_deviations": [],
            "reviewer": "test reviewer",
            "result": "pass",
        }
        self.fixtures = {self.fixture["id"]: (self.fixture_path, self.fixture)}

    def validate(self) -> tuple[list[str], tuple[int, int] | None]:
        errors: list[str] = []
        result = VALIDATOR.validate_run(ROOT / "record.json", self.run, self.fixtures, errors)
        return errors, result

    def test_accepts_complete_revision_anchored_record(self) -> None:
        errors, result = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(result, (len(self.fixture["required_assertions"]), len(self.fixture["required_assertions"])))

    def test_accepts_null_metrics(self) -> None:
        self.run["metrics"] = {
            "input_tokens": None,
            "output_tokens": None,
            "duration_seconds": None,
        }
        errors, result = self.validate()
        self.assertEqual(errors, [])
        self.assertIsNotNone(result)

    def test_rejects_dirty_or_placeholder_revision(self) -> None:
        self.run["working_tree_clean"] = False
        self.run["git_revision"] = "WORKTREE"
        errors, _result = self.validate()
        self.assertTrue(any("40-character SHA" in error for error in errors))
        self.assertTrue(any("working_tree_clean" in error for error in errors))

    def test_rejects_failed_critical_assertion_marked_pass(self) -> None:
        critical_index = self.fixture["critical_assertion_indexes"][0]
        self.run["assertions"][critical_index]["passed"] = False
        errors, result = self.validate()
        self.assertEqual(result, (len(self.fixture["required_assertions"]) - 1, len(self.fixture["required_assertions"])))
        self.assertTrue(any("result must be fail" in error for error in errors))

    def test_rejects_invalid_condition(self) -> None:
        self.run["condition"] = "skill-on"
        errors, _result = self.validate()
        self.assertTrue(any("condition must be one of" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
