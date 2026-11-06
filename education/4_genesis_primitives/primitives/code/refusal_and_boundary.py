"""Refusal Disciplines, Epistemic Frontiers, Represented Worlds, and Interpreter Boundaries.

Selected educational models related to 19L57G1:
- code/derivation/refusal.py
- code/derivation/refusal_frontier.py
- code/derivation/represented.py
- code/derivation/interpreter_boundary.py
- code/derivation/controller_category.py
- lean4/Derivation/Refusal.lean
- lean4/Derivation/Represented.lean
- lean4/Derivation/Constitution.lean

Classification: Refusal semantics, world models, and metatheoretic boundaries.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Union

from .canonical import validate_typed_fields

Token = str
Pair = tuple[int, int]
View = tuple[int, ...]
Req = tuple[int, int]


# ---------------------------------------------------------------------------
# Refusal Discipline Primitive Events
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Sup:
    """External supply of token in refusal comparison."""

    tok: Token

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class Adm:
    """Admission of token in refusal comparison."""

    tok: Token

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class Form:
    """Admission of unary judgment form."""


@dataclass(frozen=True)
class Inst:
    """Admission of instance on datum index."""

    idx: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)


REv = Union[Sup, Adm, Form, Inst]


# ---------------------------------------------------------------------------
# Composed Refusal State: RSt / RState
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RSt:
    """Refusal comparison state:
    data: admitted tokens in order
    tags: indices tagged by discipline reification
    refusals: count of recorded refusal events
    has_form: whether unary form has been admitted
    insts: set of data indices carrying the instance
    """

    data: tuple[Token, ...]
    tags: frozenset[int]
    refusals: int
    has_form: bool
    insts: frozenset[int]

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def json(self) -> dict[str, object]:
        return {
            "data": list(self.data),
            "tags": sorted(self.tags),
            "refusals": self.refusals,
            "has_form": self.has_form,
            "insts": sorted(self.insts),
        }


EMPTY_RST = RSt((), frozenset(), 0, False, frozenset())


# ---------------------------------------------------------------------------
# Re-admission Disciplines (5 Canonical Disciplines)
# ---------------------------------------------------------------------------

Discipline = Callable[[RSt, Token], RSt]


def readmit_silent(s: RSt, tok: Token) -> RSt:
    """Silent discipline: re-presentation of existing token is a no-op."""
    return s


def readmit_meta(s: RSt, tok: Token) -> RSt:
    """Meta discipline: marker in history only, state unchanged."""
    return s


def readmit_fact(s: RSt, tok: Token) -> RSt:
    """Fact discipline: increments internal refusal counter."""
    return RSt(s.data, s.tags, s.refusals + 1, s.has_form, s.insts)


def readmit_reify_untagged(s: RSt, tok: Token) -> RSt:
    """Reify untagged: appends token as new datum without tag."""
    return RSt(s.data + (tok,), s.tags, s.refusals, s.has_form, s.insts)


def readmit_reify_tagged(s: RSt, tok: Token) -> RSt:
    """Reify tagged: appends token as new datum with reification tag."""
    new_tags = s.tags | {len(s.data)}
    return RSt(s.data + (tok,), new_tags, s.refusals, s.has_form, s.insts)


DISCIPLINES: Mapping[str, Discipline] = {
    "silent": readmit_silent,
    "meta": readmit_meta,
    "fact": readmit_fact,
    "reify_untagged": readmit_reify_untagged,
    "reify_tagged": readmit_reify_tagged,
}


# ---------------------------------------------------------------------------
# Composed World: Represented-Progress Kernel State
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class World:
    """Exact represented-progress kernel state (Lean World):
    - data: admitted data carrier indices
    - views: observation views (subsets of data)
    - reqs: persistent separation requirements
    - refusals: certificate-bearing refusal records
    - budget: fuel budget
    - aug_licensed: extension licensing gate
    - notes: monotonic history notes
    """

    data: tuple[int, ...] = ()
    views: tuple[View, ...] = ()
    reqs: tuple[Req, ...] = ()
    refusals: tuple[Req, ...] = ()
    budget: int = 0
    aug_licensed: bool = True
    notes: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def json(self) -> dict[str, object]:
        return {
            "data": list(self.data),
            "views": [list(v) for v in self.views],
            "reqs": [list(r) for r in self.reqs],
            "refusals": [list(r) for r in self.refusals],
            "budget": self.budget,
            "aug_licensed": self.aug_licensed,
            "notes": list(self.notes),
        }


GENESIS_WORLD = World()


def sep(c: View, i: int, j: int) -> bool:
    """View separation."""
    return (i in c) != (j in c)


def sat(w: World, r: Req) -> bool:
    """Requirement satisfaction: some view separates the pair."""
    return any(sep(c, r[0], r[1]) for c in w.views)


def viol(w: World, r: Req) -> bool:
    """Requirement violation: requirement is imposed but not satisfied."""
    return r in w.reqs and not sat(w, r)


def quiescent(w: World) -> bool:
    """Quiescence: every imposed requirement is satisfied."""
    return all(sat(w, r) for r in w.reqs)


# ---------------------------------------------------------------------------
# Composed Type: Constitution Description (Desc / ConstitutionDesc)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Desc:
    """A constitution description: six independent boolean toggles,
    one per load-bearing guard of the sealed kernel.
    Inert quotation data; only interp_step gives it an interpretation.

    - dedup_admit: whether datum admission deduplicates on token identity
    - guard_require: whether requirements require valid data indices
    - guard_accept: whether response items require positive progress
    - gate_budget: whether budget decrements on structural transitions
    - gate_license: whether licensing is required for extensions
    - cert_refusal: whether refusal requires exhaustion certificate
    """

    dedup_admit: bool
    guard_require: bool
    guard_accept: bool
    gate_budget: bool
    gate_license: bool
    cert_refusal: bool

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def to_index(self) -> int:
        """Encode the 6 toggles into a canonical integer 0..63."""
        bits = [
            self.dedup_admit,
            self.guard_require,
            self.guard_accept,
            self.gate_budget,
            self.gate_license,
            self.cert_refusal,
        ]
        return sum((1 if b else 0) << k for k, b in enumerate(bits))

    @staticmethod
    def from_index(idx: int) -> "Desc":
        """Decode an integer 0..63 into a Desc."""
        return Desc(
            dedup_admit=bool(idx & 1),
            guard_require=bool(idx & 2),
            guard_accept=bool(idx & 4),
            gate_budget=bool(idx & 8),
            gate_license=bool(idx & 16),
            cert_refusal=bool(idx & 32),
        )


KERNEL_DESC = Desc(True, True, True, True, True, True)


# ---------------------------------------------------------------------------
# Composed Type: Controller Category Description (KindDesc)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KindDesc:
    """Controller category state description:
    (name, has_obstruction, has_declared_obs, is_halted).
    """

    name: str
    has_obstruction: bool
    has_declared_obs: bool
    is_halted: bool

    def __post_init__(self) -> None:
        validate_typed_fields(self)


# ---------------------------------------------------------------------------
# Composed Types: Refusal Frontier Protocol & State (Proto, FState)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Proto:
    """Protocol space over refusal and reflection (Frontier Run 006):
    - algebra: number of admission-result constructors (1 or 2)
    - retention: none, judgment, occurrence, or datum
    - tagging: whether datum-mode receipts carry unary observable
    - reflection: whether receipts may themselves be presented
    - autorel: whether receipt asserts relation from refused subject
    - tokens: number of distinct tokens (1 or 2)
    """

    algebra: int
    retention: str
    tagging: bool
    reflection: bool
    autorel: bool
    tokens: int

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def valid(self) -> bool:
        if self.retention not in ("none", "judgment", "occurrence", "datum"):
            return False
        if self.retention != "datum" and (self.tagging or self.reflection or self.autorel):
            return False
        return self.algebra in (1, 2) and self.tokens in (1, 2)


@dataclass(frozen=True)
class FState:
    """Frontier State for refusal exploration."""

    data: tuple[Token, ...]
    tags: frozenset[int]
    judgments: tuple[int, ...]
    rel: frozenset[Pair]
    results_seen: int = 0

    def __post_init__(self) -> None:
        validate_typed_fields(self)
