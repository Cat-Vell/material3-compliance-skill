"""Rule M3-004: unstable_api (flutter)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-004',
    'title': 'unstable_api',
    'dimension': 'D09',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'flutter',
    'source_id': 'S-FLUTTER-W',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '\\b(?:SplitButton|ButtonGroup|MotionScheme|LoadingIndicator)\\b',
    'remediation': 'Do not imply Compose Expressive parity; use a disclosed standard-widget fallback or remove the claim.',
}
