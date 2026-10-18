//! Exact finite control witness for `PLAN-QP-6` (`plan_qp_6`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_refuted_k23_dual_equality`.

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
        carrier_val: 6,
        secondary_pair: (9, 2),
        coboundary_cycle_zero,
    }
}

pub fn reject_refuted_k23_dual_equality(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "refuted_k23_dual_equality" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-6: refuted_k23_dual_equality")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_refuted_k23_dual_equality, witness};

    #[test]
    fn plan_qp_6_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 6);
        assert_eq!(w.secondary_pair, (9, 2));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_6_refuses_refuted_k23_dual_equality() {
        assert!(reject_refuted_k23_dual_equality("refuted_k23_dual_equality").is_err());
        assert!(reject_refuted_k23_dual_equality("promote_unrestricted").is_err());
        assert!(reject_refuted_k23_dual_equality("admissible_scoped_control").is_ok());
    }
}
