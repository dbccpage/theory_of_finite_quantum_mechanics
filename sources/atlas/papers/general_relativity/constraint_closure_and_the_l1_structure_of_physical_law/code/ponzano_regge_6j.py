"""SP3b: Ponzano-Regge SU(2) 6j Recoupling via Exact Rational Arithmetic.

Exact Racah single-sum formula for the Wigner 6j symbol:
  {j1 j2 j3; j4 j5 j6} = Δ(j1,j2,j3)Δ(j1,j5,j6)Δ(j4,j2,j6)Δ(j4,j5,j3)
    × Σ_z (-1)^z (z+1)! / [∏(z-p_i)! ∏(q_k-z)!]

Result on regular tetrahedron: {1 1 1; 1 1 1} = 1/6

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from fractions import Fraction


def triangle_valid(j1: int, j2: int, j3: int) -> bool:
    """Check the triangle inequality for nonnegative integer-spin inputs."""
    return min(j1, j2, j3) >= 0 and abs(j1 - j2) <= j3 <= j1 + j2


def _sqrt_fraction_exact(value: Fraction) -> Fraction:
    """Return an exact rational square root, refusing irrational results."""
    numerator_root = math.isqrt(value.numerator)
    denominator_root = math.isqrt(value.denominator)
    if (
        numerator_root * numerator_root != value.numerator
        or denominator_root * denominator_root != value.denominator
    ):
        raise ValueError("Racah prefactor is not rational for these integer spins")
    return Fraction(numerator_root, denominator_root)


def triangle_delta_squared(a: int, b: int, c: int) -> Fraction:
    """Racah triangle coefficient Δ(a,b,c)^2 = (a+b-c)!(a-b+c)!(-a+b+c)! / (a+b+c+1)!"""
    num = (
        Fraction(math.factorial(a + b - c))
        * Fraction(math.factorial(a - b + c))
        * Fraction(math.factorial(-a + b + c))
    )
    den = Fraction(math.factorial(a + b + c + 1))
    return num / den


def wigner_6j_exact(j1: int, j2: int, j3: int, j4: int, j5: int, j6: int) -> Fraction:
    """Exact Wigner 6j symbol via Racah single-sum formula.

    Arguments are integer spins (for half-integer, multiply all by 2 and adjust).

    {j1 j2 j3}
    {j4 j5 j6}
    """
    # Check all four triangle conditions
    triads = [(j1, j2, j3), (j1, j5, j6), (j4, j2, j6), (j4, j5, j3)]
    for triad in triads:
        if not triangle_valid(*triad):
            return Fraction(0)

    # Prefactor: product of four Δ(triad) values
    # Δ(a,b,c)² = (a+b-c)!(a-b+c)!(-a+b+c)! / (a+b+c+1)!
    # Product of 4 Δ² values, then take sqrt at the end
    prefactor_sq = Fraction(1)
    for triad in triads:
        prefactor_sq *= triangle_delta_squared(*triad)

    # Perimeter sums p_i
    p = [
        j1 + j2 + j3,
        j1 + j5 + j6,
        j4 + j2 + j6,
        j4 + j5 + j3,
    ]

    # Opposite-edge sums q_k
    q = [
        j1 + j2 + j4 + j5,
        j2 + j3 + j5 + j6,
        j1 + j3 + j4 + j6,
    ]

    z_min = max(p)
    z_max = min(q)

    total = Fraction(0)
    for z in range(z_min, z_max + 1):
        num = Fraction((-1) ** z) * Fraction(math.factorial(z + 1))
        den = Fraction(1)
        for pi in p:
            den *= Fraction(math.factorial(z - pi))
        for qk in q:
            den *= Fraction(math.factorial(qk - z))
        total += num / den

    # Result = sqrt(prefactor_sq) * total.  A Fraction return value is honest
    # only when the prefactor has a rational square root.  Refuse other cases
    # instead of silently replacing an irrational algebraic value by a nearby
    # bounded-denominator fraction.  For the regular spin-1 fixture:
    # prefactor_sq = (1/24)^4, sqrt = (1/24)^2 = 1/576
    return _sqrt_fraction_exact(prefactor_sq) * total


def verify_regular_tetrahedron() -> dict:
    """Verify {1 1 1; 1 1 1} = 1/6 on the regular spin-1 tetrahedron."""
    result = wigner_6j_exact(1, 1, 1, 1, 1, 1)

    # Intermediate values for audit
    p = [3, 3, 3, 3]
    q = [4, 4, 4]
    z_min, z_max = 3, 4

    # Term at z=3
    num_3 = (-1) ** 3 * math.factorial(4)
    den_3_p = math.factorial(0) ** 4
    den_3_q = math.factorial(1) ** 3
    term_3 = num_3 // (den_3_p * den_3_q)

    # Term at z=4
    num_4 = (-1) ** 4 * math.factorial(5)
    den_4_p = math.factorial(1) ** 4
    den_4_q = math.factorial(0) ** 3
    term_4 = num_4 // (den_4_p * den_4_q)

    raw_sum = term_3 + term_4  # = -24 + 120 = 96
    prefactor = Fraction(1, 576)  # Δ^4 = (1/24)^2 = 1/576

    return {
        "6j_exact": result,
        "6j_float": float(result),
        "expected": Fraction(1, 6),
        "match": result == Fraction(1, 6),
        "z_range": (z_min, z_max),
        "term_z3": term_3,
        "term_z4": term_4,
        "raw_sum": raw_sum,
        "prefactor": prefactor,
        "product": prefactor * raw_sum,
        "triangle_checks": {
            f"({t[0]},{t[1]},{t[2]})": triangle_valid(*t)
            for t in [(1, 1, 1)] * 4
        },
        "perimeter_is_integer": all(p_i == int(p_i) for p_i in p),
    }
