//! P2 Provenance-Gated Output Layer (PROD-P2) exact verifier.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GateVerdict {
    Accepted { midpoint: i64, radius_num: i64, radius_den: i64 },
    Refused { reason: String },
}

pub fn gate_measurement_output(
    indication_mapped: bool,
    uncertainty_num: i64,
    uncertainty_den: i64,
    midpoint: i64,
) -> GateVerdict {
    if !indication_mapped {
        return GateVerdict::Refused {
            reason: "UNMAPPED_INDICATION".to_string(),
        };
    }
    if uncertainty_den <= 0 || uncertainty_num < 0 {
        return GateVerdict::Refused {
            reason: "INVALID_UNCERTAINTY".to_string(),
        };
    }
    GateVerdict::Accepted {
        midpoint,
        radius_num: uncertainty_num,
        radius_den: uncertainty_den,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p2_provenance_gate() {
        assert_eq!(
            gate_measurement_output(true, 3, 2, -12),
            GateVerdict::Accepted {
                midpoint: -12,
                radius_num: 3,
                radius_den: 2
            }
        );
        assert_eq!(
            gate_measurement_output(true, -1, 10, -12),
            GateVerdict::Refused {
                reason: "INVALID_UNCERTAINTY".to_string()
            }
        );
    }
}
