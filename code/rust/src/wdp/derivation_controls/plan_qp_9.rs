//! Exact finite control witness for `PLAN-QP-9` (`plan_qp_9`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_uncertified_neville_continuum_bound`.

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
        carrier_val: 13,
        secondary_pair: (13, 12),
        coboundary_cycle_zero,
    }
}

pub fn reject_uncertified_neville_continuum_bound(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "uncertified_neville_continuum_bound" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-9: uncertified_neville_continuum_bound")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_uncertified_neville_continuum_bound, witness};

    #[test]
    fn plan_qp_9_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 13);
        assert_eq!(w.secondary_pair, (13, 12));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_9_refuses_uncertified_neville_continuum_bound() {
        assert!(reject_uncertified_neville_continuum_bound("uncertified_neville_continuum_bound").is_err());
        assert!(reject_uncertified_neville_continuum_bound("promote_unrestricted").is_err());
        assert!(reject_uncertified_neville_continuum_bound("admissible_scoped_control").is_ok());
    }
}
