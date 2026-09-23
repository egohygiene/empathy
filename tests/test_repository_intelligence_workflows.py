# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Consumer publication policy and real-scheduler fixture contracts.

The expression evaluator checks the explicit policy. The no-op GitHub fixture
also exercises implicit status handling, which local boolean tests cannot prove.
PyYAML 6.0.3 is a validation-only dependency, installed by the contract workflow.
"""

from __future__ import annotations

import ast
from itertools import product
import json
import os
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
import unittest

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPOSITORY_ROOT / ".github/workflows"
RELAY_REVISION = "9a6315978766c336566b9fa7139b800fa8789ba5"
RESULTS = ("success", "failure", "cancelled", "skipped")
PRODUCERS = ("MegaLinter", "OpenSSF Scorecard", "🔍 OSV Vulnerability Scan")


class UniqueKeyLoader(yaml.BaseLoader):
    """Keep GitHub's `on` key a string and reject overwritten policy fields."""


def unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode) -> dict:
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in result:
            raise ValueError(f"duplicate YAML mapping key: {key}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def workflow(name: str) -> dict:
    return yaml.load((WORKFLOWS / name).read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def expression(source: str) -> str:
    return re.sub(r"\s+", " ", source.strip().removeprefix("${{").removesuffix("}}")).strip()


def evaluate(source: str, context: dict, *, cancelled: bool = False) -> bool:
    """Evaluate only the small, fail-closed expression grammar used by these gates."""

    source = expression(source).replace("&&", " and ").replace("||", " or ")
    source = re.sub(r"!(?!=)", " not ", source).strip()
    source = re.sub(
        r"\b(?:github|needs|inputs)(?:\.[\w-]+)+",
        lambda match: f"value({match.group()!r})",
        source,
    )

    def value(path: str):
        result = context
        for segment in path.split("."):
            result = result.get(segment, "") if isinstance(result, dict) else ""
        return result

    functions = {
        "value": value,
        "cancelled": lambda: cancelled,
        "always": lambda: True,
        "contains": lambda sequence, item: item in sequence,
        "fromJSON": json.loads,
        "format": lambda template, *args: template.format(*args),
    }

    def visit(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name) and node.id in ("true", "false"):
            return node.id == "true"
        if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
            values = [bool(visit(child)) for child in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not visit(node.operand)
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            left, right = visit(node.left), visit(node.comparators[0])
            if isinstance(node.ops[0], ast.Eq):
                return left == right
            if isinstance(node.ops[0], ast.NotEq):
                return left != right
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in functions and not node.keywords:
                return functions[node.func.id](*(visit(arg) for arg in node.args))
        raise ValueError(f"unsupported policy expression node: {type(node).__name__}")

    return bool(visit(ast.parse(source, mode="eval").body))


def event_context(event="push", *, ref="refs/heads/main", producer="MegaLinter",
                  producer_event="push", producer_repository="egohygiene/empathy",
                  workflow_repository="egohygiene/empathy", producer_branch="main",
                  conclusion="success") -> dict:
    return {
        "github": {
            "event_name": event,
            "repository": "egohygiene/empathy",
            "ref": ref,
            "ref_name": ref.removeprefix("refs/heads/"),
            "event": {
                "repository": {"default_branch": "main"},
                "workflow_run": {
                    "name": producer,
                    "event": producer_event,
                    "head_repository": {"full_name": producer_repository},
                    "repository": {"full_name": workflow_repository},
                    "head_branch": producer_branch,
                    "conclusion": conclusion,
                },
            },
        },
        "needs": {
            "intelligence-review": {"result": "success"},
            "build": {"result": "success"},
            "deploy": {"result": "success"},
            "finalize-deployment": {"result": "success"},
        },
        "inputs": {"mode": "current"},
    }


class RepositoryIntelligenceWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pages = workflow("mindgarden-pages.yml")
        self.standalone = workflow("repository-intelligence.yml")
        self.gates = workflow("repository-intelligence-gates.yml")

    def run_report(self, step: dict, filename: str, extra_environment: dict,
                   expected_status: int) -> dict:
        with TemporaryDirectory() as directory:
            environment = {
                **os.environ,
                "RUNNER_TEMP": directory,
                "GITHUB_SHA": "a" * 40,
                "GITHUB_RUN_ID": "123",
                "GITHUB_RUN_ATTEMPT": "2",
                "PRIVATE_SENTINEL": "private-environment-sentinel",
                **extra_environment,
            }
            completed = subprocess.run(
                ["bash", "-c", step["run"]], check=False, capture_output=True, text=True,
                cwd=directory, env=environment,
            )
            self.assertEqual(completed.returncode, expected_status, completed.stderr)
            report_text = (Path(directory) / filename).read_text(encoding="utf-8")
            self.assertLessEqual(len(report_text.encode("utf-8")), 8192)
            public_output = report_text + completed.stdout + completed.stderr
            self.assertNotIn("private-", public_output)
            self.assertNotIn(directory, public_output)
            self.assertNotIn("outputs", report_text)
            return json.loads(report_text)

    def test_duplicate_yaml_keys_cannot_silently_replace_a_trust_guard(self) -> None:
        for source in (
            "permissions:\n  contents: read\n  contents: write\n",
            "jobs:\n  build:\n    if: false\n    if: true\n",
            "jobs:\n  deploy: {}\n  deploy: {}\n",
        ):
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "duplicate"):
                yaml.load(source, Loader=UniqueKeyLoader)
        for name in ("mindgarden-pages.yml", "repository-intelligence.yml",
                     "repository-intelligence-gates.yml"):
            self.assertIn("on", workflow(name))

    def test_both_integrations_pin_the_reviewed_relay_revision(self) -> None:
        for name in ("mindgarden-pages.yml", "repository-intelligence.yml"):
            source = (WORKFLOWS / name).read_text(encoding="utf-8")
            current = re.findall(
                r"uses:\s*egohygiene/relay/(?:actions/repository-intelligence|"
                r"\.github/workflows/repository-intelligence\.yml)@([0-9a-f]{40})",
                source,
            )
            self.assertIn(RELAY_REVISION, current, name)
            if name == "repository-intelligence.yml":
                self.assertEqual(set(current), {RELAY_REVISION})
            for target in re.findall(r"^\s*uses:\s*([^\s#]+)", source, re.MULTILINE):
                if not target.startswith("./"):
                    self.assertRegex(target, r"@[0-9a-f]{40}$", name)
            self.assertNotIn("pull_request_target:", source)
            self.assertNotRegex(source, r"secrets\s*[.:]")

    def test_trusted_refresh_allowlist_preserves_unsuccessful_producer_evidence(self) -> None:
        build = self.pages["jobs"]["build"]["if"]
        self.assertNotIn("workflow_run.conclusion", build)
        self.assertEqual(set(self.pages["on"]["workflow_run"]["workflows"]), set(PRODUCERS))
        self.assertEqual(self.pages["on"]["workflow_run"]["types"], ["completed"])
        for producer, producer_event, conclusion in product(
            PRODUCERS, ("push", "schedule", "workflow_dispatch"),
            ("success", "failure", "cancelled", "timed_out", "action_required", "neutral", "skipped"),
        ):
            context = event_context("workflow_run", producer=producer,
                                    producer_event=producer_event, conclusion=conclusion)
            with self.subTest(producer=producer, event=producer_event, conclusion=conclusion):
                self.assertTrue(evaluate(build, context))
        for changes in (
            {"producer": "Unknown producer"},
            {"producer_event": "pull_request"},
            {"producer_event": "pull_request_target"},
            {"producer_event": "repository_dispatch"},
            {"producer_repository": "untrusted/fork"},
            {"workflow_repository": "untrusted/fork"},
            {"producer_branch": "feature"},
        ):
            with self.subTest(changes=changes):
                self.assertFalse(evaluate(build, event_context("workflow_run", **changes)))

    def test_pr_and_untrusted_events_never_enter_publication(self) -> None:
        self.assertNotIn("pull_request_target", self.pages["on"])
        self.assertEqual(self.pages["on"]["push"]["branches"], ["main"])
        for context, build_allowed, publication_allowed in (
            (event_context("pull_request", ref="refs/pull/94/merge"), True, False),
            # Unconfigured events are excluded by the trigger, not a write-capable
            # build path. Manual branches may retain read-only review artifacts.
            (event_context("pull_request_target"), True, False),
            (event_context("push"), True, True),
            (event_context("push", ref="refs/heads/feature"), True, False),
            (event_context("workflow_dispatch"), True, True),
            (event_context("workflow_dispatch", ref="refs/heads/feature"), True, False),
            (event_context("workflow_run", producer_event="pull_request"), False, False),
            (event_context("workflow_run", producer_repository="untrusted/fork"), False, False),
        ):
            with self.subTest(context=context):
                self.assertEqual(evaluate(self.pages["jobs"]["build"]["if"], context), build_allowed)
                for name in ("deploy", "finalize-deployment", "verify-live"):
                    self.assertEqual(evaluate(self.pages["jobs"][name]["if"], context), publication_allowed, name)

    def test_deployment_status_gates_reject_failed_or_cancelled_prerequisites(self) -> None:
        jobs = self.pages["jobs"]
        self.assertIn("!cancelled()", expression(jobs["deploy"]["if"]))
        self.assertIn("!cancelled()", expression(jobs["verify-live"]["if"]))
        self.assertIn("always()", expression(jobs["finalize-deployment"]["if"]))
        for cancelled, build, deployed, finalized in product((False, True), RESULTS, RESULTS, RESULTS):
            context = event_context("workflow_dispatch")
            for name, result in (("build", build), ("deploy", deployed), ("finalize-deployment", finalized)):
                context["needs"][name]["result"] = result
            with self.subTest(cancelled=cancelled, build=build, deploy=deployed, finalized=finalized):
                self.assertEqual(
                    evaluate(jobs["deploy"]["if"], context, cancelled=cancelled),
                    not cancelled and build == "success",
                )
                self.assertEqual(
                    evaluate(jobs["finalize-deployment"]["if"], context, cancelled=cancelled),
                    build == "success" and deployed not in ("cancelled", "skipped"),
                )
                self.assertEqual(
                    evaluate(jobs["verify-live"]["if"], context, cancelled=cancelled),
                    not cancelled and build == deployed == finalized == "success",
                )

    def test_privileged_deployer_runs_only_the_official_pinned_pages_action(self) -> None:
        for document in (self.pages, self.standalone):
            self.assertEqual(document.get("permissions"), {"contents": "read"})
            for name, job in document["jobs"].items():
                permissions = job.get("permissions", document["permissions"])
                writes = {key for key, value in permissions.items() if value == "write"}
                if document is self.pages and name == "deploy":
                    self.assertEqual(writes, {"pages", "id-token"})
                    self.assertEqual(job["environment"]["name"], "github-pages")
                    self.assertEqual(len(job["steps"]), 1)
                    self.assertRegex(job["steps"][0]["uses"], r"^actions/deploy-pages@[0-9a-f]{40}$")
                else:
                    self.assertEqual(writes, set(), name)
                    self.assertNotIn("environment", job, name)
        self.assertNotIn("contents: write", (WORKFLOWS / "mindgarden-pages.yml").read_text())

    def test_build_has_no_shared_cache_credentials_or_snapshot_publisher(self) -> None:
        for name in ("mindgarden-pages.yml", "repository-intelligence.yml"):
            document = workflow(name)
            for job_name, job in document["jobs"].items():
                if job_name == "deploy":
                    continue
                for step in job.get("steps", []):
                    target = step.get("uses", "")
                    self.assertNotIn("publish-report-snapshot", target)
                    self.assertNotIn("actions/cache@", target)
                    if target.startswith("actions/checkout@"):
                        self.assertEqual(step.get("with", {}).get("persist-credentials"), "false")
                    if target.startswith("actions/setup-node@"):
                        self.assertNotIn("cache", step.get("with", {}))
        source = (WORKFLOWS / "mindgarden-pages.yml").read_text(encoding="utf-8")
        self.assertNotIn("secrets: inherit", source)
        self.assertNotIn("secrets.", source)

    def test_pr_matrix_retains_review_evidence_without_a_pages_artifact(self) -> None:
        build = self.pages["jobs"]["build"]
        matrix = build["strategy"]["matrix"]["mode"]
        self.assertIn("github.event_name == 'pull_request'", matrix)
        self.assertIn('fromJSON(\'["current","rollback-v1.4"]\')', matrix)
        self.assertEqual(build["strategy"]["fail-fast"], "false")
        publications = []
        artifacts = []
        for step in build["steps"]:
            action = step.get("uses", "")
            if action.startswith(("actions/configure-pages@", "actions/upload-pages-artifact@")):
                publications.append(step)
                self.assertFalse(evaluate(step["if"], event_context("pull_request")))
                self.assertFalse(evaluate(step["if"], event_context("workflow_run", producer_event="pull_request")))
                self.assertFalse(evaluate(step["if"], event_context("workflow_run", producer_repository="untrusted/fork")))
                self.assertTrue(evaluate(step["if"], event_context("push")))
            if action.startswith("actions/upload-artifact@"):
                artifacts.append(step)
                self.assertEqual(step["with"]["retention-days"], "30")
        self.assertEqual(len(publications), 2)
        for prefix in ("empathy-composed-", "empathy-provenance-"):
            matching = [step for step in artifacts if step["with"]["name"].startswith(prefix)]
            self.assertEqual(len(matching), 1, prefix)
            self.assertNotIn("if", matching[0], "successful PR builds must retain review evidence")
            self.assertIn("github.run_id", matching[0]["with"]["name"])
            self.assertIn("github.run_attempt", matching[0]["with"]["name"])
        standalone_upload = next(
            step for step in self.standalone["jobs"]["generate"]["steps"]
            if step.get("name") == "Upload public intelligence review artifact"
        )
        self.assertNotIn("inputs.output-root", standalone_upload["with"]["path"])
        self.assertIn("inputs.dashboard-output-root", standalone_upload["with"]["path"])

    def test_deployment_receipt_is_separate_from_deterministic_public_output(self) -> None:
        jobs = self.pages["jobs"]
        operations = {
            step.get("with", {}).get("operation")
            for step in jobs["build"]["steps"]
        }
        self.assertIn("capture-baseline", operations)
        self.assertIn("verify-composition", operations)
        self.assertNotIn("record-receipt", operations)
        receipt = next(
            step for step in jobs["finalize-deployment"]["steps"]
            if step.get("with", {}).get("operation") == "record-receipt"
        )
        options = receipt["with"]
        self.assertEqual(options["site-directory"], ".cache/mindgarden/site")
        self.assertEqual(options["evidence-directory"], ".cache/mindgarden/publication")
        self.assertIn("needs.build.outputs.represented-revision", options["consumer-revision"])
        self.assertIn("needs.deploy.outputs.deployment-url", options["deployment-url"])
        self.assertIn("github.run_id", options["workflow-run-id"])
        self.assertIn("github.run_attempt", options["workflow-run-attempt"])
        for name in ("finalize-deployment", "verify-live"):
            download = next(
                step for step in jobs[name]["steps"]
                if step.get("uses", "").startswith("actions/download-artifact@")
            )
            self.assertIn("github.run_id", download["with"]["name"])
            self.assertIn("github.run_attempt", download["with"]["name"])
            self.assertIn("needs.build.outputs.deployment-mode", download["with"]["name"])

    def test_build_report_requires_artifact_uploads_and_every_applicable_stage(self) -> None:
        steps = self.pages["jobs"]["build"]["steps"]
        report_step = next(step for step in steps if step.get("name") == "Preserve sanitized build result")
        pages_upload = next(step for step in steps if step.get("id") == "pages_artifact")
        self.assertEqual(expression(report_step["env"]["PUBLISH_EXPECTED"]), expression(pages_upload["if"]))
        self.assertEqual(expression(report_step["if"]), "always()")
        statuses = {
            step["id"]: {"outcome": "success", "outputs": {"ignored": "private-output-sentinel"}}
            for step in steps if "id" in step
        }
        statuses["unrecognized-stage"] = {"outcome": "private-stage-sentinel"}
        filename = "empathy-publication-run.json"
        for mode, publish in product(("current", "rollback-v1.4"), ("true", "false")):
            environment = {"RESULTS": json.dumps(statuses), "MODE": mode, "PUBLISH_EXPECTED": publish}
            report = self.run_report(report_step, filename, environment, 0)
            self.assertEqual(report["conclusion"], "success")
            self.assertEqual(report["publication_expected"], publish == "true")
            self.assertEqual("pages_artifact" in report["observed"], publish == "true")
            self.assertEqual("rollback_checkout" in report["observed"], mode == "rollback-v1.4")
            self.assertEqual("canonical_baseline" in report["observed"], mode == "current")
            for stage, code in (
                ("helper_tools", "EMRI-001"), ("runtime", "EMRI-004"),
                ("review_artifact", "EMRI-008"), ("provenance_artifact", "EMRI-008"),
                ("pages_artifact", "EMRI-009"), ("configure_pages", "EMRI-009"),
                ("rollback_checkout", "EMRI-002"),
            ):
                if stage not in report["observed"]:
                    continue
                failed = {**statuses, stage: {"outcome": "failure", "outputs": {"ignored": "private-output-sentinel"}}}
                failure = self.run_report(report_step, filename, {**environment, "RESULTS": json.dumps(failed)}, 1)
                self.assertEqual(failure["conclusion"], "failure")
                self.assertEqual(failure["stage"], stage)
                self.assertEqual(failure["error_code"], code)
                self.assertTrue(failure["remediation"])
        statuses["review_artifact"]["outcome"] = "private-outcome-sentinel"
        failure = self.run_report(
            report_step, filename,
            {"RESULTS": json.dumps(statuses), "MODE": "current", "PUBLISH_EXPECTED": "false"}, 1,
        )
        self.assertEqual(failure["observed"]["review_artifact"], "unavailable")
        failure = self.run_report(
            report_step, filename,
            {"RESULTS": json.dumps(statuses), "MODE": "private-mode-sentinel", "PUBLISH_EXPECTED": "false"}, 1,
        )
        self.assertEqual(failure["mode"], "unavailable")
        self.assertEqual(failure["error_code"], "EMRI-010")

    def test_standalone_report_requires_review_upload_and_sanitizes_outcomes(self) -> None:
        steps = self.standalone["jobs"]["generate"]["steps"]
        report_step = next(step for step in steps if step.get("name") == "Preserve sanitized run evidence")
        filename = "empathy-intelligence-run.json"
        environment = {key: "success" for key in ("HARDEN_RESULT", "CHECKOUT_RESULT", "INPUT_RESULT", "BUILD_RESULT", "ARTIFACT_RESULT")}
        report = self.run_report(report_step, filename, environment, 0)
        self.assertEqual(report["conclusion"], "success")
        for value in ("failure", "cancelled", "skipped", "private-outcome-sentinel"):
            report = self.run_report(report_step, filename, {**environment, "ARTIFACT_RESULT": value}, 1)
            self.assertEqual(report["conclusion"], "failure")
            self.assertEqual(report["stage"], "review_artifact")
            self.assertEqual(report["error_code"], "EMRI-008")
            self.assertEqual(report["observed"]["review_artifact"], value if value != "private-outcome-sentinel" else "unavailable")

    def test_scheduler_fixture_preserves_production_status_guards(self) -> None:
        production = self.pages["jobs"]
        fixtures = self.gates["jobs"]
        deploy = expression(production["deploy"]["if"])
        prefix = "!cancelled() && needs.build.result == 'success' && "
        self.assertTrue(deploy.startswith(prefix), "keep the status and trust clauses distinct")
        trusted_event = deploy.removeprefix(prefix)
        self.assertIn("github.event_name", trusted_event)
        for name in ("deploy", "finalize-deployment", "verify-live"):
            predicate = expression(production[name]["if"])
            self.assertTrue(predicate.endswith(trusted_event), name)
            self.assertEqual(
                expression(fixtures[name]["if"]), predicate.replace(trusted_event, "true"), name
            )
        for fixture_name, production_name in (
            ("forbidden-pr-deploy", "deploy"),
            ("forbidden-pr-finalize", "finalize-deployment"),
            ("forbidden-pr-live", "verify-live"),
        ):
            self.assertEqual(
                expression(fixtures[fixture_name]["if"]),
                expression(production[production_name]["if"]).replace(trusted_event, "false"),
                fixture_name,
            )
            self.assertEqual(fixtures[fixture_name]["steps"], [{"run": "exit 1"}])
        self.assertEqual(
            expression(fixtures["forbidden-failed-build-deploy"]["if"]),
            deploy.replace(trusted_event, "true").replace("needs.build.result", "'failure'"),
        )
        self.assertEqual(
            expression(fixtures["forbidden-cancelled-deploy"]["if"]),
            deploy.replace(trusted_event, "true").replace("cancelled()", "true"),
        )
        self.assertEqual(expression(fixtures["review"]["if"]), "github.run_id == '0'")
        self.assertEqual(expression(fixtures["build"]["if"]), "always()")
        self.assertEqual(fixtures["build"]["needs"], "review")
        self.assertEqual(expression(fixtures["assert-gates"]["if"]), "always()")

    def test_scheduler_fixture_has_no_publication_or_repository_execution_authority(self) -> None:
        source = (WORKFLOWS / "repository-intelligence-gates.yml").read_text(encoding="utf-8")
        self.assertEqual(self.gates["permissions"], {"contents": "read"})
        self.assertNotRegex(source, r":\s*write\b|secrets[.:]|pull_request_target|environment:")
        self.assertNotRegex(source, r"actions/(?:deploy-pages|upload-pages-artifact|configure-pages|checkout)@")
        for job in self.gates["jobs"].values():
            self.assertLessEqual(int(job["timeout-minutes"]), 5)
            for step in job.get("steps", []):
                if "uses" in step:
                    self.assertRegex(step["uses"], r"^actions/upload-artifact@[0-9a-f]{40}$")
                    self.assertEqual(step["with"]["retention-days"], "30")

    def test_scheduler_report_detects_skipped_deployment_and_excludes_private_payloads(self) -> None:
        report_step = next(
            step for step in self.gates["jobs"]["assert-gates"]["steps"]
            if step.get("name") == "Record and assert gate results"
        )
        expected = {
            "review": "skipped", "build": "success", "deploy": "success",
            "finalize-deployment": "success", "verify-live": "success",
            "forbidden-pr-deploy": "skipped", "forbidden-pr-finalize": "skipped",
            "forbidden-pr-live": "skipped", "forbidden-failed-build-deploy": "skipped",
            "forbidden-cancelled-deploy": "skipped",
        }
        results = {
            name: {"result": result, "outputs": {"ignored": "private-output-sentinel"}}
            for name, result in expected.items()
        }
        results["unrecognized-job"] = {"result": "private-job-sentinel"}
        with TemporaryDirectory() as directory:
            environment = {
                **os.environ,
                "RUNNER_TEMP": directory,
                "GITHUB_SHA": "a" * 40,
                "GITHUB_RUN_ID": "123",
                "GITHUB_RUN_ATTEMPT": "2",
                "PRIVATE_SENTINEL": "private-environment-sentinel",
            }
            for mutation, expected_status in ((None, 0), ("skipped", 1), ("private-result-sentinel", 1)):
                if mutation:
                    results["deploy"]["result"] = mutation
                completed = subprocess.run(
                    ["bash", "-c", report_step["run"]], check=False, capture_output=True,
                    text=True, cwd=directory, env={**environment, "GATE_RESULTS": json.dumps(results)},
                )
                self.assertEqual(completed.returncode, expected_status, completed.stderr)
                report_text = (Path(directory) / "empathy-gate-fixture.json").read_text(encoding="utf-8")
                report = json.loads(report_text)
                self.assertEqual(report["conclusion"], "success" if expected_status == 0 else "failure")
                self.assertEqual(report["run"], {"id": 123, "attempt": 2})
                self.assertLessEqual(len(report_text.encode("utf-8")), 8192)
                if mutation is None:
                    self.assertEqual(report["observed"], expected)
                if mutation == "private-result-sentinel":
                    self.assertEqual(report["observed"]["deploy"], "unavailable")
                public_output = report_text + completed.stdout + completed.stderr
                self.assertNotIn("private-", public_output)
                self.assertNotIn(directory, public_output)
                self.assertNotIn("outputs", report_text)


if __name__ == "__main__":
    unittest.main()
