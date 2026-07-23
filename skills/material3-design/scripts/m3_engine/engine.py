"""Core scan pipeline: discovery, rule application, rendering."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import Finding, MatchContext, Rule, make_finding
from .registry import load_rules
from .suppressions import (
    config_suppresses,
    file_level_suppressions,
    line_suppressions,
    load_config_suppressions,
)

TEXT_SUFFIXES = {'.kt', '.kts', '.dart', '.html', '.htm', '.css', '.scss', '.js', '.mjs', '.ts', '.tsx', '.jsx'}
IGNORED_PARTS = {'.git', '.gradle', '.dart_tool', 'build', 'dist', 'node_modules', 'coverage'}


def source_files(target: Path) -> list[Path]:
    candidates = [target] if target.is_file() else target.rglob('*')
    return sorted(
        p for p in candidates
        if p.is_file()
        and p.suffix.lower() in TEXT_SUFFIXES
        and not any(part in IGNORED_PARTS for part in p.parts)
    )


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


def _relative(path: Path, root: Path) -> str:
    return str(path.relative_to(root) if root.is_dir() else path.name)


def _is_suppressed(
    rule: Rule,
    path: Path,
    root: Path,
    file_ids: set[str],
    line_ids: set[str],
    config_items,
) -> bool:
    if rule.rule_id in file_ids or rule.rule_id in line_ids:
        return True
    if rule.builtin_skip and rule.builtin_skip(path):
        return True
    return config_suppresses(config_items, rule.rule_id, _relative(path, root))


def scan(files: list[Path], texts: dict[Path, str], root: Path, platform: str) -> tuple[list[Finding], int]:
    rules = [rule for rule in load_rules(platform) if rule.platform == platform]
    config_items = load_config_suppressions(root)
    findings: list[Finding] = []
    suppressed_count = 0
    regex_rules = [rule for rule in rules if rule.matcher == 'regex' and rule.pattern is not None]
    whole_rules = [rule for rule in rules if rule.matcher == 'whole_file' and rule.check is not None]

    for path in files:
        text = texts[path]
        lines = text.splitlines()
        file_ids = file_level_suppressions(text)
        for number, line in enumerate(lines, start=1):
            line_ids = line_suppressions(lines, number - 1)
            for rule in regex_rules:
                if not rule.pattern.search(line):
                    continue
                if _is_suppressed(rule, path, root, file_ids, line_ids, config_items):
                    suppressed_count += 1
                    continue
                findings.append(make_finding(rule, path, root, number, line))

    ctx = MatchContext(files=files, texts=texts, root=root, platform=platform)
    for rule in whole_rules:
        # whole-file suppressions: file-level or config on primary evidence file
        for candidate in rule.check(rule, ctx):
            path = root / candidate.file if (root / candidate.file).exists() else None
            if path is None:
                # Finding already has relative path; try resolve
                path = next((p for p in files if _relative(p, root) == candidate.file), files[0])
            candidate_text = texts.get(path, '')
            candidate_lines = candidate_text.splitlines()
            file_ids = file_level_suppressions(candidate_text)
            line_ids = (
                line_suppressions(candidate_lines, candidate.line - 1)
                if 1 <= candidate.line <= len(candidate_lines)
                else set()
            )
            if _is_suppressed(rule, path, root, file_ids, line_ids, config_items):
                suppressed_count += 1
                continue
            findings.append(candidate)

    findings = sorted(findings, key=lambda item: (item.file, item.line, item.rule_id))
    return findings, suppressed_count


def render_markdown(platform: str, files: int, findings: list[Finding], suppressed_count: int = 0) -> str:
    lines = [
        '# Material 3 heuristic scan', '',
        f'- Platform: `{platform}`', f'- Files scanned: {files}',
        f'- Findings: {len(findings)}',
        f'- Suppressed: {suppressed_count}',
        '- Scope: heuristic evidence collection; not a compliance certificate', '',
    ]
    if not findings:
        lines.append('No configured risks detected.')
        return '\n'.join(lines)
    lines.extend([
        '| Rule | Dimension | Severity | Confidence | Evidence | Remediation |',
        '|---|---|---|---|---|---|',
    ])
    for item in findings:
        evidence = f'`{item.file}:{item.line}` — {item.evidence}'.replace('|', '\\|')
        remediation = item.remediation.replace('|', '\\|')
        lines.append(
            f'| {item.rule_id} | {item.dimension} | {item.severity} | {item.confidence} | {evidence} | {remediation} |'
        )
    return '\n'.join(lines)


def run_scan(target: Path, platform: str, output_format: str) -> tuple[int, str]:
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
    resolved_platform = detect_platform(files, texts) if platform == 'auto' else platform
    if resolved_platform is None:
        raise ValueError('could not infer platform; pass --platform')
    root = target if target.is_dir() else target.parent
    findings, suppressed_count = scan(files, texts, root, resolved_platform)
    if output_format == 'json':
        payload = {
            'platform': resolved_platform,
            'files_scanned': len(files),
            'certificate': False,
            'suppressed_count': suppressed_count,
            'findings': [asdict(item) for item in findings],
        }
        text = json.dumps(payload, indent=2)
    else:
        text = render_markdown(resolved_platform, len(files), findings, suppressed_count)
    code = 1 if any(f.severity == 'blocker' and f.confidence == 'high' for f in findings) else 0
    return code, text
