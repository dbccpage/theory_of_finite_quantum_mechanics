"""Tests for Certified Adaptive Quantum Dynamics (CAQD) solver.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.adaptive import evolve_adaptive, QuantumCluster, _merge_clusters
from caqd.dynamics import evolve_exact, evolve_mean_field
from caqd.bounds import verify_bound_honesty
from caqd.spin_chains import (
    TFIMChain,
    neel_state,
    polarized_x_state,
    staggered_magnetization,
    center_correlation,
)


def test_quantum_cluster_basics():
    """Verify QuantumCluster creation, marginal extraction, and merging."""
    c0 = QuantumCluster([0], 0.5 * np.eye(2))
    c1 = QuantumCluster([1], np.diag([1.0, 0.0]))
    
    assert c0.contains_site(0)
    assert not c0.contains_site(1)
    
    # Merge c0 and c1
    c01 = _merge_clusters(c0, c1)
    assert c01.sites == [0, 1]
    assert c01.dim == 4
    
    # Marginal on site 1 must be |0><0|
    m1 = c01.single_site_marginal(1)
    np.testing.assert_allclose(m1, np.diag([1.0, 0.0]), atol=1e-12)


def test_adaptive_refinement_reduces_residual(tfim_n4):
    """Verify that adaptive cluster merging reduces cumulative projection residual."""
    rho0 = polarized_x_state(4)
    obs = {"M_stag": staggered_magnetization(4)}
    times = [0.0, 0.1, 0.2, 0.3]
    
    # Fixed chi=1 mean field
    mf_res = evolve_mean_field(tfim_n4, rho0, times, obs)
    
    # Adaptive CAQD with tight threshold forcing cluster merging
    adapt_res = evolve_adaptive(
        tfim_n4,
        rho0,
        obs,
        times,
        tol=0.01, # strict tolerance forces merging
        max_bond=4,
        refine_threshold=0.01,
    )
    
    # At least one cluster merger must have occurred
    final_clusters = adapt_res.metadata["final_clusters"]
    assert any(len(c) > 1 for c in final_clusters)
    
    # Total accumulated residual rate in adaptive run should be <= mean field rate
    assert adapt_res.total_rates[-1] <= mf_res.total_rates[-1] + 1e-12


def test_adaptive_certificate_honesty(tfim_n4):
    """Verify that CAQD adaptive trajectories satisfy Margin_O(t) >= 0."""
    rho0 = neel_state(4)
    obs = {"C_mid": center_correlation(4)}
    times = np.linspace(0.0, 0.3, 7)
    
    exact_res = evolve_exact(tfim_n4, rho0, times, obs)
    adapt_res = evolve_adaptive(tfim_n4, rho0, obs, times, tol=0.1, max_bond=4)
    
    report = verify_bound_honesty(exact_res, adapt_res, obs)
    for name, verif in report.items():
        assert verif.is_honest, f"Certificate violated in adaptive run for {name}"
        assert np.all(verif.margins >= -1e-5)


def test_adaptive_max_bond_constraint(tfim_n4):
    """Verify max_bond ceiling is strictly respected during adaptation."""
    rho0 = polarized_x_state(4)
    times = [0.0, 0.1, 0.2]
    # Set max_bond = 2 (clusters cannot exceed 2 sites)
    adapt_res = evolve_adaptive(tfim_n4, rho0, {}, times, tol=0.001, max_bond=2, refine_threshold=0.001)
    
    for c in adapt_res.metadata["final_clusters"]:
        assert len(c) <= 2


def test_correlated_initial_state_cannot_have_zero_initial_error():
    import pytest
    from caqd.dynamics import evolve_mean_field
    from caqd.spin_chains import TFIMChain
    psi = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    rho = np.outer(psi, psi.conj())
    model = TFIMChain(2)
    with pytest.raises(ValueError, match="Product-state"):
        evolve_adaptive(model, rho, t_span=[0.0, 0.01])
    with pytest.raises(ValueError, match="Product-state"):
        evolve_mean_field(model, rho, t_span=[0.0, 0.01])


def test_periodic_cluster_reconstruction_preserves_site_order():
    from caqd.spin_chains import TFIMChain
    model = TFIMChain(3, h=0.0, periodic=True)
    for term in model.terms:
        if term.term_type == "2-local" and set(term.sites) != {0, 2}:
            term.matrix[:] = 0
    plus = np.ones((2, 2), dtype=complex) / 2
    zero = np.diag([1.0, 0.0]).astype(complex)
    initial = np.kron(np.kron(plus, zero), plus)
    result = evolve_adaptive(model, [plus, zero, plus], t_span=[0.0], max_bond=2, refine_threshold=0.01)
    assert any(set(cluster) == {0, 2} for cluster in result.metadata["final_clusters"])
    assert np.allclose(result.states[0], initial)
    assert result.metadata["certificate_status"] == "HEURISTIC_UNCERTIFIED"
