# Architecture Notes for Future Anime Compiler

## Purpose

These notes capture long-term architectural ideas. They are **not**
intended for Version 1 of the project.

## Keep

-   Scene IR as the source of truth.
-   State + Delta (Initial State + Visual Delta = Final State).
-   Complexity budget (one primary motion, one primary transformation,
    one emotional purpose).
-   Prompt Compiler instead of Prompt Enhancer.
-   Compiler diagnostics explaining what was included and omitted.

## Delay

Wait until later before introducing:

-   Environment DNA
-   Symbol Registry
-   Dozens of specification files
-   Highly granular schemas

Extract these only after real reuse appears.

## Add an Animation IR

Pipeline:

Project → Scene IR → Animation IR → Backend Profile → Prompt Compiler →
Backend Prompt

This keeps creative intent independent from Gemini or any future model.

## Reference Authority

Each reference image should declare what it controls:

-   composition
-   identity
-   clothing
-   tattoos
-   palette
-   environment

## Backend Profiles

Gemini-specific behavior belongs in backend profiles, not Scene IR.

## Rename

Prefer: - Prompt Compiler - Prompt Optimization

Instead of: - Prompt Enhancement

## Version 1

Keep Version 1 intentionally small:

1.  Project
2.  Visual DNA
3.  Character DNA
4.  Scene IR
5.  Gemini Backend

## Core Principle

The Scene IR is the source of truth.

The prompt is a compiled artifact and should be considered disposable.
