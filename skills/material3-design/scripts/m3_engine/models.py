"""Shared data models for the Material 3 heuristic scanner."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
    title: str
    dimension: str
    severity: str
    confidence: str
    platform: str
    source_id: str
    autofix: bool
    matcher: str
    remediation: str
    pattern: re.Pattern[str] | None = None
    check: Callable[..., list[Finding]] | None = None
    module_dir: Path | None = None
    builtin_skip: Callable[[Path], bool] | None = None


@dataclass(frozen=True)
class MatchContext:
    files: list[Path]
    texts: dict[Path, str]
    root: Path
    platform: str


def make_finding(rule: Rule, path: Path, root: Path, line_number: int, evidence: str) -> Finding:
    text = evidence.strip()
    if len(text) > 180:
        text = text[:177] + '...'
    relative = str(path.relative_to(root) if root.is_dir() else path.name)
    return Finding(
        rule.rule_id,
        rule.dimension,
        rule.severity,
        rule.confidence,
        relative,
        line_number,
        text,
        rule.remediation,
    )


def rule_from_dict(data: dict[str, Any], module_dir: Path | None = None) -> Rule:
    matcher = data.get('matcher', 'regex')
    pattern = re.compile(data['pattern']) if matcher == 'regex' and data.get('pattern') else None
    return Rule(
        rule_id=data['rule_id'],
        title=data['title'],
        dimension=data['dimension'],
        severity=data['severity'],
        confidence=data['confidence'],
        platform=data['platform'],
        source_id=data['source_id'],
        autofix=bool(data.get('autofix', False)),
        matcher=matcher,
        remediation=data['remediation'],
        pattern=pattern,
        check=data.get('check'),
        module_dir=module_dir,
        builtin_skip=data.get('builtin_skip'),
    )
