"""Tests for ProbabilitySimplex and StochasticMap under exact rational arithmetic.
Unit, integration, and negative tests.

Origin: code/python/src/finite_probability/simplex.py
Claim: urn:omega:fqm:simplex:fractional-half:v1
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

import pytest
from fractions import Fraction
from src.finite_probability.simplex import (
    ProbabilitySimplex,
    StochasticMap,
)


def test_negative_simplex_construction_and_normalization():
    p = ProbabilitySimplex([Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)])
    assert p.dim == 3
    assert p[0] == Fraction(1, 2)
    assert p[1] == Fraction(1, 3)
    assert p[2] == Fraction(1, 6)

    u = ProbabilitySimplex.uniform(4)
    assert u.dim == 4
    for i in range(4):
        assert u[i] == Fraction(1, 4)

    d = ProbabilitySimplex.dirac(3, 1)
    assert d.probs == [Fraction(0), Fraction(1), Fraction(0)]

    with pytest.raises(ValueError):
        ProbabilitySimplex([Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)])
    with pytest.raises(ValueError):
        ProbabilitySimplex([-Fraction(1, 2), Fraction(3, 2)])


def test_unit_total_variation_distance():
    p = ProbabilitySimplex.dirac(2, 0)
    q = ProbabilitySimplex.dirac(2, 1)
    assert p.total_variation_distance(q) == Fraction(1)
    assert p.total_variation_distance(p) == Fraction(0)

    u = ProbabilitySimplex.uniform(2)
    assert p.total_variation_distance(u) == Fraction(1, 2)


def test_mixture_and_expectation():
    p = ProbabilitySimplex.dirac(2, 0)
    q = ProbabilitySimplex.dirac(2, 1)
    mix = p.mixture(q, Fraction(1, 2))
    assert mix.equals(ProbabilitySimplex.uniform(2)) if hasattr(mix, 'equals') else mix == ProbabilitySimplex.uniform(2)

    u = ProbabilitySimplex.uniform(2)
    assert u.expectation([10, 20]) == Fraction(15)


def test_stochastic_map_pushforward():
    t = StochasticMap([
        [Fraction(1, 2), Fraction(1, 2)],
        [Fraction(0), Fraction(1)],
    ])
    p = ProbabilitySimplex([Fraction(1), Fraction(0)])
    p_next = t.apply(p)
    assert p_next.probs == [Fraction(1, 2), Fraction(1, 2)]

    p2 = ProbabilitySimplex([Fraction(0), Fraction(1)])
    assert t.apply(p2) == p2


_MODULE_PATH = __import__("pathlib").Path(__file__).resolve().parents[1] / 'src' / 'finite_probability' / 'simplex.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "ProbabilitySimplex" in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.finite_probability.simplex',)
_USE_SHIM = False
_MUTANTS = (('_variation:209', '    return total / 2', '    return total / 3'),)
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
