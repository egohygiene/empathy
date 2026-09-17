# Layered gitignore contract

This is the **part 1 proposal** for [Empathy #82](https://github.com/egohygiene/empathy/issues/82).
Review the universal rules and their behavior before adopting them. The
[iteration checkpoint](ITERATION-01.md) records the process and next bounded step.

## Contract record

| Field            | Proposal                                                                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Purpose          | Keep disposable local state out of Git without hiding reasonable source or reviewed artifacts.                                     |
| Consumer path    | `.gitignore`; already required and repository-owned in the foundation catalog.                                                     |
| Applicability    | Universal candidate plus explicitly selected profile rules and justified repository-local rules.                                   |
| Canonical source | [`foundation/ignore/universal.gitignore`](../../../foundation/ignore/universal.gitignore), owned by Empathy.                       |
| Content model    | Curated baseline with explicit profile composition and local additions; composition is not implemented in this part.               |
| Source identity  | Review the source at a commit; no released artifact version or downstream pin exists yet.                                          |
| Local variation  | Narrow project rules and reviewed exceptions; local rules must preserve required protections.                                      |
| Update behavior  | Candidate only. Catalog integration, composition ordering, provenance, preservation, and rollback mechanics remain part 2 work.    |
| Validation       | Actual Git ignore behavior in isolated temporary repositories, including intentionally visible paths and duplicate-rule detection. |
| Adoption         | No golden-root or Filament adoption yet. The existing root `.gitignore` remains active.                                            |

## Universal rule decisions

The candidate has 27 active rules, including negations. It reserves only the
reviewed OS/editor debris, local environment patterns, private `.secrets/`
namespace, and unambiguous `.cache/`, `.tmp/`, `.venv/`, `__pycache__/`, and
`node_modules/` directories. These namespaces are local at every depth.

- Keep shared `.vscode/` and `.idea/` configuration visible. Ignore only the
  named JetBrains user state covered by its
  [version-control guidance](https://intellij-support.jetbrains.com/hc/en-us/articles/206544839-How-to-manage-projects-under-Version-Control-Systems).
- Ignore `.env` and local variants. Allow `.env.example`, `.env.sample`,
  `.env.template`, and variants ending in those three suffixes, including
  `.env.production.example`. Templates contain placeholders, never credentials.
  `.env.example.local` remains ignored. Templates inside `.secrets/` remain hidden.
- Preserve lockfiles, public certificates, binary fixtures, archives, patches,
  screenshots, snapshots, logs used as fixtures, and reviewed reports by default.
- Keep `bin/`, `build/`, `dist/`, `out/`, `target/`, `vendor/`, `coverage/`, and
  similar ambiguous names out of the universal layer. Profile rules require
  evidence of generated output and an appropriate project scope.

The [rule audit](RULE_AUDIT.md) classifies all 176 rules in the existing root at
the recorded revision. Its relocation proposals do not claim that profiles or
narrower secret protections have already been implemented.

## Layering and exceptions

Proposed ownership remains: Empathy owns baseline/profile policy, consumers own
their local facts, Holon owns materialization, EgoLint owns conformance semantics,
Relay runs reusable checks, and Pace owns reviewed fleet convergence.

The next part must define deterministic composition against the existing catalog
and manifest. Avoid concatenating every language's rules into the root. A Rust
project can own `/target/` in its nearest `.gitignore`, without hiding unrelated
`target/` paths elsewhere. Existing profile names are not evidence that ignore
overlays for them already exist.

Git applies directory scope and pattern order, rather than this ownership model:
later matching rules win at the same level, and a closer `.gitignore` can override
ancestor rules. A rule containing an internal slash is relative to its ignore
file; a slashless name can match at any depth. A leading slash anchors the rule
to that ignore file's directory. These are
[Git's documented semantics](https://git-scm.com/docs/gitignore).

To keep a reviewed file inside an otherwise ignored output directory, keep the
parent traversable and ignore its contents. For example, in a selected project's
own `.gitignore`:

```gitignore
/build/*
!/build/README.md
```

Using `/build/` followed by `!/build/README.md` does not work: Git cannot reinclude
files beneath an excluded parent. A global `!**/.gitkeep` has the same limitation.
Document the path, owner, and reason for an exception, and test both the exception
and adjacent generated files. Do not use exceptions to expose private local state.

## Secret boundary and migration gate

Ignore rules do not remove already tracked files, prevent forced additions, or
detect secrets. The behavior checks deliberately demonstrate that a nested
`!.env` can bypass a root rule. A future conformance check must detect prohibited
overrides; this candidate does not enforce that policy by itself.

Before replacing the active root, account for every current credential rule.
For `*.key`, keystores, certificates, `*.secrets.*`, and infrastructure state or
variables, identify the real private locations, add narrow profile/local rules,
and test them alongside public/fixture exceptions. Use `.secrets/` for deliberate
private local material; it does not cover secrets stored arbitrarily elsewhere.
Keep secret scanning as a separate protection. Do not drop existing protections
merely because an extension is absent from the universal candidate.

Migration must inspect untracked files newly exposed by changed rules without
printing their contents or staging them wholesale. An ignored file is never
evidence that deletion is safe. No cleanup is required by this proposal.

## Validation

Run from the repository root:

```bash
python3 -m unittest discover \
  --start-directory tests \
  --pattern "test_gitignore_baseline.py" \
  --verbose
```

The harness installs the candidate into temporary Git repositories, creates
real untracked fixtures, and uses `git check-ignore --no-index`. Failures include
the winning rule via `--verbose`. It isolates Git configuration, inherited Git
environment overrides, templates, and global excludes. The full automation test
job also runs these tests when the candidate changes.

Nested examples prove Git semantics; they are not released profile fixtures or
golden-consumer proof. Catalog/manifest validation, profile composition,
generated inventory and contract checks, and root adoption remain required to
finish #82. Filament follows an accepted, immutable upstream contract.
