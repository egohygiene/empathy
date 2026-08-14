# identity

🎨 A spec-driven visual identity compiler for repositories, products, and
organizations.

`identity` is currently incubated inside Empathy as an independently
extractable Rust holon. It separates human-approved creative direction and
canonical source artwork from deterministic crops, sizes, formats, metadata,
and platform projections.

## Boundary

`identity/` owns the reusable CLI, contracts, profiles, and generation rules.
A consumer repository owns its `.identity/` directory and the generated
`assets/identity/` package. AI systems, designers, and image tools may all
author candidates; none of them becomes a required runtime dependency.

The first vertical slice provides:

- a versioned `.identity/identity.toml` project contract;
- versioned `core`, `web`, `pwa`, `github`, `docs`, `social`, `tokens`, and
  `metadata` target profiles;
- deterministic specification validation and target planning;
- a self-contained Markdown handoff for ChatGPT or another creative tool;
- an explicit candidate-source manifest and human approval boundary.

Rasterization, candidate import, asset generation, visual validation, and
Renderflow adapters intentionally remain future work.

## Commands

Run from a consumer repository root:

```bash
cargo run \
  --manifest-path "identity/Cargo.toml" \
  -- validate \
  --repository-root "."

cargo run \
  --manifest-path "identity/Cargo.toml" \
  -- plan \
  --repository-root "." \
  --format "markdown"

cargo run \
  --manifest-path "identity/Cargo.toml" \
  -- handoff \
  --repository-root "." \
  --output-directory ".cache/identity/handoff"
```

The handoff directory contains:

- `identity-handoff.md` — ready to attach or paste into a contextual AI
  conversation;
- `candidate-manifest.template.json` — the required source-package response
  contract;
- `handoff-manifest.json` — deterministic input provenance.

## Source and output lifecycle

```text
.identity/identity.toml + .identity/brief.md + project context
                              |
                              v
                     identity handoff
                              |
                              v
                  human/tool source candidates
                              |
                              v
                review and approval (future import)
                              |
                              v
               deterministic generation and checks
                              |
                              v
                       assets/identity/
```

Generated assets never become a substitute for the approved source pack.
