#!/usr/bin/env python3
"""
Independent check for Campaign Target 3: CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT
AuthorityEffect: None.
Outcome: Reduced.

Verifies:
1. Exact symbolic multiplicativity of 2x2 determinant under local maps A M B^T.
2. Product state determinant vanishing: det(a ⊗ b) = 0.
3. Invariance of zero determinant (Schmidt rank <= 1) under all local maps.
4. Exact phase family determinant det(M_u) = (u - 1)/4 and concurrence C^2 = |u - 1|^2 / 4.
5. Exact Pythagorean unit phase u = (3 + 4i)/5 has |u|^2 = 1 and C^2 = 1/5.
6. Impossibility of producing C^2 = 1/5 from separable state via any local operation pair (A, B).
7. LOCC Kraus channel product-state preservation: every local Kraus branch maps product pure states to product pure states.

Zero repository imports (only standard library and SymPy).
"""

from fractions import Fraction
import sys
import sympy as sp


def check_symbolic_local_action_determinant():
    """Verify det(A * M * B^T) = det(A) * det(M) * det(B) symbolically."""
    A00, A01, A10, A11 = sp.symbols('A00 A01 A10 A11')
    B00, B01, B10, B11 = sp.symbols('B00 B01 B10 B11')
    M00, M01, M10, M11 = sp.symbols('M00 M01 M10 M11')

    A = sp.Matrix([[A00, A01], [A10, A11]])
    B = sp.Matrix([[B00, B01], [B10, B11]])
    M = sp.Matrix([[M00, M01], [M10, M11]])

    transformed = A * M * B.T
    det_transformed = sp.simplify(transformed.det())
    det_product = sp.simplify(A.det() * M.det() * B.det())

    diff = sp.simplify(det_transformed - det_product)
    assert diff == 0, f"Determinant multiplicativity failed: diff = {diff}"

    # If det(M) = 0, transformed det is identically 0
    det_zero_case = sp.simplify(det_transformed.subs(M11, (M01 * M10) / M00))
    assert det_zero_case == 0, "Zero determinant preservation failed"
    print("  [PASS] Symbolic local operation determinant multiplicativity: det(A M B^T) = det(A) det(M) det(B)")


def check_product_state_zero_determinant():
    """Verify that any pure product state a ⊗ b has zero determinant and local maps preserve it."""
    a0, a1, b0, b1 = sp.symbols('a0 a1 b0 b1')
    M_prod = sp.Matrix([[a0 * b0, a0 * b1], [a1 * b0, a1 * b1]])
    det_prod = sp.simplify(M_prod.det())
    assert det_prod == 0, f"Product state determinant not zero: {det_prod}"

    A00, A01, A10, A11 = sp.symbols('A00 A01 A10 A11')
    B00, B01, B10, B11 = sp.symbols('B00 B01 B10 B11')
    A = sp.Matrix([[A00, A01], [A10, A11]])
    B = sp.Matrix([[B00, B01], [B10, B11]])

    M_mapped = A * M_prod * B.T
    det_mapped = sp.simplify(M_mapped.det())
    assert det_mapped == 0, f"Mapped product state determinant not zero: {det_mapped}"
    print("  [PASS] Pure product state determinant is identically zero and preserved under A ⊗ B")


def check_phase_family_determinant_and_concurrence():
    """Verify det(M_u) = (u - 1)/4 and C^2(M_u) = |u - 1|^2 / 4."""
    u_re, u_im = sp.symbols('u_re u_im', real=True)
    u = u_re + sp.I * u_im

    # M_u = 1/2 * [[1, 1], [1, u]]
    M_u = sp.Matrix([
        [sp.Rational(1, 2), sp.Rational(1, 2)],
        [sp.Rational(1, 2), u / 2]
    ])

    det_Mu = sp.simplify(M_u.det())
    expected_det = sp.simplify((u - 1) / 4)
    assert sp.simplify(det_Mu - expected_det) == 0, f"det(M_u) mismatch: {det_Mu} != {expected_det}"

    # Squared modulus of determinant: |det(M_u)|^2
    normSq_det = sp.simplify(sp.re(det_Mu)**2 + sp.im(det_Mu)**2)
    expected_normSq_det = sp.simplify(((u_re - 1)**2 + u_im**2) / 16)
    assert sp.simplify(normSq_det - expected_normSq_det) == 0

    # Squared concurrence C^2 = 4 |det(M)|^2
    concurrence_sq = sp.simplify(4 * normSq_det)
    expected_C2 = sp.simplify(((u_re - 1)**2 + u_im**2) / 4)
    assert sp.simplify(concurrence_sq - expected_C2) == 0, f"Concurrence mismatch: {concurrence_sq} != {expected_C2}"
    print("  [PASS] Phase family det(M_u) = (u - 1)/4 and C^2(M_u) = |u - 1|^2 / 4")


def check_exact_pythagorean_concurrence():
    """Verify exact arithmetic for Pythagorean unit u = (3 + 4i)/5 using fractions.Fraction."""
    u_re = Fraction(3, 5)
    u_im = Fraction(4, 5)

    # Unit modulus
    norm_u_sq = u_re**2 + u_im**2
    assert norm_u_sq == Fraction(1, 1), f"|u|^2 = {norm_u_sq} != 1"

    # det(M_u) = (u - 1) / 4
    det_re = (u_re - 1) / 4  # (3/5 - 1)/4 = (-2/5)/4 = -1/10
    det_im = u_im / 4        # (4/5)/4 = 1/5
    assert det_re == Fraction(-1, 10)
    assert det_im == Fraction(1, 5)

    normSq_det = det_re**2 + det_im**2  # (-1/10)^2 + (1/5)^2 = 1/100 + 4/100 = 5/100 = 1/20
    assert normSq_det == Fraction(1, 20)

    # Concurrence squared: C^2 = 4 * |det|^2 = 4 * 1/20 = 1/5
    C2 = 4 * normSq_det
    assert C2 == Fraction(1, 5), f"C^2 = {C2} != 1/5"

    # Initial state u = 1:
    det_init_re = Fraction(0, 1)
    det_init_im = Fraction(0, 1)
    C2_init = Fraction(0, 1)

    delta_C2 = C2 - C2_init
    assert delta_C2 == Fraction(1, 5), f"Delta C^2 = {delta_C2} != 1/5"
    print(f"  [PASS] Exact Pythagorean unit u = (3 + 4i)/5: |u|^2 = {norm_u_sq}, C^2 = {C2}, delta_C^2 = {delta_C2}")


def check_locc_kraus_branch_preservation():
    """Verify that any LOCC Kraus operator A_i ⊗ B_j preserves product states and cannot raise rank."""
    # A generic product state |psi> = |a> ⊗ |b>
    # Under Kraus operator A_i ⊗ B_j:
    # (A_i ⊗ B_j)(|a> ⊗ |b>) = (A_i |a>) ⊗ (B_j |b>)
    # Which is manifestly a product vector |a'> ⊗ |b'>.
    a = sp.Matrix([sp.symbols('a0'), sp.symbols('a1')])
    b = sp.Matrix([sp.symbols('b0'), sp.symbols('b1')])

    A_i = sp.Matrix([[sp.symbols('Ai00'), sp.symbols('Ai01')], [sp.symbols('Ai10'), sp.symbols('Ai11')]])
    B_j = sp.Matrix([[sp.symbols('Bj00'), sp.symbols('Bj01')], [sp.symbols('Bj10'), sp.symbols('Bj11')]])

    a_prime = A_i * a
    b_prime = B_j * b

    # Amplitude matrix of |a'> ⊗ |b'>:
    M_prime = a_prime * b_prime.T
    det_M_prime = sp.simplify(M_prime.det())
    assert det_M_prime == 0, f"Kraus branch output determinant not zero: {det_M_prime}"
    print("  [PASS] LOCC Kraus branch (A_i ⊗ B_j) maps product vector to product vector with det = 0")


def main():
    print("=== CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT Independent Verification ===")
    check_symbolic_local_action_determinant()
    check_product_state_zero_determinant()
    check_phase_family_determinant_and_concurrence()
    check_exact_pythagorean_concurrence()
    check_locc_kraus_branch_preservation()
    print("=== All 5 independent mathematical checks passed successfully (exit 0) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
