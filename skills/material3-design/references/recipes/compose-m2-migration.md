# Recipe: Compose M2 → M3 migration

## When to use

- Existing Jetpack Compose (or View + Compose) codebase still on Material 2 imports/theme.
- A staged vertical slice is preferred over a big-bang rewrite.

## Required inputs

- Inventory of M2 imports, theme, and navigation consumers.
- Existing UI tests to preserve behavior.
- Rollback boundary agreed with the project.

## References to read

- [migrations.md](../shared/migrations.md)
- [foundations-and-styles.md](../shared/foundations-and-styles.md)
- [component-catalog.md](../shared/component-catalog.md)
- [compose.md](../compose/compose.md)
- [source-registry.md](../shared/source-registry.md)

## Template to adapt

- Use [compose-core](../../assets/templates/compose-core) only as a target-shape reference for the M3 theme/shell slice; do not replace the whole app architecture.

## Implementation sequence

1. Inventory M2 imports, theme, and navigation; declare the bridge and rollback boundary.
2. Map theme roles to M3 ColorScheme / Typography / Shapes.
3. Migrate one vertical slice; review component semantics (not import-only replacement).
4. Search remaining M2 consumers; keep interoperability exceptions explicit.
5. Update tests; run scanner before/after; refuse undocumented leftover consumers as “done.”

## Required states

- Pre-migration and post-migration behavior for the migrated slice.
- Interop paths for unmigrated consumers, if any.

## Tests to run

- Existing UI tests for the migrated slice.
- Scanner before/after on the migration surface.
- Explicit search for remaining M2 imports.

## Known unsupported cases

- Migration as import rename only.
- Claiming visual identity of all defaults.
- Completing while undocumented M2 consumers remain.
- Unverified API replacements.

## Expected output profile

Evidence.

## Bound fixture

`evals/fixtures/04-compose-m2-migration.json` (`compose-m2-migration`).
