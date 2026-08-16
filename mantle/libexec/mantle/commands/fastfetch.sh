#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2312 # Substitutions are validated by their enclosing operation.
# Provide compact, privacy-conscious values for Mantle's Fastfetch config.

set -o errexit
set -o nounset
set -o pipefail

mantle_fastfetch_usage() {
	printf "%s\n" \
		"Usage: mantle fastfetch COLLECTOR" \
		"" \
		"Collectors:" \
		"  runtime      Mantle version, active shell, environment, and OS family" \
		"  workspace    Current directory or compact Git workspace state" \
		"  toolchains   Installed Git, Node, Python, Rust, Go, and Task versions" \
		"  contexts     Active local Docker and Kubernetes client contexts" \
		"" \
		"Options:" \
		"  --help       Show help and exit." \
		"  --version    Show Mantle's central version and exit."
}

mantle_fastfetch_error() {
	printf "[mantle:error] %s\n" "$1" >&2
}

mantle_fastfetch_first_line() {
	local first_line=""
	IFS= read -r first_line || true
	printf "%s\n" "${first_line}"
}

mantle_fastfetch_runtime_environment() {
	if [[ -n "${MANTLE_RUNTIME_ENVIRONMENT:-}" ]]; then
		printf "%s\n" "${MANTLE_RUNTIME_ENVIRONMENT}"
	elif [[ -n "${GITHUB_ACTIONS:-}" || "${CI:-}" == "1" || "${CI:-}" == "true" ]]; then
		printf "ci\n"
	elif [[ -n "${DEVCONTAINER:-}" || -n "${REMOTE_CONTAINERS:-}" ]]; then
		printf "devcontainer\n"
	elif [[ -n "${WSL_DISTRO_NAME:-}" ]]; then
		printf "wsl\n"
	elif [[ -n "${container:-}" || -f "/.dockerenv" ]]; then
		printf "container\n"
	else
		printf "native\n"
	fi
}

mantle_fastfetch_shell_name() {
	if [[ -n "${MANTLE_SHELL_NAME:-}" ]]; then
		printf "%s\n" "${MANTLE_SHELL_NAME}"
	elif [[ -n "${SHELL:-}" ]]; then
		basename -- "${SHELL}"
	else
		printf "unknown\n"
	fi
}

mantle_fastfetch_os_family() {
	local kernel_name=""
	kernel_name="$(uname -s 2>/dev/null || true)"
	case "${kernel_name}" in
	Darwin) printf "macOS\n" ;;
	Linux) printf "Linux\n" ;;
	*) printf "%s\n" "${kernel_name:-unknown}" ;;
	esac
}

mantle_fastfetch_version() {
	"${MANTLE_ROOT}/bin/mantle" version --short
}

mantle_fastfetch_runtime() {
	printf "mantle %s · %s · %s %s\n" \
		"$(mantle_fastfetch_version)" \
		"$(mantle_fastfetch_shell_name)" \
		"$(mantle_fastfetch_runtime_environment)" \
		"$(mantle_fastfetch_os_family)"
}

mantle_fastfetch_abbreviate_directory() {
	local directory="${1:-${PWD:-unknown}}"
	if [[ -n "${HOME:-}" && "${directory}" == "${HOME}" ]]; then
		printf "~\n"
	elif [[ -n "${HOME:-}" && "${directory}" == "${HOME}/"* ]]; then
		printf "%s/%s\n" "~" "${directory#"${HOME}/"}"
	else
		printf "%s\n" "${directory}"
	fi
}

mantle_fastfetch_workspace() {
	local repository_root=""
	local workspace_name=""
	local workspace_ref=""
	local workspace_state=""
	local porcelain=""

	if ! command -v git >/dev/null 2>&1 ||
		! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
		mantle_fastfetch_abbreviate_directory "${PWD:-unknown}"
		return 0
	fi

	repository_root="$(git rev-parse --show-toplevel 2>/dev/null)" || {
		mantle_fastfetch_abbreviate_directory "${PWD:-unknown}"
		return 0
	}
	workspace_name="$(basename -- "${repository_root}")"
	workspace_ref="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
	if [[ -z "${workspace_ref}" ]]; then
		workspace_ref="$(git rev-parse --short HEAD 2>/dev/null || true)"
	fi
	if [[ -z "${workspace_ref}" ]]; then
		workspace_ref="unborn"
	fi

	porcelain="$(git status --porcelain=v1 --untracked-files=normal --ignore-submodules=all 2>/dev/null || true)"
	if [[ -z "${porcelain}" ]]; then
		workspace_state="✓ clean"
	else
		workspace_state="● changed"
	fi
	printf "%s · %s · %s\n" "${workspace_name}" "${workspace_ref}" "${workspace_state}"
}

mantle_fastfetch_emit_toolchain() {
	local label="$1"
	local value="$2"
	if [[ -z "${value}" ]]; then
		return 0
	fi
	if [[ -n "${MANTLE_FASTFETCH_TOOLCHAINS}" ]]; then
		MANTLE_FASTFETCH_TOOLCHAINS="${MANTLE_FASTFETCH_TOOLCHAINS} · ${label} ${value}"
	else
		MANTLE_FASTFETCH_TOOLCHAINS="${label} ${value}"
	fi
}

mantle_fastfetch_tool_version() {
	local tool_name="$1"
	local raw_version=""
	local _discard=""
	local parsed_version=""

	case "${tool_name}" in
	git)
		raw_version="$(git --version 2>/dev/null | mantle_fastfetch_first_line)"
		parsed_version="${raw_version#git version }"
		;;
	node)
		raw_version="$(node --version 2>/dev/null | mantle_fastfetch_first_line)"
		parsed_version="${raw_version#v}"
		;;
	python3)
		raw_version="$(python3 --version 2>&1 | mantle_fastfetch_first_line)"
		parsed_version="${raw_version#Python }"
		;;
	rustc)
		raw_version="$(rustc --version 2>/dev/null | mantle_fastfetch_first_line)"
		read -r _discard parsed_version _discard <<<"${raw_version}"
		;;
	go)
		raw_version="$(go version 2>/dev/null | mantle_fastfetch_first_line)"
		read -r _discard _discard parsed_version _discard <<<"${raw_version}"
		parsed_version="${parsed_version#go}"
		;;
	task)
		raw_version="$(task --version 2>/dev/null | mantle_fastfetch_first_line)"
		parsed_version="${raw_version##* }"
		parsed_version="${parsed_version#v}"
		;;
	esac
	printf "%s\n" "${parsed_version}"
}

mantle_fastfetch_toolchains() {
	local tool_name=""
	local display_name=""
	local version=""
	MANTLE_FASTFETCH_TOOLCHAINS=""

	for tool_name in git node python3 rustc go task; do
		command -v "${tool_name}" >/dev/null 2>&1 || continue
		version="$(mantle_fastfetch_tool_version "${tool_name}")"
		case "${tool_name}" in
		git) display_name="git" ;;
		node) display_name="node" ;;
		python3) display_name="python" ;;
		rustc) display_name="rust" ;;
		go) display_name="go" ;;
		task) display_name="task" ;;
		esac
		mantle_fastfetch_emit_toolchain "${display_name}" "${version:-unknown}"
	done

	printf "%s\n" "${MANTLE_FASTFETCH_TOOLCHAINS:-none detected}"
}

mantle_fastfetch_emit_context() {
	local label="$1"
	local value="$2"
	if [[ -z "${value}" ]]; then
		return 0
	fi
	if [[ -n "${MANTLE_FASTFETCH_CONTEXTS}" ]]; then
		MANTLE_FASTFETCH_CONTEXTS="${MANTLE_FASTFETCH_CONTEXTS} · ${label} ${value}"
	else
		MANTLE_FASTFETCH_CONTEXTS="${label} ${value}"
	fi
}

mantle_fastfetch_contexts() {
	local context_value=""
	MANTLE_FASTFETCH_CONTEXTS=""

	if command -v docker >/dev/null 2>&1; then
		context_value="$(docker context show 2>/dev/null | mantle_fastfetch_first_line || true)"
		mantle_fastfetch_emit_context "docker" "${context_value}"
	fi
	if command -v kubectl >/dev/null 2>&1; then
		context_value="$(kubectl config current-context 2>/dev/null | mantle_fastfetch_first_line || true)"
		mantle_fastfetch_emit_context "k8s" "${context_value}"
	fi

	printf "%s\n" "${MANTLE_FASTFETCH_CONTEXTS:-none active}"
}

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	mantle_fastfetch_error "MANTLE_ROOT is required for command dispatch"
	exit 70
fi

if (($# == 0)); then
	mantle_fastfetch_error "fastfetch requires exactly one collector name"
	mantle_fastfetch_usage >&2
	exit 64
fi

case "$1" in
--summary)
	printf "Collect compact values for Mantle's Fastfetch config.\n"
	exit 0
	;;
--help | -h)
	mantle_fastfetch_usage
	exit 0
	;;
--version)
	if (($# != 1)); then
		mantle_fastfetch_error "--version does not accept arguments"
		exit 64
	fi
	"${MANTLE_ROOT}/bin/mantle" version
	exit 0
	;;
esac

if (($# != 1)) || [[ ! "$1" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
	mantle_fastfetch_error "fastfetch requires exactly one collector name"
	mantle_fastfetch_usage >&2
	exit 64
fi

case "$1" in
runtime) mantle_fastfetch_runtime ;;
workspace) mantle_fastfetch_workspace ;;
toolchains) mantle_fastfetch_toolchains ;;
contexts) mantle_fastfetch_contexts ;;
*)
	mantle_fastfetch_error "unknown fastfetch collector: $1"
	mantle_fastfetch_usage >&2
	exit 64
	;;
esac
