# Empathy

🤝 A humane, reusable repository foundation for maintainers, contributors,
users, automation, and AI agents.

Empathy is the integration monorepo for Ego Hygiene's opinionated repository
baseline. It assembles universal contracts and selectable capability profiles in
one place before independently versioned components are extracted.

## Current foundation

The current consolidation passes establish the GitHub automation and Egolint
quality layers:

- immutable external action references;
- least-privilege workflow permissions and bounded job runtimes;
- reusable composite actions for common toolchain and generation steps;
- automation policy tests and MegaLinter validation;
- dependency, CodeQL, OSV, and OpenSSF supply-chain checks;
- safe manual workflows for contributor and repository-intelligence generation.
- an encapsulated, cross-language Egolint subsystem with root Taskfile imports;
- universal and holistic MegaLinter profiles with generated output under
  `.reports/`;
- canonical emoji Conventional Commits with Commitizen, Husky, and Commitlint;
- reviewed Detect Secrets, MIT/SPDX header, and REUSE policies;
- durable quality audits and remediation guidance under `.audits/`.

Imported workflows that still depend on a product, toolchain, secret set, or
release strategy are preserved in [`.staging/github/`](.staging/github/README.md)
and are intentionally inert.

## Repository contract

```bash
task check
task hooks:install
task commit:test
task precommit:staged
task precommit:all
task license:check
task secrets:check
task lint:all
task lint:holistic
```

Husky is the sole Git hook manager. Its pre-commit hook combines lint-staged's
fast file-aware fixes with the intentionally small structural/security
pre-commit stage; the complete pre-commit profile remains an explicit command.
Install hooks through `task hooks:install`; do not run `pre-commit install`,
because Husky owns the repository hook path.
Commit messages use `type(scope): emoji subject` and can be authored through
`task commit:create`.

The standard check validates formatting, tests, and the changed-file Egolint
profile. The complete and holistic commands expand that scope deliberately.
See [the Egolint subsystem](egolint/README.md) and
[the composite action catalog](.github/actions/README.md) for their contracts.

## Status

Empathy is under active foundation development. Staged material is preserved for
classification and must not be treated as production-ready template content.
