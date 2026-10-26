"""Independent integer check of the Bool-by-Bool pointwise product and dump-right rival.

No repository modules are imported. AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
import sympy as sp

BOOLS = (False, True)
POINTS = tuple(itertools.product(BOOLS, repeat=2))


def delta(i, q):
    return sp.Integer(1) if i == q else sp.Integer(0)


def tensor(u, v, a, b):
    return sp.expand(u[a] * v[b])


def dump_right(u, v, a, b):
    if b:
        return sp.Integer(0)
    return sp.expand(u[a] * (v[False] + v[True]))


def vec(f, t):
    return {False: f, True: t}


def add(x, y):
    return vec(x[False] + y[False], x[True] + y[True])


def scale(c, x):
    return vec(c * x[False], c * x[True])


def basis(i):
    return vec(delta(i, False), delta(i, True))


def laws(embed, u1, u2, v1, v2, c):
    """Yield (name, lhs - rhs) for additivity and homogeneity in each argument."""
    for a, b in POINTS:
        yield "add_left", embed(add(u1, u2), v1, a, b) - embed(u1, v1, a, b) - embed(u2, v1, a, b)
        yield "add_right", embed(u1, add(v1, v2), a, b) - embed(u1, v1, a, b) - embed(u1, v2, a, b)
        yield "smul_left", embed(scale(c, u1), v1, a, b) - c * embed(u1, v1, a, b)
        yield "smul_right", embed(u1, scale(c, v1), a, b) - c * embed(u1, v1, a, b)


def main() -> None:
    failures = 0
    checks = 0

    def expect(ok):
        nonlocal failures, checks
        checks += 1
        if not ok:
            failures += 1

    uf, ut, wf, wt, vf, vt, xf, xt, c = sp.symbols("uf ut wf wt vf vt xf xt c")
    u, w, v, x = vec(uf, ut), vec(wf, wt), vec(vf, vt), vec(xf, xt)

    # Bilinearity in both arguments, with symbolic integer coordinates and scalar.
    for embed in (tensor, dump_right):
        for _, diff in laws(embed, u, w, v, x, c):
            expect(sp.expand(diff) == 0)

    # Coordinate formulas.
    for a, b in POINTS:
        expect(tensor(u, v, a, b) == sp.expand(u[a] * v[b]))
        want = sp.Integer(0) if b else sp.expand(u[a] * (vf + vt))
        expect(sp.expand(dump_right(u, v, a, b) - want) == 0)

    # Uniqueness: a map with the four laws is fixed by its values on delta pairs.
    # Expanding u and v on the deltas and inserting the identity tag delta (i, j)
    # gives the pointwise product at every point.
    for a, b in POINTS:
        expanded = sum(
            u[i] * v[j] * delta((i, j), (a, b)) for i, j in POINTS
        )
        expect(sp.expand(expanded - u[a] * v[b]) == 0)

    # Tags on delta pairs: identity tag for tensor, collapsed tag for dump-right.
    collapsed = 0
    for i, j in POINTS:
        for a, b in POINTS:
            expect(tensor(basis(i), basis(j), a, b) == delta((i, j), (a, b)))
            expect(dump_right(basis(i), basis(j), a, b) == delta((i, False), (a, b)))
        if any(dump_right(basis(i), basis(j), a, b) != tensor(basis(i), basis(j), a, b) for a, b in POINTS):
            collapsed += 1

    # Witness values, computed rather than printed as constants.
    witness_tensor = tensor(basis(False), basis(True), False, True)
    witness_dump = dump_right(basis(False), basis(True), False, True)
    expect(witness_tensor == 1)
    expect(witness_dump == 0)
    expect(witness_dump != witness_tensor)

    # Integer samples for both maps and all four laws.
    coords = (-2, -1, 0, 1, 2)
    samples = 0
    for vals in itertools.product(coords, repeat=4):
        p = vec(sp.Integer(vals[0]), sp.Integer(vals[1]))
        q = vec(sp.Integer(vals[2]), sp.Integer(vals[3]))
        r = vec(sp.Integer(vals[3]), sp.Integer(vals[0]))
        k = sp.Integer(vals[1] - vals[2])
        for embed in (tensor, dump_right):
            for _, diff in laws(embed, p, r, q, p, k):
                expect(diff == 0)
        samples += 1

    print(
        f"checks={checks} failures={failures} samples={samples} "
        f"witness_dump={witness_dump} witness_tensor={witness_tensor} "
        f"points={len(POINTS)} collapsed_delta_pairs={collapsed}"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
