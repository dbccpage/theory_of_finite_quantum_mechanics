"""Regression checks for the three-role gate's structure and three semantic faults.

This replaces the ad-hoc metric/mutation entrypoints. Mutants execute in memory;
the real source is never overwritten. It is a selected regression campaign, not
an exhaustive AST mutation benchmark.
"""
from __future__ import annotations
import ast
import copy
import sys
import io
import unittest
from pathlib import Path
from types import ModuleType
import pytest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "code/python/src/wdp/three_role_gate.py"


def packet() -> dict:
    return {
        "claim_id": "test-claim", "scope": "test-scope",
        "proposer": {"identifier": "p", "principal": "alice"},
        "evaluator": {"identifier": "e", "principal": "bob"},
        "authorizer": {"identifier": "a", "principal": "carol"},
        "observer": {key: "declared" for key in ("kernel", "admissibility", "norm", "terminal", "layer")},
        "authority_root": "test-root", "policy": "pairwise_distinct",
    }


def load(source: str, name: str, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    module = ModuleType(name)
    module.__file__ = str(SOURCE)
    monkeypatch.setitem(sys.modules, name, module)
    exec(compile(source, str(SOURCE), "exec"), module.__dict__)
    return module


FAULTS = [
    ("if packet.scope != self._scope:", "if False:", "scope"),
    ("if packet.authority_root not in self._admitted_roots:", "if False:", "root"),
    ("if any(a.identifier != b.identifier and a.principal == b.principal for a, b in pairs):", "if False:", "principal"),
]


@pytest.mark.parametrize("old,new,boundary", FAULTS)
def test_gate_rejects_each_designated_semantic_fault(old: str, new: str, boundary: str,
                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert source.count(old) == 1, "mutation target changed; re-review the selected fault"
    candidate = copy.deepcopy(packet())
    if boundary == "scope":
        candidate["scope"] = "unrelated-scope"
    elif boundary == "root":
        candidate["authority_root"] = "unadmitted-root"
    else:
        candidate["evaluator"]["principal"] = "alice"
    original = load(source, "original_gate_" + boundary, monkeypatch)
    mutant = load(source.replace(old, new), "mutant_gate_" + boundary, monkeypatch)
    good = original.ThreeRoleGate("test-scope", frozenset({"test-root"}))
    bad = mutant.ThreeRoleGate("test-scope", frozenset({"test-root"}))
    assert good.evaluate_mapping(packet()).admitted
    assert good.evaluate_mapping(candidate).code.value == "REJECTED"
    # The same independently specified rejection oracle fails for the valid mutant.
    assert bad.evaluate_mapping(candidate).admitted
    assert bad.evaluate_mapping(candidate).authority_effect == "None"
    monkeypatch.syspath_prepend(str(ROOT / "code/python"))
    monkeypatch.setitem(sys.modules, "src.wdp.three_role_gate", mutant)
    tests = load((ROOT / "code/python/tests/test_three_role_gate.py").read_text(encoding="utf-8"),
                 "mutant_suite_" + boundary, monkeypatch)
    tests.FIXTURE = ROOT / "code/python/src/wdp/three_role_provenance_fixtures.json"
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
    assert result.testsRun == 15
    assert result.failures and not result.errors, stream.getvalue()
    print(boundary, "KILLED", "tests", result.testsRun, "failures", len(result.failures))


def test_gate_function_size_budget() -> None:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    functions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    assert functions
    for function in functions:
        assert function.end_lineno is not None
        assert function.end_lineno - function.lineno + 1 <= 60, function.name

