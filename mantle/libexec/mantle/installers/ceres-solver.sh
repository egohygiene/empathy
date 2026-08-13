#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2034 # Declarative installer metadata is consumed by the runtime.
# Install the Ceres Solver development library with the native package manager.

set -o errexit
set -o nounset
set -o pipefail

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	MANTLE_ROOT="$(builtin cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)"
fi
export MANTLE_ROOT

# shellcheck disable=SC1091
source "${MANTLE_ROOT}/lib/install/runtime.sh"

MANTLE_INSTALL_TOOL_NAME="ceres-solver"
declare -a MANTLE_INSTALL_PACKAGES_APT=("libceres-dev")
declare -a MANTLE_INSTALL_PACKAGES_BREW=("ceres-solver")
declare -a MANTLE_INSTALL_PACKAGES_DNF=("ceres-solver-devel")
declare -a MANTLE_INSTALL_PACKAGES_PACMAN=("ceres-solver")
declare -a MANTLE_INSTALL_PACKAGES_ZYPPER=("ceres-solver-devel")

mantle_install_native_package_main "$@"
