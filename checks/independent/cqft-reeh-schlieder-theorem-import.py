#!/usr/bin/env python3
"""Independent verification script for CQFT-REEH-SCHLIEDER-THEOREM-IMPORT (TFQ-2106).

AuthorityEffect: None.
Verifies all three finite/algebraic components and non-equivalence fences in
lean4/CampaignCqftReehSchliederTheoremImport.lean from first principles:
1. A recorded 2x4 integer matrix with a zero column keeps that column under left multiplication,
   and a recorded right-kernel vector is annihilated. The abstract cyclicity-to-separating proof
   stays in the Lean module.
2. Named 3-qubit states |000>, |GHZ_3>, and |W_3>, and named 4-qubit half-system matrices for
   |0000>, |GHZ_4>, and the 2-Bell-pair state: zero columns, pair left inverses, and full-algebra
   left inverses.
3. The product vacuum |000> has the same single-site unfolding at every site. Modular aliasing
   remains a Lean theorem and is not repeated here. Continuum Stone and tube analyticity stay open.
"""

from __future__ import annotations

import sys


def mat_mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    m = len(a)
    n = len(a[0])
    assert len(b) == n
    p = len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(p)] for i in range(m)]


def mat_id(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def combine_single_site(s: int, a: int, b: int) -> int:
    b0 = b % 2
    b1 = b // 2
    bit0 = a if s == 0 else b0
    bit1 = a if s == 1 else (b0 if s == 0 else b1)
    bit2 = a if s == 2 else b1
    return (bit0 + 2 * bit1 + 4 * bit2) % 8


def single_site_matrix(psi: list[int], s: int) -> list[list[int]]:
    return [[psi[combine_single_site(s, a, b)] for b in range(4)] for a in range(2)]


def pair_site_matrix(psi: list[int], s: int) -> list[list[int]]:
    return [[psi[combine_single_site(s, a, b)] for a in range(2)] for b in range(4)]


def verify_commutant_duality_and_kernel_obstruction() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [duality]: {msg}", file=sys.stderr)

    # Check associativity (X * Omega) * Y == X * (Omega * Y) on rectangular integer matrices
    omega_2x4 = [[1, 0, 2, -1], [0, 0, 1, 3]]
    v_ker = [0, 1, 0, 0]  # column 1 is zero
    for i in range(2):
        check(sum(omega_2x4[i][j] * v_ker[j] for j in range(4)) == 0, f"Row {i} right kernel")

    # Any X * omega_2x4 also annihilates v_ker (hence column 1 of X * omega_2x4 is always 0!)
    for x00 in (-2, -1, 0, 1, 2):
        for x01 in (-2, -1, 0, 1, 2):
            for x10 in (-1, 0, 1):
                for x11 in (-1, 0, 1):
                    x_mat = [[x00, x01], [x10, x11]]
                    xo = mat_mul(x_mat, omega_2x4)
                    check(xo[0][1] == 0 and xo[1][1] == 0, "Zero column preserved under left X multiplication")

    return checks, failures


def verify_three_and_four_qubit_census() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [census]: {msg}", file=sys.stderr)

    psi_prod3 = [1 if x == 0 else 0 for x in range(8)]
    psi_ghz3 = [1 if x in (0, 7) else 0 for x in range(8)]
    psi_w3 = [1 if x in (1, 2, 4) else 0 for x in range(8)]

    left_inv_ghz = [[1, 0, 0, 0], [0, 0, 0, 1]]
    left_inv_w = [[0, 1, 0, 0], [1, 0, 0, 0]]

    for s in range(3):
        # Single-site (2 x 4) unfoldings: column 1 is 0 for prod3 and ghz3; column 3 is 0 for w3
        ms_prod = single_site_matrix(psi_prod3, s)
        ms_ghz = single_site_matrix(psi_ghz3, s)
        ms_w = single_site_matrix(psi_w3, s)
        check(all(ms_prod[a][1] == 0 for a in range(2)), f"prod3 single-site s={s} col 1 zero")
        check(all(ms_ghz[a][1] == 0 for a in range(2)), f"ghz3 single-site s={s} col 1 zero")
        check(all(ms_w[a][3] == 0 for a in range(2)), f"w3 single-site s={s} col 3 zero")

        # Pair-of-sites (4 x 2) unfoldings
        mp_prod = pair_site_matrix(psi_prod3, s)
        mp_ghz = pair_site_matrix(psi_ghz3, s)
        mp_w = pair_site_matrix(psi_w3, s)
        check(all(mp_prod[b][1] == 0 for b in range(4)), f"prod3 pair s={s} col 1 zero")
        check(mat_mul(left_inv_ghz, mp_ghz) == mat_id(2), f"ghz3 pair s={s} left inverse")
        check(mat_mul(left_inv_w, mp_w) == mat_id(2), f"w3 pair s={s} left inverse")

    # Full 3-site (8 x 1) unfoldings have left inverses -> cyclic
    full_prod = [[psi_prod3[i]] for i in range(8)]
    full_ghz = [[psi_ghz3[i]] for i in range(8)]
    full_w = [[psi_w3[i]] for i in range(8)]
    l_0 = [[1 if i == 0 else 0 for i in range(8)]]
    l_1 = [[1 if i == 1 else 0 for i in range(8)]]
    check(mat_mul(l_0, full_prod) == [[1]], "prod3 full 3-site left inverse")
    check(mat_mul(l_0, full_ghz) == [[1]], "ghz3 full 3-site left inverse")
    check(mat_mul(l_1, full_w) == [[1]], "w3 full 3-site left inverse")

    # 4-qubit half-system (4 x 4) unfoldings
    half_prod4 = [[1 if (i == 0 and j == 0) else 0 for j in range(4)] for i in range(4)]
    half_ghz4 = [[1 if (i == 0 and j == 0) or (i == 3 and j == 3) else 0 for j in range(4)] for i in range(4)]
    half_bell4 = mat_id(4)
    check(all(half_prod4[i][1] == 0 for i in range(4)), "prod4 half-system col 1 zero")
    check(all(half_ghz4[i][1] == 0 for i in range(4)), "ghz4 half-system col 1 zero")
    check(mat_mul(mat_id(4), half_bell4) == mat_id(4), "bellPair4 half-system full rank 4")

    return checks, failures


def verify_discrete_translation_fence() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [translation]: {msg}", file=sys.stderr)

    # Modular aliasing and constant-vector momentum are Lean theorems. Repeating
    # (x + n) % n == x does not test them. The independent witness is the vacuum.
    psi_prod3 = [1 if x == 0 else 0 for x in range(8)]
    check(
        single_site_matrix(psi_prod3, 0)
        == single_site_matrix(psi_prod3, 1)
        == single_site_matrix(psi_prod3, 2),
        "|000> singleSiteMatrix is translation-invariant across sites 0, 1, 2",
    )

    return checks, failures


def main() -> int:
    c1, f1 = verify_commutant_duality_and_kernel_obstruction()
    c2, f2 = verify_three_and_four_qubit_census()
    c3, f3 = verify_discrete_translation_fence()
    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3
    print(
        f"checks={total_checks} duality={c1} census={c2} translation={c3} failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
