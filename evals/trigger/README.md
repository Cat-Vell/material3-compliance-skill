# Trigger evaluation results (example only)

Copy this shape when recording whether the host activated `material3-design` for each case in `cases.json`.

```json
{
  "host": "codex",
  "model": "example-model",
  "skill_commit": "REPLACE_WITH_40_CHAR_SHA",
  "reviewed_at": "2026-07-23T00:00:00Z",
  "results": [
    {"id": "st-01", "observed": "trigger"},
    {"id": "sn-01", "observed": "no-trigger"},
    {"id": "nm-01", "observed": "no-trigger"}
  ]
}
```

Do not treat a partial example as release evidence. Score with:

```bash
python evals/trigger/score_trigger_runs.py --results evals/trigger/results.example.json --require-pass
```
