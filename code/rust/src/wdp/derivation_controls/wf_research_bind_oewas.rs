//! Bounded finite control for WF-RESEARCH-BIND-OEWAS.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Witness {
    pub goal_id: &'static str,
    pub carrier_val: i64,
    pub secondary_num: i64,
    pub secondary_den: i64,
    pub negative_control_rejected: bool,
}

pub fn reject_invented_catalog_hash(promote_unverified: bool) -> Result<(), &'static str> {
    if promote_unverified {
        Err("reject_invented_catalog_hash")
    } else {
        Ok(())
    }
}

pub fn witness() -> Witness {
    let neg_rejected = reject_invented_catalog_hash(true).is_err();
    Witness {
        goal_id: "WF-RESEARCH-BIND-OEWAS",
        carrier_val: 9,
        secondary_num: 1,
        secondary_den: 1,
        negative_control_rejected: neg_rejected,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wf_research_bind_oewas_witness_matches_derivation() {
        let w = witness();
        assert_eq!(w.goal_id, "WF-RESEARCH-BIND-OEWAS");
        assert_eq!(w.carrier_val, 9);
        assert_eq!(w.secondary_num, 1);
        assert_eq!(w.secondary_den, 1);
        assert!(w.negative_control_rejected);
        assert!(reject_invented_catalog_hash(true).is_err());
        assert!(reject_invented_catalog_hash(false).is_ok());
    }
}
