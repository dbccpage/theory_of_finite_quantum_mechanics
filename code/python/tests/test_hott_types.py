"""Tests for HoTT shape types: Path, ContractibleType, HigherInductiveType.
Unit, integration, and negative tests.

Origin: code/python/src/homotopy_type_theory/hott_types.py
Claim: urn:omega:fqm:hott:circle-step-witness:v1
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

import pytest
from src.homotopy_type_theory.hott_types import (
    Path,
    ContractibleType,
    PointConstructor,
    PathConstructor,
    HigherInductiveType,
    MissingReferenceError,
    InvalidHITError,
)


def test_negative_path_validation():
    p = Path(type_id="A", source="x", target="y", path_ref="p_xy")
    p.validate()

    bad_p = Path(type_id="", source="x", target="y", path_ref="p")
    with pytest.raises(MissingReferenceError):
        bad_p.validate()


def test_contractible_type():
    c = ContractibleType(type_ref="Unit", center_ref="tt", contraction_ref="contr_unit")
    c.validate()

    bad_c = ContractibleType(type_ref="Unit", center_ref="", contraction_ref="contr")
    with pytest.raises(MissingReferenceError):
        bad_c.validate()


def test_unit_circle_s1_hit():
    s1 = HigherInductiveType.circle_s1()
    assert s1.type_name == "S^1"
    assert len(s1.points) == 1
    assert s1.points[0].name == "base"
    assert len(s1.paths) == 1
    assert s1.paths[0].name == "loop"
    assert s1.paths[0].source_point == "base"
    assert s1.paths[0].target_point == "base"


def test_interval_i_hit():
    interval = HigherInductiveType.interval_i()
    assert interval.type_name == "Interval"
    assert len(interval.points) == 2
    assert len(interval.paths) == 1
    assert interval.paths[0].name == "seg"


def test_torus_t2_hit():
    t2 = HigherInductiveType.torus_t2()
    assert t2.type_name == "T^2"
    assert len(t2.points) == 1
    assert len(t2.paths) == 2


def test_invalid_hit_raises():
    bad_hit = HigherInductiveType(
        type_name="Broken",
        points=[PointConstructor("x")],
        paths=[PathConstructor("p", "x", "non_existent_point")],
    )
    with pytest.raises(InvalidHITError):
        bad_hit.validate()


_MODULE_PATH = __import__("pathlib").Path(__file__).resolve().parents[1] / 'src' / 'homotopy_type_theory' / 'hott_types.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'Path' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.homotopy_type_theory.hott_types',)
_USE_SHIM = False
_MUTANTS = (('torus_t2:143', '            "T^2",', '            "T^3",'),)
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
