"""Genesis Seed, Admission Events, Regimes, and Candidate Responses.

Selected educational models related to 19L57G1:
- code/derivation/model.py
- code/derivation/candidates.py
- code/derivation/observe.py
- lean4/Derivation/Basic.lean

Classification: Object-language core and metatheoretic apparatus.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Union

from .canonical import validate_typed_fields

# ---------------------------------------------------------------------------
# Type aliases for tuples and indices
# ---------------------------------------------------------------------------

Args = tuple[int, ...]
Inst = tuple[int, Args]
Pair = tuple[int, int]
Slot = Optional[int]
Context = tuple[int, tuple[Slot, ...]]


class AdmissionError(ValueError):
    """An event is ill-formed relative to the current regime."""


# ---------------------------------------------------------------------------
# Primitive Admission Events (Object Language & Metatheory)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Supply:
    """External presentation of an opaque token. Not an admission.

    Supply is an external presentation event and provably does not change
    the admitted regime state (step(r, Supply(token)) == r).
    """

    token: str

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class AdmitDatum:
    """Admission of a presented token as an internal datum.

    Re-admission of an already admitted token is a designation of the
    existing datum, not a duplication (presentation identity dedups admissions).
    """

    token: str

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class AdmitForm:
    """Admission of a judgment form with arity >= 1."""

    arity: int

    def __post_init__(self) -> None:
        if self.arity < 1:
            raise AdmissionError(f"Form arity must be >= 1, got {self.arity}")
        validate_typed_fields(self)


@dataclass(frozen=True)
class AdmitInst:
    """Admission of a judgment instance (form index, arguments tuple)."""

    form: int
    args: Args

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class AdmitRuleAll:
    """Admission of the uniform all-tuples rule for a form."""

    form: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class Impose:
    """External requirement: data i and j must be internally separable.

    Requirements are persistent constraints with i < j.
    """

    i: int
    j: int

    def __post_init__(self) -> None:
        if not 0 <= self.i < self.j:
            raise AdmissionError(f"Impose requires i < j, got ({self.i}, {self.j})")
        validate_typed_fields(self)


# ---------------------------------------------------------------------------
# Composed Event Union
# ---------------------------------------------------------------------------

Event = Union[Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose]


# ---------------------------------------------------------------------------
# Composed State: Regime
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Regime:
    """Admitted state of the object language.

    data:  Admitted data in admission order (presentation tokens; internal identity is index).
    forms: Admitted judgment forms; entry a at index f means form f has arity a >= 1.
    insts: Admitted judgment instances (form, args).
    rules: Forms carrying the uniform all-tuples rule.
    reqs:  Externally imposed persistent separation requirements (i, j) with i < j.
    """

    data: tuple[str, ...]
    forms: tuple[int, ...]
    insts: frozenset[Inst]
    rules: frozenset[int]
    reqs: frozenset[Pair]

    def __post_init__(self) -> None:
        validate_typed_fields(self)
        if len(set(self.data)) != len(self.data) or any(arity < 1 for arity in self.forms):
            raise AdmissionError("REFUSED_SHAPE: duplicate tokens or invalid form arity")
        for form, args in self.insts:
            if not 0 <= form < len(self.forms) or len(args) != self.forms[form]:
                raise AdmissionError("REFUSED_SHAPE: instance form or arity")
            if any(not 0 <= arg < len(self.data) for arg in args):
                raise AdmissionError("REFUSED_SHAPE: instance argument outside carrier")
        if any(not 0 <= form < len(self.forms) for form in self.rules):
            raise AdmissionError("REFUSED_SHAPE: rule outside form carrier")
        if any(not 0 <= i < j < len(self.data) for i, j in self.reqs):
            raise AdmissionError("REFUSED_SHAPE: requirement outside carrier")

    def n_data(self) -> int:
        """Return the number of admitted data."""
        return len(self.data)

    def n_forms(self) -> int:
        """Return the number of admitted forms."""
        return len(self.forms)


EMPTY = Regime((), (), frozenset(), frozenset(), frozenset())


# ---------------------------------------------------------------------------
# Candidate Response Items and Deltas
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NewDatum:
    """Candidate item: admit one fresh datum."""


@dataclass(frozen=True)
class NewForm:
    """Candidate item: admit one judgment form."""

    arity: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class NewInst:
    """Candidate item: admit one judgment instance."""

    form: int
    args: Args

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class NewRuleAll:
    """Candidate item: admit uniform all-tuples rule for a form."""

    form: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)


Item = Union[NewDatum, NewForm, NewInst, NewRuleAll]
Delta = tuple[Item, ...]


def item_key(it: Item) -> tuple[int, int, Args]:
    """Deterministic sort key giving canonical item order:
    data (0), forms (1), rules (2), instances (3).
    """
    if isinstance(it, NewDatum):
        return (0, 0, ())
    if isinstance(it, NewForm):
        return (1, it.arity, ())
    if isinstance(it, NewRuleAll):
        return (2, it.form, ())
    return (3, it.form, it.args)


def canonical_delta(items: Sequence[Item]) -> Delta:
    """Return canonically ordered delta."""
    return tuple(sorted(items, key=item_key))


def mu1(delta: Delta) -> int:
    """Cost measure 1: raw number of items."""
    return len(delta)


def mu2(delta: Delta) -> tuple[int, int]:
    """Cost measure 2: (number of items, sum of arities of new forms)."""
    return (
        len(delta),
        sum(it.arity for it in delta if isinstance(it, NewForm)),
    )


# ---------------------------------------------------------------------------
# Candidate Space Bounds & Precomputed Observation Views
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Bounds:
    """Declared finite bounds of the candidate space."""

    max_items: int = 2
    max_arity: int = 2

    def __post_init__(self) -> None:
        validate_typed_fields(self)
        if self.max_items < 0 or self.max_arity < 0:
            raise AdmissionError("REFUSED_SHAPE: candidate bounds must be nonnegative")


@dataclass(frozen=True)
class Ctx:
    """Context representation: form index, hole slot, prefix and suffix args."""

    form: int
    slot: int
    prefix: Args
    suffix: Args

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class NodeView:
    """Precomputed observation data for one base regime."""

    base: Regime
    ctxs: tuple[Context, ...]
    profs: tuple[frozenset[Context], ...]

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class MinResponses:
    """Minimum valid responses to an imposed separation requirement."""

    measure: str
    cost: tuple[int, int]
    deltas: tuple[Delta, ...]
    bounds: Bounds

    def __post_init__(self) -> None:
        validate_typed_fields(self)


# ---------------------------------------------------------------------------
# Transition Semantics (Deterministic State Transitions & Replay)
# ---------------------------------------------------------------------------


def step(r: Regime, e: Event) -> Regime:
    """Apply one event deterministically. Raises AdmissionError on ill-formed events."""
    if isinstance(e, Supply):
        return r
    if isinstance(e, AdmitDatum):
        if e.token in r.data:
            return r
        return Regime(r.data + (e.token,), r.forms, r.insts, r.rules, r.reqs)
    if isinstance(e, AdmitForm):
        if e.arity < 1:
            raise AdmissionError(f"Form arity must be >= 1, got {e.arity}")
        return Regime(r.data, r.forms + (e.arity,), r.insts, r.rules, r.reqs)
    if isinstance(e, AdmitInst):
        if not (0 <= e.form < len(r.forms)):
            raise AdmissionError(f"Unknown form {e.form}")
        if len(e.args) != r.forms[e.form]:
            raise AdmissionError(
                f"Form {e.form} has arity {r.forms[e.form]}, got {len(e.args)} arguments"
            )
        if not all(0 <= a < len(r.data) for a in e.args):
            raise AdmissionError(f"Instance arguments out of range: {e.args}")
        return Regime(r.data, r.forms, r.insts | {(e.form, e.args)}, r.rules, r.reqs)
    if isinstance(e, AdmitRuleAll):
        if not (0 <= e.form < len(r.forms)):
            raise AdmissionError(f"Unknown form {e.form}")
        return Regime(r.data, r.forms, r.insts, r.rules | {e.form}, r.reqs)
    if isinstance(e, Impose):
        if not (0 <= e.i < e.j < len(r.data)):
            raise AdmissionError(f"Requirement out of range: ({e.i}, {e.j})")
        return Regime(r.data, r.forms, r.insts, r.rules, r.reqs | {(e.i, e.j)})
    raise AdmissionError(f"Unknown event type: {type(e)}")


def replay(history: Sequence[Event], base: Regime = EMPTY) -> Regime:
    """Replay a history from base (genesis by default).

    Every certified regime must equal the replay of its recorded history.
    """
    r = base
    for e in history:
        r = step(r, e)
    return r
