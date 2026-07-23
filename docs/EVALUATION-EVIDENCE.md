# Behavior Evaluation Evidence

Fixtures and run records are different artifacts:

- evals/fixtures/*.json defines the task contract.
- evals/runs/*.json records one observed execution (schema_version 2).
- A fixture without a run record is **not evidence of assistant behavior**.
- Local template build evidence is **not evidence of assistant behavior**.
- Baseline (`condition: baseline`) runs are contrast evidence; release gates apply to `with-skill` only.

## Run a fixture

1. Generate the matrix prompts/templates: `python evals/generate_run_matrix.py`.
2. Start a fresh host session. For `with-skill`, install the skill and only the fixture's input evidence. For `baseline`, use the same prompt without the skill.
3. Preserve the exact prompt, response, generated files, and test output.
4. Evaluate every required assertion and forbidden claim.
5. Record a full Git revision, clean-tree state, host, model when known, `condition`, `repetition`, metrics (tokens/duration or null), UTC timestamps, reviewer, and human deviations.
6. Store the prompt, response, and generated artifacts at repository-relative paths committed with the run record.
7. Create a run record conforming to evals/run-record.schema.json (schema_version 2).
8. Validate it with python tests/validate_eval_runs.py.

Before a release claiming Codex and Claude support with with-skill/baseline contrast:

~~~bash
python tests/validate_eval_runs.py --require-host codex --require-host claude --require-all-fixtures --min-repetitions 1
~~~

## Pass calculation

- Every fixture-declared critical assertion must pass on `with-skill` records.
- At least 90% of all required assertions must pass across the selected `with-skill` release set.
- No forbidden claim may be observed on `with-skill` records.
- The stored result must match the deterministic calculation (also for baseline records, which may fail).
- A release still requires green stable-template and repository checks.

The validator checks record completeness and arithmetic. It cannot determine whether a human reviewer judged an output correctly.

## Provenance boundary

A valid run record requires a full 40-character Git commit hash that exists in repository history and working_tree_clean: true. Prompt and response artifact paths must also exist inside the repository. This intentionally prevents an uncommitted working tree or detached summary from being presented as release-grade behavior evidence. The evidence record may be committed after the evaluated source revision. Draft experiments may be kept elsewhere, but they do not satisfy the release gate.

This file owns behavior-run provenance only. The full six-link release chain—including templates, hosted CI, and fresh installs—is documented in [RELEASE-EVIDENCE-CHAIN.md](RELEASE-EVIDENCE-CHAIN.md). Aggregate comparison tables are produced by `python evals/benchmark_report.py` into [BENCHMARK.md](../BENCHMARK.md).
