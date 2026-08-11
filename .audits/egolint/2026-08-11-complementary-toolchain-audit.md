# Complementary toolchain and editor-parity audit

**Date:** 2026-08-11

**Scope:** Direct non-MegaLinter tools, applicability, Taskfile contracts, VS
Code parity, and supply-chain ownership

**Outcome:** Complementary platform complete; CI publication remains deferred

## Architecture

MegaLinter continues to own every tool represented by its v10 descriptors. The
complementary layer owns tools that require a direct command, a project-aware
activation rule, editor integration, or a specialized local contract.

The source manifest is
`egolint/.config/toolchain/complementary-tools.json`. The generated
`tool-matrix.json` is the machine-readable handoff to PR 4's infographic and
report-publishing work. Native configurations remain authoritative; the matrix
points to them instead of copying rule policy.

## Result model

Applicability and execution are separate dimensions:

| State                   | Meaning                                                     |
| ----------------------- | ----------------------------------------------------------- |
| `applicable`            | All required repository markers exist.                      |
| `not_applicable`        | The project or file markers do not exist.                   |
| `missing_dependency`    | The project applies, but its pinned runtime is unavailable. |
| `deliberately_disabled` | Policy explicitly disables the tool with a reason.          |
| `passed`                | The direct command completed without findings.              |
| `failed_findings`       | The tool ran and reported policy findings.                  |
| `execution_error`       | The command could not execute correctly.                    |
| `timed_out`             | The command exceeded its bounded runtime.                   |

Fixtures never activate a tool for the repository itself. A lone `go` fixture,
for example, cannot make govulncheck appear applicable to a repository without
a real Go module.

## Complementary inventory

| Tool           | Version | Ownership                               | Repository state |
| -------------- | ------: | --------------------------------------- | ---------------- |
| Tombi          |  1.2.10 | TOML parser, formatter, linter, and LSP | Enabled          |
| REUSE          |   6.2.0 | Source copyright and licensing          | Enabled          |
| Commitlint     |  21.2.1 | Emoji commit-message policy             | Enabled          |
| typos          |  1.32.0 | Identifier and prose typos              | Enabled          |
| Vacuum         |  0.30.0 | Spectral-compatible API descriptions    | Conditional      |
| latexindent    |     4.0 | LaTeX formatting                        | Conditional      |
| detect-secrets |   1.5.0 | Reviewed-baseline secret gate           | Enabled          |
| addlicense     |   1.2.0 | Compatible MIT/SPDX header insertion    | Enabled          |
| Knip           |  6.32.1 | JavaScript/TypeScript unused surface    | Conditional      |
| deptry         |  0.24.0 | Python dependency declarations          | Conditional      |
| cargo-deny     |  0.20.2 | Rust dependency policy                  | Conditional      |
| govulncheck    |   1.1.4 | Reachable Go vulnerabilities            | Conditional      |
| Buf            |  1.72.0 | Protocol Buffer module policy           | Conditional      |
| Regal          |  0.42.0 | Rego language and style policy          | Conditional      |
| Conftest       |  0.69.0 | Policy-as-code assertions               | Conditional      |
| Vulture        |    2.16 | High-confidence dead Python code        | Conditional      |
| interrogate    |   1.7.0 | Python docstring coverage               | Conditional      |
| complexipy     |   7.0.0 | Python cognitive complexity             | Conditional      |

## Taskfile contract

- `task lint` and `task lint:holistic` remain the holistic MegaLinter profile.
- `task lint:fast` remains the deterministic changed-file profile.
- `task lint:complementary` runs applicable direct tools.
- `task lint:contracts` validates both generated inventories.
- `task security:source` composes Detect Secrets, Betterleaks, and Secretlint.
- `task security:dependencies` composes Grype and Trivy.
- `task sbom:generate` composes Syft SPDX/CycloneDX and Trivy CycloneDX.
- `task sbom:scan` consumes the dependency-vulnerability contract.
- `task tools:status` and `task tools:versions` are non-mutating diagnostics.
- `task tools:install` installs the locked Python lint group.
- `task tools:install:security` installs the separately locked security group.

The security and developer groups are declared as incompatible because
current Checkov constrains `packaging` below 24 while current Commitizen requires
`packaging` 26 or newer. uv resolves both variants in one portable lock but
prevents them from being installed into the same environment. This preserves
both capabilities without hiding or overriding an upstream incompatibility.

`egolint/pnpm-workspace.yaml` also records pnpm 11's dependency-build policy.
Only the native build steps required by the checked-in toolchain (`@swc/core`,
esbuild, Nx, protobufjs, and unrs-resolver) are allowed; telemetry, donation,
optional acceleration, and unrelated product-package scripts are explicitly
denied. Installs therefore remain non-interactive without globally enabling
dependency lifecycle scripts.

## Supply-chain ownership

| Concern                               | Canonical owner        | Destination                          |
| ------------------------------------- | ---------------------- | ------------------------------------ |
| Source-file copyright and licensing   | REUSE                  | `.reports/complementary/reuse/`      |
| Compatible source headers             | addlicense             | `.reports/complementary/addlicense/` |
| Dependency inventories                | Syft and Trivy SBOM    | `.reports/megalinter/`               |
| SBOM/package vulnerabilities          | Grype and Trivy        | `.reports/megalinter/`               |
| Manifest and lockfile vulnerabilities | Dedicated OSV workflow | `.reports/osv/`                      |

These signals remain separate. PR 4 may publish or summarize them, but it must
not merge unlike findings into an ambiguous pass/fail result.

## VS Code parity

The root `.vscode/` directory owns extension recommendations, formatter
ownership, canonical config paths, and tasks. Both workspace files now contain
only folder, terminal, telemetry, and visual preferences. Every VS Code task
delegates to Taskfile rather than reproducing a tool command.

Formatter ownership is single-valued per language: Ruff for Python, Tombi for
TOML, shfmt for shell, LaTeX Workshop/latexindent for LaTeX, SQLFluff for SQL,
OPA for Rego, and Prettier for supported web, data, and prose formats.

## Deferred boundary

This PR does not add scheduled workflows, trusted report commits, the reusable
report-publishing action, Node 24 migration, the generated architecture
infographic, the Egolint CLI, typed adapters, or production packaging. Those
remain PR 4 and the later product sequence.
