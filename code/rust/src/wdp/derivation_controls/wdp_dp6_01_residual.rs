#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PfpPersistenceCalibrationReceipt {
    pub status: &'static str,
    pub persisted_rounds: usize,
    pub max_brier_num: i64,
    pub reason: &'static str,
}

pub fn check_pfp_persistence_and_calibration(
    round_digests: &[&str],
    persisted_digests: &[&str],
    brier_numerators: &[i64],
    brier_denom: i64,
    max_allowed_num: i64,
) -> PfpPersistenceCalibrationReceipt {
    if round_digests.is_empty()
        || brier_denom <= 0
        || round_digests.len() != brier_numerators.len()
    {
        return PfpPersistenceCalibrationReceipt {
            status: "REFUSED",
            persisted_rounds: 0,
            max_brier_num: 0,
            reason: "INVALID_ROUND_OR_CALIBRATION_INPUT",
        };
    }
    if round_digests != persisted_digests {
        return PfpPersistenceCalibrationReceipt {
            status: "REFUSED",
            persisted_rounds: 0,
            max_brier_num: 0,
            reason: "PERSISTENCE_DIGEST_DRIFT",
        };
    }
    let peak = *brier_numerators.iter().max().unwrap_or(&0);
    if brier_numerators.iter().any(|&b| b < 0) || peak > max_allowed_num {
        return PfpPersistenceCalibrationReceipt {
            status: "REFUSED",
            persisted_rounds: round_digests.len(),
            max_brier_num: peak,
            reason: "CALIBRATION_THRESHOLD_EXCEEDED",
        };
    }
    PfpPersistenceCalibrationReceipt {
        status: "PASS",
        persisted_rounds: round_digests.len(),
        max_brier_num: peak,
        reason: "PERSISTENCE_AND_CALIBRATION_VERIFIED",
    }
}

#[test]
fn test_wdp_dp6_01_residual_persistence_and_calibration() {
    let digests = ["sha256:r1", "sha256:r2", "sha256:r3"];
    let ok = check_pfp_persistence_and_calibration(&digests, &digests, &[12, 15, 11], 100, 20);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.persisted_rounds, 3);

    let bad = check_pfp_persistence_and_calibration(&digests, &digests, &[12, 25, 11], 100, 20);
    assert_eq!(bad.status, "REFUSED");
    assert_eq!(bad.reason, "CALIBRATION_THRESHOLD_EXCEEDED");
}
