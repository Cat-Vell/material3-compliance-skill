---
name: material3-design
description: >-
  Design, build, migrate, and audit Material 3 interfaces for Jetpack Compose,
  Flutter, and Web. Use for Material 3 or M3 themes, components, layouts, app
  shells, accessibility and responsive behavior, M2-to-M3 or MDC migrations,
  Dynamic Color, Material You, M3 Expressive, compliance reviews, or generated
  implementation code. Compose has full-depth support; Flutter is production-
  focused; Web is limited to verified Material Web elements, tokens, and
  accessible native/custom fallbacks.
---

# Material 3 Build + Audit

Produce integration-ready Material 3 work and evidence-based audits. Treat platform support and volatile APIs honestly.

## Non-negotiable rules

1. Use semantic theme roles and tokens; keep primitives inside token definitions.
2. Define Color Scheme, Typography, and Shapes before screen-level overrides.
3. Specify applicable enabled, disabled, hover, focus, pressed, selected, loading, empty, error, and success states.
4. Provide accessible names, semantics, visible focus, keyboard behavior, usable targets, non-color cues, and reduced-motion behavior.
5. Adapt from current window, content, destination count, posture, and input mode; never route only from device labels.
6. Keep one obvious highest-emphasis action per key view.
7. Verify volatile APIs in first-party sources. Never invent a version or claim Expressive parity.
8. Pair container/content roles and ship light/dark static schemes; Dynamic Color never replaces a fallback.

## Modes

### Design

Produce theme decisions, hierarchy, component choices, states, responsive behavior, accessibility, and handoff specifications. Do not emit code unless implementation is requested.

### Build

Infer the platform from supplied files. Ask only when it cannot be determined. Route the task to `component`, `theme`, `layout`, `scaffold`, or `migrate`. Adapt an asset under [assets/templates](assets/templates) when it fits; otherwise produce integration-ready files. Read the canonical shared owner for every requested concern, [component-catalog.md](references/component-catalog.md) for component work, and exactly one platform guide. Do not implement from the catalog mapping alone.

Return this contract:

```text
Platform: [Compose | Flutter | Web]
Task: [component | theme | layout | scaffold | migrate]
Implementation: [files/code]
API status: [stable | verify-current | unsupported/custom]
States and accessibility: [...]
Adaptive behavior: [...]
Verification: [tests/checks]
M3 Compliance: [...]
```

For `verify-current`, cite the checked first-party source and date. For `unsupported/custom`, explain the accessible fallback or refuse the unsupported parity claim.

### Audit

Read [audit-framework.md](references/audit-framework.md). Use `D01`–`D10`, evidence references, and release gates. Use `U` for missing evidence. Use `n/a` only when a dimension is genuinely outside the declared scope and include a reason. Never infer dark theme, Dynamic Color, accessibility, responsive behavior, or hidden states.

## Routing map

| Need | Read |
|---|---|
| Ownership and conflict resolution | [content-ownership.md](references/content-ownership.md) |
| Official sources and support labels | [source-registry.md](references/source-registry.md) |
| Tokens, theme, color, type, shape, elevation, motion | [foundations-and-styles.md](references/foundations-and-styles.md) |
| States, forms, content, and accessibility | [interaction-and-accessibility.md](references/interaction-and-accessibility.md) |
| Component semantics and cross-platform mapping | [component-catalog.md](references/component-catalog.md) |
| Responsive layouts, panes, insets, IME, foldables | [layout-and-responsive.md](references/layout-and-responsive.md) |
| Navigation, back, deep links | [navigation-patterns.md](references/navigation-patterns.md) |
| Compose implementation | [compose.md](references/compose.md) |
| Flutter implementation | [flutter.md](references/flutter.md) |
| Web implementation and refusal gates | [web.md](references/web.md) |
| M2/MDC/widget migration | [migrations.md](references/migrations.md) |
| Audit score and verdict | [audit-framework.md](references/audit-framework.md) |

## Platform tiers

| Platform | Depth | Default API policy |
|---|---|---|
| Compose | Full | Stable Material 3 first; gate alpha/experimental/Expressive and Navigation 3 |
| Flutter | Production secondary | Official Material widgets; disclose incomplete Expressive parity |
| Web | Limited | Verified `@material/web` element or accessible native/custom fallback; refuse full Expressive parity |

## Delivery discipline

- Preserve the project architecture, version catalog, routing, and test conventions.
- Hoist durable state; preserve selection, input, scroll, focus, and work across resize and navigation changes.
- Include loading/error/empty recovery for data-driven UI and validation for forms.
- Add focused semantics/state/adaptive tests for changed behavior.
- Run `python scripts/m3_scan.py <path> --platform auto --format markdown` when repository files are available. Treat findings as heuristic evidence, not certification.
- End Design and Build work with the compact M3 Compliance summary from the Build contract. End Audit work with its scorecard, gates, prioritized findings, then that summary.

## Accuracy gates

- Check source IDs in [source-registry.md](references/source-registry.md) before platform claims.
- Treat dates and tested baselines as evidence, never as “latest.”
- Keep volatile or experimental examples outside stable templates.
- Do not recommend a community dependency unless the user requests alternatives and its maintenance, license, and risk are verified and disclosed.
