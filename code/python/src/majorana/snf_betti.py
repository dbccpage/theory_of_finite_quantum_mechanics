from __future__ import annotations
r"""
Exact integer Smith Normal Form and Betti numbers.

AuthorityEffect: None.

"""


from typing import Any, Dict, List, Sequence

import numpy as np


def _as_exact_integer(mat: np.ndarray, atol: float = 1e-12) -> np.ndarray:
    a = np.asarray(mat)
    if a.size == 0:
        return a.astype(np.int64)
    if np.iscomplexobj(a):
        raise TypeError("exact integer SNF requires a real integral matrix, got complex")
    nearest = np.rint(a)
    if not np.all(np.abs(a - nearest) <= atol):
        worst = int(np.argmax(np.abs(a - nearest)))
        raise ValueError(
            "exact integer SNF requires an integral matrix; entry "
            f"{a.flat[worst]!r} is not an integer (tolerance {atol}). "
        )
    return nearest.astype(np.int64)


def _integer_matrix_rank(mat: np.ndarray) -> int:
    from sympy import Matrix
    from sympy.matrices.normalforms import smith_normal_form as _snf

    if mat.size == 0 or min(mat.shape) == 0:
        return 0
    m = Matrix(_as_exact_integer(mat).tolist())
    snf = _snf(m)
    return int(sum(1 for i in range(min(snf.shape)) if snf[i, i] != 0))


def smith_normal_form_diagonal(mat: np.ndarray) -> List[int]:
    from sympy import Matrix
    from sympy.matrices.normalforms import smith_normal_form as _snf

    if mat.size == 0 or min(mat.shape) == 0:
        return []
    m = Matrix(_as_exact_integer(mat).tolist())
    snf = _snf(m)
    return [int(snf[i, i]) for i in range(min(snf.shape)) if snf[i, i] != 0]


def betti_numbers(graph) -> Dict[str, Any]:
    d0 = graph.d0_matrix()
    d1 = graph.d1_matrix() if graph.n_faces else np.zeros((0, graph.n_edges))

    r0 = _integer_matrix_rank(d0)
    r1 = _integer_matrix_rank(d1)

    b0 = graph.n_vertices - r0
    b1 = graph.n_edges - r0 - r1
    b2 = graph.n_faces - r1

    factors0 = smith_normal_form_diagonal(d0)
    factors1 = smith_normal_form_diagonal(d1)
    torsion = [d for d in (factors0 + factors1) if abs(d) > 1]

    euler_cells = graph.n_vertices - graph.n_edges + graph.n_faces
    euler_betti = b0 - b1 + b2

    return {
        "b0": int(b0),
        "b1": int(b1),
        "b2": int(b2),
        "rank_d0": r0,
        "rank_d1": r1,
        "invariant_factors_d0": factors0,
        "invariant_factors_d1": factors1,
        "torsion_summands": [f"Z/{abs(d)}" for d in torsion],
        "has_torsion": bool(torsion),
        "euler_from_cells": int(euler_cells),
        "euler_from_betti": int(euler_betti),
        "euler_identity_holds": bool(euler_cells == euler_betti),
        "method": "exact integer SNF (sympy), not float SVD rank",
        "authority_effect": "None",
    }


def float_rank_disagrees(mat: np.ndarray, tol: float = 1e-10) -> Dict[str, Any]:
    exact = _integer_matrix_rank(mat)
    approx = int(np.linalg.matrix_rank(mat, tol=tol)) if mat.size else 0
    return {
        "exact_integer_rank": exact,
        "float_rank": approx,
        "agree": bool(exact == approx),
        "authority_effect": "None",
    }


__all__ = [
    "betti_numbers",
    "smith_normal_form_diagonal",
    "float_rank_disagrees",
]



