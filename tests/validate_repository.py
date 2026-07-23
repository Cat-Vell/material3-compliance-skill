from __future__ import annotations

import json
import re
import sys
from datetime import date as current_date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'material3-design'
REFERENCES = SKILL / 'references'
TEMPLATES = SKILL / 'assets' / 'templates'

REQUIRED_FILES = [
    ROOT / 'README.md', ROOT / 'LICENSE', ROOT / 'NOTICE.md', ROOT / 'CONTRIBUTING.md',
    ROOT / 'CHANGELOG.md', ROOT / 'RELEASE_CHECKLIST.md', ROOT / 'docs' / 'MATURITY-ROADMAP.md',
    ROOT / 'docs' / 'CAPABILITY-MATRIX.md', ROOT / 'docs' / 'EVALUATION-EVIDENCE.md',
    ROOT / 'docs' / 'RELEASE-EVIDENCE-CHAIN.md', ROOT / 'docs' / 'FIRST-COMMIT-INVENTORY.md',
    ROOT / 'docs' / 'evidence' / 'README.md', ROOT / 'docs' / 'evidence' / 'local-verification.md',
    ROOT / 'docs' / 'evidence' / 'hosted-ci.md', ROOT / 'docs' / 'evidence' / 'fresh-install.md',
    ROOT / 'docs' / 'evidence' / 'templates' / 'README.md',
    ROOT / 'docs' / 'evidence' / 'templates' / 'run-record.example.json',
    ROOT / '.github' / 'workflows' / 'ci.yml', ROOT / '.github' / 'dependabot.yml',
    ROOT / '.claude-plugin' / 'plugin.json', ROOT / '.claude-plugin' / 'marketplace.json',
    ROOT / 'evals' / 'README.md', ROOT / 'evals' / 'run-record.schema.json',
    ROOT / 'evals' / 'generate_run_matrix.py', ROOT / 'evals' / 'benchmark_report.py',
    ROOT / 'evals' / 'trigger' / 'cases.json', ROOT / 'evals' / 'trigger' / 'score_trigger_runs.py',
    ROOT / 'BENCHMARK.md', ROOT / 'benchmark.json',
    ROOT / 'tests' / 'validate_fixtures.py', ROOT / 'tests' / 'validate_eval_runs.py',
    ROOT / 'tests' / 'test_eval_run_validator.py',
    ROOT / 'tests' / 'test_m3_scan.py', SKILL / 'SKILL.md', SKILL / 'agents' / 'openai.yaml',
    SKILL / 'scripts' / 'm3_scan.py',
]

REFERENCE_FILES = [
    'audit/audit-framework.md',
    'compose/compose.md',
    'flutter/flutter.md',
    'recipes/compose-adaptive-app-shell.md',
    'recipes/compose-form.md',
    'recipes/compose-list-detail.md',
    'recipes/compose-m2-migration.md',
    'recipes/compose-theme.md',
    'shared/component-catalog.md',
    'shared/content-ownership.md',
    'shared/foundations-and-styles.md',
    'shared/interaction-and-accessibility.md',
    'shared/layout-and-responsive.md',
    'shared/material3-design-system.md',
    'shared/migrations.md',
    'shared/navigation-patterns.md',
    'shared/source-registry.md',
    'web/web.md',
]

TEMPLATE_FILES = {
    'compose-core': [
        'README.md', 'baseline.json', 'settings.gradle.kts', 'build.gradle.kts', 'gradle.properties',
        'app/build.gradle.kts', 'app/src/main/AndroidManifest.xml',
        'app/src/main/java/dev/material3/core/MainActivity.kt',
        'app/src/main/java/dev/material3/core/Theme.kt',
        'app/src/main/java/dev/material3/core/App.kt',
        'app/src/main/java/dev/material3/core/Motion.kt',
        'app/src/test/java/dev/material3/core/AppStateTest.kt',
    ],
    'flutter-core': [
        'README.md', 'baseline.json', 'pubspec.yaml', 'pubspec.lock', 'analysis_options.yaml',
        'lib/app_theme.dart', 'lib/main.dart', 'test/widget_test.dart',
    ],
    'web-core': [
        'README.md', 'baseline.json', 'package.json', 'package-lock.json',
        'scripts/build.mjs', 'scripts/a11y-smoke.mjs', 'src/index.html',
        'src/app.js', 'src/tokens.css', 'test/build.test.mjs',
    ],
}


def slugify(heading: str) -> str:
    value = heading.strip().lower()
    value = re.sub(r'[^\w\s-]', '', value, flags=re.UNICODE)
    return re.sub(r'\s+', '-', value)


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob('*.md') if '.git' not in path.parts)


def heading_slugs(text: str) -> set[str]:
    return {slugify(match.group(1)) for match in re.finditer(r'^#{1,6}\s+(.+)$', text, flags=re.MULTILINE)}


def validate_files_and_utf8(errors: list[str]) -> None:
    for name in REFERENCE_FILES:
        REQUIRED_FILES.append(REFERENCES / name)
    for template, names in TEMPLATE_FILES.items():
        REQUIRED_FILES.extend(TEMPLATES / template / name for name in names)
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f'missing required file: {path.relative_to(ROOT)}')
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
            continue
        if path.suffix.lower() in {'.md', '.py', '.json', '.yaml', '.yml', '.kt', '.kts', '.dart', '.html', '.xml', '.css', '.js', '.mjs'} or path.name in {'gradle.properties'}:
            try:
                path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                errors.append(f'invalid UTF-8: {path.relative_to(ROOT)}')


def validate_frontmatter(errors: list[str]) -> None:
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', text, flags=re.DOTALL)
    if not match:
        errors.append('SKILL.md is missing YAML frontmatter')
        return
    keys = [m.group(1) for m in re.finditer(r'^([a-zA-Z][\w-]*):', match.group(1), flags=re.MULTILINE)]
    if keys != ['name', 'description']:
        errors.append(f'SKILL.md frontmatter keys must be name, description only: {keys}')
    if not re.search(r'^name:\s+material3-design\s*$', match.group(1), flags=re.MULTILINE):
        errors.append('SKILL.md name must be material3-design')
    lines = text.splitlines()
    if len(lines) >= 180:
        errors.append(f'SKILL.md must stay below 180 lines, found {len(lines)}')
    for phrase in ('### Design', '### Build', '### Audit', 'Platform: [Compose | Flutter | Web]',
                   'API status: [stable | verify-current | unsupported/custom]', 'D01`–`D10',
                   'Use `U` for missing evidence', 'M3 Compliance'):
        if phrase not in text:
            errors.append(f'missing runtime contract phrase: {phrase}')


def validate_markdown(errors: list[str]) -> None:
    link_pattern = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
    for path in markdown_files():
        text = path.read_text(encoding='utf-8')
        if sum(1 for line in text.splitlines() if line.startswith('```')) % 2:
            errors.append(f'unbalanced code fences: {path.relative_to(ROOT)}')
        for target in link_pattern.findall(text):
            if target.startswith(('http://', 'https://', 'mailto:')):
                continue
            local_target, separator, anchor = target.partition('#')
            resolved = (path.parent / local_target).resolve() if local_target else path.resolve()
            if not resolved.exists():
                errors.append(f'missing local link {target} in {path.relative_to(ROOT)}')
                continue
            if separator and resolved.suffix.lower() == '.md':
                if anchor not in heading_slugs(resolved.read_text(encoding='utf-8')):
                    errors.append(f'missing anchor #{anchor} for {target} in {path.relative_to(ROOT)}')


def validate_sources(errors: list[str]) -> None:
    text = (REFERENCES / 'shared' / 'source-registry.md').read_text(encoding='utf-8')
    rows = re.findall(r'^\| (S-[A-Z0-9-]+) \| ([^|]+) \| ([^|]+) \| (https://[^ ]+) \| ([^|]+) \| (\d{4}-\d{2}-\d{2}) \|$', text, flags=re.MULTILINE)
    ids = [row[0] for row in rows]
    if len(rows) < 15:
        errors.append(f'source registry must contain at least 15 structured sources, found {len(rows)}')
    if len(ids) != len(set(ids)):
        errors.append('source registry IDs must be unique')
    allowed = {'supported', 'verify-current', 'custom fallback', 'refuse'}
    for source_id, _platform, _topic, url, status, date in rows:
        if status.strip() not in allowed:
            errors.append(f'{source_id}: invalid support status {status.strip()}')
        if date > current_date.today().isoformat():
            errors.append(f'{source_id}: future verification date {date}')
        if not any(host in url for host in ('m3.material.io', 'developer.android.com', 'docs.flutter.dev', 'github.com/material-components/material-web', 'w3.org', 'kotlinlang.org', 'nodejs.org')):
            errors.append(f'{source_id}: source is not in the first-party allowlist: {url}')


def validate_catalog(errors: list[str]) -> None:
    text = (REFERENCES / 'shared' / 'component-catalog.md').read_text(encoding='utf-8')
    rows = re.findall(r'^\| C(\d{2}) ([^\n]+)$', text, flags=re.MULTILINE)
    numbers = [int(number) for number, _ in rows]
    if numbers != list(range(1, 39)):
        errors.append(f'catalog IDs must be C01-C38 in order: {numbers}')
    for number, row in rows:
        if row.count('|') < 8:
            errors.append(f'C{number}: incomplete catalog schema columns')
        if '2026-07-22' not in row or ' · ' not in row:
            errors.append(f'C{number}: missing source/recipe/verification metadata')
        if not any(f' {status} ' in row or f' {status} |' in row for status in ('S', 'V', 'F', 'R')):
            errors.append(f'C{number}: missing platform support status')


def validate_audit_and_scanner(errors: list[str]) -> None:
    audit = (REFERENCES / 'audit' / 'audit-framework.md').read_text(encoding='utf-8')
    dimensions = re.findall(r'^### (D\d{2})\.', audit, flags=re.MULTILINE)
    expected = [f'D{number:02d}' for number in range(1, 11)]
    if dimensions != expected:
        errors.append(f'audit dimension IDs must be D01-D10: {dimensions}')
    for phrase in ('Unknown is not compliant', 'a written reason is mandatory', '## 4. Release gates',
                   '**Coverage:**', '### Must-fix', '### Nice-to-have'):
        if phrase.lower() not in audit.lower():
            errors.append(f'missing audit contract phrase: {phrase}')
    rules_root = SKILL / 'scripts' / 'rules'
    scanner_text = '\n'.join(
        path.read_text(encoding='utf-8')
        for path in sorted(rules_root.rglob('__init__.py'))
        if path.parent.name not in {'_shared', 'compose', 'flutter', 'web', 'rules'}
    )
    scanner_text += (SKILL / 'scripts' / 'm3_scan.py').read_text(encoding='utf-8')
    for number in range(1, 12):
        rule = f'M3-{number:03d}'
        if rule not in scanner_text:
            errors.append(f'missing scanner rule ID: {rule}')
    for dimension in ('D01', 'D04', 'D05', 'D06', 'D09', 'D10'):
        if dimension not in scanner_text:
            errors.append(f'scanner does not reference audit dimension: {dimension}')
    if not (SKILL / 'scripts' / 'm3_engine' / 'engine.py').is_file():
        errors.append('missing scanner engine package scripts/m3_engine/engine.py')


def validate_templates_and_metadata(errors: list[str]) -> None:
    for template in TEMPLATE_FILES:
        baseline_path = TEMPLATES / template / 'baseline.json'
        if baseline_path.exists():
            baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
            if not baseline.get('release_verification_required'):
                errors.append(f'{template}: baseline must require release verification')
            if 'latest' in baseline.get('label', '').lower():
                errors.append(f'{template}: baseline label must not claim latest')
    claude_paths = (ROOT / '.claude-plugin' / 'plugin.json', ROOT / '.claude-plugin' / 'marketplace.json')
    for path in claude_paths:
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f'invalid Claude metadata {path.name}: {exc}')
    try:
        plugin = json.loads(claude_paths[0].read_text(encoding='utf-8'))
        marketplace = json.loads(claude_paths[1].read_text(encoding='utf-8'))
        entries = marketplace.get('plugins', [])
        if plugin.get('name') != 'material3-design':
            errors.append('Claude plugin name must be material3-design')
        if len(entries) != 1 or entries[0].get('name') != 'material3-design':
            errors.append('Claude marketplace must contain exactly the material3-design entry')
        elif (
            entries[0].get('source') != './'
            or entries[0].get('strict') is not False
            or entries[0].get('skills') != ['./skills/material3-design']
        ):
            errors.append('Claude marketplace source/strict/skills mapping is invalid')
        if plugin.get('version') and entries and entries[0].get('version'):
            errors.append('Claude version must not be duplicated in plugin and marketplace metadata')
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        errors.append(f'cannot validate Claude metadata contract: {exc}')
    try:
        json.loads((ROOT / 'evals' / 'run-record.schema.json').read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f'invalid behavior run-record schema: {exc}')
    metadata = (SKILL / 'agents' / 'openai.yaml').read_text(encoding='utf-8')
    if '$material3-design' not in metadata or 'Build + Audit' not in metadata:
        errors.append('agents/openai.yaml must match the Build + Audit runtime skill')


def validate_ci_security(errors: list[str]) -> None:
    workflow = (ROOT / '.github' / 'workflows' / 'ci.yml').read_text(encoding='utf-8')
    action_refs = re.findall(r'^\s*- uses:\s+([^@\s]+)@([^\s#]+)', workflow, flags=re.MULTILINE)
    if not action_refs:
        errors.append('CI workflow must contain action references')
    for action, ref in action_refs:
        if not re.fullmatch(r'[0-9a-f]{40}', ref):
            errors.append(f'CI action must use a full commit SHA: {action}@{ref}')


def main() -> int:
    errors: list[str] = []
    validate_files_and_utf8(errors)
    if not errors:
        validate_frontmatter(errors)
        validate_markdown(errors)
        validate_sources(errors)
        validate_catalog(errors)
        validate_audit_and_scanner(errors)
        validate_templates_and_metadata(errors)
        validate_ci_security(errors)
    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return 1
    print('Repository validation passed.')
    print('Validated portable skill contract, 38 component families, D01-D10, scanner rules, sources, fixtures, templates, and metadata.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
