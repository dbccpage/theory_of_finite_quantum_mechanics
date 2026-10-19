//! Raw inventories for a proposed HoTT model. AuthorityEffect: None.
//! validate_minimal_model checks only that two inventories are nonempty.
//! Their contents, the model name and truncation inventory remain unchecked.
//! Empty diagnostics do not certify a model or interpretation.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ToposHottModel {
    pub name: String,
    pub universes: Vec<String>,
    pub identity_type_interpretations: Vec<String>,
    pub truncation_modalities: Vec<String>,
}

impl ToposHottModel {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.into(),
            universes: Vec::new(),
            identity_type_interpretations: Vec::new(),
            truncation_modalities: Vec::new(),
        }
    }

    pub fn validate_minimal_model(&self) -> Vec<String> {
        let mut violations = Vec::new();
        if self.universes.is_empty() {
            violations.push(format!(
                "Model {} has no universe interpretation",
                self.name
            ));
        }
        if self.identity_type_interpretations.is_empty() {
            violations.push(format!(
                "Model {} has no identity type interpretation",
                self.name
            ));
        }
        violations
    }
}
