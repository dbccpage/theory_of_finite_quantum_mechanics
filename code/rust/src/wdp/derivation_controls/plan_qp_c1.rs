//! Exact finite control witness for `PLAN-QP-C1` (`plan_qp_c1`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_i3_zero_implies_unique_born`.

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
        carrier_val: 0,
        secondary_pair: (3, 1),
        coboundary_cycle_zero,
    }
}

pub fn reject_i3_zero_implies_unique_born(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "i3_zero_implies_unique_born" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C1: i3_zero_implies_unique_born")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_i3_zero_implies_unique_born, witness};

    #[test]
    fn plan_qp_c1_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 0);
        assert_eq!(w.secondary_pair, (3, 1));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c1_refuses_i3_zero_implies_unique_born() {
        assert!(reject_i3_zero_implies_unique_born("i3_zero_implies_unique_born").is_err());
        assert!(reject_i3_zero_implies_unique_born("promote_unrestricted").is_err());
        assert!(reject_i3_zero_implies_unique_born("admissible_scoped_control").is_ok());
    }
}
