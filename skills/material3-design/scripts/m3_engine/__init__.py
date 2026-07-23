"""Material 3 heuristic evidence scanner engine package."""

from .engine import detect_platform, run_scan, scan, source_files
from .models import Finding, Rule
from .registry import all_dimensions, all_rule_ids, load_rules

__all__ = [
    'Finding',
    'Rule',
    'all_dimensions',
    'all_rule_ids',
    'detect_platform',
    'load_rules',
    'run_scan',
    'scan',
    'source_files',
]
