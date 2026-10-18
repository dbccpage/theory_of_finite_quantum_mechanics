"""E2E: QM-226 / QM-227 / QM-228 QED, weak and hadronic finite-map control.

AuthorityEffect: None.

Each test recomputes the quantity it checks from the stored values or from the
public functions, rather than reading a flag the builder wrote.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.dressed_qed_g2_control import RationalInterval
from finite_qm.use_cases.page_wootters_tsirelson_wigner_control import (
    Qi,
    qi_add,
    qi_dagger,
    qi_eye,
    qi_mat_eq,
    qi_matmul,
    qi_matvec,
    qi_scale,
    qi_zeros,
)
from finite_qm.use_cases.qed_weak_hadronic_control import (
    BaryonMassInputs,
    QedWeakHadronicRefusal,
    abj_colour_factor,
    bhabha_reduced_amplitude,
    build_abj_anomaly_audit,
    build_chiral_projector_audit,
    build_ckm_unitarity_audit,
    build_gell_mann_okubo_audit,
    build_muon_decay_audit,
    build_qed_tree_level_audit,
    evaluate_qed_weak_hadronic_control,
    jarlskog_invariant,
    klein_nishina_ratio,
    ln_interval,
    moller_reduced_amplitude,
    muon_recoil_polynomial,
    qi_inverse,
    sqrt_interval,
    su3_mass_coefficients,
    thomson_angular_integral,
    thomson_limit_ratio,
)


def test_qm226_klein_nishina_values_and_thomson_limit() -> None:
    audit = build_qed_tree_level_audit()
    assert klein_nishina_ratio(Fraction(1), Fraction(0)) == Fraction(3, 16)
    assert klein_nishina_ratio(Fraction(2), Fraction(-1)) == Fraction(13, 125)
    assert klein_nishina_ratio(Fraction(1, 10), Fraction(-1)) == Fraction(305, 432)
    assert len(audit.kn_samples) == 9
    assert all(klein_nishina_ratio(x, u) == r for x, u, r in audit.kn_samples)
    assert audit.kn_forward_values == (Fraction(1),) * 5
    for u in (Fraction(-1), Fraction(1, 2), Fraction(-3, 7)):
        assert klein_nishina_ratio(Fraction(0), u) == thomson_limit_ratio(u) == (1 + u * u) / 2
    assert all(a == b for a, b in audit.thomson_pairs)
    assert audit.thomson_angular_integral == thomson_angular_integral() == 1
    with pytest.raises(QedWeakHadronicRefusal):
        klein_nishina_ratio(Fraction(1), Fraction(2))


def test_qm226_bhabha_moller_crossing_is_s_u_not_s_t() -> None:
    s, t, u = Fraction(5), Fraction(-2), Fraction(-3)
    assert bhabha_reduced_amplitude(s, t, u) == moller_reduced_amplitude(u, t, s)
    assert bhabha_reduced_amplitude(s, t, u) == Fraction(361, 25)
    assert moller_reduced_amplitude(t, s, u) == Fraction(1444, 225)
    audit = build_qed_tree_level_audit()
    assert audit.s_t_swap_values == (Fraction(361, 25), Fraction(1444, 225))
    assert all(a == b for a, b in audit.crossing_s_u_pairs)
    assert all(a == b for a, b in audit.moller_t_u_pairs)
    with pytest.raises(QedWeakHadronicRefusal):
        bhabha_reduced_amplitude(Fraction(1), Fraction(1), Fraction(1))


def test_qm227_weyl_gammas_gamma5_and_projectors() -> None:
    audit = build_chiral_projector_audit()
    metric = (1, -1, -1, -1)
    for mu in range(4):
        for nu in range(4):
            anti = qi_add(qi_matmul(audit.gammas[mu], audit.gammas[nu]), qi_matmul(audit.gammas[nu], audit.gammas[mu]))
            expected = qi_scale(Fraction(2 * metric[mu]), qi_eye(4)) if mu == nu else qi_zeros(4)
            assert qi_mat_eq(anti, expected)
    diag = [Qi.from_int(d) for d in (-1, -1, 1, 1)]
    assert all(audit.gamma5[i][j] == (diag[i] if i == j else Qi.from_int(0)) for i in range(4) for j in range(4))
    pl, pr = audit.p_left, audit.p_right
    assert [pl[k][k] for k in range(4)] == [Qi.from_int(d) for d in (1, 1, 0, 0)]
    assert [pr[k][k] for k in range(4)] == [Qi.from_int(d) for d in (0, 0, 1, 1)]
    assert qi_mat_eq(qi_matmul(pl, pl), pl) and qi_mat_eq(qi_matmul(pl, pr), qi_zeros(4))
    assert qi_mat_eq(qi_add(pl, pr), qi_eye(4))
    right = qi_matvec(pr, audit.spinor)
    assert any(not x.is_zero() for x in right)
    assert all(x.is_zero() for x in qi_matvec(pl, right))
    assert audit.passed


def test_qm227_muon_decay_fermi_constant_enclosure() -> None:
    audit = build_muon_decay_audit()
    x = audit.mass_ratio_sq_x
    assert audit.recoil_polynomial_f0 == muon_recoil_polynomial(x) == 1 - 8 * x + 8 * x**3 - x**4
    assert audit.ln_x_enclosure.hi < 0
    assert audit.one_loop_kinoshita_sirlin_dq_enclosure.hi < 0
    gf = audit.fermi_constant_gev_minus2_enclosure
    assert Fraction(11663, 10**9) <= gf.lo and gf.hi <= Fraction(11665, 10**9)
    assert Fraction(11663, 10**9) <= gf.lo <= gf.hi < Fraction(11664, 10**9)
    assert gf.lo * gf.lo <= audit.fermi_constant_sq_enclosure.lo
    assert audit.fermi_constant_sq_enclosure.hi <= gf.hi * gf.hi


def test_qm227_interval_helpers_bracket_known_values() -> None:
    ln2 = ln_interval(Fraction(2), 30)
    assert Fraction(69314718055, 10**11) < ln2.lo and ln2.hi < Fraction(69314718056, 10**11)
    assert ln_interval(Fraction(1, 4), 30).hi < 0
    root = sqrt_interval(RationalInterval.exact(Fraction(2)), 10)
    assert root.lo * root.lo <= 2 <= root.hi * root.hi
    with pytest.raises(QedWeakHadronicRefusal):
        ln_interval(Fraction(0))
    with pytest.raises(QedWeakHadronicRefusal):
        qi_inverse(Qi.from_int(0))


def test_qm227_ckm_cayley_unitary_triangle_and_jarlskog() -> None:
    audit = build_ckm_unitarity_audit()
    v = audit.ckm
    assert qi_mat_eq(qi_dagger(audit.generator), qi_scale(Fraction(-1), audit.generator))
    assert qi_mat_eq(qi_matmul(qi_dagger(v), v), qi_eye(3))
    assert qi_mat_eq(qi_matmul(v, qi_dagger(v)), qi_eye(3))
    z = audit.triangle
    assert (z[0] + z[1] + z[2]).is_zero()
    j = jarlskog_invariant(v, (0, 1), (0, 1))
    assert j == audit.jarlskog_ud_cs
    assert Fraction(1, 100000) < abs(j) < Fraction(1, 10000)
    assert abs(jarlskog_invariant(v, (1, 2), (0, 2))) == abs(j)
    lam_sq = Fraction(81, 1600)
    assert Fraction(81, 100) * lam_sq <= audit.abs_vus_sq <= Fraction(121, 100) * lam_sq
    a_lam2_sq = (Fraction(4, 5) * lam_sq) ** 2
    assert Fraction(81, 100) * a_lam2_sq <= audit.abs_vcb_sq <= Fraction(121, 100) * a_lam2_sq


def test_qm228_abj_colour_factor_and_pion_rate() -> None:
    assert abj_colour_factor(3) == 1
    assert abj_colour_factor(1) == Fraction(1, 3)
    audit = build_abj_anomaly_audit()
    assert (audit.s_pi0_nc3 / audit.s_pi0_nc1) ** 2 == 9
    r3, r1 = audit.rate_nc3_ev_enclosure, audit.rate_nc1_ev_enclosure
    assert r3.lo <= Fraction(772, 100) <= r3.hi
    assert r3.lo <= Fraction(785, 100) and Fraction(760, 100) <= r3.hi
    assert r1.hi < Fraction(760, 100)
    with pytest.raises(QedWeakHadronicRefusal):
        abj_colour_factor(0)


def test_qm228_gell_mann_okubo_identity_and_pdg_residuals() -> None:
    assert su3_mass_coefficients(Fraction(1, 2), Fraction(1)) == (1, 1, Fraction(1, 2))
    audit = build_gell_mann_okubo_audit()
    assert audit.octet_coefficients == (0, 0, 0)
    assert audit.decuplet_second_differences == ((0, 0, 0), (0, 0, 0))
    inp = BaryonMassInputs()
    lhs = 2 * (inp.nucleon + inp.xi)
    rhs = 3 * inp.lambda_ + inp.sigma
    assert audit.octet_lhs_2_n_plus_xi == lhs
    assert audit.octet_rhs_3_lambda_plus_sigma == rhs
    assert lhs < rhs
    residual = (rhs - lhs) / rhs
    assert audit.octet_fractional_residual == residual
    assert Fraction(5, 1000) < residual <= Fraction(6, 1000)
    prediction = 2 * inp.xi_star - inp.sigma_star
    assert audit.omega_equal_spacing_prediction == prediction
    omega_residual = (prediction - inp.omega) / inp.omega
    assert audit.omega_fractional_residual == omega_residual
    assert 0 < omega_residual <= Fraction(1, 100)


def test_qm226_227_228_combined_report_passes() -> None:
    report = evaluate_qed_weak_hadronic_control()
    assert report.control_ids == ("QM-226", "QM-227", "QM-228")
    assert report.passed
