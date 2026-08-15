# Sanctuary Tools Roadmap

## Purpose

This roadmap governs the reusable tools developed under Sanctuary's `tools/`
root. It is intentionally self-contained from Sanctuary's primary roadmap.

The tools convert scattered personal and project material into durable,
portable, reviewable knowledge while reducing repeated setup work and cognitive
load. Each tool should solve an immediate local problem first, then grow into a
safe, reusable workflow that can support additional sources, destinations, and
automation later.

The initial journey covers:

- Universal knowledge and context extraction
- ChatGPT conversation capture, processing, and archival assistance
- Chrome bookmark organization and webpage ingestion
- Repository context snapshots for AI handoffs
- Music catalog and creative-project archival
- OpenWiki ingestion and wiki maintenance
- Future Garden and Obsidian integration

## Product Principles

1. **Acquire without loss.** Preserve raw source material before transforming
   or reorganizing it.
2. **Separate concerns.** Acquisition, normalization, extraction, review,
   routing, and archival are independent stages.
3. **Use portable contracts.** Core formats must not depend on one model,
   platform, wiki, or note-taking application.
4. **Prefer local-first processing.** Personal sessions, credentials, raw
   archives, and sensitive material stay local by default.
5. **Be non-destructive by default.** Retrieval and extraction never imply
   permission to archive, delete, publish, overwrite, or reorganize sources.
6. **Require review at trust boundaries.** Destructive actions and publication
   require verified outputs and explicit approval.
7. **Preserve provenance.** Durable knowledge must remain traceable to its
   source, time scope, and processing history.
8. **Design for replacement.** Platform-specific integrations are adapters that
   can be replaced when APIs or services change.
9. **Automate proven workflows.** Begin with manual or locally invoked tools;
   schedule them only after their behavior is trustworthy.
10. **Keep destinations downstream.** Extraction outputs should remain useful
    before the final Garden, Obsidian, wiki, or repository structure is known.

## System Model

```text
Source
  -> acquisition adapter
  -> immutable raw snapshot
  -> canonical source envelope
  -> knowledge extraction
  -> portable knowledge packet
  -> human review
  -> destination adapter
  -> optional source archival
```

The stable center of the system is the canonical source envelope plus the
portable knowledge packet. Source and destination integrations may evolve
without rewriting the extraction engine.

## Planned Tool Suite

```text
tools/
├── ROADMAP.md
├── knowledge-core/
├── chatgpt-extract/
├── bookmark-extract/
├── repository-context/
└── music-catalog/
```

Names remain provisional until each project is scaffolded. Each tool may be a
small Poetry project with its own `pyproject.toml`, `src/`, `tests/`, and
fixtures. Shared behavior belongs in `knowledge-core`; platform-specific logic
must not leak into it.

## Shared Contracts and AI Surfaces

The tooling depends on three related but distinct layers located outside or
alongside the individual Python projects:

- `knowledge-extract.spec.md`: Portable, vendor-neutral extraction contract
  that can be attached to or pasted into an AI conversation.
- `knowledge-extract` skill: Thin operational wrapper that teaches compatible
  agents how to load, apply, and verify the specification.
- Agent instructions: Repository-specific guidance that tells agents when to
  use the skill or apply the specification directly.

The specification is the source of truth. Skills, agent instructions, and code
may implement or extend it, but must not silently redefine it.

## Delivery Phases

### Phase 0 — Repository alignment

**Goal:** Fit the tools into Sanctuary without creating a competing structure.

- Inspect Sanctuary's existing tree, conventions, and partially completed work.
- Confirm project names and locations.
- Identify reusable code already present in Sanctuary.
- Establish root and nested agent-instruction boundaries.
- Define how local secrets, raw archives, fixtures, and generated artifacts are
  ignored or retained.
- Record supported Python versions and shared quality tooling.

**Exit criteria:** The intended structure is agreed upon and no existing work is
duplicated or displaced unintentionally.

### Phase 1 — Knowledge extraction specification

**Goal:** Establish the portable context-extraction contract.

- Finalize `knowledge-extract.spec.md` version 0.1.
- Validate zero-configuration drag-and-drop usage.
- Support quick, standard, deep, continuation, archive, compare, and update
  modes.
- Define source registration, provenance, confidence, status, and time scope.
- Define the portable Markdown output contract.
- Include structured and wiki-source output profiles.
- Establish instruction-boundary, privacy, and non-destructive rules.
- Test the specification with trivial and useful real-world sources.

**Exit criteria:** Several independent AI sessions can apply the specification
to the same sources and produce meaningfully equivalent, reviewable outputs.

### Phase 2 — Knowledge extraction skill and agent instructions

**Goal:** Make the specification convenient and reliable for AI agents.

- Scaffold the `knowledge-extract` skill.
- Keep `SKILL.md` procedural and concise.
- Reference the canonical specification without creating manually maintained,
  divergent copies.
- Generate `agents/openai.yaml` from the completed skill.
- Add repository instructions that prefer the skill when available and fall
  back to the specification directly.
- Add representative prompts and fixtures.
- Validate triggering, output quality, source fidelity, and safe defaults.

**Exit criteria:** A user can invoke knowledge extraction explicitly or by
attaching the specification, and the agent follows the same contract in either
workflow.

### Phase 3 — `knowledge-core`

**Goal:** Implement deterministic shared behavior as a reusable Poetry library
and CLI.

- Define canonical source-envelope models.
- Define portable knowledge-packet models.
- Add schema validation and version handling.
- Add stable identifiers, source references, hashing, and deduplication.
- Add filename and slug normalization.
- Add processing manifests and review states.
- Render portable Markdown without requiring a destination taxonomy.
- Define acquisition, extraction, destination, and archival protocols.
- Add structured errors and resumable processing primitives.
- Keep model-provider integration behind an interface.

**Exit criteria:** Fixtures can be validated, normalized, rendered, and rerun
without unstable output or duplicate records.

### Phase 4 — ChatGPT conversation extraction MVP

**Goal:** Process low-value conversations safely before scaling to important
history.

#### Acquisition strategies

- Manually copied Markdown or text
- Official ChatGPT data export
- Shared-link snapshot
- Authenticated local browser session
- Future supported per-conversation API

#### Processing workflow

- List, search, and select conversations.
- Retrieve a conversation by identifier or URL when supported.
- Preserve raw responses, message order, branches, metadata, and attachments.
- Normalize data into the canonical source envelope.
- Apply the knowledge-extraction specification.
- Generate a review bundle and processing report.
- Maintain a local ledger of unprocessed, processed, skipped, and failed items.
- Recommend `active`, `reference`, `processed`, `ignore`, or `archive-candidate`.
- Rerun without duplicating accepted outputs.

#### Archival strategies

- No-op archiver by default
- Manual archive instructions
- Explicit authenticated-browser archive operation
- No automated deletion

**Exit criteria:** A disposable conversation can be retrieved, extracted,
reviewed, marked as processed, and explicitly archived end to end.

### Phase 5 — OpenWiki integration

**Goal:** Use OpenWiki as the first working knowledge-base layer without waiting
for the final Garden or Obsidian architecture.

- Store accepted knowledge packets in a stable local directory or repository.
- Configure that location as an OpenWiki personal-mode source where practical.
- Use the specification's `wiki-source` profile for packets intended for wiki
  synthesis.
- Preserve raw packets separately from OpenWiki-generated wiki pages.
- Establish an update workflow that retains provenance and supersession history.
- Evaluate whether a configured local Git repository is sufficient.
- Create a dedicated connector only if the repository-source workflow becomes a
  real limitation.
- Keep OpenWiki-generated agent-file changes reviewable.

**Exit criteria:** Accepted conversation packets can update a local OpenWiki
personal wiki while remaining independently usable outside OpenWiki.

### Phase 6 — Bookmark organization and extraction

**Goal:** Safely organize Chrome bookmarks and convert valuable sources into
knowledge packets.

#### Bookmark organization

- Read Chrome bookmark data locally.
- Create an immutable backup before every mutation.
- Preserve bookmark identity and metadata where possible.
- Detect exact and probable duplicates.
- Detect inaccessible links without automatically deleting them.
- Propose a stable folder taxonomy.
- Preview changes as a reviewable plan or diff.
- Apply only approved changes.
- Support restore and incremental reruns.

#### Knowledge ingestion

- Fetch and normalize accessible webpage content.
- Record dynamic, authenticated, missing, or unsupported pages.
- Apply the extraction specification.
- Track source hashes and processing state.
- Send accepted packets to OpenWiki or another destination adapter.

**Exit criteria:** A copied bookmark fixture and then the real bookmark set can
be processed reversibly, with no silent loss and no duplicate knowledge output.

### Phase 7 — Repository context snapshots

**Goal:** Generate compact, current context for starting or continuing AI work.

- Reuse the existing repository-tree automation.
- Respect ignore rules and explicit sensitivity boundaries.
- Exclude secrets, binaries, dependencies, caches, and generated noise.
- Capture purpose, architecture, conventions, decisions, implementation state,
  unresolved work, and known risks.
- Separate observed repository state from plans described in documentation.
- Produce compact handoff, detailed context, and component-focused profiles.
- Avoid rewriting snapshots when meaningful context has not changed.
- Add a GitHub Action after the local workflow is proven.

**Exit criteria:** A new AI conversation can understand a repository using its
README, generated tree, and compact context snapshot without a manual history
dump.

### Phase 8 — Music catalog and creative archive

**Goal:** Create a canonical, multi-artist archive independent of publishing and
generation platforms.

#### Initial sources

- Local masters, drafts, stems, lyrics, and production notes
- Suno workspaces, generations, prompts, metadata, and relationships
- Artwork concepts, references, prompts, drafts, and finals
- DistroKid release metadata and identifiers
- SoundCloud publication metadata
- Future platform adapters

#### Processing workflow

- Preserve immutable raw platform snapshots.
- Normalize data into a canonical artist and track manifest.
- Hash and validate downloaded assets.
- Preserve parent, variation, draft, final, and published relationships.
- Extract audio and media metadata.
- Apply the knowledge-extraction specification to complete track archives.
- Generate visual-development, animation, release, portfolio, and continuation
  packets.
- Produce a completeness report before upstream content is archived.

**Exit criteria:** One released track can be reconstructed and understood from
the local archive without consulting its original platforms.

### Phase 9 — Garden and Obsidian adapters

**Goal:** Route accepted knowledge into the existing Sanctuary Garden after its
structure is ready.

- Inspect and finalize the root Garden taxonomy separately.
- Map portable knowledge packets into Garden note types.
- Preserve stable source references and backlinks.
- Add Obsidian-compatible frontmatter, aliases, attachments, and links.
- Generate maps of content only when the taxonomy supports them.
- Reconcile OpenWiki-generated knowledge with curated Garden notes.
- Avoid making OpenWiki output and curated notes competing sources of truth.

**Exit criteria:** Accepted packets can be routed into the Garden without
changing the extraction core or losing provenance.

### Phase 10 — Automation and maintenance

**Goal:** Automate only workflows that have demonstrated stable, safe behavior.

- Schedule local ChatGPT and bookmark acquisition where appropriate.
- Add repository-context updates to CI.
- Validate portable packets and Garden links in CI.
- Add incremental source refresh and failure reporting.
- Use pull requests or staging areas for generated knowledge changes.
- Keep browser sessions and personal credentials out of GitHub Actions.
- Add migration tools for specification and schema version changes.
- Track upstream adapter breakage without blocking unaffected tools.

**Exit criteria:** Automations are resumable, observable, reversible where
applicable, and do not require secrets outside their appropriate trust boundary.

## Recommended Execution Order

```text
Specification
  -> skill and agent instructions
  -> knowledge-core
  -> ChatGPT MVP
  -> OpenWiki integration
  -> bookmark extraction
  -> repository context
  -> music catalog
  -> Garden and Obsidian adapters
  -> automation
```

This is a dependency order, not a rigid priority order. Independent adapters may
be prototyped earlier when doing so answers a concrete design question, but
shared contracts should stabilize before substantial platform-specific code is
built.

## Immediate Work Queue

1. Review `knowledge-extract.spec.md` against one trivial ChatGPT conversation.
2. Review it against one technical or project conversation.
3. Record missing, noisy, or ambiguous output behavior.
4. Revise and tag the specification as version 0.1.
5. Scaffold the `knowledge-extract` skill.
6. Generate and validate the skill's agent metadata.
7. Inspect Sanctuary's existing Python and Poetry conventions.
8. Scaffold `knowledge-core` with models and fixtures only.
9. Implement manual transcript ingestion before authenticated retrieval.
10. Connect accepted packets to a small OpenWiki personal-mode experiment.

## Deferred Backlog

- Authenticated ChatGPT browser retrieval and archiving
- Full-history batch processing
- Custom OpenWiki connector
- Automatic bookmark taxonomy application
- Scheduled webpage refresh
- Repository-context GitHub Action
- Suno, DistroKid, and SoundCloud adapters
- Multi-artist catalog support beyond initial schema validation
- Garden routing and Obsidian graph generation
- Cross-source entity resolution
- Semantic search and embeddings
- Interactive review UI
- Desktop drag-and-drop interface
- Plugin or packaged distribution

## Cross-Cutting Definition of Done

A phase or tool is complete only when applicable criteria are satisfied:

- Inputs and outputs use documented, versioned contracts.
- Raw sources are preserved or their absence is explicitly documented.
- Material output remains traceable to source references.
- Reruns are idempotent or produce a clear, reviewable update.
- Partial failures do not corrupt completed work.
- Sensitive values do not appear in logs, fixtures, generated packets, or Git.
- Destructive behavior is disabled by default and separately authorized.
- Tests cover successful, partial, malformed, duplicate, and inaccessible input.
- Platform-specific code is isolated behind an adapter boundary.
- A human-readable processing report explains coverage and failures.
- Documentation states what is implemented rather than only what is intended.

## Current Status

| Area | Status | Next milestone |
| --- | --- | --- |
| Knowledge extraction specification | Draft created | Validate with real fixtures |
| Knowledge extraction skill | Planned | Scaffold after spec validation |
| Agent instructions | Planned | Define Sanctuary boundaries |
| `knowledge-core` | Planned | Define canonical models |
| ChatGPT extraction | Planned | Manual transcript MVP |
| OpenWiki integration | Evaluating | Ingest one accepted packet |
| Bookmark extraction | Backlog | Design Chrome source adapter |
| Repository context | Backlog | Inventory existing tree action |
| Music catalog | Backlog | Define one-track fixture |
| Garden and Obsidian | Deferred | Integrate after Garden design |
| Automation | Deferred | Automate proven workflows only |

## Roadmap Maintenance

- Update the status table when milestones change.
- Record newly discovered work in the most relevant phase or deferred backlog.
- Split implementation-ready work into focused GitHub issues with acceptance
  criteria and dependencies.
- Keep Sanctuary-wide product or business planning out of this file.
- Move a tool into Sanctuary's main roadmap only when it becomes a dependency of
  the wider repository rather than an implementation detail of `tools/`.
