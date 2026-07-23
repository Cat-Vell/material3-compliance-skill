"""Rule M3-004: unstable_api (compose)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-004',
    'title': 'unstable_api',
    'dimension': 'D09',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'compose',
    'source_id': 'S-COMP-REL',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\b(?:ButtonGroup|SplitButton|LoadingIndicator|MotionScheme|WideNavigationRail)\\b',
    'remediation': 'Verify the exact API and release channel in current Compose Material 3 documentation; disclose opt-in risk.',
}
