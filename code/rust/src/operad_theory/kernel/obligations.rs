
use std::collections::BTreeSet;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};

use super::canonical::{
    canonical_bytes, canonical_id, require_digest, require_identifier, require_text, sorted_unique,
    CanonicalError,
};
use super::model::AuthorityEffect;
use super::result::KernelError;
use super::terms::NormalizedTerm;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ObligationKind {
    #[serde(rename = "Associativity")]
    Associativity,
    #[serde(rename = "Unit")]
    Unit,
    #[serde(rename = "Parallelism")]
    Parallelism,
    #[serde(rename = "Comparison")]
    Comparison,
    #[serde(rename = "Refinement")]
    Refinement,
    #[serde(rename = "Coherence")]
    Coherence,
}

impl ObligationKind {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Associativity => "Associativity",
            Self::Unit => "Unit",
            Self::Parallelism => "Parallelism",
            Self::Comparison => "Comparison",
            Self::Refinement => "Refinement",
            Self::Coherence => "Coherence",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProofObligation {
    pub obligation_id: String,
    pub kind: ObligationKind,
    pub statement: String,
    pub subject_refs: Vec<String>,
    pub premise_digests: Vec<String>,
}

impl ProofObligation {
    pub fn new(
        obligation_id: &str,
        kind: ObligationKind,
        statement: &str,
        subject_refs: Vec<String>,
        premise_digests: Vec<String>,
    ) -> Result<Self, KernelError> {
        let valid_refs = subject_refs
            .into_iter()
            .map(|r| require_digest(&r, "subject_ref"))
            .collect::<Result<Vec<_>, _>>()?;
        let refs = sorted_unique(&valid_refs, "subject_refs")?;
        let valid_premises = premise_digests
            .into_iter()
            .map(|p| require_digest(&p, "premise_digest"))
            .collect::<Result<Vec<_>, _>>()?;
        let premises = sorted_unique(&valid_premises, "premise_digests")?;

        Ok(Self {
            obligation_id: require_identifier(obligation_id, "obligation_id")?,
            kind,
            statement: require_text(statement, "statement")?,
            subject_refs: refs,
            premise_digests: premises,
        })
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "obligation_id": self.obligation_id,
            "kind": self.kind.as_str(),
            "statement": self.statement,
            "subject_refs": self.subject_refs,
            "premise_digests": self.premise_digests,
            "status": "Open",
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObligationBundle {
    pub bundle_id: String,
    pub kernel_version: String,
    pub generated_from: Vec<String>,
    pub obligations: Vec<ProofObligation>,
    pub authority_effect: AuthorityEffect,
}

impl ObligationBundle {
    pub fn new(
        bundle_id: &str,
        kernel_version: &str,
        generated_from: Vec<String>,
        mut obligations: Vec<ProofObligation>,
        authority_effect: AuthorityEffect,
    ) -> Result<Self, KernelError> {
        if authority_effect != AuthorityEffect::None {
            return Err(KernelError::Message(
                "obligation bundles carry AuthorityEffect None".into(),
            ));
        }

        let valid_roots = generated_from
            .into_iter()
            .map(|r| require_digest(&r, "generated_from"))
            .collect::<Result<Vec<_>, _>>()?;
        let roots = sorted_unique(&valid_roots, "generated_from")?;

        let mut seen = BTreeSet::new();
        for ob in &obligations {
            if !seen.insert(ob.obligation_id.clone()) {
                return Err(KernelError::Message(
                    "obligation IDs must be unique".into(),
                ));
            }
        }
        obligations.sort_by(|a, b| a.obligation_id.cmp(&b.obligation_id));

        Ok(Self {
            bundle_id: require_identifier(bundle_id, "bundle_id")?,
            kernel_version: require_identifier(kernel_version, "kernel_version")?,
            generated_from: roots,
            obligations,
            authority_effect,
        })
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "bundle_id": self.bundle_id,
            "kernel_version": self.kernel_version,
            "generated_from": self.generated_from,
            "obligations": self.obligations.iter().map(ProofObligation::to_canonical).collect::<Vec<_>>(),
            "authority_effect": self.authority_effect.as_str(),
        })
    }

    pub fn canonical_id(&self) -> Result<String, CanonicalError> {
        canonical_id("omega.oewas.obligation-bundle.v1", &self.to_canonical())
    }

    pub fn export_bytes(&self) -> Result<Vec<u8>, CanonicalError> {
        canonical_bytes("omega.oewas.obligation-bundle.export.v1", &self.to_canonical())
    }

    pub fn export_json(&self) -> Result<String, KernelError> {
        let bytes = self.export_bytes()?;
        let val: Value = serde_json::from_slice(&bytes)
            .map_err(|e| KernelError::Message(e.to_string()))?;
        serde_json::to_string(&val).map_err(|e| KernelError::Message(e.to_string()))
    }
}

pub fn export_lean_obligations(
    presentation: &[NormalizedTerm],
    bound: usize,
) -> Result<ObligationBundle, KernelError> {
    if presentation.is_empty() {
        return Err(KernelError::Message(
            "presentation must be non-empty".into(),
        ));
    }
    if bound < 2 {
        return Err(KernelError::Message(
            "obligation bound must be at least two".into(),
        ));
    }

    let mut roots_set = BTreeSet::new();
    for term in presentation {
        roots_set.insert(term.canonical_id()?);
    }
    let roots: Vec<String> = roots_set.into_iter().collect();

    let mut obligations = Vec::new();
    for (index, root) in roots.iter().enumerate() {
        obligations.push(ProofObligation::new(
            &format!("unit-{index}"),
            ObligationKind::Unit,
            "Prove left and right unit normalization for this finite term root.",
            vec![root.clone()],
            Vec::new(),
        )?);
        obligations.push(ProofObligation::new(
            &format!("associativity-{index}"),
            ObligationKind::Associativity,
            "Prove all well-typed nested substitutions reachable from this term root.",
            vec![root.clone()],
            Vec::new(),
        )?);
    }

    for dimension in 3..=bound {
        obligations.push(ProofObligation::new(
            &format!("coherence-dimension-{dimension}"),
            ObligationKind::Coherence,
            &format!("Check all generated tree-boundary coherence obligations through dimension {dimension}."),
            roots.clone(),
            Vec::new(),
        )?);
    }

    ObligationBundle::new(
        &format!("finite-presentation-through-{bound}"),
        "oewas-higher-operad-v1",
        roots,
        obligations,
        AuthorityEffect::None,
    )
}
