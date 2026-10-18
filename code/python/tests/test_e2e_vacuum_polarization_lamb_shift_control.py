# AuthorityEffect: None.
"""End-to-end tests for QM-216 1-loop QED vacuum polarization, running alpha, and Lamb shift."""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.vacuum_polarization_lamb_shift_control import (
    check_transverse_projector_identities,
    evaluate_vacuum_polarization_lamb_shift_control,
    fermion_bubble_numerator_analytic,
    fermion_bubble_numerator_clifford_trace,
    feynman_parameter_moment_beta_closed,
    feynman_parameter_moment_polynomial,
    transverse_projector,
)


def test_part_a_transverse_ward_projector_and_null_guard() -> None:
    """Verify q_mu P_T^{mu nu}(q) = 0, P_T^2 = P_T, tr(P_T) = 3, and null-momentum refusal."""
    q_timelike = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(1, 1)]
    q_spacelike = [Fraction(2, 1), Fraction(3, 1), Fraction(1, 1), Fraction(1, 1)]
    for q_vec in (q_timelike, q_spacelike):
        ward_ok, idemp_ok, tr_val = check_transverse_projector_identities(q_vec)
        assert ward_ok
        assert idemp_ok
        assert tr_val == Fraction(3, 1)

    # Negative control: null light-cone momentum q^2 = 0 must raise ZeroDivisionError
    q_null = [Fraction(5, 1), Fraction(3, 1), Fraction(4, 1), Fraction(0, 1)]
    with pytest.raises(ZeroDivisionError):
        transverse_projector(q_null)


def test_part_a_clifford_bubble_numerator_trace_matches_analytic() -> None:
    """Verify 4x4 Clifford trace tr[gamma^mu(k_slash+q_slash+m)gamma^nu(k_slash+m)] over Q(i)."""
    k = [Fraction(5, 1), Fraction(-1, 1), Fraction(2, 1), Fraction(3, 1)]
    q = [Fraction(2, 1), Fraction(3, 1), Fraction(1, 1), Fraction(1, 1)]
    mass = Fraction(2, 1)
    num_cliff = fermion_bubble_numerator_clifford_trace(k, q, mass)
    num_anal = fermion_bubble_numerator_analytic(k, q, mass)
    assert num_cliff == num_anal

    # Negative control: perturbing mass m = 2 -> m = 3 changes diagonal trace entries
    assert num_cliff != fermion_bubble_numerator_analytic(k, q, Fraction(3, 1))


def test_part_a_symanzik_bubble_simplex_and_bphz_on_shell_subtraction() -> None:
    """Verify U_{G_bub}(x, 1-x) = 1, F_{G_bub} = m^2 - x(1-x)q^2, and BPHZ UV cutoff cancellation."""
    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.transverse_ward_identity_exact
    assert report.transverse_projector_idempotent_exact
    assert report.transverse_projector_trace_equals_three == Fraction(3, 1)
    assert report.clifford_bubble_trace_matches_analytic
    assert report.symanzik_bubble_simplex_u_equals_one
    assert report.symanzik_bubble_simplex_f_matches_feynman_denom
    assert report.bphz_uv_cutoff_cancels_at_all_scales
    assert report.bphz_on_shell_pi_r_at_zero_is_zero


def test_part_b_feynman_parameter_moments_and_uehling_series() -> None:
    """Verify exact polynomial integration matches Beta((n+1)!^2/(2n+3)!) and Uehling 1/15 slope."""
    expected_moments = [
        Fraction(1, 30),
        Fraction(1, 140),
        Fraction(1, 630),
        Fraction(1, 2772),
    ]
    for n, exp_m in enumerate(expected_moments, start=1):
        assert feynman_parameter_moment_polynomial(n) == exp_m
        assert feynman_parameter_moment_beta_closed(n) == exp_m

    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.moments_match_beta_closed_form
    assert report.uehling_leading_slope_coeff == Fraction(1, 15)
    assert report.second_moment_series_coeff == Fraction(1, 140)
    assert report.third_moment_series_coeff == Fraction(1, 945)


def test_part_b_spacelike_vacuum_polarization_and_running_alpha_enclosure() -> None:
    """Verify 12-decimal enclosure of Pi_R(-9m^2/4) and running alpha_eff^{-1}(-9m^2/4)."""
    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.spacelike_velocity_v == Fraction(5, 3)
    assert report.spacelike_q2_over_m2 == Fraction(-9, 4)
    assert report.pi_r_spacelike_interval.hi < 0
    assert report.pi_r_spacelike_12_digits_agree
    assert report.pi_r_spacelike_decimal_12 == "-0.000284802666"
    assert report.alpha_eff_inv_spacelike_12_digits_agree
    assert report.alpha_eff_inv_spacelike_decimal_12 == "136.996970947974"
    assert report.alpha_eff_exceeds_bare_alpha


def test_part_c_uehling_potential_and_hydrogen_lamb_shift_enclosure() -> None:
    """Verify 5/6 + 1/8 - 1/5 = 91/120 contact sum and 12-decimal -27.128756729153 MHz Uehling shift."""
    report = evaluate_vacuum_polarization_lamb_shift_control()
    assert report.lamb_contact_se_term == Fraction(5, 6)
    assert report.lamb_contact_g2_magnetic_term == Fraction(1, 8)
    assert report.lamb_contact_uehling_vp_term == Fraction(-1, 5)
    assert report.lamb_contact_total_rational == Fraction(91, 120)
    assert report.lamb_contact_se_term + report.lamb_contact_uehling_vp_term == Fraction(19, 30)
    assert report.uehling_2s_dimensionless_coeff == Fraction(-1, 30)
    assert report.uehling_2s_dimensionless_interval.hi < 0
    assert report.uehling_2s_mhz_12_digits_agree
    assert report.uehling_2s_mhz_decimal_12 == "-27.128756729153"
