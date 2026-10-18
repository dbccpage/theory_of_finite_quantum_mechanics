"""Prime 002: CanContinue_n continuation policy stage (OE003-*). AuthorityEffect: None."""

from __future__ import annotations

from typing import Tuple

from ..type.prime.continuation import (
    AntiCheatFlags,
    CanContinueInput,
    CanContinueResult,
)


def can_continue(inp: CanContinueInput) -> CanContinueResult:
    """Evaluate CanContinue_n and budget bound #ops ≤ floor(B/δ)."""
    if inp.cost_floor <= 0:
        return CanContinueResult(
            may_continue=False,
            reason="INVALID_cost_floor",
            max_ops=0,
            anti_cheat_violations=(),
        )
    max_ops = int(inp.budget_total // inp.cost_floor)
    if inp.ops_so_far >= max_ops:
        return CanContinueResult(
            may_continue=False,
            reason="BUDGET_EXHAUSTED",
            max_ops=max_ops,
            anti_cheat_violations=(),
        )
    if inp.anti_cheat.any_violation():
        return CanContinueResult(
            may_continue=False,
            reason="ANTI_CHEAT_HALT",
            max_ops=max_ops,
            anti_cheat_violations=inp.anti_cheat.violation_names(),
        )
    if inp.gtla_continuation_refusal:
        return CanContinueResult(
            may_continue=False,
            reason="GTLA_CONTINUATION_REFUSAL",
            max_ops=max_ops,
            anti_cheat_violations=(),
        )
    conjuncts = (
        inp.outstanding_obligation,
        inp.higher_obligation_witness,
        inp.next_carrier_declared,
        inp.adapter_sound,
        inp.detector_adequate,
        inp.minimal_licensed_lift,
        inp.skeleton_preserved,
        inp.budget_available,
    )
    if not all(conjuncts):
        return CanContinueResult(
            may_continue=False,
            reason="CAN_CONTINUE_FALSE",
            max_ops=max_ops,
            anti_cheat_violations=(),
        )
    return CanContinueResult(
        may_continue=True,
        reason="CAN_CONTINUE_TRUE",
        max_ops=max_ops,
        anti_cheat_violations=(),
    )
