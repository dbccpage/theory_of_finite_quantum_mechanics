//! Declared small causal-order witnesses and bounded campaign census.
//! AuthorityEffect: None.
use omega_homology::finite_poset::{FinitePoset, PosetError};
use omega_homology::poset_census::{canonical_relations, labelled_posets};
use std::collections::BTreeMap;

pub fn construct_c1() -> FinitePoset {
    FinitePoset::new(3, [(0, 1), (0, 2)]).expect("declared fork poset")
}
pub fn construct_c2() -> FinitePoset {
    FinitePoset::new(4, [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]).expect("declared diamond poset")
}
pub fn census_unlabeled(
    n: usize,
) -> Result<BTreeMap<Vec<(usize, usize)>, Vec<FinitePoset>>, PosetError> {
    let mut classes = BTreeMap::<Vec<(usize, usize)>, Vec<FinitePoset>>::new();
    for p in labelled_posets(n)? {
        classes.entry(canonical_relations(&p)?).or_default().push(p);
    }
    Ok(classes)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;

    #[test]
    fn test_c1_properties() {
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
    fn test_c2_properties() {
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
    fn test_census_n3() {
        let posets_3 = labelled_posets(3).unwrap();
        assert_eq!(posets_3.len(), 19);
        let classes_3 = census_unlabeled(3).unwrap();
        assert_eq!(classes_3.len(), 5);
        let with_sl = classes_3
            .values()
            .filter(|members| !members[0].incomparable_pairs().is_empty())
            .count();
        assert_eq!(with_sl, 4);
    }

    #[test]
    fn test_census_n4() {
        let posets_4 = labelled_posets(4).unwrap();
        assert_eq!(posets_4.len(), 219);
        let classes_4 = census_unlabeled(4).unwrap();
        assert_eq!(classes_4.len(), 16);
        let with_sl = classes_4
            .values()
            .filter(|members| !members[0].incomparable_pairs().is_empty())
            .count();
        assert_eq!(with_sl, 15);
    }

    // T817 Negative Controls / Mutation Tests
    #[test]
    fn test_t817_negative_1_scalar_as_causal() {
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
    }

    #[test]
    fn test_t817_negative_2_preorder_asymmetry_rejection() {
        let mut rels = BTreeSet::new();
        rels.insert((0, 1));
        rels.insert((1, 0));
        assert!(FinitePoset::new(3, rels).is_err());
    }

    #[test]
    fn test_t817_negative_3_transitivity_rejection() {
        let mut rels = BTreeSet::new();
        rels.insert((0, 1));
        rels.insert((1, 2));
        assert!(FinitePoset::new(3, rels).is_err());
    }

    #[test]
    fn test_t817_negative_4_spacelike_as_inequality() {
        let c1 = construct_c1();
        let buggy_spacelike_len = (0..3)
            .flat_map(|i| (0..3).map(move |j| (i, j)))
            .filter(|(i, j)| i < j)
            .count();
        let true_spacelike = c1.incomparable_pairs();
        assert_eq!(buggy_spacelike_len, 3);
        assert_eq!(true_spacelike, vec![(1, 2)]);
    }

    #[test]
    fn test_t817_negative_5_missing_isomorphism_class() {
        let classes_3 = census_unlabeled(3).unwrap();
        let incomplete: BTreeMap<_, _> = classes_3
            .into_iter()
            .filter(|(k, _)| !k.is_empty())
            .collect();
        assert_eq!(incomplete.len(), 4);
    }
}
