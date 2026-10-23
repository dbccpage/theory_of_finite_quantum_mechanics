"""Edge case and branch coverage tests for CAQD package.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.adaptive import QuantumCluster, evolve_adaptive
from caqd.bounds import evaluate_bound, compute_cumulative_bounds, CertificateTracker
from caqd.dynamics import SimulationResult, evolve_mean_field, evolve_exact
from caqd.residuals import (
    compute_local_residuals,
    verify_lemma_5_3_tangent_isolation,
    dual_witness_schatten1,
)
from caqd.spin_chains import TFIMChain, partial_trace


def test_quantum_cluster_dimension_mismatch():
    """Verify QuantumCluster raises ValueError on shape mismatch."""
    with pytest.raises(ValueError):
        QuantumCluster([0, 1], np.eye(2)) # Needs 4x4


def test_adaptive_rho0_validation(tfim_n4):
    """Verify evolve_adaptive validates rho0 input format."""
    with pytest.raises(ValueError):
        evolve_adaptive(tfim_n4, rho0=np.zeros((3, 3)))
    with pytest.raises(ValueError):
        evolve_adaptive(tfim_n4, rho0=[np.eye(2), np.eye(2)]) # 2 sites instead of 4


def test_adaptive_list_observables(tfim_n4):
    """Verify evolve_adaptive accepts list of observables."""
    res = evolve_adaptive(
        tfim_n4,
        rho0=[0.5 * np.eye(2) for _ in range(4)],
        obs_dict=[np.eye(16)],
        t_span=[0.0, 0.05],
    )
    assert "obs_0" in res.observables


def test_bounds_edge_cases():
    """Verify evaluate_bound edge cases with single time point and None times."""
    assert evaluate_bound([0.1, 0.2], obs_norm=1.0, times=None) == pytest.approx(0.3)
    assert evaluate_bound([0.1], obs_norm=1.0, times=[0.0]) == 0.0
    
    # compute_cumulative_bounds on empty simulation result
    empty_res = SimulationResult(
        times=np.array([]),
        states=[],
        observables={},
        residuals={},
        total_rates=np.array([]),
        method="empty",
    )
    assert len(compute_cumulative_bounds(empty_res, obs=1.0)) == 0


def test_certificate_tracker_edge_cases():
    """Verify CertificateTracker with dictionary rates and past horizon."""
    tracker = CertificateTracker(obs_norm=1.0)
    tracker.step(1.0, {(0, 1): 0.1, (1, 2): 0.2})
    # Predict with horizon <= current time
    pred = tracker.predict_horizon_error(0.5)
    assert pred == tracker.cumulative_bound


def test_residuals_format_validation(tfim_n4):
    """Verify compute_local_residuals format validation."""
    with pytest.raises(ValueError):
        compute_local_residuals(tfim_n4, rho_state=np.zeros((5, 5)))
        
    # Test dual witness unit ball assertion error if fed invalid matrix
    with pytest.raises(RuntimeError):
        # Construct an artificial W with norm > 1.0 by patching svd return
        class BadSVD:
            @staticmethod
            def svd(Q, **kwargs):
                return 2.0 * np.eye(Q.shape[0]), np.ones(Q.shape[0]), np.eye(Q.shape[0])
        import scipy.linalg
        orig_svd = scipy.linalg.svd
        try:
            scipy.linalg.svd = BadSVD.svd
            dual_witness_schatten1(np.eye(4))
        finally:
            scipy.linalg.svd = orig_svd


def test_mean_field_rho0_validation(tfim_n4):
    """Verify evolve_mean_field validates rho0 format."""
    with pytest.raises(ValueError):
        evolve_mean_field(tfim_n4, rho0=np.zeros((7, 7)), t_span=[0.0, 0.1])


def test_lemma_5_3_embedded():
    """Verify verify_lemma_5_3_tangent_isolation with arbitrary 2x2 matrix."""
    rho_a = 0.5 * np.eye(2)
    rho_b = 0.5 * np.eye(2)
    h_a = np.array([[1.0, 0.5], [0.5, -1.0]])
    res = verify_lemma_5_3_tangent_isolation(rho_a, rho_b, h_a)
    assert res == pytest.approx(0.0, abs=1e-14)
