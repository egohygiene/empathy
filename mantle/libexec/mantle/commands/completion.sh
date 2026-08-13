#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2249 # Closed case statements intentionally treat unmatched values as no-ops.
# Generate shell completion definitions for the public Mantle CLI.

set -o errexit
set -o nounset
set -o pipefail

mantle_completion_usage() {
	printf "%s\n" \
		"Usage: mantle completion SHELL" \
		"" \
		"Generate completion definitions for bash, zsh, or fish."
}

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	printf "[mantle:error] MANTLE_ROOT is required for command dispatch\n" >&2
	exit 70
fi

if (($# == 0)); then
	mantle_completion_usage
	exit 0
fi

case "$1" in
--summary)
	printf "Generate shell completion definitions.\n"
	exit 0
	;;
--help | -h)
	mantle_completion_usage
	exit 0
	;;
esac

if (($# != 1)); then
	printf "[mantle:error] completion requires exactly one shell name\n" >&2
	mantle_completion_usage >&2
	exit 64
fi

mantle_completion_commands=""
for mantle_completion_path in "${MANTLE_ROOT}/libexec/mantle/commands"/*.sh; do
	[[ -f "${mantle_completion_path}" && -x "${mantle_completion_path}" ]] || continue
	mantle_completion_name="${mantle_completion_path##*/}"
	mantle_completion_name="${mantle_completion_name%.sh}"
	mantle_completion_commands="${mantle_completion_commands}${mantle_completion_commands:+ }${mantle_completion_name}"
done

mantle_completion_installers=""
for mantle_completion_path in "${MANTLE_ROOT}/libexec/mantle/installers"/*.sh; do
	[[ -f "${mantle_completion_path}" && -x "${mantle_completion_path}" ]] || continue
	mantle_completion_name="${mantle_completion_path##*/}"
	mantle_completion_name="${mantle_completion_name%.sh}"
	mantle_completion_installers="${mantle_completion_installers}${mantle_completion_installers:+ }${mantle_completion_name}"
done

case "$1" in
bash)
	# The expressions below belong to generated Bash.
	# shellcheck disable=SC2016
	printf '%s\n' \
		'_mantle_completion() {' \
		'  local current previous' \
		'  current="${COMP_WORDS[COMP_CWORD]}"' \
		'  previous="${COMP_WORDS[COMP_CWORD-1]}"' \
		'  if [[ "${COMP_CWORD}" -eq 1 ]]; then' \
		"    COMPREPLY=( \$(compgen -W \"${mantle_completion_commands}\" -- \"\${current}\") )" \
		'  elif [[ "${COMP_WORDS[1]}" == "install" && "${COMP_CWORD}" -eq 2 ]]; then' \
		"    COMPREPLY=( \$(compgen -W \"${mantle_completion_installers}\" -- \"\${current}\") )" \
		'  elif [[ "${COMP_WORDS[1]}" == "completion" && "${COMP_CWORD}" -eq 2 ]]; then' \
		'    COMPREPLY=( $(compgen -W "bash zsh fish" -- "${current}") )' \
		'  elif [[ "${COMP_WORDS[1]}" == "config" && "${COMP_CWORD}" -eq 2 ]]; then' \
		'    COMPREPLY=( $(compgen -W "list-profiles path validate show explain" -- "${current}") )' \
		'  elif [[ "${previous}" == "fastfetch" ]]; then' \
		'    COMPREPLY=( $(compgen -W "runtime workspace toolchains contexts" -- "${current}") )' \
		'  fi' \
		'}' \
		'complete -F _mantle_completion mantle'
	;;
zsh)
	# $words belongs to generated Zsh.
	# shellcheck disable=SC2016
	printf '#compdef mantle\n_arguments "1:command:(%s)" "2:argument:->args"\ncase $words[2] in\n  install) _values "installer" %s ;;\n  completion) _values "shell" bash zsh fish ;;\n  config) _values "config command" list-profiles path validate show explain ;;\n  fastfetch) _values "collector" runtime workspace toolchains contexts ;;\nesac\n' \
		"${mantle_completion_commands}" "${mantle_completion_installers}"
	;;
fish)
	printf "complete -c mantle -f -n '__fish_use_subcommand' -a '%s'\n" "${mantle_completion_commands}"
	printf "complete -c mantle -f -n '__fish_seen_subcommand_from install' -a '%s'\n" "${mantle_completion_installers}"
	printf "complete -c mantle -f -n '__fish_seen_subcommand_from completion' -a 'bash zsh fish'\n"
	printf "complete -c mantle -f -n '__fish_seen_subcommand_from config' -a 'list-profiles path validate show explain'\n"
	printf "complete -c mantle -f -n '__fish_seen_subcommand_from fastfetch' -a 'runtime workspace toolchains contexts'\n"
	;;
*)
	printf "[mantle:error] unsupported completion shell: %s\n" "$1" >&2
	mantle_completion_usage >&2
	exit 64
	;;
esac
