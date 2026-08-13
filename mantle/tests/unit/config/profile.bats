# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Unit tests for the typed profile resolver and non-executing config parser.

setup() {
	load '../../test_helper/common'
	load '../../test_helper/assertions'
	setup_isolated_home
	mkdir -p "${XDG_CONFIG_HOME}/mantle"
}

teardown() {
	teardown_isolated_home
}

resolve_profile() {
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" MANTLE_ROOT="${MANTLE_ROOT}" "$@" \
		/bin/bash --noprofile --norc -c '
			source "${MANTLE_ROOT}/lib/config/profile.sh"
			mantle_config_resolve || exit $?
			printf "profile=%s safe=%s network=%s status=%s\n" \
				"${MANTLE_PROFILE}" "${MANTLE_POLICY_ALIASES_SAFE}" \
				"${MANTLE_POLICY_ALIASES_NETWORK}" "${MANTLE_CONFIG_FILE_STATUS}"
			mantle_config_print_effective aliases.safe
		'
}

@test "default resolution selects the standard profile when no file exists" {
	resolve_profile
	assert_success
	assert_output_contains "profile=standard safe=true network=false status=absent"
}

@test "config values override profile defaults and environment overrides config" {
	printf "%s\n" \
		"schema_version=1" \
		"profile=minimal" \
		"aliases.safe=true" >"${XDG_CONFIG_HOME}/mantle/config.conf"

	resolve_profile MANTLE_PROFILE=full MANTLE_ENABLE_SAFE_ALIASES=false
	assert_success
	assert_output_contains "profile=full safe=false network=true status=loaded"
	assert_output_contains "environment:MANTLE_ENABLE_SAFE_ALIASES"
}

@test "parser rejects unknown and duplicate keys" {
	printf "%s\n" "schema_version=1" "mystery=true" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	resolve_profile
	assert_status 78
	assert_output_contains "unknown config key"

	printf "%s\n" "schema_version=1" "profile=standard" "profile=full" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	resolve_profile
	assert_status 78
	assert_output_contains "duplicate config key"
}

@test "parser rejects unsupported schema versions" {
	printf "%s\n" "schema_version=999" "profile=standard" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	resolve_profile
	assert_status 78
	assert_output_contains "schema_version must be 1"
}

@test "configuration text is never evaluated as shell code" {
	printf 'schema_version=1\nprofile=$(touch %s)\n' \
		"${TEST_HOME}/executed" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	resolve_profile
	assert_status 78
	[[ ! -e "${TEST_HOME}/executed" ]]
}

@test "explicit unavailable config files fail instead of silently falling back" {
	resolve_profile MANTLE_CONFIG_FILE="${TEST_HOME}/missing.conf"
	assert_status 66
	assert_output_contains "config file is unavailable"
}

@test "relative XDG config roots fall back without becoming executable paths" {
	resolve_profile XDG_CONFIG_HOME=relative/config
	assert_success
	assert_output_contains "profile=standard"
}

@test "repeated resolution does not promote a derived profile into an override" {
	printf "%s\n" "schema_version=1" "profile=standard" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" MANTLE_ROOT="${MANTLE_ROOT}" \
		/bin/bash --noprofile --norc -c '
			source "${MANTLE_ROOT}/lib/config/profile.sh"
			mantle_config_resolve || exit $?
			printf "%s\n" "schema_version=1" "profile=minimal" >"${HOME}/.config/mantle/config.conf"
			mantle_config_resolve || exit $?
			printf "%s %s\n" "${MANTLE_PROFILE}" "${MANTLE_PROFILE_SOURCE}"
		'
	assert_success
	assert_output_contains "minimal config:"
}

@test "a caller can replace a previously derived profile with an explicit override" {
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" MANTLE_ROOT="${MANTLE_ROOT}" \
		/bin/bash --noprofile --norc -c '
			source "${MANTLE_ROOT}/lib/config/profile.sh"
			mantle_config_resolve || exit $?
			MANTLE_PROFILE=full
			mantle_config_resolve || exit $?
			printf "%s %s\n" "${MANTLE_PROFILE}" "${MANTLE_PROFILE_SOURCE}"
		'
	assert_success
	assert_output_contains "full environment:MANTLE_PROFILE"
}
