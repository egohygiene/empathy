#!/usr/bin/env bash
#
# Documentation:
#
# Historically this workstation used
# /usr/libexec/gnome-tweak-tool-lid-inhibitor
# via a GNOME autostart entry.
#
# That approach has been retired in favor of configuring
# logind (HandleLidSwitch=ignore) or GNOME power settings
# directly during provisioning.
#
# This file intentionally serves as documentation until
# workstation provisioning fully manages lid behavior.
