# Baseline validation checkpoint

Empathy owns repository-baseline evidence under
[ADR-0001](decisions/ADR-0001-foundation-ownership.md). This checkpoint addresses
the local repair slice of [#109](https://github.com/egohygiene/empathy/issues/109),
under [#118](https://github.com/egohygiene/empathy/issues/118).

## Independently retained unittest commands

The automation workflow invokes `tools/baseline_tests.py` after its existing
automation validator and locked PyYAML installation. The helper attempts both
fixed discovery commands in separate Python interpreters, even when the first
returns a nonzero exit code, cannot launch, or reaches its five-minute limit:

```bash
python3 tools/baseline_tests.py --output-directory /path/to/disposable-results
```

Each suite retains its verbose output in `repository.log` or `egolint.log`.
`results.json` records the actual exit code or an explicit unavailable reason;
`summary.md` presents both outcomes. The workflow appends that summary to the
step summary and retains this bounded result directory as an ordinary artifact
for 14 days, including after suite failure. Any failed or unavailable command
fails the aggregate. Setup failure or cancellation can prevent command execution;
an absent artifact is not successful evidence. The existing 15-minute job timeout
still applies, so upstream setup time can also prevent complete retention.

A zero command exit is **not full acceptance**. Unittest's own verbose logs retain
actual counts and environment skips; the helper does not invent counts, convert
skips into passes, or certify that required owner scenarios ran. The JSON records
`acceptance: unqualified` even when both commands succeed. Before acceptance,
provide the declared owner inputs, inspect every skip, and independently prove
each required scenario. The two-process boundary also prevents one discovery's
module state from leaking into the other suite.

## Python and toolchain repair

The commit-policy fixture accepts a reviewed immutable setup-node SHA rather
than freezing an unrelated historical action revision. It also checks the Node
version and package-manager selection against the current EgoLint package
declaration, locked dependency installation without lifecycle scripts, the local
commitlint configuration, and exact pull-request base/head bindings. This slice
does not upgrade or roll back those workflow inputs.

The Task catalog adapter validates the JSON fields it consumes into typed Task
records. Missing or null aliases become an empty array; malformed names,
descriptions, aliases, duplicate task names, or a missing tasks array fail instead
of becoming misleading Markdown. Task remains the source of command discovery;
the adapter does not copy lint policy or execute a caller-supplied shell command.

Subprocess observations have narrow source dispositions: the suite runner uses
the active Python interpreter and fixed discovery argv; Task discovery resolves
the explicit operator-selected Task executable and uses fixed argv; the Identity
fixture invokes the pinned owner's validator and an explicitly required Cargo
executable. All execute without a shell. Inline Ruff/Bandit annotations cover
only those reviewed import/call sites. Canonical EgoLint configurations remain
unchanged. Identity's owner inputs, skips, generated contract, and frozen hashes
remain unchanged.

## Deferred qualification and separate owners

This change was prepared with source and syntax review only. No unittest suite,
Task discovery, Identity validator, Cargo command, formatter, linter, application,
build, or CI workflow was executed for this checkpoint. Authored regressions are
unexecuted; the October audit's historical test and diagnostic counts are not
current results.

Required follow-up evidence remains:

- Execute both suites with declared owner inputs and resolve every required
  scenario skip; inspect the independently retained logs.
- Run canonical Ruff/format, strict Mypy, Bandit, Secretlint, Lychee, and the
  exact-head holistic procedure required by `AGENTS.md`. Source annotations are
  reviewed dispositions, not proof of a clean diagnostic run.
- Keep the root Cargo workspace/profile decision under
  [#79](https://github.com/egohygiene/empathy/issues/79); this slice does not change
  root Cargo membership or absorb unfinished specialist Rust source.
- Keep lint-runtime/tool-catalog adoption under
  [#110](https://github.com/egohygiene/empathy/issues/110), and staging gate/helper
  changes under [#112](https://github.com/egohygiene/empathy/issues/112).

Decision disposition: **no new ADR required**. This is a repository-local evidence
adapter and fixture repair within ADR-0001's existing Empathy baseline ownership;
it does not move reusable policy or specialist implementation ownership. #109
remains an acceptance issue until its deferred evidence and profile disposition
are reviewed.

## Source integration — 2026-11-12

The source merge composes the already merged optional Mindgarden lane, typed
Intelligence feed and approved Actions update. Existing automation prerequisites
and the current Harden Runner pin are retained. The deterministic Task catalog
refresh recorded under PR120 was list-only source generation; it did not run
these suites or qualify the new typed adapter. All test/lint/native and
required-scenario acceptance gates above remain unexecuted for this integration.

## Executed qualification and repairs — 2026-11-13

The [source-bound result](evidence/2026-11-13-baseline-validation.json) records
actual local commands after the merged attribution correction, using Python
3.12.14, Task3.54.0, Cargo1.97.1, exact Relay `d7c60473626f8dcc901210a208ad01a6474e8c1d`
and Identity `481e284a77e0a7cc3bf25f40dc91a71120d036ef`.

The initial equipped run exposed stale capture-clock/retention fixtures and
missing disposable Identity output. The workflow fixtures now exercise current
capture and no-capture paths, seven-day source/review retention separately from
30-day publication evidence, and failed/cancelled/skipped/unavailable source and
review uploads. Publication guards and frozen recovery bytes were not changed.

Identity source validation and `v1-generate` created 26 disposable projections,
then the suite verified the generated package. No generated assets are added to
source. The repository command now passes **224 tests with zero skips**.
The independent embedded EgoLint command runs **31 tests**, with **one retained
catalog/runtime pin failure** owned by #110. The runner correctly returns a
failing aggregate and `acceptance: unqualified`; no owner test is suppressed.

Canonical Ruff check/format, strict Mypy and Bandit pass for the six changed
baseline files. The changes resolve actual malformed-input exception typing,
stale stub/module-mocking types and Cargo executable resolution. Narrow stdlib
unittest/PyYAML stub and fixed-subprocess annotations retain their documented
purpose without introducing another test framework or disabling shared policy.
Bandit's warnings about prose after existing `nosec` comments were inspected;
they are distinct from a new executable finding.

A wider root `tools`/`tests` Ruff read still reports **44 diagnostics** in the
four staging gate/helper fixture files; their per-file/rule counts are in the
result. Those diagnostics are not relabeled passing by the 27 successful staging
runtime fixtures. Root `cargo metadata --no-deps` also reproduces the missing
`tests/fixtures/clippy` member. Its ownership/profile disposition remains #79.
Full holistic/runtime-image and wider platform qualification remain open.

Reproduce the equipped owner checks using the guide above: initialize the exact
Identity input, generate disposable output before verification, set
`RELAY_CHECKOUT` to the exact recorded owner revision, and run
`tools/baseline_tests.py`. Preserve both logs and every nonzero outcome.
