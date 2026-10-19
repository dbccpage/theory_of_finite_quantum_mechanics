//! Natural Transformations — Spec Section 2.
//!
//! A natural transformation η : F ⇒ G between functors F, G : C → D
//! assigns to each object A in C a morphism η_A : F(A) → G(A) in D,
//! such that the naturality square commutes:
//!
//!   For all f: A → B in C:
//!     η_B ∘ F(f) = G(f) ∘ η_A
//!
//! Only the immutable owned finite certificate checks complete endpoint functors,
//! component domains/boundaries and all squares. Generic traits and public raw
//! records are caller contracts; separate diagnostics inspect supplied tables
//! and are vacuous on empty supplied domains. AuthorityEffect: None.

use super::cat_functor::{CatFunctor, Category, CompositionLookup, DeclaredFiniteFunctor};
use super::finite_category::DeclaredFiniteCategory;
use super::validation::{
    NatTransValidation, ValidationLocation, ValidationReport, ValidationSeverity, ValidationUnit,
    ValidationViolation,
};
use std::collections::BTreeMap;

/// Compatibility marker for abstract arithmos modules that talk about natural
/// isomorphisms independently of the finite natural-transformation records.
pub trait NaturalIsomorphism {
    type C;
    type F;
    type G;
}

// ---------------------------------------------------------------------------
// Trait: NaturalTransformation
// ---------------------------------------------------------------------------

/// A natural transformation η : F ⇒ G.
///
/// F and G must share the same source and target categories.
pub trait NaturalTransformation {
    type F: CatFunctor;
    type G: CatFunctor<
        Source = <Self::F as CatFunctor>::Source,
        Target = <Self::F as CatFunctor>::Target,
    >;

    /// The component η_A : F(A) → G(A) in the target category.
    fn component(
        &self,
        x: &<<Self::F as CatFunctor>::Source as Category>::Ob,
    ) -> <<Self::F as CatFunctor>::Target as Category>::Mor;
}

// ---------------------------------------------------------------------------
// Data: DeclaredFiniteNaturalTransformation
// ---------------------------------------------------------------------------

/// An explicit, finite natural transformation declaration for kernel audit.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteNatTrans {
    pub name: String,
    pub source_functor: String,
    pub target_functor: String,
    /// Component map: object name → morphism name in the target category.
    pub components: BTreeMap<String, String>,
}

impl DeclaredFiniteNatTrans {
    pub fn new(name: &str, source_functor: &str, target_functor: &str) -> Self {
        Self {
            name: name.into(),
            source_functor: source_functor.into(),
            target_functor: target_functor.into(),
            components: BTreeMap::new(),
        }
    }

    pub fn set_component(&mut self, object: &str, morphism: &str) {
        self.components.insert(object.into(), morphism.into());
    }

    pub fn component(&self, object: &str) -> Option<&str> {
        self.components.get(object).map(|s| s.as_str())
    }
}

// ---------------------------------------------------------------------------
// Validated Wrapper
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteNatTrans {
    declared: DeclaredFiniteNatTrans,
    source_category: DeclaredFiniteCategory,
    target_category: DeclaredFiniteCategory,
    source_functor: DeclaredFiniteFunctor,
    target_functor: DeclaredFiniteFunctor,
}

impl ValidatedFiniteNatTrans {
    pub fn try_new(
        declared: DeclaredFiniteNatTrans,
        source_category: &DeclaredFiniteCategory,
        target_category: &DeclaredFiniteCategory,
        source_functor: &DeclaredFiniteFunctor,
        target_functor: &DeclaredFiniteFunctor,
    ) -> Result<Self, ValidationReport> {
        let report = validate_natural_transformation_between(
            &declared,
            source_category,
            target_category,
            source_functor,
            target_functor,
        );

        if report.all_passed() {
            Ok(Self {
                declared,
                source_category: source_category.clone(),
                target_category: target_category.clone(),
                source_functor: source_functor.clone(),
                target_functor: target_functor.clone(),
            })
        } else {
            Err(report)
        }
    }

    pub fn declared(&self) -> &DeclaredFiniteNatTrans {
        &self.declared
    }
    pub fn source_category(&self) -> &DeclaredFiniteCategory {
        &self.source_category
    }
    pub fn target_category(&self) -> &DeclaredFiniteCategory {
        &self.target_category
    }
    pub fn source_functor(&self) -> &DeclaredFiniteFunctor {
        &self.source_functor
    }
    pub fn target_functor(&self) -> &DeclaredFiniteFunctor {
        &self.target_functor
    }
}

// ---------------------------------------------------------------------------
// Validation Logic
// ---------------------------------------------------------------------------

/// Exhaustive finite naturality admission. A certificate requires lawful
/// endpoint categories and total lawful functors; component data alone is not
/// sufficient. Runtime finite verification only. AuthorityEffect: None.
pub fn validate_natural_transformation_between(
    nat: &DeclaredFiniteNatTrans,
    source_category: &DeclaredFiniteCategory,
    target_category: &DeclaredFiniteCategory,
    source_functor: &DeclaredFiniteFunctor,
    target_functor: &DeclaredFiniteFunctor,
) -> ValidationReport {
    let mut report = ValidationReport::new(&nat.name);
    check_functor_endpoints(
        &mut report,
        source_category,
        target_category,
        source_functor,
        target_functor,
    );
    add_nat_errors(&mut report, NatTransValidation::Name, check_nat_name(nat));
    add_nat_errors(
        &mut report,
        NatTransValidation::FunctorBinding,
        check_functor_binding(nat, source_functor, target_functor),
    );
    add_nat_errors(
        &mut report,
        NatTransValidation::ComponentDomain,
        check_component_domain(nat, source_category),
    );
    add_nat_errors(
        &mut report,
        NatTransValidation::ComponentBoundary,
        check_component_boundaries(
            nat,
            source_category,
            target_category,
            source_functor,
            target_functor,
        ),
    );
    add_nat_errors(
        &mut report,
        NatTransValidation::NaturalitySquare,
        check_naturality_square(
            nat,
            source_category,
            &source_functor.morphism_map,
            &target_functor.morphism_map,
            &target_category.compositions,
        ),
    );
    report
}

fn check_functor_endpoints(
    report: &mut ValidationReport,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
    f: &DeclaredFiniteFunctor,
    g: &DeclaredFiniteFunctor,
) {
    let checked_f = super::functor_composition::validate_functor_between(f, source, target);
    report.add_typed("nat::source_functor", checked_f.typed_violations);
    if f != g {
        let checked_g = super::functor_composition::validate_functor_between(g, source, target);
        report.add_typed("nat::target_functor", checked_g.typed_violations);
    }
}

fn add_nat_errors(report: &mut ValidationReport, unit: NatTransValidation, errors: Vec<String>) {
    let violations = errors
        .into_iter()
        .map(|message| {
            ValidationViolation::new(
                ValidationUnit::NatTrans(unit),
                ValidationLocation::Global,
                message,
                ValidationSeverity::Error,
            )
        })
        .collect();
    report.add_typed(&format!("nat::{unit:?}"), violations);
}

fn check_nat_name(nat: &DeclaredFiniteNatTrans) -> Vec<String> {
    if nat.name.trim().is_empty() {
        return vec!["Empty natural transformation name".into()];
    }
    Vec::new()
}

fn check_functor_binding(
    nat: &DeclaredFiniteNatTrans,
    f: &DeclaredFiniteFunctor,
    g: &DeclaredFiniteFunctor,
) -> Vec<String> {
    if nat.source_functor != f.name || nat.target_functor != g.name {
        return vec![format!(
            "Transformation {} names {} => {}, expected {} => {}",
            nat.name, nat.source_functor, nat.target_functor, f.name, g.name
        )];
    }
    Vec::new()
}

fn check_component_domain(
    nat: &DeclaredFiniteNatTrans,
    source: &DeclaredFiniteCategory,
) -> Vec<String> {
    if !nat.components.keys().eq(source.objects.iter()) {
        return vec!["Component domain differs from the source objects".into()];
    }
    Vec::new()
}

pub fn check_component_boundaries(
    nat: &DeclaredFiniteNatTrans,
    source_category: &DeclaredFiniteCategory,
    target_category: &DeclaredFiniteCategory,
    source_functor: &DeclaredFiniteFunctor,
    target_functor: &DeclaredFiniteFunctor,
) -> Vec<String> {
    let mut violations = Vec::new();

    for obj in &source_category.objects {
        let Some(component) = nat.component(obj) else {
            violations.push(format!("Natural transformation: η_{} is not defined", obj));
            continue;
        };

        let Some(f_obj) = source_functor.object_map.get(obj) else {
            violations.push(format!("Natural transformation: F({}) is not defined", obj));
            continue;
        };

        let Some(g_obj) = target_functor.object_map.get(obj) else {
            violations.push(format!("Natural transformation: G({}) is not defined", obj));
            continue;
        };

        let Some(actual_mor) = target_category.morphisms.get(component) else {
            violations.push(format!(
                "Natural transformation: component η_{} = {} is not a target morphism",
                obj, component
            ));
            continue;
        };

        if actual_mor.source != *f_obj || actual_mor.target != *g_obj {
            violations.push(format!(
                "Natural transformation: η_{} = {} has boundary {} -> {}, expected {} -> {}",
                obj, component, actual_mor.source, actual_mor.target, f_obj, g_obj
            ));
        }
    }

    violations
}

/// Check every requested square, reporting absent data as a failure. This
/// diagnostic can be used on partial declarations; it never silently skips one.
pub fn check_naturality_square(
    nat: &DeclaredFiniteNatTrans,
    source_category: &DeclaredFiniteCategory,
    f_map: &BTreeMap<String, String>,
    g_map: &BTreeMap<String, String>,
    target_compositions: &BTreeMap<(String, String), String>,
) -> Vec<String> {
    let lookup = CompositionLookup::new(target_compositions);
    source_category
        .morphisms
        .iter()
        .filter_map(|(name, mor)| {
            check_square_at(
                nat,
                name,
                &mor.source,
                &mor.target,
                f_map,
                g_map,
                &lookup,
            )
            .err()
        })
        .collect()
}

fn check_square_at(
    nat: &DeclaredFiniteNatTrans,
    mor: &str,
    source: &str,
    target: &str,
    f_map: &BTreeMap<String, String>,
    g_map: &BTreeMap<String, String>,
    table: &CompositionLookup<'_>,
) -> Result<(), String> {
    let eta_a = nat
        .component(source)
        .ok_or_else(|| format!("Missing component at {source}"))?;
    let eta_b = nat
        .component(target)
        .ok_or_else(|| format!("Missing component at {target}"))?;
    let f_mor = f_map.get(mor).ok_or_else(|| format!("Missing F({mor})"))?;
    let g_mor = g_map.get(mor).ok_or_else(|| format!("Missing G({mor})"))?;
    let left = table
        .compose(f_mor, eta_b)
        .ok_or_else(|| format!("Missing eta_{target} after F({mor})"))?;
    let right = table
        .compose(eta_a, g_mor)
        .ok_or_else(|| format!("Missing G({mor}) after eta_{source}"))?;
    if left != right {
        return Err(format!(
            "Naturality fails at {mor}: left {left}, right {right}"
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::finite_category_builder::DeclaredFiniteCategoryBuilder;

    fn identity_fixture() -> (
        DeclaredFiniteCategory,
        DeclaredFiniteFunctor,
        DeclaredFiniteNatTrans,
    ) {
        let cat = DeclaredFiniteCategoryBuilder::walking_arrow("C", "A", "B", "f").build();
        let functor = crate::functor_composition::identity_functor(&cat, "Id");
        let mut nat = DeclaredFiniteNatTrans::new("eta", "Id", "Id");
        nat.set_component("A", "id_A");
        nat.set_component("B", "id_B");
        (cat, functor, nat)
    }

    #[test]
    fn rejects_partial_functor_instead_of_skipping_the_square() {
        let (cat, mut functor, nat) = identity_fixture();
        functor.morphism_map.remove("f");
        assert!(ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &functor, &functor).is_err());
    }

    #[test]
    fn admitted_certificate_owns_its_endpoint_context() {
        let (mut cat, mut f, nat) = identity_fixture();
        let checked = ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &f, &f).unwrap();
        cat.compositions.clear();
        f.morphism_map.clear();
        assert!(checked.source_category().compose("id_A", "f").is_some());
        assert_eq!(checked.source_functor().on_morphism("f"), Some("f"));
    }

    #[test]
    fn full_maps_do_not_excuse_unlawful_functors_or_nonassociative_categories() {
        let table = [[0, 1, 2], [1, 0, 0], [2, 1, 0]];
        let mut cat = DeclaredFiniteCategory::new("nonassociative");
        for a in 0..3 {
            cat.add_morphism(&a.to_string(), "*", "*");
        }
        cat.set_identity("*", "0");
        for a in 0..3 {
            for b in 0..3 {
                cat.set_composition(&a.to_string(), &b.to_string(), &table[a][b].to_string());
            }
        }
        let f = crate::functor_composition::identity_functor(&cat, "F");
        let mut nat = DeclaredFiniteNatTrans::new("eta", "F", "F");
        nat.set_component("*", "0");
        assert!(check_naturality_square(
            &nat,
            &cat,
            &f.morphism_map,
            &f.morphism_map,
            &cat.compositions
        )
        .is_empty());
        assert!(ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &f, &f).is_err());

        // A total map C3 -> C3 preserving identities but not composition.
        let mut cyclic = DeclaredFiniteCategory::new("C3");
        for a in 0..3 {
            cyclic.add_morphism(&a.to_string(), "*", "*");
        }
        cyclic.set_identity("*", "0");
        for a in 0..3 {
            for b in 0..3 {
                cyclic.set_composition(&a.to_string(), &b.to_string(), &((a + b) % 3).to_string());
            }
        }
        let mut f = DeclaredFiniteFunctor::new("F", "C3", "C3");
        f.map_object("*", "*");
        for (a, b) in [("0", "0"), ("1", "1"), ("2", "1")] {
            f.map_morphism(a, b);
        }
        let mut nat = DeclaredFiniteNatTrans::new("eta", "F", "F");
        nat.set_component("*", "0");
        assert!(check_naturality_square(
            &nat,
            &cyclic,
            &f.morphism_map,
            &f.morphism_map,
            &cyclic.compositions
        )
        .is_empty());
        assert!(ValidatedFiniteNatTrans::try_new(nat, &cyclic, &cyclic, &f, &f).is_err());
    }

    #[test]
    fn every_missing_square_operand_and_path_is_a_reported_error() {
        let (cat, f, nat) = identity_fixture();
        let mut partial = f.morphism_map.clone();
        partial.remove("f");
        assert!(
            !check_naturality_square(&nat, &cat, &f.morphism_map, &partial, &cat.compositions)
                .is_empty()
        );
        for object in ["A", "B"] {
            let mut bad = nat.clone();
            bad.components.remove(object);
            assert!(!check_naturality_square(
                &bad,
                &cat,
                &f.morphism_map,
                &f.morphism_map,
                &cat.compositions
            )
            .is_empty());
        }
        for (first, second) in [("f", "id_B"), ("id_A", "f")] {
            let mut table = cat.compositions.clone();
            table.remove(&(first.into(), second.into()));
            assert!(
                !check_naturality_square(&nat, &cat, &f.morphism_map, &f.morphism_map, &table)
                    .is_empty()
            );
        }
        let mut nameless = nat.clone();
        nameless.name.clear();
        assert!(ValidatedFiniteNatTrans::try_new(nameless, &cat, &cat, &f, &f).is_err());
        let mut wrong = nat.clone();
        wrong.source_functor = "other".into();
        assert!(ValidatedFiniteNatTrans::try_new(wrong, &cat, &cat, &f, &f).is_err());
        let mut wrong = nat.clone();
        wrong.set_component("A", "f");
        assert!(ValidatedFiniteNatTrans::try_new(wrong, &cat, &cat, &f, &f).is_err());
    }

    #[test]
    fn square_checker_reports_missing_maps_and_components() {
        let (cat, functor, mut nat) = identity_fixture();
        let mut partial = functor.morphism_map.clone();
        partial.remove("f");
        assert!(!check_naturality_square(
            &nat,
            &cat,
            &partial,
            &functor.morphism_map,
            &cat.compositions
        )
        .is_empty());
        nat.components.remove("A");
        assert!(!check_naturality_square(
            &nat,
            &cat,
            &functor.morphism_map,
            &functor.morphism_map,
            &cat.compositions
        )
        .is_empty());
    }

    #[test]
    fn rejects_extra_components_and_unlawful_endpoint_categories() {
        let (mut cat, functor, mut nat) = identity_fixture();
        nat.set_component("outside", "id_A");
        assert!(ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &functor, &functor).is_err());
        let (_, _, nat) = identity_fixture();
        cat.compositions.remove(&("id_A".into(), "id_A".into()));
        assert!(ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &functor, &functor).is_err());
    }

    #[test]
    fn trivial_nat_trans_passes_naturality() {
        let cat = DeclaredFiniteCategoryBuilder::new("C")
            .object("A")
            .object("B")
            .identity("A", "id_A")
            .identity("B", "id_B")
            .morphism("f", "A", "B")
            .composition("id_A", "id_A", "id_A")
            .composition("id_B", "id_B", "id_B")
            .composition("id_A", "f", "f")
            .composition("f", "id_B", "f")
            .build();

        let mut nat = DeclaredFiniteNatTrans::new("id_η", "Id", "Id");
        nat.set_component("A", "id_A");
        nat.set_component("B", "id_B");

        let mut f_functor = DeclaredFiniteFunctor::new("Id", "C", "C");
        f_functor.map_object("A", "A");
        f_functor.map_object("B", "B");
        f_functor.map_morphism("id_A", "id_A");
        f_functor.map_morphism("id_B", "id_B");
        f_functor.map_morphism("f", "f");

        let report =
            validate_natural_transformation_between(&nat, &cat, &cat, &f_functor, &f_functor);
        assert!(report.all_passed(), "Should pass: {:?}", report);
    }
}
