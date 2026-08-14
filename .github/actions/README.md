# Composite actions

Empathy keeps reusable step-level behavior in composite actions and keeps event,
permission, runner, and job orchestration in workflows. This boundary lets a
technology profile reuse setup logic without inheriting an unrelated trigger or
token policy.

## Contracts

- Callers check out the repository before invoking a local action.
- External actions use immutable full-length commit SHAs with a readable version
  comment.
- Tool versions are exact inputs with pinned defaults; consumers may override
  them deliberately.
- GitHub expressions enter shell scripts through environment variables rather
  than direct interpolation.
- Actions do not commit, push, or open pull requests unless their name and
  documentation explicitly describe that side effect.
- Repository-relative working directories are the default. Product paths are
  never embedded in a shared action.

## Catalog

| Action                                       | Responsibility                                                               | Side effects                     |
| -------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------- |
| `commit-if-changed`                          | Stage explicit pathspecs and create one conditional commit                   | Optional push                    |
| `contributors`                               | Hydrate All Contributors metadata and regenerate `CONTRIBUTORS.md`           | Working-tree changes             |
| `flutter-generate`                           | Run selected Flutter source generators and formatting                        | Working-tree changes             |
| `flutter-setup`                              | Install pinned Flutter and resolve pub dependencies                          | Tool/cache installation          |
| `generate-repository-intelligence`           | Produce deterministic tree, activity, and SVG artifacts                      | Writes selected output directory |
| `generate-repository-intelligence-dashboard` | Aggregate normalized reports and repository vitality into a static dashboard | Writes selected output directory |
| `install-linux-build-deps`                   | Install Flutter desktop build packages on Debian-family runners              | System packages                  |
| `normalize-repository-report`                | Normalize scanner outputs into a versioned intelligence contract             | Writes one summary JSON          |
| `python-poetry-setup`                        | Install pinned Python/Poetry and locked dependencies                         | Tool/cache installation          |
| `setup-environment`                          | Detect and prepare Node.js, Python/Poetry, and Flutter projects              | Tool/dependency installation     |
| `setup-osv-scanner`                          | Install a checksum-verified OSV Scanner release                              | Temporary tool installation      |
| `generate-lint-infographic`                  | Generate architecture SVG and legend from canonical tool matrices            | `.reports/egolint/architecture/` |
| `publish-report-snapshot`                    | Guard and publish stable reports from trusted default-branch runs            | Explicit `.reports/` paths       |
| `validate-automation`                        | Run actionlint, action metadata validation, and repository policy            | Temporary tool downloads         |

## Selection guide

Use `setup-environment` when a repository needs a convenient, auto-detected
baseline. Use the technology-specific actions when a workflow needs explicit
control over versions, dependency installation, or job boundaries.

Use a reusable workflow instead of a composite action when the abstraction owns
multiple jobs, permissions, environments, matrices, or deployment credentials.
Those reusable workflows will live in Relay once their contracts stabilize.
