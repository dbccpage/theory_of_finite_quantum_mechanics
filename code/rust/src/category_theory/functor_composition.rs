//! First-class finite functor operations.
//!
//! This module keeps `DeclaredFiniteFunctor` as auditable data and adds the
//! derived operations needed to build larger categorical structures.
//! Only this module's immutable certificate constructor admits both endpoints
//! and all finite functor laws. Its type is distinct from cat_functor's wrapper.
//! Raw identity/composition/opposite/inclusion helpers return declarations that
//! require separate admission; inclusion checks membership/boundaries only.
//! Composing certificates returns a raw declaration, with exact middle-context
//! equality enforced first. Empty or invalid caller names are not repaired.

use super::cat_functor::{CompositionLookup, DeclaredFiniteFunctor};
use super::finite_category::{DeclaredFiniteCategory, DeclaredMorphism};
use super::validation::{
    FunctorValidation, ValidationLocation, ValidationReport, ValidationSeverity, ValidationUnit,
    ValidationViolation,
};

fn violation(
    unit: FunctorValidation,
    location: ValidationLocation,
    message: impl Into<String>,
) -> ValidationViolation {
    ValidationViolation::new(
        ValidationUnit::Functor(unit),
        location,
        message,
        ValidationSeverity::Error,
    )
}

fn add_unit(
    report: &mut ValidationReport,
    unit: FunctorValidation,
    violations: Vec<ValidationViolation>,
) {
    report.add_typed(&format!("functor::{:?}", unit), violations);
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteFunctor {
    declared: DeclaredFiniteFunctor,
    source: DeclaredFiniteCategory,
    target: DeclaredFiniteCategory,
}

impl ValidatedFiniteFunctor {
    pub fn try_new(
        declared: DeclaredFiniteFunctor,
        source: &DeclaredFiniteCategory,
        target: &DeclaredFiniteCategory,
    ) -> Result<Self, ValidationReport> {
        let report = validate_functor_between(&declared, source, target);
        if report.all_passed() {
            Ok(Self {
                declared,
                source: source.clone(),
                target: target.clone(),
            })
        } else {
            Err(report)
        }
    }

    pub fn declared(&self) -> &DeclaredFiniteFunctor {
        &self.declared
    }

    pub fn source(&self) -> &DeclaredFiniteCategory {
        &self.source
    }

    pub fn target(&self) -> &DeclaredFiniteCategory {
        &self.target
    }

    pub fn into_declared(self) -> DeclaredFiniteFunctor {
        self.declared
    }
}

pub fn identity_functor(category: &DeclaredFiniteCategory, name: &str) -> DeclaredFiniteFunctor {
    let mut functor = DeclaredFiniteFunctor::new(name, &category.name, &category.name);

    for object in &category.objects {
        functor.map_object(object, object);
    }
    for morphism in category.morphisms.keys() {
        functor.map_morphism(morphism, morphism);
    }

    functor
}

/// Compose raw declared functors F : C -> D and G : D -> E as G after F.
/// This does not validate that the inputs or output are lawful functors.
pub fn compose_declared_functors(
    name: &str,
    first: &DeclaredFiniteFunctor,
    second: &DeclaredFiniteFunctor,
) -> Result<DeclaredFiniteFunctor, String> {
    if first.target_category != second.source_category {
        return Err(format!(
            "Cannot compose {} then {}: target {} does not match source {}",
            first.name, second.name, first.target_category, second.source_category
        ));
    }

    let mut composite =
        DeclaredFiniteFunctor::new(name, &first.source_category, &second.target_category);

    for (object, middle_object) in &first.object_map {
        let Some(target_object) = second.object_map.get(middle_object) else {
            return Err(format!(
                "Cannot compose object {}: {}({}) = {}, but {} is undefined there",
                object, first.name, object, middle_object, second.name
            ));
        };
        composite.map_object(object, target_object);
    }

    for (morphism, middle_morphism) in &first.morphism_map {
        let Some(target_morphism) = second.morphism_map.get(middle_morphism) else {
            return Err(format!(
                "Cannot compose morphism {}: {}({}) = {}, but {} is undefined there",
                morphism, first.name, morphism, middle_morphism, second.name
            ));
        };
        composite.map_morphism(morphism, target_morphism);
    }

    Ok(composite)
}

/// Compose two validated functors. Requires that the first functor's target
/// exactly matches the second functor's source.
pub fn compose_validated_functors(
    name: &str,
    first: &ValidatedFiniteFunctor,
    second: &ValidatedFiniteFunctor,
) -> Result<DeclaredFiniteFunctor, String> {
    if first.target() != second.source() {
        return Err(format!(
            "Cannot compose validated functors {} and {}: target {} does not match source {}",
            first.declared().name,
            second.declared().name,
            first.target().name,
            second.source().name
        ));
    }

    compose_declared_functors(name, first.declared(), second.declared())
}

pub fn opposite_category(category: &DeclaredFiniteCategory, name: &str) -> DeclaredFiniteCategory {
    let mut opposite = DeclaredFiniteCategory::new(name);

    opposite.objects = category.objects.clone();
    for morphism in category.morphisms.values() {
        if !opposite.objects.contains(&morphism.target) {
            opposite.add_object(&morphism.target);
        }
        if !opposite.objects.contains(&morphism.source) {
            opposite.add_object(&morphism.source);
        }
        opposite.morphisms.insert(morphism.name.clone(),
            DeclaredMorphism::new(&morphism.name, &morphism.target, &morphism.source));
    }
    for (object, identity) in &category.identities {
        if !opposite.objects.contains(object) {
            opposite.add_object(object);
        }
        opposite.identities.insert(object.clone(), identity.clone());
    }
    for ((first, second), composite) in &category.compositions {
        opposite.set_composition(second, first, composite);
    }

    opposite
}

/// Given F : C -> D, returns F^op : C^op -> D^op.
/// Object/morphism maps are unchanged; endpoint labels are supplied by the caller.
/// Opposite category structure must be constructed and admitted separately.
pub fn opposite_functor(
    name: &str,
    functor: &DeclaredFiniteFunctor,
    source_op_category: &str,
    target_op_category: &str,
) -> DeclaredFiniteFunctor {
    let mut opposite = DeclaredFiniteFunctor::new(name, source_op_category, target_op_category);
    opposite.object_map = functor.object_map.clone();
    opposite.morphism_map = functor.morphism_map.clone();
    opposite
}

pub fn inclusion_functor(
    name: &str,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteFunctor, String> {
    let mut functor = DeclaredFiniteFunctor::new(name, &source.name, &target.name);

    for object in &source.objects {
        if !target.has_object(object) {
            return Err(format!("Target category lacks object {}", object));
        }
        functor.map_object(object, object);
    }

    for (name, morphism) in &source.morphisms {
        let Some(target_morphism) = target.morphisms.get(name) else {
            return Err(format!("Target category lacks morphism {}", name));
        };
        if target_morphism.source != morphism.source || target_morphism.target != morphism.target {
            return Err(format!(
                "Target morphism {} has boundary {} -> {}, expected {} -> {}",
                name,
                target_morphism.source,
                target_morphism.target,
                morphism.source,
                morphism.target
            ));
        }
        functor.map_morphism(name, name);
    }

    Ok(functor)
}

pub fn declared_finite_functor_from_maps(
    name: &str,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
    object_map: &[(&str, &str)],
    morphism_map: &[(&str, &str)],
) -> DeclaredFiniteFunctor {
    let mut functor = DeclaredFiniteFunctor::new(name, &source.name, &target.name);
    for (source_object, target_object) in object_map {
        functor.map_object(source_object, target_object);
    }
    for (source_morphism, target_morphism) in morphism_map {
        functor.map_morphism(source_morphism, target_morphism);
    }
    functor
}

/// Exhaustive finite functor checking. Endpoints must first satisfy all finite
/// category laws; both maps have exactly the source domain. Law checks are
/// polynomial in the explicit tables, including O(m^3 log c) endpoint validation.
pub fn validate_functor_between(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> ValidationReport {
    let mut report = ValidationReport::new(&functor.name);
    check_endpoint_categories(&mut report, source, target);
    add_unit(
        &mut report,
        FunctorValidation::Name,
        check_functor_name(functor),
    );
    add_unit(
        &mut report,
        FunctorValidation::MappingDomain,
        check_mapping_domains(functor, source),
    );
    add_unit(
        &mut report,
        FunctorValidation::ObjectTotality,
        check_object_images(functor, source, target),
    );
    add_unit(
        &mut report,
        FunctorValidation::MorphismTotality,
        check_morphism_images(functor, source, target),
    );
    add_unit(
        &mut report,
        FunctorValidation::BoundaryPreservation,
        check_boundary_images(functor, source, target),
    );
    add_unit(
        &mut report,
        FunctorValidation::IdentityPreservation,
        check_identity_images(functor, source, target),
    );
    add_unit(
        &mut report,
        FunctorValidation::CompositionPreservation,
        check_composition_images(functor, source, target),
    );
    report
}

fn check_endpoint_categories(
    report: &mut ValidationReport,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) {
    let checked_source = super::finite_category_validation::validate_finite_category(source);
    report.add_typed("functor::source_category", checked_source.typed_violations);
    if source != target {
        let checked_target = super::finite_category_validation::validate_finite_category(target);
        report.add_typed("functor::target_category", checked_target.typed_violations);
    }
}

fn check_functor_name(functor: &DeclaredFiniteFunctor) -> Vec<ValidationViolation> {
    if functor.name.trim().is_empty() {
        return vec![violation(
            FunctorValidation::Name,
            ValidationLocation::Global,
            "Empty functor name",
        )];
    }
    Vec::new()
}

fn check_mapping_domains(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
) -> Vec<ValidationViolation> {
    let mut errors = Vec::new();
    if !functor.object_map.keys().eq(source.objects.iter()) {
        errors.push(violation(
            FunctorValidation::MappingDomain,
            ValidationLocation::Global,
            "Object map domain differs from source objects",
        ));
    }
    if !functor.morphism_map.keys().eq(source.morphisms.keys()) {
        errors.push(violation(
            FunctorValidation::MappingDomain,
            ValidationLocation::Global,
            "Morphism map domain differs from source morphisms",
        ));
    }
    errors
}

fn check_object_images(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> Vec<ValidationViolation> {
    let mut object_violations = Vec::new();
    if functor.source_category != source.name {
        object_violations.push(violation(
            FunctorValidation::ObjectTotality,
            ValidationLocation::Global,
            format!(
                "Functor source category is {}, expected {}",
                functor.source_category, source.name
            ),
        ));
    }
    if functor.target_category != target.name {
        object_violations.push(violation(
            FunctorValidation::ObjectTotality,
            ValidationLocation::Global,
            format!(
                "Functor target category is {}, expected {}",
                functor.target_category, target.name
            ),
        ));
    }

    for object in &source.objects {
        match functor.on_object(object) {
            Some(image) if target.has_object(image) => {}
            Some(image) => object_violations.push(violation(
                FunctorValidation::ObjectTotality,
                ValidationLocation::Object(object.clone()),
                format!(
                    "F({}) = {} is not an object of {}",
                    object, image, target.name
                ),
            )),
            None => object_violations.push(violation(
                FunctorValidation::ObjectTotality,
                ValidationLocation::Object(object.clone()),
                format!("Object {} is not mapped by {}", object, functor.name),
            )),
        }
    }
    object_violations
}

fn check_morphism_images(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> Vec<ValidationViolation> {
    let mut morphism_violations = Vec::new();
    for morphism in source.morphisms.keys() {
        match functor.on_morphism(morphism) {
            Some(image) if target.has_morphism(image) => {}
            Some(image) => morphism_violations.push(violation(
                FunctorValidation::MorphismTotality,
                ValidationLocation::Morphism(morphism.clone()),
                format!(
                    "F({}) = {} is not a morphism of {}",
                    morphism, image, target.name
                ),
            )),
            None => morphism_violations.push(violation(
                FunctorValidation::MorphismTotality,
                ValidationLocation::Morphism(morphism.clone()),
                format!("Morphism {} is not mapped by {}", morphism, functor.name),
            )),
        }
    }
    morphism_violations
}

fn check_boundary_images(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> Vec<ValidationViolation> {
    let mut boundary_violations = Vec::new();
    for morphism in source.morphisms.values() {
        let Some(image_morphism) = functor.on_morphism(&morphism.name) else {
            continue;
        };
        let Some(image_source) = functor.on_object(&morphism.source) else {
            continue;
        };
        let Some(image_target) = functor.on_object(&morphism.target) else {
            continue;
        };
        let Some((actual_source, actual_target)) = target.boundary_of(image_morphism) else {
            continue;
        };

        if actual_source != image_source || actual_target != image_target {
            boundary_violations.push(violation(
                FunctorValidation::BoundaryPreservation,
                ValidationLocation::Boundary {
                    morphism: morphism.name.clone(),
                    source: image_source.into(),
                    target: image_target.into(),
                },
                format!(
                    "F({}) has boundary {} -> {}, expected {} -> {}",
                    morphism.name, actual_source, actual_target, image_source, image_target
                ),
            ));
        }
    }
    boundary_violations
}

fn check_identity_images(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> Vec<ValidationViolation> {
    let mut identity_violations = Vec::new();
    for object in &source.objects {
        let Some(source_identity) = source.identity_of(object) else {
            continue;
        };
        let Some(image_object) = functor.on_object(object) else {
            continue;
        };
        let Some(expected_identity) = target.identity_of(image_object) else {
            continue;
        };
        match functor.on_morphism(source_identity) {
            Some(image_identity) if image_identity == expected_identity => {}
            Some(image_identity) => identity_violations.push(violation(
                FunctorValidation::IdentityPreservation,
                ValidationLocation::Object(object.clone()),
                format!(
                    "F(id_{}) = {}, expected {}",
                    object, image_identity, expected_identity
                ),
            )),
            None => identity_violations.push(violation(
                FunctorValidation::IdentityPreservation,
                ValidationLocation::Morphism(source_identity.into()),
                format!("F({}) is not defined", source_identity),
            )),
        }
    }
    identity_violations
}

fn check_composition_images(
    functor: &DeclaredFiniteFunctor,
    source: &DeclaredFiniteCategory,
    target: &DeclaredFiniteCategory,
) -> Vec<ValidationViolation> {
    let mut composition_violations = Vec::new();
    let lookup = CompositionLookup::new(&target.compositions);
    for ((first, second), composite) in &source.compositions {
        let Some(first_image) = functor.on_morphism(first) else {
            continue;
        };
        let Some(second_image) = functor.on_morphism(second) else {
            continue;
        };
        let Some(composite_image) = functor.on_morphism(composite) else {
            continue;
        };

        match lookup.compose(first_image, second_image) {
            Some(target_composite) if target_composite == composite_image => {}
            Some(target_composite) => composition_violations.push(violation(
                FunctorValidation::CompositionPreservation,
                ValidationLocation::Composition {
                    first: first.clone(),
                    second: second.clone(),
                    composite: Some(composite.clone()),
                },
                format!(
                    "F({} after {}) = {}, but F({}) after F({}) = {}",
                    second, first, composite_image, second, first, target_composite
                ),
            )),
            None => composition_violations.push(violation(
                FunctorValidation::CompositionPreservation,
                ValidationLocation::Composition {
                    first: first.clone(),
                    second: second.clone(),
                    composite: Some(composite.clone()),
                },
                format!(
                    "Target composition F({}) after F({}) is not defined",
                    second, first
                ),
            )),
        }
    }
    composition_violations
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn admission_rejects_non_categories_and_extra_map_entries() {
        let mut c = walking_arrow("C");
        let valid = identity_functor(&c, "F");
        let mut extra = valid.clone();
        extra.map_object("outside", "A");
        assert!(ValidatedFiniteFunctor::try_new(extra, &c, &c).is_err());
        c.compositions.clear();
        assert!(ValidatedFiniteFunctor::try_new(valid, &c, &c).is_err());
    }

    #[test]
    fn composition_rejects_different_middle_categories_with_the_same_name() {
        let middle = walking_arrow("SameName");
        let mut different = middle.clone();
        different.add_identity("Extra", "id_Extra");
        different.set_composition("id_Extra", "id_Extra", "id_Extra");
        let first =
            ValidatedFiniteFunctor::try_new(identity_functor(&middle, "F"), &middle, &middle)
                .unwrap();
        let second = ValidatedFiniteFunctor::try_new(
            identity_functor(&different, "G"),
            &different,
            &different,
        )
        .unwrap();
        assert!(compose_validated_functors("GF", &first, &second).is_err());
    }
    use crate::finite_category_builder::DeclaredFiniteCategoryBuilder;

    fn walking_arrow(name: &str) -> DeclaredFiniteCategory {
        DeclaredFiniteCategoryBuilder::new(name)
            .identity("A", "id_A")
            .identity("B", "id_B")
            .morphism("f", "A", "B")
            .identity_compositions()
            .build()
    }

    #[test]
    fn identity_functor_validates() {
        let cat = walking_arrow("C");
        let id = identity_functor(&cat, "Id_C");
        let report = validate_functor_between(&id, &cat, &cat);
        assert!(report.all_passed(), "{:?}", report.typed_violations);
    }

    #[test]
    fn functor_composition_maps_through_middle() {
        let c = walking_arrow("C");
        let d = walking_arrow("D");
        let e = walking_arrow("E");

        let f = declared_finite_functor_from_maps(
            "F",
            &c,
            &d,
            &[("A", "A"), ("B", "B")],
            &[("id_A", "id_A"), ("id_B", "id_B"), ("f", "f")],
        );
        let g = declared_finite_functor_from_maps(
            "G",
            &d,
            &e,
            &[("A", "A"), ("B", "B")],
            &[("id_A", "id_A"), ("id_B", "id_B"), ("f", "f")],
        );

        let gf = compose_declared_functors("GF", &f, &g).expect("composition should exist");
        assert_eq!(gf.on_object("A"), Some("A"));
        assert_eq!(gf.on_morphism("f"), Some("f"));
        assert!(validate_functor_between(&gf, &c, &e).all_passed());
    }

    #[test]
    fn opposite_category_reverses_composition_order() {
        let cat = walking_arrow("C");
        let op = opposite_category(&cat, "C_op");

        assert_eq!(op.boundary_of("f"), Some(("B", "A")));
        assert_eq!(op.compose("f", "id_A"), Some("f"));
    }

    #[test]
    fn invalid_functor_reports_typed_boundary_violation() {
        let c = walking_arrow("C");
        let d = walking_arrow("D");
        let bad = declared_finite_functor_from_maps(
            "Bad",
            &c,
            &d,
            &[("A", "B"), ("B", "A")],
            &[("id_A", "id_B"), ("id_B", "id_A"), ("f", "f")],
        );

        let report = validate_functor_between(&bad, &c, &d);
        assert!(!report.all_passed());
        assert!(report.typed_violations.iter().any(|violation| {
            violation.unit == ValidationUnit::Functor(FunctorValidation::BoundaryPreservation)
        }));
    }

    #[test]
    fn invalid_functor_reports_composition_violation() {
        let source = DeclaredFiniteCategoryBuilder::new("Src")
            .identity_object("X")
            .identity_object("Y")
            .identity_object("Z")
            .morphism("u", "X", "Y")
            .morphism("v", "Y", "Z")
            .morphism("vu", "X", "Z")
            .path_composition("u", "v", "vu")
            .identity_compositions()
            .build();

        let target = source.clone();

        let bad = declared_finite_functor_from_maps(
            "BadComp",
            &source,
            &target,
            &[("X", "X"), ("Y", "Y"), ("Z", "Z")],
            &[
                ("id_X", "id_X"),
                ("id_Y", "id_Y"),
                ("id_Z", "id_Z"),
                ("u", "u"),
                ("v", "v"),
                ("vu", "u"),
            ],
        );

        let report = validate_functor_between(&bad, &source, &target);
        assert!(!report.all_passed());
        assert!(
            report
                .typed_violations
                .iter()
                .any(|v| v.unit
                    == ValidationUnit::Functor(FunctorValidation::CompositionPreservation))
        );
    }

    #[test]
    fn invalid_functor_reports_identity_violation() {
        let c = walking_arrow("C");
        let d = walking_arrow("D");

        let bad = declared_finite_functor_from_maps(
            "BadId",
            &c,
            &d,
            &[("A", "A"), ("B", "B")],
            &[("id_A", "id_B"), ("id_B", "id_B"), ("f", "f")],
        );

        let report = validate_functor_between(&bad, &c, &d);

        assert!(report.typed_violations.iter().any(|violation| {
            violation.unit == ValidationUnit::Functor(FunctorValidation::IdentityPreservation)
        }));
    }

    #[test]
    fn partial_functor_reports_totality_violations() {
        let c = walking_arrow("C");
        let d = walking_arrow("D");

        let partial = declared_finite_functor_from_maps(
            "Partial",
            &c,
            &d,
            &[("A", "A")],
            &[("id_A", "id_A")],
        );

        let report = validate_functor_between(&partial, &c, &d);
        assert!(!report.all_passed());
        assert!(report
            .typed_violations
            .iter()
            .any(|v| v.unit == ValidationUnit::Functor(FunctorValidation::ObjectTotality)));
        assert!(report
            .typed_violations
            .iter()
            .any(|v| v.unit == ValidationUnit::Functor(FunctorValidation::MorphismTotality)));
    }
}
