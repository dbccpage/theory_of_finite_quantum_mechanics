"""Unit and property tests for Calibration Quotients & Nuisance Transformations (R5)."""

from fractions import Fraction

import pytest
from calibration_quotient import (
    CalibrationQuotient,
    CalibrationQuotientCertificate,
    NuisanceModel,
    OperationalMeasurementSet,
    evaluate_nuisance_invariance,
)


def test_operational_measurement_set_construction():
    """Verify initialization, bounds, and observable family indexing."""
    with pytest.raises(ValueError, match="at least 3 sites"):
        OperationalMeasurementSet(2)

    meas = OperationalMeasurementSet(5)
    assert meas.n_sites == 5
    family = meas.observable_family
    assert len(family) == 15
    assert family[0] == "K_0"
    assert family[1] == "X_0"
    assert family[2] == "Z_0"
    assert family[12] == "K_4"
    assert family[14] == "Z_4"


def test_cochain_construction_on_ring_graph_state():
    """On a 5-qubit graph state, <K_j> = -1, <X_j> = 0, <Z_j> = 0, yielding omega_j = -1."""
    meas = OperationalMeasurementSet(5)
    mu_K = [-1, -1, -1, -1, -1]
    mu_X = [0, 0, 0, 0, 0]
    mu_Z = [0, 0, 0, 0, 0]

    cochain = meas.construct_cochain_from_moments(mu_K, mu_X, mu_Z)
    assert cochain == (Fraction(-1), Fraction(-1), Fraction(-1), Fraction(-1), Fraction(-1))

    quotient = CalibrationQuotient(5)
    assert quotient.mean_circulation(cochain) == Fraction(-1)
    assert quotient.exact_circulation(cochain) == Fraction(1)


def test_cochain_construction_on_optimal_product_state():
    """On the optimal product state with <K> = -r^3, <X> = -r, <Z> = r, omega vanishes identically."""
    # Using rational approximation of Cardano root r ~= 682328 / 1000000
    r = Fraction(682328, 1000000)
    r3 = r * r * r
    meas = OperationalMeasurementSet(5)
    mu_K = [-r3] * 5
    mu_X = [-r] * 5
    mu_Z = [r] * 5

    cochain = meas.construct_cochain_from_moments(mu_K, mu_X, mu_Z)
    # Factor product is r * (-r) * r = -r^3, so mu_K - (-r^3) = 0
    for val in cochain:
        assert val == Fraction(0)

    quotient = CalibrationQuotient(5)
    assert quotient.exact_circulation(cochain) == Fraction(0)


def test_nuisance_model_coboundary_matrix_and_kernel():
    """Coboundary matrix d0 has column sum 0, rank n-1, and im(d0) = ker(ell)."""
    n = 6
    nuisance = NuisanceModel(n)
    mat = nuisance.coboundary_matrix()
    assert len(mat) == n
    assert len(mat[0]) == n

    # Check each column sums to 0
    for col in range(n):
        col_sum = sum(mat[row][col] for row in range(n))
        assert col_sum == Fraction(0)

    # Any potential yields a vector summing to 0
    potential = [Fraction(j, 3) for j in range(n)]
    d0_alpha = nuisance.coboundary(potential)
    assert sum(d0_alpha) == Fraction(0)
    assert nuisance.is_exact_coboundary(d0_alpha) is True

    # A non-zero constant vector is NOT a coboundary
    non_coboundary = (Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    assert nuisance.is_exact_coboundary(non_coboundary) is False


def test_optimal_repair_potential_and_strong_duality():
    """Check that d0 alpha* = omega - (ell omega) 1 and primal L1 distance matches dual value."""
    n = 5
    quotient = CalibrationQuotient(n)
    cochain = (Fraction(2), Fraction(-1), Fraction(4), Fraction(1), Fraction(-2))

    ell = quotient.mean_circulation(cochain)
    assert ell == Fraction(2 - 1 + 4 + 1 - 2, 5)  # 4/5

    potential = quotient.optimal_repair_potential(cochain)
    assert len(potential) == n
    assert potential[0] == Fraction(0)

    nuisance = NuisanceModel(n)
    d0_alpha = nuisance.coboundary(potential)

    # Verify (d0 alpha)_j = omega_j - ell
    for j in range(n):
        assert d0_alpha[j] == cochain[j] - ell

    # Verify residual is uniform and equals ell
    residual = tuple(c - da for c, da in zip(cochain, d0_alpha, strict=True))
    for r in residual:
        assert r == ell

    # Primal normalized L1 norm: (1/n) sum |ell| = |ell|
    primal_val = sum(abs(r) for r in residual) / Fraction(n)
    assert primal_val == abs(ell)

    # Dual pairing: <y, omega> where y_j = sgn(ell) / n
    dual_y = quotient.dual_witness(cochain)
    dual_val = sum(y * c for y, c in zip(dual_y, cochain, strict=True))
    assert dual_val == abs(ell)
    assert primal_val == dual_val  # Zero duality gap!


def test_calibration_invariance():
    """Circulation Phi(omega) is invariant under omega -> omega + d0 alpha for arbitrary potentials."""
    n = 7
    quotient = CalibrationQuotient(n)
    cochain = (Fraction(1), Fraction(2), Fraction(-3), Fraction(4), Fraction(0), Fraction(-1), Fraction(5))

    test_potentials = [
        [Fraction(0)] * n,
        [Fraction(1)] * n,
        [Fraction(j, 2) for j in range(n)],
        [Fraction(-3 * j + 1, 5) for j in range(n)],
    ]
    for pot in test_potentials:
        assert quotient.verify_calibration_invariance(cochain, pot) is True


def test_presentation_invariance():
    """Circulation Phi(omega) is invariant under cyclic relabelings and orientation reversals."""
    n = 5
    quotient = CalibrationQuotient(n)
    cochain = (Fraction(1), Fraction(3), Fraction(-2), Fraction(0), Fraction(4))

    for shift in range(n):
        assert quotient.verify_presentation_invariance(cochain, cyclic_shift=shift, reverse_orientation=False) is True
        assert quotient.verify_presentation_invariance(cochain, cyclic_shift=shift, reverse_orientation=True) is True


def test_coarse_graining_invariance():
    """Aggregating adjacent microscopic cells preserves total and intensive circulation."""
    n = 6
    quotient = CalibrationQuotient(n)
    cochain = (Fraction(1), Fraction(2), Fraction(-1), Fraction(3), Fraction(0), Fraction(2))

    partitions = [
        (2, 2, 2),
        (3, 3),
        (1, 2, 3),
        (4, 2),
        (1, 1, 1, 1, 1, 1),
    ]
    for part in partitions:
        assert quotient.verify_coarse_graining_invariance(cochain, part) is True


def test_evaluate_nuisance_invariance_contract():
    """Test the PROJECT.md interface contract evaluate_nuisance_invariance."""
    cochain = (Fraction(1), Fraction(-2), Fraction(3), Fraction(1), Fraction(5))
    nuisance = NuisanceModel(5)

    # Valid coboundary perturbation
    pot = (Fraction(1), Fraction(-1), Fraction(2), Fraction(0), Fraction(-3))
    valid_coboundary = nuisance.coboundary(pot)
    assert evaluate_nuisance_invariance(cochain, valid_coboundary) is True

    # Invalid perturbation that changes total circulation (not in im(d0))
    invalid_coboundary = (Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    assert evaluate_nuisance_invariance(cochain, invalid_coboundary) is False


def test_calibration_quotient_certificate_and_tampering():
    """Certificate generation, self-verification, and tamper detection."""
    quotient = CalibrationQuotient(5)
    cochain = (Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5))
    cert = quotient.certificate(cochain)
    assert cert.verify() is True
    assert cert.is_separated is True
    assert cert.duality_gap == Fraction(0)

    # Tamper with quotient norm
    tampered = CalibrationQuotientCertificate(
        n_sites=cert.n_sites,
        cochain=cert.cochain,
        mean_circulation=cert.mean_circulation,
        quotient_norm=Fraction(999),  # tampered
        optimal_repair_potential=cert.optimal_repair_potential,
        optimal_residual=cert.optimal_residual,
        dual_witness=cert.dual_witness,
        primal_value=cert.primal_value,
        dual_value=cert.dual_value,
        duality_gap=cert.duality_gap,
        is_separated=cert.is_separated,
    )
    assert tampered.verify() is False


def test_circulation_functional_properties():
    """Verify linearity of ell(omega) and triangle inequality / homogeneity of Phi(omega)."""
    n = 6
    quot = CalibrationQuotient(n)
    omega1 = (Fraction(1), Fraction(-2), Fraction(3), Fraction(0), Fraction(1), Fraction(-1))
    omega2 = (Fraction(2), Fraction(1), Fraction(-1), Fraction(4), Fraction(-2), Fraction(0))

    a = Fraction(3, 2)
    b = Fraction(-5, 3)

    # Linearity of ell:
    comb = tuple(a * w1 + b * w2 for w1, w2 in zip(omega1, omega2, strict=True))
    ell_comb = quot.mean_circulation(comb)
    expected_ell = a * quot.mean_circulation(omega1) + b * quot.mean_circulation(omega2)
    assert ell_comb == expected_ell

    # Triangle inequality of Phi: Phi(omega1 + omega2) <= Phi(omega1) + Phi(omega2)
    sum_omega = tuple(w1 + w2 for w1, w2 in zip(omega1, omega2, strict=True))
    assert quot.exact_circulation(sum_omega) <= quot.exact_circulation(omega1) + quot.exact_circulation(omega2)

    # Homogeneity: Phi(c * omega) = |c| * Phi(omega)
    c = Fraction(-7, 4)
    scaled = tuple(c * w for w in omega1)
    assert quot.exact_circulation(scaled) == abs(c) * quot.exact_circulation(omega1)


def test_exact_coboundary_has_identically_zero_quotient():
    """Any cochain in im(d0) has zero circulation and zero quotient distance."""
    n = 8
    nuisance = NuisanceModel(n)
    quot = CalibrationQuotient(n)

    potentials = [
        [Fraction(k * k, 7) for k in range(n)],
        [Fraction(10 - 2 * k, 3) for k in range(n)],
    ]
    for pot in potentials:
        coboundary = nuisance.coboundary(pot)
        assert quot.mean_circulation(coboundary) == Fraction(0)
        assert quot.exact_circulation(coboundary) == Fraction(0)
        assert quot.quotient_distance(coboundary) == Fraction(0)
        cert = quot.certificate(coboundary)
        assert cert.is_separated is False
        assert cert.verify() is True


def test_large_cycle_and_cohomological_projection():
    """Test decomposition omega = [omega]*1 + d0 alpha* on a 20-qubit cycle."""
    n = 20
    quot = CalibrationQuotient(n)
    cochain = tuple(Fraction(k % 5 - 2, 3) for k in range(n))

    ell, coboundary = quot.cohomological_projection(cochain)
    assert isinstance(ell, Fraction)
    assert len(coboundary) == n

    # Check sum(coboundary) == 0
    assert sum(coboundary) == Fraction(0)

    # Check cochain == ell * 1 + coboundary
    for j in range(n):
        assert cochain[j] == ell + coboundary[j]


def test_input_validation_and_error_paths():
    """Verify fail-closed error handling on invalid dimension and types."""
    with pytest.raises(ValueError, match="at least 3 sites"):
        CalibrationQuotient(2)

    quot = CalibrationQuotient(4)
    with pytest.raises(ValueError, match="Cochain length"):
        quot.mean_circulation([1, 2, 3])  # 3 != 4

    nuisance = NuisanceModel(4)
    with pytest.raises(ValueError, match="Potential length"):
        nuisance.coboundary([1, 2])

    with pytest.raises(ValueError, match="cochain length"):
        evaluate_nuisance_invariance([1, 2, 3, 4], [1, 2, 3])

    meas = OperationalMeasurementSet(4)
    with pytest.raises(ValueError, match="mu_K length"):
        meas.construct_cochain_from_moments([1, 2], [1, 2, 3, 4], [1, 2, 3, 4])



def test_multiplicative_gain_drift_and_error_budget():
    """Verify Review Finding 6 multiplicative gain response omega' = g^3 omega and error budget.

    |Phi(omega') - Phi(omega)| <= |g^3 - 1| * Phi(omega).
    """
    n = 5
    quotient = CalibrationQuotient(n)
    # 5-qubit graph state cochain omega = (-1, -1, -1, -1, -1), Phi(omega) = 1
    cochain = tuple(Fraction(-1) for _ in range(n))
    phi_nominal = quotient.exact_circulation(cochain)
    assert phi_nominal == Fraction(1)

    # Test across various gain factors g = 1 + delta
    gains = [Fraction(99, 100), Fraction(101, 100), Fraction(95, 100), Fraction(105, 100), Fraction(11, 10)]
    for g in gains:
        res = quotient.verify_multiplicative_gain_budget(cochain, g)
        assert res["status"] == "pass"
        assert res["is_within_budget"] is True
        g3 = g * g * g
        expected_drift = abs(g3 - Fraction(1)) * phi_nominal
        assert res["actual_drift"] == expected_drift
        assert res["error_budget"] == expected_drift
