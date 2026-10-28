//! Comprehensive Unit and Integration Test Suite for Target A10:
//! Rust Native Global Atlas Aggregator & Volume Certifier.
//!
//! AuthorityEffect: None.

use std::fs;
use std::path::Path;

use num_rational::BigRational;
use num_traits::{One, Zero};
use syn::visit::Visit;

use tfqm_mub::native::exact::mub6_constants::{
    base_gap, certified_margin, delta_certified, lipschitz_bound,
};
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_mub::native::exact::mub6_global_cover::{
    build_canonical_global_atlas, build_component_partition, ChartBoundaryInterface,
    CompositeCycleLoop, GlobalAtlasAggregator, GlobalCoverError, RationalCell,
    RegionalCoverComponent, RegionalCoverPatch, RegionalPartitionTree, NUM_REGIONAL_COMPONENTS,
};
use omega_number_theory::rational::rq;

// ============================================================================
// 1. STRICT ZERO-FLOAT DISCIPLINE AST AUDIT
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
        .join("native")
        .join("mub6_global_cover.rs");

    let source = fs::read_to_string(&target_file)
        .unwrap_or_else(|e| panic!("Failed to read {}: {}", target_file.display(), e));

    // 1. AST-level parse and visit
    let syntax_tree = syn::parse_file(&source)
        .unwrap_or_else(|e| panic!("Failed to parse {}: {}", target_file.display(), e));

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.is_empty(),
        "Target A10 Rust module violated zero-float discipline at AST level: {:?}",
        visitor.found_floats
    );

    // 2. Lexical check
    assert!(
        !source.contains("f32"),
        "mub6_global_cover.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_global_cover.rs must contain zero f64 occurrences"
    );
}

// ============================================================================
// 2. EPISTEMIC FIREWALL & CANONICAL CONSTANTS
// ============================================================================

#[test]
fn test_firewall_and_canonical_constants() {
    assert_eq!(
        FIREWALL,
        "stated region only; mints no authority"
    );
    assert_eq!(AUTHORITY_EFFECT, "None");
    assert_eq!(NUM_REGIONAL_COMPONENTS, 6);

    let bg = base_gap();
    let lb = lipschitz_bound();
    let ms = delta_certified();
    let cm = certified_margin();

    assert_eq!(bg, rq(37249, 90000));
    assert_eq!(lb, rq(85, 9));
    assert_eq!(ms, rq(1, 1000));
    assert_eq!(cm, rq(12133, 30000));

    // Margin erosion check: bg - lb * ms = cm
    let erosion = &lb * &ms;
    assert_eq!(&bg - &erosion, cm);
    assert!(cm > BigRational::zero());
}

// ============================================================================
// 3. RATIONAL CELL & PARTITION TREE UNIT TESTS
// ============================================================================

#[test]
fn test_rational_cell_operations() {
    let margin = certified_margin();
    let cell = RationalCell::new(
        vec![
            (rq(0, 1), rq(1, 2)),
            (rq(0, 1), rq(1, 3)),
            (rq(0, 1), rq(1, 4)),
        ],
        margin.clone(),
    )
    .expect("Cell creation must succeed");

    assert_eq!(cell.dimension(), 3);
    assert_eq!(cell.volume(), rq(1, 24));

    // Point containment
    let inside_pt = [rq(1, 4), rq(1, 6), rq(1, 8)];
    assert!(cell.contains_point(&inside_pt));

    let outside_pt = [rq(3, 4), rq(1, 6), rq(1, 8)];
    assert!(!cell.contains_point(&outside_pt));

    // Bisection along dimension 0: [0, 1/4] and [1/4, 1/2]
    let (left, right) = cell.bisect(0).expect("Bisection must succeed");
    assert_eq!(left.volume(), rq(1, 48));
    assert_eq!(right.volume(), rq(1, 48));
    assert_eq!(&left.volume() + &right.volume(), cell.volume());

    // Interior overlap check
    assert!(!left.overlaps_interior(&right));
    assert!(cell.overlaps_interior(&left));
    assert!(cell.overlaps_interior(&right));

    // Invalid interval rejection
    let inv = RationalCell::new(vec![(rq(1, 2), rq(1, 4))], margin);
    assert!(inv.is_err());
}

#[test]
fn test_partition_tree_properties() {
    let margin = certified_margin();
    let tree =
        build_component_partition(3, rq(1, 8), 4, margin.clone()).expect("Tree build must succeed");

    assert_eq!(tree.leaf_count(), 4);
    assert_eq!(tree.total_volume(), rq(1, 8));
    assert_eq!(tree.min_margin(), margin);
    assert!(tree.all_margins_positive());

    let leaves = tree.leaves();
    assert_eq!(leaves.len(), 4);
    for l in leaves {
        assert_eq!(l.volume(), rq(1, 32));
        assert_eq!(l.margin, margin);
    }
}

// ============================================================================
// 4. AGGREGATION OF ALL 6 REGIONAL COVERS
// ============================================================================

#[test]
fn test_canonical_atlas_all_six_components_present() {
    let atlas = build_canonical_global_atlas();

    assert_eq!(atlas.patches.len(), 6);
    assert!(atlas.verify_component_completeness().is_ok());

    // Check all 6 components
    let expected = [
        (
            RegionalCoverComponent::DitaFourierF6,
            "F6_dita_fourier",
            rq(1, 12),
        ),
        (
            RegionalCoverComponent::SzollosiDeltoidB6,
            "B6_szollosi_deltoid",
            rq(1, 12),
        ),
        (
            RegionalCoverComponent::TaoConfluenceS6,
            "S6_tao_confluence",
            rq(1, 12),
        ),
        (
            RegionalCoverComponent::PeriodicCollar2D,
            "C2_periodic_collar",
            rq(2, 12),
        ),
        (
            RegionalCoverComponent::KarlssonVolumeExterior,
            "K6_karlsson_exterior",
            rq(6, 12),
        ),
        (
            RegionalCoverComponent::HaagerupOrbitH6,
            "H6_haagerup_orbit",
            rq(1, 12),
        ),
    ];

    for (comp, cid, vol) in expected {
        assert_eq!(comp.canonical_id(), cid);
        let patch = atlas.patches.get(&comp).expect("Patch must exist in atlas");
        assert_eq!(patch.component, comp);
        assert_eq!(patch.volume, vol);
        assert!(patch.certified);
        assert!(patch.margin > BigRational::zero());
        assert!(patch.leaf_count() > 0);
    }
}

// ============================================================================
// 5. EXACT VOLUME CONSERVATION CERTIFICATION
// ============================================================================

#[test]
fn test_exact_volume_conservation_certifier() {
    let atlas = build_canonical_global_atlas();

    let receipt = atlas
        .certify_volume_conservation()
        .expect("Volume conservation must pass with exact zero gap");

    assert_eq!(receipt.declared_total_volume, BigRational::one());
    assert_eq!(receipt.sum_component_volumes, BigRational::one());
    assert!(receipt.volume_difference.is_zero());
    assert!(receipt.is_exact_zero_gap);
    assert!(receipt.all_volumes_positive);
    assert!(receipt.certified);

    // Sum verification directly:
    // 1/12 + 1/12 + 1/12 + 2/12 + 6/12 + 1/12 = 12/12 = 1
    let sum: BigRational = receipt.component_volumes.iter().map(|(_, v)| v).sum();
    assert_eq!(sum, BigRational::one());
}

// ============================================================================
// 6. MULTI-CHART BOUNDARY INTERFACE ADJACENCY
// ============================================================================

#[test]
fn test_boundary_interface_adjacency_and_connectivity() {
    let atlas = build_canonical_global_atlas();

    let report = atlas
        .check_all_interfaces()
        .expect("Boundary interface adjacency check must succeed");

    assert_eq!(report.total_interfaces, 6);
    assert!(report.all_interfaces_adjacent);
    assert!(!report.any_gap_detected);
    assert!(report.is_atlas_connected);
    assert_eq!(report.min_interface_margin, certified_margin());

    for rc in &report.receipts {
        assert!(rc.is_adjacent);
        assert!(!rc.gap_detected);
        assert!(rc.continuity_certified);
        assert_eq!(rc.overlap_volume, delta_certified());
        assert_eq!(rc.interface_margin, certified_margin());
    }
}

// ============================================================================
// 7. NETWORK SIMPLEX POSITIVE CYCLE CIRCULATION PHI_1 > 0
// ============================================================================

#[test]
fn test_network_simplex_positive_cycle_circulation() {
    let atlas = build_canonical_global_atlas();
    let scale = 30000i128;

    let receipts = atlas
        .certify_cycle_circulations(scale)
        .expect("Cycle circulation certification must succeed");

    assert_eq!(receipts.len(), 3);

    // 1. Triad loop: F_6 -> B_6 -> S_6 -> F_6
    let triad_rc = &receipts[0];
    assert_eq!(triad_rc.loop_name, "TriadLoop_F6_B6_S6");
    assert_eq!(triad_rc.cycle_length, 3);
    assert_eq!(triad_rc.edge_cochain, vec![12133, 12133, 12133]);
    assert_eq!(triad_rc.net_circulation, 36399);
    assert_eq!(triad_rc.phi1_objective, 36399);
    assert_eq!(triad_rc.coboundary_sum, 0);
    assert!(triad_rc.circulation_conserved);
    assert!(triad_rc.dual_gap_zero);
    assert!(triad_rc.certified);
    assert_eq!(triad_rc.rational_phi1, "12133/10000");

    // 2. Collar-Karlsson-Haagerup boundary loop
    let boundary_rc = &receipts[1];
    assert_eq!(
        boundary_rc.loop_name,
        "BoundaryLoop_Collar_Karlsson_Haagerup"
    );
    assert_eq!(boundary_rc.cycle_length, 3);
    assert_eq!(boundary_rc.phi1_objective, 36399);
    assert_eq!(boundary_rc.coboundary_sum, 0);
    assert!(boundary_rc.dual_gap_zero);
    assert!(boundary_rc.certified);

    // 3. Full 6-chart composite loop
    let full_rc = &receipts[2];
    assert_eq!(full_rc.loop_name, "FullSixChartCompositeLoop");
    assert_eq!(full_rc.cycle_length, 6);
    assert_eq!(full_rc.edge_cochain, vec![12133; 6]);
    assert_eq!(full_rc.net_circulation, 12133 * 6);
    assert_eq!(full_rc.phi1_objective, 12133 * 6);
    assert_eq!(full_rc.coboundary_sum, 0);
    assert!(full_rc.circulation_conserved);
    assert!(full_rc.dual_gap_zero);
    assert!(full_rc.certified);
    assert_eq!(full_rc.rational_phi1, "12133/5000");
}

// ============================================================================
// 8. FULL COMPREHENSIVE GLOBAL ATLAS RECEIPT
// ============================================================================

#[test]
fn test_certify_full_global_atlas() {
    let atlas = build_canonical_global_atlas();
    let scale = 30000i128;

    let receipt = atlas
        .certify_global_atlas(scale)
        .expect("Full global atlas certification must succeed");

    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(receipt.component_count, 6);
    assert!(receipt.all_components_present);
    assert!(receipt.volume_conservation.is_exact_zero_gap);
    assert!(receipt.boundary_adjacency.all_interfaces_adjacent);
    assert!(receipt.boundary_adjacency.is_atlas_connected);
    assert_eq!(receipt.composite_loop_receipts.len(), 3);
    assert!(!receipt.atlas_hash.is_empty());
    assert!(receipt.certified);
}

// ============================================================================
// 9. NEGATIVE CONTROLS
// ============================================================================

#[test]
fn test_negative_control_rejection_of_missing_component() {
    let mut atlas = GlobalAtlasAggregator::new(BigRational::one());
    let margin = certified_margin();

    // Add only 5 of the 6 components (omitting HaagerupOrbitH6)
    let components = [
        (RegionalCoverComponent::DitaFourierF6, rq(1, 12)),
        (RegionalCoverComponent::SzollosiDeltoidB6, rq(1, 12)),
        (RegionalCoverComponent::TaoConfluenceS6, rq(1, 12)),
        (RegionalCoverComponent::PeriodicCollar2D, rq(2, 12)),
        (RegionalCoverComponent::KarlssonVolumeExterior, rq(7, 12)),
    ];

    for (comp, vol) in components {
        let tree = build_component_partition(2, vol, 2, margin.clone()).unwrap();
        let patch = RegionalCoverPatch::new(comp, comp.canonical_id(), tree).unwrap();
        atlas.add_patch(patch).unwrap();
    }

    // Must fail completeness verification
    let res = atlas.verify_component_completeness();
    assert!(matches!(
        res,
        Err(GlobalCoverError::MissingComponent(
            RegionalCoverComponent::HaagerupOrbitH6
        ))
    ));

    // Volume conservation check must also reject missing component
    let vol_res = atlas.certify_volume_conservation();
    assert!(matches!(
        vol_res,
        Err(GlobalCoverError::MissingComponent(
            RegionalCoverComponent::HaagerupOrbitH6
        ))
    ));
}

#[test]
fn test_negative_control_rejection_of_volume_discrepancy() {
    let mut atlas = build_canonical_global_atlas();

    // Declare expected total volume = 2, while components sum to 1
    atlas.declared_total_volume = rq(2, 1);

    let res = atlas.certify_volume_conservation();
    match res {
        Err(GlobalCoverError::VolumeConservationMismatch {
            expected,
            actual,
            difference,
        }) => {
            assert_eq!(expected, rq(2, 1));
            assert_eq!(actual, rq(1, 1));
            assert_eq!(difference, rq(-1, 1));
        }
        other => panic!("Expected VolumeConservationMismatch, got {:?}", other),
    }
}

#[test]
fn test_negative_control_rejection_of_boundary_gap() {
    let mut atlas = build_canonical_global_atlas();

    // Introduce an uncertified gap between F6 and B6 by zeroing overlap volume
    atlas.interfaces[0].overlap_volume = BigRational::zero();
    atlas.interfaces[0].gap_detected = true;

    let res = atlas.check_all_interfaces();
    match res {
        Err(GlobalCoverError::BoundaryGapDetected {
            chart_a, chart_b, ..
        }) => {
            assert_eq!(chart_a, RegionalCoverComponent::DitaFourierF6);
            assert_eq!(chart_b, RegionalCoverComponent::SzollosiDeltoidB6);
        }
        other => panic!("Expected BoundaryGapDetected, got {:?}", other),
    }
}

#[test]
fn test_negative_control_rejection_of_non_positive_margin() {
    let zero = BigRational::zero();

    // 1. Rejection of non-positive cell margin in patch
    let cell_res = RationalCell::new(vec![(rq(0, 1), rq(1, 2))], zero.clone());
    assert!(cell_res.is_ok());
    let cell = cell_res.unwrap();

    let patch_res = RegionalCoverPatch::new(
        RegionalCoverComponent::DitaFourierF6,
        "ZeroMarginPatch",
        RegionalPartitionTree::leaf(cell),
    );
    assert!(matches!(
        patch_res,
        Err(GlobalCoverError::NonPositiveMargin { .. })
    ));

    // 2. Rejection of non-positive interface margin
    let bad_iface = ChartBoundaryInterface::new(
        RegionalCoverComponent::DitaFourierF6,
        RegionalCoverComponent::SzollosiDeltoidB6,
        delta_certified(),
        zero,
        vec![],
    );
    assert!(bad_iface.verify_adjacency().is_err());

    // 3. Rejection of non-positive circulation scale
    let loop_def = CompositeCycleLoop::triad_loop();
    let atlas = build_canonical_global_atlas();
    let bad_scale_res = atlas.solve_loop_circulation(&loop_def, 0);
    assert!(matches!(
        bad_scale_res,
        Err(GlobalCoverError::NonPositiveCirculation { .. })
    ));
}

#[test]
fn test_negative_control_rejection_of_disconnected_atlas() {
    let mut atlas = build_canonical_global_atlas();

    // Replace interfaces with disjoint pairs (F6-B6, S6-Collar) disconnected from Karlsson-Haagerup
    atlas.interfaces.clear();

    let dummy_cell =
        RationalCell::new(vec![(rq(0, 1), delta_certified())], certified_margin()).unwrap();

    atlas
        .add_interface(ChartBoundaryInterface::new(
            RegionalCoverComponent::DitaFourierF6,
            RegionalCoverComponent::SzollosiDeltoidB6,
            delta_certified(),
            certified_margin(),
            vec![dummy_cell.clone()],
        ))
        .unwrap();

    atlas
        .add_interface(ChartBoundaryInterface::new(
            RegionalCoverComponent::TaoConfluenceS6,
            RegionalCoverComponent::PeriodicCollar2D,
            delta_certified(),
            certified_margin(),
            vec![dummy_cell],
        ))
        .unwrap();

    let res = atlas.check_all_interfaces();
    assert!(matches!(res, Err(GlobalCoverError::DisconnectedAtlas)));
}
