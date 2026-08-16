# README pack

The README pack is Holon's reusable, evidence-first authoring system for
project and GitHub profile READMEs. It turns repository context and identity
material into a complete front door without treating one giant document as the
correct output for every repository.

## Ownership

- Holon owns template structure, placeholder grammar, profile contracts,
  validation, and source provenance.
- Identity owns logos, banners, palette, typography, and approved voice.
- Each consumer repository owns its facts, commands, compatibility claims,
  screenshots, support channels, and final materialized README.
- Automation may update only bounded generated regions. Human-authored
  narrative remains the source of truth.

## Pack contents

| Artifact | Purpose |
| --- | --- |
| [Project template](templates/project/README.md) | Universal repository baseline with explicit conditional sections |
| [Profile template](templates/profile/README.md) | Trust-first professional and open-source profile structure |
| [Research brief](references/research-and-design.md) | Design rationale, corpus snapshot, patterns, and anti-patterns |
| [Pack manifest](pack.yaml) | Machine-readable template, audience, section, and validation contract |
| [Provenance](PROVENANCE.md) | Checksums and transformation record for the promoted source material |
| [Validator](tools/validate.py) | Offline structural and placeholder-contract validation |

## Instantiation workflow

1. Collect observed repository facts: audience, repository type, maturity,
   supported platforms, primary command, quality gates, proof assets, security
   path, support path, license, and current limitations.
2. Select the project or profile template.
3. Preserve required sections from [`pack.yaml`](pack.yaml). Retain only the
   conditional sections that help the selected audience and repository type.
4. Replace every `{{UPPER_SNAKE_CASE}}` token with verified content.
5. Delete unused instructions, examples, badges, references, and optional
   blocks.
6. Test every published command from a clean environment and check every
   repository-owned link and asset.
7. Validate the materialized README with the consumer's Markdown, link,
   accessibility, and placeholder checks.

The templates are authoring sources, not files to copy unchanged. A small CLI
may need half of the project sections; a service may need operations,
observability, and recovery; a data repository needs method, provenance,
reproducibility, and citation.

## Agent handoff

Any capable authoring tool can use this pack. For a ChatGPT or agent-assisted
pass, provide:

- the repository context layer;
- the selected template;
- the repository type and maturity;
- paths to approved identity assets;
- verified commands and compatibility constraints; and
- evidence for every outcome or professional claim.

Use this request:

> Materialize the selected Holon README template for this repository. Treat the
> supplied repository context as observed state, do not invent claims or
> support guarantees, preserve required sections, retain only useful
> conditional sections, replace every placeholder, bound generated content,
> and return a short verification ledger for commands, links, assets, and
> unresolved evidence.

The final review must distinguish missing evidence from prose quality. An agent
should leave a visible unresolved item rather than converting an assumption
into a published claim.

## Repository-type guidance

| Type | Add or emphasize |
| --- | --- |
| CLI | Install matrix, command synopsis, examples, exit codes, completions, structured output |
| Library or SDK | Minimal import, API stability, compatibility, version policy, migrations |
| Service or API | Deployment, health, configuration, API contract, data flow, observability, recovery |
| Web or mobile app | Live demo, screenshots, environment setup, local run, build, deployment |
| Template or platform | Intended consumers, customization seams, upgrade and synchronization policy |
| Workflow or automation | Inputs, outputs, permissions, secrets, invocation, failure modes, version pinning |
| Data or research | Method, provenance, reproducibility, results, layout, license, citation |
| Monorepo | Workspace map, package responsibilities, shared commands, dependency boundaries |

## Generated regions

Generated content must use stable paired markers with a named owner:

```markdown
<!-- profile:recent-work:START -->
Generated content
<!-- profile:recent-work:END -->
```

Automation may replace only the content between the matching markers. It must
not rewrite neighboring prose or create unbounded feeds.

## Validate the pack

```sh
python3 holon/packs/readme/tools/validate.py
python3 -m unittest tests.test_readme_pack
```

The source templates intentionally contain placeholders. Consumer repositories
must add a materialized-output check that rejects any remaining token before
publication.
