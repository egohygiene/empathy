# Empathy

🤝 A humane, reusable repository foundation for maintainers, contributors,
users, automation, and AI agents.

Empathy is the integration monorepo for Ego Hygiene's opinionated repository
baseline. It assembles universal contracts and selectable capability profiles in
one place before independently versioned components are extracted.

## Current foundation

This first consolidation pass establishes the GitHub automation layer:

- immutable external action references;
- least-privilege workflow permissions and bounded job runtimes;
- reusable composite actions for common toolchain and generation steps;
- automation policy tests and MegaLinter validation;
- dependency, CodeQL, OSV, and OpenSSF supply-chain checks;
- safe manual workflows for contributor and repository-intelligence generation.

Imported workflows that still depend on a product, toolchain, secret set, or
release strategy are preserved in [`.staging/github/`](.staging/github/README.md)
and are intentionally inert.

## Repository contract

```bash
task check
```

The command validates formatting, Markdown, Python syntax, unit tests, and the
GitHub automation policy. See [the composite action catalog](.github/actions/README.md)
for reusable action contracts.

## Status

Empathy is under active foundation development. Staged material is preserved for
classification and must not be treated as production-ready template content.
