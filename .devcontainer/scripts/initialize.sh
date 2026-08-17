#!/usr/bin/env bash
# shellcheck shell=bash
#
# Generic, repository-agnostic Dev Container initialization hook.
#
# Extension points:
#   .devcontainer/scripts/initialize.local.sh
#   .devcontainer/scripts/initialize.d/*.sh
#
# Optional environment variables:
#   DEVCONTAINER_CREATE_ENV=1                 Copy .env.example to .env when absent.
#   DEVCONTAINER_HOOK_FAILURES_ARE_FATAL=1    Stop when an extension hook fails.
#   DEVCONTAINER_INIT_VERBOSE=1               Enable Bash execution tracing.

set -Eeuo pipefail

readonly SCRIPT_NAME="${BASH_SOURCE[0]##*/}"
readonly LOG_PREFIX="[devcontainer:init]"

REPO_ROOT=""
CURRENT_HOOK=""
TEMPORARY_DIRECTORIES=()

# Print a timestamped informational message.
log() {
  printf "%s %s\n" "$LOG_PREFIX" "$*" >&2
}

# Print a timestamped warning message.
warn() {
  printf "%s [warn] %s\n" "$LOG_PREFIX" "$*" >&2
}

# Print an error message and terminate with a non-zero status.
die() {
  printf "%s [error] %s\n" "$LOG_PREFIX" "$*" >&2
  exit 1
}

# Run during an unexpected command failure.
on_error() {
  local exit_code="$1"
  local line_number="$2"
  local command="$3"

  printf "%s [error] Command failed (exit %d) at line %d: %s\n" \
    "$LOG_PREFIX" \
    "$exit_code" \
    "$line_number" \
    "$command" \
    >&2
}

# Remove temporary resources and report the final lifecycle status.
cleanup() {
  local exit_code="$1"
  local directory

  for directory in "${TEMPORARY_DIRECTORIES[@]}"; do
    [ -d "$directory" ] && rm -rf -- "$directory"
  done

  if [ "$exit_code" -eq 0 ]; then
    log "Initialization complete."
  else
    warn "Initialization ended with exit code $exit_code."
  fi
}

# Configure lifecycle signal and error handlers.
install_traps() {
  trap 'on_error "$?" "$LINENO" "$BASH_COMMAND"' ERR
  trap 'cleanup "$?"' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
}

# Return the repository root inferred from this script's standard location.
resolve_repository_root() {
  local script_directory

  script_directory="$(
    cd -- "$(dirname -- "${BASH_SOURCE[0]}")" \
      && pwd -P
  )"

  cd -- "$script_directory/../.." && pwd -P
}

# Create a directory when it is absent and best-effort apply its permissions.
ensure_directory() {
  local directory="${1:?Directory path is required}"
  local mode="${2:-0755}"

  mkdir -p -- "$directory"

  if ! chmod "$mode" "$directory" 2>/dev/null; then
    warn "Could not set permissions on: $directory"
  fi
}

# Append a directory to PATH only when it is not already present.
prepend_path_once() {
  local directory="${1:?Directory path is required}"
  local path_entry

  IFS=":" read -r -a path_entries <<< "${PATH:-}"
  for path_entry in "${path_entries[@]}"; do
    [ "$path_entry" = "$directory" ] && return 0
  done

  export PATH="$directory${PATH:+:$PATH}"
}

# Configure portable, user-local XDG locations for development tooling.
configure_environment() {
  : "${HOME:?HOME must be set for Dev Container initialization}"

  export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
  export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
  export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
  export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

  prepend_path_once "$HOME/.local/bin"
  prepend_path_once "$HOME/bin"
}

# Create harmless runtime and cache directories used by common local tooling.
create_baseline_directories() {
  ensure_directory "$REPO_ROOT/.devcontainer/cache" 0775
  ensure_directory "$REPO_ROOT/.devcontainer/tmp" 0775
  ensure_directory "$REPO_ROOT/.cache" 0775
  ensure_directory "$REPO_ROOT/.tmp" 0775
  ensure_directory "$XDG_CACHE_HOME" 0775
  ensure_directory "$XDG_CONFIG_HOME" 0775
  ensure_directory "$XDG_DATA_HOME" 0775
  ensure_directory "$XDG_STATE_HOME" 0775
}

# Optionally create a local environment file from the repository template.
create_environment_file_if_requested() {
  [ "${DEVCONTAINER_CREATE_ENV:-0}" = "1" ] || return 0

  if [ -f "$REPO_ROOT/.env.example" ] && [ ! -e "$REPO_ROOT/.env" ]; then
    log "Creating .env from .env.example"
    cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
  fi
}

# Execute one extension hook with a documented, stable environment contract.
run_hook() {
  local hook="${1:?Hook path is required}"

  CURRENT_HOOK="$hook"
  log "Running hook: ${hook#$REPO_ROOT/}"

  if DEVCONTAINER_REPO_ROOT="$REPO_ROOT" \
    DEVCONTAINER_INITIALIZE_HOOK=1 \
    bash "$hook"; then
    CURRENT_HOOK=""
    return 0
  fi

  if [ "${DEVCONTAINER_HOOK_FAILURES_ARE_FATAL:-0}" = "1" ]; then
    die "Hook failed: ${hook#$REPO_ROOT/}"
  fi

  warn "Hook failed; continuing: ${hook#$REPO_ROOT/}"
  CURRENT_HOOK=""
}

# Discover and execute local and ordered extension hooks.
run_extension_hooks() {
  local hooks_directory="$REPO_ROOT/.devcontainer/scripts/initialize.d"
  local hook

  if [ -f "$REPO_ROOT/.devcontainer/scripts/initialize.local.sh" ]; then
    run_hook "$REPO_ROOT/.devcontainer/scripts/initialize.local.sh"
  fi

  [ -d "$hooks_directory" ] || return 0

  while IFS= read -r -d "" hook; do
    run_hook "$hook"
  done < <(
    find "$hooks_directory" \
      -mindepth 1 \
      -maxdepth 1 \
      -type f \
      -name "*.sh" \
      -print0 \
      | LC_ALL=C sort -z
  )
}

# Report recognized project manifests without performing package installation.
report_detected_toolchains() {
  local detected=()

  [ -f "$REPO_ROOT/package.json" ] && detected+=("Node.js")
  [ -f "$REPO_ROOT/pyproject.toml" ] \
    || [ -f "$REPO_ROOT/requirements.txt" ] \
    || [ -f "$REPO_ROOT/setup.py" ] \
    && detected+=("Python")
  [ -f "$REPO_ROOT/Cargo.toml" ] && detected+=("Rust")
  [ -f "$REPO_ROOT/go.mod" ] && detected+=("Go")
  [ -f "$REPO_ROOT/compose.yaml" ] \
    || [ -f "$REPO_ROOT/docker-compose.yml" ] \
    && detected+=("Docker Compose")

  if [ "${#detected[@]}" -gt 0 ]; then
    log "Detected project tooling: $(IFS=", "; printf "%s" "${detected[*]}")"
  else
    log "No common project manifest detected."
  fi
}

# Initialize the Dev Container workspace.
main() {
  if [ "${DEVCONTAINER_INIT_VERBOSE:-0}" = "1" ]; then
    set -x
  fi

  REPO_ROOT="$(resolve_repository_root)"
  cd -- "$REPO_ROOT"

  configure_environment
  create_baseline_directories
  create_environment_file_if_requested

  log "Repository root: $REPO_ROOT"
  report_detected_toolchains
  run_extension_hooks

  log "Add repository-specific setup to .devcontainer/scripts/initialize.d/*.sh"
}

install_traps
main "$@"
