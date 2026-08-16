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
- an explicit complementary-tool matrix with truthful project applicability;
- Taskfile-backed VS Code settings, extensions, and quality tasks;
- separated source-license, SBOM, and vulnerability ownership contracts;
- an incubated Mindgarden holon with versioned `.garden` contracts,
  dependency-free validation, deterministic agent access, a reviewed-public
  Quartz projection, and Empathy as its first consumer.
- an incubated Rust `identity` holon with a consumer-owned `.identity/`
  contract, versioned asset profiles, deterministic planning, and a contextual
  creative handoff that keeps human approval canonical.
- an incubated Rust `beacon` holon with versioned document-template packages,
  deterministic project initialization, binary-level smoke coverage, and root
  validation integration.
- an incubated Holon-owned React + Vite pack that combines website, docs,
  playground, provider-neutral auth, optional commerce, shared Vite policy, and
  Tailwind CSS v3 into one comprehensive pnpm workspace.

Imported workflows that still depend on a product, toolchain, secret set, or
release strategy are preserved in [`.staging/github/`](.staging/github/README.md)
and are intentionally inert.

## Repository contract

The root [`Taskfile.yml`](Taskfile.yml) composes focused modules from
[`.tasks/`](.tasks/) with subsystem-owned Taskfiles. See [`TASKS.md`](TASKS.md)
for the stable lifecycle contract, operational boundaries, namespaces, and the
generated catalog of every public command.

Husky is the sole Git hook manager. Its pre-commit hook combines lint-staged's
fast file-aware fixes with the intentionally small structural/security
pre-commit stage; the complete pre-commit profile remains an explicit command.
Install hooks through `task hooks:install`; do not run `pre-commit install`,
because Husky owns the repository hook path.
Commit messages use `type(scope): emoji subject` and can be authored through
`task commit:create`.

The standard check validates task composition, formatting, tests, the incubated
holons and frontend pack, and the holistic Egolint profile. Focused commands
reduce that scope deliberately. See [the Egolint subsystem](egolint/README.md) and
[the composite action catalog](.github/actions/README.md) for their contracts.
See [Mindgarden](mindgarden/README.md) for the knowledge lifecycle,
[`identity`](identity/README.md) for the visual identity lifecycle, and
[`beacon`](beacon/README.md) for reproducible document-project bootstrapping.
See [`holon/packs/react-vite`](holon/packs/react-vite/README.md) for the
incubating frontend repository pack and its staging-promotion ledger.

## Architecture

Empathy's architecture is a connected set of 18 repository-specific documents
derived from the reusable Aether architecture specifications. Start with
[`META.md`](META.md) for the inventory, ownership map, dependency graph, reading
order, lifecycle, and change-propagation rules.

The shortest orientation path is:

1. [`PURPOSE.md`](PURPOSE.md), [`VISION.md`](VISION.md), and
   [`PRINCIPLES.md`](PRINCIPLES.md) for intent;
2. [`ONTOLOGY.md`](ONTOLOGY.md) for canonical language;
3. [`SYSTEM.md`](SYSTEM.md) and [`ARCHITECTURE.md`](ARCHITECTURE.md) for logical
   and structural boundaries;
4. [`DECISIONS.md`](DECISIONS.md) and [`ROADMAP.md`](ROADMAP.md) for accepted
   choices and strategic evolution.

Run `task architecture:check` to validate metadata, governing specifications,
relationships, graph acyclicity, document structure, and inventory coverage.

## Status

Empathy is under active foundation development. Staged material is preserved for
classification and must not be treated as production-ready template content.
