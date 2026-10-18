// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Integration tests and mutation kill tests for Campaign C1000 Block 08 Commuting Observables.

use finite_qm_native::campaigns::causal_order::{construct_c1, construct_c2};
use finite_qm_native::campaigns::commuting_observables::*;
use linear_algebra::exact_field::{
    involution::is_hermitian,
    matrix::{commutator, is_scalar_matrix, is_zero_matrix},
};
use omega_lie_theory::pauli_symplectic::{pauli, Pauli};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_quantum_physics::commuting_observables::*;
use std::collections::HashMap;

#[test]
fn test_t990_independent_reimplementation() {
    // 1. Single-qubit Pauli matrices
    let x = pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted");
    let y = pauli::<GaussianRat>(Pauli::Y).expect("the exact Gaussian Pauli fixture is admitted");
    let z = pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted");
    assert!(is_hermitian(&x).unwrap());
    assert!(is_hermitian(&y).unwrap());
    assert!(is_hermitian(&z).unwrap());
    assert!(!is_scalar_matrix(&x).unwrap());
    assert!(!is_scalar_matrix(&y).unwrap());
    assert!(!is_scalar_matrix(&z).unwrap());

    // [X, Y] != 0
    let comm_xy = commutator(&x, &y).unwrap();
    assert!(!is_zero_matrix(&comm_xy));

    // Factor commutation: [M (x) I, I (x) N] = 0
    let m1 = embed_factor_1(&x).unwrap();
    let m2 = embed_factor_2(&z).unwrap();
    let comm_12 = commutator(&m1, &m2).unwrap();
    assert!(is_zero_matrix(&comm_12));

    // 2. Base case C1 witness
    let c1 = construct_c1();
    let (obs1, fac1) = construct_c1_assignment().unwrap();
    let (valid1, reason1, deg1) = validate_observable_assignment(&c1, &obs1, &fac1, true);
    assert!(valid1, "C1 validation failed: {}", reason1);
    assert_eq!(deg1, 0);

    // 3. Structural verdict C2 witness
    let c2 = construct_c2();
    let (obs2, fac2) = construct_c2_assignment().unwrap();
    let (valid2, reason2, deg2) = validate_observable_assignment(&c2, &obs2, &fac2, true);
    assert!(valid2, "C2 validation failed: {}", reason2);
    assert_eq!(deg2, 0);

    // 4. 3-element antichain obstruction
    let c3_anti = construct_c3_antichain();
    let res_c3 = search_poset_assignment(&c3_anti, true).unwrap();
    assert!(!res_c3.admitted);
    assert!(res_c3.has_odd_cycle);
    assert_eq!(res_c3.status, "OBSTRUCTED_BY_ODD_CYCLE");
    assert!(res_c3.degenerate_assignments_rejected > 0);

    // 5. Exhaustive census search
    let census = search_census_at_declared_bound(true).unwrap();
    assert_eq!(census.posets_searched, 21);
    assert_eq!(census.n3_census_count, 5);
    assert_eq!(census.n4_census_count, 16);
    assert_eq!(census.smallest_obstructed_poset_size, Some(3));
    assert!(census.obstructed_poset_found);
    assert_eq!(census.n3_obstructed_count, 1);
    assert_eq!(census.n4_obstructed_count, 6);
    assert_eq!(census.total_obstructed_count, 7);
    assert_eq!(census.total_admitted_count, 14);
}

#[test]
fn test_t991_cross_language_parity() {
    // Parity on independent checker
    let c1 = construct_c1();
    let (obs1, fac1) = construct_c1_assignment().unwrap();
    let strict_1: Vec<(usize, usize)> = (0..c1.size())
        .flat_map(|i| (0..c1.size()).map(move |j| (i, j)))
        .filter(|&(i, j)| c1.less(i, j).unwrap())
        .collect();
    let res1 = verify_witness_independent(c1.size(), &strict_1, &obs1, &fac1, true);
    assert_eq!(res1, Ok(true));

    let c2 = construct_c2();
    let (obs2, fac2) = construct_c2_assignment().unwrap();
    let strict_2: Vec<(usize, usize)> = (0..c2.size())
        .flat_map(|i| (0..c2.size()).map(move |j| (i, j)))
        .filter(|&(i, j)| c2.less(i, j).unwrap())
        .collect();
    let res2 = verify_witness_independent(c2.size(), &strict_2, &obs2, &fac2, true);
    assert_eq!(res2, Ok(true));

    // Parity on census counts
    let census = search_census_at_declared_bound(true).unwrap();
    assert_eq!(census.posets_searched, 21);
    assert_eq!(census.smallest_obstructed_poset_size, Some(3));
    assert_eq!(census.total_obstructed_count, 7);
    assert_eq!(census.total_admitted_count, 14);
}

#[test]
fn test_t992_mutation_1_tolerance_rejected() {
    let m1 = embed_factor_1(
        &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
    )
    .unwrap();
    let m2 = embed_factor_1(
        &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
    )
    .unwrap();
    let comm = commutator(&m1, &m2).unwrap();
    assert!(!is_zero_matrix(&comm));

    let tiny = linear_algebra::exact_field::matrix::scale(
        &m1,
        &omega_number_theory::cyclotomic::GaussianRat::from_rational(
            omega_number_theory::rational::rq(1, 1_000_000_000),
        ),
    )
    .unwrap();
    assert!(!is_zero_matrix(&commutator(&tiny, &m2).unwrap()));
}

#[test]
fn test_t992_mutation_2_comparable_events_tested_rejected() {
    let c1 = construct_c1();
    let (obs1, _fac1) = construct_c1_assignment().unwrap();

    // Comparable events (0, 1) do not commute
    let comm_01 = commutator(obs1.get(&0).unwrap(), obs1.get(&1).unwrap()).unwrap();
    assert!(!is_zero_matrix(&comm_01));

    // Erroneous all-pairs check falsely rejects C1
    let mut all_pairs_commute = true;
    for i in 0..c1.size() {
        for j in (i + 1)..c1.size() {
            let comm = commutator(obs1.get(&i).unwrap(), obs1.get(&j).unwrap()).unwrap();
            if !is_zero_matrix(&comm) {
                all_pairs_commute = false;
                break;
            }
        }
    }
    assert!(
        !all_pairs_commute,
        "Erroneous all-pairs test must fail on C1"
    );

    // Correct spacelike-only check passes C1
    let (valid, _, _) = validate_observable_assignment(&c1, &obs1, &_fac1, true);
    assert!(valid);
}

#[test]
fn test_t992_mutation_3_observable_class_enlarged_rejected() {
    let c1 = construct_c1();
    let (obs, mut labels) = construct_c1_assignment().unwrap();
    labels.insert(2, 3);
    let relations = (0..c1.size())
        .flat_map(|i| (0..c1.size()).map(move |j| (i, j)))
        .filter(|&(i, j)| c1.less(i, j).unwrap())
        .collect::<Vec<_>>();
    assert!(
        verify_witness_independent(c1.size(), &relations, &obs, &labels, true)
            .unwrap_err()
            .contains("two-factor")
    );
}

#[test]
fn test_t992_mutation_4_partial_search_rejected() {
    let partial = finite_qm_native::campaigns::causal_order::census_unlabeled(3)
        .unwrap()
        .len();
    let complete = search_census_at_declared_bound(true).unwrap();
    assert_eq!(partial, complete.n3_census_count);
    assert_eq!(
        complete.posets_searched,
        complete.n3_census_count + complete.n4_census_count
    );
    assert!(partial < complete.posets_searched);
}

#[test]
fn test_t992_mutation_5_planted_non_commuting_rejected() {
    let c1 = construct_c1();
    // Plant non-commuting on spacelike pair {1, 2}
    let mut planted_obs = HashMap::new();
    planted_obs.insert(
        0,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .unwrap(),
    );
    planted_obs.insert(
        1,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .unwrap(),
    );
    planted_obs.insert(
        2,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .unwrap(),
    ); // Both 1 and 2 on factor 1, non-commuting!

    let mut planted_fac = HashMap::new();
    planted_fac.insert(0, 1);
    planted_fac.insert(1, 1);
    planted_fac.insert(2, 1);

    let (valid, reason, _) = validate_observable_assignment(&c1, &planted_obs, &planted_fac, true);
    assert!(!valid);
    assert!(reason.contains("spacelike events 1 and 2 do not commute"));
}

#[test]
fn test_t992_mutation_6_planted_all_scalar_rejected() {
    let c1 = construct_c1();
    let id4 = linear_algebra::exact_field::matrix::identity::<GaussianRat>(4).unwrap();
    let mut planted_obs = HashMap::new();
    planted_obs.insert(0, id4.clone());
    planted_obs.insert(1, id4.clone());
    planted_obs.insert(2, id4);

    let mut planted_fac = HashMap::new();
    planted_fac.insert(0, 1);
    planted_fac.insert(1, 1);
    planted_fac.insert(2, 2);

    let (valid, reason, deg_count) =
        validate_observable_assignment(&c1, &planted_obs, &planted_fac, true);
    assert!(!valid);
    assert_eq!(deg_count, 1);
    assert!(reason.contains("scalar multiple of identity"));
}
