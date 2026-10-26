//! Integration tests for Smith Normal Form (SNF) & Integral Torsion Extraction over Z.
//!
//! AuthorityEffect: None. GenesisEffect: None.

use mssn_stage_024::smith_normal_form::{compute_integral_homology, IntegerMatrix};

#[test]
fn test_rp2_2_torsion_extraction() {
    // Cellular chain complex for Real Projective Plane RP^2:
    // C_2 = Z^1, C_1 = Z^1, C_0 = Z^1
    // d_1 : C_1 -> C_0 is 0
    // d_2 : C_2 -> C_1 is [2] (the 2-cell attaches with degree 2 along the 1-cell)
    let a1 = IntegerMatrix::from_dense(1, 1, &[0]);
    let a2 = IntegerMatrix::from_dense(1, 1, &[2]);

    let receipt = compute_integral_homology("RealProjectivePlane_RP2", 1, &a1, &a2)
        .expect("RP^2 homology computation must succeed");

    assert_eq!(receipt.status, "PASS");
    assert_eq!(receipt.betti_number, 0, "beta_1(RP^2) = 0");
    assert_eq!(receipt.invariant_factors, vec![2]);
    assert_eq!(receipt.torsion_subgroups, vec!["Z/2Z"]);
    assert!(!receipt.is_torsion_free);

    let json = serde_json::to_string_pretty(&receipt).expect("Receipt must serialize");
    assert!(json.contains("\"Z/2Z\""));
}

#[test]
fn test_klein_bottle_torsion_extraction() {
    // Cellular chain complex for Klein Bottle K^2:
    // C_2 = Z^1, C_1 = Z^2, C_0 = Z^1
    // d_1 : C_1 -> C_0 is [0, 0]
    // d_2 : C_2 -> C_1 is [[2], [0]] (attaching map: a + b + a - b = 2a)
    let a1 = IntegerMatrix::from_dense(1, 2, &[0, 0]);
    let a2 = IntegerMatrix::from_dense(2, 1, &[2, 0]);

    let receipt = compute_integral_homology("KleinBottle_K2", 1, &a1, &a2)
        .expect("Klein Bottle homology computation must succeed");

    assert_eq!(receipt.status, "PASS");
    assert_eq!(receipt.betti_number, 1, "beta_1(K^2) = 1");
    assert_eq!(receipt.invariant_factors, vec![2]);
    assert_eq!(receipt.torsion_subgroups, vec!["Z/2Z"]);
    assert!(!receipt.is_torsion_free);
}

#[test]
fn test_torus_torsion_free() {
    // Cellular chain complex for Torus T^2:
    // C_2 = Z^1, C_1 = Z^2, C_0 = Z^1
    // d_1 : C_1 -> C_0 is [0, 0]
    // d_2 : C_2 -> C_1 is [[0], [0]] (attaching map: a + b - a - b = 0)
    let a1 = IntegerMatrix::from_dense(1, 2, &[0, 0]);
    let a2 = IntegerMatrix::from_dense(2, 1, &[0, 0]);

    let receipt = compute_integral_homology("Torus_T2", 1, &a1, &a2)
        .expect("Torus homology computation must succeed");

    assert_eq!(receipt.status, "PASS");
    assert_eq!(receipt.betti_number, 2, "beta_1(T^2) = 2");
    assert!(receipt.is_torsion_free);
    assert!(receipt.torsion_subgroups.is_empty());
}

#[test]
fn test_sphere_torsion_free() {
    // 2-Sphere S^2:
    // C_2 = Z^1, C_1 = Z^0 (or minimal triangulation), H_1 = 0
    let a1 = IntegerMatrix::from_dense(1, 1, &[1]);
    let a2 = IntegerMatrix::from_dense(1, 1, &[0]);

    let receipt = compute_integral_homology("Sphere_S2", 1, &a1, &a2)
        .expect("Sphere homology computation must succeed");

    assert_eq!(receipt.status, "PASS");
    assert_eq!(receipt.betti_number, 0, "beta_1(S^2) = 0");
    assert!(receipt.is_torsion_free);
}

#[test]
fn test_boundary_nilpotence_violation_fails_closed() {
    // Non-zero composition: d_1 * d_2 != 0
    let a1 = IntegerMatrix::from_dense(1, 1, &[1]);
    let a2 = IntegerMatrix::from_dense(1, 1, &[1]);

    let err = compute_integral_homology("InvalidComplex", 1, &a1, &a2)
        .expect_err("Non-nilpotent boundary operator must fail closed");

    assert!(err.contains("Boundary nilpotence violation"));
}
