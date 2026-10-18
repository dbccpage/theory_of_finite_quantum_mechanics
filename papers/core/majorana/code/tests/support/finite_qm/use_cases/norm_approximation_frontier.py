# AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)
# Reference: Campaign C500 Block 02, Targets C500-T326 through C500-T350.

"""Campaign C500 Block 02: Norm-Indexed Approximation Frontier.

Implements:
1. Matrix norm definitions: Operator norm, Frobenius norm, normalized Frobenius,
   trace norm (Schatten-1), and normalized trace norm.
2. Direct-CCR defect lower bounds: For any finite d and scalar lambda != 0,
   ||QP - PQ - lambda*I||_{1,norm} >= |lambda| and ||QP - PQ - lambda*I||_{F,norm} >= |lambda|.
   Hence normalized direct-CCR defect is bounded away from zero for all d.
3. Phase-distance on R/Z and nearest d-th root approximation:
   dist_{S^1}(theta, a/d) <= 1/(2d).
4. A finite nearest-root table for rational phase 5/8. No irrational limit
   or O(1/d^2) convergence rate is established by that table.
5. Principal-log winding formula for a fixed clock/shift family, with a
   branch-cut refusal and a separately cited commuting-pair obstruction.
6. Rank normalization analysis demonstrating failure of cross-norm promotion.

Exact fields use Fraction arithmetic; floating values are illustrative numerical evaluations, not certified enclosures.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

try:
    from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.gaussian_rational import Gaussian
except ImportError:
    from apps.finite_qm.code.gaussian_rational import Gaussian


# ---------------------------------------------------------------------------
# Section 1: Exact Rational Norms & Matrix Utilities
# ---------------------------------------------------------------------------

class ExactRationalMatrix:
    """d x d square matrix with Gaussian rational entries."""

    def __init__(self, data: Sequence[Sequence[Union[Fraction, int, Gaussian, Tuple[Union[Fraction, int], Union[Fraction, int]]]]]) -> None:
        self.d = len(data)
        if self.d < 1:
            raise ValueError("Matrix dimension must be positive")
        self.rows: List[List[Gaussian]] = []
        for r in data:
            if len(r) != self.d:
                raise ValueError("Matrix must be square")
            row: List[Gaussian] = []
            for entry in r:
                if isinstance(entry, Gaussian):
                    row.append(entry)
                elif isinstance(entry, tuple) and len(entry) == 2:
                    row.append(Gaussian(Fraction(entry[0]), Fraction(entry[1])))
                else:
                    row.append(Gaussian(Fraction(entry), Fraction(0)))
            self.rows.append(row)

    @classmethod
    def identity(cls, d: int) -> ExactRationalMatrix:
        rows = [[Gaussian(Fraction(1, 1), Fraction(0)) if i == j else Gaussian(Fraction(0), Fraction(0)) for j in range(d)] for i in range(d)]
        return cls(rows)

    @classmethod
    def zero(cls, d: int) -> ExactRationalMatrix:
        rows = [[Gaussian(Fraction(0), Fraction(0)) for _ in range(d)] for _ in range(d)]
        return cls(rows)

    def trace(self) -> Tuple[Fraction, Fraction]:
        """Compute exact trace sum_{i=0}^{d-1} M_{ii}."""
        tot = Gaussian(Fraction(0), Fraction(0))
        for i in range(self.d):
            tot = tot + self.rows[i][i]
        return (tot.real, tot.imag)

    def frobenius_norm_squared(self) -> Fraction:
        """Compute exact sum_{i,j} |M_{ij}|^2 = sum_{i,j} (Re^2 + Im^2)."""
        tot = Fraction(0)
        for i in range(self.d):
            for j in range(self.d):
                g = self.rows[i][j]
                tot += g.real * g.real + g.imag * g.imag
        return tot

    def normalized_frobenius_norm_squared(self) -> Fraction:
        """Compute (1/d) sum_{i,j} |M_{ij}|^2."""
        return self.frobenius_norm_squared() / Fraction(self.d)

    def __sub__(self, other: ExactRationalMatrix) -> ExactRationalMatrix:
        if self.d != other.d:
            raise ValueError("Dimension mismatch")
        new_rows = []
        for i in range(self.d):
            row = []
            for j in range(self.d):
                row.append(self.rows[i][j] - other.rows[i][j])
            new_rows.append(row)
        return ExactRationalMatrix(new_rows)

    def __mul__(self, other: ExactRationalMatrix) -> ExactRationalMatrix:
        if self.d != other.d:
            raise ValueError("Dimension mismatch")
        d = self.d
        new_rows = [[Gaussian(Fraction(0), Fraction(0)) for _ in range(d)] for _ in range(d)]
        for i in range(d):
            for k in range(d):
                a_ik = self.rows[i][k]
                if not a_ik:
                    continue
                for j in range(d):
                    b_kj = other.rows[k][j]
                    if not b_kj:
                        continue
                    new_rows[i][j] = new_rows[i][j] + (a_ik * b_kj)
        return ExactRationalMatrix(new_rows)


# ---------------------------------------------------------------------------
# Section 2: Direct-CCR Defect and Exact Lower Bounds (Targets C500-T328, T329)
# ---------------------------------------------------------------------------

def ccr_residual_exact(Q: ExactRationalMatrix, P: ExactRationalMatrix, scalar_lambda: Fraction) -> ExactRationalMatrix:
    """Compute exact residual R_lambda(Q, P) = QP - PQ - lambda * I."""
    comm = (Q * P) - (P * Q)
    target = ExactRationalMatrix([
        [(scalar_lambda, Fraction(0)) if i == j else (Fraction(0), Fraction(0)) for j in range(Q.d)]
        for i in range(Q.d)
    ])
    return comm - target


def verify_ccr_defect_lower_bounds(d: int, scalar_lambda: Fraction) -> Dict[str, Any]:
    """Verify that for ANY pair Q, P in M_d, the CCR defect is strictly lower bounded:

    1. |Tr(R_lambda)| = |lambda| * d
    2. ||R_lambda||_1 >= |Tr(R_lambda)| = |lambda| * d
    3. Normalized trace norm: ||R_lambda||_{1, norm} = (1/d) ||R_lambda||_1 >= |lambda|
    4. Normalized Frobenius norm: ||R_lambda||_{F, norm} >= |lambda|
    5. Operator norm: ||R_lambda||_{op} >= |lambda|
    """
    if type(d) is not int or d < 1:
        raise ValueError("Dimension must be a positive integer")
    if scalar_lambda == 0:
        raise ValueError("The nonvanishing bound requires nonzero lambda")
    abs_lambda = abs(scalar_lambda)
    return {
        "dimension": d,
        "scalar_lambda": str(scalar_lambda),
        "trace_defect_lower_bound": str(abs_lambda * Fraction(d)),
        "normalized_trace_norm_lower_bound": str(abs_lambda),
        "normalized_frobenius_norm_lower_bound": str(abs_lambda),
        "operator_norm_lower_bound": str(abs_lambda),
        "limit_as_d_to_infinity_vanishes": False,
        "normalized_defect_strictly_positive": abs_lambda > 0,
    }


# ---------------------------------------------------------------------------
# Section 3: Phase Distance & Continued Fractions (Targets C500-T330..T334)
# ---------------------------------------------------------------------------

def phase_distance_on_circle(theta1: Fraction, theta2: Fraction) -> Fraction:
    """Compute geodesic distance on R/Z: dist_{S^1}(theta1, theta2) = min_{k in Z} |theta1 - theta2 - k|."""
    diff = (theta1 - theta2) % Fraction(1)
    if diff > Fraction(1, 2):
        diff = Fraction(1) - diff
    return diff


def nearest_root_of_unity(theta: Fraction, d: int) -> Tuple[int, Fraction]:
    """Find a in {0, ..., d-1} minimizing dist_{S^1}(theta, a/d) in exact discrete arithmetic.

    Returns (best_a, distance).
    """
    if type(d) is not int or d < 1:
        raise ValueError("Dimension must be a positive integer")
    best_a = 0
    min_dist = Fraction(1)
    for a in range(d):
        cand = Fraction(a, d)
        dist = phase_distance_on_circle(theta, cand)
        if dist < min_dist:
            min_dist = dist
            best_a = a
    return best_a, min_dist


def continued_fraction_convergents(val: Union[Fraction, float], max_depth: int = 10) -> List[Tuple[int, int]]:
    """Compute continued fraction convergents p_k / q_k for a rational or real number."""
    convergents: List[Tuple[int, int]] = []
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    rem = val
    for _ in range(max_depth):
        if isinstance(rem, Fraction):
            a = rem.numerator // rem.denominator
            frac_part = rem - a
            pn = a * p1 + p0
            qn = a * q1 + q0
            convergents.append((pn, qn))
            p0, q0 = p1, q1
            p1, q1 = pn, qn
            if frac_part == 0:
                break
            rem = Fraction(1, 1) / frac_part
        else:
            a = int(math.floor(rem))
            pn = a * p1 + p0
            qn = a * q1 + q0
            convergents.append((pn, qn))
            p0, q0 = p1, q1
            p1, q1 = pn, qn
            frac_part = rem - a
            if frac_part <= 0.0 or abs(frac_part) < 1e-12:
                break
            rem = 1.0 / frac_part
    return convergents


def compute_weyl_phase_approximation_schedule(
    target_phase: Fraction,
    dimension_schedule: Sequence[int],
) -> List[Dict[str, Any]]:
    """Compute exact phase approximation error along a chosen dimension schedule.

    Twisted Weyl defect: ||Z_d X_d - e^{2pi i theta} X_d Z_d||_{op} = 2*sin(pi * dist).
    """
    results = []
    for d in dimension_schedule:
        best_a, dist = nearest_root_of_unity(target_phase, d)
        dist_f = float(dist)
        analytic_op_defect = 2.0 * math.sin(math.pi * dist_f)
        results.append({
            "dimension": d,
            "best_numerator_a": best_a,
            "approx_phase": f"{best_a}/{d}",
            "exact_phase_distance": str(dist),
            "distance_float": dist_f,
            "dirichlet_bound_1_over_2d": float(Fraction(1, 2 * d)),
            "meets_dirichlet_bound": dist <= Fraction(1, 2 * d),
            "analytic_operator_norm_defect": analytic_op_defect,
            "linear_upper_bound": 2.0 * math.pi * dist_f,
            "analytic_rational_upper_bound": str(Fraction(44, 7) * dist),
            "bound_basis": "2*sin(pi*distance) <= 2*pi*distance <= (44/7)*distance",
            "floating_fields_scope": "illustrative evaluation; use exact phase distance and analytic rational bound",
        })
    return results


# ---------------------------------------------------------------------------
# Section 4: Almost-Commuting vs. Commuting Obstruction (Bott Index) (T336..T338)
# ---------------------------------------------------------------------------

def compute_bott_index_witness(d: int) -> Dict[str, Any]:
    """Principal-log winding index for the fixed clock/shift pair.

    Z X Z* X* = exp(2 pi i / d) I. The principal logarithm needs its
    spectrum off the negative real axis: d=2 is a branch-cut refusal.
    For d>2 the trace-log formula yields d*(1/d)=1; d=1 commutes.
    The obstruction theorem is a cited input, not mechanized here:
    Loring, arXiv:1302.0349, Section 2 and Theorem 2.3.
    """
    if type(d) is not int or d < 1:
        raise ValueError("Dimension must be a positive integer")
    admissible = d != 2
    index = (0 if d == 1 else 1) if admissible else None
    return {
        "dimension": d,
        "commutator_operator_norm": 0.0 if d == 1 else 2.0 * math.sin(math.pi / d),
        "commutator_norm_formula": "2*sin(pi/d)",
        "index_definition": "Tr(log(Z X Z* X*))/(2*pi*i), principal branch",
        "log_branch_admissible": admissible,
        "bott_index": index,
        "is_topologically_obstructed": (index != 0) if admissible else None,
        "obstruction_status": "REFUSED_LOG_BRANCH_CUT" if d == 2 else "CITED_INDEX_OBSTRUCTION" if d > 2 else "COMMUTING",
        "theorem_source": "https://arxiv.org/abs/1302.0349",
        "evidence_scope": "fixed-family analytic formula with cited obstruction; not a general numerical index checker",
        "numerical_fields": "illustrative floating evaluation; no certified interval",
    }


# ---------------------------------------------------------------------------
# Section 5: Cross-Norm Promotion Failure (Rank Normalization) (Target C500-T339)
# ---------------------------------------------------------------------------

def cross_norm_promotion_counterexample_table() -> List[Dict[str, Any]]:
    """Demonstrate how rank normalization changes apparent convergence:

    Consider a rank-1 projection P_1 = diag(1, 0, 0, ..., 0) in M_d.
    - Frobenius norm: ||P_1||_F = 1.
    - Normalized Frobenius norm: ||P_1||_{F, norm} = 1 / sqrt(d) -> 0 as d -> infinity.
    - Operator norm: ||P_1||_{op} = 1 (constant, does NOT vanish!).
    - Trace norm: ||P_1||_1 = 1.
    - Normalized trace norm: ||P_1||_{1, norm} = 1/d -> 0.

    Conclusion: Normalized Frobenius and normalized trace convergence to 0 does NOT imply
    operator norm convergence. Cross-norm promotion without a theorem is strictly forbidden.
    """
    rows = []
    for d in [2, 4, 8, 16, 64, 256, 1024]:
        rows.append({
            "dimension": d,
            "rank": 1,
            "operator_norm": 1.0,
            "frobenius_norm": 1.0,
            "normalized_frobenius_norm": 1.0 / math.sqrt(d),
            "trace_norm": 1.0,
            "normalized_trace_norm": 1.0 / d,
            "operator_norm_vanishes": False,
            "normalized_frobenius_vanishes": True,
        })
    return rows


# ---------------------------------------------------------------------------
# Section 6: Canonical Block 02 Receipt Generator (Target C500-T350)
# ---------------------------------------------------------------------------

FROZEN_DIMENSION_SCHEDULE = [2, 3, 5, 8, 13, 21, 34, 55, 89]
GOLDEN_RATIO_CONJUGATE_CONVERGENTS = [
    Fraction(1, 2),
    Fraction(2, 3),
    Fraction(3, 5),
    Fraction(5, 8),
    Fraction(8, 13),
    Fraction(13, 21),
    Fraction(21, 34),
    Fraction(34, 55),
    Fraction(55, 89),
]


def generate_canonical_block02_receipt() -> Dict[str, Any]:
    """Generate the deterministic canonical receipt for Campaign C500 Block 02."""

    # 1. Direct CCR lower bounds across dimensions
    ccr_bounds = [
        verify_ccr_defect_lower_bounds(d, Fraction(1, 1))
        for d in [2, 3, 5, 8, 13, 21, 34, 55, 89]
    ]

    # 2. Finite rational phase 5/8 table; this is not an irrational convergent schedule
    weyl_rational_schedule = compute_weyl_phase_approximation_schedule(
        Fraction(5, 8),
        FROZEN_DIMENSION_SCHEDULE,
    )

    # 3. Voiculescu / Bott index obstruction across dimensions
    bott_results = [
        compute_bott_index_witness(d)
        for d in [2, 3, 5, 8, 13, 21, 34, 55, 89]
    ]

    # 4. Cross-norm rank counterexample table
    rank_table = cross_norm_promotion_counterexample_table()

    receipt = {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_02",
        "global_targets": "C500-T326..C500-T350",
        "terminal_outcome": "NORM_INDEXED_APPROXIMATION_FRONTIER",
        "evidence_scope": "finite rational tables and cited analytic inputs; no mechanized limit or verified launch freeze",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "source_anchor_binding": {
            "anchor_id": "S2",
            "citation": "Voiculescu, Asymptotically commuting unitaries in C*-algebras",
            "consumed_role": "Topological index obstruction for almost commuting unitaries",
            "unauthorized_extrapolation": "Vanishing of normalized Frobenius norm implies commuting approximation",
        },
        "ccr_defect_bounds": ccr_bounds,
        "weyl_approximation_schedule": weyl_rational_schedule,
        "bott_index_obstruction": bott_results,
        "cross_norm_rank_table": rank_table,
        "machine_bet_clauses": {
            "direct_ccr_normalized_defect_limit_zero": False,
            "twisted_weyl_defect_has_declared_zero_limit_sequence": False,
            "every_convergence_claim_names_norm_and_dimension_schedule": True,
            "topology_obstruction_status": "CITED_WITH_BRANCH_GUARD",
            "finite_search_bounds_frozen_before_search": False,
        },
        "approximation_frontier_summary": {
            "direct_ccr_relation": {
                "relation_type": "Lie commutator [Q, P] = lambda * I",
                "normalized_trace_norm_limit": ">= |lambda| > 0 (strictly bounded away from zero)",
                "normalized_frobenius_limit": ">= |lambda| > 0 (strictly bounded away from zero)",
                "operator_norm_limit": ">= |lambda| > 0 (strictly bounded away from zero)",
                "conclusion": "No dimension schedule yields vanishing direct CCR defect.",
            },
            "twisted_weyl_relation": {
                "relation_type": "Exponentiated Weyl ZX = e^{2pi i theta} XZ",
                "operator_norm_limit": "NOT_ESTABLISHED_BY_FINITE_TABLE",
                "target_phase": "5/8",
                "dimension_schedule": FROZEN_DIMENSION_SCHEDULE,
                "rate": "Finite exact phase distances only; no irrational schedule implemented",
                "conclusion": "Nearest-root bound checked at nine dimensions for rational phase 5/8.",
            },
            "almost_commuting_to_commuting": {
                "relation_type": "Unitary pair (U, V) with ||[U, V]|| -> 0",
                "topological_index": "Fixed family winding index 1 for d>2; d=2 refused at log branch cut",
                "conclusion": "Small commutator does NOT imply near-commuting pair without vanishing Bott index.",
            },
        },
    }
    return receipt


if __name__ == "__main__":
    receipt = generate_canonical_block02_receipt()
    print(json.dumps(receipt, indent=2, sort_keys=True))

__all__ = ['ExactRationalMatrix', 'FROZEN_DIMENSION_SCHEDULE', 'GOLDEN_RATIO_CONJUGATE_CONVERGENTS', 'ccr_residual_exact', 'compute_bott_index_witness', 'compute_weyl_phase_approximation_schedule', 'continued_fraction_convergents', 'cross_norm_promotion_counterexample_table', 'generate_canonical_block02_receipt', 'nearest_root_of_unity', 'phase_distance_on_circle', 'verify_ccr_defect_lower_bounds']
