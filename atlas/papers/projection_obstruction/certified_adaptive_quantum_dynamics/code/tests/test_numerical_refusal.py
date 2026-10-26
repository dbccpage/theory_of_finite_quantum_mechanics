"""Finite input does not imply a representable sampled bound or an honest ratio."""

import numpy as np
import pytest

from caqd.bounds import (
    CertificateTracker, NumericalRefusalError, compute_cumulative_bounds,
    evaluate_bound, verify_bound_honesty,
)
from caqd.dynamics import SimulationResult


def result(rates, values=(0.0, 0.0), **metadata):
    return SimulationResult(
        times=np.array([0.0, 1.0]), states=[], observables={"z": np.array(values)},
        residuals={}, total_rates=np.array(rates), method="test", metadata=metadata,
    )


def test_large_finite_trapezoid_does_not_overflow_its_mean():
    assert evaluate_bound([1e308, 1e308], 1.0, [0.0, 1.0]) == 1e308
    np.testing.assert_array_equal(
        compute_cumulative_bounds(result([1e308, 1e308]), 1.0), [0.0, 1e308]
    )
    tracker = CertificateTracker(1.0)
    tracker.step(0, 1e308)
    assert tracker.step(1, 1e308) == 1e308


@pytest.mark.parametrize("rates,norm,times", [
    ([1e308, 1e308], 1.0, None),
    ({(0, 1): [1e308], (1, 2): [1e308]}, 1.0, [0.0]),
    ([1e308, 1e308], 1.0, [0.0, 2.0]),
    ([1e308, 1e308], 2.0, [0.0, 1.0]),
    ([1.0, 1.0], 1.0, [-1e308, 1e308]),
])
def test_unrepresentable_aggregate_refuses(rates, norm, times):
    with pytest.raises(NumericalRefusalError):
        evaluate_bound(rates, norm, times)


def test_cumulative_and_stored_estimates_refuse_overflow():
    for trajectory in (
        result([1e308, 1e308]),
        result([0.0, 0.0], cumulative_residual_estimates=np.array([0.0, 1e308])),
    ):
        with pytest.raises(NumericalRefusalError):
            compute_cumulative_bounds(trajectory, 2.0)


def test_streaming_refusal_preserves_accepted_state():
    tracker = CertificateTracker(2.0)
    tracker.step(0.0, 1e308)
    before = vars(tracker).copy()
    with pytest.raises(NumericalRefusalError):
        tracker.step(1.0, 1e308)
    assert vars(tracker) == before
    with pytest.raises(NumericalRefusalError):
        tracker.predict_horizon_error(1.0)
    assert vars(tracker) == before
    with pytest.raises(NumericalRefusalError):
        tracker.step(1.0, {(0, 1): 1e308, (1, 2): 1e308})
    assert vars(tracker) == before


def test_subtolerance_dust_at_zero_bound_is_not_an_infinite_ratio():
    report = verify_bound_honesty(
        result([0.0, 0.0], [0.0, 0.0]),
        result([0.0, 0.0], [1e-15, 0.0]),
        {"z": np.diag([1.0, -1.0])},
    )["z"]
    assert report.is_honest
    assert report.tightness_ratios[0] == 0.0
    assert report.tightness_ratios[1] == 0.0
    assert np.isfinite(report.max_tightness)


def test_zero_estimate_does_not_hide_positive_reference_error():
    report = verify_bound_honesty(
        result([0.0, 0.0], [0.0, 0.5]), result([0.0, 0.0]),
        {"z": np.diag([1.0, -1.0])},
    )["z"]
    assert not report.is_honest
    assert report.tightness_ratios[0] == 0.0
    assert report.tightness_ratios[1] == np.inf
    assert report.max_tightness == np.inf
