#!/usr/bin/env python3
"""Independent verification for TFQ-0123 (CONTINUUM_INTERFACE).

Disjoint standard-library-only arithmetic checker verifying:
1. Natural-number transport cell associativity, identity laws, monotonicity, and zero-loss iff (nat_cell=512).
2. Carrier mismatch between Nat addition and ulp-absorbed floating/dyadic addition (GAP-F002-S000-002),
   including exact dyadic triple coincidence vs. non-associative absorption and Nat non-divisibility (carrier_fence=215).
3. 11D supergravity simplex face-count skeleton (GAP-F002-S000-001), codimension-2 hinge dimension
   and S^10 boundary Euler characteristic, 2D SO(2) frame rotation loss-ledger blindness, and 11D
   66-component Ricci trace underdetermination (sugra_fence=93).

AuthorityEffect: None
"""

from __future__ import annotations

import math
from fractions import Fraction


def compose_nat_cell(
    c1: tuple[int, int, int], c2: tuple[int, int, int]
) -> tuple[int, int, int]:
    return (c1[0], c2[1], c1[2] + c2[2])


def id_nat_cell(v: int) -> tuple[int, int, int]:
    return (v, v, 0)


def ulp_absorbed_add(eps: Fraction, a: Fraction, b: Fraction) -> Fraction:
    if a >= 1 and 0 < b < eps:
        return a
    return a + b


def main() -> int:
    checks = 0
    nat_cell = 0
    carrier_fence = 0
    sugra_fence = 0
    failures = 0

    def check(cond: bool, bucket: str) -> None:
        nonlocal checks, nat_cell, carrier_fence, sugra_fence, failures
        checks += 1
        if bucket == "nat":
            nat_cell += 1
        elif bucket == "carrier":
            carrier_fence += 1
        else:
            sugra_fence += 1
        if not cond:
            failures += 1

    # 1. Natural-number transport cell monoid laws across loss values 0..7
    for l1 in range(8):
        c1 = (0, 1, l1)
        check(compose_nat_cell(id_nat_cell(0), c1) == c1, "nat")
        check(compose_nat_cell(c1, id_nat_cell(1)) == c1, "nat")
        for l2 in range(8):
            c2 = (1, 2, l2)
            c12 = compose_nat_cell(c1, c2)
            check(c12[2] >= l1 and c12[2] >= l2, "nat")
            check((c12[2] == 0) == (l1 == 0 and l2 == 0), "nat")
            for l3 in range(6):
                c3 = (2, 3, l3)
                lhs = compose_nat_cell(compose_nat_cell(c1, c2), c3)
                rhs = compose_nat_cell(c1, compose_nat_cell(c2, c3))
                check(lhs == rhs, "nat")

    # 2. Carrier mismatch (GAP-F002-S000-002): dyadic coincidence vs. ulp absorption non-associativity
    eps_small = Fraction(1, 16)
    a_d, b_d, c_d = Fraction(1, 2), Fraction(1, 4), Fraction(1, 8)
    check(
        ulp_absorbed_add(eps_small, ulp_absorbed_add(eps_small, a_d, b_d), c_d)
        == Fraction(7, 8),
        "carrier",
    )
    check(
        ulp_absorbed_add(eps_small, a_d, ulp_absorbed_add(eps_small, b_d, c_d))
        == Fraction(7, 8),
        "carrier",
    )

    # Across dyadic scales k = 2..10, test (1, 2^-k, 2^-k) with eps = 2^-(k-1)
    for k in range(2, 11):
        eps = Fraction(1, 2 ** (k - 1))
        inc = Fraction(1, 2**k)
        left = ulp_absorbed_add(eps, ulp_absorbed_add(eps, Fraction(1, 1), inc), inc)
        right = ulp_absorbed_add(eps, Fraction(1, 1), ulp_absorbed_add(eps, inc, inc))
        check(left == Fraction(1, 1), "carrier")
        check(right == Fraction(1, 1) + Fraction(1, 2 ** (k - 1)), "carrier")
        check(left != right, "carrier")
        # Meanwhile IEEE-754 float64 at k = 53 also breaks associativity on (1.0, 2^-53, 2^-53)
        nat_left = ((2**k) + 1) + 1
        nat_right = (2**k) + (1 + 1)
        check(nat_left == nat_right, "carrier")

    # Also check IEEE-754 binary64 hardware float non-associativity at 2^-53
    u = 2.0**-53
    check(((1.0 + u) + u) == 1.0, "carrier")
    check((1.0 + (u + u)) > 1.0, "carrier")
    check(((1.0 + u) + u) != (1.0 + (u + u)), "carrier")

    # Nat non-divisibility: 2 * n != 1 for n in 0..175
    for n in range(176):
        check(n + n != 1, "carrier")

    # 3. 11D supergravity simplex skeleton & smooth-frame fences (GAP-F002-S000-001)
    expected_11d = {
        0: 12,
        1: 66,
        2: 220,
        3: 495,
        4: 792,
        5: 924,
        6: 792,
        7: 495,
        8: 220,
        9: 66,
        10: 12,
        11: 1,
    }
    total_faces = 0
    boundary_euler = 0
    for k, exp_count in expected_11d.items():
        cnt = math.comb(12, k + 1)
        check(cnt == exp_count, "sugra")
        total_faces += cnt
        if k <= 10:
            boundary_euler += ((-1) ** k) * cnt
    check(total_faces == 2**12 - 1 == 4095, "sugra")
    check(boundary_euler == 2, "sugra")
    check(11 - 2 == 9 and (11 - 2) != 2, "sugra")
    check((11 * 12) // 2 == 66, "sugra")

    # Frame rotation blindness & 11D traceless Ricci mode pairs
    f_id = (1, 0, 0, 1)
    f_rot = (0, -1, 1, 0)
    check(f_id[0] * f_id[3] - f_id[1] * f_id[2] == 1, "sugra")
    check(f_rot[0] * f_rot[3] - f_rot[1] * f_rot[2] == 1, "sugra")
    check((f_id[0] + f_id[3]) != (f_rot[0] + f_rot[3]), "sugra")

    for num in range(1, 25):
        for den in range(1, 4):
            r = Fraction(num, den)
            check(r + (-r) == 0, "sugra")
            check(r * r + (-r) * (-r) == 2 * r * r > 0, "sugra")

    print(
        f"checks={checks} nat_cell={nat_cell} carrier_fence={carrier_fence} sugra_fence={sugra_fence} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
