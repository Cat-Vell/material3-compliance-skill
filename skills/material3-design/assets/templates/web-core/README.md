# Web Core Template

Dependency-free semantic Material 3 token theme and responsive shell. It intentionally uses native HTML rather than claiming unsupported official component parity. Add verified `@material/web` elements selectively when the host build and source review support them.

Tested baseline (not “latest”): Node 24.18.0 LTS, npm 11.16.0, lockfile v3, and zero runtime dependencies. Source IDs: S-NODE, S-M3-WEB, S-WEB-REPO; verified 2026-07-22. `npm ci`, `npm run build`, two unit tests, and six accessibility smoke checks passed locally on 2026-07-22; rerun them in release CI. The accessibility check is a smoke test, not certification.
