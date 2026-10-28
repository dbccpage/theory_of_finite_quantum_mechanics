//! Comprehensive Unit and Integration Test Suite for Target A13:
//! Rust Native Grand Synthesis Pipeline.
//!
//! AuthorityEffect: None
//! The formal result is strictly scoped to the declared classification premises, the certified
//! partition cover, and the combinatorial basis gluing theorem.

use std::fs;
use std::path::Path;

use num_rational::BigRational;
use num_traits::{One, Zero};
use syn::visit::Visit;

use tfqm_mub::native::exact::mub6_constants::{
    base_gap, certified_margin, delta_certified, lipschitz_bound,
};
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_mub::native::exact::mub6_grand_synthesis::{
    candidate_fourth_indices, canonical_global_partition_tree, certify_grand_synthesis,
    circulation_gamma, evaluate_grand_synthesis, evaluate_synthetic_root_bifurcation,
    grand_synthesis_certified, total_domain_volume, verify_all_combinatorial_triples,
    verify_bifurcation_mutual_exclusivity, verify_boundary_circulation, verify_volume_conservation,
    BifurcationBranch, GrandSynthesisChart, GrandSynthesisError, GrandSynthesisPartitionTree,
    SynthesisCandidate, SynthesisLeafCell, COMPLETE_MUB_BASES_COUNT, NUM_REGIONAL_CHARTS,
    REMAINING_CANDIDATE_BASES_COUNT, TOTAL_CELL_COUNT, TOTAL_COMBINATORIAL_TRIPLES_COUNT,
};
use tfqm_mub::native::exact::mub6_haagerup::haagerup_h6_matrix;
use tfqm_mub::native::exact::mub6_orbit_exhaustiveness::{
    classify_orbit, standard_fourier_f6, CrossRatioSpectrum, OrbitClass, NUM_SUBMATRICES_225,
};
use tfqm_mub::native::exact::mub6_smale_sentry::{
    smale_alpha_threshold, CertifiedLeafCell, QuadraticComponent, RationalMatrix, SmaleSentry,
    SquarePolynomialSystem,
};
use tfqm_mub::native::exact::mub6_tao_chart::tao_s6_matrix;
use tfqm_mub::native::exact::szollosi_triad_solver::szollosi_dephased_b6;
use omega_number_theory::cyclotomic::Cyc24;
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
        .join("mub6_grand_synthesis.rs");

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
        "Target A13 Rust module violated zero-float discipline at AST level: {:?}",
        visitor.found_floats
    );

    // 2. Lexical check
    assert!(
        !source.contains("f32"),
        "mub6_grand_synthesis.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_grand_synthesis.rs must contain zero f64 occurrences"
    );
}

// ============================================================================
// 2. EPISTEMIC FIREWALL & CANONICAL RATIONAL CONSTANTS
// ============================================================================

#[test]
fn test_firewall_and_canonical_constants() {
    assert_eq!(
        FIREWALL,
        "stated region only; mints no authority"
    );
    assert_eq!(AUTHORITY_EFFECT, "None");
    assert_eq!(NUM_REGIONAL_CHARTS, 6);
    assert_eq!(TOTAL_CELL_COUNT, 28);

    let eps0 = base_gap();
    let l_const = lipschitz_bound();
    let delta = delta_certified();
    let min_margin = certified_margin();
    let gamma = circulation_gamma();
    let total_vol = total_domain_volume();
    let alpha_0 = smale_alpha_threshold();

    assert_eq!(eps0, rq(37249, 90000));
    assert_eq!(l_const, rq(85, 9));
    assert_eq!(delta, rq(1, 1000));
    assert_eq!(min_margin, rq(12133, 30000));
    assert_eq!(gamma, rq(12133, 5000));
    assert_eq!(total_vol, rq(5001, 1000));
    assert_eq!(alpha_0, rq(157, 1000));

    // Margin erosion identity: eps_0 - L * delta = min_margin
    let erosion = &l_const * &delta;
    assert_eq!(&eps0 - &erosion, min_margin);
    assert!(min_margin > BigRational::zero());
    assert!(gamma > BigRational::zero());
}

// ============================================================================
// 3. CANONICAL GLOBAL PARTITION TREE STRUCTURE & 28 LEAF CELLS
// ============================================================================

#[test]
fn test_canonical_partition_tree_structure_and_cell_counts() {
    let tree = canonical_global_partition_tree();

    assert_eq!(tree.leaf_count(), TOTAL_CELL_COUNT);
    assert_eq!(tree.total_volume(), rq(5001, 1000));
    assert_eq!(tree.min_margin(), rq(12133, 30000));
    assert!(tree.all_margins_positive());

    // Verify cell distribution across the 6 regional charts:
    // F6: 4 cells, vol = 1
    // B6: 8 cells, vol = 1
    // S6: 4 cells, vol = 1
    // Collar: 4 cells, vol = 1
    // Karlsson: 4 cells, vol = 1/1000
    // H6: 4 cells, vol = 1
    assert_eq!(
        tree.cell_count_for_chart(GrandSynthesisChart::DitaFourierF6),
        4
    );
    assert_eq!(
        tree.volume_for_chart(GrandSynthesisChart::DitaFourierF6),
        BigRational::one()
    );

    assert_eq!(
        tree.cell_count_for_chart(GrandSynthesisChart::SzollosiDeltoidB6),
        8
    );
    assert_eq!(
        tree.volume_for_chart(GrandSynthesisChart::SzollosiDeltoidB6),
        BigRational::one()
    );

    assert_eq!(
        tree.cell_count_for_chart(GrandSynthesisChart::TaoConfluenceS6),
        4
    );
    assert_eq!(
        tree.volume_for_chart(GrandSynthesisChart::TaoConfluenceS6),
        BigRational::one()
    );

    assert_eq!(
        tree.cell_count_for_chart(GrandSynthesisChart::PeriodicCollar2D),
        4
    );
    assert_eq!(
        tree.volume_for_chart(GrandSynthesisChart::PeriodicCollar2D),
        BigRational::one()
    );

    assert_eq!(
        tree.cell_count_for_chart(GrandSynthesisChart::KarlssonVolumeExterior),
        4
    );
    assert_eq!(
        tree.volume_for_chart(GrandSynthesisChart::KarlssonVolumeExterior),
        rq(1, 1000)
    );

    assert_eq!(
        tree.cell_count_for_chart(GrandSynthesisChart::HaagerupOrbitH6),
        4
    );
    assert_eq!(
        tree.volume_for_chart(GrandSynthesisChart::HaagerupOrbitH6),
        BigRational::one()
    );

    // Sum of cell counts: 4 + 8 + 4 + 4 + 4 + 4 = 28
    let sum_cells: usize = GrandSynthesisChart::ALL
        .iter()
        .map(|c| tree.cell_count_for_chart(*c))
        .sum();
    assert_eq!(sum_cells, 28);

    // Sum of volumes: 1 + 1 + 1 + 1 + 1/1000 + 1 = 5001/1000
    let sum_vols: BigRational = GrandSynthesisChart::ALL
        .iter()
        .map(|c| tree.volume_for_chart(*c))
        .sum();
    assert_eq!(sum_vols, rq(5001, 1000));

    // Every leaf cell carries margin >= 12133/30000
    let min_allowed = certified_margin();
    for cell in &tree.leaves {
        assert!(
            cell.margin >= min_allowed,
            "Cell {} margin {} < min allowed {}",
            cell.cell_id,
            cell.margin,
            min_allowed
        );
        assert!(cell.volume > BigRational::zero());
        assert!(!cell.bounds.is_empty());
    }
}

// ============================================================================
// 4. EXACT VOLUME CONSERVATION CERTIFIER (SUM VOL = 5001 / 1000)
// ============================================================================

#[test]
fn test_exact_volume_conservation_5001_1000() {
    let tree = canonical_global_partition_tree();
    let receipt =
        verify_volume_conservation(&tree).expect("Volume conservation verification must succeed");

    assert_eq!(receipt.declared_total_volume, rq(5001, 1000));
    assert_eq!(receipt.sum_leaf_volumes, rq(5001, 1000));
    assert!(receipt.volume_difference.is_zero());
    assert!(receipt.is_exact_zero_gap);
    assert!(receipt.all_volumes_positive);
    assert_eq!(receipt.total_cells, 28);
    assert!(receipt.certified);

    assert_eq!(receipt.chart_cell_counts["F6_dita_fourier"], 4);
    assert_eq!(receipt.chart_cell_counts["B6_szollosi_deltoid"], 8);
    assert_eq!(receipt.chart_cell_counts["S6_tao_confluence"], 4);
    assert_eq!(receipt.chart_cell_counts["C2_periodic_collar"], 4);
    assert_eq!(receipt.chart_cell_counts["K6_karlsson_exterior"], 4);
    assert_eq!(receipt.chart_cell_counts["H6_haagerup_orbit"], 4);

    assert_eq!(receipt.chart_volumes["K6_karlsson_exterior"], "1/1000");
}

// ============================================================================
// 5. BOUNDARY CYCLIC INTERFACE CIRCULATION (PHI_1 >= 12133 / 5000 > 0)
// ============================================================================

#[test]
fn test_boundary_cyclic_circulation_phi1() {
    let receipt =
        verify_boundary_circulation().expect("Boundary circulation verification must succeed");

    assert_eq!(receipt.cycle_length, 6);
    assert_eq!(receipt.scale, 30000);
    assert_eq!(receipt.net_circulation, 72798); // 6 * 12133
    assert_eq!(receipt.phi1_objective, 72798);
    assert_eq!(receipt.coboundary_sum, 0);
    assert!(receipt.circulation_conserved);
    assert!(receipt.dual_gap_zero);
    assert!(receipt.certified);
    assert_eq!(receipt.rational_phi1, "12133/5000");

    let phi1_rat = rq(72798, 30000);
    assert_eq!(phi1_rat, circulation_gamma());
    assert!(phi1_rat > BigRational::zero());
}

// ============================================================================
// 6. CANONICAL ORBIT CLASSIFICATION & 225 CROSS-RATIO SPECTRUM
// ============================================================================

#[test]
fn test_canonical_orbit_classification_and_cross_ratio_spectrum() {
    // 1. Standard Fourier F_6
    let f6 = standard_fourier_f6();
    let spec_f6 = CrossRatioSpectrum::from_matrix(&f6);
    assert_eq!(spec_f6.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec_f6.imaginary_unit_count(), 0);
    assert_eq!(classify_orbit(&f6), OrbitClass::Fourier);

    // 2. Tao S_6
    let s6 = tao_s6_matrix();
    let spec_s6 = CrossRatioSpectrum::from_matrix(&s6);
    assert_eq!(spec_s6.total_count, NUM_SUBMATRICES_225);
    assert!(spec_s6.is_strictly_cubic());
    assert_eq!(classify_orbit(&s6), OrbitClass::Tao);

    // 3. Haagerup H_6
    let h6 = haagerup_h6_matrix();
    let spec_h6 = CrossRatioSpectrum::from_matrix(&h6);
    assert_eq!(spec_h6.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec_h6.imaginary_unit_count(), 120);
    assert!(spec_h6.is_strictly_quartic());
    assert_eq!(classify_orbit(&h6), OrbitClass::Haagerup);

    // 4. Szöllősi B_6 Point A
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(8);
    let e = Cyc24::zeta24(8);
    let f = Cyc24::zeta24(0);
    let b6 = szollosi_dephased_b6(&b, &c, &e, &f).unwrap();
    let spec_b6 = CrossRatioSpectrum::from_matrix(&b6);
    assert_eq!(spec_b6.total_count, NUM_SUBMATRICES_225);
    match classify_orbit(&b6) {
        OrbitClass::Szollosi { theta_approx } => {
            let pi = tfqm_mub::native::exact::mub6_orbit_exhaustiveness::pi_approx();
            let exp_theta = (rq(8, 1) * &pi) / rq(12, 1);
            assert_eq!(theta_approx, exp_theta);
        }
        other => panic!("Expected Szollosi orbit class, got {:?}", other),
    }
}

// ============================================================================
// 7. LEAF CELL LOOKUP AND MARGIN EXTRACTION ACROSS ALL 6 CHARTS
// ============================================================================

#[test]
fn test_leaf_cell_lookup_and_margin_extraction() {
    let tree = canonical_global_partition_tree();
    let min_allowed = certified_margin();

    // 1. Chart 1: F6 (5D point)
    let pt_f6 = [rq(1, 4), rq(1, 4), rq(1, 2), rq(1, 2), rq(1, 2)];
    let cell_f6 = tree
        .lookup_cell(GrandSynthesisChart::DitaFourierF6, &pt_f6)
        .expect("F6 lookup must succeed");
    assert_eq!(cell_f6.cell_id, "F6_cell_0_0");
    assert!(cell_f6.margin >= min_allowed);
    assert_eq!(cell_f6.margin, base_gap());

    // 2. Chart 2: B6 (2D point in cusp0)
    let pt_b6_0 = [rq(1, 8), rq(1, 4)];
    let cell_b6_0 = tree
        .lookup_cell(GrandSynthesisChart::SzollosiDeltoidB6, &pt_b6_0)
        .expect("B6 cusp0 lookup must succeed");
    assert_eq!(cell_b6_0.cell_id, "B6_cusp0_cell_0");
    assert_eq!(cell_b6_0.margin, min_allowed);

    // B6 regular arc cell
    let pt_b6_arc = [rq(7, 8), rq(3, 4)];
    let cell_b6_arc = tree
        .lookup_cell(GrandSynthesisChart::SzollosiDeltoidB6, &pt_b6_arc)
        .expect("B6 arc lookup must succeed");
    assert_eq!(cell_b6_arc.cell_id, "B6_arc_reg_cell_1");
    assert_eq!(cell_b6_arc.margin, min_allowed);

    // 3. Chart 3: S6 (2D point)
    let pt_s6 = [rq(3, 4), rq(1, 4)];
    let cell_s6 = tree
        .lookup_cell(GrandSynthesisChart::TaoConfluenceS6, &pt_s6)
        .expect("S6 lookup must succeed");
    assert_eq!(cell_s6.cell_id, "S6_cell_2");
    assert_eq!(cell_s6.margin, rq(527, 576));
    assert!(cell_s6.margin > min_allowed);

    // 4. Chart 4: Collar (2D point)
    let pt_collar = [rq(3, 4), rq(3, 4)];
    let cell_collar = tree
        .lookup_cell(GrandSynthesisChart::PeriodicCollar2D, &pt_collar)
        .expect("Collar lookup must succeed");
    assert_eq!(cell_collar.cell_id, "Collar_cell_3");
    assert_eq!(cell_collar.margin, min_allowed);

    // 5. Chart 5: Karlsson exterior (3D point)
    let pt_karlsson = [rq(1, 4), rq(3, 4), rq(1, 2000)];
    let cell_karlsson = tree
        .lookup_cell(GrandSynthesisChart::KarlssonVolumeExterior, &pt_karlsson)
        .expect("Karlsson lookup must succeed");
    assert_eq!(cell_karlsson.cell_id, "Karlsson_cell_1");
    assert_eq!(cell_karlsson.margin, base_gap());

    // 6. Chart 6: Haagerup (2D point)
    let pt_h6 = [rq(3, 4), rq(1, 4)];
    let cell_h6 = tree
        .lookup_cell(GrandSynthesisChart::HaagerupOrbitH6, &pt_h6)
        .expect("H6 lookup must succeed");
    assert_eq!(cell_h6.cell_id, "H6_cell_2");
    assert_eq!(cell_h6.margin, min_allowed);
}

// ============================================================================
// 8. SMALE SENTRY INTEGRATION ACROSS ALL 28 CELLS
// ============================================================================

#[test]
fn test_smale_sentry_scan_all_28_cells() {
    let tree = canonical_global_partition_tree();
    let cert_cells: Vec<CertifiedLeafCell> = tree
        .leaves
        .iter()
        .map(|c| c.to_certified_leaf_cell())
        .collect();

    assert_eq!(cert_cells.len(), TOTAL_CELL_COUNT);

    let summary = SmaleSentry::scan_bisection_leaves(&cert_cells);

    assert!(
        summary.all_positive,
        "All 28 leaf cells must have positive residual margins"
    );
    assert_eq!(summary.scanned_count, 28);
    assert_eq!(summary.min_margin, certified_margin());
    assert!(summary.zero_or_negative_margin_cells.is_empty());
}

// ============================================================================
// 9. DECISIVE BIFURCATION: BRANCH A CONFIRMED VS BRANCH B DETECTED
// ============================================================================

/// Toy 2D quadratic system with exact isolated root at (1, 1).
fn toy_quadratic_system_2d() -> SquarePolynomialSystem {
    let c0 = rq(-2, 1);
    let a0 = vec![rq(0, 1), rq(1, 1)];
    let h0 = RationalMatrix::from_rows(vec![vec![rq(2, 1), rq(0, 1)], vec![rq(0, 1), rq(0, 1)]]);
    let q0 = QuadraticComponent::new(c0, a0, h0);

    let c1 = rq(-2, 1);
    let a1 = vec![rq(1, 1), rq(0, 1)];
    let h1 = RationalMatrix::from_rows(vec![vec![rq(0, 1), rq(0, 1)], vec![rq(0, 1), rq(2, 1)]]);
    let q1 = QuadraticComponent::new(c1, a1, h1);

    SquarePolynomialSystem::new(vec![q0, q1])
}

#[test]
fn test_decisive_bifurcation_branch_a_and_branch_b() {
    let tree = canonical_global_partition_tree();

    // 1. Branch A: Point on the certified cover evaluates to Branch A
    let pt = SynthesisCandidate::ModuliPoint {
        chart: GrandSynthesisChart::DitaFourierF6,
        coords: vec![rq(1, 4), rq(1, 4)],
    };
    let eval_a =
        evaluate_grand_synthesis(&pt, &tree).expect("Evaluation on certified cover must succeed");

    assert!(eval_a.margin_validated);
    assert!(eval_a.smale_root_absent);
    assert!(eval_a.no_fourth_basis);

    match eval_a.branch {
        BifurcationBranch::BranchA {
            margin,
            zero_rel_empty,
            no_fourth_basis,
            smale_alpha_ge_alpha0,
            ..
        } => {
            assert!(margin >= certified_margin());
            assert!(zero_rel_empty);
            assert!(no_fourth_basis);
            // No Smale alpha is evaluated at a cover point.
            assert_eq!(smale_alpha_ge_alpha0, None);
        }
        other => panic!("Expected Branch A on certified cover, got {other:?}"),
    }

    // 2. Branch B: Synthetic root injection triggers Branch B detection
    let sys = toy_quadratic_system_2d();
    let exact_root = vec![rq(1, 1), rq(1, 1)];
    let small_perturbation = rq(1, 500); // 1/500: inside Smale basin of attraction
    let box_radius = rq(1, 10);

    let branch_b =
        evaluate_synthetic_root_bifurcation(&sys, &exact_root, &small_perturbation, &box_radius)
            .expect("Synthetic root evaluation should compute");

    match branch_b {
        BifurcationBranch::BranchB {
            alpha,
            approximate_zero_detected,
            witness_coords,
        } => {
            assert!(alpha < smale_alpha_threshold());
            assert!(approximate_zero_detected);
            assert_eq!(witness_coords, vec![rq(501, 500), rq(501, 500)]);
        }
        other => panic!("Expected Branch B for genuine approximate zero, got {other:?}"),
    }

    // 3. Mutual exclusivity verification
    assert!(verify_bifurcation_mutual_exclusivity(true, false));
    assert!(verify_bifurcation_mutual_exclusivity(false, true));
    assert!(!verify_bifurcation_mutual_exclusivity(true, true));
    assert!(!verify_bifurcation_mutual_exclusivity(false, false));
}

// ============================================================================
// 10. END-TO-END GRAND SYNTHESIS PIPELINE & RECEIPT CERTIFIER
// ============================================================================

#[test]
fn test_end_to_end_grand_synthesis_pipeline_all_candidates() {
    let tree = canonical_global_partition_tree();

    // 1. Matrix candidate: standard Fourier F_6
    let f6 = standard_fourier_f6();
    let cand_f6 = SynthesisCandidate::Matrix(f6);
    let eval_f6 =
        evaluate_grand_synthesis(&cand_f6, &tree).expect("F6 pipeline evaluation must succeed");

    assert_eq!(eval_f6.chart, GrandSynthesisChart::DitaFourierF6);
    assert_eq!(eval_f6.cross_ratio_count, NUM_SUBMATRICES_225);
    assert_eq!(eval_f6.orbit_class, Some(OrbitClass::Fourier));
    assert!(eval_f6.margin_validated);
    assert!(eval_f6.smale_root_absent);
    assert!(eval_f6.no_fourth_basis);

    // 2. Matrix candidate: Tao S_6
    let s6 = tao_s6_matrix();
    let cand_s6 = SynthesisCandidate::Matrix(s6);
    let eval_s6 =
        evaluate_grand_synthesis(&cand_s6, &tree).expect("S6 pipeline evaluation must succeed");

    assert_eq!(eval_s6.chart, GrandSynthesisChart::TaoConfluenceS6);
    assert_eq!(eval_s6.orbit_class, Some(OrbitClass::Tao));
    assert!(eval_s6.margin_validated);
    assert!(eval_s6.no_fourth_basis);

    // 3. Matrix candidate: Haagerup H_6
    let h6 = haagerup_h6_matrix();
    let cand_h6 = SynthesisCandidate::Matrix(h6);
    let eval_h6 =
        evaluate_grand_synthesis(&cand_h6, &tree).expect("H6 pipeline evaluation must succeed");

    assert_eq!(eval_h6.chart, GrandSynthesisChart::HaagerupOrbitH6);
    assert_eq!(eval_h6.orbit_class, Some(OrbitClass::Haagerup));
    assert!(eval_h6.margin_validated);
    assert!(eval_h6.no_fourth_basis);

    // 4. Moduli points in Collar and Karlsson charts
    let pt_collar = SynthesisCandidate::ModuliPoint {
        chart: GrandSynthesisChart::PeriodicCollar2D,
        coords: vec![rq(1, 4), rq(1, 4)],
    };
    let eval_collar =
        evaluate_grand_synthesis(&pt_collar, &tree).expect("Collar point evaluation must succeed");
    assert_eq!(eval_collar.chart, GrandSynthesisChart::PeriodicCollar2D);
    assert!(eval_collar.no_fourth_basis);

    let pt_karlsson = SynthesisCandidate::ModuliPoint {
        chart: GrandSynthesisChart::KarlssonVolumeExterior,
        coords: vec![rq(1, 4), rq(1, 4), rq(1, 2000)],
    };
    let eval_karlsson = evaluate_grand_synthesis(&pt_karlsson, &tree)
        .expect("Karlsson point evaluation must succeed");
    assert_eq!(
        eval_karlsson.chart,
        GrandSynthesisChart::KarlssonVolumeExterior
    );
    assert!(eval_karlsson.no_fourth_basis);
}

#[test]
fn test_certify_full_grand_synthesis() {
    let receipt =
        certify_grand_synthesis().expect("Full Grand Synthesis certification must succeed");

    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(receipt.total_cell_count, 28);
    assert_eq!(receipt.total_volume, rq(5001, 1000));
    assert!(receipt.volume_conserved);
    assert!(receipt.circulation_receipt.certified);
    assert!(receipt.sentry_all_cells_positive);
    assert_eq!(receipt.sentry_min_margin, certified_margin());
    assert_eq!(
        receipt.f6_evaluation.chart,
        GrandSynthesisChart::DitaFourierF6
    );
    assert!(!receipt.receipt_hash.is_empty());
    assert!(receipt.certified);
}

// ============================================================================
// 11. NEGATIVE CONTROLS
// ============================================================================

#[test]
fn test_negative_control_cell_construction_rejection() {
    // Degenerate interval rejection: lo >= hi
    let res = SynthesisLeafCell::new(
        "bad_cell",
        GrandSynthesisChart::DitaFourierF6,
        vec![(rq(1, 2), rq(1, 4))],
        certified_margin(),
        "Test",
    );
    assert!(matches!(
        res,
        Err(GrandSynthesisError::DegenerateInterval { .. })
    ));

    // Non-positive margin rejection: margin <= 0
    let res_margin = SynthesisLeafCell::new(
        "bad_margin_cell",
        GrandSynthesisChart::DitaFourierF6,
        vec![(rq(0, 1), rq(1, 2))],
        BigRational::zero(),
        "Test",
    );
    assert!(matches!(
        res_margin,
        Err(GrandSynthesisError::NonPositiveMargin { .. })
    ));
}

#[test]
fn test_negative_control_volume_conservation_rejection() {
    let tree = canonical_global_partition_tree();
    // Drop one cell (leaving 27 cells)
    let mutated_leaves: Vec<SynthesisLeafCell> = tree.leaves.iter().take(27).cloned().collect();
    let mutated_tree = GrandSynthesisPartitionTree::new(mutated_leaves);

    let res = verify_volume_conservation(&mutated_tree);
    assert!(res.is_err());
    match res.unwrap_err() {
        GrandSynthesisError::VolumeMismatch { .. } => {}
        e => panic!("Expected VolumeMismatch, got {:?}", e),
    }
}

// ============================================================================
// COMPUTED BRANCH FLAGS (formerly hard-coded)
// ============================================================================

#[test]
fn combinatorial_gluing_enumerates_all_35_triples_with_4_candidates_each() {
    let receipt = verify_all_combinatorial_triples(COMPLETE_MUB_BASES_COUNT)
        .expect("the 7-basis enumeration must succeed");
    assert_eq!(receipt.complete_mub_bases, 7);
    assert_eq!(receipt.total_triples, TOTAL_COMBINATORIAL_TRIPLES_COUNT);
    assert_eq!(TOTAL_COMBINATORIAL_TRIPLES_COUNT, 35);
    assert_eq!(
        receipt.candidates_per_triple,
        REMAINING_CANDIDATE_BASES_COUNT
    );
    assert_eq!(REMAINING_CANDIDATE_BASES_COUNT, 4);
    assert_eq!(
        candidate_fourth_indices([0, 3, 6], 7).unwrap(),
        vec![1, 2, 4, 5]
    );
}

#[test]
fn candidate_fourth_indices_refuses_a_repeated_or_out_of_range_basis() {
    assert!(matches!(
        candidate_fourth_indices([0, 0, 1], 7),
        Err(GrandSynthesisError::InvalidBasisTriple { .. })
    ));
    assert!(matches!(
        candidate_fourth_indices([0, 1, 7], 7),
        Err(GrandSynthesisError::InvalidBasisTriple { .. })
    ));
}

#[test]
fn verify_all_combinatorial_triples_refuses_family_smaller_than_3_bases() {
    assert!(matches!(
        verify_all_combinatorial_triples(2),
        Err(GrandSynthesisError::InvalidBasisTriple { total_bases: 2, .. })
    ));
    assert!(matches!(
        verify_all_combinatorial_triples(0),
        Err(GrandSynthesisError::InvalidBasisTriple { total_bases: 0, .. })
    ));
}

#[test]
fn a_cover_evaluation_carries_the_gluing_it_computed() {
    let tree = canonical_global_partition_tree();
    let eval = evaluate_grand_synthesis(
        &SynthesisCandidate::ModuliPoint {
            chart: GrandSynthesisChart::TaoConfluenceS6,
            coords: vec![rq(1, 4), rq(1, 4)],
        },
        &tree,
    )
    .expect("a point on the certified cover must evaluate");
    assert_eq!(eval.combinatorial_gluing.total_triples, 35);
    assert_eq!(eval.combinatorial_gluing.candidates_per_triple, 4);
}

#[test]
fn a_far_synthetic_point_is_not_reported_as_branch_a() {
    // (2, 2) is far from the toy root (1, 1): alpha exceeds 157/1000.
    let branch = evaluate_synthetic_root_bifurcation(
        &toy_quadratic_system_2d(),
        &[rq(1, 1), rq(1, 1)],
        &rq(1, 1),
        &rq(1, 10),
    )
    .expect("Synthetic root evaluation should compute");
    match branch {
        BifurcationBranch::NoRootCertified {
            alpha,
            alpha_ge_alpha0,
            ..
        } => {
            assert!(alpha >= smale_alpha_threshold(), "alpha = {alpha}");
            assert!(alpha_ge_alpha0);
        }
        other => panic!("a far point must not be Branch A or B, got {other:?}"),
    }
}

#[test]
fn certification_requires_every_premise_that_ran() {
    let receipt = certify_grand_synthesis().expect("certification must run");
    let (vol, circ, f6) = (
        receipt.volume_receipt.clone(),
        receipt.circulation_receipt.clone(),
        receipt.f6_evaluation.clone(),
    );
    assert!(receipt.certified);
    assert!(grand_synthesis_certified(&vol, &circ, true, &f6));

    let mut bad_volume = vol.clone();
    bad_volume.certified = false;
    assert!(!grand_synthesis_certified(&bad_volume, &circ, true, &f6));

    let mut bad_circulation = circ.clone();
    bad_circulation.certified = false;
    assert!(!grand_synthesis_certified(
        &vol,
        &bad_circulation,
        true,
        &f6
    ));

    assert!(!grand_synthesis_certified(&vol, &circ, false, &f6));

    let mut no_root_certified = f6.clone();
    no_root_certified.branch = BifurcationBranch::NoRootCertified {
        alpha: rq(1, 1),
        alpha_ge_alpha0: true,
        reason: "probe".to_string(),
    };
    assert!(!grand_synthesis_certified(
        &vol,
        &circ,
        true,
        &no_root_certified
    ));

    let mut fourth_basis_open = f6;
    fourth_basis_open.no_fourth_basis = false;
    assert!(!grand_synthesis_certified(
        &vol,
        &circ,
        true,
        &fourth_basis_open
    ));

    let mut bad_margin = fourth_basis_open.clone();
    bad_margin.no_fourth_basis = true;
    bad_margin.margin_validated = false;
    assert!(!grand_synthesis_certified(&vol, &circ, true, &bad_margin));

    let mut incomplete_gluing = bad_margin.clone();
    incomplete_gluing.margin_validated = true;
    incomplete_gluing.combinatorial_gluing.total_triples = 34;
    assert!(!grand_synthesis_certified(
        &vol,
        &circ,
        true,
        &incomplete_gluing
    ));

    let mut bad_candidates = incomplete_gluing;
    bad_candidates.combinatorial_gluing.total_triples = TOTAL_COMBINATORIAL_TRIPLES_COUNT;
    bad_candidates.combinatorial_gluing.candidates_per_triple = 3;
    assert!(!grand_synthesis_certified(
        &vol,
        &circ,
        true,
        &bad_candidates
    ));
}

#[test]
fn volume_receipt_with_non_positive_cell_is_not_certified() {
    let receipt = certify_grand_synthesis().expect("certification must run");
    let mut vol = receipt.volume_receipt.clone();
    vol.all_volumes_positive = false;
    vol.certified = false;
    assert!(!grand_synthesis_certified(
        &vol,
        &receipt.circulation_receipt,
        true,
        &receipt.f6_evaluation,
    ));
}
