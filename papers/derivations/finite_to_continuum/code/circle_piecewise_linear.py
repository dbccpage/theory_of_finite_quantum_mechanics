"""Exact periodic rational test profiles with derived norm, slope and integral."""
from dataclasses import dataclass
from fractions import Fraction as Q
from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    _validate_exact_int, _validate_exact_rational,
)


def _bounded_scalar(value):
    value = _validate_exact_rational(value, "circle scalar")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > 256:
        raise ValueError("bounded exact circle scalar required")
    return value


@dataclass(frozen=True)
class CirclePiecewiseLinear:
    knots: tuple

    def __post_init__(self):
        knots = tuple(tuple(knot) for knot in self.knots)
        if not 2 <= len(knots) <= 65 or any(len(knot) != 2 for knot in knots):
            raise ValueError("2..=65 pairs of circle knots required")
        knots = tuple((_bounded_scalar(t), _bounded_scalar(v)) for t, v in knots)
        if knots[0][0] != 0 or knots[-1][0] != 1 or any(
                left[0] >= right[0] for left, right in zip(knots, knots[1:])):
            raise ValueError("strictly ordered knots from 0 to 1 required")
        if knots[0][1] != knots[-1][1]:
            raise ValueError("circle endpoint values must agree")
        object.__setattr__(self, "knots", knots)

    @property
    def norm(self):
        return max(abs(v) for _, v in self.knots)

    @property
    def lipschitz(self):
        return max(abs(v1-v0)/(t1-t0) for (t0, v0), (t1, v1) in zip(self.knots, self.knots[1:]))

    @property
    def square_integral(self):
        return sum(((t1-t0)*(v0*v0+v0*v1+v1*v1)/3
                    for (t0, v0), (t1, v1) in zip(self.knots, self.knots[1:])), Q(0))

    def evaluate(self, turn):
        turn = _bounded_scalar(turn)
        phase = turn % 1
        for (t0, v0), (t1, v1) in zip(self.knots, self.knots[1:]):
            if t0 <= phase < t1:
                return v0+(v1-v0)*(phase-t0)/(t1-t0)
        raise AssertionError("validated circle cover failed")

    def uniform_samples(self, nodes):
        nodes = _validate_exact_int(nodes, "grid size")
        if not 1 <= nodes <= 256:
            raise ValueError("grid size must lie in 1..=256")
        return tuple(self.evaluate(Q(x, nodes)) for x in range(nodes))
