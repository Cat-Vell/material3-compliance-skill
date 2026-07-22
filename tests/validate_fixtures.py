from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'evals' / 'fixtures'
FIELDS = {
    'id', 'mode', 'platform', 'task', 'input_evidence', 'required_assertions',
    'critical_assertion_indexes', 'forbidden_claims', 'required_files', 'dimensions', 'expected_unknown',
    'expected_na', 'expected_release_gates', 'evidence_requirements',
    'severity_requirements',
}
VALID_DIMENSIONS = {f'D{number:02d}' for number in range(1, 11)}


def main() -> int:
    errors: list[str] = []
    files = sorted(FIXTURES.glob('*.json'))
    if len(files) != 12:
        errors.append(f'expected 12 fixtures, found {len(files)}')

    ids: set[str] = set()
    counts: Counter[tuple[str, str]] = Counter()
    for path in files:
        try:
            fixture = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f'{path.name}: {exc}')
            continue
        missing = FIELDS - fixture.keys()
        if missing:
            errors.append(f'{path.name}: missing {sorted(missing)}')
        fixture_id = fixture.get('id')
        if fixture_id in ids:
            errors.append(f'{path.name}: duplicate id {fixture_id}')
        ids.add(fixture_id)
        counts[(fixture.get('mode'), fixture.get('platform'))] += 1
        unknown_dimensions = set(fixture.get('dimensions', [])) - VALID_DIMENSIONS
        if unknown_dimensions:
            errors.append(f'{path.name}: invalid dimensions {sorted(unknown_dimensions)}')
        if not fixture.get('required_assertions') or not fixture.get('forbidden_claims'):
            errors.append(f'{path.name}: assertions and forbidden claims are required')
        critical = fixture.get('critical_assertion_indexes', [])
        assertion_count = len(fixture.get('required_assertions', []))
        if not critical:
            errors.append(f'{path.name}: at least one critical assertion is required')
        if (
            not isinstance(critical, list)
            or any(not isinstance(index, int) or isinstance(index, bool) for index in critical)
            or critical != sorted(set(critical))
            or any(index < 0 or index >= assertion_count for index in critical)
        ):
            errors.append(f'{path.name}: critical assertion indexes must be unique, sorted, and in range')

    required_counts = {
        ('build', 'compose'): 4,
        ('build', 'flutter'): 2,
        ('build', 'web'): 2,
        ('audit', 'compose'): 1,
        ('audit', 'flutter'): 1,
        ('audit', 'web'): 1,
        ('design-build', 'compose'): 1,
    }
    for key, expected in required_counts.items():
        if counts[key] != expected:
            errors.append(f'expected {expected} {key} fixtures, found {counts[key]}')

    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return 1
    print('Behavior fixture validation passed (12 fixtures).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
