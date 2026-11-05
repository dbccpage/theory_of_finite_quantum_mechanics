"""Sampled estimates of the conditional analytic residual bound.

Trapezoidal quadrature and comparisons with a dense numerical reference do not
certify a continuous-time trajectory. Integration and quadrature errors are not
bounded here. Historical API names containing "certificate" are retained.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence, Tuple
import numpy as np

from caqd.dynamics import SimulationResult
from caqd.spin_chains import operator_norm


class NumericalRefusalError(ValueError):
    """Finite inputs exceeded the range of the sampled-estimate arithmetic."""


def _finite_result(value, name: str):
    if not np.all(np.isfinite(value)):
        raise NumericalRefusalError(f"{name} is not representable as a finite estimate")
    return value


def _area(left: float, right: float, start: float, stop: float) -> float:
    # Halve before adding: two finite large rates can have a finite mean even
    # when their unscaled sum overflows. No interval enclosure is implied.
    width = _finite_result(float(stop) - float(start), "interval width")
    mean = 0.5 * float(left) + 0.5 * float(right)
    return _finite_result(mean * width, "trapezoidal area")


def _nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not np.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _rates(values: Sequence[float]) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or not np.all(np.isfinite(result)) or np.any(result < 0):
        raise ValueError("rates must be a finite nonnegative one-dimensional sequence")
    return result


def _times(values: Sequence[float], length: int) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if (result.ndim != 1 or len(result) != length
            or not np.all(np.isfinite(result)) or np.any(result[1:] < result[:-1])):
        raise ValueError("times must be finite, nondecreasing, and match the rate history")
    return result


def evaluate_bound(
    residuals_history: Dict[Tuple[int, int], Sequence[float]] | Sequence[float] | np.ndarray,
    obs_norm: float,
    times: Sequence[float] | None = None,
) -> float:
    """Estimate the residual integral; this is not a numerical certificate.
    
    Args:
        residuals_history: Either a dict mapping edge (a, b) -> sequence of rates nu_e(t),
                           or an array of total instantaneous rates sum_e nu_e(t).
        obs_norm: Spectral norm ||O||_inf of the target observable.
        times: Sample times. If None, retain the legacy sum of unit-width bins.
        
    Returns:
        Scalar sampled estimate of B_O(T).
    """
    obs_norm = _nonnegative(obs_norm, "obs_norm")
    if isinstance(residuals_history, dict):
        if not residuals_history:
            total_rates = np.zeros(len(times) if times is not None else 0)
        else:
            histories = [_rates(values) for values in residuals_history.values()]
            if any(len(values) != len(histories[0]) for values in histories):
                raise ValueError("edge rate histories must have equal lengths")
            with np.errstate(over="ignore", invalid="ignore"):
                total_rates = _finite_result(np.sum(histories, axis=0), "total rates")
    else:
        total_rates = _rates(residuals_history)

    t_arr = _times(times, len(total_rates)) if times is not None else None
        
    if len(total_rates) == 0:
        return 0.0
        
    if times is None:
        # Simple rectangular sum if times not provided
        integral = _finite_result(sum(map(float, total_rates)), "residual sum")
    else:
        if len(t_arr) <= 1:
            integral = 0.0
        else:
            # Trapezoidal integration along trajectory
            integral = _finite_result(sum(
                _area(left, right, start, stop)
                for left, right, start, stop in zip(
                    total_rates[:-1], total_rates[1:], t_arr[:-1], t_arr[1:]
                )
            ), "residual integral")
            
    return _finite_result(float(obs_norm * integral), "observable estimate")


def compute_cumulative_bounds(
    sim_result: SimulationResult,
    obs: np.ndarray | float,
) -> np.ndarray:
    """Compute cumulative sampled estimates of B_O(t_k).

    Adaptive results store interval areas with the incoming rate before a merge
    and the previous outgoing rate. Reintegrating only post-merge samples would
    erase part of the estimate accumulated on the preceding partition.
    
    Args:
        sim_result: SimulationResult from variational or adaptive simulation.
        obs: Observable matrix O (to compute ||O||_inf) or float operator norm.
        
    Returns:
        1D numpy array of B_O(t_k) for k = 0, ..., K-1.
    """
    o_norm = _nonnegative(float(obs) if np.isscalar(obs) else operator_norm(obs), "obs_norm")
    total_rates = _rates(sim_result.total_rates)
    times = _times(sim_result.times, len(total_rates))

    if "cumulative_residual_estimates" in sim_result.metadata:
        integral = _rates(sim_result.metadata["cumulative_residual_estimates"])
        if (len(integral) != len(times) or np.any(np.diff(integral) < 0)
                or (len(integral) and integral[0] != 0)):
            raise ValueError("cumulative residual estimates must match times, start at zero, and be nondecreasing")
        with np.errstate(over="ignore", invalid="ignore"):
            return _finite_result(o_norm * integral, "observable estimates")
    
    if len(times) == 0:
        return np.array([])
        
    bounds = np.zeros(len(times), dtype=float)
    cumulative_integral = 0.0
    
    for i in range(1, len(times)):
        # Trapezoidal step increment
        step_area = _area(total_rates[i - 1], total_rates[i], times[i - 1], times[i])
        cumulative_integral = _finite_result(cumulative_integral + step_area, "residual integral")
        bounds[i] = _finite_result(o_norm * cumulative_integral, "observable estimate")
        
    return bounds


@dataclass
class ObservableVerification:
    """Numerical reference comparison; certified_bounds is a legacy field name."""
    name: str
    obs_norm: float
    true_errors: np.ndarray
    certified_bounds: np.ndarray
    margins: np.ndarray
    min_margin: float
    is_honest: bool
    tightness_ratios: np.ndarray
    max_tightness: float


def verify_bound_honesty(
    exact_res: SimulationResult,
    approx_res: SimulationResult,
    obs_dict: Dict[str, np.ndarray],
    tol: float = 1e-5,
) -> Dict[str, ObservableVerification]:
    """Compare sampled residual estimates with numerical reference errors.
    
    A nonnegative margin is a regression observation, not a proof or assertion.
    
    Args:
        exact_res: Exact unitary benchmark simulation.
        approx_res: Approximate (mean-field or adaptive) simulation.
        obs_dict: Dictionary of observables {"O_name": O_matrix}.
        tol: Small numerical tolerance for floating-point comparisons.
        
    Returns:
        Dictionary mapping observable name to ObservableVerification report.
    """
    tol = _nonnegative(tol, "tol")
    approx_times = _times(approx_res.times, len(approx_res.total_rates))
    exact_times = _times(exact_res.times, len(exact_res.total_rates))
    if not np.array_equal(exact_times, approx_times):
        raise ValueError("reference and approximate trajectories must use identical time grids")
    report: Dict[str, ObservableVerification] = {}
    
    for name, O in obs_dict.items():
        exact_vals = exact_res.expectation(name)
        approx_vals = approx_res.expectation(name)
        for values in (exact_vals, approx_vals):
            if (np.asarray(values).shape != approx_times.shape
                    or not np.all(np.isfinite(values))):
                raise ValueError("observable histories must be finite and match the time grid")
        with np.errstate(over="ignore", invalid="ignore"):
            true_errors = _finite_result(np.abs(exact_vals - approx_vals), "reference errors")
        
        o_norm = operator_norm(O)
        bounds = compute_cumulative_bounds(approx_res, o_norm)
        margins = bounds - true_errors
        min_margin = float(np.min(margins)) if len(margins) else 0.0
        is_honest = bool(min_margin >= -tol)
        
        # A zero estimate hides a real error. Dust within tol does not:
        # the opening sample is a zero integral before any rate is accumulated.
        with np.errstate(divide="ignore", invalid="ignore"):
            tightness = np.where(bounds > 0, true_errors / bounds,
                                 np.where(true_errors <= tol, 0.0, np.inf))
        max_tightness = float(np.max(tightness)) if len(tightness) > 0 else 0.0
        
        report[name] = ObservableVerification(
            name=name,
            obs_norm=o_norm,
            true_errors=true_errors,
            certified_bounds=bounds,
            margins=margins,
            min_margin=min_margin,
            is_honest=is_honest,
            tightness_ratios=tightness,
            max_tightness=max_tightness,
        )
        
    return report


class CertificateTracker:
    """Legacy-named streaming accumulator for sampled residual estimates."""
    def __init__(self, obs_norm: float):
        self.obs_norm = _nonnegative(obs_norm, "obs_norm")
        self.prev_time: float | None = None
        self.prev_rate: float = 0.0
        self.cumulative_bound: float = 0.0
        
    def step(self, t: float, current_edge_rates: Dict[Tuple[int, int], float] | float) -> float:
        """Record instantaneous rate at time t and update cumulative bound."""
        if isinstance(current_edge_rates, dict):
            current_rate = _finite_result(
                float(sum(_nonnegative(rate, "rate") for rate in current_edge_rates.values())),
                "total rate",
            )
        else:
            current_rate = _nonnegative(current_edge_rates, "rate")
        t = float(t)
        if not np.isfinite(t) or (self.prev_time is not None and t < self.prev_time):
            raise ValueError("time must be finite and must not move backwards")
            
        next_bound = self.cumulative_bound
        if self.prev_time is not None and t > self.prev_time:
            inc = _area(self.prev_rate, current_rate, self.prev_time, t)
            next_bound = _finite_result(self.cumulative_bound + self.obs_norm * inc,
                                        "streaming estimate")
                
        self.prev_time = t
        self.prev_rate = current_rate
        self.cumulative_bound = next_bound
        return self.cumulative_bound

    def predict_horizon_error(self, horizon_t: float) -> float:
        """Extrapolate the estimate assuming the current rate persists."""
        horizon_t = float(horizon_t)
        if not np.isfinite(horizon_t):
            raise ValueError("horizon must be finite")
        if self.prev_time is None or horizon_t <= self.prev_time:
            return self.cumulative_bound
        dt = _finite_result(horizon_t - self.prev_time, "horizon width")
        return _finite_result(self.cumulative_bound + self.obs_norm * self.prev_rate * dt,
                              "horizon estimate")
