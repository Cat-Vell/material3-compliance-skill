"""Rule M3-008: non_semantic_clickable (compose)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-008',
    'title': 'non_semantic_clickable',
    'dimension': 'D06',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'compose',
    'source_id': 'S-COMP',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\b(?:Box|Row|Column)\\b[^\\n]{0,180}\\.clickable\\s*\\(',
    'remediation': 'Prefer a Material control or add role, name, state, focus, keyboard, and target behavior.',
}
