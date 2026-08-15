# beacon

🔭 A local-first project bootstrapper and template library for reproducible
research and technical documents.

`beacon` is currently incubated inside Empathy as an independently extractable
holon. This first vertical slice establishes the reusable template contract and
imports the proven research-paper presentation layer from Renderflow without
coupling Beacon to Renderflow's runtime.

## Boundary

`beacon/` owns reusable project-template contracts, template packages,
validation rules, and eventually the Beacon CLI and local authoring experience.
A generated project owns its manuscript, bibliography, figures, data, research
notes, build configuration, and publication history.

Renderflow remains a rendering engine and reference implementation. Beacon owns
how a project template is described, discovered, validated, and instantiated.

## Current vertical slice

This foundation provides:

- a versioned, renderer-aware template manifest contract;
- a canonical `research-paper` package derived from Renderflow's research
  templates;
- explicit provenance and extraction notes;
- deterministic, dependency-free validation using Python's standard library;
- a minimal example research paper fixture.

The Rust CLI, project initialization, Git/GitHub integration, local LLM
assistance, graphical authoring interface, and root Taskfile integration
intentionally remain future work.

## Layout

```text
beacon/
├── ARCHITECTURE.md
├── EXTRACTION.md
├── PROVENANCE.md
├── README.md
├── contracts/
│   └── template-manifest.schema.json
├── scripts/
│   └── validate_templates.py
├── templates/
│   └── research-paper/
│       ├── README.md
│       ├── beacon-template.toml
│       ├── template.html
│       ├── template.tex
│       └── example/
│           └── paper.md
└── tests/
    └── test_templates.py
```

## Validation

From the Empathy repository root:

```bash
python3 beacon/scripts/validate_templates.py --repository-root "."
python3 -m unittest discover --start-directory beacon/tests --pattern "test_*.py" --verbose
```

## Design principle

Beacon templates are packages, not loose files. Every template package must be
self-describing, versioned, renderer-aware, independently validatable, and safe
to copy into a generated project without hidden repository-relative state.
