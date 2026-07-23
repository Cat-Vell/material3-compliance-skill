# Release Evidence Chain

Last reviewed: **2026-07-23**.

The release evidence chain is the ordered set of records that justify a public claim such as “v0.1.0 is usable.” Fixtures, local notes, and README prose are not substitutes for the matching link.

## Chain links

| # | Link | Proves | Canonical location | Gate |
|---|---|---|---|---|
| 1 | Revision anchor | A specific Git commit is the evaluated subject | Git history + clean tree | Required before any archived behavior run |
| 2 | Structure and contract | Skill package, D01–D10, fixtures, scanner, metadata stay consistent | `tests/validate_repository.py`, `validate_fixtures.py`, unit tests, trigger case validation | Required for every release candidate |
| 3 | Stable template baselines | Compose / Flutter / Web cores build and test on pinned versions | `baseline.json` + [local-verification.md](evidence/local-verification.md) + [hosted-ci.md](evidence/hosted-ci.md) | Local alone can mark a tested baseline; public release also needs hosted CI |
| 4 | Host behavior | Assistants follow Design / Build / Audit contracts under with-skill; baseline contrast is recorded | `evals/runs/*.json` (schema v2) + artifacts + [BENCHMARK.md](../BENCHMARK.md); see [EVALUATION-EVIDENCE.md](EVALUATION-EVIDENCE.md) | Required before claiming Codex/Claude (or other) stability |
| 5 | Fresh install | Declared distribution surfaces can install and invoke the skill | [fresh-install.md](evidence/fresh-install.md) | Required for each surface named in public docs |
| 6 | Publication authorization | Version, changelog, and human approval match the evidence | [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md) | Required before tag, GitHub release, or marketplace publish |

## Honesty rules

- Unknown or empty is honest. Do not invent CI URLs, run records, or install passes.
- A fixture without an archived run record is a contract, not behavior evidence.
- Local template success is not hosted CI evidence and not assistant-behavior evidence.
- Behavior run records must use a full 40-character commit that exists in history and `working_tree_clean: true`.
- Release gates apply to `with-skill` records; `baseline` records are contrast evidence and may fail.
- Evidence for a subject revision may be committed in a later commit; the record still points at the evaluated revision.
- Tag CI (`behavior-release-gate`) requires complete Codex and Claude fixture×condition coverage when a `v*` tag is pushed.

## Current chain status

| Link | Status on 2026-07-23 |
|---|---|
| 1 Revision anchor | Initial revision exists; the next release subject still needs a clean, recorded SHA |
| 2 Structure and contract | Passing locally (includes output profiles, recipes, trigger cases, schema v2 tooling) |
| 3 Stable templates | Local baselines recorded; hosted CI not yet anchored |
| 4 Host behavior | Zero archived run records; matrix and benchmark tooling present |
| 5 Fresh install | Codex local-copy check is partial and unanchored; no fresh install is recorded |
| 6 Publication authorization | Not granted |

## How to advance the chain

1. Review and commit the current changes when explicitly authorized, then record the full clean SHA used by later evidence.
2. Push to a remote and record hosted CI results in [hosted-ci.md](evidence/hosted-ci.md).
3. Install on each claimed surface and fill [fresh-install.md](evidence/fresh-install.md).
4. Run `python evals/generate_run_matrix.py`, execute prompts on each claimed host for with-skill and baseline, archive records under `evals/runs/`, then `python evals/benchmark_report.py`.
5. Score trigger results after any description change.
6. Check every box in [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md) that matches the intended claim, then request explicit authorization to tag or publish.

## Related

- [CAPABILITY-MATRIX.md](CAPABILITY-MATRIX.md) — what the package implements vs what it claims
- [MATURITY-ROADMAP.md](MATURITY-ROADMAP.md) — v0.1.0 / v1.0.0 gates
- [evidence/README.md](evidence/README.md) — ledgers and templates
- [BENCHMARK.md](../BENCHMARK.md) — aggregated host-behavior comparison (placeholder until runs exist)