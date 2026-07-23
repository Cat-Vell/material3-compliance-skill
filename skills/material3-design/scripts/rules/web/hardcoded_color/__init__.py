"""Rule M3-002: hardcoded_color (web)."""

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
    'platform': 'web',
    'source_id': 'S-M3-WEB',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\\b',
    'remediation': 'Move the literal into semantic CSS custom-property theme definitions.',
    'builtin_skip': theme_literal_allowed,
}
