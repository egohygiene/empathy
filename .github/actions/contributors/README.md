# Generate contributors

This action queries every page of GitHub's contributors API, updates the current
repository identity in `.allcontributorsrc`, and regenerates
`CONTRIBUTORS.md` with a pinned All Contributors CLI.

The caller must:

1. Check out the target branch.
2. Grant `contents: read` while generating metadata.
3. Commit changes separately if desired.

```yaml
- name: Generate contributor documentation
  uses: ./.github/actions/contributors

- name: Commit contributor changes
  uses: ./.github/actions/commit-if-changed
  with:
    paths: |
      .allcontributorsrc
      CONTRIBUTORS.md
    commit-message: "docs(contributors): refresh contributor metadata"
```

Separating generation from publication keeps pull-request, scheduled, and local
callers free to choose their own write policy.
