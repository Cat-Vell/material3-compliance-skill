# Foundations and Styles

Canonical shared guidance for tokens, theming, color, typography, shape, elevation, and motion. Platform references map this model to code.

## Token architecture

Use three layers:

1. **Primitive:** raw color, dimension, duration, or font values; keep private to the theme package.
2. **Semantic:** intent roles such as `color.primary`, `color.onSurface`, `type.bodyLarge`, `shape.medium`, and `motion.standard`.
3. **Component:** bounded aliases such as `button.filled.container`; default these from semantic roles.

Generated product UI consumes semantic/component tokens, never primitives. Align design variables and code identifiers. A component override is acceptable only when repeated product meaning justifies a token.

## Theme contract

Define before screens:

- complete static light and dark Color Schemes;
- Dynamic Color only where a platform supports it, with static fallback;
- type roles for display, headline, title, body, and label at required sizes;
- a coherent shape scale from none through full;
- elevation/surface hierarchy;
- shared motion tokens and reduced-motion alternatives.

Validate light, dark, high-contrast/product contrast settings, font scaling, and Dynamic/static paths separately. Do not infer one from another.

## Color

- Use `primary` for highest-emphasis action/selection, not every branded surface.
- Pair `primary/onPrimary`, `primaryContainer/onPrimaryContainer`, every other container/on-container pair, `surface/onSurface`, and `error/onError`.
- Use surface containers and elevation for structure before adding arbitrary outlines or colors.
- Preserve text/non-text contrast and add non-color indicators for selection, error, warning, and success.
- Treat raw color literals as allowed only in token/theme definitions, tests, generated palettes, and documented interoperability boundaries.

## Typography

- Map brand fonts onto Material roles; do not invent screen-local styles.
- Use display/headline sparingly, title for structure, body for reading, and label for controls/metadata.
- Test long translations, line height, bounded reading width, reflow, and the product's supported font scale.
- Expressive emphasized typography is `verify-current` in implementation and must serve a named editorial/emotional goal.

## Shape and elevation

- Use a small, named shape scale. Shape contrast may reinforce hierarchy; random radii may not.
- Keep touch/focus geometry valid when shapes morph or controls compress.
- Elevation communicates temporary or structural layering. Avoid stacks of competing shadows.
- In dark themes, verify surface relationships rather than assuming light-theme shadows transfer.

## Motion

- Motion explains cause/effect, navigation, continuity, or feedback.
- Tokenize duration/easing or spring parameters; do not create per-component physics.
- Keep interaction feedback prompt and never delay task completion for ornament.
- Replace large transitions, morphs, or looping decoration with instant/fade/static alternatives when reduced motion is requested.
- Treat platform Expressive motion schemes and shape morphs as `verify-current` unless the source registry says otherwise.

## Theme verification

- Search product UI for literals bypassing tokens.
- Snapshot representative light/dark surfaces and state layers.
- Check container/content role pairing and disabled readability.
- Exercise focus, press, hover, selection, error, and reduced motion.
- Confirm component themes inherit from the app boundary.
