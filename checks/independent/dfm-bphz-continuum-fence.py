"""Independent check for the finite forest formula of DFM-BPHZ-CONTINUUM-FENCE.

No repository module is imported. Rational arithmetic is exact.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import chain, combinations


def powerset(items):
    pool = tuple(items)
    return chain.from_iterable(combinations(pool, r) for r in range(len(pool) + 1))


def compatible(edges):
    def ok(a, b):
        ea, eb = edges[a], edges[b]
        return ea <= eb or eb <= ea or ea.isdisjoint(eb)

    return ok


def forests(names, edges):
    ok = compatible(edges)
    found = []
    for subset in powerset(names):
        if all(ok(subset[i], subset[j]) for i in range(len(subset)) for j in range(i + 1, len(subset))):
            found.append(subset)
    return found


OVERLAP = {
    "L": frozenset({0, 1, 2}),
    "R": frozenset({2, 3, 4}),
    "G": frozenset({0, 1, 2, 3, 4}),
}
NEST = {
    "inner": frozenset({0, 1}),
    "outer": frozenset({0, 1, 2, 3}),
}

overlap = forests(("L", "R", "G"), OVERLAP)
nest = forests(("inner", "outer"), NEST)
if len(overlap) != 6:
    raise SystemExit("overlap forest count")
if ("L", "R") in overlap or ("L", "R", "G") in overlap:
    raise SystemExit("overlapping pair was admitted")
if {("L", "G"), ("R", "G"), ("G",), ("L",), ("R",), ()} != set(overlap):
    raise SystemExit("overlap forest list")
if len(nest) != 4:
    raise SystemExit("nested forest count")
if 2 not in OVERLAP["L"] & OVERLAP["R"] & OVERLAP["G"]:
    raise SystemExit("shared edge")

Q = Fraction


def N(x, y):
    return 2 + 3 * x + 5 * y + 7 * x * y


def six(x, y):
    return N(x, y) - N(0, y) - N(x, 0) - N(0, 0) + N(0, 0) + N(0, 0)


def inclusion(x, y):
    return N(x, y) - N(0, y) - N(x, 0) + N(0, 0)


# Coefficient identity: N - N(0,y) - N(x,0) + N(0,0) = 7xy.
const = 2 - 2 - 2 + 2
coef_x = 3 - 0 - 3 + 0
coef_y = 5 - 5 - 0 + 0
coef_xy = 7 - 0 - 0 + 0
if (const, coef_x, coef_y, coef_xy) != (0, 0, 0, 7):
    raise SystemExit("numerator coefficients")

# Omitting G: N - N(0,y) - N(x,0) = 7xy - 2.
if (2 - 2 - 2, 3 - 3, 5 - 5, 7) != (-2, 0, 0, 7):
    raise SystemExit("three-forest coefficients")

samples = [Q(0), Q(1, 2), Q(-3), Q(4, 7), Q(5), Q(-2, 9)]
for x in samples:
    for y in samples:
        if six(x, y) != 7 * x * y or inclusion(x, y) != 7 * x * y:
            raise SystemExit(f"identity failed at {x}, {y}")
        three = N(x, y) - N(0, y) - N(x, 0)
        if three != 7 * x * y - 2:
            raise SystemExit(f"three-sum failed at {x}, {y}")
        if x * y != 0:
            if six(x, y) / (x * y) != 7:
                raise SystemExit(f"quotient failed at {x}, {y}")
            if three / (x * y) != 7 - 2 / (x * y):
                raise SystemExit(f"remainder failed at {x}, {y}")

x, y = Q(1, 2), Q(1, 3)
if six(x, y) != Q(7, 6):
    raise SystemExit("witness numerator")
if six(x, y) / (x * y) != 7:
    raise SystemExit("witness quotient")
if (N(x, y) - N(0, y) - N(x, 0)) / (x * y) != -5:
    raise SystemExit("witness remainder")


def sector_k(z, lam):
    return (1 + z * lam) / (lam * (1 + lam))


z, lam1, lam2 = Q(3, 5), Q(1, 2), Q(1, 3)
sector = (sector_k(z, lam1) - sector_k(0, lam1)) * (sector_k(z, lam2) - sector_k(0, lam2))
if sector != Q(9, 50):
    raise SystemExit("sector value")
if sector == 7 or z * z != Q(9, 25) or z * z == 7:
    raise SystemExit("sector comparison")

print("overlap forests: 6; excluded pair L with R")
print("nested forests: 4")
print("numerator identity: 7*x*y")
print("witness (1/2, 1/3): six-forest quotient 7; omitted-G quotient -5")
print("sector kernel at z=3/5, lambda=(1/2, 1/3): 9/50, distinct from 7")
print("formal sector value z*z = 9/25, distinct from 7")
print("checked: forests, coefficient identity, sample grid, witness, sector comparison")
