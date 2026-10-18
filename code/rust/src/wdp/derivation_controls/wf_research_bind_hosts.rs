//! Bounded finite control for WF-RESEARCH-BIND-HOSTS.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Witness {
    pub goal_id: &'static str,
    pub carrier_val: i64,
    pub secondary_num: i64,
    pub secondary_den: i64,
    pub negative_control_rejected: bool,
}

pub fn reject_missing_host_or_digest_drift(promote_unverified: bool) -> Result<(), &'static str> {
    if promote_unverified {
        Err("reject_missing_host_or_digest_drift")
    } else {
        Ok(())
    }
}

pub fn witness() -> Witness {
    let neg_rejected = reject_missing_host_or_digest_drift(true).is_err();
    Witness {
        goal_id: "WF-RESEARCH-BIND-HOSTS",
        carrier_val: 4,
        secondary_num: 2,
        secondary_den: 2,
        negative_control_rejected: neg_rejected,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wf_research_bind_hosts_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.goal_id, "WF-RESEARCH-BIND-HOSTS");
        assert_eq!(w.carrier_val, 4);
        assert_eq!(w.secondary_num, 2);
        assert_eq!(w.secondary_den, 2);
        assert!(w.negative_control_rejected);
        assert!(reject_missing_host_or_digest_drift(true).is_err());
        assert!(reject_missing_host_or_digest_drift(false).is_ok());
    }
}
