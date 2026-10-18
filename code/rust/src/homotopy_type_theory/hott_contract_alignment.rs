//! Contract alignment module for Homotopy Type Theory.
//!
//! Provides formal mapping and verification between Rust HoTT record types
//! and canonical `urn:omega:math:*` contract URNs.

use serde::{Deserialize, Serialize};

/// Canonical URNs for HoTT math contracts.
pub const CONTRACT_IDENTITY_TYPE: &str = "urn:omega:math:identity_type:v0.1.0";
pub const CONTRACT_PI_TYPE: &str = "urn:omega:math:pi_type:v0.1.0";
pub const CONTRACT_SIGMA_TYPE: &str = "urn:omega:math:sigma_type:v0.1.0";
pub const CONTRACT_TRUNCATION_LEVEL: &str = "urn:omega:math:truncation_level:v0.1.0";
pub const CONTRACT_UNIVALENCE_WITNESS: &str = "urn:omega:math:univalence_witness:v0.1.0";
pub const CONTRACT_HIGHER_INDUCTIVE_TYPE: &str = "urn:omega:math:higher_inductive_type:v0.1.0";

/// Record mapping a Rust HoTT concept to a contract URN.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HottContractBinding {
    pub hott_concept: String,
    pub contract_urn: String,
    pub mechanization_stratum: String,
    pub is_active: bool,
}

impl HottContractBinding {
    pub fn default_coda_bindings() -> Vec<Self> {
        vec![
            Self {
                hott_concept: "IdentityType".to_string(),
                contract_urn: CONTRACT_IDENTITY_TYPE.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                hott_concept: "PiType".to_string(),
                contract_urn: CONTRACT_PI_TYPE.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                hott_concept: "SigmaType".to_string(),
                contract_urn: CONTRACT_SIGMA_TYPE.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                hott_concept: "TruncationLevel".to_string(),
                contract_urn: CONTRACT_TRUNCATION_LEVEL.to_string(),
                mechanization_stratum: "M0".to_string(),
                is_active: true,
            },
            Self {
                hott_concept: "UnivalenceWitness".to_string(),
                contract_urn: CONTRACT_UNIVALENCE_WITNESS.to_string(),
                mechanization_stratum: "M2".to_string(),
                is_active: true,
            },
            Self {
                hott_concept: "HigherInductiveType".to_string(),
                contract_urn: CONTRACT_HIGHER_INDUCTIVE_TYPE.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
        ]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_default_bindings_valid() {
        let bindings = HottContractBinding::default_coda_bindings();
        assert_eq!(bindings.len(), 6);
        for b in &bindings {
            assert!(b.contract_urn.starts_with("urn:omega:math:"));
            assert!(b.is_active);
        }
    }
}
