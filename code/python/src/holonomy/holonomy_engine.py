"""Discrete cell complexes, connections, and holonomy in Python.
Follows exact rational arithmetic (fractions.Fraction) under the Zero-Float Law.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Tuple, Sequence, Optional


@dataclass(frozen=True)
class Vertex:
    id: str
    index: int


@dataclass(frozen=True)
class Edge:
    index: int
    source: str
    target: str


@dataclass(frozen=True)
class OrientedStep:
    edge_index: int
    direction: int  # +1 for source->target, -1 for target->source


@dataclass
class Face:
    id: str
    index: int
    boundary_vertices: List[str]
    boundary_edges: List[OrientedStep]


class CellComplex:
    """Discrete cell complex with 0-cells (vertices), 1-cells (edges), and 2-cells (faces)."""

    def __init__(self) -> None:
        self.vertices: List[Vertex] = []
        self.vertex_map: Dict[str, int] = {}
        self.edges: List[Edge] = []
        self.edge_map: Dict[Tuple[str, str], int] = {}
        self.faces: List[Face] = []
        self.face_map: Dict[str, int] = {}

    def add_vertex(self, vid: str) -> int:
        if vid in self.vertex_map:
            raise ValueError(f"Duplicate vertex: {vid}")
        idx = len(self.vertices)
        self.vertices.append(Vertex(vid, idx))
        self.vertex_map[vid] = idx
        return idx

    def add_edge(self, source: str, target: str) -> int:
        if source not in self.vertex_map:
            raise KeyError(f"Source vertex not found: {source}")
        if target not in self.vertex_map:
            raise KeyError(f"Target vertex not found: {target}")
        key = (source, target)
        if key in self.edge_map:
            raise ValueError(f"Duplicate edge: {key}")
        idx = len(self.edges)
        self.edges.append(Edge(idx, source, target))
        self.edge_map[key] = idx
        return idx

    def add_face(self, fid: str, vertices: Sequence[str]) -> int:
        if fid in self.face_map:
            raise ValueError(f"Duplicate face: {fid}")
        if len(vertices) < 3:
            raise ValueError("A face must have at least 3 vertices")

        steps: List[OrientedStep] = []
        n = len(vertices)
        for i in range(n):
            u = vertices[i]
            v = vertices[(i + 1) % n]
            if (u, v) in self.edge_map:
                steps.append(OrientedStep(self.edge_map[(u, v)], +1))
            elif (v, u) in self.edge_map:
                steps.append(OrientedStep(self.edge_map[(v, u)], -1))
            else:
                raise KeyError(f"Edge not found between {u} and {v}")

        idx = len(self.faces)
        face = Face(fid, idx, list(vertices), steps)
        self.faces.append(face)
        self.face_map[fid] = idx
        return idx

    @property
    def euler_characteristic(self) -> int:
        """chi = V - E + F."""
        return len(self.vertices) - len(self.edges) + len(self.faces)


@dataclass
class RationalMatrix:
    """Exact rational matrix using fractions.Fraction."""
    rows: int
    cols: int
    data: List[List[Fraction]]

    @classmethod
    def identity(cls, dim: int) -> RationalMatrix:
        data = [[Fraction(1) if i == j else Fraction(0) for j in range(dim)] for i in range(dim)]
        return cls(dim, dim, data)

    @classmethod
    def from_ints(cls, raw: Sequence[Sequence[int]]) -> RationalMatrix:
        rows = len(raw)
        cols = len(raw[0]) if rows > 0 else 0
        data = [[Fraction(x) for x in row] for row in raw]
        return cls(rows, cols, data)

    def multiply(self, other: RationalMatrix) -> RationalMatrix:
        if self.cols != other.rows:
            raise ValueError(f"Shape mismatch: {self.rows}x{self.cols} vs {other.rows}x{other.cols}")
        res = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return RationalMatrix(self.rows, other.cols, res)

    def inverse(self) -> RationalMatrix:
        """Exact matrix inverse via Gauss-Jordan elimination over Fraction."""
        if self.rows != self.cols:
            raise ValueError("Only square matrices can be inverted")
        n = self.rows
        aug = [row[:] + [Fraction(1) if i == j else Fraction(0) for j in range(n)] for i, row in enumerate(self.data)]

        for col in range(n):
            pivot = None
            for r in range(col, n):
                if aug[r][col] != 0:
                    pivot = r
                    break
            if pivot is None:
                raise ValueError("Singular matrix cannot be inverted")
            aug[col], aug[pivot] = aug[pivot], aug[col]

            scale = aug[col][col]
            for c in range(2 * n):
                aug[col][c] /= scale

            for r in range(n):
                if r != col and aug[r][col] != 0:
                    factor = aug[r][col]
                    for c in range(2 * n):
                        aug[r][c] -= factor * aug[col][c]

        inv_data = [row[n:] for row in aug]
        return RationalMatrix(n, n, inv_data)

    def trace(self) -> Fraction:
        if self.rows != self.cols:
            raise ValueError("Trace only defined for square matrices")
        return sum(self.data[i][i] for i in range(self.rows))

    def equals(self, other: RationalMatrix) -> bool:
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(self.data[i][j] == other.data[i][j] for i in range(self.rows) for j in range(self.cols))


class DiscreteConnection:
    """Discrete connection mapping oriented edges to exact matrices in GL(d, Q)."""

    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.forward: Dict[Tuple[str, str], RationalMatrix] = {}
        self.reverse: Dict[Tuple[str, str], RationalMatrix] = {}

    def set_connection(self, u: str, v: str, matrix: RationalMatrix) -> None:
        if matrix.rows != self.dim or matrix.cols != self.dim:
            raise ValueError(f"Expected {self.dim}x{self.dim} matrix, got {matrix.rows}x{matrix.cols}")
        inv = matrix.inverse()
        self.forward[(u, v)] = matrix
        self.reverse[(v, u)] = inv

    def get_step(self, u: str, v: str) -> RationalMatrix:
        if (u, v) in self.forward:
            return self.forward[(u, v)]
        if (u, v) in self.reverse:
            return self.reverse[(u, v)]
        raise KeyError(f"No connection registered for step {u} -> {v}")

    def path_holonomy(self, path: Sequence[str]) -> RationalMatrix:
        """Parallel transport along path u_0 -> u_1 -> ... -> u_k."""
        if len(path) < 2:
            return RationalMatrix.identity(self.dim)
        res = RationalMatrix.identity(self.dim)
        for i in range(len(path) - 1):
            step = self.get_step(path[i], path[i + 1])
            res = res.multiply(step)
        return res

    def face_holonomy(self, face: Face) -> RationalMatrix:
        """Holonomy around the oriented boundary of a face."""
        res = RationalMatrix.identity(self.dim)
        verts = face.boundary_vertices
        n = len(verts)
        for i in range(n):
            u = verts[i]
            v = verts[(i + 1) % n]
            step = self.get_step(u, v)
            res = res.multiply(step)
        return res

    def is_flat(self, complex: CellComplex) -> bool:
        """A connection is flat if the holonomy around every face is the identity."""
        identity = RationalMatrix.identity(self.dim)
        for face in complex.faces:
            holo = self.face_holonomy(face)
            if not holo.equals(identity):
                return False
        return True
