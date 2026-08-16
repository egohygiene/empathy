# OSV Vulnerability Scan

- Generated: `2026-08-16T01-48-01Z`
- Repository: `egohygiene/empathy`
- Commit: `bcf031139923cc4bd26dbb92b21c86e2beb288eb`
- Severity gate: `high`
- Duration: `11s`

## Findings

| Severity | Count |
| --- | ---: |
| Critical | 2 |
| High | 25 |
| Medium | 21 |
| Low | 5 |
| Unknown | 0 |
| **Total** | **53** |

## Discovery

Discovered 25 artifact(s) across 7 ecosystem label(s).

- `.reports/megalinter/syft/sbom.spdx.json`
- `.staging/.github/skills/drawio/scripts/package.json`
- `.staging/.github/skills/md-to-docx/scripts/package.json`
- `.staging/.github/skills/winmd-api-search/scripts/cache-generator/CacheGenerator.csproj`
- `.staging/devenvironment/containers/services/api/poetry.lock`
- `.staging/devenvironment/containers/services/api/pyproject.toml`
- `.staging/devenvironment/realm/pyproject.toml`
- `.staging/react-template/universal/apps/ui/package.json`
- `.staging/react-template/universal/apps/ui/pyproject.toml`
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
- `pyproject.toml`

## Scanned Files

- `.staging/.github/skills/winmd-api-search/scripts/cache-generator/CacheGenerator.csproj`
- `.staging/devenvironment/containers/services/api/poetry.lock`
- `egolint/Cargo.lock`
- `egolint/pnpm-lock.yaml`
- `egolint/uv.lock`

## Skipped Discovered Files

- `.reports/megalinter/syft/sbom.spdx.json`
- `.staging/.github/skills/drawio/scripts/package.json`
- `.staging/.github/skills/md-to-docx/scripts/package.json`
- `.staging/devenvironment/containers/services/api/pyproject.toml`
- `.staging/devenvironment/realm/pyproject.toml`
- `.staging/react-template/universal/apps/ui/package.json`
- `.staging/react-template/universal/apps/ui/pyproject.toml`
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
- `pyproject.toml`

## OSV Scanner Report


Total 20 packages affected by 53 known vulnerabilities (2 Critical, 25 High, 21 Medium, 5 Low, 0 Unknown) from 2 ecosystems.
50 vulnerabilities can be fixed.

| OSV URL | CVSS | Ecosystem | Package | Version | Fixed Version | Source |
| --- | --- | --- | --- | --- | --- | --- |
| https://osv.dev/PYSEC-2026-2120 | 9.8 | PyPI | black | 25.1.0 | 26.3.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2121<br/>https://osv.dev/GHSA-3936-cmfr-pm3m | 8.7 | PyPI | black | 25.1.0 | 26.3.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2132 | 7.2 | PyPI | click | 8.2.1 | 8.3.3 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2141<br/>https://osv.dev/GHSA-r6ph-v2qm-q3c2 | 8.2 | PyPI | cryptography | 45.0.4 | 46.0.5 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-35<br/>https://osv.dev/GHSA-m959-cc7f-wv43 | 5.3 | PyPI | cryptography | 45.0.4 | 46.0.6 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3552<br/>https://osv.dev/GHSA-g6cj-pr64-35w5 | 8.2 | PyPI | cryptography | 45.0.4 | 50.0.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3553<br/>https://osv.dev/GHSA-jwv3-5hgf-82ww | 8.7 | PyPI | cryptography | 45.0.4 | 49.0.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-3554<br/>https://osv.dev/GHSA-m2h6-j472-rp4c | 6.9 | PyPI | cryptography | 45.0.4 | 49.0.0 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-36<br/>https://osv.dev/GHSA-p423-j2cm-9vmq | 9.8 | PyPI | cryptography | 45.0.4 | 46.0.7 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-537c-gmf6-5ccf | 7.5 | PyPI | cryptography | 45.0.4 | 48.0.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1374<br/>https://osv.dev/GHSA-qmgc-5h2g-mvrw | 5.3 | PyPI | filelock (dev) | 3.18.0 | 3.20.3 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-1375<br/>https://osv.dev/GHSA-w853-jp5j-5j7f | 6.3 | PyPI | filelock (dev) | 3.18.0 | 3.20.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-215<br/>https://osv.dev/GHSA-65pc-fj4g-8rjx | 6.9 | PyPI | idna | 3.10 | 3.15 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-70<br/>https://osv.dev/GHSA-fjrm-76x2-c4q4 | 5.3 | PyPI | jwcrypto | 1.5.6 | 1.5.7 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/PYSEC-2026-2617<br/>https://osv.dev/GHSA-2h4p-vjrc-8xpq | 8.7 | PyPI | mako | 1.3.10 | 1.3.12 | .staging/devenvironment/containers/services/api/poetry.lock |
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
| https://osv.dev/PYSEC-2026-2009<br/>https://osv.dev/GHSA-597g-3phw-6986 | 4.5 | PyPI | virtualenv (dev) | 20.31.2 | 20.36.1 | .staging/devenvironment/containers/services/api/poetry.lock |
| https://osv.dev/GHSA-848j-6mx2-7j84 | 5.6 | npm | elliptic | 6.6.1 | -- | egolint/pnpm-lock.yaml |
| https://osv.dev/GHSA-g3ch-rx76-35fx | 4.2 | npm | vue-template-compiler | 2.7.16 | -- | egolint/pnpm-lock.yaml |
