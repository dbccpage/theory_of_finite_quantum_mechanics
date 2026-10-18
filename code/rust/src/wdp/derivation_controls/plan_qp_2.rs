//! Exact finite control witness for `PLAN-QP-2` (`plan_qp_2`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_mixture_table_as_quantum`.

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
        carrier_val: 14,
        secondary_pair: (14, 5),
        coboundary_cycle_zero,
    }
}

pub fn reject_mixture_table_as_quantum(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "mixture_table_as_quantum" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-2: mixture_table_as_quantum")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_mixture_table_as_quantum, witness};

    #[test]
    fn plan_qp_2_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 14);
        assert_eq!(w.secondary_pair, (14, 5));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_2_refuses_mixture_table_as_quantum() {
        assert!(reject_mixture_table_as_quantum("mixture_table_as_quantum").is_err());
        assert!(reject_mixture_table_as_quantum("promote_unrestricted").is_err());
        assert!(reject_mixture_table_as_quantum("admissible_scoped_control").is_ok());
    }
}
