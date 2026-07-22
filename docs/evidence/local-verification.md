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
| Notes | Pre-history local evidence; re-verify after first commit on a clean tree |

## Flutter core

| Field | Value |
|---|---|
| Subject path | `skills/material3-design/assets/templates/flutter-core` |
| Commands | `dart format --output=none --set-exit-if-changed .` · `flutter analyze` · `flutter test` |
| Result | pass (recorded in `baseline.json`) |
| Date | 2026-07-22 |
| Environment | Flutter 3.44.1 / Dart 3.12.1 |
| Operator | local maintainer |
| Hosted CI URL | _pending first remote run_ |
| Notes | Pre-history local evidence |

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
| Notes | Includes unit tests and a11y smoke; pre-history local evidence |

## Repository validators (local)

| Field | Value |
|---|---|
| Commands | `python -m unittest discover -s tests -p "test_*.py"` · `python tests/validate_fixtures.py` · `python tests/validate_eval_runs.py` · `python tests/validate_repository.py` |
| Result | pass on 2026-07-22 |
| Behavior runs | 0 archived records (explicit “no host behavior evidence”) |
| Notes | Re-run on a clean tree after the first commit |
