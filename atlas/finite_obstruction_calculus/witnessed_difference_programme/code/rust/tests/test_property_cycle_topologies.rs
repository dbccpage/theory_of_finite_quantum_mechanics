// Property-based testing for randomized cycle topologies over exact rationals.
// AuthorityEffect: None.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use proptest::prelude::*;
use std::collections::BTreeMap;
use wdp_finite_witness::cochains::{Cochain0, Cochain1, FiniteComplex};
use wdp_finite_witness::obstruction::solve_exact_potential;

prop_compose! {
    fn rational_strategy()(num in -1000i64..1000i64, den in 1i64..1000i64) -> BigRational {
        BigRational::new(BigInt::from(num), BigInt::from(den))
    }
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(50))]

    #[test]
    fn prop_coboundary_nilpotency_random_cycle(
        cycle_len in 3usize..8usize,
        potentials in proptest::collection::vec(rational_strategy(), 3..8),
    ) {
        let n = cycle_len;
        let vertices: Vec<String> = (0..n).map(|i| format!("v{}", i)).collect();
        let mut edges = Vec::new();
        for i in 0..n {
            edges.push((format!("v{}", i), format!("v{}", (i + 1) % n)));
        }
        let complex = FiniteComplex::new(vertices.clone(), edges).unwrap();

        let mut pot_map = BTreeMap::new();
        for (i, v) in vertices.iter().enumerate() {
            let val = potentials.get(i).cloned().unwrap_or_else(BigRational::zero);
            pot_map.insert(v.clone(), val);
        }
        let c0 = Cochain0 { values: pot_map };

        // Coboundary d0
        let d0_c0 = complex.coboundary_0(&c0).unwrap();

        // 1-Cochain coboundary along any 2-cell (or cycle triangle)
        // If we compute the cycle sum of d0_c0, it must telescopingly vanish:
        let mut cycle_sum = BigRational::zero();
        for i in 0..n {
            let u = format!("v{}", i);
            let v = format!("v{}", (i + 1) % n);
            let edge_val = d0_c0.values.get(&(u, v)).unwrap();
            cycle_sum += edge_val;
        }
        prop_assert!(cycle_sum.is_zero(), "Telescoping sum of exact coboundary along a cycle must be zero");
    }

    #[test]
    fn prop_obstruction_gauge_invariance(
        cycle_len in 3usize..7usize,
        edge_vals in proptest::collection::vec(rational_strategy(), 3..7),
        gauge_vals in proptest::collection::vec(rational_strategy(), 3..7),
    ) {
        let n = cycle_len;
        let vertices: Vec<String> = (0..n).map(|i| format!("v{}", i)).collect();
        let mut edges = Vec::new();
        for i in 0..n {
            edges.push((format!("v{}", i), format!("v{}", (i + 1) % n)));
        }
        let complex = FiniteComplex::new(vertices.clone(), edges.clone()).unwrap();

        let mut c1_map = BTreeMap::new();
        for (i, e) in edges.iter().enumerate() {
            let val = edge_vals.get(i).cloned().unwrap_or_else(BigRational::zero);
            c1_map.insert((e.0.clone(), e.1.clone()), val);
        }
        let c1_base = Cochain1 { values: c1_map.clone() };

        let mut pot_map = BTreeMap::new();
        for (i, v) in vertices.iter().enumerate() {
            let val = gauge_vals.get(i).cloned().unwrap_or_else(BigRational::zero);
            pot_map.insert(v.clone(), val);
        }
        let gauge_c0 = Cochain0 { values: pot_map };
        let d0_gauge = complex.coboundary_0(&gauge_c0).unwrap();

        let mut c1_gauged_map = BTreeMap::new();
        for e in &edges {
            let base_val = c1_map.get(&(e.0.clone(), e.1.clone())).cloned().unwrap_or_else(BigRational::zero);
            let g_val = d0_gauge.values.get(&(e.0.clone(), e.1.clone())).cloned().unwrap_or_else(BigRational::zero);
            c1_gauged_map.insert((e.0.clone(), e.1.clone()), base_val + g_val);
        }
        let c1_gauged = Cochain1 { values: c1_gauged_map };

        let cert_base = solve_exact_potential(&complex, &c1_base).unwrap();
        let cert_gauged = solve_exact_potential(&complex, &c1_gauged).unwrap();

        prop_assert!(cert_base.phi1_value >= BigRational::zero(), "Quotient norm phi1 must be non-negative");
        prop_assert!(cert_gauged.phi1_value >= BigRational::zero(), "Quotient norm phi1 must be non-negative");
        prop_assert_eq!(cert_base.phi1_value, cert_gauged.phi1_value, "Quotient norm phi1 is gauge invariant under exact additions");
        prop_assert_eq!(cert_base.is_exact, cert_gauged.is_exact, "Exactness status must match under gauge transformations");
    }
}
