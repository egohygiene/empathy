# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Exercise the actual Scorecard caller and immutable Relay action offline.

RELAY_CHECKOUT selects the exact workflow pin. EMPATHY_SCORECARD_SARIF may select
a retained native SARIF for a private replay; API responses below are controlled
fixtures, not a reconstruction of any unavailable provider cache. No replay
output is a provider artifact or an original normalization timestamp.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess  # nosec B404
from tempfile import TemporaryDirectory
from typing import Any, ClassVar, cast
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def yaml_object(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        message = "Expected a checked-in YAML object"
        raise TypeError(message)
    return cast("dict[str, Any]", value)


class ScorecardCallerContractTests(unittest.TestCase):
    """Keep optional API data subordinate to the unchanged source/path contract."""

    action_root: ClassVar[Path]
    action_script: ClassVar[str]
    fetch_script: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        checkout = os.environ.get("RELAY_CHECKOUT")
        if not checkout:
            message = "Set RELAY_CHECKOUT for the pinned caller/action regression"
            raise unittest.SkipTest(message)
        if not shutil.which("jq"):
            message = "The workflow caller requires jq"
            raise unittest.SkipTest(message)
        workflow = yaml_object(ROOT / ".github/workflows/ossf-scorecard.yml")
        steps = workflow["jobs"]["normalize-summary"]["steps"]
        normalize = next(step for step in steps if step.get("id") == "normalize")
        fetch = next(step for step in steps if step.get("id") == "scorecard-api")
        pin = normalize["uses"].rsplit("@", 1)[1]
        # Fixed local metadata query; no shell or repository program executes.
        actual = subprocess.run(  # noqa: S603 # nosec B603, B607
            ["git", "-C", checkout, "rev-parse", "HEAD"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if actual != pin:
            message = "RELAY_CHECKOUT must match the exact normalization action pin"
            raise AssertionError(message)
        cls.action_root = Path(checkout) / "actions/normalize-repository-report"
        cls.action_script = yaml_object(cls.action_root / "action.yml")["runs"]["steps"][0]["run"]
        cls.fetch_script = fetch["run"]

    @staticmethod
    def sarif_bytes() -> bytes:
        retained = os.environ.get("EMPATHY_SCORECARD_SARIF")
        if retained:
            return Path(retained).read_bytes()
        return json.dumps(
            {
                "version": "2.1.0",
                "runs": [
                    {
                        "tool": {
                            "driver": {"rules": [{"id": "CallerFixture", "name": "CallerFixture"}]}
                        },
                        "results": [
                            {"ruleId": "CallerFixture", "message": {"text": "score is 3: fixture"}}
                        ],
                    }
                ],
            }
        ).encode()

    def replay(self, api_state: str, *, absolute_override: bool = False) -> dict[str, Any]:
        source = os.environ.get("EMPATHY_SCORECARD_SOURCE_COMMIT", "a" * 40)
        self.assertRegex(source, r"^[a-f0-9]{40}$")
        with TemporaryDirectory() as directory:
            parent = Path(directory)
            workspace = parent / "workspace"
            cache = workspace / ".cache/scorecard"
            cache.mkdir(parents=True)
            raw = self.sarif_bytes()
            (cache / "results.sarif").write_bytes(raw)
            fixture = parent / "api-fixture.json"
            fixture.write_text(
                json.dumps(
                    {
                        "repo": {
                            "name": "github.com/egohygiene/empathy",
                            "commit": source if api_state == "matched" else "0" * 40,
                        },
                        "score": 9.0,
                        "checks": [{"name": "CallerFixture", "score": 10}],
                    }
                ),
                encoding="utf-8",
            )
            commands = parent / "commands"
            commands.mkdir()
            # Stub only network/time, keeping the actual caller, jq admission,
            # composite shell prefix and Python normalizer unchanged.
            (commands / "curl").write_text(
                "#!/bin/sh\nset -eu\noutput=''\n"
                'while [ "$#" -gt 0 ]; do\n'
                "  if [ \"$1\" = '--output' ]; then output=$2; shift 2; else shift; fi\n"
                'done\n[ -n "${SCORECARD_API_FIXTURE-}" ] || exit 22\n'
                'cp -- "$SCORECARD_API_FIXTURE" "$output"\n',
                encoding="utf-8",
            )
            (commands / "sleep").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            for command in commands.iterdir():
                command.chmod(0o700)
            output = parent / "github-output"
            environment = os.environ.copy()
            environment.update(
                {
                    "PATH": str(commands) + os.pathsep + environment["PATH"],
                    "RUNNER_TEMP": str(parent),
                    "GITHUB_OUTPUT": str(output),
                    "GITHUB_SHA": source,
                    "SCORECARD_API_URL": "https://api.scorecard.dev/projects/github.com/egohygiene/empathy",
                    "SCORECARD_API_FIXTURE": str(fixture) if api_state != "unavailable" else "",
                }
            )
            subprocess.run(  # noqa: S603 # nosec B603, B607
                ["bash", "-euo", "pipefail", "-c", self.fetch_script],  # noqa: S607
                cwd=workspace,
                env=environment,
                check=True,
                capture_output=True,
            )
            selected = output.read_text(encoding="utf-8").strip().removeprefix("path=")
            if absolute_override:
                selected = str(parent / "scorecard-api.json")
            environment.update(
                {
                    "GITHUB_WORKSPACE": str(workspace),
                    "GITHUB_ACTION_PATH": str(self.action_root),
                    "GITHUB_REPOSITORY": "egohygiene/empathy",
                    "GITHUB_SERVER_URL": "https://github.com",
                    "GITHUB_EVENT_NAME": "workflow_dispatch",
                    "GITHUB_WORKFLOW": "Offline Scorecard caller regression",
                    "GITHUB_RUN_ID": "",
                    "GITHUB_RUN_ATTEMPT": "",
                    "INPUT_PRODUCER": "scorecard",
                    "INPUT_PATH": ".cache/scorecard/results.sarif",
                    "INPUT_OUTPUT": ".reports/scorecard/summary.json",
                    "INPUT_POLICY_PATH": "",
                    "INPUT_SCORECARD_API_PATH": selected,
                    "INPUT_STALE_AFTER_DAYS": "8",
                    "INPUT_REPOSITORY": "",
                    "INPUT_COMMIT": "",
                    "INPUT_GENERATED_AT": "",
                    "INPUT_DETAIL_URL": "",
                }
            )
            result = subprocess.run(  # noqa: S603 # nosec B603, B607
                ["bash", "-euo", "pipefail", "-c", self.action_script],  # noqa: S607
                cwd=workspace,
                env=environment,
                capture_output=True,
                check=False,
            )
            summary = workspace / ".reports/scorecard/summary.json"
            self.assertEqual((cache / "results.sarif").read_bytes(), raw)
            if absolute_override:
                self.assertEqual(result.returncode, 2)
                self.assertIn(b"scorecard-api-input must be", result.stderr)
                self.assertFalse(summary.exists())
                return {}
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            if selected:
                self.assertFalse(Path(selected).is_absolute())
                self.assertTrue(selected.startswith(".cache/scorecard/"))
            document = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(document["commit"], source)
            self.assertEqual(document["execution"]["state"], "success")
            self.assertIsNone(document["provenance"]["run_id"])
            return cast("dict[str, Any]", document)

    def test_optional_api_source_states_preserve_fresh_sarif(self) -> None:
        missing = self.replay("unavailable")
        stale = self.replay("stale")
        for document, state in ((missing, "unavailable"), (stale, "stale")):
            self.assertEqual(document["scorecard"]["api_status"], state)
            self.assertIsNone(document["scorecard"]["aggregate_score"])
            self.assertEqual(document["scorecard"]["check_source"], "sarif")
            self.assertGreater(document["scorecard"]["checks_needing_attention"], 0)
        self.assertEqual(missing["findings"], stale["findings"])
        matched = self.replay("matched")
        self.assertEqual(matched["scorecard"]["api_status"], "matched")
        self.assertEqual(matched["scorecard"]["aggregate_score"], 9.0)
        self.assertEqual(matched["scorecard"]["check_source"], "api")

    def test_absolute_optional_api_path_remains_denied(self) -> None:
        self.replay("matched", absolute_override=True)

    def test_selected_api_cache_is_ignored(self) -> None:
        result = subprocess.run(  # nosec B603, B607
            ["git", "check-ignore", "--no-index", ".cache/scorecard/scorecard-api.json"],  # noqa: S607
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
