#!/usr/bin/env python3
"""Independent verification for ADS-CFT-DUALITY-IMPORT (TFQ-2202).

AuthorityEffect: None.

Recomputes all concrete numbers, algebraic identities, and finite-matrix
witnesses in lean4/CampaignAdsCftDualityImport.lean using Python's exact
fractions.Fraction and SymPy, without importing any repository code:

1. GKPW scalar mass-dimension quadratic (m R)^2 = Delta (Delta - d),
   shadow involution d - Delta, Vieta sum/product, completed square
   (2 Delta - d)^2 = d^2 + 4 Delta (Delta - d), Breitenlohner-Freedman
   lower bound -(d^2)/4, double root Delta = d/2 at BF saturation,
   concrete points in d = 4 (AdS_5/CFT_4) and d = 2 (AdS_3/CFT_2),
   absence of rational roots below the BF bound, and non-square
   discriminant D = 20 at (d = 4, mSq = 1).
2. 't Hooft large-N ribbon-graph double-line weight g_YM^{2(E-V)} N^F,
   factorization (g_YM^2)^{E-V} N^F N^{E-V} = lambda^{E-V} N^F,
   planar (g = 0, V=2, E=3, F=3, chi=2) vs. genus-1 torus (g = 1, V=2, E=3, F=1, chi=0)
   1/N^2 suppression, and U(N)/SU(N) adjoint dimension split N^2 = (N^2 - 1) + 1.
3. Finite isometric bulk-to-boundary operator pushforward V O_bulk V^T and
   boundary-to-bulk pullback V^T O_bdry V, exact recovery V^T (V O_bulk V^T) V = O_bulk,
   multiplicativity on the code subspace, quadratic correlator matching
   <V psi, O_bdry V psi> = <psi, (V^T O_bdry V) psi>, and the explicit 1-to-2
   isometry V = [[1], [0]] with nonzero boundary annihilator [[0, 0], [0, 1]]
   whose bulk pullback is 0 and which lies outside the image of pushforward.
"""

from __future__ import annotations

from fractions import Fraction
import sys
import sympy as sp


def gkpw_mass_sq(d: Fraction, delta: Fraction) -> Fraction:
    return delta * (delta - d)


def shadow_dimension(d: Fraction, delta: Fraction) -> Fraction:
    return d - delta


def gkpw_discriminant(d: Fraction, m_sq: Fraction) -> Fraction:
    return d * d + 4 * m_sq


def bf_bound(d: Fraction) -> Fraction:
    return -(d * d) / Fraction(4, 1)


def gkpw_root_plus(d: Fraction, s: Fraction) -> Fraction:
    return (d + s) / Fraction(2, 1)


def gkpw_root_minus(d: Fraction, s: Fraction) -> Fraction:
    return (d - s) / Fraction(2, 1)


def check_gkpw_identities() -> int:
    checks = 0
    d_sym, delta_sym, m_sq_sym, s_sym = sp.symbols("d delta m_sq s")

    # Symbolic involution, sum, shadow invariance, Vieta product, completed square
    shadow_sym = d_sym - delta_sym
    assert sp.simplify(d_sym - shadow_sym - delta_sym) == 0
    checks += 1
    assert sp.simplify(delta_sym + shadow_sym - d_sym) == 0
    checks += 1
    mass_sym = delta_sym * (delta_sym - d_sym)
    mass_shadow_sym = shadow_sym * (shadow_sym - d_sym)
    assert sp.simplify(mass_shadow_sym - mass_sym) == 0
    checks += 1
    assert sp.simplify(delta_sym * shadow_sym + mass_sym) == 0
    checks += 1
    disc_sym = d_sym**2 + 4 * mass_sym
    assert sp.simplify((2 * delta_sym - d_sym) ** 2 - disc_sym) == 0
    checks += 1

    # Symbolic BF excess (Delta - d/2)^2
    bf_sym = -(d_sym**2) / sp.Rational(4, 1)
    assert sp.simplify((mass_sym - bf_sym) - (delta_sym - d_sym / 2) ** 2) == 0
    checks += 1

    # Symbolic square-discriminant root recovery
    rp = (d_sym + s_sym) / 2
    rm = (d_sym - s_sym) / 2
    assert sp.simplify(rp * (rp - d_sym) - (s_sym**2 - d_sym**2) / 4) == 0
    assert sp.simplify(rm * (rm - d_sym) - (s_sym**2 - d_sym**2) / 4) == 0
    assert sp.simplify((rp + rm) - d_sym) == 0
    assert sp.simplify((rp - rm) - s_sym) == 0
    checks += 4

    # Rational grid verification
    for d_val in [Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5)]:
        assert gkpw_discriminant(d_val, bf_bound(d_val)) == 0
        assert gkpw_root_plus(d_val, Fraction(0)) == d_val / 2
        assert gkpw_root_minus(d_val, Fraction(0)) == d_val / 2
        assert gkpw_mass_sq(d_val, d_val / 2) == bf_bound(d_val)
        checks += 4
        for num in range(-8, 17):
            delta_val = Fraction(num, 2)
            assert shadow_dimension(d_val, shadow_dimension(d_val, delta_val)) == delta_val
            assert delta_val + shadow_dimension(d_val, delta_val) == d_val
            assert gkpw_mass_sq(d_val, shadow_dimension(d_val, delta_val)) == gkpw_mass_sq(d_val, delta_val)
            assert delta_val * shadow_dimension(d_val, delta_val) == -gkpw_mass_sq(d_val, delta_val)
            assert (2 * delta_val - d_val) ** 2 == gkpw_discriminant(d_val, gkpw_mass_sq(d_val, delta_val))
            assert gkpw_mass_sq(d_val, delta_val) >= bf_bound(d_val)
            checks += 6

    # Recorded AdS_5 (d = 4) and AdS_3 (d = 2) points
    d4 = Fraction(4)
    assert gkpw_discriminant(d4, Fraction(0)) == 16
    assert gkpw_root_plus(d4, Fraction(4)) == 4
    assert gkpw_root_minus(d4, Fraction(4)) == 0
    assert gkpw_mass_sq(d4, Fraction(4)) == 0
    assert gkpw_mass_sq(d4, Fraction(0)) == 0
    assert bf_bound(d4) == -4
    assert gkpw_discriminant(d4, Fraction(-4)) == 0
    assert gkpw_mass_sq(d4, Fraction(2)) == -4
    assert gkpw_discriminant(d4, Fraction(-3)) == 4
    assert gkpw_root_plus(d4, Fraction(2)) == 3
    assert gkpw_root_minus(d4, Fraction(2)) == 1
    assert gkpw_mass_sq(d4, Fraction(3)) == -3
    assert gkpw_mass_sq(d4, Fraction(1)) == -3
    assert gkpw_discriminant(d4, Fraction(5)) == 36
    assert gkpw_root_plus(d4, Fraction(6)) == 5
    assert gkpw_root_minus(d4, Fraction(6)) == -1
    assert gkpw_mass_sq(d4, Fraction(5)) == 5
    assert gkpw_mass_sq(d4, Fraction(-1)) == 5

    d2 = Fraction(2)
    assert bf_bound(d2) == -1
    assert gkpw_discriminant(d2, Fraction(-1)) == 0
    assert gkpw_mass_sq(d2, Fraction(1)) == -1

    disc_d4_m1 = gkpw_discriminant(d4, Fraction(1))
    assert disc_d4_m1 == 20
    assert Fraction(4) ** 2 < disc_d4_m1 < Fraction(5) ** 2
    checks += 23

    return checks


def check_thooft_scaling() -> int:
    checks = 0
    gym_sq, n_sym = sp.symbols("gYM_sq N")
    lam_sym = gym_sq * n_sym

    for v_cnt, e_cnt, f_cnt in [(2, 3, 3), (2, 3, 1), (4, 6, 4), (4, 6, 2), (1, 2, 2)]:
        weight = gym_sq ** (e_cnt - v_cnt) * (n_sym**f_cnt)
        lhs = weight * (n_sym ** (e_cnt - v_cnt))
        rhs = (lam_sym ** (e_cnt - v_cnt)) * (n_sym**f_cnt)
        assert sp.simplify(lhs - rhs) == 0
        checks += 1

    # Planar (g=0: V=2, E=3, F=3) vs torus (g=1: V=2, E=3, F=1)
    chi_planar = 2 - 3 + 3
    chi_torus = 2 - 3 + 1
    assert chi_planar == 2 - 2 * 0
    assert chi_torus == 2 - 2 * 1
    checks += 2

    gym_val = Fraction(1, 3)
    n_val = Fraction(3)
    lam_val = gym_val * n_val
    assert lam_val == 1
    w_planar = (gym_val ** (3 - 2)) * (n_val**3)
    w_torus = (gym_val ** (3 - 2)) * (n_val**1)
    assert w_planar == 9
    assert w_torus == 1
    assert w_torus * (n_val**2) == w_planar
    assert Fraction(3) ** 2 - 1 == 8
    assert Fraction(4) ** 2 - 1 == 15
    checks += 6

    return checks


def check_isometric_dictionary_and_fence() -> int:
    checks = 0
    # Symbolic 1-to-2 isometry V = [[1], [0]] and general 2-to-3 isometry
    v12 = sp.Matrix([[1], [0]])
    assert v12.T * v12 == sp.eye(1)
    proj12 = v12 * v12.T
    assert proj12 == sp.Matrix([[1, 0], [0, 0]])
    assert proj12 != sp.eye(2)
    checks += 3

    o_perp = sp.Matrix([[0, 0], [0, 1]])
    assert o_perp != sp.zeros(2, 2)
    pullback_perp = v12.T * o_perp * v12
    assert pullback_perp == sp.zeros(1, 1)
    checks += 2

    # For any 1x1 bulk matrix [[a]], pushforward is [[a, 0], [0, 0]], whose (1,1) entry is 0 != 1
    a_sym, b_sym, psi1, psi2 = sp.symbols("a b psi1 psi2")
    o_bulk_1 = sp.Matrix([[a_sym]])
    pushed_1 = v12 * o_bulk_1 * v12.T
    assert pushed_1 == sp.Matrix([[a_sym, 0], [0, 0]])
    assert pushed_1[1, 1] == 0 and o_perp[1, 1] == 1
    assert v12.T * pushed_1 * v12 == o_bulk_1
    checks += 3

    # Exact rational 2-to-3 isometric embedding with Pythagorean rational columns
    # Column 0: (3/5, 4/5, 0)^T, Column 1: (0, 0, 1)^T
    v23 = sp.Matrix([
        [sp.Rational(3, 5), 0],
        [sp.Rational(4, 5), 0],
        [0, 1],
    ])
    assert v23.T * v23 == sp.eye(2)
    assert v23 * v23.T != sp.eye(3)
    checks += 2

    mat_a = sp.Matrix([[sp.Rational(2, 1), sp.Rational(-1, 3)], [sp.Rational(5, 2), sp.Rational(7, 4)]])
    mat_c = sp.Matrix([[sp.Rational(-3, 2), sp.Rational(4, 5)], [sp.Rational(1, 2), sp.Rational(-2, 3)]])
    push_a = v23 * mat_a * v23.T
    push_c = v23 * mat_c * v23.T
    assert v23.T * push_a * v23 == mat_a
    assert push_a * push_c == v23 * (mat_a * mat_c) * v23.T
    checks += 2

    psi_vec = sp.Matrix([[psi1], [psi2]])
    encoded_psi = v23 * psi_vec
    exp_bdry = (encoded_psi.T * push_a * encoded_psi)[0, 0]
    exp_bulk = (psi_vec.T * mat_a * psi_vec)[0, 0]
    assert sp.simplify(exp_bdry - exp_bulk) == 0
    checks += 1

    return checks


def main() -> int:
    c1 = check_gkpw_identities()
    c2 = check_thooft_scaling()
    c3 = check_isometric_dictionary_and_fence()
    total = c1 + c2 + c3
    print(
        "ads-cft-duality-import independent check: "
        f"checks={total} gkpw={c1} thooft={c2} isometry_fence={c3} failures=0"
    )
    print(
        "recorded gkpw points: d=4 mSq=0 -> D=16, Delta+=(4,0); "
        "d=4 mSq=-4 (BF) -> D=0, Delta=2; d=4 mSq=-3 -> D=4, Delta=(3,1); "
        "d=4 mSq=5 -> D=36, Delta=(5,-1); d=2 mSq=-1 (BF) -> D=0, Delta=1; "
        "d=4 mSq=1 -> D=20 (4^2 < 20 < 5^2)"
    )
    print(
        "recorded thooft points: gYM^2=1/3, N=3 -> lambda=1, "
        "planar(2,3,3)=9, torus(2,3,1)=1, ratio=9=N^2; "
        "dim SU(3)=8, dim SU(4)=15"
    )
    print(
        "recorded isometric dictionary fence: V=[[1],[0]], V^T V=[[1]], "
        "V V^T=[[1,0],[0,0]] != I_2, O_perp=[[0,0],[0,1]] != 0 has pullback 0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
