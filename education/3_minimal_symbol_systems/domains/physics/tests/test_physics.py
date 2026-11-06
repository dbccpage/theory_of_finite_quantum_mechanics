"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import sys
from pathlib import Path

# Add domain code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import numpy as np
from domain_physics_kernel import (
    DomainEngine,
    PrimitiveDifferenceSetting,
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
    assert engine.state.invariants["irreflexive"] is True


def test_admit_orientation_and_tie_retention():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()
    assert engine.step_04_admit_orientation()
    assert engine.state.step == 4
    assert engine.state.invariants["tie_retention_active"] is True
    assert "branch_D2" in engine.state.branches_retained
    assert "branch_S2" in engine.state.branches_retained
    assert len(engine.state.branches_retained) == 2
    assert engine.state.branch_metadata["branch_D2"]["symmetric"] is False
    assert engine.state.branch_metadata["branch_S2"]["symmetric"] is True


def test_admit_transposition_and_antisymmetry():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()
    engine.step_04_admit_orientation()
    assert engine.step_05_admit_transposition()
    assert engine.state.step == 5
    assert engine.state.invariants["transposition_sign_inversion"] is True


def test_boundary_closure_invariant():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()
    receipt = engine.evaluate_boundary_closure()
    assert isinstance(receipt, SimplicialBoundaryReceipt)
    assert receipt.is_nilpotent is True
    assert receipt.product_matrix == [[0], [0], [0]]
    assert receipt.euler_characteristic == 1
    assert engine.state.invariants["boundary_nilpotence"] is True


def test_evaluate_simplicial_boundary_matrices_multi_complex():
    engine = DomainEngine()
    # Tetrahedron boundary shell (4 vertices, 6 edges, 4 faces)
    vertices = ["v0", "v1", "v2", "v3"]
    edges = [("v0", "v1"), ("v1", "v2"), ("v0", "v2"), ("v0", "v3"), ("v1", "v3"), ("v2", "v3")]
    faces = [("v0", "v1", "v2"), ("v0", "v1", "v3"), ("v1", "v2", "v3"), ("v0", "v2", "v3")]
    receipt = engine.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
    assert receipt.is_nilpotent is True
    assert receipt.euler_characteristic == 4 - 6 + 4  # chi = 2 (topological sphere S^2)
    assert np.all(np.array(receipt.product_matrix) == 0)




def test_explicit_recovery_gap_detection():
    engine = DomainEngine()
    gap_info = engine.check_gap_obstruction()
    assert gap_info["gap_id"] == "ContinuumMetricObstruction"
    assert gap_info["status"] == "UNBRIDGED_OBSTRUCTION"
    assert engine.gap_detected


# ==============================================================================
# Negative Controls
# ==============================================================================


def test_negative_reflexivity_violation():
    """Negative Control 1: Injected reflexive loop violates distinctness."""
    bad_setting = PrimitiveDifferenceSetting(
        carrier={"a", "b"}, relation={("a", "b"), ("a", "a")}, a="a", b="b"
    )
    assert not bad_setting.is_irrefl(), "Reflexive pair ('a', 'a') must violate irreflexivity"
    assert not bad_setting.is_distinct(), "Reflexive pair must violate distinctness theorem"

    # Degenerate collapse a == b
    collapsed_setting = PrimitiveDifferenceSetting(
        carrier={"a"}, relation={("a", "a")}, a="a", b="a"
    )
    assert not collapsed_setting.is_distinct(), "Point collapse a == b must violate distinctness"

    # Transposition on reflexive pair yields zero boundary rather than sign inversion
    refl_boundary = bad_setting.evaluate_1chain_boundary(("a", "a"))
    assert refl_boundary == {}, "Reflexive pair boundary must vanish trivially"
    assert not bad_setting.verify_transposition_sign_inversion(("a", "a")), (
        "Transposition sign inversion must fail on reflexive pairs"
    )


def test_negative_unauthorized_admission():
    """Negative Control 2: Unauthorized transitions and skipped steps are rejected."""
    engine = DomainEngine()

    # Skipping step 1: attempting to admit germ from void without root reference
    assert not engine.step_02_admit_germ("a", "b"), (
        "Attempting step 2 without step 1 must be rejected"
    )

    # Attempting step 3 without initialized setting
    engine_uninit = DomainEngine()
    assert not engine_uninit.step_03_enforce_irrefl(), (
        "Attempting irreflexivity enforcement without prior germ must return False"
    )

    # Skipping step 3: attempting orientation before enforcing irreflexivity
    engine_skip = DomainEngine()
    engine_skip.step_01_admit_root("<>")
    engine_skip.step_02_admit_germ("a", "b")
    assert not engine_skip.step_04_admit_orientation(), (
        "Attempting orientation without irreflexivity enforcement must return False"
    )

    # Attempting unproved branch collapse: tie-retention invariant requires preserving both tied branches
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_a", "pt_b")
    engine.step_03_enforce_irrefl()
    engine.step_04_admit_orientation()
    assert "branch_D2" in engine.state.branches_retained
    assert "branch_S2" in engine.state.branches_retained
    assert len(engine.state.branches_retained) == 2, (
        "Tie-retention invariant requires preserving both tied branches"
    )


def test_negative_boundary_non_nilpotence():
    """Negative Control 3: Symmetric or non-alternating boundary matrices violate nilpotence."""
    # Correct B1 for triangle:
    # V = [v0, v1, v2], E = [e0=(v0,v1), e1=(v1,v2), e2=(v0,v2)]
    # B1 = [[-1,  0, -1],
    #       [+1, -1,  0],
    #       [ 0, +1, +1]]
    # Malformed B2 with all positive signs: e0 + e1 + e2 instead of e0 + e1 - e2
    b1 = np.array([[-1, 0, -1], [1, -1, 0], [0, 1, 1]], dtype=np.int64)
    malformed_b2 = np.array([[1], [1], [1]], dtype=np.int64)

    prod = np.dot(b1, malformed_b2)
    assert not np.all(prod == 0), "Malformed boundary matrix must fail nilpotency (prod != 0)"
    assert np.any(prod != 0), "Non-zero boundary residual must be detected"
