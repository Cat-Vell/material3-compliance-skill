"""Rule M3-009: icon_button_label (compose)."""

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
        for call in re.finditer(r'\bIconButton\s*\(', text):
            arguments_start = text.find('(', call.start())
            arguments_end = matching_delimiter(text, arguments_start, '(', ')')
            if arguments_end is None:
                continue
            body_start = arguments_end + 1
            while body_start < len(text) and text[body_start].isspace():
                body_start += 1
            if body_start >= len(text) or text[body_start] != '{':
                continue
            body_end = matching_delimiter(text, body_start, '{', '}')
            if body_end is None:
                continue
            arguments = text[arguments_start + 1:arguments_end]
            if re.search(r'\bcontentDescription\s*=\s*(?!null\b)[^,\n)]+', arguments):
                continue
            body = text[body_start + 1:body_end]
            for icon in re.finditer(r'\bIcon\s*\(', body):
                icon_start = body.find('(', icon.start())
                icon_end = matching_delimiter(body, icon_start, '(', ')')
                if icon_end is None:
                    continue
                icon_arguments = body[icon_start + 1:icon_end]
                if re.search(r'\bcontentDescription\s*=\s*null\b', icon_arguments):
                    line = text.count('\n', 0, call.start()) + 1
                    findings.append(finding_at(rule, ctx, path, text.splitlines()[line - 1], line=line))
                    break
    return findings



RULE = {
    'rule_id': 'M3-009',
    'title': 'icon_button_label',
    'dimension': 'D06',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'compose',
    'source_id': 'S-COMP',
    'autofix': False,
    'matcher': 'whole_file',
    'remediation': 'Give the icon-only action a localized accessible name; null is valid only when the parent action supplies equivalent semantics.',
    'check': check,
}
