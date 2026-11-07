"""Independent check for the rational-ray part of FQ-GAP-BORN-UNIQUENESS-GLEASON.

Exact integer and rational arithmetic only; no repository imports; no floats.

Checks, for the function exotic(v) = (1 + sgn v)/3 on integer vectors not all even
(sgn v = pairSign of the two odd coordinates when exactly two coordinates are odd, where
pairSign(x, y) = -1 if x = y (mod 4) and +1 otherwise; sgn v = 0 for other parity patterns):
1. exotic(u) + exotic(v) + exotic(w) = 1 on every pairwise orthogonal triple of vectors with
   coordinates in [-B, B] (B = 6), all not all even;
2. the key congruence: for odd a, b, c, d and even e, f with ac + bd + ef = 0 (sampled over a
   box), pairSign(a, b) + pairSign(c, d) = 0;
3. exotic is not quadratic: the 6 x 6 linear system for a symmetric rational form agreeing with
   exotic(v) * (a^2 + b^2 + c^2) on seven explicit rays is inconsistent;
4. the values of exotic lie in {0, 1/3, 2/3}; invariance under negation and odd scalings
   over the box.
Exit code 0 only if every check passes.
"""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction

B = 6
failures = 0
checked = 0


def pair_sign(x: int, y: int) -> int:
    return -1 if (x - y) % 4 == 0 else 1


def sgn(v: tuple[int, int, int]) -> int:
    a, b, c = v
    if a % 2 == 1 and b % 2 == 1 and c % 2 == 0:
        return pair_sign(a, b)
    if a % 2 == 1 and c % 2 == 1 and b % 2 == 0:
        return pair_sign(a, c)
    if b % 2 == 1 and c % 2 == 1 and a % 2 == 0:
        return pair_sign(b, c)
    return 0


def exotic(v: tuple[int, int, int]) -> Fraction:
    return Fraction(1 + sgn(v), 3)


def dot(u, v) -> int:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def is_ray(v) -> bool:
    return not (v[0] % 2 == 0 and v[1] % 2 == 0 and v[2] % 2 == 0)


def check(cond: bool, msg: str) -> None:
    global failures, checked
    checked += 1
    if not cond:
        failures += 1
        print("FAIL:", msg)


# 1. frame additivity over the box
rays = [v for v in itertools.product(range(-B, B + 1), repeat=3) if v != (0, 0, 0) and is_ray(v)]
n_frames = 0
for i, u in enumerate(rays):
    for v in rays[i + 1:]:
        if dot(u, v) != 0:
            continue
        w = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        if not is_ray(w):
            # reduce by the content so that the completing vector is a ray
            from math import gcd
            g = gcd(gcd(abs(w[0]), abs(w[1])), abs(w[2]))
            if g == 0:
                continue
            w = (w[0] // g, w[1] // g, w[2] // g)
        n_frames += 1
        check(exotic(u) + exotic(v) + exotic(w) == 1, f"frame sum {u} {v} {w}")
print(f"frames checked in box [-{B},{B}]^3: {n_frames}")

# 2. key congruence over a box
n_key = 0
R = range(-7, 8)
for a, b, c, d in itertools.product([x for x in R if x % 2 == 1], repeat=4):
    for e, f in itertools.product([x for x in R if x % 2 == 0], repeat=2):
        if a * c + b * d + e * f == 0:
            n_key += 1
            check(pair_sign(a, b) + pair_sign(c, d) == 0, f"key {a,b,c,d,e,f}")
print(f"key-congruence instances checked: {n_key}")

# 3. non-quadraticity on seven rays: unknowns r00 r11 r22 r01 r02 r12
seven = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
rows = []
for (a, b, c) in seven:
    rows.append([Fraction(a * a), Fraction(b * b), Fraction(c * c), Fraction(2 * a * b),
                 Fraction(2 * a * c), Fraction(2 * b * c), exotic((a, b, c)) * (a * a + b * b + c * c)])
# Gaussian elimination on the augmented 7 x 7 system
M = [r[:] for r in rows]
nrow, ncol = 7, 6
rank = 0
pivot_cols = []
for col in range(ncol):
    p = next((r for r in range(rank, nrow) if M[r][col] != 0), None)
    if p is None:
        continue
    M[rank], M[p] = M[p], M[rank]
    pv = M[rank][col]
    M[rank] = [x / pv for x in M[rank]]
    for r in range(nrow):
        if r != rank and M[r][col] != 0:
            f = M[r][col]
            M[r] = [x - f * y for x, y in zip(M[r], M[rank])]
    pivot_cols.append(col)
    rank += 1
inconsistent = any(all(x == 0 for x in M[r][:ncol]) and M[r][ncol] != 0 for r in range(nrow))
check(inconsistent, "seven-ray system should be inconsistent (exotic is not quadratic)")
print("seven-ray quadratic system: rank", rank, "inconsistent:", inconsistent)
vals = {exotic(v) for v in seven}
print("exotic values on the seven rays:", sorted(vals))
check(exotic((1, 0, 0)) == Fraction(1, 3) and exotic((1, 1, 0)) == 0 and exotic((1, 1, 1)) == Fraction(1, 3),
      "expected values 1/3, 0, 1/3")

# 4. values and invariances
for v in rays:
    check(exotic(v) in (Fraction(0), Fraction(1, 3), Fraction(2, 3)), f"value {v}")
    check(exotic((-v[0], -v[1], -v[2])) == exotic(v), f"negation {v}")
    for k in (3, 5, -3):
        check(exotic((k * v[0], k * v[1], k * v[2])) == exotic(v), f"odd scaling {k} {v}")

print(f"checked {checked} conditions, {failures} failures")
sys.exit(0 if failures == 0 else 1)
