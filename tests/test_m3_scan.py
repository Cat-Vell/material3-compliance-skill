from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills' / 'material3-design' / 'scripts' / 'm3_scan.py'
SPEC = importlib.util.spec_from_file_location('m3_scan', SCRIPT)
assert SPEC and SPEC.loader
m3_scan = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m3_scan
SPEC.loader.exec_module(m3_scan)


class ScannerTests(unittest.TestCase):
    def scan(self, files: dict[str, str], platform: str = 'auto') -> tuple[int, dict]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
            output = StringIO()
            with redirect_stdout(output):
                code = m3_scan.main([str(root), '--platform', platform, '--format', 'json'])
            return code, json.loads(output.getvalue())

    def test_compose_m2_import_is_blocker(self) -> None:
        code, report = self.scan({'Main.kt': 'import androidx.compose.material.Button\n@Composable fun A() {}'}, 'compose')
        self.assertEqual(1, code)
        self.assertIn('M3-001', {item['rule_id'] for item in report['findings']})

    def test_theme_literals_are_allowed(self) -> None:
        code, report = self.scan({
            'Theme.kt': 'import androidx.compose.material3.MaterialTheme\nval p = Color(0xFF6750A4)\n@Composable fun T() { MaterialTheme {} }',
            'Screen.kt': '@Composable fun S() { BoxWithConstraints {} }',
        }, 'compose')
        self.assertEqual(0, code)
        self.assertNotIn('M3-002', {item['rule_id'] for item in report['findings']})

    def test_web_mdc_and_unverified_element_block(self) -> None:
        code, report = self.scan({
            'index.html': '<!doctype html><main><md-split-button></md-split-button></main>',
            'style.css': '@media (width > 1px) { .mdc-button { color: var(--md-sys-color-primary); } }',
        }, 'web')
        self.assertEqual(1, code)
        ids = {item['rule_id'] for item in report['findings']}
        self.assertTrue({'M3-004', 'M3-010'} <= ids)

    def test_invalid_path_returns_two(self) -> None:
        error = StringIO()
        with redirect_stderr(error):
            self.assertEqual(2, m3_scan.main(['missing-path', '--format', 'json']))
        self.assertIn('path does not exist', error.getvalue())


if __name__ == '__main__':
    unittest.main()
