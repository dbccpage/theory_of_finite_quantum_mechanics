from __future__ import annotations
from .witness import check_claim_index_parity, witness_wdp_dp4_03

def test_wdp_dp4_03_claim_index_parity() -> None:
    summary = witness_wdp_dp4_03()
    assert summary["positive_status"] == "PASS"
    assert summary["matched_count"] == 3
    assert summary["negative_status"] == "REFUSED"
    assert summary["negative_missing_lean"] == ["WDP-THM-9.3"]

def test_wdp_dp4_03_refuses_orphan_and_empty_sets() -> None:
    empty = check_claim_index_parity((), (), (), ())
    assert empty.status == "REFUSED"
    assert empty.reason == "EMPTY_EXPECTED_CLAIM_SET"
    orphan = check_claim_index_parity(("C1",), ("C1", "C2"), ("C1",), ("C1",))
    assert orphan.status == "REFUSED"
    assert orphan.reason == "UNDECLARED_ORPHAN_CLAIM_ID"
