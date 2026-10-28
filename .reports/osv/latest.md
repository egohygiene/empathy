# OSV Vulnerability Scan

- Generated: `2026-10-28T10-08-56Z`
- Repository: `egohygiene/empathy`
- Commit: `e154b325c40f35901bff4b409e3871e2c2fcd5e3`
- Severity gate: `high`
- Duration: `12s`

## Findings

| Severity | Count |
| --- | ---: |
| Critical | 34 |
| High | 274 |
| Medium | 243 |
| Low | 58 |
| Unknown | 1 |
| **Total** | **610** |

## Discovery

Discovered 49 artifact(s) across 7 ecosystem label(s).

- `.reports/megalinter/syft/sbom.spdx.json`
- `.staging/.github/skills/drawio/scripts/package.json`
- `.staging/.github/skills/md-to-docx/scripts/package.json`
- `.staging/.github/skills/winmd-api-search/scripts/cache-generator/CacheGenerator.csproj`
- `.staging/devenvironment/containers/services/api/poetry.lock`
- `.staging/devenvironment/containers/services/api/pyproject.toml`
- `.staging/devenvironment/realm/pyproject.toml`
- `.staging/tools/emoji-precache/package-lock.json`
- `.staging/tools/emoji-precache/package.json`
- `egolint/.config/lint/python/pyproject.toml`
- `egolint/Cargo.lock`
- `egolint/package.json`
- `egolint/pnpm-lock.yaml`
- `egolint/pyproject.toml`
- `egolint/tests/fixtures/dart-analyzer/pubspec.lock`
- `egolint/tests/fixtures/deptry/pyproject.toml`
- `egolint/tests/fixtures/govulncheck/go.mod`
- `egolint/tests/fixtures/knip/package.json`
- `egolint/tests/fixtures/negative/deptry/pyproject.toml`
- `egolint/tests/fixtures/negative/knip/package.json`
- `egolint/tests/fixtures/negative/v8r/package.json`
- `egolint/tests/fixtures/npm-package-json-lint/package.json`
- `egolint/tests/fixtures/v8r/package.json`
- `egolint/uv.lock`
- `holon/packs/react-vite/template/apps/docs/package.json`
- `holon/packs/react-vite/template/apps/playground/package.json`
- `holon/packs/react-vite/template/apps/storefront/package.json`
- `holon/packs/react-vite/template/apps/web/package.json`
- `holon/packs/react-vite/template/package.json`
- `holon/packs/react-vite/template/packages/api-client/package.json`
- `holon/packs/react-vite/template/packages/auth/package.json`
- `holon/packs/react-vite/template/packages/commerce/package.json`
- `holon/packs/react-vite/template/packages/config/package.json`
- `holon/packs/react-vite/template/packages/content/package.json`
- `holon/packs/react-vite/template/packages/design-tokens/package.json`
- `holon/packs/react-vite/template/packages/i18n/package.json`
- `holon/packs/react-vite/template/packages/icons/package.json`
- `holon/packs/react-vite/template/packages/schemas/package.json`
- `holon/packs/react-vite/template/packages/store-config/package.json`
- `holon/packs/react-vite/template/packages/store-ui/package.json`
- `holon/packs/react-vite/template/packages/tailwind-config/package.json`
- `holon/packs/react-vite/template/packages/themes/package.json`
- `holon/packs/react-vite/template/packages/ui/package.json`
- `holon/packs/react-vite/template/packages/utilities/package.json`
- `holon/packs/react-vite/template/packages/visualizations/package.json`
- `holon/packs/react-vite/template/packages/vite-config/package.json`
- `package.json`
- `pnpm-lock.yaml`
- `pyproject.toml`

## Scanned Files

- `.staging/.github/skills/winmd-api-search/scripts/cache-generator/CacheGenerator.csproj`
- `.staging/devenvironment/containers/services/api/poetry.lock`
- `.staging/tools/emoji-precache/package-lock.json`
- `egolint/Cargo.lock`
- `egolint/pnpm-lock.yaml`
- `egolint/uv.lock`
- `pnpm-lock.yaml`

## Skipped Discovered Files

- `.reports/megalinter/syft/sbom.spdx.json`
- `.staging/.github/skills/drawio/scripts/package.json`
- `.staging/.github/skills/md-to-docx/scripts/package.json`
- `.staging/devenvironment/containers/services/api/pyproject.toml`
- `.staging/devenvironment/realm/pyproject.toml`
- `.staging/tools/emoji-precache/package.json`
- `egolint/.config/lint/python/pyproject.toml`
- `egolint/package.json`
- `egolint/pyproject.toml`
- `egolint/tests/fixtures/dart-analyzer/pubspec.lock`
- `egolint/tests/fixtures/deptry/pyproject.toml`
- `egolint/tests/fixtures/govulncheck/go.mod`
- `egolint/tests/fixtures/knip/package.json`
- `egolint/tests/fixtures/negative/deptry/pyproject.toml`
- `egolint/tests/fixtures/negative/knip/package.json`
- `egolint/tests/fixtures/negative/v8r/package.json`
- `egolint/tests/fixtures/npm-package-json-lint/package.json`
- `egolint/tests/fixtures/v8r/package.json`
- `holon/packs/react-vite/template/apps/docs/package.json`
- `holon/packs/react-vite/template/apps/playground/package.json`
- `holon/packs/react-vite/template/apps/storefront/package.json`
- `holon/packs/react-vite/template/apps/web/package.json`
- `holon/packs/react-vite/template/package.json`
- `holon/packs/react-vite/template/packages/api-client/package.json`
- `holon/packs/react-vite/template/packages/auth/package.json`
- `holon/packs/react-vite/template/packages/commerce/package.json`
- `holon/packs/react-vite/template/packages/config/package.json`
- `holon/packs/react-vite/template/packages/content/package.json`
- `holon/packs/react-vite/template/packages/design-tokens/package.json`
- `holon/packs/react-vite/template/packages/i18n/package.json`
- `holon/packs/react-vite/template/packages/icons/package.json`
- `holon/packs/react-vite/template/packages/schemas/package.json`
- `holon/packs/react-vite/template/packages/store-config/package.json`
- `holon/packs/react-vite/template/packages/store-ui/package.json`
- `holon/packs/react-vite/template/packages/tailwind-config/package.json`
- `holon/packs/react-vite/template/packages/themes/package.json`
- `holon/packs/react-vite/template/packages/ui/package.json`
- `holon/packs/react-vite/template/packages/utilities/package.json`
- `holon/packs/react-vite/template/packages/visualizations/package.json`
- `holon/packs/react-vite/template/packages/vite-config/package.json`
- `package.json`
- `pyproject.toml`

## OSV Scanner Report


Total 173 packages affected by 610 known vulnerabilities (34 Critical, 274 High, 243 Medium, 58 Low, 1 Unknown) from 2 ecosystems.
599 vulnerabilities can be fixed.

| OSV URL | CVSS | Ecosystem | Package | Version | Fixed Version | Source |
| --- | --- | --- | --- | --- | --- | --- |
| https://osv.dev/PYSEC-2026-4024<br/>https://osv.dev/GHSA-5p39-cfhj-2xmp | 6.8 | PyPI | anyio | 4.9.0 | 4.14.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4025<br/>https://osv.dev/GHSA-82r6-8w77-94w6 | 9.3 | PyPI | anyio | 4.9.0 | 4.14.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2120 | 9.8 | PyPI | black | 25.1.0 | 26.3.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2121<br/>https://osv.dev/GHSA-3936-cmfr-pm3m | 8.7 | PyPI | black | 25.1.0 | 26.3.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-cg8m-r9f2-5wm2 | 8.7 | PyPI | black | 25.1.0 | 26.10.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4320<br/>https://osv.dev/GHSA-6q48-6c7w-9gw2 | 9.1 | PyPI | certifi | 2025.6.15 | 2026.10.19 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2141<br/>https://osv.dev/GHSA-r6ph-v2qm-q3c2 | 8.2 | PyPI | cryptography | 45.0.4 | 46.0.5 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-35<br/>https://osv.dev/GHSA-m959-cc7f-wv43 | 5.3 | PyPI | cryptography | 45.0.4 | 46.0.6 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3552<br/>https://osv.dev/GHSA-g6cj-pr64-35w5 | 8.2 | PyPI | cryptography | 45.0.4 | 50.0.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3553<br/>https://osv.dev/GHSA-jwv3-5hgf-82ww | 8.7 | PyPI | cryptography | 45.0.4 | 49.0.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3554<br/>https://osv.dev/GHSA-m2h6-j472-rp4c | 6.9 | PyPI | cryptography | 45.0.4 | 49.0.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-36<br/>https://osv.dev/GHSA-p423-j2cm-9vmq | 9.8 | PyPI | cryptography | 45.0.4 | 46.0.7 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-537c-gmf6-5ccf | 7.5 | PyPI | cryptography | 45.0.4 | 48.0.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-45c3-73f7-pv4m | 7.5 | PyPI | dnspython | 2.7.0 | 2.9.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1374<br/>https://osv.dev/GHSA-qmgc-5h2g-mvrw | 5.3 | PyPI | filelock (dev) | 3.18.0 | 3.20.3 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1375<br/>https://osv.dev/GHSA-w853-jp5j-5j7f | 6.3 | PyPI | filelock (dev) | 3.18.0 | 3.20.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-215<br/>https://osv.dev/GHSA-65pc-fj4g-8rjx | 6.9 | PyPI | idna | 3.10 | 3.15 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-70<br/>https://osv.dev/GHSA-fjrm-76x2-c4q4 | 5.3 | PyPI | jwcrypto | 1.5.6 | 1.5.7 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2617<br/>https://osv.dev/GHSA-2h4p-vjrc-8xpq | 8.7 | PyPI | mako | 1.3.10 | 1.3.12 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4243<br/>https://osv.dev/GHSA-5639-2j2p-m4mx | 6.5 | PyPI | mako | 1.3.10 | 1.4.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-88<br/>https://osv.dev/GHSA-v92g-xgxw-vvmm | 7.7 | PyPI | mako | 1.3.10 | 1.3.11 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-107<br/>https://osv.dev/GHSA-hx9q-6w63-j58v | 7.7 | PyPI | orjson | 3.10.18 | 3.11.5 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2987<br/>https://osv.dev/GHSA-5239-wwwm-4pmq | 3.3 | PyPI | pygments | 2.19.2 | 2.20.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2025-183 | 7.0 | PyPI | pyjwt | 2.10.1 | -- | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-120<br/>https://osv.dev/GHSA-752w-5fwx-jx9f | 7.5 | PyPI | pyjwt | 2.10.1 | 2.12.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-175<br/>https://osv.dev/GHSA-993g-76c3-p5m4 | 4.2 | PyPI | pyjwt | 2.10.1 | 2.13.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-176<br/>https://osv.dev/GHSA-jq35-7prp-9v3f | 5.4 | PyPI | pyjwt | 2.10.1 | 2.12.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-177<br/>https://osv.dev/GHSA-fhv5-28vv-h8m8 | 3.7 | PyPI | pyjwt | 2.10.1 | 2.13.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-178<br/>https://osv.dev/GHSA-w7vc-732c-9m39 | 5.3 | PyPI | pyjwt | 2.10.1 | 2.13.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-179<br/>https://osv.dev/GHSA-xgmm-8j9v-c9wx | 7.4 | PyPI | pyjwt | 2.10.1 | 2.13.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4140<br/>https://osv.dev/GHSA-2gx3-rcp4-g85q | 5.3 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4141<br/>https://osv.dev/GHSA-42vr-xj54-vc7v | 5.3 | PyPI | pyjwt | 2.10.1 | 2.15.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4144<br/>https://osv.dev/GHSA-9v7f-9g4p-ffgj | 7.4 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4145<br/>https://osv.dev/GHSA-ffc3-869f-jxw9 | 9.1 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4147<br/>https://osv.dev/GHSA-hxm8-2xgr-2p9m | 4.8 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4148<br/>https://osv.dev/GHSA-jwrc-g2q2-pq5p | 4.4 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4149<br/>https://osv.dev/GHSA-p4g4-x82p-q773 | 7.4 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4152<br/>https://osv.dev/GHSA-w6j9-cwv2-h6wq | 5.9 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4183<br/>https://osv.dev/GHSA-x33g-cr3x-6449 | 8.2 | PyPI | pyjwt | 2.10.1 | 2.15.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-pxh4-856f-4h89 | 7.4 | PyPI | pyjwt | 2.10.1 | 2.14.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1845<br/>https://osv.dev/GHSA-6w46-j5rx-g56g | 6.8 | PyPI | pytest (dev) | 8.4.1 | 9.0.3 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2270<br/>https://osv.dev/GHSA-mf9w-mj56-hr94 | 6.6 | PyPI | python-dotenv | 1.1.1 | 1.2.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1852<br/>https://osv.dev/GHSA-wp53-j4wj-2cfg | 8.6 | PyPI | python-multipart | 0.0.20 | 0.0.22 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3036<br/>https://osv.dev/GHSA-5rvq-cxj2-64vf | 7.5 | PyPI | python-multipart | 0.0.20 | 0.0.30 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3037<br/>https://osv.dev/GHSA-6jv3-5f52-599m | 3.7 | PyPI | python-multipart | 0.0.20 | 0.0.30 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3038<br/>https://osv.dev/GHSA-mj87-hwqh-73pj | 5.3 | PyPI | python-multipart | 0.0.20 | 0.0.26 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3039<br/>https://osv.dev/GHSA-pp6c-gr5w-3c5g | 7.5 | PyPI | python-multipart | 0.0.20 | 0.0.27 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3040<br/>https://osv.dev/GHSA-v9pg-7xvm-68hf | 3.7 | PyPI | python-multipart | 0.0.20 | 0.0.31 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3041<br/>https://osv.dev/GHSA-vffw-93wf-4j4q | 3.7 | PyPI | python-multipart | 0.0.20 | 0.0.30 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2275<br/>https://osv.dev/GHSA-gc5v-m9x4-r6x2 | 5.5 | PyPI | requests | 2.32.4 | 2.33.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-161<br/>https://osv.dev/GHSA-86qp-5c8j-p5mr | 6.5 | PyPI | starlette | 0.46.2 | 1.0.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1941<br/>https://osv.dev/GHSA-2c2j-9gv5-cj73 | 5.3 | PyPI | starlette | 0.46.2 | 0.47.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1942<br/>https://osv.dev/GHSA-7f5h-v6xp-fcq8 | 7.5 | PyPI | starlette | 0.46.2 | 0.49.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2280<br/>https://osv.dev/GHSA-x746-7m8f-x49c | 5.3 | PyPI | starlette | 0.46.2 | 1.1.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2281<br/>https://osv.dev/GHSA-wqp7-x3pw-xc5r | 7.5 | PyPI | starlette | 0.46.2 | 1.1.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-248<br/>https://osv.dev/GHSA-jp82-jpqv-5vv3 | 5.3 | PyPI | starlette | 0.46.2 | 1.3.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-249<br/>https://osv.dev/GHSA-82w8-qh3p-5jfq | 7.5 | PyPI | starlette | 0.46.2 | 1.3.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2291<br/>https://osv.dev/GHSA-wgvc-ghv9-3pmm | 7.5 | PyPI | ujson | 5.10.0 | 5.12.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2292<br/>https://osv.dev/GHSA-c8rr-9gxc-jprv | 7.5 | PyPI | ujson | 5.10.0 | 5.12.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2293<br/>https://osv.dev/GHSA-c38f-wx89-p2xg | 8.7 | PyPI | ujson | 5.10.0 | 5.12.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2294<br/>https://osv.dev/GHSA-3j69-69wj-xqx2 | 6.5 | PyPI | ujson | 5.10.0 | 5.13.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-141<br/>https://osv.dev/GHSA-qccp-gfcp-xxvc | 8.2 | PyPI | urllib3 | 2.5.0 | 2.7.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1994<br/>https://osv.dev/GHSA-2xpw-w6gg-jr37 | 8.9 | PyPI | urllib3 | 2.5.0 | 2.6.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1996<br/>https://osv.dev/GHSA-38jv-5279-wg99 | 8.9 | PyPI | urllib3 | 2.5.0 | 2.6.3 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1998<br/>https://osv.dev/GHSA-gm62-xv2j-4w53 | 8.9 | PyPI | urllib3 | 2.5.0 | 2.6.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4175<br/>https://osv.dev/GHSA-8988-9cw3-xx77 | 7.6 | PyPI | urllib3 | 2.5.0 | 2.8.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4177<br/>https://osv.dev/GHSA-vxq7-64xx-v4gw | 8.9 | PyPI | urllib3 | 2.5.0 | 2.8.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2009<br/>https://osv.dev/GHSA-597g-3phw-6986 | 4.5 | PyPI | virtualenv (dev) | 20.31.2 | 20.36.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4011<br/>https://osv.dev/GHSA-94p9-xgh2-xp45 | 7.7 | PyPI | virtualenv (dev) | 20.31.2 | 21.7.12 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4012<br/>https://osv.dev/GHSA-9h9j-4vrj-gf7g | 5.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.7.11 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4013<br/>https://osv.dev/GHSA-p58f-9548-mpm2 | 7.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.7.13 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-4014<br/>https://osv.dev/GHSA-x78j-v8h9-3j2q | 7.3 | PyPI | virtualenv (dev) | 20.31.2 | 21.7.12 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-394h-qwmc-48pf | 7.1 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-43mp-35q3-x3fq | 4.5 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-494p-63j8-28p3 | 2.3 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-558c-9hv2-4prj | 4.5 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-5vjq-rrrf-7h2q | 7.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.4 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-6w3r-xr62-4xcp | 7.1 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-8rjx-v5ww-45pp | 7.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-c947-3pg5-gm8q | 7.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.2 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-c978-59m8-c77v | 7.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-cw65-gx24-rc82 | 4.5 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-cx28-75q4-x26q | 2.3 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-fc2g-4w5p-6whm | 4.4 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-hhxq-47xx-j5xx | 4.5 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-qmx5-4p3x-wvqf | 2.0 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.9 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-vxj4-q4g9-crj7 | 7.8 | PyPI | virtualenv (dev) | 20.31.2 | 21.14.7 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-2g87-pp6c-29x5 | 8.7 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-494j-54xm-rwp3 | 6.3 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-5wr8-gcqf-gqf3 | 8.2 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-6cjc-53gc-5rqm | 6.9 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-9xw5-w5jj-pvcg | 8.2 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-f9xw-jh8m-3mwq | 6.3 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-gx76-c99x-2c96 | 2.3 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-pqxq-w44r-73xw | 6.3 | PyPI | aiohttp | 3.14.3 | 3.14.4 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-3807<br/>https://osv.dev/GHSA-89v8-rhwq-hf77 | 5.0 | PyPI | asteval | 1.0.6 | 1.0.9 | egolint/uv.lock |
| https://osv.dev/GHSA-9w56-46f6-3qhx | 5.5 | PyPI | asteval | 1.0.6 | 1.0.9 | egolint/uv.lock |
| https://osv.dev/GHSA-cg8m-r9f2-5wm2 | 8.7 | PyPI | black | 26.5.1 | 26.10.1 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4320<br/>https://osv.dev/GHSA-6q48-6c7w-9gw2 | 9.1 | PyPI | certifi | 2026.7.22 | 2026.10.19 | egolint/uv.lock |
| https://osv.dev/GHSA-567q-5qvw-pf92 | 2.5 | PyPI | filelock | 3.32.2 | 4.2.1 | egolint/uv.lock |
| https://osv.dev/GHSA-9vhv-jxww-xfm5 | 3.3 | PyPI | filelock | 3.32.2 | 4.2.1 | egolint/uv.lock |
| https://osv.dev/GHSA-v4x8-3wr5-3wq8 | 7.1 | PyPI | filelock | 3.32.2 | 4.2.1 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-3982<br/>https://osv.dev/GHSA-239g-whfq-7xj9 | 8.8 | PyPI | gitpython | 3.1.59 | 3.1.60 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-3984<br/>https://osv.dev/GHSA-g5vv-9gxw-82hx | 7.5 | PyPI | gitpython | 3.1.59 | 3.1.60 | egolint/uv.lock |
| https://osv.dev/GHSA-23mf-xhv8-69c2 | 7.1 | PyPI | gitpython | 3.1.59 | 3.2.0 | egolint/uv.lock |
| https://osv.dev/GHSA-59cr-6r3x-644w | 6.1 | PyPI | gitpython | 3.1.59 | 3.1.62 | egolint/uv.lock |
| https://osv.dev/GHSA-83vg-56qc-22m7 | 7.5 | PyPI | gitpython | 3.1.59 | 3.2.1 | egolint/uv.lock |
| https://osv.dev/GHSA-f9j4-qggq-h239 | 8.1 | PyPI | gitpython | 3.1.59 | 3.2.0 | egolint/uv.lock |
| https://osv.dev/GHSA-fx3j-rwgx-fr94 | 6.5 | PyPI | gitpython | 3.1.59 | 3.2.0 | egolint/uv.lock |
| https://osv.dev/GHSA-gq48-pqfc-9p58 |  | PyPI | gitpython | 3.1.59 | 3.2.0 | egolint/uv.lock |
| https://osv.dev/GHSA-m64x-33q8-m5h7 | 8.7 | PyPI | gitpython | 3.1.59 | 3.2.0 | egolint/uv.lock |
| https://osv.dev/GHSA-w8jc-g24h-crhw | 7.5 | PyPI | gitpython | 3.1.59 | 3.2.0 | egolint/uv.lock |
| https://osv.dev/GHSA-whh4-5q6c-9v3x | 6.5 | PyPI | gitpython | 3.1.59 | 3.1.60 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4054<br/>https://osv.dev/GHSA-c3mw-737p-c7g2 | 7.1 | PyPI | jupyter-server | 2.20.0 | 2.21.0 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4055<br/>https://osv.dev/GHSA-3325-v43h-43rv | 5.4 | PyPI | jupyterlab | 4.6.3 | 4.6.4 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4056<br/>https://osv.dev/GHSA-3jqq-pw4j-pqcj | 6.8 | PyPI | jupyterlab | 4.6.3 | 4.6.4 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4057<br/>https://osv.dev/GHSA-6966-vjj6-99xv | 8.1 | PyPI | jupyterlab | 4.6.3 | 4.6.4 | egolint/uv.lock |
| https://osv.dev/GHSA-jwrc-gm9j-263p | 4.2 | PyPI | jupyterlab | 4.6.3 | 4.6.4 | egolint/uv.lock |
| https://osv.dev/GHSA-j586-36cw-2gc2 | 7.5 | PyPI | msgpack | 1.2.1 | 1.2.3 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4244<br/>https://osv.dev/GHSA-54p9-h82j-f925 | 5.3 | PyPI | multidict | 6.7.1 | 6.9.1 | egolint/uv.lock |
| https://osv.dev/GHSA-pjvx-prjx-h659 | 8.8 | PyPI | nbconvert | 7.17.1 | 7.17.2 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4112<br/>https://osv.dev/GHSA-6966-vjj6-99xv | 8.1 | PyPI | notebook | 7.6.2 | 7.6.3 | egolint/uv.lock |
| https://osv.dev/GHSA-jwrc-gm9j-263p | 4.2 | PyPI | notebook | 7.6.2 | 7.6.3 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4326<br/>https://osv.dev/GHSA-27h8-gf7j-v5hc | 8.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4327<br/>https://osv.dev/GHSA-4558-3h8r-v8xp | 8.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4328<br/>https://osv.dev/GHSA-4rr5-89j8-mwwm | 7.5 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-22hg-r758-rrw9 | 8.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-24rc-8hj2-v98c | 6.5 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-254f-3936-288h | 6.3 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-332p-7hrc-92wf | 9.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-3j72-p6qg-6xp7 | 7.1 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-462x-pgg6-55fp | 6.5 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-4rm8-3hmm-39fg | 6.5 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-58r4-6rv3-gfh8 | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-5x8w-8jj5-q52h | 9.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-5xm2-6676-qcp9 | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-654x-cwwv-5j9c | 6.3 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-65qm-jvmh-6pqg | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-74r2-7ff9-mjj2 | 6.9 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-78g4-xqwv-q3g8 | 8.1 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-7mwm-ghpf-9vrm | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-8g5g-8vmr-9782 | 9.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-9v9v-9qvf-h2hj | 7.1 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-c6hw-5grf-ff96 | 8.8 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-cp9v-662q-vvx9 | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-f2g6-542v-9j58 | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-fc9g-5qg7-mf45 | 6.9 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-g4qv-2jxx-769h | 7.1 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-g7cr-3p24-7wf7 | 7.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-g842-9rc4-69pw | 7.1 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-gg2r-wvfm-q9rx | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-j4m9-6w36-pw47 | 8.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-jg86-v3jv-hrpm | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-mrfp-p49p-3hf2 | 8.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-p4wg-p73j-c528 | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-p8hx-v2p6-rp84 | 6.5 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-pchr-8j38-3x4p | 8.8 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-q45j-58j2-45rg | 8.7 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-rfgq-q3w2-pmv2 | 6.9 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-v9pv-5gc8-w2m6 | 9.8 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-vx6w-vv9f-6gvg | 6.9 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-w889-685w-c8fh | 9.2 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-xgh8-jp6q-p5x8 | 6.9 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-xvh5-g6gv-559v | 8.8 | PyPI | pillow | 12.3.0 | 13.0.0 | egolint/uv.lock |
| https://osv.dev/GHSA-22qq-2fwx-7p67 | 5.4 | PyPI | pylint | 4.0.7 | 4.0.9 | egolint/uv.lock |
| https://osv.dev/GHSA-xmj3-9gf7-h52w | 1.0 | PyPI | setuptools | 84.0.0 | 84.1.0 | egolint/uv.lock |
| https://osv.dev/GHSA-3hv7-mjh2-fv65 | 5.3 | PyPI | tornado | 6.5.8 | 6.5.9 | egolint/uv.lock |
| https://osv.dev/GHSA-c2m8-h5v5-343r | 8.2 | PyPI | tornado | 6.5.8 | 6.5.9 | egolint/uv.lock |
| https://osv.dev/GHSA-chx6-46f5-w4vp | 7.5 | PyPI | tornado | 6.5.8 | 6.5.9 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4175<br/>https://osv.dev/GHSA-8988-9cw3-xx77 | 7.6 | PyPI | urllib3 | 2.7.0 | 2.8.0 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4176<br/>https://osv.dev/GHSA-gh4c-6fx4-qh6g | 6.9 | PyPI | urllib3 | 2.7.0 | 2.8.0 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4177<br/>https://osv.dev/GHSA-vxq7-64xx-v4gw | 8.9 | PyPI | urllib3 | 2.7.0 | 2.8.0 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4011<br/>https://osv.dev/GHSA-94p9-xgh2-xp45 | 7.7 | PyPI | virtualenv | 21.7.4 | 21.7.12 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4012<br/>https://osv.dev/GHSA-9h9j-4vrj-gf7g | 5.8 | PyPI | virtualenv | 21.7.4 | 21.7.11 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4013<br/>https://osv.dev/GHSA-p58f-9548-mpm2 | 7.8 | PyPI | virtualenv | 21.7.4 | 21.7.13 | egolint/uv.lock |
| https://osv.dev/PYSEC-2026-4014<br/>https://osv.dev/GHSA-x78j-v8h9-3j2q | 7.3 | PyPI | virtualenv | 21.7.4 | 21.7.12 | egolint/uv.lock |
| https://osv.dev/GHSA-394h-qwmc-48pf | 7.1 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-43mp-35q3-x3fq | 4.5 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-494p-63j8-28p3 | 2.3 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-558c-9hv2-4prj | 4.5 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-5vjq-rrrf-7h2q | 7.8 | PyPI | virtualenv | 21.7.4 | 21.14.4 | egolint/uv.lock |
| https://osv.dev/GHSA-6w3r-xr62-4xcp | 7.1 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-8rjx-v5ww-45pp | 7.8 | PyPI | virtualenv | 21.7.4 | 21.14.2 | egolint/uv.lock |
| https://osv.dev/GHSA-c947-3pg5-gm8q | 7.8 | PyPI | virtualenv | 21.7.4 | 21.14.2 | egolint/uv.lock |
| https://osv.dev/GHSA-c978-59m8-c77v | 7.8 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-cw65-gx24-rc82 | 4.5 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-cx28-75q4-x26q | 2.3 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-fc2g-4w5p-6whm | 4.4 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-hhxq-47xx-j5xx | 4.5 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-qmx5-4p3x-wvqf | 2.0 | PyPI | virtualenv | 21.7.4 | 21.14.9 | egolint/uv.lock |
| https://osv.dev/GHSA-vxj4-q4g9-crj7 | 7.8 | PyPI | virtualenv | 21.7.4 | 21.14.7 | egolint/uv.lock |
| https://osv.dev/GHSA-3jxr-9vmj-r5cp | 7.7 | npm | brace-expansion | 1.1.12 | 1.1.16 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 1.1.12 | 1.1.19 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-f886-m6hf-6m8v | 6.5 | npm | brace-expansion | 1.1.12 | 1.1.13 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-mh99-v99m-4gvg | 7.5 | npm | brace-expansion | 1.1.12 | 1.1.17 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 1.1.12 | 1.1.21 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 1.1.12 | 1.1.20 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-rgw5-rvv9-x895 | 7.5 | npm | brace-expansion | 1.1.12 | 1.1.18 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-23c5-xmqv-rm74 | 7.5 | npm | minimatch | 3.1.2 | 3.1.4 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-3ppc-4f35-3m26 | 8.7 | npm | minimatch | 3.1.2 | 3.1.3 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-7r86-cg39-jmmj | 7.5 | npm | minimatch | 3.1.2 | 3.1.3 | .staging/tools/emoji-precache/package-lock.json |
| https://osv.dev/GHSA-f596-whhp-79r4 | 3.7 | npm | @grpc/grpc-js | 1.14.4 | 1.14.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-m9gg-hp2v-232j | 7.4 | npm | @grpc/grpc-js | 1.14.4 | 1.14.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-v5rq-49vh-5v5c | 9.2 | npm | @simple-git/argv-parser | 1.1.1 | 2.0.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3pq3-5fj3-cg6v | 7.0 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-44g4-m2mj-wpvx | 6.9 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4hqw-qxg8-jxx2 | 6.9 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-542g-h47m-68v8 | 8.2 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-9fr6-4gfg-395g | 6.9 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-c29m-xwm3-cm6r | 8.2 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-j8rh-479h-cp32 | 6.9 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-m8m8-qj5v-23w3 | 7.6 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-mghh-pgcx-3jjj | 8.2 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r4gj-5m52-g5wh | 7.0 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-vh66-26gq-q6x8 | 6.9 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-x97p-jq2g-jp4f | 8.3 | npm | axios | 1.18.1 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3pq3-5fj3-cg6v | 7.0 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-44g4-m2mj-wpvx | 6.9 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4hqw-qxg8-jxx2 | 6.9 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-542g-h47m-68v8 | 8.2 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-9fr6-4gfg-395g | 6.9 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-c29m-xwm3-cm6r | 8.2 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-j8rh-479h-cp32 | 6.9 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-m8m8-qj5v-23w3 | 7.6 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-mghh-pgcx-3jjj | 8.2 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r4gj-5m52-g5wh | 7.0 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-vh66-26gq-q6x8 | 6.9 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-x97p-jq2g-jp4f | 8.3 | npm | axios | 1.19.0 | 1.20.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-c475-qrg2-pj4r | 8.2 | npm | basic-ftp | 5.3.1 | 6.2.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-27r3-jxmh-p828 | 7.5 | npm | body-parser | 1.20.6 | 1.20.9 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 1.1.18 | 1.1.19 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 1.1.18 | 1.1.21 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 1.1.18 | 1.1.20 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 2.1.4 | 2.1.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 2.1.4 | 2.1.7 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 2.1.4 | 2.1.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 5.0.9 | 5.0.10 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 5.0.9 | 5.0.12 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 5.0.9 | 5.0.11 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2wm5-q62r-hmrv | 6.9 | npm | colord | 2.9.3 | 2.9.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-vc2v-76pw-4v95 | 7.5 | npm | compression | 1.8.1 | 1.8.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-hrh2-vp3x-79xf | 9.1 | npm | decompress | 4.2.1 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-gcqx-w48m-w2h4 | 5.3 | npm | deepmerge | 4.3.1 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-848j-6mx2-7j84 | 5.6 | npm | elliptic | 6.6.1 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-jggr-w7fw-pc2j | 6.3 | npm | fast-copy | 3.0.2 | 3.1.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-333x-w4r6-6crp | 3.7 | npm | fast-uri | 3.1.5 | 3.1.9 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-5jgf-p345-68v8 | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-f65p-4m7j-42xc | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-fph4-wmhf-6fwf | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-hrr3-gc8f-f4qj | 4.8 | npm | fast-uri | 3.1.5 | 3.1.8 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-jqff-g426-hqxp | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qw65-cvwx-89v3 | 7.5 | npm | fast-uri | 3.1.5 | 3.1.7 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-w74x-v6f9-j3xg | 6.1 | npm | fast-uri | 3.1.5 | 3.1.9 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-wjr9-j795-jxcr | 4.8 | npm | fast-uri | 3.1.5 | 3.1.9 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-xhq7-xmqj-769h | 3.7 | npm | fast-uri | 3.1.5 | 3.1.9 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-8r9p-f939-6h3c | 8.2 | npm | follow-redirects | 1.16.0 | 1.16.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-q3jh-wrc6-jgq8 | 8.2 | npm | follow-redirects | 1.16.0 | 1.16.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-8r5x-fm3f-whwj | 9.8 | npm | handlebars | 4.7.9 | 4.7.10 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-p8wg-vrv2-v86f | 9.2 | npm | handlebars | 4.7.9 | 4.7.10 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-xw65-4hp5-5hc7 | 4.7 | npm | handlebars | 4.7.9 | 4.7.10 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-ch52-4w7c-c8xp | 8.7 | npm | http-cache-semantics | 4.2.0 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2vr4-cq9g-pvrc | 6.9 | npm | ip-address | 10.5.0 | 10.5.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-h3mg-xc3c-68pw | 6.3 | npm | ip-address | 10.5.0 | 10.7.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-j6r3-76f7-8jcv | 6.3 | npm | ip-address | 10.5.0 | 10.7.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rpw4-54j3-4h4q | 6.3 | npm | ip-address | 10.5.0 | 10.5.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rxp7-6hxx-x8q5 | 6.3 | npm | ip-address | 10.5.0 | 10.7.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6h2x-m376-mqjq | 8.7 | npm | joi | 17.13.4 | 17.13.7 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6w3j-5fw6-r9vr | 3.7 | npm | joi | 17.13.4 | 17.13.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-gg4h-3hg2-grpc | 3.7 | npm | joi | 17.13.4 | 17.13.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-wr44-6hxh-3jwq | 6.3 | npm | joi | 17.13.4 | 17.13.8 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6h2x-m376-mqjq | 8.7 | npm | joi | 18.2.3 | 18.2.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6w3j-5fw6-r9vr | 3.7 | npm | joi | 18.2.3 | 18.2.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-gg4h-3hg2-grpc | 3.7 | npm | joi | 18.2.3 | 18.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-wr44-6hxh-3jwq | 6.3 | npm | joi | 18.2.3 | 18.2.9 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2883-xcg3-v3hh | 7.5 | npm | js-yaml | 3.15.1 | 3.15.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2883-xcg3-v3hh | 7.5 | npm | js-yaml | 4.3.1 | 4.3.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r3ph-w7gj-g6xm | 5.3 | npm | js-yaml | 5.2.2 | 5.4.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r3ph-w7gj-g6xm | 5.3 | npm | js-yaml | 5.2.3 | 5.4.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-238p-pmpm-9mq7 | 2.1 | npm | katex | 0.16.47 | 0.18.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-587h-7wmj-h5pm | 7.5 | npm | launch-editor | 2.14.1 | 2.14.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-698v-4r3x-3vcv | 6.3 | npm | launch-editor | 2.14.1 | 2.14.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r825-w8mm-5pxw | 6.3 | npm | launch-editor | 2.14.1 | 2.14.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-253c-mchw-3w2r | 6.3 | npm | markdown-it | 14.3.0 | 14.3.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-gfr2-rv44-r23c | 7.5 | npm | markdown-it | 14.3.0 | 14.3.3 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r7fv-28h4-cvq7 | 7.5 | npm | markdown-it | 14.3.0 | 14.3.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-vfgh-jcmw-g37q | 3.7 | npm | markdown-it | 14.3.0 | 14.3.3 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-hrvq-x7jp-36xv | 5.8 | npm | nx | 23.1.1 | 23.2.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-w3vv-58gj-gw77 | 8.5 | npm | nx | 23.1.1 | 23.1.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-477h-4r7f-fvrx | 6.3 | npm | pbkdf2 | 3.1.6 | 3.1.7 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-67c8-pqhq-4rmx | 9.2 | npm | piscina | 4.9.3 | 4.9.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rj75-hqrm-r3gf | 5.9 | npm | postcss-selector-parser | 6.1.4 | 6.1.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rj75-hqrm-r3gf | 5.9 | npm | postcss-selector-parser | 7.1.5 | 7.1.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-jqcg-44mw-7w3h | 9.1 | npm | proxy-addr | 2.0.7 | 2.0.8 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4mjr-xmp4-gh2g | 6.3 | npm | qs | 6.15.3 | 6.16.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-6pq8-jhm2-2vcw | 6.3 | npm | qs | 6.15.3 | 6.16.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-x5fp-wj9c-mxmx | 6.3 | npm | qs | 6.15.3 | 6.16.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-m5mm-p8h7-m29v | 2.1 | npm | serialize-javascript | 7.1.0 | 7.1.3 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rgj7-g3m4-5g8c | 8.9 | npm | sharp | 0.35.3 | 0.35.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-wq5f-xc86-pv6w | 8.9 | npm | sharp | 0.35.3 | 0.35.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-pqg4-j6r4-53mv | 9.2 | npm | shell-quote | 1.10.0 | 1.11.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-pqg4-j6r4-53mv | 9.2 | npm | shell-quote | 1.9.0 | 1.11.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-858h-whjf-mvg5 | 8.1 | npm | simple-git | 3.36.0 | 4.0.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-g4wm-2vf7-vfgr | 8.1 | npm | simple-git | 3.36.0 | 4.0.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-x6jw-m9v5-85vh | 9.2 | npm | simple-git | 3.36.0 | 4.0.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-7w5x-hrqm-74c2 | 8.2 | npm | smol-toml | 1.6.1 | 1.7.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.6.1 | 1.9.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-7w5x-hrqm-74c2 | 8.2 | npm | smol-toml | 1.7.0 | 1.7.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.7.0 | 1.9.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.7.1 | 1.9.0 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-68fv-2mgg-jv7q | 8.7 | npm | source-map-js | 1.2.1 | 1.2.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4vpr-x523-8j87 | 6.1 | npm | svgo | 2.8.3 | 2.8.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-w27v-7q3p-w38r | 8.2 | npm | svgo | 2.8.3 | 2.8.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4vpr-x523-8j87 | 6.1 | npm | svgo | 3.3.4 | 3.3.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-w27v-7q3p-w38r | 8.2 | npm | svgo | 3.3.4 | 3.3.5 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-5gmw-xhrv-c9v3 | 9.5 | npm | tinypool | 1.1.1 | 2.1.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-85c8-ppgw-ccpr | 9.5 | npm | tinypool | 1.1.1 | 2.1.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 6.28.0 | 6.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3wwx-pv8p-q78v | 5.9 | npm | undici | 6.28.0 | 6.28.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4qv8-2p9j-2685 | 5.9 | npm | undici | 6.28.0 | 6.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 6.28.0 | 6.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 6.28.0 | 6.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 6.28.0 | 6.28.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rfgv-xxqx-mfg5 | 7.5 | npm | undici | 6.28.0 | 6.28.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-xjj6-f33q-929c | 7.5 | npm | undici | 6.28.0 | 6.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2gqq-gqf2-x968 | 3.7 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2jfj-6hjv-fm6j | 6.5 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3wwx-pv8p-q78v | 5.9 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3xpg-4rpp-hhhm | 5.9 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4qv8-2p9j-2685 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4w7w-5xrc-9h26 | 7.4 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-55wc-3pg8-jfw6 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-8436-99hf-9mmv | 3.7 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-f72v-6w45-q472 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-pmjh-fq2x-6v4x | 5.9 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rfgv-xxqx-mfg5 | 7.5 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rx4f-c7p8-82vq | 5.9 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-w293-vg96-wgc3 | 7.4 | npm | undici | 7.29.0 | 7.29.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-xjj6-f33q-929c | 7.5 | npm | undici | 7.29.0 | 7.30.1 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2gqq-gqf2-x968 | 3.7 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2jfj-6hjv-fm6j | 6.5 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3wwx-pv8p-q78v | 5.9 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-3xpg-4rpp-hhhm | 5.9 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4qv8-2p9j-2685 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-4w7w-5xrc-9h26 | 7.4 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-55wc-3pg8-jfw6 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-8436-99hf-9mmv | 3.7 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-f72v-6w45-q472 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-pmjh-fq2x-6v4x | 5.9 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rfgv-xxqx-mfg5 | 7.5 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rx4f-c7p8-82vq | 5.9 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-vp8m-p9jh-q5pm | 7.4 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-w293-vg96-wgc3 | 7.4 | npm | undici | 8.10.0 | 8.10.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-xjj6-f33q-929c | 7.5 | npm | undici | 8.10.0 | 8.12.2 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-587h-7wmj-h5pm | 7.5 | npm | vite | 8.2.1 | 8.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-698v-4r3x-3vcv | 6.3 | npm | vite | 8.2.1 | 8.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-9jrq-w75r-8gcw | 2.1 | npm | vite | 8.2.1 | 8.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-r825-w8mm-5pxw | 6.3 | npm | vite | 8.2.1 | 8.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-rq7h-c2jc-7f22 | 6.3 | npm | vite | 8.2.1 | 8.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-vfpm-58rq-9qcg | 6.3 | npm | vite | 8.2.1 | 8.2.4 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-g3ch-rx76-35fx | 4.2 | npm | vue-template-compiler | 2.7.16 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-g84c-rxfj-3j2c | 7.4 | npm | webpack-dev-middleware | 7.4.5 | 7.4.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-mrhx-c7xc-m3w5 | 8.2 | npm | zod | 3.22.4 | 4.6.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-mrhx-c7xc-m3w5 | 8.2 | npm | zod | 4.4.3 | 4.6.6 | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-gxm5-99cw-xjw9 | 5.8 | npm | @fastify/busboy | 2.1.1 | 3.2.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-x8mw-p69m-v3mx | 7.5 | npm | @fastify/busboy | 2.1.1 | 3.2.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-f596-whhp-79r4 | 3.7 | npm | @grpc/grpc-js | 1.14.4 | 1.14.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-m9gg-hp2v-232j | 7.4 | npm | @grpc/grpc-js | 1.14.4 | 1.14.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-8988-4f7v-96qf | 5.3 | npm | @opentelemetry/core | 2.0.0 | 2.8.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-v5rq-49vh-5v5c | 9.2 | npm | @simple-git/argv-parser | 1.1.1 | 2.0.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2g4f-4pwh-qvx6 | 5.5 | npm | ajv | 8.17.1 | 8.18.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2g4f-4pwh-qvx6 | 5.5 | npm | ajv | 8.6.3 | 8.18.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3pq3-5fj3-cg6v | 7.0 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-44g4-m2mj-wpvx | 6.9 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4hqw-qxg8-jxx2 | 6.9 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-542g-h47m-68v8 | 8.2 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9fr6-4gfg-395g | 6.9 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-c29m-xwm3-cm6r | 8.2 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-j8rh-479h-cp32 | 6.9 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-m8m8-qj5v-23w3 | 7.6 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-mghh-pgcx-3jjj | 8.2 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r4gj-5m52-g5wh | 7.0 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vh66-26gq-q6x8 | 6.9 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-x97p-jq2g-jp4f | 8.3 | npm | axios | 1.18.1 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3pq3-5fj3-cg6v | 7.0 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-44g4-m2mj-wpvx | 6.9 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4hqw-qxg8-jxx2 | 6.9 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-542g-h47m-68v8 | 8.2 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9fr6-4gfg-395g | 6.9 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-c29m-xwm3-cm6r | 8.2 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-j8rh-479h-cp32 | 6.9 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-m8m8-qj5v-23w3 | 7.6 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-mghh-pgcx-3jjj | 8.2 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r4gj-5m52-g5wh | 7.0 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vh66-26gq-q6x8 | 6.9 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-x97p-jq2g-jp4f | 8.3 | npm | axios | 1.19.0 | 1.20.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-27r3-jxmh-p828 | 7.5 | npm | body-parser | 1.20.6 | 1.20.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 1.1.18 | 1.1.19 | pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 1.1.18 | 1.1.21 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 1.1.18 | 1.1.20 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 2.1.4 | 2.1.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 2.1.4 | 2.1.7 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 2.1.4 | 2.1.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 5.0.8 | 5.0.10 | pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 5.0.8 | 5.0.12 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 5.0.8 | 5.0.11 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rgw5-rvv9-x895 | 7.5 | npm | brace-expansion | 5.0.8 | 5.0.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6j4f-fj2g-mc7p | 7.5 | npm | brace-expansion | 5.0.9 | 5.0.10 | pnpm-lock.yaml |
| https://osv.dev/GHSA-q2hr-2g5m-vwhr | 5.3 | npm | brace-expansion | 5.0.9 | 5.0.12 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qhr7-859c-m2p7 | 7.5 | npm | brace-expansion | 5.0.9 | 5.0.11 | pnpm-lock.yaml |
| https://osv.dev/GHSA-grv7-fg5c-xmjg | 7.5 | npm | braces | 2.3.2 | 3.0.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2wm5-q62r-hmrv | 6.9 | npm | colord | 2.9.3 | 2.9.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vc2v-76pw-4v95 | 7.5 | npm | compression | 1.8.1 | 1.8.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vcc3-ghjq-m6fr | 6.6 | npm | decode-uri-component | 0.2.2 | 0.5.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-hrh2-vp3x-79xf | 9.1 | npm | decompress | 4.2.1 | -- | pnpm-lock.yaml |
| https://osv.dev/GHSA-gcqx-w48m-w2h4 | 5.3 | npm | deepmerge | 4.3.1 | -- | pnpm-lock.yaml |
| https://osv.dev/GHSA-848j-6mx2-7j84 | 5.6 | npm | elliptic | 6.6.1 | -- | pnpm-lock.yaml |
| https://osv.dev/GHSA-g7r4-m6w7-qqqr | 2.5 | npm | esbuild | 0.27.7 | 0.28.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-jggr-w7fw-pc2j | 6.3 | npm | fast-copy | 3.0.2 | 3.1.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-333x-w4r6-6crp | 3.7 | npm | fast-uri | 3.1.5 | 3.1.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5jgf-p345-68v8 | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-f65p-4m7j-42xc | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-fph4-wmhf-6fwf | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-hrr3-gc8f-f4qj | 4.8 | npm | fast-uri | 3.1.5 | 3.1.8 | pnpm-lock.yaml |
| https://osv.dev/GHSA-jqff-g426-hqxp | 7.5 | npm | fast-uri | 3.1.5 | 3.1.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qw65-cvwx-89v3 | 7.5 | npm | fast-uri | 3.1.5 | 3.1.7 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w74x-v6f9-j3xg | 6.1 | npm | fast-uri | 3.1.5 | 3.1.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-wjr9-j795-jxcr | 4.8 | npm | fast-uri | 3.1.5 | 3.1.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xhq7-xmqj-769h | 3.7 | npm | fast-uri | 3.1.5 | 3.1.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5v7r-6r5c-r473 | 5.3 | npm | file-type | 20.5.0 | 21.3.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-j47w-4g3g-c36v | 5.3 | npm | file-type | 20.5.0 | 21.3.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-8r9p-f939-6h3c | 8.2 | npm | follow-redirects | 1.16.0 | 1.16.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-q3jh-wrc6-jgq8 | 8.2 | npm | follow-redirects | 1.16.0 | 1.16.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-8r5x-fm3f-whwj | 9.8 | npm | handlebars | 4.7.9 | 4.7.10 | pnpm-lock.yaml |
| https://osv.dev/GHSA-p8wg-vrv2-v86f | 9.2 | npm | handlebars | 4.7.9 | 4.7.10 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xw65-4hp5-5hc7 | 4.7 | npm | handlebars | 4.7.9 | 4.7.10 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5r4p-p66f-jhc7 | 5.3 | npm | hono | 4.13.2 | 4.13.11 | pnpm-lock.yaml |
| https://osv.dev/GHSA-crvj-82cr-hjcx | 5.9 | npm | hono | 4.13.2 | 4.13.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-g6gw-c38x-mqfc | 5.3 | npm | hono | 4.13.2 | 4.13.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-gqvv-2mrq-wpjv | 6.5 | npm | hono | 4.13.2 | 4.13.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-hxh3-vqpv-xpqv | 4.7 | npm | hono | 4.13.2 | 4.13.7 | pnpm-lock.yaml |
| https://osv.dev/GHSA-ch52-4w7c-c8xp | 8.7 | npm | http-cache-semantics | 4.2.0 | -- | pnpm-lock.yaml |
| https://osv.dev/GHSA-2vr4-cq9g-pvrc | 6.9 | npm | ip-address | 10.5.0 | 10.5.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-h3mg-xc3c-68pw | 6.3 | npm | ip-address | 10.5.0 | 10.7.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-j6r3-76f7-8jcv | 6.3 | npm | ip-address | 10.5.0 | 10.7.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rpw4-54j3-4h4q | 6.3 | npm | ip-address | 10.5.0 | 10.5.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rxp7-6hxx-x8q5 | 6.3 | npm | ip-address | 10.5.0 | 10.7.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6h2x-m376-mqjq | 8.7 | npm | joi | 17.13.4 | 17.13.7 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6w3j-5fw6-r9vr | 3.7 | npm | joi | 17.13.4 | 17.13.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-gg4h-3hg2-grpc | 3.7 | npm | joi | 17.13.4 | 17.13.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-wr44-6hxh-3jwq | 6.3 | npm | joi | 17.13.4 | 17.13.8 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6h2x-m376-mqjq | 8.7 | npm | joi | 18.2.3 | 18.2.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6w3j-5fw6-r9vr | 3.7 | npm | joi | 18.2.3 | 18.2.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-gg4h-3hg2-grpc | 3.7 | npm | joi | 18.2.3 | 18.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-wr44-6hxh-3jwq | 6.3 | npm | joi | 18.2.3 | 18.2.9 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2883-xcg3-v3hh | 7.5 | npm | js-yaml | 3.15.1 | 3.15.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2883-xcg3-v3hh | 7.5 | npm | js-yaml | 4.1.1 | 4.3.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-52cp-r559-cp3m | 7.5 | npm | js-yaml | 4.1.1 | 4.3.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5p4m-2wfm-xmqj | 7.5 | npm | js-yaml | 4.1.1 | 4.3.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-h67p-54hq-rp68 | 5.3 | npm | js-yaml | 4.1.1 | 4.2.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2883-xcg3-v3hh | 7.5 | npm | js-yaml | 4.3.1 | 4.3.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r3ph-w7gj-g6xm | 5.3 | npm | js-yaml | 5.2.3 | 5.4.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-238p-pmpm-9mq7 | 2.1 | npm | katex | 0.16.47 | 0.18.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-587h-7wmj-h5pm | 7.5 | npm | launch-editor | 2.14.1 | 2.14.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-698v-4r3x-3vcv | 6.3 | npm | launch-editor | 2.14.1 | 2.14.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r825-w8mm-5pxw | 6.3 | npm | launch-editor | 2.14.1 | 2.14.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-f23m-r3pf-42rh | 6.5 | npm | lodash | 4.17.21 | 4.18.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r5fr-rjxr-66jc | 8.1 | npm | lodash | 4.17.21 | 4.18.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xxjr-mmjv-4gpg | 6.9 | npm | lodash | 4.17.21 | 4.17.23 | pnpm-lock.yaml |
| https://osv.dev/GHSA-253c-mchw-3w2r | 6.3 | npm | markdown-it | 14.3.0 | 14.3.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-gfr2-rv44-r23c | 7.5 | npm | markdown-it | 14.3.0 | 14.3.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r7fv-28h4-cvq7 | 7.5 | npm | markdown-it | 14.3.0 | 14.3.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vfgh-jcmw-g37q | 3.7 | npm | markdown-it | 14.3.0 | 14.3.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-952p-6rrq-rcjv | 5.3 | npm | micromatch | 3.1.10 | 4.0.8 | pnpm-lock.yaml |
| https://osv.dev/GHSA-23c5-xmqv-rm74 | 7.5 | npm | minimatch | 10.1.1 | 10.2.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3ppc-4f35-3m26 | 8.7 | npm | minimatch | 10.1.1 | 10.2.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-7r86-cg39-jmmj | 7.5 | npm | minimatch | 10.1.1 | 10.2.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-hrvq-x7jp-36xv | 5.8 | npm | nx | 23.1.1 | 23.2.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w3vv-58gj-gw77 | 8.5 | npm | nx | 23.1.1 | 23.1.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9wv6-86v2-598j | 7.7 | npm | path-to-regexp | 6.1.0 | 6.3.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-477h-4r7f-fvrx | 6.3 | npm | pbkdf2 | 3.1.6 | 3.1.7 | pnpm-lock.yaml |
| https://osv.dev/GHSA-67c8-pqhq-4rmx | 9.2 | npm | piscina | 4.9.3 | 4.9.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rj75-hqrm-r3gf | 5.9 | npm | postcss-selector-parser | 6.1.4 | 6.1.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rj75-hqrm-r3gf | 5.9 | npm | postcss-selector-parser | 7.1.5 | 7.1.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2pr8-phx7-x9h3 | 5.3 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-66ff-xgx4-vchm | 7.7 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-685m-2w69-288q | 7.5 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-75px-5xx7-5xc7 | 8.1 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-f38q-mgvj-vph7 | 5.3 | npm | protobufjs | 6.11.6 | 7.6.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-fx83-v9x8-x52w | 5.3 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-jggg-4jg4-v7c6 | 5.3 | npm | protobufjs | 6.11.6 | 7.5.8 | pnpm-lock.yaml |
| https://osv.dev/GHSA-jvwf-75h9-cwgg | 7.5 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-q6x5-8v7m-xcrf | 5.3 | npm | protobufjs | 6.11.6 | 7.5.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-wcpc-wj8m-hjx6 | 7.5 | npm | protobufjs | 6.11.6 | 7.6.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xq3m-2v4x-88gg | 9.8 | npm | protobufjs | 6.11.6 | 7.5.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-jqcg-44mw-7w3h | 9.1 | npm | proxy-addr | 2.0.7 | 2.0.8 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4mjr-xmp4-gh2g | 6.3 | npm | qs | 6.15.3 | 6.16.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-6pq8-jhm2-2vcw | 6.3 | npm | qs | 6.15.3 | 6.16.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-x5fp-wj9c-mxmx | 6.3 | npm | qs | 6.15.3 | 6.16.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5c6j-r48x-rmvq | 8.1 | npm | serialize-javascript | 4.0.0 | 7.0.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-m5mm-p8h7-m29v | 2.1 | npm | serialize-javascript | 4.0.0 | 7.1.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5c6j-r48x-rmvq | 8.1 | npm | serialize-javascript | 6.0.2 | 7.0.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-m5mm-p8h7-m29v | 2.1 | npm | serialize-javascript | 6.0.2 | 7.1.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qj8w-gfj5-8c6v | 5.9 | npm | serialize-javascript | 6.0.2 | 7.0.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rgj7-g3m4-5g8c | 8.9 | npm | sharp | 0.35.3 | 0.35.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-wq5f-xc86-pv6w | 8.9 | npm | sharp | 0.35.3 | 0.35.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-pqg4-j6r4-53mv | 9.2 | npm | shell-quote | 1.10.0 | 1.11.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-pqg4-j6r4-53mv | 9.2 | npm | shell-quote | 1.9.0 | 1.11.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-858h-whjf-mvg5 | 8.1 | npm | simple-git | 3.36.0 | 4.0.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-g4wm-2vf7-vfgr | 8.1 | npm | simple-git | 3.36.0 | 4.0.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-x6jw-m9v5-85vh | 9.2 | npm | simple-git | 3.36.0 | 4.0.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-7w5x-hrqm-74c2 | 8.2 | npm | smol-toml | 1.5.2 | 1.7.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.5.2 | 1.9.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-v3rj-xjv7-4jmq | 5.3 | npm | smol-toml | 1.5.2 | 1.6.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-7w5x-hrqm-74c2 | 8.2 | npm | smol-toml | 1.6.1 | 1.7.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.6.1 | 1.9.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.7.2 | 1.9.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r4xh-jqrq-34v2 | 5.3 | npm | smol-toml | 1.8.0 | 1.9.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-68fv-2mgg-jv7q | 8.7 | npm | source-map-js | 1.2.1 | 1.2.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4vpr-x523-8j87 | 6.1 | npm | svgo | 2.8.3 | 2.8.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w27v-7q3p-w38r | 8.2 | npm | svgo | 2.8.3 | 2.8.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4vpr-x523-8j87 | 6.1 | npm | svgo | 3.3.4 | 3.3.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w27v-7q3p-w38r | 8.2 | npm | svgo | 3.3.4 | 3.3.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-5gmw-xhrv-c9v3 | 9.5 | npm | tinypool | 1.1.1 | 2.1.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-85c8-ppgw-ccpr | 9.5 | npm | tinypool | 1.1.1 | 2.1.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-52f5-9888-hmc6 | 2.5 | npm | tmp | 0.0.33 | 0.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-ph9p-34f9-6g65 | 7.7 | npm | tmp | 0.0.33 | 0.2.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w5p7-h5w8-2hfq | 7.5 | npm | trim | 0.0.1 | 0.0.3 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 5.28.4 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2mjp-6q6p-2qxm | 6.5 | npm | undici | 5.28.4 | 6.24.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-35p6-xmwp-9g52 | 3.7 | npm | undici | 5.28.4 | 6.27.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4992-7rv2-5pvq | 4.6 | npm | undici | 5.28.4 | 6.24.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-8xcm-r25x-g524 | 4.8 | npm | undici | 5.28.4 | 6.28.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 5.28.4 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-c76h-2ccp-4975 | 6.8 | npm | undici | 5.28.4 | 5.28.5 | pnpm-lock.yaml |
| https://osv.dev/GHSA-cxrh-j4jr-qwg3 | 3.1 | npm | undici | 5.28.4 | 5.29.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-g8m3-5g58-fq7m | 3.7 | npm | undici | 5.28.4 | 6.27.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-g9mf-h72j-4rw9 | 5.9 | npm | undici | 5.28.4 | 6.23.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-m8rv-5g2x-5cg5 | 4.2 | npm | undici | 5.28.4 | 6.28.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-p88m-4jfj-68fv | 5.9 | npm | undici | 5.28.4 | 6.27.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 5.28.4 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 5.28.4 | 6.28.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-v3r7-h72x-cjcm | 4.8 | npm | undici | 5.28.4 | 6.28.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-v9p9-hfj2-hcw8 | 7.5 | npm | undici | 5.28.4 | 6.24.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vrm6-8vpv-qv8q | 7.5 | npm | undici | 5.28.4 | 6.24.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vxpw-j846-p89q | 7.5 | npm | undici | 5.28.4 | 6.27.0 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 6.28.0 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3wwx-pv8p-q78v | 5.9 | npm | undici | 6.28.0 | 6.28.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4qv8-2p9j-2685 | 5.9 | npm | undici | 6.28.0 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 6.28.0 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 6.28.0 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 6.28.0 | 6.28.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rfgv-xxqx-mfg5 | 7.5 | npm | undici | 6.28.0 | 6.28.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xjj6-f33q-929c | 7.5 | npm | undici | 6.28.0 | 6.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2gqq-gqf2-x968 | 3.7 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2jfj-6hjv-fm6j | 6.5 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3wwx-pv8p-q78v | 5.9 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3xpg-4rpp-hhhm | 5.9 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4qv8-2p9j-2685 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4w7w-5xrc-9h26 | 7.4 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-55wc-3pg8-jfw6 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-8436-99hf-9mmv | 3.7 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-f72v-6w45-q472 | 5.9 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-pmjh-fq2x-6v4x | 5.9 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rfgv-xxqx-mfg5 | 7.5 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rx4f-c7p8-82vq | 5.9 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w293-vg96-wgc3 | 7.4 | npm | undici | 7.29.0 | 7.29.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xjj6-f33q-929c | 7.5 | npm | undici | 7.29.0 | 7.30.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2gqq-gqf2-x968 | 3.7 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2jfj-6hjv-fm6j | 6.5 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-2m5v-pch6-74hx | 7.4 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3wwx-pv8p-q78v | 5.9 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-3xpg-4rpp-hhhm | 5.9 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4qv8-2p9j-2685 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-4w7w-5xrc-9h26 | 7.4 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-55wc-3pg8-jfw6 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-8436-99hf-9mmv | 3.7 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9fm3-97px-rjf6 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-f72v-6w45-q472 | 5.9 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-pmjh-fq2x-6v4x | 5.9 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-qrxm-fqhp-jwvm | 7.5 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r53p-7pc4-xj5r | 3.7 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rfgv-xxqx-mfg5 | 7.5 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rx4f-c7p8-82vq | 5.9 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vp8m-p9jh-q5pm | 7.4 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w293-vg96-wgc3 | 7.4 | npm | undici | 8.10.0 | 8.10.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-xjj6-f33q-929c | 7.5 | npm | undici | 8.10.0 | 8.12.2 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w5hq-g745-h8pq | 7.5 | npm | uuid | 3.4.0 | 11.1.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-w5hq-g745-h8pq | 7.5 | npm | uuid | 8.3.2 | 11.1.1 | pnpm-lock.yaml |
| https://osv.dev/GHSA-587h-7wmj-h5pm | 7.5 | npm | vite | 8.2.1 | 8.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-698v-4r3x-3vcv | 6.3 | npm | vite | 8.2.1 | 8.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-9jrq-w75r-8gcw | 2.1 | npm | vite | 8.2.1 | 8.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-r825-w8mm-5pxw | 6.3 | npm | vite | 8.2.1 | 8.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-rq7h-c2jc-7f22 | 6.3 | npm | vite | 8.2.1 | 8.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-vfpm-58rq-9qcg | 6.3 | npm | vite | 8.2.1 | 8.2.4 | pnpm-lock.yaml |
| https://osv.dev/GHSA-g3ch-rx76-35fx | 4.2 | npm | vue-template-compiler | 2.7.16 | -- | pnpm-lock.yaml |
| https://osv.dev/GHSA-g84c-rxfj-3j2c | 7.4 | npm | webpack-dev-middleware | 7.4.5 | 7.4.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-mrhx-c7xc-m3w5 | 8.2 | npm | zod | 3.22.4 | 4.6.6 | pnpm-lock.yaml |
| https://osv.dev/GHSA-mrhx-c7xc-m3w5 | 8.2 | npm | zod | 4.4.3 | 4.6.6 | pnpm-lock.yaml |
