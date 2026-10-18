#![cfg(any())]
// TODO: Fix imports from legacy arithmos
//! Composition and whiskering for declared finite natural transformations.

use super::cat_functor::DeclaredFiniteFunctor;
use super::finite_category::DeclaredFiniteCategory;
use super::natural_trans::DeclaredFiniteNatTrans;

fn composite_name(outer: &str, inner: &str) -> String {
    format!("Comp[{} after {}]", outer, inner)
}

pub fn identity_nat_trans(
    name: &str,
    functor: &DeclaredFiniteFunctor,
    target_category: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteNatTrans, String> {
    let mut nat = DeclaredFiniteNatTrans::new(name, &functor.name, &functor.name);

    for (source_object, target_object) in &functor.object_map {
        let Some(identity) = target_category.identity_of(target_object) else {
            return Err(format!(
                "Cannot build identity natural transformation: {} has no identity in {}",
                target_object, target_category.name
            ));
        };
        nat.set_component(source_object, identity);
    }

    Ok(nat)
}

/// Vertical composition beta after alpha.
pub fn vertical_compose_nat_trans(
    name: &str,
    alpha: &DeclaredFiniteNatTrans,
    beta: &DeclaredFiniteNatTrans,
    source_category: &DeclaredFiniteCategory,
    target_category: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteNatTrans, String> {
    if alpha.target_functor != beta.source_functor {
        return Err(format!(
            "Cannot vertically compose {} then {}: target functor {} does not match source functor {}",
            alpha.name, beta.name, alpha.target_functor, beta.source_functor
        ));
    }

    let mut composite =
        DeclaredFiniteNatTrans::new(name, &alpha.source_functor, &beta.target_functor);

    for object in &source_category.objects {
        let Some(alpha_component) = alpha.component(object) else {
            return Err(format!("{} has no component at {}", alpha.name, object));
        };
        let Some(beta_component) = beta.component(object) else {
            return Err(format!("{} has no component at {}", beta.name, object));
        };
        let Some(composed) = target_category.compose(alpha_component, beta_component) else {
            return Err(format!(
                "Target composition {} after {} is undefined at {}",
                beta_component, alpha_component, object
            ));
        };
        composite.set_component(object, composed);
    }

    Ok(composite)
}

/// Left whiskering: H alpha : H F => H G.
pub fn left_whisker_nat_trans(
    name: &str,
    outer: &DeclaredFiniteFunctor,
    alpha: &DeclaredFiniteNatTrans,
) -> Result<DeclaredFiniteNatTrans, String> {
    let source_name = composite_name(&outer.name, &alpha.source_functor);
    let target_name = composite_name(&outer.name, &alpha.target_functor);
    let mut whiskered = DeclaredFiniteNatTrans::new(name, &source_name, &target_name);

    for (object, component) in &alpha.components {
        let Some(mapped_component) = outer.on_morphism(component) else {
            return Err(format!(
                "{} does not map component {} of {}",
                outer.name, component, alpha.name
            ));
        };
        whiskered.set_component(object, mapped_component);
    }

    Ok(whiskered)
}

/// Right whiskering: alpha K : F K => G K.
pub fn right_whisker_nat_trans(
    name: &str,
    alpha: &DeclaredFiniteNatTrans,
    inner: &DeclaredFiniteFunctor,
) -> Result<DeclaredFiniteNatTrans, String> {
    let source_name = composite_name(&alpha.source_functor, &inner.name);
    let target_name = composite_name(&alpha.target_functor, &inner.name);
    let mut whiskered = DeclaredFiniteNatTrans::new(name, &source_name, &target_name);

    for object in inner.object_map.keys() {
        let Some(middle_object) = inner.on_object(object) else {
            return Err(format!("{} does not map object {}", inner.name, object));
        };
        let Some(component) = alpha.component(middle_object) else {
            return Err(format!(
                "{} has no component at {} = {}({})",
                alpha.name, middle_object, inner.name, object
            ));
        };
        whiskered.set_component(object, component);
    }

    Ok(whiskered)
}

/// Horizontal composition beta star alpha:
/// if alpha : F => G and beta : H => K, then beta star alpha : H F => K G.
pub fn horizontal_compose_nat_trans(
    name: &str,
    alpha: &DeclaredFiniteNatTrans,
    beta: &DeclaredFiniteNatTrans,
    f: &DeclaredFiniteFunctor,
    g: &DeclaredFiniteFunctor,
    h: &DeclaredFiniteFunctor,
    k: &DeclaredFiniteFunctor,
    target_category: &DeclaredFiniteCategory,
) -> Result<DeclaredFiniteNatTrans, String> {
    if alpha.source_functor != f.name || alpha.target_functor != g.name {
        return Err(format!(
            "{} must be a transformation {} => {}, got {} => {}",
            alpha.name, f.name, g.name, alpha.source_functor, alpha.target_functor
        ));
    }
    if beta.source_functor != h.name || beta.target_functor != k.name {
        return Err(format!(
            "{} must be a transformation {} => {}, got {} => {}",
            beta.name, h.name, k.name, beta.source_functor, beta.target_functor
        ));
    }

    if f.target_category != h.source_category {
        return Err(format!(
            "Cannot form H∘F: {} targets {}, but {} sources {}",
            f.name, f.target_category, h.name, h.source_category
        ));
    }
    if g.target_category != k.source_category {
        return Err(format!(
            "Cannot form K∘G: {} targets {}, but {} sources {}",
            g.name, g.target_category, k.name, k.source_category
        ));
    }
    if f.source_category != g.source_category {
        return Err(format!(
            "F and G source categories do not match: {} != {}",
            f.source_category, g.source_category
        ));
    }
    if h.source_category != k.source_category {
        return Err(format!(
            "H and K source categories do not match: {} != {}",
            h.source_category, k.source_category
        ));
    }
    if h.target_category != k.target_category {
        return Err(format!(
            "H and K target categories do not match: {} != {}",
            h.target_category, k.target_category
        ));
    }

    let source_name = composite_name(&h.name, &f.name);
    let target_name = composite_name(&k.name, &g.name);
    let mut composite = DeclaredFiniteNatTrans::new(name, &source_name, &target_name);

    for object in f.object_map.keys() {
        let alpha_component = alpha
            .component(object)
            .ok_or_else(|| format!("{} has no component at {}", alpha.name, object))?;

        let h_alpha = h
            .on_morphism(alpha_component)
            .ok_or_else(|| format!("{} does not map {}", h.name, alpha_component))?;

        let g_object = g
            .on_object(object)
            .ok_or_else(|| format!("{} does not map object {}", g.name, object))?;

        let beta_at_g_object = beta.component(g_object).ok_or_else(|| {
            format!(
                "{} has no component at {} = {}({})",
                beta.name, g_object, g.name, object
            )
        })?;

        let left_path = target_category
            .compose(h_alpha, beta_at_g_object)
            .ok_or_else(|| {
                format!(
                    "Horizontal composite path {} after {} is undefined at {}",
                    beta_at_g_object, h_alpha, object
                )
            })?;

        let f_object = f
            .on_object(object)
            .ok_or_else(|| format!("{} does not map object {}", f.name, object))?;

        let k_alpha = k
            .on_morphism(alpha_component)
            .ok_or_else(|| format!("{} does not map {}", k.name, alpha_component))?;

        let beta_at_f_object = beta.component(f_object).ok_or_else(|| {
            format!(
                "{} has no component at {} = {}({})",
                beta.name, f_object, f.name, object
            )
        })?;

        let right_path = target_category
            .compose(beta_at_f_object, k_alpha)
            .ok_or_else(|| {
                format!(
                    "Horizontal composite path {} after {} is undefined at {}",
                    k_alpha, beta_at_f_object, object
                )
            })?;

        if left_path != right_path {
            return Err(format!(
                "Horizontal composition paths disagree at {}: left {}, right {}",
                object, left_path, right_path
            ));
        }

        composite.set_component(object, left_path);
    }

    Ok(composite)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::arithmos::functors::cat_functor::DeclaredFiniteFunctor;
    use crate::arithmos::functors::functor_composition::identity_functor;

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
