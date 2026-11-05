// Executable finite evidence; AuthorityEffect: None.
//! Integration tests for the 11 WDP foundational bridges in Rust.

use std::collections::HashMap;
use num_rational::BigRational;
use num_traits::Zero;

use wdp_finite_witness::foundational_bridges::*;

#[test]
fn test_bridge_1_inscription_and_marks() {
    let e = empty_inscription();
    assert_eq!(e.depth, 0);
    assert_eq!(admit_mark(e), "mark_0");

    let n1 = e.nest();
    assert_eq!(n1.depth, 1);
    assert_eq!(admit_mark(n1), "mark_1");

    let n2 = n1.nest();
    assert_eq!(n2.depth, 2);
    assert_eq!(admit_mark(n2), "mark_2");

    let diff = apartness_witness(e, n1);
    assert!(diff.is_ok());
    assert_eq!(diff.unwrap(), true);

    let same = apartness_witness(n1, Inscription::new(1));
    assert!(same.is_err());
}

#[test]
fn test_bridge_2_marks_to_cochains() {
    assert_eq!(bool_xor(true, true), false);
    assert_eq!(bool_xor(true, false), true);
    assert_eq!(bool_xor(false, true), true);
    assert_eq!(bool_xor(false, false), false);

    let f = |node: &str| match node {
        "A" => true,
        "B" => false,
        "C" => true,
        _ => false,
    };

    assert_eq!(bool_d0(f, "A", "B"), true);
    assert_eq!(bool_d0(f, "A", "C"), false);
    assert_eq!(bool_d0(f, "B", "C"), true);

    let v1 = verify_triangle_coboundary_zero(f, "A", "B", "C");
    assert!(v1.is_ok());
    assert_eq!(v1.unwrap(), true);
}

#[test]
fn test_bridge_3_genesis_histories_to_observers() {
    let t1 = FiniteTransducer::new(2, 2, vec![vec![0, 1], vec![1, 0]]).unwrap();
    assert_eq!(t1.step(0, 0).unwrap(), 0);
    assert_eq!(t1.step(0, 1).unwrap(), 1);
    assert_eq!(t1.step(1, 1).unwrap(), 0);

    let t2 = FiniteTransducer::new(2, 1, vec![vec![1], vec![0]]).unwrap();
    let prod = product_transducer(&t1, &t2).unwrap();
    assert_eq!(prod.num_states, 4);
    assert_eq!(prod.num_inputs, 2);
}

#[test]
fn test_bridge_4_multiplicity_and_probability() {
    let mut counts = HashMap::new();
    counts.insert("heads".to_string(), 3);
    counts.insert("tails".to_string(), 7);

    let dist = MultiplicityDistribution::from_counts(counts).unwrap();
    assert_eq!(dist.total, 10);
    assert_eq!(dist.probability("heads"), BigRational::new(3.into(), 10.into()));
    assert_eq!(dist.probability("tails"), BigRational::new(7.into(), 10.into()));
    assert_eq!(dist.probability("edge"), BigRational::zero());

    let union_prob = dist.disjoint_union_probability(&["heads", "tails"]).unwrap();
    assert_eq!(union_prob, BigRational::from_integer(1.into()));

    let dup = dist.disjoint_union_probability(&["heads", "heads"]);
    assert!(dup.is_err());
}

#[test]
fn test_bridge_5_evaluation_status() {
    assert_eq!(
        evaluate_report_claim(false, true),
        EvaluationStatus::OutsideProfile
    );
    assert_eq!(
        evaluate_report_claim(true, true),
        EvaluationStatus::Accept
    );
    assert_eq!(
        evaluate_report_claim(true, false),
        EvaluationStatus::Reject
    );
}

#[test]
fn test_bridge_6_authority_effect_firewall() {
    let good_receipt = MathematicalReceipt {
        receipt_id: "rcpt_001".to_string(),
        claim_id: "claim_A".to_string(),
        verified: true,
        authority_effect: AuthorityEffect::None,
    };
    assert!(check_no_authority_effect(&good_receipt).is_ok());

    let bad_receipt = MathematicalReceipt {
        receipt_id: "rcpt_002".to_string(),
        claim_id: "claim_B".to_string(),
        verified: true,
        authority_effect: AuthorityEffect::MintsAuthority,
    };
    assert!(check_no_authority_effect(&bad_receipt).is_err());
}

#[test]
fn test_bridge_7_triangle_parity() {
    let (d_ab, d_bc, d_ac, parity) = compute_triangle_mark_differences(("mark_0", "mark_1", "mark_2"));
    assert!(d_ab);
    assert!(d_bc);
    assert!(d_ac);
    assert_eq!(parity, true);

    let (_, _, _, deg_parity) = compute_triangle_mark_differences(("mark_0", "mark_0", "mark_1"));
    assert_eq!(deg_parity, false);
}

#[test]
fn test_bridge_8_rational_l1_minimizer() {
    let p1 = vec![BigRational::from_integer(1.into()), BigRational::from_integer(2.into())];
    let p2 = vec![BigRational::new(1.into(), 2.into()), BigRational::new(1.into(), 2.into())];
    let p3 = vec![BigRational::from_integer(3.into()), BigRational::from_integer(0.into())];

    let (best_pt, best_val) = find_rational_l1_minimizer(&[p1, p2.clone(), p3]).unwrap();
    assert_eq!(best_pt, p2);
    assert_eq!(best_val, BigRational::from_integer(1.into()));

    let empty: Vec<Vec<BigRational>> = vec![];
    assert!(find_rational_l1_minimizer(&empty).is_err());
}

#[test]
fn test_bridge_9_flat_locus_curvature() {
    let d_flat = vec![
        vec![BigRational::zero(), BigRational::from_integer(1.into())],
        vec![BigRational::zero(), BigRational::zero()],
    ];
    assert!(verify_flat_locus_curvature(&d_flat).is_ok());

    let d_nonflat = vec![
        vec![BigRational::zero(), BigRational::from_integer(1.into())],
        vec![BigRational::from_integer(1.into()), BigRational::zero()],
    ];
    assert!(verify_flat_locus_curvature(&d_nonflat).is_err());
}

#[test]
fn test_bridge_10_frustrated_spin_cycle() {
    let res_odd = solve_frustrated_spin_cycle(3);
    assert!(res_odd.is_err());

    let res_even = solve_frustrated_spin_cycle(4);
    assert!(res_even.is_ok());
    let sol = res_even.unwrap();
    assert_eq!(sol.len(), 4);
    assert_eq!(sol.get("s_0").copied(), Some(false));
    assert_eq!(sol.get("s_1").copied(), Some(true));
}

#[test]
fn test_bridge_11_deterministic_retention() {
    let det_transitions = vec![
        ("s0", "0", "s0"),
        ("s0", "1", "s1"),
        ("s1", "0", "s0"),
        ("s1", "1", "s1"),
    ];
    assert!(verify_deterministic_retention(&det_transitions).is_ok());

    let non_det_transitions = vec![
        ("s0", "0", "s0"),
        ("s0", "0", "s1"),
    ];
    assert!(verify_deterministic_retention(&non_det_transitions).is_err());
}
