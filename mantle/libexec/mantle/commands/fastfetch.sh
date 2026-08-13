#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# Provide compact, privacy-conscious values for Mantle's Fastfetch config.

set -o errexit
set -o nounset
set -o pipefail

mantle_fastfetch_usage() {
	printf "%s\n" \
		"Usage: mantle fastfetch COLLECTOR" \
		"" \
		"Collectors:" \
		"  runtime      Runtime environment and active shell" \
		"  workspace    Current workspace name and Git branch" \
		"  toolchains   Available development toolchains" \
		"  contexts     CI, container, and remote-session contexts"
}

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	printf "[mantle:error] MANTLE_ROOT is required for command dispatch\n" >&2
	exit 70
fi

if (($# == 0)); then
	mantle_fastfetch_usage
	exit 0
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
esac

if (($# != 1)) || [[ ! "$1" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
	printf "[mantle:error] fastfetch requires exactly one collector name\n" >&2
	mantle_fastfetch_usage >&2
	exit 64
fi

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
		printf "local\n"
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

case "$1" in
	runtime)
		printf "%s · %s\n" "$(mantle_fastfetch_runtime_environment)" "$(mantle_fastfetch_shell_name)"
		;;
	workspace)
		if command -v git >/dev/null 2>&1 && git rev-parse --show-toplevel >/dev/null 2>&1; then
			mantle_fastfetch_workspace_root="$(git rev-parse --show-toplevel 2>/dev/null)"
			mantle_fastfetch_workspace_branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || printf "detached")"
			printf "%s · %s\n" "$(basename -- "${mantle_fastfetch_workspace_root}")" "${mantle_fastfetch_workspace_branch}"
		else
			printf "%s\n" "$(basename -- "${PWD}")"
		fi
		;;
	toolchains)
		mantle_fastfetch_toolchains=""
		for mantle_fastfetch_tool in git python3 node go rustc java; do
			if command -v "${mantle_fastfetch_tool}" >/dev/null 2>&1; then
				if [[ -n "${mantle_fastfetch_toolchains}" ]]; then
					mantle_fastfetch_toolchains="${mantle_fastfetch_toolchains} · ${mantle_fastfetch_tool}"
				else
					mantle_fastfetch_toolchains="${mantle_fastfetch_tool}"
				fi
			fi
		done
		printf "%s\n" "${mantle_fastfetch_toolchains:-none detected}"
		;;
	contexts)
		mantle_fastfetch_contexts="$(mantle_fastfetch_runtime_environment)"
		if [[ -n "${SSH_CONNECTION:-}" || -n "${SSH_TTY:-}" ]]; then
			mantle_fastfetch_contexts="${mantle_fastfetch_contexts} · ssh"
		fi
		if [[ -n "${CODESPACES:-}" ]]; then
			mantle_fastfetch_contexts="${mantle_fastfetch_contexts} · codespaces"
		fi
		printf "%s\n" "${mantle_fastfetch_contexts}"
		;;
	*)
		printf "[mantle:error] unknown fastfetch collector: %s\n" "$1" >&2
		mantle_fastfetch_usage >&2
		exit 64
		;;
esac
