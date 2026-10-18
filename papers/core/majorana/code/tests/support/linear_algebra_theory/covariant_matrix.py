r"""
Canonical covariant matrix and covariant difference operators for omega_engine.

AuthorityEffect: None.
"""

from __future__ import annotations
from typing import Iterable
import numpy as np


def _unit_vector(values: Iterable[complex], expected: int, name: str) -> np.ndarray:
    vector = np.asarray(tuple(values), dtype=complex)
    if vector.shape != (expected,):
        raise ValueError(f"{name} dimension mismatch")
    if not np.all(np.isfinite(vector)) or not np.allclose(np.abs(vector), 1.0):
        raise ValueError(f"{name} values must lie in U(1)")
    return vector


def covariant_matrix(
    graph: Any, connection: Iterable[complex]
) -> np.ndarray:
    """Computes the |E| x |V| gauge-covariant derivative matrix D(U)."""
    edge_phase = _unit_vector(connection, len(graph.edges), "connection")
    matrix = np.zeros((len(graph.edges), graph.n_vertices), dtype=complex)
    for row, (tail, head) in enumerate(graph.edges):
        matrix[row, tail] = -edge_phase[row]
        matrix[row, head] = 1.0
    return matrix


def covariant_difference(
    graph: Any,
    connection: Iterable[complex],
    field: Iterable[complex],
) -> np.ndarray:
    r"""Computes the gauge-covariant difference (D(U) \psi)_e."""
    vertex_field = np.asarray(tuple(field), dtype=complex)
    if vertex_field.shape != (graph.n_vertices,):
        raise ValueError("complex vertex field dimension mismatch")
    return covariant_matrix(graph, connection) @ vertex_field


def gauge_transform(
    graph: Any,
    connection: Iterable[complex],
    gauge: Iterable[complex],
) -> np.ndarray:
    r"""Applies a U(1) gauge transformation U'_{u,v} = g_v U_{u,v} g_u^\dagger."""

    edge_phase = _unit_vector(connection, len(graph.edges), "connection")
    vertex_phase = _unit_vector(gauge, graph.n_vertices, "gauge")
    return np.asarray(
        [
            vertex_phase[head] * edge_phase[i] * np.conj(vertex_phase[tail])
            for i, (tail, head) in enumerate(graph.edges)
        ],
        dtype=complex,
    )

