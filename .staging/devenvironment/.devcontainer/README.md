# Devcontainer

Resources:

- Dev Container Spec: <https://containers.dev/>
- Schema Reference: <https://containers.dev/implementors/json_reference/>
- Features: <https://containers.dev/features>
- Templates: <https://containers.dev/templates>

// --------------------------------------------------------------
// Init Process
// --------------------------------------------------------------
// When true, runs an init process (tini) as PID 1 inside the
// container. Benefits:
// - Proper signal handling (SIGTERM, SIGINT)
// - Zombie process reaping
// - Graceful shutdown
//
// Recommendation: true for dev containers (default behavior)
//
