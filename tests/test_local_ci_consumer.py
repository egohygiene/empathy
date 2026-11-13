# ruff: noqa: PT027
# This act fixture deliberately uses stdlib unittest without a pytest dependency.
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess  # nosec B404
import sys
import tempfile
from typing import TYPE_CHECKING, Any
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

if TYPE_CHECKING:
    from tools import foundation, local_ci
else:
    import local_ci

    import foundation


# A tiny owner-interface fixture, not a second execution engine. It records the
# delegated arguments and selected exit status without running repository checks.
OWNER_SCRIPT = """from pathlib import Path
import json
import sys

arguments = sys.argv[1:]
operation = arguments[0]
def argument(name):
    return arguments[arguments.index(name) + 1]
act = argument("--act")
status = int(act.removeprefix("status-")) if act.startswith("status-") else 0
if operation == "doctor":
    status = 2 if act == "unavailable" else status
    print(json.dumps({"ready": status == 0, "act": act}))
elif operation == "plan":
    print(json.dumps({"execution": "not-performed", "arguments": arguments}))
elif status != 2:
    destination = Path(argument("--output"))
    destination.mkdir(parents=True, exist_ok=False)
    report = {"complete": status == 0, "owner_status": status,
              "checks": [{"id": "native-platform", "kind": "unsupported",
                          "required": False, "status": "unsupported"}]}
    (destination / "report.json").write_text(json.dumps(report) + "\\n")
    print(json.dumps({"report": "report.json", "status": status}))
raise SystemExit(status)
"""


class LocalCIConsumerTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="empathy-local-ci-test-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.consumer = self.directory / "consumer"
        self.owner = self.directory / "realm"
        self.consumer.mkdir()
        self.owner.mkdir()
        self.catalog = foundation.load_json(ROOT / "foundation/catalog.json")
        self.manifest = foundation.load_json(ROOT / "foundation/empathy.manifest.json")
        self.manifest["selected_profiles"] = ["local-ci"]
        self.manifest["overrides"] = []
        self.manifest.pop("gitignore", None)
        self.write_json("foundation/catalog.json", self.catalog)
        self.write_json("foundation/empathy.manifest.json", self.manifest)
        for relative in (
            ".actrc",
            local_ci.MANIFEST_PATH,
            "tools/local_ci.py",
            ".github/act/local-validation.yml",
        ):
            destination = self.consumer / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        owner_contents = {
            "config/act.v1.json": json.dumps({"version": "0.2.97"}),
            "tools/realm_act.py": "# Synthetic installer interface fixture.\n",
            "tools/realm_act_network.py": "# Synthetic network interface fixture.\n",
            "tools/realm_local_ci.py": OWNER_SCRIPT,
        }
        for relative, contents in owner_contents.items():
            path = self.owner / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        self.git("init", "--quiet")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Synthetic owner interface")
        self.pin: dict[str, Any] = {
            "schema_version": "empathy.realm-local-ci-source/v1",
            "repository": "egohygiene/realm",
            "revision": self.git("rev-parse", "HEAD"),
            "act_version": "0.2.97",
            "files": {
                relative: local_ci.digest(self.owner / relative)
                for relative in sorted(local_ci.OWNER_FILES)
            },
        }
        self.write_json(local_ci.PIN_PATH, self.pin)

    def git(self, *arguments: str) -> str:
        """Use a disposable local Git repository without global hook execution."""
        git = shutil.which("git")
        if git is None:
            self.fail("Git is a prerequisite of the local-CI source-verification fixture")
        result = subprocess.run(  # noqa: S603  # nosec B603
            [
                git,
                "-C",
                str(self.owner),
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "commit.gpgSign=false",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                *arguments,
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
        return result.stdout.strip()

    def write_json(self, relative: str, value: object) -> None:
        path = self.consumer / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output, errors = io.StringIO(), io.StringIO()
        with (
            patch.object(local_ci, "ROOT", self.consumer),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            status = local_ci.main(list(arguments))
        return status, output.getvalue(), errors.getvalue()

    def select(self, profiles: list[str]) -> None:
        self.manifest["selected_profiles"] = profiles
        self.write_json("foundation/empathy.manifest.json", self.manifest)

    def populate_workspace(self, resolved: dict[str, Any]) -> None:
        for artifact in resolved["artifacts"]:
            path = self.consumer / artifact["path"]
            if path.exists():
                continue
            if artifact["kind"] == "directory":
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(artifact["markers"]) + "\n", encoding="utf-8")

    def test_selected_profile_requires_its_files(self) -> None:
        resolved = local_ci.selection(self.consumer)
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual({"local-ci", "universal"}, set(resolved["profiles"]))
        self.populate_workspace(resolved)
        self.assertEqual([], foundation.validate_workspace(self.consumer, resolved))
        (self.consumer / ".actrc").unlink()
        self.assertEqual(
            ["required file is missing: .actrc"],
            foundation.validate_workspace(self.consumer, resolved),
        )

    def test_unselected_profile_does_not_require_local_ci_files(self) -> None:
        self.select(["universal"])
        resolved, errors = foundation.resolve_manifest(self.catalog, self.manifest)
        self.assertEqual([], errors)
        assert resolved is not None
        self.assertIsNone(local_ci.selection(self.consumer))
        paths = {artifact["path"] for artifact in resolved["artifacts"]}
        self.assertTrue({".actrc", local_ci.MANIFEST_PATH, local_ci.PIN_PATH}.isdisjoint(paths))
        (self.consumer / ".actrc").unlink()
        self.populate_workspace(resolved)
        self.assertEqual([], foundation.validate_workspace(self.consumer, resolved))

    def test_unselected_plan_needs_no_realm_or_runtime(self) -> None:
        self.select(["universal"])
        for relative in (".actrc", local_ci.MANIFEST_PATH, local_ci.PIN_PATH):
            (self.consumer / relative).unlink()
        shutil.rmtree(self.owner)
        status, output, errors = self.invoke("plan")
        self.assertEqual(0, status, errors)
        self.assertEqual({"applicability": "not-selected", "checks": []}, json.loads(output))

    def test_unselected_run_is_not_a_successful_empty_run(self) -> None:
        self.select(["universal"])
        status, output, errors = self.invoke("run")
        self.assertEqual(2, status)
        self.assertEqual("", output)
        self.assertIn("not selected", errors)

    def test_project_host_and_broad_trust_options_are_rejected(self) -> None:
        actrc = self.consumer / ".actrc"
        original = actrc.read_text(encoding="utf-8")
        for option in (
            "--directory .",
            "--action-cache-path .cache/actions",
            "--cache-server-path .cache/cache",
            "--artifact-server-path .cache/artifacts",
            "--trust-project-actrc",
            "--env-file .env",
        ):
            with self.subTest(option=option):
                actrc.write_text(original + option + "\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "unreviewed .actrc option"):
                    local_ci.configuration(self.consumer)

    def test_runner_mapping_rejects_mutable_duplicate_and_mismatched_defaults(self) -> None:
        actrc = self.consumer / ".actrc"
        original = actrc.read_text(encoding="utf-8")
        manifest = foundation.load_json(self.consumer / local_ci.MANIFEST_PATH)
        act_check = next(check for check in manifest["checks"] if check["kind"] == "act")
        image = act_check["platforms"]["ubuntu-24.04"]
        act_check["platforms"]["ubuntu-24.04"] = "ubuntu:latest"
        self.write_json(local_ci.MANIFEST_PATH, manifest)
        with self.assertRaisesRegex(ValueError, "immutable"):
            local_ci.configuration(self.consumer)
        act_check["platforms"]["ubuntu-24.04"] = image
        self.write_json(local_ci.MANIFEST_PATH, manifest)
        actrc.write_text(original + f"--platform ubuntu-24.04={image}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            local_ci.configuration(self.consumer)
        actrc.write_text(
            original.replace(image, "example.invalid/runner@sha256:" + "a" * 64), encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "must match"):
            local_ci.configuration(self.consumer)

    def test_malformed_checks_and_mappings_fail_without_tracebacks(self) -> None:
        cases: tuple[object, ...] = (
            None,
            {},
            [None],
            [{"kind": "act", "platforms": None}],
            [{"kind": "act", "platforms": []}],
            [{"kind": "act", "platforms": {"ubuntu-24.04": 42}}],
        )
        for checks in cases:
            with self.subTest(checks=checks):
                self.write_json(local_ci.MANIFEST_PATH, {"checks": checks})
                status, output, errors = self.invoke("plan", "--realm-checkout", str(self.owner))
                self.assertEqual(2, status)
                self.assertEqual("", output)
                self.assertIn("local CI consumer failed", errors)
                self.assertNotIn("Traceback", errors)

    def test_exact_source_is_accepted_but_different_git_revision_is_rejected(self) -> None:
        self.assertEqual(self.pin, local_ci.source_pin(self.consumer, self.owner))
        self.git("commit", "--quiet", "--allow-empty", "-m", "Different owner revision")
        with self.assertRaisesRegex(ValueError, "immutable revision"):
            local_ci.source_pin(self.consumer, self.owner)

    def test_modified_owner_source_cannot_be_invoked(self) -> None:
        (self.owner / "tools/realm_local_ci.py").write_text(
            "raise AssertionError\n", encoding="utf-8"
        )
        with patch.object(local_ci, "invoke_owner") as invoke_owner:
            status, output, errors = self.invoke("plan", "--realm-checkout", str(self.owner))
        self.assertEqual(2, status)
        self.assertEqual("", output)
        self.assertIn("source bytes differ", errors)
        invoke_owner.assert_not_called()

    def test_symlinked_owner_source_is_rejected_even_with_matching_bytes(self) -> None:
        source = self.owner / "tools/realm_local_ci.py"
        outside = self.directory / "outside-owner.py"
        outside.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "source bytes differ"):
            local_ci.source_pin(self.consumer, self.owner)

    def test_owner_act_version_must_match_consumer_pin(self) -> None:
        path = self.owner / "config/act.v1.json"
        path.write_text(json.dumps({"version": "0.2.98"}), encoding="utf-8")
        self.pin["files"]["config/act.v1.json"] = local_ci.digest(path)
        self.write_json(local_ci.PIN_PATH, self.pin)
        with self.assertRaisesRegex(ValueError, "act pin differs"):
            local_ci.source_pin(self.consumer, self.owner)

    def test_plan_binds_owner_adapter_workflow_and_explicit_arguments(self) -> None:
        previous_arguments = sys.argv
        status, output, errors = self.invoke(
            "plan",
            "--realm-checkout",
            str(self.owner),
            "--act",
            "reviewed-act",
            "--cloud-network",
        )
        self.assertEqual(0, status, errors)
        self.assertIs(previous_arguments, sys.argv)
        plan = json.loads(output)
        self.assertEqual("not-performed", plan["plan"]["execution"])
        self.assertEqual(self.pin, plan["consumer"]["realm"])
        for relative in (
            "tools/local_ci.py",
            ".github/act/local-validation.yml",
            local_ci.MANIFEST_PATH,
        ):
            self.assertEqual(
                hashlib.sha256((self.consumer / relative).read_bytes()).hexdigest(),
                plan["consumer"]["configuration_sha256"][relative],
            )
        arguments = plan["plan"]["arguments"]
        self.assertIn("--cloud-network", arguments)
        self.assertEqual("reviewed-act", arguments[arguments.index("--act") + 1])
        self.assertEqual(str(self.consumer), arguments[arguments.index("--repository") + 1])

    def test_missing_selected_checkout_is_a_reported_prerequisite(self) -> None:
        status, output, errors = self.invoke("plan")
        self.assertEqual(2, status)
        self.assertEqual("", output)
        self.assertIn("explicit --realm-checkout", errors)

    def test_blocked_doctor_preserves_owner_failure(self) -> None:
        status, output, errors = self.invoke(
            "doctor",
            "--realm-checkout",
            str(self.owner),
            "--act",
            "unavailable",
        )
        self.assertEqual(2, status, errors)
        self.assertFalse(json.loads(output)["ready"])
        self.assertNotIn("consumer", json.loads(output))

    def test_failed_cancelled_and_successful_runs_keep_owner_status_and_receipt(self) -> None:
        for owner_status in (0, 1, 130, 143):
            with self.subTest(owner_status=owner_status):
                destination = self.directory / f"report-{owner_status}"
                status, _, errors = self.invoke(
                    "run",
                    "--realm-checkout",
                    str(self.owner),
                    "--act",
                    f"status-{owner_status}",
                    "--output",
                    str(destination),
                )
                self.assertEqual(owner_status, status, errors)
                report = json.loads((destination / "report.json").read_text(encoding="utf-8"))
                self.assertEqual(owner_status, report["owner_status"])
                self.assertEqual(owner_status == 0, report["complete"])
                self.assertEqual("unsupported", report["checks"][0]["status"])
                receipt = json.loads(
                    (destination / "consumer-source.json").read_text(encoding="utf-8")
                )
                self.assertEqual(self.pin, receipt["realm"])

    def test_invalid_owner_run_does_not_invent_execution_receipt(self) -> None:
        destination = self.directory / "not-run"
        status, _, errors = self.invoke(
            "run",
            "--realm-checkout",
            str(self.owner),
            "--act",
            "status-2",
            "--output",
            str(destination),
        )
        self.assertEqual(2, status, errors)
        self.assertFalse(destination.exists())

    def test_existing_report_and_receipt_are_never_rebound(self) -> None:
        destination = self.directory / "earlier-run"
        destination.mkdir()
        (destination / "report.json").write_bytes(b'{"earlier": "owner result"}\n')
        (destination / "consumer-source.json").write_bytes(b'{"earlier": "consumer source"}\n')
        before = {path.name: path.read_bytes() for path in destination.iterdir()}
        with patch.object(local_ci, "invoke_owner") as invoke_owner:
            status, _, errors = self.invoke(
                "run",
                "--realm-checkout",
                str(self.owner),
                "--output",
                str(destination),
            )
        self.assertEqual(2, status)
        self.assertIn("already exists", errors)
        invoke_owner.assert_not_called()
        self.assertEqual(before, {path.name: path.read_bytes() for path in destination.iterdir()})


if __name__ == "__main__":
    unittest.main()
