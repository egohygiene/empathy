#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# .bash_logout
#
# Executed when the final login shell exits.
#
# Common uses:
#   - Clear console history
#   - Cleanup temporary files
#   - Session teardown
#
# ------------------------------------------------------------------------------

# Clear Linux virtual console on logout.
if [ "${SHLVL}" = "1" ]; then
    if [ -x "/usr/bin/clear_console" ]; then
        /usr/bin/clear_console -q
    fi
fi
