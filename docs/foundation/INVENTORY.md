# Generated repository foundation inventory

> Generated from `foundation/catalog.json`. Do not edit by hand.

- Contract: `empathy/repository-foundation@1.0.0`
- Canonical owner: `egohygiene/empathy`
- Canonical artifacts: `30`

| Path | Category | Presence | Ownership | Profiles | Description |
| --- | --- | --- | --- | --- | --- |
| `.editorconfig` | metadata | required | required | — | Cross-editor whitespace and line-ending baseline |
| `.gitattributes` | metadata | required | required | — | Git text, EOL, binary, and generated-file behavior |
| `.github/CODEOWNERS` | community-health | profile | repository-owned | community-health | Repository review ownership |
| `.github/ISSUE_TEMPLATE/config.yml` | community-health | profile | required | community-health | Issue intake configuration |
| `.github/PULL_REQUEST_TEMPLATE.md` | community-health | profile | repository-owned | community-health | Repository review checklist |
| `.github/copilot-instructions.md` | agent-context | profile | repository-owned | agent-context | Repository-specific Copilot projection |
| `.github/dependabot.yml` | security | profile | repository-owned | risk-hardened | Repository ecosystem dependency update intent |
| `.github/workflows/codeql.yml` | security | profile | required | risk-hardened | Static security analysis caller |
| `.github/workflows/dependency-review.yml` | security | profile | required | risk-hardened | Dependency change gate |
| `.github/workflows/megalinter.yml` | quality | profile | required | quality-baseline | Thin repository caller for reusable quality automation |
| `.gitignore` | metadata | required | repository-owned | — | Repository-specific generated and local-state exclusions |
| `.identity/identity.toml` | metadata | profile | repository-owned | product | Consumer-owned product identity input |
| `.mega-linter.yml` | quality | profile | repository-owned | quality-baseline | Repository-selected EgoLint and MegaLinter policy overlay |
| `.release-please-manifest.json` | release | profile | repository-owned | release-automated | Repository release state |
| `.secrets.baseline` | security | profile | repository-owned | risk-hardened | Reviewed repository secret-scanner baseline |
| `AGENTS.md` | agent-context | profile | repository-owned | agent-context | Concise repository-specific agent entrypoint |
| `ARCHITECTURE.md` | documentation | required | repository-owned | — | Repository-local architecture and boundaries |
| `CODE_OF_CONDUCT.md` | community-health | optional | repository-owned | — | Local code of conduct only when organization defaults are insufficient |
| `CONTRIBUTING.md` | community-health | optional | repository-owned | — | Repository-specific contribution guide when external contribution is supported |
| `Cargo.toml` | metadata | profile | repository-owned | language-rust | Rust workspace intent |
| `LICENSE` | metadata | required | repository-owned | — | Repository-selected license text |
| `README.md` | documentation | required | repository-owned | — | Repository-specific introduction and navigation |
| `SECURITY.md` | security | optional | repository-owned | — | Repository-specific vulnerability reporting policy |
| `Taskfile.yml` | quality | required | repository-owned | — | Stable local task interface |
| `docs` | documentation | profile | repository-owned | documentation | Repository-owned detailed documentation |
| `docs/ecosystem/CONTEXT.md` | agent-context | profile | generated | agent-context | Pinned Hygiene ecosystem context projection |
| `package.json` | metadata | profile | repository-owned | language-node | Node.js workspace intent |
| `publication.json` | metadata | profile | repository-owned | publication | Publication-specific source manifest |
| `pyproject.toml` | metadata | profile | repository-owned | language-python | Python project intent |
| `release-please-config.json` | release | profile | repository-owned | release-automated | Repository release strategy |

## Generated outputs

| Path | Owner | Canonical input | Checked in |
| --- | --- | --- | --- |
| `docs/ecosystem/CONTEXT.md` | `egohygiene/hygiene` | `catalog/repositories.yaml + catalog/repository-context.json` | `true` |
| `docs/foundation/INVENTORY.md` | `egohygiene/empathy` | `foundation/catalog.json` | `true` |
| `foundation/contracts/empathy.repository-contract.toml` | `egohygiene/empathy` | `foundation/catalog.json + foundation/empathy.manifest.json` | `true` |
