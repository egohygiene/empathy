# Workflow profile library

This directory contains **disabled GitHub workflow profiles** that were imported
from `.staging/github/` and are not yet safe enough to become active baseline
workflows.

GitHub only executes workflow files located directly in `.github/workflows/`, so
files under this directory are inert by design. They are preserved here because
their capabilities are still useful and must not be lost while Empathy evolves
into the reference repository baseline.

## Promotion model

A profile graduates from this directory only after it has been made
repository-agnostic and split along the normal automation boundary:

1. reusable step-level behavior becomes a composite action under
   `.github/actions/<capability>/`;
2. job orchestration, permissions, matrices, environments, and credentials stay
   in a thin workflow under `.github/workflows/`;
3. automatic triggers are added only when the capability belongs in the
   universal baseline;
4. profile-specific workflows may instead expose `workflow_call` only, which
   keeps them reusable but inert until a repository deliberately calls them.

All promoted automation must use immutable external action pins, explicit token
permissions, job timeouts, safe fork/secret behavior, and the repository's
existing automation validation contract.

## Current promotions

- `agent-environment/copilot-setup-steps.yml` →
  `.github/actions/setup-agent-environment/` +
  `.github/workflows/copilot-setup-steps.yml`.
- `application-flutter/autofix.yml` →
  `.github/workflows/reusable-autofix.yml` with repository-neutral commands and
  setup inputs.
- the common build portion of `application-flutter/release-artifacts.yml` →
  `.github/workflows/reusable-flutter-build.yml`; signing and release-attachment
  policy remains preserved in the disabled source profile until its secret and
  release contracts are generalized.

## Exact duplicates

The following staged files are not copied into this library because identical
canonical blobs already exist in their owning repository:

- `source-specific/aether-pr-validation.yml` →
  `egohygiene/aether/.github/workflows/pr-validation.yml`
  (`9796474af84fdd7926819e4e79db6a564e536fbb`).
- `source-specific/aether-release-first-party-skills.yml` →
  `egohygiene/aether/.github/workflows/release-first-party-skills.yml`
  (`6d9ac607310d394e63ca358f2b9a2423b167169e`).

## Remaining categories

- `agent-environment/` — validation and richer coding-agent tooling.
- `application-flutter/` — Flutter-specific autofix and signed release details.
- `container-platform/` — Realm/container build, publish, benchmark, scan, and
  changelog capabilities.
- `content-and-docs/` — docs, bookmarks, Garden, Pages, image, NSFW, and TOC
  automation.
- `release-strategies/` — Changesets, Release Please, and semantic-release
  alternatives.
- `security-optional/` — optional governance, compliance, secret, SBOM, and
  supply-chain checks.
- `source-specific/` — source-repository automation that still needs a universal
  owner or replacement.

The original `.staging/github/` tree is removed only after every non-duplicate
file has either been promoted or copied here losslessly.
