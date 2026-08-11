# Egolint

🧹 A universal linting platform and extensible MegaLinter wrapper for
consistent, reproducible code quality.

Egolint owns Empathy's complete quality-policy catalog. It keeps linter rules,
security-scanner configuration, fixtures, dependency manifests, the local
container wrapper, and composable Taskfile commands behind one stable boundary.
The monorepo root consumes that boundary without copying the individual tool
configurations.

## Profiles

The root [`.mega-linter.yml`](../.mega-linter.yml) extends the holistic policy
and selects a small universal baseline for routine pull requests. The full
[`egolint/.mega-linter.yml`](.mega-linter.yml) retains every imported descriptor
and can be run deliberately when broad coverage is useful.

From the monorepo root:

```bash
task lint
task lint:all
task lint:holistic
task lint:doctor
task lint:fix
```

## Commit and hook policy

Install the repository-owned hooks and exercise their contracts from the
monorepo root:

```bash
task hooks:install
task hooks:check
task commit:create
task commit:test
task precommit:staged
task precommit:all
```

Husky exclusively owns `core.hooksPath`. lint-staged applies fast, file-aware
formatting and lint fixes; the automatic pre-commit stage handles structural,
secret, and license checks that do not duplicate those commands. The complete
pre-commit catalog is preserved under the manual stage.
Use `task hooks:install` instead of `pre-commit install`; Husky delegates the
selected checks through the stable pre-commit adapter.

Commitlint and Commitizen share [`.czrc`](../.czrc) as their type catalog. New
commit messages must follow `type(scope): emoji subject`, with a lowercase
subject opening and a 100-character header limit.

Detect Secrets uses the reviewed [baseline](../.secrets.baseline). First-party
source headers and repository-wide license metadata follow the MIT/SPDX policy
defined by [`REUSE.toml`](../REUSE.toml).

Generated output is always disposable and namespaced under `.reports/`:

```text
.reports/
├── megalinter/
└── osv/
```

Durable findings, architectural decisions, and future recommendations belong
under [`.audits/`](../.audits/), never in the generated report tree.

## Internal layout

```text
egolint/
├── .config/
│   ├── lint/           # Language and format rules
│   └── security/       # Scanner and supply-chain rules
├── scripts/
│   ├── megalinter.sh   # Docker/Podman wrapper
│   ├── pnpm.sh         # Corepack-aware pinned pnpm adapter
│   └── precommit.sh    # Stable pre-commit runtime adapter
├── tasks/
│   └── lint.yml        # Composable Taskfile API
├── tests/
│   └── fixtures/       # Cross-language validation fixtures
├── package.json        # Node-based quality tools
└── pyproject.toml      # Python-based quality tools
```

The root GitHub workflows are the active monorepo integration layer. Egolint
does not keep a second `.github/workflows/` tree.
