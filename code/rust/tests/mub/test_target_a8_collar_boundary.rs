//! Integration and unit tests for Target A8: Collar-Boundary Overlap & Circulation Chaining Engine.
//!
//! AuthorityEffect: None.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

use tfqm_mub::native::exact::mub6_collar_boundary::{
    certify_collar_boundary_overlap, collar_margin, critical_mesh_step, evaluate_boundary_overlap,
    interface_margin, karlsson_volume_margin, BoundaryOverlapPartition, CollarBoundaryBox3D,
    CollarBoundaryConfig, CollarBoundaryError, CollarBoundaryReceipt, InterfaceCycle,
    InterfaceCycleChain, InterfaceTransition, DIM_2D, DIM_3D,
};
use tfqm_mub::native::exact::mub6_constants::{base_gap, delta_certified, lipschitz_bound};
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_number_theory::rational::rq;

#[test]
fn test_canonical_constants_exact_values() {
    let bg = base_gap();
    let lb = lipschitz_bound();
    let ms = delta_certified();
    let cm = collar_margin();
    let km = karlsson_volume_margin();
    let im = interface_margin();
    let crit = critical_mesh_step();

    // Check dimensional constants
    assert_eq!(DIM_2D, 2);
    assert_eq!(DIM_3D, 3);

    // 1. Check exact fractions
    assert_eq!(bg, rq(37249, 90000));
    assert_eq!(lb, rq(85, 9));
    assert_eq!(ms, rq(1, 1000));
    assert_eq!(cm, rq(12133, 30000));
    assert_eq!(km, rq(37249, 90000));
    assert_eq!(im, rq(12133, 30000));
    assert_eq!(crit, rq(37249, 850000));

    // 2. Collar margin equality: base_gap - lipschitz_bound * mesh_step
    let erosion = &lb * &ms;
    assert_eq!(erosion, rq(17, 1800));
    assert_eq!(&bg - &erosion, cm);
    assert!(cm > BigRational::zero());

    // 3. Karlsson volume margin positivity
    assert!(km > BigRational::zero());

    // 4. Interface margin is min(collar_margin, karlsson_volume_margin)
    assert_eq!(im, if cm <= km { cm.clone() } else { km.clone() });
    assert!(im > BigRational::zero());

    // 5. Mesh step strictly smaller than critical threshold
    assert!(ms < crit);
}

#[test]
fn test_boundary_overlap_canonical_evaluation() {
    let config = CollarBoundaryConfig::canonical(10);
    let partition = evaluate_boundary_overlap(&config)
        .expect("Canonical boundary overlap evaluation must succeed");

    assert_eq!(partition.divisions_xy, 10);
    assert_eq!(partition.boxes.len(), 100);
    assert_eq!(partition.overlap_box_count, 0);
    assert!(partition.boundary_gap_empty);
    assert!(partition.all_margins_positive);
    assert_eq!(partition.min_margin, rq(12133, 30000));

    // Volume conservation: 1 * 1 * (1 / 1000) = 1 / 1000
    assert_eq!(partition.total_volume, rq(1, 1000));
    assert!(partition.verify_partition().is_ok());

    // Point containment tests
    let inside_pt = [rq(1, 20), rq(3, 20), rq(1, 2000)];
    let found = partition.find_box(&inside_pt);
    assert!(found.is_some());
    let b = found.unwrap();
    assert!(b.contains_point(&inside_pt));
    assert_eq!(b.effective_margin, rq(12133, 30000));
    assert!(b.collar_certified);
    assert!(!b.karlsson_certified);
    assert!(!b.is_overlap());

    let outside_pt = [rq(3, 2), rq(1, 2), rq(1, 2000)];
    assert!(partition.find_box(&outside_pt).is_none());
}

#[test]
fn test_boundary_overlap_extended_overlapping_layers() {
    // Overlapping configuration where Karlsson exterior begins at z = 9/10000 < 1/1000
    let karlsson_min = rq(9, 10000);
    let config = CollarBoundaryConfig::overlapping(10, karlsson_min);
    let partition =
        evaluate_boundary_overlap(&config).expect("Overlapping boundary evaluation must succeed");

    // 10x10 * 2 layers = 200 boxes
    assert_eq!(partition.boxes.len(), 200);
    assert_eq!(partition.overlap_box_count, 100);
    assert!(partition.boundary_gap_empty);
    assert!(partition.all_margins_positive);
    assert_eq!(partition.min_margin, rq(12133, 30000));

    // Total volume should still equal 1/1000
    assert_eq!(partition.total_volume, rq(1, 1000));
    assert!(partition.verify_partition().is_ok());

    // Check layer 1 (collar only) vs layer 2 (overlap)
    let collar_only = &partition.boxes[0];
    assert_eq!(collar_only.z_range, (BigRational::zero(), rq(9, 10000)));
    assert!(collar_only.collar_certified);
    assert!(!collar_only.karlsson_certified);

    let overlap_box = &partition.boxes[1];
    assert_eq!(overlap_box.z_range, (rq(9, 10000), rq(1, 1000)));
    assert!(overlap_box.collar_certified);
    assert!(overlap_box.karlsson_certified);
    assert!(overlap_box.is_overlap());
}

#[test]
fn test_canonical_interface_cycle_holonomy_and_circulation() {
    let cycle = InterfaceCycle::canonical(0);

    // 1. Transition holonomy W = g01 * g12 * g20
    // g01 = diag(1, zeta^8, zeta^16), g12 = diag(1, zeta^16, zeta^8), g20 = I_3
    // W = diag(1, zeta^24, zeta^24) = I_3
    assert!(
        cycle.is_cocycle_trivial(),
        "Canonical interface cycle cocycle must be trivial (W = I_3)"
    );

    // 2. Solve Network Simplex circulation with scale 90000
    let cert = cycle
        .verify_circulation(90000)
        .expect("Circulation verification must succeed");

    assert!(cert.is_cocycle_trivial);
    assert_eq!(cert.cycle_index, 0);

    // Expected cochain:
    // d0 = 12133/30000 * 90000 = 36399
    // d1 = 12133/30000 * 90000 = 36399
    // d2 = 37249/90000 * 90000 = 37249
    assert_eq!(cert.edge_cochain, vec![36399, 36399, 37249]);
    let expected_net: i128 = 36399 + 36399 + 37249;
    assert_eq!(cert.net_circulation, expected_net);
    assert_eq!(cert.net_circulation, 110047);
    assert!(cert.net_circulation > 0);

    // Phi_1 objective must be >= net circulation
    assert!(cert.phi1_objective >= cert.net_circulation);
    assert_eq!(cert.phi1_objective, 110047);

    // Coboundary sum around 3-cycle vanishes identically
    assert_eq!(cert.coboundary_sum, 0);
    assert!(cert.circulation_conserved);

    // Dual gap zero
    assert!(cert.dual_gap_zero);
    assert!(cert.certified);
}

#[test]
fn test_twisted_interface_cycle_holonomy_and_circulation() {
    let cycle = InterfaceCycle::twisted(1);

    // Permutations: g01 = (1, 0, 2), g12 = (0, 2, 1), g20 = id
    // Product W is non-trivial permutation
    assert!(
        !cycle.is_cocycle_trivial(),
        "Twisted interface cycle cocycle must be non-trivial"
    );

    let cert = cycle
        .verify_circulation(90000)
        .expect("Circulation verification on twisted cycle must succeed");

    assert!(!cert.is_cocycle_trivial);
    assert_eq!(cert.coboundary_sum, 0);
    assert!(cert.circulation_conserved);
    assert!(cert.dual_gap_zero);
    assert!(cert.certified);
    assert!(cert.phi1_objective >= cert.net_circulation);
    assert!(cert.net_circulation > 0);
}

#[test]
fn test_interface_cycle_chain_verification() {
    let chain = InterfaceCycleChain::canonical_chain(5);
    assert_eq!(chain.cycles.len(), 5);

    // Compound holonomy of trivial cycles is identity
    let w_compound = chain.compound_holonomy();
    let eye = tfqm_mub::native::exact::mub6_matrix6::eye3();
    assert_eq!(w_compound, eye);

    let certs = chain
        .verify_all(90000)
        .expect("Verification of interface cycle chain must succeed");

    assert_eq!(certs.len(), 5);
    for (i, c) in certs.iter().enumerate() {
        assert_eq!(c.cycle_index, i);
        assert!(c.certified);
        assert!(c.dual_gap_zero);
        assert!(c.circulation_conserved);
        assert_eq!(c.coboundary_sum, 0);
        assert_eq!(c.net_circulation, 110047);
        assert!(c.phi1_objective >= 110047);
    }
}

#[test]
fn test_gauge_potential_coboundary_invariance_adversarial() {
    // Test 50 adversarial 0-cochains alpha on the 3-cycle
    let cycle = InterfaceCycle::canonical(0);
    let (boundary, omega) = cycle
        .build_boundary_and_cochain(90000)
        .expect("canonical defects clear the denominator at scale 90000");
    let net_circulation: i128 = omega.iter().sum();

    for i in 0..50 {
        let alpha = [
            (i as i128) * 179 - 1234,
            (i as i128) * (-347) + 5678,
            (i as i128) * 491 - 999,
        ];

        // Evaluate (d alpha)_e = alpha[head] - alpha[tail]
        let d_alpha_sum: i128 = boundary
            .edges
            .iter()
            .map(|e| alpha[e.head] - alpha[e.tail])
            .sum();

        // Exact vanishing of circulation coboundary
        assert_eq!(
            d_alpha_sum, 0,
            "Coboundary sum must vanish identically for any potential alpha"
        );

        // Modified edge cochain omega' = omega - d alpha
        let mut z = Vec::with_capacity(3);
        for (idx, e) in boundary.edges.iter().enumerate() {
            let diff = alpha[e.head] - alpha[e.tail];
            z.push(omega[idx] - diff);
        }

        // Net circulation sum(z) = sum(omega) - sum(d alpha) = sum(omega)
        let z_sum: i128 = z.iter().sum();
        assert_eq!(
            z_sum, net_circulation,
            "Gauge potential cannot alter net cycle circulation"
        );
    }
}

#[test]
fn test_collar_boundary_receipt_generation_and_serde() {
    let receipt = certify_collar_boundary_overlap(10, 3, 90000)
        .expect("Certification and receipt generation must succeed");

    assert_eq!(
        receipt.schema_version,
        "omega.mub.target-a8-collar-boundary.v1"
    );
    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(receipt.base_gap, "37249/90000");
    assert_eq!(receipt.lipschitz_bound, "85/9");
    assert_eq!(receipt.mesh_step, "1/1000");
    assert_eq!(receipt.collar_margin, "12133/30000");
    assert_eq!(receipt.karlsson_volume_margin, "37249/90000");
    assert_eq!(receipt.interface_margin, "12133/30000");
    assert_eq!(receipt.boundary_depth, "1/1000");
    assert!(!receipt.overlap_region_certified);
    assert!(receipt.boundary_gap_empty);
    assert_eq!(receipt.num_interface_boxes, 100);
    assert_eq!(receipt.total_interface_volume, "1/1000");
    assert_eq!(receipt.num_interface_cycles, 3);
    assert!(receipt.all_cycles_positive_circulation);
    assert_eq!(receipt.min_cycle_phi1, 110047);
    assert!(receipt.coboundary_sum_zero);
    assert!(receipt.dual_gap_zero);
    assert!(receipt.verified);

    // Test JSON round-trip serialization
    let json_str = receipt
        .to_json_string()
        .expect("JSON serialization must succeed");
    assert!(json_str.contains("omega.mub.target-a8-collar-boundary.v1"));
    assert!(json_str.contains("12133/30000"));

    let deserialized =
        CollarBoundaryReceipt::from_json_str(&json_str).expect("JSON deserialization must succeed");
    assert_eq!(receipt, deserialized);
}

#[test]
fn test_negative_controls_boundary_gap_detection() {
    // Gap scenario: collar reaches only to z = 1/2000, while Karlsson begins at z = 1/1000.
    // An uncertified gap of width (1/1000 - 1/2000) = 1/2000 exists!
    let gap_config = CollarBoundaryConfig {
        collar_max_depth: rq(1, 2000),
        karlsson_min_depth: rq(1, 1000),
        divisions_xy: 10,
    };

    let result = evaluate_boundary_overlap(&gap_config);
    assert!(matches!(
        result,
        Err(CollarBoundaryError::BoundaryGapDetected { gap_lo, gap_hi })
        if gap_lo == rq(1, 2000) && gap_hi == rq(1, 1000)
    ));
}

#[test]
fn test_negative_controls_invalid_parameters() {
    // Zero divisions_xy
    let bad_div = CollarBoundaryConfig {
        collar_max_depth: rq(1, 1000),
        karlsson_min_depth: rq(1, 1000),
        divisions_xy: 0,
    };
    assert!(matches!(
        evaluate_boundary_overlap(&bad_div),
        Err(CollarBoundaryError::InvalidParameter(_))
    ));

    // Zero or negative depths
    let bad_depth = CollarBoundaryConfig {
        collar_max_depth: BigRational::zero(),
        karlsson_min_depth: rq(1, 1000),
        divisions_xy: 10,
    };
    assert!(matches!(
        evaluate_boundary_overlap(&bad_depth),
        Err(CollarBoundaryError::InvalidParameter(_))
    ));

    let neg_depth = CollarBoundaryConfig {
        collar_max_depth: rq(-1, 1000),
        karlsson_min_depth: rq(1, 1000),
        divisions_xy: 10,
    };
    assert!(matches!(
        evaluate_boundary_overlap(&neg_depth),
        Err(CollarBoundaryError::InvalidParameter(_))
    ));
}

#[test]
fn test_negative_controls_nonpositive_circulation_cycle() {
    // Create an interface cycle with non-positive edge defects
    let g01 = InterfaceTransition::identity(0, 1, BigRational::zero());
    let g12 = InterfaceTransition::identity(1, 2, rq(-1, 10));
    let g20 = InterfaceTransition::identity(2, 0, rq(-2, 10));
    let bad_cycle = InterfaceCycle::new(99, "bad_cycle".to_string(), [g01, g12, g20]);

    let res = bad_cycle.verify_circulation(90000);
    assert!(matches!(
        res,
        Err(CollarBoundaryError::NonPositiveCirculation {
            cycle_index: 99,
            ..
        })
    ));
}

#[test]
fn test_ast_zero_float_discipline() {
    let src = include_str!("../../omega_mub/src/native/mub6_collar_boundary.rs");
    assert!(
        !src.contains("f32"),
        "mub6_collar_boundary.rs must contain zero f32 occurrences"
    );
    assert!(
        !src.contains("f64"),
        "mub6_collar_boundary.rs must contain zero f64 occurrences"
    );
}

#[test]
fn test_depth_beyond_the_lipschitz_radius_is_refused() {
    let config = CollarBoundaryConfig {
        collar_max_depth: rq(37249, 425000),
        karlsson_min_depth: rq(37249, 425000),
        divisions_xy: 1,
    };
    assert!(matches!(
        evaluate_boundary_overlap(&config),
        Err(CollarBoundaryError::InvalidParameter(_))
    ));
}

#[test]
fn test_empty_cover_and_duplicated_half_boxes_are_refused() {
    let mut partition = evaluate_boundary_overlap(&CollarBoundaryConfig::canonical(1))
        .expect("canonical partition");
    partition.boxes.clear();
    assert!(partition.verify_partition().is_err());

    let delta = rq(1, 1000);
    let margin = rq(12133, 30000);
    let half = CollarBoundaryBox3D {
        index: 0,
        bounds_xy: [
            (BigRational::zero(), rq(1, 2)),
            (BigRational::zero(), BigRational::one()),
        ],
        z_range: (BigRational::zero(), delta.clone()),
        collar_certified: true,
        collar_margin: margin.clone(),
        karlsson_certified: false,
        karlsson_margin: BigRational::zero(),
        effective_margin: margin.clone(),
    };
    let duplicate = BoundaryOverlapPartition {
        divisions_xy: 1,
        collar_max_depth: delta.clone(),
        karlsson_min_depth: delta.clone(),
        boxes: vec![half.clone(), half],
        total_volume: delta,
        min_margin: margin,
        overlap_box_count: 0,
        boundary_gap_empty: true,
        all_margins_positive: true,
    };
    assert!(duplicate.verify_partition().is_err());
}

#[test]
fn test_nonintegral_and_overflowing_cochains_are_refused() {
    let cycle = |defects: [BigRational; 3]| {
        InterfaceCycle::new(
            0,
            "hostile".to_string(),
            [
                InterfaceTransition::identity(0, 1, defects[0].clone()),
                InterfaceTransition::identity(1, 2, defects[1].clone()),
                InterfaceTransition::identity(2, 0, defects[2].clone()),
            ],
        )
    };
    assert!(cycle([rq(4, 3), rq(-2, 3), rq(-2, 3)])
        .build_boundary_and_cochain(1)
        .is_err());
    assert!(cycle([rq(1, 3), rq(1, 3), rq(1, 3)])
        .build_boundary_and_cochain(1)
        .is_err());
    let huge = BigRational::from_integer(-BigInt::from(2).pow(200));
    assert!(cycle([huge, BigRational::one(), BigRational::one()])
        .build_boundary_and_cochain(1)
        .is_err());
}

#[test]
fn test_zero_cycle_campaign_is_refused() {
    assert!(matches!(
        certify_collar_boundary_overlap(1, 0, 90000),
        Err(CollarBoundaryError::InvalidParameter(_))
    ));
}
