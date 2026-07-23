# Scanner maintainer guide

The Material 3 scanner is a **heuristic evidence collector**. It reports risks with stable rule IDs; it does not score audits, grant release gates, autofix code, or certify accessibility.

## Layout

```text
skills/material3-design/scripts/
  m3_scan.py              # CLI (compatible entry point)
  m3_engine/              # discovery, suppressions, rendering, benchmark
  rules/
    compose/<slug>/       # RULE metadata + fixtures/ + metrics.json
    flutter/<slug>/
    web/<slug>/
```

Each rule exports a `RULE` dict with: `rule_id`, `title`, `dimension`, `severity` (`blocker`|`warning`), `confidence` (`high`|`medium`), `platform`, `source_id`, `autofix` (always `false`), `matcher` (`regex`|`whole_file`), remediation, and either `pattern` or `check`.

Matchers stay regex/whole-file for now. AST or language-server analysis is a later phase for Kotlin, Dart, and JavaScript — do not grow unbounded regex for structural questions.

## Suppressions

1. Inline or previous-line comment: `m3-ignore: M3-002`
2. File header: `m3-ignore-file: M3-002,M3-009`
3. Project config `.m3scan.json`:

```json
{ "suppress": [{ "rule_id": "M3-006", "path": "docs/**", "reason": "docs sample" }] }
```

Invalid JSON or suppression schema is a configuration error and exits with status `2`; it is never silently ignored.

`M3-002` also skips paths whose stem/parts include `theme`, `token`, `color`, `palette`, `baseline`, or `test`.

## Adding a rule

1. Create `rules/<platform>/<slug>/` with `__init__.py`, `fixtures/{positive,negative,edge_*}.*`, and `metrics.json`.
2. Point `source_id` at an ID in `references/shared/source-registry.md`.
3. Keep `autofix: false`.
4. Run:

```bash
python -m unittest tests.test_scanner_rules tests.test_suppressions tests.test_m3_scan
python skills/material3-design/scripts/m3_engine/benchmark.py
```

## Fixture benchmark (2026-07-23)

| Rule | Platform | Title | Precision | Recall | Fixtures | Source |
|---|---|---|---:|---:|---:|---|
| M3-001 | compose | m2_import | 1.00 | 1.00 | 3 | S-MIG-COMP |
| M3-002 | compose | hardcoded_color | 1.00 | 1.00 | 3 | S-COMP-M3 |
| M3-003 | compose | missing_theme | 1.00 | 1.00 | 3 | S-COMP-M3 |
| M3-004 | compose | unstable_api | 1.00 | 1.00 | 3 | S-COMP-REL |
| M3-005 | compose | device_nav | 1.00 | 1.00 | 3 | S-ADAPT |
| M3-007 | compose | text_field_ime | 1.00 | 1.00 | 3 | S-INSETS |
| M3-008 | compose | non_semantic_clickable | 1.00 | 1.00 | 3 | S-COMP |
| M3-009 | compose | icon_button_label | 1.00 | 1.00 | 3 | S-COMP |
| M3-011 | compose | missing_responsive | 1.00 | 1.00 | 3 | S-ADAPT |
| M3-002 | flutter | hardcoded_color | 1.00 | 1.00 | 3 | S-FLUTTER |
| M3-003 | flutter | missing_theme | 1.00 | 1.00 | 3 | S-FLUTTER |
| M3-004 | flutter | unstable_api | 1.00 | 1.00 | 3 | S-FLUTTER-W |
| M3-005 | flutter | device_nav | 1.00 | 1.00 | 3 | S-FLUTTER |
| M3-007 | flutter | text_field_ime | 1.00 | 1.00 | 3 | S-FLUTTER |
| M3-009 | flutter | icon_button_label | 1.00 | 1.00 | 3 | S-FLUTTER-W |
| M3-011 | flutter | missing_responsive | 1.00 | 1.00 | 3 | S-FLUTTER |
| M3-002 | web | hardcoded_color | 1.00 | 1.00 | 3 | S-M3-WEB |
| M3-003 | web | missing_theme | 1.00 | 1.00 | 3 | S-M3-WEB |
| M3-004 | web | unstable_api | 1.00 | 1.00 | 3 | S-WEB-REPO |
| M3-006 | web | fixed_position | 1.00 | 1.00 | 3 | S-WEB-A11Y |
| M3-008 | web | non_semantic_clickable | 1.00 | 1.00 | 3 | S-WEB-A11Y |
| M3-010 | web | deprecated_mdc | 1.00 | 1.00 | 3 | S-WEB-REPO |
| M3-011 | web | missing_responsive | 1.00 | 1.00 | 3 | S-M3-WEB |

Scope: scanner fixture benchmark only; archived host runs remain zero until `evals/runs/` is populated.
