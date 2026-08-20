---
schema: mindgarden.note/v0
id: empathy-egohygiene-web-namespace
title: Ego Hygiene repository web namespaces
kind: project
status: reviewed
reviewed: true
confidence: high
visibility: public
owners:
  - egohygiene
created: 2026-08-15
updated: 2026-08-19
sources: []
related:
  - repository-intelligence-dashboard
supersedes: []
tags:
  - architecture
  - github-pages
  - holon
  - platform
  - web
---

# Ego Hygiene repository web namespaces

## Decision

`egohygiene.io` is the organization landing portal. Each independently owned
repository receives a first-class subdomain and owns the site published there:

```text
https://<repository>.egohygiene.io/
```

Examples include:

```text
https://akashic.egohygiene.io/
https://optiflow.egohygiene.io/
https://empathy.egohygiene.io/       # target; DNS and Pages migration pending
```

This subdomain model supersedes the earlier proposed
`egohygiene.io/holon/<repository>/` namespace. A repository remains a holon in
the system architecture, but `holon` is not required in its public URL.

## Standard repository surfaces

Every repository may compose several independently generated surfaces into one
site artifact:

```text
https://<repository>.egohygiene.io/
├── /                       # project or product landing surface
├── /documentation/          # user and developer documentation
├── /intelligence/           # repository intelligence dashboard
├── /architecture/           # architecture and design material
├── /releases/               # release and changelog views
└── /garden/                 # optional repository knowledge surface
```

Not every repository must enable every surface. Paths are stable capability
contracts, not a requirement to deploy empty pages.

## Build and deployment boundary

A repository has one GitHub Pages deployment target. Shared capabilities build
subtrees; the repository-local workflow composes and deploys the complete site:

```text
landing-page builder -----------\
documentation builder ----------+--> one site directory --> one Pages artifact
Relay intelligence action ------/
```

Relay must never deploy an intelligence-only artifact over an existing product
or documentation site. It writes the configured `intelligence/` directory and
returns control to the repository-owned workflow. That workflow owns event
triggers, permissions, the `github-pages` environment, custom-domain files, and
the final upload.

## DNS and custom domains

Each repository subdomain uses one DNS CNAME pointing at the Ego Hygiene
GitHub Pages host and the matching custom domain in that repository's Pages
settings. Subpaths such as `/intelligence/` and `/documentation/` do not need
additional DNS records.

Akashic and Optiflow are the first custom-domain consumers. Empathy continues
to publish at `https://egohygiene.github.io/empathy/` until its DNS record and
GitHub Pages custom-domain setting are configured together. Public links must
not switch to `empathy.egohygiene.io` before that migration is live.

## Capability ownership

| Concern | Owner |
| --- | --- |
| Repository identity, content, configuration, and custom domain | Consumer repository |
| Reusable GitHub Actions and static-surface builders | Relay |
| Final Pages composition and deployment | Consumer repository |
| Baseline capability selection and integration proof | Empathy |
| Installing the baseline into new repositories | Holon |
| Organization desired-state rules | Hygiene |
| Cross-repository collection and comparison | Observatory |
| Version drift detection and reconciliation | Pace |

## Repository intelligence as the first proof

Repository intelligence establishes the reusable pattern:

1. Relay releases an immutable action containing the shared collector,
   contracts, renderer, assets, normalizers, and tests.
2. Each repository retains a thin caller with repository-specific paths,
   producer selection, exclusions, identity, and Pages composition.
3. The caller writes the dashboard to `site/intelligence/` or the equivalent
   site-build directory.
4. The repository uploads its complete site once.
5. Akashic and Optiflow validate the action under different real site stacks.
6. Empathy remains the strict baseline consumer rather than the implementation
   owner.

The same pattern can later support documentation, architecture, release, and
other repository-scoped surfaces without duplicating build machinery.

## Architectural principles

1. **One repository, one domain, one Pages artifact.** Shared builders may
   contribute subtrees but do not compete for deployment ownership.
2. **Repository ownership remains local.** Product content, identity, policy,
   and custom-domain configuration do not move into Relay.
3. **Reusable mechanics have one canonical source.** Consumer repositories pin
   immutable Relay releases instead of copying action implementations.
4. **Paths describe capabilities.** `/intelligence/` means the same kind of
   surface across repositories even when its inputs differ.
5. **Public URLs change only when live.** Documentation continues to use a
   working GitHub Pages URL until its custom domain is verified.
6. **Organization-wide views live above repositories.** Observatory may collect
   public summaries later; it does not replace repository-owned dashboards.

## Pending work

- Publish and pin Relay repository intelligence v1.
- Prove complete Pages composition in Akashic and Optiflow.
- Configure and verify `empathy.egohygiene.io` before updating live links.
- Define the reusable documentation builder and `/documentation/` contract.
- Let Holon install thin capability callers and let Pace detect version drift.
