"""Exact costs and admitted constructions for unnamed finite targets.

The written proofs are in paper.md, section 3.4. These algorithms are not
Lean certificates. The meeting-set search takes exponential time in n;
it is intended for the small research carriers used by this derivation.
"""

from __future__ import annotations

from itertools import combinations

from model import Change, DState, Kind, empty, perform


def _require_target(target: DState) -> None:
    if target.names is not None:
        raise ValueError("targets from the empty beginning must be unnamed")
    if type(target.n) is not int or any(type(k) is not int for k in (*target.r, *target.s)):
        raise ValueError("term counts and multiplicities must be natural integers")


def shared_pairs(target: DState) -> frozenset[tuple[int, int]]:
    """Ordered pairs asserted positively in both relations; loops are included."""
    _require_target(target)
    return frozenset(
        (x, y)
        for x in range(target.n)
        for y in range(target.n)
        if target.has("r", x, y) and target.has("s", x, y)
    )


def minimum_meeting_terms(target: DState) -> tuple[int, ...]:
    """First smallest term set meeting every shared pair, by exact enumeration."""
    pairs = shared_pairs(target)
    return next(
        subset
        for size in range(target.n + 1)
        for subset in combinations(range(target.n), size)
        if all(x in subset or y in subset for x, y in pairs)
    )


def minimum_changes(target: DState) -> int:
    """n + m + twice the minimum meeting-set size; see the written proof."""
    return target.n + target.m + 2 * len(minimum_meeting_terms(target))


def minimum_peak_terms(target: DState) -> int:
    """n+1 exactly when a nonempty target has no overlap-free term."""
    incident = {vertex for pair in shared_pairs(target) for vertex in pair}
    return target.n + int(bool(target.n) and len(incident) == target.n)


def shortest_construction(target: DState) -> tuple[tuple[Change, DState], ...]:
    """Attain both optima, with no removals, returning each admitted step.

    State writings are kept literal during the path. The final writing may
    permute target terms to put an overlap-free term last; it is the same
    unnamed result. At most one fresh helper is present at any time.
    """
    pairs = shared_pairs(target)
    incident = {vertex for pair in pairs for vertex in pair}
    spare = next((v for v in range(target.n) if v not in incident), None)
    order = [v for v in range(target.n) if v != spare]
    if spare is not None:
        order.append(spare)
    index = {old: new for new, old in enumerate(order)}
    relation_pairs = [
        [
            (index[x], index[y])
            for x in range(target.n)
            for y in range(target.n)
            for _ in range(values[x * target.n + y])
        ]
        for values in (target.r, target.s)
    ]
    renamed = DState.of(target.n, *relation_pairs)
    pairs = shared_pairs(renamed)
    meeting = minimum_meeting_terms(renamed)
    base_n = target.n - int(spare is not None)
    state = empty()
    trace: list[tuple[Change, DState]] = []

    def step(change: Change) -> None:
        nonlocal state
        state = perform(state, change)
        trace.append((change, state))

    for _ in range(base_n):
        step(Change(Kind.ADD_TERM))
    for x in range(base_n):
        for y in range(base_n):
            for _ in range(renamed.r[x * target.n + y]):
                step(Change(Kind.ADD_ASSERTION, "r", x, y))
            if (x, y) not in pairs:
                for _ in range(renamed.s[x * target.n + y]):
                    step(Change(Kind.ADD_ASSERTION, "s", x, y))
    for vertex in meeting:
        step(Change(Kind.ADD_TERM))
        for x, y in sorted(pairs):
            owner = x if x in meeting else y
            if owner != vertex:
                continue
            for _ in range(renamed.s[x * target.n + y]):
                step(
                    Change(
                        Kind.ADD_ASSERTION,
                        "s",
                        base_n if x == vertex else x,
                        base_n if y == vertex else y,
                    )
                )
        step(Change(Kind.IDENTIFY, "", vertex, base_n))
    if spare is not None:
        step(Change(Kind.ADD_TERM))
        last = target.n - 1
        for x in range(target.n):
            for y in range(target.n):
                if x != last and y != last:
                    continue
                for rel, values in (("r", renamed.r), ("s", renamed.s)):
                    for _ in range(values[x * target.n + y]):
                        step(Change(Kind.ADD_ASSERTION, rel, x, y))
    return tuple(trace)
