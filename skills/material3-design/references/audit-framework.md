# Material 3 Audit Framework

Use this framework only for Audit mode. Audit supplied evidence, never an imagined complete product.

## 1. Evidence contract

Begin with:

```text
Audit target: [product/screens/repository]
Platform: [Compose | Flutter | Web | design-only]
Evidence reviewed: [files/screens/states/tests]
Contexts reviewed: [schemes/windows/posture/input/font scale]
Not provided: [material gaps]
```

Tie each finding and score to a file/line, screen/state, token, test, or explicit requirement. Do not infer hidden states, dark theme, Dynamic Color, semantics, focus, responsive behavior, or API availability.

## 2. Scores, Unknown, and not applicable

Use `0`–`4`, `U`, or `n/a`:

| Value | Meaning |
|---|---|
| 0 | absent, fundamentally wrong, or critical failure |
| 1 | major violations; substantial rework required |
| 2 | partial; important user/product gaps remain |
| 3 | compliant with minor bounded improvements |
| 4 | strong, consistent evidence including edge cases |
| U | evidence unavailable; unknown is not compliant |
| n/a | genuinely outside the declared scope; a written reason is mandatory |

`U` is included in evidence coverage denominator but not numerical score. `n/a` is excluded from both denominator calculations.

```text
percentage = earned points / (4 × scored dimensions) × 100
coverage = scored dimensions / applicable dimensions
```

Never publish percentage without coverage and the `U`/`n/a` list. If no dimensions are scored, verdict is `Insufficient evidence`.

## 3. Stable dimension registry

IDs never change across fixtures, scanner rules, or releases.

### D01. Theme and token integrity

Check Color Scheme, Typography, Shapes, semantic-token consumption, container/content pairing, light/dark/static fallback, Dynamic Color evidence, and bounded component overrides.

### D02. Hierarchy and primary action

Check critical task clarity, one highest-emphasis action, destructive emphasis, type/space/color/elevation alignment, and hierarchy on wider windows.

### D03. Component selection and semantics

Check user-job fit, variant priority, commit model, labels, semantics, custom-component behavior, and mappings in [component-catalog.md](component-catalog.md).

### D04. Navigation and information architecture

Check destination inventory, bar/rail/drawer/tabs distinction, selected state, labels, order, badges, state preservation, back/up, and deep links using [navigation-patterns.md](navigation-patterns.md).

### D05. Adaptive layout and continuity

Check composition across applicable widths/heights, medium strategy, canonical-layout fit, insets, IME, hinge, font scaling, input modes, and preserved selection/input/scroll/focus using [layout-and-responsive.md](layout-and-responsive.md).

### D06. Accessibility

Check contrast, targets, non-color meaning, names/roles/values, screen readers, focus visibility/order/return, keyboard behavior, localization, font scaling, and reduced motion.

### D07. Content and recovery

Check task-oriented labels, consistent terms, specific errors, preserved input, useful empty states, destructive recovery, honest loading/status, and understandable unstyled content.

### D08. States and feedback

Check applicable interaction states plus loading, empty, error, success, stale/offline; feedback component fit; disabled readability; truthful progress; and preserved work.

### D09. Motion and Expressive restraint

Check purposeful/tokenized motion, reduced-motion behavior, stated emotional/usability goals, restrained color/type/shape/motion, and verified platform/API support.

### D10. Platform and implementation integrity

Check platform tier honesty, theme boundary, stable versus experimental disclosure, state ownership/restoration, insets/semantics/adaptive APIs, migrations, tests, and first-party verification. For design-only scope, score handoff completeness and platform realism.

## 4. Release gates

Check gates before calculating a verdict. Any triggered gate prevents `Release-ready candidate` regardless of average:

- a critical task cannot be completed or its primary action is unavailable;
- known contrast/accessibility failure blocks an in-scope path;
- keyboard or assistive-technology users cannot complete an in-scope task;
- meaningful state, error, or status relies on color alone;
- a destructive action lacks proportionate labeling, prevention, or recovery;
- navigation/back loses work, traps the user, or contradicts the visible destination;
- a required window/posture/input context is unusable, obscured, or resets the task;
- shipped dark, Dynamic, or static role pairing is unreadable;
- implementation claims an unavailable or unverified API/component as shipped;
- evidence is insufficient for a critical release criterion.

## 5. Verdict

After gates:

| Percentage | Baseline verdict |
|---|---|
| 90–100 | Release-ready candidate |
| 75–89 | Conditional pass |
| 50–74 | Needs revision |
| 0–49 | Not ready |

`Release-ready candidate` additionally requires: no gate; at least 80% coverage; `D04`, `D05`, `D06`, and `D08` scored; no scored dimension below 3; and every `n/a` reason accepted as scope-correct.

## 6. Procedure

1. Declare scope, platform, evidence, contexts, and gaps.
2. Identify critical journeys and primary actions.
3. Run the scanner when source files exist; validate every heuristic finding manually.
4. Inspect all applicable dimensions and record evidence.
5. Assign `0`–`4`, `U`, or reasoned `n/a` without averaging contradictions away.
6. Apply release gates.
7. Calculate percentage and coverage.
8. Separate Must-fix from Nice-to-have and give the smallest credible fix.
9. End with the M3 Compliance summary.

## 7. Required output

```markdown
## M3 Audit

**Audit target:** [...]
**Platform:** [...]
**Evidence reviewed:** [...]
**Contexts reviewed:** [...]
**Not provided:** [...]

| ID | Dimension | Score | Evidence | Highest-impact fix |
|---|---|---:|---|---|
| D01 | Theme and token integrity | [0–4/U/n/a] | [...] | [...] |
| D02 | Hierarchy and primary action | [...] | [...] | [...] |
| D03 | Component selection and semantics | [...] | [...] | [...] |
| D04 | Navigation and information architecture | [...] | [...] | [...] |
| D05 | Adaptive layout and continuity | [...] | [...] | [...] |
| D06 | Accessibility | [...] | [...] | [...] |
| D07 | Content and recovery | [...] | [...] | [...] |
| D08 | States and feedback | [...] | [...] | [...] |
| D09 | Motion and Expressive restraint | [...] | [...] | [...] |
| D10 | Platform and implementation integrity | [...] | [...] | [...] |

**Score:** [...] · **Coverage:** [...] · **U:** [...] · **n/a reasons:** [...]
**Release gates:** [none | list]
**Verdict:** [...]

### Must-fix
- [ID · evidence → impact → smallest credible fix]

### Nice-to-have
- [ID · improvement → value]

### M3 Compliance
- **Platform / API status:** [...]
- **Theme / primary action:** [...]
- **Navigation / adaptive:** [...]
- **States / accessibility:** [...]
- **Expressive / open risks:** [...]
```
