"""Tests for finite-horizon observation trade-offs and Tran et al. benchmarks (PO-000 §5.17, §7.8).

Validates:
- Combinatorial partition constants a_k, b_k and Steiner onset orders tau_G(S)
- Finite-horizon observation trade-off curve, optimal sampling time t_opt, and shot budget
- Difference-set state family generators, tracelessness, Hermiticity, and observation conditioning
- Comparative benchmarks demonstrating where exact algebraic onset and commutator cancellation
  outperform Tran et al.'s operator-spreading bounds
- Adversarial inputs, domain validations, and parameter boundary behaviors

AuthorityEffect: None.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from observation_tradeoffs import (
    DifferenceSetStateFamily,
    benchmark_against_tran_multipartite,
    cumulant_partition_constants,
    evaluate_difference_set_conditioning,
    evaluate_observation_tradeoff,
    generate_difference_set_family,
    six_variable_cumulant_counterexample,
    LeadingCoefficientEstimation,
    TrajectoryPrediction,
    steiner_tree_onset_order,
    truncation_bound_constant,
)

# ===========================================================================
# 1. Combinatorial Constants & Steiner Tree Onset Tests
# ===========================================================================


def test_cumulant_partition_constants_exact_values():
    """Verify exact combinatorial constants a_k and b_k for small support sizes (Review Finding 4)."""
    # k = 1: a_1 = 1, b_1 = 1
    a1, b1 = cumulant_partition_constants(1)
    assert a1 == 1
    assert b1 == 1

    # k = 2: a_2 = 2, b_2 = 1! + 2! = 3
    a2, b2 = cumulant_partition_constants(2)
    assert a2 == 2
    assert b2 == 3

    # k = 3: a_3 = 6, b_3 = 1! + 3*2! + 3! = 13
    a3, b3 = cumulant_partition_constants(3)
    assert a3 == 6
    assert b3 == 13

    # k = 4: a_4 = 26, b_4 = 75
    a4, b4 = cumulant_partition_constants(4)
    assert a4 == 26
    assert b4 == 75

    # k = 5: a_5 = 150, b_5 = 541
    a5, b5 = cumulant_partition_constants(5)
    assert a5 == 150
    assert b5 == 541

    # k = 6: a_6 = 1082, b_6 = 4683
    a6, b6 = cumulant_partition_constants(6)
    assert a6 == 1082
    assert b6 == 4683


@pytest.mark.parametrize("invalid_k", [0, -1, -5])
def test_cumulant_partition_constants_rejects_nonpositive_k(invalid_k):
    with pytest.raises(ValueError, match="at least 1"):
        cumulant_partition_constants(invalid_k)


@pytest.mark.parametrize("invalid_type", [1.5, "2", True, None])
def test_cumulant_partition_constants_rejects_non_integer_type(invalid_type):
    with pytest.raises((TypeError, ValueError)):
        cumulant_partition_constants(invalid_type)  # type: ignore


def test_truncation_bound_constant_exact_eval():
    """Verify B_{k,m} = a_k * comb(k+m, m+1) * (2g)^{m+1}."""
    # k=2, m=1, g=1.0: a_2=2, comb(3, 2)=3, (2*1)^2 = 4 => B = 2 * 3 * 4 = 24
    b_21 = truncation_bound_constant(2, 1, 1.0)
    assert math.isclose(b_21, 24.0, rel_tol=1e-12)

    # k=1, m=1, g=1.0: a_1=1, comb(2, 2)=1, (2*1)^2 = 4 => B = 4
    b_11 = truncation_bound_constant(1, 1, 1.0)
    assert math.isclose(b_11, 4.0, rel_tol=1e-12)

    # Scaling with g: (2g)^{m+1} scales as g^2 for m=1
    b_21_half = truncation_bound_constant(2, 1, 0.5)
    assert math.isclose(b_21_half, 2 * 3 * (1.0**2), rel_tol=1e-12)


@pytest.mark.parametrize(
    "k, m, g, err_type",
    [
        (0, 1, 1.0, ValueError),
        (2, 0, 1.0, ValueError),
        (2, 1, 0.0, ValueError),
        (2, 1, -1.0, ValueError),
        (True, 1, 1.0, ValueError),
    ],
)
def test_truncation_bound_constant_invalid_inputs(k, m, g, err_type):
    with pytest.raises(err_type):
        truncation_bound_constant(k, m, g)


def test_steiner_tree_onset_order_1d_chain():
    """Verify Steiner onset order on 1D chains equals span max(S) - min(S)."""
    assert steiner_tree_onset_order(None, [0]) == 1
    assert steiner_tree_onset_order(None, [0, 1]) == 1
    assert steiner_tree_onset_order(None, [0, 3]) == 3
    assert steiner_tree_onset_order(None, [1, 2, 5]) == 4
    assert steiner_tree_onset_order(None, [5, 1, 3]) == 4


def test_steiner_tree_onset_order_explicit_edges():
    """Verify Steiner onset on explicit graph geometries."""
    # Path graph 0 - 1 - 2 - 3
    edges = [(0, 1), (1, 2), (2, 3)]
    assert steiner_tree_onset_order(edges, [0, 3]) == 3
    assert steiner_tree_onset_order(edges, [1, 3]) == 2

    # Star graph: center 0, leaves 1, 2, 3
    star_edges = [(0, 1), (0, 2), (0, 3)]
    # Terminals 1 and 2 require path 1-0-2 (2 edges)
    assert steiner_tree_onset_order(star_edges, [1, 2]) == 2
    # Terminals 1, 2, 3 require star center (3 edges)
    assert steiner_tree_onset_order(star_edges, [1, 2, 3]) == 3


def test_steiner_tree_onset_order_empty_support_raises():
    with pytest.raises(ValueError, match="at least one site"):
        steiner_tree_onset_order(None, [])


# ===========================================================================
# 2. Finite-Horizon Observation Trade-off Formulation Tests (F8 / R3)
# ===========================================================================


def test_evaluate_observation_tradeoff_keys_and_types():
    """Verify that evaluate_observation_tradeoff returns complete typed results."""
    res = evaluate_observation_tradeoff(
        support_size=2,
        num_settings=4,
        shot_noise=0.01,
        krylov_order=2,
        conditioning=1.5,
        coupling_g=1.0,
        confidence_delta=0.05,
        time_horizon=0.2,
    )
    assert isinstance(res, dict)
    assert res["support_size"] == 2
    assert res["num_settings"] == 4
    assert res["krylov_order"] == 2
    assert res["conditioning"] == 1.5
    assert res["coupling_g"] == 1.0
    assert res["t_optimal"] > 0.0
    assert res["min_prediction_error"] > 0.0
    assert res["prediction_error_at_T"] > 0.0
    assert res["required_shots"] > 0
    assert res["tradeoff_holds"] is True
    assert res["authority_effect"] == "None"
    assert "tradeoff_curve" in res
    curve = res["tradeoff_curve"]
    assert len(curve["times"]) == 50
    assert len(curve["errors"]) == 50


def test_evaluate_observation_tradeoff_convex_minimum():
    """Verify that the error curve is convex and strictly minimized at t_optimal."""
    res = evaluate_observation_tradeoff(
        support_size=2,
        num_settings=3,
        shot_noise=0.05,
        krylov_order=2,
        conditioning=2.0,
    )
    t_opt = res["t_optimal"]
    min_err = res["min_prediction_error"]

    curve = res["tradeoff_curve"]
    times = curve["times"]
    errors = curve["errors"]
    assert len(times) == len(errors)

    # At all sampled points, error must be >= min_err (within float precision)
    for err in errors:
        assert err >= min_err - 1e-12

    # Check analytical derivative at t_opt: dE/dt = B_{k,m} - m*kappa*b_k*eps / t^(m+1) == 0
    k = res["support_size"]
    assert k == 2
    m = res["krylov_order"]
    b_km = res["B_km"]
    kappa = res["conditioning"]
    b_k = res["b_k"]
    eps = res["shot_noise"]
    derivative = b_km - m * kappa * b_k * eps * (t_opt ** (-(m + 1)))
    assert math.isclose(derivative, 0.0, abs_tol=1e-10)


def test_evaluate_observation_tradeoff_shot_noise_scaling():
    """Verify scaling: smaller shot noise decreases minimal error and shifts t_opt earlier."""
    res_coarse = evaluate_observation_tradeoff(
        support_size=2, num_settings=4, shot_noise=0.1, krylov_order=2, conditioning=1.0
    )
    res_fine = evaluate_observation_tradeoff(
        support_size=2, num_settings=4, shot_noise=0.01, krylov_order=2, conditioning=1.0
    )

    # Finer shot noise reduces minimal error
    assert res_fine["min_prediction_error"] < res_coarse["min_prediction_error"]
    # Finer shot noise allows observing earlier without being overwhelmed by noise
    assert res_fine["t_optimal"] < res_coarse["t_optimal"]
    # Required shots is much larger for fine noise
    assert res_fine["required_shots"] > res_coarse["required_shots"]


def test_evaluate_observation_tradeoff_conditioning_penalty():
    """Verify that computational ill-conditioning kappa penalizes prediction error."""
    res_well = evaluate_observation_tradeoff(
        support_size=2, num_settings=4, shot_noise=0.02, krylov_order=2, conditioning=1.0
    )
    res_ill = evaluate_observation_tradeoff(
        support_size=2, num_settings=4, shot_noise=0.02, krylov_order=2, conditioning=10.0
    )

    assert res_ill["min_prediction_error"] > res_well["min_prediction_error"]
    assert res_ill["t_optimal"] > res_well["t_optimal"]


@pytest.mark.parametrize(
    "kwargs, err_match",
    [
        (dict(support_size=0, num_settings=1, shot_noise=0.1, krylov_order=1, conditioning=1.0), "support_size"),
        (dict(support_size=1, num_settings=0, shot_noise=0.1, krylov_order=1, conditioning=1.0), "num_settings"),
        (dict(support_size=1, num_settings=1, shot_noise=-0.1, krylov_order=1, conditioning=1.0), "shot_noise"),
        (dict(support_size=1, num_settings=1, shot_noise=0.1, krylov_order=0, conditioning=1.0), "krylov_order"),
        (dict(support_size=1, num_settings=1, shot_noise=0.1, krylov_order=1, conditioning=0.5), "conditioning"),
        (dict(support_size=1, num_settings=1, shot_noise=0.1, krylov_order=1, conditioning=1.0, coupling_g=-1.0), "coupling_g"),
        (dict(support_size=1, num_settings=1, shot_noise=0.1, krylov_order=1, conditioning=1.0, confidence_delta=1.5), "confidence_delta"),
    ],
)
def test_evaluate_observation_tradeoff_validations(kwargs, err_match):
    with pytest.raises(ValueError, match=err_match):
        evaluate_observation_tradeoff(**kwargs)


# ===========================================================================
# 3. Difference-Set State Family Implementation & Conditioning Tests (F9 / R3)
# ===========================================================================


@pytest.mark.parametrize("family_type", ["product", "perturbed_graph", "orthogonal"])
def test_difference_set_state_family_invariants(family_type):
    """Verify that generated Delta is strictly traceless, Hermitian, and non-trivial."""
    fam = DifferenceSetStateFamily(num_qubits=3, family_type=family_type)  # type: ignore
    rho_1, rho_2, delta = fam.generate_state_pair(support=[0, 1], theta=0.4)

    # 1. Density matrix properties
    assert math.isclose(float(np.trace(rho_1).real), 1.0, abs_tol=1e-12)
    assert math.isclose(float(np.trace(rho_2).real), 1.0, abs_tol=1e-12)
    assert np.allclose(rho_1, rho_1.conj().T, atol=1e-12)
    assert np.allclose(rho_2, rho_2.conj().T, atol=1e-12)
    evals_1 = np.linalg.eigvalsh(rho_1)
    evals_2 = np.linalg.eigvalsh(rho_2)
    assert np.all(evals_1 >= -1e-12)
    assert np.all(evals_2 >= -1e-12)

    # 2. Difference state invariants
    trace_delta = float(np.trace(delta).real)
    assert math.isclose(trace_delta, 0.0, abs_tol=1e-12)
    assert np.allclose(delta, delta.conj().T, atol=1e-12)

    # 3. Non-trivial distance
    trace_dist = 0.5 * float(np.sum(np.linalg.svd(delta, compute_uv=False)))
    assert 0.0 < trace_dist <= 1.0


def test_difference_set_state_family_environmental_invariance():
    """Verify that sites outside support have identical reduced marginals for product family."""
    rho_1, rho_2, delta = generate_difference_set_family(
        num_qubits=3, support=[1], family_type="product", theta=0.6
    )
    # Trace out site 1 (support)
    # Dim 8 = 2 x 2 x 2. Marginals on site 0 and site 2 should be identical.
    tensor_1 = rho_1.reshape(2, 2, 2, 2, 2, 2)
    tensor_2 = rho_2.reshape(2, 2, 2, 2, 2, 2)
    red_02_1 = np.trace(tensor_1, axis1=1, axis2=4)  # trace out site 1
    red_02_2 = np.trace(tensor_2, axis1=1, axis2=4)
    assert np.allclose(red_02_1, red_02_2, atol=1e-12)


def test_evaluate_difference_set_conditioning_certification():
    """Verify observation conditioning evaluation on difference states."""
    _, _, delta = generate_difference_set_family(
        num_qubits=2, support=[0], family_type="product", theta=0.5
    )

    # Observables: Pauli basis on 2 qubits
    sx = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sz = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    id2 = np.eye(2, dtype=np.complex128)

    obs_list = [np.kron(sz, id2), np.kron(sx, id2), np.kron(id2, sz)]
    cond_report = evaluate_difference_set_conditioning(delta, obs_list)

    assert cond_report["is_valid_difference_state"] is True
    assert cond_report["trace_abs"] < 1e-12
    assert cond_report["hermitian_defect"] < 1e-12
    assert 1.0 <= cond_report["sensing_conditioning"] < float("inf")
    assert cond_report["num_observables"] == 3


def test_krylov_observability_conditioning():
    """Verify Krylov observability matrix and conditioning computation."""
    fam = DifferenceSetStateFamily(num_qubits=2)
    # Simple transverse-field Ising Hamiltonian H = Z Z + X I
    sz = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    sx = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    id2 = np.eye(2, dtype=np.complex128)

    hamiltonian = np.kron(sz, sz) + 0.5 * np.kron(sx, id2)
    observable = np.kron(sz, id2)

    # Compute Krylov chain for order m=3
    obs_mat = fam.compute_krylov_observability_matrix(hamiltonian, observable, order=3)
    assert obs_mat.shape == (3, 16)

    kappa = fam.compute_krylov_conditioning(hamiltonian, observable, order=3)
    assert isinstance(kappa, float)
    assert kappa >= 1.0
    assert math.isfinite(kappa)


# ===========================================================================
# 4. Comparative Benchmark vs Tran et al. Tests (F10 / R3)
# ===========================================================================


def test_benchmark_against_tran_multipartite_structure():
    """Verify that the benchmark returns all required fields and valid curves."""
    res = benchmark_against_tran_multipartite(lattice=4, time_horizon=0.3, num_time_points=25)
    assert isinstance(res, dict)
    assert res["lattice_size"] == 4
    assert res["steiner_onset_order"] >= 2
    assert res["exact_commutator_cancels"] is True
    assert "algebraic_cancellation_strata" in res
    assert "po000_curve" in res
    assert "tran_curve" in res
    assert len(res["time_grid"]) == 25
    assert len(res["po000_curve"]) == 25
    assert len(res["tran_curve"]) == 25


def test_benchmark_against_tran_short_time_outperformance():
    """Directly test that PO-000 algebraic onset O(t^m) outperforms Tran O(t) at short times."""
    # For m=3 (4 qubits endpoints), as t -> 0, t^3 << t
    res = benchmark_against_tran_multipartite(
        lattice=4, time_horizon=0.2, steiner_distance=3, num_time_points=40
    )
    t_early = res["short_time_sample_point"]
    assert t_early > 0.0

    # Early time ratio Tran / PO-000 must be strictly greater than 1
    early_ratio = res["outperformance_ratio_at_short_time"]
    assert early_ratio > 1.0, f"Expected Tran to be looser than PO-000 at early time, got {early_ratio}"

    # Verify that the PO-000 bound value at t_early is orders of magnitude smaller
    curve_po000 = res["po000_curve"]
    curve_tran = res["tran_curve"]
    early_idx = max(1, 40 // 10)
    assert curve_po000[early_idx] < curve_tran[early_idx]


def test_benchmark_algebraic_cancellation_strata():
    """Verify that exact commutator cancellation yields zero where Tran bound is positive."""
    res = benchmark_against_tran_multipartite(lattice=4, time_horizon=0.5)
    strata = res["algebraic_cancellation_strata"]

    # On the cancellation variety, true defect rate is certified 0
    assert strata["true_defect_rate"] == 0.0
    assert strata["po000_certified_vanishing"] is True
    # Tran operator-norm bound gives positive spurious growth
    assert strata["tran_bound_spurious_positive"] > 0.0


def test_benchmark_against_tran_spin_chain_model():
    """Verify that benchmark_against_tran_multipartite accepts a SpinChainModel object."""
    from krylov_scaling_benchmark import SpinChainModel

    model = SpinChainModel(num_qubits=4, j_zz=1.0, hx=0.5)
    res = benchmark_against_tran_multipartite(lattice=model, time_horizon=0.2)
    assert res["lattice_size"] == 4
    assert res["steiner_onset_order"] == 3
    assert res["outperformance_ratio_at_short_time"] > 1.0


@pytest.mark.parametrize("invalid_t", [0.0, -0.5, -1.0, float("nan"), float("inf")])
def test_benchmark_against_tran_invalid_time_horizon(invalid_t):
    with pytest.raises(ValueError, match="strictly positive finite float"):
        benchmark_against_tran_multipartite(lattice=4, time_horizon=invalid_t)


def test_analytical_closed_form_error_matches_evaluation():
    """Verify exact algebraic formula:
    E_pred*(t_opt) = (m+1) * (B_{k,m} / m)^(m/(m+1)) * (kappa * b_k * eps)^(1/(m+1)).
    """
    k, m, eps, kappa, g = 3, 2, 0.03, 1.8, 1.2
    res = evaluate_observation_tradeoff(
        support_size=k,
        num_settings=5,
        shot_noise=eps,
        krylov_order=m,
        conditioning=kappa,
        coupling_g=g,
    )

    a_k, b_k = cumulant_partition_constants(k)
    b_km = truncation_bound_constant(k, m, g)
    closed_form_min = (m + 1) * ((b_km / m) ** (m / (m + 1))) * ((kappa * b_k * eps) ** (1 / (m + 1)))

    assert math.isclose(res["min_prediction_error"], closed_form_min, rel_tol=1e-12)


def test_hoeffding_shot_budget_scaling():
    """Verify that required shots scale inversely quadratically with shot noise epsilon."""
    res_1 = evaluate_observation_tradeoff(2, 4, 0.1, 2, 1.0)
    res_2 = evaluate_observation_tradeoff(2, 4, 0.05, 2, 1.0)
    # Halving epsilon should roughly quadruple required shots: (0.1 / 0.05)^2 = 4
    ratio = res_2["required_shots"] / res_1["required_shots"]
    assert 3.8 <= ratio <= 4.2


def test_difference_set_identity_observable_expectation_zero():
    """Verify that identity observable expectation Tr(I * Delta) is exactly 0."""
    fam = DifferenceSetStateFamily(num_qubits=2)
    _, _, delta = fam.generate_state_pair(support=[0])
    identity = np.eye(4, dtype=np.complex128)
    exp_val = float(np.trace(identity @ delta).real)
    assert math.isclose(exp_val, 0.0, abs_tol=1e-12)



def test_six_variable_cumulant_counterexample():
    """Verify Review Finding 4 six-variable cumulant counterexample.

    Demonstrates that at epsilon = 0.01:
    Delta kappa_6 = 76(0.01) - 90(0.01)^2 + 30(0.01)^3 = 0.75103 > 0.63.
    The naive subset bound (2^6 - 1)*epsilon = 63 * 0.01 = 0.63 strictly underestimates,
    while monograph bound b_6 * epsilon = 4683 * 0.01 = 46.83 holds.
    """
    res = six_variable_cumulant_counterexample(0.01)
    assert res["status"] == "pass"
    assert math.isclose(res["exact_cumulant_error"], 0.75103, abs_tol=1e-9)
    assert math.isclose(res["naive_bound_2k_minus_1"], 0.63, abs_tol=1e-9)
    assert res["naive_bound_underestimates"] is True
    assert res["monograph_bound_holds"] is True


def test_estimation_vs_prediction_dataclasses():
    """Verify distinct semantics of LeadingCoefficientEstimation and TrajectoryPrediction."""
    est = LeadingCoefficientEstimation(
        sampling_time=0.05,
        coefficient_estimate=1.2,
        error_bound=0.08,
        truncation_term=0.03,
        noise_term=0.05,
    )
    assert est.sampling_time == 0.05

    pred = TrajectoryPrediction(
        target_horizon=0.25,
        predicted_value=0.45,
        prediction_error_bound=0.12,
        leading_term_error=0.05,
        higher_order_truncation=0.07,
    )
    assert pred.target_horizon == 0.25
