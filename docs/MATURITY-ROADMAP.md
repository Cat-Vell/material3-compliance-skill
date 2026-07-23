# Material 3 Build + Audit Maturity Roadmap

Last implementation review: **2026-07-23**.

## Product contract

`material3-design` treats Design, Build, and Audit as first-class workflows. Compose is primary/full depth; Flutter is production-focused secondary support; Web is a limited token/verified-element/accessible-fallback tier. Platform parity is never implied. Output size scales with risk via Lite / Standard / Evidence profiles.

## Implemented foundation

- Lean portable `SKILL.md` with platform and task routing, output profiles, and lead-with-artifact delivery
- Five Compose golden-path recipes under `references/recipes/`
- Stable audit IDs `D01`–`D10`, `U`, reasoned `n/a`, coverage, and release gates
- Content ownership map and dated first-party source registry
- Extracted theme/style and interaction/accessibility canonical references
- 38-family component catalog with support, source, recipe, and verification data
- Compose, Flutter, Web, and migration guidance
- Locally build-tested core baselines for all three platform tiers
- Dependency-light rule-engine scanner (`m3_engine` + `rules/{compose,flutter,web}`) with per-rule fixtures, suppressions, source IDs, and fixture precision/recall metrics
- AST/compiler-backed matching for Kotlin, Dart, and JavaScript deferred to a later maturity stage
- Twelve behavior fixtures, schema_version 2 run records (`condition` / `repetition` / `metrics`), matrix generator, and benchmark aggregator
- Fifty-case skill trigger evaluation set with precision/recall targets
- Separate capability matrix and behavior-evidence guide
- Six-link release evidence chain with local, hosted-CI, and fresh-install ledgers
- CI, dependency updates, release checklist, Codex metadata, and Claude metadata

## Release evidence still required before public v0.1.0

Track progress in [RELEASE-EVIDENCE-CHAIN.md](RELEASE-EVIDENCE-CHAIN.md) and the ledgers under [evidence/](evidence/).

- Green hosted Compose build/test on its pinned baseline (local build/test passed 2026-07-22)
- Green hosted Flutter format/analyze/test on its pinned baseline (local format, `dart analyze`, and tests passed 2026-07-22; `flutter analyze` remains pending)
- Green clean Web install/build/test/accessibility smoke (local checks passed 2026-07-22)
- Recorded Codex and Claude with-skill / baseline behavior runs (matrix tooling ready; archived count still zero)
- Scored trigger evaluation meeting precision/recall targets
- Fresh-install results for every distribution surface being claimed
- Explicit authorization for commit, tag, repository publication, release, and marketplace publication

Do not tag a documentation-only or configuration-only baseline. Local evidence promotes a template to a tested baseline; hosted release CI must independently rerun it and record release evidence.

Current behavior evidence count is zero. Fixture presence and schema validation do not satisfy the host-evaluation gate; version-tag CI requires revision-anchored with-skill records for claimed hosts (baseline contrast recommended). The initial import exists in Git history; every later evidence record must point to the exact clean revision it evaluated.

## Public v0.1.0 gate

- At least one complete theme, component, scaffold, migration, and audit workflow
- All structural, scanner, fixture, and template jobs green
- Current source review and zero invented API/version claims
- Working install instructions and release evidence

## Public v1.0.0 gate

- Entire catalog and platform recipe coverage remains current
- Twelve fixtures meet 100% critical and 90% overall thresholds on claimed hosts
- Fresh installs pass on Codex, Cursor, Claude, and `npx skills`
- Stable templates build from clean environments
- Public README independently demonstrates Design, Build, and Audit

## Maintenance cadence

- Review volatile source entries and template baselines monthly or before release, whichever comes first.
- Let dependency automation propose changes; merge only after first-party source review and affected builds/tests pass.
- Keep experimental/Expressive examples outside stable cores until promoted and re-verified.
