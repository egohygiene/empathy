# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Regression scenarios for independent baseline command outcomes."""

from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
from pathlib import Path
import subprocess  # nosec B404 - fixtures simulate subprocess outcomes without execution.
import sys
import tempfile
from typing import TYPE_CHECKING
import unittest
from unittest.mock import patch

if TYPE_CHECKING:
    from tools import baseline_tests
else:
    MODULE_PATH = Path(__file__).resolve().parents[1] / "tools/baseline_tests.py"
    SPEC = importlib.util.spec_from_file_location("baseline_tests", MODULE_PATH)
    assert SPEC is not None
    assert SPEC.loader is not None
    baseline_tests = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = baseline_tests
    SPEC.loader.exec_module(baseline_tests)


class BaselineTestsRunnerTests(unittest.TestCase):
    """No child suite is launched by these controlled process fixtures."""

    def test_first_suite_failure_does_not_hide_second_suite(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temporary,
            redirect_stdout(io.StringIO()),
            patch.object(
                subprocess,
                "run",
                side_effect=[
                    subprocess.CompletedProcess(["fixture"], 1),
                    subprocess.CompletedProcess(["fixture"], 0),
                ],
            ) as execute,
        ):
            outcomes = baseline_tests.run_suites(Path(temporary), Path(temporary) / "results")
            self.assertEqual([outcome.succeeded for outcome in outcomes], [False, True])
            self.assertEqual([outcome.suite for outcome in outcomes], ["repository", "egolint"])
            self.assertEqual(execute.call_count, 2)
            self.assertEqual(execute.call_args_list[0].args[0][5], "tests")
            self.assertEqual(execute.call_args_list[1].args[0][5], "egolint/tests")

    def test_unavailable_first_command_does_not_hide_second_suite(self) -> None:
        failures = [OSError("fixture"), subprocess.TimeoutExpired(["fixture"], 300)]
        for failure in failures:
            with (
                self.subTest(failure=type(failure).__name__),
                tempfile.TemporaryDirectory() as temporary,
                redirect_stdout(io.StringIO()),
                patch.object(
                    subprocess,
                    "run",
                    side_effect=[failure, subprocess.CompletedProcess(["fixture"], 0)],
                ),
            ):
                outcomes = baseline_tests.run_suites(Path(temporary), Path(temporary) / "results")
                self.assertIsNone(outcomes[0].exit_code)
                self.assertIsNotNone(outcomes[0].unavailable)
                self.assertFalse(outcomes[0].succeeded)
                self.assertTrue(outcomes[1].succeeded)

    def test_summary_does_not_turn_unavailable_or_success_into_acceptance(self) -> None:
        summary = baseline_tests.render_summary(
            [
                baseline_tests.SuiteOutcome("repository", None, "timeout"),
                baseline_tests.SuiteOutcome("egolint", 0),
            ],
        )
        self.assertIn("| repository | timeout | unavailable |", summary)
        self.assertIn("| egolint | succeeded | 0 |", summary)
        self.assertIn("not full acceptance evidence", summary)
        self.assertIn("environment skips", summary)

    def test_main_fails_if_either_command_fails_and_retains_both_results(self) -> None:
        with (
            tempfile.TemporaryDirectory() as temporary,
            redirect_stdout(io.StringIO()),
            patch.object(sys, "argv", ["baseline_tests.py", "--output-directory", temporary]),
            patch.object(
                baseline_tests,
                "run_suites",
                return_value=[
                    baseline_tests.SuiteOutcome("repository", 1),
                    baseline_tests.SuiteOutcome("egolint", 0),
                ],
            ),
        ):
            self.assertEqual(baseline_tests.main(), 1)
            result = (Path(temporary) / "results.json").read_text(encoding="utf-8")
            self.assertIn('"acceptance": "unqualified"', result)
            self.assertIn('"suite": "repository"', result)
            self.assertIn('"suite": "egolint"', result)


if __name__ == "__main__":
    unittest.main()
