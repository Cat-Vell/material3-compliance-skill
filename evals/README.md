# Behavior Evaluation

The twelve JSON fixtures are host-neutral contracts for Codex and Claude evaluations. They are specifications, not passing evidence. A release claiming both hosts must run every fixture on both hosts under `with-skill` and `baseline` conditions and store run records outside the runtime skill package under `evals/runs`.

Each fixture explicitly identifies critical assertion indexes. Each run record (schema_version 2) must include: fixture ID and digest, full Git revision, clean-tree state, host/version, model when known, `condition` (`with-skill`|`baseline`), `repetition`, metrics (tokens/duration or null), UTC timestamps, prompt/response artifacts, assertion results, forbidden-claim results, generated files, test output, human deviations, reviewer, and final pass/fail.

## Generate and archive runs

```bash
python evals/generate_run_matrix.py              # 12 × 2 hosts × 2 conditions = 48 prompts
python evals/generate_run_matrix.py --dry-run
# After filling records into evals/runs/:
python tests/validate_eval_runs.py
python tests/validate_eval_runs.py --require-host codex --require-host claude --require-all-fixtures --min-repetitions 1
python evals/benchmark_report.py                 # writes BENCHMARK.md + benchmark.json
```

Release thresholds apply to **with-skill** records: 100% critical assertions; at least 90% of all assertions; zero forbidden/invented API or version claims; all stable template builds green; all structural/scanner tests green. Baseline records are contrast evidence and may fail. Manual execution is allowed, but the evidence is mandatory before release. See the [evidence guide](../docs/EVALUATION-EVIDENCE.md) and the [release evidence chain](../docs/RELEASE-EVIDENCE-CHAIN.md). Example-only JSON lives under `docs/evidence/templates/`; never place examples in `evals/runs/`.

## Trigger evaluation

`evals/trigger/cases.json` holds 50 description-trigger cases (25 should-trigger, 15 should-not-trigger, 10 near-miss). Targets: precision ≥ 95%, recall ≥ 90%, near-miss false-trigger rate < 5%. Re-run after every `SKILL.md` description change.

```bash
python evals/trigger/score_trigger_runs.py
python evals/trigger/score_trigger_runs.py --results path/to/results.json --require-pass
```

Results file shape: `[{"id": "st-01", "observed": "trigger"}, ...]` (or `{"results": [...]}`).
