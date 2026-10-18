"""Tier 2: Boundary and Corner Cases E2E Tests (26 Tests).

AuthorityEffect: None.
Stress-tests extremal states, degenerate operators, near-singular configurations, and algebraic boundaries.
"""

from __future__ import annotations

from fractions import Fraction
import numpy as np
import pytest

from finite_qm.domain.cyclotomic_tower import CyclotomicElement
from finite_qm.domain.gaussian_rational import Gaussian
from finite_qm.domain.primitive_difference import PrimitiveDifference
from finite_qm.domain.primitives import (
    SIGMA_Z,
    bell_state,
    is_density_matrix,
    mutual_information,
    partial_trace_b,
    purity,
    trace_norm,
    von_neumann_entropy,
)
from finite_qm.use_cases.born_normalization import (
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)
from finite_qm.use_cases.cptp_channel import (
    apply_channel,
    apply_depolarizing_channel,
    choi_matrix,
    dephasing_kraus,
    trace_distance_contraction,
    verify_dual_witness_bound,
    wigner_yanase_skew_information,
)
from finite_qm.use_cases.discrete_walk_engines import (
    build_glued_simplex_packet,
    cayley_evolution_from_packet,
    evaluate_quartic_frame_sum_rational,
    monotone_admission_from_packet,
)
from finite_qm.use_cases.stabilizer_codes import (
    build_steane_seven_qubit_code,
    build_three_qubit_bitflip_code,
)


def test_tier2_born_normalization_uniform_distribution():
    """1. Uniform probability vector N=128 amplitude lift."""
    n = 128
    rho = np.ones(n) / n
    psi = l1_to_l2_amplitude_lift(rho)
    assert verify_born_normalization(psi) is True
    assert np.allclose(np.abs(psi) ** 2, 1.0 / n, atol=1e-12)


def test_tier2_born_normalization_delta_distribution():
    """2. Kronecker delta single-point distribution amplitude lift."""
    rho = [1.0, 0.0, 0.0, 0.0]
    psi = l1_to_l2_amplitude_lift(rho)
    assert verify_born_normalization(psi) is True
    assert np.isclose(psi[0], 1.0, atol=1e-12)
    assert np.allclose(psi[1:], 0.0, atol=1e-12)


def test_tier2_born_normalization_near_singular_distribution():
    """3. Near-singular distribution [1.0, 1e-15] numerical stability."""
    rho = [1.0, 1e-15]
    psi = l1_to_l2_amplitude_lift(rho)
    assert verify_born_normalization(psi) is True
    assert np.isfinite(psi).all()


def test_tier2_density_matrix_rank1_pure_state():
    """4. Rank-1 pure state purity = 1.0 and zero von Neumann entropy."""
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert is_density_matrix(rho) is True
    assert np.isclose(purity(rho), 1.0, atol=1e-12)
    assert np.isclose(von_neumann_entropy(rho), 0.0, atol=1e-12)


def test_tier2_density_matrix_maximally_mixed_state():
    """5. Maximally mixed state in d=4 purity = 0.25 and entropy = 2.0 bits."""
    rho = np.eye(4, dtype=complex) / 4.0
    assert is_density_matrix(rho) is True
    assert np.isclose(purity(rho), 0.25, atol=1e-12)
    assert np.isclose(von_neumann_entropy(rho), 2.0, atol=1e-12)


def test_tier2_density_matrix_boundary_eigenvalues():
    """6. Boundary spectrum [0.5, 0.5, 0.0] positive semidefiniteness."""
    rho = np.diag([0.5, 0.5, 0.0]).astype(complex)
    assert is_density_matrix(rho) is True


def test_tier2_partial_trace_product_state():
    """7. Product state partial trace yields pure marginal and zero mutual information."""
    rho_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_b = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    rho_ab = np.kron(rho_a, rho_b)
    assert np.allclose(partial_trace_b(rho_ab), rho_a, atol=1e-12)
    assert np.isclose(mutual_information(rho_ab), 0.0, atol=1e-12)


def test_tier2_partial_trace_bell_state():
    """8. Bell pair partial trace yields maximally mixed marginal and I(A:B) = 2.0."""
    rho_bell = bell_state()
    red_a = partial_trace_b(rho_bell)
    assert np.allclose(red_a, 0.5 * np.eye(2), atol=1e-12)
    assert np.isclose(mutual_information(rho_bell), 2.0, atol=1e-9)


def test_tier2_cptp_channel_identity_map():
    """9. Identity channel preserves state and contraction ratio identically 1.0."""
    rho = np.array([[0.7, 0.1], [0.1, 0.3]], dtype=complex)
    k_id = [np.eye(2, dtype=complex)]
    assert np.allclose(apply_channel(rho, k_id), rho, atol=1e-12)
    res = trace_distance_contraction(rho, np.eye(2) / 2.0, k_id)
    assert np.isclose(res["contraction_factor"], 1.0, atol=1e-9)


def test_tier2_cptp_channel_complete_depolarization():
    """10. Complete depolarization p=1.0 drives any input to maximally mixed state."""
    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_out = apply_depolarizing_channel(rho0, 1.0)
    assert np.allclose(rho_out, np.eye(2) / 2.0, atol=1e-12)


def test_tier2_cptp_channel_zero_noise():
    """11. Dephasing channel with zero noise p=0.0 acts as identity."""
    kraus = dephasing_kraus(0.0)
    rho = np.array([[0.6, 0.48], [0.48, 0.4]], dtype=complex)
    assert np.allclose(apply_channel(rho, kraus), rho, atol=1e-12)


def test_tier2_cptp_channel_maximal_dephasing():
    """12. Dephasing channel with maximal noise p=0.5 eliminates off-diagonals."""
    kraus = dephasing_kraus(0.5)
    rho = np.array([[0.6, 0.48], [0.48, 0.4]], dtype=complex)
    rho_out = apply_channel(rho, kraus)
    assert np.isclose(abs(rho_out[0, 1]), 0.0, atol=1e-12)
    assert np.isclose(rho_out[0, 0].real, 0.6, atol=1e-12)
    assert np.isclose(rho_out[1, 1].real, 0.4, atol=1e-12)


def test_tier2_choi_matrix_dimension_1_trivial():
    """13. Trivial 1x1 scalar channel Choi matrix."""
    k_scalar = [np.array([[1.0]], dtype=complex)]
    j_mat = choi_matrix(k_scalar)
    assert j_mat.shape == (1, 1)
    assert np.isclose(j_mat[0, 0], 1.0, atol=1e-12)


def test_tier2_wigner_yanase_skew_information_commuting_observable():
    """14. Wigner-Yanase skew information vanishes for commuting observable."""
    rho = np.diag([0.8, 0.2]).astype(complex)
    val = wigner_yanase_skew_information(rho, SIGMA_Z)
    assert np.isclose(val, 0.0, atol=1e-12)


def test_tier2_trace_distance_identical_states():
    """15. Trace distance between identical states vanishes and dual witness evaluates to 0."""
    rho = np.diag([0.6, 0.4]).astype(complex)
    assert np.isclose(trace_norm(rho - rho), 0.0, atol=1e-12)
    assert verify_dual_witness_bound(rho, rho) is True


def test_tier2_trace_distance_orthogonal_states():
    """16. Trace distance between orthogonal pure states equals exactly 2.0."""
    rho1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho2 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    assert np.isclose(trace_norm(rho1 - rho2), 2.0, atol=1e-12)


def test_tier2_three_qubit_code_identity_error():
    """17. Three-qubit bitflip code with identity error syndrome is (+1, +1)."""
    res = build_three_qubit_bitflip_code()
    assert res["syndromes"]["I"] == (1, 1)


def test_tier2_steane_code_identity_error():
    """18. Steane [[7, 1, 3]] code with identity error has correctable single-qubit errors."""
    res = build_steane_seven_qubit_code()
    assert res["fano_intersections_even"] is True
    assert res["all_single_qubit_errors_correctable"] is True


def test_tier2_quartic_frame_sum_standard_basis():
    """19. Quartic frame readout sum on 2D standard basis equals 1.0."""
    psi = (Fraction(1), Fraction(0))
    frame = [(Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))]
    s = evaluate_quartic_frame_sum_rational(psi, frame)
    assert s == Fraction(1)


def test_tier2_cayley_evolution_zero_time():
    """20. Cayley operator at tau = 0 evaluates to identity."""
    pkt = build_glued_simplex_packet()
    res = cayley_evolution_from_packet(pkt, tau=0.0)
    assert np.allclose(res["cayley_operator"], np.eye(res["dimension"]), atol=1e-12)


def test_tier2_monotone_admission_full_dimension():
    """21. Monotone projection admission exhibits strictly positive dissipation residue."""
    pkt = build_glued_simplex_packet()
    res = monotone_admission_from_packet(pkt, keep_dim=2)
    assert res["delta_irr_positive"] is True
    assert res["delta_irr"] > 0.0


def test_tier2_cyclotomic_element_rational_zero():
    """22. Rational zero element in CyclotomicTower."""
    zero = CyclotomicElement.rational(0, 8)
    assert zero == CyclotomicElement.rational(0, 8)
    assert zero + zero == zero


def test_tier2_cyclotomic_element_rational_one():
    """23. Rational unit element in CyclotomicTower."""
    one = CyclotomicElement.rational(1, 8)
    assert one * one == one
    assert one != CyclotomicElement.rational(0, 8)


def test_tier2_gaussian_rational_purely_imaginary():
    """24. Gaussian rational exact arithmetic with imaginary unit."""
    z = Gaussian(Fraction(0), Fraction(1))
    z_sq = z * z
    assert z_sq == Gaussian(Fraction(-1), Fraction(0))
    inv_z = Gaussian(Fraction(1), Fraction(0)) / z
    assert inv_z == Gaussian(Fraction(0), Fraction(-1))


def test_tier2_primitive_difference_constant_section():
    """25. Constant section on graph has zero raw L1 defect and empty support."""
    section = {"v0": 42.0, "v1": 42.0, "v2": 42.0}
    edges = [("v0", "v1"), ("v1", "v2"), ("v2", "v0")]
    assert PrimitiveDifference.phi_raw(section, edges) == 0.0
    assert PrimitiveDifference.support(section, edges) == 0


def test_tier2_superposition_single_sector():
    """26. Single sector probability lift has trivial phase space."""
    rho = [1.0]
    psi = l1_to_l2_amplitude_lift(rho)
    assert verify_born_normalization(psi) is True
    assert len(psi) == 1
    assert np.isclose(psi[0], 1.0, atol=1e-12)
