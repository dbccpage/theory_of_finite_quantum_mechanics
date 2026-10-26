"""Genesis Primitives Category 15: Trace Algebra, Mazurkiewicz Monoids & Causal Concurrency.

Selected educational models related to 19L57G1 (lean4/Derivation/TraceAlgebra.lean, code/derivation/trace_algebra.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Typed transition records, event commutation laws, Mazurkiewicz traces, and
the causal partial order of discrete relational dynamics without an external clock.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import cast

from .canonical import validate_typed_fields
from .primitive_passage import PS, Col, Cols, PEvent, pstep


@dataclass(frozen=True)
class TRecord:
    """Candidate transition record; an exact snapshot requires guarded replay."""

    pre: PS
    ev: PEvent
    post: PS
    discharged: bool

    def __post_init__(self) -> None:
        validate_typed_fields(self)

    def is_well_formed(self) -> bool:
        from .transition_and_trace import guard_holds

        try:
            return self.post == pstep(self.pre, self.ev) and self.discharged == guard_holds(
                self.pre, self.ev
            )
        except (KeyError, TypeError, ValueError, IndexError):
            return False


def post_of(s: PS, e: PEvent) -> PS:
    """The post-state installed when event e's guard is discharged."""
    kind = e[0]
    if kind == "admitOcc":
        return replace(s, occ=s.occ + (cast(int, e[1]),))
    if kind == "assertWit":
        return replace(s, asserted=s.asserted + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "admitWit":
        return replace(s, wit=s.wit + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "protect":
        return replace(s, prot=s.prot + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "declareObs":
        return replace(s, obs=())
    if kind == "refineCol":
        if s.obs is None:
            return s
        v, p = cast(Col, e[1]), cast(int, e[2])
        cols: Cols = tuple((p,) + c if c == v else c for c in s.obs)
        return replace(s, obs=cols, budget=s.budget - 1)
    if kind == "addCol":
        if s.obs is None:
            return s
        return replace(s, obs=s.obs + (cast(Col, e[1]),), budget=s.budget - 1)
    if kind == "refuse":
        return replace(s, refusals=s.refusals + ((cast(int, e[1]), cast(int, e[2])),))
    if kind == "setBudget":
        return replace(s, budget=cast(int, e[1]))
    if kind == "setLicense":
        return replace(s, licensed=cast(bool, e[1]))
    return replace(s, halted=True)


def are_independent_events(e1: PEvent, e2: PEvent) -> bool:
    """Decides whether two events are causally independent (commute in effect)."""
    k1, k2 = e1[0], e2[0]
    # Events affecting disjoint state stores commute
    disjoint_pairs = {
        ("assertWit", "setBudget"),
        ("setBudget", "assertWit"),
        ("admitWit", "setBudget"),
        ("setBudget", "admitWit"),
        ("protect", "setBudget"),
        ("setBudget", "protect"),
        ("admitOcc", "setLicense"),
        ("setLicense", "admitOcc"),
    }
    return (k1, k2) in disjoint_pairs


def trace_commutes(s: PS, e1: PEvent, e2: PEvent) -> bool:
    """Verifies that sequential application order does not alter the terminal state."""
    s12 = pstep(pstep(s, e1), e2)
    s21 = pstep(pstep(s, e2), e1)
    return s12 == s21
