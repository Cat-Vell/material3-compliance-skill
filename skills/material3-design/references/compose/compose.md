# Jetpack Compose Recipes

Primary/full-depth implementation guide. Read shared semantics in [component-catalog.md](../shared/component-catalog.md) and source status in [source-registry.md](../shared/source-registry.md). The reusable stable baseline is [compose-core](../../assets/templates/compose-core/README.md).

## API policy

- Use the project version catalog or BOM; never replace it merely because this skill has a newer tested baseline.
- Stable Material 3 first. Check `S-COMP-REL` for every experimental/Expressive symbol and disclose `@OptIn` plus compatibility risk.
- Navigation 3 is production-stable in the source snapshot but still `verify-current` for project integration: inspect its release, migration, state model, and existing navigation architecture before replacing Navigation 2.
- Keep alpha/experimental recipes out of the stable core template.

## Theme recipe (`C-THEME`)

At the app boundary provide complete `lightColorScheme` and `darkColorScheme`, project `Typography`, and `Shapes`. Dynamic Color is optional on Android 12+ and always falls back to the static schemes.

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {
    val context = LocalContext.current
    val colors = when {
        dynamicColor && Build.VERSION.SDK_INT >= 31 && darkTheme -> dynamicDarkColorScheme(context)
        dynamicColor && Build.VERSION.SDK_INT >= 31 -> dynamicLightColorScheme(context)
        darkTheme -> AppDarkColors
        else -> AppLightColors
    }
    MaterialTheme(colors, AppTypography, AppShapes, content)
}
```

Keep literals in token files. Verify light, dark, Dynamic light/dark, and Dynamic-disabled fallback. Tokenize motion outside `MaterialTheme` when the project needs a shared scheme; provide reduced/no-motion behavior based on an app accessibility setting or verified platform signal.

## State, forms, and data (`C-FORMS`, `C-SEARCH`)

- Hoist durable state to the lowest common owner; use `rememberSaveable` for restorable UI state and a state holder/ViewModel for business state.
- Prefer immutable screen state representing `loading`, `content`, `empty`, and `error`; preserve last useful content for recoverable refresh errors when appropriate.
- Use persistent labels, keyboard options/actions, visual error text, and semantics. Announce validation/status deliberately; do not repeatedly interrupt TalkBack.
- Disable or debounce duplicate submission while retaining progress and cancellation/retry behavior.
- Move focus using `FocusRequester` only for a user-benefiting transition; keep traversal logical and test it.

## Component recipes

| Recipe | Catalog IDs | Stable approach |
|---|---|---|
| C-ACTIONS | C01–C04 | Material 3 button/FAB families; hoisted callbacks/state; labeled icon semantics |
| C-SELECTION | C05, C21–C25 | standard selection composables; whole-row semantics; values announced |
| C-FEEDBACK | C08–C12 | `SnackbarHost`, badges, progress, stable tooltip variant; truthful status |
| C-CONTAIN | C13–C17 | cards/dialogs/sheets/dividers; explicit modal focus/back and state restoration |
| C-COLLECTION | C18, C36–C37 | lazy list/grid, stable keys, bounded adaptive cell width, complete data states |
| C-MENUS | C26 | menus with selected state, keyboard/focus return, dismissal |
| C-PICKERS | C27–C28 | current picker APIs only after checking experimental annotations |
| C-NAV | C29–C33 | app bars, bar/rail/drawer selected from IA and window context |
| C-TABS | C34 | current tab-row API; peer sections only; selection saved |
| C-SCAFFOLD | C38 | consume `Scaffold` padding once; coordinate FAB/snackbar/insets |
| C-EXPRESSIVE | C06–C07, C10, C35 | `verify-current`; implement only from checked release/API docs |

## Adaptive shell (`C-ADAPT`, `C-SCAFFOLD`)

Use current window/adaptive information as changing state. Choose feed, list-detail, supporting pane, or focused form from content relationships. `NavigationSuiteScaffold` is appropriate only when its bar/rail calculation matches the information architecture; an explicit drawer/layout type needs a reason.

- Preserve destination ID, selected item, input, scroll, expansion, and focus across pane-count changes.
- Use current Material 3 Adaptive canonical scaffolds when verified against the project dependencies.
- Avoid placing critical content across a hinge; support tabletop/short-height and pointer/keyboard contexts.
- Consume `Scaffold` padding/insets once. Account for system bars, cutouts, gestures, and IME; do not stack safe-area padding blindly.
- Predictive back preview and committed destination must agree. Verify sheet/dialog/drawer dismissal before destination pop.

## Navigation status

Model destinations independently of bar/rail/drawer UI. Existing Navigation 2 projects can remain on a supported architecture; do not migrate solely for novelty. For Navigation 3:

1. verify current stable artifact/API in `S-NAV3`;
2. map back-stack ownership, saved state, deep links, predictive back, and testing;
3. migrate one coherent graph boundary at a time;
4. keep interoperability explicit until the old boundary is removed.

## Insets, IME, and edge-to-edge

Material 3 components may handle their own insets, while `Scaffold` passes content padding for content to consume. Inspect each container before adding modifiers. Test gesture and three-button navigation, compact landscape, IME-open forms, modal surfaces, and transient bars. The focused field and completion action must remain reachable.

## M2 interoperability and migration

Follow [migrations.md](../shared/migrations.md). During staged migration, alias Material 2 and 3 imports, keep one design-token source, bridge theme values deliberately, and avoid nesting conflicting theme boundaries accidentally. Replace component semantics and tests, not only imports. Remove the bridge when no M2 consumer remains.

## Testing

- Unit-test reducers/state holders for validation and loading/error/empty transitions.
- Compose UI-test accessible names, state descriptions, selection, error text, click/keyboard actions, modal dismissal, and focus when APIs allow.
- Test compact/medium/expanded composition and state continuity with controlled window inputs.
- Screenshot representative light/dark/static/Dynamic paths where the project supports screenshot testing.
- Run `m3_scan.py`; manually validate findings.

## Delivery gate

Report dependency source/date, stable versus opt-in APIs, files changed, state ownership, accessibility semantics, adaptive/inset behavior, and tests run. Do not claim build success unless the actual project or bundled template built.
