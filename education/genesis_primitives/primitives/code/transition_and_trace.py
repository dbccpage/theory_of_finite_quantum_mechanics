"""Transition Alphabet, DDC 8-Letter Trace Primitives, and Trace Algebra.

Selected educational models related to 19L57G1:
- code/derivation/transition_alphabet.py
- code/derivation/trace_algebra.py
- lean4/Derivation/TransitionAlphabet.lean
- lean4/Derivation/TraceAlgebra.lean

Classification: Transition monoid, trace calculus, and DDC operational alphabet.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from .canonical import validate_typed_fields
from .primitive_passage import (
    PS,
    Col,
    Pair,
    PEvent,
    col_ok,
    obst_p,
    pstep,
    refine_ok,
    wf_pair,
)

# ---------------------------------------------------------------------------
# Discrete Deformation Calculus (DDC) 8-Letter Operational Alphabet
# ---------------------------------------------------------------------------

DDC_ALPHABET = ("E", "R", "C", "I", "LAMBDA", "D", "M", "T")

FIELDS: tuple[str, ...] = (
    "occ",
    "asserted",
    "wit",
    "prot",
    "obs",
    "budget",
    "licensed",
    "refusals",
    "halted",
)

GUARD_OF: dict[str, str] = {
    "admitOcc": "freshOcc",
    "assertWit": "wfAssert",
    "admitWit": "assertedWit",
    "protect": "witnessedProt",
    "declareObs": "preObservational",
    "refineCol": "refineOk",
    "addCol": "colOk",
    "refuse": "obstRefuse",
    "setBudget": "budgetMove",
    "setLicense": "licenseMove",
    "halt": "activeHalt",
}

ORIGIN_OF: dict[str, str] = {
    "admitOcc": "env",
    "assertWit": "env",
    "admitWit": "env",
    "protect": "env",
    "declareObs": "int",
    "refineCol": "int",
    "addCol": "int",
    "refuse": "int",
    "setBudget": "env",
    "setLicense": "env",
    "halt": "env",
}


# ---------------------------------------------------------------------------
# Transition Guards and State Effects
# ---------------------------------------------------------------------------


def accepted(s: PS, e: PEvent) -> bool:
    """Lean Accepted: the event transition modifies the passage state."""
    return pstep(s, e) != s


def guard_holds(s: PS, e: PEvent) -> bool:
    """Lean guardHolds: exact acceptance condition constructor by constructor."""
    kind = e[0]
    if kind == "halt":
        return not s.halted
    if s.halted:
        return False
    if kind == "admitOcc":
        return cast(int, e[1]) not in s.occ
    if kind == "assertWit":
        i, j = cast(int, e[1]), cast(int, e[2])
        return wf_pair(s, i, j) and (i, j) not in s.asserted
    if kind == "admitWit":
        i, j = cast(int, e[1]), cast(int, e[2])
        return wf_pair(s, i, j) and (i, j) in s.asserted and (i, j) not in s.wit
    if kind == "protect":
        i, j = cast(int, e[1]), cast(int, e[2])
        return (i, j) in s.wit and (i, j) not in s.prot
    if kind == "declareObs":
        return s.obs is None
    if kind == "refineCol":
        return refine_ok(s, cast(Col, e[1]), cast(int, e[2])) and s.budget > 0
    if kind == "addCol":
        return col_ok(s, cast(Col, e[1])) and s.licensed and s.budget > 0
    if kind == "refuse":
        i, j = cast(int, e[1]), cast(int, e[2])
        return obst_p(s, i, j) and (i, j) not in s.refusals
    if kind == "setBudget":
        return cast(int, e[1]) != s.budget
    return cast(bool, e[1]) != s.licensed


def field_delta(s: PS, t: PS) -> tuple[bool, ...]:
    """Lean fieldDelta: boolean indicator for each of the 9 fields."""
    return (
        t.occ != s.occ,
        t.asserted != s.asserted,
        t.wit != s.wit,
        t.prot != s.prot,
        t.obs != s.obs,
        t.budget != s.budget,
        t.licensed != s.licensed,
        t.refusals != s.refusals,
        t.halted != s.halted,
    )


def obstructed_pairs(s: PS) -> tuple[Pair, ...]:
    return tuple(r for r in s.prot if obst_p(s, r[0], r[1]))


def obst_effect(s: PS, t: PS) -> str:
    """Lean obstEffect: removed, created, untouched, or preserved."""
    before = obstructed_pairs(s)
    after = obstructed_pairs(t)
    lost = tuple(r for r in before if r not in after)
    gained = tuple(r for r in after if r not in before)
    if lost:
        return "removed"
    if gained:
        return "created"
    if not before:
        return "untouched"
    return "preserved"


def budget_delta(s: PS, t: PS) -> str:
    """Lean budgetDeltaOf: unchanged, spentOne, or rewritten."""
    if t.budget == s.budget:
        return "unchanged"
    if t.budget + 1 == s.budget:
        return "spentOne"
    return "rewritten"


def continuity_of(t: PS) -> str:
    """Lean continuityOf: absorption if halted else continuation."""
    return "absorption" if t.halted else "continuation"


Profile = tuple[tuple[bool, ...], str, str, str, str, str, bool]
Sig = tuple[tuple[bool, ...], str, str, str, str]
EffectSig = tuple[tuple[bool, ...], str, str, str]


def profile_of(s: PS, e: PEvent) -> Profile:
    """Full 7-component effect profile."""
    t = pstep(s, e)
    kind = cast(str, e[0])
    return (
        field_delta(s, t),
        GUARD_OF[kind],
        obst_effect(s, t),
        budget_delta(s, t),
        continuity_of(t),
        ORIGIN_OF[kind],
        accepted(s, e),
    )


# ---------------------------------------------------------------------------
# Composed Trace Record: TRecord
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TRecord:
    """Lean TRecord: typed transition record.
    pre: pre-state
    ev: passage event
    guard: discharged guard identifier
    post: post-state
    cls: equivalence class signature
    spend: resource budget delta
    profile: full 7-component effect profile
    """

    pre: PS
    ev: PEvent
    guard: str
    post: PS
    cls: str
    spend: str
    profile: Profile

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def is_well_formed(self) -> bool:
        try:
            return self == make_record(self.pre, self.ev)
        except (KeyError, TypeError, ValueError, IndexError):
            return False


def make_record(s: PS, e: PEvent) -> TRecord:
    """Construct a certified transition record from state and event."""
    t = pstep(s, e)
    kind = cast(str, e[0])
    prof = profile_of(s, e)
    cls_sig = f"{GUARD_OF[kind]}:{obst_effect(s, t)}:{budget_delta(s, t)}"
    return TRecord(
        pre=s,
        ev=e,
        guard=GUARD_OF[kind],
        post=t,
        cls=cls_sig,
        spend=budget_delta(s, t),
        profile=prof,
    )
