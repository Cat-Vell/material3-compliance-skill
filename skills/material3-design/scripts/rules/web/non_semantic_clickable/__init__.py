"""Rule M3-008: non_semantic_clickable (web)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-008',
    'title': 'non_semantic_clickable',
    'dimension': 'D06',
    'severity': 'warning',
    'confidence': 'high',
    'platform': 'web',
    'source_id': 'S-WEB-A11Y',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '<(?:div|span)[^>]+(?:onclick=|role=["\\\']button["\\\'])',
    'remediation': 'Prefer a native button/link; otherwise implement the complete keyboard and focus contract.',
}
