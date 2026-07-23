"""Rule M3-003: missing_theme (compose)."""

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
        if path.suffix.lower() not in {'.kt', '.kts'}:
            continue
        for call in re.finditer(r'\bsetContent\s*(?=[({])', text):
            if re.search(r'\bfun\s*$', text[max(0, call.start() - 12):call.start()]):
                continue
            cursor = call.end()
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            end = None
            if cursor < len(text) and text[cursor] == '(':
                end = matching_delimiter(text, cursor, '(', ')')
                if end is not None:
                    trailing = end + 1
                    while trailing < len(text) and text[trailing].isspace():
                        trailing += 1
                    if trailing < len(text) and text[trailing] == '{':
                        trailing_end = matching_delimiter(text, trailing, '{', '}')
                        end = trailing_end if trailing_end is not None else end
            elif cursor < len(text) and text[cursor] == '{':
                end = matching_delimiter(text, cursor, '{', '}')
            if end is None:
                continue
            invocation = text[call.start():end + 1]
            if not re.search(r'\b(?:MaterialTheme|[A-Z]\w*Theme)\s*[\({]', invocation):
                line = text.count('\n', 0, call.start()) + 1
                findings.append(finding_at(rule, ctx, path, 'Compose setContent has no theme boundary.', line=line))
    return findings



RULE = {
    'rule_id': 'M3-003',
    'title': 'missing_theme',
    'dimension': 'D01',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'compose',
    'source_id': 'S-COMP-M3',
    'autofix': False,
    'matcher': 'whole_file',
    'remediation': 'Wrap emitted Material UI in the app MaterialTheme with complete schemes/type/shapes.',
    'check': check,
}
