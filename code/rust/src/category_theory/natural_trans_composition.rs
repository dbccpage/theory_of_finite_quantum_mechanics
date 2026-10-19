//! Finite natural-transformation composition. AuthorityEffect: None.
//!
//! Functions on `Declared*` data assemble candidates and reject missing data;
//! they do not certify naturality. The `*_validated_*` operations own and check
//! complete category/functor contexts, then replay output admission. Both paths
//! for horizontal composition must agree. No sampled or infinite claim is made.

use super::cat_functor::{CompositionLookup, DeclaredFiniteFunctor};
use super::finite_category::DeclaredFiniteCategory;
use super::functor_composition::{compose_declared_functors, ValidatedFiniteFunctor};
use super::natural_trans::{DeclaredFiniteNatTrans, ValidatedFiniteNatTrans};
use super::validation::ValidationReport;

#[derive(Debug, Clone)]
pub enum CompositionError {
    Binding {
        role: &'static str,
        expected: String,
        got: String,
    },
    ContextMismatch {
        boundary: &'static str,
    },
    Missing {
        kind: &'static str,
        owner: String,
        key: String,
    },
    Undefined {
        object: String,
        first: String,
        second: String,
    },
    Interchange {
        object: String,
        left: String,
        right: String,
    },
    FunctorComposition(String),
    Admission(ValidationReport),
}
impl std::fmt::Display for CompositionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for CompositionError {}

fn composite_name(outer: &str, inner: &str) -> String {
    format!("Comp[{outer} after {inner}]")
}

fn same(role: &'static str, expected: &str, got: &str) -> Result<(), CompositionError> {
    if expected != got {
        return Err(CompositionError::Binding {
            role,
            expected: expected.into(),
            got: got.into(),
        });
    }
    Ok(())
}

fn component<'a>(
    nat: &'a DeclaredFiniteNatTrans,
    object: &str,
) -> Result<&'a str, CompositionError> {
    nat.component(object)
        .ok_or_else(|| CompositionError::Missing {
            kind: "component",
            owner: nat.name.clone(),
            key: object.into(),
        })
}
fn mapped_morphism<'a>(
    functor: &'a DeclaredFiniteFunctor,
    name: &str,
) -> Result<&'a str, CompositionError> {
    functor
        .on_morphism(name)
        .ok_or_else(|| CompositionError::Missing {
            kind: "morphism image",
            owner: functor.name.clone(),
            key: name.into(),
        })
}
fn mapped_object<'a>(
    functor: &'a DeclaredFiniteFunctor,
    name: &str,
) -> Result<&'a str, CompositionError> {
    functor
        .on_object(name)
        .ok_or_else(|| CompositionError::Missing {
            kind: "object image",
            owner: functor.name.clone(),
            key: name.into(),
        })
}
fn compose_at<'a>(
    table: &CompositionLookup<'a>,
    object: &str,
    first: &str,
    second: &str,
) -> Result<&'a str, CompositionError> {
    table
        .compose(first, second)
        .ok_or_else(|| CompositionError::Undefined {
            object: object.into(),
            first: first.into(),
            second: second.into(),
        })
}

pub fn identity_nat_trans(
    name: &str,
    functor: &DeclaredFiniteFunctor,
    target_category: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteNatTrans, CompositionError> {
    same(
        "identity target category",
        &functor.target_category,
        &target_category.name,
    )?;
    let mut nat = DeclaredFiniteNatTrans::new(name, &functor.name, &functor.name);
    for (object, image) in &functor.object_map {
        let identity =
            target_category
                .identity_of(image)
                .ok_or_else(|| CompositionError::Missing {
                    kind: "identity",
                    owner: target_category.name.clone(),
                    key: image.clone(),
                })?;
        nat.set_component(object, identity);
    }
    Ok(nat)
}

/// Candidate beta after alpha, one component at every provided source object.
pub fn vertical_compose_nat_trans(
    name: &str,
    alpha: &DeclaredFiniteNatTrans,
    beta: &DeclaredFiniteNatTrans,
    source_category: &DeclaredFiniteCategory,
    target_category: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteNatTrans, CompositionError> {
    same(
        "vertical middle functor",
        &alpha.target_functor,
        &beta.source_functor,
    )?;
    let mut nat = DeclaredFiniteNatTrans::new(name, &alpha.source_functor, &beta.target_functor);
    let lookup = CompositionLookup::new(&target_category.compositions);
    for object in &source_category.objects {
        let first = component(alpha, object)?;
        let second = component(beta, object)?;
        nat.set_component(object, compose_at(&lookup, object, first, second)?);
    }
    Ok(nat)
}

/// Candidate H alpha: H F => H G.
pub fn left_whisker_nat_trans(
    name: &str,
    outer: &DeclaredFiniteFunctor,
    alpha: &DeclaredFiniteNatTrans,
) -> Result<DeclaredFiniteNatTrans, CompositionError> {
    let mut nat = DeclaredFiniteNatTrans::new(
        name,
        &composite_name(&outer.name, &alpha.source_functor),
        &composite_name(&outer.name, &alpha.target_functor),
    );
    for (object, arrow) in &alpha.components {
        nat.set_component(object, mapped_morphism(outer, arrow)?);
    }
    Ok(nat)
}

/// Candidate alpha K: F K => G K.
pub fn right_whisker_nat_trans(
    name: &str,
    alpha: &DeclaredFiniteNatTrans,
    inner: &DeclaredFiniteFunctor,
) -> Result<DeclaredFiniteNatTrans, CompositionError> {
    let mut nat = DeclaredFiniteNatTrans::new(
        name,
        &composite_name(&alpha.source_functor, &inner.name),
        &composite_name(&alpha.target_functor, &inner.name),
    );
    for (object, middle) in &inner.object_map {
        nat.set_component(object, component(alpha, middle)?);
    }
    Ok(nat)
}

struct HorizontalContext<'a> {
    alpha: &'a DeclaredFiniteNatTrans,
    beta: &'a DeclaredFiniteNatTrans,
    f: &'a DeclaredFiniteFunctor,
    g: &'a DeclaredFiniteFunctor,
    h: &'a DeclaredFiniteFunctor,
    k: &'a DeclaredFiniteFunctor,
    target: &'a DeclaredFiniteCategory,
}
impl HorizontalContext<'_> {
    fn check_binding(&self) -> Result<(), CompositionError> {
        self.check_transformation_names()?;
        check_parallel(self.f, self.g)?;
        check_parallel(self.h, self.k)?;
        same(
            "horizontal middle category",
            &self.f.target_category,
            &self.h.source_category,
        )?;
        same(
            "horizontal target category",
            &self.h.target_category,
            &self.target.name,
        )
    }
    fn check_transformation_names(&self) -> Result<(), CompositionError> {
        same("alpha source", &self.f.name, &self.alpha.source_functor)?;
        same("alpha target", &self.g.name, &self.alpha.target_functor)?;
        same("beta source", &self.h.name, &self.beta.source_functor)?;
        same("beta target", &self.k.name, &self.beta.target_functor)
    }
    fn component_at<'a>(&self, lookup: &CompositionLookup<'a>, object: &str) -> Result<&'a str, CompositionError> {
        let alpha = component(self.alpha, object)?;
        let left = self.left_path(lookup, object, alpha)?;
        let right = self.right_path(lookup, object, alpha)?;
        if left != right {
            return Err(CompositionError::Interchange {
                object: object.into(),
                left: left.into(),
                right: right.into(),
            });
        }
        Ok(left)
    }
    fn left_path<'a>(&self, lookup: &CompositionLookup<'a>, object: &str, alpha: &str) -> Result<&'a str, CompositionError> {
        let h_alpha = mapped_morphism(self.h, alpha)?;
        let g_object = mapped_object(self.g, object)?;
        compose_at(
            lookup,
            object,
            h_alpha,
            component(self.beta, g_object)?,
        )
    }
    fn right_path<'a>(&self, lookup: &CompositionLookup<'a>, object: &str, alpha: &str) -> Result<&'a str, CompositionError> {
        let k_alpha = mapped_morphism(self.k, alpha)?;
        let f_object = mapped_object(self.f, object)?;
        compose_at(
            lookup,
            object,
            component(self.beta, f_object)?,
            k_alpha,
        )
    }
}
fn check_parallel(
    f: &DeclaredFiniteFunctor,
    g: &DeclaredFiniteFunctor,
) -> Result<(), CompositionError> {
    same(
        "parallel source category",
        &f.source_category,
        &g.source_category,
    )?;
    same(
        "parallel target category",
        &f.target_category,
        &g.target_category,
    )
}

/// Candidate beta star alpha: H F => K G; verify both interchange paths.
pub fn horizontal_compose_nat_trans(
    name: &str,
    alpha: &DeclaredFiniteNatTrans,
    beta: &DeclaredFiniteNatTrans,
    f: &DeclaredFiniteFunctor,
    g: &DeclaredFiniteFunctor,
    h: &DeclaredFiniteFunctor,
    k: &DeclaredFiniteFunctor,
    target_category: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteNatTrans, CompositionError> {
    let context = HorizontalContext {
        alpha,
        beta,
        f,
        g,
        h,
        k,
        target: target_category,
    };
    context.check_binding()?;
    let lookup = CompositionLookup::new(&target_category.compositions);
    let mut nat = DeclaredFiniteNatTrans::new(
        name,
        &composite_name(&h.name, &f.name),
        &composite_name(&k.name, &g.name),
    );
    for object in f.object_map.keys() {
        nat.set_component(object, context.component_at(&lookup, object)?);
    }
    Ok(nat)
}

pub fn identity_validated_nat_trans(
    name: &str,
    functor: &ValidatedFiniteFunctor,
) -> Result<ValidatedFiniteNatTrans, CompositionError> {
    let candidate = identity_nat_trans(name, functor.declared(), functor.target())?;
    ValidatedFiniteNatTrans::try_new(
        candidate,
        functor.source(),
        functor.target(),
        functor.declared(),
        functor.declared(),
    )
    .map_err(CompositionError::Admission)
}

/// Vertical composition binds complete middle functor data, not just its name.
pub fn vertical_compose_validated_nat_trans(
    name: &str,
    alpha: &ValidatedFiniteNatTrans,
    beta: &ValidatedFiniteNatTrans,
) -> Result<ValidatedFiniteNatTrans, CompositionError> {
    check_vertical_context(alpha, beta)?;
    let candidate = vertical_compose_nat_trans(
        name,
        alpha.declared(),
        beta.declared(),
        alpha.source_category(),
        alpha.target_category(),
    )?;
    ValidatedFiniteNatTrans::try_new(
        candidate,
        alpha.source_category(),
        alpha.target_category(),
        alpha.source_functor(),
        beta.target_functor(),
    )
    .map_err(CompositionError::Admission)
}
fn check_vertical_context(
    alpha: &ValidatedFiniteNatTrans,
    beta: &ValidatedFiniteNatTrans,
) -> Result<(), CompositionError> {
    if alpha.source_category() != beta.source_category()
        || alpha.target_category() != beta.target_category()
        || alpha.target_functor() != beta.source_functor()
    {
        return Err(CompositionError::ContextMismatch {
            boundary: "vertical middle functor and categories",
        });
    }
    Ok(())
}

/// Horizontal composition is an operation on admitted finite diagrams. The
/// derived endpoint functors and transformation are admitted again before return.
pub fn horizontal_compose_validated_nat_trans(
    name: &str,
    alpha: &ValidatedFiniteNatTrans,
    beta: &ValidatedFiniteNatTrans,
) -> Result<ValidatedFiniteNatTrans, CompositionError> {
    if alpha.target_category() != beta.source_category() {
        return Err(CompositionError::ContextMismatch {
            boundary: "horizontal middle category",
        });
    }
    let (f, g, h, k) = (
        alpha.source_functor(),
        alpha.target_functor(),
        beta.source_functor(),
        beta.target_functor(),
    );
    let candidate = horizontal_compose_nat_trans(
        name,
        alpha.declared(),
        beta.declared(),
        f,
        g,
        h,
        k,
        beta.target_category(),
    )?;
    let source = compose_declared_functors(&candidate.source_functor, f, h)
        .map_err(CompositionError::FunctorComposition)?;
    let target = compose_declared_functors(&candidate.target_functor, g, k)
        .map_err(CompositionError::FunctorComposition)?;
    ValidatedFiniteNatTrans::try_new(
        candidate,
        alpha.source_category(),
        beta.target_category(),
        &source,
        &target,
    )
    .map_err(CompositionError::Admission)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cat_functor::DeclaredFiniteFunctor;
    use crate::functor_composition::identity_functor;

    fn cyclic_three() -> DeclaredFiniteCategory {
        let mut cat = DeclaredFiniteCategory::new("C3");
        for a in 0..3 {
            cat.add_morphism(&a.to_string(), "*", "*");
        }
        cat.set_identity("*", "0");
        for a in 0..3 {
            for b in 0..3 {
                cat.set_composition(&a.to_string(), &b.to_string(), &((a + b) % 3).to_string());
            }
        }
        cat
    }

    fn multiplier(name: &str, a: usize, cat: &DeclaredFiniteCategory) -> DeclaredFiniteFunctor {
        let mut f = DeclaredFiniteFunctor::new(name, &cat.name, &cat.name);
        f.map_object("*", "*");
        for x in 0..3 {
            f.map_morphism(&x.to_string(), &((a * x) % 3).to_string());
        }
        f
    }

    fn cyclic_nat(name: &str, a: usize, component: usize) -> ValidatedFiniteNatTrans {
        let cat = cyclic_three();
        let f = multiplier(name, a, &cat);
        let mut nat = DeclaredFiniteNatTrans::new("eta", name, name);
        nat.set_component("*", &component.to_string());
        ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &f, &f).unwrap()
    }

    #[test]
    fn cyclic_naturality_matches_the_generator_equation_for_all_27_candidates() {
        let cat = cyclic_three();
        for code in 0..27 {
            let (a, b, c) = (code % 3, (code / 3) % 3, (code / 9) % 3);
            let f = multiplier("F", a, &cat);
            let g = multiplier("G", b, &cat);
            let mut nat = DeclaredFiniteNatTrans::new("eta", "F", "G");
            nat.set_component("*", &c.to_string());
            // At the generator: c+a=b+c in C3, exactly when a=b.
            assert_eq!(
                ValidatedFiniteNatTrans::try_new(nat, &cat, &cat, &f, &g).is_ok(),
                a == b
            );
        }
    }

    #[test]
    fn horizontal_components_match_all_81_exact_scalar_cases() {
        for code in 0..81 {
            let (a, b, p, q) = (code % 3, (code / 3) % 3, (code / 9) % 3, (code / 27) % 3);
            let alpha = cyclic_nat("F", a, p);
            let beta = cyclic_nat("H", b, q);
            let result =
                horizontal_compose_validated_nat_trans("beta*alpha", &alpha, &beta).unwrap();
            assert_eq!(
                result.declared().component("*"),
                Some(((b * p + q) % 3).to_string().as_str())
            );
            for arrow in 0..3 {
                assert_eq!(
                    result.source_functor().on_morphism(&arrow.to_string()),
                    Some(((b * a * arrow) % 3).to_string().as_str())
                );
            }
        }
    }

    #[test]
    fn vertical_composition_has_units_and_is_associative() {
        let cat = cyclic_three();
        let f = multiplier("F", 1, &cat);
        let checked_f = ValidatedFiniteFunctor::try_new(f, &cat, &cat).unwrap();
        let id = identity_validated_nat_trans("id_F", &checked_f).unwrap();
        for code in 0..27 {
            let (a, b, c) = (code % 3, (code / 3) % 3, (code / 9) % 3);
            let alpha = cyclic_nat("F", 1, a);
            let beta = cyclic_nat("F", 1, b);
            let gamma = cyclic_nat("F", 1, c);
            let ba = vertical_compose_validated_nat_trans("ba", &alpha, &beta).unwrap();
            let cb = vertical_compose_validated_nat_trans("cb", &beta, &gamma).unwrap();
            let left = vertical_compose_validated_nat_trans("left", &ba, &gamma).unwrap();
            let right = vertical_compose_validated_nat_trans("right", &alpha, &cb).unwrap();
            assert_eq!(left.declared().components, right.declared().components);
            assert_eq!(
                vertical_compose_validated_nat_trans("unit_left", &id, &alpha)
                    .unwrap()
                    .declared()
                    .components,
                alpha.declared().components
            );
            assert_eq!(
                vertical_compose_validated_nat_trans("unit_right", &alpha, &id)
                    .unwrap()
                    .declared()
                    .components,
                alpha.declared().components
            );
        }
    }

    #[test]
    fn admitted_interchange_law_for_all_81_component_quadruples() {
        for code in 0..81 {
            let (a, b, c, d) = (code % 3, (code / 3) % 3, (code / 9) % 3, (code / 27) % 3);
            let alpha = cyclic_nat("F", 1, a);
            let alpha2 = cyclic_nat("F", 1, b);
            let beta = cyclic_nat("H", 1, c);
            let beta2 = cyclic_nat("H", 1, d);
            let av = vertical_compose_validated_nat_trans("av", &alpha, &alpha2).unwrap();
            let bv = vertical_compose_validated_nat_trans("bv", &beta, &beta2).unwrap();
            let left = horizontal_compose_validated_nat_trans("left", &av, &bv).unwrap();
            let first = horizontal_compose_validated_nat_trans("first", &alpha, &beta).unwrap();
            let second = horizontal_compose_validated_nat_trans("second", &alpha2, &beta2).unwrap();
            let right = vertical_compose_validated_nat_trans("right", &first, &second).unwrap();
            assert_eq!(left.declared().components, right.declared().components);
            assert_eq!(left.source_functor(), right.source_functor());
            assert_eq!(left.target_functor(), right.target_functor());
        }
    }

    #[test]
    fn checked_composition_refuses_equal_names_with_different_endpoint_data() {
        let alpha = cyclic_nat("F", 1, 0);
        let beta = cyclic_nat("F", 2, 0);
        assert!(matches!(
            vertical_compose_validated_nat_trans("bad", &alpha, &beta),
            Err(CompositionError::ContextMismatch { .. })
        ));
        let cat = cyclic_three();
        let mut other = cat.clone();
        other.add_identity("extra", "id_extra");
        other.set_composition("id_extra", "id_extra", "id_extra");
        let f = identity_functor(&other, "F");
        let checked = ValidatedFiniteFunctor::try_new(f, &other, &other).unwrap();
        let beta = identity_validated_nat_trans("beta", &checked).unwrap();
        assert!(matches!(
            horizontal_compose_validated_nat_trans("bad", &alpha, &beta),
            Err(CompositionError::ContextMismatch { .. })
        ));
    }

    #[test]
    fn missing_data_and_invalid_output_names_fail_closed() {
        let cat = cyclic_three();
        let f = multiplier("F", 1, &cat);
        let alpha = cyclic_nat("F", 1, 1);
        let beta = cyclic_nat("F", 1, 2);
        assert!(matches!(
            vertical_compose_validated_nat_trans("", &alpha, &beta),
            Err(CompositionError::Admission(_))
        ));
        let mut raw = alpha.declared().clone();
        raw.components.clear();
        assert!(matches!(
            vertical_compose_nat_trans("bad", &raw, beta.declared(), &cat, &cat),
            Err(CompositionError::Missing { .. })
        ));
        assert!(matches!(
            right_whisker_nat_trans("bad", &raw, &f),
            Err(CompositionError::Missing { .. })
        ));
        let mut broken = f.clone();
        broken.morphism_map.clear();
        assert!(matches!(
            left_whisker_nat_trans("bad", &broken, alpha.declared()),
            Err(CompositionError::Missing { .. })
        ));
        let mut no_identity = cat.clone();
        no_identity.identities.clear();
        assert!(matches!(
            identity_nat_trans("bad", &f, &no_identity),
            Err(CompositionError::Missing { .. })
        ));
        let mut no_composition = cat.clone();
        no_composition.compositions.clear();
        assert!(matches!(
            vertical_compose_nat_trans(
                "bad",
                alpha.declared(),
                beta.declared(),
                &cat,
                &no_composition
            ),
            Err(CompositionError::Undefined { .. })
        ));
    }

    #[test]
    fn raw_horizontal_composition_rejects_noncommuting_paths() {
        // All endomaps of {0,1}, composed by direct evaluation.
        let maps = [[0, 0], [0, 1], [1, 0], [1, 1]];
        let mut cat = DeclaredFiniteCategory::new("End2");
        for i in 0..4 {
            cat.add_morphism(&i.to_string(), "*", "*");
        }
        cat.set_identity("*", "1");
        for i in 0..4 {
            for j in 0..4 {
                let composite = [maps[j][maps[i][0]], maps[j][maps[i][1]]];
                let k = maps.iter().position(|m| *m == composite).unwrap();
                cat.set_composition(&i.to_string(), &j.to_string(), &k.to_string());
            }
        }
        let f = identity_functor(&cat, "F");
        let mut a = DeclaredFiniteNatTrans::new("a", "F", "F");
        let mut b = a.clone();
        a.set_component("*", "0");
        b.set_component("*", "2");
        assert!(matches!(
            horizontal_compose_nat_trans("bad", &a, &b, &f, &f, &f, &f, &cat),
            Err(CompositionError::Interchange { .. })
        ));
    }

    fn one_object_monoid() -> DeclaredFiniteCategory {
        let mut cat = DeclaredFiniteCategory::new("M");
        cat.add_morphism("id_A", "A", "A");
        cat.add_morphism("u", "A", "A");
        cat.add_morphism("v", "A", "A");
        cat.add_morphism("vu", "A", "A");
        cat.set_identity("A", "id_A");

        for morphism in ["id_A", "u", "v", "vu"] {
            cat.set_composition("id_A", morphism, morphism);
            cat.set_composition(morphism, "id_A", morphism);
        }
        cat.set_composition("u", "v", "vu");
        cat.set_composition("u", "vu", "vu");
        cat.set_composition("vu", "v", "vu");
        cat.set_composition("v", "u", "vu");
        cat.set_composition("v", "vu", "vu");
        cat.set_composition("vu", "u", "vu");
        cat.set_composition("vu", "vu", "vu");
        cat.set_composition("u", "u", "u");
        cat.set_composition("v", "v", "v");
        cat
    }

    fn renamed_identity_functor(
        name: &str,
        category: &DeclaredFiniteCategory,
    ) -> DeclaredFiniteFunctor {
        let mut functor = identity_functor(category, name);
        functor.name = name.into();
        functor
    }

    #[test]
    fn identity_nat_trans_uses_target_identities() {
        let category = one_object_monoid();
        let functor = renamed_identity_functor("F", &category);
        let nat = identity_nat_trans("id_F", &functor, &category).unwrap();
        assert_eq!(nat.component("A"), Some("id_A"));
    }

    #[test]
    fn vertical_composition_composes_components() {
        let category = one_object_monoid();
        let mut alpha = DeclaredFiniteNatTrans::new("alpha", "F", "G");
        alpha.set_component("A", "u");
        let mut beta = DeclaredFiniteNatTrans::new("beta", "G", "H");
        beta.set_component("A", "v");

        let composite =
            vertical_compose_nat_trans("beta_alpha", &alpha, &beta, &category, &category).unwrap();
        assert_eq!(composite.component("A"), Some("vu"));
    }

    #[test]
    fn whiskering_maps_components() {
        let category = one_object_monoid();
        let outer = renamed_identity_functor("H", &category);
        let mut alpha = DeclaredFiniteNatTrans::new("alpha", "F", "G");
        alpha.set_component("A", "u");

        let whiskered = left_whisker_nat_trans("H_alpha", &outer, &alpha).unwrap();
        assert_eq!(whiskered.component("A"), Some("u"));
    }

    #[test]
    fn horizontal_composition_uses_whiskered_component_path() {
        let category = one_object_monoid();
        let f = renamed_identity_functor("F", &category);
        let g = renamed_identity_functor("G", &category);
        let h = renamed_identity_functor("H", &category);
        let k = renamed_identity_functor("K", &category);

        let mut alpha = DeclaredFiniteNatTrans::new("alpha", "F", "G");
        alpha.set_component("A", "u");
        let mut beta = DeclaredFiniteNatTrans::new("beta", "H", "K");
        beta.set_component("A", "v");

        let composite = horizontal_compose_nat_trans(
            "beta_star_alpha",
            &alpha,
            &beta,
            &f,
            &g,
            &h,
            &k,
            &category,
        )
        .unwrap();
        assert_eq!(composite.component("A"), Some("vu"));
    }
}
