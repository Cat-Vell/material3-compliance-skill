# Recipe: Compose adaptive app shell

## When to use

- Jetpack Compose project with 3–5 top-level destinations.
- Compact and expanded (and usually medium) layouts are required.
- Selection and work must survive resize and navigation changes.

## Required inputs

- Destination count and information architecture.
- Window-size / posture expectations (compact, medium, expanded, IME).
- Existing navigation or scaffold conventions in the target repo.

## References to read

- [layout-and-responsive.md](../shared/layout-and-responsive.md)
- [navigation-patterns.md](../shared/navigation-patterns.md)
- [compose.md](../compose/compose.md)

## Template to adapt

- [assets/templates/compose-core](../../assets/templates/compose-core) — `App.kt` adaptive shell and state tests.

## Implementation sequence

1. Define one destination model shared across window sizes.
2. Choose navigation (bar / rail / drawer) from window context and IA, not device labels.
3. Hoist selection and durable state so layout changes do not drop work.
4. Consume Scaffold padding once; handle insets and IME.
5. State predictive-back risk if relevant; add continuity tests.

## Required states

- Compact, medium, and expanded navigation presentations.
- Selection preserved across layout changes.
- Loading/error/empty recovery for the primary content pane when data-driven.

## Tests to run

- State continuity / resize tests from the template or project suite.
- Manual checks: compact nav, expanded nav, selection preservation, back behavior, live resize.
- Scanner on changed shell files.

## Known unsupported cases

- “Tablet always means drawer.”
- One expanded screenshot as proof of adaptive compliance.
- Invented Navigation 3 APIs without verify-current evidence.

## Expected output profile

Standard.

## Bound fixture

`evals/fixtures/03-compose-adaptive-shell.json` (`compose-adaptive-shell`).
