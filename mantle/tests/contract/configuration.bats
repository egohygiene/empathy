# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Contract checks for Mantle's versioned configuration registries.

setup() {
	load '../test_helper/common'
	load '../test_helper/assertions'
}

@test "profile registry has unique names and valid typed values" {
	local failed=0
	local schema profile safe network system legacy safety history updates experimental presentation _description
	while IFS=$'\t' read -r schema profile safe network system legacy safety history updates experimental presentation _description; do
		[[ "${schema}" == "schema_version" ]] && continue
		[[ "${schema}" == "1" ]] || failed=1
		[[ "${profile}" =~ ^[a-z0-9][a-z0-9-]*$ ]] || failed=1
		for value in "${safe}" "${network}" "${system}" "${legacy}" "${safety}" "${history}" "${updates}" "${experimental}"; do
			[[ "${value}" == "true" || "${value}" == "false" ]] || failed=1
		done
		case "${presentation}" in private | share-safe | ci | off) ;; *) failed=1 ;; esac
	done <"${MANTLE_ROOT}/config/profiles.tsv"
	[[ "$(tail -n +2 "${MANTLE_ROOT}/config/profiles.tsv" | cut -f 2 | sort | uniq -d | wc -l | tr -d ' ')" -eq 0 ]]
	[[ "${failed}" -eq 0 ]]
}

@test "settings registry has unique keys and environment overrides" {
	[[ "$(tail -n +2 "${MANTLE_ROOT}/config/settings.tsv" | cut -f 1 | sort | uniq -d | wc -l | tr -d ' ')" -eq 0 ]]
	[[ "$(tail -n +2 "${MANTLE_ROOT}/config/settings.tsv" | cut -f 3 | sort | uniq -d | wc -l | tr -d ' ')" -eq 0 ]]
}

@test "shipped example config validates through the public CLI" {
	run env -i HOME="${BATS_TEST_TMPDIR}" PATH="${PATH}" MANTLE_ROOT="${MANTLE_ROOT}" \
		"${MANTLE_ROOT}/bin/mantle" config validate "${MANTLE_ROOT}/config/example.conf"
	assert_success
	assert_output_contains "status: loaded"
}
