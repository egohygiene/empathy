# Antidote research workspace

> **Status:** provisional project codename and research bootstrap.

This workspace is the first real project used to dogfood Beacon's
`research-paper` contract inside Empathy. `antidote` is intentionally a
provisional codename; the final project and repository name may change after the
literature and novelty scan.

## Central research question

> Can an adaptive system learn an individual mapping from interpretable sonic
> language → generated acoustic structure → affective response, and use that
> mapping to better target future state transitions?

The project began from an N-of-1 creative observation: a highly intentional
generative-audio process produced a strong subjective experience of catharsis.
That observation is treated as **hypothesis-generating**, not as evidence of
clinical efficacy or a neurological mechanism.

## Research boundary

The strongest current contribution hypothesis is the longitudinal relationship
between:

```text
interpretable semantic controls
        ↓
measured acoustic realization
        ↓
individual response
```

The work should remain imaginative about generation and conservative about
interpretation. Sources, hypotheses, observations, interpretations, and final
claims must remain distinguishable throughout the project.

## Workspace

```text
research/antidote/
├── beacon-project.toml
├── paper.md
├── references.bib
├── templates/
│   ├── template.tex
│   └── template.html
├── figures/
├── data/
└── research/
    ├── bootstrap/
    ├── notes/
    └── sources/
```

The files under `research/bootstrap/` preserve the distilled research snapshot
captured before implementation began. They are working research artifacts, not
claims that belong automatically in the manuscript.

## Immediate next phase

After this bootstrap lands, the next phase is a deep literature and novelty scan
across five converging areas:

1. music psychology and affect regulation;
2. generative AI and controllable audio;
3. neuroscience and psychophysiology;
4. psychedelic / ketamine music research;
5. phenomenology, semantics, embodiment, and human meaning systems.

That scan should produce a verified bibliography, literature matrix, novelty
map, and a refined statement of contribution **before** the experimental
architecture is frozen.
