"""Tests for the 4 imported omega_engine solvers in the flat paper code/ directory.

Verifies:
1. solv_finite_cochain_obstruction: exact repair and closed residual classification.
2. solv_phi_l1_lp: primal-dual L1 minimization and dual certificate verification.
3. solv_phi1_l1_boundary: integer network simplex L1 boundary solver.
4. solv_hodge_primal_dual: architectural boundary (deprecation of heuristic float L2 solver)
   and live exact Q-kernel spectral Hodge solver.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np
import pytest

from solv_finite_cochain_obstruction import (
    Verdict,
    analyze_finite_cochain,
    solve_finite_cochain_obstruction,
    self_check as finite_cochain_self_check,
    _matvec,
)
from solv_phi_l1_lp import solve_phi
from solv_phi1_l1_boundary import (
    Boundary1,
    BoundaryEdge,
    solve_l1_boundary,
)
from solv_hodge_primal_dual import (
    Topology,
    quotient_decomposition,
    solve_l1_hodge,
    SpectralHodgeInput,
    solve_spectral_hodge,
)
try:
    from finite_cochain_complex import FiniteCochainComplex
except ImportError:
    from ..finite_cochain_complex import FiniteCochainComplex


class TestFiniteCochainObstructionSolver:
    """Test exact classification of finite C1 cochains into exact repair vs closed residual."""

    def test_self_check(self):
        """Run built-in self check from the solver module."""
        finite_cochain_self_check()

    def test_exact_repair_classification(self):
        """When omega is in im(d0), solver classifies verdict as EXACT_REPAIR."""
        # 3 vertices, 3 edges (0->1, 1->2, 0->2)
        # d0 coboundary matrix (edges x vertices):
        # e0: -v0 + v1
        # e1: -v1 + v2
        # e2: -v0 + v2
        # d1: e0 + e1 - e2 = 0
        filled = FiniteCochainComplex.from_rows(
            (3, 3, 1),
            ((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
            ((1, 1, -1),),
        )

        # Exact coboundary: alpha = (1, 2, 4) -> d0 alpha = (1, 2, 3)
        res = analyze_finite_cochain(filled, (1, 2, 3))
        assert res.verdict == Verdict.EXACT_REPAIR
        assert res.primitive_witness is not None
        # Verify the witness exactly reconstructs beta = (1, 2, 3)
        reconstructed = _matvec(filled.d0, res.primitive_witness)
        assert reconstructed == (Fraction(1), Fraction(2), Fraction(3))
        assert res.authority_effect == "None"

    def test_curvature_classification(self):
        """When omega has nonzero curl, classifies verdict as CURVATURE."""
        filled = FiniteCochainComplex.from_rows(
            (3, 3, 1),
            ((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
            ((1, 1, -1),),
        )

        # Nonzero curvature: (1, 2, 4) gives d1 * (1, 2, 4) = 1 + 2 - 4 = -1 != 0
        res = analyze_finite_cochain(filled, (1, 2, 4))
        assert res.verdict == Verdict.CURVATURE
        assert res.closure_defect == (Fraction(-1),)


class TestPhiL1LPSolver:
    """Test primal-dual L1 LP solver and certificate verification."""

    def test_solve_phi_exact_and_dual_certificate(self):
        """Solve min_f ||omega - B f||_1 and verify strong duality and dual certificate."""
        # Cycle on 3 vertices
        B = np.array([
            [-1.0, 1.0, 0.0],
            [0.0, -1.0, 1.0],
            [1.0, 0.0, -1.0],
        ])
        omega = np.array([1.0, 1.0, 1.0])

        f_star, h1, cert = solve_phi(B, omega)

        # Duality gap must be zero
        assert cert.duality_gap == pytest.approx(0.0, abs=1e-7)
        assert cert.phi1 == pytest.approx(3.0, abs=1e-7)

        # Verify dual certificate
        assert cert.verify() is True
        assert np.max(np.abs(cert.dual.values)) <= 1.0 + 1e-7

    def test_solve_phi_weighted(self):
        """Solve weighted L1 obstruction and verify bounds."""
        B = np.array([
            [-1.0, 1.0],
            [1.0, -1.0],
        ])
        omega = np.array([2.0, 0.0])
        weights = np.array([1.0, 3.0])

        f_star, h1, cert = solve_phi(B, omega, weights=weights)
        assert cert.verify() is True
        assert cert.duality_gap == pytest.approx(0.0, abs=1e-7)


class TestPhi1IntegerBoundarySolver:
    """Test integer network simplex L1 boundary solver."""

    def test_integer_l1_boundary_cycle(self):
        """Solve integer L1 boundary for a balanced demand vector."""
        # 3 vertices, edges: 0->1, 1->2, 2->0
        boundary = Boundary1(
            num_vertices=3,
            edges=[
                BoundaryEdge(tail=0, head=1, weight=1),
                BoundaryEdge(tail=1, head=2, weight=1),
                BoundaryEdge(tail=2, head=0, weight=1),
            ],
        )
        # Balanced demand vector summing to 0 (flow conservation)
        x = [1, -1, 0]
        solution = solve_l1_boundary(boundary, x)

        assert isinstance(solution.objective, int)
        assert solution.objective == 1
        assert len(solution.z) == 3
        assert len(solution.vertex_potential) == 3
        assert len(solution.reduced_costs) == 3


class TestHodgePrimalDualArchivedBoundary:
    """Test architectural boundary: deprecated heuristic float L2 Hodge solver raises NotImplementedError."""

    def test_topology_independent(self):
        topo = Topology.independent(6)
        assert topo.num_edges() == 6

    def test_deprecated_solver_raises_not_implemented(self):
        with pytest.raises(NotImplementedError, match="Heuristic float-based solvers are deprecated"):
            quotient_decomposition(Topology.independent(3), [1.0, 0.0, 0.0])

        with pytest.raises(NotImplementedError, match="Heuristic float-based solvers are deprecated"):
            solve_l1_hodge(Topology.independent(3), [1.0, 0.0, 0.0])
