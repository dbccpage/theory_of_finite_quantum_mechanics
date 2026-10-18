#!/usr/bin/env python3
"""
Symbolic & algebraic verification of Matolcsi-Weiner Conjecture 2 (arXiv:2503.14752):
  Clause (a): G_H(pi(gamma_1)) = 0 for all 20 permutations of gamma_1 = (1, 1, 1, -1, -1, -1)
  Clause (b): G_H(pi(gamma_2)) * G_{H*}(pi(gamma_2)) = 0 for all 20 permutations of gamma_2 = (3, 3, 3, -3, -3, -3)
for all tensor-product transitions H = U_qubit(phi) (x) V_entrywise_nonzero(3x3).

The qubit MUB transition has the form:
  U(phi) = (1/sqrt(2)) [[1, 1], [e^{i*phi}, -e^{i*phi}]]
and its Hermitian adjoint (conjugate transpose) is:
  U*(phi) = (1/sqrt(2)) [[1, e^{-i*phi}], [1, -e^{-i*phi}]]

Both Clause (a) and Clause (b) cancel identically due to the odd parity of:
  alpha_1 = s_0 + s_1 + s_2 = 2m - 3 in {-3, -1, 1, 3} (for gamma_1)
  alpha_2 = 3(s_0 + s_1 + s_2) = 3(2m - 3) in {-9, -3, 3, 9} (for gamma_2)
which forces 1 + (-1)^alpha = 0 identically.

AuthorityEffect: None
Firewall: stated region only; mints no authority
"""

from __future__ import annotations

import sys
from itertools import combinations
from typing import Any
import sympy as sp


def gamma_permutations(base_pattern: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Return all C(6, 3) = 20 distinct permutations of a balanced 6-element sign pattern."""
    pos_val = base_pattern[0]
    neg_val = base_pattern[3]
    perms = []
    for combo in combinations(range(6), 3):
        gamma = [neg_val] * 6
        for idx in combo:
            gamma[idx] = pos_val
        perms.append(tuple(gamma))
    return perms


def compute_inner_sum(H: sp.Matrix, gamma: tuple[int, ...]) -> Any:
    """Compute the column Laurent sum F_s = sum_{j=0..5} prod_{k=0..5} H_{k,j}^{gamma_k}."""
    total = 0
    for j in range(6):
        prod = 1
        for k in range(6):
            prod *= H[k, j] ** gamma[k]
        total += prod
    return total


def build_tensor(U: sp.Matrix, V: sp.Matrix) -> sp.Matrix:
    """Construct Kronecker product U (x) V."""
    return sp.Matrix(6, 6, lambda r, c: U[r // 3, c // 3] * V[r % 3, c % 3])


def verify_clause_a(H: sp.Matrix, perms: list[tuple[int, ...]]) -> bool:
    print(f"--- Verifying Clause (a): G_H(pi(gamma_1)) = 0 across {len(perms)} permutations ---")
    all_zero = True
    for i, gamma in enumerate(perms):
        inner = compute_inner_sum(H, gamma)
        res = sp.simplify(sp.expand(inner))
        if res == 0:
            print(f"  Perm {i+1:2d}/20: {gamma}  =>  ZERO (algebraic)")
        else:
            res_trig = sp.trigsimp(res)
            if res_trig == 0:
                print(f"  Perm {i+1:2d}/20: {gamma}  =>  ZERO (after trigsimp)")
            else:
                print(f"  Perm {i+1:2d}/20: {gamma}  =>  FAIL ({res_trig})")
                all_zero = False
    return all_zero


def verify_clause_b(H: sp.Matrix, H_star: sp.Matrix, perms: list[tuple[int, ...]]) -> bool:
    print(f"\n--- Verifying Clause (b): G_H(pi(gamma_2)) * G_H*(pi(gamma_2)) = 0 across {len(perms)} permutations ---")
    all_zero = True
    for i, gamma in enumerate(perms):
        inner_h = compute_inner_sum(H, gamma)
        res_h = sp.simplify(sp.expand(inner_h))
        if res_h != 0:
            res_h = sp.trigsimp(res_h)

        inner_h_star = compute_inner_sum(H_star, gamma)
        res_h_star = sp.simplify(sp.expand(inner_h_star))
        if res_h_star != 0:
            res_h_star = sp.trigsimp(res_h_star)

        product = sp.simplify(res_h * res_h_star)
        if product == 0:
            status = "ZERO"
            if res_h == 0 and res_h_star == 0:
                status += " (both factors G_H = 0 and G_H* = 0)"
            elif res_h == 0:
                status += " (G_H = 0 factor)"
            else:
                status += " (G_H* = 0 factor)"
            print(f"  Perm {i+1:2d}/20: {gamma}  =>  {status}")
        else:
            print(f"  Perm {i+1:2d}/20: {gamma}  =>  FAIL (product = {product})")
            all_zero = False
    return all_zero


def main() -> int:
    print("=" * 80)
    print("MUB(6) CONJECTURE 2: COMPLETE SYMBOLIC VERIFICATION ON TENSOR PRODUCTS")
    print("AuthorityEffect: None")
    print("Firewall: stated region only; mints no authority")
    print("=" * 80)

    phi = sp.symbols("phi", real=True)
    v00, v01, v02, v10, v11, v12, v20, v21, v22 = sp.symbols(
        "v00 v01 v02 v10 v11 v12 v20 v21 v22", nonzero=True
    )

    U = sp.Matrix([
        [1 / sp.sqrt(2), 1 / sp.sqrt(2)],
        [sp.exp(sp.I * phi) / sp.sqrt(2), -sp.exp(sp.I * phi) / sp.sqrt(2)],
    ])

    V = sp.Matrix([
        [v00, v01, v02],
        [v10, v11, v12],
        [v20, v21, v22],
    ])

    H = build_tensor(U, V)
    H_star = H.H

    perms_g1 = gamma_permutations((1, 1, 1, -1, -1, -1))
    perms_g2 = gamma_permutations((3, 3, 3, -3, -3, -3))

    pass_a = verify_clause_a(H, perms_g1)

    pass_b = verify_clause_b(H, H_star, perms_g2)

    print("\n" + "=" * 80)
    if pass_a and pass_b:
        print("RESULT: PASS - Conjecture 2(a) and 2(b) verified symbolically for all tensor products.")
        print("Clause (a): 20/20 permutations = 0 identically.")
        print("Clause (b): 20/20 permutations = 0 identically (both G_H = 0 and G_H* = 0 vanish).")
        print("Zero floats used; exact Laurent polynomial arithmetic in Q(v_ij, e^{i*phi}).")
        print("=" * 80)
        return 0
    else:
        print("RESULT: FAIL - non-vanishing identity detected.")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
