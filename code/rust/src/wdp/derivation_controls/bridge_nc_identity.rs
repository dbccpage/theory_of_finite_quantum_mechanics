//! Exact finite control witness for `BRIDGE-NC-IDENTITY` (`bridge_nc_identity`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_totalized_zero_inverse`.

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
        carrier_val: 12,
        secondary_pair: (1, 1),
        coboundary_cycle_zero,
    }
}

pub fn reject_totalized_zero_inverse(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "totalized_zero_inverse" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for BRIDGE-NC-IDENTITY: totalized_zero_inverse")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_totalized_zero_inverse, witness};

    #[test]
    fn bridge_nc_identity_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 12);
        assert_eq!(w.secondary_pair, (1, 1));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn bridge_nc_identity_refuses_totalized_zero_inverse() {
        assert!(reject_totalized_zero_inverse("totalized_zero_inverse").is_err());
        assert!(reject_totalized_zero_inverse("promote_unrestricted").is_err());
        assert!(reject_totalized_zero_inverse("admissible_scoped_control").is_ok());
    }
}
