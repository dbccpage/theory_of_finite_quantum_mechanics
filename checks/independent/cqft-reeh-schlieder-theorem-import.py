#!/usr/bin/env python3
"""Independent verification script for CQFT-REEH-SCHLIEDER-THEOREM-IMPORT (TFQ-2106).

AuthorityEffect: None.
Checks finite matrix/state instances associated with lean4/ReehSchliederImport.lean:
1. A recorded 2x4 integer matrix with a zero column keeps that column under left multiplication,
   and a recorded right-kernel vector is annihilated. The abstract cyclicity-to-separating proof
   stays in the Lean module.
2. Unnormalized integer representatives of 3-qubit states |000>, |GHZ_3>, and |W_3>, and unnormalized 4-qubit half-system matrices for
   |0000>, |GHZ_4>, and the 2-Bell-pair state: zero columns, pair left inverses, and full-algebra
   left inverses.
Nonzero rescaling preserves ranks and zero columns, but changes left inverses.
3. The product vacuum |000> has the same single-site unfolding at every site. Modular aliasing
   remains a Lean theorem and is not repeated here. Continuum Stone and tube analyticity stay open.
"""

from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

# Shared checker infrastructure only; no production implementation is imported.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.cases import Cases
from checker_support.rational_matrix import RationalMatrix
from collections.abc import Callable
from checker_support.domains import integer, sequence


def mat_mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    left, right = RationalMatrix.from_integers(a), RationalMatrix.from_integers(b)
    return [list(row) for row in left.mul(right).integer_rows()]


def mat_id(n: int) -> list[list[int]]:
    return [list(row) for row in RationalMatrix.eye(n).integer_rows()]


def _coefficients(psi: object) -> tuple[int, ...]:
    values = sequence(psi, "three-qubit coefficients", 8)
    return RationalMatrix.from_integers((values,)).integer_rows()[0]


def combine_single_site(s: int, a: int, b: int) -> int:
    integer(s, "site", 0, 2)
    integer(a, "site bit", 0, 1)
    integer(b, "complement index", 0, 3)
    b0 = b % 2
    b1 = b // 2
    bit0 = a if s == 0 else b0
    bit1 = a if s == 1 else (b0 if s == 0 else b1)
    bit2 = a if s == 2 else b1
    return bit0 + 2 * bit1 + 4 * bit2


def single_site_matrix(psi: list[int], s: int) -> list[list[int]]:
    coefficients = _coefficients(psi)
    integer(s, "site", 0, 2)
    return [[coefficients[combine_single_site(s, a, b)] for b in range(4)] for a in range(2)]


def pair_site_matrix(psi: list[int], s: int) -> list[list[int]]:
    coefficients = _coefficients(psi)
    integer(s, "site", 0, 2)
    return [[coefficients[combine_single_site(s, a, b)] for a in range(2)] for b in range(4)]


def verify_commutant_duality_and_kernel_obstruction() -> tuple[int, int]:
    cases = Cases()

    def check(cond: bool, msg: str) -> None:
        cases.append((f"duality.{len(cases)}:{msg}", cond))

    # Check the recorded kernel and its preservation, not the general associativity theorem
    omega_2x4 = [[1, 0, 2, -1], [0, 0, 1, 3]]
    v_ker = [0, 1, 0, 0]  # column 1 is zero
    for i in range(2):
        check(sum(omega_2x4[i][j] * v_ker[j] for j in range(4)) == 0, f"Row {i} right kernel")

    # Any X * omega_2x4 also annihilates v_ker (hence column 1 of X * omega_2x4 is always 0!)
    for x00, x01, x10, x11 in product(range(-2, 3), range(-2, 3), range(-1, 2), range(-1, 2)):
        xo = mat_mul([[x00, x01], [x10, x11]], omega_2x4)
        check(xo[0][1] == 0 and xo[1][1] == 0, "Zero column preserved under left X multiplication")

    return len(cases), sum(not passed for _, passed in cases)


def check_three_qubit_unfoldings(check: Callable[[bool, str], None]) -> tuple[list[int], list[int], list[int]]:
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
    return psi_ghz3, psi_prod3, psi_w3


def check_full_system_inverses(check: Callable[[bool, str], None], psi_ghz3: list[int], psi_prod3: list[int], psi_w3: list[int]) -> None:
    prod, ghz, wstate = _coefficients(psi_prod3), _coefficients(psi_ghz3), _coefficients(psi_w3)
    full_prod = [[prod[i]] for i in range(8)]
    full_ghz = [[ghz[i]] for i in range(8)]
    full_w = [[wstate[i]] for i in range(8)]
    l_0 = [[1 if i == 0 else 0 for i in range(8)]]
    l_1 = [[1 if i == 1 else 0 for i in range(8)]]
    check(mat_mul(l_0, full_prod) == [[1]], "prod3 full 3-site left inverse")
    check(mat_mul(l_0, full_ghz) == [[1]], "ghz3 full 3-site left inverse")
    check(mat_mul(l_1, full_w) == [[1]], "w3 full 3-site left inverse")


def check_four_qubit_unfoldings(check: Callable[[bool, str], None]) -> None:
    half_prod4 = [[1 if (i == 0 and j == 0) else 0 for j in range(4)] for i in range(4)]
    half_ghz4 = [[1 if (i == 0 and j == 0) or (i == 3 and j == 3) else 0 for j in range(4)] for i in range(4)]
    half_bell4 = mat_id(4)
    check(all(half_prod4[i][1] == 0 for i in range(4)), "prod4 half-system col 1 zero")
    check(all(half_ghz4[i][1] == 0 for i in range(4)), "ghz4 half-system col 1 zero")
    check(mat_mul(mat_id(4), half_bell4) == mat_id(4), "bellPair4 half-system full rank 4")


def verify_three_and_four_qubit_census() -> tuple[int, int]:
    cases = Cases()

    def check(cond: bool, msg: str) -> None:
        cases.append((f"census.{len(cases)}:{msg}", cond))

    psi_ghz3, psi_prod3, psi_w3 = check_three_qubit_unfoldings(check)

    # Full 3-site (8 x 1) unfoldings have left inverses -> cyclic
    check_full_system_inverses(check, psi_ghz3, psi_prod3, psi_w3)

    # 4-qubit half-system (4 x 4) unfoldings
    check_four_qubit_unfoldings(check)

    return len(cases), sum(not passed for _, passed in cases)


def verify_discrete_translation_fence() -> tuple[int, int]:
    cases = Cases()

    def check(cond: bool, msg: str) -> None:
        cases.append((f"translation.{len(cases)}:{msg}", cond))

    # Modular aliasing and constant-vector momentum are Lean theorems. Repeating
    # (x + n) % n == x does not test them. The independent witness is the vacuum.
    psi_prod3 = [1 if x == 0 else 0 for x in range(8)]
    check(
        single_site_matrix(psi_prod3, 0)
        == single_site_matrix(psi_prod3, 1)
        == single_site_matrix(psi_prod3, 2),
        "|000> singleSiteMatrix is translation-invariant across sites 0, 1, 2",
    )

    return len(cases), sum(not passed for _, passed in cases)


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
    raise SystemExit(cli(main))
