//! CatFunctor, ContravariantFunctor, and DeclaredFiniteFunctor.
//!
//! Spec references: Sections 1A, 1B, 1D, 3, 4.
//!
//! Laws (CatFunctor):
//!   F(id_A) = id_{F(A)}
//!   F(g ∘ f) = F(g) ∘ F(f)
//!   source(F(f)) = F(source(f))
//!   target(F(f)) = F(target(f))
//!
//! Laws (ContravariantFunctor):
//!   F(id_A) = id_{F(A)}
//!   F(g ∘ f) = F(f) ∘ F(g)   ← reversed
//!
//! Generic traits express caller obligations without checking laws. Only the
//! immutable finite certificate constructor checks actual admitted endpoints.
//! Legacy free diagnostic functions inspect supplied names/cases; in particular,
//! check_identity_law assumes the literal id_ naming convention, not arbitrary
//! identity labels. Empty supplied diagnostic domains pass vacuously.

use super::finite_category::ValidatedFiniteCategory;
use std::collections::BTreeMap;

/// Finite functor admission failures. Declarations and certificates are distinct.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FunctorAdmissionError {
    Name,
    CategoryBinding,
    MappingDomain { kind: &'static str },
    UnknownImage { kind: &'static str, image: String },
    Boundary { morphism: String },
    Identity { object: String },
    Composition { first: String, second: String },
}

/// A functor certificate owns immutable admitted endpoints and its total maps.
/// The checker verifies both boundaries, identities, and every source composite.
/// AuthorityEffect: None. Finite runtime verification, not a formal proof build.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteFunctor {
    declared: DeclaredFiniteFunctor,
    source: ValidatedFiniteCategory,
    target: ValidatedFiniteCategory,
}

impl ValidatedFiniteFunctor {
    pub fn try_new(
        declared: DeclaredFiniteFunctor,
        source: ValidatedFiniteCategory,
        target: ValidatedFiniteCategory,
    ) -> Result<Self, FunctorAdmissionError> {
        let candidate = Self {
            declared,
            source,
            target,
        };
        candidate.check_binding()?;
        candidate.check_maps()?;
        candidate.check_boundaries()?;
        candidate.check_identities()?;
        candidate.check_compositions()?;
        Ok(candidate)
    }

    pub fn declared(&self) -> &DeclaredFiniteFunctor {
        &self.declared
    }
    pub fn source(&self) -> &ValidatedFiniteCategory {
        &self.source
    }
    pub fn target(&self) -> &ValidatedFiniteCategory {
        &self.target
    }
    pub fn on_object(&self, object: &str) -> Option<&str> {
        self.declared.on_object(object)
    }
    pub fn on_morphism(&self, morphism: &str) -> Option<&str> {
        self.declared.on_morphism(morphism)
    }

    fn check_binding(&self) -> Result<(), FunctorAdmissionError> {
        if self.declared.name.trim().is_empty() {
            return Err(FunctorAdmissionError::Name);
        }
        if self.declared.source_category != self.source.declared().name
            || self.declared.target_category != self.target.declared().name
        {
            return Err(FunctorAdmissionError::CategoryBinding);
        }
        Ok(())
    }

    fn check_maps(&self) -> Result<(), FunctorAdmissionError> {
        let source = self.source.declared();
        let target = self.target.declared();
        if !self.declared.object_map.keys().eq(source.objects.iter()) {
            return Err(FunctorAdmissionError::MappingDomain { kind: "objects" });
        }
        if !self
            .declared
            .morphism_map
            .keys()
            .eq(source.morphisms.keys())
        {
            return Err(FunctorAdmissionError::MappingDomain { kind: "morphisms" });
        }
        check_images(
            &self.declared.object_map,
            |x| target.has_object(x),
            "objects",
        )?;
        check_images(
            &self.declared.morphism_map,
            |x| target.has_morphism(x),
            "morphisms",
        )
    }

    fn check_boundaries(&self) -> Result<(), FunctorAdmissionError> {
        for (name, morphism) in &self.source.declared().morphisms {
            let image = self
                .on_morphism(name)
                .and_then(|n| self.target.declared().boundary_of(n));
            let expected = self
                .on_object(&morphism.source)
                .zip(self.on_object(&morphism.target));
            if image.is_none() || image != expected {
                return Err(FunctorAdmissionError::Boundary {
                    morphism: name.clone(),
                });
            }
        }
        Ok(())
    }

    fn check_identities(&self) -> Result<(), FunctorAdmissionError> {
        for (object, identity) in &self.source.declared().identities {
            let expected = self
                .on_object(object)
                .and_then(|n| self.target.declared().identity_of(n));
            if self.on_morphism(identity) != expected || expected.is_none() {
                return Err(FunctorAdmissionError::Identity {
                    object: object.clone(),
                });
            }
        }
        Ok(())
    }

    fn check_compositions(&self) -> Result<(), FunctorAdmissionError> {
        let lookup = CompositionLookup::new(&self.target.declared().compositions);
        for ((first, second), result) in &self.source.declared().compositions {
            let pair = self.on_morphism(first).zip(self.on_morphism(second));
            let expected = pair.and_then(|(f, g)| lookup.compose(f, g));
            if self.on_morphism(result) != expected || expected.is_none() {
                return Err(FunctorAdmissionError::Composition {
                    first: first.clone(),
                    second: second.clone(),
                });
            }
        }
        Ok(())
    }
}

fn check_images(
    map: &BTreeMap<String, String>,
    contains: impl Fn(&str) -> bool,
    kind: &'static str,
) -> Result<(), FunctorAdmissionError> {
    for image in map.values() {
        if !contains(image) {
            return Err(FunctorAdmissionError::UnknownImage {
                kind,
                image: image.clone(),
            });
        }
    }
    Ok(())
}

/// Composition table convention:
/// compositions[(f, g)] = g ∘ f
pub type CompositionTable = BTreeMap<(String, String), String>;

/// Shared sorted borrowed view for repeated table queries in admission phases.
/// O(C) references once; O(log(C+1)) key comparisons per query, including string
/// comparison costs. Returned values borrow the immutable original table.
pub(crate) struct CompositionLookup<'a> {
    rows: Vec<((&'a str, &'a str), &'a str)>,
}

impl<'a> CompositionLookup<'a> {
    pub(crate) fn new(table: &'a CompositionTable) -> Self {
        Self {
            rows: table.iter().map(|((first, second), composite)| {
                ((first.as_str(), second.as_str()), composite.as_str())
            }).collect(),
        }
    }

    pub(crate) fn compose(&self, first: &str, second: &str) -> Option<&'a str> {
        let index = self.rows.binary_search_by_key(&(first, second), |(key, _)| *key).ok()?;
        self.rows.get(index).map(|(_, composite)| *composite)
    }
}
// ---------------------------------------------------------------------------
// Trait: CatFunctor (covariant)
// ---------------------------------------------------------------------------

/// A covariant functor F : C → D between categories.
///
/// Implementations are required to preserve identity and composition; this
/// signature alone does not check those laws or callback purity/termination.
pub trait CatFunctor {
    type Source: Category;
    type Target: Category;

    fn map_object(&self, object: &<Self::Source as Category>::Ob)
        -> <Self::Target as Category>::Ob;

    fn map_morphism(
        &self,
        morphism: &<Self::Source as Category>::Mor,
    ) -> <Self::Target as Category>::Mor;
}

// ---------------------------------------------------------------------------
// Trait: ContravariantFunctor
// ---------------------------------------------------------------------------

/// A contravariant functor F : C^op → D.
///
/// Maps f: A → B to F(f): F(B) → F(A).
/// Composition is reversed: F(g ∘ f) = F(f) ∘ F(g).
pub trait ContravariantFunctor {
    type Source: Category;
    type Target: Category;

    fn map_object(&self, object: &<Self::Source as Category>::Ob)
        -> <Self::Target as Category>::Ob;

    /// Maps f: A → B to F(f): F(B) → F(A).
    fn map_morphism(
        &self,
        morphism: &<Self::Source as Category>::Mor,
    ) -> <Self::Target as Category>::Mor;
}

// ---------------------------------------------------------------------------
// Data: DeclaredFiniteFunctor (kernel-auditable record)
// ---------------------------------------------------------------------------

/// An explicit, finite functor declaration for kernel audit.
///
/// This is data, not behavior. Missing mappings are violations (spec §3).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteFunctor {
    pub name: String,
    pub source_category: String,
    pub target_category: String,
    pub object_map: BTreeMap<String, String>,
    pub morphism_map: BTreeMap<String, String>,
}

impl DeclaredFiniteFunctor {
    pub fn new(name: &str, source: &str, target: &str) -> Self {
        Self {
            name: name.into(),
            source_category: source.into(),
            target_category: target.into(),
            object_map: BTreeMap::new(),
            morphism_map: BTreeMap::new(),
        }
    }

    pub fn map_object(&mut self, src: &str, tgt: &str) {
        self.object_map.insert(src.into(), tgt.into());
    }

    pub fn map_morphism(&mut self, src: &str, tgt: &str) {
        self.morphism_map.insert(src.into(), tgt.into());
    }

    pub fn on_object(&self, obj: &str) -> Option<&str> {
        self.object_map.get(obj).map(|s| s.as_str())
    }

    pub fn on_morphism(&self, mor: &str) -> Option<&str> {
        self.morphism_map.get(mor).map(|s| s.as_str())
    }
}

// ---------------------------------------------------------------------------
// Local root Category interface used by finite-certificate implementations.
// Other catalog/legacy Category traits are distinct nominal Rust interfaces.
// ---------------------------------------------------------------------------

/// Caller contract for objects, morphisms and partial identifier lookups.
/// The trait itself does not admit laws; ValidatedFiniteCategory supplies a
/// separately checked finite implementation of this particular Rust interface.
pub trait Category {
    type Ob: Clone + Eq + std::fmt::Debug;
    type Mor: Clone + Eq + std::fmt::Debug;

    /// Unknown identifiers are outside the category, even if the category itself
    /// has been validated. Public lookups therefore return an admission result.
    fn id(&self, x: &Self::Ob) -> Option<Self::Mor>;
    fn src(&self, f: &Self::Mor) -> Option<Self::Ob>;
    fn tgt(&self, f: &Self::Mor) -> Option<Self::Ob>;
    fn compose(&self, f: &Self::Mor, g: &Self::Mor) -> Option<Self::Mor>;
}

// ---------------------------------------------------------------------------
// Validation: finite functor law checkers (spec §3, §4)
// ---------------------------------------------------------------------------

/// Check the literal id_ name rule on all supplied object mappings.
/// This is a legacy naming diagnostic, not arbitrary-category law admission.
///
/// Missing identity mappings produce violations, not silent skips (spec §3).
pub fn check_identity_law(functor: &DeclaredFiniteFunctor) -> Vec<String> {
    let mut violations = Vec::new();
    for (src_obj, tgt_obj) in &functor.object_map {
        let src_id = format!("id_{}", src_obj);
        let Some(mapped) = functor.morphism_map.get(&src_id) else {
            violations.push(format!("Identity law: F(id_{}) is not defined", src_obj));
            continue;
        };
        let expected_tgt_id = format!("id_{}", tgt_obj);
        if mapped != &expected_tgt_id {
            violations.push(format!(
                "Identity law violated at {}: F(id_{}) = {} but expected {}",
                src_obj, src_obj, mapped, expected_tgt_id
            ));
        }
    }
    violations
}

/// Check composition law: F(g∘f) = F(g) ∘ F(f).
///
/// Missing morphism mappings produce violations, not silent skips (spec §3).
pub fn check_composition_law(
    functor: &DeclaredFiniteFunctor,
    source_compositions: &[(&str, &str, &str)], // (f, g, g∘f) in source
    target_compositions: &CompositionTable,     // (f, g) → g∘f in target
) -> Vec<String> {
    let mut violations = Vec::new();
    let lookup = CompositionLookup::new(target_compositions);
    for &(f, g, gf) in source_compositions {
        let Some(f_img) = functor.on_morphism(f) else {
            violations.push(format!("Composition law: F({}) is not defined", f));
            continue;
        };
        let Some(g_img) = functor.on_morphism(g) else {
            violations.push(format!("Composition law: F({}) is not defined", g));
            continue;
        };
        let Some(gf_img) = functor.on_morphism(gf) else {
            violations.push(format!("Composition law: F({}) is not defined", gf));
            continue;
        };

        match lookup.compose(f_img, g_img) {
            Some(composed) if composed == gf_img => {}
            Some(composed) => {
                violations.push(format!(
                    "Composition law violated: F({}∘{}) = {} but F({})∘F({}) = {}",
                    g, f, gf_img, g, f, composed
                ));
            }
            None => {
                violations.push(format!(
                    "Composition law: F({})∘F({}) = {}∘{} not in target composition table",
                    g, f, g_img, f_img
                ));
            }
        }
    }
    violations
}

/// Check object totality: every object in the declared source set is mapped.
pub fn check_object_totality(
    functor: &DeclaredFiniteFunctor,
    source_objects: &[&str],
) -> Vec<String> {
    let mut violations = Vec::new();
    for &obj in source_objects {
        if functor.on_object(obj).is_none() {
            violations.push(format!(
                "Object totality: {} is not mapped by functor {}",
                obj, functor.name
            ));
        }
    }
    violations
}

/// Check morphism totality: every morphism in the declared source set is mapped.
pub fn check_morphism_totality(
    functor: &DeclaredFiniteFunctor,
    source_morphisms: &[&str],
) -> Vec<String> {
    let mut violations = Vec::new();
    for &mor in source_morphisms {
        if functor.on_morphism(mor).is_none() {
            violations.push(format!(
                "Morphism totality: {} is not mapped by functor {}",
                mor, functor.name
            ));
        }
    }
    violations
}

/// Check boundary preservation: source(F(f)) = F(source(f)) and target(F(f)) = F(target(f)).
pub fn check_boundary_preservation(
    functor: &DeclaredFiniteFunctor,
    source_boundaries: &[(&str, &str, &str)], // (morphism, source_obj, target_obj) in source cat
    target_boundaries: &BTreeMap<String, (String, String)>, // F(f) -> (src, tgt)
) -> Vec<String> {
    let mut violations = Vec::new();

    for &(mor, src_obj, tgt_obj) in source_boundaries {
        let Some(f_img) = functor.on_morphism(mor) else {
            violations.push(format!("Boundary preservation: F({}) is not defined", mor));
            continue;
        };

        let Some(src_img) = functor.on_object(src_obj) else {
            violations.push(format!(
                "Boundary preservation: F({}) is not defined",
                src_obj
            ));
            continue;
        };

        let Some(tgt_img) = functor.on_object(tgt_obj) else {
            violations.push(format!(
                "Boundary preservation: F({}) is not defined",
                tgt_obj
            ));
            continue;
        };

        let Some((actual_src, actual_tgt)) = target_boundaries.get(f_img) else {
            violations.push(format!(
                "Boundary preservation: target boundary for F({}) = {} is not defined",
                mor, f_img
            ));
            continue;
        };

        if actual_src != src_img {
            violations.push(format!(
                "Boundary preservation violated for {}: src(F({})) = {}, expected F(src({})) = {}",
                mor, mor, actual_src, mor, src_img
            ));
        }

        if actual_tgt != tgt_img {
            violations.push(format!(
                "Boundary preservation violated for {}: tgt(F({})) = {}, expected F(tgt({})) = {}",
                mor, mor, actual_tgt, mor, tgt_img
            ));
        }
    }

    violations
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn declared_finite_functor_identity_law() {
        let mut f = DeclaredFiniteFunctor::new("Id", "C", "C");
        f.map_object("A", "A");
        f.map_object("B", "B");
        f.map_morphism("id_A", "id_A");
        f.map_morphism("id_B", "id_B");

        let violations = check_identity_law(&f);
        assert!(
            violations.is_empty(),
            "Identity law should pass: {:?}",
            violations
        );
    }

    #[test]
    fn declared_finite_functor_missing_mapping_is_violation() {
        let mut f = DeclaredFiniteFunctor::new("F", "C", "D");
        f.map_object("A", "X");
        // id_A is not mapped — this must be a violation, not silent skip
        let violations = check_identity_law(&f);
        assert_eq!(violations.len(), 1);
        assert!(violations[0].contains("not defined"));
    }

    #[test]
    fn composition_law_missing_mapping_is_violation() {
        let mut f = DeclaredFiniteFunctor::new("F", "C", "D");
        f.map_morphism("f", "Ff");
        // g is not mapped
        f.map_morphism("gf", "Fgf");

        let target_comp: BTreeMap<(String, String), String> = BTreeMap::new();
        let violations = check_composition_law(&f, &[("f", "g", "gf")], &target_comp);
        assert!(!violations.is_empty());
        assert!(violations[0].contains("not defined"));
    }

    #[test]
    fn object_totality_check() {
        let mut f = DeclaredFiniteFunctor::new("F", "C", "D");
        f.map_object("A", "X");
        let violations = check_object_totality(&f, &["A", "B"]);
        assert_eq!(violations.len(), 1);
        assert!(violations[0].contains("B"));
    }
}
