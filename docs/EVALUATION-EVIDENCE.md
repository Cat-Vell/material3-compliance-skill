# Behavior Evaluation Evidence

Fixtures and run records are different artifacts:

- evals/fixtures/*.json defines the task contract.
- evals/runs/*.json records one observed execution.
- A fixture without a run record is **not evidence of assistant behavior**.
- Local template build evidence is **not evidence of assistant behavior**.

## Run a fixture

1. Start a fresh host session with the installed skill and only the fixture's input evidence.
2. Preserve the exact prompt, response, generated files, and test output.
3. Evaluate every required assertion and forbidden claim.
4. Record a full Git revision, clean-tree state, host, model when known, UTC timestamps, reviewer, and human deviations.
5. Store the prompt, response, and generated artifacts at repository-relative paths committed with the run record.
6. Create a run record conforming to evals/run-record.schema.json.
7. Validate it with python tests/validate_eval_runs.py.

Before a release claiming Codex and Claude support, run:

~~~bash
python tests/validate_eval_runs.py --require-host codex --require-host claude --require-all-fixtures
~~~

## Pass calculation

- Every fixture-declared critical assertion must pass.
- At least 90% of all required assertions must pass across the selected release set.
- No forbidden claim may be observed.
- The stored result must match the deterministic calculation.
- A release still requires green stable-template and repository checks.

The validator checks record completeness and arithmetic. It cannot determine whether a human reviewer judged an output correctly.

## Provenance boundary

A valid run record requires a full 40-character Git commit hash that exists in repository history and working_tree_clean: true. Prompt and response artifact paths must also exist inside the repository. This intentionally prevents an uncommitted working tree or detached summary from being presented as release-grade behavior evidence. The evidence record may be committed after the evaluated source revision. Draft experiments may be kept elsewhere, but they do not satisfy the release gate.

This file owns behavior-run provenance only. The full six-link release chain—including templates, hosted CI, and fresh installs—is documented in [RELEASE-EVIDENCE-CHAIN.md](RELEASE-EVIDENCE-CHAIN.md).
