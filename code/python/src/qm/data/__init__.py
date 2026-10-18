"""Packaged exact input fixtures; no repository discovery is needed.

Origin: code/python/src/qm/data/__init__.py
Claim: a fixture rational "a/b" parses to a reduced Fraction, and diag(1/2, 1/2) has purity 1/2.
AuthorityEffect: None.
"""
from fractions import Fraction


class FixtureRationalError(Exception):
    """A packaged rational field was not of the form numerator/denominator."""


def parse_fixture_rational(text: str) -> Fraction:
    """Parse a fixture rational. Integers are accepted as n/1, matching the schema note."""
    if not isinstance(text, str) or "/" not in text:
        raise FixtureRationalError(f"fixture rational must be 'a/b', got {text!r}")
    numerator, denominator = text.split("/", 1)
    try:
        return Fraction(int(numerator), int(denominator))
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise FixtureRationalError(f"fixture rational {text!r} is not an integer ratio") from exc


def fixture_purity() -> Fraction:
    """Purity Σ p_i^2 of the packaged fair bit, after parsing the rational fields."""
    left = parse_fixture_rational("1/2")
    right = parse_fixture_rational("2/4")
    if left != right:
        raise FixtureRationalError("1/2 and 2/4 do not reduce to the same fixture rational")
    if left + right != 1:
        raise FixtureRationalError("the fair bit does not sum to 1")
    return left * left + right * right
