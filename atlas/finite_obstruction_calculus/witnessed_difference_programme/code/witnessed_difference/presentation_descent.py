"""Descent of a target through a finite surjective presentation, and sections.

For a surjective q: X -> P and a target F on X, the obstruction set
{(x, y) : q x = q y, F x != F y} is empty exactly when F factors through q; the
factor is then unique; and F = F o i o q for one section i of q exactly when
the obstruction set is empty, in which case it holds for every section.
Uniqueness and sections are refused for a non-surjective q, where the factor
is free off the image and a section need not exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import prod
from typing import Hashable, Mapping

from .outcomes import Accepted, Outcome, RefusalCode, Refused

Assignment = tuple[tuple[Hashable, Hashable], ...]
FACTOR_BUDGET = 4096


def _carrier(points: object) -> tuple[Hashable, ...] | None:
    try:
        return points if type(points) is tuple and len(set(points)) == len(points) else None  # type: ignore[return-value]
    except TypeError:
        return None


def _total(mapping: object, domain: tuple[Hashable, ...]) -> bool:
    return isinstance(mapping, Mapping) and set(mapping) == set(domain)


def _presentation(
    domain: object, codomain: object, quotient: object
) -> Outcome[tuple[tuple[Hashable, ...], tuple[Hashable, ...], Mapping]]:  # type: ignore[type-arg]
    points, presentations = _carrier(domain), _carrier(codomain)
    if points is None or presentations is None:
        return Refused(RefusalCode.INVALID_INPUT, "X and P must be tuples of distinct hashable points")
    if not _total(quotient, points):
        return Refused(RefusalCode.INVALID_INPUT, "q must be a total map on X")
    if any(quotient[x] not in presentations for x in points):  # type: ignore[index]
        return Refused(RefusalCode.OUTSIDE_CARRIER, "q takes a value outside P")
    return Accepted((points, presentations, quotient))  # type: ignore[arg-type]


def _declared(
    domain: object, codomain: object, quotient: object, target: object
) -> Outcome[tuple[tuple[Hashable, ...], tuple[Hashable, ...], Mapping, Mapping]]:  # type: ignore[type-arg]
    presented = _presentation(domain, codomain, quotient)
    if isinstance(presented, Refused):
        return presented
    if not _total(target, presented.value[0]):
        return Refused(RefusalCode.INVALID_INPUT, "F must be a total map on X")
    return Accepted(presented.value + (target,))  # type: ignore[arg-type]


def _obstruction(points: tuple[Hashable, ...], quotient: Mapping, target: Mapping) -> frozenset[tuple[Hashable, Hashable]]:  # type: ignore[type-arg]
    return frozenset(
        (x, y) for x in points for y in points if quotient[x] == quotient[y] and target[x] != target[y]
    )


def obstruction_set(
    domain: tuple[Hashable, ...],
    codomain: tuple[Hashable, ...],
    quotient: Mapping[Hashable, Hashable],
    target: Mapping[Hashable, Hashable],
) -> Outcome[frozenset[tuple[Hashable, Hashable]]]:
    """All ordered pairs with equal presentation and unequal target."""

    declared = _declared(domain, codomain, quotient, target)
    if isinstance(declared, Refused):
        return declared
    points, _, q, f = declared.value
    return Accepted(_obstruction(points, q, f))


def _surjective(points: tuple[Hashable, ...], presentations: tuple[Hashable, ...], quotient: Mapping) -> bool:  # type: ignore[type-arg]
    return {quotient[x] for x in points} == set(presentations)


@dataclass(frozen=True)
class Factorization:
    factor: Assignment
    unique: bool


def factor_through(
    domain: tuple[Hashable, ...],
    codomain: tuple[Hashable, ...],
    quotient: Mapping[Hashable, Hashable],
    target: Mapping[Hashable, Hashable],
) -> Outcome[Factorization]:
    """The unique G on P with G o q = F, for surjective q and an empty obstruction set."""

    declared = _declared(domain, codomain, quotient, target)
    if isinstance(declared, Refused):
        return declared
    points, presentations, q, f = declared.value
    if not _surjective(points, presentations, q):
        return Refused(RefusalCode.NOT_SURJECTIVE, "q is not onto P; a factor is not unique off the image")
    obstruction = _obstruction(points, q, f)
    if obstruction:
        pair = min(obstruction, key=repr)
        return Refused(RefusalCode.DOES_NOT_DESCEND, f"obstruction pair {pair!r}: equal presentation, unequal target")
    values = {q[x]: f[x] for x in points}
    return Accepted(Factorization(tuple((p, values[p]) for p in presentations), True))


def count_factorizations(
    domain: tuple[Hashable, ...],
    codomain: tuple[Hashable, ...],
    quotient: Mapping[Hashable, Hashable],
    target: Mapping[Hashable, Hashable],
    values: tuple[Hashable, ...],
) -> Outcome[int]:
    """Count every G: P -> values with G o q = F by exhaustive enumeration; q need not be onto."""

    declared = _declared(domain, codomain, quotient, target)
    if isinstance(declared, Refused):
        return declared
    choices = _carrier(values)
    if choices is None:
        return Refused(RefusalCode.INVALID_INPUT, "the value set must be a tuple of distinct points")
    points, presentations, q, f = declared.value
    if len(choices) ** len(presentations) > FACTOR_BUDGET:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, f"the factor census is budgeted to {FACTOR_BUDGET} maps")
    count = 0
    for assignment in product(choices, repeat=len(presentations)):
        g = dict(zip(presentations, assignment))
        count += all(g[q[x]] == f[x] for x in points)
    return Accepted(count)


def all_sections(
    domain: tuple[Hashable, ...],
    codomain: tuple[Hashable, ...],
    quotient: Mapping[Hashable, Hashable],
) -> Outcome[tuple[Assignment, ...]]:
    """Every i: P -> X with q o i = identity; refused when q is not onto P."""

    presented = _presentation(domain, codomain, quotient)
    if isinstance(presented, Refused):
        return presented
    points, presentations, q = presented.value
    if not _surjective(points, presentations, q):
        return Refused(RefusalCode.NOT_SURJECTIVE, "q is not onto P; some fibre is empty and has no section value")
    fibres = [tuple(x for x in points if q[x] == p) for p in presentations]
    if prod(len(fibre) for fibre in fibres) > FACTOR_BUDGET:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, f"the section census is budgeted to {FACTOR_BUDGET} sections")
    return Accepted(tuple(tuple(zip(presentations, choice)) for choice in product(*fibres)))


@dataclass(frozen=True)
class SectionRecord:
    section: Assignment
    defect: frozenset[Hashable]
    zero_defect: bool
    obstruction_empty: bool


def section_test(
    domain: tuple[Hashable, ...],
    codomain: tuple[Hashable, ...],
    quotient: Mapping[Hashable, Hashable],
    target: Mapping[Hashable, Hashable],
    section: Mapping[Hashable, Hashable],
) -> Outcome[SectionRecord]:
    """Compare the defect {x : F x != F(i(q x))} of one section with the obstruction set."""

    declared = _declared(domain, codomain, quotient, target)
    if isinstance(declared, Refused):
        return declared
    points, presentations, q, f = declared.value
    if not _surjective(points, presentations, q):
        return Refused(RefusalCode.NOT_SURJECTIVE, "q is not onto P; sections do not exist")
    if not _total(section, presentations) or any(
        section[p] not in points or q[section[p]] != p for p in presentations
    ):
        return Refused(RefusalCode.INVALID_INPUT, "i is not a section: q o i must be the identity on P")
    defect = frozenset(x for x in points if f[x] != f[section[q[x]]])
    return Accepted(
        SectionRecord(
            tuple((p, section[p]) for p in presentations),
            defect,
            not defect,
            not _obstruction(points, q, f),
        )
    )


# Executable finite evidence; AuthorityEffect: None.
