"""Finite claim-index parity check across Lean, Python, and Rust registries (WDP-DP4-03)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ClaimIndexParityReceipt:
    status: str
    matched_ids: tuple[str, ...]
    missing_in_lean: tuple[str, ...]
    missing_in_python: tuple[str, ...]
    missing_in_rust: tuple[str, ...]
    reason: str

def check_claim_index_parity(
    expected_ids: tuple[str, ...],
    lean_ids: tuple[str, ...],
    python_ids: tuple[str, ...],
    rust_ids: tuple[str, ...],
) -> ClaimIndexParityReceipt:
    expected_set = set(expected_ids)
    if not expected_set:
        return ClaimIndexParityReceipt("REFUSED", (), (), (), (), "EMPTY_EXPECTED_CLAIM_SET")
    lean_set = set(lean_ids)
    py_set = set(python_ids)
    rs_set = set(rust_ids)
    missing_lean = tuple(sorted(expected_set - lean_set))
    missing_py = tuple(sorted(expected_set - py_set))
    missing_rs = tuple(sorted(expected_set - rs_set))
    extra = (lean_set | py_set | rs_set) - expected_set
    if missing_lean or missing_py or missing_rs:
        return ClaimIndexParityReceipt(
            "REFUSED",
            tuple(sorted(expected_set & lean_set & py_set & rs_set)),
            missing_lean,
            missing_py,
            missing_rs,
            "MISSING_CLAIM_BINDING",
        )
    if extra:
        return ClaimIndexParityReceipt(
            "REFUSED",
            tuple(sorted(expected_set)),
            (),
            (),
            (),
            "UNDECLARED_ORPHAN_CLAIM_ID",
        )
    return ClaimIndexParityReceipt(
        "PASS",
        tuple(sorted(expected_set)),
        (),
        (),
        (),
        "EXACT_THREE_WAY_CLAIM_PARITY",
    )

def witness_wdp_dp4_03() -> dict[str, object]:
    claims = ("WDP-THM-2.2", "WDP-PROP-4.2", "WDP-THM-9.3")
    ok = check_claim_index_parity(claims, claims, claims, claims)
    bad = check_claim_index_parity(claims, claims[:2], claims, claims)
    return {
        "control_id": "WDP-DP4-03",
        "positive_status": ok.status,
        "matched_count": len(ok.matched_ids),
        "negative_status": bad.status,
        "negative_missing_lean": list(bad.missing_in_lean),
    }
