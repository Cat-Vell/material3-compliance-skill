# Material 3 Migrations

Use for `migrate` tasks. Migration is a behavior/theme/test change, not a mechanical rename.

## Shared sequence

1. Inventory dependencies, theme boundaries, component usages, navigation, custom components, screenshots/tests, and accessibility behavior.
2. Run `m3_scan.py` and classify findings; confirm false positives manually.
3. Define complete M3 light/dark tokens and component priority before swapping widgets.
4. Create an interoperability boundary so old/new code can coexist without duplicated token sources.
5. Migrate one vertical slice: theme → shell/navigation → components/states → tests.
6. Compare hierarchy, labels, semantics, focus, keyboard, targets, insets, loading/error/empty behavior, and adaptive layout.
7. Remove bridges and old dependencies only after repository search and tests show no consumers.

## Compose M2 to M3

- Replace `androidx.compose.material.*` with `androidx.compose.material3.*` deliberately; alias imports during coexistence.
- Map `MaterialTheme.colors` to `colorScheme`, M2 typography to M3 type roles, and shapes to the M3 scale.
- Review renamed/new component APIs, parameter/default changes, and state objects. Do not mass-replace symbols blindly.
- Ensure one `MaterialTheme` governs a subtree. Bridge custom design-system tokens explicitly.
- Rework bottom navigation, app bars, text fields, buttons/FABs, dialogs/sheets, and ripples based on semantics and current stable APIs.
- Re-test edge-to-edge/insets, Dynamic/static theme paths, navigation/back, semantics, and screenshots.

## Flutter older Material to M3

- Confirm M3 default behavior for the project's Flutter SDK; keep `useMaterial3: true` explicit only when it improves migration clarity.
- Build `ColorScheme`/`TextTheme`/component themes before visual comparison.
- Replace components requiring new implementations (for example, legacy bottom navigation to `NavigationBar`) using `S-FLUTTER-MIG`.
- Review changed defaults for color, elevation, typography, shape, padding, and state layers.
- Run format/analyze/tests and inspect all supported platforms and theme modes.

## Web MDC to Material 3

- Inventory legacy `@material/*` MDC JavaScript/Sass and imperative lifecycle code.
- For each component, choose verified `@material/web`, semantic native HTML, accessible custom fallback, or removal. Record the support status.
- Replace Sass theme globals/literals with semantic CSS custom properties and complete light/dark schemes.
- Expect different DOM/events/form association/custom-element upgrade behavior; adapt integration and tests.
- Remove MDC initialization/destroy code only when no component uses it.
- Verify keyboard/focus, forms, SSR/hydration, zoom/reflow, reduced motion, and accessibility.

## Migration delivery

Report inventory, slice completed, compatibility bridge, intentional visual/behavior changes, unsupported gaps, remaining old consumers, tests/checks, rollback boundary, and M3 Compliance. Never claim migration complete while old imports/widgets remain unless they are documented interoperability exceptions.
