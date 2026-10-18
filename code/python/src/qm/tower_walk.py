"""Dyadic cover degrees and the two-factor multiplicity law.

Origin: lean4/H071RefinementSubsystemTower.lean theorem
multiplicity_composition (d3 = (k12 * k23) * d1 when d2 = k12 * d1 and
d3 = k23 * d2).
Claim: urn:omega:fqm:tower:multiplicity-composition:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_tower_walk.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: multiplicity_composition returns (left * right) * base for three
natural numbers after that product agrees with right * (left * base).
cover_degree returns the uniform block ratio of a nonempty tower step.
tower_degree_product checks the 8-atom dyadic partition whose cover degrees
are 2, 2, and 2, and returns their product. The cited theorem is the
two-factor natural-number identity. This file does not prove it, and it does
not claim the phase-mismatch or arrow-label sections of that Lean file.
"""

from __future__ import annotations

from typing import Mapping

_ATOM_COUNT = 8


class TowerWalkError(Exception):
    """One violated multiplicity or cover-degree invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> TowerWalkError:
    return TowerWalkError(invariant, parameters)


def _require_count(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the multiplicity boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a natural number was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("multiplicity count is negative", role=role, received=value)
        return value
    raise _fail(
        "multiplicity count is not an exact integer",
        role=role,
        received=type(value).__name__,
    )


def _require_tuple(blocks: object, role: str) -> tuple[object, ...]:
    if isinstance(blocks, (str, bytes)) or not isinstance(blocks, tuple):
        raise _fail("blocks are not a tuple", role=role, received=type(blocks).__name__)
    return tuple(blocks)


def _require_nonempty(blocks: tuple[object, ...], role: str) -> tuple[object, ...]:
    if len(blocks) == 0:
        raise _fail("blocks are empty", role=role)
    return blocks


def _as_block(value: object, role: str, index: int) -> frozenset[int]:
    if not isinstance(value, frozenset):
        raise _fail(
            "block is not a frozenset",
            role=role,
            index=index,
            received=type(value).__name__,
        )
    members: list[int] = []
    for member in value:
        members.append(_require_count(member, role))
    return frozenset(members)


def _collect_blocks(blocks: tuple[object, ...], role: str) -> tuple[frozenset[int], ...]:
    collected: list[frozenset[int]] = []
    for index, value in enumerate(blocks):
        collected.append(_as_block(value, role, index))
    return tuple(collected)


def _containers(block: frozenset[int], coarse: tuple[frozenset[int], ...]) -> int:
    count = 0
    for parent in coarse:
        if block <= parent:
            count += 1
    return count


def _composed(base: int, left_factor: int, right_factor: int) -> int:
    return (left_factor * right_factor) * base


def _stepped(base: int, left_factor: int, right_factor: int) -> int:
    return right_factor * (left_factor * base)


def multiplicity_composition(base: object, left_factor: object, right_factor: object) -> int:
    """Return (left * right) * base after it agrees with the stepped product."""
    checked_base = _require_count(base, "base")
    checked_left = _require_count(left_factor, "left")
    checked_right = _require_count(right_factor, "right")
    composed = _composed(checked_base, checked_left, checked_right)
    stepped = _stepped(checked_base, checked_left, checked_right)
    if composed != stepped:
        raise _fail(
            "multiplicity readings differ",
            composed=composed,
            stepped=stepped,
        )
    return composed


def cover_degree(coarse: object, fine: object) -> int:
    """Return |fine| / |coarse| when each fine block sits in one coarse block."""
    coarse_blocks = _collect_blocks(_require_nonempty(_require_tuple(coarse, "coarse"), "coarse"), "coarse")
    fine_blocks = _collect_blocks(_require_nonempty(_require_tuple(fine, "fine"), "fine"), "fine")
    if len(fine_blocks) % len(coarse_blocks) != 0:
        raise _fail(
            "fine block count does not divide into the coarse count",
            fine=len(fine_blocks),
            coarse=len(coarse_blocks),
        )
    for block in fine_blocks:
        if _containers(block, coarse_blocks) != 1:
            raise _fail("a fine block is not in exactly one coarse block", block=str(sorted(block)))
    return len(fine_blocks) // len(coarse_blocks)


def _atoms() -> tuple[frozenset[int], ...]:
    return tuple(frozenset((index,)) for index in range(_ATOM_COUNT))


def _pairs() -> tuple[frozenset[int], ...]:
    return tuple(frozenset(range(2 * index, 2 * index + 2)) for index in range(4))


def _fours() -> tuple[frozenset[int], ...]:
    return (frozenset(range(4)), frozenset(range(4, _ATOM_COUNT)))


def _whole() -> tuple[frozenset[int], ...]:
    return (frozenset(range(_ATOM_COUNT)),)


def tower_degree_product() -> int:
    """Return the product of the three dyadic cover degrees. It is 8."""
    atoms = _atoms()
    pairs = _pairs()
    fours = _fours()
    whole = _whole()
    first = cover_degree(whole, fours)
    second = cover_degree(fours, pairs)
    third = cover_degree(pairs, atoms)
    paired = multiplicity_composition(len(whole), first, second)
    if paired != len(pairs):
        raise _fail("paired block count missed the multiplicity law", count=paired)
    reached = multiplicity_composition(paired, third, 1)
    if reached != len(atoms):
        raise _fail("atom count missed the multiplicity law", count=reached)
    return first * second * third


def main() -> int:
    value = tower_degree_product()
    print(value)
    if value == _ATOM_COUNT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
