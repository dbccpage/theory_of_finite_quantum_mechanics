//! Comprehensive Integration and Unit Test Suite for Target B2:
//! Global Manifold Gluing and Cross-Section Holonomy Obstruction Engine.
//!
//! AuthorityEffect: None
//!
//! Enforces 100% exact rational and cyclotomic arithmetic, strict zero-floating-point
//! discipline via AST-level inspection with `syn`, exact Čech cocycle condition across
//! all covering nerve triples, non-trivial loop holonomy Hol(γ) ≠ I_6 around generating loops
//! of π_1(ℳ_6), discrete cycle circulation obstruction Φ_1 ≥ Γ > 0 via Network Simplex,
//! and negative controls rejecting perturbed cocycles, gauge twist corruptions, and zero circulation.

use std::fs;
use std::path::Path;
use syn::visit::Visit;

use num_rational::BigRational;
use num_traits::Zero;

use tfqm_mub::native::exact::mub6_constants::{
    base_gap, certified_erosion, certified_margin, delta_certified, delta_crit, lipschitz_bound,
};
use tfqm_mub::native::exact::mub6_global_gluing::{
    canonical_gauge_for_chart, circulation_gamma_threshold, enumerate_nerve1_edges,
    enumerate_nerve2_triples, evaluate_target_b2_global_gluing, is_holonomy_non_trivial, is_nerve1,
    is_nerve2, loop_holonomy, path_holonomy, solve_loop_circulation,
    verify_global_cross_section_obstruction, verify_pointwise_obstruction, GlobalGluingError,
    ModuliChart5, ModuliLoop, ModuliPoint6, TransitionCocycleFamily, Unitary6,
    NUM_CHARTS,
};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;
use engine_number_theory::rational::rq;

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
        .join("mub6_global_gluing.rs");

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
        "Target B2 mub6_global_gluing.rs violated zero-float discipline: {:?}",
        visitor.found_floats
    );

    // 2. Exact string search: zero occurrences of f32 or f64
    assert!(
        !source.contains("f32"),
        "mub6_global_gluing.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_global_gluing.rs must contain zero f64 occurrences"
    );
}

#[test]
fn test_negative_control_ast_visitor_catches_floats() {
    // Negative control: Verify that our AST visitor genuinely flags forbidden float types and literals
    let synthetic_source_with_float = r#"
        fn forbidden_calculation() {
            let a: f64 = 1.25;
            let b: f32 = 0.5;
        }
    "#;
    let syntax_tree = syn::parse_file(synthetic_source_with_float)
        .expect("Failed to parse synthetic float source");

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.len() >= 4,
        "AST visitor must detect both float types and both float literals"
    );
    assert!(visitor.found_floats.iter().any(|f| f.contains("f64")));
    assert!(visitor.found_floats.iter().any(|f| f.contains("f32")));
}

// ============================================================================
// 2. CERTIFIED TOPOLOGICAL AND CIRCULATION CONSTANTS
// ============================================================================

#[test]
fn test_certified_topological_and_circulation_constants() {
    let gamma = circulation_gamma_threshold();
    let eps_min = certified_margin();
    let eps_0 = base_gap();
    let l = lipschitz_bound();
    let delta = delta_certified();
    let erosion = certified_erosion();
    let d_crit = delta_crit();

    // 1. Exact rational values matching Lean 4 formalization
    assert_eq!(
        gamma,
        rq(12133, 5000),
        "Γ must equal 12133 / 5000"
    );
    assert_eq!(eps_min, rq(12133, 30000), "ε_min must equal 12133 / 30000");
    assert_eq!(eps_0, rq(37249, 90000), "ε_0 must equal 37249 / 90000");
    assert_eq!(l, rq(85, 9), "L must equal 85 / 9");
    assert_eq!(delta, rq(1, 1000), "δ must equal 1 / 1000");
    assert_eq!(erosion, rq(17, 1800), "L · δ must equal 17 / 1800");
    assert_eq!(
        d_crit,
        rq(37249, 850000),
        "δ_crit must equal 37249 / 850000"
    );

    // 2. Exact relation: 6 · ε_min = Γ
    let six = BigRational::from_integer(6.into());
    let computed_gamma = &six * &eps_min;
    assert_eq!(
        computed_gamma, gamma,
        "6 · ε_min must identically equal Γ = 12133 / 5000"
    );

    // 3. Exact relation: ε_0 - L · δ = ε_min
    let computed_margin = &eps_0 - &erosion;
    assert_eq!(
        computed_margin, eps_min,
        "ε_0 - L · δ must identically equal ε_min = 12133 / 30000"
    );

    // 4. Strict positivity
    assert!(gamma > BigRational::zero(), "Γ must be strictly positive");
    assert!(
        eps_min > BigRational::zero(),
        "ε_min must be strictly positive"
    );
    assert!(
        delta < d_crit,
        "Certified step 1/1000 must be strictly below critical threshold 37249/850000"
    );
}

// ============================================================================
// 3. CANONICAL 5-CHART MODULI COVERING NERVE
// ============================================================================

#[test]
fn test_canonical_5_charts_and_nerve_bijection() {
    assert_eq!(NUM_CHARTS, 5);
    assert_eq!(ModuliChart5::ALL.len(), 5);

    // 1. Bijective indexing roundtrip
    for (expected_idx, &chart) in ModuliChart5::ALL.iter().enumerate() {
        assert_eq!(chart.to_index(), expected_idx);
        assert_eq!(ModuliChart5::from_index(expected_idx), Some(chart));
        assert!(!chart.name().is_empty());
        assert!(!chart.canonical_id().is_empty());
        assert!(chart.default_margin() >= certified_margin());
    }
    assert_eq!(ModuliChart5::from_index(5), None);

    // 2. Nerve1 reflexivity: every chart overlaps with itself
    for &c in &ModuliChart5::ALL {
        assert!(is_nerve1(c, c), "Chart {:?} must overlap with itself", c);
    }

    // 3. Nerve1 symmetry: is_nerve1(i, j) == is_nerve1(j, i)
    for &i in &ModuliChart5::ALL {
        for &j in &ModuliChart5::ALL {
            assert_eq!(
                is_nerve1(i, j),
                is_nerve1(j, i),
                "Nerve1 must be symmetric for ({:?}, {:?})",
                i,
                j
            );
        }
    }

    // 4. Key topological chart overlaps matching Lean 4 formalization
    let c0 = ModuliChart5::SzollosiCurve;
    let c1 = ModuliChart5::KarlssonManifold;
    let c2 = ModuliChart5::DeltoidCusps;
    let c3 = ModuliChart5::HaagerupOrbit;
    let c4 = ModuliChart5::TaoConfluence;

    // Overlaps present:
    assert!(is_nerve1(c0, c1));
    assert!(is_nerve1(c0, c2));
    assert!(is_nerve1(c1, c2));
    assert!(is_nerve1(c1, c3));
    assert!(is_nerve1(c0, c4));
    assert!(is_nerve1(c1, c4));

    // Overlaps absent:
    assert!(
        !is_nerve1(c2, c3),
        "Deltoid cusps do not overlap with Haagerup"
    );
    assert!(!is_nerve1(c2, c4), "Deltoid cusps do not overlap with Tao");
    assert!(
        !is_nerve1(c3, c0),
        "Haagerup does not overlap with Szollosi"
    );
    assert!(!is_nerve1(c3, c4), "Haagerup does not overlap with Tao");

    // 5. Canonical 3-simplices in Nerve2
    // Deltoid corner: (0, 1, 2)
    assert!(
        is_nerve2(c0, c1, c2),
        "Canonical deltoid corner (0, 1, 2) must be in Nerve2"
    );
    assert!(is_nerve2(c1, c2, c0));
    assert!(is_nerve2(c2, c0, c1));

    // Tao confluence corner: (0, 1, 4)
    assert!(
        is_nerve2(c0, c1, c4),
        "Canonical Tao corner (0, 1, 4) must be in Nerve2"
    );
    assert!(is_nerve2(c1, c4, c0));
    assert!(is_nerve2(c4, c0, c1));

    // Haagerup is not part of any 3-cycle of distinct vertices
    assert!(!is_nerve2(c0, c1, c3));
    assert!(!is_nerve2(c2, c1, c3));

    // 6. Complete enumeration
    let edges = enumerate_nerve1_edges();
    let triples = enumerate_nerve2_triples();

    // 5 diagonal edges + 2 * 6 off-diagonal = 17 edges
    assert_eq!(
        edges.len(),
        17,
        "Nerve1 must contain exactly 17 directed edges"
    );
    assert!(
        triples.len() >= 12,
        "Nerve2 must contain all valid triple intersections"
    );
}

// ============================================================================
// 4. UNITARY TRANSITION COCYCLES & ČECH COCYCLE CONDITION
// ============================================================================

#[test]
fn test_canonical_transition_cocycles_and_cech_condition() {
    let family = TransitionCocycleFamily::canonical();

    // 1. Verify all chart gauges are exact unitary matrices
    for &chart in &ModuliChart5::ALL {
        let g = canonical_gauge_for_chart(chart);
        assert!(!g.matrix[0][0].is_zero());
        let id_check = g.mul(&g.inv());
        assert!(
            id_check.is_identity(),
            "Canonical gauge for {:?} must be unitary",
            chart
        );
    }

    // 2. Diagonal identity law: c_{ii} == I_6
    assert!(family.verify_diagonal_identity().is_ok());

    // 3. Inversion symmetry law: c_{ji} == c_{ij}†
    assert!(family.verify_inversion_symmetry().is_ok());

    // 4. Exact Čech cocycle condition across all Nerve2 triples: c_{ij} · c_{jk} · c_{ki} == I_6
    let cech_rep = family
        .verify_cech_cocycle()
        .expect("Čech cocycle verification failed");
    assert!(cech_rep.all_triples_valid);
    assert!(cech_rep.deltoid_corner_valid);
    assert!(cech_rep.tao_corner_valid);
    assert!(cech_rep.total_triples_checked >= 12);

    // 5. Explicit check on canonical deltoid corner: (0, 1, 2)
    let c0 = ModuliChart5::SzollosiCurve;
    let c1 = ModuliChart5::KarlssonManifold;
    let c2 = ModuliChart5::DeltoidCusps;

    let c01 = family.get(c0, c1);
    let c12 = family.get(c1, c2);
    let c20 = family.get(c2, c0);

    // Transitions between distinct charts are genuinely non-trivial
    assert!(
        !c01.is_identity(),
        "Transition c_{{01}} must be non-trivial"
    );
    assert!(
        !c12.is_identity(),
        "Transition c_{{12}} must be non-trivial"
    );
    assert!(
        !c20.is_identity(),
        "Transition c_{{20}} must be non-trivial"
    );

    // Their ordered product is identically identity
    let deltoid_prod = c01.mul(c12).mul(c20);
    assert!(
        deltoid_prod.is_identity(),
        "Deltoid corner product c_{{01}} c_{{12}} c_{{20}} must be I_6"
    );

    // 6. Explicit check on Tao confluence corner: (0, 1, 4)
    let c4 = ModuliChart5::TaoConfluence;
    let c14 = family.get(c1, c4);
    let c40 = family.get(c4, c0);

    let tao_prod = c01.mul(c14).mul(c40);
    assert!(
        tao_prod.is_identity(),
        "Tao corner product c_{{01}} c_{{14}} c_{{40}} must be I_6"
    );
}

// ============================================================================
// 5. NEGATIVE CONTROLS: PERTURBED COCYCLE & GAUGE CORRUPTION REJECTION
// ============================================================================

#[test]
fn test_negative_control_perturbed_cech_cocycle_rejected() {
    let mut corrupted = TransitionCocycleFamily::canonical();

    // Perturb transition c_{01} by a non-trivial root of unity phase twist ζ_24^1
    let twist = {
        let zero = Cyc24::zero();
        let phase = Cyc24::zeta24(1);
        let mat = std::array::from_fn(|i| {
            std::array::from_fn(|j| if i == j { phase.clone() } else { zero.clone() })
        });
        Unitary6::from_matrix_unchecked(mat)
    };

    let orig_c01 = corrupted.get(ModuliChart5::SzollosiCurve, ModuliChart5::KarlssonManifold);
    let perturbed_c01 = orig_c01.mul(&twist);
    corrupted.transitions[0][1] = perturbed_c01;

    // Čech cocycle verification MUST fail and reject the perturbed cocycle
    let res = corrupted.verify_cech_cocycle();
    assert!(
        res.is_err(),
        "Perturbed cocycle must be rejected by verify_cech_cocycle"
    );

    match res {
        Err(GlobalGluingError::CechCocycleViolation { i, j, k }) => {
            assert!(
                (i == 0 && j == 1) || (j == 0 && k == 1) || (k == 0 && i == 1),
                "Violation must involve the perturbed edge (0, 1)"
            );
        }
        other => panic!("Expected CechCocycleViolation, got {:?}", other),
    }
}

#[test]
fn test_negative_control_inversion_symmetry_corruption_rejected() {
    let mut corrupted = TransitionCocycleFamily::canonical();

    // Break inversion symmetry: set c_{10} = I_6 while c_{01} ≠ I_6
    corrupted.transitions[1][0] = Unitary6::identity();

    let res = corrupted.verify_inversion_symmetry();
    assert!(
        res.is_err(),
        "Corrupted inversion symmetry must be rejected"
    );

    match res {
        Err(GlobalGluingError::InversionSymmetryViolation { i, j }) => {
            assert!((i == 0 && j == 1) || (i == 1 && j == 0));
        }
        other => panic!("Expected InversionSymmetryViolation, got {:?}", other),
    }
}

#[test]
fn test_negative_control_diagonal_identity_corruption_rejected() {
    let mut corrupted = TransitionCocycleFamily::canonical();

    // Break diagonal identity: set c_{00} = ζ_24^4 · I_6 ≠ I_6
    let twist = {
        let zero = Cyc24::zero();
        let phase = Cyc24::zeta24(4);
        let mat = std::array::from_fn(|i| {
            std::array::from_fn(|j| if i == j { phase.clone() } else { zero.clone() })
        });
        Unitary6::from_matrix_unchecked(mat)
    };
    corrupted.transitions[0][0] = twist;

    let res = corrupted.verify_diagonal_identity();
    assert!(res.is_err(), "Corrupted diagonal identity must be rejected");

    match res {
        Err(GlobalGluingError::DiagonalIdentityViolation { chart }) => {
            assert_eq!(chart, 0);
        }
        other => panic!("Expected DiagonalIdentityViolation, got {:?}", other),
    }
}

// ============================================================================
// 6. GENERATING LOOPS OF π_1(ℳ₆) AND LOOP HOLONOMY OPERATOR
// ============================================================================

#[test]
fn test_generating_loops_and_holonomy_non_triviality() {
    let family = TransitionCocycleFamily::canonical();

    // 1. Flat deltoid 3-cycle in the nerve has trivial holonomy: Hol(γ_deltoid) == I_6
    let deltoid_loop = ModuliLoop::deltoid_3cycle();
    let deltoid_hol = loop_holonomy(&family, &deltoid_loop);
    assert!(
        deltoid_hol.is_identity(),
        "Contractible 3-cycle in flat nerve must have trivial holonomy"
    );
    assert!(!is_holonomy_non_trivial(&deltoid_hol));

    // 2. Generating loop around periodic collar torus T² carrying non-trivial monodromy twist
    let collar_gen = ModuliLoop::torus_collar_generator(4);
    let collar_hol = loop_holonomy(&family, &collar_gen);

    // Holonomy is non-trivial: Hol(γ) ≠ I_6
    assert!(
        is_holonomy_non_trivial(&collar_hol),
        "Generating loop of π_1(ℳ₆) must have non-trivial holonomy Hol(γ) ≠ I_6"
    );
    assert!(!collar_hol.is_identity());

    // Trace of holonomy differs from 6: Tr(Hol(γ)) ≠ 6
    let tr = collar_hol.trace();
    let tr_id = Cyc24::rat(ri(6));
    assert_ne!(
        tr, tr_id,
        "Trace of non-trivial holonomy must differ from 6"
    );

    // 3. Twisted deltoid loop
    let twisted_deltoid = ModuliLoop::twisted_deltoid_loop(6);
    let twisted_hol = loop_holonomy(&family, &twisted_deltoid);
    assert!(is_holonomy_non_trivial(&twisted_hol));

    // 4. Path holonomy along path of length 1 is identity
    let single_node = [ModuliChart5::SzollosiCurve];
    let single_hol = path_holonomy(&family, &single_node);
    assert!(single_hol.is_identity());
}

// ============================================================================
// 7. NETWORK SIMPLEX DISCRETE CYCLE CIRCULATION SOLVER
// ============================================================================

#[test]
fn test_network_simplex_circulation_deltoid_3cycle() {
    let deltoid_loop = ModuliLoop::deltoid_3cycle();
    let scale: i128 = 30000;

    let report = solve_loop_circulation(&deltoid_loop, scale, None)
        .expect("Network Simplex circulation failed on deltoid 3-cycle");

    assert_eq!(report.num_edges, 3);
    assert_eq!(report.edge_cochain.len(), 3);

    // Each edge has margin at least ε_min = 12133 / 30000, scaled to ≥ 12133
    for &w in &report.edge_cochain {
        assert!(w >= 12133);
    }

    // Net circulation is positive
    assert!(report.net_circulation >= 3 * 12133);

    // Exact cycle circulation invariance: ∑_{e in γ} (dα)_e == 0 identically
    assert_eq!(
        report.coboundary_sum, 0,
        "Coboundary sum around directed cycle must be identically zero"
    );
    assert!(report.circulation_conserved);

    // Zero duality gap certified
    assert!(report.dual_gap_zero);

    // L1 circulation lower bound: Φ_1 >= net_circulation > 0
    assert!(report.phi1_objective >= report.net_circulation);
    assert!(report.obstruction_certified);
}

#[test]
fn test_network_simplex_circulation_composite_6cycle_threshold() {
    let composite_6 = ModuliLoop::composite_6cycle();
    let scale: i128 = 30000;

    let report = solve_loop_circulation(&composite_6, scale, None)
        .expect("Network Simplex circulation failed on composite 6-cycle");

    assert_eq!(report.num_edges, 6);
    assert_eq!(report.edge_cochain.len(), 6);

    // Expected threshold Γ_scaled = (12133 / 5000) * 30000 = 72798
    let gamma_scaled: i128 = (12133_i128 * scale) / 5000;
    assert_eq!(gamma_scaled, 72798);

    // Verify Φ_1 >= Γ_scaled
    assert!(
        report.phi1_objective >= gamma_scaled,
        "Composite 6-cycle circulation Φ_1 ({}) must meet or exceed threshold Γ ({})",
        report.phi1_objective,
        gamma_scaled
    );

    // Invariance and duality verification
    assert_eq!(report.coboundary_sum, 0);
    assert!(report.circulation_conserved);
    assert!(report.dual_gap_zero);
    assert!(report.obstruction_certified);
}

#[test]
fn test_negative_control_zero_circulation_rejected() {
    let deltoid_loop = ModuliLoop::deltoid_3cycle();
    let scale: i128 = 30000;

    // Propose an uncertified zero defect vector [0, 0, 0]
    let zero_defects = vec![
        BigRational::zero(),
        BigRational::zero(),
        BigRational::zero(),
    ];

    let res = solve_loop_circulation(&deltoid_loop, scale, Some(zero_defects));
    assert!(res.is_err(), "Zero-circulation proposal must be rejected");

    match res {
        Err(GlobalGluingError::NonPositiveCirculation {
            net_circulation, ..
        }) => {
            assert!(net_circulation <= 0);
        }
        other => panic!("Expected NonPositiveCirculation, got {:?}", other),
    }
}

// ============================================================================
// 8. GLOBAL CROSS-SECTION OBSTRUCTION & MASTER GLUING SYNTHESIS
// ============================================================================

#[test]
fn test_global_cross_section_obstruction_verification() {
    let family = TransitionCocycleFamily::canonical();
    let collar_gen = ModuliLoop::torus_collar_generator(4);

    // 1. Verify pointwise obstruction across all 5 charts
    for &chart in &ModuliChart5::ALL {
        let p = ModuliPoint6::sample_for_chart(chart);
        assert!(
            verify_pointwise_obstruction(&p),
            "Point on chart {:?} must be obstructed",
            chart
        );
    }

    // 2. Verify global cross-section obstruction:
    // Non-existence of continuous fourth basis section across ℳ₆
    let cross_section_obstructed = verify_global_cross_section_obstruction(&family, &collar_gen);
    assert!(
        cross_section_obstructed,
        "Continuous fourth basis section must be obstructed across ℳ₆"
    );
}

#[test]
fn test_master_target_b2_global_gluing_synthesis() {
    let report = evaluate_target_b2_global_gluing()
        .expect("Master Target B2 global gluing synthesis failed");

    // 1. Epistemic boundaries
    assert_eq!(report.authority_effect, "None");
    assert!(report.firewall.contains("stated region only; mints no authority"));

    // 2. Constants
    assert_eq!(report.gamma_threshold, circulation_gamma_threshold());
    assert_eq!(report.min_margin, certified_margin());

    // 3. Covering nerve
    assert_eq!(report.num_charts, 5);
    assert_eq!(report.num_nerve1_edges, 17);
    assert!(report.num_nerve2_triples >= 12);

    // 4. Čech cocycle verification
    assert!(report.cech_cocycle_verified);
    assert!(report.deltoid_corner_cech_verified);
    assert!(report.tao_corner_cech_verified);

    // 5. Loop holonomy
    assert!(report.non_trivial_holonomy_verified);

    // 6. Network Simplex circulation
    assert!(report.deltoid_circulation_phi1 > 0);
    assert!(report.composite_circulation_phi1 >= 72798);
    assert!(report.circulation_obstruction_verified);

    // 7. Global cross-section obstruction
    assert!(report.global_cross_section_obstructed);

    // 8. Configuration-level non-existence certificate
    assert!(
        report.no_complete_mub6,
        "Master synthesis must certify NoCompleteMUB6 under declared premises"
    );
}
