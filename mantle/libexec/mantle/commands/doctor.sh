#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2249 # Closed case statements intentionally treat unmatched values as no-ops.
# Perform read-only checks against the active Mantle installation.

set -o errexit
set -o nounset
set -o pipefail

mantle_doctor_usage() {
	printf "%s\n" \
		"Usage: mantle doctor [--quiet] [--help]" \
		"" \
		"Check the Mantle installation and current command environment." \
		"The command is read-only and does not initialize or repair the shell."
}

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	printf "[mantle:error] MANTLE_ROOT is required for command dispatch\n" >&2
	exit 70
fi

mantle_doctor_quiet="0"
while (($# > 0)); do
	case "$1" in
	--summary)
		printf "Check the Mantle installation and environment.\n"
		exit 0
		;;
	--quiet)
		mantle_doctor_quiet="1"
		shift
		;;
	--help | -h)
		mantle_doctor_usage
		exit 0
		;;
	*)
		printf "[mantle:error] unknown doctor option: %s\n" "$1" >&2
		mantle_doctor_usage >&2
		exit 64
		;;
	esac
done

mantle_doctor_failures=0
mantle_doctor_warnings=0

mantle_doctor_report() {
	local level="$1"
	local message="$2"

	case "${level}" in
	fail) mantle_doctor_failures=$((mantle_doctor_failures + 1)) ;;
	warn) mantle_doctor_warnings=$((mantle_doctor_warnings + 1)) ;;
	esac

	if [[ "${mantle_doctor_quiet}" != "1" || "${level}" == "fail" ]]; then
		printf "%-4s %s\n" "${level}" "${message}"
	fi
}

mantle_doctor_require_file() {
	local relative_path="$1"
	if [[ -r "${MANTLE_ROOT}/${relative_path}" ]]; then
		mantle_doctor_report "pass" "${relative_path} is readable"
	else
		mantle_doctor_report "fail" "${relative_path} is missing or unreadable"
	fi
}

mantle_doctor_require_directory() {
	local relative_path="$1"
	if [[ -d "${MANTLE_ROOT}/${relative_path}" ]]; then
		mantle_doctor_report "pass" "${relative_path}/ is present"
	else
		mantle_doctor_report "fail" "${relative_path}/ is missing"
	fi
}

mantle_doctor_require_file ".shellrc"
mantle_doctor_require_file "bin/mantle"
mantle_doctor_require_file "init/init.sh"
mantle_doctor_require_directory "lib"
mantle_doctor_require_directory "libexec/mantle/commands"
mantle_doctor_require_directory "runtime"

if [[ -x "${MANTLE_ROOT}/bin/mantle" ]]; then
	mantle_doctor_report "pass" "bin/mantle is executable"
else
	mantle_doctor_report "fail" "bin/mantle is not executable"
fi

case ":${PATH:-}:" in
*":${MANTLE_ROOT}/bin:"*)
	mantle_doctor_report "pass" "Mantle bin directory is on PATH"
	;;
*)
	mantle_doctor_report "warn" "Mantle bin directory is not on PATH"
	;;
esac

if ((mantle_doctor_failures > 0)); then
	printf "status: failed (%d failure(s), %d warning(s))\n" \
		"${mantle_doctor_failures}" "${mantle_doctor_warnings}"
	exit 1
fi

if [[ "${mantle_doctor_quiet}" != "1" ]]; then
	printf "status: ok (%d warning(s))\n" "${mantle_doctor_warnings}"
fi
