// Adversarial fuzzing for LP boundary handling, zero division guards, and degenerate cycles in Rust.
// AuthorityEffect: None.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use proptest::prelude::*;
use std::collections::BTreeMap;
use std::str::FromStr;
use wdp_finite_witness::cochains::{Cochain1, FiniteComplex};
use wdp_finite_witness::error::WdpError;
use wdp_finite_witness::obstruction::solve_exact_potential;

fn parse_rational_guarded(s: &str) -> Result<BigRational, String> {
    if let Ok(r) = BigRational::from_str(s) {
        return Ok(r);
    }
    if let Some((num_s, den_s)) = s.split_once('/') {
        let num = num_s.trim().parse::<BigInt>().map_err(|e| e.to_string())?;
        let den = den_s.trim().parse::<BigInt>().map_err(|e| e.to_string())?;
        if den.is_zero() {
            return Err("Division by zero in rational input".to_string());
        }
        return Ok(BigRational::new(num, den));
    }
    let int_val = s.trim().parse::<BigInt>().map_err(|e| e.to_string())?;
    Ok(BigRational::from(int_val))
}

#[test]
fn test_rust_zero_division_guard_in_rational_parser() {
    assert!(parse_rational_guarded("1/0").is_err());
    assert!(parse_rational_guarded("-99/0").is_err());
    assert!(parse_rational_guarded("0/0").is_err());
    let err_msg = parse_rational_guarded("5/0").unwrap_err();
    assert!(err_msg.contains("Division by zero"));
}

#[test]
fn test_rust_empty_and_duplicate_complex_guards() {
    // Empty vertices
    let res_empty = FiniteComplex::new(vec![], vec![]);
    assert!(res_empty.is_ok()); // Complex can be created
    let empty_c1 = Cochain1 { values: BTreeMap::new() };
    let res_pot = solve_exact_potential(&res_empty.unwrap(), &empty_c1);
    assert!(matches!(res_pot, Err(WdpError::InvalidInput { .. })));

    // Duplicate vertices
    let res_dup = FiniteComplex::new(vec!["v0".into(), "v0".into()], vec![]);
    assert!(matches!(res_dup, Err(WdpError::InvalidInput { .. })));

    // Edge referencing undeclared vertex
    let res_undeclared = FiniteComplex::new(vec!["v0".into()], vec![("v0".into(), "v_ghost".into())]);
    assert!(matches!(res_undeclared, Err(WdpError::InvalidInput { .. })));
}

#[test]
fn test_rust_degenerate_zero_weight_cycle() {
    // 3-cycle where all edge values are zero
    let complex = FiniteComplex::new(
        vec!["v0".into(), "v1".into(), "v2".into()],
        vec![
            ("v0".into(), "v1".into()),
            ("v1".into(), "v2".into()),
            ("v0".into(), "v2".into()),
        ],
    ).unwrap();

    let mut cochain_map = BTreeMap::new();
    cochain_map.insert(("v0".into(), "v1".into()), BigRational::zero());
    cochain_map.insert(("v1".into(), "v2".into()), BigRational::zero());
    cochain_map.insert(("v0".into(), "v2".into()), BigRational::zero());

    let h = Cochain1 { values: cochain_map };
    let cert = solve_exact_potential(&complex, &h).unwrap();

    assert!(cert.phi1_value.is_zero());
    assert!(cert.is_exact);
    assert_eq!(cert.authority_effect, "None");
}

#[test]
fn test_rust_high_order_rational_arbitrary_precision() {
    // High-order rational numerators and denominators (10^20)
    let big_num = BigInt::from(10).pow(20);
    let big_den = BigInt::from(7).pow(20);
    let r1 = BigRational::new(big_num.clone(), big_den.clone());

    let complex = FiniteComplex::new(
        vec!["v0".into(), "v1".into()],
        vec![("v0".into(), "v1".into())],
    ).unwrap();

    let mut map = BTreeMap::new();
    map.insert(("v0".into(), "v1".into()), r1.clone());
    let h = Cochain1 { values: map };

    let cert = solve_exact_potential(&complex, &h).unwrap();
    // On a single edge (tree), potential unwinding is exact
    assert!(cert.phi1_value.is_zero());
    assert!(cert.is_exact);
    assert_eq!(cert.potential_c0.get("v1").unwrap(), r1);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(50))]

    #[test]
    fn prop_rust_adversarial_disconnected_forest_fuzzing(
        num_components in 2usize..6usize,
        edges_per_comp in 1usize..3usize,
    ) {
        let mut vertices = Vec::new();
        let mut edges = Vec::new();
        let mut cochain_map = BTreeMap::new();

        for c in 0..num_components {
            let v_base = format!("c{}_v0", c);
            vertices.push(v_base.clone());
            for e in 1..=edges_per_comp {
                let v_next = format!("c{}_v{}", c, e);
                vertices.push(v_next.clone());
                edges.push((v_base.clone(), v_next.clone()));
                cochain_map.insert((v_base.clone(), v_next.clone()), BigRational::from_integer(BigInt::from(e)));
            }
        }

        let complex = FiniteComplex::new(vertices, edges).unwrap();
        let h = Cochain1 { values: cochain_map };

        let cert = solve_exact_potential(&complex, &h).unwrap();
        // Since each component is a tree (star graph), the exact potential completely unwinds all edges
        prop_assert!(cert.phi1_value.is_zero(), "Forest of trees must have phi1 == 0");
        prop_assert!(cert.is_exact, "Forest of trees must be exact");
    }
}
