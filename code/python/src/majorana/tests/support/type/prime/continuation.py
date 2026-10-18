"""Continuation types for Prime 002 halting policy and anti-cheat laws (OE003-*)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AntiCheatFlags:
    """Six anti-cheat halting laws (OE003-02). True = law violated → halt."""

    degree_laundering: bool = False
    lift_laundering: bool = False
    anomalon_evasion: bool = False
    skeleton_destroyed: bool = False
    detector_not_revalidated: bool = False
    dishonest_first_unresolved: bool = False

    def any_violation(self) -> bool:
        return any(
            (
                self.degree_laundering,
                self.lift_laundering,
                self.anomalon_evasion,
                self.skeleton_destroyed,
                self.detector_not_revalidated,
                self.dishonest_first_unresolved,
            )
        )

    def violation_names(self) -> Tuple[str, ...]:
        names = []
        if self.degree_laundering:
            names.append("NoDegreeLaundering")
        if self.lift_laundering:
            names.append("NoLiftLaundering")
        if self.anomalon_evasion:
            names.append("NoAnomalonEvasion")
        if self.skeleton_destroyed:
            names.append("OldSkeletonPreservation")
        if self.detector_not_revalidated:
            names.append("DetectorRevalidation")
        if self.dishonest_first_unresolved:
            names.append("FirstUnresolvedDegreeHonesty")
        return tuple(names)


@dataclass(frozen=True)
class CanContinueInput:
    """Inputs to CanContinue_n (OE003-01). Booleans are already decided by hosts."""

    outstanding_obligation: bool
    higher_obligation_witness: bool
    next_carrier_declared: bool
    adapter_sound: bool
    detector_adequate: bool
    minimal_licensed_lift: bool
    skeleton_preserved: bool
    budget_available: bool
    gtla_continuation_refusal: bool
    anti_cheat: AntiCheatFlags
    budget_total: float = 1.0
    cost_floor: float = 0.1
    ops_so_far: int = 0


@dataclass(frozen=True)
class CanContinueResult:
    may_continue: bool
    reason: str
    max_ops: int
    anti_cheat_violations: Tuple[str, ...]
    authority_effect: str = "None"
