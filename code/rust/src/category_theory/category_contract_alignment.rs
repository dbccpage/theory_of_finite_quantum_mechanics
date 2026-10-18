//! Category theory contract alignment module.
//!
//! Maps Rust category-theoretic structures (categories, functors, natural transformations,
//! adjunctions, monads, operads, limits, colimits, coends) to canonical `urn:omega:math:*` contract URNs.

pub const CONTRACT_CATEGORY: &str = "urn:omega:math:category:v0.1.0";
pub const CONTRACT_FUNCTOR: &str = "urn:omega:math:functor:v0.1.0";
pub const CONTRACT_NATURAL_TRANSFORMATION: &str = "urn:omega:math:natural_transformation:v0.1.0";
pub const CONTRACT_ADJUNCTION: &str = "urn:omega:math:adjunction:v0.1.0";
pub const CONTRACT_MONAD: &str = "urn:omega:math:monad:v0.1.0";
pub const CONTRACT_OPERAD: &str = "urn:omega:math:operad:v0.1.0";
pub const CONTRACT_LIMIT: &str = "urn:omega:math:limit:v0.1.0";
pub const CONTRACT_COLIMIT: &str = "urn:omega:math:colimit:v0.1.0";
pub const CONTRACT_COEND: &str = "urn:omega:math:coend:v0.1.0";
pub const CONTRACT_END: &str = "urn:omega:math:end:v0.1.0";

/// Record mapping a Rust category-theoretic type/trait to a contract URN.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CategoryContractBinding {
    pub concept_name: String,
    pub contract_urn: String,
    pub mechanization_stratum: String,
    pub is_active: bool,
}

impl CategoryContractBinding {
    pub fn default_category_bindings() -> Vec<Self> {
        vec![
            Self {
                concept_name: "Category".to_string(),
                contract_urn: CONTRACT_CATEGORY.to_string(),
                mechanization_stratum: "M0".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Functor".to_string(),
                contract_urn: CONTRACT_FUNCTOR.to_string(),
                mechanization_stratum: "M0".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "NaturalTransformation".to_string(),
                contract_urn: CONTRACT_NATURAL_TRANSFORMATION.to_string(),
                mechanization_stratum: "M0".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Adjunction".to_string(),
                contract_urn: CONTRACT_ADJUNCTION.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Monad".to_string(),
                contract_urn: CONTRACT_MONAD.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Operad".to_string(),
                contract_urn: CONTRACT_OPERAD.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Limit".to_string(),
                contract_urn: CONTRACT_LIMIT.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Colimit".to_string(),
                contract_urn: CONTRACT_COLIMIT.to_string(),
                mechanization_stratum: "M1".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "Coend".to_string(),
                contract_urn: CONTRACT_COEND.to_string(),
                mechanization_stratum: "M2".to_string(),
                is_active: true,
            },
            Self {
                concept_name: "End".to_string(),
                contract_urn: CONTRACT_END.to_string(),
                mechanization_stratum: "M2".to_string(),
                is_active: true,
            },
        ]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_category_bindings_valid() {
        let bindings = CategoryContractBinding::default_category_bindings();
        assert_eq!(bindings.len(), 10);
        for b in &bindings {
            assert!(b.contract_urn.starts_with("urn:omega:math:"));
            assert!(b.is_active);
        }
    }
}
