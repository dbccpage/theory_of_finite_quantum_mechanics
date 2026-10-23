"""Regressions from the review of PR #673 at 94239354."""

from pathlib import Path

import numpy as np
import pytest
import tomllib
from krylov_scaling_benchmark import (
    SpinChainModel,
    build_initial_product_state,
    build_sparse_hamiltonian,
    compute_bipartite_linear_entropy,
    compute_cumulative_duhamel_bound,
    compute_cumulative_duhamel_estimate,
    compute_entropy_expansion,
    compute_higher_order_expansion_and_timescale,
    compute_trace_distance_pure,
    evolve_exact_krylov,
    run_single_scaling_benchmark,
    solve_mean_field_trajectory,
)


@pytest.mark.parametrize("steps", [2, 5])
def test_coarse_oscillatory_mesh_does_not_underestimate_error(steps):
    model = SpinChainModel(num_qubits=2, j_zz=1.0, hx=100.0)
    sites = [np.array([1.0, 0.0], dtype=complex)] * 2
    times = np.linspace(0.0, np.pi / 50.0, steps)
    psi0, sites = build_initial_product_state(sites)
    exact = evolve_exact_krylov(build_sparse_hamiltonian(model), psi0, times)
    mf = solve_mean_field_trajectory(model, sites, times)
    bounds = compute_cumulative_duhamel_bound(model, mf, times)
    errors = [compute_trace_distance_pure(p, np.kron(*u)) for p, u in zip(exact, mf)]
    estimates = compute_cumulative_duhamel_estimate(model, mf, times)
    assert estimates[-1] < errors[-1] / 100
    assert errors[-1] > 0.05
    assert np.all(bounds + 1e-7 >= errors)


@pytest.mark.parametrize("coupling", [0.01, 1.0, 100.0])
def test_xx_product_state_has_known_taylor_coefficients_at_any_scale(coupling):
    model = SpinChainModel(num_qubits=2, j_xx=coupling, j_zz=0.0)
    sites = [np.array([1.0, 0.0], dtype=complex)] * 2
    c2, c3, c4, tau = compute_higher_order_expansion_and_timescale(model, sites, 0)
    assert c2 == pytest.approx(2 * coupling**2, rel=1e-10)
    assert c3 == pytest.approx(0.0, abs=1e-10)
    assert c4 == pytest.approx(-8 * coupling**4 / 3, rel=1e-10)
    assert tau == pytest.approx(np.sqrt(3) / (2 * abs(coupling)), rel=1e-10)
    result = compute_entropy_expansion(model, sites, 0)
    assert result.quartic_status == "available"
    assert result.quartic_crossover_time == pytest.approx(tau)


@pytest.mark.parametrize("scale", [0.01, 1.0, 100.0])
def test_cancelled_quartic_term_has_no_validity_interval(scale):
    # Two sites, hence no bulk: c2=1/8, c3=c4=c5=0, c6=7/10-sqrt(2)/2.
    model = SpinChainModel(num_qubits=2, j_zz=scale, hx=scale / np.sqrt(2))
    u = np.array([np.cos(np.pi / 12), np.sin(np.pi / 12)], dtype=complex)
    result = compute_entropy_expansion(model, [u, u], 0)
    assert result.c2 == pytest.approx(scale**2 / 8, rel=1e-12)
    assert abs(result.c3) < 1e-12 * scale**3
    assert abs(result.c4) < 1e-12 * scale**4
    assert result.quartic_status == "quartic_unresolved"
    assert result.quartic_crossover_time is None
    legacy = compute_higher_order_expansion_and_timescale(model, [u, u], 0)
    assert np.isnan(legacy[3])
    psi0, _ = build_initial_product_state([u, u])
    t = 2 / scale
    evolved = evolve_exact_krylov(build_sparse_hamiltonian(model), psi0, np.array([t]))[0]
    entropy = compute_bipartite_linear_entropy(evolved, 0, 2)
    assert entropy == pytest.approx(0.2753315136, abs=1e-9)
    assert abs(entropy - result.c2 * t**2) > 0.2


def test_zero_hamiltonian_has_unavailable_quartic_diagnostic():
    model = SpinChainModel(num_qubits=2, j_zz=0.0)
    sites = [np.array([1.0, 0.0], dtype=complex)] * 2
    result = compute_entropy_expansion(model, sites, 0)
    assert (result.c2, result.c3, result.c4) == (0.0, 0.0, 0.0)
    assert result.quartic_status == "quadratic_unresolved"
    assert result.quartic_crossover_time is None


def test_site_rescaling_does_not_change_exact_or_mean_field_comparison():
    model = SpinChainModel(num_qubits=2, j_zz=1.0, hx=0.8)
    u = np.array([np.cos(0.4), np.sin(0.4)], dtype=complex)
    first = run_single_scaling_benchmark(model, [u, u], "normalized")
    scaled = run_single_scaling_benchmark(model, [2 * u, u], "rescaled")
    assert first.max_trace_distance == pytest.approx(scaled.max_trace_distance, abs=1e-10)
    assert first.max_observable_error == pytest.approx(scaled.max_observable_error, abs=1e-10)
    times = np.linspace(0.0, 0.2, 5)
    a = solve_mean_field_trajectory(model, [u, u], times)
    b = solve_mean_field_trajectory(model, [2 * u, u], times)
    assert np.allclose(a, b, atol=1e-10)


def test_clean_install_declares_scipy_dependency():
    metadata = tomllib.loads((Path(__file__).resolve().parents[2] / "pyproject.toml").read_text())
    assert any(dep.lower().startswith("scipy") for dep in metadata["project"]["dependencies"])


@pytest.mark.parametrize("vector", [np.zeros(2), np.array([np.nan, 1]), np.ones(3)])
def test_invalid_site_vectors_are_refused(vector):
    with pytest.raises(ValueError):
        build_initial_product_state([vector])


def test_benchmark_does_not_report_numerical_certification():
    model = SpinChainModel(num_qubits=2, j_xx=1.0, j_zz=0.0)
    sites = [np.array([1.0, 0.0], dtype=complex)] * 2
    result = run_single_scaling_benchmark(model, sites, "XX")
    assert result.numerical_error_certified is False
    assert result.max_duhamel_bound >= result.max_trace_distance
