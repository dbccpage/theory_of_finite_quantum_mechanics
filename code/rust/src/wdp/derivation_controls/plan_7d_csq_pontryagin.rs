#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_plan_7d_csq_pontryagin(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "PLAN-7D-CSQ-PONTRYAGIN",
            domain: "csq_pontryagin_assumption_separation",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (6, 4, 2);
    if candidate != expected {
        return ControlReceipt {
            control_id: "PLAN-7D-CSQ-PONTRYAGIN",
            domain: "csq_pontryagin_assumption_separation",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "PLAN-7D-CSQ-PONTRYAGIN",
        domain: "csq_pontryagin_assumption_separation",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_plan_7d_csq_pontryagin_scoped_control() {
    let ok = evaluate_plan_7d_csq_pontryagin((6, 4, 2), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (6, 4, 2));

    let drifted = evaluate_plan_7d_csq_pontryagin((6 + 1, 4, 2), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_plan_7d_csq_pontryagin((6, 4, 2), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
