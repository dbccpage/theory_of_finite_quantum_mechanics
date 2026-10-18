"""Exact tests for the QM-211 finite map: finite spectral theorem and clock towers.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/clock_tower_control.py
Claim: clock_tower_control certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

import pytest
from finite_qm.use_cases import clock_tower_control as ctc
from finite_qm.use_cases import holonomy_bridge_control as hbc

N = 24


@pytest.fixture(scope="module")
def control() -> dict:
    return ctc.evaluate_clock_tower_control(conductor=N)


def test_finite_spectral_theorem_on_three_clocks(control: dict) -> None:
    spectral = control["spectral"]
    assert spectral["fourier_d4"]["order"] == 4
    assert spectral["fourier_d4"]["multiplicities"] == [2, 1, 1, 0]
    assert spectral["shift_d4"]["multiplicities"] == [1, 1, 1, 1]
    assert spectral["clock_d3"]["order"] == 3
    assert spectral["clock_d3"]["multiplicities"] == [1, 1, 1]
    for row in spectral.values():
        assert row["projectors_sum_to_identity"]
        assert row["projectors_orthogonal_idempotent"]
        assert row["discrete_steps_u_to_t_match_for_all_t"]
        assert row["multiplicities_sum_to_dimension"]
        assert row["hermitian_exponent_vector_is_class_mod_m"]


def test_square_roots_count_two_to_the_occupied_eigenspaces(control: dict) -> None:
    roots = control["square_roots"]
    assert (
        roots["fourier_d4"]["occupied_eigenspaces"],
        roots["fourier_d4"]["square_root_count"],
    ) == (3, 8)
    assert (roots["shift_d4"]["occupied_eigenspaces"], roots["shift_d4"]["square_root_count"]) == (
        4,
        16,
    )
    assert (roots["clock_d3"]["occupied_eigenspaces"], roots["clock_d3"]["square_root_count"]) == (
        3,
        8,
    )
    for row in roots.values():
        assert row["count_is_two_to_occupied"]
        assert row["all_square_to_u"] and row["all_unitary"] and row["all_distinct"]


def test_clocks_refine_along_divisibility_only(control: dict) -> None:
    tower = control["tower"]
    assert tower["zeta4_refines_zeta3"] is None and tower["zeta3_refines_zeta4"] is None
    assert tower["zeta12_refines_zeta3"] == 4
    assert tower["zeta12_refines_zeta4"] == 3
    assert tower["zeta24_refines_zeta12"] == 2
    assert tower["chain_condition_is_divisibility"]
    existing = control["existing_refinement_tower"]
    assert existing["orders"] == [3, 6, 12]
    assert existing["half_step_squares_to_previous"]


def test_swap_has_a_unitary_root_and_no_real_root(control: dict) -> None:
    sto = control["stochastic_control"]
    assert sto["swap_is_stochastic_and_unitary"]
    assert sto["unitary_root_squares_to_swap"] and sto["unitary_root_is_unitary"]
    assert sto["unitary_root_has_real_entries"] is False
    assert sto["real_root_exists"] is False
    assert sto["stochastic_half_step_exists"] is False
    assert sto["rational_root_exists"] is False
    assert sto["rational_root_candidates"] == ["-1", "-1/2", "-1/4", "1/4", "1/2", "1"]
    assert sto["forced_stochastic_candidate"] == [["0", "1"], ["0", "1"]]


def test_ledger_has_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == ["finite invariant", "completion", "residual import"]
    assert [row["status"] for row in ledger] == ["COMPUTED", "IMPORTED", "IMPORTED"]
    assert "continuity" in ledger[2]["statement"]


def test_negative_refusals() -> None:
    clock3 = hbc.weyl_clock(3, N)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.spectral_projectors(clock3, 5)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.matrix_order(hbc.weyl_shift(4, N), 3)
    two = hbc.root_of_unity(N, 0) + hbc.root_of_unity(N, 0)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.finite_spectral_theorem(ctc.mat_scale(hbc.identity(2, N), two))
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.clock_square_roots(hbc.weyl_shift(4, 12))
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.refines(5, 3, N)
    with pytest.raises(ctc.ClockControlRefusal):
        ctc.evaluate_clock_tower_control(conductor=12)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'clock_tower_control.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'clock_tower_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.clock_tower_control', 'finite_qm.use_cases.clock_tower_control')
_USE_SHIM = True
_MUTANTS = (('matrix_order:43', '    for m in range(1, max_order + 1):', '    for m in range(1, max_order + 2):'),)
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
