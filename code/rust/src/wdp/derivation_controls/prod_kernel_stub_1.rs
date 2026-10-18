//! Finite executable witness for `PROD-KERNEL-STUB-1`.
//!
//! Models `CheckReceipt` replay on the 3-state `cheaper_route` arena (`s --direct(5)--> t`,
//! `s --step(1)--> u --finish(1)--> t`) and on stalled/trapped `LOSS` arenas:
//! - Accepts `WIN_OPTIMAL` with `initial_value = 2/1`.
//! - Accepts `WIN_FEASIBLE` with suboptimal `initial_value = 5/1` without substituting `2/1`.
//! - Rejects forged `WIN_OPTIMAL` claiming `5/1` is optimal.
//! - Distinguishes `LOSS` with `initial_stalled = true` vs `initial_stalled = false`.

#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CertificateClaim {
    Loss,
    WinOptimal,
    WinFeasible,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CheckReceipt {
    pub accepted: bool,
    pub claim: Option<CertificateClaim>,
    pub initial_value_num: Option<i64>,
    pub initial_value_den: Option<i64>,
    pub initial_stalled: Option<bool>,
    pub failures: Vec<&'static str>,
    pub authority_effect: &'static str,
}

/// Replay a submitted strategy certificate on the `cheaper_route` arena:
/// `s --direct(5)--> t`, `s --step(1)--> u --finish(1)--> t`.
/// Never calls a solver and never substitutes the optimal value `2` for a suboptimal or bad certificate.
pub fn replay_cheaper_route_certificate(
    claim: CertificateClaim,
    action_at_s: &str,
    value_s: i64,
    value_u: i64,
    value_t: i64,
    rank_s: i64,
    rank_u: i64,
    rank_t: i64,
) -> CheckReceipt {
    if claim == CertificateClaim::Loss {
        return CheckReceipt {
            accepted: false,
            claim: None,
            initial_value_num: None,
            initial_value_den: None,
            initial_stalled: None,
            failures: vec!["losing region contains a successful terminal"],
            authority_effect: "None",
        };
    }
    if value_t != 0 || rank_t != 0 {
        return CheckReceipt {
            accepted: false,
            claim: None,
            initial_value_num: None,
            initial_value_den: None,
            initial_stalled: None,
            failures: vec!["terminal value and rank must be zero"],
        authority_effect: "None",
        };
    }
    if value_u != 1 + value_t || rank_u <= rank_t {
        return CheckReceipt {
            accepted: false,
            claim: None,
            initial_value_num: None,
            initial_value_den: None,
            initial_stalled: None,
            failures: vec!["upper equality or rank descent failed at u"],
            authority_effect: "None",
        };
    }
    let (selected_cost, succ_val, succ_rank) = match action_at_s {
        "direct" => (5, value_t, rank_t),
        "step" => (1, value_u, rank_u),
        _ => {
            return CheckReceipt {
                accepted: false,
                claim: None,
                initial_value_num: None,
                initial_value_den: None,
                initial_stalled: None,
                failures: vec!["selected action is not admissible"],
                authority_effect: "None",
            }
        }
    };
    if rank_s <= succ_rank {
        return CheckReceipt {
            accepted: false,
            claim: None,
            initial_value_num: None,
            initial_value_den: None,
            initial_stalled: None,
            failures: vec!["strategy leaves winners or fails strict rank descent"],
            authority_effect: "None",
        };
    }
    if value_s != selected_cost + succ_val {
        return CheckReceipt {
            accepted: false,
            claim: None,
            initial_value_num: None,
            initial_value_den: None,
            initial_stalled: None,
            failures: vec!["upper equality failed"],
            authority_effect: "None",
        };
    }
    if claim == CertificateClaim::WinOptimal {
        let alt_direct = 5 + value_t;
        let alt_step = 1 + value_u;
        if value_s > alt_direct || value_s > alt_step {
            return CheckReceipt {
                accepted: false,
                claim: None,
                initial_value_num: None,
                initial_value_den: None,
                initial_stalled: None,
                failures: vec!["lower inequality failed: a cheaper action exists"],
                authority_effect: "None",
            };
        }
    }
    CheckReceipt {
        accepted: true,
        claim: Some(claim),
        initial_value_num: Some(value_s),
        initial_value_den: Some(1),
        initial_stalled: None,
        failures: vec![],
        authority_effect: "None",
    }
}

pub fn replay_loss_certificate(initial_has_moves: bool) -> CheckReceipt {
    CheckReceipt {
        accepted: true,
        claim: Some(CertificateClaim::Loss),
        initial_value_num: None,
        initial_value_den: None,
        initial_stalled: Some(!initial_has_moves),
        failures: vec![],
        authority_effect: "None",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn replays_optimal_feasible_and_forged_certificates_without_substituting_answers() {
        let opt = replay_cheaper_route_certificate(
            CertificateClaim::WinOptimal,
            "step",
            2,
            1,
            0,
            2,
            1,
            0,
        );
        assert!(opt.accepted);
        assert_eq!(opt.claim, Some(CertificateClaim::WinOptimal));
        assert_eq!(opt.initial_value_num, Some(2));

        let feas = replay_cheaper_route_certificate(
            CertificateClaim::WinFeasible,
            "direct",
            5,
            1,
            0,
            1,
            1,
            0,
        );
        assert!(feas.accepted);
        assert_eq!(feas.claim, Some(CertificateClaim::WinFeasible));
        assert_eq!(feas.initial_value_num, Some(5));

        let forged = replay_cheaper_route_certificate(
            CertificateClaim::WinOptimal,
            "direct",
            5,
            1,
            0,
            1,
            1,
            0,
        );
        assert!(!forged.accepted);
        assert_eq!(forged.claim, None);
        assert_eq!(
            forged.failures,
            vec!["lower inequality failed: a cheaper action exists"]
        );
    }

    #[test]
    fn distinguishes_stalled_and_trapped_loss_certificates() {
        let stalled = replay_loss_certificate(false);
        assert!(stalled.accepted);
        assert_eq!(stalled.initial_stalled, Some(true));

        let trapped = replay_loss_certificate(true);
        assert!(trapped.accepted);
        assert_eq!(trapped.initial_stalled, Some(false));
    }
}
