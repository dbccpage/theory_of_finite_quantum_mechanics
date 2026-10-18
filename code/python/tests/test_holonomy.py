"""Tests for discrete cell complexes, connections, and holonomy.
Unit, integration, and negative tests.

Origin: code/python/src/holonomy/holonomy_engine.py
Claim: urn:omega:fqm:holonomy:coboundary-cycle-zero:v1
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

import pytest
from fractions import Fraction
from src.holonomy.holonomy_engine import (
    CellComplex,
    RationalMatrix,
    DiscreteConnection,
)


def test_unit_cell_complex_euler_characteristic():
    cc = CellComplex()
    v0 = cc.add_vertex("A")
    v1 = cc.add_vertex("B")
    v2 = cc.add_vertex("C")
    assert len(cc.vertices) == 3

    e0 = cc.add_edge("A", "B")
    e1 = cc.add_edge("B", "C")
    e2 = cc.add_edge("C", "A")
    assert len(cc.edges) == 3

    f0 = cc.add_face("F0", ["A", "B", "C"])
    assert len(cc.faces) == 1
    assert cc.euler_characteristic == 1


def test_rational_matrix_inverse():
    m = RationalMatrix.from_ints([[2, 1], [1, 1]])
    inv = m.inverse()
    prod = m.multiply(inv)
    id2 = RationalMatrix.identity(2)
    assert prod.equals(id2)
    assert m.trace() == Fraction(3)


def test_discrete_connection_edge_inversion():
    conn = DiscreteConnection(dim=2)
    u_ab = RationalMatrix.from_ints([[1, 2], [0, 1]])
    conn.set_connection("A", "B", u_ab)

    assert conn.get_step("A", "B").equals(u_ab)
    u_ba = conn.get_step("B", "A")
    assert u_ab.multiply(u_ba).equals(RationalMatrix.identity(2))


def test_flat_and_curved_holonomy():
    cc = CellComplex()
    cc.add_vertex("A")
    cc.add_vertex("B")
    cc.add_vertex("C")
    cc.add_edge("A", "B")
    cc.add_edge("B", "C")
    cc.add_edge("C", "A")
    cc.add_face("triangle", ["A", "B", "C"])

    conn_flat = DiscreteConnection(dim=2)
    id2 = RationalMatrix.identity(2)
    conn_flat.set_connection("A", "B", id2)
    conn_flat.set_connection("B", "C", id2)
    conn_flat.set_connection("C", "A", id2)
    assert conn_flat.is_flat(cc)
    assert conn_flat.face_holonomy(cc.faces[0]).equals(id2)

    conn_curved = DiscreteConnection(dim=2)
    m1 = RationalMatrix.from_ints([[1, 1], [0, 1]])
    m2 = RationalMatrix.from_ints([[1, 0], [1, 1]])
    m3 = RationalMatrix.identity(2)
    conn_curved.set_connection("A", "B", m1)
    conn_curved.set_connection("B", "C", m2)
    conn_curved.set_connection("C", "A", m3)
    assert not conn_curved.is_flat(cc)
    holo = conn_curved.face_holonomy(cc.faces[0])
    assert not holo.equals(id2)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'holonomy' / 'holonomy_engine.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'CellComplex' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.holonomy.holonomy_engine',)
_USE_SHIM = False
_MUTANTS = (('is_flat:386', '                return False', '                return True'),)
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
