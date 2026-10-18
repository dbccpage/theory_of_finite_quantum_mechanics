r"""
Canonical gauge-connection Laplacian operator \Delta_U = D(U)^\dagger W D(U) for omega_engine.

AuthorityEffect: None.
"""

from __future__ import annotations
from typing import Any, Iterable
import numpy as np

from .covariant_matrix import covariant_matrix


def connection_laplacian(
    graph: Any,
    connection: Iterable[complex],
    weights: Iterable[float] | None = None,
) -> np.ndarray:
    r"""Computes the gauge-covariant Laplacian matrix \Delta_U = D(U)^\dagger W D(U)."""

    derivative = covariant_matrix(graph, connection)
    if weights is None:
        edge_weights = np.ones(len(graph.edges))
    else:
        edge_weights = np.asarray(tuple(weights), dtype=float)
        if edge_weights.shape != (len(graph.edges),) or np.any(edge_weights <= 0):
            raise ValueError("connection weights must be positive on every edge")
    return derivative.conj().T @ np.diag(edge_weights) @ derivative

