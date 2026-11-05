"""Concrete product target selection gate (WDP-DP8-01-RESIDUAL)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ProductTargetSelectionReceipt:
    status: str
    selected_targets: tuple[str, ...]
    reason: str

def verify_product_target_selection(
    targets: tuple[dict[str, str], ...],
) -> ProductTargetSelectionReceipt:
    if not targets:
        return ProductTargetSelectionReceipt("REFUSED", (), "EMPTY_PRODUCT_TARGET_SET")
    selected: list[str] = []
    required_keys = ("target_id", "consumer", "defect_witness", "rust_owner", "deciding_check")
    for item in targets:
        for key in required_keys:
            val = item.get(key, "").strip()
            if not val:
                return ProductTargetSelectionReceipt("REFUSED", tuple(selected), f"MISSING_FIELD:{key}")
        if not item["rust_owner"].startswith("omega_engine/crates_rs/"):
            return ProductTargetSelectionReceipt("REFUSED", tuple(selected), "NON_CANONICAL_RUST_OWNER")
        selected.append(item["target_id"])
    return ProductTargetSelectionReceipt("PASS", tuple(selected), "CONCRETE_PRODUCT_TARGETS_VERIFIED")

def witness_wdp_dp8_01_residual() -> dict[str, object]:
    valid_targets = (
        {
            "target_id": "TARGET-1-PROTECTED-QUESTION-SEAM",
            "consumer": "omega_engine_woland",
            "defect_witness": "unwitnessed_summary_collapse",
            "rust_owner": "omega_engine/crates_rs/omega_wdp/src/lib.rs",
            "deciding_check": "cargo test -p omega_wdp",
        },
        {
            "target_id": "TARGET-2-PARITY-BRIDGE",
            "consumer": "omega_engine_pfp",
            "defect_witness": "untyped_packet_fallback",
            "rust_owner": "omega_engine/crates_rs/omega_symbol_game/src/lib.rs",
            "deciding_check": "cargo test -p omega_symbol_game",
        },
    )
    ok = verify_product_target_selection(valid_targets)
    bad = verify_product_target_selection(
        (
            {
                "target_id": "TARGET-BAD",
                "consumer": "omega_engine_woland",
                "defect_witness": "",
                "rust_owner": "omega_engine/crates_rs/omega_wdp/src/lib.rs",
                "deciding_check": "cargo test -p omega_wdp",
            },
        )
    )
    return {
        "control_id": "WDP-DP8-01-RESIDUAL",
        "positive_status": ok.status,
        "selected_count": len(ok.selected_targets),
        "negative_status": bad.status,
        "negative_reason": bad.reason,
    }
