# Selected local CI consumer

Empathy's optional `local-ci` foundation profile selects repository-owned
`.actrc`, an explicit validation manifest, and a pinned Realm consumer adapter.
It is a golden-consumer example for [issue #140](https://github.com/egohygiene/empathy/issues/140),
not a universal requirement for every repository. Empathy owns applicability,
selection, and integration evidence; Realm owns the execution engine.

## Applicability and native-only use

The golden manifest selects `local-ci`, which requires only `universal`.
Foundation `2.1.0` adds this capability while retaining authoring schema `1.1.0`.
Consumers must update their exact foundation input and manifest reference
together. Existing pinned consumers are not upgraded by this source change.

A consumer that does not select `local-ci` has no foundation requirement for
`.actrc`, Realm, act, or Docker. Existing native commands remain available, for
example:

```sh
python3 tools/foundation.py validate-catalog
python3 tools/foundation.py validate-manifest \
  --manifest foundation/empathy.manifest.json
python3 -m unittest tests.test_foundation_contract --verbose
```

Leaving the profile unselected is the native-only choice; it does not make
unexecuted workflow coverage pass. Selecting the profile also does not install a
client, provision a Docker engine, or adopt a different Dev Container.

## Requirements and pinned source

Use Python 3.11+, Git, and the tools required by the selected native commands.
The act selection additionally needs the pinned client and a reachable Linux
Docker engine. Docker access is a host capability and must be reviewed by the
developer; the profile does not grant it.

`integrations/realm/local-ci.source.json` records Realm revision
`75c1b2e1475b972a0ce1c8594e8daba2e1cf8686`, the selected source-file hashes, and
act `0.2.97`. This is immutable source consumption of the implementation
delivered by [Realm PR #64](https://github.com/egohygiene/realm/pull/64), with
[Reflector PR #266](https://github.com/egohygiene/reflector/pull/266) as an earlier
consumer example. It is not a claim that a Realm package or image was published.

Prepare a separate checkout at that exact revision, then inspect the plan:

```sh
git clone --no-checkout https://github.com/egohygiene/realm.git \
  .cache/realm/local-ci/source
git -C .cache/realm/local-ci/source checkout --detach \
  75c1b2e1475b972a0ce1c8594e8daba2e1cf8686
python3 tools/local_ci.py plan \
  --realm-checkout .cache/realm/local-ci/source
```

For an existing source checkout, verify its revision rather than updating it to
a mutable branch. The adapter verifies the selected source before invoking the
Realm runner. A wrong checkout or changed selected source is an input failure,
not permission to fetch, repair, or trust arbitrary source automatically.

Use the installer from the pinned source to obtain its checksum-pinned client:

```sh
python3 .cache/realm/local-ci/source/tools/realm_act.py install \
  --output .cache/realm/local-ci/bin/act
python3 tools/local_ci.py doctor \
  --realm-checkout .cache/realm/local-ci/source \
  --act .cache/realm/local-ci/bin/act
```

The installer supports Linux AMD64 and ARM64 and accepts a previously downloaded
official archive for offline installation; consult its `--help`. macOS developers
can use an eligible Linux environment connected to their Docker engine. An
emulated architecture is not native-platform qualification.

## Plan, run, and evidence

`plan` validates the selected inputs without running repository checks.
`doctor` inspects runtime prerequisites; a successful preflight is not a test
result. Run from the Empathy checkout with a new output directory:

```sh
python3 tools/local_ci.py run \
  --realm-checkout .cache/realm/local-ci/source \
  --act .cache/realm/local-ci/bin/act \
  --output .cache/realm/local-ci/review-001
```

Managed workspaces that require their configured container proxy and CA may
explicitly append `--cloud-network`. Ordinary desktop Docker installations do
not need that option. Do not place proxy configuration or private runtime
diagnostics in source.

Realm's JSON and Markdown reports retain execution status, represented checkout,
selection, commands, timings, and bounded logs. The adjacent
`consumer-source.json` records Empathy's consumer-source binding; it supplements
the Realm execution report and does not replace or promote its results. Review
both before sharing evidence. Output directories are exclusive, so every repeat
uses a new directory.

Passed, failed, blocked, skipped, and unsupported outcomes remain distinct.
Required incomplete checks keep the run unsuccessful. Missing prerequisites
must be reported; they are not evidence that the underlying tests passed.
Reports stay local unless separately reviewed and published.

## Project configuration and trust

`.actrc` contains only supported ordinary defaults and the reviewed immutable
Ubuntu runner mappings. The explicit act manifest also binds its runner image
by digest. A mutable tag is not a substitute for that binding.

act `0.2.97` restricts options accepted from an untrusted project configuration.
Host paths, caches, artifact handling, networking, Docker socket policy, and
secret inputs belong to the explicit reviewed launcher or developer boundary.
Do not enable broad `--trust-project-actrc` to make ignored project options work.
The pinned Realm launcher supplies its own isolation and execution controls;
Empathy does not maintain a second runner implementation.

## Selected coverage and retained gaps

`config/local-ci.json` is the explicit selection. Its direct check and
`.github/act/local-validation.yml` fixture exercise the bounded foundation
consumer tests. The fixture lives outside `.github/workflows`, so GitHub does
not schedule it. act's checkout emulation copies the working tree; it does not
qualify the remote checkout Action itself.

This selection does not establish a complete `task check` or holistic lint
result. Staged projects, the held runtime suite, hosted/provider scheduling,
publication, release, native platform behavior, and other unselected jobs remain
separate coverage. No production credentials or publishing operation are
selected. A successful fixture is evidence for its declared checks only.

The held catalog/runtime pin mismatch under [#110](https://github.com/egohygiene/empathy/issues/110)
and the twenty owner-input skips recorded under
[#109](https://github.com/egohygiene/empathy/issues/109) retain their existing
owners and source-bound evidence. This capability does not resolve them or
relabel an earlier incomplete baseline as qualified. Existing canonical lint
commands remain selected; a future stable EgoLint migration requires separate
review and reconciliation.

Record the exact review head, actual plan/report identities, executed platform,
and remaining gaps when qualifying this consumer. Linux AMD64 evidence does not
establish ARM64, macOS, or Windows execution. Merged producer code, source pins,
or a passing focused check do not establish full consumer acceptance, published
artifacts, or hosted-CI parity. Holon materialization and Pace fleet adoption
remain later work.
