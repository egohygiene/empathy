#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# shellcheck shell=bash
# shellcheck disable=SC2034 # Declarative installer metadata is consumed by the runtime.
# Install goreleaser/nfpm from a verified GitHub release.

set -o errexit
set -o nounset
set -o pipefail

if [[ -z "${MANTLE_ROOT:-}" ]]; then
	MANTLE_ROOT="$(builtin cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)"
fi
export MANTLE_ROOT

# shellcheck disable=SC1091
source "${MANTLE_ROOT}/lib/install/runtime.sh"

MANTLE_INSTALL_TOOL_NAME="nfpm"
MANTLE_INSTALL_GITHUB_OWNER="goreleaser"
MANTLE_INSTALL_GITHUB_REPOSITORY="nfpm"
MANTLE_INSTALL_ASSET_TEMPLATE="nfpm_{{version}}_{{platform}}_{{arch}}.tar.gz"
MANTLE_INSTALL_PLATFORM_LINUX="Linux"
MANTLE_INSTALL_PLATFORM_DARWIN="Darwin"
MANTLE_INSTALL_ARCH_X86_64="x86_64"
MANTLE_INSTALL_ARCH_ARM64="arm64"
MANTLE_INSTALL_ARCH_X86="i386"
MANTLE_INSTALL_CHECKSUM_ASSET_TEMPLATE="checksums.txt"
MANTLE_INSTALL_ARCHIVE_FORMAT="tar.gz"
MANTLE_INSTALL_ARCHIVE_MEMBER_TEMPLATE="nfpm"
MANTLE_INSTALL_BINARY_NAME="nfpm"
declare -a MANTLE_INSTALL_VERIFY_ARGUMENTS=("--version")

mantle_install_github_main "$@"
