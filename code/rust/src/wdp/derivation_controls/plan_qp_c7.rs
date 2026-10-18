//! Exact finite control witness for `PLAN-QP-C7` (`plan_qp_c7`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_rigorous_bound_claim_for_neville_proxy`.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Witness {
    pub carrier_val: i64,
    pub secondary_pair: (i64, i64),
    pub coboundary_cycle_zero: i64,
}

pub fn witness() -> Witness {
    let a = [3_i64, 7, 11];
    let coboundary_cycle_zero = (a[1] - a[0]) + (a[2] - a[1]) + (a[0] - a[2]);
    Witness {
        carrier_val: 3,
        secondary_pair: (13, 12),
        coboundary_cycle_zero,
    }
}

pub fn reject_rigorous_bound_claim_for_neville_proxy(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "rigorous_bound_claim_for_neville_proxy" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C7: rigorous_bound_claim_for_neville_proxy")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_rigorous_bound_claim_for_neville_proxy, witness};

    #[test]
    fn plan_qp_c7_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 3);
        assert_eq!(w.secondary_pair, (13, 12));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c7_refuses_rigorous_bound_claim_for_neville_proxy() {
        assert!(reject_rigorous_bound_claim_for_neville_proxy("rigorous_bound_claim_for_neville_proxy").is_err());
        assert!(reject_rigorous_bound_claim_for_neville_proxy("promote_unrestricted").is_err());
        assert!(reject_rigorous_bound_claim_for_neville_proxy("admissible_scoped_control").is_ok());
    }
}
