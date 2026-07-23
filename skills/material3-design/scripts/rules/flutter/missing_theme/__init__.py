"""Rule M3-003: missing_theme (flutter)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from m3_engine.helpers import entry_file, finding_at, matching_delimiter
from m3_engine.models import MatchContext, Rule


def check(rule: Rule, ctx: MatchContext):
    findings = []
    for path, text in ctx.texts.items():
        if path.suffix.lower() != '.dart':
            continue
        for call in re.finditer(r'\bMaterialApp(?:\.router)?\s*\(', text):
            arguments_start = text.find('(', call.start())
            arguments_end = matching_delimiter(text, arguments_start, '(', ')')
            if arguments_end is None:
                continue
            arguments = text[arguments_start + 1:arguments_end]
            if not re.search(r'\b(?:theme|darkTheme)\s*:', arguments):
                line = text.count('\n', 0, call.start()) + 1
                findings.append(
                    finding_at(rule, ctx, path, 'MaterialApp has no explicit theme or darkTheme.', line=line)
                )
    return findings



RULE = {
    'rule_id': 'M3-003',
    'title': 'missing_theme',
    'dimension': 'D01',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'flutter',
    'source_id': 'S-FLUTTER',
    'autofix': False,
    'matcher': 'whole_file',
    'remediation': 'Wire paired ThemeData/ColorScheme themes at MaterialApp.',
    'check': check,
}
