// Executable finite evidence; AuthorityEffect: None.
use num_rational::BigRational;
use num_traits::Zero;
use std::collections::{BTreeMap, BTreeSet};
use wdp_finite_witness::cochains::{Cochain0, Cochain1, FiniteComplex};
use wdp_finite_witness::difference::Carrier;
use wdp_finite_witness::functional_classification::{classify_observer, FunctionalClass};
use wdp_finite_witness::genesis_observer::{DescentResult, HistoryMemory, WordTransducer};
use wdp_finite_witness::obstruction::solve_exact_potential;
use wdp_finite_witness::profile_evaluator::{EvaluationStatus, Evidence, FiniteProfile};
use wdp_finite_witness::self_reference::evaluate_diagonal_fixed_point;
use wdp_finite_witness::semiring::coarse_grain;

fn make_prefix_transducer() -> WordTransducer {
    WordTransducer::new(
        vec![vec![0, 0]],
        vec![vec![vec![0], vec![1]]],
        0,
        vec![1],
        vec![vec![]],
    ).expect("valid transducer")
}

#[test]
fn test_carrier_primitive_difference() {
    let c1 = Carrier::new(vec!["mark_a".into(), "mark_b".into()]).expect("valid carrier");
    let c2 = Carrier::new(vec!["mark_b".into(), "mark_c".into()]).expect("valid carrier");
    assert_eq!(c1.size(), 2);
    assert!(c1.contains("mark_a"));
    assert!(!c1.contains("mark_c"));
    let diff = c1.difference(&c2);
    assert_eq!(diff.len(), 1);
    assert!(diff.contains(&wdp_finite_witness::difference::Mark("mark_a".into())));
}

#[test]
fn test_cochain_coboundary_and_boundary() {
    let vertices = vec!["v0".into(), "v1".into(), "v2".into()];
    let edges = vec![
        ("v0".into(), "v1".into()),
        ("v1".into(), "v2".into()),
        ("v0".into(), "v2".into()),
    ];
    let complex = FiniteComplex::new(vertices, edges).expect("valid complex");

    let mut pot_values = BTreeMap::new();
    pot_values.insert("v0".into(), BigRational::zero());
    pot_values.insert("v1".into(), BigRational::from_integer(1.into()));
    pot_values.insert("v2".into(), BigRational::from_integer(3.into()));
    let c0 = Cochain0 { values: pot_values };

    let d0_c0 = complex.coboundary_0(&c0).expect("coboundary success");
    assert_eq!(d0_c0.values.get(&("v0".into(), "v1".into())), Some(&BigRational::from_integer(1.into())));
    assert_eq!(d0_c0.values.get(&("v1".into(), "v2".into())), Some(&BigRational::from_integer(2.into())));
    assert_eq!(d0_c0.values.get(&("v0".into(), "v2".into())), Some(&BigRational::from_integer(3.into())));

    // The boundary of an oriented cycle is identically zero
    let mut cycle_values = BTreeMap::new();
    cycle_values.insert(("v0".into(), "v1".into()), BigRational::from_integer(1.into()));
    cycle_values.insert(("v1".into(), "v2".into()), BigRational::from_integer(1.into()));
    cycle_values.insert(("v0".into(), "v2".into()), BigRational::from_integer((-1).into()));
    let c1_cycle = Cochain1 { values: cycle_values };

    let boundary_cycle = complex.boundary_1(&c1_cycle).expect("boundary success");
    for v in &complex.vertices {
        let val = boundary_cycle.get(v).expect("vertex present");
        assert!(val.is_zero(), "boundary of oriented 1-cycle must be zero at vertex {}", v);
    }
}

#[test]
fn test_exact_potential_and_obstruction() {
    let vertices = vec!["v0".into(), "v1".into(), "v2".into()];
    let edges = vec![
        ("v0".into(), "v1".into()),
        ("v1".into(), "v2".into()),
        ("v0".into(), "v2".into()),
    ];
    let complex = FiniteComplex::new(vertices, edges).expect("valid complex");

    // Case 1: Exact 1-cochain (cycle holonomy is zero)
    let mut exact_values = BTreeMap::new();
    exact_values.insert(("v0".into(), "v1".into()), BigRational::from_integer(1.into()));
    exact_values.insert(("v1".into(), "v2".into()), BigRational::from_integer(2.into()));
    exact_values.insert(("v0".into(), "v2".into()), BigRational::from_integer(3.into()));
    let h_exact = Cochain1 { values: exact_values };

    let cert_exact = solve_exact_potential(&complex, &h_exact).expect("solve exact");
    assert!(cert_exact.is_exact);
    assert_eq!(cert_exact.phi1_value, BigRational::zero());
    assert_eq!(cert_exact.authority_effect, "None");

    // Case 2: Obstructed 1-cochain (non-zero holonomy around triangle)
    let mut obst_values = BTreeMap::new();
    obst_values.insert(("v0".into(), "v1".into()), BigRational::from_integer(1.into()));
    obst_values.insert(("v1".into(), "v2".into()), BigRational::from_integer(1.into()));
    obst_values.insert(("v0".into(), "v2".into()), BigRational::zero());
    let h_obst = Cochain1 { values: obst_values };

    let cert_obst = solve_exact_potential(&complex, &h_obst).expect("solve obstructed");
    assert!(!cert_obst.is_exact);
    assert!(cert_obst.phi1_value > BigRational::zero());
    assert_eq!(cert_obst.authority_effect, "None");
}

#[test]
fn test_genesis_observer_descent_map() {
    let memory = HistoryMemory::new(vec![vec![0, 1], vec![1, 0]], 0).expect("valid memory");
    let rho = make_prefix_transducer();

    let descent = rho.descent(&memory).expect("admitted transducer and memory");
    match descent {
        DescentResult::Map { prefix, .. } => {
            assert_eq!(prefix, vec![1]);
        }
        DescentResult::Collision { .. } => {
            panic!("expected map result");
        }
    }
}

#[test]
fn test_genesis_observer_descent_collision() {
    let memory = HistoryMemory::new(vec![vec![0, 1], vec![0, 1]], 0).expect("valid memory");
    let rho = make_prefix_transducer();

    let descent = rho.descent(&memory).expect("admitted transducer and memory");
    match descent {
        DescentResult::Collision { first, second } => {
            assert_eq!(memory.run(&first), memory.run(&second));
            assert_ne!(memory.run(&rho.apply(&first)), memory.run(&rho.apply(&second)));
        }
        DescentResult::Map { .. } => {
            panic!("expected collision result");
        }
    }
}

#[test]
fn test_profile_evaluator_ch20() {
    let mut table = BTreeMap::new();
    table.insert("query_a".into(), true);
    table.insert("query_b".into(), false);

    let mut admitted = BTreeSet::new();
    admitted.insert("query_a".into());
    admitted.insert("query_b".into());

    let mut refused = BTreeSet::new();
    refused.insert("query_b".into());

    let profile = FiniteProfile::new(table, admitted, refused, 2).expect("valid profile");

    let ev_match = vec![Evidence { query: "query_a".into(), value: true }];
    assert_eq!(profile.evaluate("query_a", &ev_match), EvaluationStatus::Admitted(true));

    let ev_mismatch = vec![Evidence { query: "query_a".into(), value: false }];
    assert_eq!(profile.evaluate("query_a", &ev_mismatch), EvaluationStatus::Admitted(false));

    assert_eq!(profile.evaluate("query_b", &ev_match), EvaluationStatus::Refused);
    assert_eq!(profile.evaluate("undeclared", &ev_match), EvaluationStatus::OutsideDomain);
}

#[test]
fn test_functional_classification_trichotomy() {
    let rho = make_prefix_transducer();
    let parity = HistoryMemory::new(vec![vec![0, 1], vec![1, 0]], 0).expect("valid memory");
    let profiles_ab = vec!["a".to_string(), "b".to_string()];
    let profiles_aa = vec!["a".to_string(), "a".to_string()];

    let class_o1 = classify_observer(&parity, &profiles_ab, &[("prefix", &rho)]).expect("admitted profiles");
    assert_eq!(class_o1, FunctionalClass::O1Only);

    let class_outside = classify_observer(&parity, &profiles_aa, &[("prefix", &rho)]).expect("admitted profiles");
    assert_eq!(class_outside, FunctionalClass::OutsideO1);

    let last = HistoryMemory::new(vec![vec![0, 1], vec![0, 1]], 0).expect("valid memory");
    let class_o2 = classify_observer(&last, &profiles_ab, &[("prefix", &rho)]).expect("admitted profiles");
    match class_o2 {
        FunctionalClass::O2 { name, first, second } => {
            assert_eq!(name, "prefix");
            assert_eq!(last.run(&first), last.run(&second));
            assert_ne!(last.run(&rho.apply(&first)), last.run(&rho.apply(&second)));
        }
        _ => panic!("expected O2 classification"),
    }
}

#[test]
fn test_self_reference_diagonal() {
    let table = vec![
        vec![true, false],
        vec![false, false],
    ];
    let witness = evaluate_diagonal_fixed_point(&table);
    assert!(witness.is_some());
    let w = witness.unwrap();
    assert_eq!(w.index, 0);
    assert!(w.fixed_point);
    assert_eq!(w.authority_effect, "None");
}

#[test]
fn test_semiring_coarse_graining() {
    let weights = vec![
        BigRational::from_integer(1.into()),
        BigRational::from_integer(2.into()),
        BigRational::from_integer(3.into()),
    ];
    let partition = vec![0, 0, 1];
    let receipt = coarse_grain(&weights, &partition).expect("matching partition");
    assert_eq!(receipt.partition_sums.get(&0), Some(&BigRational::from_integer(3.into())));
    assert_eq!(receipt.partition_sums.get(&1), Some(&BigRational::from_integer(3.into())));
    assert_eq!(receipt.total_mass, BigRational::from_integer(6.into()));
}
