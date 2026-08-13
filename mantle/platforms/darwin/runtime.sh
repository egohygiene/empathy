# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2249 # Closed case statements intentionally treat unmatched values as no-ops.

if [[ -n "${BASH_VERSION:-}" && "${BASH_SOURCE[0]}" == "$0" ]]; then
	printf "[mantle:error] platforms/darwin/runtime.sh must be sourced\n" >&2
	exit 64
fi

if [[ "${MANTLE_PLATFORM_DARWIN_LOADED:-0}" == "1" ]]; then
	return 0
fi

if [[ -z "${MANTLE_ROOT:-}" || ! -d "${MANTLE_ROOT}" ]]; then
	printf "[mantle:error] darwin runtime requires a valid MANTLE_ROOT\n" >&2
	return 1
fi

if ! command -v mantle_core_path_prepend >/dev/null 2>&1; then
	printf "[mantle:error] darwin runtime requires the core PATH API\n" >&2
	return 1
fi

# Lowest-to-highest priority because every discovered path is prepended.
for __mantle_darwin_path in "/usr/local/sbin" "/usr/local/bin" "/opt/homebrew/sbin" "/opt/homebrew/bin"; do
	if [[ -d "${__mantle_darwin_path}" ]]; then
		mantle_core_path_prepend "${__mantle_darwin_path}" || {
			unset __mantle_darwin_path
			return 1
		}
	fi
done

MANTLE_PLATFORM_RUNTIME="darwin"
MANTLE_PLATFORM_DARWIN_LOADED="1"
export MANTLE_PLATFORM_RUNTIME

unset __mantle_darwin_path
return 0
