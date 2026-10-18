"""Exact tests for the finite multi-report holonomy bridge control (QM-207..QM-211).

AuthorityEffect: None.
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


def test_qm207_cycle_invariants_classify_gauge_orbits(control: dict) -> None:
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
    # a tree-edge change is not pure gauge: it moves the cycles through that edge
    values = list(base.values)
    tree_edge = diamond.spanning_tree()[0]
    values[tree_edge] = values[tree_edge] * z(5)
    assert hbc.U1Cochain(diamond, tuple(values)).cycle_invariants() != base.cycle_invariants()


def test_qm207_refusals(diamond: hbc.FiniteCarrierGraph) -> None:
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
    assert hbc.commutator_holonomy(X, Z) == hbc.root_of_unity(N, 8)  # omega_3^{-1}
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
