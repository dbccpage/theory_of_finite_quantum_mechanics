//! Declared fullness obligations and candidate lifts, at label level only.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A full functor is surjective on each Hom_C(a,b) -> Hom_D(Fa,Fb).
//! This record checks coverage of a supplied obligation list, not whether that
//! list enumerates every required target arrow for every source-object pair.
//! Categories, arrow membership, identities and composition are not checked.

use super::functor::Functor;
use crate::errors::ArithmosError;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

fn invalid(message: impl Into<String>) -> ArithmosError {
    ArithmosError::InvalidShape(message.into())
}

/// An arrow label with declared endpoints; its enclosing field determines C or D.
/// Labels are opaque, compared verbatim, and never normalized.
#[derive(Debug, Clone, Default, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct LabeledMorphism {
    pub source_object: String,
    pub target_object: String,
    pub morphism: String,
}

impl LabeledMorphism {
    pub fn new(
        source_object: impl Into<String>,
        target_object: impl Into<String>,
        morphism: impl Into<String>,
    ) -> Self {
        Self {
            source_object: source_object.into(),
            target_object: target_object.into(),
            morphism: morphism.into(),
        }
    }

    fn has_blank_field(&self) -> bool {
        self.source_object.trim().is_empty()
            || self.target_object.trim().is_empty()
            || self.morphism.trim().is_empty()
    }
}

/// A declared source arrow and its claimed target image, not a certified lift.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FullnessWitness {
    pub preimage: LabeledMorphism,
    pub image: LabeledMorphism,
}

impl FullnessWitness {
    pub fn new(preimage: LabeledMorphism, image: LabeledMorphism) -> Self {
        Self { preimage, image }
    }
}

/// A mutable, possibly vacuous declaration of supplied fullness obligations.
///
/// Default is an invalid placeholder. Equality compares stored list order.
/// Old serialized records omit obligations/witnesses and become vacuous records.
/// Deserialize is unchecked; validated() checks only the current record.
/// Successful validation is neither a lawful-functor nor a fullness certificate.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FullFunctor {
    pub label: String,
    pub functor_ref: String,
    #[serde(default)]
    pub obligations: Vec<LabeledMorphism>,
    #[serde(default)]
    pub witnesses: Vec<FullnessWitness>,
    /// Unrestricted prose, preserved without normalization.
    pub notes: Vec<String>,
}

impl FullFunctor {
    /// An unchecked candidate whose functor reference is still unset.
    pub fn new(label: impl Into<String>) -> Self {
        Self::on_functor(label, "")
    }

    /// An unchecked, vacuous declaration; no obligations are inferred.
    pub fn on_functor(label: impl Into<String>, functor_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            functor_ref: functor_ref.into(),
            obligations: Vec::new(),
            witnesses: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_obligations(mut self, obligations: Vec<LabeledMorphism>) -> Self {
        self.obligations = obligations;
        self
    }

    pub fn with_obligation(mut self, obligation: LabeledMorphism) -> Self {
        self.obligations.push(obligation);
        self
    }

    pub fn with_witnesses(mut self, witnesses: Vec<FullnessWitness>) -> Self {
        self.witnesses = witnesses;
        self
    }

    pub fn with_witness(mut self, witness: FullnessWitness) -> Self {
        self.witnesses.push(witness);
        self
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Whether no obligations were supplied. Dangling witnesses can still fail.
    pub fn is_vacuous(&self) -> bool {
        self.obligations.is_empty()
    }

    /// Check nonblank fields, unique obligations, arrow typing, witness
    /// functionality, dangling witnesses and coverage of supplied obligations.
    /// First failures follow names, obligations, witnesses, then coverage.
    /// Identical repeated witnesses are permitted and add no evidence.
    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.trim().is_empty() {
            return Err(invalid("empty label"));
        }
        if self.functor_ref.trim().is_empty() {
            return Err(invalid("empty functor_ref"));
        }
        let obligations = self.obligation_index()?;
        let covered = self.covered_by_witnesses(&obligations)?;
        for ob in &self.obligations {
            if !covered.contains(ob) {
                return Err(invalid(format!(
                    "obligation {} : {} -> {} has no witness",
                    ob.morphism, ob.source_object, ob.target_object
                )));
            }
        }
        Ok(())
    }

    fn obligation_index(&self) -> Result<BTreeSet<&LabeledMorphism>, ArithmosError> {
        let mut obligations = BTreeSet::new();
        let mut endpoints = BTreeMap::new();
        for (i, ob) in self.obligations.iter().enumerate() {
            if ob.has_blank_field() {
                return Err(invalid(format!("blank obligation at index {i}")));
            }
            if !obligations.insert(ob) {
                return Err(invalid(format!(
                    "duplicate obligation {} at index {i}",
                    ob.morphism
                )));
            }
            check_endpoints(&mut endpoints, ob, "target")?;
        }
        Ok(obligations)
    }

    fn covered_by_witnesses<'a>(
        &'a self,
        obligations: &BTreeSet<&LabeledMorphism>,
    ) -> Result<BTreeSet<&'a LabeledMorphism>, ArithmosError> {
        let mut covered = BTreeSet::new();
        let mut endpoints = BTreeMap::new();
        let mut images = BTreeMap::new();
        for (i, w) in self.witnesses.iter().enumerate() {
            if w.preimage.has_blank_field() {
                return Err(invalid(format!("blank witness preimage at index {i}")));
            }
            if w.image.has_blank_field() {
                return Err(invalid(format!("blank witness image at index {i}")));
            }
            if !obligations.contains(&w.image) {
                return Err(invalid(format!(
                    "witness {i} has image {} which is not among the obligations",
                    w.image.morphism
                )));
            }
            check_endpoints(&mut endpoints, &w.preimage, "source")?;
            if let Some(previous) = images.insert(w.preimage.morphism.as_str(), &w.image) {
                if previous != &w.image {
                    return Err(invalid(format!(
                        "source morphism {} is claimed to map to both {} and {}",
                        w.preimage.morphism, previous.morphism, w.image.morphism
                    )));
                }
            }
            covered.insert(&w.image);
        }
        Ok(covered)
    }

    /// Consume a raw candidate, checking internal consistency at this call.
    /// The returned record retains public mutable fields and is not a certificate.
    pub fn validated(self) -> Result<Self, ArithmosError> {
        self.validate_shell()?;
        Ok(self)
    }

    /// Recorded obligations with no exact declared witness image, in list order.
    /// This diagnostic does not validate either list.
    pub fn unwitnessed_obligations(&self) -> Vec<&LabeledMorphism> {
        let images: BTreeSet<_> = self.witnesses.iter().map(|w| &w.image).collect();
        self.obligations
            .iter()
            .filter(|ob| !images.contains(ob))
            .collect()
    }

    /// Distinct declared preimages grouped by exact target arrow.
    ///
    /// Repeated identical witnesses count once; output is sorted by complete
    /// endpoint/arrow tuples. A collision across different source Hom-sets
    /// does not refute faithfulness. This diagnostic does not validate inputs.
    pub fn multiply_preimages(&self) -> Vec<(&LabeledMorphism, Vec<&LabeledMorphism>)> {
        let mut groups: BTreeMap<_, BTreeSet<_>> = BTreeMap::new();
        for w in &self.witnesses {
            groups.entry(&w.image).or_default().insert(&w.preimage);
        }
        groups
            .into_iter()
            .filter(|(_, preimages)| preimages.len() > 1)
            .map(|(image, preimages)| (image, preimages.into_iter().collect()))
            .collect()
    }

    /// Check against the supplied raw maps, rejecting blanks and duplicate keys.
    ///
    /// Every witness must agree with both endpoint images and its arrow image.
    /// Empty maps are empty: they cannot support a populated claim. Since every
    /// obligation has a witness, successful checks cover all supplied obligations.
    /// A target arrow missing from the image is a failed lift, not an excuse to
    /// remove an obligation. No completeness, category-law or Hom-set claim follows.
    /// This maps-only API cannot bind functor_ref; use validate_against_functor
    /// to check the referenced shell's label as well.
    pub fn validate_against_maps(
        &self,
        object_map: &[(String, String)],
        morphism_map: &[(String, String)],
    ) -> Result<(), ArithmosError> {
        self.validate_shell()?;
        let objects = map_index(object_map, "object_map")?;
        let morphisms = map_index(morphism_map, "morphism_map")?;
        for (i, w) in self.witnesses.iter().enumerate() {
            check_image(
                &objects,
                &w.preimage.source_object,
                &w.image.source_object,
                i,
                "source object",
            )?;
            check_image(
                &objects,
                &w.preimage.target_object,
                &w.image.target_object,
                i,
                "target object",
            )?;
            check_image(
                &morphisms,
                &w.preimage.morphism,
                &w.image.morphism,
                i,
                "morphism",
            )?;
        }
        Ok(())
    }

    /// Also bind functor_ref to the supplied shell's exact label.
    /// This still checks recorded maps, not a lawful functor or actual fullness.
    pub fn validate_against_functor(&self, functor: &Functor) -> Result<(), ArithmosError> {
        self.validate_shell()?;
        functor.validate_shell()?;
        if self.functor_ref != functor.label {
            return Err(invalid(
                "functor_ref does not match the supplied functor label",
            ));
        }
        self.validate_against_maps(&functor.object_map, &functor.morphism_map)
    }
}

fn check_endpoints<'a>(
    known: &mut BTreeMap<&'a str, (&'a str, &'a str)>,
    arrow: &'a LabeledMorphism,
    side: &str,
) -> Result<(), ArithmosError> {
    let pair = (arrow.source_object.as_str(), arrow.target_object.as_str());
    if let Some(previous) = known.insert(arrow.morphism.as_str(), pair) {
        if previous != pair {
            return Err(invalid(format!(
                "{side} morphism {} is used with inconsistent endpoints",
                arrow.morphism
            )));
        }
    }
    Ok(())
}

fn map_index<'a>(
    pairs: &'a [(String, String)],
    kind: &str,
) -> Result<BTreeMap<&'a str, &'a str>, ArithmosError> {
    let mut index = BTreeMap::new();
    for (i, (source, target)) in pairs.iter().enumerate() {
        if source.trim().is_empty() || target.trim().is_empty() {
            return Err(invalid(format!("blank {kind} tag at index {i}")));
        }
        if index.insert(source.as_str(), target.as_str()).is_some() {
            return Err(invalid(format!(
                "duplicate {kind} source {source:?} at index {i}"
            )));
        }
    }
    Ok(index)
}

fn check_image(
    map: &BTreeMap<&str, &str>,
    source: &str,
    expected: &str,
    index: usize,
    role: &str,
) -> Result<(), ArithmosError> {
    let actual = map.get(source).copied().ok_or_else(|| {
        invalid(format!(
            "witness {index}: {role} {source:?} is not in the recorded map"
        ))
    })?;
    if actual != expected {
        return Err(invalid(format!(
            "witness {index}: {role} {source:?} maps to {actual:?}, not {expected:?}"
        )));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn lm(a: &str, b: &str, f: &str) -> LabeledMorphism {
        LabeledMorphism::new(a, b, f)
    }

    fn witness() -> FullnessWitness {
        FullnessWitness::new(lm("a", "b", "f"), lm("Fa", "Fb", "g"))
    }

    fn populated() -> FullFunctor {
        FullFunctor::on_functor("full", "F")
            .with_obligation(witness().image)
            .with_witness(witness())
    }

    fn maps() -> Functor {
        Functor::between("F", "C", "D")
            .with_object_map(vec![("a".into(), "Fa".into()), ("b".into(), "Fb".into())])
            .with_morphism_map(vec![("f".into(), "g".into())])
    }

    fn assert_invalid(f: &FullFunctor, message: &str) {
        assert_eq!(f.validate_shell(), Err(invalid(message)));
    }

    #[test]
    fn empty_claim_is_valid_but_explicitly_vacuous() {
        let f = FullFunctor::on_functor("full", "F");
        assert!(f.is_vacuous());
        assert!(f.validate_shell().is_ok());
        assert!(!populated().is_vacuous());
    }

    #[test]
    fn labels_are_checked_independently() {
        for blank in ["", " \t", "\u{2003}"] {
            assert_invalid(&FullFunctor::on_functor(blank, "F"), "empty label");
            assert_invalid(&FullFunctor::on_functor("full", blank), "empty functor_ref");
        }
    }

    #[test]
    fn default_and_new_are_uninitialized_candidates() {
        assert_invalid(&FullFunctor::default(), "empty label");
        assert_invalid(&FullFunctor::new("full"), "empty functor_ref");
    }

    #[test]
    fn populated_owned_validation_preserves_record_and_notes() {
        let f = populated().with_note("").with_note("diagnostic");
        assert_eq!(f.clone().validated(), Ok(f));
    }

    #[test]
    fn all_obligation_fields_reject_blanks() {
        for blank in ["", " \t", "\u{2003}"] {
            for ob in [
                lm(blank, "Fb", "g"),
                lm("Fa", blank, "g"),
                lm("Fa", "Fb", blank),
            ] {
                assert_invalid(
                    &FullFunctor::on_functor("full", "F").with_obligation(ob),
                    "blank obligation at index 0",
                );
            }
        }
    }

    #[test]
    fn identical_obligations_are_rejected() {
        assert_invalid(
            &populated().with_obligation(witness().image),
            "duplicate obligation g at index 1",
        );
    }

    #[test]
    fn target_arrow_labels_have_consistent_endpoints() {
        assert_invalid(
            &populated().with_obligation(lm("Other", "Fb", "g")),
            "target morphism g is used with inconsistent endpoints",
        );
    }

    #[test]
    fn all_preimage_fields_reject_blanks() {
        for blank in ["", " \t", "\u{2003}"] {
            for preimage in [
                lm(blank, "b", "f"),
                lm("a", blank, "f"),
                lm("a", "b", blank),
            ] {
                let f = FullFunctor::on_functor("full", "F")
                    .with_obligation(witness().image)
                    .with_witness(FullnessWitness::new(preimage, witness().image));
                assert_invalid(&f, "blank witness preimage at index 0");
            }
        }
    }

    #[test]
    fn all_image_fields_reject_blanks_before_membership() {
        for blank in ["", " \t", "\u{2003}"] {
            for image in [
                lm(blank, "Fb", "g"),
                lm("Fa", blank, "g"),
                lm("Fa", "Fb", blank),
            ] {
                let f = FullFunctor::on_functor("full", "F")
                    .with_obligation(witness().image)
                    .with_witness(FullnessWitness::new(witness().preimage, image));
                assert_invalid(&f, "blank witness image at index 0");
            }
        }
    }

    #[test]
    fn dangling_images_are_rejected_including_wrong_endpoints() {
        for image in [lm("Fa", "Fb", "h"), lm("Other", "Fb", "g")] {
            let expected = format!(
                "witness 1 has image {} which is not among the obligations",
                image.morphism
            );
            assert_invalid(
                &populated().with_witness(FullnessWitness::new(lm("a", "b", "u"), image)),
                &expected,
            );
        }
    }

    #[test]
    fn witnesses_on_an_empty_claim_are_dangling() {
        let f = FullFunctor::on_functor("full", "F").with_witness(witness());
        assert!(f.is_vacuous());
        assert_invalid(
            &f,
            "witness 0 has image g which is not among the obligations",
        );
    }

    #[test]
    fn source_arrow_labels_have_consistent_endpoints() {
        let w = FullnessWitness::new(lm("Other", "b", "f"), witness().image);
        assert_invalid(
            &populated().with_witness(w),
            "source morphism f is used with inconsistent endpoints",
        );
    }

    #[test]
    fn one_source_arrow_cannot_claim_two_images() {
        let image = lm("Fa", "Fb", "h");
        let f = populated()
            .with_obligation(image.clone())
            .with_witness(FullnessWitness::new(witness().preimage, image));
        assert_invalid(&f, "source morphism f is claimed to map to both g and h");
    }

    #[test]
    fn every_declared_obligation_needs_a_witness() {
        let f = populated().with_obligation(lm("Fa", "Fb", "h"));
        assert_invalid(&f, "obligation h : Fa -> Fb has no witness");
        assert_eq!(f.unwitnessed_obligations(), vec![&f.obligations[1]]);
        assert!(f.clone().validated().is_err());
    }

    #[test]
    fn repeated_identical_witnesses_are_not_distinct_preimages() {
        let f = populated().with_witness(witness());
        assert!(f.validate_shell().is_ok());
        assert!(f.multiply_preimages().is_empty());
    }

    #[test]
    fn distinct_preimages_are_reported_in_deterministic_order() {
        let f = populated()
            .with_witness(FullnessWitness::new(lm("a", "b", "u"), witness().image))
            .with_witness(witness());
        assert!(f.validate_shell().is_ok());
        let groups = f.multiply_preimages();
        assert_eq!(groups.len(), 1);
        assert_eq!(groups[0].0, &f.obligations[0]);
        assert_eq!(
            groups[0].1,
            vec![&f.witnesses[0].preimage, &f.witnesses[1].preimage]
        );
        let mut reversed = f.clone();
        reversed.witnesses.reverse();
        assert_eq!(groups, reversed.multiply_preimages());
    }

    #[test]
    fn diagnostics_match_complete_arrow_tuples_without_validation() {
        let f = FullFunctor::on_functor("full", "F")
            .with_obligation(witness().image)
            .with_witness(FullnessWitness::new(
                witness().preimage,
                lm("Other", "Fb", "g"),
            ));
        assert_eq!(f.unwitnessed_obligations(), vec![&f.obligations[0]]);
    }

    #[test]
    fn maps_and_bound_functor_accept_matching_declarations() {
        let m = maps();
        assert!(populated()
            .validate_against_maps(&m.object_map, &m.morphism_map)
            .is_ok());
        assert!(populated().validate_against_functor(&m).is_ok());
    }

    #[test]
    fn bound_functor_refuses_wrong_label_even_with_matching_maps() {
        let mut m = maps();
        m.label = "Other".into();
        assert_eq!(
            populated().validate_against_functor(&m),
            Err(invalid(
                "functor_ref does not match the supplied functor label"
            ))
        );
    }

    #[test]
    fn each_witness_map_entry_must_be_present() {
        for (missing, role, tag) in [(0, "source object", "a"), (1, "target object", "b")] {
            let mut m = maps();
            m.object_map.remove(missing);
            assert_eq!(
                populated().validate_against_maps(&m.object_map, &m.morphism_map),
                Err(invalid(format!(
                    "witness 0: {role} {tag:?} is not in the recorded map"
                )))
            );
        }
        assert_eq!(
            populated().validate_against_maps(&maps().object_map, &[]),
            Err(invalid(
                "witness 0: morphism \"f\" is not in the recorded map"
            ))
        );
    }

    #[test]
    fn each_witness_map_value_must_agree() {
        for (field, role, tag, expected) in [
            (0, "source object", "a", "Fa"),
            (1, "target object", "b", "Fb"),
        ] {
            let mut m = maps();
            m.object_map[field].1 = "Wrong".into();
            assert_eq!(
                populated().validate_against_maps(&m.object_map, &m.morphism_map),
                Err(invalid(format!(
                    "witness 0: {role} {tag:?} maps to \"Wrong\", not {expected:?}"
                )))
            );
        }
        let m = maps().with_morphism_map(vec![("f".into(), "Wrong".into())]);
        assert_eq!(
            populated().validate_against_maps(&m.object_map, &m.morphism_map),
            Err(invalid(
                "witness 0: morphism \"f\" maps to \"Wrong\", not \"g\""
            ))
        );
    }

    #[test]
    fn empty_maps_are_not_unspecified_maps() {
        assert!(populated().validate_against_maps(&[], &[]).is_err());
        assert!(FullFunctor::on_functor("full", "F")
            .validate_against_maps(&[], &[])
            .is_ok());
    }

    #[test]
    fn malformed_maps_are_rejected_even_for_a_vacuous_claim() {
        let f = FullFunctor::on_functor("full", "F");
        for kind in ["object_map", "morphism_map"] {
            for (pairs, message) in [
                (
                    vec![("a".into(), "x".into()), ("a".into(), "y".into())],
                    format!("duplicate {kind} source \"a\" at index 1"),
                ),
                (
                    vec![("a".into(), "x".into()), ("a".into(), "x".into())],
                    format!("duplicate {kind} source \"a\" at index 1"),
                ),
                (
                    vec![(" \t".into(), "x".into())],
                    format!("blank {kind} tag at index 0"),
                ),
                (
                    vec![("a".into(), "\u{2003}".into())],
                    format!("blank {kind} tag at index 0"),
                ),
            ] {
                let result = if kind == "object_map" {
                    f.validate_against_maps(&pairs, &[])
                } else {
                    f.validate_against_maps(&[], &pairs)
                };
                assert_eq!(result, Err(invalid(message)));
            }
        }
    }

    #[test]
    fn shell_failure_is_not_hidden_by_map_validation() {
        let f = FullFunctor::on_functor("", "F");
        assert_eq!(
            f.validate_against_maps(&[], &[]),
            Err(invalid("empty label"))
        );
    }

    #[test]
    fn populated_record_does_not_establish_actual_fullness_or_nonfaithfulness() {
        use crate::cat_functor::{DeclaredFiniteFunctor, ValidatedFiniteFunctor};
        use crate::finite_category::{DeclaredFiniteCategory, ValidatedFiniteCategory};
        let mut c = DeclaredFiniteCategory::new("C");
        for (object, id) in [("a", "ia"), ("b", "ib")] {
            c.add_identity(object, id);
            c.set_composition(id, id, id);
        }
        let mut d = DeclaredFiniteCategory::new("D");
        d.add_identity("X", "e");
        d.set_composition("e", "e", "e");
        let mut declaration = DeclaredFiniteFunctor::new("F", "C", "D");
        for (a, b) in [("a", "X"), ("b", "X")] {
            declaration.map_object(a, b);
        }
        for (f, g) in [("ia", "e"), ("ib", "e")] {
            declaration.map_morphism(f, g);
        }
        let lawful = ValidatedFiniteFunctor::try_new(
            declaration,
            ValidatedFiniteCategory::try_new(c).unwrap(),
            ValidatedFiniteCategory::try_new(d).unwrap(),
        )
        .unwrap();
        let image = lm("X", "X", "e");
        let claim = FullFunctor::on_functor("partial", "F")
            .with_obligation(image.clone())
            .with_witness(FullnessWitness::new(lm("a", "a", "ia"), image.clone()))
            .with_witness(FullnessWitness::new(lm("b", "b", "ib"), image));
        let m = Functor::between("F", "C", "D")
            .with_object_map(vec![("a".into(), "X".into()), ("b".into(), "X".into())])
            .with_morphism_map(vec![("ia".into(), "e".into()), ("ib".into(), "e".into())]);
        assert!(claim.validate_against_functor(&m).is_ok());
        assert_eq!(claim.multiply_preimages()[0].1.len(), 2);
        let source = lawful.source().declared();
        let mut missing_pairs = 0;
        for a in &source.objects {
            for b in &source.objects {
                let arrows: Vec<_> = source
                    .morphisms
                    .values()
                    .filter(|f| &f.source == a && &f.target == b)
                    .collect();
                let images: BTreeSet<_> = arrows
                    .iter()
                    .map(|f| lawful.on_morphism(&f.name).unwrap())
                    .collect();
                assert_eq!(arrows.len(), images.len()); // injective on each source Hom-set
                if arrows.is_empty() {
                    assert_eq!(lawful.on_object(a), Some("X"));
                    assert_eq!(lawful.on_object(b), Some("X"));
                    assert_eq!(
                        lawful.target().declared().boundary_of("e"),
                        Some(("X", "X"))
                    );
                    missing_pairs += 1;
                }
            }
        }
        assert_eq!(missing_pairs, 2); // no lift of e in Hom_C(a,b) or Hom_C(b,a)
    }
}
