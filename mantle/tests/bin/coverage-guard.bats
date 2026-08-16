# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Coverage guard for bin/ commands.
#
# This test suite enforces that:
#   1. Every regular executable in bin/ has a coverage-map entry.
#   2. Every test file listed in the coverage map exists.
#   3. Every command listed in the map still exists in bin/.
#   4. Every row has the documented five-column schema.
#   5. Every exemption entry has a non-empty justification.
#   6. Commands are unique and the map count matches bin/.
#
# Fail any of these checks to force developers to register new commands.

setup() {
	load 'helpers/environment'
	COVERAGE_MAP="${MANTLE_ROOT}/tests/bin/coverage-map.tsv"
	BIN_DIR="${MANTLE_ROOT}/bin"
}

# ---------------------------------------------------------------------------
# Helper: read the coverage map, skipping blank lines and comments.
# ---------------------------------------------------------------------------

_map_commands() {
	grep -v '^[[:space:]]*#' "${COVERAGE_MAP}" |
		grep -v '^[[:space:]]*$' |
		cut -f1
}

_map_test_files() {
	grep -v '^[[:space:]]*#' "${COVERAGE_MAP}" |
		grep -v '^[[:space:]]*$' |
		cut -f2
}

# ---------------------------------------------------------------------------
# 1. Every executable in bin/ must appear in coverage-map.tsv.
# ---------------------------------------------------------------------------

@test "every bin/ executable has a coverage-map entry" {
	local missing=0
	local cmd
	for f in "${BIN_DIR}"/*; do
		[[ -f "${f}" && -x "${f}" ]] || continue
		cmd="${f##*/}"
		if ! grep -q "^${cmd}	" "${COVERAGE_MAP}"; then
			printf "Missing coverage-map entry for: %s\n" "${cmd}" >&2
			missing=1
		fi
	done
	[[ "${missing}" -eq 0 ]]
}

# ---------------------------------------------------------------------------
# 2. Every test file listed in the map must exist.
# ---------------------------------------------------------------------------

@test "every coverage-map test file exists" {
	local missing=0
	local test_file
	while IFS=$'\t' read -r cmd test_file _rest; do
		[[ "${cmd}" =~ ^[[:space:]]*# ]] && continue
		[[ -z "${cmd}" ]] && continue
		local full_path="${MANTLE_ROOT}/tests/${test_file}"
		if [[ ! -f "${full_path}" ]]; then
			printf "Missing test file for %s: %s\n" "${cmd}" "${full_path}" >&2
			missing=1
		fi
	done < <(grep -v '^[[:space:]]*#' "${COVERAGE_MAP}" | grep -v '^[[:space:]]*$')
	[[ "${missing}" -eq 0 ]]
}

# ---------------------------------------------------------------------------
# 3. Every command in the map must still exist in bin/.
# ---------------------------------------------------------------------------

@test "every coverage-map command still exists in bin/" {
	local stale=0
	local cmd
	while IFS=$'\t' read -r cmd _rest; do
		[[ "${cmd}" =~ ^[[:space:]]*# ]] && continue
		[[ -z "${cmd}" ]] && continue
		if [[ ! -f "${BIN_DIR}/${cmd}" ]]; then
			printf "Coverage-map references non-existent command: %s\n" "${cmd}" >&2
			stale=1
		fi
	done < <(grep -v '^[[:space:]]*#' "${COVERAGE_MAP}" | grep -v '^[[:space:]]*$')
	[[ "${stale}" -eq 0 ]]
}

# ---------------------------------------------------------------------------
# 4. Every row uses the documented schema.
# ---------------------------------------------------------------------------

@test "every coverage-map row has five populated columns" {
	local bad=0
	local cmd test_file categories exemptions reason extra
	while IFS=$'\t' read -r cmd test_file categories exemptions reason extra; do
		[[ "${cmd}" =~ ^[[:space:]]*# ]] && continue
		[[ -z "${cmd}" ]] && continue
		if [[ -z "${test_file}" || -z "${categories}" || -z "${exemptions}" || -z "${reason}" || -n "${extra}" ]]; then
			printf "Invalid coverage-map schema for %s\n" "${cmd}" >&2
			bad=1
		fi
	done <"${COVERAGE_MAP}"
	[[ "${bad}" -eq 0 ]]
}

# ---------------------------------------------------------------------------
# 5. Every exemption must have a non-empty justification.
# ---------------------------------------------------------------------------

@test "every coverage-map exemption has a justification" {
	local bad=0
	local cmd exemptions reason
	while IFS=$'\t' read -r cmd _test_file _categories exemptions reason; do
		[[ "${cmd}" =~ ^[[:space:]]*# ]] && continue
		[[ -z "${cmd}" ]] && continue
		# Skip entries with no exemptions.
		[[ "${exemptions}" == "none" || -z "${exemptions}" ]] && continue
		if [[ -z "${reason}" || "${reason}" == "none" ]]; then
			printf "Exemption for %s (%s) lacks a justification\n" \
				"${cmd}" "${exemptions}" >&2
			bad=1
		fi
	done < <(grep -v '^[[:space:]]*#' "${COVERAGE_MAP}" | grep -v '^[[:space:]]*$')
	[[ "${bad}" -eq 0 ]]
}

# ---------------------------------------------------------------------------
# 6. Commands are unique and the map has exactly the right entry count.
# ---------------------------------------------------------------------------

@test "coverage-map commands are unique" {
	local duplicates=""
	duplicates="$(_map_commands | sort | uniq -d)"
	if [[ -n "${duplicates}" ]]; then
		printf "Duplicate coverage-map commands:\n%s\n" "${duplicates}" >&2
		return 1
	fi
}

@test "coverage-map entry count matches bin/ executable count" {
	local bin_count=0
	local map_count=0

	for f in "${BIN_DIR}"/*; do
		[[ -f "${f}" && -x "${f}" ]] && ((bin_count++)) || true
	done

	while IFS=$'\t' read -r cmd _rest; do
		[[ "${cmd}" =~ ^[[:space:]]*# ]] && continue
		[[ -z "${cmd}" ]] && continue
		((map_count++)) || true
	done < <(grep -v '^[[:space:]]*#' "${COVERAGE_MAP}" | grep -v '^[[:space:]]*$')

	if [[ "${bin_count}" -ne "${map_count}" ]]; then
		printf "bin/ has %d executables but coverage-map has %d entries\n" \
			"${bin_count}" "${map_count}" >&2
		return 1
	fi
}
