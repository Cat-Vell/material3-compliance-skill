"""Rule M3-006: fixed_position (web)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-006',
    'title': 'fixed_position',
    'dimension': 'D05',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'web',
    'source_id': 'S-WEB-A11Y',
    'autofix': False,
    'matcher': 'regex',
    'pattern': 'position\\s*:\\s*fixed',
    'remediation': 'Verify fixed UI against safe-area insets, zoom/reflow, keyboard, and obscured content.',
}
