# Consumer-owned mailmap baseline

Foundation **3.0.0** requires a root `.mailmap` as a repository-owned artifact.
This is a breaking addition to the previous 2.1.0 required-file baseline.
Authoring schema **1.2.0** adds the optional `mailmap` identity selection; the
existing v1 schema filenames and Holon presence contract remain unchanged.
Existing consumers keep their exact old source/resolver until reviewed adoption.
No release, automatic upgrade or fleet rollout is implied by this source change.

The universal template contains comments only. Names, email addresses and alias
equivalences belong to the consumer and must have reviewed public evidence.
Another organization supplies its own input; it must not copy Empathy's identity
selection. The golden input preserves the sole existing committed mapping from
[the prior root file](https://github.com/egohygiene/empathy/blob/41d4c8bdba88cd5cc17318647d542eea57a70364/.mailmap).
It introduces no new address, private email or alias equivalence. The old file's
comments are preserved as local text. This records source provenance; it does
not claim an additional identity approval or change the author of any commit.

## Presence, syntax and meaning

`verify-workspace` establishes file presence and repository ownership. A
comment-only file can satisfy that inventory check while identity configuration
remains unselected. It cannot pass mailmap planning: missing or comment-only
baseline input produces an actionable error. New repositories with no reviewed
author data retain that explicit unconfigured state rather than inventing people.
There is no visibility-specific identity default or silent lifecycle exemption.

`mailmap` in the consumer manifest has three fields:

- `baseline`: approved organization/consumer mapping lines, with a final LF;
- `local_additions`: exact local mappings and comments, empty or LF-terminated;
- `identity_evidence`: public HTTPS source/review references supporting the input.

The references are provenance, not automated proof of rights or identity.
Maintainers review them with each mapping change. Synthetic tests use only
`example.invalid` identities. Private addresses and person-level analytics are
outside this contract.

The portable header is SHA-256 pinned in the catalog. Plans bind its exact bytes,
the canonical catalog and resolved manifest, both input layers and output bytes.
Identical inputs produce identical JSON without timestamps or machine paths.

## Git semantics and conflict policy

[Git's mailmap reference](https://git-scm.com/docs/gitmailmap) is authoritative.
The parser supports its four explicit forms, illustrated with synthetic values:

```text
Canonical Name <old@example.invalid>
<new@example.invalid> <old@example.invalid>
Canonical Name <new@example.invalid> <old@example.invalid>
Canonical Name <new@example.invalid> Old Name <old@example.invalid>
```

The first form changes only the displayed name. The second changes only the
email. The third changes both; the fourth restricts matching to a name/email
pair. Matching of alias names and emails is case-insensitive; canonical display
text is preserved. Git matches mappings rather than rewriting commit objects.

This conservative portable subset requires explicit email addresses with `@`,
UTF-8 LF-terminated input, bounded size and whole-line `#` comments. Unsupported
forms fail instead of being silently ignored. Canonical names are optional only
in the email-only form. No wildcard identity or guessed alias is accepted.

Git can silently replace an earlier entry for the same alias. Composition
rejects conflicting case-insensitive aliases across either layer instead.
Email-wide and name-specific entries may coexist only when their specified
canonical fields agree. This deliberately rejects ambiguous overrides even if
Git would choose a result. Identical repeated entries preserve their text.
Local mappings and comments remain byte-preserved through baseline updates.
Unlike gitignore, there is no baseline-last rule designed to defeat local text.

## Plan, review and adopt

```sh
python3 tools/foundation.py validate-catalog
python3 tools/foundation.py validate-manifest --manifest foundation/empathy.manifest.json
python3 tools/foundation.py plan-mailmap \
  --manifest foundation/empathy.manifest.json \
  --output foundation/contracts/empathy.mailmap-plan.json
python3 tools/foundation.py check-mailmap-plan \
  --manifest foundation/empathy.manifest.json \
  --output foundation/contracts/empathy.mailmap-plan.json
python3 -m unittest discover -s tests -p 'test_foundation_mailmap.py' -v
```

The planner writes only the explicitly selected JSON proposal. It rejects a
`.mailmap` output target and does not read or overwrite consumer mailmaps,
rewrite commits, amend, rebase or push. Empathy's reviewed root adopts the
planned content in this source change. Consumers must inspect their current
file and place all retained local mappings/comments in their own manifest.

For an update, retain the previous plan/file as a preimage, review identity and
local-text diffs, and verify the current file hash before replacing it. An
idempotent rerun has the same output hash. Rollback restores the retained bytes
only after checking that the current file still matches the applied output;
changed local files require a fresh plan. This protocol is exercised in a
throwaway real Git repository, including unchanged commit/tree IDs and raw
`%an/%ae` history, mapped `%aN/%aE`, unmapped authors and local additions.
No `filter-repo`, history rewrite or force push is involved.

## Pilot and owner handoffs

The first adopter remains Filament, through a separate pinned, reviewed consumer
change after this upstream baseline is accepted. Its input must preserve local
contributors and use only reviewed public mappings. The intended sequence is:

| Boundary                    | Owner          | Current status and acceptance needed                                                                                         |
| --------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Contract and golden plan    | Empathy #100   | This candidate; acceptance belongs to its review, with exact Git fixtures.                                                   |
| Materialize/update/rollback | Holon          | Future adapter must consume the versioned plan and exact preimage/output hashes; the planner does not grant write authority. |
| Meaningful conformance      | EgoLint        | Presence projection is generated here; content/Git-behavior conformance is a separate owner interface.                       |
| Reusable execution          | Relay #5 / #49 | Existing execution seams; no new workflow or permissions are introduced here.                                                |
| Filament pilot              | Filament       | Not adopted by this PR; record upstream revision, source/output hashes and local preservation in its own review.             |
| Reviewed fleet waves        | Pace #30       | Not started; requires accepted producer/adopter inputs and normal consumer PRs.                                              |

The [master file-contract tracker](https://github.com/egohygiene/.github/issues/32)
links this work and retains the selected `.gitattributes` progression. Mailmap
contract/golden composition is independently reviewable under #100; it does not
promote another file or claim that all gitignore/attributes rollout is complete.
Reuse existing owner issues where applicable; a source plan is not proof of a
released Holon/EgoLint/Relay adapter or accepted pilot/fleet adoption.
