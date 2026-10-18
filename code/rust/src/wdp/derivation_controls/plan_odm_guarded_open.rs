#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_plan_odm_guarded_open(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "PLAN-ODM-GUARDED-OPEN",
            domain: "guarded_history_higher_cell_control",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (8, 12, 6);
    if candidate != expected {
        return ControlReceipt {
            control_id: "PLAN-ODM-GUARDED-OPEN",
            domain: "guarded_history_higher_cell_control",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "PLAN-ODM-GUARDED-OPEN",
        domain: "guarded_history_higher_cell_control",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_plan_odm_guarded_open_scoped_control() {
    let ok = evaluate_plan_odm_guarded_open((8, 12, 6), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (8, 12, 6));

    let drifted = evaluate_plan_odm_guarded_open((8 + 1, 12, 6), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_plan_odm_guarded_open((8, 12, 6), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
