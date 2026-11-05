"""Exact arithmetic on supplied error enclosures; does not establish those enclosures."""
from fractions import Fraction

Exact = int | Fraction


def nonnegative(value: Exact, name: str) -> Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError(f"{name} must be an integer or Fraction")
    value = Fraction(value)
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def advance_budget(error: Exact, rate: Exact, duration: Exact,
                   integration: Exact = 0, jump: Exact = 0) -> Fraction:
    """e_next <= e + rate * duration + integration + jump, given the premises."""
    values = [nonnegative(x, n) for x, n in zip(
        (error, rate, duration, integration, jump),
        ("error", "rate", "duration", "integration", "jump"))]
    e, r, h, i, j = values
    return e + r * h + i + j


def waiting_window(target: Exact, error: Exact, reserve: Exact,
                   rate: Exact, horizon: Exact) -> Fraction:
    """Largest duration allowed by this scalar bound within the declared horizon."""
    target, error, reserve, rate, horizon = [nonnegative(x, n) for x, n in zip(
        (target, error, reserve, rate, horizon),
        ("target", "error", "reserve", "rate", "horizon"))]
    if error + reserve > target:
        raise ValueError("the current error and reserve already exceed the target")
    if rate == 0:
        return horizon
    return min(horizon, (target - error - reserve) / rate)


def product_defect_interval(factors: int, estimate: Exact, state_radius: Exact,
                            evaluation_radius: Exact = 0) -> tuple[Fraction, Fraction]:
    """Conditional interval for D(rho), with rho and its reference both density states."""
    if type(factors) is not int or factors < 1:
        raise ValueError("factors must be a positive integer")
    estimate = nonnegative(estimate, "estimate")
    radius = (factors + 1) * nonnegative(state_radius, "state_radius")
    radius += nonnegative(evaluation_radius, "evaluation_radius")
    return max(Fraction(0), estimate - radius), estimate + radius


def onset_lower_bound(rate_estimate: Exact, rate_radius: Exact,
                      quadratic_cap: Exact, duration: Exact) -> Fraction:
    """Conditional lower bound when the true onset rate and remainder are enclosed."""
    estimate, radius, cap, t = [nonnegative(x, n) for x, n in zip(
        (rate_estimate, rate_radius, quadratic_cap, duration),
        ("rate_estimate", "rate_radius", "quadratic_cap", "duration"))]
    rate_lower = max(Fraction(0), estimate - radius)
    return max(Fraction(0), rate_lower * t - cap * t * t)
