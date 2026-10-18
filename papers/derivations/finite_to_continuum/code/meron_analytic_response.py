"""Exact finite bounds for the written uniform-source AR-1--AR-10 theorem."""
from dataclasses import dataclass
from fractions import Fraction as Q

from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    RationalInterval, _validate_exact_rational,
)
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import EulerTimePlan, _size
from omega_engine_projects.finite_to_continuum.code.meron_observable_transport import staggered_moments


@dataclass(frozen=True)
class AnalyticResponsePlan:
    time: EulerTimePlan
    resolution: Q

    source_radius = Q(1, 64)
    log_pressure_majorant = Q(1, 19)

    def __post_init__(self):
        if not isinstance(self.time, EulerTimePlan):
            raise TypeError("one exact temperature plan required")
        eps = _validate_exact_rational(self.resolution, "response resolution")
        _size(eps)
        object.__setattr__(self, "resolution", eps)
        if self.time.parameter.hi > Q(1, 192):
            raise ValueError("temperature interval exceeds proved upper bound 1/192")
        if not 0 < eps <= self.source_radius / 2:
            raise ValueError("response resolution must lie in (0,1/128]")
        if self.exponential_ceiling > 64:
            raise ValueError("exponential majorant resource limit")

    @property
    def exponential_ceiling(self):
        x = Q(self.time.sites, self.time.repetitions) * (
            self.time.parameter.midpoint + self.source_radius)
        return -(-x.numerator // x.denominator)

    @property
    def pressure_error(self):
        time, r, radius = self.time, self.time.parameter.midpoint, self.source_radius
        return (Q(time.sites, time.repetitions) * (r + radius / 2) ** 2
                * 3 ** self.exponential_ceiling
                + Q(3, 4) * time.parameter_drift
                + Q(3, 2) * time.parameter.hi / time.sites)

    @property
    def response_error(self):
        return (4 * self.pressure_error / self.resolution ** 2
                + 64 * self.log_pressure_majorant * self.resolution ** 2 / self.source_radius ** 4)


@dataclass(frozen=True)
class DeclaredAnalyticResponse:
    plan: AnalyticResponsePlan
    moments: object
    intensive_response: Q
    thermodynamic_response_enclosure: RationalInterval
    authority_effect: str = "None"


def sample_analytic_response(plan):
    if not isinstance(plan, AnalyticResponsePlan):
        raise TypeError("an admitted analytic response plan required")
    time = plan.time
    moments = staggered_moments(time.sites, time.repetitions, time.q)
    if moments.first != 0:
        raise ValueError("actual zero-source particle-hole symmetry failed")
    value = moments.mean_square / time.sites
    return DeclaredAnalyticResponse(plan, moments, value,
        RationalInterval.from_point(value, plan.response_error))
