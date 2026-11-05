"""Single-witness-per-question realization rule check (WDP-DP2-01-RESIDUAL)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RealizationRuleReceipt:
    status: str
    realized_questions: tuple[str, ...]
    reason: str

def check_single_witness_realization_rule(
    questions: dict[str, tuple[int, ...]],
    witnesses: dict[str, tuple[int, ...]],
) -> RealizationRuleReceipt:
    if not questions:
        return RealizationRuleReceipt("REFUSED", (), "EMPTY_QUESTION_FAMILY")
    realized: list[str] = []
    for q_id, q_vec in sorted(questions.items()):
        w_vec = witnesses.get(q_id)
        if w_vec is None or len(w_vec) != len(q_vec) or not q_vec:
            return RealizationRuleReceipt("REFUSED", tuple(realized), f"MISSING_OR_MALFORMED_WITNESS:{q_id}")
        for i in range(len(q_vec)):
            for j in range(i + 1, len(q_vec)):
                if q_vec[i] != q_vec[j] and w_vec[i] == w_vec[j]:
                    return RealizationRuleReceipt("REFUSED", tuple(realized), f"REALIZATION_COLLISION:{q_id}")
        realized.append(q_id)
    return RealizationRuleReceipt("PASS", tuple(realized), "ALL_QUESTIONS_REALIZED_BY_SINGLE_WITNESS")

def witness_wdp_dp2_01_residual() -> dict[str, object]:
    questions = {"q_parity": (0, 1, 0, 1), "q_sign": (1, 1, -1, -1)}
    good_witnesses = {"q_parity": (2, 5, 2, 5), "q_sign": (10, 10, 20, 20)}
    bad_witnesses = {"q_parity": (2, 2, 2, 5), "q_sign": (10, 10, 20, 20)}
    ok = check_single_witness_realization_rule(questions, good_witnesses)
    bad = check_single_witness_realization_rule(questions, bad_witnesses)
    return {
        "control_id": "WDP-DP2-01-RESIDUAL",
        "positive_status": ok.status,
        "realized_questions": list(ok.realized_questions),
        "negative_status": bad.status,
        "negative_reason": bad.reason,
    }
