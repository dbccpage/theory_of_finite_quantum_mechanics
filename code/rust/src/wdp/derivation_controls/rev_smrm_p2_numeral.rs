//! Numeral-Bearing Measurement & Replay Calculus (REV-SMRM-P2-NUMERAL) exact verifier.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MeasurementStep {
    pub state_id: usize,
    pub observed_class: usize,
    pub calibrated_numeral: u64,
}

pub fn verify_measurement_replay(
    trace: &[MeasurementStep],
    calibration: &[u64],
    expected_total: u64,
) -> bool {
    if trace.is_empty() {
        return false;
    }
    let mut sum = 0u64;
    for step in trace {
        if step.observed_class >= calibration.len() {
            return false;
        }
        if calibration[step.observed_class] != step.calibrated_numeral {
            return false;
        }
        sum += step.calibrated_numeral;
    }
    sum == expected_total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_numeral_replay_verification() {
        let calibration = [10u64, 20, 35];
        let valid_trace = vec![
            MeasurementStep {
                state_id: 0,
                observed_class: 1,
                calibrated_numeral: 20,
            },
            MeasurementStep {
                state_id: 1,
                observed_class: 2,
                calibrated_numeral: 35,
            },
        ];
        assert!(verify_measurement_replay(&valid_trace, &calibration, 55));
        assert!(!verify_measurement_replay(&valid_trace, &calibration, 50));
    }
}
