#!/usr/bin/env bash
# shellcheck shell=bash
#
# @file on-create.sh
# @brief Container-side initialization after a development container is created.
# @description
#   Prepares user-local and repository-local state inside a newly created
#   development container. This script is lightweight, idempotent, safe to run
#   repeatedly, and intentionally independent of any specific repository
#   toolchain.
#
#   Responsibilities:
#   - validate the container workspace and user environment
#   - create baseline XDG, cache, state, and temporary directories
#   - report container identity and common project manifests
#   - execute repository-specific extension hooks
#   - establish a container-aware completion marker
#
#   Non-responsibilities:
#   - installing project dependencies
#   - selecting a repository package manager
#   - changing global Git configuration
#   - changing ownership of arbitrary workspace content
#   - starting long-running services
#
# Extension points, executed in this order:
#   .devcontainer/scripts/on-create.local.sh
#   .devcontainer/scripts/on-create.d/*.sh
#
# Supported environment variables:
#   DEVCONTAINER_ID
#     Dev Container configuration identifier. The --devcontainer-id option
#     takes precedence when both are provided.
#   DEVCONTAINER_RUNTIME_ID
#     Runtime container identifier. The --container-id option takes precedence.
#     When absent, the script derives the value from /etc/hostname or hostname.
#   DEVCONTAINER_REPO_ROOT
#     Override repository-root discovery.
#   DEVCONTAINER_ON_CREATE_CONTINUE_ON_HOOK_FAILURE=1
#     Warn and continue when an extension hook fails. The default is fail-fast.
#   DEVCONTAINER_ON_CREATE_FORCE=1
#     Run initialization even when a matching completion marker exists.
#   DEVCONTAINER_ON_CREATE_VERBOSE=1
#     Enable verbose diagnostic logging.
#   DEVCONTAINER_ON_CREATE_TRACE=1
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

readonly STATUS_PREFIX="📦 [devcontainer:on-create]"
readonly WARNING_PREFIX="⚠️  [devcontainer:on-create]"
readonly ERROR_PREFIX="❌ [devcontainer:on-create]"
readonly DEBUG_PREFIX="🔎 [devcontainer:on-create]"

readonly DEVCONTAINER_DIRECTORY=".devcontainer"
readonly ON_CREATE_STATE_DIRECTORY_NAME="devcontainer"
readonly ON_CREATE_MARKER_NAME="on-create.complete"
readonly ON_CREATE_SCHEMA_VERSION="1"

# -----------------------------------------------------------------------------
# Runtime state
# -----------------------------------------------------------------------------

REPO_ROOT=""
SCRIPT_DIRECTORY=""
ON_CREATE_STATE_DIRECTORY=""
ON_CREATE_MARKER_FILE=""
TEMPORARY_FILE=""
DEVCONTAINER_ID="${DEVCONTAINER_ID:-}"
RUNTIME_CONTAINER_ID="${DEVCONTAINER_RUNTIME_ID:-}"
DRY_RUN=0
FORCE_ON_CREATE=0
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
        print_warning "On-create lifecycle stopped with exit code $exit_code."
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
    print_warning "Received $signal_name; stopping the on-create lifecycle."
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
    printf "Initialize the container-side, repository-agnostic Dev Container baseline.\n"
    printf "\n"
    printf "Options:\n"
    printf "  --devcontainer-id ID  Record and display the Dev Container identifier.\n"
    printf "  --container-id ID     Override runtime container identity detection.\n"
    printf "  --dry-run             Report actions without modifying files or running hooks.\n"
    printf "  --force               Ignore a matching on-create marker and run again.\n"
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
            --container-id)
                (($# >= 2)) || usage_error "Option --container-id requires a value."
                RUNTIME_CONTAINER_ID="$2"
                shift
                ;;
            --container-id=*)
                RUNTIME_CONTAINER_ID="${1#*=}"
                ;;
            --dry-run)
                DRY_RUN=1
                ;;
            --force)
                FORCE_ON_CREATE=1
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
# Rejects line breaks in an identifier used by the completion marker.
#
# Arguments:
#   $1 - Identifier label.
#   $2 - Identifier value.
##
validate_identifier() {
    local label="${1:?Identifier label is required}"
    local value="${2:-}"

    case "$value" in
        *$'\n'* | *$'\r'*)
            usage_error "$label must not contain line breaks."
            ;;
    esac
}

##
# Validates and normalizes the optional Dev Container identifier.
##
normalize_devcontainer_id() {
    if [[ $DEVCONTAINER_ID == "\${devcontainerId}" ]]; then
        print_warning "The devcontainerId substitution was not resolved by this implementation."
        DEVCONTAINER_ID=""
    fi

    validate_identifier "The Dev Container ID" "$DEVCONTAINER_ID"
}

# -----------------------------------------------------------------------------
# Path, identity, and environment setup
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
# Resolves the script directory and repository root.
##
resolve_paths() {
    SCRIPT_DIRECTORY="$(resolve_directory "$(dirname "${BASH_SOURCE[0]}")")"

    if [[ -n ${DEVCONTAINER_REPO_ROOT:-} ]]; then
        REPO_ROOT="$(resolve_directory "$DEVCONTAINER_REPO_ROOT")"
    else
        REPO_ROOT="$(resolve_directory "$SCRIPT_DIRECTORY/../..")"
    fi

    [[ -d $REPO_ROOT/$DEVCONTAINER_DIRECTORY ]] ||
        print_warning "Expected Dev Container directory not found: $REPO_ROOT/$DEVCONTAINER_DIRECTORY"
}

##
# Resolves the runtime container identifier when one was not supplied.
##
resolve_runtime_container_id() {
    if [[ -n $RUNTIME_CONTAINER_ID ]]; then
        validate_identifier "The runtime container ID" "$RUNTIME_CONTAINER_ID"
        return 0
    fi

    if [[ -r /etc/hostname ]]; then
        IFS= read -r RUNTIME_CONTAINER_ID < /etc/hostname || true
    fi

    if [[ -z $RUNTIME_CONTAINER_ID ]] && command -v hostname > /dev/null 2>&1; then
        RUNTIME_CONTAINER_ID="$(hostname 2> /dev/null || true)"
    fi

    if [[ -z $RUNTIME_CONTAINER_ID && -n ${HOSTNAME:-} ]]; then
        RUNTIME_CONTAINER_ID="$HOSTNAME"
    fi

    validate_identifier "The runtime container ID" "$RUNTIME_CONTAINER_ID"
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
    : "${HOME:?HOME must be set for the Dev Container on-create lifecycle}"

    export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
    export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
    export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
    export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

    ON_CREATE_STATE_DIRECTORY="$XDG_STATE_HOME/$ON_CREATE_STATE_DIRECTORY_NAME"
    ON_CREATE_MARKER_FILE="$ON_CREATE_STATE_DIRECTORY/$ON_CREATE_MARKER_NAME"

    export DEVCONTAINER_ID
    export DEVCONTAINER_RUNTIME_ID="$RUNTIME_CONTAINER_ID"
    export DEVCONTAINER_LIFECYCLE="on-create"
    export DEVCONTAINER_REPO_ROOT="$REPO_ROOT"
    export DEVCONTAINER_SCRIPT_DIRECTORY="$SCRIPT_DIRECTORY"

    prepend_path_once "$HOME/.local/bin"
    prepend_path_once "$HOME/bin"

    print_debug "Platform: $(uname -s 2> /dev/null || printf "unknown")/$(uname -m 2> /dev/null || printf "unknown")"
    print_debug "PATH: $PATH"
}

# -----------------------------------------------------------------------------
# Container and workspace baseline
# -----------------------------------------------------------------------------

##
# Validates basic workspace and home-directory expectations.
##
validate_environment() {
    [[ -d $REPO_ROOT ]] || die "Repository root does not exist: $REPO_ROOT"
    [[ -r $REPO_ROOT ]] || die "Repository root is not readable: $REPO_ROOT"
    [[ -d $HOME ]] || die "Home directory does not exist: $HOME"

    if [[ ! -w $REPO_ROOT ]]; then
        print_warning "Repository root is not writable: $REPO_ROOT"
    fi

    if [[ ! -w $HOME ]]; then
        print_warning "Home directory is not writable: $HOME"
    fi
}

##
# Creates a directory when it does not already exist.
#
# Arguments:
#   $1 - Directory to create.
#   $2 - Optional directory mode. Defaults to 0755.
##
ensure_directory() {
    local directory="${1:?Directory path is required}"
    local mode="${2:-0755}"

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

    if ! chmod "$mode" "$directory" 2> /dev/null; then
        print_warning "Could not set mode $mode on directory: $directory"
    fi
}

##
# Creates baseline user-local and repository-local directories.
##
create_required_directories() {
    ensure_directory "$HOME/.local/bin"
    ensure_directory "$XDG_CACHE_HOME"
    ensure_directory "$XDG_CONFIG_HOME"
    ensure_directory "$XDG_DATA_HOME"
    ensure_directory "$XDG_STATE_HOME"
    ensure_directory "$ON_CREATE_STATE_DIRECTORY" 0700
    ensure_directory "$REPO_ROOT/.cache" 0775
    ensure_directory "$REPO_ROOT/.tmp" 0775
}

##
# Reports the effective user and container identifiers.
##
report_runtime_identity() {
    local user_name
    local user_id
    local group_name
    local group_id

    user_name="$(id -un 2> /dev/null || printf "unknown")"
    user_id="$(id -u 2> /dev/null || printf "unknown")"
    group_name="$(id -gn 2> /dev/null || printf "unknown")"
    group_id="$(id -g 2> /dev/null || printf "unknown")"

    print_status "Container user: $user_name (uid=$user_id, gid=$group_id, group=$group_name)"

    if [[ -n $DEVCONTAINER_ID ]]; then
        print_status "Dev Container ID: $DEVCONTAINER_ID"
    else
        print_status "Dev Container ID: unavailable"
    fi

    if [[ -n $RUNTIME_CONTAINER_ID ]]; then
        print_status "Runtime container ID: $RUNTIME_CONTAINER_ID"
    else
        print_status "Runtime container ID: unavailable"
    fi
}

##
# Determines whether the completion marker matches the current container.
#
# Returns:
#   0 when a matching marker exists; otherwise 1.
##
is_already_created() {
    [[ -f $ON_CREATE_MARKER_FILE ]] || return 1

    grep -Fqx "schema_version=$ON_CREATE_SCHEMA_VERSION" \
        "$ON_CREATE_MARKER_FILE" || return 1

    if [[ -n $DEVCONTAINER_ID ]]; then
        grep -Fqx "devcontainer_id=$DEVCONTAINER_ID" \
            "$ON_CREATE_MARKER_FILE" || return 1
    fi

    if [[ -n $RUNTIME_CONTAINER_ID ]]; then
        grep -Fqx "runtime_container_id=$RUNTIME_CONTAINER_ID" \
            "$ON_CREATE_MARKER_FILE" || return 1
    fi

    return 0
}

##
# Atomically writes the on-create completion marker.
##
write_on_create_marker() {
    local completed_at

    if ((DRY_RUN == 1)); then
        print_status "Would write on-create marker: $ON_CREATE_MARKER_FILE"
        return 0
    fi

    completed_at="$(date -u "+%Y-%m-%dT%H:%M:%SZ")"
    TEMPORARY_FILE="$(mktemp "${ON_CREATE_MARKER_FILE}.tmp.XXXXXX")"

    {
        printf "schema_version=%s\n" "$ON_CREATE_SCHEMA_VERSION"
        printf "completed_at=%s\n" "$completed_at"
        printf "devcontainer_id=%s\n" "$DEVCONTAINER_ID"
        printf "runtime_container_id=%s\n" "$RUNTIME_CONTAINER_ID"
        printf "repository_root=%s\n" "$REPO_ROOT"
    } > "$TEMPORARY_FILE"

    chmod 0600 "$TEMPORARY_FILE"
    mv "$TEMPORARY_FILE" "$ON_CREATE_MARKER_FILE"
    TEMPORARY_FILE=""

    print_status "Wrote on-create marker: $ON_CREATE_MARKER_FILE"
}

# -----------------------------------------------------------------------------
# Extension hooks and project reporting
# -----------------------------------------------------------------------------

##
# Executes one repository-specific on-create hook.
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

    if is_enabled "${DEVCONTAINER_ON_CREATE_CONTINUE_ON_HOOK_FAILURE:-0}"; then
        print_warning "Hook failed; continuing: $relative_hook"
        return 0
    fi

    die "Hook failed: $relative_hook"
}

##
# Discovers and executes on-create hooks in deterministic filename order.
##
run_extension_hooks() {
    local hooks_directory="$REPO_ROOT/$DEVCONTAINER_DIRECTORY/scripts/on-create.d"
    local local_hook="$REPO_ROOT/$DEVCONTAINER_DIRECTORY/scripts/on-create.local.sh"
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
# Runs the container-side Dev Container on-create lifecycle.
#
# Arguments:
#   $@ - Script arguments.
##
main() {
    parse_arguments "$@"
    normalize_devcontainer_id
    install_traps

    if is_enabled "${DEVCONTAINER_ON_CREATE_VERBOSE:-0}"; then
        VERBOSE=1
    fi

    if is_enabled "${DEVCONTAINER_ON_CREATE_FORCE:-0}"; then
        FORCE_ON_CREATE=1
    fi

    if is_enabled "${DEVCONTAINER_ON_CREATE_TRACE:-0}"; then
        set -o xtrace
    fi

    resolve_paths
    resolve_runtime_container_id
    cd -- "$REPO_ROOT"
    configure_environment

    print_status "Preparing newly created development container."
    print_status "Repository root: $REPO_ROOT"

    validate_environment
    report_runtime_identity
    create_required_directories
    report_detected_tooling

    if ((FORCE_ON_CREATE == 0)) && is_already_created; then
        print_status "Development container on-create state is already complete."
        return 0
    fi

    run_extension_hooks
    write_on_create_marker

    print_status "Development container on-create lifecycle complete."
}

main "$@"
