# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

function mantle_public_ip --description 'Print the current public IP address'
    if not set -q MANTLE_POLICY_ALIASES_NETWORK; or test "$MANTLE_POLICY_ALIASES_NETWORK" != true
        printf '[mantle:error] network helpers are disabled by the active Mantle profile\n' >&2
        return 77
    end
    if command -q dig
        command dig +short myip.opendns.com @resolver1.opendns.com
    else if command -q curl
        command curl --fail --silent --show-error https://api.ipify.org
        printf '\n'
    else
        printf '[mantle:error] dig or curl is required to resolve the public IP address\n' >&2
        return 69
    end
end
