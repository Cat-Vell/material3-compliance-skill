# Material 3 Build + Audit Skill

Routes Material 3 design, build, migration, and audit work through platform-honest contracts, golden-path recipes, and heuristic scan evidence — so outputs stay integration-ready without claiming host-behavior certificates that are not yet archived.

Compared with asking a model directly: this skill forces semantic tokens, state/accessibility coverage, adaptive window context, API status honesty (`stable` / `verify-current` / `unsupported/custom`), and risk-matched output profiles (Lite / Standard / Evidence).

## Install

From this repository root (Cursor):

```powershell
New-Item -ItemType Junction -Force -Path "$HOME\.cursor\skills\material3-design" -Target "$PWD\skills\material3-design"
```

Keep the folder name `material3-design`. Other hosts can link the same folder into their skill directory (`~/.codex/skills`, `~/.claude/skills`, `.agents/skills`).

## Standard task entry points

```text
$material3-design component — build a Material 3 Button / TextField / IconButton with states and a11y notes
$material3-design theme — ship light/dark ColorScheme, type, and shapes (Dynamic Color gated)
$material3-design layout — adaptive list-detail or pane layout from window context, not device labels
$material3-design scaffold — adaptive app shell for 3–5 destinations with selection continuity
$material3-design migrate — staged M2→M3 or MDC migration with inventory, bridge, and rollback
$material3-design audit — score D01–D10, mark missing evidence U, separate Must-fix from Nice-to-have
```

**Design (no code yet)**

```text
Use $material3-design to design a responsive list-detail inbox. Define theme roles, component jobs, states, navigation, accessibility, and the Design-to-Build handoff. Do not write code yet.
```

**Build**

```text
Use $material3-design to build the Material 3 theme and adaptive app shell in this Compose project. Preserve its architecture, use stable APIs, add state/accessibility tests, run the scanner, and report the Standard output profile.
```

**Audit**

```text
Use $material3-design in Audit mode on these screens and files. Score D01–D10, mark missing evidence U, justify every n/a, apply release gates, and separate Must-fix from Nice-to-have.
```

## Output shape (illustrative)

Without the skill, a “make a Compose theme” request often returns a single light `ColorScheme` snippet and no dark/Dynamic Color/fallback path.

With Lite/Standard profiles, the same request leads with the theme files, then states the API status, light/dark/dynamic/fallback paths, and a verification note — without narrating internal routing. Full contracts live in `skills/material3-design/SKILL.md`.

## Benchmark

Host-behavior results: [BENCHMARK.md](BENCHMARK.md) (generated from `evals/runs/`). **Archived host behavior runs: 0** — no with-skill / baseline comparison is claimed yet.

| Metric | Without skill | With skill |
|---|---:|---:|
| Compile pass rate | — | — |
| Critical assertion pass rate | — | — |
| Forbidden / invented API claims | — | — |
| Average token cost | — | — |

Regenerate after archiving runs:

```bash
python evals/benchmark_report.py
```

### Scanner fixture benchmark

Heuristic rules only — measured against packaged positive/negative/edge fixtures. Not a host-behavior or accessibility certificate.

| Metric | Value |
|---|---|
| Rule modules | 23 (IDs `M3-001`–`M3-011` across Compose / Flutter / Web) |
| Mean precision | 1.00 |
| Mean recall | 1.00 |
| Fixtures per module | 3 |
| Archived host behavior runs | 0 |

```bash
python skills/material3-design/scripts/m3_scan.py <path> --platform auto --format markdown
python skills/material3-design/scripts/m3_engine/benchmark.py
```

Exit `0` = no high-confidence blockers; `1` = blockers found; `2` = invalid input. Full rule table: [docs/SCANNER.md](docs/SCANNER.md).

## Support levels

Guidance is **covered** for three platforms; host-behavior is **verified** only where `evals/runs/` holds records (currently none).

| Platform | Support | Honesty boundary |
|---|---|---|
| Jetpack Compose | Primary / full depth (verified target) | Stable APIs by default; Expressive, experimental, and Navigation 3 are verified per project |
| Flutter | Secondary / production-focused (preview until host runs exist) | Official widgets and ThemeData; no Compose Expressive parity promise |
| Web | Limited / experimental until host runs exist | Verified `@material/web` exports or accessible native/custom fallbacks; full Expressive parity refused |

## Verified hosts and versions

| Surface | Status |
|---|---|
| Cursor / Codex / Claude host behavior | Not archived yet (`evals/runs/` empty) |
| Compose template baseline | JDK 17, Gradle 9.5.0, AGP 9.3.0, Compose BOM `2026.06.00` (local pass 2026-07-22) |
| Flutter template baseline | Flutter 3.44.1 / Dart 3.12.1 (local format/analyze/tests pass 2026-07-22) |
| Web template baseline | Node 24.18.0 / npm 11.16.0 (local build/test pass 2026-07-22) |

Pinned versions are tested baselines, never “latest.”

## Limitations

- The scanner collects heuristic evidence; it does not certify Material 3 or WCAG compliance.
- Automated scans and a11y smoke tests do not replace manual accessibility evidence.
- Web support refuses full M3 / Expressive parity claims.
- Flutter does not promise Compose Expressive feature parity.
- Volatile APIs require a first-party source check before use.
- Community dependencies are not recommended unless requested and risk-reviewed.
- No public owner or marketplace release is claimed by this working tree.

## Maintainer docs

Evidence chain, capability matrix, evals, and release gates live under [docs/](docs/) — start with [RELEASE-EVIDENCE-CHAIN.md](docs/RELEASE-EVIDENCE-CHAIN.md) and [SCANNER.md](docs/SCANNER.md). Runtime package: `skills/material3-design/` (`SKILL.md`, `references/{shared,compose,flutter,web,audit,recipes}/`, `scripts/`, `assets/`). Behavior matrix tooling: `evals/generate_run_matrix.py`, `evals/benchmark_report.py`, `evals/trigger/`.

## License

Original repository content is released under the [MIT License](LICENSE). Material and third-party sources remain under their own terms; see [NOTICE.md](NOTICE.md).
