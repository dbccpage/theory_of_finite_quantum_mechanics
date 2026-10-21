"""Snapshot structural observations; no source metric awards a capability grade."""
import ast
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path

import lizard
from radon.visitors import ComplexityVisitor

ROOT = Path(__file__).resolve().parents[4]
SUBJECT = "code/python/src/finite_probability/simplex.py"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def controls(node, depth=0):
    """Conservative nesting-weighted count for this file's simple AST subset.

    This is an upper bound, not a claim of Sonar implementation conformance.
    Boolean groups each add one. Every compound control (including with/try)
    and every comprehension clause adds 1+depth. Nested function bodies are
    separately reviewed and forbidden by this measurement's input preflight.
    """
    compound = isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With,
                                ast.IfExp, ast.comprehension, ast.ExceptHandler))
    increment = 1 + depth if compound else int(isinstance(node, ast.BoolOp))
    maximum = depth + int(compound)
    for child in ast.iter_child_nodes(node):
        score, nesting = controls(child, depth + int(compound))
        increment += score
        maximum = max(maximum, nesting)
    return increment, maximum


def main():
    raw = (ROOT / SUBJECT).read_bytes()
    tree = ast.parse(raw)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    unsupported = [type(node).__name__ for node in ast.walk(tree)
        if isinstance(node, (ast.AsyncFunctionDef, ast.Lambda, ast.Match, ast.AsyncFor, ast.AsyncWith, ast.Yield, ast.YieldFrom))]
    for function in functions:
        if any(isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) for statement in function.body for child in ast.walk(statement)):
            unsupported.append("nested function")
    if unsupported:
        raise ValueError("Unsupported syntax: " + repr(unsupported))
    visitor = ComplexityVisitor.from_code(raw.decode())
    radon_rows = [{"name": f.name, "line": f.lineno, "ccn": f.complexity}
                  for f in [*visitor.functions, *[m for c in visitor.classes for m in c.methods]]]
    lizard_rows = [{"name": f.name, "line": f.start_line, "ccn": f.cyclomatic_complexity}
                   for f in lizard.analyze_file.analyze_source_code(SUBJECT, raw.decode()).function_list]
    structural = []
    for function in functions:
        rows = [controls(statement) for statement in function.body]
        structural.append({"name": function.name, "line": function.lineno,
            "weighted_control_upper_bound": sum(value for value, _ in rows),
            "control_nesting": max((nesting for _, nesting in rows), default=0)})
    # Calibration examples distinguish sequential and nested control structure.
    fixtures = {"sequential": ("if x:\n pass\nif y:\n pass", 2, 1),
                "nested": ("if x:\n if y:\n  pass", 3, 2),
                "boolean": ("if x and y:\n pass", 2, 1)}
    calibration = {}
    for name, (text, expected_score, expected_depth) in fixtures.items():
        rows = [controls(statement) for statement in ast.parse(text).body]
        observed = (sum(v for v, _ in rows), max(n for _, n in rows))
        assert observed == (expected_score, expected_depth)
        calibration[name] = {"source": text, "score": observed[0], "nesting": observed[1]}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/expanded_scope" / (stamp + "-simplex-metrics")
    output.mkdir(parents=True)
    (output / "source.py").write_bytes(raw)
    runner = Path(__file__).read_bytes()
    (output / "runner.py").write_bytes(runner)
    receipt = {"AuthorityEffect": "None", "subject": SUBJECT, "source_sha256": sha(raw),
        "runner_sha256": sha(runner), "versions": {n: importlib.metadata.version(n) for n in ["radon", "lizard"]},
        "radon": radon_rows, "lizard": lizard_rows, "structural_upper_bound": structural,
        "calibration": calibration, "unsupported_syntax": unsupported,
        "scope": "Source control structure only; no formal runtime bound, memory measurement or engineering grade inferred.",
        "source_unchanged": sha((ROOT / SUBJECT).read_bytes()) == sha(raw)}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": output.relative_to(ROOT).as_posix(),
        "max_ccn_radon": max(row["ccn"] for row in radon_rows),
        "max_ccn_lizard": max(row["ccn"] for row in lizard_rows),
        "max_weighted_control_upper_bound": max(row["weighted_control_upper_bound"] for row in structural),
        "max_control_nesting": max(row["control_nesting"] for row in structural)}))


if __name__ == "__main__":
    main()
