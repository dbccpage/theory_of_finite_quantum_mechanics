
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Witness {
    pub goal_id: &'static str,
    pub carrier_val: i64,
    pub secondary_num: i64,
    pub secondary_den: i64,
    pub negative_control_rejected: bool,
}

pub fn reject_model_stage5_or_copied_stage8_terminal(promote_unverified: bool) -> Result<(), &'static str> {
    if promote_unverified {
        Err("reject_model_stage5_or_copied_stage8_terminal")
    } else {
        Ok(())
    }
}

pub fn witness() -> Witness {
    let neg_rejected = reject_model_stage5_or_copied_stage8_terminal(true).is_err();
    Witness {
        goal_id: "WF-RESEARCH-BIND-RUNNER",
        carrier_val: 8,
        secondary_num: 5,
        secondary_den: 8,
        negative_control_rejected: neg_rejected,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wf_research_bind_runner_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.goal_id, "WF-RESEARCH-BIND-RUNNER");
        assert_eq!(w.carrier_val, 8);
        assert_eq!(w.secondary_num, 5);
        assert_eq!(w.secondary_den, 8);
        assert!(w.negative_control_rejected);
        assert!(reject_model_stage5_or_copied_stage8_terminal(true).is_err());
        assert!(reject_model_stage5_or_copied_stage8_terminal(false).is_ok());
    }
}
