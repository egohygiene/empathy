---
title: Process Specification — Captured Terminal Execution Workflow
version: 1.0.0
date_created: 2026-07-29
last_updated: 2026-07-29
owner: Ego Hygiene
status: draft
tags:
  - process
  - shell
  - terminal
  - validation
  - observability
  - developer-experience
  - reproducibility
---

## Introduction

This specification defines a reusable terminal execution workflow for running
multi-step repository operations non-interactively, capturing complete output
to a temporary artifact, displaying the result in the terminal, and copying
the same result to the system clipboard for review or handoff.

The workflow is designed for safe collaboration between a human operator and
an AI assistant. It turns an ephemeral terminal session into a reproducible,
inspectable execution record without requiring manual output selection.

### 1. Purpose and Scope

This specification standardizes shell snippets used for:

- repository migrations
- validation passes
- cleanup operations
- commits and pushes
- release preparation
- diagnostic collection
- AI-assisted engineering handoffs

The workflow applies to commands executed locally from an interactive shell
but wrapped in a non-interactive Bash process.

The workflow does not define the domain-specific commands being run. It
defines how those commands are executed, observed, preserved, and handed off.

### 2. Core Outcome

Every workflow run must produce the same result in three places:

1. the terminal
2. a timestamped file under the operating system temporary directory
3. the system clipboard when a compatible clipboard command is available

This creates a durable short-lived execution artifact while preserving a fast
copy-and-paste workflow.

### 3. Design Principles

#### 3.1 Non-interactive execution

Commands must not unexpectedly open pagers, editors, credential prompts, or
interactive confirmation interfaces.

The execution environment should set:

    export GIT_PAGER=cat
    export GH_PAGER=cat
    export PAGER=cat
    export GIT_TERMINAL_PROMPT=0

Commands that may prompt must use explicit non-interactive flags or fail
clearly.

#### 3.2 Strict shell behavior

The execution wrapper must use:

    set -Eeuo pipefail

This ensures that:

- failed commands stop the workflow
- unset variables are errors
- pipeline failures are preserved
- error traps can observe inherited failures

#### 3.3 Complete output capture

Both standard output and standard error must be redirected to the same
timestamped file.

The command body should use:

    >"${OUTPUT_FILE}" 2>&1

The captured file is the authoritative execution transcript.

#### 3.4 Show after capture

After the command body completes, the workflow must print the captured output
using `cat`.

This avoids partial output interleaving and ensures the terminal displays the
same content that is stored and copied.

#### 3.5 Clipboard handoff

On macOS, the workflow should copy the output using:

    pbcopy <"${OUTPUT_FILE}"

Portable implementations may detect clipboard tools in this order:

1. `pbcopy`
2. `wl-copy`
3. `xclip`
4. `xsel`

Clipboard failure should not destroy the captured output file.

#### 3.6 Explicit status reporting

The workflow must print:

- output file path
- clipboard status
- command exit status
- repository and branch when repository work is involved

The final exit code must match the wrapped command's result.

### 4. Canonical Execution Pattern

Use the following structure as the default implementation:

    bash <<'BASH'
    set -Eeuo pipefail

    OUTPUT_FILE="/tmp/workflow-name-$(date '+%Y%m%d-%H%M%S').txt"

    export GIT_PAGER=cat
    export GH_PAGER=cat
    export PAGER=cat
    export GIT_TERMINAL_PROMPT=0

    set +e

    (
      set -Eeuo pipefail

      printf 'Workflow context:\n'
      printf 'Working directory: %s\n' "${PWD}"

      # Domain-specific commands go here.
    ) >"${OUTPUT_FILE}" 2>&1

    COMMAND_STATUS=$?

    set -e

    cat "${OUTPUT_FILE}"

    if command -v pbcopy >/dev/null 2>&1; then
      pbcopy <"${OUTPUT_FILE}"
      CLIPBOARD_STATUS="copied with pbcopy"
    elif command -v wl-copy >/dev/null 2>&1; then
      wl-copy <"${OUTPUT_FILE}"
      CLIPBOARD_STATUS="copied with wl-copy"
    elif command -v xclip >/dev/null 2>&1; then
      xclip -selection clipboard <"${OUTPUT_FILE}"
      CLIPBOARD_STATUS="copied with xclip"
    elif command -v xsel >/dev/null 2>&1; then
      xsel --clipboard --input <"${OUTPUT_FILE}"
      CLIPBOARD_STATUS="copied with xsel"
    else
      CLIPBOARD_STATUS="clipboard tool unavailable"
    fi

    printf '\nOutput file: %s\n' "${OUTPUT_FILE}"
    printf 'Clipboard: %s\n' "${CLIPBOARD_STATUS}"
    printf 'Exit status: %s\n' "${COMMAND_STATUS}"

    exit "${COMMAND_STATUS}"
    BASH

### 5. Repository Operation Requirements

#### 5.1 Resolve paths explicitly

Repository workflows must define absolute paths near the top of the script.

Example:

    REPOSITORY="${HOME}/src/egohygiene/aether"

The script must validate that expected directories exist before modifying
content.

#### 5.2 Verify repository identity

Before destructive or publishing operations, verify:

- the path is a Git repository
- the current branch is expected
- the repository working tree is in the expected state
- the remote is configured
- the operator is not accidentally in a parent or sibling repository

Recommended checks include:

    test -d "${REPOSITORY}/.git"
    git -C "${REPOSITORY}" rev-parse --show-toplevel
    git -C "${REPOSITORY}" branch --show-current
    git -C "${REPOSITORY}" status --short --branch

#### 5.3 Guard destructive operations

Deletion, replacement, reset, and cleanup workflows must:

1. list the exact targeted paths
2. verify the expected repository and branch
3. avoid wildcard deletion when explicit paths are available
4. fail when the repository is not in the expected state
5. capture the resulting staged diff before commit

#### 5.4 Separate execution from validation

A repository-changing workflow should present its phases explicitly:

1. preflight
2. execution
3. validation
4. staging
5. commit
6. push
7. final status

Each phase should emit a visible heading with `printf`.

### 6. Output Format

Execution output should be concise but complete.

Every transcript should include, when applicable:

- repository path
- branch name
- remote tracking state
- operation summary
- validation results
- changed-file count
- diff statistics
- commit identifier
- push result
- final Git status

Large file lists should be summarized when the complete list is not necessary
for decision-making.

### 7. Temporary Artifact Rules

#### 7.1 Naming

Temporary output files must use a descriptive prefix and timestamp:

    /tmp/<workflow-name>-YYYYMMDD-HHMMSS.txt

#### 7.2 Lifetime

Temporary artifacts are review records, not permanent repository files.

They may be deleted after:

- the result has been reviewed
- the relevant commit has been pushed
- the output has been transferred into an issue, report, or conversation

#### 7.3 Sensitive information

Before copying output to the clipboard or sharing it, workflows must avoid
printing:

- secrets
- access tokens
- cookies
- private keys
- authentication headers
- unredacted personal data
- proprietary file contents unless intentionally requested

Diagnostic commands should prefer metadata and paths over raw sensitive
content.

### 8. Failure Behavior

A failed domain command must:

1. preserve all output collected before failure
2. print the captured transcript
3. attempt clipboard handoff
4. report the nonzero exit status
5. exit with that same status

The workflow must not hide a failure merely because output capture or
clipboard transfer succeeded.

Clipboard failure may be reported as a warning when the output file remains
available.

### 9. Bash Style Requirements

Reusable Bash functions should use shdoc-compatible documentation.

Example:

    # @description Copy a captured workflow transcript to the first available
    # clipboard provider.
    # @arg $1 string Path to the transcript file.
    # @stdout Clipboard provider status.
    # @exitcode 0 Clipboard copy succeeded.
    # @exitcode 1 No supported clipboard provider was available.
    copy_transcript_to_clipboard() {
      local transcript_path="$1"
      # Implementation.
    }

Scripts must:

- prefer `printf` over `echo`
- use descriptive variable names
- quote variable expansions
- use long-form command flags when supported
- avoid implicit current-directory assumptions
- include clear error messages
- preserve the wrapped command's exit status

### 10. Validation Requirements

A conforming workflow must be tested for:

- successful command execution
- failing command execution
- standard error capture
- paths containing spaces
- missing repository directories
- unexpected Git branches
- unavailable clipboard commands
- output file creation
- matching terminal and clipboard content
- correct final exit status

### 11. Acceptance Criteria

- [ ] The command runs through an explicit Bash wrapper.
- [ ] Strict shell settings are enabled.
- [ ] Interactive pagers and Git prompts are disabled.
- [ ] Standard output and standard error are captured together.
- [ ] Output is written to a timestamped temporary file.
- [ ] The complete transcript is printed after execution.
- [ ] The transcript is copied to the clipboard when supported.
- [ ] Clipboard failure does not lose the transcript.
- [ ] The output file path is printed.
- [ ] The wrapped command's exit status is printed and preserved.
- [ ] Repository workflows verify repository identity and branch.
- [ ] Destructive workflows target explicit paths.
- [ ] Sensitive data is not emitted unintentionally.
- [ ] Bash functions use shdoc-compatible documentation.
- [ ] `printf` is preferred over `echo`.

### 12. Recommended Adoption

Store this specification at:

    .github/specs/process/terminal-execution-capture.spec.md

Reusable implementation should eventually live in a shared engineering
repository as a script or shell library, while individual repositories consume
it through a stable command or task interface.
