#!/usr/bin/env bash
#
# Apply GNOME power management preferences.

set -euo pipefail

# Never blank the screen automatically.
gsettings set org.gnome.desktop.session idle-delay 0

# Never suspend while on AC power.
gsettings set \
    org.gnome.settings-daemon.plugins.power \
    sleep-inactive-ac-timeout \
    0

# Never suspend while on battery.
gsettings set \
    org.gnome.settings-daemon.plugins.power \
    sleep-inactive-battery-timeout \
    0
