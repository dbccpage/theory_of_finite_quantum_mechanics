"""Hermetic finite witnesses for declared labelled relational retention.

This independent research oracle deletes pairs with unmatched successors; the
production implementation refines partitions in omega_category_theory. Labels
and directed successor sets are admitted input, never selected from reports.
Exact report equality is used. Bisimulation is stronger than trace equality;
set-level quotients imply neither HoTT equivalence nor Kan fibrancy.
"""

from collections import deque
from dataclasses import dataclass

Pair = tuple[int, int]
Relation = frozenset[Pair]


@dataclass(frozen=True)
class RelationalModel:
    reports: tuple[int, ...]
    successors: tuple[tuple[frozenset[int], ...], ...]

    def __post_init__(self) -> None:
        if not self.reports or any(type(r) is not int or r < 0 for r in self.reports):
            raise ValueError("nonempty carrier with exact nonnegative report IDs required")
        if len(self.successors) != len(self.reports):
            raise ValueError("one labelled successor row per state required")
        labels = len(self.successors[0])
        if any(len(row) != labels for row in self.successors):
            raise ValueError("all rows must declare the same label alphabet")
        if any(
            type(y) is not int or not 0 <= y < len(self.reports)
            for row in self.successors
            for targets in row
            for y in targets
        ):
            raise ValueError("successor outside the finite state carrier")

    @property
    def state_count(self) -> int:
        return len(self.reports)

    @property
    def label_count(self) -> int:
        return len(self.successors[0])


@dataclass(frozen=True)
class BisimulationReceipt:
    relations: tuple[Relation, ...]
    partition: tuple[int, ...]


def refinement(model: RelationalModel, relation: Relation) -> Relation:
    """R intersect report equality and two-sided successor matching into R."""
    return frozenset(
        (x, y)
        for x, y in relation
        if model.reports[x] == model.reports[y]
        and all(
            all(
                any((a, b) in relation for b in model.successors[y][label])
                for a in model.successors[x][label]
            )
            and all(
                any((a, b) in relation for a in model.successors[x][label])
                for b in model.successors[y][label]
            )
            for label in range(model.label_count)
        )
    )


def is_bisimulation(model: RelationalModel, relation: Relation) -> bool:
    if any(
        type(x) is not int
        or type(y) is not int
        or not 0 <= x < model.state_count
        or not 0 <= y < model.state_count
        for x, y in relation
    ):
        return False
    return refinement(model, relation) == relation


def greatest_bisimulation(model: RelationalModel) -> BisimulationReceipt:
    relation = frozenset(
        (x, y)
        for x in range(model.state_count)
        for y in range(model.state_count)
        if model.reports[x] == model.reports[y]
    )
    chain = [relation]
    while True:
        next_relation = refinement(model, relation)
        if next_relation == relation:
            break
        relation = next_relation
        chain.append(relation)
    partition: list[int] = []
    for x in range(model.state_count):
        earlier = next((y for y in range(x) if (x, y) in relation), None)
        partition.append(partition[earlier] if earlier is not None else len(set(partition)))
    return BisimulationReceipt(tuple(chain), tuple(partition))


def verify_bisimulation_receipt(model: RelationalModel, receipt: BisimulationReceipt) -> bool:
    return type(receipt) is BisimulationReceipt and receipt == greatest_bisimulation(model)


def relation_of_partition(partition: tuple[int, ...]) -> Relation:
    return frozenset(
        (x, y)
        for x in range(len(partition))
        for y in range(len(partition))
        if partition[x] == partition[y]
    )


def behavioral_quotient(model: RelationalModel, receipt: BisimulationReceipt) -> RelationalModel:
    if not verify_bisimulation_receipt(model, receipt):
        raise ValueError("quotient requires a replayed greatest-bisimulation receipt")
    partition = receipt.partition
    representatives = tuple(partition.index(block) for block in range(max(partition) + 1))
    return RelationalModel(
        tuple(model.reports[x] for x in representatives),
        tuple(
            tuple(frozenset(partition[y] for y in targets) for targets in model.successors[x])
            for x in representatives
        ),
    )


@dataclass(frozen=True)
class SuccessionClassification:
    nonempty_reachability: Relation
    acyclic: bool
    state_to_component: tuple[int, ...]
    component_strict_order: Relation


def succession_classification(model: RelationalModel) -> SuccessionClassification:
    """Independent BFS oracle for raw cycles and SCC-condensation succession."""
    reach: set[Pair] = set()
    for x in range(model.state_count):
        pending = deque(y for targets in model.successors[x] for y in targets)
        visited: set[int] = set()
        while pending:
            y = pending.popleft()
            if y in visited:
                continue
            visited.add(y)
            pending.extend(z for targets in model.successors[y] for z in targets)
        reach.update((x, y) for y in visited)
    components: list[int] = []
    for x in range(model.state_count):
        earlier = next((y for y in range(x) if (x, y) in reach and (y, x) in reach), None)
        components.append(components[earlier] if earlier is not None else len(set(components)))
    order = frozenset(
        (components[x], components[y]) for x, y in reach if components[x] != components[y]
    )
    return SuccessionClassification(
        frozenset(reach),
        all((x, x) not in reach for x in range(model.state_count)),
        tuple(components),
        order,
    )


def bounded_traces(model: RelationalModel, state: int, depth: int) -> frozenset[tuple[int, ...]]:
    """Finite test surface, not a general trace-equivalence decision procedure."""
    if (
        type(depth) is not int
        or depth < 0
        or type(state) is not int
        or not 0 <= state < model.state_count
    ):
        raise ValueError("valid state and nonnegative integral depth required")
    traces: set[tuple[int, ...]] = {()}
    if depth:
        for label, targets in enumerate(model.successors[state]):
            for target in targets:
                traces.update((label, *word) for word in bounded_traces(model, target, depth - 1))
    return frozenset(traces)
