"""Causal order of the four-event diamond.

Origin: code/python/src/qm/campaigns/causal_order.py
The counted interval is the diamond 0→1, 0→2, 1→3, 2→3.
Claim: urn:omega:fqm:qm:diamond-interval-size:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 7; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: Ranks are the longest incoming path on these four edges. The
height of event 3 is 2 and the closed interval has 4 events. No general poset
theorem is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_SIZE = 4
_EDGES = ((0, 1), (0, 2), (1, 3), (2, 3))


class CausalOrderError(Exception):
    """One violated causal invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CausalOrderError:
    return CausalOrderError(invariant, parameters)


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


def _rank_of(node: int) -> int:
    rank = 0
    for src, dst in _EDGES:
        if dst == node:
            rank = max(rank, _rank_of(src) + 1)
    return rank


def _reaches(src: int, dst: int, seen: tuple[int, ...]) -> bool:
    if src == dst:
        return True
    if src in seen:
        return False
    step = seen + (src,)
    for left, right in _EDGES:
        if left == src and _reaches(right, dst, step):
            return True
    return False


def diamond_interval_size() -> int:
    """Events reachable from 0 that can reach 3."""
    ranks = tuple(_rank_of(node) for node in range(4))
    if ranks != (0, 1, 1, 2):
        raise _fail("diamond ranks drifted", ranks=str(ranks))
    count = 0
    node = 0
    while node < 4:
        if _reaches(0, node, ()) and _reaches(node, 3, ()):
            count += 1
        node += 1
    if count != _SIZE:
        raise _fail("diamond interval size drifted", size=count)
    return count


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the interval size 4."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(diamond_interval_size()), Fraction(_SIZE), "diamond interval drifted")


def main() -> int:
    value = diamond_interval_size()
    print(value)
    if value == _SIZE:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
