"""Finite graded-square examples and a semigroup coefficient calculator.

No non-Abelian structure or automatic quantum-to-cochain bridge is supplied.
The seven-step trace is a schema, not an executed simulation.
AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from ._validation import integer, matrix, nonnegative
from .simplicial_complex import SimplicialComplex, simplicial_coboundary_matrix


class DoubleBicomplex:
    """Constant-coefficient commuting double complex used as a baseline.

    Vertical maps alternate identity and zero, so successive vertical maps
    compose to zero. They commute with the horizontal coboundary.
    """

    def __init__(self, complex_: SimplicialComplex, num_memory_grades: int = 3) -> None:
        self.complex = complex_
        self.num_memory_grades = integer(num_memory_grades, "num_memory_grades", 1)

    def horizontal_coboundary(self, p: int) -> np.ndarray:
        return simplicial_coboundary_matrix(self.complex, integer(p, "p"))

    def vertical_differential(self, p: int, q: int) -> np.ndarray:
        p, q = integer(p, "p"), integer(q, "q")
        if q >= self.num_memory_grades:
            raise ValueError("q is outside the memory grades")
        size = self.complex.num_simplices(p)
        if q == self.num_memory_grades - 1 or q % 2:
            return np.zeros((size, size))
        return np.eye(size)


def bicomplex_curvature_tensor(
    d_h_q: np.ndarray,
    d_h_qp1: np.ndarray,
    d_v_p: np.ndarray,
    d_v_pp1: np.ndarray,
) -> np.ndarray:
    """Square defect C = d_h(q+1) d_v(p) - d_v(p+1) d_h(q).

    For D = d_h + (-1)^p d_v, the mixed block of D^2 is (-1)^p C.
    This alone does not establish d_h^2=d_v^2=0.
    Zero-dimensional spaces are allowed in a graded square.
    """
    maps = [np.asarray(x, dtype=complex) for x in (d_h_q, d_h_qp1, d_v_p, d_v_pp1)]
    if any(x.ndim != 2 or not np.isfinite(x).all() for x in maps):
        raise ValueError("graded maps must be finite matrices")
    h0, h1, v0, v1 = maps
    if h1.shape[1] != v0.shape[0] or v1.shape[1] != h0.shape[0]:
        raise ValueError("graded square compositions are undefined")
    if h1.shape[0] != v1.shape[0] or v0.shape[1] != h0.shape[1]:
        raise ValueError("graded square paths have different endpoints")
    return h1 @ v0 - v1 @ h0


def semigroup_defect_tensor(
    tangent_proj: np.ndarray,
    generator: np.ndarray,
    normal_residual: np.ndarray,
    hessian_retraction: np.ndarray,
) -> tuple[np.ndarray, bool]:
    """Assemble P A n + B and numerically check P K=K.

    A true C^2 retraction supplies B=D^2 Pi(Am,n). Arbitrary B is not
    certified as a Hessian. Projector and normal-input conditions are checked.
    """
    p = matrix(tangent_proj, "projector")
    if p.shape[0] != p.shape[1]:
        raise ValueError("projector must be square")
    a = matrix(generator, "generator", p.shape)
    n = np.asarray(normal_residual, dtype=complex)
    b = np.asarray(hessian_retraction, dtype=complex)
    if (
        n.shape != (p.shape[0],)
        or b.shape != n.shape
        or not np.isfinite(n).all()
        or not np.isfinite(b).all()
    ):
        raise ValueError("normal and Hessian vectors must be finite and match the projector")
    if not np.allclose(p @ p, p, atol=1e-10, rtol=0):
        raise ValueError("P must be idempotent")
    if not np.allclose(p @ n, 0, atol=1e-10, rtol=0):
        raise ValueError("n must be in ker(P)")
    result = p @ a @ n + b
    return result, bool(np.allclose(p @ result, result, atol=1e-10, rtol=0))


def ddc_trace_sequence_evaluation(
    k_cell_id: str,
    initial_residual_norm: float,
    budget: int = 100,
) -> dict[str, Any]:
    """Return a seven-label local trace schema, never a verified receipt.

    Each emitted schema entry uses one display-budget slot. No quantum
    contraction, harmonic estimate, or marginal gluing is executed.
    """
    if not isinstance(k_cell_id, str) or not k_cell_id.strip():
        raise ValueError("k_cell_id must be nonempty")
    residual = nonnegative(initial_residual_norm, "initial_residual_norm")
    budget = integer(budget, "budget")
    planned = ["E", "R", "C", "Lambda", "D", "M", "T"]
    operations = [
        "DeclareState",
        "DeclareBoundary",
        "RequireRetraction",
        "RequireLaplacian",
        "RequireEvolution",
        "RequireGluingCheck",
        "RequireReceipt",
    ]
    log = [
        {"step": step, "operation": op, "status": "NOT_EVALUATED"}
        for step, op in zip(planned[:budget], operations[:budget], strict=True)
    ]
    return {
        "k_cell_id": k_cell_id,
        "declared_initial_residual_norm": residual,
        "trace_sequence": [entry["step"] for entry in log],
        "trace_log": log,
        "schema_complete": len(log) == 7,
        "budget_used": len(log),
        "receipt_verified": False,
        "scope": "seven-step schema only",
        "authority_effect": "None",
    }
