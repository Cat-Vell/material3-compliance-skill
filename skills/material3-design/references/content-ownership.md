# Content Ownership

Use this map to resolve conflicts and prevent duplicated facts. The listed file is canonical; other references may link or summarize without redefining the rule.

| Topic | Canonical owner | Update rule |
|---|---|---|
| Runtime modes, routing, output contracts | `SKILL.md` | Keep under 180 lines; link details |
| Source IDs, URLs, verification dates, support labels | `source-registry.md` | First-party evidence required for volatile APIs |
| Tokens, color, typography, shape, elevation, motion | `foundations-and-styles.md` | Platform files only map these concepts to APIs |
| Interaction states, semantics, content, accessibility | `interaction-and-accessibility.md` | Component records list applicability, not duplicate rules |
| Component jobs, avoid cases, variants, cross-platform mapping | `component-catalog.md` | Platform files own implementation recipes |
| Window context, layouts, panes, insets, IME, foldables | `layout-and-responsive.md` | Navigation choice remains in navigation owner |
| Information architecture, navigation, back, deep links | `navigation-patterns.md` | Platform files map APIs only |
| Compose code and API gates | `compose.md` | Stable recipes reference catalog identifiers |
| Flutter code and parity gates | `flutter.md` | No community packages by default |
| Web code, SSR, ARIA, and fallback gates | `web.md` | Never promise full M3 parity |
| Migration sequencing and interoperability | `migrations.md` | Platform files may link to the relevant section |
| Audit dimensions, evidence, scoring, gates | `audit-framework.md` | IDs are permanently `D01`–`D10` |
| Reusable output files | `assets/templates/*` | Each baseline manifest records tested versions |
| Scanner behavior and rule IDs | `scripts/m3_scan.py` | Tests define deterministic output/exit behavior |

When two files disagree, follow this map, then record the source review needed. Do not silently blend conflicting API claims.
