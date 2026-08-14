# Extraction Contract

`identity` is physically colocated with Empathy while its contracts mature,
but it must remain independently extractable.

## Required invariants

- Reusable source stays beneath `identity/`.
- Reusable source does not import files from its parent repository.
- Consumer intent and approved artwork stay beneath `.identity/`.
- Generated consumer assets stay beneath `assets/identity/`.
- Public interfaces are versioned contracts or documented commands.
- Unit tests stay beneath `identity/`; Empathy integration tests may live in
  the repository-root test surface.
- Third-party code, artwork, fonts, and references require recorded provenance
  and license review.

Extraction is intentionally deferred until the incubation work is mature.
