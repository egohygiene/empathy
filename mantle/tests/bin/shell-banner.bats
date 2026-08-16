# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Behavioral tests for bin/shell-banner.

setup() {
	load "helpers/environment"
	load "helpers/assertions"
	load "helpers/stubs"
	bin_test_setup

	PRESENTATION_ROOT="${BIN_TEST_HOME}/mantle root"
	ORDER_FILE="${BIN_TEST_HOME}/order"
	mkdir -p \
		"${PRESENTATION_ROOT}/assets/presentation" \
		"${PRESENTATION_ROOT}/bin" \
		"${PRESENTATION_ROOT}/config/fastfetch"
	printf "image fixture\n" >"${PRESENTATION_ROOT}/assets/presentation/mantle-banner.png"
	printf "MANTLE TEXT FALLBACK\n" >"${PRESENTATION_ROOT}/assets/presentation/mantle-banner.txt"
	printf "{}\n" >"${PRESENTATION_ROOT}/config/fastfetch/fastfetch.jsonc"
}

teardown() {
	bin_test_teardown
}

install_imgcat_stub() {
	local exit_code="${1:-0}"
	local stub_path="${PRESENTATION_ROOT}/bin/imgcat"
	{
		printf "#!/bin/sh\n"
		printf 'printf "imgcat\\n" >> "$ORDER_FILE"\n'
		printf 'printf "IMAGE RENDERED\\n"\n'
		printf "exit %d\n" "${exit_code}"
	} >"${stub_path}"
	chmod 0755 "${stub_path}"
}

install_fastfetch_stub() {
	local exit_code="${1:-0}"
	local stub_path="${BIN_STUB_DIR}/fastfetch"
	{
		printf "#!/bin/sh\n"
		printf 'printf "fastfetch:%%s\\n" "$*" >> "$ORDER_FILE"\n'
		printf 'case "$1" in --version) printf "fastfetch 2.67.0\\n" ;; *) printf "FASTFETCH RENDERED\\n" ;; esac\n'
		printf "exit %d\n" "${exit_code}"
	} >"${stub_path}"
	chmod 0755 "${stub_path}"
}

@test "shell-banner --help exits 0 and documents the presentation surface" {
	run_bin shell-banner --help
	assert_success
	assert_output_contains "Usage"
	assert_output_contains "--fastfetch-only"
	assert_output_contains "MANTLE_PRESENTATION_SHOWN"
}

@test "shell-banner --version exits 0 and prints a version" {
	run_bin shell-banner --version
	assert_success
	assert_valid_version
}

@test "shell-banner rejects unknown and incompatible options" {
	run_bin shell-banner --no-such-flag
	assert_status 64

	run_bin shell-banner --banner-only --fastfetch-only
	assert_status 64

	run_bin shell-banner --image
	assert_status 64
}

@test "normal noninteractive CI execution is silent and successful" {
	run_bin shell-banner --root "${PRESENTATION_ROOT}"
	assert_success
	[[ -z "${output}" ]]
}

@test "verbose mode explains why normal execution was skipped" {
	run_bin_with_env shell-banner \
		"MANTLE_PRESENTATION_SHOWN=1" \
		"MANTLE_INTERACTIVE=1" \
		"CI=" \
		"GITHUB_ACTIONS=" \
		"TERM=xterm-256color" \
		-- --root "${PRESENTATION_ROOT}" --verbose
	assert_success
	assert_output_contains "already evaluated"
}

@test "dry-run resolves the plan without invoking image or Fastfetch commands" {
	install_imgcat_stub
	install_fastfetch_stub

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" --dry-run
	assert_success
	assert_output_contains "sequence: banner -> fastfetch"
	assert_output_contains "fastfetch-config"
	[[ ! -e "${ORDER_FILE}" ]]
}

@test "forced presentation renders the banner before explicit Fastfetch config" {
	install_imgcat_stub
	install_fastfetch_stub

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" --force
	assert_success
	assert_output_contains "IMAGE RENDERED"
	assert_output_contains "FASTFETCH RENDERED"

	run sed -n "1p" "${ORDER_FILE}"
	[[ "${output}" == "imgcat" ]]
	run sed -n "2p" "${ORDER_FILE}"
	assert_output_contains "fastfetch:--config ${PRESENTATION_ROOT}/config/fastfetch/fastfetch.jsonc"
}

@test "banner-only does not invoke Fastfetch" {
	install_imgcat_stub
	install_fastfetch_stub

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" --force --banner-only
	assert_success
	assert_output_contains "IMAGE RENDERED"
	run cat "${ORDER_FILE}"
	assert_output_not_contains "fastfetch"
}

@test "share-safe mode defaults to banner-only presentation" {
	install_imgcat_stub
	install_fastfetch_stub

	run_bin_with_env shell-banner \
		"MANTLE_PRESENTATION_MODE=share-safe" \
		"ORDER_FILE=${ORDER_FILE}" \
		-- --root "${PRESENTATION_ROOT}" --force
	assert_success
	assert_output_contains "IMAGE RENDERED"
	run cat "${ORDER_FILE}"
	assert_output_not_contains "fastfetch"
}

@test "fastfetch-only does not invoke the image renderer" {
	install_imgcat_stub
	install_fastfetch_stub

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" --force --fastfetch-only
	assert_success
	assert_output_contains "FASTFETCH RENDERED"
	run cat "${ORDER_FILE}"
	assert_output_not_contains "imgcat"
}

@test "image renderer failure falls back to plain text without ANSI" {
	install_imgcat_stub 5

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" --force --banner-only
	assert_success
	assert_output_contains "MANTLE TEXT FALLBACK"
	[[ "${output}" != *$'\033'* ]]
}

@test "Fastfetch failure is nonfatal and diagnostic only when requested" {
	install_fastfetch_stub 7

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" --force --fastfetch-only --verbose
	assert_success
	assert_output_contains "failed with status 7"
}

@test "paths containing spaces are forwarded unchanged" {
	local custom_root="${BIN_TEST_HOME}/custom paths"
	local custom_image="${custom_root}/banner image.png"
	local custom_text="${custom_root}/banner text.txt"
	local custom_config="${custom_root}/fastfetch config.jsonc"
	mkdir -p "${custom_root}"
	printf "image\n" >"${custom_image}"
	printf "custom fallback\n" >"${custom_text}"
	printf "{}\n" >"${custom_config}"
	install_imgcat_stub
	install_fastfetch_stub

	run_bin_with_env shell-banner "ORDER_FILE=${ORDER_FILE}" -- \
		--root "${PRESENTATION_ROOT}" \
		--force \
		--image "${custom_image}" \
		--text "${custom_text}" \
		--config "${custom_config}"
	assert_success
	run cat "${ORDER_FILE}"
	assert_output_contains "fastfetch:--config ${custom_config}"
}

@test "explicit unreadable overrides fail before presentation work" {
	run_bin shell-banner --root "${PRESENTATION_ROOT}" --image "${BIN_TEST_HOME}/missing.png"
	assert_status 66
}

@test "shell-banner never invokes network clients" {
	make_stub "curl" 99 ""
	make_stub "wget" 99 ""

	run_bin shell-banner --root "${PRESENTATION_ROOT}" --force --banner-only
	assert_success
}
