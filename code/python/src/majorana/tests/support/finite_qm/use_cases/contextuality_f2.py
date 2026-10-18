r"""
Mermin--Peres contextuality as an :math:`\mathbb F_2` parity obstruction.

AuthorityEffect: None.

Canonical Implementation: omega_engine_projects.ms_majorana.code.tests.support.finite_qm.use_cases.contextuality_f2
"""

from __future__ import annotations
from itertools import product as _iterproduct
from typing import Any, Dict, List, Tuple

import numpy as np

try:
    from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.primitives import I2, SIGMA_X, SIGMA_Y, SIGMA_Z
except ImportError:
    from omega_engine_projects.ms_majorana.code.tests.support.finite_qm.domain.primitives import I2, SIGMA_X, SIGMA_Y, SIGMA_Z


def peres_mermin_square() -> List[List[np.ndarray]]:
    """The nine observables, as 4x4 complex matrices."""
    return [
        [np.kron(SIGMA_X, I2), np.kron(I2, SIGMA_X), np.kron(SIGMA_X, SIGMA_X)],
        [np.kron(I2, SIGMA_Y), np.kron(SIGMA_Y, I2), np.kron(SIGMA_Y, SIGMA_Y)],
        [np.kron(SIGMA_X, SIGMA_Y), np.kron(SIGMA_Y, SIGMA_X), np.kron(SIGMA_Z, SIGMA_Z)],
    ]


def context_products() -> Dict[str, Any]:
    r"""Compute the six context products and read off their signs."""
    sq = peres_mermin_square()
    eye4 = np.eye(4, dtype=complex)

    signs: List[int] = []
    labels: List[str] = []
    commuting: List[bool] = []

    for i in range(3):
        ctx = sq[i]
        prod = ctx[0] @ ctx[1] @ ctx[2]
        signs.append(1 if np.allclose(prod, eye4, atol=1e-9) else -1)
        labels.append(f"row{i}")
        commuting.append(_all_commute(ctx))

    for j in range(3):
        ctx = [sq[i][j] for i in range(3)]
        prod = ctx[0] @ ctx[1] @ ctx[2]
        signs.append(1 if np.allclose(prod, eye4, atol=1e-9) else -1)
        labels.append(f"col{j}")
        commuting.append(_all_commute(ctx))

    return {
        "labels": labels,
        "signs": signs,
        "all_contexts_commute": bool(all(commuting)),
        "n_negative_contexts": int(sum(1 for s in signs if s == -1)),
        "parity_of_signs": int(np.prod(signs)),
        "authority_effect": "None",
    }


def _all_commute(ops: List[np.ndarray], atol: float = 1e-9) -> bool:
    for a, op_a in enumerate(ops):
        for op_b in ops[a + 1:]:
            if not np.allclose(op_a @ op_b, op_b @ op_a, atol=atol):
                return False
    return True


def f2_system() -> Tuple[np.ndarray, np.ndarray]:
    r"""The :math:`\mathbb F_2` constraint system :math:`Ax = b` on the nine cells."""
    a = np.zeros((6, 9), dtype=int)
    for i in range(3):
        for j in range(3):
            a[i, 3 * i + j] = 1
            a[3 + j, 3 * i + j] = 1
    signs = context_products()["signs"]
    b = np.array([0 if s == 1 else 1 for s in signs], dtype=int)
    return a, b


def f2_rank(mat: np.ndarray) -> int:
    """Rank over F2 by Gaussian elimination."""
    m = (np.asarray(mat, dtype=int) % 2).copy()
    rows, cols = m.shape
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if m[i, c] == 1), None)
        if piv is None:
            continue
        m[[r, piv]] = m[[piv, r]]
        for i in range(rows):
            if i != r and m[i, c] == 1:
                m[i] = (m[i] + m[r]) % 2
        r += 1
        if r == rows:
            break
    return r


def parity_obstruction() -> Dict[str, Any]:
    r"""Derive the inconsistency: :math:`\operatorname{rank}(A) < \operatorname{rank}([A|b])`."""
    a, b = f2_system()
    aug = np.hstack([a, b.reshape(-1, 1)])
    r_a, r_aug = f2_rank(a), f2_rank(aug)

    return {
        "rank_A": r_a,
        "rank_augmented": r_aug,
        "system_inconsistent": bool(r_aug > r_a),
        "row_sum_parity": int(np.sum(b[:3]) % 2),
        "col_sum_parity": int(np.sum(b[3:]) % 2),
        "parities_disagree": bool((np.sum(b[:3]) % 2) != (np.sum(b[3:]) % 2)),
        "obstruction_class": "nonzero in F_2",
        "authority_effect": "None",
    }


def enumerate_all_assignments() -> Dict[str, Any]:
    r"""Exhaustively check all :math:`2^9 = 512` value assignments."""
    a, b = f2_system()
    total = 0
    best = 0
    best_count = 0
    for bits in _iterproduct((0, 1), repeat=9):
        x = np.array(bits, dtype=int)
        satisfied = int(np.sum(((a @ x) % 2) == b))
        if satisfied == 6:
            total += 1
        if satisfied > best:
            best, best_count = satisfied, 1
        elif satisfied == best:
            best_count += 1

    return {
        "n_assignments_enumerated": 512,
        "n_fully_consistent": total,
        "max_contexts_satisfiable": best,
        "n_assignments_achieving_max": best_count,
        "n_contexts": 6,
        "verdict": (
            "no non-contextual value assignment exists; at most 5 of 6 contexts satisfiable"
        ),
        "authority_effect": "None",
    }


def contextuality_report() -> Dict[str, Any]:
    """The three checks together."""
    prods = context_products()
    obstruction = parity_obstruction()
    enumeration = enumerate_all_assignments()
    return {
        "context_products": prods,
        "f2_obstruction": obstruction,
        "exhaustive_enumeration": enumeration,
        "consistent": bool(
            prods["n_negative_contexts"] == 1
            and obstruction["system_inconsistent"]
            and enumeration["n_fully_consistent"] == 0
        ),
        "imports": ["two-qubit Pauli host (OB-NONCOMM)", "tensor product (OB-COMPOSE)"],
        "authority_effect": "None",
    }


__all__ = [
    "peres_mermin_square",
    "context_products",
    "f2_system",
    "f2_rank",
    "parity_obstruction",
    "enumerate_all_assignments",
    "contextuality_report",
]
