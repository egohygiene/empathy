# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Integration tests for the public mantle CLI (bin/mantle).

setup() {
	load '../test_helper/common'
	load '../test_helper/assertions'
	load '../test_helper/stubs'
	setup_isolated_home
	setup_stub_dir
	MANTLE_BIN="${MANTLE_ROOT}/bin/mantle"
}

teardown() {
	teardown_stub_dir
	teardown_isolated_home
}

_mantle() {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_BIN}" "$@"
}

# ---------------------------------------------------------------------------
# Basic invocation
# ---------------------------------------------------------------------------

@test "mantle with no arguments prints help" {
	_mantle
	assert_success
	assert_output_contains "Usage:"
	assert_output_contains "mantle"
}

@test "mantle --help prints help" {
	_mantle --help
	assert_success
	assert_output_contains "Usage:"
}

@test "mantle -h prints help" {
	_mantle -h
	assert_success
	assert_output_contains "Usage:"
}

@test "mantle help prints help" {
	_mantle help
	assert_success
	assert_output_contains "Usage:"
}

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

@test "mantle version prints version" {
	_mantle version
	assert_success
	assert_output_contains "mantle"
}

@test "mantle --version prints version" {
	_mantle --version
	assert_success
	assert_output_contains "mantle"
}

@test "mantle version --short prints version without prefix" {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		MANTLE_VERSION="1.2.3-test" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_BIN}" version --short
	assert_success
	assert_output_contains "1.2.3-test"
	assert_output_not_contains "mantle "
}

@test "mantle version uses MANTLE_VERSION env var first" {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		MANTLE_VERSION="99.0.0-env" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_BIN}" version
	assert_success
	assert_output_contains "99.0.0-env"
}

# ---------------------------------------------------------------------------
# Unknown commands and options
# ---------------------------------------------------------------------------

@test "mantle unknown command exits with status 64" {
	_mantle unknown-command-xyz
	assert_status 64
}

@test "mantle unknown global option exits with status 64" {
	_mantle --unknown-option
	assert_status 64
}

@test "mantle traversal command name is rejected" {
	_mantle "../etc/passwd"
	assert_status 64
}

@test "mantle empty command name is rejected" {
	_mantle ""
	assert_status 64
}

# ---------------------------------------------------------------------------
# Install subcommand
# ---------------------------------------------------------------------------

@test "mantle install --help prints usage" {
	_mantle install --help
	assert_success
	assert_output_contains "mantle install"
}

@test "mantle install --list lists installers" {
	_mantle install --list
	assert_success
}

@test "mantle install --assurance publishes locked resolution" {
	_mantle install --assurance eza
	assert_success
	assert_output_contains "explicit-opt-out"
	assert_output_contains "0.23.5"
}

@test "mantle install --assurance rejects unknown installers" {
	_mantle install --assurance nonexistent-tool-xyz
	assert_status 64
}

@test "mantle install eza --help prints eza-specific usage" {
	_mantle install eza --help
	assert_success
	assert_output_contains "eza"
}

@test "mantle install talisman --dry-run succeeds without network" {
	_mantle install talisman --dry-run --version 1.32.0
	assert_success
	assert_output_contains "tool: talisman"
}

@test "mantle install unknown-tool exits non-zero" {
	_mantle install nonexistent-tool-xyz
	[[ "${status}" -ne 0 ]]
}

# ---------------------------------------------------------------------------
# Help for each discovered command
# ---------------------------------------------------------------------------

@test "mantle help install prints install help" {
	_mantle help install
	assert_success
	assert_output_contains "install"
}

@test "mantle help version prints version help" {
	_mantle help version
	assert_success
	assert_output_contains "version"
}

@test "mantle help unknown-command exits with status 64" {
	_mantle help unknown-xyz
	assert_status 64
}

# ---------------------------------------------------------------------------
# Initial public diagnostics and environment commands
# ---------------------------------------------------------------------------

@test "mantle doctor validates the repository installation" {
	_mantle doctor
	assert_success
	assert_output_contains "status: ok"
}

@test "mantle doctor reports preserved XDG migrations without failing" {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		MANTLE_XDG_MIGRATION_WARNINGS="CARGO_HOME:DOCKER_CONFIG" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_BIN}" doctor
	assert_success
	assert_output_contains "XDG migration pending for CARGO_HOME"
	assert_output_contains "XDG migration pending for DOCKER_CONFIG"
	assert_output_contains "status: ok (3 warning(s))"
}

@test "mantle env reports the resolved installation root" {
	_mantle env
	assert_success
	assert_output_contains "MANTLE_ROOT"
	assert_output_contains "${MANTLE_ROOT}"
}

@test "mantle env --shell emits reusable exports" {
	_mantle env --shell
	assert_success
	assert_output_contains "export MANTLE_ROOT="
}

@test "mantle config lists the built-in typed profiles" {
	_mantle config list-profiles
	assert_success
	assert_output_contains "standard"
	assert_output_contains "workbench"
	assert_output_contains "share-safe"
}

@test "mantle config show reports effective standard defaults" {
	_mantle config show
	assert_success
	assert_output_contains "schema_version=1"
	assert_output_contains "profile=standard"
	assert_output_contains "aliases.safe=true"
}

@test "mantle config explain reports value provenance" {
	_mantle config explain aliases.safe
	assert_success
	assert_output_contains "profile:standard"
	assert_output_contains "interactive"
}

@test "mantle config rejects unknown explain settings" {
	_mantle config explain unknown.setting
	assert_status 64
}

@test "mantle path --root prints only the resolved root" {
	_mantle path --root
	assert_success
	[[ "${output}" == "${MANTLE_ROOT}" ]]
}

@test "mantle fastfetch exposes every configured collector" {
	local collector
	for collector in runtime workspace toolchains contexts; do
		_mantle fastfetch "${collector}"
		assert_success
		[[ -n "${output}" ]]
	done
}

@test "mantle completion generates definitions for supported shells" {
	local shell_name
	for shell_name in bash zsh fish; do
		_mantle completion "${shell_name}"
		assert_success
		assert_output_contains "mantle"
	done
}

@test "mantle completion includes typed config subcommands" {
	_mantle completion bash
	assert_success
	assert_output_contains "list-profiles path validate show explain"
}

@test "mantle completion includes installer assurance diagnostics" {
	_mantle completion bash
	assert_success
	assert_output_contains "--assurance"
}

# ---------------------------------------------------------------------------
# Symlink invocation
# ---------------------------------------------------------------------------

@test "mantle is invocable through an absolute symlink" {
	local link_path="${TEST_HOME}/mantle-link"
	ln -s "${MANTLE_BIN}" "${link_path}"
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${link_path}" version
	assert_success
}

# ---------------------------------------------------------------------------
# MANTLE_ROOT validation
# ---------------------------------------------------------------------------

@test "mantle rejects MANTLE_ROOT pointing at another directory" {
	local other_dir
	other_dir="$(mktemp -d "${TMPDIR:-/tmp}/other-root-XXXXXX")"
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${other_dir}" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_BIN}" version
	[[ "${status}" -ne 0 ]]
	rm -rf "${other_dir}"
}

# ---------------------------------------------------------------------------
# Arguments with spaces
# ---------------------------------------------------------------------------

@test "mantle forwards arguments containing spaces unchanged" {
	# install --help with a known installer should print usage including the tool name
	_mantle install "eza" --help
	assert_success
	assert_output_contains "eza"
}
