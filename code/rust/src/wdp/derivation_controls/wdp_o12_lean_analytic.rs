#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_wdp_o12_lean_analytic(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "WDP-O12-LEAN-ANALYTIC",
            domain: "o12_thermodynamic_tail_envelope",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (1, 256, 127);
    if candidate != expected {
        return ControlReceipt {
            control_id: "WDP-O12-LEAN-ANALYTIC",
            domain: "o12_thermodynamic_tail_envelope",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "WDP-O12-LEAN-ANALYTIC",
        domain: "o12_thermodynamic_tail_envelope",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_wdp_o12_lean_analytic_scoped_control() {
    let ok = evaluate_wdp_o12_lean_analytic((1, 256, 127), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (1, 256, 127));

    let drifted = evaluate_wdp_o12_lean_analytic((1 + 1, 256, 127), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_wdp_o12_lean_analytic((1, 256, 127), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
