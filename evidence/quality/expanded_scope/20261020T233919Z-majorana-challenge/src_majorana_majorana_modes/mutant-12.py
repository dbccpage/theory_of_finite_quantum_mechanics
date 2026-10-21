"""Majorana basis blades and the single-fermion-mode CAR identity.

Origin: lean4/FiniteQM.lean theorem car_clifford_nilpotency_and_occupation_projector.
The annihilation matrix is [[0, 1], [0, 0]] and its transpose is creation.
Claim: urn:omega:fqm:majorana:car-nilpotency-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/majorana/test_majorana_control.py.
Gate 5: use the source-bound observations in the companion history.
Scope Fence: car_nilpotency_witness checks c^2 = 0, (c dagger)^2 = 0,
{c, c dagger} = I, and n = c dagger c is a rank-one projector. Majorana
monomials use gamma_i^2 = 1 and anticommutation for i distinct. This file
does not prove a braid-group image or a Kitaev-chain topological index.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Mapping

# Declared admission/work policies, not derived physics constants.
MAX_INTEGER_BITS = 1024
MAX_MONOMIAL_MODES = 256
MAX_OPERATOR_TERMS = 4096
MAX_TERM_PRODUCTS = 65536
MAX_TERM_MODE_WORK = 1_000_000
MAX_COEFFICIENT_BITS = 1024
MAX_WORK_BITS = 8192
_ABSENT = object()


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
    if issubclass(type(value), float):
        raise _fail("float refused at the Majorana boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer was required", role=role)
    if type(value) is int:
        if value.bit_length() > MAX_INTEGER_BITS:
            raise _fail("integer bit budget exceeded", role=role, limit=MAX_INTEGER_BITS)
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if issubclass(type(value), float):
        raise _fail("float refused at the Majorana boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if type(value) is Fraction:
        return _coefficient_bits(value, role, MAX_COEFFICIENT_BITS)
    if type(value) is int:
        if value.bit_length() > MAX_COEFFICIENT_BITS:
            raise _fail("coefficient bit budget exceeded", role=role, limit=MAX_COEFFICIENT_BITS)
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _coefficient_bits(value: Fraction, role: str, limit: int) -> Fraction:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > limit:
        raise _fail("coefficient bit budget exceeded", role=role, limit=limit)
    return value


@dataclass(frozen=True, slots=True, init=False, eq=False)
class MajoranaMonomial:
    """Canonical basis blade. Constructor order labels a set, not an ordered word."""

    modes: tuple[int, ...]

    def __init__(self, modes: object) -> None:
        if hasattr(self, "modes"):
            raise _fail("Majorana monomial already initialized")
        object.__setattr__(self, "modes", _sorted_modes(modes))

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("MajoranaMonomial does not admit subclasses")

    def __eq__(self, other: object) -> bool:
        return type(other) is MajoranaMonomial and self.modes == other.modes

    def __hash__(self) -> int:
        return hash(self.modes)

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
    if type(value) is MajoranaMonomial:
        return value
    raise _fail("value is not a Majorana monomial", received=type(value).__name__)


def _sorted_modes(modes: object) -> tuple[int, ...]:
    if type(modes) is not tuple:
        raise _fail("modes are not a tuple", received=type(modes).__name__)
    if len(modes) > MAX_MONOMIAL_MODES:
        raise _fail("monomial degree budget exceeded", limit=MAX_MONOMIAL_MODES)
    parsed = tuple(_require_mode(item) for item in modes)
    ordered = tuple(sorted(parsed))
    if len(set(ordered)) != len(ordered):
        raise _fail("Majorana monomial repeats a mode")
    return ordered


def _multiply_modes(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[Fraction, tuple[int, ...]]:
    crossings = sum(len(left) - bisect_right(left, mode) for mode in right)
    merged = tuple(sorted(set(left).symmetric_difference(right)))
    if len(merged) > MAX_MONOMIAL_MODES:
        raise _fail("monomial degree budget exceeded", limit=MAX_MONOMIAL_MODES)
    return Fraction(-1 if crossings % 2 == 0 else 1), merged


@dataclass(frozen=True, slots=True, init=False, eq=False)
class MajoranaOperator:
    """Finite rational linear combination of Majorana monomials."""

    _terms: Mapping[MajoranaMonomial, Fraction]

    def __init__(self, terms: object = _ABSENT) -> None:
        if hasattr(self, "_terms"):
            raise _fail("Majorana operator already initialized")
        object.__setattr__(self, "_terms", MappingProxyType(_clean_terms({} if terms is _ABSENT else terms)))

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("MajoranaOperator does not admit subclasses")

    @property
    def terms(self) -> dict[MajoranaMonomial, Fraction]:
        """Detached export. Arithmetic uses the owned immutable table."""
        return dict(self._terms)

    def __eq__(self, other: object) -> bool:
        return type(other) is MajoranaOperator and self._terms == other._terms

    __hash__ = None

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
        merged = dict(self._terms)
        for monomial, coeff in partner._terms.items():
            _add_coeff(merged, monomial, coeff)
        return MajoranaOperator(merged)

    def multiply(self, other: MajoranaOperator) -> MajoranaOperator:
        partner = _require_operator(other)
        _product_budget(self, partner)
        merged: dict[MajoranaMonomial, Fraction] = {}
        for left, left_coeff in self._terms.items():
            _multiply_into(merged, left, left_coeff, partner)
        return MajoranaOperator(merged)

    def is_zero(self) -> bool:
        return len(self._terms) == 0

    def is_scalar(self) -> bool:
        if len(self._terms) == 0:
            return True
        if len(self._terms) != 1:
            return False
        return MajoranaMonomial.identity() in self._terms

    def scalar_value(self) -> Fraction:
        """Identity coefficient; this does not assert that the operator is scalar."""
        return self._terms.get(MajoranaMonomial.identity(), Fraction(0))


def _clean_terms(terms: object) -> dict[MajoranaMonomial, Fraction]:
    if type(terms) is not dict:
        raise _fail("operator terms are not a dictionary", received=type(terms).__name__)
    if len(terms) > MAX_OPERATOR_TERMS:
        raise _fail("operator term budget exceeded", limit=MAX_OPERATOR_TERMS)
    cleaned: dict[MajoranaMonomial, Fraction] = {}
    for key, value in terms.items():
        monomial = _require_monomial(key)
        coeff = _require_fraction(value, "coefficient")
        if coeff != 0:
            cleaned[monomial] = coeff
    return cleaned


def _require_operator(value: object) -> MajoranaOperator:
    if type(value) is MajoranaOperator:
        return value
    raise _fail("value is not a Majorana operator", received=type(value).__name__)


def _add_coeff(terms: dict[MajoranaMonomial, Fraction], monomial: MajoranaMonomial, coeff: Fraction) -> None:
    _coefficient_bits(coeff, "product", MAX_WORK_BITS)
    total = _coefficient_bits(terms.get(monomial, Fraction(0)) + coeff, "sum", MAX_WORK_BITS)
    if total == 0:
        terms.pop(monomial, None)
        return
    if monomial not in terms and len(terms) >= MAX_OPERATOR_TERMS:
        raise _fail("operator term budget exceeded", limit=MAX_OPERATOR_TERMS)
    terms[monomial] = total


def _product_budget(left: MajoranaOperator, right: MajoranaOperator) -> None:
    a, b = len(left._terms), len(right._terms)
    if a * b > MAX_TERM_PRODUCTS:
        raise _fail("operator product budget exceeded", limit=MAX_TERM_PRODUCTS)
    work = b * sum(len(m.modes) for m in left._terms) + a * sum(len(m.modes) for m in right._terms)
    if work > MAX_TERM_MODE_WORK:
        raise _fail("operator mode-work budget exceeded", limit=MAX_TERM_MODE_WORK)


def _multiply_into(
    terms: dict[MajoranaMonomial, Fraction],
    left: MajoranaMonomial,
    left_coeff: Fraction,
    other: MajoranaOperator,
) -> None:
    for right, right_coeff in other._terms.items():
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
    if sites > MAX_MONOMIAL_MODES // 2:
        raise _fail("Kitaev parity degree budget exceeded", limit=MAX_MONOMIAL_MODES // 2)
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
        try:
            print(error.invariant)
        except (OSError, ValueError):
            return 2
        return 1
    except (OSError, ValueError):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
