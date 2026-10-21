"""Majorana monomials and the two-mode CAR nilpotency identity.

Origin: lean4/FiniteQM.lean theorem car_clifford_nilpotency_and_occupation_projector.
The annihilation matrix is [[0, 1], [0, 0]] and its transpose is creation.
Claim: urn:omega:fqm:majorana:car-nilpotency-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/majorana/test_majorana_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: car_nilpotency_witness checks c^2 = 0, (c dagger)^2 = 0,
{c, c dagger} = I, and n = c dagger c is a rank-one projector. Majorana
monomials use gamma_i^2 = 1 and anticommutation for i distinct. This file
does not prove a braid-group image or a Kitaev-chain topological index.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Mapping


class MajoranaError(ValueError):
    """One violated Majorana or CAR invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> MajoranaError:
    return MajoranaError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the Majorana boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the Majorana boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


@dataclass(frozen=True)
class MajoranaMonomial:
    """Product of distinct modes gamma_{i_1} ... gamma_{i_k} with i_1 < ... < i_k."""

    modes: tuple[int, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "modes", _sorted_modes(self.modes))

    @classmethod
    def identity(cls) -> MajoranaMonomial:
        return cls(())

    @classmethod
    def single(cls, index: object) -> MajoranaMonomial:
        mode = _require_mode(index)
        return cls((mode,))

    def multiply(self, other: MajoranaMonomial) -> tuple[Fraction, MajoranaMonomial]:
        partner = _require_monomial(other)
        sign, merged = _multiply_modes(self.modes, partner.modes)
        return sign, MajoranaMonomial(merged)


def _require_mode(value: object) -> int:
    mode = _require_int(value, "mode")
    if mode < 0:
        raise _fail("Majorana mode is negative", mode=mode)
    return mode


def _require_monomial(value: object) -> MajoranaMonomial:
    if isinstance(value, MajoranaMonomial):
        return value
    raise _fail("value is not a Majorana monomial", received=type(value).__name__)


def _sorted_modes(modes: object) -> tuple[int, ...]:
    if isinstance(modes, (str, bytes)) or not isinstance(modes, tuple):
        raise _fail("modes are not a tuple", received=type(modes).__name__)
    parsed = tuple(_require_mode(item) for item in modes)
    ordered = tuple(sorted(parsed))
    if len(set(ordered)) != len(ordered):
        raise _fail("Majorana monomial repeats a mode")
    return ordered


def _multiply_modes(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[Fraction, tuple[int, ...]]:
    combined = list(left) + list(right)
    sign = _sort_sign(combined)
    return sign, _cancel_pairs(combined)


def _sort_sign(modes: list[int]) -> Fraction:
    sign = Fraction(1)
    span = len(modes)
    for start in range(span):
        sign = _bubble_pass(modes, sign, span - 1 - start)
    return sign


def _bubble_pass(modes: list[int], sign: Fraction, last: int) -> Fraction:
    current = sign
    for index in range(last):
        if modes[index] > modes[index + 1]:
            modes[index], modes[index + 1] = modes[index + 1], modes[index]
            current = -current
    return current


def _cancel_pairs(modes: list[int]) -> tuple[int, ...]:
    merged: list[int] = []
    index = 0
    while index < len(modes):
        index = _consume(modes, merged, index)
    return tuple(merged)


def _consume(modes: list[int], merged: list[int], index: int) -> int:
    if index + 1 < len(modes) and modes[index] == modes[index + 1]:
        return index + 2
    merged.append(modes[index])
    return index + 1


@dataclass(frozen=True)
class MajoranaOperator:
    """Finite rational linear combination of Majorana monomials."""

    terms: dict[MajoranaMonomial, Fraction] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "terms", _clean_terms(self.terms))

    @classmethod
    def zero(cls) -> MajoranaOperator:
        return cls({})

    @classmethod
    def identity(cls) -> MajoranaOperator:
        return cls({MajoranaMonomial.identity(): Fraction(1)})

    @classmethod
    def mode(cls, index: object) -> MajoranaOperator:
        return cls({MajoranaMonomial.single(index): Fraction(1)})

    def add(self, other: MajoranaOperator) -> MajoranaOperator:
        partner = _require_operator(other)
        merged = dict(self.terms)
        for monomial, coeff in partner.terms.items():
            _add_coeff(merged, monomial, coeff)
        return MajoranaOperator(merged)

    def multiply(self, other: MajoranaOperator) -> MajoranaOperator:
        partner = _require_operator(other)
        merged: dict[MajoranaMonomial, Fraction] = {}
        for left, left_coeff in self.terms.items():
            _multiply_into(merged, left, left_coeff, partner)
        return MajoranaOperator(merged)

    def is_zero(self) -> bool:
        return len(self.terms) == 0

    def is_scalar(self) -> bool:
        if len(self.terms) == 0:
            return True
        if len(self.terms) != 1:
            return False
        return MajoranaMonomial.identity() in self.terms

    def scalar_value(self) -> Fraction:
        return self.terms.get(MajoranaMonomial.identity(), Fraction(0))


def _clean_terms(terms: object) -> dict[MajoranaMonomial, Fraction]:
    if not isinstance(terms, dict):
        raise _fail("operator terms are not a dictionary", received=type(terms).__name__)
    cleaned: dict[MajoranaMonomial, Fraction] = {}
    for key, value in terms.items():
        monomial = _require_monomial(key)
        coeff = _require_fraction(value, "coefficient")
        if coeff != 0:
            cleaned[monomial] = coeff
    return cleaned


def _require_operator(value: object) -> MajoranaOperator:
    if isinstance(value, MajoranaOperator):
        return value
    raise _fail("value is not a Majorana operator", received=type(value).__name__)


def _add_coeff(terms: dict[MajoranaMonomial, Fraction], monomial: MajoranaMonomial, coeff: Fraction) -> None:
    total = terms.get(monomial, Fraction(0)) + coeff
    if total == 0:
        terms.pop(monomial, None)
        return
    terms[monomial] = total


def _multiply_into(
    terms: dict[MajoranaMonomial, Fraction],
    left: MajoranaMonomial,
    left_coeff: Fraction,
    other: MajoranaOperator,
) -> None:
    for right, right_coeff in other.terms.items():
        sign, product = left.multiply(right)
        _add_coeff(terms, product, left_coeff * right_coeff * sign)


def anticommutator(left: object, right: object) -> MajoranaOperator:
    """Return AB + BA."""
    first = _require_operator(left)
    second = _require_operator(right)
    return first.multiply(second).add(second.multiply(first))


def commutator(left: object, right: object) -> MajoranaOperator:
    """Return AB - BA."""
    first = _require_operator(left)
    second = _require_operator(right)
    negative = MajoranaOperator({monomial: -coeff for monomial, coeff in second.terms.items()})
    return first.multiply(second).add(negative.multiply(first))


def kitaev_chain_parity(num_sites: object) -> MajoranaOperator:
    """Return the monomial product gamma_0 gamma_1 ... gamma_{2N-1}."""
    sites = _require_int(num_sites, "sites")
    if sites < 0:
        raise _fail("Kitaev site count is negative", sites=sites)
    parity = MajoranaOperator.identity()
    for site in range(sites):
        parity = parity.multiply(MajoranaOperator.mode(2 * site)).multiply(MajoranaOperator.mode(2 * site + 1))
    return parity


def _mat_mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] * right[0][0] + left[0][1] * right[1][0], left[0][0] * right[0][1] + left[0][1] * right[1][1]),
        (left[1][0] * right[0][0] + left[1][1] * right[1][0], left[1][0] * right[0][1] + left[1][1] * right[1][1]),
    )


def _mat_add(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] + right[0][0], left[0][1] + right[0][1]),
        (left[1][0] + right[1][0], left[1][1] + right[1][1]),
    )


def car_nilpotency_witness() -> int:
    """Return 0 when the 2x2 CAR matrices match the cited theorem."""
    annihilate = ((0, 1), (0, 0))
    create = ((0, 0), (1, 0))
    zero = ((0, 0), (0, 0))
    identity = ((1, 0), (0, 1))
    if _mat_mul(annihilate, annihilate) != zero:
        raise _fail("annihilation matrix is not nilpotent")
    if _mat_mul(create, create) != zero:
        raise _fail("creation matrix is not nilpotent")
    if _mat_add(_mat_mul(annihilate, create), _mat_mul(create, annihilate)) != identity:
        raise _fail("CAR anticommutator is not the identity")
    number = _mat_mul(create, annihilate)
    if _mat_mul(number, number) != number:
        raise _fail("occupation matrix is not a projector")
    if number[0][0] + number[1][1] != 1:
        raise _fail("occupation trace is not one", trace=number[0][0] + number[1][1])
    determinant = number[0][0] * number[1][1] - number[0][1] * number[1][0]
    if determinant != 0:
        raise _fail("occupation determinant is not zero", determinant=determinant)
    return 0


def main() -> int:
    """Print the CAR nilpotency certificate."""
    try:
        print(car_nilpotency_witness())
    except MajoranaError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
