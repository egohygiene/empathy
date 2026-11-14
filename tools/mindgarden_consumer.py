#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Build a disposable golden knowledge corpus through the installed pinned owner."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from contextlib import redirect_stdout
import hashlib
import importlib
import importlib.metadata
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
from tempfile import TemporaryDirectory
from typing import Any

MAX_FILE_BYTES = 1024 * 1024
MAX_OUTPUT_FILES = 1000


def load(path: Path) -> dict[str, Any]:
    """Load a consumer-owned object without running imported source."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        message = "Consumer input must be a JSON object"
        raise TypeError(message)
    return value


def engine(root: Path) -> Any:
    """Reject local incubation, a mutable checkout or a different installed source."""
    requirements = (root / "requirements/mindgarden-standalone.txt").read_text().splitlines()
    selected = [line for line in requirements if line.startswith("mindgarden @ git+")]
    if len(selected) != 1:
        message = "Select exactly one immutable standalone Mindgarden source"
        raise ValueError(message)
    url, pin = selected[0].split(" @ git+", 1)[1].rsplit("@", 1)
    distribution = importlib.metadata.distribution("mindgarden")
    direct = json.loads(distribution.read_text("direct_url.json") or "{}")
    owner = importlib.import_module("mindgarden")
    owner_file = owner.__file__
    if (
        not re.fullmatch(r"[0-9a-f]{40}", pin)
        or direct.get("url") != url
        or direct.get("vcs_info", {}).get("vcs") != "git"
        or direct.get("vcs_info", {}).get("commit_id") != pin
        or not isinstance(owner_file, str)
        or not Path(owner_file).resolve().is_relative_to(Path(sys.prefix).resolve())
    ):
        message = "Run with the isolated immutable standalone Mindgarden installation"
        raise ValueError(message)
    return owner


def source_bytes(root: Path, row: dict[str, Any]) -> bytes:
    """Read only the explicit public manifest, rejecting path and source drift."""
    relative = PurePosixPath(row["path"])
    if relative.is_absolute() or ".." in relative.parts or ".garden.local" in relative.parts:
        message = "Corpus paths must be explicit repository-relative public inputs"
        raise ValueError(message)
    target = root / relative
    if any(path.is_symlink() for path in (target, *target.parents)):
        message = "Corpus input must not follow a symlink"
        raise ValueError(message)
    with target.open("rb") as stream:
        raw = stream.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES or hashlib.sha256(raw).hexdigest() != row["sha256"]:
        message = "Corpus input digest or size mismatch; review the source manifest"
        raise ValueError(message)
    return raw


def build(root: Path, output: Path, exchange: str | None = None) -> dict[str, Any]:
    """Delegate normalization/index/privacy gates; never mutate canonical knowledge."""
    if output.is_relative_to(root) and not output.is_relative_to(root / ".cache"):
        message = "Repository corpus outputs belong under ignored .cache, never canonical knowledge"
        raise ValueError(message)
    owner = engine(root)
    agent = importlib.import_module("mindgarden.application.agent")
    publishing = importlib.import_module("mindgarden.adapters.publishing")
    manifest = load(root / "integrations/mindgarden/corpus.json")
    if manifest["schema"] != "empathy.mindgarden-corpus/v1":
        message = "Unsupported corpus contract"
        raise ValueError(message)
    # Validate every byte before creating the new destination; source never comes from untracked files.
    rows = [*manifest["support_files"], *manifest["sources"]]
    payloads = {row["path"]: source_bytes(root, row) for row in rows}
    if output.exists() or output.is_symlink():
        message = "Corpus destination must be new; retain or review prior outputs explicitly"
        raise ValueError(message)
    output.mkdir(parents=False)
    stage = output / "repository"
    for relative, raw in payloads.items():
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    captured = []
    for row in manifest["sources"]:
        identifier = "capture-" + row["artifact_id"]
        arguments = Namespace(
            repository_root=stage,
            input=stage / row["path"],
            source_id=identifier,
            title="Source: " + row["artifact_id"],
            origin="https://github.com/egohygiene/empathy/blob/"
            + manifest["source_revision"]
            + "/"
            + row["path"],
            captured=manifest["captured"],
            owner="egohygiene",
            rights="Existing tracked first-party source; repository MIT license; source status retained.",
            media_type="text/markdown",
            related=[],
            tag=["architecture-source"],
            write=True,
            confirm_public=True,
        )
        with redirect_stdout(io.StringIO()):
            agent.run_ingest(arguments)
        captured.append(
            {
                "artifact_id": row["artifact_id"],
                "source_sha256": row["sha256"],
                "declared_status": row["declared_status"],
                "capture_id": identifier,
            }
        )
    index = agent.build_index(stage)
    for note in index["notes"]:
        if note["id"].startswith("capture-") and (note["reviewed"] or note["status"] != "proposed"):
            message = "Captured architecture must remain explicitly unreviewed"
            raise ValueError(message)
    (output / "index.json").write_text(agent.canonical_json(index), encoding="utf-8")
    public = output / "public"
    paths = publishing.project_garden(
        stage, public, Path("mindgarden/profiles/quartz/profile.yaml")
    )
    count = publishing.verify_projection(stage, Path("mindgarden/profiles/quartz/profile.yaml"))
    if exchange:
        destination = output / exchange
        shutil.copytree(public, destination)
        # A prototype file round trip is owner-normalized as new unreviewed evidence, never a canonical overwrite.
        with redirect_stdout(io.StringIO()):
            agent.run_ingest(
                Namespace(
                    repository_root=stage,
                    input=destination / "index.md",
                    source_id="exchange-" + exchange,
                    title="Prototype " + exchange + " Markdown exchange",
                    origin="urn:empathy:prototype:" + exchange,
                    captured=manifest["captured"],
                    owner="egohygiene",
                    rights="Reviewed public projection; prototype re-import.",
                    media_type="text/markdown",
                    related=[],
                    tag=["exchange-prototype"],
                    write=True,
                    confirm_public=True,
                )
            )
        owner.validate_repository(stage)
        imported = next(
            note
            for note in agent.build_index(stage)["notes"]
            if note["id"] == "exchange-" + exchange
        )
        if imported["reviewed"] or imported["status"] != "proposed":
            message = "Prototype imports must remain proposed and unreviewed"
            raise ValueError(message)
    if any(source_bytes(root, row) != payloads[row["path"]] for row in rows):
        message = "Canonical source changed during the disposable operation"
        raise ValueError(message)
    report = {
        "schema": "empathy.mindgarden-corpus-result/v1",
        "source_revision": manifest["source_revision"],
        "source_count": len(captured),
        "indexed_notes": len(index["notes"]),
        "captured": captured,
        "public_notes": count,
        "public_files": [path.as_posix() for path in paths],
        "engine": importlib.metadata.distribution("mindgarden").version,
        "exchange_prototype": exchange,
        "exchange_host_acceptance": "not-exercised" if exchange else None,
        "canonical_source_mutation": False,
        "canonical_input_hashes_unchanged": True,
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def inventory(root: Path) -> dict[str, str]:
    """Compare only bounded regular generated files; a check never repairs output."""
    result: dict[str, str] = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            message = "Corpus output must not contain symlinks"
            raise ValueError(message)
        if path.is_file():
            if len(result) >= MAX_OUTPUT_FILES or path.stat().st_size > 2 * MAX_FILE_BYTES:
                message = "Corpus output exceeds the bounded golden comparison"
                raise ValueError(message)
            result[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def check(root: Path, output: Path, exchange: str | None) -> dict[str, Any]:
    """Reproduce declared inputs without rewriting an existing result."""
    with TemporaryDirectory(prefix="empathy-corpus-check-") as temporary:
        generated = Path(temporary) / "result"
        report = build(root, generated, exchange)
        if inventory(generated) != inventory(output):
            message = (
                "Corpus output is missing or stale; review a fresh output instead of repairing it"
            )
            raise ValueError(message)
    return report


def main() -> int:
    """Run only an explicit isolated consumer operation."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--exchange", choices=["openwiki", "obsidian"])
    parser.add_argument(
        "--check", action="store_true", help="Reproduce into scratch and compare existing output"
    )
    args = parser.parse_args()
    try:
        report = (
            check(args.repository_root.resolve(), args.output.resolve(), args.exchange)
            if args.check
            else build(args.repository_root.resolve(), args.output.resolve(), args.exchange)
        )
    except (OSError, TypeError, ValueError, importlib.metadata.PackageNotFoundError) as error:
        sys.stderr.write(f"Mindgarden consumer unavailable: {error}\n")
        return 2
    sys.stdout.write(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
