# Recipe: Compose accessible form

## When to use

- Jetpack Compose sign-up, settings, or similar multi-field form.
- Validation, async submit, and accessible error recovery are required.

## Required inputs

- Field list and validation rules.
- Async submit / loading behavior.
- Target accessibility expectations (TalkBack, keyboard, IME).

## References to read

- [interaction-and-accessibility.md](../shared/interaction-and-accessibility.md)
- [component-catalog.md](../shared/component-catalog.md) for TextField / Button jobs
- [compose.md](../compose/compose.md)
- [layout-and-responsive.md](../shared/layout-and-responsive.md) for IME / insets

## Template to adapt

- No dedicated form template; adapt TextField / Button patterns from [compose-core](../../assets/templates/compose-core) and project conventions.

## Implementation sequence

1. Hoist form state so it is restorable across configuration and process death as needed.
2. Use persistent labels; never treat placeholder as the accessible name.
3. Provide recovery text for errors; avoid color-only validation.
4. Prevent duplicate submit while loading; expose loading/error/success transitions.
5. Specify focus order and IME actions; add semantics tests for errors.

## Required states

- Enabled, disabled, focused, error, loading, success.
- Keyboard and TalkBack completable paths.

## Tests to run

- Compose UI or state tests covering error semantics and submit gating.
- Scanner on form files when available.

## Known unsupported cases

- Placeholder-as-label.
- Color-only validation cues.
- “Disabled” used instead of an accessible explanation of why submit is blocked.

## Expected output profile

Lite for a single-field tweak; Standard for a full form surface.

## Bound fixture

`evals/fixtures/02-compose-form.json` (`compose-accessible-form`).
