# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Operating-system mutation abbreviations enabled by aliases.system.

function __mantle_fish_system_abbreviations
    status is-interactive; or return 0
    abbr --add -- system-update mantle_system_update
    return 0
end
__mantle_fish_system_abbreviations; set -l __mantle_s $status
functions --erase __mantle_fish_system_abbreviations
test $__mantle_s -eq 0
