"""Apply one mutation per law to a copy of ``code/`` and require the suite to fail.

Each mutation disables exactly one step, control or letter law. The unchanged
suite must pass first. Only a test failure with a valid JUnit report counts as
a kill; collection and runner errors abort the audit. A mutation that leaves
the suite green means that law is untested. Run from anywhere:

    python scripts/mutation_audit.py

Exit 0 when every mutation is killed. AuthorityEffect: None.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

PACKAGE = Path(__file__).resolve().parents[1]

# (law, file under code/, exact source text, replacement)
MUTATIONS = (
    (
        "Measurement requires admission gate",
        "oe_prime_algorithms.py",
        '        if not admitted:\n            raise PermissionError("MEASUREMENT_REFUSED_UNADMITTED_PACKET")\n',
        "        if False:\n            raise PermissionError(\"MEASUREMENT_REFUSED_UNADMITTED_PACKET\")\n",
    ),
    (
        "Measurement admitted defaults to False",
        "oe_prime_algorithms.py",
        "        admitted: bool = False,\n",
        "        admitted: bool = True,\n",
    ),
    (
        "CanContinue requires obligation",
        "oe_prime_algorithms.py",
        "        return (\n            self.has_obligation\n",
        "        return (\n            True\n",
    ),
    (
        "CanContinue requires witness",
        "oe_prime_algorithms.py",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and True\n",
    ),
    (
        "CanContinue requires next carrier declared",
        "oe_prime_algorithms.py",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and True\n",
    ),
    (
        "CanContinue requires adapter sound",
        "oe_prime_algorithms.py",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and True\n",
    ),
    (
        "CanContinue requires detector adequate",
        "oe_prime_algorithms.py",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n            and self.detector_adequate\n",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n            and True\n",
    ),
    (
        "CanContinue requires minimal lift",
        "oe_prime_algorithms.py",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n            and self.detector_adequate\n            and self.minimal_lift\n",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n            and self.detector_adequate\n            and True\n",
    ),
    (
        "CanContinue requires skeleton preserved",
        "oe_prime_algorithms.py",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n            and self.detector_adequate\n            and self.minimal_lift\n            and self.skeleton_preserved\n",
        "    def evaluate(self) -> bool:\n        \"\"\"Evaluate the canonical nine-conjunct continuation condition.\"\"\"\n        return (\n            self.has_obligation\n            and self.has_witness\n            and self.next_carrier_declared\n            and self.adapter_sound\n            and self.detector_adequate\n            and self.minimal_lift\n            and True\n",
    ),
    (
        "CanContinue requires budget remains",
        "oe_prime_algorithms.py",
        "            and self.skeleton_preserved\n            and self.budget_remains\n",
        "            and self.skeleton_preserved\n            and True\n",
    ),
    (
        "CanContinue requires not GTLA refusal",
        "oe_prime_algorithms.py",
        "            and self.budget_remains\n            and self.not_gtla_refusal\n",
        "            and self.budget_remains\n            and True\n",
    ),
    (
        "Declaration order requires grounding hash",
        "oe_prime_algorithms.py",
        "        if not self.step0_grounding_hash:\n",
        "        if False:\n",
    ),
    (
        "Declaration order requires valid carrier",
        "oe_prime_algorithms.py",
        "        if not self.step1_carrier or not self.step1_carrier.vertices or not self.step1_carrier.validate():\n",
        "        if False:\n",
    ),
    (
        "Declaration order requires observer",
        "oe_prime_algorithms.py",
        "        if not self.step2_observer or not self.step2_observer.observer_id:\n",
        "        if False:\n",
    ),
    (
        "Declaration order requires witness certificate",
        "oe_prime_algorithms.py",
        "        if not self.step5_witness_certificate:\n",
        "        if False:\n",
    ),
    (
        "Intake evaluation refuses missing carrier",
        "oe_prime_algorithms.py",
        "        if not packet.carrier_proposal:\n",
        "        if False:\n",
    ),
    (
        "Intake evaluation refuses missing witness",
        "oe_prime_algorithms.py",
        "        if not packet.witness_available:\n",
        "        if False:\n",
    ),
    (
        "Terminalization requires zero residual",
        "oe_prime_algorithms.py",
        "        if phi == 0 and gamma == 0 and detector_adequate:\n",
        "        if detector_adequate:\n",
    ),
    (
        "Terminalization refuses blind observer",
        "oe_prime_algorithms.py",
        '        if not detector_adequate:\n            return False, "REFUSED_BLIND_OBSERVER"\n',
        '        if False:\n            return False, "REFUSED_BLIND_OBSERVER"\n',
    ),
    (
        "Merkle tape verifies entry hash mismatch",
        "oe_prime_algorithms.py",
        '        if entry["hash"] != expected_hash:\n',
        "        if False:\n",
    ),
)


@dataclass(frozen=True)
class SuiteResult:
    returncode: int
    tests: int
    failures: int
    errors: int
    output: str

    def classification(self) -> str:
        if self.tests > 0 and self.errors == 0:
            if self.returncode == 0 and self.failures == 0:
                return "PASS"
            if self.returncode == 1 and self.failures > 0:
                return "KILLED"
        return "ERROR"


def run_suite(root: Path) -> SuiteResult:
    report = root / "mutation-results.xml"
    report.unlink(missing_ok=True)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-x",
            "-p",
            "no:cacheprovider",
            f"--junitxml={report}",
            str(root / "code" / "test_oe_prime_algorithms.py"),
        ],
        cwd=root,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    try:
        suites = list(ET.parse(report).getroot().iter("testsuite"))
        tests = sum(int(suite.get("tests", "0")) for suite in suites)
        failures = sum(int(suite.get("failures", "0")) for suite in suites)
        errors = sum(int(suite.get("errors", "0")) for suite in suites)
    except (OSError, ET.ParseError, ValueError) as error:
        return SuiteResult(result.returncode, 0, 0, 1, output + f"\nInvalid test report: {error}")
    return SuiteResult(result.returncode, tests, failures, errors, output)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        shutil.copytree(PACKAGE / "code", root / "code", ignore=shutil.ignore_patterns("__pycache__"))
        baseline = run_suite(root)
    if baseline.classification() != "PASS":
        print("ERROR: unchanged suite must pass before mutation detection can be assessed")
        print(baseline.output[-2000:])
        return 2
    print(f"BASELINE: {baseline.tests} tests passed")
    survivors = []
    for law, filename, old, new in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(PACKAGE / "code", root / "code", ignore=shutil.ignore_patterns("__pycache__"))
            target = root / "code" / filename
            text = target.read_text(encoding="utf-8")
            if text.count(old) != 1:
                print(f"ANCHOR  {law}: expected one match in {filename}, found {text.count(old)}")
                return 2
            target.write_text(text.replace(old, new), encoding="utf-8")
            result = run_suite(root)
            status = result.classification()
        if status == "ERROR":
            print(f"ERROR   {law}: runner or test-report failure")
            print(result.output[-2000:])
            return 2
        killed = status == "KILLED"
        print(f"{'KILLED ' if killed else 'SURVIVED'} {law}")
        if not killed:
            survivors.append(law)
    print(f"{len(MUTATIONS) - len(survivors)}/{len(MUTATIONS)} mutations killed")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
