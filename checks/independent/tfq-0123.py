#!/usr/bin/env python3
"""Independent verification for TFQ-0123 (CONTINUUM_INTERFACE).

Disjoint standard-library-only arithmetic checker verifying:
1. Natural-number transport: left and right identity for losses 0..7, the zero-loss iff on that square,
   and one associativity witness. Loss monotonicity and the repeated addition-associativity product
   are not rechecked.
2. Carrier mismatch (GAP-F002-S000-002): the exact dyadic triple, ulp absorption for k = 2..10,
   the binary64 2^-53 witness, and two witnesses that an even sum is not 1.
3. 11-simplex face counts, the power-set total, the boundary Euler value, the 66-component count,
   and the two SO(2) frames (GAP-F002-S000-001).

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

    # Identity and zero-loss on losses 0..7, plus one associativity witness.
    # Loss monotonicity and the repeated addition-associativity product are not rechecked.
    for l1 in range(8):
        c1 = (0, 1, l1)
        check(compose_nat_cell(id_nat_cell(0), c1) == c1, "nat")
        check(compose_nat_cell(c1, id_nat_cell(1)) == c1, "nat")
        for l2 in range(8):
            c12 = compose_nat_cell(c1, (1, 2, l2))
            check((c12[2] == 0) == (l1 == 0 and l2 == 0), "nat")
    assoc_left = compose_nat_cell(compose_nat_cell((0, 1, 1), (1, 2, 2)), (2, 3, 3))
    assoc_right = compose_nat_cell((0, 1, 1), compose_nat_cell((1, 2, 2), (2, 3, 3)))
    check(assoc_left == assoc_right, "nat")

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

    # Also check IEEE-754 binary64 hardware float non-associativity at 2^-53
    u = 2.0**-53
    check(((1.0 + u) + u) == 1.0, "carrier")
    check((1.0 + (u + u)) > 1.0, "carrier")
    check(((1.0 + u) + u) != (1.0 + (u + u)), "carrier")

    check(0 + 0 != 1, "carrier")
    check(1 + 1 != 1, "carrier")

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
    check((11 * 12) // 2 == 66, "sugra")

    # Frame rotation blindness & 11D traceless Ricci mode pairs
    f_id = (1, 0, 0, 1)
    f_rot = (0, -1, 1, 0)
    check(f_id[0] * f_id[3] - f_id[1] * f_id[2] == 1, "sugra")
    check(f_rot[0] * f_rot[3] - f_rot[1] * f_rot[2] == 1, "sugra")
    check((f_id[0] + f_id[3]) != (f_rot[0] + f_rot[3]), "sugra")

    print(
        f"checks={checks} nat_cell={nat_cell} carrier_fence={carrier_fence} sugra_fence={sugra_fence} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
