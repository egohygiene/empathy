# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Deliberate historical collisions enabled only by aliases.legacy.

function __mantle_fish_legacy_abbreviations
    status is-interactive; or return 0
    abbr --add -- ip mantle_public_ip
    abbr --add -- update mantle_system_update
    abbr --add -- rmf 'command rm -rf'
    abbr --add -- clone 'command git clone'
    return 0
end
__mantle_fish_legacy_abbreviations; set -l __mantle_s $status
functions --erase __mantle_fish_legacy_abbreviations
test $__mantle_s -eq 0
