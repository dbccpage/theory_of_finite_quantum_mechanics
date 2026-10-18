#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_ch19_o04(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "CH19-O04",
            domain: "ch19_calibration_authentication",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (3, 15, 20);
    if candidate != expected {
        return ControlReceipt {
            control_id: "CH19-O04",
            domain: "ch19_calibration_authentication",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "CH19-O04",
        domain: "ch19_calibration_authentication",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_ch19_o04_scoped_control() {
    let ok = evaluate_ch19_o04((3, 15, 20), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (3, 15, 20));

    let drifted = evaluate_ch19_o04((3 + 1, 15, 20), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_ch19_o04((3, 15, 20), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
