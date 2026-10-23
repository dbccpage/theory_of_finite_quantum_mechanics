"""Finite PFP persistence and calibration check (WDP-DP6-01-RESIDUAL)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PfpPersistenceCalibrationReceipt:
    status: str
    persisted_rounds: int
    max_brier_num: int
    reason: str

def check_pfp_persistence_and_calibration(
    round_digests: tuple[str, ...],
    persisted_digests: tuple[str, ...],
    brier_numerators: tuple[int, ...],
    brier_denom: int,
    max_allowed_num: int,
) -> PfpPersistenceCalibrationReceipt:
    if not round_digests or brier_denom <= 0 or len(round_digests) != len(brier_numerators):
        return PfpPersistenceCalibrationReceipt("REFUSED", 0, 0, "INVALID_ROUND_OR_CALIBRATION_INPUT")
    if round_digests != persisted_digests:
        return PfpPersistenceCalibrationReceipt("REFUSED", 0, 0, "PERSISTENCE_DIGEST_DRIFT")
    peak = max(brier_numerators)
    if any(b < 0 for b in brier_numerators) or peak > max_allowed_num:
        return PfpPersistenceCalibrationReceipt("REFUSED", len(round_digests), peak, "CALIBRATION_THRESHOLD_EXCEEDED")
    return PfpPersistenceCalibrationReceipt("PASS", len(round_digests), peak, "PERSISTENCE_AND_CALIBRATION_VERIFIED")

def witness_wdp_dp6_01_residual() -> dict[str, object]:
    digests = ("sha256:r1", "sha256:r2", "sha256:r3")
    ok = check_pfp_persistence_and_calibration(digests, digests, (12, 15, 11), 100, 20)
    bad = check_pfp_persistence_and_calibration(digests, digests, (12, 25, 11), 100, 20)
    return {
        "control_id": "WDP-DP6-01-RESIDUAL",
        "positive_status": ok.status,
        "persisted_rounds": ok.persisted_rounds,
        "negative_status": bad.status,
        "negative_reason": bad.reason,
    }
