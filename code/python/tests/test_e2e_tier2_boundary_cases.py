"""Tier 2 exact boundary cases: constant sections, cocycles, and grid error.
Unit, integration, and negative tests.

Origin: code/python/src/qm/domain/primitive_difference.py
Claim: PrimitiveDifference certificate locked by exact checks in this file
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""
from fractions import Fraction

from src.qm.campaigns.continuum_lift import cyclotomic_density_approximation
from src.qm.campaigns.rungs import exact_cocycle_defect, triangle_boundary_rank
from src.qm.domain.primitive_difference import (
    PrimitiveDifference,
    evaluate_mu1_tied_classes,
)


def test_unit_tier2_constant_section_has_zero_defect():
    section = {"v0": Fraction(42), "v1": Fraction(42), "v2": Fraction(42)}
    edges = [("v0", "v1"), ("v1", "v2"), ("v2", "v0")]
    assert PrimitiveDifference.phi_raw(section, edges) == Fraction(0)
    assert PrimitiveDifference.support(section, edges) == 0


def test_tier2_integer_constant_section_matches_rational_zero():
    section = {"v0": Fraction(42), "v1": Fraction(42), "v2": Fraction(42)}
    edges = [("v0", "v1"), ("v1", "v2"), ("v2", "v0")]
    assert PrimitiveDifference.phi_raw(section, edges) == Fraction(0)


def test_tier2_cocycle_defect_and_triangle_rank():
    assert exact_cocycle_defect(Fraction(1, 2), Fraction(2, 3), Fraction(5, 7)) == 0
    assert triangle_boundary_rank() == 2


def test_tier2_separation_classes_are_enumerated():
    assert evaluate_mu1_tied_classes(2, max_arity=1) == 1
    assert evaluate_mu1_tied_classes(2, max_arity=2) == 3
    assert evaluate_mu1_tied_classes(5, max_arity=2) == 5


def test_tier2_gaussian_grid_squared_error_is_inside_the_bound():
    report = cyclotomic_density_approximation(0, grid_resolution=7)
    assert report["error_sq"] <= report["bound_sq"]
    assert isinstance(report["error_sq"], Fraction)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'domain' / 'primitive_difference.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'PrimitiveDifference' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.domain.primitive_difference',)
_USE_SHIM = False
_MUTANTS = (('evaluate_mu1_tied_classes:226', '    if max_arity < 1:', '    if max_arity < 2:'),)
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
