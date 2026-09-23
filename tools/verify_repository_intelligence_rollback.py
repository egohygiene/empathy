#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify Empathy's fixed pre-upgrade publication without rewriting Quartz."""

from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess  # nosec B404
import sys
from typing import Any
from xml.etree import ElementTree as ET

REPOSITORY = "egohygiene/empathy"
SOURCE_COMMIT = "254185272ab27b6858b8b0393af6549c205c9a8d"
SOURCE_TREE = "a5cdaba679c8c0b9d677730273c9779569649929"
RELAY_COMMIT = "b71b090406a3a9e4cd9f107e9d14a623bbecb127"
QUARTZ_COMMIT = "075afd3f712da0088a07f5284a7b3aba37dd61b6"
ORIGINAL_SITE_DIGEST = "sha256:1e92a0a74c154bbc3c339a6ef1764852bfcceba1a58b294e238b4a0331f94498"
MAX_BYTES = 64 * 1024 * 1024
MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_FILES = 128
MAX_REPORT_BYTES = 8192
FEEDS = frozenset({"index.xml", "sitemap.xml"})
TAG_PREFIX = "https://egohygiene.github.io/empathy/tags/"


@dataclass(frozen=True)
class Baseline:
    """Reviewed inventory digests; no command-line override is supported."""

    paths: str
    intelligence: str
    stable_quartz: str
    rss: str
    sitemap: str


# Derived from run 35840040112's retained Pages archive, independently checked
# against a same-source, same-pin replay in a checkout named `empathy`, TZ=UTC.
# Inventories use sorted Path objects (component ordering), not string sorting.
BASELINE = Baseline(
    paths="sha256:ab0321da0c6859c55aff7f2b0b348982d5a80e859125e15a33a872267283ff2c",
    intelligence="sha256:c25caf4249cb4de83e5a747b02db4fa080df93385a0d7344899a5361831e7db9",
    stable_quartz="sha256:605507bc7780341bb519a0b9ff09e4dac9632214abf4407b95faf38ec9bbd6df",
    rss="sha256:770f1adfcbec0ea02ebe996db56c77ce26e49c9682f9f828228267157a9b7bf0",
    sitemap="sha256:9b12dc82e5429d3ff2b7b6b3d00b8b2858cede1acb781c703ab0729c43e93890",
)


class RollbackError(ValueError):
    """A bounded diagnostic code that never includes source data or paths."""


def digest_bytes(data: bytes) -> str:
    """Return a namespaced SHA-256 digest."""
    return "sha256:" + hashlib.sha256(data).hexdigest()


def inventory_digest(records: list[dict[str, Any]]) -> str:
    """Use the reviewed Relay deployment inventory serialization."""
    canonical = json.dumps(records, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    return digest_bytes((canonical + "\n").encode("utf8"))


def inventory(root: Path) -> list[dict[str, Any]]:
    """Reject links and special files, then inventory bounded public bytes."""
    if root.is_symlink() or not root.is_dir():
        raise RollbackError("ERB-001")
    records: list[dict[str, Any]] = []
    total = 0
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise RollbackError("ERB-001")
        if path.is_dir():
            continue
        if not path.is_file():
            raise RollbackError("ERB-001")
        relative = path.relative_to(root).as_posix()
        if not re.fullmatch(r"[A-Za-z0-9._/-]+", relative):
            raise RollbackError("ERB-001")
        total += path.stat().st_size
        if total > MAX_BYTES or len(records) >= MAX_FILES:
            raise RollbackError("ERB-002")
        data = path.read_bytes()
        records.append({"path": relative, "bytes": len(data), "sha256": digest_bytes(data)})
    if not records:
        raise RollbackError("ERB-001")
    return records


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys without echoing their names."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RollbackError("ERB-003")
        result[key] = value
    return result


def reject_constant(_value: str) -> None:
    """Reject JSON extensions such as NaN and Infinity."""
    raise RollbackError("ERB-003")


def read_json(path: Path) -> Any:
    """Read bounded strict JSON with public-safe errors."""
    if path.stat().st_size > MAX_JSON_BYTES:
        raise RollbackError("ERB-002")
    try:
        return json.loads(
            path.read_text(encoding="utf8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise RollbackError("ERB-003") from error


def verify_provenance(value: Any) -> None:
    """Require the actual old public provenance, never a new manifest claim."""
    if not isinstance(value, dict):
        raise RollbackError("ERB-004")
    expected = {
        "consumer": {
            "repository": REPOSITORY,
            "source_commit": SOURCE_COMMIT,
            "visibility": "public",
        },
        "generator": {
            "immutable": True,
            "name": "egohygiene/relay/actions/repository-intelligence",
            "repository": "egohygiene/relay",
            "source_commit": RELAY_COMMIT,
            "source_ref": RELAY_COMMIT,
            "version": "1.4.0",
        },
        "projection": {
            "classification": "public-safe",
            "deployment_authority": "consumer",
            "route": "/intelligence/",
        },
        "schema": "egohygiene.relay.repository-intelligence-provenance/v1",
        "schema_version": 1,
        "generated_at": "2026-09-23T08:56:50Z",
        "timestamp_source": "consumer-source-commit",
    }
    if any(value.get(key) != expected_value for key, expected_value in expected.items()):
        raise RollbackError("ERB-004")


def normalized_feed_digest(path: Path) -> str:
    """Ignore only synthetic tag dates; pin all other historical feed content."""
    data = path.read_bytes()
    if len(data) > MAX_JSON_BYTES:
        raise RollbackError("ERB-005")
    try:
        text = data.decode("utf-8")
    except UnicodeError as error:
        raise RollbackError("ERB-005") from error
    # Only the retained UTF-8 feeds are supported. NUL rejection also closes the
    # UTF-16/32 encoding bypass of a byte-only declaration check.
    without_empty_cdata = text.replace("<![CDATA[  ]]>", "")
    if "\x00" in text or "<!" in without_empty_cdata:
        raise RollbackError("ERB-005")
    try:
        # Bounded UTF-8 text above rejects all DTD/entity declarations; the only
        # accepted declaration-like content is the retained empty CDATA marker.
        document = ET.fromstring(text)  # noqa: S314  # nosec B314
        entries = (
            list(document) if path.name == "sitemap.xml" else document.findall("./channel/item")
        )
        for entry in entries:
            is_sitemap = path.name == "sitemap.xml"
            link = entry.findtext("{*}loc" if is_sitemap else "link", "")
            if not link.startswith(TAG_PREFIX):
                continue
            date = entry.find("{*}lastmod" if is_sitemap else "pubDate")
            if date is None or date.text is None:
                raise RollbackError("ERB-005")
            if is_sitemap:
                if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z", date.text):
                    raise RollbackError("ERB-005")
                instant = datetime.fromisoformat(date.text)
            else:
                instant = parsedate_to_datetime(date.text)
            if instant.tzinfo is None or instant.utcoffset() != UTC.utcoffset(instant):
                raise RollbackError("ERB-005")
            date.text = "RUNTIME_DATE"
        return digest_bytes(ET.tostring(document, encoding="utf-8"))
    except (ET.ParseError, ValueError, TypeError, OverflowError) as error:
        raise RollbackError("ERB-005") from error


def verify_source(repository_root: Path) -> None:
    """Check the exact immutable consumer revision and tree when requested."""
    for reference, expected in (("HEAD", SOURCE_COMMIT), ("HEAD^{tree}", SOURCE_TREE)):
        # Trusted runner Git and fixed HEAD/tree references; never a shell.
        result = subprocess.run(  # noqa: S603  # nosec B603
            ["git", "-C", str(repository_root), "rev-parse", "--verify", reference],  # noqa: S607
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or result.stdout.strip() != expected:
            raise RollbackError("ERB-006")


def verify_site(
    site_root: Path,
    repository_root: Path | None = None,
    *,
    baseline: Baseline = BASELINE,
) -> dict[str, Any]:
    """Verify fixed historical payloads and report the actual new composition."""
    records = inventory(site_root)
    for record in records:
        if record["path"].endswith(".json"):
            read_json(site_root / record["path"])
    provenance_path = site_root / "intelligence" / "provenance.json"
    if not provenance_path.is_file():
        raise RollbackError("ERB-004")
    verify_provenance(read_json(provenance_path))
    if inventory_digest([{"path": record["path"]} for record in records]) != baseline.paths:
        raise RollbackError("ERB-007")
    intelligence = inventory_digest(inventory(site_root / "intelligence"))
    stable_quartz = inventory_digest(
        [
            record
            for record in records
            if not record["path"].startswith("intelligence/") and record["path"] not in FEEDS
        ]
    )
    if intelligence != baseline.intelligence or stable_quartz != baseline.stable_quartz:
        raise RollbackError("ERB-008")
    if (
        normalized_feed_digest(site_root / "index.xml") != baseline.rss
        or normalized_feed_digest(site_root / "sitemap.xml") != baseline.sitemap
    ):
        raise RollbackError("ERB-005")
    if repository_root is not None:
        verify_source(repository_root)
    return {
        "schema": "egohygiene.empathy.repository-intelligence-rollback/v1",
        "status": "verified",
        "mode": "rollback-v1.4",
        "consumer": {
            "repository": REPOSITORY,
            "source_commit": SOURCE_COMMIT,
            "source_tree": SOURCE_TREE,
        },
        "generator": {"source_commit": RELAY_COMMIT, "version": "1.4.0"},
        "quartz_commit": QUARTZ_COMMIT,
        "known_good": {
            "run_id": 35840040112,
            "run_attempt": 1,
            "run_url": "https://github.com/egohygiene/empathy/actions/runs/35840040112",
            "pages_artifact_id": 10741177073,
            "pages_artifact_url": "https://github.com/egohygiene/empathy/actions/runs/35840040112/artifacts/10741177073",
            "pages_archive_digest": "sha256:3175c601487b61ecf4e87fc820a33ce8d3a137fa34bf21b2256d9868aa04257b",
            "original_composed_digest": ORIGINAL_SITE_DIGEST,
        },
        "verification": {
            "source_checkout_checked": repository_root is not None,
            "intelligence_digest": intelligence,
            "stable_quartz_digest": stable_quartz,
            "composed_digest": inventory_digest(records),
            "files": len(records),
            "bytes": sum(record["bytes"] for record in records),
            "full_site_equality_claimed": False,
            "runtime_variance": "The two feeds match retained normalized XML with synthetic tag dates ignored; the other 79 files and all public paths match the retained deployment exactly.",
        },
    }


def write_report(site_root: Path, output: Path, repository_root: Path | None) -> None:
    """Validate output isolation and write the bounded rollback evidence."""
    if output.is_symlink() or any(parent.is_symlink() for parent in output.parents):
        raise RollbackError("ERB-009")
    if output.resolve().is_relative_to(site_root.resolve()):
        raise RollbackError("ERB-009")
    report = verify_site(site_root, repository_root)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if len(text.encode("utf8")) > MAX_REPORT_BYTES:
        raise RollbackError("ERB-002")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf8")


def main(argv: list[str] | None = None) -> int:
    """Write a bounded private evidence report or a sanitized diagnostic."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repository-root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        write_report(arguments.site_root, arguments.output, arguments.repository_root)
    except RollbackError as error:
        # RollbackError contains only a fixed ERB code, never source values.
        print(f"Rollback verification failed: {error}", file=sys.stderr)  # noqa: T201
        return 1
    except (OSError, UnicodeError, RecursionError):
        # Fixed command-line diagnostic, including for lower-level failures.
        print("Rollback verification failed: ERB-010", file=sys.stderr)  # noqa: T201
        return 1
    # Intentional command-line success status.
    print("Verified Empathy rollback publication")  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
