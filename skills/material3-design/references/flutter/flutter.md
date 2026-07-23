# Flutter Material 3 Recipes

Production-focused secondary support. Use official framework widgets and the shared component semantics. Reusable baseline: [flutter-core](../../assets/templates/flutter-core/README.md).

## Support policy

- Material 3 is the default in current Flutter documentation, but migration may require new widgets rather than restyling old ones.
- Treat official stable framework widgets as `supported`; check current API docs before using a symbol absent from the project's SDK.
- Do not promise Compose Expressive parity. Button groups, split buttons, expressive loading/motion, and other gaps use a disclosed custom fallback or are refused.
- Do not recommend a community dependency without explicit verification and disclosure.

## Theme (`F-THEME`)

Create paired schemes from the same seed/brand intent and wire both at `MaterialApp`:

```dart
final lightScheme = ColorScheme.fromSeed(
  seedColor: const Color(0xff6750a4),
  brightness: Brightness.light,
);
final darkScheme = ColorScheme.fromSeed(
  seedColor: const Color(0xff6750a4),
  brightness: Brightness.dark,
);

MaterialApp(
  theme: ThemeData(colorScheme: lightScheme, useMaterial3: true),
  darkTheme: ThemeData(colorScheme: darkScheme, useMaterial3: true),
  themeMode: ThemeMode.system,
)
```

Extend with `textTheme`, component themes, and consistent shapes/elevation. Keep raw colors inside theme/token definitions. Flutter does not provide Android wallpaper Dynamic Color as a framework-equivalent cross-platform guarantee; implement only with an explicitly verified platform strategy and retain static schemes.

## State and forms (`F-FORMS`, `F-SEARCH`)

- Own controllers/focus nodes in a `State` object or the app's established state architecture and dispose them.
- Use `Form`/`TextFormField`, persistent labels, validation and recovery text, autofill/input types, and guarded async submit.
- Represent loading/content/empty/error explicitly; keep retries and user input.
- Use `Semantics` only to add/fix meaning; avoid duplicating semantics already supplied by Material widgets.
- Use `FocusTraversalGroup`/policies when visual and source order diverge; verify keyboard and screen-reader behavior.

## Component recipes

| Recipe | Catalog IDs | Approach |
|---|---|---|
| F-ACTIONS | C01–C04 | official button and FAB constructors; explicit labels and hierarchy |
| F-SELECTION | C05, C21–C25 | segmented/checkbox/radio/switch/slider/chip widgets; labeled groups |
| F-FEEDBACK | C08–C12 | `Badge`, progress widgets, `ScaffoldMessenger`, `Tooltip` |
| F-CONTAIN | C13–C17 | card/dialog/sheet/divider; explicit focus, dismissal, safe destructive defaults |
| F-COLLECTION | C18, C36–C37 | `ListView`/`GridView`; stable keys, state restoration, full data states |
| F-MENUS | C26 | menu widgets with current selection, keyboard/dismissal |
| F-PICKERS | C27–C28 | official picker functions; locale/manual entry/invalid values |
| F-NAV | C29–C33 | app bars, `NavigationBar`, rail, drawer from IA/window context |
| F-TABS | C34 | `TabBar` for peer sections, not top-level destinations |
| F-SCAFFOLD | C38 | `Scaffold`, `SafeArea` only where needed, coordinated transient UI |
| F-ADAPT | C16, C38 | `LayoutBuilder`/`MediaQuery` plus content-driven breakpoints and preserved state |
| F-FALLBACK | C06–C07, C10, C35 | compose from standard widgets only when semantics/keyboard/state are fully specified |

## Adaptive shell (`F-ADAPT`, `F-SCAFFOLD`)

- Use available constraints, not a `phone/tablet` label.
- Keep one destination model and swap navigation presentation without recreating page state.
- Use a bounded single-pane form, adaptive grid, list-detail, or supporting region according to content.
- Respect `MediaQuery.viewInsets` for IME and `SafeArea`/view padding without double-padding.
- Test narrow landscape, split window, large text, keyboard traversal, and live resize on supported desktop/web targets.

## Migration

Follow [migrations.md](../shared/migrations.md). Pay particular attention to manual replacements such as old bottom navigation with `NavigationBar`, theme defaults, typography/color-role changes, and visual regressions caused by mixing old/new widgets. Run `dart fix` only after reviewing changes and never treat it as semantic verification.

## Verification

- Run `dart format --set-exit-if-changed .`, `flutter analyze`, and `flutter test`.
- Widget-test theme mode, validation/error recovery, semantics labels, navigation selection, and adaptive breakpoints.
- Add golden tests only if the project already maintains stable fonts/rendering baselines.
- Report the actual Flutter SDK used; label bundled versions as tested baselines, not latest.
