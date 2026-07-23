"""Rule M3-011: missing_responsive (flutter)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from m3_engine.helpers import entry_file, finding_at, matching_delimiter
from m3_engine.models import MatchContext, Rule


def check(rule: Rule, ctx: MatchContext):
    combined = '\n'.join(ctx.texts.values())
    if not re.search(r'LayoutBuilder|MediaQuery|OrientationBuilder', combined):
        path = entry_file(ctx, {'MainActivity.kt', 'main.dart', 'index.html'})
        return [finding_at(rule, ctx, path, 'No recognized responsive/adaptive strategy found.')]
    return []



RULE = {
    'rule_id': 'M3-011',
    'title': 'missing_responsive',
    'dimension': 'D05',
    'severity': 'warning',
    'confidence': 'medium',
    'platform': 'flutter',
    'source_id': 'S-FLUTTER',
    'autofix': False,
    'matcher': 'whole_file',
    'remediation': 'Document and implement content-driven window behavior; verify resize continuity.',
    'check': check,
}
