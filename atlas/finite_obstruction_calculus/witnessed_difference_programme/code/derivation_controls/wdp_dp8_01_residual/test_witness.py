from __future__ import annotations
from .witness import verify_product_target_selection, witness_wdp_dp8_01_residual

def test_wdp_dp8_01_residual_product_target_selection() -> None:
    summary = witness_wdp_dp8_01_residual()
    assert summary["positive_status"] == "PASS"
    assert summary["selected_count"] == 2
    assert summary["negative_status"] == "REFUSED"
    assert summary["negative_reason"] == "MISSING_FIELD:defect_witness"

def test_wdp_dp8_01_residual_refuses_non_canonical_owner() -> None:
    bad = verify_product_target_selection(
        (
            {
                "target_id": "T1",
                "consumer": "woland",
                "defect_witness": "defect",
                "rust_owner": "scratch/prototype.rs",
                "deciding_check": "cargo test",
            },
        )
    )
    assert bad.status == "REFUSED"
    assert bad.reason == "NON_CANONICAL_RUST_OWNER"
