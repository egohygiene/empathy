# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Contract tests for Mantle's startup presentation assets and configuration.

setup() {
	load "../test_helper/common"
	load "../test_helper/assertions"
}

@test "Fastfetch config and presentation assets satisfy the offline contract" {
	run python3 "${MANTLE_ROOT}/tests/validate_fastfetch.py"
	assert_success
	assert_output_contains "presentation contract is valid"
}

@test "all shell adapters invoke the single shell-banner orchestrator" {
	run grep -F '"${__mantle_presentation_command}"' "${MANTLE_ROOT}/init/init.sh"
	assert_success
	run grep -F '"$presentation_command"' "${MANTLE_ROOT}/runtime/shells/fish/runtime.fish"
	assert_success
}
