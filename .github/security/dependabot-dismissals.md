# Dependabot dismissal register

This register records the rationale previously used for dependency exceptions
and identifies the review still required under
[Empathy #113](https://github.com/egohygiene/empathy/issues/113). It is not a
scanner suppression mechanism or a live query of hosted Dependabot alerts.
GitHub manages alert state separately;
[`osv-scanner.toml`](../../osv-scanner.toml) contains the nine configured OSV IDs.
The two policies must be reconciled against actual current evidence before
claiming they are equivalent.

## Source-bound review checkpoint

Static inspection source: `058d92a0f8c970f98a58d446408716936e593c99`.
No registry request, vulnerability audit, install, or scanner was run for this
checkpoint. Existing OSV policy IDs and reason strings remain unchanged. Their
historical statements about unpublished releases and production exclusion are
not freshly verified approvals.

The [dependency checkpoint](../../docs/security/dependency-coverage.md) binds
the native and normalized OSV receipts to source
`18d22e113e87c306b76d24873841249d41358c77`, generated
`2026-11-11T11:34:05Z`. Scanned input blobs and the suppression policy match
the inspection base. The nine configured IDs do not occur in native advisory
groups; that absence is consistent with suppression and cannot validate the
exception or establish that the installed packages are unaffected.

## Configured IDs requiring renewed review

| Package and locked version | Advisory IDs | Retained paths and owner | Historical rationale, unverified now | Review boundary |
| --- | --- | --- | --- | --- |
| `decompress@4.2.1` | `GHSA-mp2f-45pm-3cg9`, `GHSA-h39j-r5qq-r9mm`, `GHSA-jwp9-9v96-94mx` | Root and `egolint/pnpm-lock.yaml`; ShellCheck development-tool chain. Empathy owns the root graph, EgoLint owns reusable tooling. | Prior policy says the advisory-declared `4.2.2` was unpublished. Recheck registry publication, parent-chain alternatives, and actual command exposure. | Next dependency refresh, upstream change, or `2026-11-19`, whichever comes first; before #113 acceptance. |
| `image-size@2.0.2` | `GHSA-w3rx-r6r6-pgpr`, `GHSA-5p2g-fcmc-qvqq` | Root and `egolint/pnpm-lock.yaml`; Docusaurus MDX tooling chain. Empathy/EgoLint ownership as above. | Prior policy says `2.0.3` was unpublished. The register previously omitted these configured IDs; no new suppression is added here. | Same review boundary; verify publication and supported parent upgrade, then remove obsolete exceptions. |
| `ecdsa@0.19.2` | `GHSA-wj6h-64fc-37mp`, `PYSEC-2026-1325` | `egolint/uv.lock`; Checkov security-tool dependency. Canonical owner: EgoLint; Empathy owns consumption. | Prior policy records no published PyPI fix. Review current alias equivalence, registry state and P-256 use in actual invoked tooling; development classification does not establish non-exposure. | Same review boundary; owner remedy and reviewed immutable consumer adoption under #110/#79. |
| `httpie@3.2.4` | `GHSA-8r96-8889-qg2x`, `PYSEC-2023-242` | `egolint/uv.lock`; direct `dev` group tool. Canonical owner: EgoLint; Empathy owns consumption. | Prior policy records no published PyPI fix. The register previously omitted these IDs; inspect actual TLS/network invocation and upstream publication before renewing rationale. | Same review boundary; owner remedy and reviewed immutable consumer adoption under #110/#79. |

The review date is a required evidence checkpoint, not an automatic scanner
expiry or a renewed risk acceptance. No path-specific enforcement is implied:
the current OSV configuration ignores IDs globally. Newly observed paths,
changed aliases, and different package versions require applicability review;
this table cannot authorize extending an exception to them.

Do not add broad package or ecosystem dismissals. Record exact IDs and aliases,
source/lock identity, canonical owner, affected tool invocation, observed
registry/advisory evidence and a concrete reopening condition. Remove an
obsolete exception when a supported remedy exists, then obtain fresh native
and normalized scanner evidence. Until that review occurs, these four package
cases remain unresolved investigations under #113, not current assertions that
no fix exists or that development tooling is safe.
