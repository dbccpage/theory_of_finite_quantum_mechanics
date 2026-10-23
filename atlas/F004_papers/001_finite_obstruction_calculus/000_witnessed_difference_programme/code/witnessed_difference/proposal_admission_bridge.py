"""Finite decision descent and declared replay; no credential or authority service."""

from dataclasses import dataclass

from .finite_observer_adapter_completeness import DescentError, Operation, Structure, descend


def _natural(value: int) -> bool:
    return type(value) is int and value >= 0


@dataclass(frozen=True)
class DecisionTable:
    reports: tuple[int, ...]
    decisions: tuple[bool | None, ...]

    def __post_init__(self) -> None:
        if type(self.reports) is not tuple or type(self.decisions) is not tuple:
            raise ValueError("immutable tables required")
        if len(self.reports) != len(self.decisions):
            raise ValueError("domain mismatch")
        if any(not _natural(x) for x in self.reports):
            raise ValueError("invalid report")
        if any(x is not None and type(x) is not bool for x in self.decisions):
            raise ValueError("decisions must be bool or None")


@dataclass(frozen=True)
class Decoder:
    image: tuple[int, ...]
    decisions: tuple[bool | None, ...]

    def decode(self, report: int) -> bool | None:
        if not _natural(report) or report not in self.image:
            raise ValueError("outside declared image")
        return self.decisions[self.image.index(report)]


def decision_decoder(table: DecisionTable) -> Decoder:
    """Exists exactly for fiber-constant decisions, including undefinedness."""
    if type(table) is not DecisionTable:
        raise ValueError("invalid decision table")
    DecisionTable.__post_init__(table)
    image = tuple(sorted(set(table.reports)))
    q = tuple(image.index(x) for x in table.reports)
    values = tuple(None if x is None else int(x) for x in table.decisions)
    source = Structure((len(q), 2), (Operation((0,), 1, values),))
    target = descend(source, (len(image), 2), (q, (0, 1)))
    decoded = tuple(None if x is None else bool(x) for x in target.operations[0].values)
    return Decoder(image, decoded)


def joint_commit_table(
    evaluation: tuple[bool | None, ...], permission: tuple[bool | None, ...]
) -> DecisionTable:
    """Undefined inputs yield undefined; defined commit is evaluation AND permission."""
    for values in (evaluation, permission):
        if type(values) is not tuple or any(x is not None and type(x) is not bool for x in values):
            raise ValueError("immutable bool/None table required")
    if len(evaluation) != len(permission):
        raise ValueError("domain mismatch")
    tags = {None: 0, False: 1, True: 2}
    reports = tuple(3 * tags[e] + tags[a] for e, a in zip(evaluation, permission))
    decisions = tuple(
        None if e is None or a is None else e and a for e, a in zip(evaluation, permission)
    )
    return DecisionTable(reports, decisions)


@dataclass(frozen=True)
class DeclaredTransitions:
    states: int
    events: int
    rule: str
    scope: str
    # Row-major state x event, None is an explicitly unavailable transition.
    table: tuple[int | None, ...]

    def __post_init__(self) -> None:
        if not _natural(self.states) or self.states == 0 or not _natural(self.events):
            raise ValueError("invalid carrier")
        if (
            type(self.rule) is not str
            or not self.rule
            or type(self.scope) is not str
            or not self.scope
        ):
            raise ValueError("declared rule and scope required")
        if type(self.table) is not tuple or len(self.table) != self.states * self.events:
            raise ValueError("invalid transition table")
        if any(x is not None and (not _natural(x) or x >= self.states) for x in self.table):
            raise ValueError("invalid target state")


@dataclass(frozen=True)
class Occurrence:
    index: int
    event: int
    before: int
    after: int

    def __post_init__(self) -> None:
        if any(not _natural(x) for x in (self.index, self.event, self.before, self.after)):
            raise ValueError("invalid occurrence")


@dataclass(frozen=True)
class ReplayReceipt:
    declaration: DeclaredTransitions
    initial: int
    events: tuple[int, ...]
    occurrences: tuple[Occurrence, ...]
    final: int

    def __post_init__(self) -> None:
        if type(self.declaration) is not DeclaredTransitions:
            raise ValueError("invalid declaration")
        DeclaredTransitions.__post_init__(self.declaration)
        if any(not _natural(x) or x >= self.declaration.states for x in (self.initial, self.final)):
            raise ValueError("invalid receipt state")
        if type(self.events) is not tuple or any(not _natural(x) for x in self.events):
            raise ValueError("invalid receipt events")
        if type(self.occurrences) is not tuple or any(
            type(x) is not Occurrence for x in self.occurrences
        ):
            raise ValueError("invalid receipt occurrences")
        for occurrence in self.occurrences:
            Occurrence.__post_init__(occurrence)
            if (
                occurrence.event >= self.declaration.events
                or occurrence.before >= self.declaration.states
                or occurrence.after >= self.declaration.states
            ):
                raise ValueError("occurrence outside declared domain")
        if any(x >= self.declaration.events for x in self.events):
            raise ValueError("receipt event outside declared domain")


def replay(
    declaration: DeclaredTransitions, initial: int, events: tuple[int, ...]
) -> ReplayReceipt:
    if type(declaration) is not DeclaredTransitions:
        raise ValueError("invalid declaration")
    DeclaredTransitions.__post_init__(declaration)
    if not _natural(initial) or initial >= declaration.states or type(events) is not tuple:
        raise ValueError("invalid replay input")
    state = initial
    occurrences = []
    for index, event in enumerate(events):
        if not _natural(event) or event >= declaration.events:
            raise ValueError("invalid event")
        target = declaration.table[state * declaration.events + event]
        if target is None:
            raise ValueError("transition undefined")
        occurrences.append(Occurrence(index, event, state, target))
        state = target
    return ReplayReceipt(declaration, initial, events, tuple(occurrences), state)


def verify_replay(
    declaration: DeclaredTransitions, initial: int, events: tuple[int, ...], receipt: ReplayReceipt
) -> None:
    """Reexecute against independently supplied originals, never receipt self-binding."""
    if type(receipt) is not ReplayReceipt:
        raise ValueError("invalid receipt")
    ReplayReceipt.__post_init__(receipt)
    if receipt != replay(declaration, initial, events):
        raise DescentError("replay receipt mismatch")
