# MegaLinter Remediation Checklist

Use this checklist to validate and remediate each linter independently.

Run a task with:

    task lint:<task-name>

Check an item only after the task completes successfully and its findings have been resolved or intentionally documented.

## Runtime and baseline

- [x] `task lint:doctor` — validate the MegaLinter runtime and repository configuration
- [ ] `task lint:dry-run` — inspect the redacted container command
- [ ] `task lint:all` — run the complete enabled suite after individual remediation is complete

## Actions, infrastructure, and configuration

- [x] `task lint:actionlint` — GitHub Actions
- [x] `task lint:ansible` — Ansible descriptor
- [x] `task lint:arm` — Azure Resource Manager TTK
- [x] `task lint:cloudformation` — AWS CloudFormation
- [x] `task lint:dockerfile` — Dockerfile descriptor
- [x] `task lint:hadolint` — Dockerfiles
- [ ] `task lint:editorconfig` — EditorConfig policy
- [x] `task lint:checkmake` — Makefiles; native task
- [x] `task lint:tekton-lint` — Tekton Tasks and Pipelines
- [x] `task lint:terrascan` — Terrascan compatibility; deprecated/dormant
- [x] `task lint:tflint` — Terraform
- [x] `task lint:terragrunt` — Terragrunt formatting
- [ ] `task lint:yamllint` — YAML syntax and style
- [ ] `task lint:v8r-yaml` — YAML schema validation

## API, data, and schema formats

- [x] `task lint:graphql-schema` — GraphQL schemas
- [ ] `task lint:jsonlint` — JSON syntax
- [ ] `task lint:npm-package-json` — `package.json` policy
- [ ] `task lint:prettier-json` — JSON formatting
- [x] `task lint:protolint` — Protocol Buffers
- [x] `task lint:tsqllint` — T-SQL
- [x] `task lint:sqlfluff` — SQL syntax, style, and formatting

## C, C++, Clojure, CoffeeScript, and Dart

- [ ] `task lint:clang-format-c` — C formatting
- [ ] `task lint:clang-format` — C++ formatting
- [x] `task lint:cljstyle` — Clojure formatting
- [x] `task lint:clj-kondo` — Clojure static analysis
- [x] `task lint:coffeescript` — CoffeeScript
- [ ] `task lint:dart-analyze` — Dart and Flutter analysis

## Go, Groovy, Java, Lua, and Raku

- [x] `task lint:revive` — Go
- [x] `task lint:groovy` — Groovy and Jenkinsfiles
- [x] `task lint:checkstyle` — Java style
- [x] `task lint:pmd` — Java static analysis
- [x] `task lint:luacheck` — Lua
- [x] `task lint:raku` — Raku

## JavaScript, TypeScript, CSS, and HTML

- [ ] `task lint:eslint` — JavaScript, TypeScript, and React through MegaLinter
- [ ] `task lint:eslint-jsx` — JSX through the repository ESLint toolchain
- [ ] `task lint:eslint-typescript` — TypeScript through the repository ESLint toolchain
- [ ] `task lint:eslint-tsx` — TSX through the repository ESLint toolchain
- [ ] `task lint:prettier` — general Prettier validation
- [ ] `task lint:prettier-typescript` — TypeScript formatting
- [ ] `task lint:prettier-yaml` — YAML formatting
- [ ] `task lint:stylelint` — CSS and stylesheets
- [ ] `task lint:htmlhint` — HTML

## Markdown, prose, spelling, links, and reStructuredText

- [ ] `task lint:markdownlint` — Markdown style
- [ ] `task lint:markdown-link-check` — Markdown links
- [ ] `task lint:remark-lint` — Markdown syntax-tree rules; currently dormant if disabled
- [ ] `task lint:cspell` — spelling and project dictionaries
- [ ] `task lint:proselint` — sentence-level prose checks
- [ ] `task lint:vale` — editorial style and terminology
- [ ] `task lint:lychee` — repository links
- [x] `task lint:rstcheck` — reStructuredText

## LaTeX

- [ ] `task lint:chktex` — LaTeX analysis
- [ ] `task lint:latexindent:check` — LaTeX formatting; native task

## PHP, PowerShell, Puppet, Ruby, and Salesforce

- [x] `task lint:phplint` — PHP syntax
- [x] `task lint:phpcs` — PHP coding standards
- [x] `task lint:phpstan` — PHP static typing
- [x] `task lint:psalm` — PHP type and data-flow analysis
- [x] `task lint:powershell` — PowerShell analysis
- [x] `task lint:powershell-formatter` — PowerShell formatting
- [x] `task lint:puppet-lint` — Puppet; currently dormant if disabled
- [x] `task lint:rubocop` — Ruby
- [ ] `task lint:salesforce-apex` — Salesforce Apex

## Python

### Active universal profile

- [ ] `task lint:ruff` — primary Python linting
- [ ] `task lint:bandit` — Python security
- [ ] `task lint:mypy` — static typing
- [ ] `task lint:pylint` — deeper inference and maintainability
- [ ] `task lint:pyright` — static typing and editor parity

### Compatibility profile

- [ ] `task lint:black` — Black formatting compatibility
- [ ] `task lint:flake8` — Flake8 compatibility
- [ ] `task lint:isort` — isort compatibility

## R, Rust, Scala, Swift, and Snakemake

- [x] `task lint:lintr` — R and R Markdown
- [x] `task lint:clippy` — Rust
- [x] `task lint:scalafix` — Scala
- [ ] `task lint:swiftlint` — Swift
- [x] `task lint:snakefmt` — Snakemake formatting

## Repository structure and duplication

- [ ] `task lint:jscpd` — duplicate source blocks
- [ ] `task lint:ls-lint` — repository naming conventions

## Security, secrets, SBOMs, and supply chain

- [ ] `task lint:checkov` — infrastructure-as-code security
- [ ] `task lint:devskim` — insecure coding patterns; currently dormant if disabled
- [ ] `task lint:gitleaks` — Git-oriented secret detection
- [ ] `task lint:grype` — vulnerability scanning
- [ ] `task lint:kics` — infrastructure-as-code security; currently disabled pending upstream safety review
- [ ] `task lint:secretlint` — working-tree secret detection
- [ ] `task lint:syft` — SBOM generation
- [ ] `task lint:trivy` — repository security scanning
- [ ] `task lint:trivy-sbom` — CycloneDX SBOM generation
- [ ] `task lint:trufflehog` — exposed and verified credential detection

## Final aggregate verification

Run these after the individual checklist is complete:

- [ ] `task lint:changed` — validate current worktree changes
- [ ] `task lint:all` — validate the complete enabled suite
- [ ] Review `.engineering/reports/megalinter/`
- [ ] Confirm no unexpected modified files with `git status --short`
- [ ] Confirm no accidental mode changes with `git diff --summary`

## Notes

- Disabled or dormant linters can remain unchecked until their upstream issue, dependency, or compatibility constraint is resolved.
- Fix tasks intentionally are not listed as separate completion items. Use the matching `:fix` task where appropriate, then rerun the non-fix task before checking the item.
- Aggregate descriptor tasks such as `task lint:javascript`, `task lint:json`, `task lint:markdown`, `task lint:spellcheck`, `task lint:terraform`, and `task lint:yaml` are convenience commands rather than separate linter completion requirements.
