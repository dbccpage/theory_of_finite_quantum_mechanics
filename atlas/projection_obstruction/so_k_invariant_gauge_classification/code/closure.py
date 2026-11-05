"""
Mixed 2-Cell Closure Bound Evaluator and Operator Norm Engine.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np

from carrier import GraphComplex, Cochain
from solver import MixedNormSolver


@dataclass(frozen=True)
class ClosureBoundResult:
    """Report on 2-cell closure bound evaluation."""

    gamma_closure_defect: float
    operator_norm_bound: float
    candidate_primal_value: float
    certified_quotient_value: Optional[float]
    candidate_bound_holds: bool
    certified_bound_holds: bool
    is_bound_satisfied: bool
    closure_ratio: Optional[float]
    is_exact_repair: bool
    details: Dict[str, Any]

    @property
    def phi_quotient_obstruction(self) -> float:
        """Compatibility alias for candidate_primal_value."""
        return self.candidate_primal_value


class ClosureBoundEvaluator:
    """
    Evaluates:
        Gamma_{2,1,u}([h]) = ||d1 h||_{1,2,u}
    and asserts:
        Gamma_{2,1,u}([h]) <= ||d1||_{(1,2,c)->(1,2,u)} * Phi_{2,1,c}([h]).
    """

    def __init__(self, complex: GraphComplex) -> None:
        if not complex.verify_complex():
            raise ValueError("d1 @ d0 != 0: GraphComplex is not a valid chain complex.")
        self.complex = complex
        self.solver = MixedNormSolver(complex)

    def compute_operator_norm(self) -> float:
        """
        Exact constructive formula for ||d1||_{(1,2,c)->(1,2,u)}:
            ||d1|| = max_{e in E} (sum_{f in F} u_f |(d1)_{f,e}|) / c_e.
        """
        if self.complex.num_faces == 0:
            return 0.0

        d1 = self.complex.d1  # (F, m)
        u = self.complex.face_weights  # (F,)
        c = self.complex.edge_weights  # (m,)

        abs_d1 = np.abs(d1)
        col_sums = u @ abs_d1  # (m,)
        ratios = col_sums / c
        return float(np.max(ratios))

    def evaluate(self, h: Cochain) -> ClosureBoundResult:
        """
        Evaluate Gamma, Phi, and the closure inequality for cochain h.
        Distinguishes candidate primal value from certified quotient value.
        """
        if h.shape != (self.complex.num_edges, self.complex.stalk_dim):
            raise ValueError(f"Cochain shape {h.shape} does not match complex edges.")

        # 1. Compute Gamma = ||d1 h||_{1,2,u}
        d1_h = self.complex.coboundary_d1(h)
        gamma = d1_h.mixed_l1_l2_norm(self.complex.face_weights)

        # 2. Compute Phi candidate and certification
        cert = self.solver.solve(h)
        candidate_primal = cert.primal_value
        certified_quotient = cert.primal_value if cert.is_optimal else None

        # 3. Compute operator norm
        op_norm = self.compute_operator_norm()

        # Check bounds
        max_allowed_gamma = op_norm * candidate_primal
        candidate_bound_holds = bool(gamma <= max_allowed_gamma + 1e-6)
        certified_bound_holds = bool(cert.is_optimal and candidate_bound_holds)
        is_satisfied = certified_bound_holds  # fail closed!

        # A small positive quotient is still positive. Report a ratio only
        # for a tolerance-qualified positive quotient, never for a candidate
        # that failed certification. A computed zero is not an exact proof.
        is_exact = bool(cert.is_optimal and candidate_primal == 0.0)
        closure_ratio = (
            gamma / candidate_primal
            if cert.is_optimal and candidate_primal > 0.0 else None
        )

        return ClosureBoundResult(
            gamma_closure_defect=gamma,
            operator_norm_bound=op_norm,
            candidate_primal_value=candidate_primal,
            certified_quotient_value=certified_quotient,
            candidate_bound_holds=candidate_bound_holds,
            certified_bound_holds=certified_bound_holds,
            is_bound_satisfied=is_satisfied,
            closure_ratio=closure_ratio,
            is_exact_repair=is_exact,
            details={
                "duality_gap": cert.duality_gap,
                "signed_duality_gap": getattr(cert, "signed_duality_gap", cert.duality_gap),
                "is_solver_optimal": cert.is_optimal,
            },
        )

    def construct_sharp_achiever(self) -> Cochain:
        """
        Construct a cochain h that attains the operator norm ||d1|| exactly:
        Concentrate all vector mass on an edge e* that maximizes the column ratio.
        """
        if self.complex.num_faces == 0:
            return Cochain(np.zeros((self.complex.num_edges, self.complex.stalk_dim)))

        d1 = self.complex.d1
        u = self.complex.face_weights
        c = self.complex.edge_weights

        abs_d1 = np.abs(d1)
        col_sums = u @ abs_d1
        ratios = col_sums / c
        best_e = int(np.argmax(ratios))

        data = np.zeros((self.complex.num_edges, self.complex.stalk_dim), dtype=float)
        data[best_e, 0] = 1.0
        return Cochain(data, degree=1)
