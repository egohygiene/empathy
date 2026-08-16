#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Generate the deterministic file-level disposition ledger for ``.staging``."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import io
from pathlib import Path
import re
import subprocess
import sys

EMPTY_BLOB = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
CSV_FIELDS = (
    "source_path",
    "bytes",
    "canonical_owner",
    "incubation_home",
    "canonical_home",
    "disposition",
    "merge_group",
    "trust_class",
    "duplicate_of",
    "flags",
)


@dataclass
class Classification:
    collection: str
    canonical_owner: str
    incubation_home: str
    canonical_home: str
    disposition: str
    merge_group: str
    trust_class: str
    confidence: str
    notes: str


@dataclass
class LedgerRow:
    source_path: str
    bytes: int
    git_mode: str
    git_blob: str
    kind: str
    collection: str
    canonical_owner: str
    incubation_home: str
    canonical_home: str
    disposition: str
    merge_group: str
    trust_class: str
    confidence: str
    duplicate_of: str
    duplicate_action: str
    flags: str
    notes: str


HYGIENE_OWNERS = {
    "33965.png": "egolint",
    "33986.png": "empathy",
    "IMG_20260705_135315.png": "research",
    "IMG_20260725_173315.png": "dreamscape",
    "IMG_20260725_173326.png": "research",
    "IMG_20260725_173346.png": "empathy",
    "Neon tech infographic_ Realm developer environment.png": "realm",
    "aniflow-architecture.png": "aniflow",
    "architecture-design.png": "empathy",
    "egolint-architecture.png": "egolint",
    "file_0000000000e8720c8267d3573a3ab98c.png": "dreamscape",
    "file_000000000428722f94d32cfcdc72d24b.png": "empathy",
    "file_000000000f4881f58c7dfbe4ebed8c04.png": "beacon",
    "file_000000000ffc722f9ca6eb302699b0c1.png": "reflector",
    "file_000000001154722f8ee619fcba1bcc67.png": "empathy",
    "file_0000000013b481f6b4d3deefddfee037.png": "empathy",
    "file_00000000143881f5868734463f460d37.png": "aether",
    "file_0000000015fc722fabc6c07a9e4c36bb.png": "empathy",
    "file_00000000216071f68697b89112908b2a.png": "holon",
    "file_0000000021e081f6856ca695252c15c1.png": "egolint",
    "file_0000000021e481f6b29a419bc4b311a7.png": "holon",
    "file_00000000270c720cae8a8dc846c6cbd3.png": "beacon",
    "file_00000000299481f59cc2fb2899cc2e34.png": "renderflow",
    "file_000000002c1881f68b66f785f5abdd7d.png": "realm",
    "file_000000002c3c71f59cc8d354ef13a47b.png": "identity",
    "file_000000002c6481f6875ab9b29b0e386a.png": "holon",
    "file_000000003b8c722f8bf6f4e3f3ba0585.png": "mindgarden",
    "file_0000000041d4722fa3d832b80f56f190.png": "empathy",
    "file_000000004b6c71f5876cf4a4d194eff3.png": "aether",
    "file_000000004fe071f5b46334e3dbfa7477.png": "aether",
    "file_0000000059dc71f5af1533ffa363427c.png": "empathy",
    "file_000000005a0071f7a9070ca4d6a4f0dc.png": "empathy",
    "file_000000005ce471f5b74deeef246ee6db.png": "aether",
    "file_0000000071b4720cabae6f4b488b8140.png": "dreamscape",
    "file_00000000736c71f5b571dd4fe9aa537c.png": "dreamscape",
    "file_0000000075f471f5a4cba15260da824a.png": "dreamscape",
    "file_0000000082ac81f5931b9e6ef3ea572e.png": "empathy",
    "file_000000009b2c81f5be91f6113e2e3741.png": "aether",
    "file_00000000a26481f69e08d630141671f5.png": "renderflow",
    "file_00000000a43481f6820c6471a16dfd91.png": "identity",
    "file_00000000a964722faa6e6946fd77f81e.png": "reflector",
    "file_00000000aaf0720c84b1917ba66ee1a0.png": "dreamscape",
    "file_00000000af9071f5b21daeac97018df7.png": "research",
    "file_00000000b0dc71f6a4ef589356ba8890.png": "mindgarden",
    "file_00000000b300720ca08e1455f16d35e7.png": "dreamscape",
    "file_00000000b32c81f583a2294dd81ab8fa.png": "dreamscape",
    "file_00000000b71871f78204271e1d7c61ae.png": "mindgarden",
    "file_00000000bc5c722f8313caf63ae053ec.png": "identity",
    "file_00000000bef8720cae15d10fabd96c34.png": "empathy",
    "file_00000000c214822fac33d78c0acf249a.png": "external-incompris",
    "file_00000000c25871f5b03e88f65b73f960.png": "empathy",
    "file_00000000c33071f5bc8d983f29e39d31.png": "empathy",
    "file_00000000c5c071f79196b9191e5c5f3f.png": "empathy",
    "file_00000000c87c722f94df4754ed62c89d.png": "empathy",
    "file_00000000c9a481f5879c3fab78c86e9e.png": "dreamscape",
    "file_00000000cc48722f8232bba67f12f8af.png": "dreamscape",
    "file_00000000cf5081f68e06cf594c88f3ad.png": "mindcap",
    "file_00000000d258720c9ccbeca602b49339.png": "personal-archive",
    "file_00000000dc48720cb3f0b5cd2fc3420e.png": "dreamscape",
    "file_00000000e6c881f681508cafdd35f2e5.png": "realm",
    "file_00000000efdc81f5b175832ccac47cb1.png": "egolint",
    "file_00000000f77c71f5b3930b1e2f4bcb51.png": "empathy",
    "file_00000000f8a081f698d9e0472a3829e0.png": "renderflow",
    "file_00000000fc0081f6b9df9b331da36635.png": "mindgarden",
    "file_00000000fd40722f8dc7d4d656f3c878.png": "dreamscape",
    "markup_7991.png": "empathy",
    "markup_8948.png": "empathy",
    "markup_8964.png": "dreamscape",
    "markup_8966.png": "personal-archive",
    "markup_9109.png": "empathy",
    "markup_9250.png": "empathy",
    "mindgarden-architecture.png": "mindgarden",
    "mindgarden-banner.png": "mindgarden",
}


AWESOME_AGENTIC_WORKFLOWS = {
    "cli-for-beginners-sync",
    "duplicate-resource-detector",
    "learning-hub-updater",
    "pr-duplicate-check",
    "resource-staleness-report",
}

AETHER_WORKFLOWS = {
    "check-plugin-structure.yml",
    "skill-check-comment.yml",
    "skill-check.yml",
    "skill-quality-report.yml",
    "validate-agentic-workflows-pr.yml",
}

AWESOME_WORKFLOWS = {
    "build-website.yml",
    "contributor-check.yml",
    "contributors.yml",
    "deploy-website.yml",
    "medium-rss-sync.yml",
    "pinterest-rss-sync.yml",
    "traffic-reporting.yml",
    "validate-readme.yml",
}

RELAY_WORKFLOWS = {
    "build.yml",
    "check-line-endings.yml",
    "codespell.yml",
    "copilot-setup-steps.yml",
    "development-build.yml",
    "flutter-ci-reusable.yml",
    "label-pr-intent.yml",
    "pr-risk-scan-comment.yml",
    "pr-risk-scan.yml",
    "publish.yml",
    "setup-labels.yml",
    "webhook-caller.yml",
}


def run_git(repository_root: Path, *arguments: str) -> bytes:
    return subprocess.check_output(["git", *arguments], cwd=repository_root, stderr=subprocess.PIPE)


def tracked_entries(repository_root: Path) -> list[tuple[str, str, str]]:
    raw = run_git(repository_root, "ls-files", "-s", "-z")
    entries: list[tuple[str, str, str]] = []
    for record in raw.decode("utf-8", errors="surrogateescape").split("\0"):
        if not record:
            continue
        metadata, path = record.split("\t", 1)
        mode, blob, _stage = metadata.split(" ", 2)
        entries.append((path, mode, blob))
    return entries


def file_kind(path: str, size: int) -> str:
    if size == 0:
        return "empty-placeholder"
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()
    if name == "skill.md":
        return "agent-skill"
    if name.endswith(".agent.md"):
        return "agent"
    if name.endswith(".instructions.md"):
        return "instruction"
    if name.endswith(".spec.md"):
        return "specification"
    if "/workflows/" in path and suffix == ".md":
        return "agentic-workflow-source"
    if "/workflows/" in path and suffix in {".yml", ".yaml"}:
        return "workflow"
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"}:
        return "image"
    if suffix in {".ttf", ".otf", ".pf2"}:
        return "font"
    if suffix in {".sh", ".bash", ".zsh", ".fish", ".ps1", ".mjs", ".js"}:
        return "script"
    if suffix in {".py", ".pyi", ".ts", ".tsx", ".jsx", ".rs"}:
        return "source-code"
    if suffix in {".md", ".txt"}:
        return "documentation"
    if suffix in {".json", ".jsonc", ".yml", ".yaml", ".toml", ".conf"}:
        return "configuration"
    if "dockerfile" in name:
        return "container-build"
    return "artifact"


def aether_community(path: str, relative: str, collection: str) -> Classification:
    executable = file_kind(path, 1) in {"script", "source-code"}
    return Classification(
        collection=collection,
        canonical_owner="aether",
        incubation_home=f"aether/.staging/community/awesome-copilot/{relative}",
        canonical_home=f"aether/library/community/awesome-copilot/{relative}",
        disposition="quarantine-and-curate",
        merge_group="aether-community-awesome-copilot",
        trust_class="quarantined-executable" if executable else "quarantined-instruction",
        confidence="high",
        notes=(
            "Preserve the upstream package boundary; verify provenance, license, prompt safety, "
            "and bundled executable behavior before any generated distribution can activate it."
        ),
    )


def classify_workflow(path: str, relative: str) -> Classification:
    name = Path(relative).name
    stem = name.removesuffix(".lock.yml").removesuffix(".yml").removesuffix(".md")
    if stem in AWESOME_AGENTIC_WORKFLOWS:
        return Classification(
            "awesome-copilot agentic workflows",
            "awesome",
            f"awesome/.staging/.github/workflows/{name}",
            f"awesome/.github/workflows/{name}",
            "preserve-source-and-generated-pair",
            f"awesome-gh-aw-{stem}",
            "privileged-automation",
            "high",
            "Product-specific GitHub Agentic Workflow; keep the Markdown source paired with its generated lock workflow.",
        )
    if name == "codeowner-update.md":
        return Classification(
            "organization agentic workflow source",
            "aether",
            f"aether/.staging/workflows/github-agentic/{name}",
            f"aether/library/organization/workflows/github-agentic/{name}",
            "refactor-source-contract",
            "codeowner-update-agentic-workflow",
            "staged-instruction",
            "high",
            "Aether owns the agent instructions; Relay should own compilation and reusable delivery mechanics.",
        )
    if name == "codeowner-update.lock.yml":
        return Classification(
            "organization agentic workflow build",
            "relay",
            f"relay/.staging/generated/github-agentic/{name}",
            f"relay/generated/github-agentic/{name}",
            "regenerate-after-source-review",
            "codeowner-update-agentic-workflow",
            "privileged-automation",
            "high",
            "Generated output is non-authoritative; regenerate from the accepted Aether source using a pinned compiler.",
        )
    if name in AETHER_WORKFLOWS:
        return Classification(
            "aether consumer automation",
            "aether",
            f"aether/.staging/.github/workflows/{name}",
            f"aether/.github/workflows/{name}",
            "split-policy-from-mechanics",
            f"aether-workflow-{stem}",
            "privileged-automation",
            "high",
            "Keep the Aether-specific policy caller thin and extract reusable mechanics into Relay.",
        )
    if name in AWESOME_WORKFLOWS:
        return Classification(
            "awesome product automation",
            "awesome",
            f"awesome/.staging/.github/workflows/{name}",
            f"awesome/.github/workflows/{name}",
            "preserve-for-product-review",
            f"awesome-workflow-{stem}",
            "privileged-automation",
            "high",
            "This workflow references Awesome-specific website, catalog, contributor, or distribution behavior.",
        )
    if name in RELAY_WORKFLOWS:
        return Classification(
            "reusable repository automation",
            "relay",
            f"relay/.staging/.github/workflows/{name}",
            f"relay/.github/workflows/{name}",
            "refactor-to-reusable-workflow",
            f"relay-workflow-{stem}",
            "privileged-automation",
            "high",
            "Normalize permissions, timeouts, action pins, inputs, and consumer boundaries before activation.",
        )
    return Classification(
        "unclassified workflow",
        "relay",
        f"relay/.staging/.github/workflows/{name}",
        f"relay/.github/workflows/{name}",
        "manual-workflow-review",
        f"relay-workflow-{stem}",
        "privileged-automation",
        "medium",
        "Workflow ownership is likely Relay but its consumer and policy boundary still require confirmation.",
    )


def classify_script(relative: str) -> Classification:
    name = Path(relative).name
    if name == "delete-gone-branches.sh":
        owner, destination, action = "mantle", "mantle/bin/git-delete-gone-branches", "refactor-cli"
    elif name == "fix-line-endings.sh":
        owner, destination, action = (
            "egolint",
            "egolint/scripts/fix-line-endings.sh",
            "merge-with-format-policy",
        )
    elif name == "pr-risk-scan.mjs":
        owner, destination, action = (
            "relay",
            "relay/actions/pr-risk-scan/pr-risk-scan.mjs",
            "extract-composite-action",
        )
    elif name in {"create-skill.mjs", "validate-skills.mjs"}:
        owner, destination, action = "aether", f"aether/tools/{name}", "repair-and-promote"
    else:
        owner, destination, action = (
            "awesome",
            f"awesome/tools/catalog/{relative.removeprefix('scripts/')}",
            "preserve-for-product-review",
        )
    missing_dependency = name in {
        "create-skill.mjs",
        "generate-open-pr-report.mjs",
        "update-readme.mjs",
        "validate-skills.mjs",
    }
    notes = "Imported script; validate command execution, path confinement, and destructive modes before use."
    if missing_dependency:
        notes += " It imports constants.mjs, which is absent from this intake snapshot."
    return Classification(
        "repository support scripts",
        owner,
        destination.replace(f"{owner}/", f"{owner}/.staging/", 1),
        destination,
        action,
        f"{owner}-script-{Path(name).stem}",
        "quarantined-executable",
        "high",
        notes,
    )


def classify_devenvironment(relative: str) -> Classification:
    inner = relative.removeprefix("devenvironment/")
    if inner.startswith("containers/services/api/"):
        suffix = inner.removeprefix("containers/services/api/")
        final = f"holon/templates/universal-app/apps/api/{suffix}"
        group = "holon-universal-app-api"
        if Path(inner).name == "Dockerfile.old":
            final = "holon/templates/universal-app/apps/api/Dockerfile"
            group = "holon-universal-app-api-dockerfile"
        return Classification(
            "universal application API fixture",
            "holon",
            f"holon/.staging/templates/universal-app/apps/api/{suffix}",
            final,
            "merge-into-application-template",
            group,
            "executable-application-fixture",
            "high",
            "Product/API code is a Holon application template; Realm should provide only its environment adapter.",
        )
    if inner.startswith("workstation/shared/shell/"):
        suffix = inner.removeprefix("workstation/shared/shell/")
        return Classification(
            "portable shell session defaults",
            "mantle",
            f"mantle/.staging/runtime/shells/{suffix}",
            f"mantle/runtime/shells/{suffix}",
            "merge-with-shell-runtime",
            "mantle-shell-session-defaults",
            "host-runtime-configuration",
            "high",
            "Mantle owns portable shell behavior; Realm may consume the published profile.",
        )

    final = f"realm/{inner}"
    action = "move-and-refactor"
    group = "realm-development-environment"
    notes = "Realm owns development images, devcontainers, services, orchestration, and workstation profiles."

    if inner in {".devcontainer/devcontainer.json", ".devcontainer/devcontainer2.json"}:
        final = "realm/devcontainers/baseline/.devcontainer/devcontainer.json"
        action = "merge-variants"
        group = "realm-devcontainer-config"
        notes += " Merge both variants; remove personal editor settings, host credential mounts, and unsafe SSH overrides."
    elif inner in {"compose/docker-compose.yml", "compose/docker-compose2.yml"}:
        final = "realm/devcontainers/baseline/compose.yaml"
        action = "merge-and-profile"
        group = "realm-compose-baseline"
        notes += " Split the baseline development service from optional service profiles and replace weak defaults."
    elif inner in {"dockerfiles/todo.Dockerfile", "dockerfiles/todo2.Dockerfile"}:
        final = "realm/images/baseline/Dockerfile"
        action = "merge-variants"
        group = "realm-baseline-image-candidates"
    elif inner == "dockerfiles/base.Dockerfile":
        final = "realm/images/baseline/Dockerfile"
        action = "merge-with-baseline-image"
        group = "realm-baseline-image-candidates"
    elif inner in {"containers/caddy/caddy.yml", "containers/caddy/caddy copy.yml"}:
        final = "realm/services/caddy/compose.yaml"
        action = "merge-variants"
        group = "realm-caddy-compose"
    elif inner in {"containers/redis/redis.Dockerfile", "containers/redis/redis2.Dockerfile"}:
        final = "realm/services/redis/Dockerfile"
        action = "merge-variants"
        group = "realm-redis-image"
    elif "/certs/" in inner:
        final = f"realm/.staging/security-review/{inner}"
        action = "replace-with-generated-fixture"
        group = "realm-apache-development-tls"
        notes += " Do not publish tracked development certificates as runtime identity; replace them with deterministic fixture generation."
    elif inner.startswith("workstation/linux/grub/themes/"):
        action = "quarantine-third-party-assets"
        group = "realm-workstation-grub-theme"
        notes += (
            " Preserve the theme tree intact until upstream license and attribution are recorded."
        )
    elif inner.startswith("workstation/"):
        action = "normalize-workstation-profile"
        group = "realm-workstation-profile"
        notes += " Remove personal paths and convert host mutations into opt-in, idempotent profile modules."
    elif inner.startswith("containers/"):
        action = "normalize-service-module"
        service_parts = inner.split("/")
        service = service_parts[1] if len(service_parts) > 1 else "shared"
        group = f"realm-service-{service}"
        final = f"realm/services/{'/'.join(service_parts[1:])}"
    elif inner.startswith(".devcontainer/features/"):
        final = f"realm/devcontainer-features/{inner.removeprefix('.devcontainer/features/')}"
        group = "realm-devcontainer-features"
    elif inner.startswith(".devcontainer/"):
        final = f"realm/devcontainers/baseline/{inner.removeprefix('.devcontainer/')}"
        group = "realm-devcontainer-baseline"
    elif inner.startswith("realm/"):
        final = f"realm/{inner.removeprefix('realm/')}"
        group = "realm-project-root-candidates"

    return Classification(
        "realm development environment intake",
        "realm",
        f"realm/.staging/{inner}",
        final,
        action,
        group,
        "executable-infrastructure",
        "high",
        notes,
    )


def classify_hygiene(relative: str) -> Classification:
    name = Path(relative).name
    owner = HYGIENE_OWNERS.get(name, "identity")
    if owner in {"external-incompris", "personal-archive"}:
        return Classification(
            "creative architecture references",
            "identity",
            f"identity/.staging/references/external/{owner}/{name}",
            f"identity/references/external/{owner}/{name}",
            "archive-outside-product-assets",
            f"identity-reference-{owner}",
            "passive-binary",
            "high",
            "Reference belongs to a personal or Incompris context; do not publish it as an Ego Hygiene project asset.",
        )
    if owner == "empathy":
        incubation = f"identity/.staging/references/ego-hygiene/{name}"
        final = f".identity/references/ego-hygiene/{name}"
    elif owner == "research":
        incubation = f"research/.staging/assets/therapy/{name}"
        final = f"research/antidote/assets/references/{name}"
    else:
        incubation = f"{owner}/.staging/assets/references/{name}"
        final = f"{owner}/assets/references/{name}"
    return Classification(
        "creative architecture references",
        owner,
        incubation,
        final,
        "visual-review-rename-and-curate",
        f"{owner}-visual-reference-intake",
        "passive-binary",
        "high",
        "Owner was assigned from visual inspection and OCR; rename opaque uploads and retain generation provenance before publication.",
    )


def classify_task(relative: str) -> Classification:
    name = Path(relative).name
    if name in {"agents.yml", "agents copy.yml"}:
        return Classification(
            "agent and Mindcap task candidates",
            "aether",
            f"aether/.staging/tasks/{name}",
            "aether/tasks/agents.yml",
            "split-and-merge-variants",
            "aether-mindcap-agent-tasks",
            "executable-task-configuration",
            "high",
            "Split generic agent diagnostics from Mindcap-specific tasks; keep only thin root aliases.",
        )
    if name == "copilot.yml":
        return Classification(
            "Copilot hook tasks",
            "aether",
            f"aether/.staging/tasks/{name}",
            "aether/tasks/copilot.yml",
            "merge-with-agent-distribution",
            "aether-copilot-tasks",
            "executable-task-configuration",
            "high",
            "Aether owns Copilot hook contracts and generated adapters.",
        )
    if name in {"security.yml", "security copy.yml"}:
        return Classification(
            "security task candidates",
            "egolint",
            f"egolint/.staging/tasks/{name}",
            "egolint/tasks/security.yml",
            "merge-variants",
            "egolint-security-tasks",
            "executable-task-configuration",
            "high",
            "Merge Lynis tasks into Egolint's security policy and remove obsolete paths.",
        )
    if name == "app.yml":
        return Classification(
            "Flutter application task template",
            "holon",
            f"holon/.staging/templates/flutter/tasks/{name}",
            f"holon/templates/flutter/tasks/{name}",
            "parameterize-template",
            "holon-flutter-task-template",
            "executable-task-configuration",
            "high",
            "The tasks hard-code apps/egohygiene and belong to a parameterized Flutter project template.",
        )
    if name == "git.yml":
        return Classification(
            "portable Git tasks",
            "mantle",
            f"mantle/.staging/tasks/{name}",
            f"mantle/tasks/{name}",
            "merge-with-git-tooling",
            "mantle-git-tasks",
            "executable-task-configuration",
            "high",
            "Mantle owns portable local Git helpers; Relay owns only CI automation.",
        )
    return Classification(
        "universal repository tasks",
        "empathy",
        f".staging/tasks/{name}",
        f"tasks/{name}",
        "merge-into-root-task-contract",
        "empathy-root-task-modules",
        "executable-task-configuration",
        "medium",
        "Promote only generic orchestration aliases; an empty task file is a removal candidate after ledger approval.",
    )


def classify(path: str) -> Classification:
    relative = path.removeprefix(".staging/")

    if relative == "tasks-todo.yml":
        return Classification(
            "deferred repository task review queue",
            "empathy",
            ".staging/tasks-todo.yml",
            ".tasks/ or an owning capability profile",
            "review-adapt-or-delete",
            "empathy-deferred-task-review",
            "inert-executable-task-configuration",
            "high",
            "The file is intentionally not imported; each task awaits an explicit owner and capability decision.",
        )

    if relative.startswith(".github/skills/"):
        suffix = relative.removeprefix(".github/skills/")
        return aether_community(path, f"skills/{suffix}", "community agent skills")
    if relative.startswith(".github/agents/awesome/"):
        suffix = relative.removeprefix(".github/agents/awesome/")
        return aether_community(path, f"agents/{suffix}", "community Copilot agents")
    if relative.startswith(".github/instructions/awesome-copilot/"):
        suffix = relative.removeprefix(".github/instructions/awesome-copilot/")
        return aether_community(path, f"instructions/{suffix}", "community Copilot instructions")
    if relative == ".github/copilot-instructions.awesome-copilot.md":
        return aether_community(path, "copilot-instructions.md", "community Copilot review policy")
    if relative == ".github/copilot-instructions.aether.md":
        return Classification(
            "Aether Copilot instruction source",
            "aether",
            "aether/.staging/distributions/copilot/copilot-instructions.md",
            "aether/distributions/copilot/copilot-instructions.md",
            "merge-with-canonical-agent-distribution",
            "aether-copilot-distribution",
            "staged-instruction",
            "high",
            "Treat as a generated adapter candidate and preserve its mapping to canonical Aether source contracts.",
        )
    if relative.startswith(".github/agents/"):
        suffix = relative.removeprefix(".github/agents/")
        return Classification(
            "organization agent sources",
            "aether",
            f"aether/.staging/library/organization/agents/{suffix}",
            f"aether/library/organization/agents/{suffix}",
            "merge-with-canonical-agent-library",
            "aether-organization-agents",
            "staged-instruction",
            "high",
            "Compare with evolved active agent material and preserve provenance before accepting supersession.",
        )
    if relative.startswith(".github/specs/"):
        suffix = relative.removeprefix(".github/specs/")
        return Classification(
            "organization specifications",
            "aether",
            f"aether/.staging/library/organization/specifications/{suffix}",
            f"aether/library/organization/specifications/{suffix}",
            "merge-with-canonical-spec-library",
            "aether-organization-specifications",
            "staged-instruction",
            "high",
            "Treat as source candidates, not active Empathy policy; compare schemas, versions, and provenance first.",
        )
    if relative.startswith(".github/skills2/"):
        suffix = relative.removeprefix(".github/skills2/")
        final_suffix = suffix
        group = "aether-organization-skills"
        if suffix in {"flutter/ai-providers.md", "flutter/offline-first.md"}:
            final_suffix = suffix.removeprefix("flutter/")
            final_suffix = f"flutter-engineering/references/{final_suffix}"
            group = "aether-flutter-skill-reference-merge"
        return Classification(
            "organization skill sources",
            "aether",
            f"aether/.staging/library/organization/skills/{suffix}",
            f"aether/library/organization/skills/{final_suffix}",
            "merge-with-canonical-skill-library",
            group,
            "staged-instruction",
            "high",
            "Normalize naming and compare overlapping Flutter references semantically before promotion.",
        )
    if relative.startswith(".github/workflows/"):
        return classify_workflow(path, relative.removeprefix(".github/workflows/"))
    if relative.startswith(".github/scripts/"):
        return classify_script(relative.removeprefix(".github/"))
    if relative == ".github/aw/actions-lock.json":
        return Classification(
            "GitHub Agentic Workflow lock metadata",
            "relay",
            "relay/.staging/generated/github-agentic/actions-lock.json",
            "relay/generated/github-agentic/actions-lock.json",
            "regenerate-after-source-review",
            "relay-github-agentic-workflow-locks",
            "privileged-automation",
            "high",
            "Generated lock metadata is non-authoritative and must follow reviewed source workflows.",
        )
    if relative == ".github/context7.json":
        return Classification(
            "agent context provider adapter",
            "aether",
            "aether/.staging/integrations/context7.json",
            "aether/integrations/context7.json",
            "validate-and-parameterize",
            "aether-context-providers",
            "staged-configuration",
            "high",
            "Aether owns reusable agent context-provider configuration.",
        )
    if relative.startswith("devenvironment/"):
        return classify_devenvironment(relative)
    if relative.startswith("react-template/universal/"):
        suffix = relative.removeprefix("react-template/universal/")
        return Classification(
            "universal application UI template",
            "holon",
            f"holon/.staging/templates/universal-app/{suffix}",
            f"holon/templates/universal-app/{suffix}",
            "merge-into-application-template",
            "holon-universal-app-ui",
            "executable-application-fixture",
            "high",
            "Keep product code out of Realm; Realm should supply only the development profile and service adapter.",
        )
    if relative.startswith("hygiene/"):
        return classify_hygiene(relative)
    if relative.startswith("templates/paper/"):
        suffix = relative.removeprefix("templates/paper/")
        return Classification(
            "research paper template candidate",
            "beacon",
            f"beacon/.staging/templates/research-paper/{suffix}",
            f"beacon/templates/research-paper/{suffix}",
            "merge-with-existing-template",
            "beacon-research-paper-template",
            "passive-template-source",
            "high",
            "Merge the Markdown/LaTeX skeleton with Beacon's manifest-driven research-paper template.",
        )
    if relative.startswith("templates/changesets/"):
        suffix = relative.removeprefix("templates/changesets/")
        return Classification(
            "repository release template",
            "holon",
            f"holon/.staging/templates/node/changesets/{suffix}",
            f"holon/templates/node/changesets/{suffix}",
            "parameterize-template",
            "holon-changesets-template",
            "passive-template-source",
            "high",
            "Holon owns optional repository scaffolding; Relay owns the release workflow that consumes it.",
        )
    if relative == "templates/community/GOVERNANCE.md":
        return Classification(
            "universal community governance",
            "empathy",
            ".staging/universal/GOVERNANCE.md",
            "GOVERNANCE.md",
            "merge-into-universal-baseline",
            "empathy-universal-community-files",
            "passive-policy-source",
            "high",
            "Empathy can incubate the universal file; the organization .github repository should distribute it later.",
        )
    if relative.startswith(".specify/"):
        suffix = relative.removeprefix(".specify/")
        if suffix == "memory/constitution.md":
            return Classification(
                "Spec Kit project constitution",
                "empathy",
                ".staging/governance/spec-kit-constitution.md",
                "AI_CONSTITUTION.md",
                "merge-governance-source",
                "empathy-ai-constitution",
                "staged-policy-source",
                "high",
                "Reconcile its privacy and provenance clauses with the richer active constitution; do not overwrite it.",
            )
        return Classification(
            "Spec Kit adapter bundle",
            "aether",
            f"aether/.staging/community/spec-kit/{suffix}",
            f"aether/library/community/spec-kit/{suffix}",
            "preserve-and-adapt",
            "aether-spec-kit-adapter",
            "quarantined-executable" if "/scripts/" in relative else "staged-instruction",
            "high",
            "Aether owns reusable specification methodology and generated agent adapters; retain upstream provenance.",
        )
    if relative.startswith(".opencode/commands/"):
        suffix = relative.removeprefix(".opencode/commands/")
        return Classification(
            "OpenCode command distribution",
            "aether",
            f"aether/.staging/distributions/opencode/commands/{suffix}",
            f"aether/distributions/opencode/commands/{suffix}",
            "reverse-map-to-canonical-source",
            "aether-opencode-distribution",
            "staged-instruction",
            "high",
            "Generated adapters are non-authoritative; map each command back to an Aether source contract.",
        )
    if relative.startswith(".opencode/"):
        suffix = relative.removeprefix(".opencode/")
        return Classification(
            "OpenCode workstation presentation",
            "realm",
            f"realm/.staging/workstation/opencode/{suffix}",
            f"realm/workstation/shared/opencode/{suffix}",
            "parameterize-workstation-profile",
            "realm-opencode-workstation-profile",
            "host-runtime-configuration",
            "high",
            "Theme and TUI preferences belong to the opt-in Realm workstation profile, not Aether behavior.",
        )
    if relative.startswith("tasks/"):
        return classify_task(relative)
    if relative.startswith("renderflow/"):
        suffix = relative.removeprefix("renderflow/")
        return Classification(
            "Renderflow branding candidates",
            "renderflow",
            f"renderflow/.staging/assets/branding/{suffix}",
            f"renderflow/assets/branding/{suffix}",
            "visual-review-rename-and-curate",
            "renderflow-branding-assets",
            "passive-binary",
            "high",
            "Choose one canonical badge set and retain generation/source provenance.",
        )
    if relative == "misc/ROADMAP.md":
        return Classification(
            "miscellaneous intake",
            "empathy",
            "tools/ROADMAP.md",
            "tools/ROADMAP.md",
            "delete-exact-duplicate",
            "empathy-tools-roadmap",
            "passive-reference",
            "high",
            "Byte-identical to the active tools/ROADMAP.md.",
        )
    if relative == "misc/fastfetch.jsonc":
        return Classification(
            "portable shell presentation",
            "mantle",
            "mantle/.staging/config/fastfetch.jsonc",
            "mantle/config/fastfetch.jsonc",
            "merge-with-shell-banner",
            "mantle-fastfetch-presentation",
            "host-runtime-configuration",
            "high",
            "Mantle owns portable shell presentation; Realm may install dependencies but must not own behavior.",
        )
    if relative == "misc/future-anime-compiler-architecture-notes.md":
        return Classification(
            "creative pipeline research note",
            "dreamscape",
            "dreamscape/.staging/research/future-anime-compiler-architecture-notes.md",
            "dreamscape/research/future-anime-compiler-architecture-notes.md",
            "preserve-as-research",
            "dreamscape-animation-research",
            "passive-reference",
            "high",
            "Dreamscape owns the creative intent; Aniflow and Renderflow may later implement bounded stages.",
        )
    if relative == "misc/megalinter-remediation-checklist-indented.md":
        return Classification(
            "Egolint remediation notes",
            "egolint",
            "egolint/.staging/audits/megalinter-remediation-checklist-indented.md",
            ".audits/egolint/megalinter-remediation-checklist.md",
            "merge-with-active-audit",
            "egolint-megalinter-remediation-checklist",
            "passive-reference",
            "high",
            "Compare against the active checklist and retain only new findings or rationale.",
        )
    if relative == "misc/terminal-execution-capture.spec.md":
        return Classification(
            "organization specification candidate",
            "aether",
            "aether/.staging/library/organization/specifications/terminal-execution-capture.spec.md",
            "aether/library/organization/specifications/terminal-execution-capture.spec.md",
            "validate-and-promote",
            "aether-terminal-capture-spec",
            "staged-instruction",
            "high",
            "Aether owns the reusable contract; Mantle or Relay may implement consumers.",
        )
    if relative == "misc/universal.png":
        return Classification(
            "universal application branding",
            "holon",
            "holon/.staging/templates/universal-app/apps/ui/public/universal.png",
            "holon/templates/universal-app/apps/ui/public/universal.png",
            "delete-exact-duplicate-after-move",
            "holon-universal-app-ui",
            "passive-binary",
            "high",
            "Byte-identical to the copy already inside the staged React template.",
        )
    if relative == "awesome-obsidian.md":
        return Classification(
            "Obsidian source references",
            "mindgarden",
            "mindgarden/.staging/sources/awesome-obsidian.md",
            "mindgarden/sources/awesome-obsidian.md",
            "merge-with-provenance-catalog",
            "mindgarden-obsidian-reference-sources",
            "passive-reference",
            "high",
            "Retain upstream links and license/attribution data for vendored Obsidian assets.",
        )
    if relative == "mkdocs.yml":
        return Classification(
            "alternative knowledge-site projection",
            "mindgarden",
            "mindgarden/.staging/profiles/mkdocs/mkdocs.yml",
            "mindgarden/profiles/mkdocs/mkdocs.yml",
            "parameterize-publishing-profile",
            "mindgarden-mkdocs-profile",
            "executable-site-configuration",
            "high",
            "The Sanctuary identity is stale; parameterize repository metadata and keep Quartz as the current Empathy projection.",
        )
    if relative == "repository-open-graph-template.png":
        return Classification(
            "identity generation reference",
            "identity",
            "identity/.staging/references/github/repository-open-graph-template.png",
            "identity/references/github/repository-open-graph-template.png",
            "preserve-as-reference",
            "identity-github-social-preview",
            "passive-binary",
            "high",
            "Reference template informs the GitHub social-preview output profile; it is not a generated project asset.",
        )
    if relative == "vite.corpus.txt":
        return Classification(
            "Vite configuration corpus",
            "holon",
            "holon/.staging/corpora/vite-configs.txt",
            "holon/references/corpora/vite-configs.txt",
            "preserve-as-reference-corpus",
            "holon-vite-template-research",
            "passive-reference",
            "high",
            "Use as design evidence for a parameterized web template; do not execute or copy configurations wholesale.",
        )
    if relative == ".pre-commit-config.yaml":
        return Classification(
            "pre-commit policy candidates",
            "egolint",
            "egolint/.staging/config/pre-commit-config.yaml",
            "egolint/.pre-commit-config.yaml",
            "split-and-merge-invalid-concatenation",
            "egolint-pre-commit-policy",
            "executable-hook-configuration",
            "high",
            "The file concatenates multiple repository configs and duplicate YAML documents; mine policy, do not promote directly.",
        )
    if relative == ".husky/commit-msg":
        return Classification(
            "Git hook candidate",
            "egolint",
            "egolint/.staging/.husky/commit-msg",
            "egolint/.husky/commit-msg",
            "compare-and-discard-disabled-hook",
            "egolint-husky-hooks",
            "executable-hook",
            "high",
            "The only command is commented out and the active Egolint hook contract is already authoritative.",
        )

    return Classification(
        "unclassified staging intake",
        "manual-review",
        f".staging/unclassified/{relative}",
        "TBD",
        "manual-classification-required",
        "unclassified",
        "unknown",
        "low",
        "No ownership rule matched this path; do not move or activate it.",
    )


def text_flags(path: Path, mode: str) -> list[str]:
    flags: list[str] = []
    if mode == "100755":
        flags.append("executable")
    lowered = str(path).lower()
    if any(
        token in lowered
        for token in (" copy", "devcontainer2", "compose2", "redis2", ".old", "/todo")
    ):
        flags.append("variant")
    if path.suffix.lower() in {".env", ".pem", ".crt", ".key"} or "/certs/" in lowered:
        flags.append("sensitive-configuration")
    try:
        raw = path.read_bytes()
    except OSError:
        return flags
    if b"\0" in raw[:8192]:
        return flags
    content = raw.decode("utf-8", errors="ignore")
    patterns = (
        (r"StrictHostKeyChecking=no", "ssh-host-verification-disabled"),
        (r"(?:privileged:\s*true|\"privileged\"\s*:\s*true)", "privileged-runtime"),
        (r"NOPASSWD", "passwordless-sudo"),
        (
            r"(?i)(?:adminpassword|miniosecret|mysecret|changeme|Root123!)",
            "development-credentials",
        ),
        (
            r"(?i)(?:override directive|show your thinking|absolute transparency|ignore (?:all |any )?(?:previous|prior))",
            "prompt-override-content",
        ),
    )
    for pattern, flag in patterns:
        if re.search(pattern, content):
            flags.append(flag)
    return flags


def preferred_duplicate(paths: list[str]) -> str:
    def score(path: str) -> tuple[int, int, int, str]:
        staged = int(path.startswith(".staging/"))
        opaque = int("file_000000" in path or "/markup_" in path)
        variant = int(bool(re.search(r"(?: copy|2\.|\.old$)", path)))
        return staged, opaque + variant, len(path), path

    return min(paths, key=score)


def duplicate_policy(path: str, blob: str, duplicate_of: str) -> tuple[str, str]:
    if not duplicate_of or blob == EMPTY_BLOB:
        return "", ""
    if path.startswith(".staging/.github/skills/"):
        return (
            "preserve-package-local-copy",
            "Package-local references and licenses remain self-contained.",
        )
    if "/workstation/linux/grub/themes/" in path:
        return "preserve-layout-copy", "Theme filenames encode layout roles even when pixels match."
    if "/__init__.py" in path or "/__init__.pyi" in path:
        return "preserve-package-initializer", "Package initializers are structurally significant."
    if path.startswith(".staging/hygiene/"):
        return (
            "deduplicate-after-visual-classification",
            "Retain one named/provenanced visual after owner review.",
        )
    if path in {".staging/misc/ROADMAP.md", ".staging/misc/universal.png"}:
        return "delete-exact-duplicate-after-approval", "A retained canonical copy already exists."
    if " copy" in path:
        return "merge-or-delete-variant", "Compare references, then retain the canonical filename."
    return (
        "review-exact-duplicate",
        "Exact content match detected; structural context decides whether removal is safe.",
    )


def build_rows(repository_root: Path) -> list[LedgerRow]:
    entries = tracked_entries(repository_root)
    paths_by_blob: dict[str, list[str]] = {}
    for path, _mode, blob in entries:
        paths_by_blob.setdefault(blob, []).append(path)

    canonical_by_blob = {
        blob: preferred_duplicate(paths)
        for blob, paths in paths_by_blob.items()
        if len(paths) > 1 and blob != EMPTY_BLOB
    }

    rows: list[LedgerRow] = []
    for path, mode, blob in entries:
        if not path.startswith(".staging/"):
            continue
        absolute = repository_root / path
        size = absolute.stat().st_size
        classification = classify(path)
        canonical = canonical_by_blob.get(blob, "")
        duplicate_of = canonical if canonical and canonical != path else ""
        duplicate_action, duplicate_note = duplicate_policy(path, blob, duplicate_of)
        flags = text_flags(absolute, mode)
        notes = classification.notes
        if duplicate_note:
            notes = f"{notes} {duplicate_note}"
        rows.append(
            LedgerRow(
                source_path=path,
                bytes=size,
                git_mode=mode,
                git_blob=blob,
                kind=file_kind(path, size),
                collection=classification.collection,
                canonical_owner=classification.canonical_owner,
                incubation_home=classification.incubation_home,
                canonical_home=classification.canonical_home,
                disposition=classification.disposition,
                merge_group=classification.merge_group,
                trust_class=classification.trust_class,
                confidence=classification.confidence,
                duplicate_of=duplicate_of,
                duplicate_action=duplicate_action,
                flags=";".join(sorted(set(flags))),
                notes=notes,
            )
        )
    return sorted(rows, key=lambda row: row.source_path)


def render_csv(rows: list[LedgerRow]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=CSV_FIELDS,
        extrasaction="ignore",
        lineterminator="\n",
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(asdict(row))
    return stream.getvalue()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".audits/data/2026-08-15-staging-file-disposition.csv"),
    )
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    repository_root = arguments.repository_root.resolve()
    output = arguments.output
    if not output.is_absolute():
        output = repository_root / output
    rendered = render_csv(build_rows(repository_root))

    if arguments.check:
        if not output.exists():
            print(f"Missing generated ledger: {output}", file=sys.stderr)
            return 1
        if output.read_text(encoding="utf-8") != rendered:
            print(f"Generated ledger is stale: {output}", file=sys.stderr)
            return 1
        print(f"Staging ledger is current: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {len(rendered.splitlines()) - 1} staging dispositions to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
