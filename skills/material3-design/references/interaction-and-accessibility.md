# Interaction and Accessibility

Canonical shared guidance for state, semantics, focus, input, content, and recovery.

## State model

For each interactive component mark every state as required, not applicable with reason, or intentionally delegated to a platform primitive:

- enabled, disabled, hover, focus, pressed, dragged;
- selected/checked/expanded/current;
- validating, loading, empty, error, success, stale/offline.

State changes must be perceivable without color alone. Disabled content remains understandable. Preserve user work through validation, retries, resize, navigation, and process recreation where the platform contract requires it.

## Names and semantics

- Give every actionable control a localized accessible name describing its outcome.
- Do not duplicate an adjacent text label by also naming its decorative icon.
- Expose role, value, selected/checked/expanded state, validation error, progress, and live status as applicable.
- Group radio/checkbox/segmented controls with a programmatic group name.
- Make whole labeled rows interactive only when semantics remain one unambiguous control.

## Focus, keyboard, and pointer

- Provide visible, unclipped focus and logical traversal matching reading/task order.
- Trap focus only in truly modal surfaces; restore it to the invoker on dismissal.
- Support expected activation, arrow-key, Escape, Tab, and shortcut behavior for the platform pattern.
- Keep hover supplementary. Maintain usable touch/pointer targets and spacing even in dense layouts.

## Forms

- Use persistent labels, appropriate input types, autofill hints, and clear constraints.
- Validate at a helpful time; preserve input; move/announce focus to a useful summary or first invalid field without surprise.
- Error text states what failed and how to recover. Do not use placeholder-only labels or color-only borders.
- Loading submission prevents accidental duplication while preserving cancellation/recovery where needed.

## Content and feedback

- Buttons use outcome verbs; navigation labels name destinations.
- Empty states explain why and offer the next useful action.
- Snackbars report short, non-blocking outcomes; dialogs request necessary decisions; inline text handles field errors.
- Determinate progress must be truthful. Long indeterminate work needs explanatory status and cancellation/background behavior when feasible.
- Destructive actions need specific labels plus prevention, confirmation, undo, or recovery proportionate to impact.

## Accessibility verification

Test, do not infer:

- contrast under every shipped scheme and state;
- screen reader names, roles, values, ordering, headings, errors, and live regions;
- keyboard/D-pad traversal, activation, dismissal, and focus return;
- touch/pointer targets and motor accessibility;
- 200% text or the declared product target, zoom, localization, and reflow;
- reduced motion and non-color meaning;
- IME visibility and reachability of the active field and completion action.

Automated checks are smoke tests, not certification. Record manual evidence for critical journeys.
