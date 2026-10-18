"""Exact rational L1 quotient solver and dual witness verification using Fraction.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np


@dataclass(frozen=True)
class ExactL1Result:
    """Exact rational result of L1 quotient minimization."""

    primal_obj: Fraction
    dual_obj: Fraction
    duality_gap: Fraction
    is_closed: bool
    is_certified: bool
    primal_alpha: List[Fraction]
    primal_residual: List[Fraction]
    dual_witness: List[Fraction]
    authority_effect: str = "None"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primal_obj": str(self.primal_obj),
            "dual_obj": str(self.dual_obj),
            "duality_gap": str(self.duality_gap),
            "is_closed": self.is_closed,
            "is_certified": self.is_certified,
            "primal_alpha": [str(x) for x in self.primal_alpha],
            "primal_residual": [str(x) for x in self.primal_residual],
            "dual_witness": [str(x) for x in self.dual_witness],
            "authority_effect": self.authority_effect,
        }


def _exact_solve_q(
    A: List[List[Fraction]],
    b: List[Fraction],
) -> Optional[List[Fraction]]:
    """Solve A x = b over Fraction using Gauss-Jordan elimination. Free variables set to 0."""
    nrows = len(A)
    if nrows == 0:
        return []
    ncols = len(A[0])
    M = [[A[i][j] for j in range(ncols)] + [b[i]] for i in range(nrows)]

    pivot_cols = []
    r = 0
    for c in range(ncols):
        pivot_r = None
        for i in range(r, nrows):
            if M[i][c] != 0:
                pivot_r = i
                break
        if pivot_r is None:
            continue
        M[r], M[pivot_r] = M[pivot_r], M[r]
        p_val = M[r][c]
        M[r] = [val / p_val for val in M[r]]
        for i in range(nrows):
            if i != r and M[i][c] != 0:
                factor = M[i][c]
                M[i] = [M[i][k] - factor * M[r][k] for k in range(ncols + 1)]
        pivot_cols.append((r, c))
        r += 1
        if r == nrows:
            break

    for i in range(r, nrows):
        if M[i][-1] != 0:
            return None

    sol = [Fraction(0)] * ncols
    for row_idx, col_idx in pivot_cols:
        sol[col_idx] = M[row_idx][-1]
    return sol


def _exact_nullspace_q(A: List[List[Fraction]]) -> List[List[Fraction]]:
    """Find a basis for the nullspace of A over Fraction (vectors x such that A x = 0)."""
    nrows = len(A)
    if nrows == 0:
        return []
    ncols = len(A[0])
    M = [[A[i][j] for j in range(ncols)] for i in range(nrows)]

    pivot_cols: List[Tuple[int, int]] = []
    r = 0
    for c in range(ncols):
        pivot_r = None
        for i in range(r, nrows):
            if M[i][c] != 0:
                pivot_r = i
                break
        if pivot_r is None:
            continue
        M[r], M[pivot_r] = M[pivot_r], M[r]
        p_val = M[r][c]
        M[r] = [val / p_val for val in M[r]]
        for i in range(nrows):
            if i != r and M[i][c] != 0:
                factor = M[i][c]
                M[i] = [M[i][k] - factor * M[r][k] for k in range(ncols)]
        pivot_cols.append((r, c))
        r += 1
        if r == nrows:
            break

    pivot_col_indices = {c for _, c in pivot_cols}
    free_col_indices = [c for c in range(ncols) if c not in pivot_col_indices]

    basis = []
    for free_c in free_col_indices:
        vec = [Fraction(0)] * ncols
        vec[free_c] = Fraction(1)
        for r_idx, c_idx in pivot_cols:
            vec[c_idx] = -M[r_idx][free_c]
        basis.append(vec)

    return basis


def exact_rational_l1_quotient(
    omega: Sequence[Any],
    d0: Sequence[Sequence[Any]],
) -> ExactL1Result:
    """Compute exact rational L1 quotient and dual witness for a simplicial network.

    Converts inputs to fractions.Fraction and uses exact linear algebra.
    Uses floating-point LP solely as a basis discovery heuristic, then reconstructs
    and strictly verifies all certificate equations over Fraction.
    """
    m = len(d0)
    n = len(d0[0]) if m > 0 else 0

    omega_frac = [Fraction(x) for x in omega]
    d0_frac = [[Fraction(x) for x in row] for row in d0]

    if m == 0:
        return ExactL1Result(
            primal_obj=Fraction(0),
            dual_obj=Fraction(0),
            duality_gap=Fraction(0),
            is_closed=True,
            is_certified=True,
            primal_alpha=[Fraction(0)] * n,
            primal_residual=[],
            dual_witness=[],
        )

    exact_closure_alpha = _exact_solve_q(d0_frac, omega_frac)
    if exact_closure_alpha is not None:
        residual_frac = [Fraction(0)] * m
        w_frac = [Fraction(0)] * m
        return ExactL1Result(
            primal_obj=Fraction(0),
            dual_obj=Fraction(0),
            duality_gap=Fraction(0),
            is_closed=True,
            is_certified=True,
            primal_alpha=exact_closure_alpha,
            primal_residual=residual_frac,
            dual_witness=w_frac,
        )

    omega_flt = np.array([float(x) for x in omega_frac])
    d0_flt = np.array([[float(x) for x in row] for row in d0_frac])

    from dual_witness import compute_l1_quotient_with_dual_witness
    num_res = compute_l1_quotient_with_dual_witness(omega_flt, d0_flt)

    active_rows = [i for i, r_val in enumerate(num_res.primal_residual) if abs(r_val) < 1e-6]
    alpha_frac: Optional[List[Fraction]] = None
    if active_rows:
        A_sub = [d0_frac[i] for i in active_rows]
        b_sub = [omega_frac[i] for i in active_rows]
        alpha_frac = _exact_solve_q(A_sub, b_sub)

    if alpha_frac is None:
        alpha_frac = [Fraction(x).limit_denominator(10**12) for x in num_res.primal_alpha]

    w_frac = [Fraction(x).limit_denominator(10**12) for x in num_res.dual_witness]

    d0_T_frac = [[d0_frac[i][j] for i in range(m)] for j in range(n)]
    cycles = _exact_nullspace_q(d0_T_frac)

    if cycles and any(sum(d0_frac[i][j] * w_frac[i] for i in range(m)) != 0 for j in range(n)):
        cycle_matrix = [[cycles[k][i] for k in range(len(cycles))] for i in range(m)]
        c_sol = _exact_solve_q(cycle_matrix, w_frac)
        if c_sol is not None:
            w_frac = [sum(cycles[k][i] * c_sol[k] for k in range(len(cycles))) for i in range(m)]

    residual_frac: List[Fraction] = []
    for i in range(m):
        d0_alpha_i = sum(d0_frac[i][j] * alpha_frac[j] for j in range(n))
        residual_frac.append(omega_frac[i] - d0_alpha_i)

    exact_primal = sum(abs(r) for r in residual_frac)
    exact_dual = sum(w_frac[i] * omega_frac[i] for i in range(m))
    exact_gap = abs(exact_primal - exact_dual)

    dual_divergence_zero = all(
        sum(d0_frac[i][j] * w_frac[i] for i in range(m)) == 0 for j in range(n)
    )
    dual_bounds_satisfied = all(abs(w_frac[i]) <= 1 for i in range(m))
    zero_duality_gap = (exact_gap == 0)

    is_certified = bool(dual_divergence_zero and dual_bounds_satisfied and zero_duality_gap)
    is_closed = bool(is_certified and exact_primal == 0)

    return ExactL1Result(
        primal_obj=exact_primal,
        dual_obj=exact_dual,
        duality_gap=exact_gap,
        is_closed=is_closed,
        is_certified=is_certified,
        primal_alpha=alpha_frac,
        primal_residual=residual_frac,
        dual_witness=w_frac,
    )
