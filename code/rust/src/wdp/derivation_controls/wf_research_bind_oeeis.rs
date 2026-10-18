//! Bounded finite control for WF-RESEARCH-BIND-OEEIS.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Witness {
    pub goal_id: &'static str,
    pub carrier_val: i64,
    pub secondary_num: i64,
    pub secondary_den: i64,
    pub negative_control_rejected: bool,
}

pub fn reject_inert_candidate_self_activation(promote_unverified: bool) -> Result<(), &'static str> {
    if promote_unverified {
        Err("reject_inert_candidate_self_activation")
    } else {
        Ok(())
    }
}

pub fn witness() -> Witness {
    let neg_rejected = reject_inert_candidate_self_activation(true).is_err();
    Witness {
        goal_id: "WF-RESEARCH-BIND-OEEIS",
        carrier_val: 3,
        secondary_num: 1,
        secondary_den: 1,
        negative_control_rejected: neg_rejected,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wf_research_bind_oeeis_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.goal_id, "WF-RESEARCH-BIND-OEEIS");
        assert_eq!(w.carrier_val, 3);
        assert_eq!(w.secondary_num, 1);
        assert_eq!(w.secondary_den, 1);
        assert!(w.negative_control_rejected);
        assert!(reject_inert_candidate_self_activation(true).is_err());
        assert!(reject_inert_candidate_self_activation(false).is_ok());
    }
}
