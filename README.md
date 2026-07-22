# Material 3 Build + Audit Skill

A portable AI-assistant skill for designing, building, migrating, and auditing production-oriented Material 3 interfaces.

It combines implementation workflows with an evidence contract: Compose receives full-depth guidance, Flutter receives production-focused support, and Web uses verified Material Web elements plus accessible native/custom fallbacks without claiming feature parity.

## Capabilities

| Mode | Outcome |
|---|---|
| Design | Theme, hierarchy, component, state, accessibility, responsive, and handoff decisions; no code unless requested |
| Build | Integration-ready `component`, `theme`, `layout`, `scaffold`, or `migrate` work with API status and verification |
| Audit | `D01`–`D10` evidence scorecard, `U`/reasoned `n/a`, release gates, and prioritized fixes |

Build coverage includes:

- 38 component families with Compose, Flutter, and Web mappings
- complete token/theme strategy for light, dark, and platform-appropriate Dynamic/static paths
- forms, state hoisting, validation, loading/error/empty states, focus, semantics, and tests
- adaptive navigation, canonical layouts, insets, IME, foldables, live resize, and state continuity
- Compose M2, Flutter older-Material, and Web MDC migrations
- locally build-tested core baselines for Compose, Flutter, and Web
- a dependency-light heuristic scanner with deterministic Markdown/JSON output
- twelve structured behavior-evaluation fixtures

## Platform tiers

| Platform | Support | Honesty boundary |
|---|---|---|
| Jetpack Compose | Primary/full depth | Stable APIs by default; Expressive, experimental, and Navigation 3 integration are verified per project |
| Flutter | Secondary/production focused | Official widgets and ThemeData; no promise of Compose Expressive parity |
| Web | Limited | Verified `@material/web` exports or accessible native/custom fallbacks; full Expressive parity is refused |

## Install locally

Copy or link `skills/material3-design` to the skill directory used by the assistant:

```text
~/.codex/skills/material3-design
~/.cursor/skills/material3-design
~/.claude/skills/material3-design
```

Keep the folder name `material3-design`. After this repository is published, it can also be installed with a compatible skill installer using the repository URL; no public owner or release is claimed by this working tree.

## Examples

### Design

```text
Use $material3-design to design a responsive list-detail inbox. Define theme roles, component jobs, states, navigation, accessibility, and the Design-to-Build handoff. Do not write code yet.
```

### Build

```text
Use $material3-design to build the Material 3 theme and adaptive app shell in this Compose project. Preserve its architecture, use stable APIs, add state/accessibility tests, run the scanner, and report the Build output contract.
```

```text
Use $material3-design to migrate this Flutter app from legacy bottom navigation to Material 3 while preserving destination state and testing light/dark and compact/expanded layouts.
```

```text
Use $material3-design to implement these Web components. Verify each official Material Web element, use semantic native fallbacks for gaps, and refuse unsupported Expressive parity.
```

### Audit

```text
Use $material3-design in Audit mode on these screens and files. Score D01–D10, mark missing evidence U, justify every n/a, apply release gates, and separate Must-fix from Nice-to-have.
```

## Scanner

```bash
python skills/material3-design/scripts/m3_scan.py <path> --platform auto --format markdown
python skills/material3-design/scripts/m3_scan.py <path> --platform compose --format json
```

The scanner returns rule ID, audit dimension, severity, confidence, file/line evidence, and remediation. Exit `0` means a completed scan without high-confidence blockers, `1` means blockers were found, and `2` means invalid input/configuration. It is heuristic evidence collection, not a compliance or WCAG certificate.

## Repository map

```text
.github/                 CI and dependency-update configuration
.claude-plugin/          Claude plugin/marketplace metadata
docs/                    maturity, capability, and release evidence chain
docs/evidence/           local, hosted-CI, and fresh-install ledgers
evals/fixtures/          twelve host-neutral behavior contracts
evals/runs/              revision-anchored host execution records (currently empty)
skills/material3-design/
  SKILL.md               lean runtime router and contracts
  references/            canonical shared and platform guidance
  scripts/m3_scan.py     deterministic heuristic scanner
  assets/templates/      Compose, Flutter, and Web core projects
tests/                   structure, scanner, fixture, and run validation
```

The runtime package contains only `SKILL.md`, agent metadata, references, the scanner, and reusable template assets. Repository/release documentation remains outside it. See the [release evidence chain](docs/RELEASE-EVIDENCE-CHAIN.md).

## Verification

Run the checks available in the current environment:

```bash
python -m unittest discover -s tests -p "test_*.py"
python tests/validate_fixtures.py
python tests/validate_eval_runs.py
python tests/validate_repository.py
```

Template release checks are:

```bash
gradle testDebugUnitTest assembleDebug  # from compose-core
dart format --set-exit-if-changed . && flutter analyze && flutter test  # flutter-core
npm ci && npm run build && npm test  # web-core
```

Pinned versions are tested baselines, never “latest.” All three local build/test paths passed on 2026-07-22; release CI must rerun them and record the evidence. See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

Fixture validation proves only that evaluation contracts are well formed. There are currently zero archived host run records, so this repository does not claim stable Codex, Claude, or Cursor behavior. See the [release evidence chain](docs/RELEASE-EVIDENCE-CHAIN.md), [capability matrix](docs/CAPABILITY-MATRIX.md), and [evaluation evidence guide](docs/EVALUATION-EVIDENCE.md).

## Accuracy model

- Volatile claims use first-party URLs and last-verified dates in the [source registry](skills/material3-design/references/source-registry.md).
- Shared facts have one canonical owner in the [content ownership map](skills/material3-design/references/content-ownership.md).
- Audits never infer dark theme, Dynamic Color, accessibility, responsive behavior, or hidden states.
- Automated scans and accessibility smoke tests do not replace manual evidence.
- Community dependencies are not recommended without maintenance, license, support, and risk verification.

## License and attribution

Original repository content is released under the [MIT License](LICENSE). Material, Android, Flutter, Web, and third-party sources remain subject to their own terms; see [NOTICE.md](NOTICE.md).
