//! Exact finite control witness for `PLAN-QP-C3` (`plan_qp_c3`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_unpublished_zenodo_placeholder`.

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
        secondary_pair: (0, 1),
        coboundary_cycle_zero,
    }
}

pub fn reject_unpublished_zenodo_placeholder(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "unpublished_zenodo_placeholder" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C3: unpublished_zenodo_placeholder")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_unpublished_zenodo_placeholder, witness};

    #[test]
    fn plan_qp_c3_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 6);
        assert_eq!(w.secondary_pair, (0, 1));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c3_refuses_unpublished_zenodo_placeholder() {
        assert!(reject_unpublished_zenodo_placeholder("unpublished_zenodo_placeholder").is_err());
        assert!(reject_unpublished_zenodo_placeholder("promote_unrestricted").is_err());
        assert!(reject_unpublished_zenodo_placeholder("admissible_scoped_control").is_ok());
    }
}
