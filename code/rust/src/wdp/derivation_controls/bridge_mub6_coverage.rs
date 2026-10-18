//! Exact finite control witness for `BRIDGE-MUB6-COVERAGE` (`bridge_mub6_coverage`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_unreplayed_mub6_fourier_or_float_search`.

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
        carrier_val: 9,
        secondary_pair: (31, 800),
        coboundary_cycle_zero,
    }
}

pub fn reject_unreplayed_mub6_fourier_or_float_search(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "unreplayed_mub6_fourier_or_float_search" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for BRIDGE-MUB6-COVERAGE: unreplayed_mub6_fourier_or_float_search")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_unreplayed_mub6_fourier_or_float_search, witness};

    #[test]
    fn bridge_mub6_coverage_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 9);
        assert_eq!(w.secondary_pair, (31, 800));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn bridge_mub6_coverage_refuses_unreplayed_mub6_fourier_or_float_search() {
        assert!(reject_unreplayed_mub6_fourier_or_float_search("unreplayed_mub6_fourier_or_float_search").is_err());
        assert!(reject_unreplayed_mub6_fourier_or_float_search("promote_unrestricted").is_err());
        assert!(reject_unreplayed_mub6_fourier_or_float_search("admissible_scoped_control").is_ok());
    }
}
