"""Rational probability simplex and the Bool half-weight witness.

Origin: lean4/H001Rats.lean theorem fractional_half_simplex
(uniformHalf on Bool sums to one, half ≠ 0, half ≠ 1, and the half
numerator is nonnegative) and theorem half_add_half (half + half = 1).
Claim: urn:omega:fqm:simplex:fractional-half:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_half_simplex.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: half_simplex_mass checks those conjuncts on uniform(2) and
returns 1. ProbabilitySimplex, total variation, mixture, expectation, and
StochasticMap are exact rational operations and are not ScaledProb and not
the cited half theorem. This file does not prove H001Rats.lean.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping


class SimplexError(ValueError):
    """One violated simplex invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SimplexError:
    return SimplexError(invariant, parameters)


def _refuse_non_exact(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the simplex boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an exact rational was required", role=role)


def _require_int(value: object, role: str) -> int:
    _refuse_non_exact(value, role)
    if type(value) is int:
        return value
    raise _fail("count is not an integer", role=role, received=type(value).__name__)


def _require_positive_int(value: object, role: str) -> int:
    number = _require_int(value, role)
    if number <= 0:
        raise _fail("count is not positive", role=role, value=number)
    return number


def _pair_fraction(value: tuple[object, ...], role: str) -> Fraction:
    if len(value) != 2:
        raise _fail("ratio is not a pair", role=role, length=len(value))
    numerator = _require_int(value[0], role)
    denominator = _require_int(value[1], role)
    if denominator == 0:
        raise _fail("ratio denominator is zero", role=role)
    return Fraction(numerator, denominator)


def _require_fraction(value: object, role: str) -> Fraction:
    _refuse_non_exact(value, role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, tuple):
        return _pair_fraction(value, role)
    raise _fail("mass is not an exact rational", role=role, received=type(value).__name__)


def _require_sequence(values: object, role: str) -> tuple[object, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise _fail("masses are not a sequence", role=role, received=type(values).__name__)
    return tuple(values)


def _require_nonempty(values: tuple[object, ...], role: str) -> None:
    if len(values) == 0:
        raise _fail("masses are empty", role=role)


def _sum(masses: list[Fraction]) -> Fraction:
    total = Fraction(0)
    for mass in masses:
        total += mass
    return total


def _require_nonnegative(mass: Fraction, role: str) -> None:
    if mass < 0:
        raise _fail("mass is negative", role=role, mass=str(mass))


def _require_unit_total(total: Fraction, role: str) -> None:
    if total != Fraction(1):
        raise _fail("mass is not one", role=role, total=str(total))


def _parse_distribution(probs: object) -> list[Fraction]:
    entries = _require_sequence(probs, "distribution")
    _require_nonempty(entries, "distribution")
    parsed: list[Fraction] = []
    for index, entry in enumerate(entries):
        mass = _require_fraction(entry, f"distribution[{index}]")
        _require_nonnegative(mass, f"distribution[{index}]")
        parsed.append(mass)
    _require_unit_total(_sum(parsed), "distribution")
    return parsed


def _require_label(label: object) -> str:
    if type(label) is str:
        return label
    raise _fail("label is not a string", received=type(label).__name__)


def _require_half(mass: Fraction) -> Fraction:
    if mass != Fraction(1, 2):
        raise _fail("half weight is not 1/2", mass=str(mass))
    if mass == 0 or mass == 1:
        raise _fail("half weight collapsed", mass=str(mass))
    if mass.numerator < 0:
        raise _fail("half numerator is negative", numerator=mass.numerator)
    return mass


class ProbabilitySimplex:
    """Exact rational distribution on a finite set. The masses sum to 1."""

    def __init__(self, probs: object, label: str = "") -> None:
        self._probs = _parse_distribution(probs)
        self.label = _require_label(label)

    @classmethod
    def uniform(cls, n: object, label: str = "uniform") -> ProbabilitySimplex:
        count = _require_positive_int(n, "dimension")
        mass = Fraction(1, count)
        return cls([mass] * count, label)

    @classmethod
    def dirac(cls, n: object, index: object, label: str = "dirac") -> ProbabilitySimplex:
        count = _require_positive_int(n, "dimension")
        slot = _require_int(index, "index")
        if slot < 0 or slot >= count:
            raise _fail("dirac index is outside the set", index=slot, dimension=count)
        probs = [Fraction(0)] * count
        probs[slot] = Fraction(1)
        return cls(probs, label)

    @property
    def dim(self) -> int:
        return len(self._probs)

    @property
    def probs(self) -> list[Fraction]:
        return list(self._probs)

    def __getitem__(self, index: int) -> Fraction:
        return self._probs[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProbabilitySimplex):
            return False
        return self._probs == other._probs

    def total_variation_distance(self, other: object) -> Fraction:
        """Return one half of the L1 distance to another distribution."""
        target = _require_simplex(other)
        if self.dim != target.dim:
            raise _fail("dimensions differ", left=self.dim, right=target.dim)
        return _variation(self._probs, target._probs)

    def mixture(self, other: object, weight: object) -> ProbabilitySimplex:
        """Return w * self + (1 - w) * other."""
        target = _require_simplex(other)
        share = _require_fraction(weight, "weight")
        if share < 0 or share > 1:
            raise _fail("mixture weight is outside the unit interval", weight=str(share))
        if self.dim != target.dim:
            raise _fail("dimensions differ", left=self.dim, right=target.dim)
        mixed = _mix(self._probs, target._probs, share)
        return ProbabilitySimplex(mixed, f"mix({self.label},{target.label})")

    def expectation(self, values: object) -> Fraction:
        entries = _require_sequence(values, "values")
        if len(entries) != self.dim:
            raise _fail("values length differs", length=len(entries), dimension=self.dim)
        return _expectation(self._probs, entries)


def _require_simplex(value: object) -> ProbabilitySimplex:
    if not isinstance(value, ProbabilitySimplex):
        raise _fail("value is not a probability simplex", received=type(value).__name__)
    return value


def _variation(left: list[Fraction], right: list[Fraction]) -> Fraction:
    total = Fraction(0)
    for mass, other in zip(left, right, strict=True):
        total += abs(mass - other)
    return total / 2


def _mix(left: list[Fraction], right: list[Fraction], share: Fraction) -> list[Fraction]:
    mixed: list[Fraction] = []
    gap = Fraction(1) - share
    for mass, other in zip(left, right, strict=True):
        mixed.append(share * mass + gap * other)
    return mixed


def _expectation(masses: list[Fraction], values: tuple[object, ...]) -> Fraction:
    total = Fraction(0)
    for index, mass in enumerate(masses):
        total += mass * _require_fraction(values[index], f"values[{index}]")
    return total


def _row_width(row: object) -> int:
    entries = _require_sequence(row, "row0")
    _require_nonempty(entries, "row0")
    return len(entries)


def _parse_row(row: object, width: int, index: int) -> list[Fraction]:
    entries = _require_sequence(row, f"row{index}")
    if len(entries) != width:
        raise _fail("row width differs", role=f"row{index}", length=len(entries), width=width)
    parsed: list[Fraction] = []
    for column, entry in enumerate(entries):
        mass = _require_fraction(entry, f"row{index}[{column}]")
        _require_nonnegative(mass, f"row{index}[{column}]")
        parsed.append(mass)
    _require_unit_total(_sum(parsed), f"row{index}")
    return parsed


def _parse_matrix(matrix: object) -> list[list[Fraction]]:
    rows = _require_sequence(matrix, "matrix")
    _require_nonempty(rows, "matrix")
    width = _row_width(rows[0])
    return [_parse_row(row, width, index) for index, row in enumerate(rows)]


class StochasticMap:
    """Row-stochastic matrix with exact rational entries."""

    def __init__(self, matrix: object) -> None:
        parsed = _parse_matrix(matrix)
        self.rows = len(parsed)
        self.cols = len(parsed[0])
        self._data = parsed

    def apply(self, dist: object) -> ProbabilitySimplex:
        """Push a distribution forward along the rows."""
        source = _require_simplex(dist)
        if source.dim != self.rows:
            raise _fail("distribution width differs", left=source.dim, right=self.rows)
        pushed = _push(self._data, source)
        return ProbabilitySimplex(pushed)


def _push(data: list[list[Fraction]], source: ProbabilitySimplex) -> list[Fraction]:
    width = len(data[0])
    out: list[Fraction] = []
    for column in range(width):
        total = Fraction(0)
        for row in range(len(data)):
            total += source[row] * data[row][column]
        out.append(total)
    return out


def half_simplex_mass() -> Fraction:
    """Return the total mass of the Bool half-weight simplex, which is 1."""
    simplex = ProbabilitySimplex.uniform(2)
    left = _require_half(simplex[0])
    right = _require_half(simplex[1])
    total = left + right
    _require_unit_total(total, "half")
    return total


def main() -> int:
    value = half_simplex_mass()
    print(value)
    if value == Fraction(1):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
