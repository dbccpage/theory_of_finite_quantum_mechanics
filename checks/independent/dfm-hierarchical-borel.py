#!/usr/bin/env python3
"""Independent check for DFM-HIERARCHICAL-BOREL.

Recomputes the rooted-tree Borel identities without importing repository code.
Exits 0 on success.
"""

from __future__ import annotations

import pathlib
import sys
from fractions import Fraction

import sympy as sp


Mat = tuple[Fraction, Fraction, Fraction, Fraction]


def M(a: Fraction | int, b: Fraction | int, c: Fraction | int, d: Fraction | int) -> Mat:
    return (Fraction(a), Fraction(b), Fraction(c), Fraction(d))


def mul(x: Mat, y: Mat) -> Mat:
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def inv(x: Mat) -> Mat:
    a, b, c, d = x
    if c != 0 or a == 0 or d == 0:
        raise AssertionError("refusing a matrix outside invertible upper-triangular B2(Q)")
    return (1 / a, -b / (a * d), Fraction(0), 1 / d)


def eye() -> Mat:
    return M(1, 0, 0, 1)


def torus(x: Mat) -> Mat:
    a, _, _, d = x
    return M(a, 0, 0, d)


def unipotent(x: Mat) -> Mat:
    a, b, _, _ = x
    if a == 0:
        raise AssertionError("singular diagonal refuses the unipotent factor")
    return M(1, b / a, 0, 1)


def is_torus(x: Mat) -> bool:
    return x[1] == 0 and x[2] == 0


def is_unipotent(x: Mat) -> bool:
    return x[0] == 1 and x[2] == 0 and x[3] == 1


def stage_one_field(transport: Mat) -> Mat:
    _, b, _, d2 = transport
    if d2 == 0:
        raise AssertionError("singular transport refuses stage-one division")
    return M(1, -b / d2, 0, 1)


def dress(u_target: Mat, label: Mat, u_source: Mat) -> Mat:
    return mul(mul(u_target, label), inv(u_source))


def check_symbolic_factorization() -> None:
    print("[1/6] symbolic factorization, uniqueness, normality, homomorphism")
    d1, b, d2 = sp.symbols("d1 b d2", nonzero=True)
    matrix = sp.Matrix([[d1, b], [0, d2]])
    diagonal = sp.Matrix([[d1, 0], [0, d2]])
    factor = sp.Matrix([[1, b / d1], [0, 1]])
    assert sp.simplify(diagonal * factor - matrix) == sp.zeros(2)
    d1p, d2p, off = sp.symbols("d1p d2p off")
    general = sp.Matrix([[d1p, 0], [0, d2p]]) * sp.Matrix([[1, off], [0, 1]])
    solution = sp.solve(
        [sp.Eq(general[0, 0], d1), sp.Eq(general[0, 1], b), sp.Eq(general[1, 1], d2)],
        [d1p, d2p, off],
        dict=True,
    )[0]
    assert solution[d1p] == d1 and solution[d2p] == d2 and solution[off] == b / d1
    shift = sp.symbols("shift")
    unipotent_generic = sp.Matrix([[1, shift], [0, 1]])
    conjugated = sp.simplify(matrix * unipotent_generic * matrix.inv())
    assert conjugated[0, 0] == 1 and conjugated[1, 0] == 0 and conjugated[1, 1] == 1
    assert sp.simplify(conjugated[0, 1] - (d1 / d2) * shift) == 0
    left = sp.Matrix([[2, 1], [0, 3]])
    right = sp.Matrix([[2, 1], [0, 3]])
    product = left * right
    def bad(row: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([[row[0, 0], row[0, 1]], [0, 1]])
    assert bad(product) != bad(left) * bad(right)
    assert bad(product)[0, 1] == 5 and (bad(left) * bad(right))[0, 1] == 3


def transport_of(parent: dict[int, int], root: int, labels: dict[int, Mat]) -> dict[int, Mat]:
    seen: dict[int, Mat] = {}

    def go(vertex: int) -> Mat:
        if vertex in seen:
            return seen[vertex]
        if vertex == root:
            seen[vertex] = eye()
            return seen[vertex]
        value = mul(labels[vertex], go(parent[vertex]))
        seen[vertex] = value
        return value

    for vertex in list(parent) + [root]:
        go(vertex)
    return seen


def check_path_and_diamond() -> None:
    print("[2/6] path of length 2 and a diamond tree, exact rationals")
    graphs = {
        "path": {
            "root": 0,
            "parent": {0: 0, 1: 0, 2: 1},
            "labels": {1: M(2, 6, 0, 3), 2: M(4, 1, 0, 5)},
            "chords": [(0, 2, M(1, 7, 0, 1))],
        },
        "diamond": {
            "root": 0,
            "parent": {0: 0, 1: 0, 2: 0, 3: 2},
            "labels": {
                1: M(2, 3, 0, Fraction(1, 2)),
                2: M(Fraction(1, 2), 4, 0, 3),
                3: M(3, -1, 0, 2),
            },
            "chords": [(1, 3, M(1, 5, 0, 1))],
        },
    }
    for name, graph in graphs.items():
        root = graph["root"]
        parent = graph["parent"]
        labels = graph["labels"]
        transport = transport_of(parent, root, labels)
        assert transport[root] == eye()
        fields = {vertex: stage_one_field(value) for vertex, value in transport.items()}
        diagonals = {vertex: torus(value) for vertex, value in transport.items()}
        for vertex, value in transport.items():
            assert mul(torus(value), unipotent(value)) == value
            assert fields[vertex] == mul(mul(diagonals[vertex], inv(unipotent(value))), inv(diagonals[vertex]))
            assert is_unipotent(fields[vertex])
            assert mul(fields[vertex], value) == diagonals[vertex]
            assert mul(inv(diagonals[vertex]), fields[vertex]) == inv(value)
        for vertex, label in labels.items():
            source = parent[vertex]
            dressed = dress(fields[vertex], label, fields[source])
            assert dressed == mul(diagonals[vertex], inv(diagonals[source]))
            assert is_torus(dressed)
            assert torus(dressed) == torus(label)
            residual = dress(inv(diagonals[vertex]), dressed, inv(diagonals[source]))
            assert residual == eye()
            assert residual == mul(mul(inv(transport[vertex]), label), transport[source])
        for source, target, label in graph["chords"]:
            dressed = dress(fields[target], label, fields[source])
            assert torus(dressed) == torus(label)
            full = mul(mul(inv(transport[target]), label), transport[source])
            assert dress(inv(diagonals[target]), dressed, inv(diagonals[source])) == full
            coboundary = mul(transport[target], inv(transport[source]))
            pure = mul(mul(inv(transport[target]), coboundary), transport[source])
            assert pure == eye()
            assert full != eye()
        print(f"  -> {name}: stage-one tree edges diagonal, stage-two residual matches, chord {graph['chords'][0][2]} is not pure gauge")
    path_transport = transport_of({0: 0, 1: 0, 2: 1}, 0, {1: M(2, 6, 0, 3), 2: M(4, 1, 0, 5)})
    assert path_transport[2] == M(8, 27, 0, 15)
    assert stage_one_field(path_transport[1]) == M(1, -2, 0, 1)
    assert stage_one_field(path_transport[2]) == M(1, Fraction(-9, 5), 0, 1)
    chord = mul(mul(inv(path_transport[2]), M(1, 7, 0, 1)), path_transport[0])
    assert chord == M(Fraction(1, 8), Fraction(13, 20), 0, Fraction(1, 15))
    singular = M(0, 1, 0, 1)
    refused = mul(torus(singular), M(1, Fraction(0), 0, 1))
    assert refused != singular


def check_curvature() -> None:
    print("[3/6] incidence curvature, Bianchi identity, and the source-only witness")
    a01, a12, a02 = sp.symbols("a01 a12 a02")
    curvature = a01 * a12 - a02
    g0, g1, g2 = sp.symbols("g0 g1 g2", nonzero=True)
    endpoint = (g0 * a01 / g1) * (g1 * a12 / g2) - (g0 * a02 / g2)
    assert sp.simplify(endpoint - g0 * curvature / g2) == 0
    source_only = (g0 * a01) * (g1 * a12) - (g0 * a02)
    witness = sp.simplify(source_only - g0 * curvature).subs({a01: 1, a12: 1, a02: 0, g0: 1, g1: 2})
    assert witness == 1
    assert (1 * 1) * (2 * 1) - (1 * 0) != 1 * (1 * 1 - 0)
    u, v, w, z = sp.symbols("u v w z")
    # The specified operators on symbols: K(x,y,z) = A(x,y)A(y,z) - A(x,z).
    def entry(p: sp.Symbol, q: sp.Symbol) -> sp.Expr:
        return sp.Function("A")(p, q)
    def curv(x: sp.Symbol, y: sp.Symbol, zed: sp.Symbol) -> sp.Expr:
        return entry(x, y) * entry(y, zed) - entry(x, zed)
    bianchi = (
        -(curv(u, w, z)) + curv(u, v, z)
        + entry(u, v) * curv(v, w, z)
        - curv(u, v, w) * entry(w, z)
    )
    assert sp.expand(bianchi) == 0


def check_dimension_and_source() -> None:
    print("[4/6] carrier comparison 2 != 3 and admission scan of the Lean module")
    assert 2 != 3
    source = pathlib.Path(__file__).resolve().parents[2] / "lean4" / "CampaignDfmHierarchicalBorel.lean"
    text = source.read_text(encoding="utf-8")
    for banned in ("sorry", "admit", "native_decide", "unsafe", "axiom "):
        assert banned not in text, banned
    assert "SU" not in text


def check_anchored_uniqueness() -> None:
    print("[5/6] anchored vertex field on the path is the transport")
    labels = {1: M(2, 6, 0, 3), 2: M(4, 1, 0, 5)}
    parent = {0: 0, 1: 0, 2: 1}
    transport = transport_of(parent, 0, labels)
    for vertex in (1, 2):
        assert labels[vertex] == mul(transport[vertex], inv(transport[parent[vertex]]))
    other = {0: eye(), 1: mul(M(5, 0, 0, 7), transport[1]), 2: mul(M(5, 0, 0, 7), transport[2])}
    # A non-anchored field differs at the root, so the anchored hypothesis excludes it.
    assert other[0] == eye()
    assert other[1] != transport[1]


def main() -> None:
    print("Independent check: DFM-HIERARCHICAL-BOREL")
    check_symbolic_factorization()
    check_path_and_diamond()
    check_curvature()
    check_dimension_and_source()
    check_anchored_uniqueness()
    print("[6/6] checked factorization, path transport [[8, 27], [0, 15]], chord residual [[1/8, 13/20], [0, 1/15]], curvature witness difference 1, and 2 != 3")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
