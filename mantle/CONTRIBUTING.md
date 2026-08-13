# Contributing to Mantle

Mantle is a portable shell runtime, so changes must preserve its execution
boundaries across Bash, Zsh, Fish, macOS, Linux, and CI.

## Source roles

Every maintained shell file has exactly one role:

| Role                  | Locations                                                         | Mode           | First line            |
| --------------------- | ----------------------------------------------------------------- | -------------- | --------------------- |
| Public executable     | `bin/mantle`, `install.sh`                                        | Executable     | `#!/usr/bin/env bash` |
| Private executable    | `libexec/mantle/commands/*.sh`, `libexec/mantle/installers/*.sh`  | Executable     | `#!/usr/bin/env bash` |
| Validation executable | `tests/run.sh`                                                    | Executable     | `#!/usr/bin/env bash` |
| Source-only runtime   | `.shellrc`, `init/`, `lib/`, `modules/`, `platforms/`, `runtime/` | Non-executable | Copyright header      |
| Test source           | `tests/**/*.bats`, `tests/**/*.bash`                              | Non-executable | Copyright header      |

Source-only files deliberately omit shebangs. A shebang describes direct
execution, conflicts with their guarded source contract, and causes executable
mode validators to classify them incorrectly.

All maintained shell files must place these lines within the first eight lines:

```text
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
```

Executable files place them immediately after the shebang. Source-only files
place them first.

## Dialects and formatting

- Bash libraries, commands, installers, helpers, and Bats tests use tabs and the
  nearest rules in `.editorconfig`.
- Shared and POSIX runtime files use the POSIX shfmt dialect.
- `.shellrc` is a Bash/Zsh hybrid and the Zsh runtime uses native Zsh syntax;
  both are syntax-tested but intentionally excluded from shfmt.
- Fish files are checked with `fish --no-execute` in strict validation.
- ShellCheck suppressions must sit next to the file or operation whose contract
  requires them and include a reason. Do not add unexplained global exclusions.
- Installer descriptor variables are consumed dynamically by the sourced
  installer runtime, so installer entrypoints document the corresponding
  `SC2034` exception at file scope.

## Validation

Run the local suite while iterating:

```sh
./tests/run.sh --local
```

Before opening a pull request, install every required validation tool and run:

```sh
./tests/run.sh --strict
```

The contract suite rejects missing license metadata, misplaced executable bits,
noncanonical executable shebangs, and shebangs on source-only files.

## Adding files

1. Choose the file's role before writing it.
2. Add the canonical copyright and SPDX metadata.
3. Set executable mode only for one of the executable locations above.
4. Register new public commands in `tests/bin/coverage-map.tsv`.
5. Add behavioral coverage at the narrowest appropriate test layer.
6. Run formatting and strict validation before submission.
