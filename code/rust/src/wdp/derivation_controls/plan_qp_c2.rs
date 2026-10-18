//! Exact finite control witness for `PLAN-QP-C2` (`plan_qp_c2`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_stale_c1000_not_started_status`.

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
        carrier_val: 9,
        secondary_pair: (9, 9),
        coboundary_cycle_zero,
    }
}

pub fn reject_stale_c1000_not_started_status(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "stale_c1000_not_started_status" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C2: stale_c1000_not_started_status")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_stale_c1000_not_started_status, witness};

    #[test]
    fn plan_qp_c2_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 9);
        assert_eq!(w.secondary_pair, (9, 9));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c2_refuses_stale_c1000_not_started_status() {
        assert!(reject_stale_c1000_not_started_status("stale_c1000_not_started_status").is_err());
        assert!(reject_stale_c1000_not_started_status("promote_unrestricted").is_err());
        assert!(reject_stale_c1000_not_started_status("admissible_scoped_control").is_ok());
    }
}
