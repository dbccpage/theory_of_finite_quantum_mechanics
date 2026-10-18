//! campaign modules for the omega-native MUB lane.
#![allow(clippy::module_inception)]
#[path = "../mub6_balanced_table_replay.rs"]
pub mod mub6_balanced_table_replay;
#[path = "../mub6_dita_seed_cover.rs"]
pub mod mub6_dita_seed_cover;
#[path = "../mub6_f6_external_b3.rs"]
pub mod mub6_f6_external_b3;
#[path = "../mub6_prompt05_campaign_checks.rs"]
pub mod mub6_prompt05_campaign_checks;

/// Campaign state machine tracking for MUB(6) frontier resolution.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CampaignTracker {
    pub campaign_name: String,
    pub targets_total: usize,
    pub targets_passed: usize,
}

impl CampaignTracker {
    pub fn new(campaign_name: impl Into<String>, targets_total: usize) -> Self {
        Self {
            campaign_name: campaign_name.into(),
            targets_total,
            targets_passed: 0,
        }
    }

    pub fn record_target_pass(&mut self) -> Result<(), String> {
        if self.targets_passed >= self.targets_total {
            return Err("Cannot pass more targets than declared total".to_string());
        }
        self.targets_passed += 1;
        Ok(())
    }

    pub fn is_complete(&self) -> bool {
        self.targets_passed == self.targets_total && self.targets_total > 0
    }
}

#[cfg(test)]
mod campaign_tests {
    use super::*;

    #[test]
    fn test_campaign_tracker() {
        let mut ct = CampaignTracker::new("OptionB", 3);
        assert!(!ct.is_complete());
        ct.record_target_pass().unwrap();
        ct.record_target_pass().unwrap();
        ct.record_target_pass().unwrap();
        assert!(ct.is_complete());
        assert!(ct.record_target_pass().is_err());
    }
}
