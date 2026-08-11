from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

REMOTE_USE_PATTERN = re.compile(
    r'^\s*(?:-\s*)?uses:\s*["\']?(?P<target>[^\s#"\']+)',
    re.MULTILINE,
)
FULL_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DOCKER_DIGEST_PATTERN = re.compile(r"^docker://[^@\s]+@sha256:[0-9a-f]{64}$")
TOP_LEVEL_PERMISSIONS_PATTERN = re.compile(r"^permissions:(?:\s|$)", re.MULTILINE)
DOCUMENT_MARKER_PATTERN = re.compile(r"^---\s*$", re.MULTILINE)
JOB_PATTERN = re.compile(r"^  (?P<name>[A-Za-z0-9_-]+):\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str
    line: int | None = None

    def render(self, repository_root: Path) -> str:
        relative_path = self.path.relative_to(repository_root).as_posix()
        location = f"{relative_path}:{self.line}" if self.line else relative_path
        return f"{location}: {self.message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enforce repository-local GitHub automation policy."
    )
    parser.add_argument("--repository-root", required=True)
    return parser.parse_args()


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_remote_uses(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in REMOTE_USE_PATTERN.finditer(text):
        target = match.group("target")
        if target.startswith("./"):
            continue
        if target.startswith("docker://"):
            if not DOCKER_DIGEST_PATTERN.fullmatch(target):
                findings.append(
                    Finding(
                        path,
                        f"container action must use a SHA-256 image digest: {target}",
                        line_number(text, match.start()),
                    )
                )
            continue
        if "@" not in target:
            findings.append(
                Finding(
                    path,
                    f"external action or workflow is missing a ref: {target}",
                    line_number(text, match.start()),
                )
            )
            continue
        reference = target.rsplit("@", maxsplit=1)[1]
        if not FULL_COMMIT_PATTERN.fullmatch(reference):
            findings.append(
                Finding(
                    path,
                    f"external action or workflow must use a full commit SHA: {target}",
                    line_number(text, match.start()),
                )
            )
    return findings


def check_workflow(path: Path, repository_root: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings = check_remote_uses(path, text)

    if " " in path.name:
        findings.append(Finding(path, "workflow filenames must not contain spaces"))
    if not TOP_LEVEL_PERMISSIONS_PATTERN.search(text):
        findings.append(Finding(path, "workflow must declare top-level permissions"))
    if re.search(
        r"^\s*permissions:\s*[\"']?write-all[\"']?\s*(?:#.*)?$",
        text,
        re.MULTILINE,
    ):
        findings.append(Finding(path, "permissions: write-all is forbidden"))
    if re.search(r"^\s*pull_request_target:\s*$", text, re.MULTILINE):
        findings.append(Finding(path, "pull_request_target requires an explicit security review"))

    document_markers = list(DOCUMENT_MARKER_PATTERN.finditer(text))
    if len(document_markers) > 1:
        findings.append(
            Finding(
                path,
                "workflow must contain exactly one YAML document",
                line_number(text, document_markers[1].start()),
            )
        )

    jobs_section = re.search(r"^jobs:\s*$", text, re.MULTILINE)
    if jobs_section is None:
        findings.append(Finding(path, "workflow must declare jobs"))
        return findings

    jobs_offset = jobs_section.end()
    jobs_text = text[jobs_offset:]
    job_matches = list(JOB_PATTERN.finditer(jobs_text))
    for index, match in enumerate(job_matches):
        segment_end = (
            job_matches[index + 1].start() if index + 1 < len(job_matches) else len(jobs_text)
        )
        segment = jobs_text[match.start() : segment_end]
        if re.search(r"^    uses:", segment, re.MULTILINE):
            continue
        if not re.search(r"^    timeout-minutes:\s*[0-9]+\s*$", segment, re.MULTILINE):
            findings.append(
                Finding(
                    path,
                    f"job '{match.group('name')}' must declare timeout-minutes",
                    line_number(text, jobs_offset + match.start()),
                )
            )

    return findings


def check_action(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings = check_remote_uses(path, text)
    for required_key in ("name:", "description:", "runs:"):
        if not re.search(rf"^{re.escape(required_key)}", text, re.MULTILINE):
            findings.append(Finding(path, f"action metadata is missing {required_key[:-1]}"))
    return findings


def validate(repository_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    workflow_root = repository_root / ".github" / "workflows"
    action_root = repository_root / ".github" / "actions"

    workflow_paths = sorted(
        path for path in workflow_root.iterdir() if path.suffix in {".yaml", ".yml"}
    )
    for path in workflow_paths:
        findings.extend(check_workflow(path, repository_root))
    for path in sorted(action_root.glob("*/action.yml")):
        findings.extend(check_action(path))
    return findings


def main() -> int:
    args = parse_args()
    repository_root = Path(args.repository_root).resolve()
    if not repository_root.is_dir():
        print(f"Repository root is not a directory: {repository_root}", file=sys.stderr)
        return 2

    findings = validate(repository_root)
    for finding in findings:
        print(finding.render(repository_root), file=sys.stderr)
    if findings:
        print(f"Automation policy failed with {len(findings)} finding(s).", file=sys.stderr)
        return 1

    workflow_count = sum(
        path.suffix in {".yaml", ".yml"}
        for path in (repository_root / ".github/workflows").iterdir()
    )
    action_count = len(list((repository_root / ".github/actions").glob("*/action.yml")))
    print(f"Automation policy passed: {workflow_count} workflow(s), {action_count} action(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
