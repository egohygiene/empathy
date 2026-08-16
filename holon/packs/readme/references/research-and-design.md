# README system research and design brief

## Snapshot status

This document preserves and operationalizes a user-provided August 2026
research snapshot. The corpus counts are heuristic pattern detections, not
quality scores, and were not recomputed during promotion into Holon. Future
research refreshes must record a retrieval date, accessible corpus, detection
method, and changed conclusions.

## Executive decision

The reusable system should not be one enormous README copied into every
repository. It should provide:

1. A universal project baseline that answers what the project is, why it
   matters, how to try it, how it works, and how to contribute.
2. Repository-type adaptation for CLIs, libraries, services, applications,
   templates, automation, data, documentation, and monorepos.
3. A profile baseline that changes the information architecture from “time to
   first success” to “time to trust.”
4. Automation that validates Markdown, links, local assets, placeholders, and
   generated regions without making third-party widgets critical.

The visual language may be expressive and unmistakably personal. Information
architecture must remain professional, accessible, fast to scan, and grounded
in proof.

## Research corpus

The supplied brief synthesized:

- [Best README Template](https://github.com/othneildrew/Best-README-Template).
- The 105 entries cataloged by
  [Awesome README](https://github.com/matiassingers/awesome-readme), including
  93 directly retrievable root README bodies in the snapshot.
- The 151 entries in
  [Awesome GitHub Profiles](https://recodehive.github.io/awesome-github-profiles/),
  including 134 directly retrievable profile README bodies in the snapshot.
- [Tilburg Science Hub README guidance](https://www.tilburgsciencehub.com/topics/collaborate-share/share-your-work/content-creation/readme-best-practices/).
- GitHub guidance on
  [repository READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
  [job-search profiles](https://docs.github.com/en/account-and-profile/tutorials/using-your-github-profile-to-enhance-your-resume),
  and [accessible profile READMEs](https://github.blog/developer-skills/github/5-tips-for-making-your-github-profile-page-accessible/).
- [SSW Rules](https://www.ssw.com.au/rules/awesome-readme) and GitHub's
  [standout profile examples](https://dev.to/github/10-standout-github-profile-readmes-h2o).

These references guide structure and evaluation. Their README bodies are not
vendored into the pack.

## Corpus observations

### Profile patterns

Among the 134 directly retrievable profile READMEs in the supplied snapshot:

| Pattern | Profiles | Share |
| --- | ---: | ---: |
| Contact or social links | 125 | 93% |
| GitHub statistics widgets | 111 | 83% |
| Skills or technology stack | 109 | 81% |
| Current work or learning | 102 | 76% |
| Projects or portfolio links | 96 | 72% |
| Badge collections | 94 | 70% |
| Animated media | 91 | 68% |
| Visitor counters | 83 | 62% |
| Banners or large headers | 52 | 39% |
| Accomplishments, awards, or certifications | 46 | 34% |
| Professional experience | 35 | 26% |
| Blog or writing feed | 29 | 22% |
| Contribution animation | 18 | 13% |

The useful gap is not another widget: skill icons, statistics, badges, and
animation were common, while measurable accomplishments, professional scope,
and decision-making evidence were comparatively rare.

### Project patterns

Among the 93 directly retrievable project READMEs in the supplied snapshot:

| Pattern | Projects | Share |
| --- | ---: | ---: |
| Support or community path | 81 | 87% |
| Installation guidance | 80 | 86% |
| Status or metadata badges | 78 | 84% |
| Contributing guidance | 72 | 77% |
| Documentation links | 71 | 76% |
| License information | 70 | 75% |
| Usage or examples | 67 | 72% |
| Screenshot, demo, or visual proof | 67 | 72% |
| Project value or motivation | 54 | 58% |
| Configuration guidance | 50 | 54% |
| Architecture or design explanation | 48 | 52% |
| Development workflow | 47 | 51% |
| Compatibility or prerequisites | 46 | 49% |
| Quick start | 42 | 45% |
| Roadmap | 20 | 22% |
| Security guidance | 15 | 16% |
| Troubleshooting | 11 | 12% |
| Explicit testing instructions | 9 | 10% |

Celebrated READMEs consistently reduce uncertainty: they state value quickly,
show a result, provide a copyable path to success, and route deeper questions
to dedicated documentation. Concise testing, security, and troubleshooting
paths remain meaningful differentiators.

## Design principles

### Optimize three reading depths

| Visit | Reader question | README response |
| --- | --- | --- |
| 15 seconds | What is this, is it active, and should I care? | Identity, promise, state, proof, primary action |
| 2 minutes | Can I use it, and is it credible? | Highlights, quick start, example, compatibility, evidence |
| 10 minutes | Can I adopt, evaluate, or contribute? | Architecture, configuration, development, quality, security, support, deeper docs |

### Lead with outcomes

Open with the problem, useful outcome, and intended audience. Technologies
belong in the explanation of how the outcome is achieved.

### Point claims to evidence

Project evidence may be a release, demo, benchmark, test suite, architecture
decision, or documentation page. Profile evidence should be a case study,
artifact, shipped outcome, quantified accomplishment, talk, publication, or
contribution.

### Use progressive disclosure

The README is a front door. Route deep material to `docs/`,
`CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, runbooks, API reference,
and architecture records.

### Make visuals functional

Use banners for identity, screenshots for behavior, and diagrams for
relationships. Keep critical facts in text, use meaningful alt text, and make
motion optional.

### Prefer durable signals

Build, release, coverage, security, documentation, and license signals answer
adoption questions. Stars, visitor counters, trophy walls, and random quotes
should never carry the argument.

### Degrade gracefully

External SVG and widget services fail, rate-limit, or disappear. Prefer
repository-owned assets and bounded action-generated artifacts. The document
must remain coherent if every external image is unavailable.

### Treat accessibility as a quality gate

Use descriptive links, concise alt text, hierarchical headings, plain language,
proper list markup, and thoughtful motion and emoji.

## Section contracts

Every active project README should provide:

- identity, one-sentence promise, state, and useful visual proof;
- problem, audience, differentiation, and concrete highlights;
- deterministic quick start and realistic usage;
- compatibility, documentation, and current limitations;
- development setup and exact quality commands;
- security, support, contribution, and license paths.

Conditional modules follow repository type:

- CLI: synopsis, examples, exit codes, completions, structured output.
- Library: import, API stability, compatibility, versioning, migration.
- Service: deployment, health, data flow, observability, recovery.
- App: live proof, screenshots, environment, local run, build, deployment.
- Template: consumers, customization seams, upgrades, synchronization.
- Automation: inputs, outputs, permissions, secrets, failures, pinning.
- Data/research: method, provenance, reproducibility, citation.
- Monorepo: workspace map, responsibilities, commands, boundaries.

A profile README should move through identity, proof, selected impact, featured
systems, capabilities, experience, current direction, and contact. It should
use a few case-study-quality projects and show systems thinking, actual AI
workflow evidence, and interdisciplinary practice only where those claims are
publicly demonstrable.

## Anti-patterns

- Copying every optional section into every repository.
- Centering the complete document and weakening scanability.
- Opening with a technology or badge wall.
- Repeating one claim in the tagline, overview, features, and about sections.
- Publishing commands that were not tested from a clean environment.
- Using generic link text or images without alt text.
- Depending on several unrelated third-party statistic services.
- Showing skill icons without evidence.
- Maintaining a hand-written table of contents when the platform outline is enough.
- Allowing generated feeds to grow without bounds or overwrite authored prose.
- Leaving tokens, fake badges, dead screenshots, or sample domains in published output.
- Treating a profile as a complete autobiography instead of a guided portfolio.

## Validation model

The mature organization workflow should enforce:

1. Markdown style and heading hierarchy.
2. Deliberately scoped prose and inclusive-language checks.
3. Link validation with rate-limit-aware retries and exclusions.
4. Local image existence and nonempty alt text.
5. Rejection of unresolved placeholders in materialized output.
6. Presence of required community and security files.
7. A rendered preview artifact for README-focused changes.
8. Integrity of bounded generated regions.
9. Repository-type policy synchronized through the future governance layer.

The Holon pack validator checks source-template structure offline. Consumer
repositories remain responsible for command execution, factual accuracy, links,
assets, and publication-time token rejection.

## Definition of done

The system is mature when a new repository can adopt the baseline without
inheriting irrelevant sections; every visible claim is accurate and evidenced;
the clean-environment quick start succeeds; the profile tells a coherent story
within two minutes; critical information survives missing widgets; headings,
links, assets, and lists meet the accessibility contract; generated regions
remain bounded; and the project/profile templates remain visibly related
without pretending they serve the same audience.
