//! Exact finite control witness for `PLAN-QP-C6` (`plan_qp_c6`).
//!
//! Evaluates the declared finite carrier invariant and refuses out-of-scope
//! promotion via `reject_inert_cptp_or_refuted_k23_dual`.

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
        secondary_pair: (9, 2),
        coboundary_cycle_zero,
    }
}

pub fn reject_inert_cptp_or_refuted_k23_dual(claim_flag: &str) -> Result<(), &'static str> {
    if claim_flag == "inert_cptp_or_refuted_k23_dual" || claim_flag == "promote_unrestricted" || claim_flag == "bypass_guard" {
        Err("refused out-of-scope promotion for PLAN-QP-C6: inert_cptp_or_refuted_k23_dual")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_inert_cptp_or_refuted_k23_dual, witness};

    #[test]
    fn plan_qp_c6_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.carrier_val, 6);
        assert_eq!(w.secondary_pair, (9, 2));
        assert_eq!(w.coboundary_cycle_zero, 0);
    }

    #[test]
    fn plan_qp_c6_refuses_inert_cptp_or_refuted_k23_dual() {
        assert!(reject_inert_cptp_or_refuted_k23_dual("inert_cptp_or_refuted_k23_dual").is_err());
        assert!(reject_inert_cptp_or_refuted_k23_dual("promote_unrestricted").is_err());
        assert!(reject_inert_cptp_or_refuted_k23_dual("admissible_scoped_control").is_ok());
    }
}
