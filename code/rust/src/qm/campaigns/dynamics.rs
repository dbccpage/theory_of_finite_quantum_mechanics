//! Program Stone interface pricing. AuthorityEffect: None.
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct StoneCostingReport {
    pub gap_id: String,
    pub disposition: String,
    pub continuous_time_imported: bool,
    pub strong_continuity_imported: bool,
    pub infinite_branch_ambiguity: bool,
}

/// Returns the formal pricing report for Stone's theorem (GAP-F001-S000-008).
pub fn price_stone_theorem_interface() -> StoneCostingReport {
    StoneCostingReport {
        gap_id: "GAP-F001-S000-008".to_string(),
        disposition: "PRICED_CONTINUUM_INTERFACE".to_string(),
        continuous_time_imported: true,
        strong_continuity_imported: true,
        infinite_branch_ambiguity: true,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_stone_interface_costing() {
        let rep = price_stone_theorem_interface();
        assert_eq!(rep.gap_id, "GAP-F001-S000-008");
        assert_eq!(rep.disposition, "PRICED_CONTINUUM_INTERFACE");
        assert!(rep.continuous_time_imported);
        assert!(rep.strong_continuity_imported);
        assert!(rep.infinite_branch_ambiguity);
    }
}
