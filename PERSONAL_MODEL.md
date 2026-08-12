---
schema: aether.architecture-document/v1
id: empathy-personal-model
title: Empathy Personal Model
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-11
updated: 2026-08-11
governed_by:
  - architecture-personal-model
depends_on:
  - empathy-purpose
  - empathy-vision
  - empathy-principles
  - empathy-epistemology
  - empathy-ontology
related:
  - empathy-ai-constitution
  - empathy-design
  - empathy-design-system
supersedes: []
---

# Empathy Personal Model

## Introduction

Empathy is a repository foundation, not a system for modeling individuals. It nevertheless encodes
assumptions about maintainers, contributors, adopters, users affected by software, and other people
who encounter repository processes. This document makes those assumptions explicit and constrains
how downstream profiles, automation, and AI assistance may represent people.

## Human Assumptions

- People have limited and variable time, attention, energy, expertise, access, and confidence.
- People can hold several repository roles at once, and those roles can change.
- Behavior visible in Git history or a platform event does not reveal a person's full intent,
  identity, ability, or circumstances.
- People make mistakes and need understandable feedback, recovery, and correction paths.
- Accessibility needs, communication styles, languages, devices, and working contexts vary.
- Participation volume, speed, compliance, and engagement are not universal measures of value or
  well-being.

These are design assumptions, not diagnoses or claims about a particular person.

## Person and Representation

A person is distinct from every representation a repository can hold: username, email, commit,
issue, role, permission, contribution count, label, profile, generated summary, or inferred
preference.

Representations are partial, contextual, fallible, and purpose-bound. They must not silently become
portable identity records or permanent judgments.

## Agency and Autonomy

Repository experiences should preserve meaningful human control. People should be able to:

- understand what an action, check, automation, or profile will do;
- choose among relevant options when a choice exists;
- stop or avoid optional automation;
- review and contest consequential output;
- recover from ordinary mistakes without disproportionate cost;
- escalate when an automated path does not fit their context.

No metric or automation objective outranks safety, consent, repository policy, or explicit human
authority.

## Identity and Self-Description

Use the identity information a person intentionally supplies for the relevant context. Do not infer
gender, disability, health, ethnicity, religion, sexuality, socioeconomic status, neurotype,
motivation, or other sensitive traits from contribution behavior, language, timing, or repository
metadata.

Names, pronouns, roles, affiliations, and preferences may change. Corrections should propagate to
active representations where practical without rewriting immutable historical records deceptively.

## Context and Relationships

A person's action is interpreted within its repository, task, authority, and communication context.
The same person may be a maintainer in one repository, an adopter in another, and a new contributor
in a third. Authority does not transfer between those scopes automatically.

Relationships such as maintainer, reviewer, contributor, and recipient require verification when an
action depends on identity. Familiarity or prior interaction is not blanket consent.

## Needs, Intentions, and Motivations

Empathy does not assume that visible behavior proves intention. A delayed response may reflect
capacity, access, priority, uncertainty, health, or many unknown factors. A failed check indicates a
contract result, not carelessness or competence. A contribution is not consent to profiling,
marketing, or unrelated analysis.

When intent matters, ask or rely on an explicit request rather than infer it from activity.

## Growth and Change

People, projects, skills, needs, and relationships change. The foundation should support learning,
correction, and evolving responsibility rather than preserve avoidable labels as permanent identity.
Historical evidence remains historically scoped.

## Consent

Consent is informed, contextual, specific, and revocable where the underlying action is reversible.
Accepting a repository's contribution terms does not imply consent to unrelated data use or AI
profiling. Optional telemetry, personalization, external publication, or person-directed automation
requires its own clear basis and controls.

Public repository data may be visible, but visibility alone does not make every reuse respectful or
necessary.

## Privacy and Inference Boundaries

The universal foundation should minimize personal data and avoid hidden profiling. It may process
repository metadata necessary for access, attribution, review, security, and automation, but it
should not:

- infer sensitive traits without an explicit, legitimate, reviewed requirement;
- rank people by engagement, velocity, sentiment, or predicted value;
- combine unrelated activity into a behavioral profile;
- expose private context in generated reports, issues, prompts, or logs;
- retain personal data merely because a tool can collect it.

Security and abuse investigations may require bounded evidence handling under applicable policy and
human authority. They do not erase proportionality, confidentiality, or contestability.

## Correction and Contestability

Consequential representations and AI-generated summaries should identify their source and provide a
path to correction or human review. A person should not have to debate an opaque model to correct a
simple factual error.

Immutable records may receive a corrective follow-up rather than silent historical rewriting.
Disputes remain visible to authorized reviewers until resolved.

## Limits of the Model

Empathy does not define a universal model of personality, productivity, wellness, morality, or
community health. It does not diagnose individuals or predict behavior. It cannot know unexpressed
needs or intent. Consumer repositories may serve domains with stricter human-subject, accessibility,
privacy, safety, or legal requirements; this baseline does not replace them.

## Architectural Implications

- Contributor and issue templates should use direct, respectful, nonjudgmental language.
- Automation results describe artifacts and contracts, not personal qualities.
- AI agents remain explicitly non-human actors with bounded authority.
- Metrics and repository intelligence must avoid hidden person-level scoring.
- Optional data collection and person-directed actions require explicit purpose and scope.
- Accessibility, cognitive load, recovery, and alternative paths are design requirements.
- Consumer profiles may strengthen these protections but must not silently weaken the universal
  boundary.

## Assumptions and Open Questions

- **Observed:** Current repository intelligence and quality automation operate primarily on Git,
  files, dependencies, workflows, and reports rather than a person model.
- **Unverified:** Community-health contracts and accessibility review procedures are not yet complete
  in the active repository foundation.
- **Open:** Which repository-intelligence metrics, if any, are appropriate for universal
  organization health without turning contributors into scores?
- **Open:** What consumer domains require a stricter personal model or explicit exclusion from a
  universal profile?

## Validation

- Governing specification: `architecture-personal-model` version `2.0.0`.
- People remain distinct from representations, accounts, roles, events, and inferences.
- Agency, identity, context, consent, privacy, correction, uncertainty, and model limits are explicit.
- The document contains no diagnosis, fixed persona, sensitive-trait inference, or claim that
  engagement equals benefit.
