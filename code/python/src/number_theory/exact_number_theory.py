"""Exact Q[x] arithmetic, cyclotomic polynomials, and the conductor 120.

Origin: lean4/CyclotomicTowerDirected.lean theorem cyclotomic_tower_is_directed,
theorem subfield_inclusion_trans, and theorem all_targets_embed_in_lcm_conductor.
targetConductors is 1, 2, 3, 4, 5, 8, 12 and targetLcmConductor is 120.
Claim: urn:omega:fqm:number:conductor-120-divisibility:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/number_theory/test_number_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: conductor_lcm_witness checks that each listed conductor divides
120. Phi_n is the monic divisor recurrence for x^n - 1. Quadratic norm and
trace are the field operations of Q(sqrt(d)). This file does not prove the
cyclotomic tower embedding and does not prove Kronecker-Weber.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


TARGET_CONDUCTORS: tuple[int, ...] = (1, 2, 3, 4, 5, 8, 12)
TARGET_LCM_CONDUCTOR: int = 120


class NumberTheoryError(ValueError):
    """One violated number-theory invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> NumberTheoryError:
    return NumberTheoryError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the number boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the number boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


@dataclass(frozen=True)
class ExactPolynomial:
    """Univariate polynomial over Q, low degree first."""

    coeffs: tuple[Fraction, ...]

    @classmethod
    def from_ints(cls, *values: object) -> ExactPolynomial:
        parsed = tuple(_require_fraction(item, f"coefficient[{index}]") for index, item in enumerate(values))
        return cls(parsed).canonical()

    @classmethod
    def zero(cls) -> ExactPolynomial:
        return cls(())

    @classmethod
    def one(cls) -> ExactPolynomial:
        return cls((Fraction(1),))

    @classmethod
    def x(cls) -> ExactPolynomial:
        return cls((Fraction(0), Fraction(1)))

    def canonical(self) -> ExactPolynomial:
        trimmed = list(self.coeffs)
        while trimmed and trimmed[-1] == 0:
            trimmed.pop()
        return ExactPolynomial(tuple(trimmed))

    @property
    def degree(self) -> int:
        canonical = self.canonical()
        if not canonical.coeffs:
            return -1
        return len(canonical.coeffs) - 1

    def is_zero(self) -> bool:
        return self.degree < 0

    def leading_coeff(self) -> Fraction:
        canonical = self.canonical()
        if not canonical.coeffs:
            return Fraction(0)
        return canonical.coeffs[-1]

    def __add__(self, other: ExactPolynomial) -> ExactPolynomial:
        partner = _require_polynomial(other, "addend")
        return _linear_combine(self.coeffs, partner.coeffs, 1)

    def __sub__(self, other: ExactPolynomial) -> ExactPolynomial:
        partner = _require_polynomial(other, "subtrahend")
        return _linear_combine(self.coeffs, partner.coeffs, -1)

    def __mul__(self, other: ExactPolynomial) -> ExactPolynomial:
        partner = _require_polynomial(other, "factor")
        if self.is_zero() or partner.is_zero():
            return ExactPolynomial.zero()
        return _multiply(self.coeffs, partner.coeffs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExactPolynomial):
            return False
        return self.canonical().coeffs == other.canonical().coeffs

    def __hash__(self) -> int:
        return hash(self.canonical().coeffs)

    def divmod(self, divisor: ExactPolynomial) -> tuple[ExactPolynomial, ExactPolynomial]:
        partner = _require_polynomial(divisor, "divisor")
        if partner.is_zero():
            raise _fail("polynomial divisor is zero")
        if self.degree < partner.degree:
            return ExactPolynomial.zero(), self.canonical()
        return _divide(self.canonical().coeffs, partner.canonical().coeffs)

    def make_monic(self) -> ExactPolynomial:
        lead = self.leading_coeff()
        if lead == 0:
            return self
        scaled = tuple(coeff / lead for coeff in self.coeffs)
        return ExactPolynomial(scaled).canonical()

    def gcd(self, other: ExactPolynomial) -> ExactPolynomial:
        partner = _require_polynomial(other, "gcd partner")
        return _euclidean(self.canonical(), partner.canonical()).make_monic()

    @classmethod
    def cyclotomic(cls, degree: object) -> ExactPolynomial:
        width = _require_int(degree, "cyclotomic degree")
        if width < 1:
            raise _fail("cyclotomic degree is smaller than 1", degree=width)
        body = _xn_minus_one(width)
        for divisor in range(1, width):
            body = _divide_proper_divisor(body, divisor, width)
        return body.make_monic()


def _require_polynomial(value: object, role: str) -> ExactPolynomial:
    if isinstance(value, ExactPolynomial):
        return value
    raise _fail("value is not a polynomial", role=role, received=type(value).__name__)


def _linear_combine(left: tuple[Fraction, ...], right: tuple[Fraction, ...], sign: int) -> ExactPolynomial:
    width = max(len(left), len(right))
    combined: list[Fraction] = []
    for index in range(width):
        combined.append(_coeff_at(left, index) + sign * _coeff_at(right, index))
    return ExactPolynomial(tuple(combined)).canonical()


def _coeff_at(coeffs: tuple[Fraction, ...], index: int) -> Fraction:
    if index < len(coeffs):
        return coeffs[index]
    return Fraction(0)


def _multiply(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> ExactPolynomial:
    width = len(left) + len(right) - 1
    product = [Fraction(0)] * width
    for left_index, left_coeff in enumerate(left):
        _accumulate_product(product, right, left_index, left_coeff)
    return ExactPolynomial(tuple(product)).canonical()


def _accumulate_product(product: list[Fraction], right: tuple[Fraction, ...], left_index: int, left_coeff: Fraction) -> None:
    for right_index, right_coeff in enumerate(right):
        product[left_index + right_index] += left_coeff * right_coeff


def _divide(dividend: tuple[Fraction, ...], divisor: tuple[Fraction, ...]) -> tuple[ExactPolynomial, ExactPolynomial]:
    remainder = list(dividend)
    degree_gap = len(dividend) - len(divisor)
    quotient = [Fraction(0)] * (degree_gap + 1)
    lead = divisor[-1]
    while len(remainder) >= len(divisor):
        _division_step(remainder, quotient, divisor, lead)
    return ExactPolynomial(tuple(quotient)).canonical(), ExactPolynomial(tuple(remainder)).canonical()


def _division_step(remainder: list[Fraction], quotient: list[Fraction], divisor: tuple[Fraction, ...], lead: Fraction) -> None:
    shift = len(remainder) - len(divisor)
    scale = remainder[-1] / lead
    quotient[shift] = scale
    for index, coeff in enumerate(divisor):
        remainder[shift + index] -= scale * coeff
    while remainder and remainder[-1] == 0:
        remainder.pop()


def _euclidean(left: ExactPolynomial, right: ExactPolynomial) -> ExactPolynomial:
    current = left
    other = right
    while not other.is_zero():
        _unused, remainder = current.divmod(other)
        current, other = other, remainder
    return current


def _xn_minus_one(degree: int) -> ExactPolynomial:
    coeffs = [-Fraction(1)] + [Fraction(0)] * (degree - 1) + [Fraction(1)]
    return ExactPolynomial(tuple(coeffs))


def _divide_proper_divisor(body: ExactPolynomial, divisor: int, degree: int) -> ExactPolynomial:
    if degree % divisor != 0:
        return body
    quotient, remainder = body.divmod(ExactPolynomial.cyclotomic(divisor))
    if not remainder.is_zero():
        raise _fail("cyclotomic divisor left a remainder", divisor=divisor, degree=degree)
    return quotient


@dataclass(frozen=True)
class QuadraticExtension:
    """Element a + b sqrt(d) of Q(sqrt(d))."""

    a: Fraction
    b: Fraction
    d: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", _require_fraction(self.a, "rational part"))
        object.__setattr__(self, "b", _require_fraction(self.b, "radical part"))
        object.__setattr__(self, "d", _require_discriminant(self.d))

    def __add__(self, other: QuadraticExtension) -> QuadraticExtension:
        partner = _same_disc(self, other)
        return QuadraticExtension(self.a + partner.a, self.b + partner.b, self.d)

    def __mul__(self, other: QuadraticExtension) -> QuadraticExtension:
        partner = _same_disc(self, other)
        real = self.a * partner.a + self.b * partner.b * self.d
        radical = self.a * partner.b + self.b * partner.a
        return QuadraticExtension(real, radical, self.d)

    def trace(self) -> Fraction:
        return self.a * 2

    def norm(self) -> Fraction:
        return self.a * self.a - self.b * self.b * self.d


def _require_discriminant(value: object) -> int:
    disc = _require_int(value, "discriminant")
    if disc == 0:
        raise _fail("quadratic discriminant is zero")
    return disc


def _same_disc(left: QuadraticExtension, right: object) -> QuadraticExtension:
    if not isinstance(right, QuadraticExtension):
        raise _fail("value is not a quadratic element", received=type(right).__name__)
    if left.d != right.d:
        raise _fail("quadratic discriminants differ", left=left.d, right=right.d)
    return right


def _divides(divisor: int, modulus: int) -> bool:
    if divisor == 0:
        return False
    return modulus % divisor == 0


def conductor_lcm_witness() -> int:
    """Return 120 when every target conductor divides 120."""
    for conductor in TARGET_CONDUCTORS:
        if not _divides(conductor, TARGET_LCM_CONDUCTOR):
            raise _fail("conductor does not divide 120", conductor=conductor)
    if not _tower_directed(3, 4):
        raise _fail("conductors 3 and 4 have no common multiple witness")
    return TARGET_LCM_CONDUCTOR


def _tower_directed(left: int, right: int) -> bool:
    common = left * right
    if common < 1:
        return False
    if not _divides(left, common):
        return False
    return _divides(right, common)


def main() -> int:
    """Print the conductor certificate."""
    try:
        print(conductor_lcm_witness())
    except NumberTheoryError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
