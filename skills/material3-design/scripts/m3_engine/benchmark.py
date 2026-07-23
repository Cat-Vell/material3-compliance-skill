"""Aggregate scanner fixture metrics into a single benchmark table."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from m3_engine.registry import load_rules


def aggregate() -> list[dict]:
    rows = []
    for rule in sorted(load_rules(), key=lambda item: (item.platform, item.rule_id, item.title)):
        metrics = json.loads((rule.module_dir / 'metrics.json').read_text(encoding='utf-8'))
        rows.append({
            'rule_id': rule.rule_id,
            'title': rule.title,
            'platform': rule.platform,
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'fixtures': metrics['fixture_count'],
            'source_id': rule.source_id,
        })
    return rows


def render_markdown(rows: list[dict]) -> str:
    lines = [
        '| Rule | Platform | Title | Precision | Recall | Fixtures | Source |',
        '|---|---|---|---:|---:|---:|---|',
    ]
    for row in rows:
        lines.append(
            f"| {row['rule_id']} | {row['platform']} | {row['title']} | "
            f"{row['precision']:.2f} | {row['recall']:.2f} | {row['fixtures']} | {row['source_id']} |"
        )
    return '\n'.join(lines)


def main() -> int:
    rows = aggregate()
    print(render_markdown(rows))
    print()
    print(f'Rules: {len(rows)} | Mean precision: {sum(r["precision"] for r in rows) / len(rows):.2f} | '
          f'Mean recall: {sum(r["recall"] for r in rows) / len(rows):.2f}')
    print('Scope: scanner fixture benchmark only; not a host-behavior or accessibility certificate.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
