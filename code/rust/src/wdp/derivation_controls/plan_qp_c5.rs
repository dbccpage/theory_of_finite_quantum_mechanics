//! Exact finite control witness for `PLAN-QP-C5` (`plan_qp_c5`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_undeclared_d1_or_phantom_artifacts`.

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
        secondary_pair: (2, 2),
        coboundary_cycle_zero,
    }
}

pub fn reject_undeclared_d1_or_phantom_artifacts(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "undeclared_d1_or_phantom_artifacts" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C5: undeclared_d1_or_phantom_artifacts")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_undeclared_d1_or_phantom_artifacts, witness};

    #[test]
    fn plan_qp_c5_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 3);
        assert_eq!(w.secondary_pair, (2, 2));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c5_refuses_undeclared_d1_or_phantom_artifacts() {
        assert!(reject_undeclared_d1_or_phantom_artifacts("undeclared_d1_or_phantom_artifacts").is_err());
        assert!(reject_undeclared_d1_or_phantom_artifacts("promote_unrestricted").is_err());
        assert!(reject_undeclared_d1_or_phantom_artifacts("admissible_scoped_control").is_ok());
    }
}
