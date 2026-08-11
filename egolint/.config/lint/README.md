# Linter configuration catalog

Each directory owns the native configuration for one language, file format, or
quality dimension. `egolint/.mega-linter.yml` maps MegaLinter descriptor keys to
these files explicitly, while `egolint/tasks/lint.yml` exposes focused commands
for local use.

Keep rules tool-native whenever possible. MegaLinter should orchestrate a
linter, not redefine its policy through opaque command-line overrides.

Configuration changes should include at least one matching fixture or a
documented reason why an executable fixture is impractical.
