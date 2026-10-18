#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SingleWitnessAuditReceipt {
    pub status: &'static str,
    pub sufficient: bool,
    pub collision_count: usize,
    pub reason: &'static str,
}

pub fn audit_single_witness_sufficiency(
    question_values: &[i64],
    witness_values: &[i64],
) -> SingleWitnessAuditReceipt {
    if question_values.is_empty() || question_values.len() != witness_values.len() {
        return SingleWitnessAuditReceipt {
            status: "REFUSED",
            sufficient: false,
            collision_count: 0,
            reason: "INVALID_CARRIER_LENGTH",
        };
    }
    let mut collisions = 0usize;
    for i in 0..question_values.len() {
        for j in (i + 1)..question_values.len() {
            if question_values[i] != question_values[j] && witness_values[i] == witness_values[j] {
                collisions += 1;
            }
        }
    }
    if collisions > 0 {
        return SingleWitnessAuditReceipt {
            status: "REFUSED",
            sufficient: false,
            collision_count: collisions,
            reason: "WITNESS_COLLISION_ON_PROTECTED_QUESTION",
        };
    }
    SingleWitnessAuditReceipt {
        status: "PASS",
        sufficient: true,
        collision_count: 0,
        reason: "SINGLE_WITNESS_FACTORS_QUESTION_EXACTLY",
    }
}

#[test]
fn test_wdp_p2a_residual_single_witness_sufficiency() {
    let q = [0, 1, 1];
    let w_good = [10, 20, 20];
    let w_bad = [10, 10, 20];
    let ok = audit_single_witness_sufficiency(&q, &w_good);
    assert_eq!(ok.status, "PASS");
    assert!(ok.sufficient);

    let bad = audit_single_witness_sufficiency(&q, &w_bad);
    assert_eq!(bad.status, "REFUSED");
    assert_eq!(bad.collision_count, 1);
}
