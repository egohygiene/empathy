# Agent System Specification

## Metadata

- **Spec ID:** `agent-system`
- **File Name:** `agent-system.spec.md`
- **Status:** Draft
- **Owner:** Ego Hygiene
- **Related Issues:** N/A
- **Related ADRs:** N/A
- **Last Updated:** 2026-07-21

## 1. Purpose

Define a portable, composable customization system for GitHub Copilot, VS Code, Copilot CLI, and other Agent Skills-compatible coding agents.

The system separates role orchestration, reusable procedure, task or domain requirements, ambient repository rules, and immediate work so each concern has one canonical owner.

## 2. Goals

- Provide focused specialist agents with least-privilege tool access.
- Provide reusable skills that load only for relevant work.
- Preserve specifications as authoritative scope and behavior contracts.
- Prevent duplicated instructions and contradictory sources of truth.
- Support both human-invoked and model-selected agents.
- Keep project skills portable across Agent Skills-compatible tools.
- Make every workflow evidence-based, reviewable, and verifiable.

## 3. Non-Goals

- Require one spec for every agent or one agent for every skill.
- Encode repository-specific facts in universal skills.
- Replace project instructions, ADRs, issues, tests, or CI.
- Grant every agent every available tool.
- Automate external writes, publishing, or destructive actions without task-specific authority.

## 4. Conceptual Model

| Layer | Primary question | Canonical responsibility |
| --- | --- | --- |
| Instructions | What rules always apply here? | Repository conventions, commands, architecture facts, and coding standards |
| Specification | What must this system or task accomplish? | Scope, requirements, constraints, interfaces, decisions, and acceptance criteria |
| Skill | How is this class of work performed? | Reusable workflow, decision logic, validation, scripts, references, and assets |
| Agent | Who performs and orchestrates the work? | Role, mission, tools, boundaries, context selection, and skill coordination |
| Issue or prompt | What outcome is needed now? | Concrete task, selected scope, supplied context, and requested deliverable |

Relationships are many-to-many. A Flutter agent may use Flutter engineering, bug-fixing, and test-engineering skills while following several feature specifications. A skill may be used by the default agent without a dedicated custom agent.

## 5. Canonical Structure

```text
.
├── .agents/
│   ├── scripts/
│   │   └── validate-agent-system.sh
│   └── skills/
│       └── <skill-name>/
│           ├── SKILL.md
│           ├── scripts/
│           ├── references/
│           └── assets/
├── .github/
│   ├── agents/
│   │   └── <agent-name>.agent.md
│   ├── instructions/
│   │   └── <scope>.instructions.md
│   ├── specs/
│   │   └── <system>.spec.md
│   └── copilot-instructions.md
├── AGENTS.md
└── docs/
    └── ai/
        └── agent-system.md
```

Optional directories must be created only when content requires them. A skill must not include an auxiliary README, changelog, or installation guide.

## 6. Requirements

### 6.1 Agent profiles

- Agent profiles must live under `.github/agents/` and use the `.agent.md` extension.
- Every profile must include a specific `description` in YAML frontmatter.
- Profiles should declare the minimum portable tool aliases required by the role.
- Profiles must use `user-invocable` and `disable-model-invocation`; deprecated `infer` must not be used.
- Profiles should omit fixed model selection unless the workflow has a demonstrated model requirement.
- Profiles must keep procedural detail in skills and task requirements in specifications.
- Profile instructions must remain below the platform's 30,000-character limit.
- A planning or review-only agent must not silently perform production implementation.

### 6.2 Skills

- Project skills must live under `.agents/skills/<skill-name>/SKILL.md`.
- Skill directory and frontmatter `name` must match exactly.
- Skill names must use lowercase letters, digits, and hyphens and must not exceed 64 characters.
- Portable skill frontmatter must contain only `name` and `description`.
- The description must explain both capability and triggering context and must not exceed 1024 characters.
- `SKILL.md` must remain concise and under 500 lines.
- Detailed variants and domain guidance should move to directly linked references.
- Included scripts must be deterministic, documented, and tested with representative input.
- Resources must not duplicate content owned by the skill body or another canonical source.

### 6.3 Specifications

- Specifications must live under `.github/specs/` and use kebab-case names ending in `.spec.md`.
- Agent profiles must not be stored in the specifications directory.
- Specifications must define requirements and boundaries rather than reusable agent procedure.
- The most specific applicable approved specification takes precedence within its scope.
- Material conflicts must be surfaced rather than silently resolved.

### 6.4 Instructions

- Repository-wide rules should live in `AGENTS.md` or `.github/copilot-instructions.md`.
- Path-specific rules should use `.instructions.md` files with explicit application scope.
- Instructions must not duplicate a complete skill workflow or task specification.
- Repository commands and facts must be verified from maintained automation and configuration.

### 6.5 Issues and prompts

- Immediate work must identify a concrete outcome and relevant scope.
- Tasks should name the applicable spec when discovery cannot infer it safely.
- Acceptance criteria must be observable and validation must be executable.
- External writes and destructive actions require authority from the immediate task, not merely from an agent role.

## 7. Selection and Precedence

Apply instructions in this order when they overlap:

1. Platform and safety rules.
1. Explicit user instructions for the current task.
1. The most specific applicable repository specification or path instruction.
1. Repository-wide instructions and approved architecture decisions.
1. Selected skill workflow.
1. Agent defaults.
1. General engineering practice.

Do not use precedence to conceal a contradiction. Record material conflicts and request a decision when the result changes behavior, architecture, data safety, security, or acceptance criteria.

## 8. Validation Plan

- Run `.agents/scripts/validate-agent-system.sh` from any directory within the repository.
- Use the editor's customization diagnostics to confirm agent and skill discovery.
- Invoke each skill with at least one representative request.
- Confirm that review-only agents do not make production changes.
- Confirm that implementation agents run repository-mandated validation.
- Check all relative links after moving or renaming artifacts.
- Revalidate against current official platform documentation when customization syntax changes.

## 9. Acceptance Criteria

- [ ] Every supplied specialist role has a valid profile under `.github/agents/`.
- [ ] Every reusable procedure has a valid skill under `.agents/skills/`.
- [ ] Detailed Flutter guidance is available through on-demand references.
- [ ] Misplaced agent files and operating-system metadata are absent from `.github/specs/`.
- [ ] Agent profiles reference applicable skills and authoritative specifications.
- [ ] Skill metadata passes naming and description validation.
- [ ] Agent tool access follows least privilege.
- [ ] The bundle validation script passes.
- [ ] Documentation explains the mapping without requiring a forced one-to-one relationship.

## 10. Open Questions

- Should repository-wide `AGENTS.md` and `.github/copilot-instructions.md` be consolidated in a later batch?
- Which agents should gain VS Code-only handoffs after the cross-environment baseline is stable?
- Should complex skills use forked context after that experimental behavior matures across supported tools?
- Which validation checks should be promoted into CI?
