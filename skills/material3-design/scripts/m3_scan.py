#!/usr/bin/env python3
"""Dependency-light Material 3 heuristic evidence scanner.

This tool reports risks; it does not certify Material 3 or accessibility compliance.
Exit 0: completed without high-confidence blockers.
Exit 1: one or more high-confidence blockers.
Exit 2: invalid input/configuration.

Rule IDs M3-001..M3-011 live under scripts/rules/{compose,flutter,web}/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from m3_engine.engine import run_scan  # noqa: E402


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Collect heuristic Material 3 evidence.')
    parser.add_argument('path', help='File or directory to scan')
    parser.add_argument('--platform', choices=('compose', 'flutter', 'web', 'auto'), default='auto')
    parser.add_argument('--format', choices=('markdown', 'json'), default='markdown')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
        target = Path(args.path).resolve()
        code, output = run_scan(target, args.platform, args.format)
        print(output)
        return code
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
