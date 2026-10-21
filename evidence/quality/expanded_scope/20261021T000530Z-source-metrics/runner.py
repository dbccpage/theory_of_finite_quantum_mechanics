"""Apply the calibrated structural observer to explicit Python source paths."""
import ast
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

import lizard
from radon.visitors import ComplexityVisitor
from measure_simplex import controls

ROOT = Path(__file__).resolve().parents[4]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    output = ROOT / "evidence/quality/expanded_scope" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-source-metrics")
    output.mkdir(parents=True)
    paths = [ROOT / name for name in sys.argv[1:]]
    rows = {}
    for path in paths:
        name = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        tree = ast.parse(raw)
        unsupported = [type(node).__name__ for node in ast.walk(tree)
            if isinstance(node, (ast.AsyncFunctionDef, ast.Match, ast.AsyncFor, ast.AsyncWith, ast.TryStar, ast.Yield, ast.YieldFrom))]
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        for function in functions:
            if any(isinstance(child, ast.FunctionDef) for statement in function.body for child in ast.walk(statement)):
                unsupported.append("nested function")
        visitor = ComplexityVisitor.from_code(raw.decode())
        ccn_radon = [{"name": f.name, "line": f.lineno, "ccn": f.complexity}
                     for f in [*visitor.functions, *[m for c in visitor.classes for m in c.methods]]]
        ccn_lizard = [{"name": f.name, "line": f.start_line, "ccn": f.cyclomatic_complexity}
                     for f in lizard.analyze_file.analyze_source_code(name, raw.decode()).function_list]
        structural = []
        for function in functions:
            measured = [controls(statement) for statement in function.body]
            structural.append({"name": function.name, "line": function.lineno,
                "weighted_control_upper_bound": sum(value for value, _ in measured),
                "control_nesting": max((nesting for _, nesting in measured), default=0)})
        snapshot = output / "sources" / name
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(raw)
        rows[name] = {"source_sha256": sha(raw), "unsupported_syntax": unsupported,
            "radon": ccn_radon, "lizard": ccn_lizard, "structural": structural,
            "maxima": {"radon_ccn": max((r["ccn"] for r in ccn_radon), default=None),
                "lizard_ccn": max((r["ccn"] for r in ccn_lizard), default=None),
                "weighted_control_upper_bound": max((r["weighted_control_upper_bound"] for r in structural), default=None),
                "control_nesting": max((r["control_nesting"] for r in structural), default=None)},
            "unchanged": sha(path.read_bytes()) == sha(raw)}
    runner = Path(__file__).read_bytes()
    helper = Path(__file__).with_name("measure_simplex.py").read_bytes()
    (output / "runner.py").write_bytes(runner)
    (output / "observer.py").write_bytes(helper)
    receipt = {"AuthorityEffect": "None", "sources": rows, "runner_sha256": sha(runner),
        "observer_sha256": sha(helper), "versions": {n: importlib.metadata.version(n) for n in ["radon", "lizard"]},
        "scope": "Source structure only. Conservative weighted-control count is not Sonar conformance or a runtime/grade measurement. Lambdas are included in their surrounding AST, not separately certified.",
        "calibration": "Observer fixtures: sequential if -> (2,1), nested if -> (3,2), boolean if -> (2,1).",
        "status": "PASS" if all(r["unchanged"] and not r["unsupported_syntax"] for r in rows.values()) else "REVIEW_UNSUPPORTED_OR_DRIFT"}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": output.relative_to(ROOT).as_posix(), "status": receipt["status"],
                      "maxima": {name: r["maxima"] for name, r in rows.items()}}, indent=2))


if __name__ == "__main__":
    main()
