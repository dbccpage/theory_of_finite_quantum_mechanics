"""Independent check for the finite forest formula of DFM-BPHZ-CONTINUUM-FENCE.

No repository module is imported. Rational arithmetic is exact.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import chain, combinations, product
from collections.abc import Callable, Iterator


def powerset(items: tuple[str, ...]) -> Iterator[tuple[str, ...]]:
    pool = tuple(items)
    return chain.from_iterable(combinations(pool, r) for r in range(len(pool) + 1))


def compatible(edges: dict[str, frozenset[int]]) -> Callable[[str, str], bool]:
    def ok(a: str, b: str) -> bool:
        ea, eb = edges[a], edges[b]
        return ea <= eb or eb <= ea or ea.isdisjoint(eb)

    return ok


def forests(names: tuple[str, ...], edges: dict[str, frozenset[int]]) -> list[tuple[str, ...]]:
    ok = compatible(edges)
    found: list[tuple[str, ...]] = []
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


def exact(value: object) -> Fraction:
    if type(value) is int or type(value) is Fraction:
        return Fraction(value)
    raise ValueError("exact int or Fraction required")


def N(x: Fraction | int, y: Fraction | int) -> Fraction:
    x, y = exact(x), exact(y)
    return Fraction(2) + 3 * x + 5 * y + 7 * x * y


def six(x: Fraction | int, y: Fraction | int) -> Fraction:
    # {L,G} and {R,G} are the two nested forests. Both evaluate at (0, 0).
    empty = N(x, y)
    only_l = N(0, y)
    only_r = N(x, 0)
    only_g = N(0, 0)
    nested_lg = N(0, 0)
    nested_rg = N(0, 0)
    return empty - only_l - only_r - only_g + nested_lg + nested_rg


def inclusion(x: Fraction | int, y: Fraction | int) -> Fraction:
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


def sector_k(z: Fraction | int, lam: Fraction) -> Fraction:
    z, lam = exact(z), exact(lam)
    if lam in (0, -1):
        raise ValueError("sector denominator vanishes")
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


Matrix = tuple[Fraction, Fraction, Fraction, Fraction]
IDENTITY: Matrix = (Q(1), Q(0), Q(0), Q(1))
ZERO: Matrix = (Q(0), Q(0), Q(0), Q(0))


def multiply(a: Matrix, b: Matrix) -> Matrix:
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def residual(p: Matrix) -> Matrix:
    return (1-p[0], -p[1], -p[2], 1-p[3])


def checked_reduce(projectors: tuple[Matrix, ...]) -> Matrix:
    for p in projectors:
        if any(type(x) is not Fraction for x in p):
            raise ValueError("exact Fraction entries required")
        if multiply(p, p) != p:
            raise ValueError("non-idempotent projector")
        for q in projectors:
            if multiply(p, q) != multiply(q, p):
                raise ValueError("noncommuting projectors")
    result = IDENTITY
    for p in reversed(projectors):
        result = multiply(residual(p), result)
    return result


def check_family(family: tuple[Matrix, ...]) -> None:
    result = checked_reduce(family)
    if multiply(result, result) != result:
        raise SystemExit("reduction is not idempotent")
    if any(multiply(p, result) != ZERO for p in family):
        raise SystemExit("reduction misses a supplied kernel")
    for p in family:
        if multiply(residual(p), result) != result:
            raise SystemExit("subfamily does not absorb")
    if family:
        if checked_reduce(family + family) != result:
            raise SystemExit("repeated family changes reduction")
    elif result != IDENTITY:
        raise SystemExit("empty subtraction is not identity")


def check_projector_api() -> None:
    matrices: list[Matrix] = [(Q(a), Q(b), Q(c), Q(d)) for a,b,c,d in product((-1,0,1), repeat=4)]
    projectors = [p for p in matrices if multiply(p,p) == p]
    checked = 0
    for size in range(3):
        for family in product(projectors, repeat=size):
            if all(multiply(p,q) == multiply(q,p) for p in family for q in family):
                check_family(family)
                checked += 1
    bad: Matrix = (Q(2),Q(0),Q(0),Q(0))
    p: Matrix = (Q(1),Q(0),Q(0),Q(0))
    q: Matrix = (Q(1),Q(1),Q(0),Q(0))
    for family in ((bad,), (p,q)):
        try:
            checked_reduce(family)
        except ValueError:
            continue
        raise SystemExit("invalid projector family admitted")
    print(f"projectors: {len(projectors)} exact idempotents; {checked} compatible lists; two invalid families refused")


check_projector_api()


def check_invalid_scalars() -> None:
    bad: tuple[object, ...] = (True, 0.5, "1")
    for value in bad:
        try:
            exact(value)
        except ValueError:
            continue
        raise SystemExit("inexact scalar admitted")
    for pole in (Q(0), Q(-1)):
        try:
            sector_k(1, pole)
        except ValueError:
            continue
        raise SystemExit("sector pole admitted")
    print("three inexact scalar inputs and two sector poles refused")


check_invalid_scalars()
