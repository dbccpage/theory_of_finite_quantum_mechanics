"""Actual source-field traces and conditional common-target response enclosures.

The written infinite-volume theorem is separate from these bounded samples.
Finite resolution is retained; no pointwise susceptibility is inferred.
"""
from dataclasses import dataclass
from fractions import Fraction

from sympy import SparseMatrix

from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    RationalInterval, _validate_exact_int, _validate_exact_rational, certified_ln_interval,
)
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import EulerTimePlan, _size
from omega_engine_projects.finite_to_continuum.code.meron_observable_transport import (
    _occupation_layers, _validated_occupation_query,
)


def source_field_trace(sites, repetitions, q, v):
    sites, repetitions, q = _validated_occupation_query(sites, repetitions, q)
    v = _validate_exact_rational(v, "source multiplier")
    _size(v)
    if v <= 0:
        raise ValueError("source multiplier must be positive")
    insertion, layers = _occupation_layers(sites, q)
    diagonal = SparseMatrix.diag(*(v ** int(insertion[i, i]) for i in range(1 << sites)))
    product = (layers[1] * diagonal * layers[0] * diagonal) ** repetitions
    return Fraction(str(product.trace()))


@dataclass(frozen=True)
class SourceFieldPlan:
    time: EulerTimePlan
    field: RationalInterval

    def __post_init__(self):
        if not isinstance(self.time, EulerTimePlan) or not isinstance(self.field, RationalInterval):
            raise TypeError("exact time plan and field interval required")
        _size(self.field.midpoint)
        _size(self.field.radius)
        _size(self.v)
        if self.exponential_ceiling > 64:
            raise ValueError("exponential majorant resource limit")

    @property
    def v(self):
        s = self.field.midpoint
        positive = 1 + abs(s) / (2 * self.time.repetitions)
        return 1 / positive if s < 0 else positive

    @property
    def exponential_ceiling(self):
        x = self.time.sites * (self.time.parameter.midpoint + abs(self.field.midpoint)) / self.time.repetitions
        return -(-x.numerator // x.denominator)

    @property
    def exponential_majorant(self):
        return Fraction(3 ** self.exponential_ceiling)

    @property
    def field_drift(self):
        return self.field.midpoint ** 2 / (4 * self.time.repetitions) + self.field.radius

    @property
    def finite_density_error(self):
        time = self.time
        splitting = Fraction(time.sites, time.repetitions) * (
            time.parameter.midpoint + abs(self.field.midpoint) / 2) ** 2 * self.exponential_majorant
        return splitting + Fraction(3, 4) * time.parameter_drift + self.field_drift / 2

    @property
    def thermodynamic_density_error(self):
        return self.finite_density_error + Fraction(3, 2) * self.time.parameter.hi / self.time.sites


@dataclass(frozen=True)
class DeclaredSourceSample:
    plan: SourceFieldPlan
    unscaled_partition: Fraction
    physical_density: RationalInterval
    finite_target_enclosure: RationalInterval
    thermodynamic_target_enclosure: RationalInterval
    authority_effect: str = "None"


def sample_source_plan(plan, *, log_order=20):
    if not isinstance(plan, SourceFieldPlan):
        raise TypeError("SourceFieldPlan required")
    order = _validate_exact_int(log_order, "log order")
    if not 1 <= order <= 64:
        raise ValueError("logarithm order resource limit")
    time = plan.time
    trace = source_field_trace(time.sites, time.repetitions, time.q, plan.v)
    if trace <= 0:
        raise ValueError("positive source generating trace required")
    raw = certified_ln_interval(RationalInterval(trace), order=order) / time.sites
    effective_temperature = certified_ln_interval(RationalInterval(time.q), order=order) * time.repetitions
    physical = raw - effective_temperature / 4
    def widen(bound):
        return RationalInterval(physical.lo - bound, physical.hi + bound)
    return DeclaredSourceSample(plan, trace, physical, widen(plan.finite_density_error),
                                widen(plan.thermodynamic_density_error))


def central_second_difference(minus, center, plus, epsilon):
    """Propagate three enclosures of p(x-eps), p(x), p(x+eps)."""
    if not all(isinstance(value, RationalInterval) for value in (minus, center, plus)):
        raise TypeError("three exact pressure enclosures required")
    epsilon = _validate_exact_rational(epsilon, "response resolution")
    if epsilon <= 0:
        raise ValueError("positive response resolution required")
    return (minus + plus - 2 * center) / epsilon ** 2


def with_declared_third_derivative_bound(response, epsilon, bound):
    """Conditional on |p'''|<=bound throughout the resolution interval."""
    if not isinstance(response, RationalInterval):
        raise TypeError("exact finite response interval required")
    epsilon = _validate_exact_rational(epsilon, "response resolution")
    bound = _validate_exact_rational(bound, "third derivative bound")
    if epsilon <= 0 or bound < 0:
        raise ValueError("positive resolution and nonnegative declared bound required")
    radius = bound * epsilon / 3
    return RationalInterval(response.lo - radius, response.hi + radius)


@dataclass(frozen=True)
class DeclaredSourceResponse:
    temperature_plan: EulerTimePlan
    field_center: Fraction
    resolution: Fraction
    samples: tuple
    thermodynamic_response_enclosure: RationalInterval
    authority_effect: str = "None"


def sample_source_response(time, field_center, epsilon, *, log_order=20):
    """Build all three samples at one declared temperature and field resolution."""
    if not isinstance(time, EulerTimePlan):
        raise TypeError("one common temperature plan required")
    x = _validate_exact_rational(field_center, "field center")
    epsilon = _validate_exact_rational(epsilon, "response resolution")
    if epsilon <= 0:
        raise ValueError("positive response resolution required")
    samples = tuple(sample_source_plan(SourceFieldPlan(time, RationalInterval(point)), log_order=log_order)
                    for point in (x - epsilon, x, x + epsilon))
    response = central_second_difference(*(sample.thermodynamic_target_enclosure for sample in samples), epsilon)
    return DeclaredSourceResponse(time, x, epsilon, samples, response)
