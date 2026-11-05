// Adversarial dual witness stress-testing in pure Rust over BigRational.
// AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::{One, Zero};
use std::collections::BTreeMap;
use wdp_finite_witness::cochains::{Cochain1, FiniteComplex};
use wdp_finite_witness::obstruction::{solve_exact_potential, solve_exact_potential_weighted};

#[test]
fn test_rust_adversarial_cycle_with_chord_simplex_beats_bfs() {
    let complex = FiniteComplex::new(
        vec!["0".into(), "1".into(), "2".into(), "3".into()],
        vec![
            ("0".into(), "1".into()),
            ("1".into(), "2".into()),
            ("2".into(), "3".into()),
            ("3".into(), "0".into()),
            ("1".into(), "3".into()),
        ],
    ).unwrap();

    let mut cochain_map = BTreeMap::new();
    cochain_map.insert(("0".into(), "1".into()), BigRational::one());
    cochain_map.insert(("1".into(), "2".into()), BigRational::one());
    cochain_map.insert(("2".into(), "3".into()), BigRational::one());
    cochain_map.insert(("3".into(), "0".into()), BigRational::one());
    cochain_map.insert(("1".into(), "3".into()), BigRational::zero());
    let h = Cochain1 { values: cochain_map };

    let cert = solve_exact_potential(&complex, &h).expect("solve cycle with chord");

    // Simplex achieves exact global minimum of 4 (BFS would produce 6)
    assert_eq!(cert.phi1_value, BigRational::from_integer(4.into()));
    assert!(!cert.is_exact);

    // Algebraic verification of emitted dual witness:
    cert.verify(&complex, &h, None).expect("5-point verification must pass");

    // Check Kirchhoff divergence directly:
    let mut div_map = BTreeMap::new();
    for v in &complex.vertices {
        div_map.insert(v.clone(), BigRational::zero());
    }
    for (u, v) in &complex.edges {
        let edge = (u.clone(), v.clone());
        let y = cert.dual_witness_c1.values.get(&edge).unwrap();
        *div_map.get_mut(u).unwrap() -= y;
        *div_map.get_mut(v).unwrap() += y;
    }
    for (v, div) in div_map {
        assert!(div.is_zero(), "Divergence at vertex {} was not zero: {}", v, div);
    }
}

#[test]
fn test_rust_adversarial_k4_frustrated_circulation() {
    let complex = FiniteComplex::new(
        vec!["0".into(), "1".into(), "2".into(), "3".into()],
        vec![
            ("0".into(), "1".into()),
            ("0".into(), "2".into()),
            ("0".into(), "3".into()),
            ("1".into(), "2".into()),
            ("1".into(), "3".into()),
            ("2".into(), "3".into()),
        ],
    ).unwrap();

    let mut cochain_map = BTreeMap::new();
    cochain_map.insert(("0".into(), "1".into()), BigRational::one());
    cochain_map.insert(("0".into(), "2".into()), -BigRational::one());
    cochain_map.insert(("0".into(), "3".into()), BigRational::one());
    cochain_map.insert(("1".into(), "2".into()), BigRational::one());
    cochain_map.insert(("1".into(), "3".into()), BigRational::zero());
    cochain_map.insert(("2".into(), "3".into()), -BigRational::one());
    let h = Cochain1 { values: cochain_map };

    let cert = solve_exact_potential(&complex, &h).expect("solve K4");

    // Simplex achieves exact global minimum of 3 (BFS produces 6)
    assert_eq!(cert.phi1_value, BigRational::from_integer(3.into()));
    cert.verify(&complex, &h, None).expect("K4 dual witness passes 5-point verification");
}

#[test]
fn test_rust_adversarial_mobius_ladder_m3() {
    // Mobius Ladder M3 (6 vertices, 9 edges, K_3,3)
    let vertices = vec!["0".into(), "1".into(), "2".into(), "3".into(), "4".into(), "5".into()];
    let edges = vec![
        ("0".into(), "1".into()), ("1".into(), "2".into()), ("2".into(), "3".into()),
        ("3".into(), "4".into()), ("4".into(), "5".into()), ("5".into(), "0".into()),
        ("0".into(), "3".into()), ("1".into(), "4".into()), ("2".into(), "5".into()),
    ];
    let complex = FiniteComplex::new(vertices, edges).unwrap();

    let mut cochain_map = BTreeMap::new();
    cochain_map.insert(("0".into(), "1".into()), BigRational::one());
    cochain_map.insert(("1".into(), "2".into()), BigRational::one());
    cochain_map.insert(("2".into(), "3".into()), BigRational::one());
    cochain_map.insert(("3".into(), "4".into()), BigRational::one());
    cochain_map.insert(("4".into(), "5".into()), BigRational::one());
    cochain_map.insert(("5".into(), "0".into()), BigRational::one());
    cochain_map.insert(("0".into(), "3".into()), BigRational::zero());
    cochain_map.insert(("1".into(), "4".into()), BigRational::zero());
    cochain_map.insert(("2".into(), "5".into()), BigRational::zero());
    let h = Cochain1 { values: cochain_map };

    let cert = solve_exact_potential(&complex, &h).expect("solve M3");

    // Simplex achieves exact global minimum of 6 (BFS produces 9)
    assert_eq!(cert.phi1_value, BigRational::from_integer(6.into()));
    cert.verify(&complex, &h, None).expect("M3 dual witness passes 5-point verification");
}

#[test]
fn test_rust_adversarial_mobius_ladder_m4() {
    // Mobius Ladder M4 (8 vertices, 12 edges)
    let vertices = (0..8).map(|i| i.to_string()).collect::<Vec<_>>();
    let edges = vec![
        ("0".into(), "1".into()), ("1".into(), "2".into()), ("2".into(), "3".into()), ("3".into(), "4".into()),
        ("4".into(), "5".into()), ("5".into(), "6".into()), ("6".into(), "7".into()), ("7".into(), "0".into()),
        ("0".into(), "4".into()), ("1".into(), "5".into()), ("2".into(), "6".into()), ("3".into(), "7".into()),
    ];
    let complex = FiniteComplex::new(vertices, edges).unwrap();

    let mut cochain_map = BTreeMap::new();
    cochain_map.insert(("0".into(), "1".into()), BigRational::from_integer(2.into()));
    cochain_map.insert(("1".into(), "2".into()), -BigRational::one());
    cochain_map.insert(("2".into(), "3".into()), BigRational::from_integer(3.into()));
    cochain_map.insert(("3".into(), "4".into()), BigRational::one());
    cochain_map.insert(("4".into(), "5".into()), -BigRational::from_integer(2.into()));
    cochain_map.insert(("5".into(), "6".into()), BigRational::from_integer(2.into()));
    cochain_map.insert(("6".into(), "7".into()), BigRational::one());
    cochain_map.insert(("7".into(), "0".into()), -BigRational::one());
    cochain_map.insert(("0".into(), "4".into()), BigRational::one());
    cochain_map.insert(("1".into(), "5".into()), -BigRational::one());
    cochain_map.insert(("2".into(), "6".into()), BigRational::from_integer(2.into()));
    cochain_map.insert(("3".into(), "7".into()), BigRational::zero());
    let h = Cochain1 { values: cochain_map };

    let cert = solve_exact_potential(&complex, &h).expect("solve M4");

    // Simplex achieves exact global minimum of 5 (BFS produces 12)
    assert_eq!(cert.phi1_value, BigRational::from_integer(5.into()));
    cert.verify(&complex, &h, None).expect("M4 dual witness passes 5-point verification");
}

#[test]
fn test_rust_weighted_simplex_capacity_conformance() {
    let complex = FiniteComplex::new(
        vec!["0".into(), "1".into(), "2".into(), "3".into()],
        vec![
            ("0".into(), "1".into()),
            ("1".into(), "2".into()),
            ("2".into(), "3".into()),
            ("3".into(), "0".into()),
            ("1".into(), "3".into()),
        ],
    ).unwrap();

    let mut cochain_map = BTreeMap::new();
    cochain_map.insert(("0".into(), "1".into()), BigRational::one());
    cochain_map.insert(("1".into(), "2".into()), BigRational::one());
    cochain_map.insert(("2".into(), "3".into()), BigRational::one());
    cochain_map.insert(("3".into(), "0".into()), BigRational::one());
    cochain_map.insert(("1".into(), "3".into()), BigRational::zero());
    let h = Cochain1 { values: cochain_map };

    let mut weights = BTreeMap::new();
    weights.insert(("0".into(), "1".into()), BigRational::one());
    weights.insert(("1".into(), "2".into()), BigRational::one());
    weights.insert(("2".into(), "3".into()), BigRational::one());
    weights.insert(("3".into(), "0".into()), BigRational::one());
    // Assign heavy weight to chord
    weights.insert(("1".into(), "3".into()), BigRational::from_integer(50.into()));

    let cert = solve_exact_potential_weighted(&complex, &h, Some(&weights)).expect("solve weighted");

    // Optimal weighted cost must remain 4 by assigning residual to unit weight edges
    assert_eq!(cert.phi1_value, BigRational::from_integer(4.into()));
    cert.verify(&complex, &h, Some(&weights)).expect("weighted verification passes");

    // Chord must have zero residual due to high weight
    let chord_r = cert.residual_c1.values.get(&("1".into(), "3".into())).unwrap();
    assert_eq!(chord_r, &BigRational::zero());
}
