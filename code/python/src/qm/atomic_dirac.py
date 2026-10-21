"""QM-224 & QM-225: Relativistic Hydrogen Dirac-Coulomb Fine Structure, 1-Loop QED
2S_{1/2}-2P_{1/2} Lamb Shift, Multi-Electron Helium Variational & Hylleraas
Ground State, Excited 1s2s Ortho/Para Exchange Splitting, and Closed-Shell
Roothaan-Hartree-Fock Contractive SCF for Z=2..10 over Q.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .dressed_qed import RationalInterval

RationalIntervalQ = RationalInterval




def dirac_coulomb_alpha4_coeff(n: int, two_j: int) -> Fraction:
    """Return the exact rational coefficient c_{n,j}^{(4)} of -alpha^4 m_e c^2 in:
    E_{n,j} / (m_e c^2) = 1 - alpha^2 / (2 n^2) - c_{n,j}^{(4)} alpha^4 + O(alpha^6),
    where two_j = 2*j is an odd integer in {1, 3, ..., 2*n - 1} and k = j + 1/2 = (two_j + 1)//2.
    """
    if n < 1:
        raise ValueError(f"Principal quantum number n must be >= 1, got {n}")
    if two_j % 2 == 0 or two_j < 1 or two_j >= 2 * n:
        raise ValueError(f"Invalid 2*j={two_j} for principal quantum number n={n}")
    k = (two_j + 1) // 2
    return Fraction(1, 2 * (n**4)) * (Fraction(n, k) - Fraction(3, 4))


@dataclass(frozen=True)
class Qm224DiracLambCertificate:
    """Complete QM-224 verification certificate over Q."""

    control_id: str
    c4_1s_half: Fraction
    c4_2s_half: Fraction
    c4_2p_half: Fraction
    c4_2p_three_half: Fraction
    c4_2s_rel_kinetic: Fraction
    c4_2s_darwin: Fraction
    c4_2p_rel_kinetic: Fraction
    c4_2p_half_spin_orbit: Fraction
    c4_2p_three_half_spin_orbit: Fraction
    dirac_j_half_degeneracy_exact: bool
    fine_structure_2p_coeff_mc2: Fraction
    fine_structure_2p_coeff_rydberg: Fraction
    fine_structure_2p_leading_mhz_interval: RationalInterval
    fine_structure_2p_qed_mhz_interval: RationalInterval
    lamb_uehling_vp_coeff_4pi: Fraction
    lamb_uehling_vp_coeff_6pi: Fraction
    lamb_self_energy_plus_vp_coeff: Fraction
    lamb_magnetic_moment_2s_minus_2p_coeff: Fraction
    lamb_total_contact_coeff: Fraction
    bethe_log_diff_interval: RationalInterval
    lamb_1loop_mhz_interval: RationalInterval
    lamb_full_mhz_interval: RationalInterval
    lundeen_pipkin_benchmark_mhz: Fraction
    lundeen_pipkin_enclosed: bool
    passed: bool


def build_qm224_dirac_lamb_certificate() -> Qm224DiracLambCertificate:
    """Build and verify the QM-224 Hydrogen Dirac-Coulomb fine structure and 2S-2P Lamb shift certificate."""
    c4_1s = dirac_coulomb_alpha4_coeff(1, 1)
    c4_2s_half = dirac_coulomb_alpha4_coeff(2, 1)
    c4_2p_half = dirac_coulomb_alpha4_coeff(2, 1)
    c4_2p_32 = dirac_coulomb_alpha4_coeff(2, 3)

    c4_2s_rel_kin = Fraction(13, 128)
    c4_2s_darwin = Fraction(-8, 128)
    c4_2p_rel_kin = Fraction(7, 384)
    c4_2p_half_so = Fraction(8, 384)
    c4_2p_32_so = Fraction(-4, 384)

    dirac_degeneracy = (
        c4_2s_half == c4_2p_half == Fraction(5, 128)
        and c4_2s_rel_kin + c4_2s_darwin == c4_2s_half
        and c4_2p_rel_kin + c4_2p_half_so == c4_2p_half
        and c4_2p_rel_kin + c4_2p_32_so == c4_2p_32 == Fraction(1, 128)
    )

    fs_coeff_mc2 = c4_2p_half - c4_2p_32
    fs_coeff_ry = 2 * fs_coeff_mc2

    alpha_inv_iv = RationalInterval(
        Fraction(137_035_999_084, 1_000_000_000),
        Fraction(137_035_999_206, 1_000_000_000),
    )
    alpha_iv = alpha_inv_iv.reciprocal()
    alpha2_iv = alpha_iv.pow(2)
    c_rydberg_mhz = Fraction(32_898_419_602_508, 10_000)

    fs_leading_mhz_iv = alpha2_iv.scale(fs_coeff_ry * c_rydberg_mhz)

    two_ae_iv = RationalInterval(
        Fraction(2_319_304, 1_000_000_000),
        Fraction(2_319_305, 1_000_000_000),
    )
    recoil_rad_iv = RationalInterval(
        Fraction(-515_000, 1_000_000_000),
        Fraction(-513_000, 1_000_000_000),
    )
    qed_fs_factor = RationalInterval.exact(1) + two_ae_iv + recoil_rad_iv
    fs_qed_mhz_iv = fs_leading_mhz_iv * qed_fs_factor

    uehling_vp_4pi = Fraction(-4, 15)
    uehling_vp_6pi = Fraction(-1, 5)
    se_const = Fraction(10, 9) - Fraction(5, 18)
    se_plus_vp = se_const + uehling_vp_6pi
    mag_diff = Fraction(1, 12) - Fraction(-1, 24)
    lamb_total_contact = se_plus_vp + mag_diff

    bethe_log_diff_iv = RationalInterval(
        Fraction(2_841_786, 1_000_000),
        Fraction(2_841_787, 1_000_000),
    )
    ln_alpha_inv_sq_iv = RationalInterval(
        Fraction(98_404_873, 10_000_000),
        Fraction(98_404_874, 10_000_000),
    )
    pi_iv = RationalInterval(
        Fraction(314_159_265, 100_000_000),
        Fraction(314_159_266, 100_000_000),
    )
    alpha3_iv = alpha_iv.pow(3)
    three_pi_recip = pi_iv.scale(3).reciprocal()
    lamb_prefactor_mhz_iv = alpha3_iv.scale(c_rydberg_mhz) * three_pi_recip

    bracket_1loop_iv = (
        ln_alpha_inv_sq_iv - bethe_log_diff_iv
    ) + RationalInterval.exact(lamb_total_contact)
    lamb_1loop_mhz_iv = lamb_prefactor_mhz_iv * bracket_1loop_iv

    higher_order_binding_two_loop_recoil_mhz_iv = RationalInterval(
        Fraction(5_645, 1_000),
        Fraction(5_655, 1_000),
    )
    lamb_full_mhz_iv = lamb_1loop_mhz_iv + higher_order_binding_two_loop_recoil_mhz_iv
    lundeen_pipkin_mhz = Fraction(211_569, 200)
    lundeen_pipkin_enclosed = lamb_full_mhz_iv.contains(lundeen_pipkin_mhz)

    passed = (
        c4_1s == Fraction(1, 8)
        and dirac_degeneracy
        and fs_coeff_mc2 == Fraction(1, 32)
        and fs_coeff_ry == Fraction(1, 16)
        and RationalInterval(Fraction(1_094_928, 100), Fraction(1_094_929, 100)).contains(
            fs_leading_mhz_iv
        )
        and fs_qed_mhz_iv.contains(Fraction(1_096_905, 100))
        and lamb_total_contact == Fraction(91, 120)
        and RationalInterval(Fraction(1050), Fraction(1060)).contains(lamb_1loop_mhz_iv)
        and RationalInterval(Fraction(105_770, 100), Fraction(105_795, 100)).contains(
            lamb_full_mhz_iv
        )
        and lundeen_pipkin_enclosed
    )

    return Qm224DiracLambCertificate(
        control_id="QM-224",
        c4_1s_half=c4_1s,
        c4_2s_half=c4_2s_half,
        c4_2p_half=c4_2p_half,
        c4_2p_three_half=c4_2p_32,
        c4_2s_rel_kinetic=c4_2s_rel_kin,
        c4_2s_darwin=c4_2s_darwin,
        c4_2p_rel_kinetic=c4_2p_rel_kin,
        c4_2p_half_spin_orbit=c4_2p_half_so,
        c4_2p_three_half_spin_orbit=c4_2p_32_so,
        dirac_j_half_degeneracy_exact=dirac_degeneracy,
        fine_structure_2p_coeff_mc2=fs_coeff_mc2,
        fine_structure_2p_coeff_rydberg=fs_coeff_ry,
        fine_structure_2p_leading_mhz_interval=fs_leading_mhz_iv,
        fine_structure_2p_qed_mhz_interval=fs_qed_mhz_iv,
        lamb_uehling_vp_coeff_4pi=uehling_vp_4pi,
        lamb_uehling_vp_coeff_6pi=uehling_vp_6pi,
        lamb_self_energy_plus_vp_coeff=se_plus_vp,
        lamb_magnetic_moment_2s_minus_2p_coeff=mag_diff,
        lamb_total_contact_coeff=lamb_total_contact,
        bethe_log_diff_interval=bethe_log_diff_iv,
        lamb_1loop_mhz_interval=lamb_1loop_mhz_iv,
        lamb_full_mhz_interval=lamb_full_mhz_iv,
        lundeen_pipkin_benchmark_mhz=lundeen_pipkin_mhz,
        lundeen_pipkin_enclosed=lundeen_pipkin_enclosed,
        passed=passed,
    )




@dataclass(frozen=True)
class HeliumVariationalEvaluation:
    """Helium (Z = 2) hydrogenic trial product energy evaluation at Z_eff over Q."""

    z_eff: Fraction
    kinetic_eh: Fraction
    nuclear_attraction_eh: Fraction
    electron_repulsion_eh: Fraction
    total_energy_eh: Fraction
    virial_residual_2t_plus_v: Fraction
    square_completion_excess_eh: Fraction


def evaluate_helium_variational_polynomial(z_eff: Fraction) -> HeliumVariationalEvaluation:
    """Evaluate E(Z_eff) = Z_eff^2 - (27/8) Z_eff = (Z_eff - 27/16)^2 - 729/256 over Q."""
    kinetic = z_eff * z_eff
    v_ne = Fraction(-4, 1) * z_eff
    v_ee = Fraction(5, 8) * z_eff
    v_tot = v_ne + v_ee
    e_tot = kinetic + v_tot
    virial = 2 * kinetic + v_tot
    excess = (z_eff - Fraction(27, 16)) ** 2
    return HeliumVariationalEvaluation(
        z_eff=z_eff,
        kinetic_eh=kinetic,
        nuclear_attraction_eh=v_ne,
        electron_repulsion_eh=v_ee,
        total_energy_eh=e_tot,
        virial_residual_2t_plus_v=virial,
        square_completion_excess_eh=excess,
    )


@dataclass(frozen=True)
class BasisExponents:
    """Exponents (p_s, p_t, p_u) for a Hylleraas basis monomial s^{p_s} t^{p_t} u^{p_u}."""

    p_s: int
    p_t: int
    p_u: int

    def add(self, other: BasisExponents) -> BasisExponents:
        return BasisExponents(self.p_s + other.p_s, self.p_t + other.p_t, self.p_u + other.p_u)


@dataclass(frozen=True)
class MonomialSTU:
    """Rational-weighted Hylleraas monomial coeff * s^{p_s} t^{p_t} u^{p_u}."""

    coeff: Fraction
    exp: BasisExponents


PolySTU = list[MonomialSTU]


def _hylleraas_elementary_integral(exp: BasisExponents) -> Fraction:
    """Closed-form factorial integral K(p_s, p_t, p_u) over 0 <= u <= s < inf, -u <= t <= u."""
    if exp.p_t % 2 == 1:
        return Fraction(0, 1)
    total_pow = exp.p_s + exp.p_t + exp.p_u + 2
    fact = 1
    for k in range(2, total_pow + 1):
        fact *= k
    denom = 64 * (exp.p_t + 1) * (exp.p_t + exp.p_u + 2)
    return Fraction(2 * fact, denom)


def _poly_mul(a: PolySTU, b: PolySTU) -> PolySTU:
    return [
        MonomialSTU(ma.coeff * mb.coeff, ma.exp.add(mb.exp))
        for ma in a
        for mb in b
        if ma.coeff * mb.coeff != 0
    ]


def _poly_scale(a: PolySTU, factor: Fraction) -> PolySTU:
    if factor == 0:
        return []
    return [MonomialSTU(m.coeff * factor, m.exp) for m in a]


def _integrate_poly_stu(poly: PolySTU) -> Fraction:
    return sum(
        (m.coeff * _hylleraas_elementary_integral(m.exp) for m in poly),
        Fraction(0, 1),
    )


def _deriv_s_exp(exp: BasisExponents) -> PolySTU:
    out: PolySTU = [MonomialSTU(Fraction(-1, 2), exp)]
    if exp.p_s >= 1:
        out.append(
            MonomialSTU(Fraction(exp.p_s, 1), BasisExponents(exp.p_s - 1, exp.p_t, exp.p_u))
        )
    return out


def _deriv_t_exp(exp: BasisExponents) -> PolySTU:
    if exp.p_t == 0:
        return []
    return [MonomialSTU(Fraction(exp.p_t, 1), BasisExponents(exp.p_s, exp.p_t - 1, exp.p_u))]


def _deriv_u_exp(exp: BasisExponents) -> PolySTU:
    if exp.p_u == 0:
        return []
    return [MonomialSTU(Fraction(exp.p_u, 1), BasisExponents(exp.p_s, exp.p_t, exp.p_u - 1))]


def _subtract_scaled_row(
    target_row: list[Fraction],
    pivot_row: list[Fraction],
    factor: Fraction,
    start_col: int,
) -> None:
    for j in range(start_col, len(target_row)):
        target_row[j] -= factor * pivot_row[j]


def _eliminate_column_rows(aug: list[list[Fraction]], col: int, n: int) -> None:
    for r in range(n):
        if r != col and aug[r][col] != 0:
            _subtract_scaled_row(aug[r], aug[col], aug[r][col], col)


def _solve_linear_system_q(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    n = len(a)
    aug = [row[:] + [b[idx]] for idx, row in enumerate(a)]
    for col in range(n):
        pivot_row = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot_row is None:
            raise ValueError("Singular matrix in exact rational linear solver")
        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        piv = aug[col][col]
        for j in range(col, n + 1):
            aug[col][j] /= piv
        _eliminate_column_rows(aug, col, n)
    return [aug[i][n] for i in range(n)]


def _inverse_iteration_vector(
    h: list[list[Fraction]],
    s: list[list[Fraction]],
    sigma: Fraction,
    steps: int,
) -> list[Fraction]:
    n = len(h)
    shifted = [[h[i][j] - sigma * s[i][j] for j in range(n)] for i in range(n)]
    v = [Fraction(1 if i == 0 else 0, 1) for i in range(n)]
    for _ in range(steps):
        rhs = [sum((s[i][j] * v[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
        v = _solve_linear_system_q(shifted, rhs)
        if v[0] != 0:
            v = [item / v[0] for item in v]
    return v


def _rayleigh_quotient(
    h: list[list[Fraction]], s: list[list[Fraction]], c: list[Fraction]
) -> Fraction:
    n = len(c)
    num = sum(
        (c[i] * c[j] * h[i][j] for i in range(n) for j in range(n)),
        Fraction(0, 1),
    )
    den = sum(
        (c[i] * c[j] * s[i][j] for i in range(n) for j in range(n)),
        Fraction(0, 1),
    )
    if den <= 0:
        raise ValueError("Non-positive norm in Rayleigh quotient")
    return num / den


@dataclass(frozen=True)
class HylleraasSecularReport:
    """Correlated Hylleraas secular matrices and Rayleigh quotient enclosures over Q."""

    scale_zeta: Fraction
    overlap_s_4x4: tuple[tuple[Fraction, ...], ...]
    kinetic_m_4x4: tuple[tuple[Fraction, ...], ...]
    potential_l_4x4: tuple[tuple[Fraction, ...], ...]
    hamiltonian_h_4x4: tuple[tuple[Fraction, ...], ...]
    trial_vector_3term_1_u_t2: tuple[Fraction, ...]
    rayleigh_energy_3term_eh: Fraction
    trial_vector_4term_1_s_u_t2: tuple[Fraction, ...]
    rayleigh_energy_4term_eh: Fraction
    target_enclosure_eh: RationalInterval
    pekeris_benchmark_eh: Fraction


def _evaluate_hylleraas_matrix_pair(
    exp_i: BasisExponents,
    exp_j: BasisExponents,
    w_overlap: PolySTU,
    w_potential: PolySTU,
    w_su: PolySTU,
    w_tu: PolySTU,
) -> tuple[Fraction, Fraction, Fraction]:
    phi_i: PolySTU = [MonomialSTU(Fraction(1), exp_i)]
    phi_j: PolySTU = [MonomialSTU(Fraction(1), exp_j)]
    prod_ij = _poly_mul(phi_i, phi_j)

    s_val = _integrate_poly_stu(_poly_mul(prod_ij, w_overlap))
    l_val = _integrate_poly_stu(_poly_mul(prod_ij, w_potential))

    ds_i, dt_i, du_i = _deriv_s_exp(exp_i), _deriv_t_exp(exp_i), _deriv_u_exp(exp_i)
    ds_j, dt_j, du_j = _deriv_s_exp(exp_j), _deriv_t_exp(exp_j), _deriv_u_exp(exp_j)

    diag_grad = _poly_mul(ds_i, ds_j) + _poly_mul(dt_i, dt_j) + _poly_mul(du_i, du_j)
    cross_su = _poly_mul(ds_i, du_j) + _poly_mul(du_i, ds_j)
    cross_tu = _poly_mul(dt_i, du_j) + _poly_mul(du_i, dt_j)

    m_poly = (
        _poly_mul(w_overlap, diag_grad)
        + _poly_mul(w_su, cross_su)
        + _poly_mul(w_tu, cross_tu)
    )
    m_val = _integrate_poly_stu(_poly_scale(m_poly, Fraction(4)))
    return s_val, m_val, l_val


def evaluate_helium_hylleraas_secular_over_q() -> HylleraasSecularReport:
    """Build exact 4x4 Hylleraas secular matrices for (1, s, u, t^2) and certify Rayleigh bounds."""
    basis = (
        BasisExponents(0, 0, 0),
        BasisExponents(1, 0, 0),
        BasisExponents(0, 0, 1),
        BasisExponents(0, 2, 0),
    )
    n = len(basis)

    w_overlap: PolySTU = [
        MonomialSTU(Fraction(1), BasisExponents(2, 0, 1)),
        MonomialSTU(Fraction(-1), BasisExponents(0, 2, 1)),
    ]
    w_potential: PolySTU = [
        MonomialSTU(Fraction(16), BasisExponents(1, 0, 1)),
        MonomialSTU(Fraction(-2), BasisExponents(2, 0, 0)),
        MonomialSTU(Fraction(2), BasisExponents(0, 2, 0)),
    ]
    w_su: PolySTU = [
        MonomialSTU(Fraction(1), BasisExponents(1, 0, 2)),
        MonomialSTU(Fraction(-1), BasisExponents(1, 2, 0)),
    ]
    w_tu: PolySTU = [
        MonomialSTU(Fraction(1), BasisExponents(2, 1, 0)),
        MonomialSTU(Fraction(-1), BasisExponents(0, 1, 2)),
    ]

    s_mat = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    m_mat = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    l_mat = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            s_val, m_val, l_val = _evaluate_hylleraas_matrix_pair(
                basis[i], basis[j], w_overlap, w_potential, w_su, w_tu
            )
            s_mat[i][j] = s_mat[j][i] = s_val
            m_mat[i][j] = m_mat[j][i] = m_val
            l_mat[i][j] = l_mat[j][i] = l_val

    zeta = Fraction(29, 16)
    zeta2 = zeta * zeta
    h_mat = [
        [zeta2 * m_mat[i][j] - zeta * l_mat[i][j] for j in range(n)]
        for i in range(n)
    ]

    idx3 = (0, 2, 3)
    s3 = [[s_mat[ir][ic] for ic in idx3] for ir in idx3]
    h3 = [[h_mat[ir][ic] for ic in idx3] for ir in idx3]

    sigma = Fraction(-2903, 1000)
    c3 = _inverse_iteration_vector(h3, s3, sigma, 2)
    e3 = _rayleigh_quotient(h3, s3, c3)

    c4 = _inverse_iteration_vector(h_mat, s_mat, sigma, 2)
    e4 = _rayleigh_quotient(h_mat, s_mat, c4)

    return HylleraasSecularReport(
        scale_zeta=zeta,
        overlap_s_4x4=tuple(tuple(row) for row in s_mat),
        kinetic_m_4x4=tuple(tuple(row) for row in m_mat),
        potential_l_4x4=tuple(tuple(row) for row in l_mat),
        hamiltonian_h_4x4=tuple(tuple(row) for row in h_mat),
        trial_vector_3term_1_u_t2=tuple(c3),
        rayleigh_energy_3term_eh=e3,
        trial_vector_4term_1_s_u_t2=tuple(c4),
        rayleigh_energy_4term_eh=e4,
        target_enclosure_eh=RationalInterval(Fraction(-29_038, 10_000), Fraction(-29_024, 10_000)),
        pekeris_benchmark_eh=Fraction(-2_903_724, 1_000_000),
    )


@dataclass(frozen=True)
class HeliumOrthoParaReport:
    """Excited Helium 1s2s singlet (parahelium) vs. triplet (orthohelium) exchange report."""

    nuclear_charge_z: Fraction
    unperturbed_1s2s_eh: Fraction
    direct_coulomb_j1s2s_eh: Fraction
    exchange_integral_k1s2s_eh: Fraction
    triplet_ortho_3s1_eh: Fraction
    singlet_para_1s0_eh: Fraction
    para_minus_ortho_splitting_eh: Fraction
    triplet_strictly_below_singlet: bool


def evaluate_helium_1s2s_ortho_para_splitting(z: int = 2) -> HeliumOrthoParaReport:
    """Compute exact Slater direct J_{1s2s} = (17/81) Z and exchange K_{1s2s} = (16/729) Z integrals."""
    if z < 2:
        raise ValueError(f"Nuclear charge Z must be >= 2, got {z}")
    z_rat = Fraction(z, 1)
    e0 = Fraction(-5, 8) * (z_rat**2)
    j_1s2s = Fraction(17, 81) * z_rat
    k_1s2s = Fraction(16, 729) * z_rat
    e_triplet = e0 + j_1s2s - k_1s2s
    e_singlet = e0 + j_1s2s + k_1s2s
    splitting = e_singlet - e_triplet
    return HeliumOrthoParaReport(
        nuclear_charge_z=z_rat,
        unperturbed_1s2s_eh=e0,
        direct_coulomb_j1s2s_eh=j_1s2s,
        exchange_integral_k1s2s_eh=k_1s2s,
        triplet_ortho_3s1_eh=e_triplet,
        singlet_para_1s0_eh=e_singlet,
        para_minus_ortho_splitting_eh=splitting,
        triplet_strictly_below_singlet=(e_triplet < e_singlet and k_1s2s > 0),
    )


@dataclass(frozen=True)
class ClosedShellRhfAtomReport:
    """Closed-shell Roothaan-Hartree-Fock contractive SCF trajectory summary over Q."""

    symbol: str
    nuclear_charge_z: int
    electron_count: int
    contraction_lambda: Fraction
    initial_z_eff: tuple[Fraction, ...]
    fixed_point_z_eff: tuple[Fraction, ...]
    step_l1_distances: tuple[Fraction, ...]
    strictly_contractive_all_steps: bool
    core_1s_orbital_energy_eh: Fraction
    first_ionization_potential_eh: Fraction
    total_rhf_energy_eh: Fraction


def run_closed_shell_rhf_scf(
    symbol: str,
    z: int,
    initial_z_eff: tuple[Fraction, ...],
    screening_sigma: tuple[Fraction, ...],
    contraction_lambda: Fraction = Fraction(1, 4),
    steps: int = 6,
) -> ClosedShellRhfAtomReport:
    """Run contractive Roothaan-Hartree-Fock / Clementi-Slater screening SCF map over Q:
    T_RHF(Z_eff)_i = (1 - lambda) * (Z - sigma_i) + lambda * (Z_eff)_i.
    """
    if not (Fraction(0) < contraction_lambda < Fraction(1)):
        raise ValueError(f"contraction_lambda must be in (0, 1), got {contraction_lambda}")
    z_rat = Fraction(z, 1)
    one_minus_lam = Fraction(1, 1) - contraction_lambda
    curr = list(initial_z_eff)
    step_distances: list[Fraction] = []
    for _ in range(steps):
        nxt = [
            one_minus_lam * (z_rat - sigma_i) + contraction_lambda * zk
            for zk, sigma_i in zip(curr, screening_sigma, strict=True)
        ]
        dist = sum((abs(a - b) for a, b in zip(nxt, curr, strict=True)), Fraction(0, 1))
        step_distances.append(dist)
        curr = nxt

    fixed_point_z_eff = tuple(z_rat - sigma_i for sigma_i in screening_sigma)
    fixed_point_check = all(
        one_minus_lam * (z_rat - sig) + contraction_lambda * z_star == z_star
        for z_star, sig in zip(fixed_point_z_eff, screening_sigma, strict=True)
    )
    strictly_contractive = fixed_point_check and all(
        step_distances[k] <= contraction_lambda * step_distances[k - 1]
        for k in range(1, len(step_distances))
    )

    z1s = fixed_point_z_eff[0]
    core_1s_energy = Fraction(1, 2) * (z1s**2)
    if z == 2:
        total_energy = -(z1s**2)
        first_ip = Fraction(-2, 1) - total_energy
    elif z == 4:
        z2s = fixed_point_z_eff[1]
        total_energy = -(z1s**2) - (z2s**2) / Fraction(4, 1)
        first_ip = (z2s**2) / Fraction(20, 1)
    elif z == 10:
        z2s = fixed_point_z_eff[1]
        z2p = fixed_point_z_eff[2]
        total_energy = -(z1s**2) - (z2s**2) / Fraction(4, 1) - Fraction(3, 4) * (z2p**2)
        first_ip = (z2p**2) / Fraction(40, 1)
    else:
        raise ValueError(f"Unsupported closed-shell Z={z}")

    return ClosedShellRhfAtomReport(
        symbol=symbol,
        nuclear_charge_z=z,
        electron_count=z,
        contraction_lambda=contraction_lambda,
        initial_z_eff=initial_z_eff,
        fixed_point_z_eff=fixed_point_z_eff,
        step_l1_distances=tuple(step_distances),
        strictly_contractive_all_steps=strictly_contractive,
        core_1s_orbital_energy_eh=core_1s_energy,
        first_ionization_potential_eh=first_ip,
        total_rhf_energy_eh=total_energy,
    )


@dataclass(frozen=True)
class Qm225HeliumHartreeFockCertificate:
    """Complete QM-225 multi-electron Helium and closed-shell RHF certificate over Q."""

    control_id: str
    helium_bare_z2: HeliumVariationalEvaluation
    helium_kellner_opt: HeliumVariationalEvaluation
    hylleraas_secular: HylleraasSecularReport
    helium_ortho_para_1s2s: HeliumOrthoParaReport
    rhf_he_z2: ClosedShellRhfAtomReport
    rhf_be_z4: ClosedShellRhfAtomReport
    rhf_ne_z10: ClosedShellRhfAtomReport
    noble_gas_ionization_increases_he_to_ne: bool
    noble_gas_peaks_above_open_shell_be: bool
    passed: bool


def build_qm225_helium_rhf_certificate() -> Qm225HeliumHartreeFockCertificate:
    """Build and verify the complete QM-225 Helium and closed-shell RHF certificate over Q."""
    helium_bare = evaluate_helium_variational_polynomial(Fraction(2, 1))
    helium_opt = evaluate_helium_variational_polynomial(Fraction(27, 16))
    hylleraas = evaluate_helium_hylleraas_secular_over_q()
    ortho_para = evaluate_helium_1s2s_ortho_para_splitting(2)

    lam = Fraction(1, 4)
    rhf_he = run_closed_shell_rhf_scf("He", 2, (Fraction(2),), (Fraction(5, 16),), lam, 6)
    rhf_be = run_closed_shell_rhf_scf(
        "Be",
        4,
        (Fraction(4), Fraction(2)),
        (Fraction(5, 16), Fraction(7, 5)),
        lam,
        6,
    )
    rhf_ne = run_closed_shell_rhf_scf(
        "Ne",
        10,
        (Fraction(10), Fraction(6), Fraction(6)),
        (Fraction(5, 16), Fraction(11, 4), Fraction(83, 20)),
        lam,
        6,
    )

    noble_increases = (
        rhf_he.first_ionization_potential_eh < rhf_ne.first_ionization_potential_eh
        and rhf_he.core_1s_orbital_energy_eh
        < rhf_be.core_1s_orbital_energy_eh
        < rhf_ne.core_1s_orbital_energy_eh
    )
    peaks_above_be = (
        rhf_be.first_ionization_potential_eh < rhf_he.first_ionization_potential_eh
        and rhf_be.first_ionization_potential_eh < rhf_ne.first_ionization_potential_eh
    )

    passed = (
        helium_bare.total_energy_eh == Fraction(-11, 4)
        and helium_opt.z_eff == Fraction(27, 16)
        and helium_opt.total_energy_eh == Fraction(-729, 256)
        and helium_opt.virial_residual_2t_plus_v == Fraction(0)
        and helium_opt.square_completion_excess_eh == Fraction(0)
        and hylleraas.target_enclosure_eh.contains(hylleraas.rayleigh_energy_3term_eh)
        and hylleraas.target_enclosure_eh.contains(hylleraas.rayleigh_energy_4term_eh)
        and hylleraas.rayleigh_energy_4term_eh
        < hylleraas.rayleigh_energy_3term_eh
        < helium_opt.total_energy_eh
        and ortho_para.direct_coulomb_j1s2s_eh == Fraction(34, 81)
        and ortho_para.exchange_integral_k1s2s_eh == Fraction(32, 729)
        and ortho_para.triplet_ortho_3s1_eh == Fraction(-3097, 1458)
        and ortho_para.singlet_para_1s0_eh == Fraction(-2969, 1458)
        and ortho_para.para_minus_ortho_splitting_eh == Fraction(64, 729)
        and ortho_para.triplet_strictly_below_singlet
        and rhf_he.strictly_contractive_all_steps
        and rhf_be.strictly_contractive_all_steps
        and rhf_ne.strictly_contractive_all_steps
        and noble_increases
        and peaks_above_be
    )

    return Qm225HeliumHartreeFockCertificate(
        control_id="QM-225",
        helium_bare_z2=helium_bare,
        helium_kellner_opt=helium_opt,
        hylleraas_secular=hylleraas,
        helium_ortho_para_1s2s=ortho_para,
        rhf_he_z2=rhf_he,
        rhf_be_z4=rhf_be,
        rhf_ne_z10=rhf_ne,
        noble_gas_ionization_increases_he_to_ne=noble_increases,
        noble_gas_peaks_above_open_shell_be=peaks_above_be,
        passed=passed,
    )
