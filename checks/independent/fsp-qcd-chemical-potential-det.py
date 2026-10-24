#!/usr/bin/env python3
"""Independent check for FSP-QCD-CHEMICAL-POTENTIAL-DET (TFQ-1201).

Verifies with zero repository imports (using fractions.Fraction and SymPy):
1. Exact gamma_5 / staggered-parity chemical-potential intertwining:
       Gamma_5 D(mu) Gamma_5 = D(-conj(mu))^dagger
   and the induced determinant conjugation identity
       conj(det D(mu)) = det D(-conj(mu))
   across real, purely imaginary, and general complex chemical potentials mu
   (or fugacities z = exp(mu)).
2. Exact confirmation of the 6x6 chiral SU(3) clock-link witness from
   lean4/CampaignFspQcdChemicalPotentialDet.lean:
       U = diag(i, i, -1) in SU(3),
       D_SU3(z) = diag(I_3 - z U, I_3 - z^{-1} U^dagger),
       det D_SU3(2)   = 63/8 - 27 i,
       det D_SU3(1/2) = 63/8 + 27 i = conj(det D_SU3(2)),
   together with symbolic polynomial-in-(z, z^{-1}) identity across generic z.
3. Exact Kogut-Susskind staggered Dirac operator D(mu) on 1D (L=4, 12x12) and
   2D (2x2, 12x12) bipartite periodic lattices coupled to SU(3) gauge links
   (including non-diagonal SU(3) links with Gell-Mann generators):
   - Gamma_5 D(mu) Gamma_5 = D(-conj(mu))^dagger holds identically;
   - At mu = 0 and purely imaginary mu = i * mu_I, Im(det D(mu)) = 0;
   - At generic real mu != 0, SU(3) backgrounds carrying complex Polyakov loop
     traces produce Im(det D(mu)) != 0 and det D(mu) != det D(-mu);
   - Contrast with SU(2) fundamental gauge links in the same lattice geometry,
     where pseudoreality keeps Im(det D(mu)) = 0 for all real mu.
"""

from __future__ import annotations

from fractions import Fraction
import sys
import sympy as sp


def check_su3_clock_witness() -> tuple[int, int]:
    """Verify the 6x6 chiral SU(3) clock-link witness symbolically and at rational z."""
    checks = 0
    complex_det_witnesses = 0

    i = sp.I
    u_clock = sp.diag(i, i, -1)
    ident3 = sp.eye(3)

    # Check U in SU(3) and Im(Tr(U)) = 2 != 0
    assert u_clock * u_clock.H == ident3, "su3ClockLink must be unitary"
    assert sp.simplify(u_clock.det() - 1) == 0, "su3ClockLink must have determinant 1"
    assert sp.im(u_clock.trace()) == 2, "su3ClockLink must have Im(Tr(U)) = 2"
    checks += 3

    z = sp.Symbol("z", complex=True, nonzero=True)
    gamma5 = sp.BlockMatrix([[sp.zeros(3, 3), ident3], [ident3, sp.zeros(3, 3)]]).as_explicit()
    assert gamma5 * gamma5 == sp.eye(6)
    assert gamma5.H == gamma5
    checks += 2

    def d_su3(fugacity: sp.Expr) -> sp.Matrix:
        top = ident3 - fugacity * u_clock
        bot = ident3 - (1 / fugacity) * u_clock.H
        return sp.BlockMatrix([[top, sp.zeros(3, 3)], [sp.zeros(3, 3), bot]]).as_explicit()

    # Symbolic intertwining: Gamma5 * D(z) * Gamma5 == D(1/conj(z))^H
    lhs = gamma5 * d_su3(z) * gamma5
    rhs = d_su3(1 / sp.conjugate(z)).H
    assert sp.simplify(lhs - rhs) == sp.zeros(6, 6), "Symbolic chiral SU(3) intertwining failed"
    checks += 1

    # Exact rational fugacity evaluations matching the Lean theorem
    det_2 = sp.simplify(d_su3(sp.Rational(2, 1)).det())
    det_half = sp.simplify(d_su3(sp.Rational(1, 2)).det())
    expected_2 = sp.Rational(63, 8) - 27 * i
    expected_half = sp.Rational(63, 8) + 27 * i
    assert det_2 == expected_2, f"Expected 63/8 - 27*I, got {det_2}"
    assert det_half == expected_half, f"Expected 63/8 + 27*I, got {det_half}"
    assert sp.conjugate(det_2) == det_half
    assert sp.im(det_2) == -27 and sp.im(det_2) != 0
    assert det_2 != det_half
    checks += 5
    complex_det_witnesses += 1

    # Rational fugacity sweep using exact Fraction arithmetic
    for p, q in [(3, 2), (2, 1), (5, 3), (3, 1), (4, 3), (7, 4)]:
        r = Fraction(p, q)
        # det(I - r * diag(i, i, -1)) = (1 - r*i)^2 * (1 + r)
        #   = ((1 - r^2) - 2*r*i) * (1 + r) = (1 + r)*(1 - r^2) - 2*r*(1 + r)*i
        # det(I - r^{-1} * diag(-i, -i, -1)) = (1 + r^{-1}*i)^2 * (1 + r^{-1})
        #   = ((1 - r^{-2}) + 2*r^{-1}*i) * (1 + r^{-1})
        re_top = (1 + r) * (1 - r * r)
        im_top = -2 * r * (1 + r)
        rinv = Fraction(1, 1) / r
        re_bot = (1 + rinv) * (1 - rinv * rinv)
        im_bot = 2 * rinv * (1 + rinv)

        det_re = re_top * re_bot - im_top * im_bot
        det_im = re_top * im_bot + im_top * re_bot

        sym_det = sp.simplify(d_su3(sp.Rational(p, q)).det())
        sym_det_inv = sp.simplify(d_su3(sp.Rational(q, p)).det())
        assert sym_det == sp.Rational(det_re.numerator, det_re.denominator) + i * sp.Rational(
            det_im.numerator, det_im.denominator
        )
        assert sp.conjugate(sym_det) == sym_det_inv
        assert det_im != 0, f"Expected nonzero Im(det) at r={r}"
        checks += 3
        complex_det_witnesses += 1

    # Unit-circle fugacity z = (3 + 4i)/5 (purely imaginary chemical potential mu = i * mu_I)
    for a, b, c in [(3, 4, 5), (5, 12, 13), (8, 15, 17)]:
        z_unit = sp.Rational(a, c) + i * sp.Rational(b, c)
        assert sp.simplify(z_unit * sp.conjugate(z_unit) - 1) == 0
        det_unit = sp.simplify(d_su3(z_unit).det())
        assert sp.im(det_unit) == 0, f"Unit-circle fugacity must give real determinant, got {det_unit}"
        checks += 2

    return checks, complex_det_witnesses


def build_su3_links() -> list[sp.Matrix]:
    """Construct exact unitary unimodular SU(3) matrices (diagonal and non-diagonal)."""
    i = sp.I
    # Link 0: clock matrix diag(i, i, -1)
    u0 = sp.diag(i, i, -1)
    # Link 1: non-diagonal SU(3) rotation on colors (0,1) times phase diag(i, -1, i)
    c = sp.Rational(3, 5)
    s = sp.Rational(4, 5)
    rot01 = sp.Matrix([[c, i * s, 0], [i * s, c, 0], [0, 0, 1]])
    u1 = rot01 * sp.diag(i, -1, i)
    # Link 2: non-diagonal SU(3) rotation on colors (1,2)
    rot12 = sp.Matrix([[1, 0, 0], [0, sp.Rational(5, 13), sp.Rational(12, 13)], [0, -sp.Rational(12, 13), sp.Rational(5, 13)]])
    u2 = rot12 * sp.diag(i, i, -1)
    # Link 3: unitary SU(3) phase-and-rotation link
    u3 = rot01 * sp.diag(1, 1, 1)

    links = [u0, u1, u2, u3]
    for idx, u in enumerate(links):
        assert sp.simplify(u * u.H - sp.eye(3)) == sp.zeros(3, 3), f"SU(3) link {idx} not unitary"
        assert sp.simplify(u.det() - 1) == 0, f"SU(3) link {idx} does not have det 1"
    return links


def check_1d_staggered_qcd_ring() -> tuple[int, int]:
    """Verify 1D L=4 staggered SU(3) Dirac operator with Hasenfratz-Karsch chemical potential."""
    checks = 0
    complex_det_witnesses = 0
    i = sp.I
    links = build_su3_links()
    checks += len(links) * 2

    n_sites = 4
    dim = 3 * n_sites  # 12x12 matrix

    # Staggered parity epsilon(x) = (-1)^x I_3
    gamma5_blocks = [((-1) ** x) * sp.eye(3) for x in range(n_sites)]
    gamma5 = sp.diag(*gamma5_blocks)
    assert gamma5 * gamma5 == sp.eye(dim)
    assert gamma5.H == gamma5
    checks += 2

    def staggered_1d(mass: sp.Expr, fugacity: sp.Expr, link_list: list[sp.Matrix]) -> sp.Matrix:
        mat = mass * sp.eye(dim)
        # Forward temporal hopping K_pos and backward temporal hopping K_neg = -K_pos^H
        # With antiperiodic/periodic staggered sign on L=4 ring:
        for x in range(n_sites):
            y = (x + 1) % n_sites
            r_slice = slice(3 * x, 3 * (x + 1))
            c_slice = slice(3 * y, 3 * (y + 1))
            mat[r_slice, c_slice] += sp.Rational(1, 2) * fugacity * link_list[x]
            mat[c_slice, r_slice] -= sp.Rational(1, 2) * (1 / fugacity) * link_list[x].H
        return mat

    # Check forward/backward hopping anticommutation with staggered parity
    m_sym = sp.Rational(1, 2)
    z_sym = sp.Symbol("z", complex=True, nonzero=True)
    d_z = staggered_1d(m_sym, z_sym, links)
    d_z_dual = staggered_1d(m_sym, 1 / sp.conjugate(z_sym), links).H
    assert sp.simplify(gamma5 * d_z * gamma5 - d_z_dual) == sp.zeros(dim, dim)
    checks += 1

    # Verify Polyakov loop P = U_0 U_1 U_2 U_3 has Im(Tr(P)) != 0
    polyakov = links[0] * links[1] * links[2] * links[3]
    assert sp.simplify(polyakov * polyakov.H - sp.eye(3)) == sp.zeros(3, 3)
    assert sp.simplify(polyakov.det() - 1) == 0
    assert sp.im(polyakov.trace()) != 0, f"Expected complex Polyakov trace, got {polyakov.trace()}"
    checks += 3

    # At z = 1 (mu = 0), determinant is real
    det_mu0 = sp.simplify(staggered_1d(m_sym, sp.Integer(1), links).det())
    assert sp.im(det_mu0) == 0, f"Expected real det at mu=0, got {det_mu0}"
    checks += 1

    # At unit-circle fugacity z = (3 + 4i)/5 (imaginary mu), determinant is real
    z_imag = sp.Rational(3, 5) + i * sp.Rational(4, 5)
    det_imag = sp.simplify(staggered_1d(m_sym, z_imag, links).det())
    assert sp.im(det_imag) == 0, f"Expected real det at imaginary mu, got {det_imag}"
    checks += 1

    # At real chemical potential fugacities z = 2, 3/2, 3 (and their inverses 1/2, 2/3, 1/3):
    for p, q in [(2, 1), (3, 2), (3, 1)]:
        z_pos = sp.Rational(p, q)
        z_neg = sp.Rational(q, p)
        det_pos = sp.simplify(staggered_1d(m_sym, z_pos, links).det())
        det_neg = sp.simplify(staggered_1d(m_sym, z_neg, links).det())
        assert sp.conjugate(det_pos) == det_neg, "Conjugation law conj(det D(mu)) = det D(-mu) failed"
        assert sp.im(det_pos) != 0, f"Expected nonzero Im(det D(mu)) at z={z_pos}, got {det_pos}"
        assert det_pos != det_neg
        checks += 3
        complex_det_witnesses += 1

    # General complex fugacity z = 2 + i -> 1/conj(z) = 1/(2 - i) = (2 + i)/5
    z_cplx = 2 + i
    z_cplx_dual = 1 / sp.conjugate(z_cplx)
    det_cplx = sp.simplify(staggered_1d(m_sym, z_cplx, links).det())
    det_cplx_dual = sp.simplify(staggered_1d(m_sym, z_cplx_dual, links).det())
    assert sp.conjugate(det_cplx) == det_cplx_dual
    checks += 1

    return checks, complex_det_witnesses


def check_2d_staggered_vs_su2_contrast() -> tuple[int, int]:
    """Compare 2x2 2D staggered lattice for SU(3) (complex det) vs SU(2) (real det)."""
    checks = 0
    complex_det_witnesses = 0
    i = sp.I
    su3_links = build_su3_links()

    # 2x2 lattice: sites (t, x) in {0, 1} x {0, 1}, indexed 0..3
    # Temporal links along t (chemical potential fugacity z on forward, 1/z on backward)
    # Spatial links along x (no chemical potential, staggered phase (-1)^t)
    # On a 2-site periodic direction, forward and backward links are distinct gauge links U_fwd, U_bwd!
    n_sites = 4
    dim_su3 = 12
    gamma5_su3 = sp.diag(*[((-1) ** ((idx // 2) + (idx % 2))) * sp.eye(3) for idx in range(n_sites)])

    def staggered_2x2(
        nc: int,
        mass: sp.Expr,
        fugacity: sp.Expr,
        t_links_fwd: dict[tuple[int, int], sp.Matrix],
        t_links_bwd: dict[tuple[int, int], sp.Matrix],
        x_links: dict[tuple[int, int], sp.Matrix],
    ) -> sp.Matrix:
        mat = mass * sp.eye(nc * n_sites)
        for t in range(2):
            for x in range(2):
                s = 2 * t + x
                s_t = 2 * ((t + 1) % 2) + x
                s_x = 2 * t + ((x + 1) % 2)
                rs = slice(nc * s, nc * (s + 1))
                rt = slice(nc * s_t, nc * (s_t + 1))
                rx = slice(nc * s_x, nc * (s_x + 1))

                # Temporal hop: forward on bond0 (t -> t+1) with fugacity z,
                # plus distinct second bond (t+1 -> t) so the 2-site temporal loop wraps with U_a * U_b
                if t == 0:
                    u_a = t_links_fwd[(0, x)]
                    u_b = t_links_bwd[(1, x)]
                    # Hop 0 -> 1 via bond a (forward) and bond b (backward from 1 -> 0)
                    mat[rs, rt] += sp.Rational(1, 2) * (fugacity * u_a - (1 / fugacity) * u_b.H)
                    mat[rt, rs] += sp.Rational(1, 2) * (fugacity * u_b - (1 / fugacity) * u_a.H)

                # Spatial hop with staggered phase eta_1(t, x) = (-1)^t
                if x == 0:
                    eta1 = (-1) ** t
                    u_spatial = x_links[(t, 0)]
                    mat[rs, rx] += sp.Rational(1, 2) * eta1 * u_spatial
                    mat[rx, rs] -= sp.Rational(1, 2) * eta1 * u_spatial.H
        return mat

    t_fwd_su3 = {(0, 0): su3_links[0], (0, 1): su3_links[1]}
    t_bwd_su3 = {(1, 0): su3_links[0], (1, 1): su3_links[2]}
    x_su3 = {(0, 0): su3_links[3], (1, 0): sp.eye(3)}

    m_val = sp.Rational(1, 1)
    for p, q in [(2, 1), (3, 2)]:
        z_pos = sp.Rational(p, q)
        z_neg = sp.Rational(q, p)
        d_pos = staggered_2x2(3, m_val, z_pos, t_fwd_su3, t_bwd_su3, x_su3)
        d_neg = staggered_2x2(3, m_val, z_neg, t_fwd_su3, t_bwd_su3, x_su3)
        assert gamma5_su3 * d_pos * gamma5_su3 == d_neg.H
        det_pos = sp.simplify(d_pos.det())
        det_neg = sp.simplify(d_neg.det())
        assert sp.conjugate(det_pos) == det_neg
        assert sp.im(det_pos) != 0, f"Expected nonzero Im(det) in 2D SU(3), got {det_pos}"
        checks += 3
        complex_det_witnesses += 1

    # Contrast: replace every link by an SU(2) fundamental matrix U in SU(2)
    def su2_mat(a0: sp.Expr, a1: sp.Expr, a2: sp.Expr, a3: sp.Expr) -> sp.Matrix:
        return sp.Matrix([[a0 + i * a3, a2 + i * a1], [-a2 + i * a1, a0 - i * a3]])

    u_su2_0 = su2_mat(sp.Rational(3, 5), sp.Rational(4, 5), 0, 0)
    u_su2_1 = su2_mat(sp.Rational(5, 13), 0, sp.Rational(12, 13), 0)
    u_su2_2 = su2_mat(0, sp.Rational(8, 17), 0, sp.Rational(15, 17))
    for u in [u_su2_0, u_su2_1, u_su2_2]:
        assert sp.simplify(u * u.H - sp.eye(2)) == sp.zeros(2, 2)
        assert sp.simplify(u.det() - 1) == 0
    checks += 6

    t_fwd_su2 = {(0, 0): u_su2_0, (0, 1): u_su2_1}
    t_bwd_su2 = {(1, 0): u_su2_2, (1, 1): u_su2_0}
    x_su2 = {(0, 0): u_su2_1, (1, 0): u_su2_2}

    for p, q in [(2, 1), (3, 2), (5, 3)]:
        z_pos = sp.Rational(p, q)
        d_su2 = staggered_2x2(2, m_val, z_pos, t_fwd_su2, t_bwd_su2, x_su2)
        det_su2 = sp.simplify(d_su2.det())
        assert sp.im(det_su2) == 0, f"SU(2) fundamental determinant must be real at real mu, got {det_su2}"
        assert det_su2 > 0
        checks += 2

    return checks, complex_det_witnesses


def main() -> int:
    c1, w1 = check_su3_clock_witness()
    c2, w2 = check_1d_staggered_qcd_ring()
    c3, w3 = check_2d_staggered_vs_su2_contrast()
    total_checks = c1 + c2 + c3
    total_witnesses = w1 + w2 + w3
    print(
        f"PASS fsp-qcd-chemical-potential-det: "
        f"checks={total_checks} complex_det_witnesses={total_witnesses} failures=0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
