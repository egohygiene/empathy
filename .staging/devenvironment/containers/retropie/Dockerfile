######################################################################
# RetroPie – containerized retro-gaming emulation platform
# https://retropie.org.uk/
#
# This image installs RetroPie and EmulationStation on a Debian base.
# It is intentionally exploratory; architecture will evolve as the
# broader homelab Dockerfile matures.
#
# Build
# -----
#   docker build -t retropie .
#
# Run (minimal — display required on host)
# -----------------------------------------
#   docker run --rm \
#     -e DISPLAY=$DISPLAY \
#     -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
#     --device /dev/dri \
#     --device /dev/input \
#     -v retropie_roms:/home/pi/RetroPie/roms \
#     retropie emulationstation
#
# See docs/retropie-runtime.md for full runtime flag documentation.
######################################################################
# hadolint global ignore=DL3008
FROM debian:bookworm-slim

# ── Build arguments ─────────────────────────────────────────────────
# RETROPIE_USER: unprivileged user that owns the RetroPie home tree.
ARG RETROPIE_USER=pi
ARG RETROPIE_UID=1000
ARG RETROPIE_GID=1000

# ── Non-interactive apt environment ─────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    TZ=UTC

# ── System locale ────────────────────────────────────────────────────
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

SHELL ["/bin/bash", "-o", "errexit", "-o", "nounset", "-o", "pipefail", "-c"]

# ── 1. Core system dependencies ──────────────────────────────────────
# Install locale tooling, ca-certificates, and the packages required
# to bootstrap the RetroPie-Setup script on Debian.
# Reference: https://retropie.org.uk/docs/Debian/
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        locales \
        lsb-release \
        sudo \
        tzdata \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# ── 2. RetroPie build dependencies ───────────────────────────────────
# These packages are needed by RetroPie-Setup (autotools, SDL2, etc.).
# The list mirrors the Debian prerequisites documented at
# https://retropie.org.uk/docs/Debian/
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        autoconf \
        automake \
        build-essential \
        cmake \
        dialog \
        ffmpeg \
        gettext \
        libasound2-dev \
        libboost-filesystem-dev \
        libboost-locale-dev \
        libboost-system-dev \
        libcurl4-openssl-dev \
        libdrm-dev \
        libevdev-dev \
        libfreeimage-dev \
        libfreetype6-dev \
        libgbm-dev \
        libgles2-mesa-dev \
        libjpeg-dev \
        libpng-dev \
        libsdl2-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libssl-dev \
        libudev-dev \
        libvlc-dev \
        libxkbcommon-dev \
        libyaml-dev \
        pkg-config \
        python3 \
        python3-pip \
        rapidjson-dev \
        udev \
        xmlstarlet \
    && rm -rf /var/lib/apt/lists/*

# ── 3. Display / audio runtime ───────────────────────────────────────
# X11 client libraries, Mesa, and ALSA so EmulationStation can render
# and produce sound when a display is forwarded from the host.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        alsa-utils \
        libgl1-mesa-dri \
        libglu1-mesa \
        libpulse0 \
        libx11-6 \
        libxext6 \
        libxrandr2 \
        libxrender1 \
        pulseaudio \
        x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# ── 4. Create an unprivileged user ───────────────────────────────────
# RetroPie-Setup expects a non-root user environment.  The "pi" user
# mirrors the Raspberry Pi OS convention so that community scripts
# resolve paths correctly by default.
RUN groupadd --gid "${RETROPIE_GID}" "${RETROPIE_USER}" \
    && useradd \
        --uid "${RETROPIE_UID}" \
        --gid "${RETROPIE_GID}" \
        --shell /bin/bash \
        --create-home \
        "${RETROPIE_USER}" \
    && echo "${RETROPIE_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/retropie \
    && chmod 0440 /etc/sudoers.d/retropie

# ── 5. Clone RetroPie-Setup ──────────────────────────────────────────
# Clone the upstream setup script into the conventional location under
# the pi home directory.  The depth=1 flag minimizes image size.
ARG RETROPIE_SETUP_REF=master
RUN git clone --depth 1 --branch "${RETROPIE_SETUP_REF}" \
        https://github.com/RetroPie/RetroPie-Setup.git \
        /home/${RETROPIE_USER}/RetroPie-Setup \
    && chown -R "${RETROPIE_USER}:${RETROPIE_USER}" \
        /home/${RETROPIE_USER}/RetroPie-Setup

# ── 6. ROM directory structure ───────────────────────────────────────
# Create the expected RetroPie directory hierarchy.  ROM paths are
# intentionally left empty — populate them at runtime via volume mounts
# so no ROMs are baked into the image.
RUN install -d -o "${RETROPIE_USER}" -g "${RETROPIE_USER}" -m 0755 \
        /home/${RETROPIE_USER}/RetroPie/roms \
        /home/${RETROPIE_USER}/RetroPie/BIOS \
        /home/${RETROPIE_USER}/RetroPie/splashscreens \
        /home/${RETROPIE_USER}/.emulationstation

# ── 7. EmulationStation basic configuration ──────────────────────────
# Write a minimal es_systems.cfg so EmulationStation can start without
# crashing on first launch.  The full list of systems is populated by
# RetroPie-Setup modules after ROMs are in place.
COPY --chown=${RETROPIE_USER}:${RETROPIE_USER} es_systems.cfg \
    /home/${RETROPIE_USER}/.emulationstation/es_systems.cfg

# ── Switch to the unprivileged user ─────────────────────────────────
USER ${RETROPIE_USER}
WORKDIR /home/${RETROPIE_USER}

# ── Volumes ──────────────────────────────────────────────────────────
# Declare mountable paths for ROM storage and BIOS files.
# Populate these via -v / --mount flags at runtime.
VOLUME ["/home/pi/RetroPie/roms", "/home/pi/RetroPie/BIOS"]

# ── Default command ──────────────────────────────────────────────────
# Attempt to launch EmulationStation.  The container will exit if no
# display is available; bind-mount the X11 socket at runtime.
CMD ["emulationstation"]
