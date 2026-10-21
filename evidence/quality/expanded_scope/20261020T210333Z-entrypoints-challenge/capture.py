"""Run a source-pinned finite API challenge with explicit mutant outcomes.

No failed build, child crash or timeout is counted as a killed mutant.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
SUBJECT = "code/python/src/finite_probability/simplex.py"
TESTS = ["code/python/tests/test_simplex_lifecycle.py", "code/python/tests/test_expanded_exact_admission.py"]
MUTANTS = [
    ("overriding fraction admitted", "if type(value) is Fraction:", "if isinstance(value, Fraction):"),
    ("hostile sequence admitted", "if type(values) not in (list, tuple):", "if False and type(values) not in (list, tuple):"),
    ("input bit refusal disabled", '_bound_bits(value.numerator, limit, role)', 'pass  # numerator bit refusal disabled'),
    ("dimension refusal disabled", "if number > MAX_DIMENSION:", "if False and number > MAX_DIMENSION:"),
    ("matrix entry refusal disabled", "if len(rows) * width > MAX_MATRIX_ENTRIES:", "if False and len(rows) * width > MAX_MATRIX_ENTRIES:"),
    ("negative indexing misrouted", "return self._probs[slot]", "return self._probs[0]"),
    ("variation scaled incorrectly", "return total / 2", "return total / 3"),
    ("mixture coefficients swapped", "gap = Fraction(1) - share", "gap = share"),
    ("expectation signs flipped", 'total += mass * _require_fraction', 'total -= mass * _require_fraction'),
    ("pushforward term dropped", 'total += source[row] * data[row][column]', 'total = source[row] * data[row][column]'),
    ("reinitialization admitted", 'if hasattr(self, "_probs"):', 'if False and hasattr(self, "_probs"):'),
    ("label refusal disabled", "if len(label) > MAX_LABEL_LENGTH:", "if False and len(label) > MAX_LABEL_LENGTH:"),
    ("work bit check disabled", 'if value.bit_length() > limit:', 'if False and value.bit_length() > limit:'),
    ("public equality inverted", 'return self._probs == other._probs', 'return self._probs != other._probs'),
]
CHILD = r'''
import json, pathlib, sys, types
root, source, temp, *tests = sys.argv[1:]
sys.path.insert(0, str(pathlib.Path(root) / "code/python"))
import src.finite_probability as parent
name = "src.finite_probability.simplex"
module = types.ModuleType(name)
module.__file__ = source
module.__package__ = "src.finite_probability"
sys.modules[name] = module
parent.simplex = module
try:
    exec(compile(pathlib.Path(source).read_bytes(), source, "exec"), module.__dict__)
except Exception as error:
    print(json.dumps({"phase": "load", "error": type(error).__name__, "detail": str(error)}))
    sys.exit(3)
import pytest
result = pytest.main([*tests, "-q", "--basetemp", temp, "-p", "no:cacheprovider"])
print(json.dumps({"phase": "pytest", "exit_code": int(result)}))
sys.exit(result)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(source, work, tag):
    candidate = work / (tag + ".py")
    candidate.write_bytes(source)
    command = [sys.executable, "-B", "-c", CHILD, str(ROOT), str(candidate),
               str(ROOT / ".pytest_cache/expanded-candidates" / work.name / tag), *TESTS]
    try:
        compile(source, str(candidate), "exec")
    except (SyntaxError, ValueError) as error:
        return {"status": "INVALID", "reason": str(error), "source_sha256": sha(candidate)}
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired as error:
        (work / (tag + ".log")).write_bytes((error.stdout or b"") + (error.stderr or b""))
        return {"status": "INCONCLUSIVE", "reason": "60 second child timeout", "source_sha256": sha(candidate)}
    log = work / (tag + ".log")
    log.write_text(process.stdout + process.stderr, encoding="utf-8")
    try:
        last = json.loads(process.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        last = {}
    status = ("SURVIVED" if process.returncode == 0 and last == {"phase": "pytest", "exit_code": 0}
              else "KILLED" if process.returncode == 1 and last == {"phase": "pytest", "exit_code": 1}
              else "INVALID" if last.get("phase") == "load"
              else "INCONCLUSIVE")
    return {"status": status, "exit_code": process.returncode, "last_status": last,
            "source_sha256": sha(candidate), "log_sha256": sha(log)}


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    work = ROOT / "evidence/quality/expanded_scope" / (stamp + "-simplex-challenge")
    work.mkdir(parents=True)
    (work / "runner.py").write_bytes(Path(__file__).read_bytes())
    (work / "child.py").write_text(CHILD, encoding="utf-8")
    inputs = [SUBJECT, *TESTS, "SCORING.md", "code/python/tests/conftest.py",
              "code/python/src/bin/__init__.py", "code/python/src/bin/entropy_cli.py",
              "code/python/src/finite_probability/__init__.py"]
    pins = {p: sha(ROOT / p) for p in inputs}
    for name in inputs:
        target = work / "inputs" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())
    receipt = {"AuthorityEffect": "None", "inputs": pins, "python": sys.version,
        "pytest_version": importlib.metadata.version("pytest"), "runner_sha256": sha(Path(__file__)),
        "scope": "Finite simplex API, scalar rejection, immutable lifecycle and engineering resource policies. No Lean proof or whole-program certification.",
        "unbound_inputs": "Other modules imported by test conftest, pytest transitive code and host OS are trusted, not fully snapshotted.",
        "mutants": []}
    source = (ROOT / SUBJECT).read_bytes()
    baseline = execute(source, work, "baseline")
    receipt["baseline"] = {**baseline, "status": "PASS" if baseline["status"] == "SURVIVED" else "FAILED_OR_INCONCLUSIVE"}
    if baseline["status"] == "SURVIVED":
        text = source.decode("utf-8")
        for index, (name, old, new) in enumerate(MUTANTS):
            if text.count(old) != 1:
                result = {"status": "INVALID", "reason": "mutation site not unique", "matches": text.count(old)}
            else:
                result = execute(text.replace(old, new, 1).encode(), work, f"mutant-{index:02d}")
            receipt["mutants"].append({"name": name, **result})
            print(json.dumps(receipt["mutants"][-1]), flush=True)
    else:
        receipt["mutants"] = [{"name": name, "status": "UNRUN", "reason": "baseline did not pass"} for name, _, _ in MUTANTS]
    counts = Counter(row["status"] for row in receipt["mutants"])
    receipt["outcomes"] = dict(counts)
    eligible = sum(counts[k] for k in ["KILLED", "SURVIVED", "INCONCLUSIVE", "UNRUN"])
    receipt["detection_fraction"] = {"numerator": counts["KILLED"], "denominator": eligible} if eligible else None
    receipt["inputs_unchanged"] = all(sha(ROOT / name) == value for name, value in pins.items())
    receipt["status"] = ("FAILED_OR_INCONCLUSIVE" if receipt["baseline"]["status"] != "PASS" or not receipt["inputs_unchanged"]
        else "SURVIVORS" if counts["SURVIVED"] else "INCONCLUSIVE_OR_UNRUN" if counts["INCONCLUSIVE"] or counts["UNRUN"]
        else "PASS" if counts["KILLED"] == len(MUTANTS) else "REVIEW_INVALID_OR_EQUIVALENT")
    (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": work.relative_to(ROOT).as_posix(), "status": receipt["status"], "outcomes": dict(counts)}), flush=True)


if __name__ == "__main__":
    main()
