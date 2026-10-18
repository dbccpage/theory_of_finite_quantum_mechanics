r"""
Canonical U(1) path holonomy operator for omega_engine.

AuthorityEffect: None.
"""

from __future__ import annotations
from typing import Any, Iterable, Sequence
import numpy as np

from .covariant_matrix import _unit_vector


def path_holonomy(
    graph: Any,
    connection: Iterable[complex],
    path: Sequence[tuple[int, int]],
    *,
    require_closed: bool = False,
) -> complex:
    r"""Computes the U(1) path holonomy \prod_{e \in \gamma} U_e^{\pm 1} along an oriented path."""

    phases = _unit_vector(connection, len(graph.edges), "connection")
    if not path:
        raise ValueError("path must contain at least one oriented edge")
    product = 1.0 + 0.0j
    start_vertex: int | None = None
    current_vertex: int | None = None
    for edge_index, direction in path:
        if not 0 <= edge_index < phases.size or direction not in (-1, 1):
            raise ValueError("path uses an invalid edge or orientation")
        tail, head = graph.edges[edge_index]
        step_start, step_end = (tail, head) if direction == 1 else (head, tail)
        if current_vertex is not None and step_start != current_vertex:
            raise ValueError("path is not continuous on the declared graph")
        if start_vertex is None:
            start_vertex = step_start
        current_vertex = step_end
        product *= phases[edge_index] if direction == 1 else np.conj(phases[edge_index])
    if require_closed and current_vertex != start_vertex:
        raise ValueError("path is not closed")
    return complex(product)

