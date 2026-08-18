# GitHub Issue: Build Flow as the unified orchestration layer for the Ego Hygiene media-processing suite

## Suggested title

`feat: build Flow as a resumable orchestration layer for Aniflow, Optiflow, and Renderflow`

## Summary

Create the first working version of **Flow**, the unified command-line facade and orchestration layer for the Ego Hygiene media-processing tool suite.

Flow must compose the independently releasable `aniflow`, `optiflow`, and `renderflow` tools into reproducible, observable, resumable pipelines without merging their repositories or making them depend directly on one another.

The first vertical slice must accept a source video, execute a real end-to-end restoration/processing/optimization pipeline using the capabilities that actually exist in the three tools, and produce a validated output video plus a complete artifact bundle and run report.

## Product intent

The user should be able to treat several specialized Ego Hygiene tools as one coherent suite:

    flow process "input.mp4" \
      --pipeline "restore-and-optimize" \
      --output-directory "./artifacts"

Flow should answer:

- Which compatible tools are installed?
- Which stages will run, in what order, and why?
- What inputs and outputs belong to each stage?
- What progress has been made?
- Can an interrupted run resume safely?
- Which exact tool versions and configuration produced an artifact?
- Did the final output preserve the intended streams and satisfy validation?
- If a stage failed, what completed successfully and how can the user continue?

## Architectural boundary

Treat every participating tool as an independent **holon**: a complete, useful tool on its own that can also participate in a larger system.

The dependency direction must remain:

    flow
      -> invokes aniflow
      -> invokes optiflow
      -> invokes renderflow

    aniflow     independent
    optiflow    independent
    renderflow  independent

Do **not**:

- Move the three tools into the Flow repository.
- Convert the organization into a monorepo.
- Make Aniflow depend on Optiflow or Renderflow.
- Make Optiflow depend on Aniflow or Renderflow.
- Make Renderflow depend on Aniflow or Optiflow.
- Couple Flow to private implementation details of another tool.
- Begin with cross-repository Rust library dependencies.
- Reimplement processing capabilities already owned by a participating tool.
- Hide subprocess invocation behind unstructured console parsing.

For the initial implementation, integrate through explicit CLI subprocess adapters and structured, versioned JSON contracts. Preserve the possibility of native library integration later, but do not require it for this milestone.

## Source repositories

Inspect the current default branches, documentation, command help, machine-readable output, tests, and release metadata for:

- `egohygiene/aniflow`
- `egohygiene/optiflow`
- `egohygiene/renderflow`

Do not infer responsibilities solely from repository names. Record the capabilities that actually exist at implementation time, including gaps that block the desired pipeline.

If one tool cannot yet perform an expected stage, do not silently emulate it inside Flow. Document the missing contract, add a clear adapter capability status, and either:

1. Select a supported stage path that still produces a valid first vertical slice; or
2. Stop with an actionable compatibility error and record the required upstream follow-up.

## Required discovery artifact

Before implementing orchestration behavior, create:

`docs/integrations/capability-matrix.md`

For each tool, record:

- Repository and inspected revision
- Current package/release version
- Installation and executable discovery method
- Supported input and output types
- Relevant commands and long-form arguments
- Machine-readable output support
- Progress-reporting behavior
- Exit-code behavior
- Configuration format
- Resumability or checkpoint support
- Artifact and metadata outputs
- Error and partial-success behavior
- Capabilities suitable for the first pipeline
- Contract gaps or upstream changes required

Use this matrix to determine which tool owns each pipeline stage.

## First end-to-end pipeline

Implement a built-in pipeline named `restore-and-optimize`.

Its logical lifecycle is:

    source video
      -> inspect and fingerprint
      -> plan compatible stages
      -> extract or decompose media when required
      -> process or repair supported components
      -> reassemble when required
      -> normalize and optimize
      -> validate final media
      -> emit artifacts, provenance, and reports

The exact assignment of stages to Aniflow, Optiflow, and Renderflow must follow the capability matrix rather than assumptions in this issue.

The pipeline must:

- Preserve the original input without modification.
- Use a dedicated run workspace beneath the selected output directory.
- Generate a deterministic plan before execution.
- Validate stage prerequisites before doing expensive work.
- Avoid repeating a completed valid stage when resuming.
- Preserve useful intermediate artifacts by policy.
- Produce a final playable media output when all required stages succeed.
- Validate video, audio, duration, dimensions, frame rate, container, and expected stream presence as applicable.
- Report intentional transformations and unexpected deviations.

## Proposed repository structure

Adapt names to existing project conventions when necessary, but preserve these responsibilities:

    flow/
    ├── Cargo.toml
    ├── README.md
    ├── schemas/
    │   ├── artifact-manifest.schema.json
    │   ├── pipeline.schema.json
    │   └── tool-result.schema.json
    ├── pipelines/
    │   └── restore-and-optimize.yml
    ├── src/
    │   ├── cli/
    │   ├── adapters/
    │   │   ├── aniflow.rs
    │   │   ├── optiflow.rs
    │   │   └── renderflow.rs
    │   ├── artifacts/
    │   ├── configuration/
    │   ├── diagnostics/
    │   ├── execution/
    │   ├── pipeline/
    │   ├── planning/
    │   ├── progress/
    │   ├── validation/
    │   └── main.rs
    ├── tests/
    │   ├── fixtures/
    │   ├── integration/
    │   └── end_to_end/
    └── docs/
        ├── architecture.md
        ├── artifact-layout.md
        ├── pipeline-authoring.md
        └── integrations/
            └── capability-matrix.md

If Flow already has an established structure, integrate cleanly rather than mechanically replacing it.

## CLI requirements

Provide an explicit, scriptable command surface. At minimum:

    flow doctor [--format "human|json"]

    flow inspect <input> [--format "human|json"]

    flow plan <input> \
      --pipeline <name-or-path> \
      [--output-directory <path>] \
      [--format "human|json"]

    flow process <input> \
      --pipeline <name-or-path> \
      --output-directory <path> \
      [--resume] \
      [--keep-intermediates <policy>] \
      [--format "human|json"]

    flow status <run-directory> [--format "human|json"]

    flow validate <run-directory-or-output> [--format "human|json"]

    flow diagnostics <run-directory> \
      --output <archive-path> \
      [--redact-paths]

CLI behavior must include:

- Long-form argument names in documentation and examples.
- Stable, documented exit codes.
- Human-readable output by default.
- Versioned JSON output for automation.
- No ANSI control sequences when output is non-interactive or JSON is requested.
- Clear distinction among validation failure, missing dependency, incompatible dependency, stage failure, partial completion, and internal failure.
- A `--dry-run` or equivalent planning-only mode for `process` if it adds value beyond `flow plan`.

Do not accept ambiguous silent fallback. If a configured tool, pipeline, codec, or stage is unsupported, explain exactly what is missing and how to resolve it.

## Tool adapter contract

Define one internal adapter interface implemented consistently for all three tools. It should support, as applicable:

- Executable discovery
- Version probing
- Compatibility evaluation
- Capability probing
- Invocation planning
- Environment construction
- Structured argument construction
- Subprocess execution
- Progress/event translation
- Cancellation and signal forwarding
- Exit-code interpretation
- Structured-result parsing
- Output verification
- Redacted diagnostics

Never construct subprocess commands through a shell string when a direct argv-based process API is available.

Capture stdout and stderr independently. Preserve raw logs in the run directory, but keep user-facing summaries concise. Treat nonzero exits, signals, invalid JSON, missing declared artifacts, and output validation failures as distinct errors.

If an upstream CLI lacks a sufficient JSON mode, add a narrowly scoped compatibility parser with tests and document the upstream contract required to remove it. Do not rely on fragile parsing without an explicit warning in the capability matrix.

## Pipeline definition contract

Create a versioned declarative pipeline schema. A pipeline must be able to declare:

- Schema version
- Pipeline identifier, title, and description
- Accepted input media types
- Ordered stages
- Stage dependencies
- Tool and capability requirements
- Stage configuration
- Declared inputs and outputs
- Conditional execution
- Retry policy
- Resume/checkpoint policy
- Intermediate-retention policy
- Validation rules
- Final artifact selection

Reject unknown or unsupported schema versions with an actionable error. Validate the complete pipeline before execution.

Do not create an unrestricted arbitrary-command runner. Pipeline stages must resolve through registered, typed adapters and supported capabilities.

## Artifact manifest contract

Every run must produce a machine-readable, versioned artifact manifest, for example:

    schema_version: 1
    run_id: "2026-08-07T210000Z-example"
    status: "completed"

    source:
      original_path: "input.mp4"
      fingerprint:
        algorithm: "sha256"
        value: "..."

    pipeline:
      id: "restore-and-optimize"
      definition_digest: "sha256:..."

    tools:
      aniflow:
        executable: "aniflow"
        version: "..."
      optiflow:
        executable: "optiflow"
        version: "..."
      renderflow:
        executable: "renderflow"
        version: "..."

    stages:
      - id: "inspect"
        status: "completed"
        started_at: "..."
        completed_at: "..."
        inputs: ["source"]
        outputs: ["source-metadata"]

    artifacts:
      - id: "final-video"
        type: "video"
        relative_path: "outputs/final.mp4"
        producer_stage: "optimize"
        fingerprint: "sha256:..."
        media_metadata: {}

The final schema may be JSON-backed even when examples or configuration use YAML.

The manifest must record:

- Source fingerprint and relevant source metadata
- Pipeline identifier, schema version, and definition digest
- Flow version
- Participating tool executables and versions
- Effective configuration with secrets removed
- Stage state, timing, inputs, outputs, and errors
- Artifact paths relative to the run directory
- Artifact types, fingerprints, producers, and validation results
- Final run status
- Warnings, deviations, and partial results

Use atomic writes so a crash cannot leave a manifest that falsely appears complete.

## Run directory and checkpointing

Use a predictable self-contained layout similar to:

    artifacts/
    └── <run-id>/
        ├── manifest.json
        ├── plan.json
        ├── effective-config.json
        ├── checkpoints/
        ├── inputs/
        ├── intermediates/
        ├── outputs/
        ├── logs/
        ├── reports/
        └── diagnostics/

Checkpoint validity must be based on more than the presence of a file. Include source fingerprints, stage configuration digest, tool version, declared input fingerprints, completion status, and output validation.

When `--resume` is requested:

- Reuse only checkpoints proven compatible and complete.
- Explain which stages are reused and which are invalidated.
- Invalidate a stage and its dependents when relevant inputs, configuration, pipeline definition, or tool compatibility changes.
- Never overwrite a valid original artifact silently.
- Preserve enough state to diagnose a previously failed stage.

## Planning and compatibility

`flow plan` must resolve the pipeline into an executable plan without doing expensive media processing. It should report:

- Resolved stages and dependencies
- Tool selected for each stage
- Tool versions and compatibility
- Expected inputs and outputs
- Missing capabilities or executables
- Effective configuration
- Estimated operations when reliable estimates are available
- Checkpoints eligible for reuse
- Validation that will run

Introduce a small compatibility policy for supported tool versions. Prefer explicit tested version ranges and actionable warnings over an indefinite claim of universal compatibility.

If practical, add a generated `FLOW.lock` or equivalent run-specific lock data that records the resolved toolchain and pipeline digest. Do not invent a package-manager lockfile; document its purpose and regeneration behavior clearly.

## Failure handling and progress

Provide unified stage-oriented progress while preserving upstream detail:

- Planned
- Preparing
- Running
- Validating
- Completed
- Skipped
- Failed
- Cancelled

On interruption, forward termination signals safely, allow the active child process a bounded graceful shutdown, persist the run state, and leave the workspace resumable when possible.

A failed run must still emit a useful manifest and partial-run report containing:

- Failed stage
- Interpreted reason
- Underlying tool and exit information
- Completed stages and reusable checkpoints
- Available artifacts
- Exact resume command
- Suggested remediation

## Configuration

Provide layered, typed, versioned configuration with an explainable effective result. At minimum consider:

1. Built-in defaults
2. Project or user configuration, if supported
3. Pipeline definition
4. Command-line overrides

Document precedence. `flow plan` and run artifacts must expose the effective configuration with secrets and sensitive paths redacted appropriately.

Avoid adding configuration surface solely for hypothetical future needs. Implement the options required by the first real pipeline and preserve schema extensibility.

## Validation

Validation must occur at three levels:

### Preflight

- Input exists, is readable, and has a supported media type.
- Output location is writable and does not conflict unsafely.
- Required tools are discoverable.
- Tool versions and capabilities are compatible.
- Pipeline and configuration schemas are valid.
- Required codecs, models, or external assets are available when applicable.
- Disk-space requirements are checked when a reliable estimate is possible.

### Stage outputs

- Declared artifacts exist.
- Outputs are nonempty and decodable where applicable.
- Fingerprints and metadata are recorded.
- Dimensions, frame count, duration, streams, or other invariants satisfy the stage contract.

### Final output

- Output container is readable and playable by a probing tool.
- Required video and audio streams are present.
- Duration deviation is within a documented tolerance unless intentionally transformed.
- Dimensions and frame rate match the intended pipeline result.
- No temporary path is accidentally referenced.
- Manifest and final validation report agree.

## Security and privacy

- Invoke tools without shell interpolation.
- Validate paths and prevent directory traversal from pipeline or tool results.
- Prevent artifacts from escaping the selected run directory unless explicitly configured.
- Treat media and pipeline files as untrusted inputs.
- Do not execute arbitrary commands from pipeline definitions.
- Redact environment secrets, credentials, tokens, and unnecessary absolute user paths from reports.
- Make diagnostic bundles privacy-safe by default and document exactly what they contain.
- Never upload media or metadata unless a future explicit feature requires and discloses it.

## Testing requirements

Add deterministic tests at the appropriate levels.

### Unit tests

- Pipeline schema parsing and validation
- Artifact manifest serialization and migration/version rejection
- Configuration precedence
- Tool version parsing and compatibility decisions
- Process-result and exit-code interpretation
- Path normalization and containment
- Checkpoint compatibility and invalidation
- Redaction
- Execution-plan ordering

### Adapter contract tests

Create fake executables or controlled fixtures for each adapter to test:

- Discovery
- Compatible and incompatible versions
- Successful structured output
- Nonzero exit
- Signal termination
- Malformed JSON
- Missing declared output
- Partial success
- Progress translation

Do not require the real heavyweight media toolchain for the majority of tests.

### Integration tests

- Plan a complete built-in pipeline.
- Execute a small deterministic fixture through mocked or lightweight adapters.
- Resume after a simulated mid-pipeline failure.
- Invalidate the correct stages after input, configuration, or version changes.
- Produce and validate the expected run directory and artifact manifest.

### End-to-end smoke test

Provide an opt-in test that uses the real compatible Aniflow, Optiflow, and Renderflow executables with a tiny redistribution-safe media fixture. Skip with an explicit reason when dependencies are unavailable.

The test must verify the command exit status, final media probe, manifest, stage state, provenance, and resume behavior.

## Documentation and developer experience

Update `README.md` with:

- What Flow is and is not
- Relationship to Aniflow, Optiflow, and Renderflow
- Architecture and dependency direction
- Installation prerequisites
- Quick-start example
- Planning before processing
- Artifact layout
- Resume workflow
- JSON automation examples
- Diagnostic workflow
- Current compatibility policy
- Known limitations

Create or update:

- `docs/architecture.md`
- `docs/artifact-layout.md`
- `docs/pipeline-authoring.md`
- `docs/integrations/capability-matrix.md`

Include generated shell completions and a man page if the repository's current CLI framework supports them without destabilizing the first vertical slice; otherwise record them as a focused follow-up.

## CI and quality gates

Add or extend CI so that pull requests validate:

- Formatting
- Linting with warnings treated according to repository policy
- Unit tests
- Adapter contract tests
- Integration tests
- JSON Schema validation
- Documentation examples or command-help snapshots where practical
- Dependency and supply-chain checks consistent with the Ego Hygiene organization
- Linux and macOS behavior for path, process, and filesystem-sensitive code

Keep real heavyweight end-to-end processing opt-in or scheduled if it is too expensive for every pull request, but ensure the lightweight orchestration path runs on normal CI.

## Implementation sequence

Work in this order and keep commits logically reviewable:

1. Inventory the Flow repository and the three source tools.
2. Produce the capability matrix and identify contract gaps.
3. Document the architecture and concrete first-pipeline stage ownership.
4. Define versioned pipeline, tool-result, and artifact-manifest schemas.
5. Implement CLI scaffolding, configuration, and stable exit behavior.
6. Implement tool discovery, version probing, and adapter contracts.
7. Implement deterministic planning and preflight validation.
8. Implement execution, progress, logs, state persistence, and cancellation.
9. Implement artifact collection, manifest updates, validation, and reporting.
10. Implement checkpoint compatibility and resume behavior.
11. Add the built-in `restore-and-optimize` pipeline.
12. Add tests, fixtures, CI, and documentation.
13. Run the real end-to-end vertical slice and capture evidence in the PR.

If implementation discovers that an upstream repository needs a change, document a proposed upstream issue with:

- Repository
- Missing contract or capability
- Minimal change requested
- Compatibility implications
- Tests required

Do not broaden this PR into simultaneous unreviewable rewrites of all four repositories.

## Acceptance criteria

- [ ] Flow is implemented as an orchestrator and suite facade, not as a monorepo or replacement for the three tools.
- [ ] Aniflow, Optiflow, and Renderflow remain independent and have no new direct dependencies on one another.
- [ ] `docs/integrations/capability-matrix.md` records verified current capabilities and inspected revisions.
- [ ] A versioned, validated pipeline schema exists.
- [ ] A versioned, validated tool-result schema exists.
- [ ] A versioned artifact-manifest schema exists.
- [ ] `flow doctor` reports tool discovery, versions, capabilities, and compatibility in human and JSON formats.
- [ ] `flow inspect` fingerprints and describes a source media file without modifying it.
- [ ] `flow plan` produces a deterministic executable plan without performing expensive processing.
- [ ] `flow process` executes the built-in `restore-and-optimize` pipeline through typed tool adapters.
- [ ] Every run uses an isolated, self-contained run directory.
- [ ] Every run emits a plan, effective configuration, logs, reports, checkpoints, and artifact manifest.
- [ ] The original source is never modified.
- [ ] Tool invocations use safe argv-based subprocess execution rather than shell interpolation.
- [ ] Stage progress and final status are available in human-readable and machine-readable forms.
- [ ] Failures preserve partial artifacts, actionable diagnostics, and an exact resume path.
- [ ] `--resume` reuses only verified compatible checkpoints.
- [ ] Changes to relevant inputs, pipeline definitions, configuration, or tool versions invalidate the correct stages.
- [ ] Final output is probed and validated against documented invariants.
- [ ] A privacy-safe diagnostic bundle can be generated.
- [ ] Unit, adapter-contract, integration, and opt-in real-tool end-to-end tests exist.
- [ ] CI validates the lightweight orchestration path on Linux and macOS.
- [ ] Documentation explains installation, architecture, pipeline authoring, artifact layout, compatibility, processing, validation, and recovery.
- [ ] The PR includes the exact commands and summarized evidence from one successful real end-to-end video run.

## Definition of done

This issue is complete when a user can install or locate compatible versions of the three tools and successfully run:

    flow doctor

    flow plan "input.mp4" \
      --pipeline "restore-and-optimize" \
      --output-directory "./artifacts"

    flow process "input.mp4" \
      --pipeline "restore-and-optimize" \
      --output-directory "./artifacts"

The completed run must produce:

- A validated final video
- A machine-readable artifact manifest
- A human-readable run report
- Tool and pipeline provenance
- Stage logs and validation results
- Recoverable intermediate state
- A demonstrated resume path

The implementation should establish the smallest durable contract that lets future pipelines compose Ego Hygiene tools without sacrificing their independence.

