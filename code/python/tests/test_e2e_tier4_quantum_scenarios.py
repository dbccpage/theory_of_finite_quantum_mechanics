"""Tier 4 exact scenarios: prices, towers, frames, and the trace obstruction.
Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/continuum_lift.py
Claim: trace_obstruction certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""
from fractions import Fraction

from src.qm.campaigns.continuum import trace_obstruction
from src.qm.campaigns.continuum_lift import wintner_wielandt_trace_obstruction
from src.qm.campaigns.mub_reports import overlap_gap
from src.qm.causal_prices import cycle_price_defect
from src.qm.tower_walk import tower_degree_product
from src.linear_algebra.smith_form import smith_normal_form
from src.linear_algebra.matrix import ExactMatrix


def test_unit_tier4_price_cycle_and_tower_degree():
    assert cycle_price_defect() == Fraction(0)
    assert tower_degree_product() == 8


def test_tier4_trace_obstruction_is_the_dimension():
    assert trace_obstruction() == Fraction(4)
    report = wintner_wielandt_trace_obstruction(4)
    assert report["trace_commutator"] == 0
    assert report["obstruction_holds"] is True
    assert report["trace_discrepancy"] == Fraction(4)


def test_tier4_mub_gap_and_smith_identity():
    assert overlap_gap() == Fraction(1, 2) - Fraction(16, 25)
    witness = ExactMatrix.from_rows([[2, 4], [2, 6]])
    diagonal, left, right = smith_normal_form(witness)
    assert left * witness * right == diagonal
    assert diagonal.get(0, 0) + diagonal.get(1, 1) == Fraction(4)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'continuum_lift.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'trace_obstruction' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.continuum_lift',)
_USE_SHIM = False
_MUTANTS = (('wintner_wielandt_trace_obstruction:38', '    trace = Fraction(0)', '    trace = Fraction(1)'),)
_CHILD = '\nimport importlib\nimport importlib.util\nimport json\nimport sys\nimport tempfile\nfrom pathlib import Path\n\npayload = json.loads(sys.stdin.read())\nfor root in payload["roots"]:\n    if root not in sys.path:\n        sys.path.insert(0, root)\nif payload["shim"]:\n    import tests.conftest\nprimary = payload["modules"][0]\nparent_name, _, _child_name = primary.rpartition(".")\nif parent_name and parent_name not in sys.modules:\n    importlib.import_module(parent_name)\nspec = importlib.util.spec_from_loader(primary, loader=None)\nmodule = importlib.util.module_from_spec(spec)\nmodule.__package__ = parent_name or None\nmodule.__file__ = payload["origin"]\nfor name in payload["modules"]:\n    sys.modules[name] = module\n    parent, _, child = name.rpartition(".")\n    if parent in sys.modules:\n        setattr(sys.modules[parent], child, module)\nexec(compile(payload["source"], payload["origin"], "exec"), module.__dict__)\ntest_spec = importlib.util.spec_from_file_location("certificate_probe", payload["test"])\ntest_mod = importlib.util.module_from_spec(test_spec)\ntest_spec.loader.exec_module(test_mod)\n\n\ndef _unwrap(fn):\n    wrapped = getattr(fn, "__wrapped__", None)\n    if callable(wrapped):\n        return wrapped\n    holder = getattr(fn, "__pytest_wrapped__", None)\n    obj = getattr(holder, "obj", None)\n    if callable(obj):\n        return obj\n    return fn\n\n\ndef _fixture(name):\n    if name == "tmp_path":\n        return Path(tempfile.mkdtemp())\n    fix = getattr(test_mod, name, None)\n    if not callable(fix):\n        return None\n    target = _unwrap(fix)\n    code = getattr(target, "__code__", None)\n    if code is None or code.co_argcount != 0:\n        return None\n    return target()\n\n\nran = 0\ntry:\n    for name in dir(test_mod):\n        if not name.startswith("test_"):\n            continue\n        if "mutation" in name:\n            continue\n        if name == "test_integration_origin_locks_the_source_module":\n            continue\n        fn = getattr(test_mod, name)\n        code = getattr(fn, "__code__", None)\n        if code is None:\n            continue\n        values = []\n        ready = True\n        for arg in code.co_varnames[: code.co_argcount]:\n            value = _fixture(arg)\n            if value is None:\n                ready = False\n                break\n            values.append(value)\n        if ready is False:\n            continue\n        fn(*values)\n        ran += 1\n    if ran == 0:\n        print("FAIL none")\n    else:\n        print("PASS " + str(ran))\nexcept Exception as exc:\n    print("FAIL " + type(exc).__name__)\n'

def _suite_passes(source: str) -> bool:
    payload = json.dumps({
        "modules": list(_ALIAS_NAMES),
        "source": source,
        "origin": str(_MODULE_PATH),
        "test": str(__import__("pathlib").Path(__file__).resolve()),
        "shim": _USE_SHIM,
        "roots": [str(__import__("pathlib").Path(__file__).resolve().parents[1]), str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src")],
    })
    completed = subprocess.run(
        [sys.executable, "-c", _CHILD],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = completed.stdout.strip().splitlines()
    status = lines[-1] if lines else ""
    return status.startswith("PASS")

def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    if _suite_passes(source) is False:
        raise AssertionError("baseline suite failed")
    killed = 0
    for name, old, new in _MUTANTS:
        if source.count(old) != 1:
            raise AssertionError(name)
        if _suite_passes(source.replace(old, new, 1)) is not False:
            raise AssertionError(name)
        killed += 1
    if killed != len(_MUTANTS):
        raise AssertionError(str(killed))
    record = f"Mutation-Kills: {killed} non-equivalent"
    if record not in __import__('pathlib').Path(__file__).read_text(encoding="utf-8"):
        raise AssertionError(record)
