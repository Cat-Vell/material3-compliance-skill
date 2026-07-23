"""Rule M3-003: missing_theme (web)."""

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
    ui_files = [path for path in ctx.files if path.suffix.lower() in {'.html', '.htm', '.css', '.scss'}]
    if not ui_files:
        return []
    combined = '\n'.join(ctx.texts[path] for path in ui_files)
    required = {'--md-sys-color-primary', '--md-sys-color-surface', '--md-sys-color-on-surface'}
    missing = sorted(
        token for token in required if not re.search(re.escape(token) + r'\s*:', combined)
    )
    has_dark_scheme = bool(re.search(r'@media[^{}]*prefers-color-scheme\s*:\s*dark|\[[^\]]*data-theme[^\]]*dark[^\]]*\]\s*\{', combined))
    if missing or not has_dark_scheme:
        path = entry_file(ctx, {'index.html'})
        gaps = []
        if missing:
            gaps.append('missing ' + ', '.join(missing))
        if not has_dark_scheme:
            gaps.append('no dark-scheme override')
        return [finding_at(rule, ctx, path, 'Incomplete Material theme: ' + '; '.join(gaps) + '.')]
    return []



RULE = {
    'rule_id': 'M3-003',
    'title': 'missing_theme',
    'dimension': 'D01',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'web',
    'source_id': 'S-M3-WEB',
    'autofix': False,
    'matcher': 'whole_file',
    'remediation': 'Define complete light/dark semantic token schemes and consume them.',
    'check': check,
}
