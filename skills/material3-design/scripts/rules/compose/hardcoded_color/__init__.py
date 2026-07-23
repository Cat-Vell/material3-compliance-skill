"""Rule M3-002: hardcoded_color (compose)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from m3_engine.helpers import theme_literal_allowed

RULE = {
    'rule_id': 'M3-002',
    'title': 'hardcoded_color',
    'dimension': 'D01',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'compose',
    'source_id': 'S-COMP-M3',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\bColor\\(0x[0-9A-Fa-f]{6,8}\\)',
    'remediation': 'Move the literal into a theme/token definition and consume a semantic role.',
    'builtin_skip': theme_literal_allowed,
}
