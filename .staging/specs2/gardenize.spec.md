---
title: Process Specification — Gardenization of Extracted Knowledge
version: 1.0
date_created: 2026-07-18
last_updated: 2026-07-18
owner: Ego Hygiene
tags: [process, mindgarden, obsidian, formatting, organization]
---

# Introduction

This specification defines how extracted knowledge and synapses are formatted, classified, and placed into the Mindgarden digital garden and Obsidian-compatible note structures.

## 1. Purpose & Scope

This specification defines post-extraction formatting and organizational behavior for derived artifacts.  
The audience is engineers and AI agents implementing vault-writing workflows.  
This specification covers note shaping, frontmatter mapping, folder routing, and link integrity for Mindgarden and Obsidian usage.

## 2. Definitions

- **Gardenization**: Converting extracted artifacts into structured vault-native notes.
- **Vault**: The `mindgarden/` directory opened as an Obsidian workspace.
- **Canonical Template**: Required note template in `mindgarden/_system/templates/`.
- **Placement Rule**: Deterministic mapping of artifact type and metadata to destination folder.
- **Backlink Integrity**: Validity of wikilinks between source, knowledge, and synapse notes.

## 3. Requirements, Constraints & Guidelines

- **REQ-001**: The system shall transform extracted knowledge into notes compatible with `mindgarden/_system/templates/knowledge.md`.
- **REQ-002**: The system shall transform synapses into notes compatible with `mindgarden/_system/templates/synapse.md`.
- **REQ-003**: The system shall create or update source records compatible with `mindgarden/_system/templates/source.md`.
- **REQ-004**: The system shall route notes to canonical folders: `sources/`, `knowledge/`, and `synapses/`.
- **REQ-005**: The system shall emit Obsidian wikilinks connecting source → knowledge → synapse artifacts.
- **REQ-006**: The system shall preserve provenance references from extraction outputs in note bodies and frontmatter.
- **REQ-007**: The system shall normalize frontmatter keys and values to vault metadata conventions.
- **REQ-008**: The system shall support idempotent reruns without creating duplicate notes for the same artifact id.
- **REQ-009**: The system shall mark lifecycle/review statuses based on processing state.
- **REQ-010**: The system shall maintain human-readable markdown with no mandatory plugin-specific syntax beyond existing vault conventions.
- **SEC-001**: The system shall carry sensitivity labels into note frontmatter and avoid writing secrets.
- **SEC-002**: The system shall avoid embedding protected source payloads unless explicitly allowed by sensitivity policy.
- **CON-001**: The system shall not mutate original source meaning during formatting.
- **CON-002**: The system shall not place notes outside approved vault directories.
- **GUD-001**: Prefer stable file naming (`kebab-case` plus deterministic suffix/prefix strategy) for predictable linking.
- **GUD-002**: Prefer atomic synapse notes (one major insight per note) for reuse in visuals and maps.
- **PAT-001**: Use staged output flow: map metadata → render template fields → route file → verify links.

## 4. Interfaces & Data Contracts

### 4.1 Gardenize Input Contract

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `artifact_type` | enum | Yes | `source \| knowledge \| synapse` |
| `artifact_id` | string | Yes | Stable unique identifier |
| `content` | object | Yes | Structured extraction output payload |
| `metadata` | object | Yes | Domains, topics, timestamps, sensitivity, status |
| `links` | object | No | Related source/knowledge/synapse ids |

### 4.2 Rendered Note Contract

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | string | Yes | Destination path under `mindgarden/` |
| `filename` | string | Yes | Deterministic note filename |
| `frontmatter` | object | Yes | Template-aligned YAML |
| `body_markdown` | string | Yes | Human-readable markdown sections |
| `wikilinks` | array[string] | Yes | Outbound Obsidian links |
| `render_version` | string | Yes | Gardenization schema/process version |

### 4.3 Folder Routing Contract

| Artifact Type | Destination Root | Required Template |
| --- | --- | --- |
| `source` | `mindgarden/sources/` | `_system/templates/source.md` |
| `knowledge` | `mindgarden/knowledge/` | `_system/templates/knowledge.md` |
| `synapse` | `mindgarden/synapses/` | `_system/templates/synapse.md` |

## 5. Acceptance Criteria

- **AC-001**: Given extracted knowledge input, when gardenization runs, then a knowledge note is created in `mindgarden/knowledge/` with template-aligned frontmatter.
- **AC-002**: Given derived synapse input, when gardenization runs, then a synapse note is created in `mindgarden/synapses/` with required sections and confidence/provenance fields.
- **AC-003**: Given source metadata, when source rendering runs, then a source note exists in `mindgarden/sources/` with processing history updated.
- **AC-004**: Given linked artifacts, when notes are rendered, then wikilinks between source, knowledge, and synapse resolve.
- **AC-005**: Given repeated runs for the same artifact id, when rendering completes, then duplicates are not created and updates are deterministic.
- **AC-006**: Given sensitive artifacts, when persisted, then sensitivity and redaction policies remain enforced.

## 6. Test Automation Strategy

- **Test Levels**: Unit (mapping and rendering), Integration (artifact-to-file routing), End-to-End (full extraction-to-vault flow)
- **Frameworks**: Use repository-native test frameworks for content and file pipeline modules
- **Test Data Management**: Maintain fixtures with representative source, knowledge, and synapse payloads including sensitive and contradictory cases
- **CI/CD Integration**: Validate frontmatter schema, routing, and link checks on pull requests
- **Coverage Requirements**: Validate all artifact types, template mappings, and rerun/idempotency behavior
- **Performance Testing**: Validate bulk gardenization throughput for large batches

## 7. Rationale & Context

Extraction quality is insufficient unless artifacts become navigable and durable in the operating knowledge system. Gardenization operationalizes extracted material by aligning it with vault templates, conventions, and folder structure used by both humans and AI agents. This enables Obsidian queries, graph links, dashboard surfacing, and future publishing workflows.

## 8. Dependencies & External Integrations

### External Systems

- **EXT-001**: Mindgarden vault filesystem - Destination for rendered notes.

### Third-Party Services

- **SVC-001**: Obsidian ecosystem compatibility - Notes must remain readable and queryable in standard Obsidian workflows.

### Infrastructure Dependencies

- **INF-001**: File write/update engine with deterministic path and merge behavior.

### Data Dependencies

- **DAT-001**: Outputs from `knowledge-extract.spec.md` contracts.
- **DAT-002**: Vault metadata conventions in `mindgarden/_system/schemas/metadata-conventions.md`.

### Technology Platform Dependencies

- **PLT-001**: Markdown + YAML frontmatter renderer preserving valid UTF-8 and line endings.

### Compliance Dependencies

- **COM-001**: Privacy classification propagation from source artifacts into vault notes.

## 9. Examples & Edge Cases

```code
Example:
- Input: Extracted knowledge on "retrieval practice" with domains ["learning"]
- Output Path: mindgarden/knowledge/concepts/retrieval-practice.md
- Output Links: [[sources/<source-note>]], [[synapses/<synapse-note>]]

Edge Case:
- Input: Same artifact_id arrives with revised summary
- Expected: Existing note is updated in place, `updated_at` changes, filename remains stable
```

## 10. Validation Criteria

- Frontmatter validates against expected keys per artifact type.
- Rendered note paths conform to approved routing rules.
- All generated wikilinks are syntactically valid and target existing or intentionally stubbed notes.
- Idempotency checks confirm no duplicate file creation for same artifact id.
- Secret scanning confirms no credentials are written into generated notes.

## 11. Related Specifications / Further Reading

- `.github/specs/knowledge-extract.spec.md`
- `mindgarden/_system/templates/source.md`
- `mindgarden/_system/templates/knowledge.md`
- `mindgarden/_system/templates/synapse.md`
- `mindgarden/_system/schemas/metadata-conventions.md`
