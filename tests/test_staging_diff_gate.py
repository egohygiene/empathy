# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Stdlib unittest is the repository framework; do not add pytest for exception assertions.
# ruff: noqa: PT027
"""Disposable Git histories only; no production staged file is edited or removed."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil

# Controlled disposable Git histories only; no shell or supplied executable.
import subprocess  # nosec B404
import sys
import tempfile
from typing import Any
import unittest

import yaml

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "staging_diff_gate", ROOT / "tools/staging_diff_gate.py"
)
assert SPEC is not None
assert SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)
STAGED = ".staging/devenvironment/workstation/shared/shell/.bash_logout"


class StagingDiffFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="empathy-staging-fixture-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.git("config", "user.name", "Synthetic fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write(
            "tools/staging_home_audit.py", (ROOT / "tools/staging_home_audit.py").read_text()
        )
        self.write(STAGED, "# inert synthetic shell-session fixture\n")
        self.write(gate.RECEIPTS, json.dumps({"schema": gate.SCHEMA, "receipts": []}))
        self.source = self.commit()
        self.source_blob = self.git("rev-parse", f"{self.source}:{STAGED}")

    def git(self, *arguments: str) -> str:
        environment = {
            "PATH": os.defpath,
            "LC_ALL": "C.UTF-8",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
        }
        executable = shutil.which("git", path=os.defpath)
        self.assertIsNotNone(executable)
        return (
            subprocess.check_output(  # noqa: S603  # nosec B603
                [
                    str(executable),
                    "-c",
                    "core.hooksPath=/dev/null",
                    "-c",
                    "commit.gpgsign=false",
                    "-C",
                    str(self.root),
                    *arguments,
                ],
                env=environment,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            .decode()
            .strip()
        )

    def write(self, path: str, content: str) -> None:
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    def commit(self, *, refresh: bool = True) -> str:
        self.git("add", "--all")
        if refresh:
            audit = gate.audit_module()
            self.write(gate.LEDGER, audit.render_csv(audit.build_rows(self.root)))
            self.git("add", "--all")
        self.git("commit", "--quiet", "--allow-empty", "-m", "synthetic fixture [skip ci]")
        return self.git("rev-parse", "HEAD")

    def receipt(self) -> dict[str, Any]:
        return {
            "id": "STG-synthetic-mantle-session",
            "source": {
                "revision": self.source,
                "path": STAGED,
                "mode": "100644",
                "blob": self.source_blob,
            },
            "destination": {
                "canonical_home": "mantle/config/session/bash_logout",
                "revision": "1" * 40,
                "validation_evidence": "https://github.com/egohygiene/mantle/pull/40",
            },
            "provenance_resolution": "Synthetic first-party fixture; no real migration claim.",
            "sensitivity_resolution": "Inert disposable text, never sourced or installed.",
            "authority": {
                "kind": "human-claim",
                "actor": "synthetic-unverified-actor",
                "recorded_at": "2026-10-18T03:32:03Z",
                "evidence": "https://github.com/egohygiene/empathy/issues/112",
            },
        }

    def admit(self, receipt: dict[str, Any] | None = None) -> str:
        self.write(
            gate.RECEIPTS,
            json.dumps({"schema": gate.SCHEMA, "receipts": [receipt or self.receipt()]}),
        )
        return self.commit()

    def test_deletion_without_receipt_denies(self) -> None:
        (self.root / STAGED).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "Missing base-admitted"):
            gate.check(self.root, self.source, head)

    def test_same_change_cannot_supply_its_own_approval(self) -> None:
        self.write(gate.RECEIPTS, json.dumps({"schema": gate.SCHEMA, "receipts": [self.receipt()]}))
        (self.root / STAGED).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "Missing base-admitted"):
            gate.check(self.root, self.source, head)

    def test_exact_prior_receipt_binds_removed_preimage_and_survives_regeneration(self) -> None:
        base = self.admit()
        (self.root / STAGED).unlink()
        head = self.commit()
        result = gate.check(self.root, base, head)
        self.assertEqual(result["changes"][0]["change"], "removed")
        self.assertEqual(result["receipts"][0]["state"], "removed")
        self.assertEqual(result["human_authority"], "not-authenticated")
        self.assertEqual(result["receipts"][0]["authority"], "claim-not-authenticated")
        self.assertIn("synthetic-unverified-actor", (self.root / gate.RECEIPTS).read_text())

    def test_modified_preimage_is_checked_even_when_path_survives(self) -> None:
        self.write(STAGED, "replacement must not bypass the removal gate\n")
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "Missing base-admitted"):
            gate.check(self.root, self.source, head)

    def test_renaming_does_not_transfer_approval(self) -> None:
        base = self.admit()
        other = ".staging/misc/ROADMAP.md"
        self.write(other, (self.root / STAGED).read_text())
        base = self.commit()
        (self.root / other).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "Missing base-admitted"):
            gate.check(self.root, base, head)

    def test_actual_rename_requires_the_removed_source_preimage(self) -> None:
        self.git("mv", STAGED, ".staging/devenvironment/workstation/shared/shell/renamed")
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "Missing base-admitted"):
            gate.check(self.root, self.source, head)

    def test_stale_receipt_blob_denies(self) -> None:
        receipt = self.receipt()
        receipt["source"]["blob"] = "0" * 40
        base = self.admit(receipt)
        (self.root / STAGED).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "source revision/preimage"):
            gate.check(self.root, base, head)

    def test_destination_cannot_be_retargeted_by_head_classifier_or_ledger(self) -> None:
        receipt = self.receipt()
        receipt["destination"]["canonical_home"] = "mantle/unrelated/path"
        base = self.admit(receipt)
        (self.root / STAGED).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "reviewed base ledger"):
            gate.check(self.root, base, head)

    def test_existing_receipt_cannot_disappear_with_current_inventory_row(self) -> None:
        base = self.admit()
        self.write(gate.RECEIPTS, json.dumps({"schema": gate.SCHEMA, "receipts": []}))
        (self.root / STAGED).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "append-only"):
            gate.check(self.root, base, head)

    def test_stale_generated_current_ledger_denies(self) -> None:
        base = self.admit()
        (self.root / STAGED).unlink()
        head = self.commit(refresh=False)
        with self.assertRaisesRegex(ValueError, "ledger is stale"):
            gate.check(self.root, base, head)

    def test_legacy_claim_alone_cannot_authorize_new_cleanup(self) -> None:
        receipt = self.receipt()
        legacy = {
            "source_path": STAGED,
            "git_blob": self.source_blob,
            "destination": receipt["destination"]["canonical_home"],
            "destination_revision": "1" * 40,
            "validation_evidence": "synthetic fixture evidence only",
            "provenance_resolution": "synthetic source",
            "sensitivity_resolution": "inert text",
            "approved_by": "synthetic unverified claim",
            "approved_at": "2026-10-18T03:32:03Z",
        }
        self.write(gate.LEGACY, json.dumps({"schema_version": "1.0.0", "approvals": [legacy]}))
        base = self.commit()
        (self.root / STAGED).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "Missing base-admitted"):
            gate.check(self.root, base, head)

    def test_diverged_pr_base_requires_an_explicit_branch_update(self) -> None:
        self.write("head.txt", "head fixture\n")
        head = self.commit()
        self.git("checkout", "--quiet", "-b", "advanced-base", self.source)
        self.write("base.txt", "base fixture\n")
        base = self.commit()
        self.git("checkout", "--quiet", "main")
        with self.assertRaisesRegex(ValueError, "update the branch first"):
            gate.check(self.root, base, head)

    def test_working_tree_cannot_replace_the_committed_preimage(self) -> None:
        base = self.admit()
        self.write(STAGED, "uncommitted replacement\n")
        with self.assertRaisesRegex(ValueError, "working bytes"):
            gate.check(self.root, base, base)

    def test_duplicate_receipt_fields_and_invalid_authority_are_denied(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
            gate.receipts(b'{"schema":"x","schema":"y","receipts":[]}')
        receipt = self.receipt()
        receipt["authority"]["kind"] = "verified-human"
        with self.assertRaisesRegex(ValueError, "cannot authenticate"):
            gate.receipts(json.dumps({"schema": gate.SCHEMA, "receipts": [receipt]}).encode())

    def test_malformed_evidence_url_has_no_payload_diagnostic(self) -> None:
        # Construct explicit fake userinfo as fixture data, not a credential-looking source URL.
        synthetic_userinfo = "synthetic-user:synthetic-password"
        for value in (
            "https://example.org:secret/",
            "https://example.org/white space",
            "https://example.org\\evil/",
            f"https://{synthetic_userinfo}@example.invalid/",
        ):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "^HTTPS evidence required$"),
            ):
                gate.url(value)

    def test_pr_and_push_filters_cover_each_staging_control_surface(self) -> None:
        # Source scheduling contract only. Hosted event qualification is separate.
        # BaseLoader constructs scalar strings only, preserving GitHub's literal on key.
        workflow = yaml.load(  # nosec B506
            (ROOT / ".github/workflows/automation.yml").read_text(),
            Loader=yaml.BaseLoader,  # noqa: S506
        )
        for event in ("pull_request", "push"):
            for pattern in (
                ".staging/**",
                "migration/**",
                "tools/staging_*.py",
                "schemas/staging-*.schema.json",
                "docs/migration/**",
            ):
                self.assertIn(pattern, workflow["on"][event]["paths"])
        job = workflow["jobs"]["staging"]
        self.assertNotIn("needs", job)
        self.assertEqual(workflow["permissions"], {"contents": "read"})


if __name__ == "__main__":
    unittest.main()
