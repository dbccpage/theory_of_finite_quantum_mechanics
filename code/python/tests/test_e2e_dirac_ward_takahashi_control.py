# AuthorityEffect: None.
"""End-to-end tests for QM-215 Dirac/Kulish-Faddeev dressed matter and Ward-Takahashi Z_1 = Z_2."""

from __future__ import annotations

from fractions import Fraction

from finite_qm.use_cases.dirac_ward_takahashi_control import (
    Qi,
    check_clifford_anticommutation,
    dirac_propagator,
    dirac_propagator_inverse,
    evaluate_dirac_ward_takahashi_control,
    feynman_slash,
    mat4_identity,
    mat4_mul,
    mat4_sub,
    one_loop_self_energy_integrand,
    one_loop_self_energy_minus_derivative,
    one_loop_vertex_integrand,
)


def test_part_a_clifford_algebra_and_tree_level_ward_takahashi() -> None:
    """Verify 4x4 Clifford anticommutation over Q(i) and tree-level Ward-Takahashi identity."""
    assert check_clifford_anticommutation()
    p = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    q = [Fraction(2, 1), Fraction(-1, 1), Fraction(1, 1), Fraction(3, 1)]
    pq = [p[mu] + q[mu] for mu in range(4)]
    mass = Fraction(2, 1)

    sf_p = dirac_propagator(p, mass)
    sf_p_inv = dirac_propagator_inverse(p, mass)
    sf_pq = dirac_propagator(pq, mass)
    sf_pq_inv = dirac_propagator_inverse(pq, mass)
    q_slash = feynman_slash(q)

    assert mat4_mul(sf_p, sf_p_inv) == mat4_identity()
    assert mat4_mul(sf_pq, sf_pq_inv) == mat4_identity()
    assert mat4_sub(sf_pq_inv, sf_p_inv) == q_slash
    assert mat4_mul(sf_pq, mat4_mul(q_slash, sf_p)) == mat4_sub(sf_p, sf_pq)


def test_part_a_dfm_spanning_tree_dressed_fermion_gauge_invariance() -> None:
    """Verify bare correlator gauge dependence vs. DFM dressed correlator gauge invariance."""
    report = evaluate_dirac_ward_takahashi_control()
    assert report.bare_correlator_gauge_dependent
    assert report.dfm_dressed_correlator_gauge_invariant_all_trees
    assert report.dfm_tree_change_shifts_by_cycle_holonomy


def test_part_b_one_loop_ward_takahashi_integrand_identity() -> None:
    """Verify q_mu I_Lambda^mu(p+q, p; k) == I_Sigma(p, k) - I_Sigma(p+q, k) in M_4(Q(i))."""
    report = evaluate_dirac_ward_takahashi_control()
    assert report.one_loop_ward_takahashi_integrand_exact


def test_part_b_differential_ward_identity_and_z1_equals_z2() -> None:
    """Verify I_Lambda^mu(p, p; k) == -d I_Sigma(p, k)/d p_mu at q=0 and Z_1 / Z_2 == 1."""
    p = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    k = [Fraction(3, 1), Fraction(-2, 1), Fraction(1, 2), Fraction(1, 1)]
    mass = Fraction(2, 1)
    photon_mass_sq = Fraction(1, 3)

    for mu in range(4):
        lam_mu = one_loop_vertex_integrand(p, p, k, mu, mass, photon_mass_sq)
        minus_dsigma_mu = one_loop_self_energy_minus_derivative(p, k, mu, mass, photon_mass_sq)
        assert lam_mu == minus_dsigma_mu

    # Negative control: perturbing p' != p breaks equality with -d I_Sigma(p, k)/d p_0
    p_perturbed = [Fraction(6, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    lam_pert = one_loop_vertex_integrand(p_perturbed, p, k, 0, mass, photon_mass_sq)
    assert lam_pert != one_loop_self_energy_minus_derivative(p, k, 0, mass, photon_mass_sq)

    report = evaluate_dirac_ward_takahashi_control()
    assert report.one_loop_differential_ward_identity_at_q_zero_exact
    assert report.bphz_vertex_and_self_energy_uv_counterterms_equal
    assert report.z1_over_z2_ratio_exact_one == Fraction(1, 1)


def test_part_c_kulish_faddeev_ir_cancellation_and_enclosure() -> None:
    """Verify IR regulator cancellation and 12-decimal enclosure of S_KF = exp(E_KF)."""
    report = evaluate_dirac_ward_takahashi_control()
    assert report.kf_ir_scale_cancels_across_all_cutoffs
    assert report.kf_ir_laurent_pole_cancels_identically
    assert report.kf_cusp_velocity == Fraction(3, 5)
    assert report.kf_energy_resolution_ratio == Fraction(1, 2)
    assert report.kf_exponent_interval.hi < 0
    assert report.kf_attenuation_12_digits_agree
    assert report.kf_attenuation_interval.width < Fraction(1, 10**14)
    assert report.kf_attenuation_decimal_12 == "0.997892261461"


def test_gaussian_rational_qi_field_invariants() -> None:
    """Verify exact multiplicative inverse and norm on Gaussian rationals Q(i)."""
    z = Qi(Fraction(3, 5), Fraction(4, 5))
    assert z.norm_sq() == Fraction(1, 1)
    assert z * z.inv() == Qi.one()
    assert z.inv() == z.conj()
    # Non-zero check on self-energy integrand
    p = [Fraction(5, 1), Fraction(1, 1), Fraction(2, 1), Fraction(-1, 1)]
    k = [Fraction(3, 1), Fraction(-2, 1), Fraction(1, 2), Fraction(1, 1)]
    sig = one_loop_self_energy_integrand(p, k, Fraction(2, 1), Fraction(1, 3))
    assert sig != mat4_identity()
