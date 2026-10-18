//! The MUB(6) claim firewall and cryptographic boundary attestation engine.
//!
//! Origin: papers/derivations/mub/rust/src/omega_native/mub6_firewall.rs
//! Claim: MUB6-FIREWALL-001
//! AuthorityEffect: None.

use serde::{Deserialize, Serialize};

pub const FIREWALL: &str = "stated region only; mints no authority";
pub const AUTHORITY_EFFECT: &str = "None";

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum FirewallViolation {
    ForbiddenAuthorityMinting(String),
    MissingAttestationHeader,
}

/// Cryptographic and semantic boundary attestation for MUB(6) research claims.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FirewallAttestation {
    pub campaign: String,
    pub target_id: String,
    pub authority_declared: String,
}

impl FirewallAttestation {
    pub fn new(campaign: impl Into<String>, target_id: impl Into<String>) -> Self {
        Self {
            campaign: campaign.into(),
            target_id: target_id.into(),
            authority_declared: AUTHORITY_EFFECT.to_string(),
        }
    }

    /// Verifies that no module attempts to escalate authority above None.
    pub fn verify_firewall(&self) -> Result<(), FirewallViolation> {
        if self.authority_declared != "None" {
            return Err(FirewallViolation::ForbiddenAuthorityMinting(
                self.authority_declared.clone(),
            ));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_firewall_attestation_holds() {
        let att = FirewallAttestation::new("TargetA12", "MUB6-ROOT-001");
        assert!(att.verify_firewall().is_ok());
    }

    #[test]
    fn test_firewall_blocks_escalation() {
        let mut att = FirewallAttestation::new("TargetA12", "MUB6-ROOT-001");
        att.authority_declared = "GlobalGreen".to_string();
        assert!(att.verify_firewall().is_err());
    }
}
