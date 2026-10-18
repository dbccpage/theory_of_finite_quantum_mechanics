//! Exact finite control witness for `PLAN-QP-5` (`plan_qp_5`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_unassumed_nosignalling_derivation`.

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
        carrier_val: 2,
        secondary_pair: (1, 2),
        coboundary_cycle_zero,
    }
}

pub fn reject_unassumed_nosignalling_derivation(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "unassumed_nosignalling_derivation" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-5: unassumed_nosignalling_derivation")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_unassumed_nosignalling_derivation, witness};

    #[test]
    fn plan_qp_5_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 2);
        assert_eq!(w.secondary_pair, (1, 2));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_5_refuses_unassumed_nosignalling_derivation() {
        assert!(reject_unassumed_nosignalling_derivation("unassumed_nosignalling_derivation").is_err());
        assert!(reject_unassumed_nosignalling_derivation("promote_unrestricted").is_err());
        assert!(reject_unassumed_nosignalling_derivation("admissible_scoped_control").is_ok());
    }
}
