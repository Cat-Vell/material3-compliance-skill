# Contributing

Contributions should improve both Build and Audit behavior while keeping the runtime context lean and platform claims verifiable.

## Canonical ownership

Change facts in their owner first:

| Change | Owner |
|---|---|
| Runtime routing/output | `skills/material3-design/SKILL.md` |
| Source/API status | `references/source-registry.md` |
| Shared theme/style semantics | `references/foundations-and-styles.md` |
| State/accessibility semantics | `references/interaction-and-accessibility.md` |
| Component jobs/mappings | `references/component-catalog.md` |
| Platform code recipes | `references/compose.md`, `flutter.md`, or `web.md` |
| Audit IDs/scoring/gates | `references/audit-framework.md` |
| Scanner rules | `scripts/m3_scan.py` plus unit tests |

Follow [content-ownership.md](skills/material3-design/references/content-ownership.md); do not duplicate a canonical fact in multiple references.

## Source policy

- Use first-party sources for volatile APIs and support status.
- Update the source registry verification date and affected catalog rows in the same change.
- Label stable, verify-current, custom fallback, or refuse explicitly.
- Never call a dependency “latest”; template versions are tested baselines only after green build evidence.
- Do not copy third-party skill prose or examples.
- During unreleased Claude-plugin development, omit an explicit version so Git SHA identifies updates. For a release, set SemVer in `.claude-plugin/plugin.json` only, bump it for every release, and do not duplicate it in the marketplace entry.

## Runtime constraints

- Keep `SKILL.md` under 180 lines with frontmatter keys only `name` and `description`.
- Keep detailed material in directly linked references.
- Preserve `material3-design` as the skill/folder name.
- Keep repository documentation outside the runtime skill package.

## Required checks

```bash
python -m unittest discover -s tests -p "test_*.py"
python tests/validate_fixtures.py
python tests/validate_repository.py
```

Also build/test every affected template. If the installed skill-creator package is available, run its `quick_validate.py` against `skills/material3-design` as an additional official skill check.

Changes to behavior contracts require a fixture update or a written reason. Release claims require the thresholds in [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and the ordered links in [docs/RELEASE-EVIDENCE-CHAIN.md](docs/RELEASE-EVIDENCE-CHAIN.md); a docs-only baseline must not be tagged. Update the matching ledger under `docs/evidence/` when local, hosted-CI, or install evidence changes.
