######################################################################
# UBI Full Variant
#
# This is the full-featured "kitchen sink" version of UBI combining
# Python and Node.js development tools.
# Includes Python 3.13, Node.js v20, and their package managers.
#
# Use this variant when:
# - Working in polyglot environments
# - Need maximum flexibility for heavy workflows
# - Building devcontainers for large, multi-language projects
######################################################################

######################################################################
# BASE IMAGE VERSION PINNING
#
# CURRENT VERSION: 2.1.2
# CURRENT DIGEST: sha256:36751f1ee2f30745a649afc2b2061f321bacdaa0617159901fe6725b34c93df4
# LAST UPDATED: 2025-12-12
######################################################################
FROM mcr.microsoft.com/devcontainers/base:2.1.2@sha256:36751f1ee2f30745a649afc2b2061f321bacdaa0617159901fe6725b34c93df4 AS base

# Safer shell defaults
SHELL ["/bin/bash", "-o", "errexit", "-o", "errtrace", "-o", "functrace", "-o", "nounset", "-o", "pipefail", "-c"]

FROM base AS environment

######################################################################
# ARG DEFINITIONS
######################################################################

# System + locale
ARG TMPDIR=/tmp
ARG LANG=en_US.UTF-8
ARG LANGUAGE=en_US:en
ARG LC_ALL=en_US.UTF-8
ARG TZ=UTC

# UX Preferences
ARG EDITOR=code
ARG VISUAL=code
ARG PAGER=less
ARG GIT_PAGER=less
ARG TERM=xterm-256color
ARG COLORTERM=truecolor
ARG CLICOLOR=1
ARG CLICOLOR_FORCE=1
ARG FORCE_COLOR=1
ARG GCC_COLORS="error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01"
ARG LESS="-R"

# Node memory config
ARG NODE_OPTIONS="--max-old-space-size=4096 --max-semi-space-size=512"

# Rust UX
ARG CARGO_TERM_COLOR=always

# Telemetry controls
ARG DO_NOT_TRACK=1
ARG TELEMETRY_ENABLED=0
ARG NEXT_TELEMETRY_DISABLED=1
ARG YARN_ENABLE_TELEMETRY=false
ARG DOTNET_CLI_TELEMETRY_OPTOUT=1
ARG GATSBY_TELEMETRY_DISABLED=1
ARG NUXT_TELEMETRY_DISABLED=1
ARG CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=true
ARG STRIPE_CLI_TELEMETRY_OPTOUT=1

# Python behavior
ARG PYTHONWARNINGS=default
ARG PYTHONFAULTHANDLER=1
ARG PYTHONHASHSEED=random
ARG PYTHONUNBUFFERED=1
ARG PYTHONUTF8=1
ARG PYTHONIOENCODING=UTF-8
ARG PIP_DEFAULT_TIMEOUT=200
ARG PIP_DISABLE_PIP_VERSION_CHECK=on
ARG PIP_NO_CACHE_DIR=1
ARG PIP_NO_WARN_SCRIPT_LOCATION=on

######################################################################
# FIXED PLATFORM-LEVEL ENVIRONMENT VARIABLES
######################################################################

# Workspace home
ENV WORKSPACE_HOME=/workspace

# Universal filesystem layout
ENV UNIVERSAL_HOME=/opt/universal \
    UNIVERSAL_BIN=/opt/universal/bin \
    UNIVERSAL_TOOLBOX=/opt/universal/toolbox \
    UNIVERSAL_CACHE=/opt/universal/cache \
    UNIVERSAL_LOGS=/opt/universal/logs \
    UNIVERSAL_CONFIG=/opt/universal/config \
    UNIVERSAL_LIB=/opt/universal/lib \
    UNIVERSAL_LOCKS=/opt/universal/locks \
    UNIVERSAL_FONTS=/opt/universal/fonts \
    UNIVERSAL_RUNTIME=/opt/universal/runtime \
    UNIVERSAL_APPS=/opt/universal/apps \
    UNIVERSAL_REPORTS=/opt/universal/reports \
    APT_CACHE_DIR=/opt/universal/cache/apt

######################################################################
# BASE ENVIRONMENT
######################################################################
ENV \
    ##################################################################
    # Locale + system
    ##################################################################
    LANG=${LANG} \
    LANGUAGE=${LANGUAGE} \
    LC_ALL=${LC_ALL} \
    TZ=${TZ} \
    TMPDIR=${TMPDIR} \
    TERM=${TERM} \
    COLORTERM=${COLORTERM} \
    LESS=${LESS} \
    CLICOLOR=${CLICOLOR} \
    CLICOLOR_FORCE=${CLICOLOR_FORCE} \
    FORCE_COLOR=${FORCE_COLOR} \
    GCC_COLORS=${GCC_COLORS} \
    EDITOR=${EDITOR} \
    VISUAL=${VISUAL} \
    PAGER=${PAGER} \
    GIT_PAGER=${GIT_PAGER} \
    ##################################################################
    # Python defaults
    ##################################################################
    PYTHONUNBUFFERED=${PYTHONUNBUFFERED} \
    PYTHONIOENCODING=${PYTHONIOENCODING} \
    PYTHONUTF8=${PYTHONUTF8} \
    PYTHONHASHSEED=${PYTHONHASHSEED} \
    PYTHONFAULTHANDLER=${PYTHONFAULTHANDLER} \
    PYTHONWARNINGS=${PYTHONWARNINGS} \
    PIP_NO_CACHE_DIR=${PIP_NO_CACHE_DIR} \
    PIP_DISABLE_PIP_VERSION_CHECK=${PIP_DISABLE_PIP_VERSION_CHECK} \
    PIP_NO_WARN_SCRIPT_LOCATION=${PIP_NO_WARN_SCRIPT_LOCATION} \
    PIP_DEFAULT_TIMEOUT=${PIP_DEFAULT_TIMEOUT} \
    PIP_ROOT_USER_ACTION=ignore \
    ##################################################################
    # Node / Rust
    ##################################################################
    NODE_OPTIONS="${NODE_OPTIONS}" \
    CARGO_TERM_COLOR=${CARGO_TERM_COLOR} \
    ##################################################################
    # Telemetry toggles
    ##################################################################
    DO_NOT_TRACK=${DO_NOT_TRACK} \
    TELEMETRY_ENABLED=${TELEMETRY_ENABLED} \
    NEXT_TELEMETRY_DISABLED=${NEXT_TELEMETRY_DISABLED} \
    YARN_ENABLE_TELEMETRY=${YARN_ENABLE_TELEMETRY} \
    DOTNET_CLI_TELEMETRY_OPTOUT=${DOTNET_CLI_TELEMETRY_OPTOUT} \
    GATSBY_TELEMETRY_DISABLED=${GATSBY_TELEMETRY_DISABLED} \
    NUXT_TELEMETRY_DISABLED=${NUXT_TELEMETRY_DISABLED} \
    CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=${CLOUDSDK_CORE_DISABLE_USAGE_REPORTING} \
    STRIPE_CLI_TELEMETRY_OPTOUT=${STRIPE_CLI_TELEMETRY_OPTOUT} \
    ##################################################################
    # Debian noninteractive install behavior
    ##################################################################
    DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    DEBIAN_PRIORITY=critical \
    DEBCONF_NOWARNINGS=yes \
    APT_LISTCHANGES_FRONTEND=none \
    APT_LISTBUGS_FRONTEND=none

######################################################################
# XDG DIRECTORY OVERRIDES
######################################################################
ENV \
    XDG_CONFIG_HOME=${UNIVERSAL_CONFIG} \
    XDG_CACHE_HOME=${UNIVERSAL_CACHE} \
    XDG_DATA_HOME=${UNIVERSAL_TOOLBOX} \
    XDG_STATE_HOME=${UNIVERSAL_RUNTIME} \
    XDG_CONFIG_DIRS="${UNIVERSAL_CONFIG}:/etc/xdg" \
    XDG_DATA_DIRS="${UNIVERSAL_APPS}:/usr/local/share:/usr/share"

######################################################################
# CREATE UNIVERSAL DIRECTORIES
######################################################################
RUN mkdir -p \
    ${UNIVERSAL_BIN} \
    ${UNIVERSAL_TOOLBOX} \
    ${UNIVERSAL_CACHE} \
    ${UNIVERSAL_LOGS} \
    ${UNIVERSAL_CONFIG} \
    ${UNIVERSAL_LIB} \
    ${UNIVERSAL_LOCKS} \
    ${UNIVERSAL_FONTS} \
    ${UNIVERSAL_RUNTIME} \
    ${UNIVERSAL_APPS} \
    ${UNIVERSAL_REPORTS} \
  && chown -R vscode:vscode ${UNIVERSAL_HOME}

FROM environment AS python-tools

######################################################################
# INSTALL PYTHON DEVELOPMENT TOOLS
######################################################################

# Install Python build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry for Python package management via pip
# Note: This may fail in restricted environments (e.g., externally-managed-environment error)
# Core Python tooling (python3, pip, venv) is always available
RUN python3 -m pip install --user poetry 2>/dev/null || echo "Poetry installation skipped (restricted environment)" \
  && if [ -f /root/.local/bin/poetry ]; then ln -s /root/.local/bin/poetry ${UNIVERSAL_BIN}/poetry; fi

# Set up pyenv environment variables for future manual installation
# Users can install pyenv manually using: curl https://pyenv.run | bash
ENV PYENV_ROOT="${UNIVERSAL_TOOLBOX}/pyenv"
ENV PATH="${PYENV_ROOT}/bin:${PYENV_ROOT}/shims:${PATH}"

FROM python-tools AS node-tools

######################################################################
# INSTALL NODE.JS DEVELOPMENT TOOLS
######################################################################

# Install Node.js and npm via apt
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install pnpm and yarn globally
# Note: This may fail in restricted environments (e.g., certificate issues)
# Core Node.js tooling (node, npm) is always available
RUN npm install -g pnpm yarn 2>/dev/null || echo "pnpm/yarn installation skipped (restricted environment)"

# Set up nvm environment variables for future manual installation
# Users can install nvm manually using: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
ENV NVM_DIR="${UNIVERSAL_TOOLBOX}/nvm"

FROM node-tools AS final

######################################################################
# HEALTHCHECK
######################################################################
# Validates container health by checking bash, python3, and node availability.
# This ensures the shell environment and both language runtimes are operational.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD test -x /bin/bash && command -v python3 >/dev/null 2>&1 && command -v node >/dev/null 2>&1 || exit 1

######################################################################
# Final container command
######################################################################
CMD ["bash", "-lc", "sleep infinity"]




#### Dockerfile 2

FROM mcr.microsoft.com/devcontainers/base:2.1.3@sha256:30b0a0c004ca94d36c323ee993361a7e0ae25ea255ea125201e8a9587501c324 AS base

# Safer shell defaults
SHELL ["/bin/bash", "-o", "errexit", "-o", "errtrace", "-o", "functrace", "-o", "nounset", "-o", "pipefail", "-c"]

FROM base AS environment

######################################################################
# ARG DEFINITIONS
######################################################################

# System + locale
ARG TMPDIR=/tmp
ARG LANG=en_US.UTF-8
ARG LANGUAGE=en_US:en
ARG LC_ALL=en_US.UTF-8
ARG TZ=UTC

# UX Preferences
ARG EDITOR=code
ARG VISUAL=code
ARG PAGER=less
ARG GIT_PAGER=less
ARG TERM=xterm-256color
ARG COLORTERM=truecolor
ARG CLICOLOR=1
ARG CLICOLOR_FORCE=1
ARG FORCE_COLOR=1
ARG GCC_COLORS="error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01"
ARG LESS="-R"

# Node memory config
ARG NODE_OPTIONS="--max-old-space-size=4096 --max-semi-space-size=512"

# Rust UX
ARG CARGO_TERM_COLOR=always

# Telemetry controls
ARG DO_NOT_TRACK=1
ARG TELEMETRY_ENABLED=0
ARG NEXT_TELEMETRY_DISABLED=1
ARG YARN_ENABLE_TELEMETRY=false
ARG DOTNET_CLI_TELEMETRY_OPTOUT=1
ARG GATSBY_TELEMETRY_DISABLED=1
ARG NUXT_TELEMETRY_DISABLED=1
ARG CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=true
ARG STRIPE_CLI_TELEMETRY_OPTOUT=1

# Python behavior
ARG PYTHONWARNINGS=default
ARG PYTHONFAULTHANDLER=1
ARG PYTHONHASHSEED=random
ARG PYTHONUNBUFFERED=1
ARG PYTHONUTF8=1
ARG PYTHONIOENCODING=UTF-8
ARG PIP_DEFAULT_TIMEOUT=200
ARG PIP_DISABLE_PIP_VERSION_CHECK=on
ARG PIP_NO_CACHE_DIR=1
ARG PIP_NO_WARN_SCRIPT_LOCATION=on

######################################################################
# FIXED PLATFORM-LEVEL ENVIRONMENT VARIABLES
######################################################################

# Workspace home
ENV WORKSPACE_HOME=/workspace

# Universal filesystem layout
ENV UNIVERSAL_HOME=/opt/universal \
    UNIVERSAL_BIN=/opt/universal/bin \
    UNIVERSAL_TOOLBOX=/opt/universal/toolbox \
    UNIVERSAL_CACHE=/opt/universal/cache \
    UNIVERSAL_LOGS=/opt/universal/logs \
    UNIVERSAL_CONFIG=/opt/universal/config \
    UNIVERSAL_LIB=/opt/universal/lib \
    UNIVERSAL_LOCKS=/opt/universal/locks \
    UNIVERSAL_FONTS=/opt/universal/fonts \
    UNIVERSAL_RUNTIME=/opt/universal/runtime \
    UNIVERSAL_APPS=/opt/universal/apps \
    UNIVERSAL_REPORTS=/opt/universal/reports \
    APT_CACHE_DIR=/opt/universal/cache/apt

######################################################################
# BASE ENVIRONMENT
######################################################################
ENV \
    ##################################################################
    # Locale + system
    ##################################################################
    LANG=${LANG} \
    LANGUAGE=${LANGUAGE} \
    LC_ALL=${LC_ALL} \
    TZ=${TZ} \
    TMPDIR=${TMPDIR} \
    TERM=${TERM} \
    COLORTERM=${COLORTERM} \
    LESS=${LESS} \
    CLICOLOR=${CLICOLOR} \
    CLICOLOR_FORCE=${CLICOLOR_FORCE} \
    FORCE_COLOR=${FORCE_COLOR} \
    GCC_COLORS=${GCC_COLORS} \
    EDITOR=${EDITOR} \
    VISUAL=${VISUAL} \
    PAGER=${PAGER} \
    GIT_PAGER=${GIT_PAGER} \
    ##################################################################
    # Python defaults
    ##################################################################
    PYTHONUNBUFFERED=${PYTHONUNBUFFERED} \
    PYTHONIOENCODING=${PYTHONIOENCODING} \
    PYTHONUTF8=${PYTHONUTF8} \
    PYTHONHASHSEED=${PYTHONHASHSEED} \
    PYTHONFAULTHANDLER=${PYTHONFAULTHANDLER} \
    PYTHONWARNINGS=${PYTHONWARNINGS} \
    PIP_NO_CACHE_DIR=${PIP_NO_CACHE_DIR} \
    PIP_DISABLE_PIP_VERSION_CHECK=${PIP_DISABLE_PIP_VERSION_CHECK} \
    PIP_NO_WARN_SCRIPT_LOCATION=${PIP_NO_WARN_SCRIPT_LOCATION} \
    PIP_DEFAULT_TIMEOUT=${PIP_DEFAULT_TIMEOUT} \
    PIP_ROOT_USER_ACTION=ignore \
    ##################################################################
    # Node / Rust
    ##################################################################
    NODE_OPTIONS="${NODE_OPTIONS}" \
    CARGO_TERM_COLOR=${CARGO_TERM_COLOR} \
    ##################################################################
    # Telemetry toggles
    ##################################################################
    DO_NOT_TRACK=${DO_NOT_TRACK} \
    TELEMETRY_ENABLED=${TELEMETRY_ENABLED} \
    NEXT_TELEMETRY_DISABLED=${NEXT_TELEMETRY_DISABLED} \
    YARN_ENABLE_TELEMETRY=${YARN_ENABLE_TELEMETRY} \
    DOTNET_CLI_TELEMETRY_OPTOUT=${DOTNET_CLI_TELEMETRY_OPTOUT} \
    GATSBY_TELEMETRY_DISABLED=${GATSBY_TELEMETRY_DISABLED} \
    NUXT_TELEMETRY_DISABLED=${NUXT_TELEMETRY_DISABLED} \
    CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=${CLOUDSDK_CORE_DISABLE_USAGE_REPORTING} \
    STRIPE_CLI_TELEMETRY_OPTOUT=${STRIPE_CLI_TELEMETRY_OPTOUT} \
    ##################################################################
    # Debian noninteractive install behavior
    ##################################################################
    DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    DEBIAN_PRIORITY=critical \
    DEBCONF_NOWARNINGS=yes \
    APT_LISTCHANGES_FRONTEND=none \
    APT_LISTBUGS_FRONTEND=none

######################################################################
# XDG DIRECTORY OVERRIDES
# - https://wiki.archlinux.org/title/XDG_Base_Directory
# - https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
#
# Add user application .desktop files to gnome.
# https://help.gnome.org/admin//system-admin-guide/2.32/menustructure-desktopentry.html.en
######################################################################
ENV \
    XDG_CONFIG_HOME=${UNIVERSAL_CONFIG} \
    XDG_CACHE_HOME=${UNIVERSAL_CACHE} \
    XDG_DATA_HOME=${UNIVERSAL_TOOLBOX} \
    XDG_STATE_HOME=${UNIVERSAL_RUNTIME} \
    XDG_CONFIG_DIRS="${UNIVERSAL_CONFIG}:/etc/xdg" \
    XDG_DATA_DIRS="${UNIVERSAL_APPS}:/usr/local/share:/usr/share"

######################################################################
# CREATE UNIVERSAL DIRECTORIES
######################################################################
RUN mkdir -p \
    ${UNIVERSAL_BIN} \
    ${UNIVERSAL_TOOLBOX} \
    ${UNIVERSAL_CACHE} \
    ${UNIVERSAL_LOGS} \
    ${UNIVERSAL_CONFIG} \
    ${UNIVERSAL_LIB} \
    ${UNIVERSAL_LOCKS} \
    ${UNIVERSAL_FONTS} \
    ${UNIVERSAL_RUNTIME} \
    ${UNIVERSAL_APPS} \
    ${UNIVERSAL_REPORTS} \
  && chown -R vscode:vscode ${UNIVERSAL_HOME}

FROM environment AS nix-setup

######################################################################
# INSTALL NIX PACKAGE MANAGER (SINGLE-USER MODE)
######################################################################
# Install Nix in single-user mode for the vscode user.
# Single-user mode is appropriate for devcontainers where:
# - Only one user (vscode) needs access to Nix
# - We want to avoid the complexity of the Nix daemon
# - File ownership needs to be clear and simple
#
# Reference: https://nixos.org/download.html#nix-install-linux
######################################################################

# Dependencies (curl, ca-certificates, xz-utils) are already present in base image

# Create /nix directory and set ownership to vscode user
RUN mkdir -p /nix \
  && chown -R vscode:vscode /nix

# Switch to vscode user to install Nix in single-user mode
USER vscode

# Download and run Nix installer in single-user mode
# Pin to a specific version for reproducibility and security
# Using version 2.24.10 (latest stable as of Dec 2024)
RUN curl -L https://releases.nixos.org/nix/nix-2.24.10/install | sh -s -- --no-daemon

# Add Nix to PATH for all shells
# Define the sourcing snippet once to avoid duplication
RUN NIX_PROFILE_SCRIPT='if [ -e $HOME/.nix-profile/etc/profile.d/nix.sh ]; then . $HOME/.nix-profile/etc/profile.d/nix.sh; fi' \
  && echo "$NIX_PROFILE_SCRIPT" >> ~/.bashrc \
  && echo "$NIX_PROFILE_SCRIPT" >> ~/.profile

# Switch back to root for final setup
USER root

# Ensure /nix ownership is correct after installation
# This is critical because:
# 1. The Nix installer creates subdirectories under /nix
# 2. If the vscode user's UID changes (via updateRemoteUserUID), ownership must be fixed
# 3. This ensures Nix commands can write to the store
RUN chown -R vscode:vscode /nix

FROM nix-setup AS final

######################################################################
# HEALTHCHECK
######################################################################
# Validates container health by checking bash executable availability.
# This ensures the container's fundamental shell environment is operational.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD test -x /bin/bash || exit 1

######################################################################
# Final container command
######################################################################
CMD ["bash", "-lc", "sleep infinity"]


### Dockerfile 3
# syntax=docker/dockerfile:1.4
# cspell:ignore rmid lmodern rdepends
######################################################################
# Development container image
#
# This Dockerfile builds the image used by the VS Code devcontainer.
# It extends the official devcontainers base image and installs a
# collection of common build tools, language runtimes and utilities.
#
# The image is pinned to a specific digest so that builds are
# reproducible. Feel free to add or remove packages to suit your
# project's needs.
######################################################################
FROM mcr.microsoft.com/devcontainers/base@sha256:daa08ddb48ad4e4e7367c348e0a6f250762f1f0d8348f1f9acbef5f884ce093d AS base

# Override the default temporary directory if needed. Useful when
# working on filesystems where /tmp has limited space.
ARG TMPDIR=/tmp

# Locale and timezone settings used during build and at runtime
ARG LANG=en_US.UTF-8
ARG LANGUAGE=en_US:en
ARG TZ=UTC
ARG LC_ALL=en_US.UTF-8

# Optional TeX Live installation
ARG INSTALL_TEXLIVE=false

# Core environment variables for non-interactive apt operations and consistent Python behavior.
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    DEBIAN_PRIORITY=critical \
    DEBCONF_NOWARNINGS=yes \
    TERM=xterm-256color \
    APT_LISTCHANGES_FRONTEND=none \
    APT_LISTBUGS_FRONTEND=none \
    TMPDIR=${TMPDIR} \
    LANG=${LANG} \
    LANGUAGE=${LANGUAGE} \
    TZ=${TZ} \
    LC_ALL=${LC_ALL} \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONUTF8=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_WARN_SCRIPT_LOCATION=on \
    PIP_DEFAULT_TIMEOUT=200 \
    GNUTLS_FORCE_FIPS_MODE=1 \
    INSTALL_TEXLIVE=${INSTALL_TEXLIVE}

# Location where additional development utilities are installed
ENV DEVTOOLS_HOME=/opt/devtools
ENV DEVTOOLS_BIN="${DEVTOOLS_HOME}/bin"
ENV DEVTOOLS_TOOLBOX="${DEVTOOLS_HOME}/toolbox"
ENV DEVTOOLS_CACHE="${DEVTOOLS_HOME}/cache"
ENV DEVTOOLS_LOGS="${DEVTOOLS_HOME}/logs"
ENV DEVTOOLS_CONFIG="${DEVTOOLS_HOME}/config"
ENV DEVTOOLS_LIB="${DEVTOOLS_HOME}/lib"
ENV DEVTOOLS_LOCKS="${DEVTOOLS_HOME}/locks"
ENV DEVTOOLS_FONTS="${DEVTOOLS_HOME}/fonts"
ENV DEVTOOLS_RUNTIME="${DEVTOOLS_HOME}/runtime"

# Configure the ASDF version manager.
ENV ASDF_DIR="${DEVTOOLS_HOME}/.asdf"
ENV ASDF_DATA_DIR="${ASDF_DIR}/data"
ENV ASDF_SHIMS_DIR="${ASDF_DATA_DIR}/shims"

# Taskfile installation directory
ENV TASKFILE_HOME_DIR="${DEVTOOLS_HOME}/.task"

# Prepend devtool locations to the PATH for easy access
ENV PATH="${DEVTOOLS_BIN}:${DEVTOOLS_BIN}/install:${DEVTOOLS_BIN}/tests:${DEVTOOLS_TOOLBOX}:${TASKFILE_HOME_DIR}:${ASDF_DIR}/bin:${ASDF_SHIMS_DIR}:${PATH}"

# XDG Base Directories: https://wiki.archlinux.org/title/XDG_Base_Directory
ENV XDG_CONFIG_HOME=${DEVTOOLS_CONFIG} \
    XDG_CACHE_HOME=${DEVTOOLS_CACHE} \
    XDG_DATA_HOME=${DEVTOOLS_TOOLBOX} \
    XDG_STATE_HOME=${DEVTOOLS_RUNTIME}

# Set working directory
WORKDIR /workspace

# Copy custom shell scripts and binaries
COPY --chown=vscode:vscode shell/bin/ ${DEVTOOLS_BIN}/
RUN chmod +x ${DEVTOOLS_BIN}/*

# COPY custom shell library
COPY --chown=vscode:vscode shell/lib/ ${DEVTOOLS_LIB}/
RUN find ${DEVTOOLS_LIB} -type f -name "*.sh" -exec chmod +x {} \;

# Copy configuration files for apt and dpkg
COPY shell/etc/dpkg/dpkg.cfg.d/*.conf /etc/dpkg/dpkg.cfg.d/
COPY shell/etc/apt/apt.conf.d/*.conf /etc/apt/apt.conf.d/

COPY --chown=vscode:vscode shell/locks/ ${DEVTOOLS_LOCKS}/

RUN install-apt-base --from-lock

FROM base AS fonts

# Optional Google Fonts installation
ARG INSTALL_GOOGLE_FONTS=false
ARG GOOGLE_FONTS_SHA_COMMIT=2b5bd4077bd9269cdf3114266603372af6c3222d
ARG GOOGLE_FONTS_SHA256=e413e29c18fa727ff4d509280fd432fc0ecb1f6117eb29f2c0a87918d30fe3ad

ENV INSTALL_GOOGLE_FONTS=${INSTALL_GOOGLE_FONTS} \
    GOOGLE_FONTS_SHA_COMMIT=${GOOGLE_FONTS_SHA_COMMIT} \
    GOOGLE_FONTS_SHA256=${GOOGLE_FONTS_SHA256}

FROM base AS imagemagick

# Optional ImageMagick installation
ARG INSTALL_IMAGEMAGICK=false
ARG IMAGEMAGICK_VERSION=7.1.1-47
ARG IMAGEMAGICK_SHA256=53ea43035cf0a1573bebd215932ea6ffeaa7ca1703f4e57d1e849b5bc0bed859
ARG IMAGEMAGICK_MD5=895118664de9d97a10c2d86e222c60c5

ENV INSTALL_IMAGEMAGICK=${INSTALL_IMAGEMAGICK} \
    IMAGEMAGICK_VERSION=${IMAGEMAGICK_VERSION} \
    IMAGEMAGICK_SHA256=${IMAGEMAGICK_SHA256} \
    IMAGEMAGICK_MD5=${IMAGEMAGICK_MD5} \
    IMAGEMAGICK_PREFIX=${DEVTOOLS_TOOLBOX}/imagemagick

ENV PATH="${IMAGEMAGICK_PREFIX}/bin:${PATH}" \
    PKG_CONFIG_PATH="${IMAGEMAGICK_PREFIX}/lib/pkgconfig:${PKG_CONFIG_PATH}" \
    LD_LIBRARY_PATH="${IMAGEMAGICK_PREFIX}/lib:${LD_LIBRARY_PATH}"

RUN if [ "${INSTALL_IMAGEMAGICK}" = "true" ]; then install-imagemagick; fi

# RUN --mount=type=cache,target=/var/cache/fonts,sharing=locked,id=google-fonts \
#     if [ "${INSTALL_GOOGLE_FONTS}" = "true" ]; then \
#     chmod +x /workspace/scripts/install-google-fonts.sh && \
#     bash /workspace/scripts/install-google-fonts.sh "/usr/local/share/fonts/google" && \
#     fc-cache -f -v; \
#     else \
#     echo "📁 Skipping Google Fonts install"; \
#     fi

FROM base AS final

# Copy over compiled ImageMagick (and other devtools) from build stage
COPY --from=imagemagick --chown=vscode:vscode ${DEVTOOLS_HOME} ${DEVTOOLS_HOME}

ENV PATH="${IMAGEMAGICK_PREFIX}/bin:${PATH}" \
    PKG_CONFIG_PATH="${IMAGEMAGICK_PREFIX}/lib/pkgconfig:${PKG_CONFIG_PATH}" \
    LD_LIBRARY_PATH="${IMAGEMAGICK_PREFIX}/lib:${LD_LIBRARY_PATH}"



# COPY --from=fonts /opt/devtools/fonts /opt/devtools/fonts
# RUN fc-cache -f


# Disable the automatic removal of downloaded packages
# RUN rm -f /etc/apt/apt.conf.d/docker-clean

# Fix for update-alternatives: error:
# 'error creating symbolic link '/usr/share/man/man1/rmid.1.gz.dpkg-tmp': No such file or directory'
# See https://github.com/debuerreotype/docker-debian-artifacts/issues/24#issuecomment-360870939
# RUN mkdir --parents /usr/share/man/man1

# RUN apt-config dump > /workspace/_apt-config.dump
# RUN grep -r . /etc/dpkg/dpkg.cfg.d/ > /workspace/_dpkg-config.dump

# Install build tools and common utilities. The package list is
# intentionally explicit so that version locks in apt-packages.lock
# reflect exactly what was installed.
# RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=apt-cache --mount=type=cache,target=/var/lib/apt,sharing=locked,id=apt-lib --mount=type=cache,target=/var/lib/apt,sharing=locked,id=apt-lib apt-get update -qq \
#     && apt-get install --yes --no-install-recommends \
#     RUN apt-get update && apt-get install -y \


# # Optional TeX Live installation
# RUN if [ "${INSTALL_TEXLIVE}" = "true" ]; then \
#     apt-get install --yes --no-install-recommends texlive-full=2023.20240207-1; \
#     else \
#     echo "📁 Skipping texlive-full install"; \
#     fi

# Set texlive directories.
# export TEXLIVE_INSTALL_PREFIX="$USER_SYS_APPS/texlive"
# export TEXMFHOME="$TEXLIVE_INSTALL_PREFIX/texmf"
# export TEXMFVAR="$TEXLIVE_INSTALL_PREFIX/.texlive/texmf-var"
# export TEXMFCONFIG="$TEXLIVE_INSTALL_PREFIX/.texlive/texmf-config"



# # Configure the system locale and timezone
# RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
#     && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
#     && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
#     && locale-gen en_US.UTF-8 \
#     && update-locale LANG=en_US.UTF-8 \
#     && dpkg-reconfigure locales

# # Record the installed versions of apt packages for reference
# RUN dpkg-query -W -f='${Package}=${Version}\n' > apt-packages.lock

# # Install Perl modules needed for Perl Language Server
# RUN cpanm AnyEvent::AIO@1.1 IO::AIO@4.81 Perl::LanguageServer@2.6.2

# # Ensure SYS_UID_MAX and SYS_GID_MAX are set to high values, uncommented or inserted
# RUN sed -i '/^#\?SYS_UID_MAX/ d' /etc/login.defs && echo 'SYS_UID_MAX 99999' >>/etc/login.defs \
#     && sed -i '/^#\?SYS_GID_MAX/ d' /etc/login.defs && echo 'SYS_GID_MAX 99999' >>/etc/login.defs

# # Copy install-google-fonts script
# COPY scripts/install-google-fonts.sh /workspace/scripts/install-google-fonts.sh



# # Record installed font families for reference
# RUN fc-list : family | sort -u > fonts.lock


# # Create the directory in advance so ownership can be adjusted later
# RUN mkdir -p "${DEVTOOLS_HOME}"




# # Helper script that installs asdf plugins and other tooling
# COPY scripts/devtools.sh /workspace/scripts/devtools.sh

# # Copy .tool-versions file
# COPY .tool-versions /workspace/.tool-versions

# # Run the helper script and change ownership so the vscode user can
# # manage the installed tools.
# RUN chmod +x /workspace/scripts/devtools.sh && \
#     bash /workspace/scripts/devtools.sh && \
#     rm -rf /workspace/scripts && \
#     chown --recursive vscode:vscode "${DEVTOOLS_HOME}"

# # Copy and source custom shell aliases
# COPY shell/aliases.sh /etc/profile.d/docker_aliases.sh

# # Ensure correct permissions and sourcing
# RUN chmod 644 /etc/profile.d/docker_aliases.sh && \
#     echo '[ -d /etc/profile.d ] && for f in /etc/profile.d/*.sh; do [ -r "$f" ] && . "$f"; done' \
#     >> /etc/bash.bashrc

# Dockerfile 4
# syntax=docker/dockerfile:1.4

FROM mcr.microsoft.com/devcontainers/base@sha256:cdff177dd5755c0ba2afea60cdc0ab07d933c60d50c6c90dccbcc42b4b4ab76d

# Proxy Environment Variables
# https://docs.docker.com/reference/dockerfile/#predefined-args

# Override the temporary directory if needed
ARG TMPDIR=/tmp

# Locale and timezone settings
ARG LANG=en_US.UTF-8
ARG LANGUAGE=en_US:en
ARG TZ=UTC
ARG LC_ALL=en_US.UTF-8

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    DEBIAN_PRIORITY=critical \
    DEBCONF_NOWARNINGS=yes \
    TERM=xterm-256color \
    APT_LISTCHANGES_FRONTEND=none \
    APT_LISTBUGS_FRONTEND=none \
    TMPDIR=${TMPDIR} \
    LANG=${LANG} \
    LANGUAGE=${LANGUAGE} \
    TZ=${TZ} \
    LC_ALL=${LC_ALL} \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Install system dependencies required for building Python + Python packages
RUN apt-get update -qq && \
    apt-get install --no-install-recommends --yes \
        build-essential \
        ca-certificates \
        ccache \
        clang \
        clang-format \
        clang-tidy \
        cmake \
        curl \
        dnsutils \
        git \
        gnupg \
        htop \
        iputils-ping \
        jq \
        less \
        libblosc-dev \
        libboost-all-dev \
        libbz2-dev \
        libcurl4-openssl-dev \
        libdb-dev \
        libffi-dev \
        libgdbm-dev \
        liblz4-dev \
        liblzma-dev \
        libncursesw5-dev \
        libnss3-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libxi-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libxslt1-dev \
        libzstd-dev \
        llvm \
        net-tools \
        ninja-build \
        pkg-config \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
        ripgrep \
        sudo \
        tar \
        tk-dev \
        unzip \
        uuid-dev \
        vim \
        wget \
        xz-utils \
        zlib1g-dev \
        zsh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /var/tmp/* /tmp/*

RUN apt-get update -qq && apt-get install --no-install-recommends --yes \
    locales \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /var/tmp/* /tmp/*

RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 \
    && dpkg-reconfigure locales

# Ensure SYS_UID_MAX and SYS_GID_MAX are set to high values, uncommented or inserted
RUN sed -i '/^#\?SYS_UID_MAX/ d' /etc/login.defs && echo 'SYS_UID_MAX 99999' >> /etc/login.defs && \
    sed -i '/^#\?SYS_GID_MAX/ d' /etc/login.defs && echo 'SYS_GID_MAX 99999' >> /etc/login.defs

RUN mkdir -p /devtools

# Set working directory
WORKDIR /workspace


ENV NIX_CONF_DIR=/devtools/nix

# Ensure the Nix configuration directory exists
RUN mkdir -p ${NIX_CONF_DIR}

# Copy the Nix configuration file
COPY --chown=vscode:vscode .devcontainer/nix/nix.conf ${NIX_CONF_DIR}/nix.conf


