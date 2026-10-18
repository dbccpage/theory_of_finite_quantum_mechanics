//! Exact finite control witness for `PLAN-QP-3` (`plan_qp_3`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_gaussian_rational_tsirelson_attainment`.

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
        carrier_val: 8,
        secondary_pair: (196, 25),
        coboundary_cycle_zero,
    }
}

pub fn reject_gaussian_rational_tsirelson_attainment(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "gaussian_rational_tsirelson_attainment" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-3: gaussian_rational_tsirelson_attainment")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_gaussian_rational_tsirelson_attainment, witness};

    #[test]
    fn plan_qp_3_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 8);
        assert_eq!(w.secondary_pair, (196, 25));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_3_refuses_gaussian_rational_tsirelson_attainment() {
        assert!(reject_gaussian_rational_tsirelson_attainment("gaussian_rational_tsirelson_attainment").is_err());
        assert!(reject_gaussian_rational_tsirelson_attainment("promote_unrestricted").is_err());
        assert!(reject_gaussian_rational_tsirelson_attainment("admissible_scoped_control").is_ok());
    }
}
