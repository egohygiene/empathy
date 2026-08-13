#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2034 # Declarative installer metadata is consumed by the runtime.
# Install libE57Format development files with the native package manager.

set -o errexit
set -o nounset
set -o pipefail

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	MANTLE_ROOT="$(builtin cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)"
fi
export MANTLE_ROOT

# shellcheck disable=SC1091
source "${MANTLE_ROOT}/lib/install/runtime.sh"

MANTLE_INSTALL_TOOL_NAME="e57format"
declare -a MANTLE_INSTALL_PACKAGES_APT=("libe57format-dev")
declare -a MANTLE_INSTALL_PACKAGES_BREW=("libe57")
declare -a MANTLE_INSTALL_PACKAGES_DNF=("libe57-devel")
declare -a MANTLE_INSTALL_PACKAGES_PACMAN=("libe57")
declare -a MANTLE_INSTALL_PACKAGES_ZYPPER=("libe57-devel")

mantle_install_native_package_main "$@"
