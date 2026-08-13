# Mantle architecture

Copyright 2026 Ego Hygiene

SPDX-License-Identifier: MIT

Mantle is a user-owned shell runtime with three supported entry surfaces: the
`.shellrc` Bash/Zsh entrypoint, the native Fish runtime, and the `mantle` CLI.
Its architecture keeps shell initialization, reusable libraries, environment
policy, platform behavior, commands, and installation code independently
owned.

The machine-readable source of truth is
[`config/architecture/layers.tsv`](config/architecture/layers.tsv). Contract
tests reject unclassified maintained shell files and invalid dependency
declarations.

## Public and internal surfaces

| Surface                                       | Status                  | Contract                                                                                      |
| --------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------- |
| `.shellrc`                                    | Public entrypoint       | Source to initialize Bash or Zsh.                                                             |
| `runtime/shells/fish/runtime.fish`            | Public entrypoint       | Source from Fish with `MANTLE_ROOT` set.                                                      |
| `bin/mantle`                                  | Public entrypoint       | Execute to access supported CLI commands.                                                     |
| `install.sh`                                  | Public entrypoint       | Execute to install, inspect, or remove Mantle.                                                |
| `lib/core/`, `lib/bash/`                      | Public library layer    | Functions covered by the public-API contract are stable.                                      |
| `lib/modules.sh`                              | Public loader API       | `mantle_load_module`, `mantle_list_loaded_modules`, and `mantle_is_module_loaded` are stable. |
| `lib/extensions/`                             | Optional API            | Functions become available only after explicit extension loading.                             |
| `init/`, `modules/`, `platforms/`, `runtime/` | Internal runtime        | May change while preserving entrypoint and public-function behavior.                          |
| `libexec/mantle/` and `lib/install/`          | Internal implementation | Reach through the CLI or installer entrypoints, not by direct invocation.                     |

Public describes a compatibility promise, not permission to source every file
in a public layer independently. The contract tests and file-level guards
define which files are direct entrypoints.

## Layer responsibilities

- Initialization owns root resolution, ordering, idempotence, and failure
  propagation. It does not own environment values or platform policy.
- Core and Bash libraries own reusable, side-effect-limited primitives. Core
  owns all mutation of `PATH` through `mantle_core_path_prepend` and
  `mantle_core_path_append`.
- The config library owns schema parsing, profile resolution, precedence, and
  provenance reporting. It treats user configuration strictly as data.
- Modules choose portable environment values and candidates. They consume core
  APIs instead of reimplementing primitives.
- Platform adapters choose OS-specific values and candidates after portable
  modules load. They do not install software or own shell lifecycle.
- Shell runtimes adapt shared behavior to Bash, Zsh, Fish, or POSIX syntax.
- CLI commands parse user intent and report results. Installer implementations
  consume the install-library layer in a process-isolated execution path.
- Extensions remain opt-in and must not become implicit startup dependencies.

## Dependency direction

Dependencies flow from entrypoints and orchestration toward reusable policy and
library layers. A lower-level library must never depend on a public entrypoint.

| Consumer                    | May depend on                                                            |
| --------------------------- | ------------------------------------------------------------------------ |
| Shell entrypoint            | Initialization                                                           |
| Initialization              | Config, core, shared/shell runtime, module loader, modules, platform, extensions |
| Shared/shell runtime        | Core and Bash libraries; other shell-runtime files                       |
| Module loader               | Modules                                                                  |
| Modules and platforms       | Core APIs; platforms may source same-platform files                      |
| Installer entrypoint        | A copied shell entrypoint during activation                              |
| Installer implementations   | Install runtime and libraries                                            |
| Install libraries           | Core and other install libraries                                         |
| CLI dispatcher              | No source-time dependency; dispatch is process isolated                  |
| Config CLI command          | Config library                                                           |

The complete allowed-dependency sets live in the layer registry. Adding a
maintained shell file requires assigning exactly one layer. Adding a new
source-time dependency requires declaring it there and extending the contract
test when the edge is dynamic.

## Runtime lifecycle

1. `.shellrc` resolves and validates `MANTLE_ROOT`.
2. `init/init.sh` loads core/runtime adapters, the extension loader, the module
   loader, and the typed configuration resolver.
3. Bootstrap resolves the selected profile and environment overrides.
4. Bootstrap loads portable modules in dependency order.
5. The active platform adapter applies OS-specific behavior.
6. Profile-enabled capability modules load only where applicable.
7. Successful initialization records an idempotent initialized state; failures
   remain visible and retryable.

Fish uses its native runtime entrypoint and configuration fragments rather than
the Bash/Zsh loader path. CLI commands and installers execute in child
processes and do not mutate the caller's shell session.

## Mantle and Realm

Mantle owns behavior inside a shell: environment variables, executable search
paths, aliases, history, shell adapters, diagnostics, and user-owned tool
installation primitives.

Realm owns construction of a reproducible development environment: container
images, workspace lifecycle, project services, mounts, ports, and orchestration.
Realm may activate Mantle inside an environment, but Mantle must not acquire
container lifecycle, image-composition, or project-service responsibilities.
This keeps Mantle usable on a laptop, in a dev container, and in CI without
requiring Realm.

## Changing a boundary

1. Decide which existing owner is responsible before adding code.
2. Update `config/architecture/layers.tsv` if a path or dependency changes.
3. Preserve public entrypoint and function contracts or document a deliberate
   compatibility change.
4. Add the narrowest unit, integration, or contract coverage.
5. Update this document when responsibility or lifecycle changes.
6. Run `./tests/run.sh --strict` before merge.
