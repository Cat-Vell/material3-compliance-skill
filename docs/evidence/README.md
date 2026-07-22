# Evidence Ledgers

Working records that fill the [release evidence chain](../RELEASE-EVIDENCE-CHAIN.md). Keep them outside `skills/material3-design/` so the runtime package stays lean.

| Ledger | Purpose |
|---|---|
| [local-verification.md](local-verification.md) | Machine-local stable-template checks |
| [hosted-ci.md](hosted-ci.md) | Remote CI runs tied to a Git revision |
| [fresh-install.md](fresh-install.md) | Distribution-surface install and invoke checks |
| [templates/](templates/) | Copy-paste schemas; not release evidence by themselves |

Do not place real behavior run records here. Those belong in `evals/runs/` and must satisfy `tests/validate_eval_runs.py`.
