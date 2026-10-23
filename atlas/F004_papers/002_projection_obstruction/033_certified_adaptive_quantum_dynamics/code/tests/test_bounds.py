"""Tests for computable observable error bound B_O(t) and certificate honesty.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.bounds import (
    evaluate_bound,
    compute_cumulative_bounds,
    verify_bound_honesty,
    CertificateTracker,
)
from caqd.dynamics import evolve_exact, evolve_mean_field
from caqd.spin_chains import (
    TFIMChain,
    operator_norm,
    polarized_x_state,
    staggered_magnetization,
    center_correlation,
    transverse_magnetization,
)


def test_evaluate_bound_scalar_and_dict():
    """Verify evaluate_bound handles dicts, arrays, and scalar integrals correctly."""
    res_dict = {(0, 1): [0.1, 0.2, 0.3], (1, 2): [0.05, 0.1, 0.15]}
    times = [0.0, 0.5, 1.0]
    
    bound = evaluate_bound(res_dict, obs_norm=1.0, times=times)
    assert bound > 0.0
    
    # Boundary: empty input returns 0.0
    assert evaluate_bound({}, obs_norm=1.0) == 0.0
    assert evaluate_bound([], obs_norm=1.0) == 0.0


def test_certificate_tracker_online():
    """Verify streaming CertificateTracker matches batch evaluation."""
    tracker = CertificateTracker(obs_norm=2.0)
    
    b0 = tracker.step(0.0, 0.1)
    assert b0 == 0.0
    
    b1 = tracker.step(0.5, 0.2)
    # Area = 0.5 * (0.1 + 0.2) * 0.5 = 0.075 * 2.0 = 0.15
    assert b1 == pytest.approx(0.15)
    
    pred = tracker.predict_horizon_error(1.0)
    # Remaining dt = 0.5, rate = 0.2, additional = 2.0 * 0.2 * 0.5 = 0.20 => total = 0.35
    assert pred == pytest.approx(0.35)


def test_bound_honesty_kill_test_tfim(tfim_n4):
    """MANDATORY KILL-TEST: Verify Margin_O(t) >= 0 at all times for physical observables."""
    rho0 = polarized_x_state(4)
    obs = {
        "M_stag": staggered_magnetization(4),
        "C_mid": center_correlation(4),
        "M_x": transverse_magnetization(4),
    }
    times = np.linspace(0.0, 0.4, 9)
    
    exact_res = evolve_exact(tfim_n4, rho0, times, obs)
    mf_res = evolve_mean_field(tfim_n4, rho0, times, obs)
    
    report = verify_bound_honesty(exact_res, mf_res, obs)
    
    for name, verif in report.items():
        assert verif.is_honest, f"Certificate violated for {name}: min_margin = {verif.min_margin}"
        assert verif.min_margin >= -1e-12
        # Bound at t=0 must be 0
        assert verif.certified_bounds[0] == pytest.approx(0.0, abs=1e-12)
        # Margins at all steps must be >= 0
        assert np.all(verif.margins >= -1e-12)
