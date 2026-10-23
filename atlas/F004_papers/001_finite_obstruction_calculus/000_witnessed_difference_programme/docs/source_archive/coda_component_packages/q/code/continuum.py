"""Rational enclosures, not an algorithm for arbitrary real equality."""

from dataclasses import dataclass
from fractions import Fraction
from typing import Any


def _validate_exact_rational(val: Any, name: str) -> Fraction:
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, float) or (
        getattr(val, "dtype", None) is not None and "float" in str(val.dtype).lower()
    ):
        raise TypeError(
            f"{name} must be an exact rational or integer, got float (floats strictly forbidden)"
        )
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val)
    if isinstance(val, str):
        try:
            return Fraction(val)
        except (ValueError, ZeroDivisionError) as exc:
            raise TypeError(
                f"{name} string could not be converted to exact rational: {exc}"
            ) from exc
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


@dataclass(frozen=True)
class Enclosure:
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "lower", _validate_exact_rational(self.lower, "lower"))
        object.__setattr__(self, "upper", _validate_exact_rational(self.upper, "upper"))
        if self.lower > self.upper:
            raise ValueError("enclosure lower must be ≤ upper")

    @property
    def midpoint(self) -> Fraction:
        return (self.lower + self.upper) / 2

    @property
    def error_bound(self) -> Fraction:
        return (self.upper - self.lower) / 2

    def verifies_sqrt2(self) -> bool:
        return 0 <= self.lower <= self.upper and self.lower**2 <= 2 <= self.upper**2

    def midpoint_certified_exact_sqrt2(self) -> bool:
        """True only if the interval is the singleton whose square is 2.

        No rational enclosure of √2 satisfies this. A verifying interval is
        not an identification of the midpoint with √2.
        """
        return self.error_bound == 0 and self.midpoint**2 == 2


def sqrt2_enclosure(steps: int) -> Enclosure:
    if type(steps) is not int or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    lower, upper = Fraction(1), Fraction(2)
    for _ in range(steps):
        midpoint = (lower + upper) / 2
        if midpoint**2 <= 2:
            lower = midpoint
        else:
            upper = midpoint
    return Enclosure(lower, upper)
