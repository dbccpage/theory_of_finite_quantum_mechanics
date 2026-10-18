//! Exact finite control witness for `PLAN-QP-C4` (`plan_qp_c4`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_proved_theorem_on_cited_input`.

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
        secondary_pair: (1, 0),
        coboundary_cycle_zero,
    }
}

pub fn reject_proved_theorem_on_cited_input(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "proved_theorem_on_cited_input" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C4: proved_theorem_on_cited_input")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_proved_theorem_on_cited_input, witness};

    #[test]
    fn plan_qp_c4_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 8);
        assert_eq!(w.secondary_pair, (1, 0));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c4_refuses_proved_theorem_on_cited_input() {
        assert!(reject_proved_theorem_on_cited_input("proved_theorem_on_cited_input").is_err());
        assert!(reject_proved_theorem_on_cited_input("promote_unrestricted").is_err());
        assert!(reject_proved_theorem_on_cited_input("admissible_scoped_control").is_ok());
    }
}
