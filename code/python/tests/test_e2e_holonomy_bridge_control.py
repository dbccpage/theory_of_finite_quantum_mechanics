"""Exact tests for the finite multi-report holonomy bridge control (QM-207..QM-211).

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/holonomy_bridge.py
Claim: evaluate_holonomy_bridge_control certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.domain.cyclotomic_tower import CyclotomicElement
from finite_qm.use_cases import holonomy_bridge_control as hbc

N = 12


def z(k: int) -> CyclotomicElement:
    return hbc.root_of_unity(N, k)


@pytest.fixture(scope="module")
def control() -> dict:
    return hbc.evaluate_holonomy_bridge_control(conductor=N, census_conductor=3)


@pytest.fixture
def diamond() -> hbc.FiniteCarrierGraph:
    return hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))


def test_unit_qm207_cycle_invariants_classify_gauge_orbits(control: dict) -> None:
    q = control["qm207"]
    assert q["carrier"]["first_betti_number"] == 2
    assert q["cycle_invariants_gauge_invariant"]
    assert q["tree_gauge_has_unit_tree_edges"] and q["tree_gauge_same_invariants"]
    assert q["holonomy_factorizes_on_all_test_loops"]
    assert q["relative_report_phase_gauge_invariant"]
    assert q["l1_weights_phase_blind"]
    census = q["orbit_census"]
    assert census["class_count"] == 3**2 == census["expected_class_count"]
    assert census["all_classes_have_expected_size"] and census["expected_class_size"] == 3**3
    assert census["hom_h1_mu_n_classification_exact"]
    assert q["gauge_equivalence_iff_same_invariants"]


def test_qm207_tampered_cotree_value_changes_an_invariant(diamond: hbc.FiniteCarrierGraph) -> None:
    base = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    cotree = diamond.cotree_edges()
    values = list(base.values)
    values[cotree[0]] = values[cotree[0]] * z(1)
    tampered = hbc.U1Cochain(diamond, tuple(values))
    assert tampered.cycle_invariants() != base.cycle_invariants()
    values = list(base.values)
    tree_edge = diamond.spanning_tree()[0]
    values[tree_edge] = values[tree_edge] * z(5)
    assert hbc.U1Cochain(diamond, tuple(values)).cycle_invariants() != base.cycle_invariants()


def test_negative_qm207_refusals(diamond: hbc.FiniteCarrierGraph) -> None:
    two = CyclotomicElement.rational(2, N)
    with pytest.raises(hbc.HolonomyControlRefusal):
        hbc.U1Cochain(diamond, (two, z(0), z(0), z(0), z(0)))
    with pytest.raises(hbc.HolonomyControlRefusal):
        hbc.FiniteCarrierGraph(4, ((0, 1), (2, 3)))
    with pytest.raises(hbc.HolonomyControlRefusal):
        hbc.root_exponent(two)
    cochain = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    with pytest.raises(hbc.HolonomyControlRefusal):
        cochain.holonomy([0, 1, 3])


def test_qm207_reversed_edge_gives_conjugate(diamond: hbc.FiniteCarrierGraph) -> None:
    cochain = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    assert cochain.transport([1, 0]) == cochain.transport([0, 1]).conjugate()
    assert cochain.holonomy([0, 1, 2, 0]) == cochain.holonomy([0, 2, 1, 0]).conjugate()


def test_qm208_interference_and_sorkin(control: dict) -> None:
    q = control["qm208"]
    assert q["l1_readout"] == "3"
    assert q["second_order_interference_nonzero"] and q["second_order_interference_real"]
    assert Fraction(q["trivial_fiber_interference"]) == 6
    assert q["sorkin_i3_quadratic_zero"] and q["sorkin_i3_matches_reused_certifier"]
    assert Fraction(q["sorkin_i3_quartic_on_trivial_fiber"]) == 36


def test_qm208_quadratic_i3_vanishes_on_random_cyclotomic_triples() -> None:
    triples = [
        (z(a), z(b) * 2, z(c) + z(a))
        for a in range(0, 12, 5)
        for b in range(0, 12, 7)
        for c in range(0, 12, 3)
    ]
    assert all(
        hbc.third_order_interference(hbc.quadratic_readout, list(t)).is_zero() for t in triples
    )
    assert any(
        not hbc.third_order_interference(hbc.quartic_readout, list(t)).is_zero() for t in triples
    )


def test_qm209_weyl_commutator_is_central_fourth_root(control: dict) -> None:
    q = control["qm209"]
    assert q["shift_clock_unitary"]
    assert q["commutator_holonomy_is_primitive_4th_root"]
    assert q["diagonal_pair_commutator_trivial"]
    assert q["fourier_conjugates_clock_to_inverse_shift"]
    X, Z = hbc.weyl_shift(3, N), hbc.weyl_clock(3, N)
    assert hbc.commutator_holonomy(X, Z) == hbc.root_of_unity(N, 8)
    with pytest.raises(hbc.HolonomyControlRefusal):
        hbc.scalar_multiple_of_identity(hbc.matmul(X, Z))


def test_qm210_born_and_peres_mermin(control: dict) -> None:
    q = control["qm210"]
    assert q["diagonal_born_equals_l1"] and q["transported_total_equals_l1_total"]
    assert q["transported_weights"] == ["0", "0", "0", "1"]
    pm = q["peres_mermin"]
    assert pm["contexts_commute_internally"]
    assert pm["context_signs"] == [1, 1, 1, 1, 1, -1]
    assert pm["parity_holonomy"] == -1 and pm["z2_obstruction"]


def test_qm211_clock_tower(control: dict) -> None:
    t = control["qm211"]
    assert t["orders"] == [3, 6, 12]
    assert t["all_unitary"] and t["finite_orders_exact"] and t["no_smaller_order"]
    assert t["half_step_squares_to_previous"]
    with pytest.raises(hbc.HolonomyControlRefusal):
        hbc.clock_refinement_tower(3, 4, N)


def test_ledger_names_a_residual_import_for_every_slot(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["import"][:6] for row in ledger] == [
        "QM-207",
        "QM-208",
        "QM-209",
        "QM-210",
        "QM-211",
    ]
    for row in ledger:
        assert row["residual_import"]
        assert "imported" in row["completion_status"]


def test_control_refuses_conductor_without_mu12() -> None:
    with pytest.raises(hbc.HolonomyControlRefusal):
        hbc.evaluate_holonomy_bridge_control(conductor=8)


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'campaigns' / 'holonomy_bridge.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'evaluate_holonomy_bridge_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.holonomy_bridge', 'finite_qm.use_cases.holonomy_bridge', 'src.qm.campaigns.holonomy_bridge_control', 'finite_qm.use_cases.holonomy_bridge_control')
_USE_SHIM = True
_MUTANTS = (('_zero:44', '    return CyclotomicElement.rational(0, conductor)', '    return CyclotomicElement.rational(1, conductor)'),)
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
