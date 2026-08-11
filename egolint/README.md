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
│   └── megalinter.sh   # Docker/Podman wrapper
├── tasks/
│   └── lint.yml        # Composable Taskfile API
├── tests/
│   └── fixtures/       # Cross-language validation fixtures
├── package.json        # Node-based quality tools
└── pyproject.toml      # Python-based quality tools
```

The root GitHub workflows are the active monorepo integration layer. Egolint
does not keep a second `.github/workflows/` tree.
