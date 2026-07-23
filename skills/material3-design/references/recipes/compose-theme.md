# Recipe: Compose theme

## When to use

- Jetpack Compose project needs Material 3 ColorScheme, Typography, and Shapes.
- Brand seed or existing version catalog is available.
- Light and dark static schemes are required; Dynamic Color may be optional.

## Required inputs

- Platform confirmed as Compose.
- Brand seed or existing color roles.
- Target Compose BOM / dependency source (or permission to verify current).

## References to read

- [foundations-and-styles.md](../shared/foundations-and-styles.md)
- [compose.md](../compose/compose.md)
- [source-registry.md](../shared/source-registry.md)

## Template to adapt

- [assets/templates/compose-core](../../assets/templates/compose-core) — `Theme.kt` and related tests.

## Implementation sequence

1. Map brand seed to semantic roles; keep primitives inside token definitions.
2. Ship paired light and dark static ColorSchemes.
3. Wire Typography and Shapes before screen overrides.
4. Gate Dynamic Color to Android 12+ and keep the static fallback path.
5. Add a theme verification test or explicit project check.

## Required states

- Light and dark schemes applied.
- Dynamic Color on / off with static fallback.
- Container/content role pairing for primary surfaces.

## Tests to run

- Theme unit or Compose UI check for light/dark/dynamic/fallback paths.
- `python scripts/m3_scan.py <path> --platform compose --format markdown` when files exist.

## Known unsupported cases

- Invented “latest” BOM versions.
- Claiming Dynamic Color on every Android version.
- Unverified Expressive APIs in the stable theme path.

## Expected output profile

Standard (Evidence if shipping experimental/Expressive theme APIs).

## Bound fixture

`evals/fixtures/01-compose-theme.json` (`compose-theme`).
