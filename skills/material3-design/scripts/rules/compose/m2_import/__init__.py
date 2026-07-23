"""Rule M3-001: m2_import (compose)."""

from __future__ import annotations

RULE = {
    'rule_id': 'M3-001',
    'title': 'm2_import',
    'dimension': 'D10',
    'severity': 'blocker',
    'confidence': 'high',
    'platform': 'compose',
    'source_id': 'S-MIG-COMP',
    'autofix': False,
    'matcher': 'regex',
    'pattern': 'import\\s+androidx\\.compose\\.material\\.(?!icons)',
    'remediation': 'Migrate the usage to Material 3 or document a bounded interoperability exception.',
}
