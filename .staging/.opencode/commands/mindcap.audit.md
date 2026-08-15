---
description: Audit a Mindcap bundle for transcript fidelity, hidden nodes, attachments, provenance, and coverage.
agent: knowledge-reviewer
subtask: true
---

Audit the Mindcap bundle supplied in `$ARGUMENTS` without modifying it.

Check:

1. The manifest and verifier reports agree with files actually present.
1. The visible transcript contains only user-visible conversation turns.
1. Hidden system, tool, or context nodes are classified separately.
1. Attachments have registry entries, stable identifiers, capture status, and
   provenance.
1. Branch selection and message ordering are explicit.
1. Coverage identifies omitted, uncertain, unsupported, or failed regions.
1. Normalized Markdown and JSON represent the same visible conversation.
1. Sensitive or secret-like material is not copied into the audit response.

Return findings grouped as blocking, important, and polish. Cite bundle-relative
paths and stable message or attachment identifiers. Do not claim completeness
unless coverage evidence supports it.
