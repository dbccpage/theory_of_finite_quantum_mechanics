//! Raw finite idempotent-name inventories and splitting-equation diagnostics.
//! In an admitted category, Cauchy completeness means every idempotent splits.
//! Here the supplied tables and boundary/identity flags are caller premises;
//! no category admission, complete-inventory check or Karoubi construction occurs.
//! AuthorityEffect: None.

use crate::cat_functor::CompositionLookup;
use std::collections::BTreeMap;

// ---------------------------------------------------------------------------
// IdempotentSplitting
// ---------------------------------------------------------------------------

/// Declared names for an intended splitting; boundaries are not admitted here.
///
/// Laws:
///   r ∘ s = id_R   (retraction ∘ section = identity on retract)
///   s ∘ r = e      (section ∘ retraction = the idempotent)
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IdempotentSplitting {
    /// The original object carrying the idempotent.
    pub carrier: String,
    /// The idempotent morphism e : carrier → carrier.
    pub idempotent: String,
    /// The retract object R (may be a new, "virtual" object).
    pub retract: String,
    /// The section s : R → carrier.
    pub section: String,
    /// The retraction r : carrier → R.
    pub retraction: String,
}

// ---------------------------------------------------------------------------
// CauchyStatus
// ---------------------------------------------------------------------------

/// Outcome for the supplied nonidentity-flagged candidate inventory only.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CauchyStatus {
    /// Every retained candidate has a supplied pair satisfying both equations.
    Complete,
    /// Retained candidates without a matching supplied pair, in original order.
    Incomplete {
        /// Names of the unsplit idempotents.
        unsplit_idempotents: Vec<String>,
    },
}

// ---------------------------------------------------------------------------
// CauchyCompletion
// ---------------------------------------------------------------------------

/// Caller-assembled object/splitting metadata, without a category construction.
#[derive(Debug, Clone)]
pub struct CauchyCompletion {
    /// Objects of the original category.
    pub original_objects: Vec<String>,
    /// Objects added by the completion (one per unsplit idempotent).
    pub added_objects: Vec<String>,
    /// The splittings (one per idempotent that was split).
    pub splittings: Vec<IdempotentSplitting>,
}

// ---------------------------------------------------------------------------
// Detection: find idempotents and check if they split
// ---------------------------------------------------------------------------

/// Preserve ordered, repeated nonidentity-flagged entries with defined e;e=e.
/// Supplied object labels and identity flags are not checked against a category.
pub fn find_idempotents(
    endomorphisms: &[(&str, &str, bool)],
    compositions: &BTreeMap<(String, String), String>,
) -> Vec<(String, String)> {
    let view = CompositionLookup::new(compositions);
    find_idempotents_in(endomorphisms, &view)
}

fn find_idempotents_in(
    endomorphisms: &[(&str, &str, bool)],
    view: &CompositionLookup<'_>,
) -> Vec<(String, String)> {
    let mut idempotents = Vec::new();
    for &(mor, obj, is_id) in endomorphisms {
        if is_id {
            continue;
        }
        if view.compose(mor, mor) == Some(mor) {
            idempotents.push((mor.to_string(), obj.to_string()));
        }
    }
    idempotents
}

fn first_retraction<'a>(
    section: &str,
    retract: &str,
    idempotent: &str,
    from: impl Iterator<Item = (&'a str, &'a str)>,
    view: &CompositionLookup<'_>,
    identity_map: &BTreeMap<String, String>,
) -> Option<&'a str> {
    let identity = identity_map.get(retract)?;
    for (retraction, target) in from {
        if target != retract {
            continue;
        }
        if view.compose(section, retraction) == Some(identity.as_str())
            && view.compose(retraction, section) == Some(idempotent)
        {
            return Some(retraction);
        }
    }
    None
}

fn first_splitting<'a>(
    idempotent: &str,
    to: impl Iterator<Item = (&'a str, &'a str)>,
    from: impl Iterator<Item = (&'a str, &'a str)> + Clone,
    view: &CompositionLookup<'_>,
    identity_map: &BTreeMap<String, String>,
) -> Option<(&'a str, &'a str, &'a str)> {
    for (section, retract) in to {
        if let Some(retraction) = first_retraction(
            section, retract, idempotent, from.clone(), view, identity_map,
        ) {
            return Some((section, retract, retraction));
        }
    }
    None
}

/// First supplied pair with the same declared retract and both defined equations.
/// This search does not separately check e;e=e, actual boundaries or completeness.
pub fn check_idempotent_splits(
    idempotent: &str,
    carrier: &str,
    morphisms_to_carrier: &[(&str, &str)],
    morphisms_from_carrier: &[(&str, &str)],
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Option<IdempotentSplitting> {
    let view = CompositionLookup::new(compositions);
    first_splitting(idempotent, morphisms_to_carrier.iter().copied(),
        morphisms_from_carrier.iter().copied(), &view, identity_map)
        .map(|(section, retract, retraction)| IdempotentSplitting {
            carrier: carrier.to_string(), idempotent: idempotent.to_string(),
            retract: retract.to_string(), section: section.to_string(),
            retraction: retraction.to_string(),
        })
}

/// Report unsplit names in the supplied inventory, including order/duplicates.
/// Missing boundary inventories are empty; this is not full category admission.
pub fn check_cauchy_completeness(
    endomorphisms: &[(&str, &str, bool)],
    compositions: &BTreeMap<(String, String), String>,
    morphisms_to: &BTreeMap<String, Vec<(String, String)>>,
    morphisms_from: &BTreeMap<String, Vec<(String, String)>>,
    identity_map: &BTreeMap<String, String>,
) -> CauchyStatus {
    let view = CompositionLookup::new(compositions);
    let mut unsplit = Vec::new();
    for &(idem, carrier, is_id) in endomorphisms {
        if is_id || view.compose(idem, idem) != Some(idem) {
            continue;
        }
        let to = morphisms_to.get(carrier).into_iter()
            .flat_map(|rows| rows.iter().map(|(m, s)| (m.as_str(), s.as_str())));
        let from = morphisms_from.get(carrier).into_iter()
            .flat_map(|rows| rows.iter().map(|(m, t)| (m.as_str(), t.as_str())));
        if first_splitting(idem, to, from, &view, identity_map).is_none() {
            unsplit.push(idem.to_string());
        }
    }
    if unsplit.is_empty() { CauchyStatus::Complete }
    else { CauchyStatus::Incomplete { unsplit_idempotents: unsplit } }
}

// ---------------------------------------------------------------------------
// Validation: splitting law checker
// ---------------------------------------------------------------------------

// Individual observations preserve the original three diagnostic phases.
fn idempotence_diagnostic(splitting: &IdempotentSplitting, compositions: &BTreeMap<(String, String), String>) -> Option<String> {
    let key = (splitting.idempotent.clone(), splitting.idempotent.clone());
    match compositions.get(&key).map(String::as_str) {
        Some(v) if v == splitting.idempotent.as_str() => None,
        Some(v) => Some(format!("Not idempotent: {} ∘ {} = {} ≠ {}", splitting.idempotent, splitting.idempotent, v, splitting.idempotent)),
        None => Some(format!("Composition {} ∘ {} not defined", splitting.idempotent, splitting.idempotent)),
    }
}

fn retraction_diagnostic(
    splitting: &IdempotentSplitting,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Option<String> {
    let key = (splitting.section.clone(), splitting.retraction.clone());
    match (compositions.get(&key).map(String::as_str), identity_map.get(&splitting.retract)) {
        (Some(v), Some(id)) if v == id.as_str() => None,
        (Some(v), Some(id)) => Some(format!("Retraction law failed: r ∘ s = {} but id_R = {}", v, id)),
        _ => Some("Retraction law: composition r ∘ s or id_R not defined".into()),
    }
}

fn section_diagnostic(splitting: &IdempotentSplitting, compositions: &BTreeMap<(String, String), String>) -> Option<String> {
    let key = (splitting.retraction.clone(), splitting.section.clone());
    match compositions.get(&key).map(String::as_str) {
        Some(v) if v == splitting.idempotent.as_str() => None,
        Some(v) => Some(format!("Section law failed: s ∘ r = {} but e = {}", v, splitting.idempotent)),
        None => Some("Section law: composition s ∘ r not defined".into()),
    }
}

/// Check exactly three defined-name equalities, retaining all failures in order.
/// Carrier typing and category identity/composition laws are not checked.
pub fn validate_splitting(
    splitting: &IdempotentSplitting,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Vec<String> {
    [idempotence_diagnostic(splitting, compositions),
     retraction_diagnostic(splitting, compositions, identity_map),
     section_diagnostic(splitting, compositions)].into_iter().flatten().collect()
}

/// Records that three equalities passed at construction against borrowed tables.
/// Those tables are not retained; this is not an admitted-category certificate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedIdempotentSplitting(IdempotentSplitting);

impl ValidatedIdempotentSplitting {
    /// Check the three stated equalities and own the unchanged raw declaration.
    pub fn try_new(
        splitting: IdempotentSplitting,
        compositions: &BTreeMap<(String, String), String>,
        identity_map: &BTreeMap<String, String>,
    ) -> Result<Self, Vec<String>> {
        let violations = validate_splitting(&splitting, compositions, identity_map);
        if violations.is_empty() {
            Ok(Self(splitting))
        } else {
            Err(violations)
        }
    }

    /// Access the underlying declared splitting.
    pub fn declared(&self) -> &IdempotentSplitting {
        &self.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn discrete_category_is_cauchy_complete() {
        // No non-identity endomorphisms → trivially complete.
        let endomorphisms: Vec<(&str, &str, bool)> = vec![("id_A", "A", true), ("id_B", "B", true)];
        let compositions: BTreeMap<(String, String), String> = vec![
            (("id_A".into(), "id_A".into()), "id_A".into()),
            (("id_B".into(), "id_B".into()), "id_B".into()),
        ]
        .into_iter()
        .collect();

        let status = check_cauchy_completeness(
            &endomorphisms,
            &compositions,
            &BTreeMap::new(),
            &BTreeMap::new(),
            &vec![("A".into(), "id_A".into()), ("B".into(), "id_B".into())]
                .into_iter()
                .collect(),
        );
        assert_eq!(status, CauchyStatus::Complete);
    }

    #[test]
    fn unsplit_idempotent_detected() {
        // Category with object A and idempotent e: A → A, e∘e = e, e ≠ id_A.
        let endomorphisms: Vec<(&str, &str, bool)> = vec![("id_A", "A", true), ("e", "A", false)];
        let compositions: BTreeMap<(String, String), String> = vec![
            (("id_A".into(), "id_A".into()), "id_A".into()),
            (("e".into(), "e".into()), "e".into()),
            (("id_A".into(), "e".into()), "e".into()),
            (("e".into(), "id_A".into()), "e".into()),
        ]
        .into_iter()
        .collect();

        let status = check_cauchy_completeness(
            &endomorphisms,
            &compositions,
            &BTreeMap::new(),
            &BTreeMap::new(),
            &vec![("A".into(), "id_A".into())].into_iter().collect(),
        );
        assert_eq!(
            status,
            CauchyStatus::Incomplete {
                unsplit_idempotents: vec!["e".into()],
            }
        );
    }

    #[test]
    fn validate_correct_splitting() {
        // Objects A, R. Idempotent e: A → A. Section s: R → A, retraction r: A → R.
        let splitting = IdempotentSplitting {
            carrier: "A".into(),
            idempotent: "e".into(),
            retract: "R".into(),
            section: "s".into(),
            retraction: "r".into(),
        };

        let compositions: BTreeMap<(String, String), String> = vec![
            (("e".into(), "e".into()), "e".into()),    // e∘e = e
            (("s".into(), "r".into()), "id_R".into()), // r∘s = id_R
            (("r".into(), "s".into()), "e".into()),    // s∘r = e
        ]
        .into_iter()
        .collect();

        let identity_map: BTreeMap<String, String> =
            vec![("R".into(), "id_R".into()), ("A".into(), "id_A".into())]
                .into_iter()
                .collect();

        let violations = validate_splitting(&splitting, &compositions, &identity_map);
        assert!(
            violations.is_empty(),
            "Splitting should validate: {:?}",
            violations
        );
    }
}
