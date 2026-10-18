"""Relative-sign fiber over a fixed rational Born distribution.

Global sign is quotiented out. The remaining sign patterns are enumerated,
and two patterns are identified when one is the global sign of the other.
The returned count is the number of classes whose diagonal weights match.
"""
from fractions import Fraction


class ReportFiberError(Exception):
    """A sign pattern left the Born distribution."""


def relative_fiber_size() -> int:
    """Return the number of relative real signs over weights (9/25, 16/25)."""
    base = (Fraction(3, 5), Fraction(4, 5))
    weights = tuple(amplitude * amplitude for amplitude in base)
    patterns = []
    for first in (Fraction(1), Fraction(-1)):
        for second in (Fraction(1), Fraction(-1)):
            signed = (first * base[0], second * base[1])
            signed_weights = tuple(entry * entry for entry in signed)
            if signed_weights != weights:
                raise ReportFiberError("a sign changed the Born weights")
            patterns.append(signed)
    classes = []
    for pattern in patterns:
        negated = tuple(-entry for entry in pattern)
        if pattern in classes or negated in classes:
            continue
        classes.append(pattern)
    if not classes:
        raise ReportFiberError("the fiber is empty")
    return len(classes)
