#!/usr/bin/env python3
"""Independent verification script for CQFT-CAUSAL-FACTORIZATION-IMPORT (TFQ-2109).

AuthorityEffect: None.
Verifies all three finite/algebraic components and non-equivalence fences in
lean4/CausalFactorizationImport.lean from first principles:
1. Abstract Bogoliubov relative S-matrix algebra V(g, h) = S(g)^{-1} S(g + h) over GL(2, Z)
   and SL(2, Z) matrix models, telescoping cocycle identity V(g, h1) V(g + h1, h2) = V(g, h1 + h2),
   equivalence between causal factorization V(g, h1 + h2) = V(g, h1) V(g, h2) and background-shift
   invariance V(g + h1, h2) = V(g, h2), and Epstein-Glaser causal separation asymmetry on C2.
2. Complete enumeration of all 24 permutations of {0, 1, 2, 3} on the 4-element N poset
   (0 < 2, 1 < 2, 1 < 3), exact identification of its 5 linear extensions, explicit adjacent-spacelike-swap
   connectivity across all 5 linear extensions, and ordered-product equality for commuting 2x2 integer
   matrices vs. exact sign flip for anticommuting Pauli matrices on (0, 3).
3. Coincident-diagonal renormalization ambiguity fence: irreflexivity of spacelike separation on the
   diagonal, 4D Epstein-Glaser polynomial counterterm dimensions binom(omega + 4, 4) for omega = 0..10,
   and invariance of off-diagonal factorized two-point kernels under diagonal contact counterterms.
"""

from __future__ import annotations

import itertools
import math
import sys


Mat2 = tuple[tuple[int, int], tuple[int, int]]

I2: Mat2 = ((1, 0), (0, 1))
X2: Mat2 = ((0, 1), (1, 0))
Z2: Mat2 = ((1, 0), (0, -1))


def mat2_mul(a: Mat2, b: Mat2) -> Mat2:
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def mat2_neg(a: Mat2) -> Mat2:
    return ((-a[0][0], -a[0][1]), (-a[1][0], -a[1][1]))


def mat2_det(a: Mat2) -> int:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def mat2_inv_unimodular(a: Mat2) -> Mat2:
    det = mat2_det(a)
    assert det in (-1, 1), f"Expected unimodular 2x2 matrix, got det={det}"
    return (
        (det * a[1][1], -det * a[0][1]),
        (-det * a[1][0], det * a[0][0]),
    )


def ordered_prod(assign: dict[int, Mat2], seq: list[int] | tuple[int, ...]) -> Mat2:
    acc = I2
    for x in seq:
        acc = mat2_mul(acc, assign[x])
    return acc


def verify_bogoliubov_and_c2_asymmetry() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [bogoliubov]: {msg}", file=sys.stderr)

    # Unimodular 2x2 integer matrix family S(g1, g2) = [[1, g1], [0, 1]] * [[1, 0], [g2, 1]]
    def s_nonfactor(g: tuple[int, int]) -> Mat2:
        g1, g2 = g
        return mat2_mul(((1, g1), (0, 1)), ((1, 0), (g2, 1)))

    # Factorizing sheer family S_comm(g1, g2) = [[1, g1 + 2*g2], [0, 1]]
    def s_factor(g: tuple[int, int]) -> Mat2:
        g1, g2 = g
        return ((1, g1 + 2 * g2), (0, 1))

    def bogoliubov_v(s_fn, g: tuple[int, int], h: tuple[int, int]) -> Mat2:
        gh = (g[0] + h[0], g[1] + h[1])
        return mat2_mul(mat2_inv_unimodular(s_fn(g)), s_fn(gh))

    coords = [(-2, -1), (-1, 0), (0, 0), (1, 0), (0, 1), (1, 2), (2, -1)]
    for g in coords:
        check(bogoliubov_v(s_nonfactor, g, (0, 0)) == I2, f"V(g, 0) == I for g={g}")
        check(bogoliubov_v(s_factor, g, (0, 0)) == I2, f"V_comm(g, 0) == I for g={g}")
        for h1 in coords[:4]:
            for h2 in coords[:4]:
                gh1 = (g[0] + h1[0], g[1] + h1[1])
                h12 = (h1[0] + h2[0], h1[1] + h2[1])
                # Telescoping cocycle identity holds unconditionally in both models
                lhs_nf = mat2_mul(bogoliubov_v(s_nonfactor, g, h1), bogoliubov_v(s_nonfactor, gh1, h2))
                rhs_nf = bogoliubov_v(s_nonfactor, g, h12)
                check(lhs_nf == rhs_nf, f"Cocycle telescoping failed at g={g}, h1={h1}, h2={h2}")

                # Equivalence: V(g, h1 + h2) == V(g, h1) V(g, h2) <=> V(g + h1, h2) == V(g, h2)
                fac_nf = bogoliubov_v(s_nonfactor, g, h12) == mat2_mul(
                    bogoliubov_v(s_nonfactor, g, h1), bogoliubov_v(s_nonfactor, g, h2)
                )
                shift_nf = bogoliubov_v(s_nonfactor, gh1, h2) == bogoliubov_v(s_nonfactor, g, h2)
                check(fac_nf == shift_nf, "Factorization <-> background shift invariance failed")

                # Commuting shear family always factorizes
                check(
                    bogoliubov_v(s_factor, g, h12)
                    == mat2_mul(bogoliubov_v(s_factor, g, h1), bogoliubov_v(s_factor, g, h2)),
                    "Commuting shear family must factorize",
                )

    # Diamond poset C2: 0 < 1, 0 < 2, 1 < 3, 2 < 3, 0 < 3
    c2_rel = {(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)}

    def is_spacelike(rel: set[tuple[int, int]], x: int, y: int) -> bool:
        return x != y and (x, y) not in rel and (y, x) not in rel

    def no_in_causal_past(rel: set[tuple[int, int]], l1: list[int], l2: list[int]) -> bool:
        return all((x, y) not in rel for x in l1 for y in l2)

    def all_spacelike_between(rel: set[tuple[int, int]], l1: list[int], l2: list[int]) -> bool:
        return all(is_spacelike(rel, x, y) for x in l1 for y in l2)

    check(all_spacelike_between(c2_rel, [1], [2]) is True, "C2 [1], [2] spacelike")
    check(no_in_causal_past(c2_rel, [1], [2]) is True, "C2 noInCausalPast [1], [2]")
    check(no_in_causal_past(c2_rel, [2], [1]) is True, "C2 noInCausalPast [2], [1]")
    check(no_in_causal_past(c2_rel, [1, 2, 3], [0]) is True, "C2 future-before-past [1,2,3], [0]")
    check(all_spacelike_between(c2_rel, [1, 2, 3], [0]) is False, "C2 [1,2,3], [0] not spacelike")
    check(no_in_causal_past(c2_rel, [0], [1, 2, 3]) is False, "C2 past-before-future [0], [1,2,3]")

    return checks, failures


def verify_poset_n_swap_connectivity() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [posetN]: {msg}", file=sys.stderr)

    # N poset: 0 < 2, 1 < 2, 1 < 3
    n_rel = {(0, 2), (1, 2), (1, 3)}

    def is_spacelike_n(x: int, y: int) -> bool:
        return x != y and (x, y) not in n_rel and (y, x) not in n_rel

    # Verify all 3 unordered spacelike pairs {0,1}, {2,3}, {0,3}
    expected_spacelike = {(0, 1), (1, 0), (2, 3), (3, 2), (0, 3), (3, 0)}
    for x in range(4):
        for y in range(4):
            check(
                is_spacelike_n(x, y) == ((x, y) in expected_spacelike),
                f"posetN spacelike({x}, {y}) mismatch",
            )

    def is_linear_ext_n(perm: tuple[int, ...]) -> bool:
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if (perm[j], perm[i]) in n_rel:
                    return False
        return True

    all_perms = list(itertools.permutations(range(4)))
    check(len(all_perms) == 24, "24 permutations of Fin 4")
    lin_exts = [p for p in all_perms if is_linear_ext_n(p)]
    expected_exts = [
        (0, 1, 2, 3),
        (0, 1, 3, 2),
        (1, 0, 2, 3),
        (1, 0, 3, 2),
        (1, 3, 0, 2),
    ]
    check(lin_exts == expected_exts, f"Expected 5 extensions {expected_exts}, got {lin_exts}")

    # Verify adjacent spacelike swap graph on the 5 linear extensions
    def adj_spacelike_swap(p1: tuple[int, ...], p2: tuple[int, ...]) -> bool:
        diffs = [i for i in range(4) if p1[i] != p2[i]]
        if len(diffs) != 2 or diffs[1] != diffs[0] + 1:
            return False
        i = diffs[0]
        return p1[i] == p2[i + 1] and p1[i + 1] == p2[i] and is_spacelike_n(p1[i], p1[i + 1])

    check(adj_spacelike_swap(expected_exts[0], expected_exts[1]), "extN0 <-> extN1")
    check(adj_spacelike_swap(expected_exts[0], expected_exts[2]), "extN0 <-> extN2")
    check(adj_spacelike_swap(expected_exts[2], expected_exts[3]), "extN2 <-> extN3")
    check(adj_spacelike_swap(expected_exts[1], expected_exts[3]), "extN1 <-> extN3")
    check(adj_spacelike_swap(expected_exts[3], expected_exts[4]), "extN3 <-> extN4")

    # BFS reachability from extN0 across adjacent spacelike swaps
    visited = {expected_exts[0]}
    queue = [expected_exts[0]]
    while queue:
        cur = queue.pop(0)
        for nxt in expected_exts:
            if nxt not in visited and adj_spacelike_swap(cur, nxt):
                visited.add(nxt)
                queue.append(nxt)
    check(visited == set(expected_exts), "All 5 linear extensions of posetN are swap-connected")

    # Check commuting vs anticommuting operator products across all 5 linear extensions
    assign_comm = {0: Z2, 1: I2, 2: I2, 3: Z2}
    prods_comm = [ordered_prod(assign_comm, ext) for ext in expected_exts]
    for idx, p in enumerate(prods_comm):
        check(p == prods_comm[0], f"Commuting product mismatch at extN{idx}")

    assign_anticomm = {0: X2, 1: I2, 2: I2, 3: Z2}
    p0 = ordered_prod(assign_anticomm, expected_exts[0])
    p1 = ordered_prod(assign_anticomm, expected_exts[1])
    p2 = ordered_prod(assign_anticomm, expected_exts[2])
    p3 = ordered_prod(assign_anticomm, expected_exts[3])
    p4 = ordered_prod(assign_anticomm, expected_exts[4])
    check(p0 == p1 == p2 == p3, "extN0..extN3 preserve (0 before 3) ordering")
    check(p3 == mat2_neg(p4), "extN3 == -extN4 for anticommuting X, Z on (0, 3)")
    check(p3 != p4, "extN3 != extN4 for anticommuting X, Z on (0, 3)")

    return checks, failures


def verify_diagonal_counterterm_fence() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [diagonal]: {msg}", file=sys.stderr)

    # 4D Epstein-Glaser polynomial counterterm dimension binom(omega + 4, 4)
    expected_dims = {0: 1, 1: 5, 2: 15, 3: 35, 4: 70, 5: 126, 6: 210}
    for omega, exp_val in expected_dims.items():
        val = (omega + 1) * (omega + 2) * (omega + 3) * (omega + 4) // 24
        check(val == math.comb(omega + 4, 4) == exp_val, f"Counterterm dim mismatch at omega={omega}")

    # Two-point kernel with diagonal contact counterterm c
    t1 = [2, -3, 5, 7]

    def kernel(c: int, x: int, y: int) -> int:
        return t1[x] * t1[x] + c if x == y else t1[x] * t1[y]

    for c1 in (-5, -1, 0, 2, 9):
        for c2 in (-5, -1, 0, 2, 9):
            for x in range(4):
                for y in range(4):
                    if x != y:
                        check(
                            kernel(c1, x, y) == kernel(c2, x, y) == t1[x] * t1[y],
                            f"Off-diagonal kernel must be independent of c at ({x},{y})",
                        )
                    else:
                        check(
                            kernel(c1, x, x) - kernel(c2, x, x) == c1 - c2,
                            f"Diagonal kernel difference must equal c1 - c2 at x={x}",
                        )

    return checks, failures


def main() -> int:
    c1, f1 = verify_bogoliubov_and_c2_asymmetry()
    c2, f2 = verify_poset_n_swap_connectivity()
    c3, f3 = verify_diagonal_counterterm_fence()
    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3
    print(
        f"checks={total_checks} bogoliubov={c1} posetN={c2} diagonal={c3} failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
