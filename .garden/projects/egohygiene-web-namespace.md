---
schema: mindgarden.note/v0
id: empathy-egohygiene-web-namespace
title: Ego Hygiene web namespace and holon surfaces
kind: project
status: active
reviewed: true
confidence: medium
visibility: public
owners:
  - egohygiene
created: 2026-08-15
updated: 2026-08-15
sources: []
related:
  - empathy-repository-intelligence-dashboard
supersedes: []
tags:
  - architecture
  - github-pages
  - holon
  - platform
  - web
---

# Ego Hygiene web namespace and holon surfaces

## Vision

`egohygiene.io` should become the canonical web namespace for the Ego Hygiene
ecosystem. The namespace should clearly distinguish public-facing products from
the engineering and knowledge surfaces owned by individual repositories.

The root domain is the public landing portal:

```text
egohygiene.io/
```

Public products live at intentional first-class paths, for example:

```text
egohygiene.io/hygiene/
egohygiene.io/store/
```

External or independently hosted services may use subdomains when that boundary
is meaningful. The existing Medium publication is an example:

```text
articles.egohygiene.io/
```

## The holon namespace

Every Ego Hygiene repository should be able to own a web surface beneath the
shared `/holon/` namespace:

```text
egohygiene.io/holon/<repository>/
```

A holon is the web-facing representation of an independently owned repository or
component within the wider Ego Hygiene system. The repository remains the
ownership boundary for its source, documentation, metadata, intelligence, and
site build.

For example, the `empathy` repository would own:

```text
egohygiene.io/holon/empathy/
egohygiene.io/holon/empathy/docs/
egohygiene.io/holon/empathy/intelligence/
```

The same convention should extend across the organization:

```text
egohygiene.io/holon/mantle/
egohygiene.io/holon/realm/
egohygiene.io/holon/relay/
egohygiene.io/holon/egolint/
egohygiene.io/holon/aniflow/
egohygiene.io/holon/optiflow/
```

## Standard holon surfaces

A repository should be able to expose a predictable set of surfaces. Not every
surface must exist immediately, but the vocabulary should stay consistent.

```text
/holon/<repository>/
├── /                  # project landing page
├── /docs/             # user and developer documentation
├── /intelligence/     # repository intelligence dashboard
├── /architecture/     # architecture and system-design material
├── /releases/         # release and changelog views
└── /health/           # CI, quality, and maintenance signals
```

The holon landing page should answer what the repository is, why it exists, how
it fits into Ego Hygiene, its current status, and where to go next. It should not
simply duplicate the documentation site.

## Product space versus system space

Some repositories will have two legitimate web identities.

For example:

```text
egohygiene.io/store/          # public merchandise storefront
egohygiene.io/holon/store/    # engineering surface for the store repository

egohygiene.io/hygiene/        # public Ego Hygiene application
egohygiene.io/holon/hygiene/  # engineering surface for the application repository
```

This distinction is intentional. Product paths answer "use the thing" while
holon paths answer "inspect and understand the thing as part of the system."

## Repository ownership model

The long-term goal is for `/holon/` to be a platform contract rather than a
manually maintained collection of pages.

Each repository should eventually declare the web surfaces it owns and produce
its own deployable site artifact. Shared Ego Hygiene infrastructure should be
responsible for discovery, composition, routing, and common conventions rather
than owning repository-specific content.

A future declaration might conceptually resemble:

```yaml
holon:
  name: empathy
  repository: egohygiene/empathy
  path: /holon/empathy

surfaces:
  docs:
    path: /docs
  intelligence:
    path: /intelligence
```

This format is illustrative only. The schema, build system, routing mechanism,
and deployment implementation remain intentionally undecided.

## Role of empathy

`empathy` is currently the temporary workspace in which many organization-wide
repository conventions are being developed. It should therefore act as the
reference implementation for the holon web contract before those conventions are
extracted into shared platform repositories and propagated across the Ego
Hygiene organization.

The first implementation can use `empathy` to establish the desired landing,
documentation, and repository-intelligence experience while preserving a path to
organization-wide reuse.

## Relationship to repository intelligence

The holon model provides the natural public home for the repository intelligence
work already being developed:

```text
/holon/<repository>/intelligence/
```

Over time, a top-level holon directory could discover registered repositories
and expose their documentation, architecture, health, releases, dependencies,
and intelligence surfaces as a browsable view of the entire Ego Hygiene system.

## Current conceptual namespace

```text
egohygiene.io/
├── /                         # public Ego Hygiene landing portal
├── /hygiene/                 # public application
├── /store/                   # public storefront
├── /research/                # possible future public research namespace
└── /holon/
    ├── /empathy/
    │   ├── /docs/
    │   └── /intelligence/
    ├── /mantle/
    ├── /realm/
    ├── /relay/
    ├── /egolint/
    └── ...

articles.egohygiene.io/       # Medium publication
```

## Architectural principles

1. **Repository ownership remains local.** Each repository owns its own holon
   content and build inputs.
2. **The web namespace is organization-wide.** Ego Hygiene controls the public
   URL architecture rather than allowing hosting defaults to define it.
3. **Public products and engineering surfaces stay distinct.** `/store/` and
   `/holon/store/` are intentionally different experiences.
4. **Conventions should be reusable.** `empathy` is the reference implementation,
   not the permanent source of every organization's web concern.
5. **Intelligence is a first-class surface.** Repository intelligence belongs
   beside docs rather than being treated as an internal CI artifact.
6. **Implementation details remain replaceable.** GitHub Pages, Actions, routing,
   static-site tooling, and manifests should serve the namespace contract rather
   than define it.
7. **The system should become discoverable.** A future `/holon/` index should be
   derivable from repository declarations rather than maintained by hand.

## Open design questions

The following should be resolved through implementation-focused PRs rather than
prematurely fixed in this vision note:

- Which repository owns the root `egohygiene.io` portal?
- How should nested `/holon/<repository>/` routing be implemented while allowing
  repositories to retain build ownership?
- What static-site framework or shared theme, if any, should become the baseline?
- What is the minimum Holon Web Contract v1 manifest?
- Which surfaces are mandatory versus optional?
- Where should reusable GitHub Actions and deployment logic live?
- How should the root holon directory discover participating repositories?
- Which public concepts eventually deserve first-class paths such as
  `/research/`, and which should remain within product-specific namespaces?

## Near-term direction

Use `empathy` to establish the reference experience incrementally:

1. define the first holon contract and routing strategy;
2. establish the `empathy` landing surface;
3. expose repository documentation beneath the holon;
4. expose repository intelligence beneath `/intelligence/`;
5. extract reusable build and deployment behavior once the reference
   implementation proves the model;
6. propagate the convention to additional Ego Hygiene repositories.

This note is the architectural north star. Individual PRs may refine the details,
but changes should preserve the separation between public product space and the
repository-owned holon space unless the architecture is deliberately revised.
