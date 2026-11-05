#!/usr/bin/env python3
"""
Independent check for Campaign Target 3: CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT
AuthorityEffect: None.
Outcome: Narrowed (finite shadow; the node stays IMPORTED_ASSUMPTION).

Verifies (exact arithmetic; no floats):
1. Exact symbolic multiplicativity of 2x2 determinant under local maps A M B^T.
2. Product state determinant vanishing: det(a (x) b) = 0, preserved under A (x) B.
3. The coefficient matrix of (A (x) B) psi is A M B^T (row-major vectorisation, via the
   Kronecker product), the formula the Lean module takes as its definition of a local map.
4. Exact phase family determinant det(M_u) = (u - 1)/4 and normalized C^2 = 4|u - 1|^2 / (3 + |u|^2)^2; for |u|=1 this is |u-1|^2/4.
5. Exact Pythagorean unit phase u = (3 + 4i)/5 has |u|^2 = 1 and C^2 = 1/5.
6. Product-vector Kraus branch A_i (x) B_j keeps determinant 0.
7. rank(A M B^T) <= rank(M) on a deterministic family of exact rational matrices of
   several (non-square) shapes, including rank-deficient M and singular A, B.

Not checked (and not claimed): mixed states, channels with ancillas, mixtures, LOCC, any
mediating system, gravity. Items 1 to 7 are a finite spot-check and a symbolic identity, not a
proof of the general rank inequality; that is the Lean theorem schmidtRank_local_le.

Imports checker infrastructure only; no production implementation.
"""

from __future__ import annotations

from fractions import Fraction
from collections.abc import Callable
from pathlib import Path
import sys
import sympy as sp

# Shared checker infrastructure only; no production implementation is imported.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, Violation
from checker_support.cases import Cases
from checker_support.gaussian_rational import GaussianRational
from checker_support.domains import rational


def _cases(value: Cases | None) -> Cases:
    if value is None:
        return Cases()
    if type(value) is not Cases:
        raise Violation("input", "verification recorder must be Cases")
    return value


def check_symbolic_local_action_determinant(cases: Cases | None = None) -> None:
    """Verify det(A * M * B^T) = det(A) * det(M) * det(B) symbolically."""
    cases = _cases(cases)
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
    cases.require(diff == 0, f"Determinant multiplicativity failed: diff = {diff}")

    # Chart M00 != 0; when M00=0 either M01 or M10 is zero.
    for entry in (M01, M10):
        cases.require(sp.simplify(det_transformed.subs({M00: 0, entry: 0})) == 0,
               "zero-determinant chart M00=0")
    det_zero_case = sp.simplify(det_transformed.subs(M11, (M01 * M10) / M00))
    cases.require(det_zero_case == 0, "Zero determinant preservation failed")
    print("  [PASS] Symbolic local operation determinant multiplicativity: det(A M B^T) = det(A) det(M) det(B)")


def check_product_state_zero_determinant(cases: Cases | None = None) -> None:
    """Verify that any pure product state a ⊗ b has zero determinant and local maps preserve it."""
    cases = _cases(cases)
    a0, a1, b0, b1 = sp.symbols('a0 a1 b0 b1')
    M_prod = sp.Matrix([[a0 * b0, a0 * b1], [a1 * b0, a1 * b1]])
    det_prod = sp.simplify(M_prod.det())
    cases.require(det_prod == 0, f"Product state determinant not zero: {det_prod}")

    A00, A01, A10, A11 = sp.symbols('A00 A01 A10 A11')
    B00, B01, B10, B11 = sp.symbols('B00 B01 B10 B11')
    A = sp.Matrix([[A00, A01], [A10, A11]])
    B = sp.Matrix([[B00, B01], [B10, B11]])

    M_mapped = A * M_prod * B.T
    det_mapped = sp.simplify(M_mapped.det())
    cases.require(det_mapped == 0, f"Mapped product state determinant not zero: {det_mapped}")
    print("  [PASS] Pure product state determinant is identically zero and preserved under A ⊗ B")


def check_phase_family_determinant_and_concurrence(cases: Cases | None = None) -> None:
    """Verify det(M_u) = (u - 1)/4 and normalized C^2(M_u) = 4|u - 1|^2 / (3 + |u|^2)^2."""
    cases = _cases(cases)
    u_re, u_im = sp.symbols('u_re u_im', real=True)
    u = u_re + sp.I * u_im

    # M_u = 1/2 * [[1, 1], [1, u]]
    M_u = sp.Matrix([
        [sp.Rational(1, 2), sp.Rational(1, 2)],
        [sp.Rational(1, 2), u / 2]
    ])

    det_Mu = sp.simplify(M_u.det())
    expected_det = sp.simplify((u - 1) / 4)
    cases.require(sp.simplify(det_Mu - expected_det) == 0, f"det(M_u) mismatch: {det_Mu} != {expected_det}")

    # Squared modulus of determinant: |det(M_u)|^2
    normSq_det = sp.simplify(sp.re(det_Mu)**2 + sp.im(det_Mu)**2)
    expected_normSq_det = sp.simplify(((u_re - 1)**2 + u_im**2) / 16)
    cases.require(sp.simplify(normSq_det - expected_normSq_det) == 0, "phase-family determinant squared modulus")

    # Norm squared is (3+|u|^2)/4, not one for arbitrary u.
    state_norm_sq = (3 + u_re**2 + u_im**2) / 4
    concurrence_sq = sp.simplify(4 * normSq_det / state_norm_sq**2)
    expected_C2 = sp.simplify(4 * ((u_re - 1)**2 + u_im**2) / (3 + u_re**2 + u_im**2)**2)
    cases.require(sp.simplify(concurrence_sq - expected_C2) == 0, f"Concurrence mismatch: {concurrence_sq} != {expected_C2}")
    cases.require(concurrence_sq.subs({u_re: 0, u_im: 0}) == sp.Rational(4, 9), "normalized concurrence at u=0")
    print("  [PASS] General normalized concurrence; u=0 boundary")


def check_exact_pythagorean_concurrence(cases: Cases | None = None) -> None:
    """Verify exact arithmetic for Pythagorean unit u = (3 + 4i)/5 using fractions.Fraction."""
    cases = _cases(cases)
    u_re = Fraction(3, 5)
    u_im = Fraction(4, 5)

    # Unit modulus
    norm_u_sq = u_re**2 + u_im**2
    cases.require(norm_u_sq == Fraction(1, 1), f"|u|^2 = {norm_u_sq} != 1")

    # det(M_u) = (u - 1) / 4
    det_re = (u_re - 1) / 4  # (3/5 - 1)/4 = (-2/5)/4 = -1/10
    det_im = u_im / 4        # (4/5)/4 = 1/5
    cases.require(det_re == Fraction(-1, 10), "Pythagorean determinant real component")
    cases.require(det_im == Fraction(1, 5), "Pythagorean determinant imaginary component")

    normSq_det = det_re**2 + det_im**2  # (-1/10)^2 + (1/5)^2 = 1/100 + 4/100 = 5/100 = 1/20
    cases.require(normSq_det == Fraction(1, 20), "Pythagorean determinant squared modulus")

    # Concurrence squared: C^2 = 4 * |det|^2 = 4 * 1/20 = 1/5
    C2 = 4 * normSq_det
    cases.require(C2 == Fraction(1, 5), f"C^2 = {C2} != 1/5")

    # Initial state u = 1:
    C2_init = Fraction(0, 1)

    delta_C2 = C2 - C2_init
    cases.require(delta_C2 == Fraction(1, 5), f"Delta C^2 = {delta_C2} != 1/5")
    print(f"  [PASS] Exact Pythagorean unit u = (3 + 4i)/5: |u|^2 = {norm_u_sq}, C^2 = {C2}, delta_C^2 = {delta_C2}")


def check_product_branch_preservation(cases: Cases | None = None) -> None:
    """Verify that a product-vector Kraus branch A_i (x) B_j maps a product vector to a product vector."""
    cases = _cases(cases)
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
    cases.require(det_M_prime == 0, f"Kraus branch output determinant not zero: {det_M_prime}")
    print("  [PASS] Product-vector branch (A_i ⊗ B_j) maps product vector to product vector with det = 0")


def check_kron_vectorisation_matches_AMBT(cases: Cases | None = None) -> None:
    """(A (x) B) vec(M) = vec(A M B^T) with row-major vec, for symbolic 2x2 A, B, M."""
    cases = _cases(cases)
    A = sp.Matrix(2, 2, sp.symbols('A0:4'))
    B = sp.Matrix(2, 2, sp.symbols('B0:4'))
    M = sp.Matrix(2, 2, sp.symbols('M0:4'))
    def vec(matrix: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]])
    lhs = sp.kronecker_product(A, B) * vec(M)
    rhs = vec(A * M * B.T)
    cases.require((lhs - rhs).applyfunc(sp.expand) == sp.zeros(4, 1), "kron vs A M B^T mismatch")
    print("  [PASS] (A (x) B) vec(M) = vec(A M B^T): the matrix action used by the Lean module")


def check_rank_nonincrease_exact_family(cases: Cases | None = None) -> None:
    """rank(A M B^T) <= rank(M) over Q for a deterministic family of integer matrices."""
    cases = _cases(cases)
    seed = 12345
    def nxt() -> int:
        nonlocal seed
        seed = (1103515245 * seed + 12345) % (2 ** 31)
        return (seed >> 8) % 7 - 3  # integers in -3..3
    def rand(r: int, c: int) -> sp.Matrix:
        return sp.Matrix(r, c, lambda i, j: nxt())
    count = 0
    strict = 0
    for (m, p, q, n) in [(2, 2, 2, 2), (3, 2, 4, 3), (4, 3, 3, 2), (2, 4, 3, 5), (3, 3, 3, 3)]:
        for _ in range(60):
            A, M, B = rand(m, p), rand(p, q), rand(n, q)
            if _ % 3 == 0:
                M = rand(p, 1) * rand(1, q)  # rank <= 1
            r_after = (A * M * B.T).rank()
            r_before = M.rank()
            cases.require(r_after <= r_before, f"rank increased from {r_before} to {r_after}: A={A}, M={M}, B={B}")
            count += 1
            strict += r_after < r_before
    print(f"  [PASS] rank(A M B^T) <= rank(M) on {count} exact rational cases ({strict} strictly lower)")


def normalized_concurrence_squared(u_re: object, u_im: object) -> Fraction:
    """Exact normalized phase-family concurrence with bounded rational values.

    Every derived norm/defect/normalizer and result is admitted to4096 bits;
    an exceeded bound is a resource refusal, not a zero or clipped concurrence.
    """
    phase = GaussianRational(u_re, u_im)
    norm = rational(phase.norm_sq(), "phase norm")
    defect = rational((phase-GaussianRational(1)).norm_sq(), "phase defect")
    normalizer = rational(3+norm, "state normalization")
    denominator = rational(normalizer*normalizer, "squared normalization")
    return rational(4*defect/denominator, "normalized concurrence squared")


def main() -> int:
    cases = Cases()
    operations: tuple[Callable[[Cases | None], None], ...] = (
        check_symbolic_local_action_determinant, check_product_state_zero_determinant,
        check_kron_vectorisation_matches_AMBT, check_phase_family_determinant_and_concurrence,
        check_exact_pythagorean_concurrence, check_product_branch_preservation,
        check_rank_nonincrease_exact_family,
    )
    print("=== CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT Independent Verification ===")
    for operation in operations:
        operation(cases)
    print(f"=== {cases.checks} executed obligations in {len(operations)} groups passed (exit0) ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
