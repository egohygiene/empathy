# Standalone Mindgarden consumer checkpoint

Refs #65; parent [Mindgarden #20](https://github.com/egohygiene/mindgarden/issues/20).
This optional consumer lane installs the standalone Python package from immutable
source `f3a88ccf7d67deb8ecf188d10d9cd496ed6a4973`, the merged
[Mindgarden #93–#109 baseline](https://github.com/egohygiene/mindgarden/blob/f3a88ccf7d67deb8ecf188d10d9cd496ed6a4973/docs/learning-evaluation-checkpoints.md). It is an
unreleased 0.1.0 candidate, not 1.0 publication evidence.

Empathy retains its canonical `.garden/` and consumes the external command.
No engine source is copied here. Existing incubated tasks and their migration
evidence remain intact for #79; this checkpoint does not remove them or change
Pages/Repository Intelligence publication.

```bash
task garden:standalone:install
task garden:standalone:verify
```

Installation is an explicit network/software acquisition step. Verification
requires the installed environment, checks its PEP 610 full commit identity,
validates the existing garden, searches, builds
bounded context and creates/verifies the reviewed-public projection locally.
The source pin lives only in the requirements file; update it deliberately by PR.

The installed engine must come from the interpreter prefix, not the local
incubation or another mutable sibling checkout. No real private archive, Drive
connection, model, credential, deployment or destructive migration is involved.
The consumer explicitly supplies its existing incubation-owned publication profile;
the normal privacy/publication gates still control the projection.

Focused consumer evidence is recorded below. The final strict agent verification
currently returns exit 3: the tracked llms.txt uses incubation-relative documentation
links, while the standalone engine emits canonical standalone documentation URLs.
The consumer must review that cutover; this lane deliberately keeps the existing
tracked entrypoint unchanged. A failed strict check is not a passing consumer gate.
The required canonical holistic check is separate from focused checks; no full
profile or deployed-site acceptance is claimed until its actual evidence exists.
Full #65 still owns architecture/context indexing, optional projections, accepted
cutover and reviewed publication. Replace this candidate with the released-version
pin and verify it when organization release work resumes; publication is currently deferred.

## Bounded validation

On Python 3.12, the pinned VCS installation and PEP 610 identity check pass.
Version, five-record validation, search, bounded context, explicit-profile public
projection and public verification pass without changing `.garden/` or `llms.txt`.
The final strict agent verification fails with the entrypoint-link difference
described above. This remains a draft consumer checkpoint.

Commands: `python3 -m unittest discover --start-directory tests --pattern
"test_mindgarden_*integration.py" --verbose`; execute the literal verification
task commands in order. Task is unavailable in the local environment, so these
commands were executed directly. No manual workflow or publication was launched.
The required holistic profile has not run for this draft.

## Non-destructive cutover rehearsal (2026-11-08)

The merged engine pin above was installed through VCS in a fresh environment.
PEP 610 identifies the full commit, and `mindgarden.__file__` resolves inside the
interpreter prefix. The staged consumer represents `4e721715ec56a126f4efe2043298a34e6559335e`.
Only its committed public `.garden`, README, tracked `llms.txt`, and the
document/workflow files cited by those notes were copied. The existing Quartz
profile was supplied as repository-relative configuration. No incubated Python
engine was present in staging. Document evidence under `mindgarden/profiles`
remains necessary for existing citations; it is not an engine import.

Results in the network-restricted verification environment: version, five-note
validation, search, bounded JSON context, public projection and deterministic
public verification all return 0. The unchanged staged `llms.txt` initially
returns 3 under strict `verify`, preserving the actual cutover finding. Running
the installed `mindgarden llms --repository-root STAGE --write` **only in that
scratch copy**, then `mindgarden verify --repository-root STAGE`, returns 0.
This proves the proposed external entrypoint is reproducible without changing
the working consumer's `.garden`, tracked `llms.txt`, tasks or Pages authority.
It does not accept that canonical cutover or a deployed site.

Reproduce using a new empty scratch directory and the installed pinned engine:

```sh
PROOF_STAGE=/tmp/new-empathy-public-proof
mkdir --parents "$PROOF_STAGE"
git archive 4e721715ec56a126f4efe2043298a34e6559335e \
  .garden README.md llms.txt mindgarden/profiles/obsidian/README.md \
  mindgarden/profiles/quartz/profile.yaml .github/workflows/ossf-scorecard.yml \
  .github/workflows/osv-scan.yml .github/workflows/megalinter.yml \
  .github/workflows/mindgarden-pages.yml | tar --extract --directory "$PROOF_STAGE"
.cache/mindgarden-standalone/bin/mindgarden validate --repository-root "$PROOF_STAGE"
.cache/mindgarden-standalone/bin/mindgarden publish project \
  --repository-root "$PROOF_STAGE" --profile mindgarden/profiles/quartz/profile.yaml \
  --output-directory exports
.cache/mindgarden-standalone/bin/mindgarden publish verify \
  --repository-root "$PROOF_STAGE" --profile mindgarden/profiles/quartz/profile.yaml
.cache/mindgarden-standalone/bin/mindgarden llms --repository-root "$PROOF_STAGE" --write
.cache/mindgarden-standalone/bin/mindgarden verify --repository-root "$PROOF_STAGE"
```

The full canonical holistic profile is still unverified on this draft. The
repository instruction requires a manual exact-head MegaLinter run before
readiness; the maintainer's current instruction prohibits manually launching
paid workflows, so no dispatch was made. This remains a review draft, with
canonical entrypoint acceptance, full-profile evidence, Relay #40 migration and
post-merge deployment explicitly open. No real private archive or model was used.

## Source integration checkpoint — 2026-11-12

The maintainer explicitly authorized merging the open Empathy source changes
while deferring current tests, linters, builds, helper/native qualification, CI
and publication qualification. Deterministic derived-document refresh was
separately authorized for this source integration. The preceding dated focused
results remain bound to their original source; they are not fresh evidence for
the integration head.

The two optional standalone tasks leave the canonical garden, tracked entrypoint,
incubated commands and Pages authority unchanged. The existing canonical command
`python3 tools/task_catalog.py --write --repository-root .`, with `TASK_BIN`
selecting the preinstalled Task 3.54.0 binary, regenerated `TASKS.md` through
Task's list-only JSON interface. The generated region changes only its command
count and the two optional rows; no task, suite, build or native consumer
verification was executed. The strict entrypoint cutover and full acceptance
gaps above remain open after source merge.
