"""Independent occupation transfer for the actual time-integrated SQL observable.

The exact block representation carries two derivatives of an insertion curve.
This finite companion supplies no spatial scaling or estimator error law.
"""
from dataclasses import dataclass
from fractions import Fraction

from sympy import SparseMatrix, eye, zeros

from omega_engine_projects.finite_to_continuum.code.interval_calculus import (
    _validate_exact_int, _validate_exact_rational,
)
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import hop_sign, rational


@dataclass(frozen=True)
class StaggeredMoments:
    partition: Fraction
    first: Fraction
    second: Fraction
    slices: int

    @property
    def mean_square(self):
        return self.second / (self.slices ** 2 * self.partition)


def _validated_occupation_query(sites, repetitions, q):
    sites = _validate_exact_int(sites, "sites")
    repetitions = _validate_exact_int(repetitions, "repetitions")
    q = rational(q)
    if sites not in (4, 6) or not 1 <= repetitions <= 16:
        raise ValueError("bounded even chain and time count required")
    if sites * repetitions * (1 << (2 * sites)) > 1 << 18:
        raise ValueError("finite occupation work limit")
    if q < 1 or max(q.numerator.bit_length(), q.denominator.bit_length()) > 256:
        raise ValueError("bounded q>=1 required")
    return sites, repetitions, q


def _occupation_layers(sites, q):
    """Shared exact occupation layers, after bounded query validation."""
    dimension = 1 << sites
    values = [sum((1 if x % 2 == 0 else -1) * Fraction(2 * ((state >> x) & 1) - 1, 2)
                  for x in range(sites)) for state in range(dimension)]
    insertion = SparseMatrix.diag(*values)
    layers = []
    for parity in range(2):
        layer = SparseMatrix(eye(dimension))
        for x in range(parity, sites, 2):
            y = (x + 1) % sites
            entries = {}
            for state in range(dimension):
                mixed = ((state >> x) ^ (state >> y)) & 1
                entries[state, state] = (q + 1) / 2 if mixed else 1
                if mixed:
                    entries[state ^ (1 << x) ^ (1 << y), state] = (q - 1) / 2 * hop_sign(state, x, y)
            layer = SparseMatrix(dimension, dimension, entries) * layer
        layers.append(layer)
    return insertion, layers


def staggered_moments(sites, repetitions, q):
    sites, repetitions, q = _validated_occupation_query(sites, repetitions, q)
    dimension = 1 << sites
    insertion, layers = _occupation_layers(sites, q)
    return _insertion_moments(repetitions, insertion, layers)


def weighted_staggered_moments(sites, repetitions, q, weights):
    sites, repetitions, q = _validated_occupation_query(sites, repetitions, q)
    weights = tuple(_validate_exact_rational(value, "spatial weight") for value in weights)
    if len(weights) != sites or any(max(v.numerator.bit_length(), v.denominator.bit_length()) > 256
                                   for v in weights):
        raise ValueError("one bounded exact spatial weight per site required")
    _, layers = _occupation_layers(sites, q)
    values = [sum((1 if x % 2 == 0 else -1) * weights[x]
                  * Fraction(2*((state >> x) & 1)-1, 2) for x in range(sites))
              for state in range(1 << sites)]
    return _insertion_moments(repetitions, SparseMatrix.diag(*values), layers)


def _insertion_moments(repetitions, insertion, layers):
    dimension = insertion.rows
    insertion2 = insertion * insertion
    zero = SparseMatrix(zeros(dimension))
    lifted = []
    for layer in layers:
        first = layer * insertion
        second = layer * insertion2
        lifted.append(SparseMatrix.vstack(
            SparseMatrix.hstack(layer, zero, zero),
            SparseMatrix.hstack(first, layer, zero),
            SparseMatrix.hstack(second, 2 * first, layer)))
    product = SparseMatrix(eye(3 * dimension))
    for time in range(2 * repetitions):
        product = lifted[time % 2] * product
    traces = [Fraction(str(sum(product[order * dimension + i, i] for i in range(dimension))))
              for order in range(3)]
    return StaggeredMoments(*traces, 2 * repetitions)
