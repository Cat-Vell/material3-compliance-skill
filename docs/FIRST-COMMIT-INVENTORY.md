# First Commit Inventory Review

Reviewed: **2026-07-22**. Scope: prepare the initial Git commit for `material3-compliance-skill`. This document authorizes **inventory classification only**; it does **not** authorize creating the commit.

## Recommended commit message (when authorized)

```text
Initial import of Material 3 Build + Audit skill package.

Establish portable skill contracts, platform templates, scanners,
evaluation fixtures, and the release evidence chain without claiming
hosted CI or host behavior passes.
```

## Include in first commit

### Repository meta

| Path | Why |
|---|---|
| `.gitignore` | Keep build caches and `node_modules` out of history |
| `.github/workflows/ci.yml` | Hosted validation and template jobs |
| `.github/dependabot.yml` | Dependency update proposals |
| `.claude-plugin/plugin.json` | Claude install metadata |
| `.claude-plugin/marketplace.json` | Claude marketplace metadata |
| `LICENSE` | MIT for original repo content |
| `NOTICE.md` | Upstream Material / platform attribution boundary |
| `README.md` | Product contract and install map |
| `CHANGELOG.md` | Unreleased capability log |
| `CONTRIBUTING.md` | Ownership and check requirements |
| `RELEASE_CHECKLIST.md` | Human release gate |

### Docs and evidence framework

| Path | Why |
|---|---|
| `docs/MATURITY-ROADMAP.md` | Version gates |
| `docs/CAPABILITY-MATRIX.md` | Implemented vs claimed |
| `docs/EVALUATION-EVIDENCE.md` | Behavior-run provenance rules |
| `docs/RELEASE-EVIDENCE-CHAIN.md` | Six-link release evidence chain |
| `docs/FIRST-COMMIT-INVENTORY.md` | This review |
| `docs/evidence/**` | Local / CI / install ledgers and example templates |

### Eval contracts (not passes)

| Path | Why |
|---|---|
| `evals/README.md` | Fixture vs evidence distinction |
| `evals/run-record.schema.json` | Run-record shape |
| `evals/fixtures/*.json` | Twelve host-neutral contracts |
| `evals/runs/.gitkeep` | Reserve archive directory |

### Runtime skill package

| Path | Why |
|---|---|
| `skills/material3-design/SKILL.md` | Portable runtime router |
| `skills/material3-design/agents/openai.yaml` | Codex metadata |
| `skills/material3-design/scripts/m3_scan.py` | Heuristic scanner |
| `skills/material3-design/references/*.md` | Canonical guidance set |
| `skills/material3-design/assets/templates/compose-core/**` | Stable Compose baseline sources |
| `skills/material3-design/assets/templates/flutter-core/**` | Stable Flutter baseline sources |
| `skills/material3-design/assets/templates/web-core/**` | Stable Web baseline sources |

Lockfiles (`pubspec.lock`, `package-lock.json`) are intentionally included so baselines stay reproducible.

### Tests

| Path | Why |
|---|---|
| `tests/validate_repository.py` | Structural contract |
| `tests/validate_fixtures.py` | Fixture schema |
| `tests/validate_eval_runs.py` | Archived run validator |
| `tests/test_m3_scan.py` | Scanner unit tests |
| `tests/test_eval_run_validator.py` | Run-validator unit tests |

## Exclude from first commit

| Path / pattern | Why |
|---|---|
| `**/node_modules/`, `**/build/`, `**/.gradle/`, `**/.dart_tool/`, `**/dist/` | Generated; covered by `.gitignore` |
| `__pycache__/`, `*.pyc`, IDE folders, OS junk | Local noise |
| Real `evals/runs/*.json` behavior archives | Cannot be revision-anchored before history exists; add after first commit + real runs |
| Secrets, tokens, private model transcripts | None expected; never add |
| Personal `~/.cursor/skills/material3-design` | Outside this repo; sync after commit if desired |

## Defer to later commits (not first-commit blockers)

| Item | Trigger |
|---|---|
| Fill `docs/evidence/hosted-ci.md` | First green remote Actions run |
| Fill `docs/evidence/fresh-install.md` | Documented install passes |
| Archive `evals/runs/*.json` + artifacts | After subject revision exists and fixtures are executed |
| Tag `v0.1.0` | Only after [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md) and explicit authorization |
| Publish marketplace / `npx skills` | Only after public repo + install evidence |

## Pre-commit verification (local)

Run from the repository root after staging:

```bash
python -m unittest discover -s tests -p "test_*.py"
python tests/validate_fixtures.py
python tests/validate_eval_runs.py
python tests/validate_repository.py
```

Optional if toolchains are available: re-run the three template command sets recorded in [local-verification.md](evidence/local-verification.md).

Expected honest state after the first commit: links 1–2 of the evidence chain become possible; links 3 (hosted), 4, 5, and 6 remain open.

## Review verdict

| Question | Answer |
|---|---|
| Safe to stage the Include set? | Yes — no secrets found; lockfiles are intentional |
| Any must-fix before commit? | No structural blockers; evidence ledgers correctly report pending hosted/behavior/install proof |
| Authorize commit now? | **No** — wait for an explicit user request to create the commit |

When ready, ask to create the first commit; do not treat this inventory as publication or tag approval.
