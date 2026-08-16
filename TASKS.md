# Repository tasks

Empathy uses [Task](https://taskfile.dev/) as the human- and automation-facing
command contract. Run `task` or `task --list` for the current public surface and
`task --summary <name>` for a task's longer operational notes.

## Lifecycle contract

The universal lifecycle stays intentionally small and predictable:

| Command       | Purpose                                                                                                              |
| ------------- | -------------------------------------------------------------------------------------------------------------------- |
| `task setup`  | Install managed dependencies and repository-owned Git hooks; may use package registries and modify local Git config. |
| `task doctor` | Inspect the required and profile-specific local toolchain without changing the host.                                 |
| `task format` | Apply supported repository formatting.                                                                               |
| `task lint`   | Run the canonical holistic Egolint policy.                                                                           |
| `task test`   | Run root and Egolint unit tests.                                                                                     |
| `task build`  | Build the incubated Rust holons and React + Vite pack.                                                               |
| `task check`  | Run the complete deterministic validation contract.                                                                  |
| `task ci`     | Reproduce the deterministic CI contract locally.                                                                     |

## Namespaces

| Namespace     | Owner                                                     |
| ------------- | --------------------------------------------------------- |
| `beacon:`     | Document-template packages and Rust CLI                   |
| `egolint:`    | Direct MegaLinter and language/tool descriptors           |
| `garden:`     | Mindgarden indexing, context, projection, and Quartz site |
| `git:`        | Read-only Git inspection helpers                          |
| `identity:`   | Identity validation, planning, and handoff                |
| `mantle:`     | Repository development-environment contract               |
| `react-vite:` | Incubated React + Vite repository pack                    |
| `tool:`       | Complementary non-MegaLinter tools                        |

The root [`Taskfile.yml`](Taskfile.yml) only composes modules and subsystem
Taskfiles. Universal task implementations live under [`.tasks/`](.tasks/), and
subsystems retain their own Taskfiles and namespaces.

## Command catalog

This table is generated from `task --list --json`; do not edit it manually.
After changing a public task name, description, or alias, run
`task taskfile:catalog:write` and commit the result. Validation uses
`task taskfile:check`.

<!-- prettier-ignore-start -->
<!-- BEGIN GENERATED TASK CATALOG -->

_Generated from the live Taskfile graph: 248 public commands._

| Command | Description | Aliases |
| --- | --- | --- |
| `task architecture:check` | Validate the architecture document inventory and dependency graph | — |
| `task beacon:check` | Validate Beacon templates and Rust CLI | — |
| `task beacon:default` | List Beacon tasks | `beacon` |
| `task beacon:list` | List installed Beacon templates | — |
| `task beacon:smoke` | Exercise Beacon project generation through the compiled CLI | — |
| `task beacon:validate` | Validate installed Beacon templates through the Rust CLI | — |
| `task build` | Build the incubated Rust holons and React + Vite pack | — |
| `task check` | Run the complete deterministic repository validation contract | — |
| `task ci` | Reproduce the complete deterministic repository CI contract locally | — |
| `task commit:create` | Create an emoji Conventional Commit with Commitizen | — |
| `task commit:test` | Validate canonical commit-message fixtures | — |
| `task commit:validate` | Validate a commit-message file passed after -- | — |
| `task default` | List the repository task contract | — |
| `task doctor` | Diagnose the core repository toolchain without changing the host | — |
| `task egolint:actionlint` | Validate GitHub Actions workflows with actionlint | — |
| `task egolint:all` | Lint the complete repository with the holistic profile | — |
| `task egolint:ansible` | Run the Ansible descriptor family | — |
| `task egolint:arm` | Validate Azure Resource Manager templates with ARM TTK | — |
| `task egolint:bandit` | Analyze Python security with Bandit | — |
| `task egolint:betterleaks` | Scan source for committed secrets with Betterleaks | — |
| `task egolint:black` | Validate Python formatting with Black | — |
| `task egolint:black:fix` | Format Python source with Black | — |
| `task egolint:changed` | Alias for the deterministic changed-file profile | — |
| `task egolint:checkmake` | Analyze Makefiles with Checkmake | — |
| `task egolint:checkov` | Scan infrastructure-as-code and deployment configuration with Checkov | — |
| `task egolint:checkstyle` | Analyze Java source with Checkstyle | — |
| `task egolint:chktex` | Analyze LaTeX source with ChkTeX | — |
| `task egolint:clang-format` | Validate C and C++ formatting with clang-format | — |
| `task egolint:clang-format-c` | Validate C formatting with clang-format | — |
| `task egolint:clippy` | Analyze Rust crates with Clippy | — |
| `task egolint:clippy:fix` | Apply supported Clippy fixes | — |
| `task egolint:clj-kondo` | Analyze Clojure source with clj-kondo | — |
| `task egolint:cljstyle` | Validate Clojure formatting with cljstyle | — |
| `task egolint:cloudformation` | Validate AWS CloudFormation templates with cfn-lint | — |
| `task egolint:coffeescript` | Validate CoffeeScript source with CoffeeLint | — |
| `task egolint:commit:create` | Create an emoji Conventional Commit with Commitizen | — |
| `task egolint:commit:test` | Validate the canonical valid and invalid commit-message fixtures | — |
| `task egolint:commit:validate` | Validate a commit-message file passed after -- | — |
| `task egolint:contracts` | Validate MegaLinter v10 variables, profiles, fixtures, and generated inventory | — |
| `task egolint:contracts:write` | Regenerate the MegaLinter tool matrix and profile snapshots | — |
| `task egolint:cspell` | Spell-check repository source and documentation with CSpell | — |
| `task egolint:dart-analyze` | Analyze Dart and Flutter source with Dart Analyzer | — |
| `task egolint:debug` | Run MegaLinter with diagnostic output | — |
| `task egolint:default` | Run the canonical holistic MegaLinter quality suite | `egolint` |
| `task egolint:dependencies:ensure` | Ensure locked workspace dependencies are installed | — |
| `task egolint:devskim` | Scan repository source for insecure coding patterns with DevSkim | — |
| `task egolint:dockerfile` | Run the Dockerfile descriptor family | — |
| `task egolint:doctor` | Validate MegaLinter runtime and repository configuration | — |
| `task egolint:dry-run` | Print the redacted MegaLinter container command | — |
| `task egolint:editorconfig` | Validate files against EditorConfig policy | — |
| `task egolint:eslint` | Analyze JavaScript, TypeScript, and React source with ESLint | — |
| `task egolint:eslint-jsx` | Analyze JSX source with the repository ESLint toolchain | — |
| `task egolint:eslint-tsx` | Analyze TSX source with the repository ESLint toolchain | — |
| `task egolint:eslint-typescript` | Analyze TypeScript source with the repository ESLint toolchain | — |
| `task egolint:fast` | Lint changed files with the deterministic 12-linter profile | — |
| `task egolint:fix` | Apply fixes from all supported linters | — |
| `task egolint:flake8` | Analyze Python compatibility policy with Flake8 | — |
| `task egolint:gherkin` | Validate Gherkin feature files with gherkin-lint | — |
| `task egolint:gitleaks` | Scan Git history for committed credentials with Gitleaks | — |
| `task egolint:graphql-schema` | Validate GraphQL schema conventions | — |
| `task egolint:groovy` | Validate Groovy and Jenkinsfiles with npm-groovy-lint | — |
| `task egolint:grype` | Scan repository packages for known vulnerabilities with Grype | — |
| `task egolint:hadolint` | Validate Dockerfiles with Hadolint | — |
| `task egolint:holistic` | Lint the complete repository with every supported Egolint descriptor | — |
| `task egolint:hooks:check` | Verify the canonical Husky hook path and hook executability | — |
| `task egolint:hooks:install` | Install Husky as the repository's sole Git hook manager | — |
| `task egolint:htmlhint` | Validate HTML structure and accessibility with HTMLHint | — |
| `task egolint:isort` | Validate Python import ordering with isort | — |
| `task egolint:isort:fix` | Sort Python imports with isort | — |
| `task egolint:javascript` | Run the JavaScript descriptor family | — |
| `task egolint:jscpd` | Detect duplicated source blocks with jscpd | — |
| `task egolint:json` | Run the JSON descriptor family | — |
| `task egolint:jsonlint` | Validate strict JSON syntax with jsonlint | — |
| `task egolint:kics` | Scan infrastructure-as-code with KICS | — |
| `task egolint:latexindent:check` | Check LaTeX formatting with latexindent | — |
| `task egolint:latexindent:format` | Format a LaTeX file with latexindent | — |
| `task egolint:license:check` | Verify first-party SPDX headers and repository-wide REUSE compliance | — |
| `task egolint:lintr` | Analyze R and R Markdown source with lintr | — |
| `task egolint:ls-lint` | Validate repository file and directory naming conventions | — |
| `task egolint:luacheck` | Analyze Lua source with Luacheck | — |
| `task egolint:lychee` | Validate repository links with Lychee | — |
| `task egolint:markdown` | Run the Markdown descriptor family | — |
| `task egolint:markdown-link-check` | Validate links in Markdown files | — |
| `task egolint:markdownlint` | Analyze Markdown files with markdownlint | — |
| `task egolint:markdownlint:fix` | Fix supported Markdown findings with markdownlint | — |
| `task egolint:mypy` | Type-check Python source with Mypy | — |
| `task egolint:npm-package-json` | Validate package.json files with npm-package-json-lint | — |
| `task egolint:php` | Run the complete PHP analysis suite | — |
| `task egolint:phpcs` | Validate PHP coding conventions with PHP_CodeSniffer | — |
| `task egolint:phpcs:fix` | Fix supported PHP coding-standard findings with PHPCBF | — |
| `task egolint:phplint` | Validate PHP syntax with PHPLint | — |
| `task egolint:phpstan` | Analyze PHP types and correctness with PHPStan | — |
| `task egolint:pmd` | Analyze Java source with PMD | — |
| `task egolint:powershell` | Analyze PowerShell source with PSScriptAnalyzer | — |
| `task egolint:powershell-all` | Run PowerShell analysis and formatting checks | — |
| `task egolint:powershell-formatter` | Validate PowerShell formatting with PSScriptAnalyzer | — |
| `task egolint:powershell-formatter:fix` | Format PowerShell source with PSScriptAnalyzer | — |
| `task egolint:precommit:all` | Run the complete pre-commit profile against all tracked files | — |
| `task egolint:precommit:staged` | Run the structural and security profile against staged files | — |
| `task egolint:prettier` | Validate supported files with Prettier | — |
| `task egolint:prettier-json` | Validate JSON formatting with Prettier | — |
| `task egolint:prettier-json:fix` | Format JSON files with Prettier | — |
| `task egolint:prettier-typescript` | Validate TypeScript formatting with Prettier | — |
| `task egolint:prettier-typescript:fix` | Format TypeScript files with Prettier | — |
| `task egolint:prettier-yaml` | Validate YAML formatting with Prettier | — |
| `task egolint:prettier-yaml:fix` | Format YAML files with Prettier | — |
| `task egolint:prettier:fix` | Format supported files with Prettier | — |
| `task egolint:prose` | Run the complete prose-quality suite | — |
| `task egolint:proselint` | Analyze technical prose with Proselint | — |
| `task egolint:protolint` | Analyze Protocol Buffer definitions with protolint | — |
| `task egolint:protolint:fix` | Fix supported Protocol Buffer style findings with protolint | — |
| `task egolint:psalm` | Analyze PHP types and data flow with Psalm | — |
| `task egolint:puppet-lint` | Analyze Puppet manifests with puppet-lint | — |
| `task egolint:pylint` | Analyze Python maintainability with Pylint | — |
| `task egolint:pyright` | Type-check Python source with Pyright | — |
| `task egolint:python` | Run the active Python quality suite | — |
| `task egolint:raku` | Compile and validate Raku source files | — |
| `task egolint:remark-lint` | Analyze Markdown syntax trees with remark-lint | — |
| `task egolint:revive` | Analyze Go source with Revive | — |
| `task egolint:rstcheck` | Validate reStructuredText syntax and embedded code with rstcheck | — |
| `task egolint:rubocop` | Analyze Ruby source with RuboCop | — |
| `task egolint:rubocop:fix` | Apply safe RuboCop autocorrections | — |
| `task egolint:ruff` | Analyze Python source with Ruff | — |
| `task egolint:ruff:fix` | Apply supported Ruff lint and formatting fixes | — |
| `task egolint:salesforce-apex` | Analyze Salesforce Apex with Code Analyzer | — |
| `task egolint:scalafix` | Analyze and rewrite Scala syntax with Scalafix | — |
| `task egolint:scalafix:fix` | Apply supported Scalafix syntactic rewrites | — |
| `task egolint:secretlint` | Scan the repository for committed secrets with Secretlint | — |
| `task egolint:secrets:check` | Scan all tracked files against the reviewed Detect Secrets baseline | — |
| `task egolint:shell` | Run the Bash and shell descriptor families | — |
| `task egolint:snakefmt` | Validate Snakemake formatting with Snakefmt | — |
| `task egolint:snakefmt:fix` | Format Snakemake files with Snakefmt | — |
| `task egolint:spellcheck` | Run spelling and prose-related linters | — |
| `task egolint:sqlfluff` | Analyze SQL syntax and style with SQLFluff | — |
| `task egolint:sqlfluff:fix` | Apply supported SQLFluff formatting fixes | — |
| `task egolint:stylelint` | Validate CSS and stylesheet conventions with Stylelint | — |
| `task egolint:stylelint:fix` | Fix supported CSS findings with Stylelint | — |
| `task egolint:swiftlint` | Analyze Swift source with SwiftLint | — |
| `task egolint:swiftlint:fix` | Apply supported SwiftLint corrections | — |
| `task egolint:syft` | Generate repository SBOMs with Syft | — |
| `task egolint:tekton-lint` | Analyze Tekton Tasks and Pipelines with tekton-lint | — |
| `task egolint:terraform` | Run the Terraform descriptor family | — |
| `task egolint:terragrunt` | Validate Terragrunt HCL formatting | — |
| `task egolint:terragrunt:fix` | Format Terragrunt HCL files | — |
| `task egolint:terrascan` | Run deprecated Terrascan compatibility analysis | — |
| `task egolint:tflint` | Analyze Terraform modules with TFLint | — |
| `task egolint:trivy` | Scan repository security with Trivy | — |
| `task egolint:trivy-all` | Run Trivy security scanning and SBOM generation | — |
| `task egolint:trivy-sbom` | Generate a CycloneDX repository SBOM with Trivy | — |
| `task egolint:trufflehog` | Scan repository files for exposed credentials with TruffleHog | — |
| `task egolint:tsqllint` | Analyze T-SQL source with TSQLLint | — |
| `task egolint:tsqllint:fix` | Apply supported TSQLLint fixes | — |
| `task egolint:v8r-yaml` | Validate YAML files against matching JSON Schemas with v8r | — |
| `task egolint:vale` | Analyze editorial style and terminology with Vale | — |
| `task egolint:yaml` | Run the YAML descriptor family | — |
| `task egolint:yamllint` | Validate YAML syntax and style with yamllint | — |
| `task format` | Format supported text files | — |
| `task format:check` | Verify supported text formatting | — |
| `task garden:check` | Validate the incubated Mindgarden contract and Empathy garden | — |
| `task garden:context` | Render Empathy's default reviewed context pack | — |
| `task garden:index` | Materialize the disposable deterministic Mindgarden catalog | — |
| `task garden:llms:write` | Regenerate the committed llms.txt agent entrypoint | — |
| `task garden:publish` | Materialize the disposable reviewed-public projection | — |
| `task garden:publish:check` | Verify the deterministic reviewed-public projection | — |
| `task garden:site:build` | Build the public garden with the pinned Quartz engine | — |
| `task garden:site:serve` | Serve the public garden locally with the pinned Quartz engine | — |
| `task git:branch` | Print the current Git branch | — |
| `task git:changes` | Summarize unstaged and staged changes separately | — |
| `task git:contributors` | List contributors ordered by commit count | — |
| `task git:heatmap` | Show the twenty most active commit dates | — |
| `task git:remotes` | List configured Git remotes and their fetch and push URLs | — |
| `task git:summary` | Show concise worktree status and the five most recent commits | — |
| `task hooks:check` | Verify Git hook ownership and executability | — |
| `task hooks:install` | Install Husky as the repository's sole Git hook manager | — |
| `task identity:check` | Validate the incubated identity holon and Empathy identity contract | — |
| `task identity:handoff` | Build the contextual creative handoff for Empathy | — |
| `task identity:plan` | Render Empathy's resolved identity target plan | — |
| `task license:check` | Validate MIT/SPDX headers and REUSE compliance | — |
| `task lint` | Lint the complete repository through the canonical holistic policy | — |
| `task lint:all` | Lint the complete repository through the universal Egolint profile | — |
| `task lint:architecture` | Verify the generated lint architecture matches the tool matrices | — |
| `task lint:architecture:write` | Regenerate the lint architecture SVG and Markdown legend | — |
| `task lint:complementary` | Run every applicable non-MegaLinter tool | — |
| `task lint:contracts` | Validate MegaLinter and complementary toolchain contracts | — |
| `task lint:doctor` | Diagnose the local Egolint and MegaLinter runtime | — |
| `task lint:fast` | Lint changed repository files through the deterministic fast policy | — |
| `task lint:fix` | Apply supported Egolint fixes for explicit review | — |
| `task lint:holistic` | Run every supported Egolint descriptor against the repository | — |
| `task mantle:check` | Run the local Mantle validation and installation contract | — |
| `task mantle:ci` | Reproduce the strict Mantle CI contract locally | — |
| `task mantle:default` | List the Mantle task contract | `mantle` |
| `task mantle:docs` | Validate Mantle's documentation contract | — |
| `task mantle:install:smoke` | Exercise a hermetic temporary-prefix install lifecycle | — |
| `task mantle:lint` | Run Mantle's developer-friendly static validation | — |
| `task mantle:status` | Diagnose the repository-local Mantle installation | — |
| `task mantle:test` | Run Mantle's complete developer-friendly validation suite | — |
| `task platform` | Print the host platform detected by Task | — |
| `task precommit:all` | Run the complete manual pre-commit profile | — |
| `task precommit:staged` | Run the automatic structural and security profile | — |
| `task react-vite:analyze` | Build applications and emit bundle-analysis reports. | — |
| `task react-vite:build` | Build every application and package. | — |
| `task react-vite:check` | Run all deterministic quality gates. | — |
| `task react-vite:clean` | Remove generated output. | — |
| `task react-vite:dev` | Run every template application locally. | — |
| `task react-vite:dev:storefront` | Run the optional commerce profile locally. | — |
| `task react-vite:dev:web` | Run the generic web application locally. | — |
| `task react-vite:setup` | Install the workspace dependencies. | — |
| `task react-vite:test:e2e` | Run Playwright end-to-end tests. | — |
| `task sbom:generate` | Generate SPDX and CycloneDX dependency inventories | — |
| `task sbom:scan` | Scan dependency inventories and repository packages for vulnerabilities | — |
| `task secrets:check` | Validate the reviewed scanner baseline | — |
| `task security:dependencies` | Scan discovered dependencies and repository packages for vulnerabilities | — |
| `task security:source` | Run complementary and MegaLinter-native source security checks | — |
| `task setup` | Install managed workspace dependencies and repository Git hooks | — |
| `task taskfile:catalog:write` | Regenerate the complete TASKS.md command catalog | — |
| `task taskfile:check` | Validate Taskfile composition and the generated command catalog | — |
| `task test` | Run root and Egolint unit tests | — |
| `task tool:addlicense` | Validate compatible MIT/SPDX source headers | — |
| `task tool:all` | Run every applicable complementary tool | — |
| `task tool:buf` | Lint Buf Protocol Buffer modules | — |
| `task tool:cargo-deny` | Validate Rust dependency licenses and sources | — |
| `task tool:commitlint` | Validate canonical commit-message fixtures | — |
| `task tool:complexipy` | Enforce Python cognitive-complexity thresholds | — |
| `task tool:conftest` | Evaluate policy-as-code assertions with Conftest | — |
| `task tool:contracts` | Validate the complementary inventory, fixtures, applicability, and generated matrix | — |
| `task tool:contracts:write` | Regenerate the complementary tool matrix | — |
| `task tool:default` | Run every applicable complementary tool | `tool` |
| `task tool:dependencies:python` | Install the locked complementary Python lint environment | — |
| `task tool:dependencies:security` | Install the separately locked Python security group | — |
| `task tool:deptry` | Analyze Python dependency declarations | — |
| `task tool:detect-secrets` | Scan against the reviewed Detect Secrets baseline | — |
| `task tool:govulncheck` | Analyze reachable Go vulnerabilities | — |
| `task tool:interrogate` | Measure Python docstring coverage | — |
| `task tool:knip` | Analyze unused JavaScript and TypeScript project surface | — |
| `task tool:latexindent` | Check LaTeX formatting with latexindent | — |
| `task tool:regal` | Lint Rego policies with Regal | — |
| `task tool:reuse` | Validate source licensing with REUSE | — |
| `task tool:status` | Show applicability and dependency status without executing tools | — |
| `task tool:tombi` | Lint TOML with Tombi | — |
| `task tool:typos` | Detect identifier and prose typos | — |
| `task tool:vacuum` | Lint OpenAPI and AsyncAPI descriptions with Vacuum | — |
| `task tool:versions` | Print the pinned complementary-tool version inventory | — |
| `task tool:vulture` | Detect high-confidence dead Python code | — |
| `task tools:install` | Install the locked complementary Python lint environment | — |
| `task tools:install:security` | Install the separately locked Python security dependency group | — |
| `task tools:status` | Show complementary applicability and dependency state | — |
| `task tools:versions` | Print the pinned complementary tool inventory | — |
| `task version` | Print the repository task-system contract version | — |

<!-- END GENERATED TASK CATALOG -->
<!-- prettier-ignore-end -->

## Operational boundaries

- `setup`, `tools:install*`, and some subsystem commands can access package
  registries; they are never invoked merely by listing or diagnosing tasks.
- `format`, `lint:fix`, and generated `*:write` tasks intentionally modify the
  worktree and require review through Git.
- `garden:site:serve`, `react-vite:dev*`, and interactive authoring commands run
  until stopped.
- Security and SBOM tasks write disposable output under `.reports/`; durable
  remediation and promotion records belong under `.audits/`.
- Deferred product-, host-, or provider-specific definitions remain inert in
  [`.staging/tasks-todo.yml`](.staging/tasks-todo.yml).
