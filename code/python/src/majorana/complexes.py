"""Finite cell complexes for Majorana GF(2) play (triangle, plaquette, prism, torus).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .gf2_terminalizer import GF2Matrix, Gf2CocycleClassifier


@dataclass
class ChainComplexGf2:
    name: str
    d0: GF2Matrix
    d1: GF2Matrix
    num_vertices: int
    num_edges: int
    num_faces: int

    def verify_boundary(self) -> bool:
        return Gf2CocycleClassifier.verify_boundary(self.d0, self.d1)


def triangle() -> ChainComplexGf2:
    d0 = GF2Matrix.from_data([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    d1 = GF2Matrix.from_data([[1, 1, 1]])
    return ChainComplexGf2("triangle", d0, d1, 3, 3, 1)


def plaquette() -> ChainComplexGf2:
    d0 = GF2Matrix.from_data([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ])
    d1 = GF2Matrix.from_data([[1, 1, 1, 1]])
    return ChainComplexGf2("plaquette", d0, d1, 4, 4, 1)


def prism() -> ChainComplexGf2:
    # 6 vertices, 9 edges, 5 faces (2 triangular caps, 3 rectangular sides)
    edges = [
        (0, 1), (1, 2), (0, 2),  # base triangle 0, 1, 2
        (3, 4), (4, 5), (3, 5),  # top triangle 3, 4, 5
        (0, 3), (1, 4), (2, 5),  # vertical edges 6, 7, 8
    ]
    d0_data = [[0] * 6 for _ in range(9)]
    for e_idx, (u, v) in enumerate(edges):
        d0_data[e_idx][u] = 1
        d0_data[e_idx][v] = 1
    d0 = GF2Matrix.from_data(d0_data)

    # Faces:
    # f0: (0, 1, 2)
    # f1: (3, 4, 5)
    # f2: (0, 7, 3, 6) -> edges 0, 7, 3, 6
    # f3: (1, 8, 4, 7) -> edges 1, 8, 4, 7
    # f4: (2, 6, 5, 8) -> edges 2, 6, 5, 8
    d1_data = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 1, 1, 0, 1],
    ]
    d1 = GF2Matrix.from_data(d1_data)
    return ChainComplexGf2("prism", d0, d1, 6, 9, 5)


def surface_grid(rows: int, cols: int, periodic: bool) -> ChainComplexGf2:
    if rows < 1 or cols < 1:
        raise ValueError("Grid dimensions must be >= 1")
    if periodic:
        if rows < 2 or cols < 2:
            raise ValueError("Periodic torus grid requires at least 2x2")
        num_v = rows * cols
        # Each vertex (r, c) has 1 horizontal and 1 vertical edge
        num_e = 2 * rows * cols
        num_f = rows * cols

        def v_idx(r: int, c: int) -> int:
            return (r % rows) * cols + (c % cols)

        def h_edge(r: int, c: int) -> int:
            return (r % rows) * cols + (c % cols)

        def v_edge(r: int, c: int) -> int:
            return rows * cols + (r % rows) * cols + (c % cols)

        d0_data = [[0] * num_v for _ in range(num_e)]
        for r in range(rows):
            for c in range(cols):
                # Horizontal edge: (r, c) -> (r, c+1)
                eh = h_edge(r, c)
                d0_data[eh][v_idx(r, c)] = 1
                d0_data[eh][v_idx(r, c + 1)] = 1
                # Vertical edge: (r, c) -> (r+1, c)
                ev = v_edge(r, c)
                d0_data[ev][v_idx(r, c)] = 1
                d0_data[ev][v_idx(r + 1, c)] = 1

        d1_data = [[0] * num_e for _ in range(num_f)]
        for r in range(rows):
            for c in range(cols):
                f = (r % rows) * cols + (c % cols)
                d1_data[f][h_edge(r, c)] = 1
                d1_data[f][v_edge(r, c + 1)] = 1
                d1_data[f][h_edge(r + 1, c)] = 1
                d1_data[f][v_edge(r, c)] = 1

        return ChainComplexGf2(
            f"surface_grid_{rows}x{cols}_torus",
            GF2Matrix.from_data(d0_data),
            GF2Matrix.from_data(d1_data),
            num_v, num_e, num_f,
        )
    else:
        num_v = (rows + 1) * (cols + 1)
        num_e = rows * (cols + 1) + cols * (rows + 1)
        num_f = rows * cols

        def v_idx(r: int, c: int) -> int:
            return r * (cols + 1) + c

        # Horizontal edges: (rows + 1) rows of cols edges
        # Vertical edges: (cols + 1) cols of rows edges
        def h_edge(r: int, c: int) -> int:
            return r * cols + c

        h_total = (rows + 1) * cols

        def v_edge(r: int, c: int) -> int:
            return h_total + r * (cols + 1) + c

        d0_data = [[0] * num_v for _ in range(num_e)]
        for r in range(rows + 1):
            for c in range(cols):
                eh = h_edge(r, c)
                d0_data[eh][v_idx(r, c)] = 1
                d0_data[eh][v_idx(r, c + 1)] = 1
        for r in range(rows):
            for c in range(cols + 1):
                ev = v_edge(r, c)
                d0_data[ev][v_idx(r, c)] = 1
                d0_data[ev][v_idx(r + 1, c)] = 1

        d1_data = [[0] * num_e for _ in range(num_f)]
        for r in range(rows):
            for c in range(cols):
                f = r * cols + c
                d1_data[f][h_edge(r, c)] = 1
                d1_data[f][v_edge(r, c + 1)] = 1
                d1_data[f][h_edge(r + 1, c)] = 1
                d1_data[f][v_edge(r, c)] = 1

        return ChainComplexGf2(
            f"surface_grid_{rows}x{cols}_planar",
            GF2Matrix.from_data(d0_data),
            GF2Matrix.from_data(d1_data),
            num_v, num_e, num_f,
        )


def surface_grid_2x2_planar() -> ChainComplexGf2:
    return surface_grid(2, 2, False)


def surface_grid_2x2_torus() -> ChainComplexGf2:
    return surface_grid(2, 2, True)


def exact_syndrome_example() -> list[int]:
    return [1, 1, 0]


def open_syndrome_example() -> list[int]:
    return [1, 0, 0]


def closed_residual_syndrome_example() -> list[int]:
    return [1, 1, 1, 1]


def torus_logical_x_example() -> list[int]:
    return [0, 1, 0, 1, 0, 0, 0, 0]


def torus_logical_z_example() -> list[int]:
    return [0, 0, 0, 0, 1, 1, 0, 0]


def surface_open_single_edge_example() -> list[int]:
    return [1] + [0] * 7


def surface_exact_from_vertex0(complex: ChainComplexGf2) -> list[int]:
    v = [0] * complex.num_vertices
    v[0] = 1
    return complex.d0.multiply_vector(v)
