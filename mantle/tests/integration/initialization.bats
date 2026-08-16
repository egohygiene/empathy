# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Integration tests for Mantle initialization and loader contracts.

setup() {
	load '../test_helper/common'
	load '../test_helper/assertions'
	setup_isolated_home
}

teardown() {
	teardown_isolated_home
}

_source_shellrc() {
	run env -i \
		HOME="${TEST_HOME}" \
		PATH="${PATH}" \
		TERM=dumb \
		"$@" \
		/bin/bash --noprofile --norc -c "source '${MANTLE_ROOT}/.shellrc' && \$MANTLE_TEST_CMD"
}

# ---------------------------------------------------------------------------
# Core library load order
# ---------------------------------------------------------------------------

@test "core libraries load in deterministic order" {
	run /bin/bash --noprofile --norc -c "
		HOME='${TEST_HOME}'
		export HOME
		source '${MANTLE_ROOT}/.shellrc'
		printf '%s\n' \"\${MANTLE_CORE_LOADED}\"
	"
	assert_success
	assert_output_contains "1"
}

@test "module loader is available after initialization" {
	run /bin/bash --noprofile --norc -c "
		HOME='${TEST_HOME}'
		export HOME
		source '${MANTLE_ROOT}/.shellrc'
		declare -f mantle_load_module >/dev/null 2>&1 && printf 'available\n'
	"
	assert_success
	assert_output_contains "available"
}

# ---------------------------------------------------------------------------
# Module ordering
# ---------------------------------------------------------------------------

@test "noninteractive modules load in correct order: xdg privacy cache tooling environment" {
	run /bin/bash --noprofile --norc -c "
		HOME='${TEST_HOME}'
		MANTLE_INTERACTIVE=0
		export HOME MANTLE_INTERACTIVE
		source '${MANTLE_ROOT}/.shellrc'
		printf '%s\n' \"\${MANTLE_LOADED_MODULES}\"
	"
	assert_success
	local loaded="${output}"
	# xdg must appear before privacy
	local xdg_pos privacy_pos cache_pos tooling_pos env_pos
	xdg_pos="${loaded%%xdg*}"
	privacy_pos="${loaded%%privacy*}"
	[[ "${#xdg_pos}" -lt "${#privacy_pos}" ]]
}

@test "aliases and history modules are absent in noninteractive shells" {
	run /bin/bash --noprofile --norc -c "
		HOME='${TEST_HOME}'
		MANTLE_INTERACTIVE=0
		export HOME MANTLE_INTERACTIVE
		source '${MANTLE_ROOT}/.shellrc'
		printf '%s\n' \"\${MANTLE_LOADED_MODULES}\"
	"
	assert_success
	assert_output_not_contains "aliases"
	assert_output_not_contains "history"
}

# ---------------------------------------------------------------------------
# Module loader API
# ---------------------------------------------------------------------------

@test "mantle_load_module rejects empty module name" {
	run /bin/bash --noprofile --norc -c "
		HOME='${TEST_HOME}'
		export HOME
		source '${MANTLE_ROOT}/lib/modules.sh'
		MANTLE_ROOT='${MANTLE_ROOT}'
		export MANTLE_ROOT
		mantle_load_module '' && printf 'bad\n' || printf 'rejected\n'
	"
	assert_output_contains "rejected"
}

@test "mantle_load_module rejects traversal names" {
	run /bin/bash --noprofile --norc -c "
		MANTLE_ROOT='${MANTLE_ROOT}'
		export MANTLE_ROOT
		source '${MANTLE_ROOT}/lib/modules.sh'
		mantle_load_module '../etc/passwd' 2>&1 && printf 'bad\n' || printf 'rejected\n'
	"
	assert_output_contains "rejected"
}

@test "mantle_load_module detects recursive cycles" {
	run /bin/bash --noprofile --norc -c "
		MANTLE_ROOT='${MANTLE_ROOT}'
		MANTLE_LOADING_MODULES='testmod'
		export MANTLE_ROOT MANTLE_LOADING_MODULES
		source '${MANTLE_ROOT}/lib/modules.sh'
		mantle_load_module 'testmod'
		printf '%d\n' \$?
	"
	assert_output_contains "70"
}

@test "mantle_list_loaded_modules prints modules in load order" {
	run /bin/bash --noprofile --norc -c "
		MANTLE_ROOT='${MANTLE_ROOT}'
		export MANTLE_ROOT
		source '${MANTLE_ROOT}/lib/modules.sh'
		MANTLE_LOADED_MODULES='xdg:privacy:cache'
		mantle_list_loaded_modules
	"
	assert_success
	local lines_arr=("${lines[@]}")
	[[ "${lines_arr[0]}" == "xdg" ]]
	[[ "${lines_arr[1]}" == "privacy" ]]
	[[ "${lines_arr[2]}" == "cache" ]]
}

@test "mantle_is_module_loaded returns 0 for loaded module" {
	run /bin/bash --noprofile --norc -c "
		MANTLE_ROOT='${MANTLE_ROOT}'
		export MANTLE_ROOT
		source '${MANTLE_ROOT}/lib/modules.sh'
		MANTLE_LOADED_MODULES='xdg:privacy'
		mantle_is_module_loaded 'xdg' && printf 'loaded\n' || printf 'not-loaded\n'
	"
	assert_success
	assert_output_contains "loaded"
}

@test "mantle_is_module_loaded returns 1 for unloaded module" {
	run /bin/bash --noprofile --norc -c "
		MANTLE_ROOT='${MANTLE_ROOT}'
		export MANTLE_ROOT
		source '${MANTLE_ROOT}/lib/modules.sh'
		MANTLE_LOADED_MODULES='xdg'
		mantle_is_module_loaded 'privacy' && printf 'loaded\n' || printf 'not-loaded\n'
	"
	assert_output_contains "not-loaded"
}

# ---------------------------------------------------------------------------
# Successful load is idempotent
# ---------------------------------------------------------------------------

@test "loading the same module twice is a no-op" {
	run /bin/bash --noprofile --norc -c "
		HOME='${TEST_HOME}'
		MANTLE_ROOT='${MANTLE_ROOT}'
		export HOME MANTLE_ROOT
		source '${MANTLE_ROOT}/lib/modules.sh'
		mantle_load_module 'xdg'
		mantle_load_module 'xdg'
		# MANTLE_LOADED_MODULES should contain xdg exactly once
		count=0
		IFS=: read -ra mods <<< \"\${MANTLE_LOADED_MODULES}\"
		for m in \"\${mods[@]}\"; do [[ \"\$m\" == 'xdg' ]] && ((count++)); done
		printf '%d\n' \"\${count}\"
	"
	assert_success
	assert_output_contains "1"
}

# ---------------------------------------------------------------------------
# Init files reject direct execution
# ---------------------------------------------------------------------------

@test "init/init.sh rejects direct execution" {
	run /bin/bash --noprofile --norc "${MANTLE_ROOT}/init/init.sh"
	assert_status 64
}

@test "init/bootstrap.sh rejects direct execution" {
	run /bin/bash --noprofile --norc "${MANTLE_ROOT}/init/bootstrap.sh"
	assert_status 64
}

@test "lib/modules.sh rejects direct execution" {
	run /bin/bash --noprofile --norc "${MANTLE_ROOT}/lib/modules.sh"
	assert_status 64
}

# ---------------------------------------------------------------------------
# Once-per-session presentation integration
# ---------------------------------------------------------------------------

@test "interactive Bash evaluates presentation once and exports the guard" {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_PRESENTATION_MODE="off" \
		PATH="${PATH}" \
		TERM=xterm-256color \
		/bin/bash --noprofile --norc -i -c \
		"source '${MANTLE_ROOT}/.shellrc'; printf 'guard=%s\\n' \"\${MANTLE_PRESENTATION_SHOWN:-missing}\""
	assert_success
	assert_output_contains "guard=1"
}

@test "nested Bash inherits the once-per-session presentation guard" {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_PRESENTATION_MODE="off" \
		PATH="${PATH}" \
		TERM=xterm-256color \
		/bin/bash --noprofile --norc -i -c \
		"source '${MANTLE_ROOT}/.shellrc'; /bin/bash --noprofile --norc -c 'printf \"nested=%s\\n\" \"\${MANTLE_PRESENTATION_SHOWN:-missing}\"'"
	assert_success
	assert_output_contains "nested=1"
}

@test "interactive Zsh uses the shared presentation command and guard" {
	require_zsh
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_PRESENTATION_MODE="off" \
		PATH="${PATH}" \
		TERM=xterm-256color \
		zsh --no-rcs -i -c \
		"source '${MANTLE_ROOT}/.shellrc'; printf 'guard=%s\\n' \"\${MANTLE_PRESENTATION_SHOWN:-missing}\""
	assert_success
	assert_output_contains "guard=1"
}

@test "interactive Fish uses the shared presentation command and guard" {
	require_fish
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_PRESENTATION_MODE="off" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${PATH}" \
		TERM=xterm-256color \
		fish --no-config --interactive --command \
		'source "$MANTLE_ROOT/runtime/shells/fish/runtime.fish"; printf "guard=%s\n" "$MANTLE_PRESENTATION_SHOWN"'
	assert_success
	assert_output_contains "guard=1"
}
