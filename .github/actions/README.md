# Repository-local composite actions

Empathy keeps repository-specific step-level behavior in local composite actions
and consumes independently reusable automation from
[`egohygiene/relay`](https://github.com/egohygiene/relay). Event, permission,
runner, site-composition, and deployment policy remain in repository-owned
workflows. This boundary keeps the strict baseline thin without giving a shared
action authority over a consumer repository's triggers or credentials.

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
| `install-linux-build-deps`                   | Install Flutter desktop build packages on Debian-family runners              | System packages                  |
| `python-poetry-setup`                        | Install pinned Python/Poetry and locked dependencies                         | Tool/cache installation          |
| `setup-agent-environment`                    | Compose portable toolchain setup for Copilot and coding-agent environments   | Tool/dependency installation     |
| `setup-environment`                          | Detect and prepare Node.js, Python/Poetry, and Flutter projects              | Tool/dependency installation     |
| `setup-osv-scanner`                          | Install a checksum-verified OSV Scanner release                              | Temporary tool installation      |
| `generate-lint-infographic`                  | Generate architecture SVG and legend from canonical tool matrices            | `.reports/egolint/architecture/` |
| `validate-automation`                        | Run actionlint, action metadata validation, and repository policy            | Temporary tool downloads         |

## Selection guide

Use `setup-environment` when a repository needs a convenient, auto-detected
baseline. Use `setup-agent-environment` when that baseline is being prepared for
Copilot or another coding agent and may also need Linux desktop build support.
Use the technology-specific actions when a workflow needs explicit control over
versions, dependency installation, or job boundaries.

Use a reusable workflow instead of a composite action when the abstraction owns
multiple jobs, permissions, environments, matrices, or deployment credentials.
Repository intelligence, normalized report summaries, and guarded report
publication are consumed from Relay at an immutable release commit. Empathy
retains the thin caller workflows and integration tests that prove those shared
actions compose safely with its reports and complete Mindgarden Pages artifact.
