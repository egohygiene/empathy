# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Contract tests for Mantle's maintained shell-source policy.

setup() {
	load '../test_helper/common'
	load '../test_helper/assertions'
}

maintained_shell_files() {
	find "${MANTLE_ROOT}" -type f \
		\( -name "*.sh" -o -name "*.bash" -o -name "*.bats" -o -name "*.fish" -o -name ".shellrc" \) \
		-print

	local file_path=""
	for file_path in "${MANTLE_ROOT}/bin"/*; do
		[[ -f "${file_path}" ]] || continue
		if [[ "$(head -n 1 "${file_path}")" == "#!/usr/bin/env bash" ]]; then
			printf "%s\n" "${file_path}"
		fi
	done
}

is_executable_shell_role() {
	local relative_path="${1:?}"

	case "${relative_path}" in
	bin/* | install.sh | tests/run.sh | libexec/mantle/commands/*.sh | libexec/mantle/installers/*.sh)
		return 0
		;;
	esac

	return 1
}

@test "maintained shell files declare the repository license" {
	local failed=0
	local file_path=""
	local header=""

	while IFS= read -r file_path; do
		header="$(head -n 8 "${file_path}")"
		if [[ "${header}" != *"Copyright 2026 Ego Hygiene"* ]]; then
			printf "Missing copyright header: %s\n" "${file_path}" >&2
			failed=1
		fi
		if [[ "${header}" != *"SPDX-License-Identifier: MIT"* ]]; then
			printf "Missing SPDX header: %s\n" "${file_path}" >&2
			failed=1
		fi
	done < <(maintained_shell_files)

	[[ "${failed}" -eq 0 ]]
}

@test "executable shell roles have a Bash shebang and executable mode" {
	local failed=0
	local file_path=""
	local relative_path=""

	while IFS= read -r file_path; do
		relative_path="${file_path#"${MANTLE_ROOT}/"}"
		if ! is_executable_shell_role "${relative_path}"; then
			continue
		fi
		if [[ ! -x "${file_path}" ]]; then
			printf "Executable role lacks executable mode: %s\n" "${relative_path}" >&2
			failed=1
		fi
		if [[ "$(head -n 1 "${file_path}")" != "#!/usr/bin/env bash" ]]; then
			printf "Executable role lacks the canonical Bash shebang: %s\n" "${relative_path}" >&2
			failed=1
		fi
	done < <(maintained_shell_files)

	[[ "${failed}" -eq 0 ]]
}

@test "source-only and test files are non-executable and have no shebang" {
	local failed=0
	local file_path=""
	local relative_path=""

	while IFS= read -r file_path; do
		relative_path="${file_path#"${MANTLE_ROOT}/"}"
		if is_executable_shell_role "${relative_path}"; then
			continue
		fi
		if [[ -x "${file_path}" ]]; then
			printf "Source-only role is unexpectedly executable: %s\n" "${relative_path}" >&2
			failed=1
		fi
		if [[ "$(head -n 1 "${file_path}")" == "#!"* ]]; then
			printf "Source-only role has an execution shebang: %s\n" "${relative_path}" >&2
			failed=1
		fi
	done < <(maintained_shell_files)

	[[ "${failed}" -eq 0 ]]
}
