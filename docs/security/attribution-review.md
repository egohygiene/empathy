# Attribution fallback checkpoint

This addresses [#117](https://github.com/egohygiene/empathy/issues/117) under
[#118](https://github.com/egohygiene/empathy/issues/118). The repository's MIT
license is not evidence that retained third-party files are first-party MIT.

## Reviewed mappings

The first-party fallback now covers only `foundation/**` and
`docs/foundation/**`: the catalog declares Empathy ownership, and the foundation
guide defines those baseline composition sources. Existing SPDX headers on
other maintenance source remain authoritative without a root-wide annotation.
Unmapped source receives no substitute license or author merely by containment.

Two file-specific license declarations use the retained package README and
adjacent LICENSE as evidence:

| File | Declared license | Attribution and limit |
| --- | --- | --- |
| `beacon/.staging/latex/CVs and Resumes/Deedy-Resume/README.md` | Apache-2.0 | Original inline Debarghya Das notice remains; no first-party notice is added. |
| `beacon/.staging/latex/Community/TeXtured/README.md` | CC0-1.0 | No unsupported author is invented. The README names asset exceptions, so this mapping covers only that README. |

The existing package license texts are copied verbatim into `LICENSES/` for
REUSE discovery. Package files, embedded notices and sampled emoji bytes are
unchanged. The two sampled Noto outputs now have missing metadata, which is
**unresolved**, not a permissive license, clean scan or permission to distribute.

## Evidence and regression

The [recorded sample inspection](data/attribution-2026-11-13.json) binds the
actual REUSE 6.2.0 metadata, source base, policy hash and unchanged sample hashes.
Three executed regressions cover those real samples, new unknown intake under
several owner roots, reviewed baseline coverage and preserved explicit headers.
Use the already declared EgoLint REUSE dependency; a missing tool produces an
explicit test skip and cannot satisfy this issue's qualification.

```sh
python -m unittest discover --start-directory tests --pattern test_attribution.py --verbose
```

No full-corpus REUSE pass or rights determination is claimed. Removing the
unsupported fallback deliberately exposes missing provenance; do not suppress
those results to produce a badge.

## Retained review queue

| Retained class | Owner and existing follow-up | Remaining evidence |
| --- | --- | --- |
| Root `.staging/**` source and generated emoji | Destination capability owner from the staging ledger; Empathy [#79](https://github.com/egohygiene/empathy/issues/79), with supply-chain tracking in [#51](https://github.com/egohygiene/empathy/issues/51). | Immutable upstream/per-output manifest, original notices, reviewed source/license identity and destination acceptance. No blanket first-party metadata. |
| Nested `beacon/.staging/**` packages | Beacon's canonical owner; retained intake coordinated in [#79](https://github.com/egohygiene/empathy/issues/79). | Package/asset exception review and immutable origin before promotion. The two README corrections do not qualify entire packages. |
| Active specialist copies and generated outputs | Declared specialist owner under [ADR-0001](../decisions/ADR-0001-foundation-ownership.md); reconciliation remains in #79. | Preserve existing headers and source identity; review any missing metadata and unique deltas before replacement or retirement. |
| Other root files outside the verified fallback | Empathy or the file's recorded owner; #117/#79. | File-specific source/notice evidence; absence of a mapping stays unresolved. |

Attribution, scanner findings, immutable provenance, migration approval and
distribution rights are separate states. This checkpoint grants no source
removal or promotion authority and does not complete the retained corpus review.

ADR disposition: existing ADR-0001 applies. These corrections reflect declared
source metadata without selecting a new ownership or organization licensing
policy, changing human authority or authorizing distribution.
