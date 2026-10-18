//! Kleisli Category Construction — Spec Section 23.
//!
//! Given a finite category C and a finite monad T on C, the Kleisli category
//! C_T has:
//! - Objects: Same as C.
//! - Morphisms A → B: Morphisms A → T(B) in C.
//! - Identity on A: The monad unit η_A : A → T(A).
//! - Composition of f : A → T(B) and g : B → T(C):
//!   Defined as μ_C ∘ T(g) ∘ f.
//!
//! This module provides two entry points following the Declared → Validated
//! discipline:
//!
//! - `declare_kleisli_category`: builds raw `DeclaredFiniteCategory` from
//!   unvalidated monad data. The caller is responsible for validation.
//!
//! - `build_validated_kleisli_category`: accepts a `ValidatedFiniteCategory`
//!   and `ValidatedFiniteMonad`, constructs the Kleisli category, and returns
//!   a `ValidatedFiniteCategory` on success.

use super::finite_category::{DeclaredFiniteCategory, ValidatedFiniteCategory};
use super::finite_category_builder::DeclaredFiniteCategoryBuilder;
use super::legacy_monad::{DeclaredFiniteMonad, ValidatedFiniteMonad};
use super::nerve::DeclaredNerve;
use std::collections::BTreeMap;

/// A wrapper that owns a validated Kleisli category and provides a safe,
/// lifetime-free construction path for its nerve.
#[derive(Debug, Clone)]
pub struct KleisliNerve {
    pub kleisli_category: ValidatedFiniteCategory,
}

impl KleisliNerve {
    pub fn try_new(
        name: &str,
        category: &ValidatedFiniteCategory,
        monad: &ValidatedFiniteMonad,
    ) -> Result<Self, String> {
        let kleisli_category = build_validated_kleisli_category(name, category, monad)?;
        Ok(Self { kleisli_category })
    }

    pub fn nerve(&self) -> DeclaredNerve<'_> {
        DeclaredNerve::new(self.kleisli_category.declared())
    }
}

/// Internal record tracking the correspondence between a Kleisli morphism
/// and its underlying base-category morphism.
#[derive(Debug, Clone, PartialEq, Eq)]
struct KleisliMorphism {
    k_name: String,
    orig_name: String,
    source: String,
    target: String,
}

/// Constructs a Kleisli category declaration from raw (unvalidated) inputs.
///
/// Returns a `DeclaredFiniteCategory` whose composition table is derived
/// from the monad's unit, multiplication, and functor action. The result
/// is **not** validated; use `build_validated_kleisli_category` if you
/// need a trust-boundary–enforced output.
///
/// Kleisli morphism names use the delimiter format `K[f=>B]` to avoid
/// collisions when morphism or object names contain underscores.
pub fn declare_kleisli_category(
    name: &str,
    category: &DeclaredFiniteCategory,
    monad: &DeclaredFiniteMonad,
) -> Result<DeclaredFiniteCategory, String> {
    let mut builder = DeclaredFiniteCategoryBuilder::new(name);

    // 1. Objects: Ob(C_T) = Ob(C).
    for obj in &category.objects {
        builder = builder.object(obj);
    }

    let mut k_morphisms: Vec<KleisliMorphism> = Vec::new();
    let mut orig_to_k: BTreeMap<(String, String), String> = BTreeMap::new();

    // 2. Morphisms: For every f : A → T(B) in C, create K[f=>B] : A → B in C_T.
    for f in category.morphisms.values() {
        for (b, tb) in &monad.object_map {
            if tb == &f.target {
                let k_name = format!("K[{}=>{}]", f.name, b);

                // Detect name collisions (impossible with bracket delimiters
                // but guarded for defense-in-depth).
                if orig_to_k.values().any(|existing| existing == &k_name) {
                    return Err(format!("Kleisli morphism name collision: {}", k_name));
                }

                builder = builder.morphism(&k_name, &f.source, b);
                k_morphisms.push(KleisliMorphism {
                    k_name: k_name.clone(),
                    orig_name: f.name.clone(),
                    source: f.source.clone(),
                    target: b.clone(),
                });
                orig_to_k.insert((f.name.clone(), b.clone()), k_name);
            }
        }
    }

    // 3. Identities: The identity on A in Kleisli is η_A : A → T(A).
    for a in &category.objects {
        let eta_a = monad
            .unit_components
            .get(a)
            .ok_or_else(|| format!("Monad missing unit for object {}", a))?;

        let k_name = orig_to_k.get(&(eta_a.clone(), a.clone())).ok_or_else(|| {
            format!(
                "Unit {} for {} not found as a valid Kleisli morphism",
                eta_a, a
            )
        })?;

        builder = builder.identity(a, k_name);
    }

    // 4. Composition: f_K : A → B, g_K : B → C
    //    Their Kleisli composite is h_K : A → C where h = μ_C ∘ T(g) ∘ f.
    for f_k in &k_morphisms {
        for g_k in &k_morphisms {
            if f_k.target != g_k.source {
                continue;
            }
            let c = &g_k.target;

            // Step 1: T(g) — apply the monad's functor action to g.
            let tg = monad
                .morphism_map
                .get(&g_k.orig_name)
                .ok_or_else(|| format!("Monad missing T({})", g_k.orig_name))?;

            // Step 2: T(g) ∘ f in the base category.
            let step1 = category.compose(&f_k.orig_name, tg).ok_or_else(|| {
                format!(
                    "Base category missing composition {} ∘ {}",
                    tg, f_k.orig_name
                )
            })?;

            // Step 3: μ_C — the monad multiplication at C.
            let mu_c = monad
                .multiplication_components
                .get(c)
                .ok_or_else(|| format!("Monad missing μ_{}", c))?;

            // Step 4: h = μ_C ∘ (T(g) ∘ f) in the base category.
            let h_orig = category
                .compose(step1, mu_c)
                .ok_or_else(|| format!("Base category missing composition {} ∘ {}", mu_c, step1))?;

            // Map the resulting base morphism back to the Kleisli name.
            let h_k_name = orig_to_k
                .get(&(h_orig.to_string(), c.clone()))
                .ok_or_else(|| {
                    format!(
                        "Resulting morphism {} → T({}) not found in Kleisli morphisms",
                        h_orig, c
                    )
                })?;

            builder = builder.composition(&f_k.k_name, &g_k.k_name, h_k_name);
        }
    }

    Ok(builder.build())
}

/// Constructs and validates a Kleisli category from pre-validated inputs.
///
/// Accepts a `ValidatedFiniteCategory` and `ValidatedFiniteMonad`, builds
/// the Kleisli declaration, then validates the result as a finite category.
/// This enforces the full trust chain:
///
/// ```text
/// ValidatedFiniteCategory + ValidatedFiniteMonad
///   → DeclaredFiniteCategory (Kleisli)
///   → ValidatedFiniteCategory (Kleisli)
/// ```
pub fn build_validated_kleisli_category(
    name: &str,
    category: &ValidatedFiniteCategory,
    monad: &ValidatedFiniteMonad,
) -> Result<ValidatedFiniteCategory, String> {
    let declared = declare_kleisli_category(name, category.declared(), monad.declared())?;
    ValidatedFiniteCategory::try_new(declared).map_err(|report| {
        format!(
            "Kleisli category failed validation: {:?}",
            report.typed_violations
        )
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_declare_kleisli_identity_monad() {
        // Build base category C with just object A and id_A
        let cat = DeclaredFiniteCategoryBuilder::new("C")
            .identity_object("A")
            .identity_compositions()
            .build();

        // Build identity monad: T = id, η = id, μ = id
        let mut m = DeclaredFiniteMonad::new("Id", "C");
        m.set_object_map("A", "A");
        m.set_morphism_map("id_A", "id_A");
        m.set_unit("A", "id_A");
        m.set_multiply("A", "id_A");

        let kleisli =
            declare_kleisli_category("K(C)", &cat, &m).expect("Should build Kleisli category");

        assert_eq!(kleisli.name, "K(C)");
        assert!(kleisli.has_object("A"));

        // Kleisli should have exactly one morphism K[id_A=>A]
        let k_id = "K[id_A=>A]";
        assert!(kleisli.has_morphism(k_id));
        assert_eq!(kleisli.identity_of("A").unwrap(), k_id);

        // Check composition: k_id ∘ k_id = k_id
        assert_eq!(kleisli.compose(k_id, k_id).unwrap(), k_id);
    }

    /// Non-trivial test: walking arrow A → B with identity monad.
    ///
    /// Base category: {A, B}, morphisms {id_A, id_B, f : A → B}.
    /// Identity monad: T = id on all.
    ///
    /// Expected Kleisli morphisms:
    ///   K[id_A=>A] : A → A  (identity on A)
    ///   K[id_B=>B] : B → B  (identity on B)
    ///   K[f=>B]    : A → B
    ///
    /// Expected composition:
    ///   K[id_A=>A] ∘ K[f=>B] = K[f=>B]
    ///   K[f=>B] ∘ K[id_B=>B] = K[f=>B]
    #[test]
    fn test_kleisli_walking_arrow_with_identity_monad() {
        let cat = DeclaredFiniteCategoryBuilder::new("WalkingArrow")
            .identity_object("A")
            .identity_object("B")
            .morphism("f", "A", "B")
            .identity_compositions()
            .composition("id_A", "f", "f")
            .composition("f", "id_B", "f")
            .build();

        let mut m = DeclaredFiniteMonad::new("Id", "WalkingArrow");
        m.set_object_map("A", "A");
        m.set_object_map("B", "B");
        m.set_morphism_map("id_A", "id_A");
        m.set_morphism_map("id_B", "id_B");
        m.set_morphism_map("f", "f");
        m.set_unit("A", "id_A");
        m.set_unit("B", "id_B");
        m.set_multiply("A", "id_A");
        m.set_multiply("B", "id_B");

        let kleisli = declare_kleisli_category("K(WA)", &cat, &m)
            .expect("Should build walking arrow Kleisli");

        assert!(kleisli.has_object("A"));
        assert!(kleisli.has_object("B"));

        let k_f = "K[f=>B]";
        let k_id_a = "K[id_A=>A]";
        let k_id_b = "K[id_B=>B]";

        assert!(kleisli.has_morphism(k_f));
        assert!(kleisli.has_morphism(k_id_a));
        assert!(kleisli.has_morphism(k_id_b));

        // Identity compositions
        assert_eq!(kleisli.compose(k_id_a, k_f).unwrap(), k_f);
        assert_eq!(kleisli.compose(k_f, k_id_b).unwrap(), k_f);

        // Identity self-composition
        assert_eq!(kleisli.compose(k_id_a, k_id_a).unwrap(), k_id_a);
        assert_eq!(kleisli.compose(k_id_b, k_id_b).unwrap(), k_id_b);
    }

    #[test]
    fn test_validated_kleisli_from_validated_inputs() {
        let cat = DeclaredFiniteCategoryBuilder::new("C")
            .identity_object("A")
            .identity_compositions()
            .build_validated()
            .expect("Base category should validate");

        let mut m = DeclaredFiniteMonad::new("Id", "C");
        m.set_object_map("A", "A");
        m.set_morphism_map("id_A", "id_A");
        m.set_unit("A", "id_A");
        m.set_multiply("A", "id_A");

        let validated_monad = ValidatedFiniteMonad::try_new(m, cat.declared())
            .expect("Identity monad should validate");

        let validated_kleisli = build_validated_kleisli_category("K(C)", &cat, &validated_monad)
            .expect("Validated Kleisli should succeed");

        assert_eq!(validated_kleisli.declared().name, "K(C)");
        assert!(validated_kleisli.declared().has_object("A"));
    }

    #[test]
    fn test_nerve_of_kleisli_walking_arrow_identity_monad() {
        use super::super::nerve::Simplex;

        let cat = DeclaredFiniteCategoryBuilder::new("WalkingArrow")
            .identity_object("A")
            .identity_object("B")
            .morphism("f", "A", "B")
            .identity_compositions()
            .composition("id_A", "f", "f")
            .composition("f", "id_B", "f")
            .build();

        let mut m = DeclaredFiniteMonad::new("Id", "WalkingArrow");
        m.set_object_map("A", "A");
        m.set_object_map("B", "B");
        m.set_morphism_map("id_A", "id_A");
        m.set_morphism_map("id_B", "id_B");
        m.set_morphism_map("f", "f");
        m.set_unit("A", "id_A");
        m.set_unit("B", "id_B");
        m.set_multiply("A", "id_A");
        m.set_multiply("B", "id_B");

        let kleisli =
            declare_kleisli_category("K(WA)", &cat, &m).expect("Kleisli category should build");

        let nerve = DeclaredNerve::new(&kleisli);

        assert_eq!(nerve.n_simplices(0).len(), 2);
        assert_eq!(nerve.n_simplices(1).len(), 3);

        let nondegenerate_1 = nerve.nondegenerate_n_simplices(1);
        assert_eq!(
            nondegenerate_1,
            vec![Simplex::Chain(vec!["K[f=>B]".into()])]
        );
    }
}
