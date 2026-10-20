"""Exact permutation-valued finite graph witness for TFQ-0397/0398.

The general arbitrary-group proof is in lean4/FiniteGraphDressing.lean.
This executable witness accepts loops, parallel edges and disconnected graphs.
AuthorityEffect: None. No continuum or general FSP/MUB claim is made.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Permutation:
    image: tuple[int, ...]

    def __post_init__(self):
        if not isinstance(self.image, tuple) or any(type(i) is not int for i in self.image):
            raise ValueError("a permutation is an exact integer tuple")
        if sorted(self.image) != list(range(len(self.image))):
            raise ValueError("permutation is not a bijection")

    @classmethod
    def identity(cls, degree: int):
        if type(degree) is not int or degree < 0:
            raise ValueError("degree must be a nonnegative integer")
        return cls(tuple(range(degree)))

    def __mul__(self, other: Permutation):
        if len(self.image) != len(other.image):
            raise ValueError("permutation degrees differ")
        return Permutation(tuple(self.image[i] for i in other.image))

    def inverse(self):
        out = [0] * len(self.image)
        for i, j in enumerate(self.image):
            out[j] = i
        return Permutation(tuple(out))


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    value: Permutation


@dataclass(frozen=True)
class Dressing:
    transports: tuple[Permutation, ...]
    roots: tuple[int, ...]
    tree_edges: tuple[int, ...]
    residuals: tuple[Permutation, ...]

    def neutralizes(self):
        return all(p == Permutation.identity(len(p.image)) for p in self.residuals)


def forest_dressing(vertices: int, degree: int, edges: tuple[Edge, ...],
                    order: tuple[int, ...] | None = None) -> Dressing:
    """BFS spanning forest; edge order selects a forest, never drops an edge.

    T(v) is ordered root-to-vertex transport; R(e)=T(t)^-1 U(e) T(s).
    The result neutralizes iff all fundamental-loop residuals are identity.
    """
    if type(vertices) is not int or vertices < 0:
        raise ValueError("vertex count must be a nonnegative integer")
    identity = Permutation.identity(degree)
    if order is None:
        order = tuple(range(len(edges)))
    if any(type(i) is not int for i in order) or sorted(order) != list(range(len(edges))):
        raise ValueError("order must include each edge exactly once")
    adjacent = [[] for _ in range(vertices)]
    for i in order:
        e = edges[i]
        if any(type(v) is not int or not 0 <= v < vertices for v in (e.source, e.target)):
            raise ValueError("edge endpoint outside the declared graph")
        if not isinstance(e.value, Permutation) or len(e.value.image) != degree:
            raise ValueError("edge must carry a permutation of the declared degree")
        adjacent[e.source].append((i, e.target, e.value))
        adjacent[e.target].append((i, e.source, e.value.inverse()))
    transports: list[Permutation | None] = [None] * vertices
    roots = [-1] * vertices
    tree = []
    for root in range(vertices):
        if transports[root] is not None:
            continue
        transports[root] = identity
        roots[root] = root
        queue = deque([root])
        while queue:
            source = queue.popleft()
            for i, target, value in adjacent[source]:
                if transports[target] is None:
                    transports[target] = value * transports[source]
                    roots[target] = root
                    tree.append(i)
                    queue.append(target)
    ts = tuple(transports)
    residuals = tuple(ts[e.target].inverse() * e.value * ts[e.source] for e in edges)
    return Dressing(ts, tuple(roots), tuple(tree), residuals)


def gauge_transform(edges: tuple[Edge, ...], gauge: tuple[Permutation, ...]):
    return tuple(Edge(e.source, e.target, gauge[e.target] * e.value * gauge[e.source].inverse())
                 for e in edges)
