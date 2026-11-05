"""Single-witness-per-question sufficiency table audit (WDP-P2A-RESIDUAL)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SingleWitnessAuditReceipt:
    status: str
    sufficient: bool
    collision_pairs: tuple[tuple[str, str], ...]
    reason: str

def audit_single_witness_sufficiency(
    states: tuple[str, ...],
    question_values: dict[str, int],
    witness_values: dict[str, int],
) -> SingleWitnessAuditReceipt:
    if not states:
        return SingleWitnessAuditReceipt("REFUSED", False, (), "EMPTY_STATE_CARRIER")
    collisions: list[tuple[str, str]] = []
    for i, s1 in enumerate(states):
        for s2 in states[i + 1 :]:
            if s1 not in question_values or s2 not in question_values:
                return SingleWitnessAuditReceipt("REFUSED", False, (), "MISSING_QUESTION_EVALUATION")
            if s1 not in witness_values or s2 not in witness_values:
                return SingleWitnessAuditReceipt("REFUSED", False, (), "MISSING_WITNESS_EVALUATION")
            if question_values[s1] != question_values[s2] and witness_values[s1] == witness_values[s2]:
                collisions.append((s1, s2))
    if collisions:
        return SingleWitnessAuditReceipt("REFUSED", False, tuple(collisions), "WITNESS_COLLISION_ON_PROTECTED_QUESTION")
    return SingleWitnessAuditReceipt("PASS", True, (), "SINGLE_WITNESS_FACTORS_QUESTION_EXACTLY")

def witness_wdp_p2a_residual() -> dict[str, object]:
    states = ("s0", "s1", "s2")
    q = {"s0": 0, "s1": 1, "s2": 1}
    w_good = {"s0": 10, "s1": 20, "s2": 20}
    w_bad = {"s0": 10, "s1": 10, "s2": 20}
    ok = audit_single_witness_sufficiency(states, q, w_good)
    bad = audit_single_witness_sufficiency(states, q, w_bad)
    return {
        "control_id": "WDP-P2A-RESIDUAL",
        "positive_status": ok.status,
        "positive_sufficient": ok.sufficient,
        "negative_status": bad.status,
        "negative_collisions": [list(p) for p in bad.collision_pairs],
    }
