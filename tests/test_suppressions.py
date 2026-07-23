"""Suppression behavior for the Material 3 heuristic scanner."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills' / 'material3-design' / 'scripts'
sys.path.insert(0, str(SCRIPTS))

from m3_engine.engine import run_scan  # noqa: E402


class SuppressionTests(unittest.TestCase):
    def _scan(self, files: dict[str, str], platform: str, config: dict | None = None) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
            if config is not None:
                (root / '.m3scan.json').write_text(json.dumps(config), encoding='utf-8')
            _code, output = run_scan(root, platform, 'json')
            return json.loads(output)

    def test_inline_ignore_suppresses_color_literal(self) -> None:
        report = self._scan({
            'Screen.kt': (
                '@Composable fun S() {\n'
                '  // m3-ignore: M3-002\n'
                '  Text(color = Color(0xFF6750A4))\n'
                '  BoxWithConstraints {}\n'
                '}\n'
            ),
        }, 'compose')
        self.assertNotIn('M3-002', {item['rule_id'] for item in report['findings']})
        self.assertGreaterEqual(report.get('suppressed_count', 0), 1)

    def test_file_level_ignore(self) -> None:
        report = self._scan({
            'Screen.kt': (
                '// m3-ignore-file: M3-002\n'
                '@Composable fun S() { Text(color = Color(0xFF6750A4)); BoxWithConstraints {} }\n'
            ),
        }, 'compose')
        self.assertNotIn('M3-002', {item['rule_id'] for item in report['findings']})

    def test_config_path_suppression(self) -> None:
        report = self._scan(
            {'docs/demo.css': '.x { color: #6750A4; }\n@media (width > 1px) { .y {} }\n'},
            'web',
            {'suppress': [{'rule_id': 'M3-002', 'path': 'docs/**', 'reason': 'docs samples'}]},
        )
        self.assertNotIn('M3-002', {item['rule_id'] for item in report['findings']})

    def test_theme_filename_builtin_skip(self) -> None:
        report = self._scan({
            'Theme.kt': 'val p = Color(0xFF6750A4)\n@Composable fun T() { MaterialTheme {}; BoxWithConstraints {} }\n',
        }, 'compose')
        self.assertNotIn('M3-002', {item['rule_id'] for item in report['findings']})


    def test_inline_ignore_suppresses_whole_file_finding(self) -> None:
        report = self._scan({
            'Screen.kt': (
                '// m3-ignore: M3-009\n'
                'IconButton(onClick = {}) { Icon(Icons.Default.Add, contentDescription = null) }\n'
                'fun layout() { BoxWithConstraints {} }\n'
            ),
        }, 'compose')
        self.assertNotIn('M3-009', {item['rule_id'] for item in report['findings']})
        self.assertGreaterEqual(report.get('suppressed_count', 0), 1)

    def test_malformed_json_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'Screen.kt').write_text(
                'fun layout() { BoxWithConstraints {} }',
                encoding='utf-8',
            )
            (root / '.m3scan.json').write_text('{"suppress": [', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'invalid suppression config JSON'):
                run_scan(root, 'compose', 'json')


if __name__ == '__main__':
    unittest.main()
