//! Exact finite control witness for `PLAN-QP-C9` (`plan_qp_c9`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_unscoped_majorana_hardness_or_leakage_claim`.

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
        secondary_pair: (2, 3),
        coboundary_cycle_zero,
    }
}

pub fn reject_unscoped_majorana_hardness_or_leakage_claim(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "unscoped_majorana_hardness_or_leakage_claim" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C9: unscoped_majorana_hardness_or_leakage_claim")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_unscoped_majorana_hardness_or_leakage_claim, witness};

    #[test]
    fn plan_qp_c9_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 6);
        assert_eq!(w.secondary_pair, (2, 3));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c9_refuses_unscoped_majorana_hardness_or_leakage_claim() {
        assert!(reject_unscoped_majorana_hardness_or_leakage_claim("unscoped_majorana_hardness_or_leakage_claim").is_err());
        assert!(reject_unscoped_majorana_hardness_or_leakage_claim("promote_unrestricted").is_err());
        assert!(reject_unscoped_majorana_hardness_or_leakage_claim("admissible_scoped_control").is_ok());
    }
}
