"""Source-pinned entrypoint challenges; six-outcome accounting uses check_simplex.

Each candidate is imported in its package position. The CLI module exit is also
exercised in a fresh interpreter, so a live-source subprocess cannot hide a mutant.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import check_simplex as capture

ROOT = Path(__file__).resolve().parents[4]
SPECS = {
    "src.bin": {"source": "code/python/src/bin/__init__.py", "old_tests": "code/python/tests/test_bin_witness.py", "mutants": [
        ("overriding Fraction admitted", "if type(value) is Fraction:", "if isinstance(value, Fraction):"),
        ("container callback admitted", "if type(amplitudes) is not tuple:", "if False and type(amplitudes) is not tuple:"),
        ("scalar budget removed", "if value.bit_length() > MAX_SCALAR_BITS:", "if False and value.bit_length() > MAX_SCALAR_BITS:"),
        ("arity changed", "len(amplitudes) != 3", "len(amplitudes) != 4"),
        ("square replaced by addition", "return value * value", "return value + value"),
        ("last amplitude sign flipped", "_square(x_pos) + _square(y_pos) + _square(z_pos)", "_square(x_pos) + _square(y_pos) - _square(z_pos)"),
        ("fourth constant changed", "_FOURTH = Fraction(337, 625)", "_FOURTH = Fraction(337, 626)"),
        ("closed stdout unhandled", "except (OSError, ValueError):", "except ArithmeticError:"),
    ]},
    "src.bin.entropy_cli": {"source": "code/python/src/bin/entropy_cli.py", "old_tests": "code/python/tests/test_entropy_cli.py", "mutants": [
        ("overriding Fraction admitted", "if type(value) is Fraction:", "if isinstance(value, Fraction):"),
        ("container callback admitted", "if type(weights) is not tuple:", "if False and type(weights) is not tuple:"),
        ("vector budget removed", "if len(weights) > MAX_OUTCOMES:", "if False and len(weights) > MAX_OUTCOMES:"),
        ("scalar budget removed", "if value.bit_length() > limit:", "if False and value.bit_length() > limit:"),
        ("mass accumulator budget removed", '_require_fraction_bits(total, MAX_WORK_BITS, "mass sum")', 'pass  # missing mass work guard'),
        ("collision accumulator budget removed", '_require_fraction_bits(total, MAX_WORK_BITS, "collision sum")', 'pass  # missing collision work guard'),
        ("negative mass admitted", "if weight < 0:", "if weight < -1:"),
        ("unit mass check inverted", "if total != 1:", "if total == 1:"),
        ("squares omitted", "total += weight * weight", "total += weight"),
        ("closed stdout unhandled", "except (OSError, ValueError):", "except ArithmeticError:"),
    ]},
    "src.finite_probability": {"source": "code/python/src/finite_probability/__init__.py", "old_tests": "code/python/tests/test_scaled_simplex.py", "mutants": [
        ("container callback admitted", "if type(weights) is not tuple:", "if False and type(weights) is not tuple:"),
        ("integer subclass admitted", "if type(value) is int:", "if isinstance(value, int):"),
        ("weight budget removed", "if value.bit_length() > MAX_WEIGHT_BITS:", "if False and value.bit_length() > MAX_WEIGHT_BITS:"),
        ("signed sum changed", "return pair[0] + pair[1]", "return pair[0] - pair[1]"),
        ("pair arity changed", "len(entries) != 2", "len(entries) != 3"),
        ("point witness changed", "_POINT: tuple[int, int] = (1, 0)", "_POINT: tuple[int, int] = (0, 0)"),
        ("closed stdout unhandled", "except (OSError, ValueError):", "except ArithmeticError:"),
    ]},
    "src.bin.finite_cli": {"source": "code/python/src/bin/finite_cli.py", "old_tests": "code/python/tests/test_finite_cli.py", "mutants": [
        ("integer size subclass admitted", "if type(value) is int:", "if isinstance(value, int):"),
        ("dimension budget removed", "if size > MAX_IDENTITY_DIMENSION:", "if False and size > MAX_IDENTITY_DIMENSION:"),
        ("diagonal Fraction subclass admitted", "if type(entry) is Fraction:", "if isinstance(entry, Fraction):"),
        ("trace dimension shifted", "expected = Fraction(size)", "expected = Fraction(size + 1)"),
        ("provider error unwrapped", "except MatrixError as error:", "except ArithmeticError as error:"),
        ("argument container callback admitted", "if type(argv) not in (list, tuple):", "if not isinstance(argv, (list, tuple)):"),
        ("argument count budget removed", "if len(argv) > MAX_ARGUMENTS:", "if False and len(argv) > MAX_ARGUMENTS:"),
        ("argument length budget removed", "if len(argument) > MAX_ARGUMENT_CHARACTERS:", "if False and len(argument) > MAX_ARGUMENT_CHARACTERS:"),
        ("argument string callback admitted", "if type(argument) is not str:", "if not isinstance(argument, str):"),
        ("argument ownership lost", "return result\n\n\ndef main", "return argv\n\n\ndef main"),
        ("return status unchecked", "return result if type(result) is int and result in (0, 1, 2) else 2", "return result"),
        ("module exit status discarded", "raise SystemExit(main())", "main()"),
    ]},
}
CHILD = r'''
import importlib,json,pathlib,sys,types
root, source, temp, *tests = sys.argv[1:]
sys.path.insert(0,str(pathlib.Path(root)/"code/python"))
for value in PRELOAD_MODULES:
    if not value.rsplit(".",1)[-1].startswith("test_"):
        importlib.import_module(value)
name = TARGET_MODULE
old=importlib.import_module(name)
module=types.ModuleType(name)
module.__file__=str(pathlib.Path(root)/TARGET_SOURCE)
module.__package__=old.__package__
if hasattr(old,"__path__"):
    module.__path__=list(old.__path__)
    for child_name,child in list(sys.modules.items()):
        parent,_,leaf=child_name.rpartition(".")
        if parent==name:
            setattr(module,leaf,child)
sys.modules[name]=module
parent,_,leaf=name.rpartition(".")
setattr(sys.modules[parent],leaf,module)
try:
    exec(compile(pathlib.Path(source).read_bytes(),source,"exec"),module.__dict__)
except Exception as error:
    print(json.dumps({"phase":"load","error":type(error).__name__,"detail":str(error)}));sys.exit(3)
import pytest
class CandidateBindings:
    def pytest_collection_modifyitems(self,session,config,items):
        checked=set()
        for item in items:
            for value in vars(item.module).values():
                if isinstance(value,(types.FunctionType,type)) and getattr(value,"__module__",None)==name:
                    symbol=value.__name__
                    if getattr(module,symbol,None) is not value:
                        raise RuntimeError("STALE_CANDIDATE_BINDING:"+name+":"+symbol)
                    checked.add(symbol)
        print(json.dumps({"phase":"candidate_bindings","checked_symbols":sorted(checked)}))
result=pytest.main([*tests,"-q","-k","not mutation","--basetemp",temp,"-p","no:cacheprovider"],plugins=[CandidateBindings()])
print(json.dumps({"phase":"pytest","exit_code":int(result)}));sys.exit(result)
'''
EXIT_PROBE = r'''
from pathlib import Path
import sys
source,root=sys.argv[1:]
sys.path.insert(0,str(Path(root)/"code/python"))
sys.argv=[source,"evidence","check","--project-root",root]
exec(compile(Path(source).read_bytes(),source,"exec"),{"__name__":"__main__","__package__":"src.bin","__file__":source})
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_exit_probe(candidate, work, tag):
    try:
        result = subprocess.run([sys.executable, "-B", "-c", EXIT_PROBE, str(candidate), str(ROOT)],
                                cwd=ROOT, text=True, capture_output=True, timeout=30)
    except subprocess.TimeoutExpired:
        return {"status": "INCONCLUSIVE", "reason": "module exit probe timeout"}
    log = work / (tag + "-module-exit.log")
    log.write_text(json.dumps({"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}, indent=2) + "\n", encoding="utf-8")
    correct_message = result.stderr.strip() == "SOURCE_MANIFEST_REQUIRED"
    status = "SURVIVED" if correct_message and result.returncode == 2 else "KILLED" if correct_message and result.returncode == 0 else "INCONCLUSIVE"
    return {"status": status, "exit_code": result.returncode, "log_sha256": sha(log)}


def main(specifications=None, test_file="code/python/tests/test_bounded_entrypoints.py", suite="entrypoints"):
    definitions = SPECS if specifications is None else specifications
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    work = ROOT / "evidence/quality/expanded_scope" / (stamp + "-" + suite + "-challenge")
    work.mkdir(parents=True)
    (work / "runner.py").write_bytes(Path(__file__).read_bytes())
    (work / "capture.py").write_bytes(Path(capture.__file__).read_bytes())
    (work / "configuration.json").write_text(json.dumps({"suite": suite, "test_file": test_file, "definitions": definitions}, indent=2) + "\n", encoding="utf-8")
    inputs = {"SCORING.md", "code/python/tests/conftest.py", test_file,
              "code/python/src/linear_algebra/matrix.py", "code/python/src/linear_algebra/scalars.py", "code/python/src/qm/cli.py", "code/python/src/qm/api.py"}
    for spec in definitions.values():
        inputs.update([spec["source"], spec["old_tests"]])
    pins = {name: sha(ROOT / name) for name in sorted(inputs)}
    for name in pins:
        target = work / "inputs" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())
    receipt = {"AuthorityEffect": "None", "python": sys.version, "inputs": pins,
        "runner_sha256": sha(Path(__file__)), "capture_sha256": sha(Path(capture.__file__)),
        "configuration_sha256": sha(work / "configuration.json"),
        "scope": suite + ": explicitly named modules and finite API/checker behavior only; no delegated suite certification, Lean proof, numerical benchmark or OS sandbox guarantee.",
        "unbound_inputs": "Other conftest imports, default suite/claim data, native extension availability, transitive pytest/stdlib sources and OS remain trusted host inputs.", "files": {}}
    for module, definition in definitions.items():
        folder = work / module.replace(".", "_")
        folder.mkdir()
        capture.CHILD = CHILD.replace("TARGET_MODULE", repr(module)).replace("PRELOAD_MODULES", repr(list(definitions))).replace("TARGET_SOURCE", repr(definition["source"]))
        capture.TESTS = list(dict.fromkeys([test_file, definition["old_tests"]]))
        source = (ROOT / definition["source"]).read_bytes()
        baseline = capture.execute(source, folder, "baseline")
        baseline_exit = direct_exit_probe(folder / "baseline.py", folder, "baseline") if module.endswith("finite_cli") else None
        passed = baseline["status"] == "SURVIVED" and (baseline_exit is None or baseline_exit["status"] == "SURVIVED")
        result = {"source": definition["source"], "source_sha256": pins[definition["source"]],
                  "baseline": baseline, "baseline_module_exit": baseline_exit, "baseline_passed": passed, "mutants": []}
        for index, (name, old, new) in enumerate(definition["mutants"]):
            text = source.decode()
            tag = f"mutant-{index:02d}"
            if not passed:
                outcome = {"status": "UNRUN", "reason": "baseline did not pass"}
            elif text.count(old) != 1:
                outcome = {"status": "INVALID", "reason": "mutation site not unique", "matches": text.count(old)}
            else:
                outcome = capture.execute(text.replace(old, new, 1).encode(), folder, tag)
                if module.endswith("finite_cli") and outcome["status"] == "SURVIVED":
                    probe = direct_exit_probe(folder / (tag + ".py"), folder, tag)
                    outcome["module_exit_probe"] = probe
                    outcome["status"] = probe["status"]
            result["mutants"].append({"name": name, **outcome})
            print(json.dumps({"module": module, "name": name, "status": outcome["status"]}), flush=True)
        counts = Counter(row["status"] for row in result["mutants"])
        result["outcomes"] = dict(counts)
        result["eligible"] = sum(counts[k] for k in ["KILLED", "SURVIVED", "INCONCLUSIVE", "UNRUN"])
        result["detection_fraction"] = {"numerator": counts["KILLED"], "denominator": result["eligible"]} if result["eligible"] else None
        result["status"] = "PASS" if passed and counts["KILLED"] == len(definition["mutants"]) else "REVIEW_OUTCOMES"
        receipt["files"][module] = result
    receipt["inputs_unchanged"] = all(sha(ROOT / name) == value for name, value in pins.items())
    receipt["status"] = "PASS" if receipt["inputs_unchanged"] and all(item["status"] == "PASS" for item in receipt["files"].values()) else "REVIEW_OUTCOMES"
    (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": work.relative_to(ROOT).as_posix(), "status": receipt["status"],
                      "outcomes": {m: value["outcomes"] for m, value in receipt["files"].items()}}), flush=True)


if __name__ == "__main__":
    main()
