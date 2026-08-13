# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

function mantle_list_ports --description 'List listening TCP and UDP ports'
    if not set -q MANTLE_POLICY_ALIASES_NETWORK; or test "$MANTLE_POLICY_ALIASES_NETWORK" != true
        printf '[mantle:error] network helpers are disabled by the active Mantle profile\n' >&2
        return 77
    end
    if command -q ss
        command ss --listening --numeric --tcp --udp
    else if command -q lsof
        command lsof -nP -iTCP -sTCP:LISTEN -iUDP
    else if command -q netstat
        command netstat -an
    else
        printf '[mantle:error] no supported port-listing command is available\n' >&2
        return 69
    end
end
