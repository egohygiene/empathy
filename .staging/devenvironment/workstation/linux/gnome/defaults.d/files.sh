#!/usr/bin/env bash
#
# Apply GNOME file chooser preferences.

set -euo pipefail

# Always show hidden files in GTK file chooser dialogs.
gsettings set org.gtk.Settings.FileChooser show-hidden true
