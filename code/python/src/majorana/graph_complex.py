from __future__ import annotations

from typing import Any, Sequence

from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.core.gf2_schema import mod2
from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier
from omega_engine.crates.majorana.adapters.graph_to_complex import GraphToComplexAdapter


def get_triangle_complex() -> GraphToComplexAdapter:
    """Triangle graph: 3 vertices, 3 edges, 1 face (3-cycle)."""
    vertices = [0, 1, 2]
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [[0, 1, 2]]
    return GraphToComplexAdapter(vertices, edges, faces)


def get_plaquette_complex() -> GraphToComplexAdapter:
    """Square plaquette graph: 4 vertices, 4 edges, 1 face (4-cycle)."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    faces = [[0, 1, 2, 3]]
    return GraphToComplexAdapter(vertices, edges, faces)


def get_prism_complex() -> GraphToComplexAdapter:
    """Prism complex: 6 vertices, 9 edges, 5 faces."""
    vertices = [0, 1, 2, 3, 4, 5]
    edges = [
        (0, 1), (1, 2), (2, 0),
        (3, 4), (4, 5), (5, 3),
        (0, 3), (1, 4), (2, 5),
    ]
    faces = [
        [0, 1, 2],
        [3, 4, 5],
        [0, 7, 3, 6],
        [1, 8, 4, 7],
        [2, 6, 5, 8],
    ]
    return GraphToComplexAdapter(vertices, edges, faces)


def get_line_wire_complex() -> GraphToComplexAdapter:
    """Line wire graph: 3 vertices, 2 edges, 0 faces."""
    vertices = [0, 1, 2]
    edges = [(0, 1), (1, 2)]
    faces: list[list[int]] = []
    return GraphToComplexAdapter(vertices, edges, faces)


def get_t_junction_complex() -> GraphToComplexAdapter:
    """T-junction graph: 4 vertices, 3 edges, 0 faces."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (1, 3)]
    faces: list[list[int]] = []
    return GraphToComplexAdapter(vertices, edges, faces)


def get_measurement_loop_complex() -> GraphToComplexAdapter:
    """Measurement loop graph: 4 vertices, 4 edges, 1 face (4-cycle)."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    faces = [[0, 1, 2, 3]]
    return GraphToComplexAdapter(vertices, edges, faces)


def get_two_island_parity_box_complex() -> GraphToComplexAdapter:
    """Two-island parity box: 4 vertices, 3 edges, 0 faces."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (2, 3), (1, 2)]
    faces: list[list[int]] = []
    return GraphToComplexAdapter(vertices, edges, faces)


def get_braid_like_square_move_complex() -> GraphToComplexAdapter:
    """Braid-like square move (2x3 grid): 6 vertices, 7 edges, 2 faces."""
    vertices = [0, 1, 2, 3, 4, 5]
    edges = [
        (0, 1), (1, 2),
        (3, 4), (4, 5),
        (0, 3), (1, 4), (2, 5),
    ]
    faces = [
        [0, 5, 2, 4],
        [1, 6, 3, 5],
    ]
    return GraphToComplexAdapter(vertices, edges, faces)




