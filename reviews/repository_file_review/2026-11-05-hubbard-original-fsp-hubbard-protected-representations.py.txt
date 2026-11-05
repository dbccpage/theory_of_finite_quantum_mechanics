#!/usr/bin/env python3
"""
Independent check for Target 4: FSP-HUBBARD-PROTECTED-REPRESENTATIONS.
Zero repository imports: uses only SymPy and standard library.

Conventions: bonds are applied in lexicographic order (validate_bonds sorts them) and then in reverse
order, so the 4-site ring is (0,1),(0,3),(1,2),(2,3). The witness values depend on this order.
The checks 1 and 2 cover the stated parameter sets only (two time slices), not all models.

Recomputes:
1. Exact attractive spin-balanced Hubbard determinant pairing across all 64 fields of the 3-site triangle (2 slices).
2. Exact half-filled bipartite particle-hole pairing across all 256 fields of the 4-site ring (2 slices).
3. Exact negative determinant product weight for the doped 4-site ring witness (mask 15721, slices=4, r=2, hs=8, z=2).
4. Exact negative determinant product weight for the frustrated 3-site triangle witness (mask 1281, slices=4, r=2, hs=8, z=1).
"""

import sys
from fractions import Fraction
import sympy as sp
from sympy import Rational, eye


def validate_bonds(sites: int, bonds: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Validate and sort undirected bonds lexicographically."""
    norm = []
    for edge in bonds:
        if len(edge) != 2 or any(type(x) is not int or x < 0 or x >= sites for x in edge) or edge[0] == edge[1]:
            raise ValueError("invalid edge")
        norm.append(tuple(sorted(edge)))
    if len(set(norm)) != len(norm):
        raise ValueError("duplicate bond")
    return sorted(norm)


def kinetic_matrix(sites: int, bonds: list[tuple[int, int]], r: Rational) -> sp.Matrix:
    """Palindromic product of exact bond exponentials; r = exp(delta_tau * t / 2)."""
    res = eye(sites)
    bonds = validate_bonds(sites, bonds)
    all_bonds = bonds + list(reversed(bonds))
    for x, y in all_bonds:
        b = eye(sites)
        b[x, x] = (r + 1/r) / 2
        b[y, y] = (r + 1/r) / 2
        b[x, y] = (r - 1/r) / 2
        b[y, x] = (r - 1/r) / 2
        res = b * res
    return res


def compute_hubbard_determinants(
    sites: int,
    bonds: list[tuple[int, int]],
    slices: int,
    r: Rational,
    hs: Rational,
    fugacity: Rational,
    mask: int,
    attractive: bool = False,
) -> tuple[Rational, Rational, Rational, int]:
    """Compute exact single-field spin determinants (d_up, d_down), product weight W, and total field sum."""
    T = kinetic_matrix(sites, bonds, r)
    P_up = eye(sites)
    P_down = eye(sites)
    total_s = 0

    for t in range(slices):
        V_up = eye(sites)
        V_down = eye(sites)
        for i in range(sites):
            bit = (mask >> (t * sites + i)) & 1
            s = 2 * bit - 1
            total_s += s
            V_up[i, i] = fugacity * (hs ** s)
            if attractive:
                V_down[i, i] = fugacity * (hs ** s)
            else:
                V_down[i, i] = fugacity * (hs ** (-s))
        B_up = T * V_up
        B_down = T * V_down
        P_up = B_up * P_up
        P_down = B_down * P_down

    d_up = (eye(sites) + P_up).det()
    d_down = (eye(sites) + P_down).det()

    if attractive:
        prefactor = hs ** (-total_s)
    else:
        prefactor = Rational(1)

    weight = prefactor * d_up * d_down
    return d_up, d_down, weight, total_s


def main() -> None:
    print("=== Running Independent Check for FSP-HUBBARD-PROTECTED-REPRESENTATIONS ===")

    # 1. Attractive spin-balanced pairing check
    print("\n[1/4] Verifying attractive spin-balanced pairing across all 64 fields (triangle, 2 slices, z=3/2, hs=2, r=3/2)...")
    tri = [(0, 1), (1, 2), (0, 2)]
    for mask in range(64):
        d_up, d_down, w, s = compute_hubbard_determinants(
            sites=3, bonds=tri, slices=2, r=Rational(3, 2), hs=Rational(2), fugacity=Rational(3, 2), mask=mask, attractive=True
        )
        assert d_up == d_down, f"Attractive spin pairing failed at mask {mask}: {d_up} != {d_down}"
        assert w >= 0, f"Attractive weight negative at mask {mask}: {w} < 0"
    print("  ✓ All 64 fields satisfy d_up == d_down and W(s) >= 0.")

    # 2. Half-filled bipartite particle-hole pairing check
    print("\n[2/4] Verifying half-filled bipartite pairing across all 256 fields (4-site ring, 2 slices, z=1, hs=2, r=3/2)...")
    ring = [(0, 1), (1, 2), (2, 3), (0, 3)]
    for mask in range(256):
        d_up, d_down, w, s = compute_hubbard_determinants(
            sites=4, bonds=ring, slices=2, r=Rational(3, 2), hs=Rational(2), fugacity=Rational(1), mask=mask, attractive=False
        )
        expected_d_down = d_up / (Rational(2) ** s)
        assert d_down == expected_d_down, f"Half-filled pairing relation failed at mask {mask}: {d_down} != {expected_d_down}"
        assert w >= 0, f"Half-filled weight negative at mask {mask}: {w} < 0"
    print("  ✓ All 256 fields satisfy d_down == d_up / h^(sum s) and W(s) >= 0.")

    # 3. Negative witness 1: Doped 4-site ring (mask 15721) outside half-filling protection (z=2, hs=8, r=2, slices=4)
    print("\n[3/4] Recomputing negative determinant witness 1: Doped 4-site ring (mask 15721)...")
    d_up1, d_down1, w1, s1 = compute_hubbard_determinants(
        sites=4, bonds=ring, slices=4, r=Rational(2), hs=Rational(8), fugacity=Rational(2), mask=15721, attractive=False
    )
    expected_up1 = Rational(11072073737867929807204939234025, 2305843009213693952)
    expected_down1 = Rational(-1034021712177776419381618902295, 147573952589676412928)
    assert d_up1 == expected_up1, f"d_up mismatch: {d_up1} != {expected_up1}"
    assert d_down1 == expected_down1, f"d_down mismatch: {d_down1} != {expected_down1}"
    expected_w1 = Rational(
        -11448764643788789633389299083665210593647227349065798614587375,
        340282366920938463463374607431768211456,
    )
    assert w1 == d_up1 * d_down1 == expected_w1, f"W mismatch: {w1} != {expected_w1}"
    assert 340282366920938463463374607431768211456 == 2 ** 128
    assert (d_up1.q, d_down1.q, w1.q) == (2 ** 61, 2 ** 67, 2 ** 128), "denominators of the ring witness"
    assert d_up1 > 0, "d_up must be strictly positive"
    assert d_down1 < 0, "d_down must be strictly negative"
    assert w1 < 0, "determinant product weight must be strictly negative"
    # The pairing relation d_down = d_up / h^(sum s) fails here (z = 2), and the same mask at z = 1 is nonnegative.
    assert d_down1 != d_up1 / (Rational(8) ** s1), "pairing relation unexpectedly holds at z=2"
    d_up1h, d_down1h, w1h, _ = compute_hubbard_determinants(
        sites=4, bonds=ring, slices=4, r=Rational(2), hs=Rational(8), fugacity=Rational(1), mask=15721, attractive=False
    )
    assert d_down1h == d_up1h / (Rational(8) ** s1) and w1h >= 0, "mask 15721 at z=1 must satisfy the pairing relation"
    print(f"  d_up   = {d_up1} > 0")
    print(f"  d_down = {d_down1} < 0")
    print(f"  W(15721) = {w1} < 0")
    print("  ✓ Witness 1 verified: strictly negative determinant weight outside half-filling protection.")

    # 4. Negative witness 2: Frustrated 3-site triangle (mask 1281) outside bipartite protection (z=1, hs=8, r=2, slices=4)
    print("\n[4/4] Recomputing negative determinant witness 2: Frustrated 3-site triangle (mask 1281)...")
    d_up2, d_down2, w2, s2 = compute_hubbard_determinants(
        sites=3, bonds=tri, slices=4, r=Rational(2), hs=Rational(8), fugacity=Rational(1), mask=1281, attractive=False
    )
    expected_up2 = Rational(2661572208368287551525625, 9223372036854775808)
    expected_down2 = Rational(-323903084369592224375, 35184372088832)
    assert d_up2 == expected_up2, f"d_up mismatch: {d_up2} != {expected_up2}"
    assert d_down2 == expected_down2, f"d_down mismatch: {d_down2} != {expected_down2}"
    expected_w2 = Rational(
        -862091447562875338563475227905478168562109375,
        324518553658426726783156020576256,
    )
    assert w2 == d_up2 * d_down2 == expected_w2, f"W mismatch: {w2} != {expected_w2}"
    assert 324518553658426726783156020576256 == 2 ** 108
    assert (d_up2.q, d_down2.q, w2.q) == (2 ** 63, 2 ** 45, 2 ** 108), "denominators of the triangle witness"
    assert d_up2 > 0, "d_up must be strictly positive"
    assert d_down2 < 0, "d_down must be strictly negative"
    assert w2 < 0, "determinant product weight must be strictly negative"
    # The pairing relation d_down = d_up / h^(sum s) fails on the triangle at z = 1 (odd cycle).
    assert d_down2 != d_up2 / (Rational(8) ** s2), "pairing relation unexpectedly holds on the triangle"
    print(f"  d_up   = {d_up2} > 0")
    print(f"  d_down = {d_down2} < 0")
    print(f"  W(1281)  = {w2} < 0")
    print("  ✓ Witness 2 verified: strictly negative determinant weight outside bipartite protection.")

    print("\n=== All independent checks passed successfully! ===")
    sys.exit(0)


if __name__ == "__main__":
    main()
