# AuthorityEffect: None.
"""End-to-end tests for QM-218 Page-Wootters clock dressing, Q(zeta_8) Tsirelson SOS, and (Z_3)^2 Wigner."""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases.page_wootters_tsirelson_wigner_control import (
    QZeta3,
    QZeta8,
    certified_sqrt2_interval,
    compute_wigner_table_z3,
    evaluate_page_wootters_tsirelson_wigner_control,
    wigner_phase_point_operator_z3,
)


def test_part_a_page_wootters_clock_dressing_and_static_constraint() -> None:
    """Verify Page-Wootters constraint projector, DFM clock dressing, and static tick readout."""
    report = evaluate_page_wootters_tsirelson_wigner_control()
    assert report.pw_history_shift_unitary_and_order_4
    assert report.pw_constraint_projector_idempotent_hermitian
    assert report.pw_constraint_projector_trace == 2
    assert report.pw_constraint_annihilates_projector
    assert report.pw_dressing_intertwines_history_shift
    assert report.pw_dressing_decouples_projector
    assert report.pw_bare_observable_breaks_constraint
    assert report.pw_relational_observables_commute_with_constraint
    assert report.pw_heisenberg_step_covariance_exact
    assert report.pw_static_state_sigma_x_ticks == (
        Fraction(1),
        Fraction(0),
        Fraction(-1),
        Fraction(0),
    )
    assert report.pw_static_state_sigma_y_ticks == (
        Fraction(0),
        Fraction(1),
        Fraction(0),
        Fraction(-1),
    )


def test_part_b_classical_chsh_polytope_vs_cyclotomic_q_zeta8_algebra() -> None:
    """Verify classical polytope bound 2 and exact sqrt(2) = z - z^3 in Q(zeta_8)."""
    report = evaluate_page_wootters_tsirelson_wigner_control()
    assert report.chsh_classical_polytope_vertex_count == 16
    assert report.chsh_classical_polytope_max == Fraction(2)
    assert report.chsh_cyclotomic_sqrt2_squares_to_2
    assert report.chsh_cyclotomic_sqrt2_inverse_exact

    s2 = QZeta8.sqrt2()
    inv_s2 = QZeta8.inv_sqrt2()
    assert s2 * s2 == QZeta8.from_int(2)
    assert s2 * inv_s2 == QZeta8.from_int(1)


def test_part_b_tsirelson_sos_decomposition_and_bell_eigenstate() -> None:
    """Verify Landau identity, algebraic SOS decomposition, and Bell state saturation."""
    report = evaluate_page_wootters_tsirelson_wigner_control()
    assert report.chsh_observables_involutory_and_spacelike_commuting
    assert report.chsh_landau_identity_exact
    assert report.chsh_sos_decomposition_exact
    assert report.chsh_bell_state_annihilated_by_sos_witnesses
    assert report.chsh_bell_state_eigenvalue_is_2_sqrt2
    assert report.chsh_separable_state_expectation_is_sqrt2


def test_part_c_discrete_weyl_wigner_phase_space_on_z3_squared() -> None:
    """Verify (Z_3)^2 phase-point operators, line marginals, and Wigner negativity."""
    report = evaluate_page_wootters_tsirelson_wigner_control()
    assert report.wigner_phase_point_hermitian_involutory_unit_trace
    assert report.wigner_phase_point_orthogonality_and_completeness
    assert report.wigner_line_marginals_match_projectors
    assert report.wigner_stabilizer_nonnegative_and_normalized
    assert report.wigner_stabilizer_negativity == Fraction(0)
    assert report.wigner_superposition_normalized_and_marginals_exact
    assert report.wigner_superposition_min_value == Fraction(-1, 3)
    assert report.wigner_superposition_negativity == Fraction(2, 3)


def test_part_c_wigner_negative_controls_and_invalid_inputs() -> None:
    """Verify out-of-range phase-space coordinates and zero-norm states raise ValueError."""
    with pytest.raises(ValueError):
        wigner_phase_point_operator_z3(3, 0)
    with pytest.raises(ValueError):
        wigner_phase_point_operator_z3(0, -1)
    with pytest.raises(ValueError):
        compute_wigner_table_z3([QZeta3.from_int(0)] * 3)


def test_part_c_twelve_decimal_tsirelson_enclosures() -> None:
    """Verify certified 12-decimal RationalInterval enclosures for Tsirelson quantities."""
    report = evaluate_page_wootters_tsirelson_wigner_control()
    assert report.sqrt2_square_bounds_enclose_two
    sqrt2_iv = certified_sqrt2_interval()
    assert sqrt2_iv.lo * sqrt2_iv.lo <= Fraction(2) <= sqrt2_iv.hi * sqrt2_iv.hi
    assert report.tsirelson_bound_interval.width < Fraction(1, 10**14)
    assert report.bell_violation_excess_interval.width < Fraction(1, 10**14)
    assert report.tsirelson_per_correlator_interval.width < Fraction(1, 10**14)
    assert report.tsirelson_bound_decimal_12 == "2.828427124746"
    assert report.bell_violation_excess_decimal_12 == "0.828427124746"
    assert report.tsirelson_per_correlator_decimal_12 == "0.707106781186"
