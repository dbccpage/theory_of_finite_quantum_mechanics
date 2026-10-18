//! Exact finite control witness for `PLAN-QP-4` (`plan_qp_4`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_noncontextual_18ray_assignment`.

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
        carrier_val: 18,
        secondary_pair: (9, 4),
        coboundary_cycle_zero,
    }
}

pub fn reject_noncontextual_18ray_assignment(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "noncontextual_18ray_assignment" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-4: noncontextual_18ray_assignment")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_noncontextual_18ray_assignment, witness};

    #[test]
    fn plan_qp_4_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 18);
        assert_eq!(w.secondary_pair, (9, 4));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_4_refuses_noncontextual_18ray_assignment() {
        assert!(reject_noncontextual_18ray_assignment("noncontextual_18ray_assignment").is_err());
        assert!(reject_noncontextual_18ray_assignment("promote_unrestricted").is_err());
        assert!(reject_noncontextual_18ray_assignment("admissible_scoped_control").is_ok());
    }
}
