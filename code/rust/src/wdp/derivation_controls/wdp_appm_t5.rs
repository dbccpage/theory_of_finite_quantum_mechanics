#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_wdp_appm_t5(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "WDP-APPM-T5",
            domain: "topological_charge_involution",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (1, -1, 4);
    if candidate != expected {
        return ControlReceipt {
            control_id: "WDP-APPM-T5",
            domain: "topological_charge_involution",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "WDP-APPM-T5",
        domain: "topological_charge_involution",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_wdp_appm_t5_scoped_control() {
    let ok = evaluate_wdp_appm_t5((1, -1, 4), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (1, -1, 4));

    let drifted = evaluate_wdp_appm_t5((1 + 1, -1, 4), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_wdp_appm_t5((1, -1, 4), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
