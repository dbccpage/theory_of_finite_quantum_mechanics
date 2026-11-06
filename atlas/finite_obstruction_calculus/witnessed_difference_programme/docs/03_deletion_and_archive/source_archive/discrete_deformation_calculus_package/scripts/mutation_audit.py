"""Apply one mutation per law to a copy of ``code/`` and require the suite to fail.

Each mutation disables exactly one step, control or letter law. A mutation that
leaves the suite green means that law is untested. Run from anywhere:

    python scripts/mutation_audit.py

Exit 0 when every mutation is killed. AuthorityEffect: None.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

PACKAGE = Path(__file__).resolve().parents[1]

# (law, file under code/ddc, exact source text, replacement)
MUTATIONS = (
    ("E requires an exact class", "automaton.py", "        if before.cls != EXACT:\n", "        if False:\n"),
    ("E discharges the residual", "automaton.py", "        if after.phi != 0 or after.gamma != 0:\n", "        if False:\n"),
    ("R keeps Phi1", "automaton.py", "        if after.phi != before.phi:\n", "        if False:\n"),
    ("R keeps Gamma2", "automaton.py", "        if after.gamma != before.gamma:\n", "        if False:\n"),
    ("C is monotone (Law 8)", "automaton.py", "        if after.phi < before.phi or after.gamma < before.gamma:\n", "        if False:\n"),
    ("I needs a receipt (Law 5)", "automaton.py", "        if not witness.receipt:\n", "        if False:\n"),
    ("Λ needs a licence", "automaton.py", "        if not witness.lift_licence:\n", "        if False:\n"),
    ("Λ needs a trigger (Law 4)", "automaton.py", "        if not (before.cls == CLOSED or not before.adequate):\n", "        if False:\n"),
    ("D needs a loss ledger (Law 6)", "automaton.py", "        if not witness.loss_ledger:\n", "        if False:\n"),
    ("M needs a reason", "automaton.py", "        if witness.reason not in M_REASONS:\n", "        if False:\n"),
    ("T refuses Gamma2 > 0", "automaton.py", "        if after.gamma != 0:\n            v.append(\"TerminalizedOpenResidual\")\n        if not before.adequate:\n", "        if False:\n            v.append(\"TerminalizedOpenResidual\")\n        if not before.adequate:\n"),
    ("T is absorbing (Law 2)", "automaton.py", "    if control == TERMINALIZED:\n        return \"TerminalAbsorbing\"\n", "    if False:\n        return \"TerminalAbsorbing\"\n"),
    ("M is absorbing (Law 3)", "automaton.py", "    if control == REFUSED and letter not in (\"C\", \"Λ\", \"T\"):\n", "    if False:\n"),
    ("E refuses a non-exact defect", "exact_repair.py", "                    elif potential[nxt] != nxt_val:\n", "                    elif False:\n"),
    ("I chains the previous head", "integration_tape.py", "            if entry.index != i or entry.prev_hash != expected_prev:\n", "            if entry.index != i:\n"),
    ("Intake refusals stay off the tape", "typed_refusal.py", "                enters_ddc_trace=False,\n", "                enters_ddc_trace=True,\n"),
    ("T never seals an open obstruction", "terminalization.py", "        if closure_defect > 0:\n", "        if False:\n"),
    ("Phi1 takes the minimum over forests", "cochain.py", "        if best is None or value < best:\n", "        if best is None or value > best:\n"),
)


TESTS = {
    "automaton.py": "test_automaton.py",
    "exact_repair.py": "test_exact_repair.py",
    "integration_tape.py": "test_letter_modules.py",
    "typed_refusal.py": "test_letter_modules.py",
    "terminalization.py": "test_letter_modules.py",
    "cochain.py": "test_cochain.py",
}


def run_test(root: Path, filename: str) -> tuple[int, set[str], bool]:
    report = root / "pytest-result.xml"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
         f"--junitxml={report}", str(root / "code/tests" / filename)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
    )
    if not report.is_file():
        return result.returncode, set(), True
    tree = ET.parse(report)
    failures = {case.attrib["name"] for case in tree.findall(".//testcase")
                if any("AssertionError" in failure.attrib.get("message", "")
                       or "assert " in (failure.text or "") for failure in case.findall("failure"))}
    harness_error = bool(tree.findall(".//error")) or result.returncode not in (0, 1)
    return result.returncode, failures, harness_error


def main() -> int:
    survivors = []
    evidence = []
    with tempfile.TemporaryDirectory(prefix="ddc-mutation-baseline-") as tmp:
        baseline = Path(tmp)
        shutil.copytree(PACKAGE / "code", baseline / "code", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(PACKAGE / "pyproject.toml", baseline / "pyproject.toml")
        for test in sorted(set(TESTS.values())):
            code, _, error = run_test(baseline, test)
            if code or error:
                print(f"HARNESS FAILURE: baseline {test}")
                return 2
    for law, filename, old, new in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(PACKAGE / "code", root / "code", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(PACKAGE / "pyproject.toml", root / "pyproject.toml")
            target = root / "code" / "ddc" / filename
            text = target.read_text(encoding="utf-8")
            if text.count(old) != 1:
                print(f"ANCHOR  {law}: expected one match in {filename}")
                return 2
            target.write_text(text.replace(old, new), encoding="utf-8")
            code, failures, error = run_test(root, TESTS[filename])
            if error or (code == 1 and not failures):
                print(f"HARNESS FAILURE: {law}")
                return 2
            killed = code == 1 and bool(failures)
            evidence.append({"law": law, "test_file": TESTS[filename], "exit_code": code,
                             "assertion_failures": sorted(failures), "killed": killed})
        print(f"{'KILLED ' if killed else 'SURVIVED'} {law}")
        if not killed:
            survivors.append(law)
    print(f"{len(MUTATIONS) - len(survivors)}/{len(MUTATIONS)} mutations killed")
    print(json.dumps(evidence, ensure_ascii=False))
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
