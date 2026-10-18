"""Tests for Gaussian rational amplitude bridge, holonomy, and gauge invariance.
Unit, integration, and negative tests.

Origin: code/python/src/wdp/amplitude_bridge.py
Claim: urn:omega:fqm:amplitude:parallelogram-bridge:v1
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from fractions import Fraction
from src.wdp.amplitude_bridge import (
    GaussianRational,
    U_PHASE,
    u_pow,
    u_power_is_never_one,
    OrientedGraph,
    readout_quadratic,
    readout_quartic,
    AUTHORITY_FENCE,
)


def test_unit_phase_modulus():
    assert U_PHASE.norm_sq() == Fraction(1)
    assert U_PHASE.re == Fraction(3, 5)
    assert U_PHASE.im == Fraction(4, 5)

    u2 = u_pow(2)
    assert u2.re == Fraction(-7, 25)
    assert u2.im == Fraction(24, 25)
    assert u2.norm_sq() == Fraction(1)


def test_u_power_never_one():
    assert u_power_is_never_one(1) is True
    assert u_power_is_never_one(100) is True
    for n in range(1, 10):
        un = u_pow(n)
        assert not (un.re == Fraction(1) and un.im == Fraction(0))


def test_cycle_holonomy_and_gauge_invariance():
    g = OrientedGraph()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.add_edge("C", "A", -1)

    triangle_cycle = [("A", "B"), ("B", "C"), ("C", "A")]
    hol_orig = g.cycle_holonomy(triangle_cycle)

    assert hol_orig == u_pow(2)

    f = {"A": 3, "B": -2, "C": 5}
    g_gauged = g.gauge_transform(f)

    hol_gauged = g_gauged.cycle_holonomy(triangle_cycle)
    assert hol_gauged == hol_orig


def test_readouts():
    z1 = GaussianRational.from_integers(1, 0)
    z2 = GaussianRational.from_integers(0, 1)

    quad = readout_quadratic(z1, z2)
    assert quad == Fraction(2)

    quart = readout_quartic(z1, z2)
    assert quart == Fraction(4)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'wdp' / 'amplitude_bridge.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'GaussianRational' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.wdp.amplitude_bridge',)
_USE_SHIM = False
_MUTANTS = (('u_pow:121', '    if power == 0:', '    if power == 1:'),)
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
