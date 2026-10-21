"""Exact tests for the QM-209 finite map: context parity and Weyl commutator holonomy.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/context_parity.py
Claim: context_parity_control certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

import pytest
from finite_qm.use_cases import context_parity_control as cpc

N = 12


@pytest.fixture(scope="module")
def control() -> dict:
    return cpc.evaluate_context_parity_control(conductor=N)


def test_unit_peres_mermin_cokernel_is_the_total_parity(control: dict) -> None:
    pm = control["peres_mermin"]
    assert pm["all_contexts_commute"]
    assert pm["context_signs"] == [1, 1, 1, 1, 1, -1]
    assert pm["sign_product"] == -1
    assert pm["incidence_rank_f2"] == 5
    assert pm["cokernel_dimension"] == 1
    assert pm["every_observable_in_two_contexts"]
    assert pm["assignment_exists"] is False
    assert pm["obstruction_class_total_parity"] == 1
    assert pm["even_control_assignment_exists"]
    assert pm["even_control_solution_checks"]


def test_flipping_one_context_sign_removes_the_obstruction(control: dict) -> None:
    pm = control["peres_mermin"]
    rows = [[1 if o in ctx else 0 for o in pm["observables"]] for ctx in pm["contexts"]]
    rhs = [1 if s == -1 else 0 for s in pm["context_signs"]]
    assert cpc.f2_eliminate(rows, rhs)["consistent"] is False
    flipped = list(rhs)
    flipped[0] ^= 1
    solved = cpc.f2_eliminate(rows, flipped)
    assert solved["consistent"] is True
    assert cpc.f2_apply(rows, solved["solution"]) == flipped


def test_negative_f2_elimination_on_a_small_system() -> None:
    rows = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    odd = cpc.f2_eliminate(rows, [1, 1, 1])
    assert odd["rank"] == 2 and odd["consistent"] is False
    even = cpc.f2_eliminate(rows, [1, 1, 0])
    assert even["consistent"] is True
    assert cpc.f2_apply(rows, even["solution"]) == [1, 1, 0]
    with pytest.raises(cpc.ContextControlRefusal):
        cpc.f2_eliminate([[2, 0]], [0])


def test_weyl_commutator_holonomy_table(control: dict) -> None:
    census = control["weyl_census"]
    assert census[3]["holonomy_exponents_mod_conductor"] == [[0, 0, 0], [0, 8, 4], [0, 4, 8]]
    assert census[4]["holonomy_exponents_mod_conductor"] == [
        [0, 0, 0, 0],
        [0, 9, 6, 3],
        [0, 6, 0, 6],
        [0, 3, 6, 9],
    ]
    for d in (3, 4):
        assert census[d]["dimension"] == d
        assert census[d]["trivial_exactly_when_d_divides_ab"]
        assert census[d]["values_are_dth_roots"]


def test_holonomy_is_conjugation_invariant_and_diagonal_frames_give_none(control: dict) -> None:
    inv = control["conjugation_invariance"]
    assert inv["base_holonomy_exponent"] == 9
    assert inv["invariant_under"] == {"fourier": True, "diagonal_phases": True}
    assert inv["diagonal_pair_has_trivial_holonomy"]
    assert inv["commuting_powers_have_trivial_holonomy"]


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "IMPORTED", "IMPORTED"]
    assert "second context" in ledger[2]["statement"]


def test_refuses_conductor_without_mu12() -> None:
    with pytest.raises(cpc.ContextControlRefusal):
        cpc.evaluate_context_parity_control(conductor=10)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'context_parity.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'context_parity_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.context_parity', 'finite_qm.use_cases.context_parity', 'src.qm.campaigns.context_parity_control', 'finite_qm.use_cases.context_parity_control')
_USE_SHIM = True
_MUTANTS = (('context_sign:77', '        return 1', '        return 2'),)
_CHILD = '\nimport importlib\nimport importlib.util\nimport json\nimport sys\nimport tempfile\nfrom pathlib import Path\n\npayload = json.loads(sys.stdin.read())\nfor root in payload["roots"]:\n    if root not in sys.path:\n        sys.path.insert(0, root)\nif payload["shim"]:\n    import tests.conftest\nprimary = payload["modules"][0]\nreal = importlib.import_module(primary)\nspec = importlib.util.spec_from_loader(primary, loader=None)\nmodule = importlib.util.module_from_spec(spec)\nmodule.__package__ = real.__package__\nmodule.__file__ = payload["origin"]\nif hasattr(real, "__path__"):\n    module.__path__ = list(real.__path__)\nfor name in payload["modules"]:\n    sys.modules[name] = module\n    parent, _, child = name.rpartition(".")\n    if parent in sys.modules:\n        setattr(sys.modules[parent], child, module)\nexec(compile(payload["source"], payload["origin"], "exec"), module.__dict__)\ntest_spec = importlib.util.spec_from_file_location("certificate_probe", payload["test"])\ntest_mod = importlib.util.module_from_spec(test_spec)\ntest_spec.loader.exec_module(test_mod)\n\n\ndef _unwrap(fn):\n    wrapped = getattr(fn, "__wrapped__", None)\n    if callable(wrapped):\n        return wrapped\n    holder = getattr(fn, "__pytest_wrapped__", None)\n    obj = getattr(holder, "obj", None)\n    if callable(obj):\n        return obj\n    return fn\n\n\ndef _fixture(name):\n    if name == "tmp_path":\n        return Path(tempfile.mkdtemp())\n    fix = getattr(test_mod, name, None)\n    if not callable(fix):\n        return None\n    target = _unwrap(fix)\n    code = getattr(target, "__code__", None)\n    if code is None or code.co_argcount != 0:\n        return None\n    return target()\n\n\nran = 0\ntry:\n    for name in dir(test_mod):\n        if not name.startswith("test_"):\n            continue\n        if "mutation" in name:\n            continue\n        if name == "test_integration_origin_locks_the_source_module":\n            continue\n        fn = getattr(test_mod, name)\n        code = getattr(fn, "__code__", None)\n        if code is None:\n            continue\n        values = []\n        ready = True\n        for arg in code.co_varnames[: code.co_argcount]:\n            value = _fixture(arg)\n            if value is None:\n                ready = False\n                break\n            values.append(value)\n        if ready is False:\n            continue\n        fn(*values)\n        ran += 1\n    if ran == 0:\n        print("FAIL none")\n    else:\n        print("PASS " + str(ran))\nexcept Exception as exc:\n    print("FAIL " + type(exc).__name__)\n'

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
