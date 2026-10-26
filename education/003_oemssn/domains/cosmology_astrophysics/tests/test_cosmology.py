"""
Tests for Cosmology, Gravitation & Astrophysics Domain Kernel
AuthorityEffect: None
"""

import sys
from pathlib import Path

# Add domain code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import pytest
from domain_cosmology_kernel import (
    CausalSet,
    DomainEngine,
    SimplicialBoundaryReceipt,
)


def test_initial_void_to_root():
    engine = DomainEngine()
    assert engine.state.step == 0
    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1
    assert "<>" in engine.state.carrier
    assert "branch_root_single" in engine.state.branches_retained


def test_germ_creation_and_witness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    assert engine.step_02_admit_germ("pt_alpha", "pt_beta")
    assert engine.state.step == 2
    assert ("pt_alpha", "pt_beta") in engine.state.relations


def test_irreflexive_enforcement_and_distinctness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    # inject reflexive defect
    engine.state.relations.add(("pt_alpha", "pt_alpha"))
    assert not engine.setting.is_irrefl()

    # Discharge obstruction
    assert engine.step_03_enforce_irrefl()
    assert engine.setting.is_irrefl()
    assert engine.setting.is_distinct()


def test_boundary_closure_invariant():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()
    receipt = engine.evaluate_boundary_closure()
    assert isinstance(receipt, SimplicialBoundaryReceipt)
    assert receipt.is_nilpotent
    assert bool(receipt) is True


def test_explicit_recovery_gap_detection():
    engine = DomainEngine()
    gap_info = engine.check_gap_obstruction()
    assert gap_info["gap_id"] == "SmoothCurvatureObstruction"
    assert gap_info["status"] == "UNBRIDGED_OBSTRUCTION"
    assert engine.gap_detected


def test_step_01_through_16_complete_progression():
    """Verifies all 16 steps of the Genesis Domain Cosmology & Astrophysics scenario."""
    engine = DomainEngine()

    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1

    assert engine.step_02_admit_germ("a", "b")
    assert engine.state.step == 2

    assert engine.step_03_enforce_irrefl()
    assert engine.state.step == 3

    assert engine.step_04_admit_orientation()
    assert engine.state.step == 4
    assert set(engine.state.branches_retained) == {"branch_D2", "branch_S2"}
    assert "branch_D2" in engine.state.branch_metadata
    assert "branch_S2" in engine.state.branch_metadata

    assert engine.step_05_admit_transposition()
    assert engine.state.step == 5
    assert engine.state.invariants["transposition_sign_inversion"] is True

    assert engine.step_06_instantiate_causal_alphabet(["e0", "e1", "e2", "e3"])
    assert engine.state.step == 6

    receipt = engine.step_07_evaluate_boundary_closure()
    assert engine.state.step == 7
    assert receipt.is_nilpotent

    assert engine.step_08_synthesize_causal_poset()
    assert engine.state.step == 8

    assert engine.step_09_resolve_parity()
    assert engine.state.step == 9

    assert engine.step_10_admit_higher_complexes()
    assert engine.state.step == 10

    assert engine.step_11_enforce_conservation()
    assert engine.state.step == 11

    assert engine.step_12_quotient_observer_interface()
    assert engine.state.step == 12

    assert engine.step_13_prune_fuel_bounded_branches()
    assert engine.state.step == 13

    assert engine.step_14_establish_frontier()
    assert engine.state.step == 14

    gap = engine.step_15_isolate_gap_obstruction()
    assert engine.state.step == 15
    assert gap["gap_id"] == "SmoothCurvatureObstruction"

    cert = engine.step_16_terminal_certification()
    assert engine.state.step == 16
    assert cert["status"] == "SCENARIO_RECORDED"
    assert cert["reported_step"] == 16
    assert cert["authority_effect"] == "None"




def test_regge_spacetime_nilpotency_3d():
    """
    Verifies 3D Regge tetrahedron simplicial complex satisfies:
    B_1 * B_2 = 0
    B_2 * B_3 = 0
    Wheeler-DeWitt constraint defect = 0
    Euler characteristic = 1.
    """
    engine = DomainEngine()
    receipt = engine.evaluate_regge_spacetime_complex()

    assert receipt.num_vertices == 4
    assert receipt.num_edges == 6
    assert receipt.num_faces == 4
    assert receipt.num_tetrahedra == 1
    assert receipt.is_b1_b2_nilpotent is True
    assert receipt.is_b2_b3_nilpotent is True
    assert receipt.boundary_defect == 0
    assert receipt.euler_characteristic == 1
    assert bool(receipt) is True


def test_horizon_bipartite_cut_counting():
    """
    Verifies finite crossing-link counts via
    causal link cut counting between Cauchy past and future.
    """
    events = ["p0", "p1", "f0", "f1"]
    rels = {
        ("p0", "f0"),
        ("p0", "f1"),
        ("p1", "f0"),
        ("p1", "f1"),
    }
    cs = CausalSet(events, rels)
    past = {"p0", "p1"}
    future = {"f0", "f1"}

    cut = cs.compute_bipartite_link_cut(past, future)
    assert cut == 4  # 4 irreducible links crossing horizon


def test_negative_control_causal_self_loop_rejected():
    """Negative Control: Self loop violates causal irreflexivity."""
    events = ["e0", "e1"]
    with pytest.raises(ValueError, match="violates irreflexivity"):
        CausalSet(events, {("e0", "e0")})


def test_negative_control_causal_cycle_rejected():
    """Negative Control: Closed timelike curve (CTC) / causal cycle is rejected."""
    events = ["e0", "e1", "e2"]
    rels = {("e0", "e1"), ("e1", "e2"), ("e2", "e0")}
    with pytest.raises(ValueError, match="Causal cycle detected|Acyclicity violated"):
        CausalSet(events, rels)


def test_negative_control_unknown_element_rejected():
    """Negative Control: Relation referencing unknown element is rejected."""
    events = ["e0", "e1"]
    with pytest.raises(ValueError, match="references non-existent element"):
        CausalSet(events, {("e0", "e2")})
