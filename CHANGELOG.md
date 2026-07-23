# Changelog

All notable changes are recorded here. The project has not been tagged or published by this implementation.

## Unreleased

- Added Lite / Standard / Evidence output profiles and lead-with-artifact delivery rules in `SKILL.md`.
- Added five Compose golden-path recipes under `references/recipes/` with content-ownership boundaries.
- Restructured the README around install, six task entry points, illustrative output shape, and a host-behavior benchmark placeholder.
- Upgraded behavior run records to schema_version 2 (`condition`, `repetition`, `metrics`) with with-skill release gates and baseline contrast.
- Added `evals/generate_run_matrix.py`, `evals/benchmark_report.py` (`BENCHMARK.md` / `benchmark.json`), and a 50-case trigger evaluation set under `evals/trigger/`.
- Upgraded the heuristic scanner from a single regex script to a rule engine under `scripts/m3_engine/` + `scripts/rules/{compose,flutter,web}/` with unified metadata, fixtures, suppressions, source IDs, and precision/recall metrics.
- Reorganized runtime references into `shared/`, `compose/`, `flutter/`, `web/`, and `audit/` without splitting into multiple Skills.
- Simplified the README user entry (value, one install command, three examples, fixture benchmark, support levels, verified versions, limitations).
- Added maintainer scanner guide at `docs/SCANNER.md`.
- Repositioned `material3-design` as equal Build + Audit capability.
- Added Design, Build, and Audit runtime contracts with platform/task routing.
- Added canonical ownership, dated first-party source registry, extracted foundations/styles and interaction/accessibility references.
- Expanded the catalog to 38 cross-platform component families.
- Added full-depth Compose, production Flutter, limited Web, and migration recipes.
- Added locally build-tested Compose, Flutter, and Web core baselines with CI build/test jobs.
- Added deterministic `m3_scan.py`, unit tests, and twelve behavior fixtures.
- Added explicit critical fixture assertions, revision-anchored run-record schema/validation, and separate capability/evidence documentation.
- Added CI, dependency-update configuration, Claude metadata, and release gates.
- Added the six-link release evidence chain, local/hosted/install ledgers, and first-commit inventory review.
- Corrected post-import evidence status, Flutter local-verification claims, Codex install paths, and development-time Claude version handling.
- Pinned every GitHub Action to a verified full commit SHA while retaining major-version comments for dependency automation.
- Passed the official Claude marketplace validator with the documented development-version warning and added deterministic metadata checks.
