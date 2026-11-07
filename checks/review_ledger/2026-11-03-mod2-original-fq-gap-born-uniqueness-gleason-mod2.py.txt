"""Independent check for the residue-modulo-2 class rigidity on Q(i)^3
(FQ-GAP-BORN-UNIQUENESS-GLEASON, module BornGaussianMod2ClassRigidity).

Exact integer and rational arithmetic only; no repository imports; no floats.

The 56 frames below (Gaussian-integer vectors (a+bi, c+di, e+gi) written as ((a,b),(c,d),(e,g)))
are the ones used in the Lean module.  This script recomputes, independently of Lean:
  1. each vector is nonzero and has a component not divisible by 1+i (a+b odd for some component);
  2. the three vectors of each frame are pairwise orthogonal for <u,v> = sum conj(u_k) v_k;
  3. the residue classes mod 2 of the six coordinates cover all 4^3 - 2^3 = 56 admissible classes;
  4. the 56 x 56 class-incidence matrix A (row = frame, column = class, entry = multiplicity)
     is invertible over Q, and A^{-1} (1,...,1) = (1/3,...,1/3): so any class function satisfying
     the 56 frame equations is identically 1/3.
Exit code 0 only if every check passes.
"""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction

failures = 0
checked = 0


def check(cond: bool, msg: str) -> None:
    global failures, checked
    checked += 1
    if not cond:
        failures += 1
        print("FAIL:", msg)


def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gconj(a):
    return (a[0], -a[1])


def inner(u, v):
    s = (0, 0)
    for a, b in zip(u, v):
        t = gmul(gconj(a), b)
        s = (s[0] + t[0], s[1] + t[1])
    return s


def admissible(v) -> bool:
    return any((c[0] + c[1]) % 2 == 1 for c in v)


def cls(v):
    return tuple(x % 2 for c in v for x in c)


FRAMES = [
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, -1)), ((0, 0), (1, 0), (0, 0))),
    (((0, -1), (0, 0), (0, 0)), ((0, 0), (-1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((-1, 0), (1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((0, -1), (0, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((-1, 0), (0, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((0, -1), (-1, 0), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, 0), (0, 0), (-1, 0)), ((-1, 0), (0, 0), (1, 0)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (-1, 0)), ((0, -1), (0, 0), (0, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, -1)), ((-1, 0), (0, 0), (0, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, -1)), ((0, -1), (0, 0), (-1, 0)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, 0), (-1, 0)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, 0), (0, -1)), ((0, 0), (0, 1), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (-1, 0)), ((0, 0), (0, -1), (1, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (0, -1)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, 0)), ((-1, 0), (1, -1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, 0)), ((0, -1), (1, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, -1), (0, -1), (0, 0)), ((-1, 0), (1, 1), (0, 0)), ((0, 0), (0, 0), (1, 0))),
    (((-1, -1), (0, 0), (-1, 0)), ((-1, 0), (0, 0), (1, -1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, -1), (0, 0), (-1, 0)), ((0, -1), (0, 0), (1, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, -1), (0, 0), (0, -1)), ((-1, 0), (0, 0), (1, 1)), ((0, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, -1), (-1, 0)), ((0, 0), (1, 0), (-1, 1))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (-1, -1), (0, -1)), ((0, 0), (1, 0), (-1, -1))),
    (((-1, 0), (0, 0), (0, 0)), ((0, 0), (0, -1), (-1, -1)), ((0, 0), (-1, -1), (1, 0))),
    (((-1, -1), (-1, 0), (-1, 0)), ((-1, -1), (1, 0), (1, 0)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, -1), (-1, 0), (-1, 0)), ((-1, 1), (0, -1), (0, -1)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, -1)), ((-1, -1), (1, 0), (0, 1)), ((0, 0), (0, 1), (1, 0))),
    (((-1, -1), (-1, 0), (0, -1)), ((-1, 1), (0, -1), (1, 0)), ((0, 0), (0, 1), (1, 0))),
    (((-1, 0), (-1, -1), (-1, 0)), ((-1, 0), (1, 1), (-1, 0)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, -1), (-1, 0)), ((0, -1), (-1, 1), (0, -1)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, -1), (0, -1)), ((-1, 0), (1, 1), (0, -1)), ((0, 1), (0, 0), (1, 0))),
    (((-1, 0), (-1, -1), (0, -1)), ((0, -1), (-1, 1), (1, 0)), ((0, 1), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (-1, -1)), ((-1, 0), (-1, 0), (1, 1)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, 0), (-1, 0), (-1, -1)), ((0, -1), (0, -1), (-1, 1)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, 0), (0, -1), (-1, -1)), ((-1, 0), (0, -1), (1, 1)), ((0, 1), (1, 0), (0, 0))),
    (((-1, 0), (0, -1), (-1, -1)), ((0, -1), (1, 0), (-1, 1)), ((0, 1), (1, 0), (0, 0))),
    (((-1, 0), (-1, 0), (-1, 0)), ((-2, 0), (1, 0), (1, 0)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, 0), (-1, 0), (-1, 0)), ((-1, 0), (-1, 0), (2, 0)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, 0), (-1, 0), (-1, 0)), ((-1, 0), (2, 0), (-1, 0)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, 0), (-1, 0), (0, -1)), ((-2, 0), (1, 0), (0, 1)), ((0, 0), (0, 1), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((-1, 0), (1, 0), (0, -2)), ((0, 1), (0, -1), (1, 0))),
    (((-1, 0), (-1, 0), (0, 0)), ((0, -1), (0, 1), (0, -1)), ((-1, 0), (1, 0), (2, 0))),
    (((-1, 0), (0, -1), (-1, 0)), ((-2, 0), (0, 1), (1, 0)), ((0, 0), (0, -1), (1, 0))),
    (((-1, 0), (0, -1), (0, -1)), ((-2, 0), (0, 1), (0, 1)), ((0, 0), (-1, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((-1, 0), (0, 1), (0, -2)), ((0, 1), (1, 0), (1, 0))),
    (((-1, 0), (0, -1), (0, 0)), ((0, -1), (-1, 0), (0, -1)), ((0, 1), (1, 0), (0, -2))),
    (((-1, -1), (-1, -1), (-1, 0)), ((-1, -1), (0, 1), (1, -1)), ((1, 0), (-1, 1), (-1, -1))),
    (((-1, -1), (-1, -1), (-1, 0)), ((-1, -1), (1, 0), (1, 1)), ((1, 0), (-1, -1), (1, 1))),
    (((-1, -1), (-1, -1), (-1, 0)), ((0, -1), (-1, 1), (1, -1)), ((-1, -1), (1, 0), (1, 1))),
    (((-1, -1), (-1, -1), (0, -1)), ((-1, -1), (0, 1), (1, 1)), ((1, 0), (-1, 1), (1, -1))),
    (((-1, -1), (-1, -1), (-1, 0)), ((-1, 0), (-1, 0), (2, -2)), ((-1, 0), (1, 0), (0, 0))),
    (((-1, -1), (-1, 0), (-1, -1)), ((-1, 0), (2, -2), (-1, 0)), ((-1, 0), (0, 0), (1, 0))),
    (((-1, -1), (-1, 0), (0, 0)), ((-1, 0), (1, -1), (-1, 0)), ((1, 0), (-1, 1), (-3, 0))),
    (((-1, -1), (0, 0), (-1, 0)), ((-1, 0), (-1, 0), (1, -1)), ((1, 0), (-3, 0), (-1, 1))),
    (((0, 0), (-1, -1), (-1, 0)), ((-1, 0), (-1, 0), (1, -1)), ((-3, 0), (1, 0), (-1, 1))),
]

check(len(FRAMES) == 56, "56 frames")
for u, v, w in FRAMES:
    for x in (u, v, w):
        check(x != ((0, 0), (0, 0), (0, 0)), f"nonzero {x}")
        check(admissible(x), f"admissible {x}")
    check(inner(u, v) == (0, 0), f"orthogonal {u} {v}")
    check(inner(u, w) == (0, 0), f"orthogonal {u} {w}")
    check(inner(v, w) == (0, 0), f"orthogonal {v} {w}")

all_classes = sorted({c for c in itertools.product(range(2), repeat=6)
                      if any((c[2 * k] + c[2 * k + 1]) % 2 == 1 for k in range(3))})
check(len(all_classes) == 56, "56 admissible classes")
seen = sorted({cls(x) for f in FRAMES for x in f})
check(seen == all_classes, "frames cover all 56 classes")
cidx = {c: i for i, c in enumerate(all_classes)}
n = 56
A = [[Fraction(0)] * n for _ in range(n)]
for r, (u, v, w) in enumerate(FRAMES):
    for x in (u, v, w):
        A[r][cidx[cls(x)]] += 1
# Gauss-Jordan inversion
M = [A[r][:] + [Fraction(int(r == j)) for j in range(n)] for r in range(n)]
singular = False
for col in range(n):
    p = next((r for r in range(col, n) if M[r][col] != 0), None)
    if p is None:
        singular = True
        break
    M[col], M[p] = M[p], M[col]
    pv = M[col][col]
    M[col] = [x / pv for x in M[col]]
    for r in range(n):
        if r != col and M[r][col] != 0:
            f = M[r][col]
            M[r] = [x - f * y for x, y in zip(M[r], M[col])]
check(not singular, "incidence matrix invertible")
if not singular:
    Ainv = [row[n:] for row in M]
    sol = [sum(row) for row in Ainv]  # A^{-1} * (1,...,1)
    check(all(s == Fraction(1, 3) for s in sol), "unique solution is the constant 1/3")
    # sanity: A * sol = 1
    for r in range(n):
        check(sum(A[r][c] * sol[c] for c in range(n)) == 1, f"row {r} sums to 1")
    print("max |inverse entry| =", max(abs(x) for row in Ainv for x in row),
          "; max denominator =", max(x.denominator for row in Ainv for x in row))

print(f"checked {checked} conditions, {failures} failures")
sys.exit(0 if failures == 0 else 1)
