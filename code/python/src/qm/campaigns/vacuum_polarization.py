# AuthorityEffect: None.
"""QM-216: 1-Loop QED Vacuum Polarization, Running Coupling, and Uehling / Lamb Shift Control.

Implements the two-layer finite-to-continuum decomposition for 1-loop QED photon
vacuum polarization, running charge renormalization (via Z_1 = Z_2 from QM-215),
and the Uehling / Hydrogen 2S_{1/2}-2P_{1/2} Lamb shift:
  (a) Exact transverse Ward projector P_T^{mu nu}(q) = eta^{mu nu} - q^mu q^nu / q^2
      over Q (checking q_mu P_T^{mu nu} = 0, idempotence P_T^2 = P_T, and trace = 3),
      exact 4x4 Clifford Dirac trace on the 1-loop bubble numerator in M_4(Q(i)),
      and Symanzik bubble reduction with BPHZ on-shell subtraction Pi_R(q^2) = Pi(q^2) - Pi(0)
      cancelling the UV cutoff Lambda^2 identically over Q.
  (b) Exact rational Beta-moments M_n = int_0^1 x^{n+1}(1-x)^{n+1} dx = ((n+1)!)^2 / (2n+3)!
      (M_1 = 1/30 -> Uehling slope 2 M_1 = 1/15, M_2 = 1/140, M_3 = 1/630), closed-form
      space-like vacuum polarization Pi_R(-9 m^2 / 4) at rational conformal velocity
      v = 5/3 ((v+1)/(v-1) = 4 -> ln 4 = 2 ln 2), and 12-decimal RationalInterval enclosure
      of the running inverse fine-structure constant alpha_eff^{-1}(-9 m^2 / 4).
  (c) Exact rational Lamb-shift contact decomposition 5/6 (2S self-energy constant,
      including the S-state anomalous-moment term 3/8) + 1/8 (removal of the 2P_{1/2}
      anomalous-moment term -1/8) - 1/5 (Uehling vacuum polarization) = 91/120 in Q
      (the same total as QM-224; the self-energy plus vacuum-polarization part is 19/30), plus
      12-decimal RationalInterval enclosure of the Uehling 2S_{1/2}-2P_{1/2} shift
      in dimensionless units (-alpha^5 / (30 pi)) and in MHz (-27.13... MHz).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .ward_takahashi import (
    MINKOWSKI_METRIC,
    Mat4Qi,
    Qi,
    dirac_gamma_matrices,
    feynman_slash,
    mat4_add,
    mat4_identity,
    mat4_mul,
    mat4_scale,
    minkowski_dot,
)
from .dressed_qed import (
    RationalInterval,
    pi_interval,
    polylog_half_interval,
)
from .symanzik_two_forest import (
    bubble_graph,
    symanzik_f_polynomial,
    symanzik_u_polynomial,
)

Mat4Q = list[list[Fraction]]


def mat4_trace_qi(a: Mat4Qi) -> Qi:
    """Return the exact trace tr(A) in Q(i) of a 4x4 matrix A."""
    acc = Qi.zero()
    for idx in range(4):
        acc = acc + a[idx][idx]
    return acc


def transverse_tensor_t(q: list[Fraction]) -> Mat4Q:
    """Return T^{mu nu}(q) = q^mu q^nu - q^2 eta^{mu nu} over Q."""
    q_sq = minkowski_dot(q, q)
    out: Mat4Q = [[Fraction(0, 1) for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            eta_munu = MINKOWSKI_METRIC[mu] if mu == nu else Fraction(0, 1)
            out[mu][nu] = q[mu] * q[nu] - q_sq * eta_munu
    return out


def transverse_projector(q: list[Fraction]) -> Mat4Q:
    """Return P_T^{mu nu}(q) = eta^{mu nu} - q^mu q^nu / q^2 over Q for q^2 != 0."""
    q_sq = minkowski_dot(q, q)
    if q_sq == 0:
        raise ZeroDivisionError("Transverse projector requires non-null momentum q^2 != 0")
    out: Mat4Q = [[Fraction(0, 1) for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            eta_munu = MINKOWSKI_METRIC[mu] if mu == nu else Fraction(0, 1)
            out[mu][nu] = eta_munu - (q[mu] * q[nu]) / q_sq
    return out


def check_transverse_projector_identities(q: list[Fraction]) -> tuple[bool, bool, Fraction]:
    """Verify (1) Ward transversality q_mu P_T^{mu nu}(q) = 0,
    (2) idempotence P_T^{mu alpha} eta_{alpha beta} P_T^{beta nu} = P_T^{mu nu},
    and (3) Lorentz trace eta_{mu nu} P_T^{mu nu}(q) = 3 in D = 4.
    """
    pt = transverse_projector(q)
    t_mat = transverse_tensor_t(q)

    # 1. Ward transversality: sum_mu q_mu T^{mu nu} = 0 and sum_mu q_mu P_T^{mu nu} = 0
    ward_ok = True
    for nu in range(4):
        dot_t = sum(MINKOWSKI_METRIC[mu] * q[mu] * t_mat[mu][nu] for mu in range(4))
        dot_p = sum(MINKOWSKI_METRIC[mu] * q[mu] * pt[mu][nu] for mu in range(4))
        if dot_t != 0 or dot_p != 0:
            ward_ok = False

    # 2. Idempotence: sum_{a} P_T^{mu a} eta_{a a} P_T^{a nu} == P_T^{mu nu}
    idempotent_ok = True
    for mu in range(4):
        for nu in range(4):
            comp = sum(pt[mu][a] * MINKOWSKI_METRIC[a] * pt[a][nu] for a in range(4))
            if comp != pt[mu][nu]:
                idempotent_ok = False

    # 3. Lorentz trace: sum_mu eta_{mu mu} P_T^{mu mu} == 3
    trace_val = sum(MINKOWSKI_METRIC[mu] * pt[mu][mu] for mu in range(4))
    return (ward_ok, idempotent_ok, trace_val)


def fermion_bubble_numerator_clifford_trace(
    k: list[Fraction], q: list[Fraction], mass: Fraction
) -> Mat4Q:
    """Compute the exact 4x4 Lorentz tensor N^{mu nu}(k, q, m) = tr[gamma^mu (k_slash + q_slash + m I_4)
    gamma^nu (k_slash + m I_4)] by explicit matrix multiplication in M_4(Q(i)).
    """
    gammas = dirac_gamma_matrices()
    id4 = mat4_identity()
    kq = [k[idx] + q[idx] for idx in range(4)]
    factor_left = mat4_add(feynman_slash(kq), mat4_scale(Qi.from_q(mass), id4))
    factor_right = mat4_add(feynman_slash(k), mat4_scale(Qi.from_q(mass), id4))

    out: Mat4Q = [[Fraction(0, 1) for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            prod = mat4_mul(
                gammas[mu],
                mat4_mul(factor_left, mat4_mul(gammas[nu], factor_right)),
            )
            tr_val = mat4_trace_qi(prod)
            if tr_val.im != 0:
                raise ValueError(f"Non-zero imaginary part in 4-gamma trace at ({mu}, {nu})")
            out[mu][nu] = tr_val.re
    return out


def fermion_bubble_numerator_analytic(
    k: list[Fraction], q: list[Fraction], mass: Fraction
) -> Mat4Q:
    """Analytical textbook formula 4 [k^mu (k+q)^nu + (k+q)^mu k^nu - eta^{mu nu} (k.(k+q) - m^2)]."""
    kq = [k[idx] + q[idx] for idx in range(4)]
    k_dot_kq = minkowski_dot(k, kq)
    out: Mat4Q = [[Fraction(0, 1) for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            eta_munu = MINKOWSKI_METRIC[mu] if mu == nu else Fraction(0, 1)
            out[mu][nu] = Fraction(4, 1) * (
                k[mu] * kq[nu] + kq[mu] * k[nu] - eta_munu * (k_dot_kq - mass * mass)
            )
    return out


def feynman_parameter_moment_polynomial(n: int) -> Fraction:
    """Compute M_n = int_0^1 x^{n+1} (1 - x)^{n+1} dx over Q by exact binomial expansion:
    int_0^1 sum_{j=0}^{n+1} (-1)^j binom(n+1, j) x^{n+1+j} dx = sum_{j=0}^{n+1} (-1)^j binom(n+1, j) / (n + 2 + j).
    """
    if n < 0:
        raise ValueError("Moment index n must be non-negative")
    m = n + 1
    binom = 1
    total = Fraction(0, 1)
    for j in range(m + 1):
        sign = Fraction(1, 1) if j % 2 == 0 else Fraction(-1, 1)
        total += sign * Fraction(binom, m + 1 + j)
        if j < m:
            binom = (binom * (m - j)) // (j + 1)
    return total


def feynman_parameter_moment_beta_closed(n: int) -> Fraction:
    """Closed-form Beta integral B(n+2, n+2) = ((n+1)!)^2 / (2n + 3)! over Q."""
    fact_n1 = 1
    for k in range(2, n + 2):
        fact_n1 *= k
    fact_2n3 = 1
    for k in range(2, 2 * n + 4):
        fact_2n3 *= k
    return Fraction(fact_n1 * fact_n1, fact_2n3)


def vacuum_polarization_spacelike_closed_interval(
    v: Fraction,
    alpha_inv: Fraction,
    ln_v_ratio_iv: RationalInterval,
    pi_iv: RationalInterval,
) -> RationalInterval:
    """Evaluate the 1-loop renormalized vacuum polarization Pi_R(-Q^2) at space-like
    momentum Q^2 = 4 m^2 / (v^2 - 1) (with v > 1):
      Pi_R(-Q^2) = -(alpha / (3 pi)) * [v^2 - 8/3 + (v (3 - v^2) / 2) ln((v + 1)/(v - 1))].
    """
    if v <= 1:
        raise ValueError("Space-like conformal velocity v must satisfy v > 1")
    alpha_over_3pi = RationalInterval.exact(Fraction(1, 1) / (Fraction(3, 1) * alpha_inv)) * (
        pi_iv.reciprocal()
    )
    poly_part = RationalInterval.exact(v * v - Fraction(8, 3))
    log_coeff = v * (Fraction(3, 1) - v * v) / Fraction(2, 1)
    bracket = poly_part + ln_v_ratio_iv.scale(log_coeff)
    return RationalInterval.exact(Fraction(0, 1)) - (alpha_over_3pi * bracket)


@dataclass(frozen=True)
class VacuumPolarizationLambShiftReport:
    """Typed receipt for QM-216 1-loop vacuum polarization, running alpha, and Lamb shift control."""

    # Part (a): Ward transverse projector, Clifford bubble trace, and Symanzik / BPHZ subtraction
    transverse_ward_identity_exact: bool
    transverse_projector_idempotent_exact: bool
    transverse_projector_trace_equals_three: Fraction
    clifford_bubble_trace_matches_analytic: bool
    symanzik_bubble_simplex_u_equals_one: bool
    symanzik_bubble_simplex_f_matches_feynman_denom: bool
    bphz_uv_cutoff_cancels_at_all_scales: bool
    bphz_on_shell_pi_r_at_zero_is_zero: bool
    # Part (b): Exact rational Beta moments and 12-decimal running coupling enclosure
    moments_match_beta_closed_form: bool
    uehling_leading_slope_coeff: Fraction
    second_moment_series_coeff: Fraction
    third_moment_series_coeff: Fraction
    spacelike_velocity_v: Fraction
    spacelike_q2_over_m2: Fraction
    pi_r_spacelike_interval: RationalInterval
    pi_r_spacelike_decimal_12: str
    pi_r_spacelike_12_digits_agree: bool
    alpha_eff_inv_spacelike_interval: RationalInterval
    alpha_eff_inv_spacelike_decimal_12: str
    alpha_eff_inv_spacelike_12_digits_agree: bool
    alpha_eff_exceeds_bare_alpha: bool
    # Part (c): Uehling potential & Hydrogen 2S_{1/2}-2P_{1/2} Lamb shift enclosure
    lamb_contact_se_term: Fraction
    lamb_contact_g2_magnetic_term: Fraction
    lamb_contact_uehling_vp_term: Fraction
    lamb_contact_total_rational: Fraction
    uehling_2s_dimensionless_coeff: Fraction
    uehling_2s_dimensionless_interval: RationalInterval
    uehling_2s_mhz_interval: RationalInterval
    uehling_2s_mhz_decimal_12: str
    uehling_2s_mhz_12_digits_agree: bool


def evaluate_vacuum_polarization_lamb_shift_control(
    alpha_inv: Fraction = Fraction(137035999166, 10**9),
    me_c2_over_h_mhz: Fraction = Fraction(123558996383000, 1),
) -> VacuumPolarizationLambShiftReport:
    """Run all three parts of the QM-216 control over Q, Q(i), and RationalInterval."""
    # -------------------------------------------------------------------------
    # Part (a): Transverse Ward projector, Clifford bubble trace & BPHZ on-shell subtraction
    # -------------------------------------------------------------------------
    q_vec = [Fraction(2, 1), Fraction(3, 1), Fraction(1, 1), Fraction(1, 1)]
    ward_ok, idemp_ok, tr_pt = check_transverse_projector_identities(q_vec)

    k_vec = [Fraction(5, 1), Fraction(-1, 1), Fraction(2, 1), Fraction(3, 1)]
    mass = Fraction(2, 1)
    num_clifford = fermion_bubble_numerator_clifford_trace(k_vec, q_vec, mass)
    num_analytic = fermion_bubble_numerator_analytic(k_vec, q_vec, mass)
    clifford_trace_ok = num_clifford == num_analytic

    # Symanzik 1-loop bubble graph G_bub: 2 vertices, 2 parallel edges (0, 1), (0, 1)
    bub = bubble_graph()
    x_param = Fraction(3, 7)
    alphas_simplex = [x_param, Fraction(1, 1) - x_param]
    u_bub_simplex = symanzik_u_polynomial(bub, alphas_simplex)
    u_simplex_ok = u_bub_simplex == Fraction(1, 1)

    # In Euclidean signature with external momentum q_E (q_E^2 = -q^2),
    # F_{G_bub}(x, 1-x; q_E, m^2) = x(1-x) q_E^2 + (x + 1 - x)^2 m^2 = m^2 - x(1-x) q^2
    q_eucl = [[Fraction(3, 1), Fraction(0, 1)], [Fraction(-3, 1), Fraction(0, 1)]]
    q_mink_sq = Fraction(-9, 1)  # since -q^2 = q_E^2 = 9
    m2_bub = [mass * mass, mass * mass]
    f_bub_simplex = symanzik_f_polynomial(bub, alphas_simplex, q_eucl, m2_bub)
    expected_feynman_denom = mass * mass - x_param * (Fraction(1, 1) - x_param) * q_mink_sq
    f_simplex_ok = f_bub_simplex == expected_feynman_denom

    # Bare arguments Lambda^2/Delta move with the cutoff. Their ratio equals
    # m^2/Delta at every cutoff. On shell that ratio is 1, the bare argument
    # is not 1, and the same subtraction at m^2 + 1 is not 1.
    m2 = mass * mass
    delta = expected_feynman_denom
    uv_cutoffs = [Fraction(10, 1), Fraction(1000, 1), Fraction(10**9, 1)]
    bare_at_delta = [lam_sq / delta for lam_sq in uv_cutoffs]
    bare_at_m2 = [lam_sq / m2 for lam_sq in uv_cutoffs]
    subtracted = [(lam_sq / delta) / (lam_sq / m2) for lam_sq in uv_cutoffs]
    subtracted_target = m2 / delta
    bare_depends_on_cutoff = (
        bare_at_delta[0] != bare_at_delta[1]
        and bare_at_delta[1] != bare_at_delta[2]
        and bare_at_m2[0] != bare_at_m2[1]
        and bare_at_m2[1] != bare_at_m2[2]
    )
    subtracted_agrees = all(ratio == subtracted_target for ratio in subtracted) and (
        subtracted[0] == subtracted[1] == subtracted[2]
    )
    bphz_uv_cancels = bare_depends_on_cutoff and subtracted_agrees
    denom_at_zero = m2 - x_param * (Fraction(1, 1) - x_param) * Fraction(0, 1)
    on_shell_is_one = all(
        ((lam_sq / denom_at_zero) / (lam_sq / m2)) == Fraction(1, 1) for lam_sq in uv_cutoffs
    )
    bare_on_shell_not_one = all(ratio != Fraction(1, 1) for ratio in bare_at_m2)
    wrong_subtraction = m2 + Fraction(1, 1)
    wrong_point_not_one = all(
        ((lam_sq / m2) / (lam_sq / wrong_subtraction)) != Fraction(1, 1) for lam_sq in uv_cutoffs
    )
    bphz_zero_at_zero = (
        denom_at_zero == m2 and on_shell_is_one and bare_on_shell_not_one and wrong_point_not_one
    )

    # -------------------------------------------------------------------------
    # Part (b): Exact rational Beta moments & 12-decimal running coupling enclosure
    # -------------------------------------------------------------------------
    moments_poly = [feynman_parameter_moment_polynomial(n) for n in range(1, 5)]
    moments_beta = [feynman_parameter_moment_beta_closed(n) for n in range(1, 5)]
    moments_match = moments_poly == moments_beta

    # Series coefficients of Pi_R(q^2) / (alpha / pi) = sum_{n>=1} (2 M_n / n) (q^2 / m^2)^n
    c_uehling_1 = Fraction(2, 1) * moments_poly[0] / Fraction(1, 1)  # 2 * (1/30) = 1/15
    c_uehling_2 = Fraction(2, 1) * moments_poly[1] / Fraction(2, 1)  # 1/140
    c_uehling_3 = Fraction(2, 1) * moments_poly[2] / Fraction(3, 1)  # 1/945

    # Space-like evaluation at conformal velocity v = 5/3:
    # Q^2 / m^2 = 4 / (v^2 - 1) = 4 / (16/9) = 9/4 (so q^2 / m^2 = -9/4),
    # and (v + 1)/(v - 1) = (8/3)/(2/3) = 4 -> ln((v+1)/(v-1)) = 2 ln 2
    v_space = Fraction(5, 3)
    q2_over_m2_space = Fraction(-9, 4)
    pi_iv = pi_interval(20)
    ln2_iv = polylog_half_interval(1, 50)
    ln4_iv = ln2_iv.scale(Fraction(2, 1))

    pi_r_iv = vacuum_polarization_spacelike_closed_interval(v_space, alpha_inv, ln4_iv, pi_iv)
    pi_r_lo12, _pi_r_hi12, pi_r_agree12 = pi_r_iv.decimal_prefix(12)

    # Since Z_1 = Z_2 (QM-215), alpha_eff(q^2) = alpha / (1 + Pi_R(q^2)), so
    # alpha_eff^{-1}(q^2) = alpha^{-1} * (1 + Pi_R(q^2))
    one_plus_pi_r = RationalInterval.exact(Fraction(1, 1)) + pi_r_iv
    alpha_eff_inv_iv = one_plus_pi_r.scale(alpha_inv)
    aeff_lo12, _aeff_hi12, aeff_agree12 = alpha_eff_inv_iv.decimal_prefix(12)
    alpha_eff_exceeds_bare = alpha_eff_inv_iv.hi < alpha_inv

    # -------------------------------------------------------------------------
    # Part (c): Uehling potential & Hydrogen 2S_{1/2}-2P_{1/2} Lamb shift enclosure
    # -------------------------------------------------------------------------
    # 2S self-energy constant 11/24 + 3/8 = 5/6 (the 3/8 is the S-state anomalous-moment
    # part). 19/30 = 5/6 - 1/5 already contains the Uehling term, so it must not be
    # combined with lamb_vp again.
    lamb_se = Fraction(5, 6)
    lamb_g2 = Fraction(1, 8)
    lamb_vp = Fraction(-1, 5)
    lamb_total_contact = lamb_se + lamb_g2 + lamb_vp  # 91/120, as in QM-224

    # Dimensionless Uehling 2S_{1/2}-2P_{1/2} shift:
    # Delta E_Uehling / (m_e c^2) = -(4/15) * alpha^5 / (8 pi) = -alpha^5 / (30 pi)
    uehling_dimless_coeff = Fraction(-4, 15) * Fraction(1, 8)  # -1/30
    alpha_exact = RationalInterval.exact(Fraction(1, 1) / alpha_inv)
    alpha5_over_pi = alpha_exact.pow(5) * pi_iv.reciprocal()
    uehling_dimless_iv = alpha5_over_pi.scale(uehling_dimless_coeff)
    uehling_mhz_iv = uehling_dimless_iv.scale(me_c2_over_h_mhz)
    ueh_mhz_lo12, _ueh_mhz_hi12, ueh_mhz_agree12 = uehling_mhz_iv.decimal_prefix(12)

    return VacuumPolarizationLambShiftReport(
        transverse_ward_identity_exact=ward_ok,
        transverse_projector_idempotent_exact=idemp_ok,
        transverse_projector_trace_equals_three=tr_pt,
        clifford_bubble_trace_matches_analytic=clifford_trace_ok,
        symanzik_bubble_simplex_u_equals_one=u_simplex_ok,
        symanzik_bubble_simplex_f_matches_feynman_denom=f_simplex_ok,
        bphz_uv_cutoff_cancels_at_all_scales=bphz_uv_cancels,
        bphz_on_shell_pi_r_at_zero_is_zero=bphz_zero_at_zero,
        moments_match_beta_closed_form=moments_match,
        uehling_leading_slope_coeff=c_uehling_1,
        second_moment_series_coeff=c_uehling_2,
        third_moment_series_coeff=c_uehling_3,
        spacelike_velocity_v=v_space,
        spacelike_q2_over_m2=q2_over_m2_space,
        pi_r_spacelike_interval=pi_r_iv,
        pi_r_spacelike_decimal_12=pi_r_lo12,
        pi_r_spacelike_12_digits_agree=pi_r_agree12,
        alpha_eff_inv_spacelike_interval=alpha_eff_inv_iv,
        alpha_eff_inv_spacelike_decimal_12=aeff_lo12,
        alpha_eff_inv_spacelike_12_digits_agree=aeff_agree12,
        alpha_eff_exceeds_bare_alpha=alpha_eff_exceeds_bare,
        lamb_contact_se_term=lamb_se,
        lamb_contact_g2_magnetic_term=lamb_g2,
        lamb_contact_uehling_vp_term=lamb_vp,
        lamb_contact_total_rational=lamb_total_contact,
        uehling_2s_dimensionless_coeff=uehling_dimless_coeff,
        uehling_2s_dimensionless_interval=uehling_dimless_iv,
        uehling_2s_mhz_interval=uehling_mhz_iv,
        uehling_2s_mhz_decimal_12=ueh_mhz_lo12,
        uehling_2s_mhz_12_digits_agree=ueh_mhz_agree12,
    )
