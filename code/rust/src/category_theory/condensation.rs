//! Raw named splitting-equation observations and caller-supplied coherence flags.
//! No higher cells,homotopies or infinity-category laws are checked. Historical
//! InfinityCauchyStatus::Complete means only no supplied record emitted a diagnostic;
//! it does not certify mathematical infinity-Cauchy completeness. AuthorityEffect: None.

use std::collections::BTreeMap;
use super::cat_functor::CompositionLookup;

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
    /// Caller-supplied flag;the constructor/checker does not verify its description.
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

/// Raw names,declared level counter and descriptive caller flags.
/// Names are not admitted category arrows;witness descriptions carry no checked cells.
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

/// Typed refusal of a next-level update before any metadata mutation.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CoherenceLevelOverflow;

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

    /// Append one descriptive flag at checked next level;overflow leaves self unchanged.
    /// No truth of the description or previous witness inventory is admitted.
    pub fn add_witness(&mut self, description: &str, verified: bool) -> Result<(), CoherenceLevelOverflow> {
        let level = self.coherence_level.checked_add(1).ok_or(CoherenceLevelOverflow)?;
        self.witnesses.push(CoherenceWitness {
            level,
            description: description.into(),
            verified,
        });
        self.coherence_level = level;
        Ok(())
    }

    /// Largest level among caller-flagged rows;0 also represents no flagged row.
    pub fn max_verified_level(&self) -> usize {
        self.witnesses
            .iter()
            .filter(|w| w.verified)
            .map(|w| w.level)
            .max()
            .unwrap_or(0)
    }

    /// Whether every supplied flag is true,vacuously true on an empty list.
    pub fn fully_verified(&self) -> bool {
        self.witnesses.iter().all(|w| w.verified)
    }
}

// ---------------------------------------------------------------------------
// InfinityCauchyStatus
// ---------------------------------------------------------------------------

/// Legacy names for the result of a finite supplied-record diagnostic inventory.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InfinityCauchyStatus {
    /// No supplied record emitted a diagnostic;empty inventory also returns this.
    Complete,
    /// Supplied records emitted diagnostics,in input order.
    Incomplete { unsplit_condensations: Vec<String> },
    /// Raw compatibility variant;this inventory function does not produce it.
    Unknown { reason: String },
}

// ---------------------------------------------------------------------------
// Condensation detection and checking
// ---------------------------------------------------------------------------

fn retraction_diagnostic(cond: &Condensation, table: &CompositionLookup<'_>, identities: &BTreeMap<String, String>) -> Option<String> {
    match (table.compose(&cond.section, &cond.retraction), identities.get(&cond.retract).map(String::as_str)) {
        (Some(v), Some(id)) if v == id => None,
        (Some(v), Some(id)) => Some(format!("Condensation level 0: r ∘ s = {} but id_Y = {}", v, id)),
        _ => Some("Condensation level 0: r ∘ s or id_Y not defined".into()),
    }
}

fn idempotence_diagnostic(cond: &Condensation, table: &CompositionLookup<'_>) -> Option<String> {
    let Some(e) = table.compose(&cond.retraction, &cond.section) else {
        return Some("Condensation level 0: s ∘ r not defined".into());
    };
    match table.compose(e, e) {
        Some(ee) if ee == e => None,
        Some(ee) => Some(format!("Condensation level 1: e ∘ e = {} but e = {} (not idempotent)", ee, e)),
        None => Some(format!("Condensation level 1: e ∘ e not defined for e = {}", e)),
    }
}

fn validate_with_lookup(cond: &Condensation, table: &CompositionLookup<'_>, identity_map: &BTreeMap<String, String>) -> Vec<String> {
    let mut violations: Vec<String> = [retraction_diagnostic(cond, table, identity_map), idempotence_diagnostic(cond, table)].into_iter().flatten().collect();
    for w in &cond.witnesses {
        if w.level > 0 && !w.verified {
            violations.push(format!("Condensation level {}: witness '{}' not verified", w.level, w.description));
        }
    }
    violations
}

/// Observe two defined-only named splitting/idempotence checks,then positive-level
/// false flags. Base flags and level continuity are not tested;no category typing.
pub fn validate_condensation(
    cond: &Condensation,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Vec<String> {
    let table = CompositionLookup::new(compositions);
    validate_with_lookup(cond, &table, identity_map)
}

/// Ordered diagnostic inventory over supplied raw records;empty means Complete.
/// Neither inventory completeness nor actual infinity-category splitting is checked.
pub fn check_infinity_cauchy(
    condensations: &[Condensation],
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> InfinityCauchyStatus {
    let mut unsplit = Vec::new();
    let table = CompositionLookup::new(compositions);

    for cond in condensations {
        let violations = validate_with_lookup(cond, &table, identity_map);
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
        cond.add_witness("s ∘ r ⇒ e homotopy", true).expect("small level");
        cond.add_witness("coherence of e-homotopy with composition", false).expect("small level");

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
