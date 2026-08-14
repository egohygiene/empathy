# Installer assurance

Mantle resolves installer inputs through
[`config/installers.lock.tsv`](config/installers.lock.tsv). The registry is the
machine-readable source of truth used by installer execution, dry runs, tests,
and the public assurance view:

```sh
mantle install --assurance
mantle install --assurance eza
```

## Assurance model

| Resolution class | Default behavior | Integrity signal |
| --- | --- | --- |
| GitHub release | Exact release version from the registry | Upstream release checksum when published |
| Python, Ruby, or npm package | Exact package version from the registry | Package-manager transport and artifact validation |
| Git source | Exact commit SHA from the registry | Git commit identity |
| Remote installer script | Exact commit URL from the registry | Registry-pinned SHA-256 |
| Native package | Version selected by the active system package manager | Package-manager repository metadata |

`manager` is an intentional boundary, not a claim of reproducibility. Native
repositories differ by operating system, distribution release, architecture,
and update state. The assurance output labels those entries honestly instead of
inventing a cross-platform version lock Mantle cannot enforce.

## Fail-closed behavior

- Omitting `--version` or `--ref` selects the checked-in lock, never a live
  `latest`, `main`, `master`, or `HEAD` lookup.
- Well-known mutable selectors are rejected even when supplied explicitly.
- GitHub release installers without an upstream checksum refuse installation
  unless the caller explicitly supplies `--no-verify`. Their dry runs remain
  available and label the required opt-out.
- The Linuxbrew bootstrap is pinned to both a commit-specific URL and SHA-256.
- Explicit version and immutable ref overrides remain available for deliberate
  testing or upgrades and are labeled `explicit` in supported dry runs.

## Updating locks

Treat a lock refresh as a reviewed code change:

1. Confirm the upstream release, package, or commit from its authoritative
   registry.
2. Update the affected row in `config/installers.lock.tsv`.
3. For a remote script, also calculate and update its digest.
4. Run the installer's dry run and the complete Mantle test suite.
5. Review the assurance diff separately from unrelated environment changes.

The contract suite requires every discovered installer to have a registry row,
rejects duplicate component records and mutable exact locks, and verifies that
GitHub checksum declarations agree with the published assurance level.
