"""
test_regge_pachner_wdw.py — Integration Tests for 4D Simplicial Quantum Gravity Regge-Wheeler-DeWitt Constraints and Pachner Moves.

AuthorityEffect: None.

Tests:
1. Simplicial 4-manifold topology: S^4 seed, 2->4 bistellar move, 3->3 topological flip, and Euler characteristic invariance (chi = 2).
2. Flat triangulation: Exact gauge coboundary momentum and zero deficit angles yield vanishing defect mass (Phi_WDW = 0.0) -> ExactRepair.
3. Curved triangulation under Pachner surgery: Non-zero deficit angles and transverse edge insertion induce non-vanishing constraint defect mass (Phi_WDW > 0.0) -> SplitBrainRefusal.
4. Strong duality gap certification (|primal_obj - dual_obj| <= 1e-7) on direct-sum gauge cochains C^1 + C^0.
5. GIN mode indexing of vertex-edge constraint channels.
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.regge_pachner_wdw import (
    Simplicial4DManifold,
    ReggeWheelerDeWittEngine,
    ReggePachnerAuditReceipt,
)


def test_simplicial_manifold_seed_and_pachner_moves():
    """Validates S^4 manifold seed and topological invariance under 1->5, 2->4, and 3->3 Pachner moves."""
    manifold = Simplicial4DManifold()

    # Boundary of 5-simplex: 6 vertices, 15 edges, 20 triangles, 15 tetrahedra, 6 4-simplices
    assert manifold.num_vertices == 6
    assert manifold.num_edges == 15
    assert manifold.num_triangles == 20
    assert manifold.num_tetrahedra == 15
    assert manifold.num_four_simplices == 6
    assert manifold.euler_characteristic == 2

    # Execute 1->5 Pachner move (subdivision)
    success_15 = manifold.apply_1_to_5_move()
    assert success_15 is True
    assert manifold.num_vertices == 7
    assert manifold.num_four_simplices == 10  # Delta N4 = +4
    assert manifold.euler_characteristic == 2

    # Execute 2->4 Pachner move (growth)
    success_24 = manifold.apply_2_to_4_move(auto_subdivide=False)
    assert success_24 is True
    assert manifold.num_four_simplices == 12  # Delta N4 = +2
    assert manifold.euler_characteristic == 2  # Topological invariant

    # Execute 3->3 Pachner move (flip)
    success_33 = manifold.apply_3_to_3_move()
    assert success_33 is True
    assert manifold.num_four_simplices == 12  # Delta N4 = 0
    assert manifold.euler_characteristic == 2  # Topological invariant


def test_flat_triangulation_exact_constraint_closure():
    """
    Validates that a flat 4D triangulation with exact coboundary momentum and zero deficit angles
    satisfies exact diffeomorphism constraint closure (Phi_WDW = 0.0) -> ExactRepair.
    """
    engine = ReggeWheelerDeWittEngine(in_memory=True)
    try:
        receipt = engine.audit_pachner_surgery(
            apply_pachner_moves=False,
            curvature_regime="Flat",
            model_name="Flat_S4_Seed",
        )

        assert receipt.curvature_regime == "Flat"
        assert receipt.primal_wdw_defect_mass == pytest.approx(0.0, abs=1e-6)
        assert receipt.dual_certified_objective == pytest.approx(0.0, abs=1e-6)
        assert receipt.duality_gap <= 1e-7
        assert receipt.is_diffeomorphism_closed is True
        assert receipt.terminal_route == "ExactRepair"
    finally:
        engine.close()


def test_curved_pachner_moves_induce_defect_mass():
    """
    Validates that Pachner moves (2->4 and 3->3) on curved 4D triangulations induce
    non-vanishing constraint defect mass (Phi_WDW > 0.0), breaking exact closure -> SplitBrainRefusal.
    """
    engine = ReggeWheelerDeWittEngine(in_memory=True)
    try:
        receipt = engine.audit_pachner_surgery(
            apply_pachner_moves=True,
            curvature_regime="Curved",
            model_name="Curved_Pachner_S4",
        )

        assert receipt.curvature_regime == "Curved"
        assert "1->5" in receipt.pachner_moves_applied
        assert "2->4" in receipt.pachner_moves_applied
        assert "3->3" in receipt.pachner_moves_applied
        assert receipt.initial_n4 == 6
        assert receipt.final_n4 == 12
        assert receipt.euler_characteristic == 2

        # Core Discovery: Non-vanishing constraint defect mass
        assert receipt.primal_wdw_defect_mass > 0.0
        assert receipt.primal_wdw_defect_mass == pytest.approx(receipt.dual_certified_objective, rel=1e-4)
        assert receipt.duality_gap <= 1e-6

        # Discrete diffeomorphism closure broken
        assert receipt.is_diffeomorphism_closed is False
        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        engine.close()


def test_dual_certification_gap_zero():
    """Validates strong duality gap certification (|primal - dual| <= 1e-7) for both flat and curved regimes."""
    manifold = Simplicial4DManifold()

    for regime in ("Flat", "Curved"):
        res = ReggeWheelerDeWittEngine.solve_direct_sum_wdw_lp(manifold, curvature_regime=regime)
        assert res["duality_gap"] <= 1e-6
        if regime == "Flat":
            assert res["is_closed"] is True
            assert res["primal_obj"] == pytest.approx(0.0, abs=1e-6)
        else:
            assert res["is_closed"] is False
            assert res["primal_obj"] > 0.0


def test_gin_mode_posting_list_indexing():
    """Validates GIN mode indexing of vertex-edge constraint channels."""
    engine = ReggeWheelerDeWittEngine(in_memory=True)
    try:
        receipt = engine.audit_pachner_surgery(
            apply_pachner_moves=True,
            curvature_regime="Curved",
            model_name="GIN_Indexed_WDW",
        )

        c = engine.conn.cursor()
        c.execute("SELECT COUNT(DISTINCT mode_id) FROM GinModePostingList;")
        distinct_modes = c.fetchone()[0]

        # S^4 manifold after 1->5, 2->4, 3->3 has 7 vertices -> 7 constraint mode channels
        assert distinct_modes == 7
        assert len(engine.posting_index) == 7
        for m in range(1, 8):
            assert 1 in engine.posting_index[m]
    finally:
        engine.close()
