# External Mindgarden and architecture corpus

Empathy selects the immutable standalone Mindgarden candidate already declared
in `requirements/mindgarden-standalone.txt`. The installation is still an
unreleased **0.1.0 candidate**, not a published 1.0 product. The consumer checks
its PEP 610 full commit and installation prefix before importing its APIs.
`python -I` prevents the incubated source tree from becoming the selected engine.

The canonical architecture documents stay at the repository root. Hygiene's
generated context stays at `docs/ecosystem/CONTEXT.md`, with its existing owner,
revision and generator markers. The five authored garden notes remain canonical
under `.garden/`. No engine, source document or private archive is migrated here.

## Selected agent cutover

The tracked `llms.txt` now comes from the installed standalone command, including
its external documentation links. `mindgarden verify` accepts that exact output.
Those documentation links are discovery links; the executed package remains
pinned by full commit. This resolves the previously recorded exit3 from the
incubation-relative links without manually patching a generated entrypoint.

The selected `garden:check`, `garden:index`, `garden:context`, `garden:llms:write`
and public-projection commands use the external installation. The retained
`garden:legacy:check` keeps old migration paths explicit. Its strict agent check
can report the deliberate entrypoint difference after this cutover; it is not
the selected golden check. Current local site commands and Pages builds also
use the installed owner's native publishing and Quartz adapter. The retained
staged implementation and fixed historical rollback keep their original paths.

```sh
task garden:standalone:install
task garden:check
```

Installation is an explicit software acquisition step. Verification checks the
source identity, validates five existing notes, searches and renders the bounded
reviewed context, projects/verifies public Markdown and runs real owner-API
consumer fixtures. It does not install a model, connect private storage or deploy.

## Explicit public source indexing

`integrations/mindgarden/corpus.json` selects **18 architecture documents and the
generated ecosystem context**, by stable identity and exact SHA-256. It also
lists the bounded tracked support files needed by the existing notes. No
untracked file, local overlay, credential, cache or arbitrary repository scan is
an implicit input. A changed source requires a reviewed manifest refresh.

```sh
task garden:corpus:index OUTPUT=.cache/mindgarden-corpus
task garden:corpus:check OUTPUT=.cache/mindgarden-corpus
```

The thin consumer delegates ingestion, validation, indexing and publication to
the installed owner. Its disposable repository contains **24 indexed notes**:
the five existing notes and 19 source captures. Every new capture is
`status: proposed` and `reviewed: false`, retaining the source's original draft
or generated metadata inside the captured text and source report. Indexing is
not ADR acceptance, source-rights approval or promotion of a claim.

Each capture retains an exact source URL, content/provenance digests and the
declared manifest's capture date. Search of these new captures is an explicitly
unreviewed-evidence operation. The default reviewed context and `llms.txt` do
not silently include them.

New output destinations must be empty, and outputs inside the repository belong
under ignored `.cache`. `--check` reproduces into a fresh temporary directory
and compares exact file hashes without repairing an existing output. The
consumer rechecks canonical input hashes after processing. Original documents,
notes, source states and staged Git blobs are preserved.

## Optional file exchange prototypes

```sh
task garden:exchange:prototype EXCHANGE=openwiki OUTPUT=.cache/openwiki-prototype
task garden:exchange:prototype EXCHANGE=obsidian OUTPUT=.cache/obsidian-prototype
```

These are **offline Markdown file prototypes**, not hosted application or API
acceptance. They export only the owner's verified public tree, then use the
owner's ingestion API to re-import a projected file into disposable evidence.
The imported note stays proposed/unreviewed and cannot overwrite an original.
Both operations retain source hashes and leave the canonical store untouched.
Actual OpenWiki service behavior and Obsidian GUI discovery are untested.

The existing repository-root Obsidian vault and native Bases configuration stay
in place; no community plugin is enabled. OpenWiki/Obsidian are replaceable
views or exchange endpoints, never competing canonical knowledge stores.

For native architecture qualification, supply an explicit immutable owner checkout:

```sh
task garden:architecture:check AETHER_ROOT=/path/to/pinned/aether
```

The fixtures verify the selected owner program/schema hashes, then exercise its
actual validators. Without that optional owner input, baseline discovery reports
an explicit prerequisite skip. The selected qualification must execute with no
skips; old fixed-version/draft-only assertions are not treated as authority.

## Reviewed-public and private-content gates

The owner's public projection contains the same **five reviewed public notes**.
The new proposed captures are excluded. A synthetic private-note injection makes
the owner reject the public garden before creating a new output. It is not
silently filtered into a successful publication. No actual private content is
used by these tests.

`garden:standalone:verify` exercises these boundaries with the installed owner.
A fresh baseline host without that optional package reports the selected owner
fixture prerequisite as unavailable; it is not a passing golden integration.
The installed, explicitly selected lane must run those cases without skips.
Local generated Markdown and prototype evidence do not claim a fresh Pages
release, released package, host interoperability or wider fleet adoption.

## Standalone Pages delegation

The current Pages garden step installs the same immutable requirement into an
isolated environment and verifies its full PEP 610 source identity and package
prefix through the existing consumer boundary. It then calls the owner's
`publish verify` and `site build` interfaces. Quartz remains the pinned renderer;
Empathy adds no publishing engine. The historical rollback selects its original
compatibility commands and does not install the current standalone package.

The native owner projection is compared byte for byte with the retained
compatibility projection: the same five Markdown routes and ownership marker.
Both paths keep only reviewed public notes. Private injection must fail before
output creation; proposed corpus captures stay outside the public projection.

After a successful current native build, the existing private provenance archive
retains `publication/mindgarden-owner.json`: the actual package source/version,
represented consumer revision, observation clock and public input hashes. This
receipt does not enter the served site or imply a package release. The existing
composition, route preservation, duplicate-build and deployment/live verification
remain the publication gates. Source qualification alone is not a new live run.

`integrations/mindgarden/publication-evidence.json` records the later committed
input frame and actual native build. Its fresh 63-file site matches a fresh
same-input compatibility build in all 19 HTML pages and static assets. The two
XML feeds differ only in their real generated `pubDate`/`lastmod` clocks; both
raw identities are retained. The original `golden-evidence.json` observation and
its earlier input frame stay historical, with their original clocks and hashes.

## Architecture authority and preserved legacy sources

The canonical Aether architecture validator, from the exact owner source recorded
in `integrations/mindgarden/architecture-source-comparison.json`, validates the
18 root documents. This consumer adds no second architecture validator.
The source comparison records the full **22-file legacy family**:20 spec/navigation
files, the Architect agent and the architecture-authoring skill. It records actual
staged blobs, current canonical paths under `library/organization/specs/` and
domain-grouped skill/agent paths, canonical identities and exact differences.

Different bytes are retained as unaccepted deltas under #79. Changed line groups
are evidence of a difference, not an assertion of semantic equivalence. The
historical `specifications/` classifier path is not treated as canonical. No
source removal, rights approval, release metadata or cleanup receipt is created.
The immutable Aether source candidate remains distinct from a released bundle.

Refs #65; parent #118. Acceptance belongs to the actual source/consumer review;
Issue #79 retains broader graduation, migration rights and separately authorized
cleanup. Existing publication and historical qualification keep their own pins
and observation clocks.
