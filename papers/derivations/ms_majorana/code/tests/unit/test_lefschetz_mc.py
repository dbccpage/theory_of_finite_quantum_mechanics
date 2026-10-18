r"""
Unit tests for Lefschetz Thimble Monte Carlo (LTMC) & parallel transport (codaq/lefschetz_mc.py).
"""

import cmath
import math
import pytest
from omega_engine.crates.homology_theory.lefschetz_mc import (
    ThimbleMetropolisSampler,
    estimate_airy_integral,
)
from omega_engine.crates.homology_theory.lefschetz_thimble import (
    AiryAction,
    steepest_descent_flow_with_frame,
)


def test_tangent_frame_transport_airy():
    action = AiryAction(lam=1.0 + 0.0j)
    z_start = [0.2 + 1.1j]

    res = steepest_descent_flow_with_frame(action, z_start, dt=0.005, steps=50)
    assert len(res.jacobian_history) == 51

    # Check Jacobian determinant magnitude is positive and finite
    assert res.jacobian_determinant > 0.0
    assert math.isfinite(res.residual_phase)


def test_residual_phase_smoothness():
    action = AiryAction(lam=1.0 + 0.0j)
    z_start = [0.1 + 0.9j]

    res = steepest_descent_flow_with_frame(action, z_start, dt=0.002, steps=100)
    # Check that residual phase stays within [-pi, pi]
    assert -math.pi <= res.residual_phase <= math.pi
    assert res.max_im_deviation < 1e-3


def test_thimble_metropolis_sampler_1d():
    action = AiryAction(lam=1.0 + 0.0j)
    sampler = ThimbleMetropolisSampler(action, seed=123)

    cp = action.exact_critical_points()[0]
    samples, acc_rate, p_weight = sampler.sample_1d_thimble(
        cp=[cp], unstable_dir=[1.0 + 0.0j], flow_time=0.1, n_samples=500
    )

    assert len(samples) == 500
    assert 0.1 < acc_rate <= 1.0
    assert math.isfinite(p_weight)


def test_airy_integral_reconstruction():
    lam = 1.0 + 0.0j
    z_est = estimate_airy_integral(lam, n_samples=1000)

    # Reconstructed value should be finite complex number
    assert math.isfinite(z_est.real)
    assert math.isfinite(z_est.imag)


def test_tempered_lefschetz_thimble_sampler():
    from omega_engine.crates.homology_theory.lefschetz_mc import TemperedLefschetzThimbleSampler

    action = AiryAction(lam=1.0 + 0.0j)
    tltm = TemperedLefschetzThimbleSampler(
        action=action, flow_times=[0.0, 0.02, 0.05], seed=42
    )

    res = tltm.sample(n_samples=50, step_size=0.1, swap_interval=2)

    assert len(res["target_samples"]) == 50
    assert len(res["target_phases"]) == 50
    assert math.isfinite(res["reweighted_integral"])
    assert 0.0 <= res["swap_acceptance"] <= 1.0



