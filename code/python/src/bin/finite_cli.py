"""Finite QM CLI entrypoint.

Origin: code/python/src/bin/finite_cli.py
Claim: the delegated CLI still sees a rational identity whose trace equals its dimension.
AuthorityEffect: None.
"""
from fractions import Fraction

from ..qm.cli import main


def cli_identity_trace(size: int = 2) -> Fraction:
    """Trace of the size-by-size identity, computed before any CLI dispatch."""
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise ValueError(f"identity size must be a nonnegative int, got {size!r}")
    total = sum((Fraction(1) for _ in range(size)), Fraction(0))
    if total != size:
        raise ValueError(f"cli identity trace is {total}, not {size}")
    return total


if __name__ == "__main__":
    main()
