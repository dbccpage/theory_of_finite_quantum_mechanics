"""Tests for the FusionRing and FusionTable Python dual-implementation.
Unit, integration, and negative tests.

Origin: code/python/src/fusion_categories/fusion_ring.py
Claim: urn:omega:fqm:fusion:exact-ring-control:v1
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

import pytest
from src.fusion_categories.fusion_ring import (
    AbelianGroup,
    FusionTable,
    FusionRing,
    RingDefectType,
    ising_global_dimension_rational,
)


def test_negative_abelian_group_properties():
    grp = AbelianGroup([2, 3])
    assert grp.order == 6
    assert grp.moduli == [2, 3]

    for lbl in range(6):
        digits = grp.digits(lbl)
        assert grp.label(digits) == lbl

    assert grp.add(0, 5) == 5
    assert grp.add(1, 1) == grp.label([0, 0])
    for a in range(6):
        neg = grp.negate(a)
        assert grp.add(a, neg) == 0

    with pytest.raises(ValueError):
        AbelianGroup([1])
    with pytest.raises(ValueError):
        grp.digits(6)


def test_unit_ising_fusion_ring():
    ising = FusionRing.ising()
    assert ising.rank == 3
    assert ising.names == ["1", "sigma", "psi"]

    assert ising.dual(0) == 0
    assert ising.dual(1) == 1
    assert ising.dual(2) == 2

    assert ising.n(1, 1, 0) == 1
    assert ising.n(1, 1, 1) == 0
    assert ising.n(1, 1, 2) == 1

    assert ising.n(1, 2, 1) == 1

    assert ising.n(2, 2, 0) == 1

    assert ising.fusion_path_count(0, [1], 1) == 1
    assert ising.fusion_path_count(0, [1, 1], 0) == 1
    assert ising.fusion_path_count(0, [1, 1], 2) == 1
    assert ising_global_dimension_rational() == 4


def test_fibonacci_fusion_ring():
    fib = FusionRing.fibonacci()
    assert fib.rank == 2
    assert fib.names == ["1", "tau"]

    assert fib.n(1, 1, 0) == 1
    assert fib.n(1, 1, 1) == 1


def test_toric_code_ring():
    toric = FusionRing.toric_code()
    assert toric.rank == 4
    assert toric.dual(0) == 0
    assert toric.n(0, 1, 1) == 1


def test_rep_s3_ring():
    s3 = FusionRing.rep_s3()
    assert s3.rank == 3
    assert s3.dual(0) == 0
    assert s3.n(0, 1, 1) == 1


def test_defect_detection():
    mutated = [
        [[0, 0], [0, 1]],
        [[0, 1], [1, 1]],
    ]
    t = FusionTable.from_3d(mutated)
    defect = t.first_defect()
    assert defect is not None
    assert defect.defect_type == RingDefectType.UNIT


_MODULE_PATH = __import__("pathlib").Path(__file__).resolve().parents[1] / 'src' / 'fusion_categories' / 'fusion_ring.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'AbelianGroup' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.fusion_categories.fusion_ring',)
_USE_SHIM = False
_MUTANTS = (('_rational:138', '    return QuadraticRational(Fraction(value), Fraction(0), disc)', '    return QuadraticRational(Fraction(value), Fraction(1), disc)'),)
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
