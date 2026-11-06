# AuthorityEffect: None.
"""End-to-end tests for QM-217 algebraic bound-state spectra (su(2) Kravchuk & so(4) Hydrogen)."""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.algebraic_bound_state_spectra_control import (
    check_kravchuk_orthogonality_and_difference_eq,
    dirac_fine_structure_coeff,
    evaluate_algebraic_bound_state_spectra_control,
    q_comm,
    q_is_zero,
    sl2_oscillator_generators,
    so4_hydrogen_shell_operators,
)


def test_part_a_su2_kravchuk_harmonic_oscillator_and_uncertainty_saturation() -> None:
    """Verify sl(2, Q) ladder algebra, G-metric adjointness, and Robertson-Schrodinger saturation."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.kravchuk_sl2_commutators_exact
    assert report.kravchuk_casimir_matches_j_j_plus_1
    assert report.kravchuk_metric_adjoint_exact
    assert report.kravchuk_equidistant_ladder_commutators_exact
    assert report.kravchuk_ground_variance_q2 == Fraction(1, 4)
    assert report.kravchuk_ground_variance_p2 == Fraction(1, 4)
    assert report.kravchuk_ground_uncertainty_product == Fraction(1, 16)
    assert report.kravchuk_ground_saturates_robertson_schrodinger
    assert report.kravchuk_polynomial_orthogonality_exact
    assert report.kravchuk_difference_eigenvalue_exact

    # Negative control: twice_j < 1 is rejected
    with pytest.raises(ValueError):
        sl2_oscillator_generators(0)


def test_part_a_kravchuk_polynomial_orthogonality_and_difference_equation() -> None:
    """Verify discrete Kravchuk binomial orthogonality and 3-term difference eigenvalue identity."""
    for n_max in (1, 2, 3, 4, 5):
        ortho_ok, diff_ok = check_kravchuk_orthogonality_and_difference_eq(n_max)
        assert ortho_ok
        assert diff_ok


def test_part_b_so4_pauli_runge_lenz_hydrogen_spectrum_and_orthogonality() -> None:
    """Verify L . K = 0, C_2(so(4)) = (n^2 - 1) I, E_n = -1/n^2, and orbital L^2 traces."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.hydrogen_chiral_factors_commute
    assert report.hydrogen_so4_lie_brackets_exact
    assert report.hydrogen_pauli_orthogonality_l_dot_k_zero
    assert report.hydrogen_asymmetric_control_l_dot_k_nonzero
    assert report.hydrogen_casimir_matches_n_squared_minus_1
    assert report.hydrogen_balmer_rydberg_energies == (
        Fraction(-1, 1),
        Fraction(-1, 4),
        Fraction(-1, 9),
        Fraction(-1, 16),
    )
    assert report.hydrogen_lyman_alpha_dimensionless_jump == Fraction(3, 4)
    assert report.hydrogen_balmer_alpha_dimensionless_jump == Fraction(5, 36)
    assert report.hydrogen_orbital_l2_traces == (
        Fraction(0, 1),
        Fraction(6, 1),
        Fraction(36, 1),
        Fraction(120, 1),
    )
    assert report.hydrogen_orbital_l2_traces_match_clebsch_gordan

    with pytest.raises(ValueError):
        so4_hydrogen_shell_operators(0)


def test_part_c_n2_degeneracy_projectors_and_runge_lenz_symmetry_breaking() -> None:
    """Verify Pi_{2S} and Pi_{2P} projectors, Dirac fine-structure degeneracy, and [Pi_{2S}, K_z] != 0."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.n2_projectors_idempotent_orthogonal_complete
    assert report.n2_2s_rank == Fraction(1, 1)
    assert report.n2_2p_rank == Fraction(3, 1)
    assert report.n2_pi_2s_commutes_with_so3_l
    assert report.n2_pi_2s_breaks_runge_lenz_k
    assert report.dirac_fs_2s_half_coeff == Fraction(-5, 128)
    assert report.dirac_fs_2p_half_coeff == Fraction(-5, 128)
    assert report.dirac_fs_2p_three_halves_coeff == Fraction(-1, 128)
    assert report.dirac_fs_2s_2p_half_degenerate
    assert report.dirac_fs_fine_structure_splitting_coeff == Fraction(1, 32)

    # Negative control: even twice_j_tot is rejected for half-integer electron total spin
    with pytest.raises(ValueError):
        dirac_fine_structure_coeff(2, 2)


def test_part_c_12_decimal_lyman_alpha_and_lamb_contact_enclosures() -> None:
    """Verify 12-decimal RationalInterval enclosures for Lyman-alpha THz and 2S-2P contact MHz."""
    report = evaluate_algebraic_bound_state_spectra_control()
    assert report.lyman_alpha_gross_thz_12_digits_agree
    assert report.lyman_alpha_gross_thz_interval.width < Fraction(1, 10**13)
    assert report.lyman_alpha_gross_thz_decimal_12 == "2467.381467264629"

    assert report.lamb_contact_2s_2p_mhz_12_digits_agree
    assert report.lamb_contact_2s_2p_mhz_interval.width < Fraction(1, 10**13)
    assert report.lamb_contact_2s_2p_mhz_decimal_12 == "617.179215588248"


def test_part_c_so4_runge_lenz_commutes_with_unperturbed_casimir() -> None:
    """Verify [C_2(so(4)), K_z] = 0 on H_2 while [Pi_{2S}, K_z] != 0."""
    ops_n2 = so4_hydrogen_shell_operators(2)
    assert q_is_zero(q_comm(ops_n2["C2_so4"], ops_n2["Kz"]))
