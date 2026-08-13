#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2034 # Declarative installer metadata is consumed by the runtime.
# Install HTTPie as an isolated Python CLI.

set -o errexit
set -o nounset
set -o pipefail

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	MANTLE_ROOT="$(builtin cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)"
fi
export MANTLE_ROOT

# shellcheck disable=SC1091
source "${MANTLE_ROOT}/lib/install/runtime.sh"

MANTLE_INSTALL_TOOL_NAME="httpie"
MANTLE_INSTALL_PYTHON_PACKAGE="httpie"
MANTLE_INSTALL_VERSION="${HTTPIE_VERSION:-}"
declare -a MANTLE_INSTALL_PYTHON_EXECUTABLES=("http" "https")

mantle_install_python_tool_main "$@"
