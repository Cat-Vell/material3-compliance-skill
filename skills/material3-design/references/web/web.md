# Material 3 Web Recipes

Limited and honest support. Use M3 tokens, verified `@material/web` elements, and accessible native/custom fallbacks. Reusable baseline: [web-core](../../assets/templates/web-core/README.md).

## Support and refusal policy

- Check `S-WEB-REPO` for an actual exported element before importing it. Package maintenance status and exports are volatile.
- Prefer semantic HTML and platform behavior when no verified element exists.
- Custom components must implement the applicable WAI-ARIA pattern, keyboard interaction, focus management, form behavior, and states—not merely M3 styling.
- Refuse requests for complete M3 or M3 Expressive Web parity. State which parts are tokens, official elements, custom fallbacks, or unsupported.

## Tokens and schemes (`W-THEME`)

Define semantic CSS custom properties and switch values by user/system choice:

```css
:root {
  color-scheme: light dark;
  --md-sys-color-primary: #6750a4;
  --md-sys-color-on-primary: #ffffff;
  --md-sys-color-surface: #fffbfe;
  --md-sys-color-on-surface: #1c1b1f;
  --md-sys-shape-medium: 0.75rem;
  --md-sys-motion-standard: 180ms cubic-bezier(.2, 0, 0, 1);
}
@media (prefers-color-scheme: dark) {
  :root { /* complete dark role remap */ }
}
@media (prefers-reduced-motion: reduce) {
  :root { --md-sys-motion-standard: 1ms linear; }
}
```

Ship complete schemes, not the abbreviated example. Let users override system choice and persist without a flash of incorrect theme; set an early server/client attribute when appropriate. Never infer Android Dynamic Color support on the Web.

## Element and fallback recipes

| Recipe | Catalog IDs | Approach |
|---|---|---|
| W-ACTIONS | C01–C04 | verified `md-*button`/FAB elements; native `<button>` fallback |
| W-SELECTION | C05, C21–C25 | verified checkbox/radio/switch/slider; native fields; ARIA group patterns |
| W-FEEDBACK | C08–C12 | verified progress/tooltip where exported; restrained live regions; status fallback |
| W-CONTAIN | C13–C17 | semantic containers; verified dialog or native `<dialog>` with focus/return testing |
| W-COLLECTION | C18, C36–C37 | semantic list/grid DOM, stable reading order; carousel only with full keyboard controls |
| W-MENUS | C26 | verified menu or WAI-ARIA menu only for commands; native select for value selection |
| W-PICKERS | C27–C28 | native date/time inputs where suitable; disclose browser/localization variance |
| W-NAV | C29–C33 | landmarks and lists; responsive presentation without changing destination meaning |
| W-TABS | C34 | verified tabs or WAI-ARIA tabs with linked panels and arrow keys |
| W-SCAFFOLD | C38 | header/nav/main/aside/footer landmarks plus CSS layout/container queries |
| W-ADAPT | C16, C38 | container/media queries from content constraints; preserve DOM/state/focus |
| W-FALLBACK | C06–C07, C10, C35 | accessible standard controls or refuse unsupported Expressive behavior |

## Responsive and container behavior

- Use container queries for reusable regions and media queries for viewport/user preferences.
- Bound reading width; recompose columns/panes instead of stretching.
- Keep DOM and focus order logical. Avoid CSS visual reordering that contradicts keyboard/screen-reader order.
- Reserve space for fixed bars, safe-area environment insets when relevant, zoom/reflow, virtual keyboard, and sticky controls.
- Preserve URL, selected destination/item, form state, scroll intent, and focus across resize/hydration.

## Accessibility and SSR

- Use native labels, fieldsets/legends, headings, landmarks, and form submission first.
- Add ARIA only when native semantics are insufficient; no ARIA is better than incorrect ARIA.
- Modal/menu/tab fallbacks implement the complete documented keyboard/focus pattern.
- Custom elements may upgrade after HTML parse: provide useful fallback/labels, avoid hiding unupgraded content, and test hydration/SSR mismatch.
- Avoid announcing every loading tick. Use `role=status`/live regions for meaningful changes and preserve focus.

## MDC migration

Follow [migrations.md](../shared/migrations.md). Remove legacy `@material/*` MDC packages component by component; do not assume `@material/web` has a replacement. Preserve behavior with native/custom fallbacks, replace old Sass theme variables with semantic custom properties, and test SSR/forms/keyboard/focus.

## Verification

- Clean install from the lockfile, build, unit/component tests, keyboard checks, and automated accessibility smoke test.
- Manually verify screen reader, forced colors/high contrast where supported, 200% zoom/reflow, reduced motion, light/dark, and no-JS/upgrade behavior in scope.
- Report each official element import plus source/date. Automated scans are not WCAG certification.
