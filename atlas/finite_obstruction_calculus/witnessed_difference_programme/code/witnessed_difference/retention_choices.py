"""Exact typed packet extension counts and arbitrary-tolerance witnesses.

These hermetic research witnesses describe the Cartesian product of all typed
data choices. Compatibility and quotient descent are additional predicates.
The production owner is omega_category_theory::finite_retention_choices.
"""

from dataclasses import dataclass
from math import comb, factorial

Relation = frozenset[tuple[int, int]]


@dataclass(frozen=True)
class RetentionSignature:
    states: int
    labels: int
    reports: int

    def __post_init__(self) -> None:
        if any(type(n) is not int for n in (self.states, self.labels, self.reports)):
            raise TypeError("finite cardinalities must be integers, excluding bool")
        if self.states <= 0 or self.labels < 0 or self.reports < 0:
            raise ValueError("nonempty memory and nonnegative other cardinalities required")

    def counts(self) -> dict[str, int]:
        n, k, m = self.states, self.labels, self.reports
        updates, readouts, comparisons = n ** (n * k), m**n, 2 ** (m * m)
        return {
            "updates": updates,
            "readouts": readouts,
            "comparisons": comparisons,
            "packets": updates * readouts * comparisons,
            "tolerances": 2 ** (m * (m - 1) // 2),
            "reflexive_comparisons": 2 ** (m * (m - 1)),
            "symmetric_comparisons": 2 ** (m * (m + 1) // 2),
            "bijective_updates": factorial(n) ** k,
            "injective_readouts": factorial(m) // factorial(m - n) if m >= n else 0,
            "surjective_readouts": sum((-1) ** j * comb(m, j) * (m - j) ** n for j in range(m + 1)),
        }

    def from_codes(self, update: int, readout: int, comparison: int) -> "TypedRetention":
        counts = self.counts()
        for code, key in ((update, "updates"), (readout, "readouts"), (comparison, "comparisons")):
            if type(code) is not int or not 0 <= code < counts[key]:
                raise ValueError("choice code outside its independent range")
        updates = []
        for _ in range(self.states):
            row = []
            for _ in range(self.labels):
                update, digit = divmod(update, self.states)
                row.append(digit)
            updates.append(tuple(row))
        reports = []
        for _ in range(self.states):
            readout, digit = divmod(readout, self.reports)
            reports.append(digit)
        relation = frozenset(
            (x, y)
            for x in range(self.reports)
            for y in range(self.reports)
            if comparison & (1 << (self.reports * x + y))
        )
        return TypedRetention(self, tuple(updates), tuple(reports), relation)


@dataclass(frozen=True)
class TypedRetention:
    signature: RetentionSignature
    updates: tuple[tuple[int, ...], ...]
    readouts: tuple[int, ...]
    comparison: Relation

    def __post_init__(self) -> None:
        n, k, m = self.signature.states, self.signature.labels, self.signature.reports
        if (
            len(self.updates) != n
            or any(len(row) != k for row in self.updates)
            or len(self.readouts) != n
        ):
            raise ValueError("typed function shape mismatch")
        if any(type(x) is not int or not 0 <= x < n for row in self.updates for x in row):
            raise ValueError("update outside memory")
        if any(type(x) is not int or not 0 <= x < m for x in self.readouts):
            raise ValueError("readout outside report alphabet")
        if any(
            type(x) is not int or type(y) is not int or not 0 <= x < m or not 0 <= y < m
            for x, y in self.comparison
        ):
            raise ValueError("comparison outside report alphabet")

    def is_tolerance(self) -> bool:
        return all((x, x) in self.comparison for x in range(self.signature.reports)) and all(
            (y, x) in self.comparison for x, y in self.comparison
        )


@dataclass(frozen=True)
class ForwardRelationReceipt:
    relations: tuple[Relation, ...]

    @property
    def relation(self) -> Relation:
        return self.relations[-1]


def is_forward_compatible(packet: TypedRetention, relation: Relation) -> bool:
    n, k = packet.signature.states, packet.signature.labels
    return all(
        type(x) is int
        and type(y) is int
        and 0 <= x < n
        and 0 <= y < n
        and (packet.readouts[x], packet.readouts[y]) in packet.comparison
        and all((packet.updates[x][i], packet.updates[y][i]) in relation for i in range(k))
        for x, y in relation
    )


def greatest_forward_relation(packet: TypedRetention) -> ForwardRelationReceipt:
    n, k = packet.signature.states, packet.signature.labels
    relation = frozenset(
        (x, y)
        for x in range(n)
        for y in range(n)
        if (packet.readouts[x], packet.readouts[y]) in packet.comparison
    )
    chain = [relation]
    while True:
        next_relation = frozenset(
            (x, y)
            for x, y in relation
            if all((packet.updates[x][i], packet.updates[y][i]) in relation for i in range(k))
        )
        if next_relation == relation:
            return ForwardRelationReceipt(tuple(chain))
        relation = next_relation
        chain.append(relation)


def relation_is_equivalence(states: int, relation: Relation) -> bool:
    if (type(states) is not int or states < 0
            or any(type(x) is not int or type(y) is not int or not 0 <= x < states
                   or not 0 <= y < states for x, y in relation)):
        return False
    return (
        all((x, x) in relation for x in range(states))
        and all((y, x) in relation for x, y in relation)
        and all((x, z) in relation for x, y in relation for b, z in relation if b == y)
    )


def raw_report_descends(packet: TypedRetention, relation: Relation) -> bool:
    return all(packet.readouts[x] == packet.readouts[y] for x, y in relation)


def initial_recognition_is_forward_compatible(packet: TypedRetention) -> bool:
    initial = frozenset(
        (x, y)
        for x in range(packet.signature.states)
        for y in range(packet.signature.states)
        if (packet.readouts[x], packet.readouts[y]) in packet.comparison
    )
    return is_forward_compatible(packet, initial)
