"""Rule M3-007: text_field_ime (compose)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-007',
    'title': 'text_field_ime',
    'dimension': 'D05',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'compose',
    'source_id': 'S-INSETS',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\b(?:TextField|OutlinedTextField)\\s*\\(',
    'remediation': 'Verify focused fields and completion actions with the IME open; add deliberate inset/scroll handling.',
}
