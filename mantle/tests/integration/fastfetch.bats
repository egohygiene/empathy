#!/usr/bin/env bats
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Integration tests for the mantle fastfetch collector family.

setup() {
	load "../test_helper/common"
	load "../test_helper/assertions"
	load "../test_helper/stubs"
	setup_isolated_home
	setup_stub_dir
}

teardown() {
	teardown_stub_dir
	teardown_isolated_home
}

run_fastfetch() {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_ROOT}/bin/mantle" fastfetch "$@"
}

@test "fastfetch help and central version are available" {
	run_fastfetch --help
	assert_success
	assert_output_contains "runtime"
	assert_output_contains "workspace"
	assert_output_contains "toolchains"
	assert_output_contains "contexts"

	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		MANTLE_VERSION="9.8.7" \
		PATH="${STUB_DIR}:${PATH}" \
		"${MANTLE_ROOT}/bin/mantle" fastfetch --version
	assert_success
	[[ "${output}" == "mantle 9.8.7" ]]
}

@test "fastfetch rejects missing, unknown, and excess collector arguments" {
	run_fastfetch
	assert_status 64

	run_fastfetch unknown
	assert_status 64

	run_fastfetch runtime extra
	assert_status 64
}

@test "runtime reports only stable Mantle shell environment and OS identity" {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		MANTLE_VERSION="1.2.3" \
		MANTLE_SHELL_NAME="zsh" \
		MANTLE_RUNTIME_ENVIRONMENT="devcontainer" \
		PATH="${STUB_DIR}:${PATH}" \
		SECRET_VALUE="must-not-leak" \
		"${MANTLE_ROOT}/bin/mantle" fastfetch runtime
	assert_success
	assert_output_contains "mantle 1.2.3"
	assert_output_contains "zsh"
	assert_output_contains "devcontainer"
	assert_output_not_contains "${TEST_HOME}"
	assert_output_not_contains "must-not-leak"
}

@test "workspace abbreviates HOME outside a Git repository" {
	mkdir -p "${TEST_HOME}/work area"
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${STUB_DIR}:${PATH}" \
		/bin/bash --noprofile --norc -c \
		'cd "$HOME/work area" && "$MANTLE_ROOT/bin/mantle" fastfetch workspace'
	assert_success
	[[ "${output}" == "~/work area" ]]
}

@test "workspace reports clean changed detached and unborn Git states" {
	local repository="${TEST_HOME}/repository with spaces"
	mkdir -p "${repository}"
	git -C "${repository}" init --quiet
	git -C "${repository}" config user.email "test@mantle.invalid"
	git -C "${repository}" config user.name "Mantle Test"

	run env -i HOME="${TEST_HOME}" MANTLE_ROOT="${MANTLE_ROOT}" PATH="${STUB_DIR}:${PATH}" \
		/bin/bash --noprofile --norc -c \
		'cd "$1" && "$MANTLE_ROOT/bin/mantle" fastfetch workspace' _ "${repository}"
	assert_success
	assert_output_contains "repository with spaces"

	printf "tracked\n" >"${repository}/tracked.txt"
	git -C "${repository}" add tracked.txt
	git -C "${repository}" commit --quiet -m "initial"

	run env -i HOME="${TEST_HOME}" MANTLE_ROOT="${MANTLE_ROOT}" PATH="${STUB_DIR}:${PATH}" \
		/bin/bash --noprofile --norc -c \
		'cd "$1" && "$MANTLE_ROOT/bin/mantle" fastfetch workspace' _ "${repository}"
	assert_success
	assert_output_contains "✓ clean"

	printf "changed\n" >>"${repository}/tracked.txt"
	run env -i HOME="${TEST_HOME}" MANTLE_ROOT="${MANTLE_ROOT}" PATH="${STUB_DIR}:${PATH}" \
		/bin/bash --noprofile --norc -c \
		'cd "$1" && "$MANTLE_ROOT/bin/mantle" fastfetch workspace' _ "${repository}"
	assert_success
	assert_output_contains "● changed"

	git -C "${repository}" checkout --quiet --detach
	run env -i HOME="${TEST_HOME}" MANTLE_ROOT="${MANTLE_ROOT}" PATH="${STUB_DIR}:${PATH}" \
		/bin/bash --noprofile --norc -c \
		'cd "$1" && "$MANTLE_ROOT/bin/mantle" fastfetch workspace' _ "${repository}"
	assert_success
	assert_output_not_contains "https://"
}

@test "toolchains print normalized versions in deterministic order" {
	create_stub git 0 "git version 2.51.1"
	create_stub node 0 "v24.9.0"
	create_stub python3 0 "Python 3.13.7"
	create_stub rustc 0 "rustc 1.89.0 (hash date)"
	create_stub go 0 "go version go1.25.0 linux/amd64"
	create_stub task 0 "Task version: v3.45.4"

	run_fastfetch toolchains
	assert_success
	[[ "${output}" == "git 2.51.1 · node 24.9.0 · python 3.13.7 · rust 1.89.0 · go 1.25.0 · task 3.45.4" ]]
}

@test "toolchains return a neutral value when no supported command exists" {
	local empty_path="${TEST_HOME}/empty-path"
	mkdir -p "${empty_path}"
	run env -i \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${empty_path}" \
		/bin/bash "${MANTLE_ROOT}/libexec/mantle/commands/fastfetch.sh" toolchains
	assert_success
	[[ "${output}" == "none detected" ]]
}

@test "contexts use local client configuration commands only" {
	local docker_stub="${STUB_DIR}/docker"
	local kubectl_stub="${STUB_DIR}/kubectl"
	{
		printf "#!/bin/sh\n"
		printf 'printf "docker:%s\\n" "$*" >> "$MANTLE_CONTEXT_CALLS"\n'
		printf 'test "$*" = "context show"; or exit 99\n'
		printf 'printf "desktop-linux\\n"\n'
	} >"${docker_stub}"
	{
		printf "#!/bin/sh\n"
		printf 'printf "kubectl:%s\\n" "$*" >> "$MANTLE_CONTEXT_CALLS"\n'
		printf 'test "$*" = "config current-context"; or exit 99\n'
		printf 'printf "local-dev\\n"\n'
	} >"${kubectl_stub}"
	chmod 0755 "${docker_stub}" "${kubectl_stub}"

	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_CONTEXT_CALLS="${TEST_HOME}/context-calls" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${STUB_DIR}:${PATH}" \
		"${MANTLE_ROOT}/bin/mantle" fastfetch contexts
	assert_success
	[[ "${output}" == "docker desktop-linux · k8s local-dev" ]]
	run cat "${TEST_HOME}/context-calls"
	assert_output_contains "docker:context show"
	assert_output_contains "kubectl:config current-context"
}

@test "failing optional context clients produce none active" {
	create_stub docker 1 ""
	create_stub kubectl 1 ""

	run_fastfetch contexts
	assert_success
	[[ "${output}" == "none active" ]]
}
