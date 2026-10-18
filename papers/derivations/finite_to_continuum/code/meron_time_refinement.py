"""Actual finite-chain time samples with the written common-target error law.

The parameter interval is a supplied enclosure of beta*t for one fixed chain.
Finite samples do not prove that enclosure or a spatial/thermodynamic limit.
"""
from dataclasses import dataclass
from fractions import Fraction

from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    RationalInterval, _validate_exact_int, certified_ln_interval,
)
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import (
    meron_transfer_trace,
)

MAX_REPETITIONS = 256
MAX_SCALAR_BITS = 256
MAX_TRANSFER_WORK = 1 << 20


def _size(value):
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_SCALAR_BITS:
        raise ValueError("exact scalar resource limit")


@dataclass(frozen=True)
class EulerTimePlan:
    sites: int
    repetitions: int
    parameter: RationalInterval

    def __post_init__(self):
        sites = _validate_exact_int(self.sites, "sites")
        repetitions = _validate_exact_int(self.repetitions, "repetitions")
        if sites < 4 or sites % 2 or sites > 256:
            raise ValueError("bounded even checkerboard chain >=4 required")
        if not 1 <= repetitions <= MAX_REPETITIONS:
            raise ValueError("time repetition resource limit")
        if not isinstance(self.parameter, RationalInterval):
            raise TypeError("an exact parameter interval is required")
        if self.parameter.lo < 0:
            raise ValueError("nonnegative beta*t parameter required")
        _size(self.parameter.midpoint)
        _size(self.parameter.radius)
        _size(self.q)

    @property
    def q(self):
        return 1 + self.parameter.midpoint / self.repetitions

    @property
    def slice_growth(self):
        return self.q ** self.sites

    @property
    def parameter_drift(self):
        return self.parameter.midpoint ** 2 / (2 * self.repetitions) + self.parameter.radius

    @property
    def splitting_bound(self):
        return self.parameter.midpoint ** 2 * self.slice_growth / self.repetitions

    @property
    def raw_density_error(self):
        return self.splitting_bound + self.parameter_drift

    @property
    def physical_density_error(self):
        return self.splitting_bound + Fraction(3, 4) * self.parameter_drift

    @property
    def thermodynamic_density_error(self):
        return self.physical_density_error + Fraction(3, 2) * self.parameter.hi / self.sites


@dataclass(frozen=True)
class DeclaredTimeSample:
    plan: EulerTimePlan
    unscaled_partition: Fraction
    raw_density: RationalInterval
    physical_density: RationalInterval
    raw_target_enclosure: RationalInterval
    physical_target_enclosure: RationalInterval
    thermodynamic_target_enclosure: RationalInterval
    authority_effect: str = "None"


def sample_time_plan(plan: EulerTimePlan, *, log_order=20):
    """Calls the original full-Fock transfer trace without its canonical cache."""
    if not isinstance(plan, EulerTimePlan):
        raise TypeError("EulerTimePlan required")
    order = _validate_exact_int(log_order, "log order")
    if not 1 <= order <= 64:
        raise ValueError("logarithm order resource limit")
    work = plan.sites * plan.repetitions * (1 << (2 * plan.sites))
    if work > MAX_TRANSFER_WORK:
        raise ValueError("occupation-basis transfer resource limit")
    trace = Fraction(meron_transfer_trace(plan.sites, plan.repetitions, plan.q))
    if trace < 1 << plan.sites:
        raise ValueError("source trace violates the declared positive-projector model")
    raw = certified_ln_interval(RationalInterval(trace), order=order) / plan.sites
    effective_parameter = certified_ln_interval(RationalInterval(plan.q), order=order) * plan.repetitions
    physical = raw - effective_parameter / 4
    raw_error = plan.raw_density_error
    physical_error = plan.physical_density_error
    thermodynamic_error = plan.thermodynamic_density_error
    return DeclaredTimeSample(plan, trace, raw, physical,
        RationalInterval(raw.lo - raw_error, raw.hi + raw_error),
        RationalInterval(physical.lo - physical_error, physical.hi + physical_error),
        RationalInterval(physical.lo - thermodynamic_error, physical.hi + thermodynamic_error))


def canonical_parameter_interval(*, log_order=12):
    """beta*t=2*log(3), the temperature of the original q=3,M=2 fixture."""
    order = _validate_exact_int(log_order, "log order")
    if not 1 <= order <= 64:
        raise ValueError("logarithm order resource limit")
    return certified_ln_interval(RationalInterval(3), order=order) * 2
