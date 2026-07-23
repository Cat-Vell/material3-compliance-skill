# Recipe: Compose list-detail

## When to use

- Jetpack Compose inbox, catalog, or similar list → detail flow.
- Compact shows stacked destinations; expanded shows side-by-side panes.
- Selection and scroll position should survive resize.

## Required inputs

- List and detail content model.
- Destination / deep-link expectations.
- Compact vs expanded pane policy.

## References to read

- [layout-and-responsive.md](../shared/layout-and-responsive.md)
- [navigation-patterns.md](../shared/navigation-patterns.md)
- [interaction-and-accessibility.md](../shared/interaction-and-accessibility.md)
- [compose.md](../compose/compose.md)

## Template to adapt

- Start from [compose-core](../../assets/templates/compose-core) shell patterns; specialize into list and detail panes for the project.

## Implementation sequence

1. Define list and detail as one navigation model with clear selection ownership.
2. Compact: navigate list → detail; Expanded: show both panes with shared selection.
3. Preserve selection, scroll, and focus across resize.
4. Handle empty detail (no selection) and loading/error for each pane.
5. Wire back / predictive-back behavior for stacked compact flows.

## Required states

- Empty list, empty detail (no selection), loading, error, selected.
- Compact stacked and expanded dual-pane presentations.

## Tests to run

- Selection and pane continuity across width changes.
- Back behavior on compact detail.
- Scanner on new layout/navigation files.

## Known unsupported cases

- Device-label-only routing (“phone = list only”).
- Dropping selection on live resize.
- Claiming foldable/dual-pane behavior without window-context inputs.

## Expected output profile

Standard.

## Bound fixture

None dedicated; closest related fixture is `compose-adaptive-shell`. Prefer adding a list-detail fixture when host runs are archived.
