# Capability and Support Matrix

Last reviewed: **2026-07-22**.

This document describes implemented guidance and reusable assets. It does not claim that behavior fixtures have passed on any assistant host.

## Workflow coverage

| Workflow | Compose | Flutter | Web | Evidence level |
|---|---|---|---|---|
| Design | Full handoff contract | Production-focused | Token/fallback-aware | Runtime contract + fixture |
| Theme | Light, dark, Dynamic Color gate, type, shape, motion | Paired ThemeData, ColorScheme, component themes | CSS tokens, light/dark, user preference | Recipe + locally tested template |
| Component | 38-family catalog; stable recipes | Official-widget mappings and parity boundaries | Verified elements or accessible fallback | Catalog + platform recipes |
| Layout | Adaptive navigation, panes, foldables, insets, IME | Constraint-driven bar/rail and responsive layouts | Container queries, reflow, SSR cautions | Recipe + shell template |
| Scaffold | Adaptive app shell and state continuity | Responsive app shell | Responsive component shell | Locally tested template |
| Migration | M2 interoperability and staged migration | Older Material widget migration | MDC removal and token migration | Recipe + fixture |
| Audit | D01–D10, U, reasoned n/a, gates | Same evidence contract | Same contract with Web parity refusal | Contract + three fixtures |

## Platform depth

| Area | Compose | Flutter | Web |
|---|---|---|---|
| Support tier | Primary/full depth | Secondary/production focused | Limited/honest fallback |
| Stable core | Build and unit-test locally verified | Analyze and widget-test locally verified | Clean build, unit tests, and a11y smoke locally verified |
| Volatile APIs | Verify current; keep outside stable core | Verify current; disclose parity gaps | Verify each exported element |
| Expressive parity | Only behind availability gates | Not guaranteed | Explicitly refused |
| Community dependencies | Verify maintenance/license/risk first | Same | Same |

## Content ownership and reading path

Implementation quality depends on following the canonical route:

1. Read the shared owner for the requested concern: foundations, interaction/accessibility, component catalog, layout, navigation, or migration.
2. Read exactly one platform implementation guide.
3. Use the matching stable template only when its architecture fits the target project.
4. Check volatile API claims against the source registry and report their verification date.
5. Run focused project tests and the heuristic scanner; neither substitutes for manual evidence.

The authoritative ownership map is in [content-ownership.md](../skills/material3-design/references/content-ownership.md).

## Evidence maturity

Authoritative ordered chain: [RELEASE-EVIDENCE-CHAIN.md](RELEASE-EVIDENCE-CHAIN.md).

| Evidence class | Current state | What it proves |
|---|---|---|
| Structural validation | Passing locally | Package shape and deterministic contracts are internally consistent |
| Stable template checks | Passing locally | Bundled baseline source builds/analyzes/tests in the recorded local environments |
| Behavior fixtures | 12 contracts present | Defines expected and forbidden assistant behavior only |
| Archived host runs | None | No claim of stable Codex, Claude, Cursor, or other-host behavior |
| Hosted CI | Not yet anchored | No public revision/check URL exists before Git history and remote CI |
| Fresh installs | Not recorded | No distribution-surface installation claim |

