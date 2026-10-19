"""
test_open_system_transfer_bounds.py — Unit tests for continuous-to-discrete transfer bounds
under open-system Lindblad master equations (Claim MAJ-C18).

AuthorityEffect: None.
"""

import math
import numpy as np
import pytest
from majorana_evaluator import (
    OpenSystemMajoranaBraidModel,
    TransferBoundReceipt,
    NonMarkovianBosonicBathModel,
    NonMarkovianTransferReceipt,
    ContinuumCrossJunctionFemModel,
    MultiTerminalTransferReceipt,
)


def test_lindblad_trace_defect_bounds():
    """Verifies that the trace-norm transfer defect is well-defined and bounded in [0, 1]."""
    model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.01, length_over_xi=6.0)
    for t in (0.5, 1.0, 3.0, 5.0, 10.0, 20.0):
        defect = model.evaluate_defect(t)
        assert 0.0 <= defect <= 1.0
        assert not math.isnan(defect)


def test_non_adiabatic_fast_braiding_scaling():
    """Verifies that non-adiabatic bulk leakage dominates at small braiding duration T."""
    model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.0, length_over_xi=20.0)
    defect_fast = model.evaluate_defect(0.5)
    defect_moderate = model.evaluate_defect(5.0)

    # Fast braiding causes higher leakage than moderate adiabatic braiding
    assert defect_fast > defect_moderate
    assert defect_fast >= 0.5


def test_quasiparticle_poisoning_slow_braiding_scaling():
    """Verifies that quasiparticle poisoning leakage grows with braiding duration T."""
    model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.05, length_over_xi=20.0)
    # Beyond the optimal time, longer duration leads to more poisoning
    defect_sweet = model.evaluate_defect(3.0)
    defect_long = model.evaluate_defect(30.0)

    assert defect_long > defect_sweet


def test_pareto_optimal_sweet_spot_and_positive_infimum():
    """
    Verifies Claim MAJ-C18: whenever gamma_qp > 0, the continuous-to-discrete transfer defect
    has a strictly positive infimum Delta_min > 0 at finite optimal duration T*.
    """
    model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.02, length_over_xi=6.0)
    t_opt, min_def = model.optimal_braid_time()

    assert 0.5 < t_opt < 50.0
    assert min_def > 0.0

    # Numerical verification that defect at T* is lower than at small or large extremes
    defect_opt = model.evaluate_defect(t_opt)
    defect_small = model.evaluate_defect(0.5)
    defect_large = model.evaluate_defect(50.0)

    assert defect_opt < defect_small
    assert defect_opt < defect_large
    assert defect_opt > 0.0


def test_overlap_splitting_suppression_with_wire_length():
    """Verifies that increasing wire length L/xi exponentially suppresses overlap splitting."""
    model_short = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.01, length_over_xi=2.0)
    model_long = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.01, length_over_xi=8.0)

    assert model_short.overlap_splitting > model_long.overlap_splitting
    ratio = model_short.overlap_splitting / model_long.overlap_splitting
    expected_ratio = math.exp(6.0)
    assert abs(ratio - expected_ratio) < 1e-6


def test_ideal_limit_convergence_to_zero():
    """
    Verifies that the minimum transfer defect Delta_min vanishes if and only if
    quasiparticle poisoning vanishes and wire length is infinite.
    """
    model_ideal = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.0, length_over_xi=40.0)
    t_opt, min_def = model_ideal.optimal_braid_time()

    assert math.isinf(t_opt)
    assert min_def == 0.0


def test_transfer_bound_receipt_emission():
    """Verifies that audit_transfer emits a verified TransferBoundReceipt."""
    model = OpenSystemMajoranaBraidModel(delta=1.0, gamma_qp=0.01, length_over_xi=6.0)
    receipt = model.audit_transfer(braid_time=3.5)

    assert isinstance(receipt, TransferBoundReceipt)
    assert receipt.delta == 1.0
    assert receipt.gamma_qp == 0.01
    assert receipt.is_positive_lower_bounded is True
    assert receipt.status == "TRANSFER_OBSTRUCTED_NONZERO_DEFECT"
    assert receipt.trace_defect > 0.0
    assert receipt.minimum_defect > 0.0


# ============================================================================
# Non-Markovian Bosonic Bath Tests (Claim MAJ-C19)
# ============================================================================

def test_non_markovian_scaling_exponents_sub_vs_super_ohmic():
    """
    Verifies that sub-Ohmic and super-Ohmic bath spectra alter the Pareto minimum
    defect scaling exponent beta = 2 / (p + 2) (Claim MAJ-C19):
    - Sub-Ohmic (s=0.5): p = 1.5, beta = 4/7 approx 0.5714
    - Ohmic (s=1.0): p = 1.0, beta = 2/3 approx 0.6667
    - Super-Ohmic (s=2.0): p = 3.0, beta = 2/5 = 0.4000
    """
    sub_model = NonMarkovianBosonicBathModel(spectral_index=0.5, coupling_alpha=0.01)
    ohm_model = NonMarkovianBosonicBathModel(spectral_index=1.0, coupling_alpha=0.01)
    super_model = NonMarkovianBosonicBathModel(spectral_index=2.0, coupling_alpha=0.01)

    assert abs(sub_model.effective_power_p() - 1.5) < 1e-10
    assert abs(sub_model.scaling_exponent_beta() - (4.0 / 7.0)) < 1e-10

    assert abs(ohm_model.effective_power_p() - 1.0) < 1e-10
    assert abs(ohm_model.scaling_exponent_beta() - (2.0 / 3.0)) < 1e-10

    assert abs(super_model.effective_power_p() - 3.0) < 1e-10
    assert abs(super_model.scaling_exponent_beta() - 0.40) < 1e-10

    # The exponent is strictly altered across bath spectra
    assert sub_model.scaling_exponent_beta() < ohm_model.scaling_exponent_beta()
    assert super_model.scaling_exponent_beta() < ohm_model.scaling_exponent_beta()


def test_sub_gap_bath_cutoff_exponential_suppression():
    """
    Verifies that when the bath cutoff frequency is below the topological gap
    (omega_c < Delta), bulk excitation leakage is exponentially suppressed.
    """
    sub_gap = NonMarkovianBosonicBathModel(spectral_index=2.0, cutoff_omega_c=0.2, delta=1.0)
    above_gap = NonMarkovianBosonicBathModel(spectral_index=2.0, cutoff_omega_c=2.0, delta=1.0)

    f_sub = sub_gap.cutoff_suppression_factor()
    f_above = above_gap.cutoff_suppression_factor()

    assert f_sub < 1e-2
    assert f_above > 0.5
    assert f_sub < f_above


def test_non_markovian_positive_infimum_across_all_spectra():
    """
    Verifies that for any finite coupling alpha > 0, the continuous-to-discrete transfer
    defect has a strictly positive infimum Delta_min > 0 across all spectral indices.
    """
    for s_val in (0.3, 0.5, 1.0, 1.8, 2.5):
        model = NonMarkovianBosonicBathModel(spectral_index=s_val, coupling_alpha=0.02, delta=1.0)
        t_opt, min_def = model.optimal_braid_time()
        assert t_opt > 0.0
        assert not math.isinf(t_opt)
        assert min_def > 0.0
        # Check that defect at optimal time is lower than at short duration
        d_opt = model.evaluate_defect(t_opt)
        d_fast = model.evaluate_defect(0.01 * t_opt)
        assert d_opt < d_fast


def test_non_markovian_transfer_receipt_emission():
    """Verifies that audit_transfer emits a verified NonMarkovianTransferReceipt."""
    model = NonMarkovianBosonicBathModel(spectral_index=0.5, coupling_alpha=0.01, delta=1.0)
    receipt = model.audit_transfer()

    assert isinstance(receipt, NonMarkovianTransferReceipt)
    assert receipt.spectral_index == 0.5
    assert receipt.is_sub_ohmic is True
    assert receipt.is_super_ohmic is False
    assert receipt.is_positive_lower_bounded is True
    assert receipt.status == "TRANSFER_OBSTRUCTED_NONMARKOVIAN"
    assert receipt.minimum_defect > 0.0
    assert abs(receipt.scaling_exponent_beta - (4.0 / 7.0)) < 1e-10


def test_non_markovian_boundary_and_edge_cases():
    """Verifies boundary branches: omega <= 0, T <= 0, custom power p, and vanishing coupling."""
    model = NonMarkovianBosonicBathModel(spectral_index=1.0, coupling_alpha=0.01, custom_power_p=2.5)
    assert model.effective_power_p() == 2.5
    assert model.spectral_density(-1.0) == 0.0
    assert math.isinf(model.evaluate_defect(0.0))

    # Zero-coupling idealized limit
    model_zero = NonMarkovianBosonicBathModel(spectral_index=1.0, coupling_alpha=0.0, c_lz=0.0)
    t_inf, def_zero = model_zero.optimal_braid_time()
    assert math.isinf(t_inf)
    assert def_zero == 0.0


def test_multiterminal_cross_junction_transfer_bounds_and_disorder():
    """
    Verifies Claim MAJ-C20: multi-terminal cross-junction transfer bounds under
    electrostatic disorder. Demonstrates gap degradation, positive minimum defect,
    and topological phase collapse at critical disorder.
    """
    # Clean 4-terminal cross-junction
    model_clean = ContinuumCrossJunctionFemModel(
        num_terminals=4,
        arm_lengths=[6.0, 6.0, 6.0, 6.0],
        disorder_strength=0.0,
        critical_disorder=0.8,
        nominal_gap=1.0,
    )
    rcpt_clean = model_clean.audit_transfer()

    assert rcpt_clean.num_terminals == 4
    assert rcpt_clean.effective_gap_delta_eff == 1.0
    assert rcpt_clean.is_topological_phase_preserved is True
    assert rcpt_clean.is_positive_lower_bounded is True
    assert rcpt_clean.status == "TRANSFER_OBSTRUCTED_MULTITERMINAL"
    assert rcpt_clean.minimum_defect > 0.0

    # Disordered 4-terminal cross-junction
    model_disordered = ContinuumCrossJunctionFemModel(
        num_terminals=4,
        arm_lengths=[6.0, 6.0, 6.0, 6.0],
        disorder_strength=0.4,
        critical_disorder=0.8,
        nominal_gap=1.0,
    )
    rcpt_disordered = model_disordered.audit_transfer()

    # Gap decreases with disorder: Delta_eff(0.4) = 1.0 * (1 - 0.4/0.8) = 0.5
    assert abs(rcpt_disordered.effective_gap_delta_eff - 0.5) < 1e-10
    assert rcpt_disordered.minimum_defect > rcpt_clean.minimum_defect
    assert rcpt_disordered.total_crosstalk_rate > rcpt_clean.total_crosstalk_rate

    # Critical disorder collapse: sigma_V = 0.85 >= 0.8
    model_collapsed = ContinuumCrossJunctionFemModel(
        num_terminals=4,
        disorder_strength=0.85,
        critical_disorder=0.8,
    )
    rcpt_collapsed = model_collapsed.audit_transfer()
    assert rcpt_collapsed.effective_gap_delta_eff == 0.0
    assert rcpt_collapsed.is_topological_phase_preserved is False
    assert rcpt_collapsed.status == "GAP_COLLAPSED_DISORDER"
    assert rcpt_collapsed.minimum_defect == 1.0
    assert model_collapsed.evaluate_defect(10.0) == 1.0


def test_multiterminal_crosstalk_channels_and_arm_lengths():
    """Verifies that terminal scaling M*(M-1)/2 and arm lengths govern cross-talk rates."""
    # 4 terminals: 6 channels
    model_4 = ContinuumCrossJunctionFemModel(num_terminals=4, arm_lengths=[5.0] * 4)
    # 6 terminals: 15 channels
    model_6 = ContinuumCrossJunctionFemModel(num_terminals=6, arm_lengths=[5.0] * 6)

    assert model_6.total_crosstalk_rate() > model_4.total_crosstalk_rate()

    # Long vs short arms
    model_short = ContinuumCrossJunctionFemModel(num_terminals=4, arm_lengths=[3.0] * 4)
    model_long = ContinuumCrossJunctionFemModel(num_terminals=4, arm_lengths=[8.0] * 4)
    assert model_short.total_crosstalk_rate() > model_long.total_crosstalk_rate()


def test_multiterminal_validation_and_edge_cases():
    """Verifies parameter validation and edge cases."""
    with pytest.raises(ValueError, match="at least 4 terminals"):
        ContinuumCrossJunctionFemModel(num_terminals=3)

    with pytest.raises(ValueError, match="arm lengths"):
        ContinuumCrossJunctionFemModel(num_terminals=4, arm_lengths=[5.0, 5.0])

    model = ContinuumCrossJunctionFemModel(num_terminals=4)
    assert math.isinf(model.evaluate_defect(0.0))

    # Zero rate idealized limit
    model_ideal = ContinuumCrossJunctionFemModel(
        num_terminals=4,
        arm_lengths=[50.0] * 4,
        gamma_qp=0.0,
        c_lz=0.0,
    )
    t_inf, def_zero = model_ideal.optimal_braid_time()
    assert math.isinf(t_inf)
    assert def_zero == 0.0

