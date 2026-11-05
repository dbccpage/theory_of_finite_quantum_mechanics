"""Contextual congruence, critical context witnesses, and exact witness rank.

x ~ y iff p(x) = p(y).  A critical context witness (x, y, c) has p(x) = p(y)
but p(rho(c) x) != p(rho(c) y); its exposed vector is
nu(x, y, c) = p(rho(c) x) - p(rho(c) y).  The witness rank is the exact
dimension of the span of the exposed vectors.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Hashable, Mapping, Sequence

from .exact import exact_row
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .simplicial import rank_rational

State = Hashable
ExactScalar = int | str | Fraction


@dataclass(frozen=True)
class ContextualSystem:
    """States, named context actions rho(c): V -> V, and an exact profile p: V -> Q^d."""

    states: tuple[State, ...]
    contexts: Mapping[str, Mapping[State, State]]
    profile: Mapping[State, Sequence[ExactScalar]]

    def __post_init__(self) -> None:
        if type(self.states) is not tuple or not self.states or len(set(self.states)) != len(self.states):
            raise ValueError("states must be a unique nonempty tuple")
        carrier = set(self.states)
        if not isinstance(self.contexts, Mapping) or any(
            not isinstance(name, str)
            or not name
            or not isinstance(action, Mapping)
            or set(action) != carrier
            or not set(action.values()) <= carrier
            for name, action in self.contexts.items()
        ):
            raise ValueError("each named context must map every state into the carrier")
        if not isinstance(self.profile, Mapping) or set(self.profile) != carrier:
            raise ValueError("the profile must be defined on every state")
        profile = {state: exact_row(self.profile[state]) for state in self.states}
        if len({len(vector) for vector in profile.values()}) != 1 or not profile[self.states[0]]:
            raise ValueError("profile vectors must share one positive dimension")
        object.__setattr__(
            self,
            "contexts",
            MappingProxyType({name: MappingProxyType(dict(action)) for name, action in self.contexts.items()}),
        )
        object.__setattr__(self, "profile", MappingProxyType(profile))

    @property
    def dimension(self) -> int:
        return len(self.profile[self.states[0]])


@dataclass(frozen=True)
class ContextWitness:
    x: State
    y: State
    context: str
    exposed: tuple[Fraction, ...]


def contextual_congruence(system: ContextualSystem) -> Outcome[tuple[frozenset[State], ...]]:
    """Classes of x ~ y iff p(x) = p(y), in first-appearance state order."""

    if not isinstance(system, ContextualSystem):
        return Refused(RefusalCode.INVALID_INPUT, "a contextual system is required")
    blocks: dict[tuple[Fraction, ...], list[State]] = {}
    for state in system.states:
        blocks.setdefault(system.profile[state], []).append(state)  # type: ignore[arg-type]
    return Accepted(tuple(frozenset(block) for block in blocks.values()))


def critical_context_witnesses(system: ContextualSystem) -> Outcome[tuple[ContextWitness, ...]]:
    """Every (x, y, c) with x before y, p(x) = p(y), and p(rho(c) x) != p(rho(c) y)."""

    if not isinstance(system, ContextualSystem):
        return Refused(RefusalCode.INVALID_INPUT, "a contextual system is required")
    p = system.profile
    witnesses = []
    for index, x in enumerate(system.states):
        for y in system.states[index + 1 :]:
            if p[x] != p[y]:
                continue
            for name in sorted(system.contexts):
                moved_x, moved_y = p[system.contexts[name][x]], p[system.contexts[name][y]]
                if moved_x != moved_y:
                    exposed = tuple(a - b for a, b in zip(moved_x, moved_y))  # type: ignore[operator]
                    witnesses.append(ContextWitness(x, y, name, exposed))
    return Accepted(tuple(witnesses))


def witness_rank(system: ContextualSystem) -> Outcome[int]:
    """dim span{nu(w)} over Q, computed by exact elimination."""

    found = critical_context_witnesses(system)
    if isinstance(found, Refused):
        return found
    return Accepted(rank_rational([witness.exposed for witness in found.value]))


def apply_coordinate_change(
    system: ContextualSystem,
    matrix: Sequence[Sequence[ExactScalar]],
) -> Outcome[ContextualSystem]:
    """p'(s) = M p(s) for an invertible exact d x d matrix M."""

    if not isinstance(system, ContextualSystem):
        return Refused(RefusalCode.INVALID_INPUT, "a contextual system is required")
    d = system.dimension
    try:
        if isinstance(matrix, (str, bytes)):
            raise TypeError("a coordinate change is a sequence of rows, not a string")
        rows = tuple(exact_row(row) for row in matrix)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"coordinate change must be exact: {error}")
    if len(rows) != d or any(len(row) != d for row in rows):
        return Refused(RefusalCode.INVALID_INPUT, f"coordinate change must be {d} x {d}")
    if rank_rational(rows) != d:
        return Refused(RefusalCode.NOT_INVERTIBLE, "a singular coordinate change can merge profiles")
    profile = {
        state: tuple(sum((a * b for a, b in zip(row, system.profile[state])), start=Fraction(0)) for row in rows)
        for state in system.states
    }
    return Accepted(ContextualSystem(system.states, system.contexts, profile))


def _bijection(mapping: object, domain: set[Hashable]) -> bool:
    return (
        isinstance(mapping, Mapping)
        and set(mapping) == domain
        and len(set(mapping.values())) == len(domain)
    )


def relabel(
    system: ContextualSystem,
    state_map: Mapping[State, State],
    context_map: Mapping[str, str],
) -> Outcome[ContextualSystem]:
    """Transport the system along bijections of states and of context names."""

    if not isinstance(system, ContextualSystem):
        return Refused(RefusalCode.INVALID_INPUT, "a contextual system is required")
    if not _bijection(state_map, set(system.states)) or not _bijection(context_map, set(system.contexts)):
        return Refused(RefusalCode.INVALID_INPUT, "relabelings must be bijections of states and contexts")
    try:
        relabeled = ContextualSystem(
            tuple(state_map[state] for state in system.states),
            {
                context_map[name]: {state_map[s]: state_map[t] for s, t in action.items()}
                for name, action in system.contexts.items()
            },
            {state_map[state]: system.profile[state] for state in system.states},
        )
    except ValueError as error:
        return Refused(RefusalCode.INVALID_INPUT, f"relabeled system is invalid: {error}")
    return Accepted(relabeled)


# Executable finite evidence; AuthorityEffect: None.
