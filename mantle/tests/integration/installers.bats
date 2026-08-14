# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Integration tests for the installer matrix.
# Discovers all installers dynamically — no hand-written list.

setup() {
	load '../test_helper/common'
	load '../test_helper/assertions'
	load '../test_helper/stubs'
	setup_isolated_home
	setup_stub_dir

	INSTALLERS_DIR="${MANTLE_ROOT}/libexec/mantle/installers"
	MANTLE_BIN="${MANTLE_ROOT}/bin/mantle"
}

teardown() {
	teardown_stub_dir
	teardown_isolated_home
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_mantle_install() {
	run env -i \
		HOME="${TEST_HOME}" \
		MANTLE_ROOT="${MANTLE_ROOT}" \
		PATH="${STUB_DIR}:${PATH}" \
		TERM=dumb \
		"${MANTLE_BIN}" install "$@"
}

# Return the tool name from an installer path (strips directory and .sh).
_tool_name() {
	local installer_path="${1:?}"
	local name="${installer_path##*/}"
	printf "%s\n" "${name%.sh}"
}

# ---------------------------------------------------------------------------
# Per-installer structural tests (dynamic discovery)
# ---------------------------------------------------------------------------

@test "every discovered installer is executable" {
	local failed=0
	for installer in "${INSTALLERS_DIR}"/*.sh; do
		[[ -f "${installer}" ]] || continue
		if [[ ! -x "${installer}" ]]; then
			printf "Not executable: %s\n" "${installer}" >&2
			failed=1
		fi
	done
	[[ "${failed}" -eq 0 ]]
}

@test "every discovered installer has valid Bash syntax" {
	local failed=0
	for installer in "${INSTALLERS_DIR}"/*.sh; do
		[[ -f "${installer}" ]] || continue
		if ! /bin/bash -n "${installer}" 2>/dev/null; then
			printf "Syntax error: %s\n" "${installer}" >&2
			failed=1
		fi
	done
	[[ "${failed}" -eq 0 ]]
}

@test "every discovered installer does not use EGOHYGIENE namespace" {
	local failed=0
	for installer in "${INSTALLERS_DIR}"/*.sh; do
		[[ -f "${installer}" ]] || continue
		if grep -q "EGOHYGIENE" "${installer}" 2>/dev/null; then
			printf "EGOHYGIENE reference: %s\n" "${installer}" >&2
			failed=1
		fi
	done
	[[ "${failed}" -eq 0 ]]
}

@test "every discovered installer does not use legacy INSTALL_ contract" {
	local failed=0
	for installer in "${INSTALLERS_DIR}"/*.sh; do
		[[ -f "${installer}" ]] || continue
		if grep -qE '^\s*INSTALL_[A-Z]' "${installer}" 2>/dev/null; then
			printf "Legacy INSTALL_ variable: %s\n" "${installer}" >&2
			failed=1
		fi
	done
	[[ "${failed}" -eq 0 ]]
}

@test "every discovered installer does not invoke sudo" {
	local failed=0
	for installer in "${INSTALLERS_DIR}"/*.sh; do
		[[ -f "${installer}" ]] || continue
		if grep -qE '\bsudo\b' "${installer}" 2>/dev/null; then
			printf "sudo found: %s\n" "${installer}" >&2
			failed=1
		fi
	done
	[[ "${failed}" -eq 0 ]]
}

# ---------------------------------------------------------------------------
# CLI surface — help and dry-run for well-known installers
# ---------------------------------------------------------------------------

@test "mantle install eza --help exits 0" {
	_mantle_install eza --help
	assert_success
	assert_output_contains "eza"
}

@test "mantle install eza --help uses canonical mantle install form" {
	_mantle_install eza --help
	assert_success
	assert_output_contains "mantle install"
}

@test "mantle install talisman --help exits 0" {
	_mantle_install talisman --help
	assert_success
}

@test "mantle install talisman --dry-run exits 0" {
	_mantle_install talisman --dry-run --version 1.32.0
	assert_success
	assert_output_contains "tool: talisman"
}

@test "GitHub installer defaults resolve from the lock without network" {
	stub_curl_failure 99
	_mantle_install eza --dry-run
	assert_success
	assert_output_contains "version: 0.23.5"
	assert_output_contains "resolution: lockfile"
}

@test "GitHub installer rejects mutable version selectors" {
	_mantle_install eza --dry-run --version latest
	assert_status 64
	assert_output_contains "Mutable installer selector"
}

@test "unchecksummed GitHub installer fails before download without explicit opt-out" {
	stub_curl_failure 99
	_mantle_install asdf
	assert_status 77
	assert_output_contains "explicitly rerun with --no-verify"
}

@test "Python installer defaults to its exact package lock" {
	create_recording_stub "uv" 0
	_mantle_install httpie --dry-run --manager uv
	assert_success
	assert_output_contains "httpie==3.2.4"
	assert_output_contains "resolution: lockfile"
}

@test "mantle install eza unknown-option exits 64" {
	_mantle_install eza --unknown-option-xyz
	assert_status 64
}

@test "mantle install shfmt --help exits 0" {
	_mantle_install shfmt --help
	assert_success
}

@test "mantle install shdoc --help exits 0" {
	_mantle_install shdoc --help
	assert_success
}

@test "mantle install pyenv --help exits 0" {
	_mantle_install pyenv --help
	assert_success
}

@test "mantle install linuxbrew --help exits 0" {
	_mantle_install linuxbrew --help
	assert_success
}

@test "mantle install docker-desktop --help exits 0" {
	_mantle_install docker-desktop --help
	assert_success
}
