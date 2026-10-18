#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_dec_wdp_repin(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "DEC-WDP-REPIN",
            domain: "wdp_release_repin_decision",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (2183, 2184, 1);
    if candidate != expected {
        return ControlReceipt {
            control_id: "DEC-WDP-REPIN",
            domain: "wdp_release_repin_decision",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "DEC-WDP-REPIN",
        domain: "wdp_release_repin_decision",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_dec_wdp_repin_scoped_control() {
    let ok = evaluate_dec_wdp_repin((2183, 2184, 1), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (2183, 2184, 1));

    let drifted = evaluate_dec_wdp_repin((2183 + 1, 2184, 1), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_dec_wdp_repin((2183, 2184, 1), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
