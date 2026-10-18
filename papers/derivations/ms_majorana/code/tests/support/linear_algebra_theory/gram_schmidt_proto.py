"""PROTO Gram–Schmidt for playpen demos.

Rust PROD authority:
  omega_engine/crates/omega_linear_algebra/src/linear_algebra/gram_schmidt.rs

This module is an intentional PROTO float implementation so DomainWorker demos
can run without PyO3. Parity against Rust is a follow-up; do not claim PROD.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from omega_engine.crates.linear_algebra_theory.basic_matrix import (
    BasicMatrix,
    DimensionMismatch,
)


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise DimensionMismatch((len(a), 1), (len(b), 1))
    return float(sum(float(x) * float(y) for x, y in zip(a, b)))


def _norm(a: Sequence[float]) -> float:
    return float(sum(float(x) * float(x) for x in a) ** 0.5)


def _scale(a: Sequence[float], s: float) -> List[float]:
    return [float(x) * s for x in a]


def _sub(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [float(x) - float(y) for x, y in zip(a, b)]


def gram_schmidt_columns(
    columns: Sequence[Sequence[float]],
    *,
    eps: float = 1e-12,
) -> Tuple[List[List[float]], List[str]]:
    """Classical Gram–Schmidt on column vectors.

    Returns orthonormal columns (as lists) and math_path tags.
    """
    if not columns:
        return [], [
            "omega_engine.crates.linear_algebra_theory.gram_schmidt_proto",
            "PROTO:float_classical_gs",
            "PROD_TODO:omega_linear_algebra::gram_schmidt",
        ]

    dim = len(columns[0])
    for c in columns:
        if len(c) != dim:
            raise DimensionMismatch((dim, 1), (len(c), 1))

    q_cols: List[List[float]] = []
    for v in columns:
        u = [float(x) for x in v]
        for q in q_cols:
            proj = _dot(u, q)
            u = _sub(u, _scale(q, proj))
        n = _norm(u)
        if n <= eps:
            raise ValueError("gram_schmidt_proto: linearly dependent / zero column")
        q_cols.append(_scale(u, 1.0 / n))

    math_path = [
        "omega_engine.crates.linear_algebra_theory.gram_schmidt_proto.gram_schmidt_columns",
        "PROTO:float_classical_gs",
        "PROD_TODO:omega_engine/crates/omega_linear_algebra/.../gram_schmidt.rs",
    ]
    return q_cols, math_path


def columns_to_matrix(columns: Sequence[Sequence[float]]) -> BasicMatrix[float]:
    """Stack column vectors into a dense row-major matrix (rows=dim, cols=n)."""
    if not columns:
        return BasicMatrix(0, 0, [])
    rows = len(columns[0])
    cols = len(columns)
    data: List[float] = []
    for r in range(rows):
        for c in range(cols):
            data.append(float(columns[c][r]))
    return BasicMatrix(rows, cols, data)


def orthonormality_residual(q_columns: Sequence[Sequence[float]]) -> List[float]:
    """Flattened residual of Q^T Q - I (row-major)."""
    n = len(q_columns)
    residual: List[float] = []
    for i in range(n):
        for j in range(n):
            d = _dot(q_columns[i], q_columns[j])
            target = 1.0 if i == j else 0.0
            residual.append(d - target)
    return residual


__all__ = [
    "gram_schmidt_columns",
    "columns_to_matrix",
    "orthonormality_residual",
]


