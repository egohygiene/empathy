# OSV Vulnerability Scan

- Generated: `2026-08-14T01-27-29Z`
- Repository: `egohygiene/empathy`
- Commit: `aff007deadd35b149c0d1212fd0a6698bb5913db`
- Severity gate: `high`
- Duration: `8s`

## Findings

| Severity | Count |
| --- | ---: |
| Critical | 0 |
| High | 2 |
| Medium | 2 |
| Low | 0 |
| Unknown | 0 |
| **Total** | **4** |

## Discovery

Discovered 16 artifact(s) across 5 ecosystem label(s).

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


Total 4 packages affected by 4 known vulnerabilities (0 Critical, 2 High, 2 Medium, 0 Low, 0 Unknown) from 2 ecosystems.
0 vulnerabilities can be fixed.

| OSV URL | CVSS | Ecosystem | Package | Version | Fixed Version | Source |
| --- | --- | --- | --- | --- | --- | --- |
| https://osv.dev/PYSEC-2026-1325<br/>https://osv.dev/GHSA-wj6h-64fc-37mp | 7.4 | PyPI | ecdsa | 0.19.2 | -- | egolint/uv.lock |
| https://osv.dev/PYSEC-2023-242 | 7.4 | PyPI | httpie | 3.2.4 | -- | egolint/uv.lock |
| https://osv.dev/GHSA-848j-6mx2-7j84 | 5.6 | npm | elliptic | 6.6.1 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-g3ch-rx76-35fx | 4.2 | npm | vue-template-compiler | 2.7.16 | -- | egolint/pnpm-lock.yaml |
