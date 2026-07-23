"""Shared helpers for whole-file scanner rules."""

from __future__ import annotations

from pathlib import Path

from .models import Finding, MatchContext, Rule, make_finding


def entry_file(ctx: MatchContext, names: set[str]) -> Path:
    for path in ctx.files:
        if path.name in names:
            return path
    return ctx.files[0]


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int | None:
    """Return the matching delimiter while ignoring comments and quoted strings."""
    if start < 0 or start >= len(text) or text[start] != opening:
        return None
    depth = 0
    index = start
    while index < len(text):
        if text.startswith('//', index):
            newline = text.find('\n', index + 2)
            index = len(text) if newline < 0 else newline + 1
            continue
        if text.startswith('/*', index):
            end = text.find('*/', index + 2)
            index = len(text) if end < 0 else end + 2
            continue
        if text.startswith('"""', index):
            end = text.find('"""', index + 3)
            index = len(text) if end < 0 else end + 3
            continue
        if text[index] in {'"', "'"}:
            quote = text[index]
            index += 1
            while index < len(text):
                if text[index] == '\\':
                    index += 2
                    continue
                if text[index] == quote:
                    index += 1
                    break
                index += 1
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def theme_literal_allowed(path: Path) -> bool:
    stem = path.stem.lower()
    parts = {part.lower() for part in path.parts}
    return any(word in stem or word in parts for word in ('theme', 'token', 'color', 'palette', 'baseline', 'test'))


def finding_at(rule: Rule, ctx: MatchContext, path: Path, evidence: str, line: int = 1) -> Finding:
    return make_finding(rule, path, ctx.root, line, evidence)
