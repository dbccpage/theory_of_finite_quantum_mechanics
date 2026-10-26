"""Conditional constructive finite classifications; AuthorityEffect: None.

Predicate vocabulary is fixed here, rather than identifying comparison ability
with calibration success. Native generalized Moore mathematics owns production;
these hermetic witnesses use unary updates and finite pair-orbit replay only.
"""

from dataclasses import dataclass, fields


def _strict_flags(value: object) -> None:
    if any(type(getattr(value, field.name)) is not bool for field in fields(value)):
        raise TypeError("classification predicates must be Boolean")


def _indices(values: tuple[int, ...]) -> None:
    if not isinstance(values, tuple) or any(type(x) is not int or x < 0 for x in values):
        raise TypeError("finite model data must be tuples of nonnegative integer identifiers")


@dataclass(frozen=True)
class RetentionSignature:
    nontrivial: bool
    reversible: bool
    observable: bool
    tolerance: bool
    minimal: bool
    active: bool

    def __post_init__(self):
        _strict_flags(self)

    def realizable(self) -> bool:
        if not self.nontrivial:
            return self.reversible and self.observable and not self.tolerance and self.minimal and not self.active
        if self.observable and not self.tolerance and not self.minimal:
            return False
        if not self.active:
            return self.reversible and self.minimal == (self.observable and not self.tolerance)
        return True


@dataclass(frozen=True)
class UnaryRetentionWitness:
    raw: tuple[int, ...]
    recognized: tuple[int, ...]
    update: tuple[int, ...]

    def __post_init__(self):
        for row in (self.raw, self.recognized, self.update):
            _indices(row)
        n = len(self.raw)
        if n == 0 or len(self.recognized) != n or len(self.update) != n or any(x >= n for x in self.update):
            raise ValueError("retention maps must be total on a nonempty carrier")
        if any(self.raw[x] == self.raw[y] and self.recognized[x] != self.recognized[y] for x in range(n) for y in range(n)):
            raise ValueError("recognition must factor through raw reports")

    def distinguishable(self, x: int, y: int) -> bool:
        n = len(self.raw)
        if type(x) is not int or type(y) is not int or not 0 <= x < n or not 0 <= y < n:
            raise ValueError("state pair leaves carrier")
        # n^2 pair states: absent a mismatch before repetition, the orbit loops.
        for _ in range(n * n):
            if self.recognized[x] != self.recognized[y]:
                return True
            x, y = self.update[x], self.update[y]
        return False

    def signature(self) -> RetentionSignature:
        n = len(self.raw)
        return RetentionSignature(
            n > 1,
            len(set(self.update)) == n,
            len(set(self.raw)) == n,
            any(self.raw[x] != self.raw[y] and self.recognized[x] == self.recognized[y] for x in range(n) for y in range(n)),
            all(self.distinguishable(x, y) for x in range(n) for y in range(x + 1, n)),
            any(x != y for x, y in enumerate(self.update)),
        )


def realize_retention(signature: RetentionSignature) -> UnaryRetentionWitness:
    if not signature.realizable():
        raise ValueError("universally impossible retention signature")
    if not signature.nontrivial:
        raw, recognized = (0,), (0,)
    elif signature.minimal:
        raw, recognized = {
            (True, False): ((0, 1), (0, 1)),
            (False, False): ((0, 0, 1), (0, 0, 1)),
            (True, True): ((0, 1, 2), (0, 0, 1)),
            (False, True): ((0, 0, 1, 2), (0, 0, 0, 1)),
        }[signature.observable, signature.tolerance]
    else:
        raw, recognized = {
            (True, True): ((0, 1), (0, 0)),
            (False, False): ((0, 0), (0, 0)),
            (False, True): ((0, 0, 1), (0, 0, 0)),
        }[signature.observable, signature.tolerance]
    n = len(raw)
    update = tuple(
        x if not signature.active else (x + 1) % n if signature.reversible
        else min(x + 1, n - 1) if signature.minimal else 0
        for x in range(n)
    )
    return UnaryRetentionWitness(raw, recognized, update)


@dataclass(frozen=True)
class FunctionalSignature:
    linked: bool
    presentation_stable: bool
    report_stable: bool
    calibrated: bool
    blind_spot: bool

    def __post_init__(self):
        _strict_flags(self)

    def realizable(self) -> bool:
        return (self.blind_spot or self.linked) and not (self.linked and self.presentation_stable and not self.report_stable)


@dataclass(frozen=True)
class FunctionalModel:
    presentation: tuple[int, ...]
    report: tuple[int, ...]
    context: tuple[int, ...]
    target: tuple[int, ...]

    def __post_init__(self):
        for row in (self.presentation, self.report, self.context, self.target):
            _indices(row)
        n = len(self.presentation)
        if n == 0 or any(len(row) != n for row in (self.report, self.context, self.target)) or any(x >= n for x in self.context):
            raise ValueError("all functional maps must be total on the nonempty carrier")

    def report_factor(self) -> dict[int, int] | None:
        factor = {}
        for presentation, report in zip(self.presentation, self.report):
            if presentation in factor and factor[presentation] != report:
                return None
            factor[presentation] = report
        return factor

    def signature(self) -> FunctionalSignature:
        return FunctionalSignature(
            self.report_factor() is not None,
            all(self.presentation[x] == self.presentation[tx] for x, tx in enumerate(self.context)),
            all(self.report[x] == self.report[tx] for x, tx in enumerate(self.context)),
            self.report == self.target,
            len(set(self.presentation)) < len(self.presentation),
        )


def realize_functional(signature: FunctionalSignature) -> FunctionalModel:
    if not signature.realizable():
        raise ValueError("universally impossible functional signature")
    if not signature.blind_spot:
        q = (0, 1)
        if signature.presentation_stable:
            report, context = (0, 1), (0, 1)
        elif signature.report_stable:
            report, context = (0, 0), (1, 1)
        else:
            report, context = (0, 1), (1, 1)
    else:
        q = (0, 0, 1)
        if signature.linked:
            if signature.presentation_stable:
                report, context = (0, 0, 1), (0, 1, 2)
            elif signature.report_stable:
                report, context = (0, 0, 0), (2, 1, 2)
            else:
                report, context = (0, 0, 1), (2, 1, 2)
        elif signature.presentation_stable:
            report = (0, 1, 0)
            context = (0, 1, 2) if signature.report_stable else (1, 1, 2)
        elif signature.report_stable:
            report, context = (0, 1, 0), (2, 1, 2)
        else:
            report, context = (0, 1, 2), (2, 1, 2)
    target = report if signature.calibrated else (report[0] + 1,) + report[1:]
    return FunctionalModel(q, report, context, target)
