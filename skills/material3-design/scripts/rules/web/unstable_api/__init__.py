"""Rule M3-004: unstable_api (web)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-004',
    'title': 'unstable_api',
    'dimension': 'D09',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'web',
    'source_id': 'S-WEB-REPO',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '<md-(?:split-button|button-group|loading-indicator|toolbar)\\b',
    'remediation': 'The element is not in the verified stable Web set; use an accessible fallback or verify the export.',
}
