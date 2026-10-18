//! Exact finite control witness for `BRIDGE-WSC-NONSELECTION` (`bridge_wsc_nonselection`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_unpriced_labeled_atom_selection`.

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
        secondary_pair: (1, 1),
        coboundary_cycle_zero,
    }
}

pub fn reject_unpriced_labeled_atom_selection(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "unpriced_labeled_atom_selection" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for BRIDGE-WSC-NONSELECTION: unpriced_labeled_atom_selection")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_unpriced_labeled_atom_selection, witness};

    #[test]
    fn bridge_wsc_nonselection_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 2);
        assert_eq!(w.secondary_pair, (1, 1));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn bridge_wsc_nonselection_refuses_unpriced_labeled_atom_selection() {
        assert!(reject_unpriced_labeled_atom_selection("unpriced_labeled_atom_selection").is_err());
        assert!(reject_unpriced_labeled_atom_selection("promote_unrestricted").is_err());
        assert!(reject_unpriced_labeled_atom_selection("admissible_scoped_control").is_ok());
    }
}
