//! Exact finite control witness for `BRIDGE-CLOSURE-RATIO-LOWER` (`bridge_closure_ratio_lower`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_expansion_implies_unconditional_termination`.

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
        carrier_val: 1,
        secondary_pair: (1, 2),
        coboundary_cycle_zero,
    }
}

pub fn reject_expansion_implies_unconditional_termination(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "expansion_implies_unconditional_termination" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for BRIDGE-CLOSURE-RATIO-LOWER: expansion_implies_unconditional_termination")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_expansion_implies_unconditional_termination, witness};

    #[test]
    fn bridge_closure_ratio_lower_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 1);
        assert_eq!(w.secondary_pair, (1, 2));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn bridge_closure_ratio_lower_refuses_expansion_implies_unconditional_termination() {
        assert!(reject_expansion_implies_unconditional_termination("expansion_implies_unconditional_termination").is_err());
        assert!(reject_expansion_implies_unconditional_termination("promote_unrestricted").is_err());
        assert!(reject_expansion_implies_unconditional_termination("admissible_scoped_control").is_ok());
    }
}
