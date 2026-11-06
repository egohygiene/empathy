# Standalone Mindgarden consumer checkpoint

Refs #65; parent [Mindgarden #20](https://github.com/egohygiene/mindgarden/issues/20).
This optional consumer lane installs the standalone Python package from immutable
source `a3cbac93d2a68e99e7955ddb18302e0358f53247`, reviewed in
[Mindgarden #95](https://github.com/egohygiene/mindgarden/pull/95). It is an
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
