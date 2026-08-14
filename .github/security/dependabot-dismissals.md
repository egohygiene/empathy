# Dependabot dismissal register

This register mirrors the narrow, GitHub-hosted Dependabot dismissals for
unavailable upstream fixes. It is not a scanner suppression mechanism:
Dependabot alert state is managed in GitHub, while `osv-scanner.toml` keeps the
equivalent OSV policy machine-readable.

## Current reviewed dismissals

| Package | Advisory IDs | Scope | Reason | Reassess when |
| --- | --- | --- | --- | --- |
| `decompress` | `GHSA-mp2f-45pm-3cg9`, `GHSA-h39j-r5qq-r9mm`, `GHSA-jwp9-9v96-94mx` | Transitive development dependency of ShellCheck tooling in `egolint/pnpm-lock.yaml` | The advisory's named patched release is not published to npm. The package is not shipped in a production artifact. | An upstream fixed release becomes available or the tooling dependency is removed. |
| `ecdsa` | `GHSA-wj6h-64fc-37mp`, `PYSEC-2026-1325` | Transitive development dependency of Checkov in `egolint/uv.lock` | No patched PyPI release is available. The package is not shipped in a production artifact. | An upstream fixed release becomes available or the tooling dependency is removed. |

Do not add broad package or ecosystem dismissals here. Each entry must identify
the advisory, dependency path, non-production scope, and a concrete reopening
condition. Alerts that have a published upgrade path remain open and must be
remediated rather than registered here.
