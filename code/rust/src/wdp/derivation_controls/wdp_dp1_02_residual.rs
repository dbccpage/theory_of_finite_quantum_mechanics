#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlReceipt {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub status: &'static str,
    pub invariant_tuple: (i64, i64, i64),
    pub reason: &'static str,
}

pub fn evaluate_wdp_dp1_02_residual(
    candidate: (i64, i64, i64),
    allow_unrestricted_promotion: bool,
) -> ControlReceipt {
    if allow_unrestricted_promotion {
        return ControlReceipt {
            control_id: "WDP-DP1-02-RESIDUAL",
            domain: "dp1_countermodel_no_total_fn",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "UNRESTRICTED_PROMOTION_REFUSED",
        };
    }
    let expected = (3, 2, 0);
    if candidate != expected {
        return ControlReceipt {
            control_id: "WDP-DP1-02-RESIDUAL",
            domain: "dp1_countermodel_no_total_fn",
            status: "REFUSED",
            invariant_tuple: candidate,
            reason: "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        };
    }
    ControlReceipt {
        control_id: "WDP-DP1-02-RESIDUAL",
        domain: "dp1_countermodel_no_total_fn",
        status: "PASS",
        invariant_tuple: expected,
        reason: "SCOPED_CONTROL_VERIFIED",
    }
}

#[test]
fn test_wdp_dp1_02_residual_scoped_control() {
    let ok = evaluate_wdp_dp1_02_residual((3, 2, 0), false);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.invariant_tuple, (3, 2, 0));

    let drifted = evaluate_wdp_dp1_02_residual((3 + 1, 2, 0), false);
    assert_eq!(drifted.status, "REFUSED");
    assert_eq!(drifted.reason, "INVARIANT_MISMATCH_ON_DECLARED_CARRIER");

    let promoted = evaluate_wdp_dp1_02_residual((3, 2, 0), true);
    assert_eq!(promoted.status, "REFUSED");
    assert_eq!(promoted.reason, "UNRESTRICTED_PROMOTION_REFUSED");
}
