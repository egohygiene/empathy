# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
function ls --description "List directory contents with platform-aware color"
    switch (uname -s)
        case Darwin FreeBSD
            command ls -G $argv
        case '*'
            command ls --color=auto $argv
    end
end
