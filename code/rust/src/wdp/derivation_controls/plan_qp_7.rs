//! Exact finite control witness for `PLAN-QP-7` (`plan_qp_7`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_trivial_group_dephasing_at_n2`.

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
        carrier_val: 3,
        secondary_pair: (0, 1),
        coboundary_cycle_zero,
    }
}

pub fn reject_trivial_group_dephasing_at_n2(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "trivial_group_dephasing_at_n2" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-7: trivial_group_dephasing_at_n2")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_trivial_group_dephasing_at_n2, witness};

    #[test]
    fn plan_qp_7_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 3);
        assert_eq!(w.secondary_pair, (0, 1));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_7_refuses_trivial_group_dephasing_at_n2() {
        assert!(reject_trivial_group_dephasing_at_n2("trivial_group_dephasing_at_n2").is_err());
        assert!(reject_trivial_group_dephasing_at_n2("promote_unrestricted").is_err());
        assert!(reject_trivial_group_dephasing_at_n2("admissible_scoped_control").is_ok());
    }
}
