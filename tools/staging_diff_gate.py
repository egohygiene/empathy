#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Check immutable staging preimages and durable receipt claims; never remove source."""

from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil

# Fixed local Git argv only; no shell or supplied executable.
import subprocess  # nosec B404
import sys
import tempfile
from typing import Any, Never
from urllib.parse import urlsplit

RECEIPTS = "migration/staging-removal-receipts.json"
LEGACY = "migration/staging-removal-approvals.json"
LEDGER = ".audits/data/2026-08-15-staging-file-disposition.csv"
SHA = re.compile(r"[0-9a-f]{40}")
MAXIMUM = 64 * 1024 * 1024
SCHEMA = "egohygiene.empathy.staging-removal-receipts/v1"
CONTROL_LIMIT = 32
SURROGATE_START = 0xD800
SURROGATE_END = 0xDFFF
HOSTNAME_LIMIT = 253
RECEIPT_LIMIT = 10_000
MINIMUM_LEGACY_REVISION = 7


def deny(message: str) -> Never:
    raise ValueError(message)


def require(value: object, message: str) -> None:
    if not value:
        deny(message)


def git(root: Path, *arguments: str, maximum: int = MAXIMUM) -> bytes:
    environment = {
        "PATH": os.defpath,
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    # Fixed object/index operations only. No checkout, filters, hooks or provider.
    executable = shutil.which("git", path=os.defpath)
    require(executable is not None, "Git evidence unavailable")
    command = [
        str(executable),
        "--no-lazy-fetch",
        "--no-optional-locks",
        "--literal-pathspecs",
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "log.showSignature=false",
        "-c",
        "protocol.allow=never",
        "-C",
        str(root),
        *arguments,
    ]
    with tempfile.TemporaryFile() as output:
        completed = subprocess.run(  # noqa: S603  # nosec B603
            command,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=subprocess.DEVNULL,
            timeout=60,
            check=False,
        )
        require(completed.returncode == 0 and output.tell() <= maximum, "Git evidence unavailable")
        output.seek(0)
        return output.read(maximum + 1)


def document(raw: bytes) -> dict[str, Any]:
    require(len(raw) <= MAXIMUM, "JSON input exceeds bound")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result

    def invalid(_: str) -> None:
        deny("Non-finite JSON number")

    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    require(isinstance(value, dict), "JSON object required")
    return dict(value)


def closed(value: Any, fields: set[str]) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == fields, "Unsupported receipt shape")
    return dict(value)


def text(value: Any, maximum: int = 2048) -> str:
    require(isinstance(value, str) and 0 < len(value) <= maximum, "Receipt text required")
    result = str(value)
    require(
        not any(
            ord(c) < CONTROL_LIMIT or SURROGATE_START <= ord(c) <= SURROGATE_END for c in result
        ),
        "Invalid receipt text",
    )
    return result


def path(value: Any, *, staged: bool = False) -> str:
    result = text(value, 1024)
    require(
        not result.startswith("/")
        and "\\" not in result
        and PurePosixPath(result).as_posix() == result
        and all(part not in {"", ".", "..", ".git"} for part in result.split("/"))
        and (not staged or result.startswith(".staging/")),
        "Invalid source path",
    )
    return result


def revision(value: Any) -> str:
    result = text(value, 40)
    require(SHA.fullmatch(result), "Full Git object identity required")
    return result


def url(value: Any) -> str:
    result = text(value)
    require(not any(c.isspace() for c in result) and "\\" not in result, "HTTPS evidence required")
    try:
        parsed = urlsplit(result)
        hostname, port = parsed.hostname, parsed.port
    except ValueError:
        message = "HTTPS evidence required"
        raise ValueError(message) from None
    require(
        parsed.scheme == "https"
        and hostname is not None
        and parsed.username is None
        and parsed.password is None
        and port in {None, 443}
        and re.fullmatch(r"[A-Za-z0-9.-]+", hostname)
        and "." in hostname
        and len(hostname) <= HOSTNAME_LIMIT
        and not hostname.endswith(".")
        and all(
            re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
            for label in hostname.split(".")
        ),
        "HTTPS evidence required",
    )
    return result


def instant(value: Any) -> str:
    result = text(value, 20)
    require(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", result), "UTC claim time required"
    )
    datetime.strptime(result, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    return result


def tree(root: Path, commit: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for record in git(root, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
        if not record:
            continue
        header, name = record.split(b"\t", 1)
        mode, kind, identity = header.decode("ascii").split(" ")
        name_text = path(name.decode("utf-8"))
        require(name_text not in result and kind in {"blob", "commit"}, "Invalid Git tree")
        result[name_text] = mode, revision(identity)
    return result


def blob(root: Path, entries: dict[str, tuple[str, str]], name: str) -> bytes | None:
    entry = entries.get(name)
    if entry is None:
        return None
    require(entry[0] == "100644", "Receipt/ledger must be a regular source file")
    return git(root, "cat-file", "blob", entry[1])


def audit_module() -> Any:
    name = "empathy_staging_diff_classifier"
    specification = importlib.util.spec_from_file_location(
        name, Path(__file__).with_name("staging_home_audit.py")
    )
    if specification is None or specification.loader is None:
        message = "Classifier unavailable"
        raise RuntimeError(message)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def receipts(raw: bytes | None) -> dict[str, dict[str, Any]]:
    if raw is None:
        return {}
    value = closed(document(raw), {"schema", "receipts"})
    require(
        value["schema"] == SCHEMA and isinstance(value["receipts"], list),
        "Receipt contract mismatch",
    )
    require(len(value["receipts"]) <= RECEIPT_LIMIT, "Receipt inventory exceeds bound")
    result: dict[str, dict[str, Any]] = {}
    sources: set[tuple[str, str, str]] = set()
    for item in value["receipts"]:
        row = closed(
            item,
            {
                "id",
                "source",
                "destination",
                "provenance_resolution",
                "sensitivity_resolution",
                "authority",
            },
        )
        identifier = text(row["id"], 80)
        require(re.fullmatch(r"STG-[A-Za-z0-9][A-Za-z0-9._-]*", identifier), "Invalid receipt ID")
        source = closed(row["source"], {"revision", "path", "mode", "blob"})
        revision(source["revision"])
        path(source["path"], staged=True)
        require(
            isinstance(source["mode"], str) and source["mode"] in {"100644", "100755", "120000"},
            "Unsupported staged preimage",
        )
        revision(source["blob"])
        destination = closed(
            row["destination"], {"canonical_home", "revision", "validation_evidence"}
        )
        path(destination["canonical_home"])
        revision(destination["revision"])
        url(destination["validation_evidence"])
        for field in ("provenance_resolution", "sensitivity_resolution"):
            text(row[field])
        authority = closed(row["authority"], {"kind", "actor", "recorded_at", "evidence"})
        require(authority["kind"] == "human-claim", "Receipt cannot authenticate human authority")
        text(authority["actor"], 256)
        instant(authority["recorded_at"])
        url(authority["evidence"])
        key = source["path"], source["mode"], source["blob"]
        require(identifier not in result and key not in sources, "Duplicate receipt/preimage")
        sources.add(key)
        result[identifier] = row
    require(list(result) == sorted(result), "Receipts must be sorted by ID")
    return result


def legacy(raw: bytes | None) -> list[dict[str, Any]]:
    if raw is None:
        return []
    value = closed(document(raw), {"schema_version", "approvals"})
    require(
        value["schema_version"] == "1.0.0" and isinstance(value["approvals"], list),
        "Legacy approval contract mismatch",
    )
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    fields = {
        "source_path",
        "git_blob",
        "destination",
        "destination_revision",
        "validation_evidence",
        "provenance_resolution",
        "sensitivity_resolution",
        "approved_by",
        "approved_at",
    }
    for item in value["approvals"]:
        row = closed(item, fields)
        name = path(row["source_path"], staged=True)
        require(name not in seen, "Duplicate legacy approval")
        seen.add(name)
        revision(row["git_blob"])
        for field in fields - {"source_path", "git_blob", "approved_at"}:
            text(row[field])
        require(
            len(row["destination_revision"]) >= MINIMUM_LEGACY_REVISION,
            "Invalid legacy destination revision",
        )
        instant(row["approved_at"])
        result.append(row)
    return result


def validate_checkout(root: Path, head: str, entries: dict[str, tuple[str, str]]) -> None:
    require(
        git(root, "rev-parse", "HEAD", maximum=128).decode().strip() == head,
        "Ledger check requires the exact represented head checkout",
    )
    indexed: dict[str, tuple[str, str]] = {}
    for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        header, encoded_name = record.split(b"\t", 1)
        mode, identity, stage = header.decode("ascii").split(" ")
        require(stage == "0", "Unmerged index cannot prove ledger freshness")
        indexed[encoded_name.decode("utf-8")] = mode, identity
    require(indexed == entries, "Ledger check requires the represented head index")
    classifier = Path(__file__).with_name("staging_home_audit.py")
    expected_classifier = entries.get("tools/staging_home_audit.py")
    require(
        expected_classifier is not None
        and expected_classifier[0] == "100644"
        and classifier.read_bytes() == git(root, "cat-file", "blob", expected_classifier[1]),
        "Classifier must match the represented head source",
    )
    for name, (mode, identity) in entries.items():
        if not name.startswith(".staging/"):
            continue
        selected = root / name
        require(
            mode in {"100644", "100755"}
            and not any(part.is_symlink() for part in (selected, *selected.parents))
            and selected.is_file(),
            "Ledger check requires regular staged files",
        )
        require(selected.stat().st_size <= MAXIMUM, "Staged file exceeds input bound")
        content = selected.read_bytes()
        # Git blob framing, independent of filters or a mutable working-tree index.
        actual = hashlib.sha1(
            b"blob " + str(len(content)).encode() + b"\0" + content,
            usedforsecurity=False,
        ).hexdigest()
        require(actual == identity, "Staged working bytes differ from represented head")


def changed_sources(
    before: dict[str, tuple[str, str]],
    after: dict[str, tuple[str, str]],
    old: dict[str, dict[str, Any]],
    base_ledger_raw: bytes | None,
) -> list[dict[str, Any]]:
    base_ledger = (
        {}
        if base_ledger_raw is None
        else {
            row["source_path"]: row
            for row in csv.DictReader(io.StringIO(base_ledger_raw.decode("utf-8")))
        }
    )
    changes: list[dict[str, Any]] = []
    for name in sorted(set(before) | set(after)):
        if not name.startswith(".staging/") or before.get(name) == after.get(name):
            continue
        previous, following = before.get(name), after.get(name)
        match = [
            identifier
            for identifier, row in old.items()
            if row["source"]["path"] == name
            and previous == (row["source"]["mode"], row["source"]["blob"])
        ]
        require(
            previous is None or len(match) == 1,
            f"Missing base-admitted exact preimage receipt: {name}",
        )
        if previous is not None:
            ledger_row = base_ledger.get(name)
            if ledger_row is None:
                deny(f"Missing exact base ledger preimage: {name}")
            require(
                (ledger_row["git_mode"], ledger_row["git_blob"]) == previous,
                f"Missing exact base ledger preimage: {name}",
            )
            require(
                old[match[0]]["destination"]["canonical_home"] == ledger_row["canonical_home"],
                f"Receipt destination differs from the reviewed base ledger: {name}",
            )
        change = "added" if previous is None else "removed" if following is None else "modified"
        changes.append(
            {
                "path": name,
                "change": change,
                "before": previous,
                "after": following,
                "receipt": match[0] if match else None,
            }
        )
    return changes


def check(root: Path, base: str, head: str, *, check_ledger: bool = True) -> dict[str, Any]:
    base, head = revision(base), revision(head)
    for commit in (base, head):
        observed_commit = (
            git(root, "rev-parse", "--verify", commit + "^{commit}", maximum=128).decode().strip()
        )
        require(observed_commit == commit, "Exact base/head commits required")
    # Deliberately refuse a moving/diverged PR base: update the branch first.
    try:
        git(root, "merge-base", "--is-ancestor", base, head)
    except ValueError:
        message = "Reviewed base is unavailable or not an ancestor; update the branch first"
        raise ValueError(message) from None
    before, after = tree(root, base), tree(root, head)
    old = receipts(blob(root, before, RECEIPTS))
    current = receipts(blob(root, after, RECEIPTS))
    require(
        all(current.get(identifier) == row for identifier, row in old.items()),
        "Durable receipts are append-only; existing evidence must survive",
    )
    old_legacy, current_legacy = blob(root, before, LEGACY), blob(root, after, LEGACY)
    require(
        old_legacy is None or old_legacy == current_legacy, "Preserve historical approval bytes"
    )
    historical = legacy(current_legacy)
    source_trees: dict[str, dict[str, tuple[str, str]]] = {base: before, head: after}
    for row in current.values():
        selected = row["source"]
        source_revision = selected["revision"]
        if source_revision not in source_trees:
            git(root, "merge-base", "--is-ancestor", source_revision, head)
            source_trees[source_revision] = tree(root, source_revision)
        original = source_trees[source_revision].get(selected["path"])
        require(
            original == (selected["mode"], selected["blob"]),
            "Receipt source revision/preimage mismatch",
        )
    base_ledger_raw = blob(root, before, LEDGER)
    changes = changed_sources(before, after, old, base_ledger_raw)
    if check_ledger:
        validate_checkout(root, head, after)
        audit = audit_module()
        expected = blob(root, after, LEDGER)
        rendered = audit.render_csv(audit.build_rows(root)).encode("utf-8")
        require(
            expected is not None and expected == rendered,
            "Committed staging ledger is stale; regenerate through staging_home_audit.py",
        )
    reconciled = []
    for identifier, row in current.items():
        selected = row["source"]
        observed = after.get(selected["path"])
        if observed is None:
            state = "removed"
        else:
            state = (
                "present-exact"
                if observed == (selected["mode"], selected["blob"])
                else "source-changed"
            )
        reconciled.append(
            {
                "receipt": identifier,
                "state": state,
                "source": selected,
                "destination": row["destination"],
                "authority": "claim-not-authenticated",
            }
        )
    legacy_view = []
    for row in historical:
        observed = after.get(row["source_path"])
        if observed is None:
            state = "removed"
        else:
            state = "present-blob-only" if observed[1] == row["git_blob"] else "source-changed"
        legacy_view.append(
            {"claim": row, "state": state, "authority": "legacy-claim-not-authenticated"}
        )
    return {
        "schema": "egohygiene.empathy.staging-diff-evidence/v1",
        "base": base,
        "head": head,
        "binding": "valid",
        "human_authority": "not-authenticated",
        "changes": changes,
        "receipts": reconciled,
        "legacy_claims": legacy_view,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = check(args.repository_root.resolve(), args.base, args.head)
        if args.report:
            with args.report.open("x", encoding="utf-8") as output:
                json.dump(
                    result, output, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False
                )
                output.write("\n")
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        sys.stderr.write(f"Staging diff gate denied: {error}\n")
        return 1
    sys.stdout.write("Staging diff/ledger bindings valid; human authority is not authenticated\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
