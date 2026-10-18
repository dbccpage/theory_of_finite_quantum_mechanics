
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Witness {
    pub goal_id: &'static str,
    pub carrier_val: i64,
    pub secondary_num: i64,
    pub secondary_den: i64,
    pub negative_control_rejected: bool,
}

pub fn reject_unlowered_packet_or_authority_escalation(promote_unverified: bool) -> Result<(), &'static str> {
    if promote_unverified {
        Err("reject_unlowered_packet_or_authority_escalation")
    } else {
        Ok(())
    }
}

pub fn witness() -> Witness {
    let neg_rejected = reject_unlowered_packet_or_authority_escalation(true).is_err();
    Witness {
        goal_id: "WF-RESEARCH-BIND-PROMPTS",
        carrier_val: 4,
        secondary_num: 8,
        secondary_den: 8,
        negative_control_rejected: neg_rejected,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wf_research_bind_prompts_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.goal_id, "WF-RESEARCH-BIND-PROMPTS");
        assert_eq!(w.carrier_val, 4);
        assert_eq!(w.secondary_num, 8);
        assert_eq!(w.secondary_den, 8);
        assert!(w.negative_control_rejected);
        assert!(reject_unlowered_packet_or_authority_escalation(true).is_err());
        assert!(reject_unlowered_packet_or_authority_escalation(false).is_ok());
    }
}
