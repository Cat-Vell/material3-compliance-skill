"""Suppression parsing for inline, file-level, and project config ignores."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path


INLINE_RE = re.compile(r'm3-ignore:\s*([A-Z0-9_,\-\s]+)', re.IGNORECASE)
FILE_RE = re.compile(r'm3-ignore-file:\s*([A-Z0-9_,\-\s]+)', re.IGNORECASE)
RULE_TOKEN_RE = re.compile(r'M3-\d{3}', re.IGNORECASE)


@dataclass(frozen=True)
class ConfigSuppression:
    rule_id: str
    path_glob: str
    reason: str = ''


def parse_rule_ids(blob: str) -> set[str]:
    return {token.upper() for token in RULE_TOKEN_RE.findall(blob)}


def file_level_suppressions(text: str) -> set[str]:
    ids: set[str] = set()
    for line in text.splitlines()[:40]:
        match = FILE_RE.search(line)
        if match:
            ids |= parse_rule_ids(match.group(1))
    return ids


def line_suppressions(lines: list[str], index: int) -> set[str]:
    """Return rule IDs suppressed for lines[index] (0-based)."""
    ids: set[str] = set()
    inline = INLINE_RE.search(lines[index])
    if inline:
        ids |= parse_rule_ids(inline.group(1))
    if index > 0:
        previous = INLINE_RE.search(lines[index - 1])
        if previous:
            ids |= parse_rule_ids(previous.group(1))
    return ids


def load_config_suppressions(root: Path) -> list[ConfigSuppression]:
    candidates = []
    if root.is_dir():
        candidates.append(root / '.m3scan.json')
    else:
        candidates.append(root.parent / '.m3scan.json')
    for config_path in candidates:
        if not config_path.is_file():
            continue
        try:
            data = json.loads(config_path.read_text(encoding='utf-8'))
        except OSError as exc:
            raise ValueError(f'cannot read suppression config {config_path}: {exc}') from exc
        except json.JSONDecodeError as exc:
            raise ValueError(
                f'invalid suppression config JSON {config_path}:{exc.lineno}:{exc.colno}: {exc.msg}'
            ) from exc
        if not isinstance(data, dict):
            raise ValueError(f'suppression config must be a JSON object: {config_path}')
        raw_items = data.get('suppress', [])
        if not isinstance(raw_items, list):
            raise ValueError(f'suppression config "suppress" must be an array: {config_path}')
        items: list[ConfigSuppression] = []
        for index, entry in enumerate(raw_items):
            if not isinstance(entry, dict):
                raise ValueError(f'suppression config entry {index} must be an object: {config_path}')
            rule_id = entry.get('rule_id', '')
            path_glob = entry.get('path', '**/*')
            reason = entry.get('reason', '')
            if not isinstance(rule_id, str) or not RULE_TOKEN_RE.fullmatch(rule_id):
                raise ValueError(
                    f'suppression config entry {index} has invalid rule_id {rule_id!r}: {config_path}'
                )
            if not isinstance(path_glob, str) or not path_glob:
                raise ValueError(f'suppression config entry {index} has invalid path: {config_path}')
            if not isinstance(reason, str):
                raise ValueError(f'suppression config entry {index} has non-string reason: {config_path}')
            items.append(ConfigSuppression(rule_id.upper(), path_glob, reason))
        return items
    return []


def config_suppresses(items: list[ConfigSuppression], rule_id: str, relative_path: str) -> bool:
    normalized = relative_path.replace('\\', '/')
    name = Path(normalized).name
    for item in items:
        if item.rule_id != rule_id.upper():
            continue
        pattern = item.path_glob.replace('\\', '/')
        if fnmatch(normalized, pattern) or fnmatch(name, pattern):
            return True
        if not pattern.startswith('**/') and fnmatch(normalized, '**/' + pattern):
            return True
    return False
