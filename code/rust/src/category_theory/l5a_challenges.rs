//! Finite independent oracles and hostile admission fixtures. AuthorityEffect: None.

use crate::cat_functor::{
    Category, DeclaredFiniteFunctor, FunctorAdmissionError, ValidatedFiniteFunctor,
};
use crate::finite_category::{DeclaredFiniteCategory, ValidatedFiniteCategory};
use crate::finite_category_builder::DeclaredFiniteCategoryBuilder;
use crate::foundations::finite_set::{FiniteSet, ValidatedFiniteSet};

fn cyclic(n: usize) -> ValidatedFiniteCategory {
    let mut c = DeclaredFiniteCategory::new(&format!("C{n}"));
    for a in 0..n {
        c.add_morphism(&a.to_string(), "*", "*");
    }
    c.set_identity("*", "0");
    for a in 0..n {
        for b in 0..n {
            c.set_composition(&a.to_string(), &b.to_string(), &((a + b) % n).to_string());
        }
    }
    ValidatedFiniteCategory::try_new(c).unwrap()
}

fn map_c3_c2(values: [usize; 3]) -> DeclaredFiniteFunctor {
    let mut f = DeclaredFiniteFunctor::new("F", "C3", "C2");
    f.map_object("*", "*");
    for (a, b) in values.iter().enumerate() {
        f.map_morphism(&a.to_string(), &b.to_string());
    }
    f
}

#[test]
fn finite_functor_admission_matches_all_eight_c3_c2_maps() {
    let c3 = cyclic(3);
    let c2 = cyclic(2);
    for bits in 0..8 {
        let values = [bits & 1, (bits >> 1) & 1, (bits >> 2) & 1];
        // A map of cyclic groups is a homomorphism exactly when it maps 0 to 0
        // and its values are multiples of the chosen generator image.
        let expected =
            values[0] == 0 && values[2] == (2 * values[1]) % 2 && (3 * values[1]) % 2 == 0;
        let admitted = ValidatedFiniteFunctor::try_new(map_c3_c2(values), c3.clone(), c2.clone());
        assert_eq!(admitted.is_ok(), expected, "map {values:?}");
    }
}

#[test]
fn functor_rejects_each_mapping_and_binding_failure() {
    let c3 = cyclic(3);
    let c2 = cyclic(2);
    let valid = map_c3_c2([0, 0, 0]);
    let mut f = valid.clone();
    f.name.clear();
    assert_eq!(
        ValidatedFiniteFunctor::try_new(f, c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::Name)
    );
    let mut f = valid.clone();
    f.target_category = "wrong".into();
    assert_eq!(
        ValidatedFiniteFunctor::try_new(f, c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::CategoryBinding)
    );
    let mut f = valid.clone();
    f.object_map.clear();
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(f, c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::MappingDomain { .. })
    ));
    let mut f = valid.clone();
    f.map_morphism("extra", "0");
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(f, c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::MappingDomain { .. })
    ));
    let mut f = valid.clone();
    f.map_object("*", "unknown");
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(f, c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::UnknownImage { .. })
    ));
    let mut f = valid.clone();
    f.map_morphism("1", "unknown");
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(f, c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::UnknownImage { .. })
    ));
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(map_c3_c2([1, 0, 0]), c3.clone(), c2.clone()),
        Err(FunctorAdmissionError::Identity { .. })
    ));
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(map_c3_c2([0, 1, 0]), c3, c2),
        Err(FunctorAdmissionError::Composition { .. })
    ));
}

#[test]
fn category_lookup_rejects_outside_members_and_mutated_declarations() {
    let c = DeclaredFiniteCategoryBuilder::walking_arrow("C", "A", "B", "f")
        .build_validated()
        .unwrap();
    assert_eq!(c.id(&"unknown".into()), None);
    assert_eq!(c.src(&"unknown".into()), None);
    assert_eq!(c.tgt(&"unknown".into()), None);
    assert_eq!(c.compose(&"f".into(), &"f".into()), None);
    let mut forged = c.clone().into_declared();
    forged.compositions.clear();
    assert!(ValidatedFiniteCategory::try_new(forged).is_err());
    assert_eq!(c.id(&"A".into()), Some("id_A".into()));
    assert!(ValidatedFiniteCategory::try_new(DeclaredFiniteCategory::new("  ")).is_err());
}

#[test]
fn functor_boundary_is_checked_before_composition() {
    let c = DeclaredFiniteCategoryBuilder::walking_arrow("C", "A", "B", "f")
        .build_validated()
        .unwrap();
    let mut f = DeclaredFiniteFunctor::new("bad", "C", "C");
    for x in ["A", "B"] {
        f.map_object(x, x);
    }
    for x in ["id_A", "id_B"] {
        f.map_morphism(x, x);
    }
    f.map_morphism("f", "id_A");
    assert!(matches!(
        ValidatedFiniteFunctor::try_new(f, c.clone(), c),
        Err(FunctorAdmissionError::Boundary { .. })
    ));
}

#[test]
fn finite_set_admission_rejects_duplicates_and_replays_serde() {
    let duplicate = FiniteSet::with_elements("S", vec!["a".into(), "a".into()]);
    assert!(ValidatedFiniteSet::try_from(duplicate).is_err());
    let valid =
        ValidatedFiniteSet::try_from(FiniteSet::with_elements("S", vec!["a".into()])).unwrap();
    let mut raw = FiniteSet::from(valid.clone());
    raw.declared_cardinality = Some(2);
    assert!(ValidatedFiniteSet::try_from(raw).is_err());
    assert_eq!(valid.cardinality(), 1);
    assert!(valid.contains("a"));
    assert!(!valid.contains("missing"));
}

#[test]
fn exact_weight_accumulation_has_no_fixed_width_ceiling_or_float_rounding() {
    use crate::finite_profunctor::DeclaredFiniteWeightedProfunctor;
    use num_rational::BigRational as Q;
    use num_traits::Zero;
    let mut p = DeclaredFiniteWeightedProfunctor::new("P", "C", "D");
    for _ in 0..10 {
        p.add_weighted_witness("a", "b", "w", Q::new(1.into(), 10.into()))
            .unwrap();
    }
    assert_eq!(p.total_weight("a", "b"), Q::from_integer(1.into()));
    let before = p.clone();
    assert!(p
        .add_weighted_witness("a", "b", "bad", Q::new_raw(1.into(), 0.into()))
        .is_err());
    assert!(p
        .add_weighted_witness("a", "b", "bad", Q::from_integer((-1).into()))
        .is_err());
    assert_eq!(p, before);
    assert_eq!(p.total_weight("a", "missing"), Q::zero());
}

#[test]
fn scalar_density_metadata_rejects_invalid_domains() {
    use crate::density_matrix_functor::DensityMatrixFunctorWitness as W;
    use num_rational::BigRational as Q;
    assert!(W::new("", Q::from_integer(1.into())).is_err());
    assert!(W::new("x", Q::from_integer((-1).into())).is_err());
    assert!(W::new("x", Q::new_raw(1.into(), 0.into())).is_err());
    assert_eq!(
        W::new("x", Q::new(1.into(), 3.into()))
            .unwrap()
            .rank_one_weight(),
        &Q::new(1.into(), 3.into())
    );
}

#[cfg(test)]
mod category_admission {
    use super::*;
    use crate::finite_category_validation::validate_finite_category;
    use crate::validation::{FiniteCategoryValidation as Unit, ValidationUnit};

    fn walking() -> DeclaredFiniteCategory {
        DeclaredFiniteCategoryBuilder::walking_arrow("Walking", "A", "B", "f").build()
    }

    fn rejected(category: DeclaredFiniteCategory, unit: Unit) {
        let before = category.clone();
        let report = validate_finite_category(&category);
        assert_eq!(category, before, "diagnostics modified the candidate");
        assert_eq!(report.results.len(), 8, "missing checker phase");
        assert!(!report.all_passed());
        assert!(
            report
                .typed_violations
                .iter()
                .any(|v| v.unit == ValidationUnit::FiniteCategory(unit)),
            "missing {unit:?}: {:?}",
            report.typed_violations
        );
        assert!(ValidatedFiniteCategory::try_new(category).is_err());
    }

    #[test]
    fn name_and_object_reference_failures_are_reported_and_refused() {
        let mut c = walking();
        c.name = " \t".into();
        rejected(c, Unit::ObjectReference);
        let mut c = walking();
        c.objects.insert("\n".into());
        rejected(c, Unit::ObjectReference);
        let mut c = walking();
        c.add_morphism(" ", "A", "B");
        rejected(c, Unit::MorphismBoundary);
        let mut c = walking();
        c.morphisms.get_mut("f").unwrap().name = "alias".into();
        rejected(c, Unit::ObjectReference);
        let mut c = walking();
        c.morphisms.get_mut("f").unwrap().source = "outside".into();
        rejected(c, Unit::ObjectReference);
        let mut c = walking();
        c.morphisms.get_mut("f").unwrap().target = "outside".into();
        rejected(c, Unit::ObjectReference);
        let mut c = walking();
        c.identities.insert("outside".into(), "id_A".into());
        rejected(c, Unit::ObjectReference);
    }

    #[test]
    fn identity_domain_boundary_and_each_unit_law_failure_are_refused() {
        let mut c = walking();
        c.identities.remove("A");
        rejected(c, Unit::IdentityTotality);
        let mut c = walking();
        c.identities.insert("A".into(), "outside".into());
        rejected(c, Unit::IdentityTotality);
        for object in ["A", "B"] {
            let mut c = walking();
            c.identities.insert(object.into(), "f".into());
            rejected(c, Unit::IdentityTotality);
        }
        for (first, second) in [("id_A", "f"), ("f", "id_B")] {
            let mut c = walking();
            c.compositions.remove(&(first.into(), second.into()));
            rejected(c, Unit::IdentityLaw);
            let mut c = walking();
            c.set_composition(first, second, "id_A");
            rejected(c, Unit::IdentityLaw);
        }
    }

    #[test]
    fn composition_domain_closure_boundary_and_undefined_associativity_are_refused() {
        let mut c = walking();
        c.compositions.remove(&("f".into(), "id_B".into()));
        rejected(c.clone(), Unit::CompositionTotality);
        rejected(c, Unit::Associativity);
        for (first, second, result) in [
            ("outside", "id_A", "id_A"),
            ("id_A", "outside", "id_A"),
            ("id_A", "id_A", "outside"),
        ] {
            let mut c = walking();
            c.set_composition(first, second, result);
            rejected(c, Unit::CompositionClosure);
        }
        let mut c = walking();
        c.set_composition("f", "f", "f");
        rejected(c, Unit::CompositionBoundary);
        let mut c = walking();
        c.set_composition("id_A", "f", "id_A");
        rejected(c, Unit::CompositionBoundary);
    }

    type Matrix = [[u8; 3]; 3];
    fn product(a: &Matrix, b: &Matrix) -> Matrix {
        std::array::from_fn(|i| std::array::from_fn(|j| (0..3).map(|k| a[i][k] * b[k][j]).sum()))
    }

    /// Regular left actions on a three-dimensional free module. Matrix closure
    /// means L_(a*b) = L_a L_b. Delta columns recover every action value, giving
    /// an independent linear-algebra characterization of associativity.
    fn matrix_oracle(table: &[[usize; 3]; 3]) -> bool {
        let actions: [Matrix; 3] = std::array::from_fn(|a| {
            std::array::from_fn(|target| std::array::from_fn(|x| u8::from(table[a][x] == target)))
        });
        (0..3).all(|a| (0..3).all(|b| product(&actions[a], &actions[b]) == actions[table[a][b]]))
    }

    fn one_object(table: &[[usize; 3]; 3]) -> DeclaredFiniteCategory {
        let mut c = DeclaredFiniteCategory::new("three-arrow monoid");
        for a in 0..3 {
            c.add_morphism(&a.to_string(), "*", "*");
        }
        c.set_identity("*", "0");
        for (a, row) in table.iter().enumerate() {
            for (b, result) in row.iter().enumerate() {
                c.set_composition(&a.to_string(), &b.to_string(), &result.to_string());
            }
        }
        c
    }

    #[test]
    fn all_81_unital_three_arrow_tables_agree_with_regular_matrix_actions() {
        let mut accepted = 0;
        for code in 0..81 {
            let table = [
                [0, 1, 2],
                [1, code % 3, (code / 3) % 3],
                [2, (code / 9) % 3, (code / 27) % 3],
            ];
            let expected = matrix_oracle(&table);
            let result = ValidatedFiniteCategory::try_new(one_object(&table));
            assert_eq!(result.is_ok(), expected, "table {table:?}");
            accepted += usize::from(expected);
        }
        assert!(
            accepted > 0 && accepted < 81,
            "oracle challenge was vacuous"
        );
    }

    #[test]
    fn empty_category_and_owned_certificates_keep_their_exact_domains() {
        let empty = ValidatedFiniteCategory::try_new(DeclaredFiniteCategory::new("Empty")).unwrap();
        assert_eq!(empty.id(&"outside".into()), None);
        assert_eq!(empty.compose(&"outside".into(), &"outside".into()), None);
        let category = ValidatedFiniteCategory::try_new(walking()).unwrap();
        let saved = category.clone();
        let mut declaration = category.clone().into_declared();
        declaration.morphisms.clear();
        declaration.compositions.clear();
        assert!(ValidatedFiniteCategory::try_new(declaration).is_err());
        assert_eq!(category, saved);
        assert_eq!(category.id(&"outside".into()), None);
        assert_eq!(category.src(&"outside".into()), None);
        assert_eq!(category.tgt(&"outside".into()), None);
        assert_eq!(category.compose(&"id_A".into(), &"outside".into()), None);
        assert_eq!(category.compose(&"f".into(), &"f".into()), None);
        assert_eq!(
            category.compose(&"id_A".into(), &"f".into()),
            Some("f".into())
        );
    }
}
