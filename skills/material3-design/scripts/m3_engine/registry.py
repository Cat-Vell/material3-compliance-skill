"""Discover and load scanner rule modules under scripts/rules/."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from .models import Rule, rule_from_dict

RULES_ROOT = Path(__file__).resolve().parent.parent / 'rules'
PLATFORMS = ('compose', 'flutter', 'web')


def _load_module(path: Path):
    module_name = f'm3_rules_{path.parent.name}_{path.parent.name}_{path.stem}_{id(path)}'
    # Stable unique name from relative path
    rel = path.relative_to(RULES_ROOT)
    module_name = 'm3_rules_' + '_'.join(rel.with_suffix('').parts)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f'cannot load rule module: {path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_rules(platform: str | None = None) -> list[Rule]:
    rules: list[Rule] = []
    platforms = (platform,) if platform in PLATFORMS else PLATFORMS
    for plat in platforms:
        plat_dir = RULES_ROOT / plat
        if not plat_dir.is_dir():
            continue
        for rule_dir in sorted(p for p in plat_dir.iterdir() if p.is_dir() and not p.name.startswith('_')):
            init_path = rule_dir / '__init__.py'
            if not init_path.is_file():
                continue
            module = _load_module(init_path)
            raw = getattr(module, 'RULE', None)
            if not isinstance(raw, dict):
                continue
            rule = rule_from_dict(raw, module_dir=rule_dir)
            if platform is None or rule.platform == platform:
                rules.append(rule)
    return rules


def all_rule_ids() -> set[str]:
    return {rule.rule_id for rule in load_rules()}


def all_dimensions() -> set[str]:
    return {rule.dimension for rule in load_rules()}
