//! P3 Transferable Guard Library (PROD-P3) exact verifier.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TransferOutcome {
    Accepted { net_savings_num: i64, net_savings_den: i64 },
    Refused { code: String },
}

pub fn verify_guard_transfer(
    parent_digest_matches: bool,
    sound_on_valid: bool,
    trace_verified: bool,
    net_savings_num: i64,
    net_savings_den: i64,
) -> TransferOutcome {
    if !parent_digest_matches {
        return TransferOutcome::Refused {
            code: "PARENT_DIGEST_MISMATCH".to_string(),
        };
    }
    if !sound_on_valid {
        return TransferOutcome::Refused {
            code: "UNSOUND_GUARD".to_string(),
        };
    }
    if !trace_verified || net_savings_den <= 0 || net_savings_num <= 0 {
        return TransferOutcome::Refused {
            code: "TRACE_REJECTED".to_string(),
        };
    }
    TransferOutcome::Accepted {
        net_savings_num,
        net_savings_den,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p3_guard_transfer_verification() {
        assert_eq!(
            verify_guard_transfer(true, true, true, 15, 2),
            TransferOutcome::Accepted {
                net_savings_num: 15,
                net_savings_den: 2
            }
        );
        assert_eq!(
            verify_guard_transfer(false, true, true, 15, 2),
            TransferOutcome::Refused {
                code: "PARENT_DIGEST_MISMATCH".to_string()
            }
        );
    }
}
