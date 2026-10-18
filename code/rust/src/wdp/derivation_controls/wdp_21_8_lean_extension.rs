#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_wdp_21_8_lean_extension(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "WDP-21-8-LEAN-EXTENSION",
            domain: "ch21_8_lean_scope_accounting",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (154, 124, 30);
    if candidate != expected {
        return ControlReceipt {
            control_id: "WDP-21-8-LEAN-EXTENSION",
            domain: "ch21_8_lean_scope_accounting",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "WDP-21-8-LEAN-EXTENSION",
        domain: "ch21_8_lean_scope_accounting",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_wdp_21_8_lean_extension_scoped_control() {
    let ok = evaluate_wdp_21_8_lean_extension((154, 124, 30), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (154, 124, 30));

    let drifted = evaluate_wdp_21_8_lean_extension((154 + 1, 124, 30), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_wdp_21_8_lean_extension((154, 124, 30), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
