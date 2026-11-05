"""Bounded exact rooted-tree two-stage Borel dressing and symbolic controls.

AuthorityEffect: None. Finite B2(Q) and commutative incidence identities do not
establish a continuum gauge theory. Symbolic controls use fixed expressions.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path as _Path
import sys as _sys
from types import MappingProxyType
from typing import Any, cast

import sympy as sp

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import flat_matrix2, integer, rational
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix

Mat = tuple[Fraction, Fraction, Fraction, Fraction]


def M(a: object, b: object, c: object, d: object) -> Mat:
    return flat_matrix2((a, b, c, d))


def mul(x: object, y: object) -> Mat:
    left, right = RationalMatrix.from_flat2(x), RationalMatrix.from_flat2(y)
    return left.mul(right).flat2()


def _upper(value: object, invertible: bool = False) -> Mat:
    matrix = flat_matrix2(value)
    a, _, c, d = matrix
    if c != 0:
        raise Violation("input", "upper-triangular matrix required")
    if invertible and (a == 0 or d == 0):
        raise Violation("input", "invertible B2(Q) matrix required")
    return matrix


def inv(x: object) -> Mat:
    return RationalMatrix.from_flat2(_upper(x, True)).inverse2().flat2()


def eye() -> Mat:
    return M(1, 0, 0, 1)


def torus(x: object) -> Mat:
    a, _, _, d = _upper(x)
    return M(a, 0, 0, d)


def unipotent(x: object) -> Mat:
    a, b, _, _ = _upper(x, True)
    return M(1, rational(b / a), 0, 1)


def is_torus(x: object) -> bool:
    _, b, c, _ = flat_matrix2(x)
    return b == 0 and c == 0


def is_unipotent(x: object) -> bool:
    a, _, c, d = flat_matrix2(x)
    return a == 1 and c == 0 and d == 1


def stage_one_field(transport: object) -> Mat:
    _, b, _, d = _upper(transport, True)
    return M(1, rational(-b / d), 0, 1)


def dress(u_target: object, label: object, u_source: object) -> Mat:
    target, edge, source = _upper(u_target, True), _upper(label), _upper(u_source, True)
    return mul(mul(target, edge), inv(source))


def _vertex(value: object) -> int:
    return integer(value, "vertex identifier", 0, 2**31-1)


def _mapping(value: object, name: str) -> Mapping[object, object]:
    if type(value) not in (dict, MappingProxyType):
        raise Violation("input", name+" must be a dict or mappingproxy")
    mapping = cast(Mapping[object, object], value)
    if len(mapping) > 1024:
        raise Violation("resource", name+" exceeds1024 vertices")
    return dict(mapping)


def _tree_order(parent: Mapping[int, int], root: int) -> tuple[int, ...]:
    seen = {root}
    order = [root]
    for vertex in parent:
        chain: list[int] = []
        visiting: set[int] = set()
        cursor = vertex
        while cursor not in seen:
            if cursor in visiting:
                raise Violation("input", "parent map has a cycle off the root")
            visiting.add(cursor)
            chain.append(cursor)
            cursor = parent[cursor]
        for child in reversed(chain):
            seen.add(child)
            order.append(child)
    return tuple(order)


@dataclass(frozen=True, slots=True, init=False)
class BorelTree:
    """Aggregate: <=1024 owned vertices, one fixed root, invertible B2(Q) labels."""
    root: int
    parent: Mapping[int, int]
    labels: Mapping[int, Mat]
    order: tuple[int, ...]

    def __init__(self, parent: object, root: object, labels: object) -> None:
        origin = _vertex(root)
        parents = {_vertex(v): _vertex(p) for v, p in _mapping(parent, "parent map").items()}
        raw_labels = {_vertex(v): label for v, label in _mapping(labels, "labels").items()}
        if origin not in parents or parents[origin] != origin or any(p not in parents for p in parents.values()):
            raise Violation("input", "parent map must contain the fixed root and every parent")
        if set(raw_labels) != set(parents)-{origin}:
            raise Violation("input", "exactly the non-root vertices require labels")
        order = _tree_order(parents, origin)
        owned = {vertex: _upper(label, True) for vertex, label in raw_labels.items()}
        object.__setattr__(self, "root", origin)
        object.__setattr__(self, "parent", MappingProxyType(parents))
        object.__setattr__(self, "labels", MappingProxyType(owned))
        object.__setattr__(self, "order", order)

    def _transport(self) -> Mapping[int, Mat]:
        result = {self.root: eye()}
        for vertex in self.order[1:]:
            result[vertex] = mul(self.labels[vertex], result[self.parent[vertex]])
        return MappingProxyType(result)

    def transport(self) -> Outcome[Mapping[int, Mat]]:
        return evaluate(self._transport)

    def _edge_residual(self, source: object, target: object, label: object) -> Mat:
        start, finish = _vertex(source), _vertex(target)
        edge = _upper(label)
        if start not in self.parent or finish not in self.parent:
            raise Violation("input", "edge endpoints must belong to the tree")
        transport = self._transport()
        return mul(mul(inv(transport[finish]), edge), transport[start])

    def edge_residual(self, source: object, target: object, label: object) -> Outcome[Mat]:
        return evaluate(self._edge_residual, source, target, label)


def transport_of(parent: object, root: object, labels: object) -> dict[int, Mat]:
    return dict(BorelTree(parent, root, labels)._transport())


def _cases(cases: object) -> Cases:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    return cases


def check_symbolic_factorization(cases: Cases) -> None:
    run = _cases(cases)
    d1, d2 = sp.symbols("d1 d2", nonzero=True)
    b = sp.symbols("b")
    matrix = sp.Matrix([[d1, b], [0, d2]])
    diagonal = sp.Matrix([[d1, 0], [0, d2]])
    factor = sp.Matrix([[1, b / d1], [0, 1]])
    run.require(sp.simplify(diagonal * factor - matrix) == sp.zeros(2), 'symbolic Borel factorization')
    d1p, d2p, off = sp.symbols("d1p d2p off")
    general = sp.Matrix([[d1p, 0], [0, d2p]]) * sp.Matrix([[1, off], [0, 1]])
    solution = sp.solve(
        [sp.Eq(general[0, 0], d1), sp.Eq(general[0, 1], b), sp.Eq(general[1, 1], d2)],
        [d1p, d2p, off],
        dict=True,
    )
    run.require(solution == [{d1p: d1, d2p: d2, off: b / d1}], 'unique factorization coefficients')
    shift = sp.symbols("shift")
    unipotent_generic = sp.Matrix([[1, shift], [0, 1]])
    conjugated = sp.simplify(matrix * unipotent_generic * matrix.inv())
    run.require(conjugated[0, 0] == 1 and conjugated[1, 0] == 0 and (conjugated[1, 1] == 1), 'normality diagonal entries')
    run.require(sp.simplify(conjugated[0, 1] - d1 / d2 * shift) == 0, 'normality off-diagonal action')
    left = sp.Matrix([[2, 1], [0, 3]])
    right = sp.Matrix([[2, 1], [0, 3]])
    product = left * right
    def bad(row: Any) -> Any:
        return sp.Matrix([[row[0, 0], row[0, 1]], [0, 1]])
    run.require(bad(product) != bad(left) * bad(right), 'bad projection is not multiplicative')
    run.require(bad(product)[0, 1] == 5 and (bad(left) * bad(right))[0, 1] == 3, 'bad projection counterexample entries')

    e1, e2 = sp.symbols("e1 e2", nonzero=True)
    eoff = sp.symbols("eoff")
    other = sp.Matrix([[e1, eoff], [0, e2]])
    composite = matrix * other
    run.require(sp.diag(composite[0, 0], composite[1, 1]) == diagonal * sp.diag(e1, e2), "torus projection homomorphism")

def _check_vertex(value: Mat, run: Cases) -> None:
    field, diagonal = stage_one_field(value), torus(value)
    run.require(mul(diagonal, unipotent(value)) == value, "Borel factorization")
    run.require(field == mul(mul(diagonal, inv(unipotent(value))), inv(diagonal)), "unipotent conjugate")
    run.require(is_unipotent(field), "stage one is unipotent")
    run.require(mul(field, value) == diagonal, "stage one removes unipotent part")
    run.require(mul(inv(diagonal), field) == inv(value), "two-stage inverse")


def _check_tree_edge(tree: BorelTree, vertex: int, transport: Mapping[int, Mat], run: Cases) -> None:
    source, label = tree.parent[vertex], tree.labels[vertex]
    target_field, source_field = stage_one_field(transport[vertex]), stage_one_field(transport[source])
    target_diagonal, source_diagonal = torus(transport[vertex]), torus(transport[source])
    dressed = dress(target_field, label, source_field)
    run.require(dressed == mul(target_diagonal, inv(source_diagonal)), "diagonal tree edge")
    run.require(is_torus(dressed), "stage one edge in torus")
    run.require(torus(dressed) == torus(label), "quotient preserved")
    residual = dress(inv(target_diagonal), dressed, inv(source_diagonal))
    run.require(residual == eye(), "tree residual identity")
    run.require(residual == mul(mul(inv(transport[vertex]), label), transport[source]), "residual equals full dressing")


def _check_chord(tree: BorelTree, source: int, target: int, label: Mat, transport: Mapping[int, Mat], run: Cases) -> None:
    dressed = dress(stage_one_field(transport[target]), label, stage_one_field(transport[source]))
    run.require(torus(dressed) == torus(label), "chord quotient preserved")
    full = tree._edge_residual(source, target, label)
    run.require(dress(inv(torus(transport[target])), dressed, inv(torus(transport[source]))) == full, "chord two-stage residual")
    coboundary = mul(transport[target], inv(transport[source]))
    run.require(tree._edge_residual(source, target, coboundary) == eye(), "pure-gauge chord")
    run.require(full != eye(), "supplied chord is not pure gauge")


def _path_tree() -> BorelTree:
    return BorelTree({0: 0, 1: 0, 2: 1}, 0, {1: M(2, 6, 0, 3), 2: M(4, 1, 0, 5)})


def _diamond_tree() -> BorelTree:
    return BorelTree({0: 0, 1: 0, 2: 0, 3: 2}, 0,
                     {1: M(2, 3, 0, Fraction(1, 2)), 2: M(Fraction(1, 2), 4, 0, 3), 3: M(3, -1, 0, 2)})


def check_path_and_diamond(cases: Cases) -> None:
    run = _cases(cases)
    fixtures = ((_path_tree(), 0, 2, M(1, 7, 0, 1)), (_diamond_tree(), 1, 3, M(1, 5, 0, 1)))
    for tree, source, target, chord in fixtures:
        transport = tree._transport()
        run.require(transport[tree.root] == eye(), "root identity")
        for value in transport.values():
            _check_vertex(value, run)
        for vertex in tree.labels:
            _check_tree_edge(tree, vertex, transport, run)
        _check_chord(tree, source, target, chord, transport, run)
    path = _path_tree()
    transport = path._transport()
    run.require(transport[2] == M(8, 27, 0, 15), "path endpoint transport")
    run.require(stage_one_field(transport[1]) == M(1, -2, 0, 1), "first stage-one field")
    run.require(stage_one_field(transport[2]) == M(1, Fraction(-9, 5), 0, 1), "second stage-one field")
    run.require(path._edge_residual(0, 2, M(1, 7, 0, 1)) == M(Fraction(1, 8), Fraction(13, 20), 0, Fraction(1, 15)), "chord residual")
    singular = M(0, 1, 0, 1)
    run.require(mul(torus(singular), eye()) != singular, "singular factorization counterexample")


def check_curvature(cases: Cases) -> None:
    run = _cases(cases)
    a01, a12, a02 = sp.symbols("a01 a12 a02")
    curvature = a01 * a12 - a02
    g0, g1, g2 = sp.symbols("g0 g1 g2", nonzero=True)
    endpoint = (g0 * a01 / g1) * (g1 * a12 / g2) - (g0 * a02 / g2)
    run.require(sp.simplify(endpoint - g0 * curvature / g2) == 0, 'symbolic endpoint covariance')
    source_only = (g0 * a01) * (g1 * a12) - (g0 * a02)
    witness = sp.simplify(source_only - g0 * curvature).subs({a01: 1, a12: 1, a02: 0, g0: 1, g1: 2})
    run.require(witness == 1, 'source-only covariance counterexample')
    assignment = {a01: 1, a12: 1, a02: 0, g0: 1, g1: 2, g2: 1}
    run.require(endpoint.subs(assignment) == curvature.subs(assignment), "finite endpoint covariance")
    u, v, w, z = sp.symbols("u v w z")
    # The specified operators on symbols: K(x,y,z) = A(x,y)A(y,z) - A(x,z).
    def entry(p: Any, q: Any) -> Any:
        return sp.Function("A")(p, q)
    def curv(x: Any, y: Any, zed: Any) -> Any:
        return entry(x, y) * entry(y, zed) - entry(x, zed)
    bianchi = (
        -(curv(u, w, z)) + curv(u, v, z)
        + entry(u, v) * curv(v, w, z)
        - curv(u, v, w) * entry(w, z)
    )
    run.require(sp.expand(bianchi) == 0, 'commutative discrete Bianchi identity')


def check_anchored_uniqueness(cases: Cases) -> None:
    run = _cases(cases)
    labels = {1: M(2, 6, 0, 3), 2: M(4, 1, 0, 5)}
    parent = {0: 0, 1: 0, 2: 1}
    transport = transport_of(parent, 0, labels)
    for vertex in (1, 2):
        run.require(labels[vertex] == mul(transport[vertex], inv(transport[parent[vertex]])), 'anchored edge coboundary')
    # Right-multiplying every vertex field by one constant preserves all edges
    # but changes the root, exhibiting why the anchoring hypothesis is needed.
    constant = M(5, 0, 0, 7)
    other = {vertex: mul(value, constant) for vertex, value in transport.items()}
    run.require(other[0] != eye(), "the alternative field must fail anchoring")
    for vertex in (1, 2):
        run.require(labels[vertex] == mul(other[vertex], inv(other[parent[vertex]])),
                "right multiplication must preserve the edge labels")
        run.require(other[vertex] != transport[vertex], "the unanchored field must differ")


def main() -> None:
    run = Cases()
    check_symbolic_factorization(run)
    check_path_and_diamond(run)
    check_curvature(run)
    check_anchored_uniqueness(run)
    print(json.dumps({"status": "passed", "checks": run.checks,
                      "scope": "bounded B2(Q) trees and fixed commutative symbolic identities; no continuum gauge theory"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
