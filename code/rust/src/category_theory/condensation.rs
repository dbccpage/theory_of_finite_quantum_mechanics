//! Condensation — Spec Section 21.
//!
//! In ∞-categories, idempotents are replaced by condensations:
//! homotopy-coherent idempotent splittings.
//!
//! A condensation is data X →r Y →s X together with:
//!   r ∘ s ≃ id_Y
//!   s ∘ r ⇒ e (coherently associative homotopy)
//!   higher coherence data at each level
//!
//! An (∞,1)-category C is ∞-Cauchy complete iff every condensation splits.
//! Equivalently: every fully dualizable profunctor 1 ⊸ C is representable.

use std::collections::BTreeMap;

// ---------------------------------------------------------------------------
// CoherenceWitness
// ---------------------------------------------------------------------------

/// A witness for one level of homotopy coherence in a condensation.
///
/// Level 0: the splitting data (r, s) itself.
/// Level 1: the homotopy s ∘ r ⇒ e.
/// Level 2: the coherence between the homotopy and composition.
/// Level n: n-th order coherence cell.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CoherenceWitness {
    /// The coherence level (0 = base data, 1 = first homotopy, ...).
    pub level: usize,
    /// Human-readable description of what this witness asserts.
    pub description: String,
    /// Whether this witness has been verified.
    pub verified: bool,
}

impl CoherenceWitness {
    pub fn new(level: usize, description: &str) -> Self {
        Self {
            level,
            description: description.into(),
            verified: false,
        }
    }

    pub fn verified(level: usize, description: &str) -> Self {
        Self {
            level,
            description: description.into(),
            verified: true,
        }
    }
}

// ---------------------------------------------------------------------------
// Condensation
// ---------------------------------------------------------------------------

/// A condensation: homotopy-coherent idempotent splitting.
///
/// In the finite approximation used here, a condensation is represented
/// by the splitting triple (r, s, carrier) plus coherence witnesses
/// at each verified level.
///
/// The 1-categorical shadow of this is an `IdempotentSplitting` (see cauchy.rs).
/// A condensation adds higher coherence data.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Condensation {
    /// The carrier object X (where the idempotent lives).
    pub carrier: String,
    /// The retract object Y (the "image" of the condensation).
    pub retract: String,
    /// The section s : Y → X.
    pub section: String,
    /// The retraction r : X → Y.
    pub retraction: String,
    /// How many levels of homotopy coherence have been recorded.
    pub coherence_level: usize,
    /// Coherence witnesses at each level.
    pub witnesses: Vec<CoherenceWitness>,
}

impl Condensation {
    /// Create a condensation with base splitting data (level 0).
    pub fn new(carrier: &str, retract: &str, section: &str, retraction: &str) -> Self {
        Self {
            carrier: carrier.into(),
            retract: retract.into(),
            section: section.into(),
            retraction: retraction.into(),
            coherence_level: 0,
            witnesses: vec![CoherenceWitness::new(0, "base splitting data: r, s, X, Y")],
        }
    }

    /// Add a coherence witness at the next level.
    pub fn add_witness(&mut self, description: &str, verified: bool) {
        let level = self.coherence_level + 1;
        self.witnesses.push(CoherenceWitness {
            level,
            description: description.into(),
            verified,
        });
        self.coherence_level = level;
    }

    /// The maximum verified coherence level.
    pub fn max_verified_level(&self) -> usize {
        self.witnesses
            .iter()
            .filter(|w| w.verified)
            .map(|w| w.level)
            .max()
            .unwrap_or(0)
    }

    /// Whether all declared witnesses are verified.
    pub fn fully_verified(&self) -> bool {
        self.witnesses.iter().all(|w| w.verified)
    }
}

// ---------------------------------------------------------------------------
// InfinityCauchyStatus
// ---------------------------------------------------------------------------

/// Diagnostic: is the ∞-category Cauchy complete?
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InfinityCauchyStatus {
    /// All condensations split. No phantom objects in Prof∞.
    Complete,
    /// Some condensations do not split.
    Incomplete { unsplit_condensations: Vec<String> },
    /// Cannot determine: insufficient coherence data or infinite structure.
    Unknown { reason: String },
}

// ---------------------------------------------------------------------------
// Condensation detection and checking
// ---------------------------------------------------------------------------

/// Check whether a condensation satisfies its base splitting laws.
///
/// Level 0 laws (same as idempotent splitting):
///   r ∘ s = id_Y
///   s ∘ r = e (some endomorphism of X)
///
/// Level 1 law:
///   e ∘ e ≃ e (idempotent, up to homotopy witness)
pub fn validate_condensation(
    cond: &Condensation,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();

    // Level 0: r ∘ s = id_Y
    let rs_key = (cond.section.clone(), cond.retraction.clone());
    let id_y = identity_map.get(&cond.retract);
    match (compositions.get(&rs_key), id_y) {
        (Some(v), Some(id)) if v == id => {}
        (Some(v), Some(id)) => {
            violations.push(format!(
                "Condensation level 0: r ∘ s = {} but id_Y = {}",
                v, id
            ));
        }
        _ => {
            violations.push("Condensation level 0: r ∘ s or id_Y not defined".into());
        }
    }

    // Level 0: s ∘ r produces some endomorphism e of X
    let sr_key = (cond.retraction.clone(), cond.section.clone());
    let e = compositions.get(&sr_key);
    match e {
        Some(e_mor) => {
            // Level 1: e ∘ e = e (idempotent)
            let ee_key = (e_mor.clone(), e_mor.clone());
            match compositions.get(&ee_key) {
                Some(ee) if ee == e_mor => {}
                Some(ee) => {
                    violations.push(format!(
                        "Condensation level 1: e ∘ e = {} but e = {} (not idempotent)",
                        ee, e_mor
                    ));
                }
                None => {
                    violations.push(format!(
                        "Condensation level 1: e ∘ e not defined for e = {}",
                        e_mor
                    ));
                }
            }
        }
        None => {
            violations.push("Condensation level 0: s ∘ r not defined".into());
        }
    }

    // Check coherence witnesses
    for w in &cond.witnesses {
        if w.level > 0 && !w.verified {
            violations.push(format!(
                "Condensation level {}: witness '{}' not verified",
                w.level, w.description
            ));
        }
    }

    violations
}

/// Check ∞-Cauchy completeness for a finite approximation.
///
/// Takes a list of condensations and checks whether all split.
pub fn check_infinity_cauchy(
    condensations: &[Condensation],
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> InfinityCauchyStatus {
    let mut unsplit = Vec::new();

    for cond in condensations {
        let violations = validate_condensation(cond, compositions, identity_map);
        if !violations.is_empty() {
            unsplit.push(format!(
                "{} → {} ({})",
                cond.carrier,
                cond.retract,
                violations.join("; ")
            ));
        }
    }

    if unsplit.is_empty() {
        InfinityCauchyStatus::Complete
    } else {
        InfinityCauchyStatus::Incomplete {
            unsplit_condensations: unsplit,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn condensation_base_construction() {
        let cond = Condensation::new("X", "Y", "s", "r");
        assert_eq!(cond.coherence_level, 0);
        assert_eq!(cond.witnesses.len(), 1);
        assert_eq!(cond.max_verified_level(), 0);
    }

    #[test]
    fn condensation_with_witnesses() {
        let mut cond = Condensation::new("X", "Y", "s", "r");
        cond.witnesses[0].verified = true; // verify level 0
        cond.add_witness("s ∘ r ⇒ e homotopy", true);
        cond.add_witness("coherence of e-homotopy with composition", false);

        assert_eq!(cond.coherence_level, 2);
        assert_eq!(cond.max_verified_level(), 1);
        assert!(!cond.fully_verified());
    }

    #[test]
    fn valid_condensation() {
        let mut cond = Condensation::new("X", "Y", "s", "r");
        cond.witnesses[0].verified = true;

        let compositions: BTreeMap<(String, String), String> = vec![
            (("s".into(), "r".into()), "id_Y".into()), // r∘s = id_Y
            (("r".into(), "s".into()), "e".into()),    // s∘r = e
            (("e".into(), "e".into()), "e".into()),    // e∘e = e
        ]
        .into_iter()
        .collect();

        let identity_map: BTreeMap<String, String> =
            vec![("Y".into(), "id_Y".into()), ("X".into(), "id_X".into())]
                .into_iter()
                .collect();

        let violations = validate_condensation(&cond, &compositions, &identity_map);
        assert!(violations.is_empty(), "Should validate: {:?}", violations);
    }

    #[test]
    fn infinity_cauchy_complete() {
        let mut cond = Condensation::new("X", "Y", "s", "r");
        cond.witnesses[0].verified = true;

        let compositions: BTreeMap<(String, String), String> = vec![
            (("s".into(), "r".into()), "id_Y".into()),
            (("r".into(), "s".into()), "e".into()),
            (("e".into(), "e".into()), "e".into()),
        ]
        .into_iter()
        .collect();

        let identity_map: BTreeMap<String, String> =
            vec![("Y".into(), "id_Y".into())].into_iter().collect();

        let status = check_infinity_cauchy(&[cond], &compositions, &identity_map);
        assert_eq!(status, InfinityCauchyStatus::Complete);
    }
}
