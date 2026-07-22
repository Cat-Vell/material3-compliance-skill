# Hosted CI Ledger

Fill one row per successful remote workflow run that should count toward a release claim. Leave empty until a remote exists.

| Date (UTC) | Git revision | Workflow / run URL | Jobs green | Notes |
|---|---|---|---|---|
| _pending_ | _pending_ | _pending_ | validate · compose-core · flutter-core · web-core | First push after initial commit |

## Recording rules

- Prefer the full 40-character SHA.
- Link the Actions run (or equivalent) that rebuilt the three cores and ran validators.
- Tag pushes additionally exercise `behavior-release-gate`; do not claim a `v*` release until that job is green with archived Codex and Claude runs.
- If a job is skipped or flaky, say so; do not mark the chain link complete.
