# Optional website and documentation baseline

Refs #64; parent [#118](https://github.com/egohygiene/empathy/issues/118).

The universal repository baseline selects **no website**. Two explicit canaries
exercise the independent generic React/Vite and LaunchKit profiles. They compose
landing, Zensical documentation, architecture and attribution/legal routes in a
disposable target. They do not select a new Empathy Pages site or replace its
existing Quartz, Garden or Intelligence publication.

## Inputs and ownership

| Concern                       | Canonical source and consumer boundary                                                                                                                                                                                  |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Profile selection and content | Empathy's [selection](../../integrations/website/profiles.json) and two adjacent manifests; no copied template internals                                                                                                |
| Rendering and recovery        | Exact Holon source and site profile digest in [source.json](../../integrations/website/source.json); explicit site-only plan/render/verify/rollback                                                                     |
| Branding                      | Existing repository-owned `.identity/` source; released Identity `v1.0.0` compiler, source `aaad8839104704cf57bfa846539b3b875421e03d`, asset SHA-256 `eea5397c9bc4140210edc9a56c68679c89ddc496cf37aa207078719a3e93eac3` |
| CSS and Tailwind              | Identity emits both token contracts. The consumer maps semantic aliases over exact generated CSS bytes; Tailwind remains an optional token consumer, not an installed framework                                         |
| Browser policy                | Consumer-owned [browserslist](../../integrations/website/browserslist); actual browser qualification is recorded separately                                                                                             |
| Publication                   | No deployer is installed or invoked. Relay and the consuming repository retain publication authority                                                                                                                    |

The source adapter requires a clean checkout at the exact Holon pin before
invoking an owner command. It refuses a different revision, changed profile,
symlink alias or differing existing asset. It never fetches mutable sibling
source, installs agents or invents Aether release metadata.

The complete foundation intent remains in the owner plan, including its
unqualified capabilities. A successful website projection does not qualify
Aether agents, ADR governance, Realm, CI, release, or whole-foundation adoption.
Their immutable declared pins are retained, rather than promoted to executed
or accepted capabilities.

## Reproduce a disposable consumer

Use Python 3.12+, Node 24.15+ and the selected owner's `pnpm@11.24.0`.
Acquire the exact Holon checkout and the official Linux x86-64 Identity release
asset independently. Verify the compiler against the digest above and its
published `SHA256SUMS` before making it executable. Other platforms require a
separately qualified compiler; the current receipt is Linux-specific.

Set `website_holon` to that clean owner checkout and `website_identity` to the
verified compiler. From the Empathy checkout:

```sh
website_profile=generic
website_target="$PWD/.cache/website-baseline/$website_profile"
website_plan="$PWD/.cache/website-baseline/$website_profile.plan.json"
python3 tools/website_baseline.py --holon-source "$website_holon" plan \
  --profile "$website_profile" --target "$website_target" --output "$website_plan"
# Inspect the plan, selected packs, original intent and unqualified capabilities.
python3 tools/website_baseline.py --holon-source "$website_holon" render \
  --plan "$website_plan" --target "$website_target"
python3 tools/website_baseline.py --holon-source "$website_holon" identity-assets \
  --identity-binary "$website_identity" --target "$website_target"
python3 tools/website_baseline.py --holon-source "$website_holon" verify \
  --target "$website_target"
```

Repeat with `website_profile=launchkit` and a new target/plan. Both manifests use
`https://127.0.0.1:9443/` as their **local canary** canonical URL and asset origin.
They make no claim about public DNS, deployment or a production site address.

Install only the disposable target's frozen graphs, then execute its own native
quality/build command:

```sh
python3 -m venv .cache/website-baseline/python
website_python="$PWD/.cache/website-baseline/python/bin/python"
"$website_python" -m pip install --require-hashes \
  --requirement "$website_target/site-docs/requirements.lock.txt"
(cd "$website_target" && pnpm install --frozen-lockfile --ignore-scripts)
"$website_python" "$website_target/site_suite.py" check
```

Holon owns React/Vite and Zensical generation. Rebuild with `site_suite.py build`
and compare every generated byte to the first build. A repeated owner plan must
contain only `noop` operations. `website_baseline.py ... rollback --target ...`
uses guarded owner recovery and refuses later edits; it does not delete
consumer-owned Identity assets or installed dependency caches.

## Accessibility, metadata and localization checks

The opt-in [browser canary](../../tests/browser/website_baseline.py) serves only
this disposable artifact over local HTTPS and executes real Chromium, pinned
axe `4.11.0`, keyboard skip links, three viewport widths, both color schemes,
reduced motion, canonical/description/language/landmark checks, Identity CSS,
attribution and Unicode content. It hashes the artifact before and after.
[Tool identities](../../integrations/website/browser-tools.json) record the
expected axe script digest and tested Playwright version.

Provide a temporary local TLS certificate/key for `127.0.0.1`, an existing
Chromium executable and the exact axe script. Keep the key and generated proof
under ignored `.cache/`, never in source. Run each variant separately because
the fixture uses the same local port:

```sh
python3 tests/browser/website_baseline.py \
  --site-root "$website_target/dist" --variant "$website_profile" \
  --certificate .cache/website-baseline/local.crt \
  --private-key .cache/website-baseline/local.key \
  --axe-script .cache/website-baseline/axe.min.js \
  --output ".cache/website-baseline/$website_profile.browser.json"
```

The minimal Zensical profile omits its unqualified native search widget and
remote repository-statistics collector. Documentation navigation and all
content routes remain. Repository Intelligence Search is independent.
Automatic WCAG checks are evidence, not complete accessibility certification.

The supported locale is English. Authored content containing `café`, `ようこそ`
and `مرحبا` must survive native generation and actual browser text. This proves
Unicode-safe content and explicit language readiness, not translated routing or
all-language typography. Additional locales need a supported owner contract.

The [qualification receipt](data/website-baseline-20261114.json) maps the actual
canaries to the acceptance criteria and records their bounded observations.
The global foundation catalog, preserved imported source, staging, migration,
live publication workflows and previous rollback evidence are unchanged.
