# OSV Vulnerability Scan

- Generated: `2026-08-14T12-41-52Z`
- Repository: `egohygiene/empathy`
- Commit: `00db8081fa1dfedaf51a45b4726697303c8fcb88`
- Severity gate: `high`
- Duration: `8s`

## Findings

| Severity | Count |
| --- | ---: |
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 0 |
| Unknown | 0 |
| **Total** | **2** |

## Discovery

Discovered 17 artifact(s) across 6 ecosystem label(s).

- `.reports/megalinter/syft/sbom.spdx.json`
- `egolint/.config/lint/python/pyproject.toml`
- `egolint/Cargo.lock`
- `egolint/package.json`
- `egolint/pnpm-lock.yaml`
- `egolint/pyproject.toml`
- `egolint/tests/fixtures/dart-analyzer/pubspec.lock`
- `egolint/tests/fixtures/deptry/pyproject.toml`
- `egolint/tests/fixtures/govulncheck/go.mod`
- `egolint/tests/fixtures/knip/package.json`
- `egolint/tests/fixtures/negative/deptry/pyproject.toml`
- `egolint/tests/fixtures/negative/knip/package.json`
- `egolint/tests/fixtures/negative/v8r/package.json`
- `egolint/tests/fixtures/npm-package-json-lint/package.json`
- `egolint/tests/fixtures/v8r/package.json`
- `egolint/uv.lock`
- `pyproject.toml`

## Scanned Files

- `egolint/Cargo.lock`
- `egolint/pnpm-lock.yaml`
- `egolint/uv.lock`

## Skipped Discovered Files

- `.reports/megalinter/syft/sbom.spdx.json`
- `egolint/.config/lint/python/pyproject.toml`
- `egolint/package.json`
- `egolint/pyproject.toml`
- `egolint/tests/fixtures/dart-analyzer/pubspec.lock`
- `egolint/tests/fixtures/deptry/pyproject.toml`
- `egolint/tests/fixtures/govulncheck/go.mod`
- `egolint/tests/fixtures/knip/package.json`
- `egolint/tests/fixtures/negative/deptry/pyproject.toml`
- `egolint/tests/fixtures/negative/knip/package.json`
- `egolint/tests/fixtures/negative/v8r/package.json`
- `egolint/tests/fixtures/npm-package-json-lint/package.json`
- `egolint/tests/fixtures/v8r/package.json`
- `pyproject.toml`

## OSV Scanner Report


Total 2 packages affected by 2 known vulnerabilities (0 Critical, 0 High, 2 Medium, 0 Low, 0 Unknown) from 1 ecosystem.
0 vulnerabilities can be fixed.

| OSV URL | CVSS | Ecosystem | Package | Version | Fixed Version | Source |
| --- | --- | --- | --- | --- | --- | --- |
| https://osv.dev/GHSA-848j-6mx2-7j84 | 5.6 | npm | elliptic | 6.6.1 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-g3ch-rx76-35fx | 4.2 | npm | vue-template-compiler | 2.7.16 | -- | egolint/pnpm-lock.yaml |
