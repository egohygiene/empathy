#!/usr/bin/env bash
# shellcheck shell=bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
#
# @file initialize.sh
# @brief Host-side initialization for a development container.
# @description
#   Prepares repository-local host state before the development container is
#   created. This script is lightweight, idempotent, safe to run repeatedly,
#   and intentionally independent of any specific repository toolchain.
#
#   Responsibilities:
#   - create repository-local cache and temporary directories
#   - optionally create .env from .env.example
#   - establish an initialization completion marker
#   - report common project manifests
#   - execute repository-specific extension hooks
#
#   Non-responsibilities:
#   - installing packages on the host or in the container
#   - mutating the container runtime
#   - editing tracked repository configuration
#   - bootstrapping project dependencies inside the container
#
# Extension points, executed in this order:
#   .devcontainer/scripts/initialize.local.sh
#   .devcontainer/scripts/initialize.d/*.sh
#
# Supported environment variables:
#   DEVCONTAINER_ID
#     Dev Container configuration identifier. The --devcontainer-id option
#     takes precedence when both are provided.
#   DEVCONTAINER_REPO_ROOT
#     Override repository-root discovery.
#   DEVCONTAINER_INIT_CREATE_ENV=1
#     Copy .env.example to .env when .env does not exist.
#   DEVCONTAINER_INIT_CONTINUE_ON_HOOK_FAILURE=1
#     Warn and continue when an extension hook fails. The default is fail-fast.
#   DEVCONTAINER_INIT_FORCE=1
#     Run initialization even when a matching completion marker exists.
#   DEVCONTAINER_INIT_VERBOSE=1
#     Enable verbose diagnostic logging.
#   DEVCONTAINER_INIT_TRACE=1
#     Enable Bash execution tracing. This may expose command arguments.
#
# @exitcode 0 Successful execution.
# @exitcode 1 Initialization failed.
# @exitcode 2 Invalid command-line usage.
# @exitcode 130 Interrupted by SIGINT.
# @exitcode 143 Terminated by SIGTERM.

set -o errexit
set -o errtrace
set -o nounset
set -o pipefail

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

readonly STATUS_PREFIX="🐳 [devcontainer:initialize]"
readonly WARNING_PREFIX="⚠️  [devcontainer:initialize]"
readonly ERROR_PREFIX="❌ [devcontainer:initialize]"
readonly DEBUG_PREFIX="🔎 [devcontainer:initialize]"

readonly DEVCONTAINER_DIRECTORY=".devcontainer"
readonly DEVCONTAINER_CACHE_DIRECTORY="${DEVCONTAINER_DIRECTORY}/.cache"
readonly DEVCONTAINER_TEMP_DIRECTORY="${DEVCONTAINER_DIRECTORY}/.tmp"
readonly INITIALIZATION_MARKER_NAME="initialize.complete"
readonly INITIALIZATION_SCHEMA_VERSION="1"

# -----------------------------------------------------------------------------
# Runtime state
# -----------------------------------------------------------------------------

REPO_ROOT=""
SCRIPT_DIRECTORY=""
INITIALIZATION_MARKER_FILE=""
TEMPORARY_FILE=""
DEVCONTAINER_ID="${DEVCONTAINER_ID:-}"
DRY_RUN=0
FORCE_INITIALIZATION=0
VERBOSE=0
ERROR_REPORTED=0

# -----------------------------------------------------------------------------
# Logging and lifecycle handlers
# -----------------------------------------------------------------------------

##
# Prints a formatted status message with an emoji prefix.
#
# Arguments:
#   $@ - Message components to display.
#
# Outputs:
#   Writes the formatted message to stdout.
##
print_status() {
  printf "%s %s\n" "$STATUS_PREFIX" "$*"
}

##
# Prints a verbose diagnostic message when verbose output is enabled.
#
# Arguments:
#   $@ - Message components to display.
#
# Outputs:
#   Writes the formatted message to stderr when enabled.
##
print_debug() {
  if ((VERBOSE == 1)); then
    printf "%s %s\n" "$DEBUG_PREFIX" "$*" >&2
  fi
}

##
# Prints a warning message with an emoji prefix.
#
# Arguments:
#   $@ - Message components to display.
#
# Outputs:
#   Writes the formatted message to stderr.
##
print_warning() {
  printf "%s %s\n" "$WARNING_PREFIX" "$*" >&2
}

##
# Prints an error message and terminates the script.
#
# Arguments:
#   $@ - Message components to display.
#
# Returns:
#   Does not return.
##
die() {
  ERROR_REPORTED=1
  printf "%s %s\n" "$ERROR_PREFIX" "$*" >&2
  exit 1
}

##
# Prints a command-line usage error and terminates the script.
#
# Arguments:
#   $@ - Message components to display.
#
# Returns:
#   Does not return.
##
usage_error() {
  ERROR_REPORTED=1
  printf "%s %s\n" "$ERROR_PREFIX" "$*" >&2
  printf "%s Try --help for usage information.\n" "$ERROR_PREFIX" >&2
  exit 2
}

##
# Returns success when a common boolean representation is enabled.
#
# Arguments:
#   $1 - Boolean-like value to evaluate.
#
# Returns:
#   0 when enabled; otherwise 1.
##
is_enabled() {
  case "${1:-0}" in
  1 | true | TRUE | yes | YES | on | ON)
    return 0
    ;;
  *)
    return 1
    ;;
  esac
}

##
# Removes an unfinished temporary marker file.
#
# Globals:
#   TEMPORARY_FILE
##
cleanup() {
  if [[ -n $TEMPORARY_FILE && -f $TEMPORARY_FILE ]]; then
    rm -f "$TEMPORARY_FILE"
  fi

  TEMPORARY_FILE=""
}

##
# Reports an unhandled command failure with its source location.
#
# Arguments:
#   $1 - Command exit code.
#   $2 - Source line number.
#   $3 - Command text.
#
# Returns:
#   The original command exit code.
##
on_error() {
  local exit_code="${1:?Exit code is required}"
  local line_number="${2:?Line number is required}"
  local command="${3:-unknown command}"

  trap - ERR
  ERROR_REPORTED=1

  printf "%s Command failed with exit code %d at line %d: %s\n" \
    "$ERROR_PREFIX" \
    "$exit_code" \
    "$line_number" \
    "$command" >&2

  return "$exit_code"
}

##
# Preserves the original exit status while cleaning temporary state.
#
# Arguments:
#   $1 - Script exit code.
#
# Returns:
#   Does not return.
##
on_exit() {
  local exit_code="${1:?Exit code is required}"

  trap - EXIT
  cleanup

  if ((exit_code != 0 && ERROR_REPORTED == 0)); then
    print_warning "Initialization stopped with exit code $exit_code."
  fi

  exit "$exit_code"
}

##
# Converts a signal into its conventional process exit status.
#
# Arguments:
#   $1 - Signal name.
#   $2 - Conventional exit code.
#
# Returns:
#   Does not return.
##
on_signal() {
  local signal_name="${1:?Signal name is required}"
  local exit_code="${2:?Exit code is required}"

  ERROR_REPORTED=1
  print_warning "Received $signal_name; stopping initialization."
  exit "$exit_code"
}

##
# Installs error, exit, and signal handlers.
##
install_traps() {
  trap 'on_error "$?" "$LINENO" "$BASH_COMMAND"' ERR
  trap 'on_exit "$?"' EXIT
  trap 'on_signal "SIGINT" 130' INT
  trap 'on_signal "SIGTERM" 143' TERM
}

# -----------------------------------------------------------------------------
# Command-line interface
# -----------------------------------------------------------------------------

##
# Prints command usage to stdout.
##
print_usage() {
  printf "Usage: %s [OPTIONS]\n" "${0##*/}"
  printf "\n"
  printf "Initialize the host-side, repository-agnostic Dev Container baseline.\n"
  printf "\n"
  printf "Options:\n"
  printf "  --devcontainer-id ID  Record and display the Dev Container identifier.\n"
  printf "  --dry-run             Report actions without modifying files or running hooks.\n"
  printf "  --force               Ignore a matching initialization marker and run again.\n"
  printf "  --verbose             Print additional diagnostic information.\n"
  printf "  --help                Show this help text.\n"
}

##
# Parses supported command-line options.
#
# Arguments:
#   $@ - Script arguments.
##
parse_arguments() {
  while (($# > 0)); do
    case "$1" in
    --devcontainer-id)
      (($# >= 2)) || usage_error "Option --devcontainer-id requires a value."
      DEVCONTAINER_ID="$2"
      shift
      ;;
    --devcontainer-id=*)
      DEVCONTAINER_ID="${1#*=}"
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
    --force)
      FORCE_INITIALIZATION=1
      ;;
    --verbose)
      VERBOSE=1
      ;;
    --help)
      print_usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      usage_error "Unknown option: $1"
      ;;
    *)
      usage_error "Unexpected positional argument: $1"
      ;;
    esac

    shift
  done

  if (($# > 0)); then
    usage_error "Unexpected positional argument: $1"
  fi
}

##
# Validates and normalizes the optional Dev Container identifier.
#
# Globals:
#   DEVCONTAINER_ID
##
normalize_devcontainer_id() {
  if [[ $DEVCONTAINER_ID == "\${devcontainerId}" ]]; then
    print_warning "The devcontainerId substitution was not resolved by this implementation."
    DEVCONTAINER_ID=""
    return 0
  fi

  case "$DEVCONTAINER_ID" in
  *$'\n'* | *$'\r'*)
    usage_error "The Dev Container ID must not contain line breaks."
    ;;
  esac
}

# -----------------------------------------------------------------------------
# Path and environment setup
# -----------------------------------------------------------------------------

##
# Resolves an absolute, physical path for an existing directory.
#
# Arguments:
#   $1 - Directory to resolve.
#
# Outputs:
#   Writes the resolved path to stdout.
##
resolve_directory() {
  local directory="${1:?Directory path is required}"

  (
    cd -- "$directory"
    pwd -P
  )
}

##
# Resolves the script directory, repository root, and marker path.
##
resolve_paths() {
  SCRIPT_DIRECTORY="$(resolve_directory "$(dirname "${BASH_SOURCE[0]}")")"

  if [[ -n ${DEVCONTAINER_REPO_ROOT:-} ]]; then
    REPO_ROOT="$(resolve_directory "$DEVCONTAINER_REPO_ROOT")"
  else
    REPO_ROOT="$(resolve_directory "$SCRIPT_DIRECTORY/../..")"
  fi

  INITIALIZATION_MARKER_FILE="${REPO_ROOT}/${DEVCONTAINER_CACHE_DIRECTORY}/${INITIALIZATION_MARKER_NAME}"

  [[ -d $REPO_ROOT/$DEVCONTAINER_DIRECTORY ]] ||
    print_warning "Expected Dev Container directory not found: $REPO_ROOT/$DEVCONTAINER_DIRECTORY"
}

##
# Adds a directory to the beginning of PATH unless already present.
#
# Arguments:
#   $1 - Directory to add.
##
prepend_path_once() {
  local directory="${1:?Directory path is required}"

  case ":${PATH:-}:" in
  *":$directory:"*) ;;
  *) PATH="$directory${PATH:+:$PATH}" ;;
  esac

  export PATH
}

##
# Configures the environment inherited by repository-specific hooks.
##
configure_environment() {
  : "${HOME:?HOME must be set for Dev Container initialization}"

  export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
  export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
  export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
  export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

  export DEVCONTAINER_ID
  export DEVCONTAINER_LIFECYCLE="initialize"
  export DEVCONTAINER_REPO_ROOT="$REPO_ROOT"
  export DEVCONTAINER_SCRIPT_DIRECTORY="$SCRIPT_DIRECTORY"

  prepend_path_once "$HOME/.local/bin"
  prepend_path_once "$HOME/bin"

  print_debug "Host: $(uname -s 2>/dev/null || printf "unknown")/$(uname -m 2>/dev/null || printf "unknown")"
  print_debug "PATH: $PATH"
}

# -----------------------------------------------------------------------------
# Repository-local baseline state
# -----------------------------------------------------------------------------

##
# Creates a directory when it does not already exist.
#
# Arguments:
#   $1 - Directory to create.
#   $2 - Optional directory mode. Defaults to 0775.
##
ensure_directory() {
  local directory="${1:?Directory path is required}"
  local mode="${2:-0775}"

  if [[ -d $directory ]]; then
    print_debug "Directory already exists: $directory"
    return 0
  fi

  if ((DRY_RUN == 1)); then
    print_status "Would create directory: $directory"
    return 0
  fi

  print_status "Creating directory: $directory"
  mkdir -p "$directory"

  if ! chmod "$mode" "$directory" 2>/dev/null; then
    print_warning "Could not set mode $mode on directory: $directory"
  fi
}

##
# Creates harmless repository-local cache and temporary directories.
##
create_required_directories() {
  ensure_directory "$REPO_ROOT/$DEVCONTAINER_CACHE_DIRECTORY"
  ensure_directory "$REPO_ROOT/$DEVCONTAINER_TEMP_DIRECTORY"
  ensure_directory "$REPO_ROOT/.cache"
  ensure_directory "$REPO_ROOT/.tmp"
}

##
# Optionally creates .env from .env.example with private permissions.
##
create_environment_file_if_requested() {
  local destination="$REPO_ROOT/.env"
  local source="$REPO_ROOT/.env.example"

  is_enabled "${DEVCONTAINER_INIT_CREATE_ENV:-0}" || return 0

  if [[ ! -f $source ]]; then
    print_debug "Environment template not found: $source"
    return 0
  fi

  if [[ -e $destination || -L $destination ]]; then
    print_debug "Environment file already exists: $destination"
    return 0
  fi

  if ((DRY_RUN == 1)); then
    print_status "Would create .env from .env.example"
    return 0
  fi

  print_status "Creating .env from .env.example"
  (
    umask 0077
    cp "$source" "$destination"
  )
}

##
# Determines whether the completion marker matches the current configuration.
#
# Returns:
#   0 when a matching marker exists; otherwise 1.
##
is_already_initialized() {
  [[ -f $INITIALIZATION_MARKER_FILE ]] || return 1

  grep -Fqx "schema_version=$INITIALIZATION_SCHEMA_VERSION" \
    "$INITIALIZATION_MARKER_FILE" || return 1

  if [[ -n $DEVCONTAINER_ID ]]; then
    grep -Fqx "devcontainer_id=$DEVCONTAINER_ID" \
      "$INITIALIZATION_MARKER_FILE" || return 1
  fi

  return 0
}

##
# Atomically writes the initialization completion marker.
##
write_initialization_marker() {
  local initialized_at

  if ((DRY_RUN == 1)); then
    print_status "Would write initialization marker: $INITIALIZATION_MARKER_FILE"
    return 0
  fi

  initialized_at="$(date -u "+%Y-%m-%dT%H:%M:%SZ")"
  TEMPORARY_FILE="$(mktemp "${INITIALIZATION_MARKER_FILE}.tmp.XXXXXX")"

  {
    printf "schema_version=%s\n" "$INITIALIZATION_SCHEMA_VERSION"
    printf "initialized_at=%s\n" "$initialized_at"
    printf "devcontainer_id=%s\n" "$DEVCONTAINER_ID"
    printf "repository_root=%s\n" "$REPO_ROOT"
  } >"$TEMPORARY_FILE"

  chmod 0600 "$TEMPORARY_FILE"
  mv "$TEMPORARY_FILE" "$INITIALIZATION_MARKER_FILE"
  TEMPORARY_FILE=""

  print_status "Wrote initialization marker: $INITIALIZATION_MARKER_FILE"
}

# -----------------------------------------------------------------------------
# Extension hooks and project reporting
# -----------------------------------------------------------------------------

##
# Executes one repository-specific initialization hook.
#
# Arguments:
#   $1 - Hook path.
##
run_hook() {
  local hook="${1:?Hook path is required}"
  local relative_hook="${hook#"$REPO_ROOT"/}"

  if ((DRY_RUN == 1)); then
    print_status "Would run hook: $relative_hook"
    return 0
  fi

  print_status "Running hook: $relative_hook"

  if bash "$hook"; then
    return 0
  fi

  if is_enabled "${DEVCONTAINER_INIT_CONTINUE_ON_HOOK_FAILURE:-0}"; then
    print_warning "Hook failed; continuing: $relative_hook"
    return 0
  fi

  die "Hook failed: $relative_hook"
}

##
# Discovers and executes local hooks in deterministic filename order.
##
run_extension_hooks() {
  local hooks_directory="$REPO_ROOT/$DEVCONTAINER_DIRECTORY/scripts/initialize.d"
  local local_hook="$REPO_ROOT/$DEVCONTAINER_DIRECTORY/scripts/initialize.local.sh"
  local hook
  local nullglob_was_enabled=0
  local previous_lc_all="${LC_ALL-}"
  local -a hooks=()

  if [[ -f $local_hook ]]; then
    run_hook "$local_hook"
  fi

  [[ -d $hooks_directory ]] || return 0

  if shopt -q nullglob; then
    nullglob_was_enabled=1
  fi

  LC_ALL=C
  shopt -s nullglob
  hooks=("$hooks_directory"/*.sh)

  if ((nullglob_was_enabled == 0)); then
    shopt -u nullglob
  fi

  if [[ -n $previous_lc_all ]]; then
    LC_ALL="$previous_lc_all"
  else
    unset LC_ALL
  fi

  for hook in "${hooks[@]}"; do
    [[ -f $hook ]] || continue
    run_hook "$hook"
  done
}

##
# Joins arguments with a comma and a space.
#
# Arguments:
#   $@ - Labels to join.
#
# Outputs:
#   Writes the joined labels to stdout.
##
join_labels() {
  local label
  local separator=""

  for label in "$@"; do
    printf "%s%s" "$separator" "$label"
    separator=", "
  done
}

##
# Reports recognized project manifests without installing dependencies.
##
report_detected_tooling() {
  local -a detected=()

  [[ -f $REPO_ROOT/package.json ]] && detected+=("Node.js")
  [[ -f $REPO_ROOT/pyproject.toml || -f $REPO_ROOT/requirements.txt || -f $REPO_ROOT/setup.py ]] &&
    detected+=("Python")
  [[ -f $REPO_ROOT/Cargo.toml ]] && detected+=("Rust")
  [[ -f $REPO_ROOT/go.mod ]] && detected+=("Go")
  [[ -f $REPO_ROOT/pom.xml || -f $REPO_ROOT/build.gradle || -f $REPO_ROOT/build.gradle.kts ]] &&
    detected+=("Java/JVM")
  [[ -f $REPO_ROOT/Gemfile ]] && detected+=("Ruby")
  [[ -f $REPO_ROOT/composer.json ]] && detected+=("PHP")
  [[ -f $REPO_ROOT/compose.yaml || -f $REPO_ROOT/compose.yml || -f $REPO_ROOT/docker-compose.yaml || -f $REPO_ROOT/docker-compose.yml ]] &&
    detected+=("Docker Compose")
  [[ -f $REPO_ROOT/Taskfile.yml || -f $REPO_ROOT/Taskfile.yaml ]] && detected+=("Task")
  [[ -f $REPO_ROOT/Makefile ]] && detected+=("Make")

  if ((${#detected[@]} == 0)); then
    print_debug "No common project manifests detected."
    return 0
  fi

  print_status "Detected project tooling: $(join_labels "${detected[@]}")"
}

# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

##
# Runs the host-side Dev Container initialization lifecycle.
#
# Arguments:
#   $@ - Script arguments.
##
main() {
  parse_arguments "$@"
  normalize_devcontainer_id
  install_traps

  if is_enabled "${DEVCONTAINER_INIT_VERBOSE:-0}"; then
    VERBOSE=1
  fi

  if is_enabled "${DEVCONTAINER_INIT_FORCE:-0}"; then
    FORCE_INITIALIZATION=1
  fi

  if is_enabled "${DEVCONTAINER_INIT_TRACE:-0}"; then
    set -o xtrace
  fi

  resolve_paths
  cd -- "$REPO_ROOT"
  configure_environment

  print_status "Initializing development container host state."
  print_status "Repository root: $REPO_ROOT"

  if [[ -n $DEVCONTAINER_ID ]]; then
    print_status "Dev Container ID: $DEVCONTAINER_ID"
  else
    print_status "Dev Container ID: unavailable"
  fi

  create_required_directories
  create_environment_file_if_requested
  report_detected_tooling

  if ((FORCE_INITIALIZATION == 0)) && is_already_initialized; then
    print_status "Development container host state is already initialized."
    return 0
  fi

  run_extension_hooks
  write_initialization_marker

  print_status "Development container host initialization complete."
}

main "$@"
