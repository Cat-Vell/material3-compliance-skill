"""Rule M3-010: deprecated_mdc (web)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-010',
    'title': 'deprecated_mdc',
    'dimension': 'D10',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'web',
    'source_id': 'S-WEB-REPO',
    'autofix': False,
    'matcher': 'regex',
    'pattern': '(?:from\\s+["\\\']@material/(?!web)|@use\\s+["\\\']@material/|class=["\\\'][^"\\\']*\\bmdc-|\\.mdc-[\\w-]+)',
    'remediation': 'Replace deprecated MDC usage with a verified Material Web element or accessible native/custom fallback.',
}
