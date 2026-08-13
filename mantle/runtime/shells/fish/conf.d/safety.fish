# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Familiar command replacements enabled only by aliases.safety.

function __mantle_fish_safety_abbreviations
    status is-interactive; or return 0
    abbr --add -- cp 'command cp -iv'
    abbr --add -- mv 'command mv -iv'
    abbr --add -- rm 'command rm -i'
    return 0
end
__mantle_fish_safety_abbreviations; set -l __mantle_s $status
functions --erase __mantle_fish_safety_abbreviations
test $__mantle_s -eq 0
