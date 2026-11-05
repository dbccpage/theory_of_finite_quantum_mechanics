"""Failure-injection tests for mutation accounting, byte custody and cleanup."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS))
sys.path.insert(0, str(TESTS.parent))
import run_support_mutations as runner
from checker_support.mutation_case import MutationCase
from checker_support.boundary import Violation

PASS = subprocess.CompletedProcess(["test"], 0, "", "\nRan 1 test in 0.001s\n\nOK\n")
FAIL = subprocess.CompletedProcess(["test"], 1, "", "\nRan 1 test in 0.001s\n\nFAILED (failures=1)\n")


def record() -> dict[str, object]:
    prefix = "    def require(self, condition: bool, message: str) -> None:\n        "
    return {"identity": "counter-fault", "source": "cases.py",
            "before": prefix+"self._checks += 1", "after": prefix+"self._checks = 1",
            "tests": ["test_counter_is_invocation_owned_and_counts_failed_obligations"]}


class MutationCampaignTests(unittest.TestCase):
    def test_accounting_mutants_are_detected(self) -> None:
        # Explicit replacement mutants challenge the accounting oracle itself.
        for false_status in ("killed", "survived", "inconclusive"):
            with self.subTest(mutant="constant-classification-"+false_status):
                with patch.object(runner, "classify", return_value=false_status):
                    with self.assertRaises(AssertionError):
                        self.test_status_attribution_excludes_harness_failures()
        for false_fraction in (1.0, 0.0):
            with self.subTest(mutant="incorrect-denominator-"+str(false_fraction)):
                with patch.object(runner, "detection", return_value={"eligible": 4, "detected_fraction": false_fraction}):
                    with self.assertRaises(AssertionError):
                        self.test_denominator_retains_unrun_and_inconclusive()

    def test_status_attribution_excludes_harness_failures(self) -> None:
        self.assertEqual(runner.classify(PASS.returncode, PASS.stderr), "survived")
        self.assertEqual(runner.classify(FAIL.returncode, FAIL.stderr), "killed")
        for code, output in ((0, ""), (1, "Traceback: import failed"),
                             (0, FAIL.stderr), (2, FAIL.stderr), (1, "\nRan nonsense\nFAILED (x)"),
                             (0, "\nRan 0 tests in 0.001s\n\nOK\n"),
                             (0, "\nRan 1 test in 0.001s\n\nOK (skipped=1)\n")):
            self.assertEqual(runner.classify(code, output), "inconclusive")

    def test_worker_has_a_timeout_and_isolated_interpreter(self) -> None:
        with patch("run_support_mutations.subprocess.run", return_value=PASS) as launch:
            self.assertEqual(runner._run(Path("snapshot"), ("test_x",)), PASS)
        args, kwargs = launch.call_args
        self.assertEqual(args[0][:5], [sys.executable, "-I", "-B", "-X", "utf8"])
        self.assertEqual(args[0][-1], "CheckerSupportTests.test_x")
        self.assertEqual(kwargs["timeout"], 30)
        self.assertTrue(kwargs["capture_output"])
        self.assertEqual(kwargs["encoding"], "utf-8")

    def test_denominator_retains_unrun_and_inconclusive(self) -> None:
        rows: list[dict[str, object]] = [{"outcome": value} for value in ("killed", "survived", "inconclusive", "unrun", "equivalent", "invalid")]
        result = runner.detection(rows)
        self.assertEqual(result["eligible"], 4)
        self.assertEqual(result["detected_fraction"], 0.25)
        self.assertIsNone(runner.detection([])["detected_fraction"])
        self.assertIsNone(runner.detection([{"outcome": "invalid"}])["detected_fraction"])
        invalid_rows: tuple[list[dict[str, object]], ...] = ([{}], [{"outcome": None}], [{"outcome": "timeout-killed"}])
        for rows in invalid_rows:
            with self.assertRaises(Violation):
                runner.detection(rows)

    def test_manifest_schema_and_identity_refusal(self) -> None:
        with TemporaryDirectory(prefix="mutation-test-", dir=TESTS.parents[1]) as temporary:
            path = Path(temporary) / "manifest.json"
            path.write_text(json.dumps([record()]), encoding="utf-8")
            self.assertEqual(runner.load_cases(path)[0].identity, "counter-fault")
            malformed: tuple[object, ...] = ({}, [], [record()]*257, [record(), record()],
                [dict(record(), extra=3)], [dict(record(), tests="test_x")],
                [dict(record(), before=3)], [dict(record(), tests=[3])])
            for value in malformed:
                path.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaises(Violation):
                    runner.load_cases(path)
            path.write_bytes(b" "*(1024*1024+1))
            with self.assertRaises(Violation):
                runner.load_cases(path)
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ValueError):
                runner.load_cases(path)

    def test_execution_restores_bytes_and_classifies_every_outcome(self) -> None:
        case = MutationCase("test-fault", "sample.py", "value = 1", "value = 2", ("test_x",))
        original = "value = 1\n"
        with TemporaryDirectory(prefix="mutation-test-", dir=TESTS.parents[1]) as temporary:
            snapshot = Path(temporary)
            (snapshot / "checker_support").mkdir()
            source = snapshot / "checker_support/sample.py"
            source.write_text(original, encoding="utf-8", newline="\n")
            for completed, outcome in ((PASS, "survived"), (FAIL, "killed")):
                with patch.object(runner, "_run", return_value=completed):
                    self.assertEqual(runner.execute(case, snapshot, original)["outcome"], outcome)
                self.assertEqual(source.read_bytes(), original.encode())
            for error in (subprocess.TimeoutExpired("test", 30), OSError("spawn refused")):
                with patch.object(runner, "_run", side_effect=error):
                    self.assertEqual(runner.execute(case, snapshot, original)["outcome"], "inconclusive")
                self.assertEqual(source.read_bytes(), original.encode())
            with patch.object(runner, "_run", side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    runner.execute(case, snapshot, original)
            self.assertEqual(source.read_bytes(), original.encode())
            syntax = MutationCase("invalid", "sample.py", "value = 1", "value = (", ("test_x",))
            self.assertEqual(runner.execute(syntax, snapshot, original)["outcome"], "invalid")
            self.assertEqual(runner.execute(case, snapshot, "different")["outcome"], "invalid")

    def test_campaign_baseline_and_cancellation_preserve_accounting(self) -> None:
        with TemporaryDirectory(prefix="mutation-test-", dir=TESTS.parents[1]) as temporary:
            directory = Path(temporary)
            manifest, output = directory/"manifest.json", directory/"receipt.json"
            manifest.write_text(json.dumps([record()]), encoding="utf-8")
            for baseline in (FAIL, subprocess.CompletedProcess(["test"], 0, "", "")):
                with patch.object(runner, "_run", return_value=baseline):
                    self.assertEqual(runner.campaign(manifest, output), 1)
                receipt = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(receipt["summary"]["counts"]["unrun"], 1)
            with patch.object(runner, "_run", side_effect=[PASS, KeyboardInterrupt()]):
                with self.assertRaises(KeyboardInterrupt):
                    runner.campaign(manifest, output)
            self.assertEqual(json.loads(output.read_text())["summary"]["counts"]["unrun"], 1)
            with patch.object(runner, "_run", side_effect=[PASS, FAIL]):
                self.assertEqual(runner.campaign(manifest, output), 0)
            receipt = json.loads(output.read_text())
            self.assertEqual(receipt["summary"]["counts"]["killed"], 1)
            self.assertEqual(receipt["summary"]["detected_fraction"], 1)
            self.assertTrue(receipt["input_sha256"])
            self.assertEqual(sorted(path.name for path in directory.iterdir()), ["manifest.json", "receipt.json"])

    def test_output_cannot_replace_input_and_unknown_source_refused(self) -> None:
        with TemporaryDirectory(prefix="mutation-test-", dir=TESTS.parents[1]) as temporary:
            directory = Path(temporary)
            manifest = directory/"manifest.json"
            manifest.write_text(json.dumps([record()]), encoding="utf-8")
            for output in (manifest, directory/"bad.py"):
                with self.assertRaises(Violation):
                    runner.campaign(manifest, output)
            manifest.write_text(json.dumps([dict(record(), source="absent.py")]), encoding="utf-8")
            with self.assertRaises(Violation):
                runner.campaign(manifest, directory/"receipt.json")
            manifest.write_text(json.dumps([dict(record(), tests=["test_absent"])]), encoding="utf-8")
            with self.assertRaises(Violation):
                runner.campaign(manifest, directory/"receipt.json")

    def test_atomic_receipt_failure_retains_previous_bytes(self) -> None:
        with TemporaryDirectory(prefix="mutation-test-", dir=TESTS.parents[1]) as temporary:
            output = Path(temporary)/"receipt.json"
            output.write_bytes(b"previous")
            with patch("run_support_mutations.os.replace", side_effect=OSError("rename refused")):
                with self.assertRaises(OSError):
                    runner._save(output, {"new": True})
            self.assertEqual(output.read_bytes(), b"previous")
            self.assertEqual(tuple(path.name for path in output.parent.iterdir()), ("receipt.json",))

    def test_baseline_timeout_and_cli_resource_translation(self) -> None:
        with TemporaryDirectory(prefix="mutation-test-", dir=TESTS.parents[1]) as temporary:
            directory = Path(temporary)
            manifest, output = directory/"manifest.json", directory/"receipt.json"
            manifest.write_text(json.dumps([record()]), encoding="utf-8")
            with patch.object(runner, "_run", side_effect=subprocess.TimeoutExpired("test", 30)):
                with self.assertRaises(subprocess.TimeoutExpired):
                    runner.campaign(manifest, output)
            self.assertEqual(json.loads(output.read_text())["summary"]["counts"]["unrun"], 1)
            self.assertEqual(sorted(path.name for path in directory.iterdir()), ["manifest.json", "receipt.json"])
            with patch.object(sys, "argv", ["runner", str(manifest), str(output)]):
                with patch.object(runner, "campaign", side_effect=OSError("access refused")):
                    with self.assertRaises(Violation) as caught:
                        runner.main()
            self.assertEqual(caught.exception.failure.kind, "resource")


if __name__ == "__main__":
    unittest.main(verbosity=2)
