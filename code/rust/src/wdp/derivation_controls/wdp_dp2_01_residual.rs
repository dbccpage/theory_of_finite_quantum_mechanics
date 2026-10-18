#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RealizationRuleReceipt {
    pub status: &'static str,
    pub realized_count: usize,
    pub reason: &'static str,
}

pub fn check_single_witness_realization_rule(
    questions: &[(&str, &[i64])],
    witnesses: &[(&str, &[i64])],
) -> RealizationRuleReceipt {
    if questions.is_empty() {
        return RealizationRuleReceipt {
            status: "REFUSED",
            realized_count: 0,
            reason: "EMPTY_QUESTION_FAMILY",
        };
    }
    let mut realized = 0usize;
    for (qid, qvec) in questions {
        let Some((_, wvec)) = witnesses.iter().find(|(wid, _)| wid == qid) else {
            return RealizationRuleReceipt {
                status: "REFUSED",
                realized_count: realized,
                reason: "MISSING_OR_MALFORMED_WITNESS",
            };
        };
        if qvec.is_empty() || qvec.len() != wvec.len() {
            return RealizationRuleReceipt {
                status: "REFUSED",
                realized_count: realized,
                reason: "MISSING_OR_MALFORMED_WITNESS",
            };
        }
        for i in 0..qvec.len() {
            for j in (i + 1)..qvec.len() {
                if qvec[i] != qvec[j] && wvec[i] == wvec[j] {
                    return RealizationRuleReceipt {
                        status: "REFUSED",
                        realized_count: realized,
                        reason: "REALIZATION_COLLISION",
                    };
                }
            }
        }
        realized += 1;
    }
    RealizationRuleReceipt {
        status: "PASS",
        realized_count: realized,
        reason: "ALL_QUESTIONS_REALIZED_BY_SINGLE_WITNESS",
    }
}

#[test]
fn test_wdp_dp2_01_residual_realization_rule() {
    let q = [("q_parity", &[0, 1, 0, 1][..]), ("q_sign", &[1, 1, -1, -1][..])];
    let w_good = [("q_parity", &[2, 5, 2, 5][..]), ("q_sign", &[10, 10, 20, 20][..])];
    let w_bad = [("q_parity", &[2, 2, 2, 5][..]), ("q_sign", &[10, 10, 20, 20][..])];
    let ok = check_single_witness_realization_rule(&q, &w_good);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.realized_count, 2);

    let bad = check_single_witness_realization_rule(&q, &w_bad);
    assert_eq!(bad.status, "REFUSED");
    assert_eq!(bad.reason, "REALIZATION_COLLISION");
}
