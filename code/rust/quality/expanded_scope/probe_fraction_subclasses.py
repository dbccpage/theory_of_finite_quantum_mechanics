"""Reproduce exact-path subclass leakage; binary floats are negative fixtures."""
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import fractions

ROOT = Path(__file__).resolve().parents[4]
CASES = [
    ("code/python/src/finite_probability/simplex.py", "expectation"),
    ("code/python/src/bin/__init__.py", "ray"),
    ("code/python/src/bin/entropy_cli.py", "collision"),
]


class LeakingFraction(Fraction):
    def __mul__(self, other):
        return 0.5


def run(output, source_root=ROOT):
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (name, operation) in enumerate(CASES):
        source = source_root / name
        original = source.read_bytes()
        snapshot = output / "sources" / name
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(original)
        spec = importlib.util.spec_from_file_location("expanded_probe_" + str(index), snapshot)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        row = {"source": name, "executed_source": str(source), "sha256": hashlib.sha256(original).hexdigest(),
               "operation": operation, "expected_exact_value": "1",
               "input": "Fraction subclass whose __mul__ returns binary float 0.5",
               "profile": "Exact", "rule": "SCORING.md G2: unadmitted float in exact path"}
        try:
            if operation == "expectation":
                value = module.ProbabilitySimplex([LeakingFraction(1)]).expectation([1])
            elif operation == "ray":
                value = module.ray_power_two((LeakingFraction(1), 0, 0))
            else:
                value = module.collision_probability((LeakingFraction(1),))
            row.update(status="RETURNED", actual_type=type(value).__name__, actual_repr=repr(value),
                       exact_invariant_violated=type(value) is not Fraction or value != 1)
        except Exception as error:
            row.update(status="REFUSED", exception_type=type(error).__name__, error=str(error),
                       exact_invariant_violated=False)
        row["source_unchanged"] = source.read_bytes() == original
        rows.append(row)
    runner = Path(__file__).read_bytes()
    (output / "probe.py").write_bytes(runner)
    receipt = {"AuthorityEffect": "None", "cases": rows,
               "python": sys.version, "source_root": str(source_root),
               "runner_sha256": hashlib.sha256(runner).hexdigest(),
               "fractions_module": {"path": fractions.__file__,
                   "sha256": hashlib.sha256(Path(fractions.__file__).read_bytes()).hexdigest()},
               "scope": "Three adversarial public-input probes only; no global exactness or capability certification."}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output")
    parser.add_argument("--source-root", default=str(ROOT))
    args = parser.parse_args()
    run(ROOT / args.output, (ROOT / args.source_root).resolve())
