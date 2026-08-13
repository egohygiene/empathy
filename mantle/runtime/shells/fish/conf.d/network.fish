# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Network inspection abbreviations enabled by aliases.network.

function __mantle_fish_network_abbreviations
    status is-interactive; or return 0
    abbr --add -- ports mantle_list_ports
    abbr --add -- ipaddr mantle_local_ip_addresses
    abbr --add -- public-ip mantle_public_ip
    return 0
end
__mantle_fish_network_abbreviations; set -l __mantle_s $status
functions --erase __mantle_fish_network_abbreviations
test $__mantle_s -eq 0
