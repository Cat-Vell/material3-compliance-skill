# Local Verification Ledger

Records machine-local stable-template checks. Local green promotes a template to a tested baseline; it does **not** replace hosted CI for a public release.

## Compose core

| Field | Value |
|---|---|
| Subject path | `skills/material3-design/assets/templates/compose-core` |
| Commands | `gradle testDebugUnitTest assembleDebug` |
| Result | pass (recorded in `baseline.json`) |
| Date (UTC context) | 2026-07-22 |
| Environment | JDK 17.0.19, Gradle 9.5.0, AGP 9.3.0, API 37 |
| Operator | local maintainer |
| Hosted CI URL | _pending first remote run_ |
| Notes | Local evidence predates the initial import; re-verify the release subject on a clean tree |

## Flutter core

| Field | Value |
|---|---|
| Subject path | `skills/material3-design/assets/templates/flutter-core` |
| Commands | `dart format --output=none --set-exit-if-changed .` · `dart analyze` · `flutter test --no-pub` |
| Result | pass for formatting, `dart analyze`, and two widget tests (recorded in `baseline.json`) |
| Date | 2026-07-22 |
| Environment | Flutter 3.44.1 / Dart 3.12.1 |
| Operator | local maintainer |
| Hosted CI URL | _pending first remote run_ |
| Notes | `flutter analyze` itself failed in the non-ASCII Windows path because its analysis-server wrapper returned truncated JSON; hosted Ubuntu CI must run the official command |

## Web core

| Field | Value |
|---|---|
| Subject path | `skills/material3-design/assets/templates/web-core` |
| Commands | `npm ci` · `npm run build` · `npm test` |
| Result | pass (recorded in `baseline.json`) |
| Date | 2026-07-22 |
| Environment | Node 24.18.0 / npm 11.16.0 |
| Operator | local maintainer |
| Hosted CI URL | _pending first remote run_ |
| Notes | Includes unit tests and a11y smoke; local evidence predates the initial import |

## Repository validators (local)

| Field | Value |
|---|---|
| Commands | `python -m unittest discover -s tests -p "test_*.py"` · `python tests/validate_fixtures.py` · `python tests/validate_eval_runs.py` · `python tests/validate_repository.py` |
| Result | pass on 2026-07-22 |
| Behavior runs | 0 archived records (explicit “no host behavior evidence”) |
| Notes | Re-run after committing the reviewed changes and before recording release evidence |

## Distribution metadata

| Field | Value |
|---|---|
| Command | `claude plugin validate .` |
| Tool | Claude Code 2.1.217 on Node 24.18.0 (temporary local install) |
| Result | pass with one expected warning: development manifest intentionally omits SemVer |
| Date | 2026-07-22 |
| Notes | The sole warning is intentional for active development: SemVer is added only for a release; hosted/fresh-install validation remains required |
