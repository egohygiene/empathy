# Selected local CI: native qualification, 2026-11-15

The existing optional local-CI consumer passes its selected native and act checks
on Linux AMD64. The [public evidence receipt](data/local-ci-native-20261115.json)
binds this result to clean merged Empathy source
`f19fe1b072d3690b30b4314a92b41f8b5803459a`, the exact Realm source, client bytes,
manifest/configuration hashes and an observed immutable Ubuntu image digest.

## Executed selection

The verified Realm source is `75c1b2e1475b972a0ce1c8594e8daba2e1cf8686`.
All four invoked files match the consumer's recorded hashes. Its installer
verified official act 0.2.97 archive SHA-256 before installing a Linux AMD64 client
into task-owned scratch. Docker 28.4.0 pulled and inspected the exact configured
Ubuntu 24.04 manifest digest; no mutable image selection was substituted.

The source was exercised in a clean disposable consumer checkout:

- Native consumer fixture: 17 tests passed.
- act foundation-consumer job: passed with exit 0 through real Docker execution.
- Native Git whitespace check: passed with exit 0.
- Owned container cleanup: complete.

The existing launcher supplied its reviewed host/cache controls and disabled
container Docker-socket forwarding. No credentials, secret files or broad project
trust flag were forwarded. The optional cloud-network adapter was not needed by
this local fixture. Raw owner reports/logs retain their original bytes separately;
only allowlisted source/status/version/digest fields are committed here.

## Coverage boundaries

Four declared unsupported groups remain explicit: full holistic/root baseline;
staged/specialist-owner inputs; hosted provider/publication behavior; and other
native platforms. They are not passes. `complete:true` means the selected manifest
finished reporting, including those unsupported groups; it does not claim full
hosted-CI coverage. act's checkout emulation copies a local working tree and does
not qualify the real remote checkout Action.

The held canonical runtime/pin reconciliation under
[#110](https://github.com/egohygiene/empathy/issues/110), broader golden baseline
under [#109](https://github.com/egohygiene/empathy/issues/109), and its existing 20
owner-input skips keep their separate acceptance. No linter, owner pin, fixture,
workflow, `.actrc` or source implementation is changed by this evidence checkpoint.

The evidence-only PR still requires the canonical holistic profile on its exact
review head, with warning-only Mypy/Bandit/Secretlint/Lychee outcomes reviewed and
introduced diagnostics resolved. Its manual feature-branch invocation must set
`publish-snapshot=false`; a passing local selection does not supply that result.
No site/package/registry deployment is part of this local execution artifact.

## Reproduce

Follow [the selected local-CI guide](LOCAL_CI.md) with the exact source/client/image
selection and an unused output directory. `plan` is read-only; `doctor` is
preflight; only `run` executes the selected consumer checks. Native-only consumers
leave the profile unselected. Keep host resource, secret and networking choices
in the explicit launcher boundary; `.actrc` remains the reviewed ordinary defaults.

Refs [#140](https://github.com/egohygiene/empathy/issues/140) and parent
[#118](https://github.com/egohygiene/empathy/issues/118).
ADR not required: this qualifies the existing optional Realm-owned execution
under [ADR-0001](../decisions/ADR-0001-foundation-ownership.md); ownership,
applicability, runtime selection and architectural authority are unchanged.
