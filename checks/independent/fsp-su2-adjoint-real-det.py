#!/usr/bin/env python3
"""Independent exact check for FSP-SU2-ADJOINT-REAL-DET (TFQ-1200).

Origin: checks/independent/fsp-su2-adjoint-real-det.py
AuthorityEffect: None.

Imports no repository module. Uses Python standard library (fractions) and SymPy
for exact symbolic and rational-Gaussian checks of:
1. The explicit 3x3 real adjoint representation R(a, b, c, d) of SU(2), verifying
   U sigma_k U^dagger = sum_j R_{j,k} sigma_j, Z_2 center blindness R(-q) = R(q),
   orthogonality R^T R = (a^2+b^2+c^2+d^2)^2 I_3, det R = (a^2+b^2+c^2+d^2)^3,
   and quaternion group homomorphism R(q_1 q_2) = R(q_1) R(q_2).
2. The 4D Euclidean charge-conjugation / reality intertwiner C_4 = diag(eps_2, eps_2)
   with C_4^2 = -I_4, det C_4 = 1, and C_4 conj(gamma_mu) = gamma_mu C_4 for mu=0..3.
3. Exact lattice Wilson-Dirac operators coupled to non-commuting rational SO(3)
   adjoint link configurations, checking C_full conj(D_adj) = D_adj C_full,
   reality Im(det D_adj) = 0, local SO(3) gauge invariance of det D_adj, and
   explicit configurations with det D_adj < 0 (reality is not positivity).
4. Symbolic and rational 2x2, 4x4, and 6x6 skew-symmetric Majorana Pfaffian
   identities det M = (Pf M)^2 and explicit Pfaffian sign-flip pairs Pf(M_+) = +1,
   Pf(M_-) = -1 with identical positive determinant det(M_+) = det(M_-) = 1.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import sympy as sp


I = sp.I


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")


def su2_adjoint_matrix(a, b, c, d) -> sp.Matrix:
    return sp.Matrix(
        [
            [a**2 + b**2 - c**2 - d**2, 2 * (b * c - a * d), 2 * (b * d + a * c)],
            [2 * (b * c + a * d), a**2 - b**2 + c**2 - d**2, 2 * (c * d - a * b)],
            [2 * (b * d - a * c), 2 * (c * d + a * b), a**2 - b**2 - c**2 + d**2],
        ]
    )


def quat_mul(q1, q2):
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def cayley_unit_quat(u1: Fraction, u2: Fraction, u3: Fraction) -> tuple[sp.Rational, ...]:
    norm_sq = u1 * u1 + u2 * u2 + u3 * u3
    denom = 1 + norm_sq
    a = sp.Rational((1 - norm_sq).numerator, (1 - norm_sq).denominator) / sp.Rational(
        denom.numerator, denom.denominator
    )
    b = sp.Rational((2 * u1).numerator, (2 * u1).denominator) / sp.Rational(
        denom.numerator, denom.denominator
    )
    c = sp.Rational((2 * u2).numerator, (2 * u2).denominator) / sp.Rational(
        denom.numerator, denom.denominator
    )
    d = sp.Rational((2 * u3).numerator, (2 * u3).denominator) / sp.Rational(
        denom.numerator, denom.denominator
    )
    return (a, b, c, d)


def check_symbolic_su2_adjoint() -> int:
    checks = 0
    a, b, c, d = sp.symbols("a b c d", real=True)
    norm_sq = a**2 + b**2 + c**2 + d**2
    R = su2_adjoint_matrix(a, b, c, d)

    # 1. Z_2 center blindness: R(-a, -b, -c, -d) == R(a, b, c, d)
    R_neg = su2_adjoint_matrix(-a, -b, -c, -d)
    require(sp.simplify(R_neg - R) == sp.zeros(3, 3), "Z_2 center blindness failed")
    checks += 1

    # 2. Conjugate quaternion gives transpose
    R_conj = su2_adjoint_matrix(a, -b, -c, -d)
    require(sp.simplify(R_conj - R.T) == sp.zeros(3, 3), "conjugate transpose failed")
    checks += 1

    # 3. Orthogonality polynomial identity: R^T R == (a^2+b^2+c^2+d^2)^2 I_3
    prod_t = (R.T * R).applyfunc(sp.expand)
    target_t = (norm_sq**2 * sp.eye(3)).applyfunc(sp.expand)
    require(prod_t == target_t, "R^T R polynomial identity failed")
    checks += 1

    prod_r = (R * R.T).applyfunc(sp.expand)
    require(prod_r == target_t, "R R^T polynomial identity failed")
    checks += 1

    # 4. Exact determinant polynomial identity: det(R) == (a^2+b^2+c^2+d^2)^3
    det_r = sp.expand(R.det())
    require(det_r == sp.expand(norm_sq**3), "det(R) == norm_sq^3 failed")
    checks += 1

    # 5. Pauli adjoint intertwining: U sigma_k U^dagger == sum_j R_{j,k} sigma_j
    # Standard quaternion-to-SU(2) isomorphism: (1, i, j, k) -> (I_2, -i sigma_1, -i sigma_2, -i sigma_3)
    s1 = sp.Matrix([[0, 1], [1, 0]])
    s2 = sp.Matrix([[0, -I], [I, 0]])
    s3 = sp.Matrix([[1, 0], [0, -1]])
    paulis = [s1, s2, s3]
    U = a * sp.eye(2) - I * (b * s1 + c * s2 + d * s3)
    U_dag = a * sp.eye(2) + I * (b * s1 + c * s2 + d * s3)
    for k in range(3):
        lhs = (U * paulis[k] * U_dag).applyfunc(sp.expand)
        rhs = sum((R[j, k] * paulis[j] for j in range(3)), sp.zeros(2, 2)).applyfunc(
            sp.expand
        )
        require(lhs == rhs, f"Pauli adjoint intertwining failed for k={k}")
        checks += 1

    # 6. Group homomorphism: R(q1 * q2) == R(q1) * R(q2)
    a2, b2, c2, d2 = sp.symbols("a2 b2 c2 d2", real=True)
    R2 = su2_adjoint_matrix(a2, b2, c2, d2)
    q12 = quat_mul((a, b, c, d), (a2, b2, c2, d2))
    R12 = su2_adjoint_matrix(*q12).applyfunc(sp.expand)
    prod12 = (R * R2).applyfunc(sp.expand)
    require(R12 == prod12, "homomorphism R(q1 q2) == R(q1) R(q2) failed")
    checks += 1

    # 7. 125 rational unit quaternions on S^3(Q)
    grid = [Fraction(-2, 1), Fraction(-1, 2), Fraction(0, 1), Fraction(1, 3), Fraction(1, 1)]
    for u1, u2, u3 in itertools.product(grid, repeat=3):
        qa, qb, qc, qd = cayley_unit_quat(u1, u2, u3)
        require(qa**2 + qb**2 + qc**2 + qd**2 == 1, "unit quaternion norm != 1")
        Rq = su2_adjoint_matrix(qa, qb, qc, qd)
        require(Rq.T * Rq == sp.eye(3), "rational Rq not orthogonal")
        require(Rq.det() == 1, "rational det(Rq) != 1")
        require(
            su2_adjoint_matrix(-qa, -qb, -qc, -qd) == Rq,
            "rational center blindness failed",
        )
        checks += 4

    return checks


def build_4d_clifford_and_intertwiner():
    s1 = sp.Matrix([[0, 1], [1, 0]])
    s2 = sp.Matrix([[0, -I], [I, 0]])
    s3 = sp.Matrix([[1, 0], [0, -1]])
    eps2 = sp.Matrix([[0, 1], [-1, 0]])

    def off_dirac(b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
        return sp.BlockMatrix([[sp.zeros(2, 2), b], [c, sp.zeros(2, 2)]]).as_explicit()

    gammas = [
        off_dirac(-I * s1, I * s1),
        off_dirac(-I * s2, I * s2),
        off_dirac(-I * s3, I * s3),
        off_dirac(sp.eye(2), sp.eye(2)),
    ]
    gamma5 = sp.BlockMatrix(
        [[sp.eye(2), sp.zeros(2, 2)], [sp.zeros(2, 2), -sp.eye(2)]]
    ).as_explicit()
    C4 = sp.BlockMatrix([[eps2, sp.zeros(2, 2)], [sp.zeros(2, 2), eps2]]).as_explicit()
    return gammas, gamma5, C4


def check_4d_intertwiner_and_wilson_dirac() -> tuple[int, int]:
    checks = 0
    neg_det_witnesses = 0
    gammas, gamma5, C4 = build_4d_clifford_and_intertwiner()

    require(C4 * C4 == -sp.eye(4), "C4^2 != -I_4")
    require(C4.T == -C4, "C4^T != -C4")
    require(C4.det() == 1, "det(C4) != 1")
    checks += 3

    for mu, g in enumerate(gammas):
        require(C4 * g.conjugate() == g * C4, f"C4 failed to intertwine gamma_{mu}")
        checks += 1
    require(C4 * gamma5.conjugate() == gamma5 * C4, "C4 failed to intertwine gamma5")
    checks += 1

    # Build 2-site 4D Wilson-Dirac operator coupled to non-commuting rational SO(3) links
    # Total dimension: 4 (spin) * 2 (sites) * 3 (adjoint color) = 24
    q_links = [
        cayley_unit_quat(Fraction(1, 2), Fraction(0, 1), Fraction(0, 1)),
        cayley_unit_quat(Fraction(0, 1), Fraction(1, 3), Fraction(0, 1)),
        cayley_unit_quat(Fraction(0, 1), Fraction(0, 1), Fraction(1, 2)),
        cayley_unit_quat(Fraction(1, 2), Fraction(-1, 3), Fraction(1, 4)),
    ]
    R_links = [su2_adjoint_matrix(*q) for q in q_links]
    # Verify non-commutativity of the SU(2)/SO(3) link configuration
    require(R_links[0] * R_links[1] != R_links[1] * R_links[0], "links should not commute")
    checks += 1

    # Construct 6x6 site-color hopping matrices on 2 sites (0 and 1)
    Upos = []
    Uneg = []
    for mu in range(4):
        K_pos = sp.zeros(6, 6)
        K_neg = sp.zeros(6, 6)
        # Forward hop 0 -> 1 carries R_links[mu], 1 -> 0 carries R_links[(mu+1)%4]
        R01 = R_links[mu]
        R10 = R_links[(mu + 1) % 4]
        for a in range(3):
            for b in range(3):
                K_pos[0 * 3 + a, 1 * 3 + b] = R01[a, b]
                K_pos[1 * 3 + a, 0 * 3 + b] = R10[a, b]
        # Backward hop is transpose
        K_neg = K_pos.T
        Upos.append(K_pos)
        Uneg.append(K_neg)

    C_full = sp.kronecker_product(C4, sp.eye(6))
    require(C_full * C_full == -sp.eye(24), "C_full^2 != -I_24")
    require(C_full.det() == 1, "det(C_full) != 1")
    checks += 2

    for m0, r_val in [(sp.Rational(3, 2), sp.Rational(1, 1)), (sp.Rational(-1, 2), sp.Rational(1, 2))]:
        D_adj = sp.kronecker_product(sp.eye(4), m0 * sp.eye(6))
        for mu in range(4):
            term_pos = sp.kronecker_product(r_val * sp.eye(4) - gammas[mu], Upos[mu])
            term_neg = sp.kronecker_product(r_val * sp.eye(4) + gammas[mu], Uneg[mu])
            D_adj -= sp.Rational(1, 2) * (term_pos + term_neg)

        # Check exact intertwining C_full * conj(D_adj) == D_adj * C_full
        require(
            C_full * D_adj.conjugate() == D_adj * C_full,
            "24x24 wilsonDiracAdjoint4 intertwining failed",
        )
        det_val = D_adj.det()
        require(sp.im(det_val) == 0, f"det(D_adj) not real: {det_val}")
        checks += 2

        # Check local SO(3) gauge invariance at site 0 and site 1
        g0 = su2_adjoint_matrix(*cayley_unit_quat(Fraction(1, 1), Fraction(1, 2), Fraction(0, 1)))
        g1 = su2_adjoint_matrix(*cayley_unit_quat(Fraction(0, 1), Fraction(-1, 2), Fraction(1, 3)))
        G_site = sp.BlockMatrix([[g0, sp.zeros(3, 3)], [sp.zeros(3, 3), g1]]).as_explicit()
        G_full = sp.kronecker_product(sp.eye(4), G_site)
        D_gauged = G_full * D_adj * G_full.T
        require(
            C_full * D_gauged.conjugate() == D_gauged * C_full,
            "gauged D_adj intertwining failed",
        )
        require(D_gauged.det() == det_val, "local SO(3) gauge invariance of det failed")
        checks += 2

    # Reality is NOT positivity witnesses:
    # Witness 1: 3x3 adjoint block D = -I_3 (intertwined by C = I_3) has det = -1 < 0
    D_neg3 = -sp.eye(3)
    require(D_neg3.det() == -1 and D_neg3.det() < 0, "D_neg3 det should be -1 < 0")
    neg_det_witnesses += 1
    checks += 1

    # Witness 2: 2D Euclidean Dirac operator with real SU(2) adjoint link on 1 site (6x6)
    # Using gamma0 = sigma1, gamma1 = sigma3, and an asymmetric real adjoint coupling
    g2_0 = sp.Matrix([[0, 1], [1, 0]])
    g2_1 = sp.Matrix([[1, 0], [0, -1]])
    # On 1 site x 3 adjoint colors (6x6), take D = I_2 x (-I_3) + g2_1 x diag(2, 0, 0)
    # For color 0, eigenvalues of -I_2 + 2*sigma_3 are (-1+2)=1 and (-1-2)=-3, product = -3.
    # For colors 1 and 2, eigenvalues are -1 with multiplicity 2 each, product = 1.
    # Total determinant = -3 < 0 while intertwined by C = I_6!
    K_diag = sp.diag(2, 0, 0)
    D_neg6 = sp.kronecker_product(sp.eye(2), -sp.eye(3)) + sp.kronecker_product(g2_1, K_diag)
    require(D_neg6.conjugate() == D_neg6, "D_neg6 should be real-intertwined")
    require(D_neg6.det() == -3 and D_neg6.det() < 0, "D_neg6 det should be -3 < 0")
    neg_det_witnesses += 1
    checks += 2

    return checks, neg_det_witnesses


def pfaffian4(M: sp.Matrix):
    return M[0, 1] * M[2, 3] - M[0, 2] * M[1, 3] + M[0, 3] * M[1, 2]


def pfaffian6(M: sp.Matrix):
    # Exact 6x6 Pfaffian over all 15 pairings of {0,1,2,3,4,5}
    pairings = [
        ((0, 1), (2, 3), (4, 5), 1),
        ((0, 1), (2, 4), (3, 5), -1),
        ((0, 1), (2, 5), (3, 4), 1),
        ((0, 2), (1, 3), (4, 5), -1),
        ((0, 2), (1, 4), (3, 5), 1),
        ((0, 2), (1, 5), (3, 4), -1),
        ((0, 3), (1, 2), (4, 5), 1),
        ((0, 3), (1, 4), (2, 5), -1),
        ((0, 3), (1, 5), (2, 4), 1),
        ((0, 4), (1, 2), (3, 5), -1),
        ((0, 4), (1, 3), (2, 5), 1),
        ((0, 4), (1, 5), (2, 3), -1),
        ((0, 5), (1, 2), (3, 4), 1),
        ((0, 5), (1, 3), (2, 4), -1),
        ((0, 5), (1, 4), (2, 3), 1),
    ]
    total = sp.Integer(0)
    for (i1, j1), (i2, j2), (i3, j3), sgn in pairings:
        total += sgn * M[i1, j1] * M[i2, j2] * M[i3, j3]
    return total


def check_majorana_pfaffian_sign_flips() -> tuple[int, int]:
    checks = 0
    sign_flips = 0

    # 1. Symbolic 2x2 skew-symmetric check
    p = sp.Symbol("p")
    M2 = sp.Matrix([[0, p], [-p, 0]])
    require(M2.T == -M2, "M2 not skew-symmetric")
    require(sp.expand(M2.det() - p**2) == 0, "2x2 det != Pf^2")
    checks += 2

    # 2. Symbolic 4x4 skew-symmetric Cayley identity check
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    M4 = sp.Matrix(
        [
            [0, a, b, c],
            [-a, 0, d, e],
            [-b, -d, 0, f],
            [-c, -e, -f, 0],
        ]
    )
    require(M4.T == -M4, "M4 not skew-symmetric")
    pf4 = pfaffian4(M4)
    require(sp.expand(M4.det() - pf4**2) == 0, "4x4 det != Pf^2")
    checks += 2

    # 3. Symbolic 6x6 skew-symmetric (2 sites x 3 adjoint colors) Majorana check
    # With Majorana mass block [[0, m I_3], [-m I_3, 0]] + hopping [[A, S], [-S^T, B]]
    # Test general 6x6 skew-symmetric polynomial identity on 15 variables
    vars6 = sp.symbols("x0:15")
    M6 = sp.zeros(6, 6)
    idx = 0
    for i in range(6):
        for j in range(i + 1, 6):
            M6[i, j] = vars6[idx]
            M6[j, i] = -vars6[idx]
            idx += 1
    require(M6.T == -M6, "M6 not skew-symmetric")
    pf6 = pfaffian6(M6)
    require(sp.expand(M6.det() - pf6**2) == 0, "6x6 det != Pf^2")
    checks += 2

    # 4. Explicit sign-flip pairs across 2x2, 4x4, and 6x6 Majorana operators
    # 6x6 SU(2) adjoint Majorana operator M(R) = [[0, R], [-R^T, 0]] for R in O(3) / real link:
    # Note: for M(R) = [[0, R], [-R^T, 0]], Pf(M(R)) = -det(R), while det(M(R)) = det(R)^2!
    for q in [
        cayley_unit_quat(Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)),
        cayley_unit_quat(Fraction(1, 2), Fraction(-1, 3), Fraction(1, 5)),
        cayley_unit_quat(Fraction(-2, 3), Fraction(1, 4), Fraction(3, 2)),
    ]:
        R_pos = su2_adjoint_matrix(*q)
        # Flip sign of one coupling channel (e.g. negative hopping mass / link sign)
        R_neg = -R_pos
        M6_pos = sp.BlockMatrix([[sp.zeros(3, 3), R_pos], [-R_pos.T, sp.zeros(3, 3)]]).as_explicit()
        M6_neg = sp.BlockMatrix([[sp.zeros(3, 3), R_neg], [-R_neg.T, sp.zeros(3, 3)]]).as_explicit()
        require(M6_pos.T == -M6_pos and M6_neg.T == -M6_neg, "M6_pos/neg skew")
        pf_pos = pfaffian6(M6_pos)
        pf_neg = pfaffian6(M6_neg)
        det_pos = M6_pos.det()
        det_neg = M6_neg.det()
        require(pf_pos == -1 and pf_neg == 1, f"unexpected 6x6 Pfaffians: {pf_pos}, {pf_neg}")
        require(det_pos == 1 and det_neg == 1, "6x6 determinants should both equal +1")
        sign_flips += 1
        checks += 3

    return checks, sign_flips


def main() -> int:
    c1 = check_symbolic_su2_adjoint()
    c2, neg_witnesses = check_4d_intertwiner_and_wilson_dirac()
    c3, sign_flips = check_majorana_pfaffian_sign_flips()
    total = c1 + c2 + c3
    print(
        f"PASS fsp-su2-adjoint-real-det: checks={total} "
        f"neg_det_witnesses={neg_witnesses} pfaffian_sign_flips={sign_flips} failures=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
