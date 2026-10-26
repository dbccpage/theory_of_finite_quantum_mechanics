"""Independent integer check of the Bool-by-Bool pointwise product and dump-right rival.

No repository modules are imported. AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
import sympy as sp


def delta(i, q):
    return sp.Integer(1) if i == q else sp.Integer(0)


def tensor(u, v, a, b):
    return sp.expand(u[a] * v[b])


def dump_right(u, v, a, b):
    if b:
        return sp.Integer(0)
    return sp.expand(u[a] * (v[False] + v[True]))


def main() -> None:
    failures = 0
    checks = 0
    uf, ut, vf, vt = sp.symbols("uf ut vf vt")
    u = {False: uf, True: ut}
    v = {False: vf, True: vt}

    for a, b in itertools.product((False, True), repeat=2):
        checks += 1
        if tensor(u, v, a, b) != u[a] * v[b]:
            failures += 1
        expanded = sp.expand(
            uf * (vf * delta((False, False), (a, b)) + vt * delta((False, True), (a, b)))
            + ut * (vf * delta((True, False), (a, b)) + vt * delta((True, True), (a, b)))
        )
        checks += 1
        if sp.expand(expanded - u[a] * v[b]) != 0:
            failures += 1
        checks += 1
        if b is False:
            expect = sp.expand(u[a] * (v[False] + v[True]))
        else:
            expect = sp.Integer(0)
        if sp.expand(dump_right(u, v, a, b) - expect) != 0:
            failures += 1

    basis = {
        False: {False: sp.Integer(1), True: sp.Integer(0)},
        True: {False: sp.Integer(0), True: sp.Integer(1)},
    }
    checks += 1
    if tensor(basis[False], basis[True], False, True) != 1:
        failures += 1
    checks += 1
    if dump_right(basis[False], basis[True], False, True) != 0:
        failures += 1
    checks += 1
    if dump_right(basis[False], basis[True], False, True) == tensor(
        basis[False], basis[True], False, True
    ):
        failures += 1

    for i, j, a, b in itertools.product((False, True), repeat=4):
        checks += 1
        got = dump_right(basis[i], basis[j], a, b)
        expect = delta((i, False), (a, b))
        if got != expect:
            failures += 1
        checks += 1
        if tensor(basis[i], basis[j], a, b) != delta((i, j), (a, b)):
            failures += 1

    coords = (-2, -1, 0, 1, 2)
    samples = 0
    for values in itertools.product(coords, repeat=4):
        left = {False: sp.Integer(values[0]), True: sp.Integer(values[1])}
        right = {False: sp.Integer(values[2]), True: sp.Integer(values[3])}
        other = {False: sp.Integer(values[3]), True: sp.Integer(values[2])}
        scale = sp.Integer(values[0])
        for a, b in itertools.product((False, True), repeat=2):
            summed = {False: left[False] + other[False], True: left[True] + other[True]}
            checks += 1
            if dump_right(summed, right, a, b) != dump_right(left, right, a, b) + dump_right(
                other, right, a, b
            ):
                failures += 1
            checks += 1
            if tensor(summed, right, a, b) != tensor(left, right, a, b) + tensor(other, right, a, b):
                failures += 1
            scaled = {False: scale * left[False], True: scale * left[True]}
            checks += 1
            if dump_right(scaled, right, a, b) != scale * dump_right(left, right, a, b):
                failures += 1
            checks += 1
            if tensor(right, scaled, a, b) != scale * tensor(right, left, a, b):
                failures += 1
        samples += 1

    point_count = 2 * 2
    checks += 1
    if point_count != 4:
        failures += 1

    print(f"checks={checks} failures={failures} samples={samples} witness_dump=0 witness_tensor=1 points=4")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
