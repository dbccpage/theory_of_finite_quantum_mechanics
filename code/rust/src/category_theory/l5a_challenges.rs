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
