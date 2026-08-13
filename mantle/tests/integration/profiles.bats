# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Integration tests for profile-driven initialization capability groups.

setup() {
	load '../test_helper/common'
	load '../test_helper/assertions'
	setup_isolated_home
}

teardown() {
	teardown_isolated_home
}

initialize_profile() {
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" TERM=dumb \
		MANTLE_ROOT="${MANTLE_ROOT}" MANTLE_PROFILE="$1" \
		/bin/bash --noprofile --norc -ic '
			source "${MANTLE_ROOT}/.shellrc"
			printf "profile=%s modules=%s\n" "${MANTLE_PROFILE}" "${MANTLE_LOADED_MODULES}"
			alias ll 2>/dev/null || true
			alias public-ip 2>/dev/null || true
			alias update 2>/dev/null || true
		'
}

@test "minimal profile loads no interactive capability modules" {
	initialize_profile minimal
	assert_success
	assert_output_contains "profile=minimal"
	assert_output_not_contains "aliases-safe"
	assert_output_not_contains "history"
}

@test "standard profile loads safe aliases and history only" {
	initialize_profile standard
	assert_success
	assert_output_contains "aliases-safe:history"
	assert_output_contains "alias ll="
	assert_output_not_contains "aliases-network"
	assert_output_not_contains "public-ip"
}

@test "full profile adds maintained network and system capabilities" {
	initialize_profile full
	assert_success
	assert_output_contains "aliases-safe:aliases-network:aliases-system:history"
	assert_output_contains "alias public-ip="
	assert_output_not_contains "alias update="
}

@test "workbench profile preserves the legacy alias corpus explicitly" {
	initialize_profile workbench
	assert_success
	assert_output_contains "aliases-system:aliases-safety:aliases:history:update-checks"
	assert_output_contains "alias update="
}

@test "safety aliases can be enabled independently of safe aliases" {
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" TERM=dumb \
		MANTLE_ROOT="${MANTLE_ROOT}" MANTLE_PROFILE=minimal MANTLE_ENABLE_SAFETY_ALIASES=true \
		/bin/bash --noprofile --norc -ic '
			source "${MANTLE_ROOT}/.shellrc"
			printf "%s\n" "${MANTLE_LOADED_MODULES}"
			alias rm
		'
	assert_success
	assert_output_contains "aliases-safety"
	assert_output_not_contains "aliases-safe:"
	assert_output_contains "alias rm="
}

@test "ci profile is noninteractive and suppresses automatic update checks" {
	initialize_profile ci
	assert_success
	assert_output_contains "profile=ci"
	assert_output_contains "update-checks"
	assert_output_not_contains "aliases-safe"
}

@test "child config commands re-read files instead of freezing the parent result" {
	mkdir -p "${XDG_CONFIG_HOME}/mantle"
	printf "%s\n" "schema_version=1" "profile=standard" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" TERM=dumb MANTLE_ROOT="${MANTLE_ROOT}" \
		/bin/bash --noprofile --norc -c '
			source "${MANTLE_ROOT}/.shellrc" || exit $?
			printf "%s\n" "schema_version=1" "profile=minimal" >"${HOME}/.config/mantle/config.conf"
			"${MANTLE_ROOT}/bin/mantle" config show
		'
	assert_success
	assert_output_contains "profile=minimal"
}

@test "Fish resolves profiles and applies noninteractive update policy" {
	require_fish
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" TERM=dumb \
		MANTLE_ROOT="${MANTLE_ROOT}" MANTLE_PROFILE=ci \
		fish --no-config -c '
			source "$MANTLE_ROOT/runtime/shells/fish/runtime.fish"
			printf "profile=%s updates=%s homebrew=%s state=%s\n" \
				"$MANTLE_PROFILE" "$MANTLE_POLICY_SUPPRESS_UPDATE_CHECKS" \
				"$HOMEBREW_NO_AUTO_UPDATE" "$MANTLE_FISH_INITIALIZATION_STATE"
		'
	assert_success
	assert_output_contains "profile=ci updates=true homebrew=1 state=initialized"
}

@test "Fish applies config values before environment overrides" {
	require_fish
	mkdir -p "${XDG_CONFIG_HOME}/mantle"
	printf "%s\n" \
		"schema_version=1" \
		"profile=minimal" \
		"aliases.network=false" >"${XDG_CONFIG_HOME}/mantle/config.conf"
	run env -i HOME="${TEST_HOME}" PATH="${PATH}" TERM=dumb \
		MANTLE_ROOT="${MANTLE_ROOT}" MANTLE_ENABLE_NETWORK_ALIASES=true \
		fish --no-config -c '
			source "$MANTLE_ROOT/runtime/shells/fish/runtime.fish"
			printf "%s %s\n" "$MANTLE_PROFILE" "$MANTLE_POLICY_ALIASES_NETWORK"
		'
	assert_success
	assert_output_contains "minimal true"
}
