#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# Print Mantle-owned runtime state without exposing the entire environment.

set -o errexit
set -o nounset
set -o pipefail

mantle_env_usage() {
	printf "%s\n" \
		"Usage: mantle env [--shell] [--help]" \
		"" \
		"Print the public Mantle environment contract." \
		"Use --shell to emit safely quoted export statements."
}

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	printf "[mantle:error] MANTLE_ROOT is required for command dispatch\n" >&2
	exit 70
fi

mantle_env_format="text"
while (($# > 0)); do
	case "$1" in
	--summary)
		printf "Show Mantle's public environment state.\n"
		exit 0
		;;
	--shell)
		mantle_env_format="shell"
		shift
		;;
	--help | -h)
		mantle_env_usage
		exit 0
		;;
	*)
		printf "[mantle:error] unknown env option: %s\n" "$1" >&2
		mantle_env_usage >&2
		exit 64
		;;
	esac
done

mantle_env_print() {
	local variable_name="$1"
	local variable_value="$2"

	if [[ "${mantle_env_format}" == "shell" ]]; then
		printf "export %s=%q\n" "${variable_name}" "${variable_value}"
	else
		printf "%-30s %s\n" "${variable_name}" "${variable_value:-<unset>}"
	fi
}

mantle_env_print "MANTLE_ROOT" "${MANTLE_ROOT}"
mantle_env_print "MANTLE_INITIALIZATION_STATE" "${MANTLE_INITIALIZATION_STATE:-}"
mantle_env_print "MANTLE_RUNTIME_ENVIRONMENT" "${MANTLE_RUNTIME_ENVIRONMENT:-}"
mantle_env_print "MANTLE_SHELL_NAME" "${MANTLE_SHELL_NAME:-}"
mantle_env_print "MANTLE_INTERACTIVE" "${MANTLE_INTERACTIVE:-}"
mantle_env_print "MANTLE_PROFILE" "${MANTLE_PROFILE:-}"
mantle_env_print "MANTLE_PROFILE_SOURCE" "${MANTLE_PROFILE_SOURCE:-}"
mantle_env_print "MANTLE_POLICY_PRESENTATION" "${MANTLE_POLICY_PRESENTATION:-}"
mantle_env_print "MANTLE_CONFIG_FILE_RESOLVED" "${MANTLE_CONFIG_FILE_RESOLVED:-}"
mantle_env_print "XDG_CONFIG_HOME" "${XDG_CONFIG_HOME:-}"
mantle_env_print "XDG_CACHE_HOME" "${XDG_CACHE_HOME:-}"
mantle_env_print "XDG_DATA_HOME" "${XDG_DATA_HOME:-}"
mantle_env_print "XDG_STATE_HOME" "${XDG_STATE_HOME:-}"
mantle_env_print "XDG_RUNTIME_DIR" "${XDG_RUNTIME_DIR:-}"
mantle_env_print "XDG_BIN_HOME" "${XDG_BIN_HOME:-}"
