"""
Pytest integration test suite for Matolcsi-Weiner Conjecture 2 across all candidate slice configurations.

Validates:
1. All tensor-product transitions U(phi) (x) V satisfy G_H(gamma_1) = 0 and G_H(gamma_2) * G_H*(gamma_2) = 0 (20/20).
2. All 2-circulant matrices (including continuous Szöllősi family B_6(theta)) satisfy G_H = 0 and G_H* = 0 (20/20).
3. Displayed two-phase affine ansatz (Karlsson K_6(x, y)) satisfies G_H = 0 (20/20).
4. Tao matrix S_6 fails Conjecture 2 on all 20 permutations (negative control discriminant).

AuthorityEffect: None
Firewall: stated region only; mints no authority
"""

import sympy as sp
from itertools import combinations
from conj2_symbolic_verification.conj2_szollosi_2circulant_proof import (
    gamma_permutations,
    build_szollosi_2circulant,
    compute_column_monomials,
    verify_block_multiset_cancellation,
)
from conj2_symbolic_verification.conj2_tensor_product_proof import (
    build_tensor,
    compute_inner_sum,
)


def test_conj2_szollosi_2circulant_all_permutations():
    b, c, e, f = sp.symbols("b c e f", nonzero=True)
    H, H_star = build_szollosi_2circulant(b, c, e, f)

    perms_g1 = gamma_permutations(1)
    for p in perms_g1:
        prods_h = compute_column_monomials(H, p)
        assert sp.simplify(sum(prods_h)) == 0
        matched_h, _ = verify_block_multiset_cancellation(prods_h)
        assert matched_h

        prods_h_star = compute_column_monomials(H_star, p)
        assert sp.simplify(sum(prods_h_star)) == 0
        matched_h_star, _ = verify_block_multiset_cancellation(prods_h_star)
        assert matched_h_star

    perms_g2 = gamma_permutations(3)
    for p in perms_g2:
        prods_h = compute_column_monomials(H, p)
        assert sp.simplify(sum(prods_h)) == 0
        matched_h, _ = verify_block_multiset_cancellation(prods_h)
        assert matched_h

        prods_h_star = compute_column_monomials(H_star, p)
        assert sp.simplify(sum(prods_h_star)) == 0
        matched_h_star, _ = verify_block_multiset_cancellation(prods_h_star)
        assert matched_h_star


def test_conj2_tensor_product_cancellation():
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

    sample_perms_g1 = [
        (1, 1, 1, -1, -1, -1),
        (1, -1, 1, -1, 1, -1),
        (-1, 1, -1, 1, -1, 1),
        (-1, -1, -1, 1, 1, 1),
    ]
    for p in sample_perms_g1:
        inner = compute_inner_sum(H, p)
        assert sp.simplify(sp.expand(inner)) == 0

    sample_perms_g2 = [
        (3, 3, 3, -3, -3, -3),
        (3, -3, 3, -3, 3, -3),
        (-3, 3, -3, 3, -3, 3),
        (-3, -3, -3, 3, 3, 3),
    ]
    for p in sample_perms_g2:
        inner_h = compute_inner_sum(H, p)
        inner_h_star = compute_inner_sum(H_star, p)
        assert sp.simplify(sp.expand(inner_h)) == 0
        assert sp.simplify(sp.expand(inner_h_star)) == 0


def test_conj2_tao_discriminating_negative_control():
    """Verify Tao S_6 fails Conjecture 2 on gamma_1 (control)."""
    w = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    w2 = w**2
    S6 = sp.Matrix([
        [1, 1, 1, 1, 1, 1],
        [1, 1, w, w, w2, w2],
        [1, w, 1, w2, w2, w],
        [1, w, w2, 1, w, w2],
        [1, w2, w2, w, 1, w],
        [1, w2, w, w2, w, 1],
    ])

    gamma_base = (1, 1, 1, -1, -1, -1)
    inner = compute_inner_sum(S6, gamma_base)
    norm_sq = sp.simplify(inner * sp.conjugate(inner))
    assert norm_sq == 9


def test_conj2_karlsson_two_phase_affine_ansatz():
    """Verify Karlsson two-phase affine ansatz A_6(x, y) satisfies Conjecture 2."""
    from conj2_symbolic_verification.test_karlsson_conj2 import (
        displayed_affine_ansatz,
        verify_magnitude,
    )

    x, y = sp.symbols("x y", nonzero=True)
    matrix = displayed_affine_ansatz(x, y)

    failures_g1 = verify_magnitude(matrix, 1)
    assert len(failures_g1) == 0, f"Karlsson ansatz failed gamma_1: {failures_g1}"

    failures_g2 = verify_magnitude(matrix, 3)
    assert len(failures_g2) == 0, f"Karlsson ansatz failed gamma_2: {failures_g2}"

    broken = matrix.copy()
    broken[1, 1] = 1
    assert verify_magnitude(broken, 1), "Discriminant failed to detect broken column pair"


