//! Unit tests for FQCD Strong-Coupling Area Law (Record TFQ-1052).
//!
//! Governing DAG target node: FQCD-STRONG-COUPLING-AREA-LAW
//! AuthorityEffect: None

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

use theory_of_finite_qm::crate_root_inventory_holds;
use theory_of_finite_qm::fqcd::{
    area_law_decay_bound_rational, beta0_rational_approx, beta0_rational_bounds,
    check_geometric_cluster_series_bound, cluster_series_geometric_sum, collar_tube_contraction,
    const_k, coordination_number_delta, loop_perimeter, minimal_spanning_area,
    q8_center_parity_non_screening_verified, q8_cubic_character_invariant_sum,
    s3_cubic_character_invariant_sum, twod_character_decimation_area_law,
    verify_fqcd_strong_coupling_area_law_witness,
};

fn rat(n: i64, d: i64) -> BigRational {
    BigRational::new(BigInt::from(n), BigInt::from(d))
}

#[test]
fn test_coordination_numbers_and_refusals() {
    assert_eq!(coordination_number_delta(2).unwrap(), 4);
    assert_eq!(coordination_number_delta(3).unwrap(), 12);
    assert_eq!(coordination_number_delta(4).unwrap(), 24);
    assert_eq!(coordination_number_delta(5).unwrap(), 40);
    assert_eq!(coordination_number_delta(6).unwrap(), 60);

    assert!(coordination_number_delta(1).is_err());
    assert!(coordination_number_delta(0).is_err());
}

#[test]
fn test_beta0_rational_bounds_and_approx() {
    for n in [2, 3, 5] {
        for d in [2, 3, 4] {
            let (lower, upper) = beta0_rational_bounds(n, d).unwrap();
            let approx = beta0_rational_approx(n, d).unwrap();

            assert!(lower > BigRational::zero());
            assert!(upper > lower);
            assert!(approx >= lower && approx <= upper);
        }
    }

    // Monotonicity: decreasing in d and N
    let b_2_2 = beta0_rational_approx(2, 2).unwrap();
    let b_2_3 = beta0_rational_approx(2, 3).unwrap();
    let b_2_4 = beta0_rational_approx(2, 4).unwrap();
    assert!(b_2_2 > b_2_3);
    assert!(b_2_3 > b_2_4);

    let b_3_4 = beta0_rational_approx(3, 4).unwrap();
    let b_4_4 = beta0_rational_approx(4, 4).unwrap();
    assert!(b_2_4 > b_3_4);
    assert!(b_3_4 > b_4_4);

    assert!(beta0_rational_bounds(1, 4).is_err());
    assert!(beta0_rational_bounds(2, 1).is_err());
}

#[test]
fn test_spanning_area_and_perimeter() {
    assert_eq!(minimal_spanning_area(1, 1).unwrap(), 1);
    assert_eq!(loop_perimeter(1, 1).unwrap(), 4);

    assert_eq!(minimal_spanning_area(3, 5).unwrap(), 15);
    assert_eq!(loop_perimeter(3, 5).unwrap(), 16);

    assert_eq!(minimal_spanning_area(10, 20).unwrap(), 200);
    assert_eq!(loop_perimeter(10, 20).unwrap(), 60);

    assert!(minimal_spanning_area(0, 5).is_err());
    assert!(minimal_spanning_area(5, 0).is_err());
    assert!(loop_perimeter(0, 5).is_err());
}

#[test]
fn test_exact_constants_and_decay_bound() {
    assert_eq!(const_k(), BigRational::one());

    for a in 1..=8 {
        let bound = area_law_decay_bound_rational(a).unwrap();
        let expected = rat(1, 4i64.pow(a as u32));
        assert_eq!(bound, expected);
    }

    assert!(area_law_decay_bound_rational(0).is_err());
}

#[test]
fn test_cluster_series_geometric_sum_and_bound() {
    let mu_fifth = rat(1, 5);
    for a in 1..=10 {
        let s = cluster_series_geometric_sum(&mu_fifth, a).unwrap();
        let b = area_law_decay_bound_rational(a).unwrap();
        assert!(s <= b);
        assert!(check_geometric_cluster_series_bound(&mu_fifth, a).unwrap());
    }

    // Equality at Area = 1: s = (1/5) / (4/5) = 1/4 == bound(1) = 1/4
    let s1 = cluster_series_geometric_sum(&mu_fifth, 1).unwrap();
    assert_eq!(s1, rat(1, 4));

    // Refusal on invalid mu
    assert!(cluster_series_geometric_sum(&rat(1, 1), 1).is_err());
    assert!(cluster_series_geometric_sum(&rat(-1, 5), 1).is_err());
    assert!(cluster_series_geometric_sum(&mu_fifth, 0).is_err());
}

#[test]
fn test_s3_cubic_character_invariant_and_screening() {
    assert_eq!(s3_cubic_character_invariant_sum(), BigRational::one());

    assert_eq!(collar_tube_contraction(0), BigRational::one());
    assert_eq!(collar_tube_contraction(1), rat(1, 2));
    assert_eq!(collar_tube_contraction(17), rat(1, 131072));
    assert!(collar_tube_contraction(17) > BigRational::zero());
}

#[test]
fn test_q8_cubic_character_invariant_and_protection() {
    assert!(q8_cubic_character_invariant_sum().is_zero());
    assert!(q8_center_parity_non_screening_verified());
}

#[test]
fn test_twod_character_decimation_area_law() {
    let alpha = rat(1, 5);
    // Abelian (dim R = 1): (1/5)^Area
    for a in 1..=4 {
        let dec = twod_character_decimation_area_law(1, &alpha, a).unwrap();
        let expected = rat(1, 5i64.pow(a as u32));
        assert_eq!(dec, expected);
    }

    // Non-abelian (dim R = 2): 2^{1 - Area} * (1/5)^Area
    let dec1 = twod_character_decimation_area_law(2, &alpha, 1).unwrap();
    assert_eq!(dec1, rat(1, 5));

    let dec2 = twod_character_decimation_area_law(2, &alpha, 2).unwrap();
    assert_eq!(dec2, rat(1, 50));

    let dec3 = twod_character_decimation_area_law(2, &alpha, 3).unwrap();
    assert_eq!(dec3, rat(1, 500));

    assert!(twod_character_decimation_area_law(0, &alpha, 1).is_err());
    assert!(twod_character_decimation_area_law(1, &alpha, 0).is_err());
}

#[test]
fn test_crate_root_inventory_integrity() {
    assert!(crate_root_inventory_holds().is_ok());
}

#[test]
fn test_master_witness_passes() {
    assert_eq!(verify_fqcd_strong_coupling_area_law_witness(), Ok(true));
}
