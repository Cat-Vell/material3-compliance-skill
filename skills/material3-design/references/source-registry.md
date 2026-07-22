# Source Registry

Last registry review: **2026-07-22**. Status describes what this skill may claim, not the lifetime status of a product. Re-check volatile entries before release or when a project uses a newer baseline.

| ID | Platform | Topic | Official URL | Skill status | Last verified |
|---|---|---|---|---|---|
| S-M3 | shared | Material 3 system | https://m3.material.io/ | supported | 2026-07-22 |
| S-M3-COMP | shared | component semantics | https://m3.material.io/components | supported | 2026-07-22 |
| S-M3-WEB | web | official Web entry | https://m3.material.io/develop/web | verify-current | 2026-07-22 |
| S-COMP | compose | component catalog | https://developer.android.com/develop/ui/compose/components | supported | 2026-07-22 |
| S-COMP-M3 | compose | theme and Material 3 | https://developer.android.com/develop/ui/compose/designsystems/material3 | supported | 2026-07-22 |
| S-COMP-REL | compose | Material 3 releases/API stability | https://developer.android.com/jetpack/androidx/releases/compose-material3 | verify-current | 2026-07-22 |
| S-COMP-BOM | compose | tested dependency set | https://developer.android.com/develop/ui/compose/bom | verify-current | 2026-07-22 |
| S-AGP | compose | Android Gradle Plugin baseline | https://developer.android.com/build/releases/about-agp | verify-current | 2026-07-22 |
| S-KOTLIN | compose | Kotlin baseline | https://kotlinlang.org/docs/releases.html | verify-current | 2026-07-22 |
| S-ADAPT | compose | adaptive apps | https://developer.android.com/develop/adaptive-apps | supported | 2026-07-22 |
| S-NAV3 | compose | Navigation 3 | https://developer.android.com/guide/navigation/navigation-3 | verify-current | 2026-07-22 |
| S-INSETS | compose | Material 3 insets | https://developer.android.com/develop/ui/compose/system/material-insets | supported | 2026-07-22 |
| S-MIG-COMP | compose | M2 to M3 | https://developer.android.com/develop/ui/compose/designsystems/material2-material3 | supported | 2026-07-22 |
| S-FLUTTER | flutter | Material Design | https://docs.flutter.dev/ui/design/material | supported | 2026-07-22 |
| S-FLUTTER-W | flutter | official widget catalog | https://docs.flutter.dev/ui/widgets/material | supported | 2026-07-22 |
| S-FLUTTER-MIG | flutter | M3 migration | https://docs.flutter.dev/release/breaking-changes/material-3-migration | verify-current | 2026-07-22 |
| S-FLUTTER-REL | flutter | stable SDK releases | https://docs.flutter.dev/release/release-notes | verify-current | 2026-07-22 |
| S-WEB-REPO | web | `@material/web` elements/status | https://github.com/material-components/material-web | verify-current | 2026-07-22 |
| S-WEB-A11Y | web | WAI-ARIA authoring patterns | https://www.w3.org/WAI/ARIA/apg/ | supported | 2026-07-22 |
| S-WEB-WCAG | web | Web Content Accessibility Guidelines | https://www.w3.org/TR/WCAG22/ | supported | 2026-07-22 |
| S-NODE | web | Node tested runtime line | https://nodejs.org/en/about/previous-releases | verify-current | 2026-07-22 |

## Verified support snapshot

- **Compose:** stable Material 3 components and theming are supported. The stable Material 3 line observed on 2026-07-22 was 1.4.0; newer 1.5 work was alpha. Verify every Expressive or experimental symbol through `S-COMP-REL`.
- **Flutter:** Material 3 is the default in current documentation; several M2 widgets still require explicit replacement. Treat complete Expressive equivalence as unsupported unless an official widget/API is verified.
- **Web:** `@material/web` provides a bounded M3 web-component set, while its official repository states maintenance mode pending maintainers. Use only exported elements verified in `S-WEB-REPO`; otherwise use an accessible native/custom fallback. Refuse full Expressive parity.

## Status vocabulary

- `supported`: a stable, first-party implementation or design pattern is available.
- `verify-current`: the API, release channel, export, or maintenance state is volatile; check before emitting code.
- `custom fallback`: no verified official component covers the job; implement accessible behavior from native HTML/platform primitives and shared tokens.
- `refuse`: the requested parity or platform claim cannot be made honestly.
