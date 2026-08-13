#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# Inspect and validate Mantle's versioned profile configuration.

set -o errexit
set -o nounset
set -o pipefail

mantle_config_usage() {
	printf "%s\n" \
		"Usage: mantle config <command> [arguments]" \
		"" \
		"Commands:" \
		"  list-profiles       List built-in profiles and their descriptions." \
		"  path                Print the resolved configuration file path." \
		"  validate [FILE]     Validate a file without executing it." \
		"  show                Print the effective configuration as key=value." \
		"  explain [SETTING]   Explain effective values and their sources." \
		"" \
		"Precedence: profile defaults < config file < environment overrides."
}

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	printf "[mantle:error] MANTLE_ROOT is required for command dispatch\n" >&2
	exit 70
fi

if [[ "${1:-}" == "--summary" ]]; then
	printf "Validate and explain typed Mantle profiles.\n"
	exit 0
fi
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
	mantle_config_usage
	exit 0
fi
if (($# == 0)); then
	mantle_config_usage >&2
	exit 64
fi

# shellcheck disable=SC1091
source "${MANTLE_ROOT}/lib/config/profile.sh"

mantle_config_cli_resolve() {
	mantle_config_resolve || exit $?
}

mantle_config_cli_list_profiles() {
	local schema=""
	local profile=""
	local _aliases_safe=""
	local _aliases_network=""
	local _aliases_system=""
	local _aliases_legacy=""
	local _aliases_safety=""
	local _history=""
	local _suppress_update_checks=""
	local _experimental=""
	local presentation=""
	local description=""

	printf "profile\tpresentation\tdescription\n"
	while IFS=$'\t' read -r schema profile _aliases_safe _aliases_network _aliases_system _aliases_legacy _aliases_safety _history _suppress_update_checks _experimental presentation description; do
		[[ "${schema}" == "schema_version" ]] && continue
		[[ "${schema}" == "${MANTLE_CONFIG_SUPPORTED_SCHEMA_VERSION}" ]] || continue
		printf "%s\t%s\t%s\n" "${profile}" "${presentation}" "${description}"
	done <"${MANTLE_ROOT}/config/profiles.tsv"
}

mantle_config_cli_show() {
	local setting_name=""
	local _setting_metadata=""
	local setting_variable=""
	local effective_value=""

	printf "schema_version=%s\n" "${MANTLE_CONFIG_SCHEMA_VERSION}"
	printf "profile=%s\n" "${MANTLE_PROFILE}"
	while IFS=$'\t' read -r setting_name _setting_metadata; do
		[[ "${setting_name}" == "setting" ]] && continue
		setting_variable="$(mantle_config_setting_variable "${setting_name}")" || exit 78
		effective_value="$(mantle_config_get_policy_value "${setting_variable}")" || exit 78
		printf "%s=%s\n" "${setting_name}" "${effective_value}"
	done <"${MANTLE_ROOT}/config/settings.tsv"
}

mantle_config_subcommand="$1"
shift
case "${mantle_config_subcommand}" in
list-profiles)
	(($# == 0)) || {
		printf "[mantle:error] config list-profiles does not accept arguments\n" >&2
		exit 64
	}
	mantle_config_cli_list_profiles
	;;
path)
	(($# == 0)) || {
		printf "[mantle:error] config path does not accept arguments\n" >&2
		exit 64
	}
	mantle_config_cli_resolve
	printf "%s\n" "${MANTLE_CONFIG_FILE_RESOLVED}"
	;;
validate)
	if (($# > 1)); then
		printf "[mantle:error] config validate accepts at most one file\n" >&2
		exit 64
	fi
	if (($# == 1)); then
		if [[ ! -f "$1" || ! -r "$1" ]]; then
			printf "[mantle:error] configured Mantle config file is unavailable: %s\n" "$1" >&2
			exit 66
		fi
		if [[ "$1" == /* ]]; then
			MANTLE_CONFIG_FILE="$1"
		else
			MANTLE_CONFIG_FILE="$(cd -P "$(dirname -- "$1")" && pwd)/$(basename -- "$1")"
		fi
		export MANTLE_CONFIG_FILE
	fi
	mantle_config_cli_resolve
	printf "status: %s\n" "${MANTLE_CONFIG_FILE_STATUS}"
	printf "schema_version: %s\n" "${MANTLE_CONFIG_SCHEMA_VERSION}"
	printf "profile: %s\n" "${MANTLE_PROFILE}"
	;;
show)
	(($# == 0)) || {
		printf "[mantle:error] config show does not accept arguments\n" >&2
		exit 64
	}
	mantle_config_cli_resolve
	mantle_config_cli_show
	;;
explain)
	if (($# > 1)); then
		printf "[mantle:error] config explain accepts at most one setting\n" >&2
		exit 64
	fi
	if (($# == 1)) && [[ "$1" != "profile" ]] && ! mantle_config_setting_variable "$1" >/dev/null; then
		printf "[mantle:error] unknown config setting: %s\n" "$1" >&2
		exit 64
	fi
	mantle_config_cli_resolve
	mantle_config_print_effective "${1:-}"
	;;
--help | -h)
	mantle_config_usage
	;;
*)
	printf "[mantle:error] unknown config command: %s\n" "${mantle_config_subcommand}" >&2
	mantle_config_usage >&2
	exit 64
	;;
esac
