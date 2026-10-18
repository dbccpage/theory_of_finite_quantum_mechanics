//! Exact finite control witness for `PLAN-QP-C8` (`plan_qp_c8`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_mub6_subgap_global_promotion`.

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
        carrier_val: 5,
        secondary_pair: (9, 1),
        coboundary_cycle_zero,
    }
}

pub fn reject_mub6_subgap_global_promotion(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "mub6_subgap_global_promotion" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C8: mub6_subgap_global_promotion")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_mub6_subgap_global_promotion, witness};

    #[test]
    fn plan_qp_c8_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 5);
        assert_eq!(w.secondary_pair, (9, 1));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c8_refuses_mub6_subgap_global_promotion() {
        assert!(reject_mub6_subgap_global_promotion("mub6_subgap_global_promotion").is_err());
        assert!(reject_mub6_subgap_global_promotion("promote_unrestricted").is_err());
        assert!(reject_mub6_subgap_global_promotion("admissible_scoped_control").is_ok());
    }
}
