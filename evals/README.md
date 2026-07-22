# Behavior Evaluation

The twelve JSON fixtures are host-neutral contracts for Codex and Claude evaluations. They are specifications, not passing evidence. A release claiming both hosts must run every fixture on both and store a run record outside the runtime skill package under `evals/runs`.

Each fixture explicitly identifies critical assertion indexes. Each run record must include: fixture ID and digest, full Git revision, clean-tree state, host/version, model when known, UTC timestamps, prompt/response artifacts, assertion results, forbidden-claim results, generated files, test output, human deviations, reviewer, and final pass/fail.

Run `python tests/validate_eval_runs.py` to validate any archived records. With no records it succeeds while explicitly reporting that no host behavior evidence exists. Release thresholds: 100% critical assertions; at least 90% of all assertions; zero forbidden/invented API or version claims; all stable template builds green; all structural/scanner tests green. Manual execution is allowed, but the evidence is mandatory before release. See the [evidence guide](../docs/EVALUATION-EVIDENCE.md) and the [release evidence chain](../docs/RELEASE-EVIDENCE-CHAIN.md). Example-only JSON lives under `docs/evidence/templates/`; never place examples in `evals/runs/`.
