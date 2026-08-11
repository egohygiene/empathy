# MegaLinter v10 policy completion audit

**Date:** 2026-08-11

**Scope:** MegaLinter-native configuration, profiles, fixtures, and offline
contract validation

**Outcome:** Policy complete; repository findings intentionally remain visible

## Executive summary

The repository now has one holistic default and one explicit fast profile.
MegaLinter's official `v10.0.0` release is represented by a compact offline
catalog containing 124 supported tools, 2,716 valid configuration variables,
368 deprecated variables, and the removed linter/descriptor inventory.

The generated tool matrix joins that upstream inventory with repository-owned
configuration, versions, applicability, fixture evidence, profile selection,
disabled reasons, and report destinations. Unknown or silently removed
configuration is now a unit-test failure rather than a runtime notice.

## Profile contract

| Profile          | Configuration                   | Scope               | Selected tools |
| ---------------- | ------------------------------- | ------------------- | -------------: |
| Holistic/default | `.mega-linter.yml`              | Complete repository |            107 |
| Fast             | `egolint/.mega-linter.fast.yml` | Changed files       |             12 |

`task lint` and `task lint:holistic` select the holistic profile.
`task lint:fast` and pull-request CI select the fast profile. Trusted pushes and
manual workflow dispatch retain the holistic profile. PR 4 will add scheduling
and report publication without changing these selection semantics.

## Newly active holistic capabilities

- `PYTHON_RUFF_FORMAT` shares the canonical Ruff policy with `PYTHON_RUFF`.
- `JSON_V8R` shares the SchemaStore policy already used by `YAML_V8R`.
- `ENV_DOTENV_LINTER` validates committed environment examples.
- `C_CPPCHECK` and `CPP_CPPCHECK` use explicit safety-focused argument policy.
- `TERRAFORM_TERRAFORM_FMT` provides check-only Terraform formatting.

These are holistic capabilities only. The fast profile remains unchanged until
their repository baselines have proven suitable for tight feedback loops.

## Configured but deliberately disabled

| Tool                     | Activation blocker                                         |
| ------------------------ | ---------------------------------------------------------- |
| `ACTION_ZIZMOR`          | Review existing workflow security findings                 |
| `SPELL_CODESPELL`        | Classify repository spelling baseline                      |
| `REPOSITORY_SEMGREP`     | Review initial local semantic rules                        |
| `REPOSITORY_KINGFISHER`  | Measure overlap with existing secret scanners              |
| `HTML_DJLINT`            | Add a real template project and compare HTMLHint ownership |
| `GO_GOLANGCI_LINT`       | Prove project discovery with a representative Go module    |
| `KUBERNETES_KUBECONFORM` | Define an offline schema-cache policy                      |
| `KUBERNETES_HELM`        | Add a representative self-contained chart                  |
| `KUBERNETES_KUBESCAPE`   | Review a Kubernetes security baseline                      |
| `PYTHON_NBQA_MYPY`       | Define a deterministic notebook dependency environment     |
| `MARKDOWN_RUMDL`         | Compare rules with canonical Markdownlint policy           |

Existing explicit disables remain preserved for DevSkim, JSX ESLint, Black,
Flake8, and isort. Each has a machine-readable ownership reason.

## Security and supply-chain ownership

- Betterleaks remains the MegaLinter-native canonical secret scanner and
  consumes the existing Gitleaks TOML.
- Secretlint remains the structured content scanner.
- Checkov owns IaC scanning previously associated with removed KICS and
  Terrascan descriptors.
- Syft, Trivy, Trivy SBOM, and Grype retain separate native report contracts.
- The MegaLinter OSV descriptor is explicitly disabled because the dedicated
  OSV workflow owns discovery, severity policy, normalized reports, and SARIF.
- Semgrep and Kingfisher are configured but disabled until their independent
  signal and runtime costs are baselined.

No MegaLinter-native tool gained a duplicate GitHub workflow.

## Fixture and configuration evidence

Every newly evaluated tool has:

- a real config path when the tool accepts a config file;
- explicit arguments when MegaLinter exposes no config-file contract;
- applicability patterns or project markers;
- a positive and isolated negative fixture, or a named blocker;
- an expected rule/outcome identifier where stable.

Negative fixtures live beneath `egolint/tests/fixtures/negative/`. They are
excluded from aggregate formatters and scanners and are intended only for
isolated fixture verification. This prevents deliberately invalid material from
making every repository scan fail while preserving evidence for future
container contract tests.

## Removed-linter enforcement

The validator rejects removed selections and deprecated variables even though
MegaLinter v10's JSON schema intentionally continues accepting them for
migration compatibility. Regression tests specifically cover the removed
`API_SPECTRAL` variable family and `REPOSITORY_GITLEAKS` selection.

Canonical responsibility mappings remain:

| Removed capability  | Current owner                               |
| ------------------- | ------------------------------------------- |
| Gitleaks descriptor | Betterleaks                                 |
| KICS and Terrascan  | Checkov and Trivy                           |
| TSQLLint            | SQLFluff with T-SQL dialect                 |
| Markdown Link Check | Lychee                                      |
| Remark              | Markdownlint; Rumdl under evaluation        |
| JSONC ESLint        | JSONLint, V8R, and Prettier                 |
| Spectral            | Preserved rules for the PR 3 Vacuum adapter |

## Validation evidence

- Offline v10 contract: 124 supported tools validated.
- Profile snapshots: 12 fast and 107 holistic tools.
- Root unit tests: 15 passed.
- Egolint unit tests: 11 passed.
- JSON, TOML, and YAML parsing: passed.
- Ruff 0.16.2 lint and formatting for new Python code: passed.
- Canonical Prettier formatting: passed.
- Git whitespace validation: passed.

A full local MegaLinter container run remains unavailable because this runtime
has neither Docker nor Podman. The pinned GitHub Action is the authoritative
container execution environment and will validate actual linter startup,
configuration loading, skips, and findings on this PR.

## Deferred boundaries

This pass does not implement complementary adapters, VS Code parity, dependency
remediation, report commits, Node 24 migration, infographic generation, the
Egolint CLI, a production container, or Ego Hygiene-specific policy bundles.
Those remain assigned to PR 3, PR 4, and the later Egolint product sequence.
