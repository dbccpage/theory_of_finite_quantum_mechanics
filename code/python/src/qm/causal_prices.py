"""Closed price-cycle defect of positive rational prices.

Origin: lean4/CoboundaryHolonomy.lean theorem coboundary_closed_cycle_zero
(vertex_path_holonomy (coboundary φ) (u :: vs ++ [u]) = 0) and theorem
coboundary_vertex_path_telescoping
(vertex_path_holonomy (coboundary φ) (u :: vs ++ [w]) = φ w - φ u).
The coboundary is def coboundary: (δφ)(u, v) = φ v - φ u.
Claim: urn:omega:fqm:price:cycle-defect:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_causal_prices.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: cycle_price_defect returns the product of successive positive
exact-rational ratios around a nonempty cycle, minus the closing ratio of the
first price with itself. additive_holonomy sums the successive differences on
that cycle. certified_cycle checks both on (1, 2/3, 4/5) and requires each to
be 0. The cited theorems are integer additive holonomy of a coboundary on a
closed vertex path. This file uses Python Fraction, does not prove those
theorems, and the multiplicative ratio product is not the cited theorem. This
file does not claim the CausalPriceList row census or an H071 multiplicity.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_FIXTURE: tuple[object, ...] = (Fraction(1), Fraction(2, 3), Fraction(4, 5))
_DEFECT = Fraction(0)


class CausalPriceError(Exception):
    """One violated price-cycle invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CausalPriceError:
    return CausalPriceError(invariant, parameters)


def _default(prices: object | None) -> object:
    if prices is None:
        return _FIXTURE
    return prices


def _require_tuple(prices: object) -> tuple[object, ...]:
    if isinstance(prices, (str, bytes)) or not isinstance(prices, tuple):
        raise _fail("prices are not a tuple", received=type(prices).__name__)
    return tuple(prices)


def _require_nonempty(prices: tuple[object, ...]) -> tuple[object, ...]:
    if len(prices) == 0:
        raise _fail("prices are empty")
    return prices


def _require_price(value: object, index: int) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the price boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational price was required", index=index)
    if isinstance(value, Fraction):
        price = value
    elif type(value) is int:
        price = Fraction(value)
    else:
        raise _fail("price is not an exact rational", index=index, received=type(value).__name__)
    if price <= 0:
        raise _fail("price is not positive", index=index, received=str(price))
    return price


def _collect(prices: tuple[object, ...]) -> tuple[Fraction, ...]:
    collected: list[Fraction] = []
    for index, value in enumerate(prices):
        collected.append(_require_price(value, index))
    return tuple(collected)


def _ratio(current: Fraction, nxt: Fraction) -> Fraction:
    return nxt / current


def _step(current: Fraction, nxt: Fraction) -> Fraction:
    return nxt - current


def _ratio_product(prices: tuple[Fraction, ...]) -> Fraction:
    product = Fraction(1)
    for index in range(len(prices)):
        nxt = prices[(index + 1) % len(prices)]
        product = product * _ratio(prices[index], nxt)
    return product


def _closing_ratio(prices: tuple[Fraction, ...]) -> Fraction:
    return prices[0] / prices[0]


def _difference_sum(prices: tuple[Fraction, ...]) -> Fraction:
    total = Fraction(0)
    for index in range(len(prices)):
        nxt = prices[(index + 1) % len(prices)]
        total = total + _step(prices[index], nxt)
    return total


def cycle_price_defect(prices: object | None = None) -> Fraction:
    """Return the cycle product of positive rational prices minus the closing ratio."""
    checked = _collect(_require_nonempty(_require_tuple(_default(prices))))
    product = _ratio_product(checked)
    closing = _closing_ratio(checked)
    if product != closing:
        raise _fail(
            "cycle product differs from the closing ratio",
            product=str(product),
            closing=str(closing),
        )
    return product - closing


def additive_holonomy(prices: object) -> Fraction:
    """Return the sum of successive differences around a closed price cycle."""
    checked = _collect(_require_nonempty(_require_tuple(prices)))
    return _difference_sum(checked)


def certified_cycle() -> Fraction:
    """Defect of (1, 2/3, 4/5). The product gap and the additive holonomy are 0."""
    defect = cycle_price_defect()
    holonomy = additive_holonomy(_FIXTURE)
    if defect != _DEFECT or holonomy != _DEFECT:
        raise _fail("certified cycle is not closed", defect=str(defect), holonomy=str(holonomy))
    return defect


def main() -> int:
    value = certified_cycle()
    print(value)
    if value == _DEFECT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
