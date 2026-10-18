"""Bounds and retained weighted SQL readouts for the written Gaussian profile."""
from dataclasses import dataclass
from fractions import Fraction as Q
from omega_engine_projects.finite_to_continuum.code.circle_piecewise_linear import CirclePiecewiseLinear
from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    RationalInterval, _validate_exact_rational,
)
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import _size
from omega_engine_projects.finite_to_continuum.code.meron_analytic_response import AnalyticResponsePlan
from omega_engine_projects.finite_to_continuum.code.meron_observable_transport import weighted_staggered_moments


@dataclass(frozen=True)
class SpatialSourcePlan:
    response: AnalyticResponsePlan
    profile: CirclePiecewiseLinear
    probe: Q

    def __post_init__(self):
        if not isinstance(self.response, AnalyticResponsePlan) or not isinstance(self.profile, CirclePiecewiseLinear):
            raise TypeError("an admitted response and immutable circle profile required")
        probe = _validate_exact_rational(self.probe, "spatial source probe")
        _size(probe)
        object.__setattr__(self, "probe", probe)
        if self.squared_source_fraction >= 1:
            raise ValueError("spatial source probe leaves proved analytic disk")

    @property
    def squared_source_fraction(self):
        return self.probe ** 2 * self.profile.norm ** 2 / (
            self.response.time.sites * self.response.source_radius ** 2)

    @property
    def quadratic_error(self):
        r, c = self.response.source_radius, self.response.log_pressure_majorant
        kernel, susceptibility = Q(16, 143) / r**2, 2*c / r**2
        return (self.profile.norm**2 * self.response.response_error
                + (40*kernel+susceptibility)*self.profile.norm*self.profile.lipschitz
                / self.response.time.sites)

    @property
    def finite_log_tail(self):
        r, c = self.response.source_radius, self.response.log_pressure_majorant
        return c*self.probe**4*self.profile.norm**4 / (
            self.response.time.sites*r**4*(1-self.squared_source_fraction))

    @property
    def source_functional_error(self):
        return self.probe**2*self.quadratic_error/2+self.finite_log_tail


@dataclass(frozen=True)
class DeclaredSpatialSource:
    plan: SpatialSourcePlan
    moments: object
    quadratic: RationalInterval
    finite_log: RationalInterval
    continuum_log: RationalInterval
    authority_effect: str = "None"


def sample_spatial_source(plan):
    if not isinstance(plan, SpatialSourcePlan):
        raise TypeError("an admitted spatial source plan required")
    time, profile = plan.response.time, plan.profile
    moments = weighted_staggered_moments(time.sites, time.repetitions, time.q,
                                         profile.uniform_samples(time.sites))
    if moments.first != 0:
        raise ValueError("actual weighted particle-hole first moment failed")
    value = moments.mean_square/time.sites
    center = plan.probe**2*value/2
    return DeclaredSpatialSource(plan, moments,
        RationalInterval.from_point(value, plan.quadratic_error),
        RationalInterval.from_point(center, plan.finite_log_tail),
        RationalInterval.from_point(center, plan.probe**2*plan.quadratic_error/2))
