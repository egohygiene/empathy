# Repository task modules

The root [`Taskfile.yml`](../Taskfile.yml) is intentionally a composition file.
It imports these reusable modules with `flatten: true` so stable commands such
as `task check` remain short while their ownership stays explicit.

| Module           | Ownership                                                                   |
| ---------------- | --------------------------------------------------------------------------- |
| `project.yml`    | Stable lifecycle contract: setup, doctor, build, check, and CI              |
| `quality.yml`    | Formatting, tests, Egolint adapters, security, SBOM, and catalog validation |
| `mindgarden.yml` | Knowledge indexing, context, projection, and Quartz commands                |
| `identity.yml`   | Identity validation, planning, and creative handoff                         |
| `git.yml`        | Read-only, repository-independent Git inspection helpers                    |

Subsystem-owned Taskfiles are imported directly at the root and retain their
namespaces: `beacon:`, `egolint:`, `mantle:`, `react-vite:`, and `tool:`. Do not
copy subsystem implementation into these modules merely to remove a namespace.

## Design rules

- Keep the lifecycle surface stable: `setup`, `doctor`, `format`, `lint`,
  `test`, `build`, `check`, and `ci`.
- Default validation must be deterministic, nonprivileged, and suitable for CI.
- Networked installation or local mutation must remain an explicit command and
  be called out in its task summary.
- Destructive, host-specific, product-specific, or unavailable capabilities do
  not belong in the universal root contract.
- Add a description to every public task so it appears in the generated
  [`TASKS.md`](../TASKS.md) catalog.
- Run `task taskfile:catalog:write` after changing any public task name or
  description, then run `task taskfile:check`.
