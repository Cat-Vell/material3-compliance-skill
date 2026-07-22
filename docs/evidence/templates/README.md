# Evidence Templates

Copy these shapes when creating real records. Files in this directory are **not** release evidence.

| Template | Use for |
|---|---|
| [run-record.example.json](run-record.example.json) | Shape reference before writing `evals/runs/<run-id>.json` |

Real behavior records must:

1. Match `evals/run-record.schema.json`
2. Use a real fixture digest and assertion arrays from `evals/fixtures/`
3. Point `git_revision` at an existing full SHA with a clean evaluated tree
4. Store prompt/response artifacts inside the repository
5. Pass `python tests/validate_eval_runs.py`

Never place this example file under `evals/runs/`.
