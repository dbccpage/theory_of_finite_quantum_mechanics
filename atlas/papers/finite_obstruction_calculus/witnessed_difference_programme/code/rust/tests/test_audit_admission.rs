use num_rational::BigRational;
use std::collections::{BTreeMap, HashMap};
use wdp_finite_witness::cochains::{Cochain1, FiniteComplex};
use wdp_finite_witness::foundational_bridges::MultiplicityDistribution;
use wdp_finite_witness::genesis_observer::{HistoryMemory, WordTransducer};
use wdp_finite_witness::obstruction::solve_exact_potential;
use wdp_finite_witness::semiring::coarse_grain;

#[test]
fn metadata_and_carrier_are_part_of_the_certificate() {
    let edges = vec![("a".into(), "b".into()), ("b".into(), "a".into())];
    let complex = FiniteComplex::new(vec!["a".into(), "b".into()], edges.clone()).unwrap();
    let h = Cochain1 { values: edges.into_iter().map(|e| (e, BigRational::from_integer(1.into()))).collect() };
    let valid = solve_exact_potential(&complex, &h).unwrap();
    valid.verify(&complex, &h, None).unwrap();
    let mut altered = valid.clone(); altered.is_exact = true;
    assert!(altered.verify(&complex, &h, None).is_err());
    let mut altered = valid.clone(); altered.authority_effect = "Execute".into();
    assert!(altered.verify(&complex, &h, None).is_err());
    let mut altered = valid.clone(); altered.potential_c0.values.insert("extra".into(), BigRational::from_integer(0.into()));
    assert!(altered.verify(&complex, &h, None).is_err());
    let mut altered = valid.clone(); altered.dual_witness_c1.values.clear();
    assert!(altered.verify(&complex, &h, None).is_err());
    let missing = Cochain1 { values: BTreeMap::new() };
    assert!(solve_exact_potential(&complex, &missing).is_err());
    assert!(FiniteComplex::new(vec!["a".into(), "b".into()], vec![("a".into(), "b".into()); 2]).is_err());
}

#[test]
fn partition_shape_and_multiplicity_overflow_refuse() {
    let weights = vec![BigRational::from_integer(1.into()), BigRational::from_integer(2.into())];
    assert!(coarse_grain(&weights, &[0]).is_err());
    assert!(coarse_grain(&weights[..1], &[0, 1]).is_err());
    assert!(coarse_grain(&[], &[]).is_ok());
    assert!(MultiplicityDistribution::from_counts(HashMap::from([("a".into(), u64::MAX), ("b".into(), 2)])).is_err());
}

#[test]
fn transducer_tables_and_alphabets_are_admitted_before_traversal() {
    assert!(WordTransducer::new(vec![vec![0]], vec![], 0, vec![], vec![vec![]]).is_err());
    assert!(WordTransducer::new(vec![vec![1]], vec![vec![vec![]]], 0, vec![], vec![vec![]]).is_err());
    assert!(WordTransducer::new(vec![vec![0]], vec![vec![vec![1]]], 0, vec![], vec![vec![]]).is_err());
    assert!(WordTransducer::new(vec![vec![0]], vec![vec![vec![]]], 0, vec![1], vec![vec![]]).is_err());
    assert!(WordTransducer::new(vec![vec![0]], vec![vec![vec![]]], 0, vec![], vec![]).is_err());
    let t = WordTransducer::new(vec![vec![0]], vec![vec![vec![0]]], 0, vec![], vec![vec![]]).unwrap();
    let memory = HistoryMemory::new(vec![vec![0, 0]], 0).unwrap();
    assert!(t.descent(&memory).is_err());
}
