#!/usr/bin/env python3
"""Dependency-light Material 3 heuristic evidence scanner.

This tool reports risks; it does not certify Material 3 or accessibility compliance.
Exit 0: completed without high-confidence blockers.
Exit 1: one or more high-confidence blockers.
Exit 2: invalid input/configuration.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {'.kt', '.kts', '.dart', '.html', '.htm', '.css', '.scss', '.js', '.mjs', '.ts', '.tsx', '.jsx'}
IGNORED_PARTS = {'.git', '.gradle', '.dart_tool', 'build', 'dist', 'node_modules', 'coverage'}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    dimension: str
    severity: str
    confidence: str
    file: str
    line: int
    evidence: str
    remediation: str


@dataclass(frozen=True)
class Rule:
    rule_id: str
    dimension: str
    severity: str
    confidence: str
    platforms: frozenset[str]
    pattern: re.Pattern[str]
    remediation: str


def compile_rule(rule_id: str, dimension: str, severity: str, confidence: str,
                 platforms: Iterable[str], pattern: str, remediation: str) -> Rule:
    return Rule(rule_id, dimension, severity, confidence, frozenset(platforms),
                re.compile(pattern), remediation)


RULES = [
    compile_rule('M3-001', 'D10', 'blocker', 'high', ['compose'],
                 r'import\s+androidx\.compose\.material\.(?!icons)',
                 'Migrate the usage to Material 3 or document a bounded interoperability exception.'),
    compile_rule('M3-002', 'D01', 'warning', 'medium', ['compose'],
                 r'\bColor\(0x[0-9A-Fa-f]{6,8}\)',
                 'Move the literal into a theme/token definition and consume a semantic role.'),
    compile_rule('M3-002', 'D01', 'warning', 'medium', ['flutter'],
                 r'\bColor\(0x[0-9A-Fa-f]{6,8}\)',
                 'Move the literal into ThemeData/ColorScheme or a token definition.'),
    compile_rule('M3-002', 'D01', 'warning', 'medium', ['web'],
                 r'#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\b',
                 'Move the literal into semantic CSS custom-property theme definitions.'),
    compile_rule('M3-004', 'D09', 'blocker', 'high', ['compose'],
                 r'\b(?:ButtonGroup|SplitButton|LoadingIndicator|MotionScheme|WideNavigationRail)\b',
                 'Verify the exact API and release channel in current Compose Material 3 documentation; disclose opt-in risk.'),
    compile_rule('M3-004', 'D09', 'blocker', 'high', ['flutter'],
                 r'\b(?:SplitButton|ButtonGroup|MotionScheme|LoadingIndicator)\b',
                 'Do not imply Compose Expressive parity; use a disclosed standard-widget fallback or remove the claim.'),
    compile_rule('M3-004', 'D09', 'blocker', 'high', ['web'],
                 r'<md-(?:split-button|button-group|loading-indicator|toolbar)\b',
                 'The element is not in the verified stable Web set; use an accessible fallback or verify the export.'),
    compile_rule('M3-005', 'D04', 'warning', 'high', ['compose', 'flutter'],
                 r'(?i)\b(?:isTablet|isPhone|deviceType)\b.{0,100}\b(?:NavigationBar|NavigationRail|Drawer)\b',
                 'Choose navigation from available window, destination count, posture, content, and input mode.'),
    compile_rule('M3-006', 'D05', 'warning', 'medium', ['web'],
                 r'position\s*:\s*fixed',
                 'Verify fixed UI against safe-area insets, zoom/reflow, keyboard, and obscured content.'),
    compile_rule('M3-007', 'D05', 'warning', 'medium', ['compose'],
                 r'\b(?:TextField|OutlinedTextField)\s*\(',
                 'Verify focused fields and completion actions with the IME open; add deliberate inset/scroll handling.'),
    compile_rule('M3-007', 'D05', 'warning', 'medium', ['flutter'],
                 r'\b(?:TextField|TextFormField)\s*\(',
                 'Verify MediaQuery.viewInsets/Scaffold resizing keeps the active field and action reachable.'),
    compile_rule('M3-008', 'D06', 'warning', 'medium', ['compose'],
                 r'\b(?:Box|Row|Column)\b[^\n]{0,180}\.clickable\s*\(',
                 'Prefer a Material control or add role, name, state, focus, keyboard, and target behavior.'),
    compile_rule('M3-008', 'D06', 'warning', 'high', ['web'],
                 r'<(?:div|span)[^>]+(?:onclick=|role=["\']button["\'])',
                 'Prefer a native button/link; otherwise implement the complete keyboard and focus contract.'),
    compile_rule('M3-009', 'D06', 'warning', 'medium', ['flutter'],
                 r'\bIconButton\s*\(',
                 'Confirm the IconButton has a specific tooltip/semantic label and a usable target.'),
    compile_rule('M3-009', 'D06', 'warning', 'medium', ['compose'],
                 r'IconButton\s*\([^)]{0,300}contentDescription\s*=\s*null',
                 'Give an icon-only action a localized accessible name; null is only valid with an adjacent label.'),
    compile_rule('M3-010', 'D10', 'blocker', 'high', ['web'],
                 r'(?:from\s+["\']@material/(?!web)|@use\s+["\']@material/|class=["\'][^"\']*\bmdc-|\.mdc-[\w-]+)',
                 'Replace deprecated MDC usage with a verified Material Web element or accessible native/custom fallback.'),
]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Collect heuristic Material 3 evidence.')
    parser.add_argument('path', help='File or directory to scan')
    parser.add_argument('--platform', choices=('compose', 'flutter', 'web', 'auto'), default='auto')
    parser.add_argument('--format', choices=('markdown', 'json'), default='markdown')
    return parser.parse_args(argv)


def source_files(target: Path) -> list[Path]:
    candidates = [target] if target.is_file() else target.rglob('*')
    return sorted(p for p in candidates if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES
                  and not any(part in IGNORED_PARTS for part in p.parts))


def detect_platform(files: list[Path], texts: dict[Path, str]) -> str | None:
    scores = {'compose': 0, 'flutter': 0, 'web': 0}
    for path in files:
        suffix = path.suffix.lower()
        text = texts[path]
        if suffix in {'.kt', '.kts'}:
            scores['compose'] += 3
        if suffix == '.dart':
            scores['flutter'] += 3
        if suffix in {'.html', '.htm', '.css', '.scss', '.js', '.mjs', '.ts', '.tsx', '.jsx'}:
            scores['web'] += 2
        if 'androidx.compose' in text:
            scores['compose'] += 4
        if 'package:flutter/' in text:
            scores['flutter'] += 4
        if '<!doctype html' in text.lower() or '--md-sys-' in text:
            scores['web'] += 4
    winner = max(scores, key=scores.get)
    return winner if scores[winner] else None


def allowed_literal_file(path: Path) -> bool:
    stem = path.stem.lower()
    return any(word in stem or word in {part.lower() for part in path.parts}
               for word in ('theme', 'token', 'color', 'palette', 'baseline', 'test'))


def add_match(findings: list[Finding], rule: Rule, path: Path, root: Path,
              line_number: int, line: str) -> None:
    evidence = line.strip()
    if len(evidence) > 180:
        evidence = evidence[:177] + '...'
    findings.append(Finding(rule.rule_id, rule.dimension, rule.severity, rule.confidence,
                            str(path.relative_to(root) if root.is_dir() else path.name),
                            line_number, evidence, rule.remediation))


def scan(files: list[Path], texts: dict[Path, str], root: Path, platform: str) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        for number, line in enumerate(texts[path].splitlines(), start=1):
            for rule in RULES:
                if platform not in rule.platforms or not rule.pattern.search(line):
                    continue
                if rule.rule_id == 'M3-002' and allowed_literal_file(path):
                    continue
                add_match(findings, rule, path, root, number, line)

    combined = '\n'.join(texts.values())
    entry_files = [p for p in files if p.name in {'MainActivity.kt', 'main.dart', 'index.html'}]
    if platform == 'compose' and 'setContent' in combined and not re.search(r'\b(?:MaterialTheme|\w+Theme)\s*\(', combined):
        p = entry_files[0] if entry_files else files[0]
        findings.append(Finding('M3-003', 'D01', 'blocker', 'high', str(p.relative_to(root)), 1,
                                'Compose entry point found without a theme boundary.',
                                'Wrap emitted Material UI in the app MaterialTheme with complete schemes/type/shapes.'))
    if platform == 'flutter' and 'MaterialApp' in combined and not re.search(r'\b(?:theme|darkTheme|colorScheme)\s*:', combined):
        p = entry_files[0] if entry_files else files[0]
        findings.append(Finding('M3-003', 'D01', 'blocker', 'high', str(p.relative_to(root)), 1,
                                'MaterialApp found without an explicit theme/color scheme.',
                                'Wire paired ThemeData/ColorScheme themes at MaterialApp.'))
    if platform == 'web' and any(p.suffix.lower() in {'.html', '.css'} for p in files) and '--md-sys-color-' not in combined:
        p = entry_files[0] if entry_files else files[0]
        findings.append(Finding('M3-003', 'D01', 'warning', 'medium', str(p.relative_to(root)), 1,
                                'Web UI found without Material semantic color custom properties.',
                                'Define complete light/dark semantic token schemes and consume them.'))

    responsive_markers = {
        'compose': r'BoxWithConstraints|currentWindowAdaptiveInfo|WindowSizeClass|NavigationSuiteScaffold',
        'flutter': r'LayoutBuilder|MediaQuery|OrientationBuilder',
        'web': r'@media|@container|container-type',
    }
    if not re.search(responsive_markers[platform], combined):
        p = entry_files[0] if entry_files else files[0]
        findings.append(Finding('M3-011', 'D05', 'warning', 'medium', str(p.relative_to(root)), 1,
                                'No recognized responsive/adaptive strategy found.',
                                'Document and implement content-driven window behavior; verify resize continuity.'))

    return sorted(findings, key=lambda item: (item.file, item.line, item.rule_id))


def render_markdown(platform: str, files: int, findings: list[Finding]) -> str:
    lines = [
        '# Material 3 heuristic scan', '',
        f'- Platform: `{platform}`', f'- Files scanned: {files}',
        f'- Findings: {len(findings)}',
        '- Scope: heuristic evidence collection; not a compliance certificate', '',
    ]
    if not findings:
        lines.append('No configured risks detected.')
        return '\n'.join(lines)
    lines.extend(['| Rule | Dimension | Severity | Confidence | Evidence | Remediation |',
                  '|---|---|---|---|---|---|'])
    for item in findings:
        evidence = f'`{item.file}:{item.line}` — {item.evidence}'.replace('|', '\\|')
        remediation = item.remediation.replace('|', '\\|')
        lines.append(f'| {item.rule_id} | {item.dimension} | {item.severity} | {item.confidence} | {evidence} | {remediation} |')
    return '\n'.join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
        target = Path(args.path).resolve()
        if not target.exists():
            raise ValueError(f'path does not exist: {target}')
        files = source_files(target)
        if not files:
            raise ValueError('no supported source files found')
        texts: dict[Path, str] = {}
        for path in files:
            try:
                texts[path] = path.read_text(encoding='utf-8')
            except UnicodeDecodeError as exc:
                raise ValueError(f'invalid UTF-8: {path}') from exc
        platform = detect_platform(files, texts) if args.platform == 'auto' else args.platform
        if platform is None:
            raise ValueError('could not infer platform; pass --platform')
        root = target if target.is_dir() else target.parent
        findings = scan(files, texts, root, platform)
        if args.format == 'json':
            print(json.dumps({
                'platform': platform,
                'files_scanned': len(files),
                'certificate': False,
                'findings': [asdict(item) for item in findings],
            }, indent=2))
        else:
            print(render_markdown(platform, len(files), findings))
        return 1 if any(f.severity == 'blocker' and f.confidence == 'high' for f in findings) else 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
