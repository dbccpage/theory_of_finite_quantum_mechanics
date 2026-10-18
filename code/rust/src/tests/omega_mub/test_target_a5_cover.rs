//! Comprehensive unit and integration test suite for Target A5:
//! R2: Exact Rational Partition Verifier & Bisection Aggregator (`mub6_cover_tree.rs`).
//!
//! AuthorityEffect: None.

use std::fs;
use std::path::Path;

use num_rational::BigRational;
use num_traits::{One, Zero};
use syn::visit::Visit;

use omega_certifiers::phi1_certifier::Phi1Verifier;
use omega_mub::omega_native::exact::mub6_cover_tree::{
    certify_all_leaves_with_margin, certify_leaf_with_margin, certify_leaf_with_phi1,
    certify_leaf_with_phi1_solution, certify_leaf_with_sdp, check_partition_cover,
    verify_cover_obstruction, BisectionTree, CoverObstructionReceipt, CoverTreeError,
    RationalBox5D, DIM_5D,
};
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_quad_sdp::solve_quad_sdp_certificate;
use omega_number_theory::rational::rq;
use omega_solvers::solver_lp_phi1_boundary::{solve_l1_boundary, Boundary1, BoundaryEdge};

// ============================================================================
// 1. STRICT ZERO-FLOAT DISCIPLINE AST & SYNTACTIC AUDIT
// ============================================================================

struct FloatAuditVisitor {
    found_floats: Vec<String>,
}

impl<'ast> Visit<'ast> for FloatAuditVisitor {
    fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
        for seg in &node.path.segments {
            let ident_str = seg.ident.to_string();
            if ident_str == "f32" || ident_str == "f64" {
                self.found_floats
                    .push(format!("Forbidden float type: {}", ident_str));
            }
        }
        syn::visit::visit_type_path(self, node);
    }

    fn visit_lit_float(&mut self, node: &'ast syn::LitFloat) {
        self.found_floats
            .push(format!("Forbidden float literal: {}", node));
        syn::visit::visit_lit_float(self, node);
    }
}

#[test]
fn test_strict_zero_float_discipline_ast() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let target_file = Path::new(manifest_dir)
        .join("src")
        .join("omega_native")
        .join("mub6_cover_tree.rs");

    let source = fs::read_to_string(&target_file)
        .unwrap_or_else(|e| panic!("Failed to read {}: {}", target_file.display(), e));

    let syntax_tree = syn::parse_file(&source)
        .unwrap_or_else(|e| panic!("Failed to parse {}: {}", target_file.display(), e));

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.is_empty(),
        "ZERO-FLOAT DISCIPLINE VIOLATION in mub6_cover_tree.rs: {:?}",
        visitor.found_floats
    );
}

// ============================================================================
// 2. RATIONAL BOX 5D UNIT TESTS
// ============================================================================

#[test]
fn test_rational_box_5d_unit_cube_and_properties() {
    let cube = RationalBox5D::unit_cube();
    assert_eq!(cube.volume(), BigRational::one());

    // Containment of interior and boundary points
    let interior_pt = [rq(1, 2), rq(1, 3), rq(3, 4), rq(1, 5), rq(7, 10)];
    assert!(cube.contains_point(&interior_pt));

    let origin = [rq(0, 1), rq(0, 1), rq(0, 1), rq(0, 1), rq(0, 1)];
    assert!(cube.contains_point(&origin));

    let corner = [rq(1, 1), rq(1, 1), rq(1, 1), rq(1, 1), rq(1, 1)];
    assert!(cube.contains_point(&corner));

    // Points outside along each dimension
    for d in 0..DIM_5D {
        let mut pt_below = interior_pt.clone();
        pt_below[d] = rq(-1, 100);
        assert!(
            !cube.contains_point(&pt_below),
            "dim {d} below must be outside"
        );

        let mut pt_above = interior_pt.clone();
        pt_above[d] = rq(101, 100);
        assert!(
            !cube.contains_point(&pt_above),
            "dim {d} above must be outside"
        );
    }
}

#[test]
fn test_rational_box_5d_invalid_bounds_rejected() {
    let mut bounds = std::array::from_fn(|_| (rq(0, 1), rq(1, 1)));

    // lo == hi (degenerate interval)
    bounds[2] = (rq(1, 2), rq(1, 2));
    assert!(matches!(
        RationalBox5D::new(bounds.clone()),
        Err(CoverTreeError::InvalidInterval { dim: 2, .. })
    ));

    // lo > hi (inverted interval)
    bounds[2] = (rq(3, 4), rq(1, 2));
    assert!(matches!(
        RationalBox5D::new(bounds),
        Err(CoverTreeError::InvalidInterval { dim: 2, .. })
    ));
}

#[test]
fn test_rational_box_5d_subdivide_and_bisect() {
    let cube = RationalBox5D::unit_cube();
    let cut = rq(1, 3);
    let (left, right) = cube.subdivide(0, &cut).expect("valid subdivision");

    assert_eq!(left.bounds[0], (rq(0, 1), rq(1, 3)));
    assert_eq!(right.bounds[0], (rq(1, 3), rq(1, 1)));
    assert_eq!(left.volume(), rq(1, 3));
    assert_eq!(right.volume(), rq(2, 3));
    assert_eq!(left.volume() + right.volume(), cube.volume());

    // Out of bounds cuts
    assert!(matches!(
        cube.subdivide(0, &rq(0, 1)),
        Err(CoverTreeError::CutOutOfBounds { .. })
    ));
    assert!(matches!(
        cube.subdivide(0, &rq(1, 1)),
        Err(CoverTreeError::CutOutOfBounds { .. })
    ));
    assert!(matches!(
        cube.subdivide(0, &rq(3, 2)),
        Err(CoverTreeError::CutOutOfBounds { .. })
    ));
    assert!(matches!(
        cube.subdivide(0, &rq(-1, 2)),
        Err(CoverTreeError::CutOutOfBounds { .. })
    ));

    // Invalid dimension
    assert!(matches!(
        cube.subdivide(5, &rq(1, 2)),
        Err(CoverTreeError::InvalidDimension(5))
    ));

    // Midpoint bisection
    let (b_left, b_right) = cube.bisect(3).expect("valid bisect");
    assert_eq!(b_left.bounds[3], (rq(0, 1), rq(1, 2)));
    assert_eq!(b_right.bounds[3], (rq(1, 2), rq(1, 1)));
    assert_eq!(b_left.volume(), rq(1, 2));
    assert_eq!(b_right.volume(), rq(1, 2));
}

// ============================================================================
// 3. VALID 5D BISECTION COVERS (32 CELLS AND DEEPER TREES)
// ============================================================================

/// Recursively builds a uniform bisection tree bisecting dimensions 0..split_depth.
fn build_uniform_bisection_tree(
    rbox: &RationalBox5D,
    split_dim: usize,
    max_split_dim: usize,
) -> BisectionTree {
    if split_dim >= max_split_dim {
        BisectionTree::leaf(rbox.clone(), None, None)
    } else {
        let mid = rbox.midpoint(split_dim).expect("valid midpoint");
        let (left_box, right_box) = rbox.subdivide(split_dim, &mid).expect("valid split");
        let left_tree = build_uniform_bisection_tree(&left_box, split_dim + 1, max_split_dim);
        let right_tree = build_uniform_bisection_tree(&right_box, split_dim + 1, max_split_dim);
        BisectionTree::split(split_dim, mid, left_tree, right_tree)
    }
}

#[test]
fn test_5d_bisection_cover_32_cells_and_volume_conservation() {
    let domain = RationalBox5D::unit_cube();
    // Splitting all 5 dimensions 0..5 yields exactly 2^5 = 32 cells
    let tree = build_uniform_bisection_tree(&domain, 0, 5);

    assert_eq!(tree.leaf_count(), 32);
    assert_eq!(tree.depth(), 5);

    let leaves = tree.leaves();
    assert_eq!(leaves.len(), 32);

    let expected_leaf_vol = rq(1, 32);
    for leaf in &leaves {
        assert_eq!(leaf.volume(), expected_leaf_vol);
    }

    assert_eq!(tree.total_volume(), BigRational::one());
    assert_eq!(tree.total_volume(), domain.volume());

    // Check exact partition cover
    let cover_res = check_partition_cover(&tree, &domain);
    assert!(
        cover_res.is_ok(),
        "Partition cover check failed: {:?}",
        cover_res.err()
    );
}

#[test]
fn test_5d_deeper_bisection_cover_64_cells() {
    let domain = RationalBox5D::unit_cube();
    // Build 32-cell tree first, then further split dimension 0 of every leaf -> 64 cells
    let tree_32 = build_uniform_bisection_tree(&domain, 0, 5);

    fn subdivide_leaves_at_dim(node: BisectionTree, dim: usize) -> BisectionTree {
        match node {
            BisectionTree::Leaf { box_5d, .. } => {
                let mid = box_5d.midpoint(dim).expect("midpoint");
                let (l, r) = box_5d.subdivide(dim, &mid).expect("subdivide");
                BisectionTree::split(
                    dim,
                    mid,
                    BisectionTree::leaf(l, None, None),
                    BisectionTree::leaf(r, None, None),
                )
            }
            BisectionTree::Split {
                dim: sdim,
                cut,
                left,
                right,
            } => BisectionTree::split(
                sdim,
                cut,
                subdivide_leaves_at_dim(*left, dim),
                subdivide_leaves_at_dim(*right, dim),
            ),
        }
    }

    let tree_64 = subdivide_leaves_at_dim(tree_32, 0);
    assert_eq!(tree_64.leaf_count(), 64);
    assert_eq!(tree_64.depth(), 6);
    assert_eq!(tree_64.total_volume(), BigRational::one());

    let cover_res = check_partition_cover(&tree_64, &domain);
    assert!(
        cover_res.is_ok(),
        "64-cell cover check failed: {:?}",
        cover_res.err()
    );
}

#[test]
fn test_asymmetric_rational_cuts_volume_conservation() {
    // Non-uniform rational partition with asymmetric cuts
    let domain = RationalBox5D::unit_cube();

    // Cut dim 0 at 1/3
    let (l0, r0) = domain.subdivide(0, &rq(1, 3)).unwrap();

    // Cut l0 at dim 1 at 2/7
    let (l0_l1, l0_r1) = l0.subdivide(1, &rq(2, 7)).unwrap();

    // Cut r0 at dim 2 at 5/8
    let (r0_l2, r0_r2) = r0.subdivide(2, &rq(5, 8)).unwrap();

    let tree = BisectionTree::split(
        0,
        rq(1, 3),
        BisectionTree::split(
            1,
            rq(2, 7),
            BisectionTree::leaf(l0_l1, None, None),
            BisectionTree::leaf(l0_r1, None, None),
        ),
        BisectionTree::split(
            2,
            rq(5, 8),
            BisectionTree::leaf(r0_l2, None, None),
            BisectionTree::leaf(r0_r2, None, None),
        ),
    );

    assert_eq!(tree.leaf_count(), 4);
    assert_eq!(tree.total_volume(), BigRational::one());
    assert!(check_partition_cover(&tree, &domain).is_ok());
}

// ============================================================================
// 4. NEGATIVE CONTROLS (FALSIFICATION / REFUSAL AUDIT)
// ============================================================================

#[test]
fn test_negative_control_missing_deleted_cell_rejected() {
    let domain = RationalBox5D::unit_cube();
    let mid0 = domain.midpoint(0).unwrap();
    let (left0, _right0) = domain.subdivide(0, &mid0).unwrap();

    // Incomplete tree covering only [0, 1/2] along dim 0 (missing the right half [1/2, 1])
    let truncated_tree = BisectionTree::leaf(left0, None, None);

    let res = check_partition_cover(&truncated_tree, &domain);
    assert!(res.is_err(), "Truncated tree must be rejected");
    assert!(matches!(
        res.err().unwrap(),
        CoverTreeError::BoxMismatch { .. }
    ));
}

#[test]
fn test_negative_control_shrunk_interval_bound_gap_rejected() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 5);

    // Corrupt one leaf by shrinking its upper bound along dim 2 by exact epsilon = 1/1000
    let epsilon = rq(1, 1000);
    {
        let mut leaves = tree.leaves_mut();
        let (box_0, _, _) = &mut leaves[0];
        box_0.bounds[2].1 = &box_0.bounds[2].1 - &epsilon;
    }

    let res = check_partition_cover(&tree, &domain);
    assert!(
        res.is_err(),
        "Shrunk leaf bound (boundary gap) must be rejected"
    );
    match res.err().unwrap() {
        CoverTreeError::BoxMismatch { .. } | CoverTreeError::VolumeMismatch { .. } => (),
        other => panic!("Unexpected error variant: {:?}", other),
    }
}

#[test]
fn test_negative_control_corrupted_cut_out_of_bounds_rejected() {
    let domain = RationalBox5D::unit_cube();

    // Corrupted split: cut at 3/2 (strictly outside [0, 1])
    let corrupted_tree = BisectionTree::Split {
        dim: 0,
        cut: rq(3, 2),
        left: Box::new(BisectionTree::leaf(domain.clone(), None, None)),
        right: Box::new(BisectionTree::leaf(domain.clone(), None, None)),
    };

    let res = check_partition_cover(&corrupted_tree, &domain);
    assert!(
        matches!(res.err().unwrap(), CoverTreeError::CutOutOfBounds { .. }),
        "Cut out of bounds must be rejected"
    );

    // Corrupted split: cut at boundary 0
    let corrupted_boundary_tree = BisectionTree::Split {
        dim: 1,
        cut: rq(0, 1),
        left: Box::new(BisectionTree::leaf(domain.clone(), None, None)),
        right: Box::new(BisectionTree::leaf(domain.clone(), None, None)),
    };
    let res2 = check_partition_cover(&corrupted_boundary_tree, &domain);
    assert!(
        matches!(res2.err().unwrap(), CoverTreeError::CutOutOfBounds { .. }),
        "Cut at boundary must be rejected"
    );
}

#[test]
fn test_negative_control_overlapping_cells_rejected() {
    let domain = RationalBox5D::unit_cube();

    // Overlapping tree: left child is [0, 3/4] along dim 0, right child is [1/4, 1] along dim 0
    let mut left_bounds = domain.bounds.clone();
    left_bounds[0].1 = rq(3, 4);
    let left_box = RationalBox5D::new(left_bounds).unwrap();

    let mut right_bounds = domain.bounds.clone();
    right_bounds[0].0 = rq(1, 4);
    let right_box = RationalBox5D::new(right_bounds).unwrap();

    // Attempting to split at 1/2 with overlapping children
    let overlapping_tree = BisectionTree::split(
        0,
        rq(1, 2),
        BisectionTree::leaf(left_box, None, None),
        BisectionTree::leaf(right_box, None, None),
    );

    let res = check_partition_cover(&overlapping_tree, &domain);
    assert!(res.is_err(), "Overlapping children must be rejected");
}

#[test]
fn test_negative_control_unobstructed_witness_rejected() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 5);

    // 1. Missing certificate on all leaves
    assert!(matches!(
        verify_cover_obstruction(&tree, &domain),
        Err(CoverTreeError::MissingCertificate(_))
    ));

    // 2. Set certificates but leave margins None
    {
        let mut leaves = tree.leaves_mut();
        for (i, (_, cert_id, _)) in leaves.iter_mut().enumerate() {
            **cert_id = Some(format!("test_cert_{i}"));
        }
    }
    assert!(matches!(
        verify_cover_obstruction(&tree, &domain),
        Err(CoverTreeError::MissingMargin(_))
    ));

    // 3. Set positive margins on 31 leaves, but 0 on the 32nd leaf
    for i in 0..31 {
        certify_leaf_with_margin(&mut tree, i, format!("cert_{i}"), rq(1, 10)).unwrap();
    }
    certify_leaf_with_margin(&mut tree, 31, "cert_31", BigRational::zero()).unwrap();

    assert!(matches!(
        verify_cover_obstruction(&tree, &domain),
        Err(CoverTreeError::NonPositiveMargin { .. })
    ));

    // 4. Set negative margin on 32nd leaf (-1/1000)
    certify_leaf_with_margin(&mut tree, 31, "cert_31", rq(-1, 1000)).unwrap();
    assert!(matches!(
        verify_cover_obstruction(&tree, &domain),
        Err(CoverTreeError::NonPositiveMargin { .. })
    ));
}

// ============================================================================
// 5. COVER OBSTRUCTION RECEIPT & DIGEST VERIFICATION
// ============================================================================

#[test]
fn test_verified_cover_obstruction_receipt() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 5);

    // Certify all 32 leaves with positive margin >= 1/100
    for i in 0..32 {
        let margin = rq(1, 100) + rq(i as i64, 10000);
        certify_leaf_with_margin(&mut tree, i, format!("cert_obstruction_{i}"), margin).unwrap();
    }

    let receipt = verify_cover_obstruction(&tree, &domain).expect("verification must succeed");

    assert_eq!(receipt.schema_version, "omega.mub6.cover-obstruction.v1");
    assert_eq!(receipt.domain, domain);
    assert_eq!(receipt.leaf_count, 32);
    assert_eq!(receipt.certified_leaves, 32);
    assert!(receipt.verified_sound);
    assert_eq!(receipt.total_volume, BigRational::one());
    assert_eq!(receipt.min_margin, rq(1, 100));
    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);

    // Verify SHA256 digest format and determinism
    assert!(receipt.sha256_digest.is_some());
    let digest = receipt.sha256_digest.as_ref().unwrap();
    assert_eq!(digest.len(), 64);
    assert_eq!(digest, &receipt.compute_digest());
}

// ============================================================================
// 6. SERIALIZATION ROUND-TRIP & LEAN 4 / PYTHON DTO FORMATS
// ============================================================================

#[test]
fn test_json_and_lean_dto_serialization_round_trip() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 2); // 4 leaves

    for i in 0..4 {
        certify_leaf_with_margin(&mut tree, i, format!("poly_{i}"), rq(3, 10)).unwrap();
    }

    // 1. Direct JSON serialization
    let json_str = tree.to_json().expect("to_json");
    let recovered_tree = BisectionTree::from_json(&json_str).expect("from_json");
    assert_eq!(tree, recovered_tree);

    // 2. Lean 4 / Python DTO JSON serialization
    let lean_json = tree.to_lean_json().expect("to_lean_json");
    let recovered_from_lean = BisectionTree::from_lean_json(&lean_json).expect("from_lean_json");
    assert_eq!(tree, recovered_from_lean);

    // 3. Receipt serialization
    let receipt = verify_cover_obstruction(&tree, &domain).expect("receipt");
    let receipt_json = receipt.to_json().expect("receipt to_json");
    let recovered_receipt =
        CoverObstructionReceipt::from_json(&receipt_json).expect("receipt from_json");
    assert_eq!(receipt, recovered_receipt);
}

// ============================================================================
// 7. INTEGRATION WITH TARGET A4 DUAL SDP CERTIFIER & L1 SOLVER
// ============================================================================

#[test]
fn test_integration_target_a4_sdp_certifier() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 1); // 2 leaves

    // Solve Target A4 Quad SDP certificate
    let sdp_cert = solve_quad_sdp_certificate();
    assert!(sdp_cert.dual_certificate_psd_certified);
    assert!(sdp_cert.constructed_matrix_not_psd);

    // Certify leaf 0 using Target A4 dual SDP certificate
    certify_leaf_with_sdp(&mut tree, 0, &sdp_cert).expect("sdp attachment must succeed");

    // Leaf 0 should have cert_id and positive margin
    let leaves = tree.leaves_mut();
    assert_eq!(
        leaves[0].1.as_deref(),
        Some("target_a4_sdp:omega.mub.quad-sdp.v2")
    );
    assert!(leaves[0].2.as_ref().unwrap() > &BigRational::zero());

    // Certify leaf 1 with custom positive margin
    certify_leaf_with_margin(&mut tree, 1, "test_complement", rq(1, 10)).unwrap();

    let receipt = verify_cover_obstruction(&tree, &domain).expect("integrated cover verification");
    assert!(receipt.verified_sound);
    assert_eq!(receipt.leaf_count, 2);
}

#[test]
fn test_integration_l1_network_simplex_and_phi1() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 1); // 2 leaves

    // Solve a simple exact network simplex L1 boundary problem
    // Cycle: 0 -> 1, 1 -> 2, 2 -> 0 with demands and capacities
    let boundary = Boundary1 {
        num_vertices: 3,
        edges: vec![
            BoundaryEdge {
                tail: 0,
                head: 1,
                weight: 1,
            },
            BoundaryEdge {
                tail: 1,
                head: 2,
                weight: 1,
            },
            BoundaryEdge {
                tail: 2,
                head: 0,
                weight: 1,
            },
        ],
    };
    let x = [5i128, -5, 0];
    let sol = solve_l1_boundary(&boundary, &x).expect("boundary solution");
    assert!(sol.objective > 0);

    // Certify leaf 0 with network simplex solution
    certify_leaf_with_phi1_solution(&mut tree, 0, &sol).expect("simplex attachment");

    // Certify leaf 1 with Phi1 certificate
    let a_matrix = vec![vec![rq(1, 1), rq(1, 1)]];
    let b_bounds = vec![rq(2, 1)];
    let c_obj = vec![rq(1, 1), rq(1, 1)];
    let x_primal = vec![rq(1, 1), rq(1, 1)];
    let y_dual = vec![rq(1, 1)];
    let phi1_cert = Phi1Verifier::verify(&x_primal, &y_dual, &a_matrix, &b_bounds, &c_obj)
        .expect("valid phi1 cert");

    certify_leaf_with_phi1(&mut tree, 1, &phi1_cert).expect("phi1 attachment");

    let receipt = verify_cover_obstruction(&tree, &domain).expect("verification must pass");
    assert!(receipt.verified_sound);
    assert_eq!(receipt.leaf_count, 2);
}

#[test]
fn test_certify_all_leaves_with_margin() {
    let domain = RationalBox5D::unit_cube();
    let mut tree = build_uniform_bisection_tree(&domain, 0, 3); // 8 leaves
    certify_all_leaves_with_margin(&mut tree, "bulk", rq(1, 4)).expect("bulk certification");
    let receipt = verify_cover_obstruction(&tree, &domain).expect("bulk verification");
    assert_eq!(receipt.certified_leaves, 8);
    assert_eq!(receipt.min_margin, rq(1, 4));
}
