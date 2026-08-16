# README pack provenance

Copyright 2026 Ego Hygiene

SPDX-License-Identifier: MIT

## Promoted source artifacts

The first pack revision was adapted on 2026-08-16 from three user-provided
authoring artifacts:

| Source artifact | SHA-256 | Local disposition |
| --- | --- | --- |
| `README-BASELINE.md` | `a97727877f9d4c06f8e6d6c05332f5b8bb342296c387e48cda39777a30d0095f` | Generalized and tightened as `templates/project/README.md` |
| `README-PROFILE-BASELINE.md` | `bacb8eeb36a8e3b490f2e32bd54e083ea27a34553a5c03f6a29f4ffdf1142bf3` | De-personalized and promoted as `templates/profile/README.md` |
| `README-RESEARCH.md` | `e3259e3aa02f208e2a016f30420535fb6cbb6e92d58ca1264e345dada84ce005` | Preserved with snapshot caveats in `references/research-and-design.md` |

The uploaded source artifacts are not runtime dependencies and are not copied
verbatim into the pack.

## Transformations

- Removed references to temporary `.staging` profile workspaces.
- Replaced person-specific employment, education, name, and contact facts with
  explicit verified-data placeholders.
- Kept the project template comprehensive while marking conditional sections
  and repository-type decisions.
- Formalized the placeholder grammar, generated-region rules, audiences,
  required sections, and validation command in `pack.yaml`.
- Preserved the research corpus counts as a dated source snapshot rather than
  presenting them as continuously current measurements.
- Added an offline validator and repository tests.

## External references

The research brief links to public examples and guidance from GitHub, Awesome
README, Awesome GitHub Profiles, Tilburg Science Hub, SSW Rules, and Best README
Template. Those links are references and inspiration; no third-party source
code or README body is vendored here.

Future updates must record the retrieval date, changed corpus or guidance,
generator/tool version when applicable, and any new license or attribution
requirement.
