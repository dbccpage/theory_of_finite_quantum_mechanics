from __future__ import annotations
from .witness import check_pfp_persistence_and_calibration, witness_wdp_dp6_01_residual

def test_wdp_dp6_01_residual_persistence_and_calibration() -> None:
    summary = witness_wdp_dp6_01_residual()
    assert summary["positive_status"] == "PASS"
    assert summary["persisted_rounds"] == 3
    assert summary["negative_status"] == "REFUSED"
    assert summary["negative_reason"] == "CALIBRATION_THRESHOLD_EXCEEDED"

def test_wdp_dp6_01_residual_refuses_digest_drift() -> None:
    res = check_pfp_persistence_and_calibration(("sha256:r1",), ("sha256:r2",), (10,), 100, 20)
    assert res.status == "REFUSED"
    assert res.reason == "PERSISTENCE_DIGEST_DRIFT"
