//! Bridge HoTT judgments into finite topos-style semantics.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HottJudgmentInterpretation {
    pub judgment: String,
    pub context_object: String,
    pub semantic_object: String,
    pub evidence: Vec<String>,
}

impl HottJudgmentInterpretation {
    pub fn new(judgment: &str, context_object: &str, semantic_object: &str) -> Self {
        Self {
            judgment: judgment.into(),
            context_object: context_object.into(),
            semantic_object: semantic_object.into(),
            evidence: Vec::new(),
        }
    }

    pub fn add_evidence(&mut self, evidence: &str) {
        self.evidence.push(evidence.into());
    }

    pub fn validate(&self) -> Vec<String> {
        let mut violations = Vec::new();
        if self.judgment.trim().is_empty() {
            violations.push("HoTT judgment is empty".into());
        }
        if self.context_object.trim().is_empty() {
            violations.push("Context object is empty".into());
        }
        if self.semantic_object.trim().is_empty() {
            violations.push("Semantic object is empty".into());
        }
        violations
    }
}
