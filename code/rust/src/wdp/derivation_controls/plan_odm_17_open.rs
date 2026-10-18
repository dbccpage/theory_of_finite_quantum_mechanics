#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_plan_odm_17_open(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "PLAN-ODM-17-OPEN",
            domain: "odm_17_xlm_transfer_comparison",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (4, 128, 1);
    if candidate != expected {
        return ControlReceipt {
            control_id: "PLAN-ODM-17-OPEN",
            domain: "odm_17_xlm_transfer_comparison",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "PLAN-ODM-17-OPEN",
        domain: "odm_17_xlm_transfer_comparison",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_plan_odm_17_open_scoped_control() {
    let ok = evaluate_plan_odm_17_open((4, 128, 1), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (4, 128, 1));

    let drifted = evaluate_plan_odm_17_open((4 + 1, 128, 1), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_plan_odm_17_open((4, 128, 1), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
