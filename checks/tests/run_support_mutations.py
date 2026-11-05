"""Replay an explicit, source-bound mutation campaign without editing live sources.

AuthorityEffect: None. Each subprocess is time bounded; temporary snapshots are
disposed by a context manager. Cancellation propagates after retaining unrun
records. Timeout and harness failure are inconclusive, never counted as kills.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import cast

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.mutation_case import MutationCase
from checker_support.boundary import Violation

CHECKS = Path(__file__).resolve().parents[1]
OUTCOMES = ("killed", "survived", "equivalent", "invalid", "inconclusive", "unrun")


def load_cases(path: Path) -> tuple[MutationCase, ...]:
    if path.stat().st_size > 1024*1024:
        raise Violation("resource", "mutation manifest exceeds 1 MiB")
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list) or not 1 <= len(raw) <= 256:
        raise Violation("input", "manifest must contain 1..256 mutation cases")
    cases = tuple(_case(item) for item in raw)
    if len({case.identity for case in cases}) != len(cases):
        raise Violation("duplicate", "mutation identities must be unique")
    return cases


def _case(value: object) -> MutationCase:
    if not isinstance(value, dict) or set(value) != {"identity", "source", "before", "after", "tests"}:
        raise Violation("input", "mutation record fields differ from its schema")
    text_fields = [value[key] for key in ("identity", "source", "before", "after")]
    if any(type(text) is not str for text in text_fields) or type(value["tests"]) is not list:
        raise Violation("input", "mutation text fields and test list have wrong types")
    return MutationCase(*cast(tuple[str, str, str, str], tuple(text_fields)), tuple(value["tests"]))


def classify(returncode: int, output: str) -> str:
    if re.search(r"(?m)^Ran [1-9][0-9]* tests? in [0-9.]+s$", output) is None:
        return "inconclusive"
    if returncode == 0 and output.rstrip().endswith("\nOK"):
        return "survived"
    if returncode == 1 and "\nFAILED (" in output:
        return "killed"
    return "inconclusive"


def detection(records: list[dict[str, object]]) -> dict[str, object]:
    if any(type(row) is not dict or type(row.get("outcome")) is not str for row in records):
        raise Violation("input", "each mutation record must identify its outcome")
    counts = Counter(str(row["outcome"]) for row in records)
    if set(counts) - set(OUTCOMES):
        raise Violation("input", "unknown mutation outcome")
    eligible = sum(counts[key] for key in ("killed", "survived", "inconclusive", "unrun"))
    return {"counts": {key: counts[key] for key in OUTCOMES},
            "eligible": eligible,
            "detected_fraction": counts["killed"]/eligible if eligible else None}


def _run(snapshot: Path, tests: tuple[str, ...] = ()) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-I", "-B", "-X", "utf8",
               str(snapshot / "tests/test_checker_support.py")]
    command.extend("CheckerSupportTests." + test for test in tests)
    return subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=30)


def execute(case: MutationCase, snapshot: Path, original: str) -> dict[str, object]:
    record: dict[str, object] = {"identity": case.identity, "source": case.source,
                               "tests": list(case.tests), "outcome": "unrun"}
    try:
        changed = case.apply(original)
        compile(changed, case.source, "exec")
    except (SyntaxError, Violation) as error:
        return {**record, "outcome": "invalid", "reason": str(error)}
    destination = snapshot / "checker_support" / case.source
    try:
        destination.write_text(changed, encoding="utf-8", newline="\n")
        run = _run(snapshot, case.tests)
        output = run.stdout + run.stderr
        return {**record, "outcome": classify(run.returncode, output),
                "returncode": run.returncode, "output": output[-12000:]}
    except subprocess.TimeoutExpired:
        return {**record, "outcome": "inconclusive", "reason": "30-second test timeout"}
    except OSError as error:
        return {**record, "outcome": "inconclusive", "reason": str(error)}
    finally:
        destination.write_text(original, encoding="utf-8", newline="\n")


def _save(path: Path, receipt: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # A sibling temporary file makes replacement atomic on the same filesystem.
    with TemporaryDirectory(prefix="mutation-receipt-", dir=path.parent) as temporary:
        staging = Path(temporary) / "receipt.json"
        staging.write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n", encoding="utf-8", newline="\n")
        os.replace(staging, path)


def _test_names() -> set[str]:
    tree = ast.parse((CHECKS / "tests/test_checker_support.py").read_text(encoding="utf-8"))
    return {method.name for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "CheckerSupportTests"
            for method in node.body if isinstance(method, ast.FunctionDef)}


def _validate_population(cases: tuple[MutationCase, ...], originals: dict[str, str]) -> None:
    if any(case.source not in originals for case in cases):
        raise Violation("input", "mutation references a source outside checker_support")
    names = _test_names()
    if any(test not in names for case in cases for test in case.tests):
        raise Violation("input", "mutation names a test method absent from the baseline suite")


def campaign(manifest: Path, output: Path) -> int:
    cases = load_cases(manifest)
    source_paths = tuple(sorted((CHECKS / "checker_support").glob("*.py")))
    originals = {path.name: path.read_text(encoding="utf-8") for path in source_paths}
    _validate_population(cases, originals)
    inputs = source_paths + (CHECKS / "tests/test_checker_support.py", Path(__file__), manifest)
    if output.suffix != ".json" or output.resolve() in {path.resolve() for path in inputs}:
        raise Violation("input", "receipt must be a separate JSON output, never an input artifact")
    output.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = [{"identity": case.identity, "source": case.source,
                                       "tests": list(case.tests), "outcome": "unrun"} for case in cases]
    receipt: dict[str, object] = {"AuthorityEffect": "None", "python": sys.version,
        "input_sha256": {str(path.relative_to(CHECKS.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in inputs}, "baseline": "unrun", "mutants": records}
    try:
        with TemporaryDirectory(prefix="tfqm-mutations-", dir=output.parent) as temporary:
            snapshot = Path(temporary)
            shutil.copytree(CHECKS / "checker_support", snapshot / "checker_support",
                            ignore=shutil.ignore_patterns("__pycache__", "*.yaml", "*.md"))
            (snapshot / "tests").mkdir()
            shutil.copy2(CHECKS / "tests/test_checker_support.py", snapshot / "tests/test_checker_support.py")
            baseline = _run(snapshot)
            receipt["baseline"] = {"returncode": baseline.returncode, "output": baseline.stdout+baseline.stderr}
            if classify(baseline.returncode, baseline.stdout+baseline.stderr) != "survived":
                return 1
            for index, case in enumerate(cases):
                records[index] = execute(case, snapshot, originals[case.source])
                receipt["summary"] = detection(records)
                _save(output, receipt)
                print(f"{index+1}/{len(cases)} {case.identity}: {records[index]['outcome']}", flush=True)
    finally:
        receipt["summary"] = detection(records)
        _save(output, receipt)
    return 0 if all(row["outcome"] == "killed" for row in records) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        return campaign(args.manifest.resolve(), args.output.resolve())
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Violation("resource", str(error)) from error


if __name__ == "__main__":
    raise SystemExit(cli(main))
