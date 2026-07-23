"""Rule M3-009: icon_button_label (flutter)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-009',
    'title': 'icon_button_label',
    'dimension': 'D06',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'flutter',
    'source_id': 'S-FLUTTER-W',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\bIconButton\\s*\\(',
    'remediation': 'Confirm the IconButton has a specific tooltip/semantic label and a usable target.',
}
