"""Rule M3-007: text_field_ime (flutter)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-007',
    'title': 'text_field_ime',
    'dimension': 'D05',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'flutter',
    'source_id': 'S-FLUTTER',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\b(?:TextField|TextFormField)\\s*\\(',
    'remediation': 'Verify MediaQuery.viewInsets/Scaffold resizing keeps the active field and action reachable.',
}
