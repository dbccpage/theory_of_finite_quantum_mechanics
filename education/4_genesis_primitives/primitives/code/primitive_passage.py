"""Primitive Passage Dynamics, Active Obstruction Four-Gate Decomposition, and Observers.

Selected educational models related to 19L57G1:
- code/derivation/primitive_passage.py
- code/derivation/diff_interface.py
- lean4/Derivation/PrimitivePassage.lean
- lean4/Derivation/DiffInterface.lean

Classification: Dynamic passage apparatus & active obstruction calculus.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional, Sequence

from .canonical import validate_typed_fields

Pair = tuple[int, int]
Col = tuple[int, ...]
Cols = tuple[Col, ...]
PEvent = tuple[object, ...]


# ---------------------------------------------------------------------------
# Composed State: Passage State (PS / PState)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PS:
    """The passage state (Lean PState).

    Carries separated stores:
    - occ: occurrence identities (0-cells)
    - asserted: asserted difference pairs
    - wit: retained positive witness store (1-cells)
    - prot: protected-demand store (deontic fidelity constraints)
    - obs: declared observation partition columns, or None before any observer is declared
    - budget: fuel budget for operations
    - licensed: operational authorization gate
    - refusals: certificate-bearing refusal records
    - halted: absorbing terminal flag
    """

    occ: tuple[int, ...] = ()
    asserted: tuple[Pair, ...] = ()
    wit: tuple[Pair, ...] = ()
    prot: tuple[Pair, ...] = ()
    obs: Optional[Cols] = None
    budget: int = 0
    licensed: bool = True
    refusals: tuple[Pair, ...] = ()
    halted: bool = False

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def json(self) -> dict[str, object]:
        return {
            "occ": list(self.occ),
            "asserted": [list(p) for p in self.asserted],
            "wit": [list(p) for p in self.wit],
            "prot": [list(p) for p in self.prot],
            "obs": [list(c) for c in self.obs] if self.obs is not None else None,
            "budget": self.budget,
            "licensed": self.licensed,
            "refusals": [list(p) for p in self.refusals],
            "halted": self.halted,
        }


GENESIS_P = PS()


# ---------------------------------------------------------------------------
# Observation Semantics & Zero Relations
# ---------------------------------------------------------------------------


def sep_col(c: Col, i: int, j: int) -> bool:
    """One observation column separates two occurrence positions."""
    return (i in c) != (j in c)


def sep_p(cols: Cols, i: int, j: int) -> bool:
    """Observer separation: at least one declared column separates i and j."""
    return any(sep_col(c, i, j) for c in cols)


def zero_p(cols: Cols, i: int, j: int) -> bool:
    """The zero relation of a declared observation: no declared column separates i and j.

    Defined only when observation is declared; a pre-observational state has no zero relation.
    """
    return not sep_p(cols, i, j)


# ---------------------------------------------------------------------------
# Active Obstruction: Four Total Gates Decomposition
# ---------------------------------------------------------------------------


def retained_p(s: PS, i: int, j: int) -> bool:
    """Gate 1: The pair is admitted into the retained witness store."""
    return (i, j) in s.wit


def protected_p(s: PS, i: int, j: int) -> bool:
    """Gate 2: The pair is admitted into the protected-demand store."""
    return (i, j) in s.prot


def declared_p(s: PS) -> bool:
    """Gate 3: An observation has been declared (obs is not None)."""
    return s.obs is not None


def zero_p_gate(s: PS, i: int, j: int) -> bool:
    """Gate 4: The declared observation fails to separate the pair."""
    if s.obs is None:
        return False
    return zero_p(s.obs, i, j)


def obst_p(s: PS, i: int, j: int) -> bool:
    """Active obstruction predicate: product of all four independent gates.

    obst_p(s, i, j) <==> retained_p && protected_p && declared_p && zero_p_gate.
    No one gate follows from the other three (proven in Lean gate_*_independent).
    """
    return retained_p(s, i, j) and protected_p(s, i, j) and declared_p(s) and zero_p_gate(s, i, j)


# ---------------------------------------------------------------------------
# Well-formedness and Acceptance Guards
# ---------------------------------------------------------------------------


def wf_pair(s: PS, i: int, j: int) -> bool:
    """Well-formed pair on the occurrence carrier."""
    return (
        type(i) is int and type(j) is int and i != j and 0 <= i < len(s.occ) and 0 <= j < len(s.occ)
    )


def _refined(cols: Cols, v: Col, p: int) -> Cols:
    return tuple((p,) + c if c == v else c for c in cols)


def refine_ok(s: PS, v: Col, p: int) -> bool:
    """Guard for refining an existing column with point p."""
    if (
        s.obs is None
        or type(v) is not tuple
        or type(p) is not int
        or not 0 <= p < len(s.occ)
        or any(type(index) is not int or not 0 <= index < len(s.occ) for index in v)
    ):
        return False
    cols = s.obs
    return (
        v in cols
        and p not in v
        and any(obst_p(s, r[0], r[1]) and sep_col((p,) + v, r[0], r[1]) for r in s.prot)
        and all(
            (not sep_p(cols, r[0], r[1])) or sep_p(_refined(cols, v, p), r[0], r[1]) for r in s.prot
        )
    )


def col_ok(s: PS, c: Col) -> bool:
    """Guard for adding a fresh column c."""
    if s.obs is None or type(c) is not tuple:
        return False
    return (
        all(type(p) is int and 0 <= p < len(s.occ) for p in c)
        and c not in s.obs
        and any(obst_p(s, r[0], r[1]) and sep_col(c, r[0], r[1]) for r in s.prot)
    )


# ---------------------------------------------------------------------------
# Guarded Step Function (pstep) and Replay
# ---------------------------------------------------------------------------


def pstep(s: PS, e: PEvent) -> PS:
    """The guarded passage step function (Lean step).

    Enforces dedup admission, well-formedness guards, certificate-bearing refusal,
    budget/license gates on structure creation, and absorbing terminal state.
    """
    kind = e[0]
    if kind == "halt":
        return replace(s, halted=True)
    if s.halted:
        return s
    if kind == "admitOcc":
        t = e[1]
        if type(t) is not int or t < 0:
            raise ValueError("Occurrence tokens must be exact natural numbers")
        if t in s.occ:
            return s
        return replace(s, occ=s.occ + (t,))
    if kind == "assertWit":
        i, j = e[1], e[2]
        if type(i) is not int or type(j) is not int:
            raise ValueError("Occurrence positions must be exact integers")
        if wf_pair(s, i, j) and (i, j) not in s.asserted:
            return replace(s, asserted=s.asserted + ((i, j),))
        return s
    if kind == "admitWit":
        i, j = e[1], e[2]
        if type(i) is not int or type(j) is not int:
            raise ValueError("Occurrence positions must be exact integers")
        if wf_pair(s, i, j) and (i, j) in s.asserted and (i, j) not in s.wit:
            return replace(s, wit=s.wit + ((i, j),))
        return s
    if kind == "protect":
        i, j = e[1], e[2]
        if type(i) is not int or type(j) is not int:
            raise ValueError("Occurrence positions must be exact integers")
        if wf_pair(s, i, j) and (i, j) in s.wit and (i, j) not in s.prot:
            return replace(s, prot=s.prot + ((i, j),))
        return s
    if kind == "declareObs":
        if s.obs is None:
            return replace(s, obs=())
        return s
    if kind == "refineCol":
        v, p = e[1], e[2]
        if type(v) is not tuple or type(p) is not int:
            raise ValueError("Refinement requires an immutable column and integer position")
        if refine_ok(s, v, p) and s.budget > 0 and s.obs is not None:
            return replace(s, obs=_refined(s.obs, v, p), budget=max(0, s.budget - 1))
        return s
    if kind == "addCol":
        c = e[1]
        if type(c) is not tuple:
            raise ValueError("An observation column must be an immutable tuple")
        if col_ok(s, c) and s.licensed and s.budget > 0 and s.obs is not None:
            return replace(s, obs=s.obs + (c,), budget=max(0, s.budget - 1))
        return s
    if kind == "refuse":
        i, j = e[1], e[2]
        if type(i) is not int or type(j) is not int:
            raise ValueError("Occurrence positions must be exact integers")
        if wf_pair(s, i, j) and obst_p(s, i, j) and (i, j) not in s.refusals:
            return replace(s, refusals=s.refusals + ((i, j),))
        return s
    if kind == "setBudget":
        n = e[1]
        if type(n) is not int or n < 0:
            raise ValueError("Budget must be an exact natural number")
        return replace(s, budget=n)
    if kind == "setLicense":
        b = e[1]
        if type(b) is not bool:
            raise ValueError("License flag must be a Boolean")
        return replace(s, licensed=b)
    return s


def preplay(events: Sequence[PEvent], base: PS = GENESIS_P) -> PS:
    """Replay a passage event history from base."""
    s = base
    for e in events:
        s = pstep(s, e)
    return s


# ---------------------------------------------------------------------------
# Composed Observer Interface & Obstruction Records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DiffObs:
    """Native difference observer interface.

    Carries zero relation, value projection, and certified equivalence properties.
    """

    carrier_size: int
    zero_rel: frozenset[Pair]

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def is_reflexive(self) -> bool:
        return all((x, x) in self.zero_rel for x in range(self.carrier_size))

    def is_symmetric(self) -> bool:
        return all((y, x) in self.zero_rel for (x, y) in self.zero_rel)

    def is_transitive(self) -> bool:
        for x, y in self.zero_rel:
            for z in range(self.carrier_size):
                if (y, z) in self.zero_rel and (x, z) not in self.zero_rel:
                    return False
        return True


@dataclass(frozen=True)
class ActiveObstruction:
    """Record of an active obstruction: normative conflict between protected
    retained difference and observer blindness.
    """

    pair: Pair
    retained: bool
    protected: bool
    observation_declared: bool
    observer_zero: bool

    def __post_init__(self) -> None:
        validate_typed_fields(self)


@dataclass(frozen=True)
class BareReflection:
    """Record of an unobstructed collapse in the absence of fidelity protection."""

    pair: Pair
    zero_holds: bool
    protected: bool = False

    def __post_init__(self) -> None:
        validate_typed_fields(self)
