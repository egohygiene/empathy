# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

function mantle_local_ip_addresses --description 'Print non-loopback local IP addresses'
    if not set -q MANTLE_POLICY_ALIASES_NETWORK; or test "$MANTLE_POLICY_ALIASES_NETWORK" != true
        printf '[mantle:error] network helpers are disabled by the active Mantle profile\n' >&2
        return 77
    end
    if command -q hostname; and command hostname -I >/dev/null 2>&1
        command hostname -I | string split ' ' | string match --invert --regex '^$'
    else if command -q ip
        command ip -o -4 address show scope global | awk '{print $4}' | cut -d/ -f1
    else if command -q ifconfig
        command ifconfig | awk '/inet / && $2 != "127.0.0.1" {print $2}'
    else
        printf '[mantle:error] no supported local-address command is available\n' >&2
        return 69
    end
end
