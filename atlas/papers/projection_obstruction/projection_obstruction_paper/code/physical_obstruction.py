"""Exact finite cycle certificates for the declared measurement model in §7.8.

These arithmetic checks neither certify a laboratory's error bound nor authorize
an action. The licensed repairs are cycle gradients, not physical state changes.
"""

from fractions import Fraction
from math import prod
from typing import Sequence


def _rational(value: object) -> Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError("exact integer or Fraction required")
    return Fraction(value)


def _cycle(values: Sequence[object]) -> tuple[Fraction, ...]:
    result = tuple(_rational(value) for value in values)
    if len(result) < 3:
        raise ValueError("a cycle needs at least three coordinates")
    return result


def cycle_gradient(potential: Sequence[object]) -> tuple[Fraction, ...]:
    values = _cycle(potential)
    return tuple(values[(j + 1) % len(values)] - value
                 for j, value in enumerate(values))


def cycle_quotient(cochain: Sequence[object]) -> Fraction:
    """Normalized l1 distance from a cochain to the cycle-gradient subspace."""
    values = _cycle(cochain)
    return abs(sum(values) / len(values))


def cycle_minimizer(cochain: Sequence[object]) -> tuple[Fraction, ...]:
    values = _cycle(cochain)
    mean = sum(values) / len(values)
    potential = [Fraction(0)]
    for value in values[:-1]:
        potential.append(potential[-1] + value - mean)
    return tuple(potential)


def verify_cycle_certificate(cochain: Sequence[object], potential: Sequence[object],
                             claimed_mass: object) -> bool:
    """Check the submitted primal witness and the independent circulation bound."""
    values, repair = _cycle(cochain), _cycle(potential)
    mass = _rational(claimed_mass)
    if len(values) != len(repair):
        raise ValueError("cochain and potential must have the same length")
    residual = tuple(x - y for x, y in zip(values, cycle_gradient(repair)))
    primal = sum(map(abs, residual)) / len(values)
    dual = abs(sum(values) / len(values))
    return mass >= 0 and primal == mass == dual


def product_moment_defect(joint: object, factors: Sequence[object]) -> Fraction:
    joint_value = _rational(joint)
    values = tuple(_rational(value) for value in factors)
    if len(values) < 2 or any(abs(value) > 1 for value in (joint_value, *values)):
        raise ValueError("at least two factors and moments in [-1, 1] required")
    return joint_value - prod(values)


def product_distance_lower_bound(cochain: Sequence[object], arity: int,
                                 reading_error: object = 0) -> Fraction:
    """Bound conditional on every measured moment having this error budget.

    The caller supplies corrected product-moment reports from supports of at
    most `arity` sites. No data acquisition or statistical coverage is inferred.
    """
    if type(arity) is not int or arity < 2:
        raise ValueError("integer arity of at least two required")
    error = _rational(reading_error)
    if error < 0:
        raise ValueError("nonnegative reading error required")
    values = _cycle(cochain)
    if any(abs(value) > 2 for value in values):
        raise ValueError("product-moment defects must lie in [-2, 2]")
    return max(Fraction(0), cycle_quotient(values) / (arity + 1) - error)
