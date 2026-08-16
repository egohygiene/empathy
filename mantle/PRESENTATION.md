# Mantle startup presentation

Mantle owns the portable terminal behavior that presents an interactive shell.
Realm may provision optional dependencies, but it does not own banner rendering,
Fastfetch configuration, collectors, or shell-startup policy.

## Startup sequence

After Mantle resolves its profile, initializes the runtime, and constructs
`PATH`, Bash, Zsh, and Fish invoke the same `bin/shell-banner` command:

1. Confirm the session is eligible.
2. Render `assets/presentation/mantle-banner.png` through `bin/imgcat`.
3. Fall back to `assets/presentation/mantle-banner.txt` when inline images are
   unavailable.
4. If Fastfetch is installed, invoke it with
   `config/fastfetch/fastfetch.jsonc` explicitly.
5. Export `MANTLE_PRESENTATION_SHOWN=1` in the shell adapter so nested shells
   do not retry the optional sequence.

Normal startup requires an interactive Mantle shell, a stdout TTY, a
non-`dumb` terminal, no CI marker, no inherited guard, and a presentation mode
that permits interactive output. Interactive containers and devcontainers are
eligible when they provide a usable TTY. Noninteractive processes remain
silent.

The shell adapter records that presentation was evaluated even when an optional
renderer or Fastfetch fails. A new independent terminal starts without the
inherited guard and may present again.

## Modes and controls

Mantle's typed profile system owns the presentation mode:

| Mode | Startup behavior |
| --- | --- |
| `private` | Eligible interactive sessions show the full local presentation. |
| `share-safe` | Shows the repository-owned banner only; the full local Fastfetch view requires an explicit forced command. |
| `ci` | Automatic startup presentation is disabled. |
| `off` | Presentation is disabled until an explicit forced replay. |

The supported environment controls are:

| Variable | Purpose |
| --- | --- |
| `MANTLE_PRESENTATION_MODE` | Override the profile mode. |
| `MANTLE_PRESENTATION_SHOWN` | Inherited once-per-session guard. |
| `MANTLE_BANNER_IMAGE` | Override the image path for development or testing. |
| `MANTLE_BANNER_TEXT` | Override the plain-text fallback. |
| `MANTLE_FASTFETCH_CONFIG` | Override the explicit Fastfetch config. |

Overrides may contain spaces. Invalid explicit CLI paths fail before any
rendering; missing default optional components are nonfatal.

## Manual replay and diagnostics

```sh
shell-banner --force
shell-banner --banner-only --force
shell-banner --fastfetch-only --force
shell-banner --dry-run
shell-banner --dry-run --verbose
```

`--force` is the explicit authorization to replay presentation and, when
stdout is redirected, to permit renderer output. `--dry-run` prints resolved
paths, availability, eligibility, and sequence without invoking `imgcat` or
Fastfetch. `--verbose` explains skipped and failed optional components.

## Assets and Fastfetch compatibility

- Canonical banner: `assets/presentation/mantle-banner.png`, a transparent
  400×134 PNG.
- ANSI-free fallback: `assets/presentation/mantle-banner.txt`.
- Fastfetch config: `config/fastfetch/fastfetch.jsonc`.
- Compatibility schema: Fastfetch 2.67.0.
- Pinned release: [Fastfetch 2.67.0][fastfetch-release].
- Future logo contract: the bare filename `mantle.png`; no placeholder is
  generated.

When the dedicated logo exists, an installer may place only that file at
`${XDG_DATA_HOME:-${HOME}/.local/share}/fastfetch/logos/mantle.png`.
Mantle does not own the complete logo directory, does not overwrite unrelated
logos, and does not create or replace the user's global Fastfetch config.

The config keeps platform-specific general options out of the universal file,
allows Chafa to negotiate terminal capabilities, uses a one-space key for
custom section headers, and contains no public-IP or weather modules. Nerd Font
icons are progressive enhancement; the information remains available without
the expected glyph font.

## Deterministic collectors

The Fastfetch config delegates repository and tool context to four directly
testable commands:

```sh
mantle fastfetch runtime
mantle fastfetch workspace
mantle fastfetch toolchains
mantle fastfetch contexts
```

- `runtime` reports Mantle version, active shell, runtime classification, and
  OS family.
- `workspace` reports an abbreviated directory or repository name, ref, and
  clean/changed state, including untracked files.
- `toolchains` reports Git, Node.js, Python, Rust, Go, and Task versions in a
  stable order.
- `contexts` reads only the local Docker and Kubernetes client context.

Collectors perform no network calls, package-manager operations, daemon
queries, update checks, or Git remote inspection. They do not print hostnames,
absolute home paths by default, remote URLs, credentials, tokens, endpoints,
certificate paths, or arbitrary environment values.

## Installation boundary

Both copy and development-symlink installs include `assets/`, `config/`,
`bin/`, and the collector implementations as Mantle-owned payload. Updating
or uninstalling the prefix changes only installer-owned material.
`--no-shell-hook` installs the payload without activating startup
presentation.

Fastfetch, Chafa, image protocols, and Nerd Fonts remain optional and are never
installed during shell startup. A missing or failing component cannot abort
shell initialization.

## Validation

Run the focused offline contract and complete Mantle suite with:

```sh
python3 tests/validate_fastfetch.py
./tests/run.sh --local tests/bin/shell-banner.bats
./tests/run.sh --local tests/integration/fastfetch.bats
./tests/run.sh --local tests/integration/initialization.bats
./tests/run.sh --local tests/contract/presentation.bats
./tests/run.sh --strict
```

Tests use isolated home, XDG, Git, Docker, Kubernetes, renderer, and Fastfetch
fixtures. They do not modify real dotfiles, credentials, system configuration,
remote services, or network APIs. The strict GitHub Actions matrix is the source
of truth for executed Linux/macOS and Bash/Zsh/Fish coverage. It downloads the
official Fastfetch 2.67.0 archives, verifies their published SHA-256 checksums,
validates the offline contract, and executes the canonical config with the real
binary. Renderer coverage uses controlled fixtures plus the real text fallback;
no graphical backend is inferred when one is unavailable.

[fastfetch-release]: https://github.com/fastfetch-cli/fastfetch/releases/tag/2.67.0
