# Fish runtime

Fish is a first-class, native Mantle adapter. It does not source Bash/POSIX
files because Fish has a different language and runtime model.

Add this to `~/.config/fish/config.fish`:

```fish
set -gx MANTLE_ROOT "/absolute/path/to/mantle"
source "$MANTLE_ROOT/runtime/shells/fish/runtime.fish"
```

The entrypoint resolves the same versioned profile configuration used by Bash,
Zsh, and `mantle config`, then loads native environment, privacy, update, and
enabled safe/network/system/safety/legacy capability fragments in deterministic
order. Startup is quiet and idempotent. Existing user-selected values are
preserved unless a Mantle policy explicitly documents otherwise.
