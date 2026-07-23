"""Validate per-rule fixtures and metrics.json for the scanner rule engine."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills' / 'material3-design' / 'scripts'
sys.path.insert(0, str(SCRIPTS))

from m3_engine.engine import run_scan  # noqa: E402
from m3_engine.registry import RULES_ROOT, load_rules  # noqa: E402


def expect_hit(name: str) -> bool | None:
    lower = name.lower()
    if lower.startswith('positive') or lower.startswith('edge_hit'):
        return True
    if lower.startswith('negative') or lower.startswith('edge_'):
        return False
    return None


class ScannerRuleFixtureTests(unittest.TestCase):
    def test_every_rule_has_required_metadata_and_fixtures(self) -> None:
        rules = load_rules()
        self.assertGreaterEqual(len(rules), 11)
        for rule in rules:
            self.assertTrue(rule.rule_id.startswith('M3-'))
            self.assertTrue(rule.source_id.startswith('S-'))
            self.assertFalse(rule.autofix)
            self.assertIn(rule.matcher, {'regex', 'whole_file'})
            self.assertIsNotNone(rule.module_dir)
            fixtures = rule.module_dir / 'fixtures'
            metrics = rule.module_dir / 'metrics.json'
            self.assertTrue(fixtures.is_dir(), msg=f'{rule.platform}/{rule.title} missing fixtures')
            self.assertTrue(metrics.is_file(), msg=f'{rule.platform}/{rule.title} missing metrics.json')
            names = [p.name for p in fixtures.iterdir() if p.is_file()]
            self.assertTrue(any(n.startswith('positive') for n in names), msg=rule.title)
            self.assertTrue(any(n.startswith('negative') for n in names), msg=rule.title)
            self.assertTrue(any(n.startswith('edge_') for n in names), msg=rule.title)
            data = json.loads(metrics.read_text(encoding='utf-8'))
            for key in ('precision', 'recall', 'true_positives', 'false_positives', 'false_negatives'):
                self.assertIn(key, data)

    def test_fixtures_match_hit_expectations_and_metrics(self) -> None:
        for rule in load_rules():
            tp = fp = fn = 0
            fixture_count = 0
            for path in sorted((rule.module_dir / 'fixtures').iterdir()):
                if not path.is_file():
                    continue
                wanted = expect_hit(path.name)
                if wanted is None:
                    continue
                fixture_count += 1
                with tempfile.TemporaryDirectory() as directory:
                    target = Path(directory) / path.name
                    target.write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
                    code, output = run_scan(target, rule.platform, 'json')
                    report = json.loads(output)
                    hit = any(item['rule_id'] == rule.rule_id for item in report['findings'])
                if wanted and hit:
                    tp += 1
                elif wanted and not hit:
                    fn += 1
                    self.fail(f'{rule.platform}/{rule.title}/{path.name}: expected hit for {rule.rule_id}')
                elif not wanted and hit:
                    fp += 1
                    self.fail(f'{rule.platform}/{rule.title}/{path.name}: unexpected hit for {rule.rule_id}')
            precision = 1.0 if (tp + fp) == 0 else tp / (tp + fp)
            recall = 1.0 if (tp + fn) == 0 else tp / (tp + fn)
            stored = json.loads((rule.module_dir / 'metrics.json').read_text(encoding='utf-8'))
            self.assertEqual(stored['rule_id'], rule.rule_id)
            self.assertEqual(stored['platform'], rule.platform)
            self.assertAlmostEqual(stored['precision'], precision, places=4)
            self.assertAlmostEqual(stored['recall'], recall, places=4)
            self.assertEqual(stored['true_positives'], tp)
            self.assertEqual(stored['false_positives'], fp)
            self.assertEqual(stored['false_negatives'], fn)
            self.assertEqual(stored['fixture_count'], fixture_count)

    def test_rule_ids_cover_m3_001_through_011(self) -> None:
        ids = {rule.rule_id for rule in load_rules()}
        self.assertEqual(ids, {f'M3-{n:03d}' for n in range(1, 12)})
        self.assertTrue(RULES_ROOT.is_dir())


if __name__ == '__main__':
    unittest.main()
