"""Rule M3-005: device_nav (compose)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-005',
    'title': 'device_nav',
    'dimension': 'D04',
    'severity': 'warning',
    'confidence': 'high',
    'platform': 'compose',
    'source_id': 'S-ADAPT',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '(?i)\\b(?:isTablet|isPhone|deviceType)\\b.{0,100}\\b(?:NavigationBar|NavigationRail|Drawer)\\b',
    'remediation': 'Choose navigation from available window, destination count, posture, content, and input mode.',
}
