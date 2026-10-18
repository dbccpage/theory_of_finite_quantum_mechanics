// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

use finite_qm_native::campaigns::causal_order::*;
use omega_homology::finite_poset::FinitePoset;
use omega_homology::poset_census::labelled_posets;
use std::collections::HashMap;

#[test]
fn test_c1_cross_language_parity() {
    let c1 = construct_c1();
    assert_eq!(c1.size(), 3);
    assert_eq!(c1.incomparable_pairs(), vec![(1, 2)]);
    let mu = c1.mobius();
    assert_eq!(mu.get(0, 0).unwrap(), &num_bigint::BigInt::from(1));
    assert_eq!(mu.get(0, 1).unwrap(), &num_bigint::BigInt::from(-1));
    assert_eq!(mu.get(0, 2).unwrap(), &num_bigint::BigInt::from(-1));
    assert_eq!(mu.get(1, 2).unwrap(), &num_bigint::BigInt::from(0));
}

#[test]
fn test_c2_cross_language_parity() {
    let c2 = construct_c2();
    assert_eq!(c2.size(), 4);
    assert_eq!(c2.incomparable_pairs(), vec![(1, 2)]);
    assert_eq!(c2.interval(0, 3).unwrap().len(), 4);
    let mu = c2.mobius();
    assert_eq!(mu.get(0, 0).unwrap(), &num_bigint::BigInt::from(1));
    assert_eq!(mu.get(0, 1).unwrap(), &num_bigint::BigInt::from(-1));
    assert_eq!(mu.get(0, 2).unwrap(), &num_bigint::BigInt::from(-1));
    assert_eq!(mu.get(0, 3).unwrap(), &num_bigint::BigInt::from(1));
}

#[test]
fn test_census_parity() {
    let p3 = labelled_posets(3).unwrap();
    assert_eq!(p3.len(), 19);
    let c3 = census_unlabeled(3).unwrap();
    assert_eq!(c3.len(), 5);
    let sl3 = c3
        .values()
        .filter(|m| !m[0].incomparable_pairs().is_empty())
        .count();
    assert_eq!(sl3, 4);

    let p4 = labelled_posets(4).unwrap();
    assert_eq!(p4.len(), 219);
    let c4 = census_unlabeled(4).unwrap();
    assert_eq!(c4.len(), 16);
    let sl4 = c4
        .values()
        .filter(|m| !m[0].incomparable_pairs().is_empty())
        .count();
    assert_eq!(sl4, 15);

    // Combined at bound n in {3, 4}
    assert_eq!(c3.len() + c4.len(), 21);
    assert_eq!(sl3 + sl4, 19);
}

#[test]
fn test_t817_negative_controls() {
    // 1. Scalar as causal has no spacelike pairs for distinct scalars
    let scalar_vals = [1, 2, 3];
    let mut sl_pairs = Vec::new();
    for i in 0..3 {
        for j in (i + 1)..3 {
            if !(scalar_vals[i] < scalar_vals[j]) && !(scalar_vals[j] < scalar_vals[i]) {
                sl_pairs.push((i, j));
            }
        }
    }
    assert_eq!(sl_pairs.len(), 0);

    // 2. Preorder asymmetry failure
    let mut rels2 = std::collections::BTreeSet::new();
    rels2.insert((0, 1));
    rels2.insert((1, 0));
    assert!(FinitePoset::new(3, rels2).is_err());

    // 3. Transitivity failure
    let mut rels3 = std::collections::BTreeSet::new();
    rels3.insert((0, 1));
    rels3.insert((1, 2));
    assert!(FinitePoset::new(3, rels3).is_err());

    // 4. Spacelike as inequality failure
    let c1 = construct_c1();
    assert_ne!(
        (0..3)
            .flat_map(|i| (0..3).map(move |j| (i, j)))
            .filter(|(i, j)| i < j)
            .count(),
        c1.incomparable_pairs().len()
    );

    // 5. Missing isomorphism class failure
    let c3 = census_unlabeled(3).unwrap();
    let incomplete: HashMap<_, _> = c3.into_iter().filter(|(k, _)| !k.is_empty()).collect();
    assert_eq!(incomplete.len(), 4);
}
