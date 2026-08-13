# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Resolve Mantle's typed profile in Fish without evaluating configuration code.

function __mantle_fish_boolean
    switch "$argv[1]"
        case 1 true yes on
            printf 'true\n'
        case 0 false no off
            printf 'false\n'
        case '*'
            return 64
    end
end

function __mantle_fish_load_profile
    set -l requested_profile "$argv[1]"
    while read -l row
        set -l fields (string split \t -- "$row")
        test "$fields[1]" = schema_version; and continue
        test "$fields[1]" = 1; or continue
        test "$fields[2]" = "$requested_profile"; or continue
        set -gx MANTLE_POLICY_ALIASES_SAFE "$fields[3]"
        set -gx MANTLE_POLICY_ALIASES_NETWORK "$fields[4]"
        set -gx MANTLE_POLICY_ALIASES_SYSTEM "$fields[5]"
        set -gx MANTLE_POLICY_ALIASES_LEGACY "$fields[6]"
        set -gx MANTLE_POLICY_ALIASES_SAFETY "$fields[7]"
        set -gx MANTLE_POLICY_HISTORY "$fields[8]"
        set -gx MANTLE_POLICY_SUPPRESS_UPDATE_CHECKS "$fields[9]"
        set -gx MANTLE_POLICY_EXPERIMENTAL "$fields[10]"
        set -gx MANTLE_POLICY_PRESENTATION "$fields[11]"
        return 0
    end <"$MANTLE_ROOT/config/profiles.tsv"
    printf '[mantle:error] unknown Mantle profile: %s\n' "$requested_profile" >&2
    return 78
end

function __mantle_fish_profile
    set -l config_path
    if set -q MANTLE_CONFIG_FILE
        set config_path "$MANTLE_CONFIG_FILE"
    else if set -q XDG_CONFIG_HOME; and string match --quiet '/*' -- "$XDG_CONFIG_HOME"
        set config_path "$XDG_CONFIG_HOME/mantle/config.conf"
    else if set -q HOME; and string match --quiet '/*' -- "$HOME"
        set config_path "$HOME/.config/mantle/config.conf"
    else
        printf '[mantle:error] HOME must be absolute when no config path is set\n' >&2
        return 78
    end
    string match --quiet '/*' -- "$config_path"; or begin
        printf '[mantle:error] Mantle config path must be absolute: %s\n' "$config_path" >&2
        return 78
    end

    set -l config_profile
    set -l config_aliases_safe
    set -l config_aliases_network
    set -l config_aliases_system
    set -l config_aliases_legacy
    set -l config_aliases_safety
    set -l config_history
    set -l config_suppress_update_checks
    set -l config_experimental
    set -l config_presentation
    set -l declared_schema
    set -l seen_keys
    set -l line_number 0
    set -gx MANTLE_CONFIG_FILE_RESOLVED "$config_path"
    set -gx MANTLE_CONFIG_FILE_STATUS absent

    if test -e "$config_path"
        test -r "$config_path"; or begin
            printf '[mantle:error] configured Mantle config file is unreadable: %s\n' "$config_path" >&2
            return 66
        end
        while read -l config_line
            set line_number (math "$line_number + 1")
            set config_line (string trim --right --chars \r -- "$config_line")
            test -z "$config_line"; and continue
            string match --quiet '#*' -- "$config_line"; and continue
            string match --quiet '*=*' -- "$config_line"; or begin
                printf '[mantle:error] invalid config line %d: expected key=value\n' "$line_number" >&2
                return 78
            end
            set -l pair (string split --max 1 = -- "$config_line")
            set -l key "$pair[1]"
            set -l value "$pair[2]"
            if test -z "$key"; or string match --quiet --regex '[[:space:]]' -- "$key$value"
                printf '[mantle:error] invalid config line %d: whitespace is not permitted around keys or values\n' "$line_number" >&2
                return 78
            end
            contains -- "$key" $seen_keys; and begin
                printf '[mantle:error] duplicate config key on line %d: %s\n' "$line_number" "$key" >&2
                return 78
            end
            set --append seen_keys "$key"

            switch "$key"
                case schema_version
                    set declared_schema "$value"
                case profile
                    string match --quiet --regex '^[a-z0-9][a-z0-9-]*$' -- "$value"; or begin
                        printf '[mantle:error] invalid profile name on line %d: %s\n' "$line_number" "$value" >&2
                        return 78
                    end
                    set config_profile "$value"
                case aliases.safe aliases.network aliases.system aliases.legacy aliases.safety history updates.suppress_checks experimental
                    set value (__mantle_fish_boolean "$value"); or begin
                        printf '[mantle:error] invalid value on line %d for %s\n' "$line_number" "$key" >&2
                        return 78
                    end
                    switch "$key"
                        case aliases.safe; set config_aliases_safe "$value"
                        case aliases.network; set config_aliases_network "$value"
                        case aliases.system; set config_aliases_system "$value"
                        case aliases.legacy; set config_aliases_legacy "$value"
                        case aliases.safety; set config_aliases_safety "$value"
                        case history; set config_history "$value"
                        case updates.suppress_checks; set config_suppress_update_checks "$value"
                        case experimental; set config_experimental "$value"
                    end
                case presentation
                    contains -- "$value" private share-safe ci off; or begin
                        printf '[mantle:error] invalid value on line %d for presentation\n' "$line_number" >&2
                        return 78
                    end
                    set config_presentation "$value"
                case '*'
                    printf '[mantle:error] unknown config key on line %d: %s\n' "$line_number" "$key" >&2
                    return 78
            end
        end <"$config_path"
        test "$declared_schema" = 1; or begin
            printf '[mantle:error] config schema_version must be 1\n' >&2
            return 78
        end
        set -gx MANTLE_CONFIG_FILE_STATUS loaded
    else if set -q MANTLE_CONFIG_FILE
        printf '[mantle:error] configured Mantle config file is unavailable: %s\n' "$config_path" >&2
        return 66
    end

    test -z "$config_profile"; or __mantle_fish_load_profile "$config_profile"; or return
    set -l selected_profile standard
    test -z "$config_profile"; or set selected_profile "$config_profile"
    set -l profile_source default
    test -z "$config_profile"; or set profile_source "config:$config_path"
    set -l inherited_resolved_profile false
    if set -q MANTLE_CONFIG_RESOLVED MANTLE_PROFILE_SOURCE MANTLE_PROFILE_RESOLVED_VALUE; and test "$MANTLE_CONFIG_RESOLVED" = 1
        if test "$MANTLE_PROFILE_SOURCE" = default; or string match --quiet 'config:*' -- "$MANTLE_PROFILE_SOURCE"
            if not set -q MANTLE_PROFILE; or test -z "$MANTLE_PROFILE"; or test "$MANTLE_PROFILE" = "$MANTLE_PROFILE_RESOLVED_VALUE"
                set inherited_resolved_profile true
            end
        end
    end
    if test "$inherited_resolved_profile" = false; and set -q MANTLE_PROFILE; and test -n "$MANTLE_PROFILE"
        set selected_profile "$MANTLE_PROFILE"
        set profile_source environment:MANTLE_PROFILE
    end
    __mantle_fish_load_profile "$selected_profile"; or return
    set -gx MANTLE_PROFILE "$selected_profile"
    set -gx MANTLE_PROFILE_SOURCE "$profile_source"

    test -z "$config_aliases_safe"; or set -gx MANTLE_POLICY_ALIASES_SAFE "$config_aliases_safe"
    test -z "$config_aliases_network"; or set -gx MANTLE_POLICY_ALIASES_NETWORK "$config_aliases_network"
    test -z "$config_aliases_system"; or set -gx MANTLE_POLICY_ALIASES_SYSTEM "$config_aliases_system"
    test -z "$config_aliases_legacy"; or set -gx MANTLE_POLICY_ALIASES_LEGACY "$config_aliases_legacy"
    test -z "$config_aliases_safety"; or set -gx MANTLE_POLICY_ALIASES_SAFETY "$config_aliases_safety"
    test -z "$config_history"; or set -gx MANTLE_POLICY_HISTORY "$config_history"
    test -z "$config_suppress_update_checks"; or set -gx MANTLE_POLICY_SUPPRESS_UPDATE_CHECKS "$config_suppress_update_checks"
    test -z "$config_experimental"; or set -gx MANTLE_POLICY_EXPERIMENTAL "$config_experimental"
    test -z "$config_presentation"; or set -gx MANTLE_POLICY_PRESENTATION "$config_presentation"

    for override in \
        MANTLE_ENABLE_SAFE_ALIASES:ALIASES_SAFE \
        MANTLE_ENABLE_NETWORK_ALIASES:ALIASES_NETWORK \
        MANTLE_ENABLE_SYSTEM_ALIASES:ALIASES_SYSTEM \
        MANTLE_ENABLE_LEGACY_ALIASES:ALIASES_LEGACY \
        MANTLE_ENABLE_SAFETY_ALIASES:ALIASES_SAFETY \
        MANTLE_ENABLE_HISTORY:HISTORY \
        MANTLE_DISABLE_AUTOMATIC_UPDATE_CHECKS:SUPPRESS_UPDATE_CHECKS \
        MANTLE_ENABLE_EXPERIMENTAL:EXPERIMENTAL
        set -l names (string split : -- "$override")
        set -l environment_name "$names[1]"
        set -l policy_name "$names[2]"
        set -q $environment_name; or continue
        set -l normalized (__mantle_fish_boolean $$environment_name); or begin
            printf '[mantle:error] %s must be a boolean value\n' "$environment_name" >&2
            return 78
        end
        set -gx MANTLE_POLICY_$policy_name "$normalized"
    end
    if set -q MANTLE_PRESENTATION_MODE
        contains -- "$MANTLE_PRESENTATION_MODE" private share-safe ci off; or begin
            printf '[mantle:error] invalid MANTLE_PRESENTATION_MODE value: %s\n' "$MANTLE_PRESENTATION_MODE" >&2
            return 78
        end
        set -gx MANTLE_POLICY_PRESENTATION "$MANTLE_PRESENTATION_MODE"
    end
    set -gx MANTLE_CONFIG_SCHEMA_VERSION 1
    set -gx MANTLE_CONFIG_RESOLVED 1
    set -gx MANTLE_PROFILE_RESOLVED_VALUE "$MANTLE_PROFILE"
    return 0
end

__mantle_fish_profile; set -l __mantle_profile_status $status
functions --erase __mantle_fish_profile __mantle_fish_load_profile __mantle_fish_boolean
test $__mantle_profile_status -eq 0
