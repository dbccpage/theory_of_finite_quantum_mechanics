"""Actual transfer samples checked against independent finite-generator series."""
from fractions import Fraction
from functools import lru_cache
from math import factorial

import pytest
from sympy import Matrix, eye, zeros

from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    RationalInterval, certified_ln_interval,
)
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import (
    EulerTimePlan, canonical_parameter_interval, sample_time_plan,
)
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import (
    meron_transfer_trace,
)


@lru_cache(maxsize=2)
def generator_trace_powers(order):
    """Build CAR matrices directly from occupation bits, without transfer slices."""
    lowering = []
    for mode in range(4):
        c = zeros(16)
        for state in range(16):
            if state & (1 << mode):
                c[state ^ (1 << mode), state] = (-1) ** ((state & ((1 << mode) - 1)).bit_count())
        lowering.append(c)
    number = [c.T * c for c in lowering]
    generator = zeros(16)
    for x in range(4):
        y = (x + 1) % 4
        generator += (number[x] + number[y] - 2 * number[x] * number[y]
                      + lowering[x].T * lowering[y] + lowering[y].T * lowering[x]) / 2
    power = eye(16)
    traces = []
    for _ in range(order + 1):
        traces.append(Fraction(str(power.trace())))
        power = power * generator
    return tuple(traces)


def independent_density_enclosure(parameter, order=40):
    center = parameter.midpoint
    x = center * 4
    assert x < order + 2
    traces = generator_trace_powers(order)
    partial = sum(center ** k * trace / factorial(k) for k, trace in enumerate(traces))
    tail = 16 * x ** (order + 1) / factorial(order + 1) / (1 - x / (order + 2))
    interval = certified_ln_interval(RationalInterval(partial, partial + tail), order=20) / 4 - center / 4
    radius = Fraction(3, 4) * parameter.radius
    return RationalInterval(interval.lo - radius, interval.hi + radius)


@pytest.mark.parametrize("repetitions", (1, 2, 4, 8, 16, 32))
def test_same_finite_hamiltonian_target_with_actual_source_samples(repetitions):
    parameter = RationalInterval(Fraction(1, 16))
    sample = sample_time_plan(EulerTimePlan(4, repetitions, parameter))
    reference = independent_density_enclosure(parameter)
    assert sample.physical_target_enclosure.contains_interval(reference)
    assert sample.unscaled_partition == Fraction(meron_transfer_trace(4, repetitions, sample.plan.q))
    assert sample.authority_effect == "None"
    assert sample.physical_density.hi < sample.raw_density.lo


@pytest.mark.parametrize("repetitions", (4, 8, 16))
def test_original_canonical_temperature_is_retained_by_an_enclosed_parameter(repetitions):
    parameter = canonical_parameter_interval(log_order=8)
    sample = sample_time_plan(EulerTimePlan(4, repetitions, parameter))
    assert sample.physical_target_enclosure.contains_interval(independent_density_enclosure(parameter))
    assert sample.plan.q != 3
    refined = canonical_parameter_interval(log_order=10)
    assert parameter.contains_interval(refined)
    assert refined.radius < parameter.radius


def test_fixed_q_is_not_a_fixed_temperature_refinement():
    parameter = certified_ln_interval(RationalInterval(3))
    assert (parameter * 2).hi < (parameter * 4).lo
    assert Fraction(meron_transfer_trace(4, 2, 3)) == 912


def test_zero_coupling_is_exact_and_the_scalar_correction_is_zero():
    sample = sample_time_plan(EulerTimePlan(4, 8, RationalInterval(0)))
    assert sample.unscaled_partition == 16
    assert sample.raw_density == sample.physical_density
    assert sample.plan.physical_density_error == 0
    assert sample.plan.thermodynamic_density_error == 0


def test_rate_and_parameter_radius_are_separate():
    point = RationalInterval(Fraction(1, 16))
    coarse, fine = EulerTimePlan(4, 4, point), EulerTimePlan(4, 8, point)
    assert fine.physical_density_error < coarse.physical_density_error / 2
    uncertain = EulerTimePlan(4, 4, RationalInterval.from_point(Fraction(1, 16), Fraction(1, 1000)))
    assert uncertain.physical_density_error - coarse.physical_density_error == Fraction(3, 4000)
    assert coarse.thermodynamic_density_error - coarse.physical_density_error == Fraction(3, 128)
    assert sample_time_plan(fine).thermodynamic_target_enclosure.contains_interval(
        sample_time_plan(fine).physical_target_enclosure)


@pytest.mark.parametrize("value", (True, 4.0))
def test_approximate_or_boolean_time_counts_refuse(value):
    with pytest.raises(TypeError):
        EulerTimePlan(4, value, RationalInterval(0))


@pytest.mark.parametrize("sites,repetitions", ((3, 2), (4, 0), (4, 257), (258, 2)))
def test_invalid_carrier_and_clock_bounds_refuse(sites, repetitions):
    with pytest.raises(ValueError):
        EulerTimePlan(sites, repetitions, RationalInterval(0))


def test_source_work_and_scalar_budgets_refuse_before_execution():
    with pytest.raises(ValueError, match="transfer resource"):
        sample_time_plan(EulerTimePlan(8, 3, RationalInterval(0)))
    with pytest.raises(ValueError, match="scalar resource"):
        EulerTimePlan(4, 2, RationalInterval(1 << 300))
    with pytest.raises(ValueError, match="nonnegative"):
        EulerTimePlan(4, 2, RationalInterval(-1))
