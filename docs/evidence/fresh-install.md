# Fresh Install Ledger

Record one row per distribution surface named in public docs. Passing install evidence is required only for surfaces you claim.

| Date (UTC) | Surface | Git revision / package ref | Install steps used | Invoke check | Result | Operator | Notes |
|---|---|---|---|---|---|---|---|
| _pending_ | Cursor (`~/.cursor/skills/material3-design`) | _pending_ | copy or link runtime package | prompt with `$material3-design` | _pending_ | | Sync personal skill with repo package |
| 2026-07-22 | Codex installer-managed (`$CODEX_HOME/skills/material3-design`) | uncommitted working-tree copy | copy runtime package | byte-for-byte tree comparison and official skill validation; invocation awaits a new session | partial | Codex | Not a clean or revision-anchored fresh-install pass |
| _pending_ | Codex authoring/discovery (`$HOME/.agents/skills/material3-design` or repository `.agents/skills`) | _pending_ | | | _pending_ | | |
| _pending_ | Claude plugin / marketplace | _pending_ | | | _pending_ | | |
| _pending_ | `npx skills` | _pending_ | | | _pending_ | | Only after the repository is public |

## Recording rules

- Use a clean machine or a clean skills directory when claiming “fresh.”
- Keep the runtime folder name `material3-design`.
- Note host/app version when known.
- Failure or partial success stays on the ledger; do not delete rows to hide gaps.
