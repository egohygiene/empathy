# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

function __mantle_fish_record_migration_warning --argument-names variable_name
    if test -z "$variable_name"
        return 64
    end

    if set -q MANTLE_XDG_MIGRATION_WARNINGS
        contains -- "$variable_name" (string split : -- "$MANTLE_XDG_MIGRATION_WARNINGS"); and return 0
        set -gx MANTLE_XDG_MIGRATION_WARNINGS "$MANTLE_XDG_MIGRATION_WARNINGS:$variable_name"
    else
        set -gx MANTLE_XDG_MIGRATION_WARNINGS "$variable_name"
    end

    if set -q MANTLE_DEBUG; and test "$MANTLE_DEBUG" = 1
        printf '[mantle:debug] preserving legacy location for %s; an XDG migration is available\n' "$variable_name" >&2
    end
end

function __mantle_fish_set_default --argument-names variable_name variable_value
    set -q $variable_name; or set -gx $variable_name "$variable_value"
end

function __mantle_fish_set_xdg --argument-names variable_name xdg_path legacy_path
    set -q $variable_name; and return 0

    if test -n "$legacy_path"; and test -e "$legacy_path"; and not test -e "$xdg_path"
        __mantle_fish_record_migration_warning "$variable_name"
        return 0
    end

    set -gx $variable_name "$xdg_path"
end

function __mantle_fish_set_xdg_if_file --argument-names variable_name xdg_path legacy_path
    set -q $variable_name; and return 0

    if test -f "$xdg_path"
        set -gx $variable_name "$xdg_path"
    else if test -n "$legacy_path"; and test -f "$legacy_path"
        __mantle_fish_record_migration_warning "$variable_name"
    end
end

function __mantle_fish_set_xdg_private_directory --argument-names variable_name xdg_path legacy_path
    set -q $variable_name; and return 0

    if test -n "$legacy_path"; and test -e "$legacy_path"; and not test -e "$xdg_path"
        __mantle_fish_record_migration_warning "$variable_name"
        return 0
    end

    if not test -d "$xdg_path"
        if set -q MANTLE_CREATE_XDG_DIRECTORIES; and test "$MANTLE_CREATE_XDG_DIRECTORIES" != 1
            return 0
        end
        command mkdir -p -- "$xdg_path"; or return 1
        command chmod 700 "$xdg_path"; or return 1
    end

    set -gx $variable_name "$xdg_path"
end

# Wrapped in a function so that `return` works in Fish < 3.4 (for example,
# Ubuntu 22.04 ships Fish 3.3.1, which rejects top-level return statements).
function __mantle_fish_environment
    if not set -q HOME; or test -z "$HOME"
        printf '[mantle:error] Fish environment requires HOME\n' >&2
        return 1
    end

    set -q XDG_CONFIG_HOME; or set -gx XDG_CONFIG_HOME "$HOME/.config"
    set -q XDG_CACHE_HOME; or set -gx XDG_CACHE_HOME "$HOME/.cache"
    set -q XDG_DATA_HOME; or set -gx XDG_DATA_HOME "$HOME/.local/share"
    set -q XDG_STATE_HOME; or set -gx XDG_STATE_HOME "$HOME/.local/state"
    set -q XDG_BIN_HOME; or set -gx XDG_BIN_HOME "$HOME/.local/bin"
    set -q XDG_CONFIG_DIRS; or set -gx XDG_CONFIG_DIRS /etc/xdg
    set -q XDG_DATA_DIRS; or set -gx XDG_DATA_DIRS /usr/local/share /usr/share
    set -q LANG; or set -gx LANG en_US.UTF-8

    if not set -q EDITOR
        if command -q nvim
            set -gx EDITOR nvim
        else if command -q vim
            set -gx EDITOR vim
        else
            set -gx EDITOR vi
        end
    end
    set -q VISUAL; or set -gx VISUAL "$EDITOR"

    if not set -q MANTLE_CREATE_XDG_DIRECTORIES; or test "$MANTLE_CREATE_XDG_DIRECTORIES" = 1
        command mkdir -p -- "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME" "$XDG_BIN_HOME"; or return 1
    end

    # Version managers and language runtimes. Existing legacy roots remain
    # active until the user explicitly migrates them.
    __mantle_fish_set_xdg ASDF_DATA_DIR "$XDG_DATA_HOME/asdf" "$HOME/.asdf"
    __mantle_fish_set_xdg PYENV_ROOT "$XDG_DATA_HOME/pyenv" "$HOME/.pyenv"
    __mantle_fish_set_xdg RBENV_ROOT "$XDG_DATA_HOME/rbenv" "$HOME/.rbenv"
    __mantle_fish_set_xdg NVM_DIR "$XDG_DATA_HOME/nvm" "$HOME/.nvm"
    __mantle_fish_set_xdg VOLTA_HOME "$XDG_DATA_HOME/volta" "$HOME/.volta"
    __mantle_fish_set_xdg CARGO_HOME "$XDG_DATA_HOME/cargo" "$HOME/.cargo"
    __mantle_fish_set_xdg RUSTUP_HOME "$XDG_DATA_HOME/rustup" "$HOME/.rustup"
    __mantle_fish_set_xdg GOPATH "$XDG_DATA_HOME/go" "$HOME/go"
    __mantle_fish_set_xdg SDKMAN_DIR "$XDG_DATA_HOME/sdkman" "$HOME/.sdkman"
    __mantle_fish_set_default PNPM_HOME "$XDG_DATA_HOME/pnpm"
    __mantle_fish_set_default PIPX_HOME "$XDG_DATA_HOME/pipx"
    __mantle_fish_set_default PIPX_BIN_DIR "$XDG_DATA_HOME/pipx/bin"

    # Audited developer-tool locations.
    __mantle_fish_set_xdg IPYTHONDIR "$XDG_CONFIG_HOME/ipython" "$HOME/.ipython"
    __mantle_fish_set_xdg JUPYTER_CONFIG_DIR "$XDG_CONFIG_HOME/jupyter" "$HOME/.jupyter"
    __mantle_fish_set_xdg PYTHON_HISTORY "$XDG_STATE_HOME/python/history" "$HOME/.python_history"
    __mantle_fish_set_xdg GEM_HOME "$XDG_DATA_HOME/gem" "$HOME/.gem"
    __mantle_fish_set_xdg GRADLE_USER_HOME "$XDG_DATA_HOME/gradle" "$HOME/.gradle"
    __mantle_fish_set_xdg KERAS_HOME "$XDG_DATA_HOME/keras" "$HOME/.keras"
    __mantle_fish_set_xdg MPLCONFIGDIR "$XDG_CONFIG_HOME/matplotlib" "$HOME/.matplotlib"
    __mantle_fish_set_xdg NLTK_DATA "$XDG_DATA_HOME/nltk" "$HOME/nltk_data"
    __mantle_fish_set_xdg GRIPHOME "$XDG_CONFIG_HOME/grip" "$HOME/.grip"
    __mantle_fish_set_xdg FVM_CACHE_PATH "$XDG_DATA_HOME/fvm" "$HOME/fvm"
    __mantle_fish_set_default DOTNET_CLI_HOME "$XDG_DATA_HOME/dotnet"
    __mantle_fish_set_default DART_DATA_HOME "$XDG_DATA_HOME/dart"

    # Cloud and infrastructure tooling.
    __mantle_fish_set_xdg DOCKER_CONFIG "$XDG_CONFIG_HOME/docker" "$HOME/.docker"
    __mantle_fish_set_xdg KUBECONFIG "$XDG_CONFIG_HOME/kube/config" "$HOME/.kube/config"
    __mantle_fish_set_xdg MINIKUBE_HOME "$XDG_DATA_HOME/minikube" "$HOME/.minikube"
    __mantle_fish_set_xdg ANSIBLE_HOME "$XDG_DATA_HOME/ansible" "$HOME/.ansible"
    __mantle_fish_set_xdg PULUMI_HOME "$XDG_DATA_HOME/pulumi" "$HOME/.pulumi"

    # Android SDK installation paths are intentionally untouched. These
    # variables move Android's user state and emulator data only.
    __mantle_fish_set_xdg ANDROID_USER_HOME "$XDG_DATA_HOME/android" "$HOME/.android"
    __mantle_fish_set_xdg ANDROID_EMULATOR_HOME "$XDG_DATA_HOME/android/emulator" "$HOME/.android"
    __mantle_fish_set_xdg ANDROID_AVD_HOME "$XDG_DATA_HOME/android/avd" "$HOME/.android/avd"
    __mantle_fish_set_xdg ANALYZER_STATE_LOCATION_OVERRIDE "$XDG_STATE_HOME/dart/analysis-server" "$HOME/.dartServer"

    # Agent runtimes with documented location overrides.
    __mantle_fish_set_xdg_private_directory CODEX_HOME "$XDG_DATA_HOME/codex" "$HOME/.codex"; or return 1
    __mantle_fish_set_xdg CLAUDE_CONFIG_DIR "$XDG_DATA_HOME/claude" "$HOME/.claude"
    __mantle_fish_set_xdg COPILOT_HOME "$XDG_DATA_HOME/copilot" "$HOME/.copilot"
    __mantle_fish_set_xdg CLINE_DATA_DIR "$XDG_DATA_HOME/cline" "$HOME/.cline/data"
    __mantle_fish_set_xdg OH_PERSISTENCE_DIR "$XDG_STATE_HOME/openhands" "$HOME/.openhands"
    __mantle_fish_set_xdg OPENCLAW_STATE_DIR "$XDG_STATE_HOME/openclaw" "$HOME/.openclaw"
    __mantle_fish_set_xdg LOGFIRE_CREDENTIALS_DIR "$XDG_CONFIG_HOME/logfire" "$HOME/.logfire"

    # Cache and temporary-data locations.
    __mantle_fish_set_xdg PUB_CACHE "$XDG_CACHE_HOME/dart-pub" "$HOME/.pub-cache"
    __mantle_fish_set_xdg GEM_SPEC_CACHE "$XDG_CACHE_HOME/gem/specs" "$HOME/.gem/specs"
    __mantle_fish_set_xdg NPM_CONFIG_CACHE "$XDG_CACHE_HOME/npm" "$HOME/.npm"
    __mantle_fish_set_xdg KUBECACHEDIR "$XDG_CACHE_HOME/kubernetes" "$HOME/.kube/cache"
    __mantle_fish_set_xdg TF_PLUGIN_CACHE_DIR "$XDG_CACHE_HOME/terraform/plugin-cache" "$HOME/.terraform.d/plugin-cache"
    __mantle_fish_set_default DOTNET_BUNDLE_EXTRACT_BASE_DIR "$XDG_CACHE_HOME/dotnet/bundle-extract"
    __mantle_fish_set_default TASK_TEMP_DIR "$XDG_CACHE_HOME/task"

    # Config-file overrides remain unset until the XDG file exists.
    __mantle_fish_set_xdg_if_file NPM_CONFIG_USERCONFIG "$XDG_CONFIG_HOME/npm/npmrc" "$HOME/.npmrc"
    __mantle_fish_set_xdg_if_file BOTO_CONFIG "$XDG_CONFIG_HOME/boto/config" "$HOME/.boto"
    __mantle_fish_set_xdg_if_file COOKIECUTTER_CONFIG "$XDG_CONFIG_HOME/cookiecutter/config.yaml" "$HOME/.cookiecutterrc"
    __mantle_fish_set_xdg_if_file OPENCLAW_CONFIG_PATH "$XDG_CONFIG_HOME/openclaw/openclaw.json" "$HOME/.openclaw/openclaw.json"

    # Resolve PATH candidates to their still-active legacy roots when a
    # migration warning deliberately left the corresponding variable unset.
    set -l asdf_root "$XDG_DATA_HOME/asdf"
    set -q ASDF_DATA_DIR; and set asdf_root "$ASDF_DATA_DIR"
    not set -q ASDF_DATA_DIR; and test -d "$HOME/.asdf"; and set asdf_root "$HOME/.asdf"
    set -l pyenv_root "$XDG_DATA_HOME/pyenv"
    set -q PYENV_ROOT; and set pyenv_root "$PYENV_ROOT"
    not set -q PYENV_ROOT; and test -d "$HOME/.pyenv"; and set pyenv_root "$HOME/.pyenv"
    set -l volta_root "$XDG_DATA_HOME/volta"
    set -q VOLTA_HOME; and set volta_root "$VOLTA_HOME"
    not set -q VOLTA_HOME; and test -d "$HOME/.volta"; and set volta_root "$HOME/.volta"
    set -l cargo_root "$XDG_DATA_HOME/cargo"
    set -q CARGO_HOME; and set cargo_root "$CARGO_HOME"
    not set -q CARGO_HOME; and test -d "$HOME/.cargo"; and set cargo_root "$HOME/.cargo"
    set -l go_root "$XDG_DATA_HOME/go"
    set -q GOPATH; and set go_root "$GOPATH"
    not set -q GOPATH; and test -d "$HOME/go"; and set go_root "$HOME/go"

    for candidate in "$asdf_root/bin" "$asdf_root/shims" "$pyenv_root/bin" "$volta_root/bin" "$PIPX_BIN_DIR" "$go_root/bin" "$cargo_root/bin" "$PNPM_HOME" "$XDG_BIN_HOME" "$MANTLE_ROOT/bin"
        test -d "$candidate"; and fish_add_path --global --move --prepend "$candidate"
    end
    return 0
end

__mantle_fish_environment
set -l __mantle_s $status
functions --erase __mantle_fish_environment __mantle_fish_record_migration_warning __mantle_fish_set_default __mantle_fish_set_xdg __mantle_fish_set_xdg_if_file __mantle_fish_set_xdg_private_directory
test $__mantle_s -eq 0
