"""Counterexamples and input-domain regressions from the 2026-10-02 review."""

import numpy as np
import pytest

from caqd.adaptive import QuantumCluster, _cluster_residual_rates, _merge_clusters, evolve_adaptive
from caqd.bounds import CertificateTracker, compute_cumulative_bounds, evaluate_bound, verify_bound_honesty
from caqd.dynamics import SimulationResult, _mean_field_derivatives, evolve_exact, evolve_mean_field
from caqd.residuals import compute_edge_residual, compute_local_residuals, dual_witness_schatten1, retraction_tangent_projector
from caqd.spin_chains import (
    I2, SIGMA_X, SIGMA_Z, LocalTerm, SpinChainModel, TFIMChain,
    all_up_state, center_correlation, partial_trace, polarized_x_state, trace_norm,
)


def run_solver(solver, times, rho=None, **kwargs):
    model = TFIMChain(2)
    rho = all_up_state(2) if rho is None else rho
    if solver is evolve_adaptive:
        return solver(model, rho, t_span=times, **kwargs)
    return solver(model, rho, times, **kwargs)


def test_residual_is_sampled_at_recorded_time():
    model = TFIMChain(2)
    obs = {"ZZ": center_correlation(2)}
    result = evolve_adaptive(model, all_up_state(2), obs, [0, 0.2], max_bond=1)
    recomputed = sum(compute_local_residuals(model, result.states[-1]).values())
    assert recomputed > 0.29
    assert result.total_rates[-1] == pytest.approx(recomputed, abs=1e-13)
    assert compute_cumulative_bounds(result, obs["ZZ"])[-1] > 0.029
    reference = evolve_exact(model, all_up_state(2), [0, 0.2], obs)
    assert abs(reference.expectation("ZZ")[-1] - result.expectation("ZZ")[-1]) > 1e-5
    assert result.metadata["certificate_status"] == "HEURISTIC_UNCERTIFIED"


def test_full_cluster_residual_detects_hidden_boundary_correlation():
    bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
    rho_ab = np.outer(bell, bell)
    model = SpinChainModel(3)
    h = np.kron(SIGMA_Z, SIGMA_Z)
    model.terms.append(LocalTerm("2-local", (1, 2), h, np.kron(I2, h)))
    clusters = [QuantumCluster([0, 1], rho_ab), QuantumCluster([2], I2 / 2)]
    _, marginal_rate = compute_edge_residual(I2 / 2, I2 / 2, h)
    assert marginal_rate == 0
    assert _cluster_residual_rates(model, clusters)[(1, 2)] == pytest.approx(2, abs=1e-12)
    assert _cluster_residual_rates(model, clusters)[(0, 1)] == 0


def test_merge_preserves_past_interval_estimate():
    result = run_solver(evolve_adaptive, [0, 0.2], max_bond=2, refine_threshold=0)
    assert result.metadata["final_clusters"] == [[0, 1]]
    assert result.total_rates[-1] == 0
    incoming = result.metadata["pre_refinement_total_rates"][-1]
    assert incoming > 0.29
    assert compute_cumulative_bounds(result, 1)[-1] == pytest.approx(0.1 * incoming)
    assert evaluate_bound(result.total_rates, 1, result.times) == 0


def test_blocked_edge_does_not_prevent_other_merge():
    result = evolve_adaptive(TFIMChain(4), polarized_x_state(4), t_span=[0, 0.01],
                             max_bond=2, tol=0, refine_threshold=0)
    assert sorted(result.metadata["final_clusters"]) == [[0, 1], [2, 3]]


def test_cluster_updates_preserve_reflection_symmetry():
    result = evolve_adaptive(TFIMChain(3), all_up_state(3), t_span=[0, 0.1],
                             max_bond=1, tol=100, refine_threshold=100)
    np.testing.assert_allclose(partial_trace(result.states[-1], [0], 3),
                               partial_trace(result.states[-1], [2], 3), atol=1e-13)


@pytest.mark.parametrize("solver", [evolve_exact, evolve_mean_field, evolve_adaptive])
def test_translated_time_origin(solver):
    base = run_solver(solver, [0, 0.1])
    shifted = run_solver(solver, [2, 2.1])
    np.testing.assert_allclose(shifted.states[0], all_up_state(2), atol=1e-13)
    np.testing.assert_allclose(shifted.states[-1], base.states[-1], atol=1e-12)


@pytest.mark.parametrize("solver", [evolve_exact, evolve_mean_field, evolve_adaptive])
@pytest.mark.parametrize("times", [[], [0, np.nan], [0, np.inf], [1, 0], [[0, 1]]])
def test_invalid_sampling_grid(solver, times):
    with pytest.raises(ValueError):
        run_solver(solver, times)


@pytest.mark.parametrize("solver", [evolve_exact, evolve_mean_field, evolve_adaptive])
@pytest.mark.parametrize("rho", [
    np.zeros((4, 4)), np.diag([1.1, -0.1, 0, 0]),
    np.array([[1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    np.full((4, 4), np.nan),
])
def test_invalid_initial_density_matrix(solver, rho):
    with pytest.raises(ValueError):
        run_solver(solver, [0, 0.1], rho)


@pytest.mark.parametrize("max_bond", [0, 1.5, True])
def test_invalid_cluster_ceiling(max_bond):
    with pytest.raises(ValueError):
        run_solver(evolve_adaptive, [0], max_bond=max_bond)


@pytest.mark.parametrize("kwargs", [{"tol": -1}, {"tol": np.nan}, {"refine_threshold": np.inf}])
def test_invalid_refinement_parameters(kwargs):
    with pytest.raises(ValueError):
        run_solver(evolve_adaptive, [0], **kwargs)


def test_cluster_site_order_preserves_physical_state():
    up, down = np.diag([1, 0]), np.diag([0, 1])
    cluster = QuantumCluster([1, 0], np.kron(up, down))
    np.testing.assert_array_equal(cluster.single_site_marginal(0), down)
    np.testing.assert_array_equal(cluster.single_site_marginal(1), up)
    with pytest.raises(ValueError):
        _merge_clusters(cluster, QuantumCluster([0], up))


@pytest.mark.parametrize("sites", [[], [0, 0], [-1], [True], [0.5]])
def test_invalid_cluster_sites(sites):
    with pytest.raises(ValueError):
        QuantumCluster(sites, I2 / 2)


@pytest.mark.parametrize("keep", [[0, 0], [-1], [2], [True]])
def test_invalid_partial_trace_indices(keep):
    with pytest.raises(ValueError):
        partial_trace(all_up_state(2), keep, 2)


def test_partial_trace_dimension_mismatch():
    with pytest.raises(ValueError):
        partial_trace(I2 / 2, [0], 2)


def test_periodic_two_site_derivative_uses_declared_bonds_once():
    model = TFIMChain(2, periodic=True)
    marginals = [(I2 + 0.5 * SIGMA_X) / 2, (I2 + 0.4 * SIGMA_Z) / 2]
    rho = np.kron(*marginals)
    global_derivative = -1j * (model.H @ rho - rho @ model.H)
    for site, derivative in enumerate(_mean_field_derivatives(marginals, model)):
        np.testing.assert_allclose(derivative, partial_trace(global_derivative, [site], 2), atol=1e-13)
    assert len(model.get_terms_for_edge((0, 1))) == 1
    assert len(model.get_terms_for_edge((1, 0))) == 1


def test_rectangular_norm_witness_and_traceful_scaling_direction():
    q = np.array([[1, 2j, 0], [3, 0, 4]], dtype=complex)
    w, gap = dual_witness_schatten1(q)
    assert w.shape == q.shape
    assert gap < 1e-12
    assert np.real(np.trace(w.conj().T @ q)) == pytest.approx(trace_norm(q))
    rho = np.kron(I2 / 2, I2 / 2)
    np.testing.assert_allclose(retraction_tangent_projector(I2 / 2, I2 / 2, rho), rho)
    # Ambient scaling is not a trace-zero normalized density tangent.
    assert np.trace(rho) == pytest.approx(1)


def test_marginal_projector_is_not_a_trace_norm_best_approximation():
    a, b = np.diag([0.8, 0.2]), np.diag([0.7, 0.3])
    z = np.diag([1, 0, 0, -1])
    projected = retraction_tangent_projector(a, b, z)
    residual = z - projected
    tangent = np.kron(np.diag([1, -1]), b)
    witness, gap = dual_witness_schatten1(residual)
    assert gap < 1e-12
    assert abs(np.trace(witness.conj().T @ tangent)) > 0.7
    assert trace_norm(z - (projected - 0.1 * tangent)) < trace_norm(residual)


@pytest.mark.parametrize("rates,norm,times", [
    ([-0.1], 1, [0]), ([np.nan], 1, [0]), ([[0]], 1, [0]),
    ([0], -1, [0]), ([0], np.inf, [0]), ([0, 0], 1, [0]),
    ([0, 0], 1, [1, 0]), ([0, 0], 1, [0, np.inf]),
    ({(0, 1): [0], (1, 2): [0, 0]}, 1, [0]),
])
def test_invalid_estimate_inputs(rates, norm, times):
    with pytest.raises(ValueError):
        evaluate_bound(rates, norm, times)


def result_with(times, rates, values=None, metadata=None):
    return SimulationResult(np.array(times), [], {"Z": np.array(values if values is not None else times)},
                            {}, np.array(rates), "fixture", metadata or {})


def test_comparisons_reject_grid_and_observable_broadcasting():
    a = result_with([0, 1], [0, 0])
    b = result_with([0, 2], [0, 0])
    with pytest.raises(ValueError, match="identical time grids"):
        verify_bound_honesty(a, b, {"Z": SIGMA_Z})
    b.times = a.times.copy()
    b.observables["Z"] = np.array([0])
    with pytest.raises(ValueError, match="observable histories"):
        verify_bound_honesty(a, b, {"Z": SIGMA_Z})
    b.observables["Z"] = np.array([0, np.nan])
    with pytest.raises(ValueError):
        verify_bound_honesty(a, b, {"Z": SIGMA_Z})


@pytest.mark.parametrize("integral", [[0, -1], [0, np.nan], [1, 1], [0], [0, 2, 1]])
def test_invalid_stored_interval_estimates(integral):
    result = result_with([0, 1, 2], [0, 0, 0], metadata={"cumulative_residual_estimates": integral})
    with pytest.raises(ValueError):
        compute_cumulative_bounds(result, 1)


def test_tracker_refuses_invalid_steps_without_mutating_history():
    tracker = CertificateTracker(1)
    tracker.step(1, 2)
    for time, rate in [(0, 2), (np.nan, 2), (2, -1), (2, {(0, 1): -1, (1, 2): 2})]:
        with pytest.raises(ValueError):
            tracker.step(time, rate)
        assert (tracker.prev_time, tracker.prev_rate, tracker.cumulative_bound) == (1, 2, 0)
    with pytest.raises(ValueError):
        tracker.predict_horizon_error(np.inf)
    # Same-time event changes the outgoing rate without adding area.
    assert tracker.step(1, 3) == 0
    assert tracker.step(2, 3) == 3


def test_empty_edge_inventory_is_zero_and_empty_comparison_is_defined():
    assert evaluate_bound({}, 1, [0, 1]) == 0
    model = SpinChainModel(2)
    assert compute_local_residuals(model, all_up_state(2)) == {(0, 1): 0}
    assert _cluster_residual_rates(model, [QuantumCluster([0], I2 / 2), QuantumCluster([1], I2 / 2)]) == {(0, 1): 0}
    result = result_with([], [])
    assert verify_bound_honesty(result, result, {"Z": SIGMA_Z})["Z"].min_margin == 0
