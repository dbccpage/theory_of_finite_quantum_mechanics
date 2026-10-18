"""Gaussian-rational amplitude bridge and the parallelogram identity.

Origin: lean4/H010Scale.lean theorem nsq_parallelogram
(N(z+w) + N(z-w) = 2 (N(z) + N(w)) for Gaussian integers).
Claim: urn:omega:fqm:amplitude:parallelogram-bridge:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/wdp/test_amplitude_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: parallelogram_defect checks the identity on Q(i), which
specializes the cited Gaussian-integer theorem. The unit u = (3+4i)/5 and
the gauge-invariant cycle holonomy are exact powers in Q(i). This file does
not prove that every power of u is nontrivial for a reason beyond direct
evaluation of the requested exponent, and it does not prove H010Scale.lean.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Mapping


AUTHORITY_FENCE = (
    "AuthorityEffect None; not PROVED; integer cochain amplitude bridge."
)


class AmplitudeError(KeyError):
    """One violated amplitude-bridge invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> AmplitudeError:
    return AmplitudeError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the amplitude boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the amplitude boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


@dataclass(frozen=True)
class GaussianRational:
    """Exact Gaussian rational z = re + im * i."""

    re: Fraction
    im: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "re", _require_fraction(self.re, "real part"))
        object.__setattr__(self, "im", _require_fraction(self.im, "imaginary part"))

    @classmethod
    def from_integers(cls, real: object, imag: object = 0) -> GaussianRational:
        return cls(_require_fraction(real, "real part"), _require_fraction(imag, "imaginary part"))

    def __add__(self, other: GaussianRational) -> GaussianRational:
        partner = _require_gaussian(other, "addend")
        return GaussianRational(self.re + partner.re, self.im + partner.im)

    def __sub__(self, other: GaussianRational) -> GaussianRational:
        partner = _require_gaussian(other, "subtrahend")
        return GaussianRational(self.re - partner.re, self.im - partner.im)

    def __mul__(self, other: GaussianRational) -> GaussianRational:
        partner = _require_gaussian(other, "factor")
        real = self.re * partner.re - self.im * partner.im
        imag = self.re * partner.im + self.im * partner.re
        return GaussianRational(real, imag)

    def conj(self) -> GaussianRational:
        return GaussianRational(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GaussianRational):
            return False
        return self.re == other.re and self.im == other.im

    def __hash__(self) -> int:
        return hash((self.re, self.im))


def _require_gaussian(value: object, role: str) -> GaussianRational:
    if isinstance(value, GaussianRational):
        return value
    raise _fail("value is not a Gaussian rational", role=role, received=type(value).__name__)


U_PHASE = GaussianRational(Fraction(3, 5), Fraction(4, 5))


def u_pow(exponent: object) -> GaussianRational:
    """Return u^n for u = (3 + 4i)/5."""
    power = _require_int(exponent, "exponent")
    if power == 0:
        return GaussianRational(Fraction(1), Fraction(0))
    if power < 0:
        return u_pow(-power).conj()
    return _positive_power(power)


def _positive_power(exponent: int) -> GaussianRational:
    result = GaussianRational(Fraction(1), Fraction(0))
    base = U_PHASE
    remaining = exponent
    while remaining > 0:
        result, base, remaining = _power_step(result, base, remaining)
    return result


def _power_step(
    result: GaussianRational,
    base: GaussianRational,
    remaining: int,
) -> tuple[GaussianRational, GaussianRational, int]:
    if remaining % 2 == 1:
        result = result * base
    return result, base * base, remaining // 2


def u_power_is_never_one(exponent: object) -> bool:
    """Return whether u^n is distinct from 1 for this positive exponent."""
    power = _require_int(exponent, "exponent")
    if power < 1:
        return False
    value = u_pow(power)
    return not (value.re == Fraction(1) and value.im == Fraction(0))


@dataclass
class OrientedGraph:
    """Oriented graph with integer edge weights and transport by u."""

    vertices: set[str] = field(default_factory=set)
    edge_weights: dict[tuple[str, str], int] = field(default_factory=dict)

    def add_vertex(self, vertex: object) -> None:
        self.vertices.add(_require_vertex(vertex))

    def add_edge(self, source: object, target: object, weight: object) -> None:
        start = _require_vertex(source)
        end = _require_vertex(target)
        self.vertices.add(start)
        self.vertices.add(end)
        self.edge_weights[(start, end)] = _require_int(weight, "weight")

    def edge_transport(self, source: object, target: object) -> GaussianRational:
        start = _require_vertex(source)
        end = _require_vertex(target)
        forward = self.edge_weights.get((start, end))
        if forward is not None:
            return u_pow(forward)
        backward = self.edge_weights.get((end, start))
        if backward is not None:
            return u_pow(-backward)
        raise _fail("edge is not in the graph", source=start, target=end)

    def cycle_holonomy(self, path: object) -> GaussianRational:
        steps = _parse_path(path)
        holonomy = GaussianRational(Fraction(1), Fraction(0))
        for source, target in steps:
            holonomy = holonomy * self.edge_transport(source, target)
        return holonomy

    def gauge_transform(self, potential: object) -> OrientedGraph:
        values = _parse_potential(potential)
        gauged = OrientedGraph(vertices=set(self.vertices))
        for (source, target), weight in self.edge_weights.items():
            gauged.add_edge(source, target, weight + _lookup(values, target) - _lookup(values, source))
        return gauged


def _require_vertex(value: object) -> str:
    if isinstance(value, str) and value != "":
        return value
    raise _fail("vertex is not a non-empty string", received=type(value).__name__)


def _parse_path(path: object) -> tuple[tuple[str, str], ...]:
    if isinstance(path, (str, bytes)) or not isinstance(path, (list, tuple)):
        raise _fail("path is not a sequence", received=type(path).__name__)
    steps: list[tuple[str, str]] = []
    for index, item in enumerate(path):
        steps.append(_parse_step(item, index))
    return tuple(steps)


def _parse_step(item: object, index: int) -> tuple[str, str]:
    if isinstance(item, (str, bytes)) or not isinstance(item, (list, tuple)) or len(item) != 2:
        raise _fail("path step is not a pair", index=index, received=type(item).__name__)
    return (_require_vertex(item[0]), _require_vertex(item[1]))


def _parse_potential(potential: object) -> dict[str, int]:
    if not isinstance(potential, dict):
        raise _fail("gauge potential is not a dictionary", received=type(potential).__name__)
    parsed: dict[str, int] = {}
    for key, value in potential.items():
        parsed[_require_vertex(key)] = _require_int(value, "potential")
    return parsed


def _lookup(potential: dict[str, int], vertex: str) -> int:
    if vertex in potential:
        return potential[vertex]
    return 0


def readout_quadratic(left: object, right: object) -> Fraction:
    """Return N(z1 + z2)."""
    return (_require_gaussian(left, "left") + _require_gaussian(right, "right")).norm_sq()


def readout_quartic(left: object, right: object) -> Fraction:
    """Return N(z1 + z2)^2."""
    norm = readout_quadratic(left, right)
    return norm * norm


def parallelogram_defect(left: object, right: object) -> Fraction:
    """Return N(z+w) + N(z-w) - 2(N(z)+N(w))."""
    zed = _require_gaussian(left, "left")
    double = _require_gaussian(right, "right")
    summed = (zed + double).norm_sq() + (zed - double).norm_sq()
    expected = 2 * (zed.norm_sq() + double.norm_sq())
    return summed - expected


def parallelogram_witness() -> int:
    """Return 0 when the parallelogram identity holds on the Gaussian integer pair (1, i)."""
    left = GaussianRational.from_integers(1, 0)
    right = GaussianRational.from_integers(0, 1)
    defect = parallelogram_defect(left, right)
    if defect != 0:
        raise _fail("parallelogram defect is nonzero", defect=str(defect))
    if U_PHASE.norm_sq() != Fraction(1):
        raise _fail("unit phase norm is not one", norm=str(U_PHASE.norm_sq()))
    return 0


def main() -> int:
    """Print the parallelogram certificate."""
    try:
        print(parallelogram_witness())
    except AmplitudeError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
