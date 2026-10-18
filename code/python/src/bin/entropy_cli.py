"""C750 B01 parity entrypoint.

Origin: code/python/src/bin/entropy_cli.py
Claim: collision probability sum p_i^2 separates the pure vector (1, 0) from (1/2, 1/2).
The qm.c750 solver module is not in this tree, so the parity check is local.
AuthorityEffect: None.
"""
from fractions import Fraction


class ParityError(Exception):
    """A parity weight was negative or did not sum to 1."""


def collision_probability(weights) -> Fraction:
    """Return Σ p_i^2 for a rational probability vector."""
    values = [Fraction(weight) for weight in weights]
    total = sum(values, Fraction(0))
    if any(value < 0 for value in values):
        raise ParityError("weights must be nonnegative")
    if total != 1:
        raise ParityError(f"weights sum to {total}, not 1")
    return sum((value * value for value in values), Fraction(0))


def parity_gap() -> Fraction:
    """Collision of a pure state minus collision of the fair bit. The gap is 1/2."""
    pure = collision_probability((1, 0))
    mixed = collision_probability((Fraction(1, 2), Fraction(1, 2)))
    return pure - mixed


def main() -> int:
    gap = parity_gap()
    print(gap)
    return 0 if gap == Fraction(1, 2) else 1


if __name__ == "__main__":
    raise SystemExit(main())
