"""A refinement tower whose indices multiply to the number of atoms.

Origin: lean4/CyclotomicTowerDirected.lean theorem subfield_inclusion_trans.
The checked instance is 1 ∣ 2, 2 ∣ 4, hence 1 ∣ 4, matching the partition indices.
Claim: urn:omega:fqm:qm:tower-degree:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 9; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: The partitions are the whole set, the two halves, and the four
singletons. The index product is 4. No cyclotomic conductor theorem beyond
this divisibility is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_DEGREE = 4


class TowerError(Exception):
    """One violated tower invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> TowerError:
    return TowerError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _divides(left: int, right: int) -> bool:
    if left == 0:
        raise _fail("division by zero in the tower index", left=left, right=right)
    return right % left == 0


def inclusion_trans() -> bool:
    """1 divides 2 and 2 divides 4, so 1 divides 4."""
    one = int(_require_fraction(1, "one"))
    two = int(_require_fraction(2, "two"))
    four = int(_require_fraction(4, "four"))
    if not _divides(one, two) or not _divides(two, four):
        raise _fail("tower indices do not divide")
    return _divides(one, four)


def _index(coarse: tuple[frozenset[int], ...], fine: tuple[frozenset[int], ...]) -> int:
    for block in fine:
        hosts = 0
        for parent in coarse:
            if block <= parent:
                hosts += 1
        if hosts != 1:
            raise _fail("block is not inside exactly one coarser block", hosts=hosts)
    if not _divides(len(coarse), len(fine)):
        raise _fail("refinement index is not an integer", coarse=len(coarse), fine=len(fine))
    return len(fine) // len(coarse)


def tower_degree() -> int:
    """Index product of the three-level partition tower. It equals 4."""
    if inclusion_trans() is not True:
        raise _fail("divisibility failed to transit")
    levels = (
        (frozenset({0, 1, 2, 3}),),
        (frozenset({0, 1}), frozenset({2, 3})),
        (frozenset({0}), frozenset({1}), frozenset({2}), frozenset({3})),
    )
    first = _index(levels[0], levels[1])
    second = _index(levels[1], levels[2])
    degree = first * second
    if degree != len(levels[2]):
        raise _fail("tower degree is not the atom count", degree=degree, atoms=len(levels[2]))
    return degree


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the tower degree 4."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(tower_degree()), Fraction(_DEGREE), "tower degree drifted")


def main() -> int:
    value = tower_degree()
    print(value)
    if value == _DEGREE:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
