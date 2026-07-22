# Release Checklist

No commit, tag, GitHub release, marketplace publication, or package publication is authorized by this checklist.

Follow the ordered links in [docs/RELEASE-EVIDENCE-CHAIN.md](docs/RELEASE-EVIDENCE-CHAIN.md). Check a box only when the matching ledger or archive exists.

## 1. Revision anchor

- [ ] Git revision and clean/reviewed working tree recorded
- [ ] First-commit inventory reviewed ([docs/FIRST-COMMIT-INVENTORY.md](docs/FIRST-COMMIT-INVENTORY.md)) when creating history

## 2. Source and structure

- [ ] Portable skill/frontmatter, UTF-8, links, anchors, source registry, catalog, D01–D10, scanner, fixtures, and metadata validators pass
- [ ] Volatile source entries and catalog dates reviewed
- [ ] Changelog and install instructions match the intended version

## 3. Stable core templates

- [ ] Local ledger updated in [docs/evidence/local-verification.md](docs/evidence/local-verification.md)
- [ ] Compose clean CI build and unit tests pass on the recorded tested baseline
- [ ] Flutter format, analyze, and tests pass on the recorded tested baseline
- [ ] Web clean install, build, tests, and accessibility smoke pass on the recorded tested baseline
- [ ] Hosted CI ledger updated in [docs/evidence/hosted-ci.md](docs/evidence/hosted-ci.md)
- [ ] Dependency updates were merged only after source review and all affected checks passed

## 4. Behavior evaluation

- [ ] `python tests/validate_eval_runs.py` reports archived records rather than zero behavior evidence
- [ ] All twelve fixtures run on every claimed host (Codex and Claude when both are claimed)
- [ ] Every run records revision, host, model when known, UTC date, results, generated files/tests, reviewer, and human deviations
- [ ] 100% of critical assertions pass
- [ ] At least 90% of all assertions pass
- [ ] Zero forbidden, invented API, or invented version claims

Release command when Codex and Claude are both claimed:

~~~bash
python tests/validate_eval_runs.py --require-host codex --require-host claude --require-all-fixtures
~~~

## 5. Fresh installation

- [ ] Ledger updated in [docs/evidence/fresh-install.md](docs/evidence/fresh-install.md)
- [ ] Codex install and invocation pass
- [ ] Cursor install and invocation pass
- [ ] Claude plugin/marketplace install and invocation pass
- [ ] `npx skills` installation passes when the repository is public

## 6. Publication gate

- [ ] Version chosen according to maturity evidence
- [ ] Public v0.1.0 has at least one complete theme, component, scaffold, migration, and audit workflow plus all core templates green
- [ ] Public v1.0.0 has full catalog coverage, all fixture thresholds, current sources, and every fresh-install check
- [ ] Explicit authorization obtained before commits, tags, releases, GitHub publication, or marketplace publication
