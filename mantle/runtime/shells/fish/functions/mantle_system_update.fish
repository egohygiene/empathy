# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

function mantle_system_update --description 'Update supported operating-system package managers'
    if not set -q MANTLE_POLICY_ALIASES_SYSTEM; or test "$MANTLE_POLICY_ALIASES_SYSTEM" != true
        printf '[mantle:error] system helpers are disabled by the active Mantle profile\n' >&2
        return 77
    end
    set -l package_manager_found 0
    if test (uname -s) = Darwin; and command -q brew
        set package_manager_found 1
        command brew update; and command brew upgrade; or return $status
    end
    if command -q apt-get
        set package_manager_found 1
        command sudo apt-get update
        and command sudo apt-get --yes upgrade
        and command sudo apt-get --yes autoremove
        or return $status
    end
    if command -q snap
        set package_manager_found 1
        command sudo snap refresh; or return $status
    end
    if command -q aptitude
        set package_manager_found 1
        command sudo aptitude --yes safe-upgrade; or return $status
    end
    if test $package_manager_found -eq 0
        printf '[mantle:error] no supported system package manager is available\n' >&2
        return 69
    end
end
