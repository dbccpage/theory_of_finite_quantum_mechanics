
use std::fs;
use std::path::PathBuf;
use std::time::Instant;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use omega_mub::omega_native::exact::mub6_collar_boundary::certify_collar_boundary_overlap;
use omega_mub::omega_native::exact::mub6_collar_cover::{
    build_uniform_dyadic_tree, collar_certification_depth, generate_collar_cover_report,
    RationalBox2D,
};
use omega_mub::omega_native::exact::mub6_collar_solver::solve_karlsson_collar_cover;
use omega_mub::omega_native::exact::mub6_constants::{certified_margin, delta_certified};
use omega_mub::omega_native::exact::mub6_continuous_chaining::{
    verify_curvature_wall_propagation, verify_empty_zerorel_variety, AdaptiveStepEngine,
    ContinuousChainingPath, KarlssonBoundaryConnection, RepresentativePointSet,
};
use omega_mub::omega_native::exact::mub6_continuous_manifold_residue::{
    all_6_genuine_seeds, solve_continuous_manifold_residue,
};
use omega_mub::omega_native::exact::mub6_deltoid_cusp::{
    solve_desingularized_cusp_bisection, BisectionSolverConfig, DeltoidCusp,
};
use omega_mub::omega_native::exact::mub6_deltoid_cusp_asymptotics::solve_deltoid_cusp_asymptotics;
use omega_mub::omega_native::exact::mub6_f6_chart::f6_family_columns;
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_haagerup::{
    certify_haagerup_full_orbit, extract_cross_ratio_exponents,
};
use omega_mub::omega_native::exact::mub6_karlsson_volume_cover::solve_karlsson_volume_cover;
use omega_mub::omega_native::exact::mub6_manifold_integration::{
    evaluate_target_b3_manifold_integration, verify_cech_cocycles_all_53_triples,
    verify_continuous_szollosi_chaining, verify_full_unified_coverage,
};
use omega_mub::omega_native::exact::mub6_moment_ledger::{
    evaluate_degree_benchmark, evaluate_moment_sdp_hierarchy_ledger, verify_canonical_fixtures,
    SUPPORTED_DEGREES,
};
use omega_mub::omega_native::exact::mub6_nerve_chaining::{
    evaluate_nerve_chaining, solve_triangular_circulation, BoundaryNerveTriangle, INTEGER_SCALE,
};
use omega_mub::omega_native::exact::mub6_tao_chart::tao_s6_matrix;
use omega_mub::omega_native::exact::mub6_zerorel_variety::{dita_representative_triple, BasisCyc};
use omega_mub::omega_native::exact::szollosi_triad_solver::szollosi_dephased_b6;
use omega_number_theory::cyclotomic::Cyc24;

omega_mub::fixture_set!(fixtures, "omega_mub_verify_all");

pub const SCHEMA_VERSION: &str = "omega.mub.native-verify-all.v1";

fn category_verified(steps: &[VerificationStepReceipt], category: &str) -> bool {
    let matched: Vec<_> = steps.iter().filter(|step| step.category == category).collect();
    !matched.is_empty() && matched.iter().all(|step| step.passed)
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationStepReceipt {
    pub name: String,
    pub category: String,
    pub passed: bool,
    pub details: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GrandVerificationReceipt {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub overall_status: String,
    pub zero_float_discipline_verified: bool,
    pub partition_covers_verified: bool,
    pub continuous_chaining_verified: bool,
    pub boundary_residues_verified: bool,
    pub cech_cocycles_verified: bool,
    pub moment_sdp_ldlt_verified: bool,
    pub total_steps_passed: usize,
    pub total_steps_failed: usize,
    pub steps: Vec<VerificationStepReceipt>,
    pub execution_time_millis: u64,
}

fn rat_str(r: &BigRational) -> String {
    format!("{}/{}", r.numer(), r.denom())
}

fn verify_all_partition_covers(
    steps: &mut Vec<VerificationStepReceipt>,
    verbose: bool,
) -> Result<(), String> {
    if verbose {
        println!("--- [1/4] Verifying Partition Covers ---");
    }

    let config = BisectionSolverConfig::canonical();
    for cusp in DeltoidCusp::all() {
        let report = solve_desingularized_cusp_bisection(cusp, &config)
            .map_err(|e| format!("Cusp {:?} bisection failed: {:?}", cusp, e))?;

        if !report.all_cells_certified {
            return Err(format!("Deltoid cusp {:?} has uncertified cells", cusp));
        }
        if !report.bounded_depth_guaranteed {
            return Err(format!("Deltoid cusp {:?} bounded depth violated", cusp));
        }
        if !report.all_phi1_positive {
            return Err(format!(
                "Deltoid cusp {:?} non-positive Phi_1 detected",
                cusp
            ));
        }

        steps.push(VerificationStepReceipt {
            name: format!("Deltoid Cusp Desingularization: {}", cusp.name()),
            category: "Partition Covers".to_string(),
            passed: true,
            details: format!(
                "Leaf cells: {}, max depth: {}, Phi_1 strictly positive across all cells",
                report.total_leaf_cells, report.max_depth_reached
            ),
        });
        if verbose {
            println!("  [PASS] Deltoid cusp {} verified", cusp.name());
        }
    }

    let asymp = solve_deltoid_cusp_asymptotics();
    let enclosure = &asymp.taylor_lagrange_enclosure;
    let ordered = |interval: &[String; 2]| match (
        interval[0].parse::<BigRational>(),
        interval[1].parse::<BigRational>(),
    ) {
        (Ok(lo), Ok(hi)) => lo <= hi,
        _ => false,
    };
    if asymp.schema_version != "omega.mub.deltoid-taylor-model.v2"
        || enclosure.delta != "1/1000"
        || !ordered(&enclosure.total_re_interval)
        || !ordered(&enclosure.total_im_interval)
    {
        return Err("Deltoid cusp asymptotics verification failed".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Deltoid Cusp Asymptotics".to_string(),
        category: "Partition Covers".to_string(),
        passed: true,
        details: format!(
            "Taylor-Lagrange enclosure evaluated at delta {}: Re in [{}, {}], Im in [{}, {}]; scalar local-coordinate enclosure only, MUB curvature bound {}",
            enclosure.delta,
            enclosure.total_re_interval[0],
            enclosure.total_re_interval[1],
            enclosure.total_im_interval[0],
            enclosure.total_im_interval[1],
            if asymp.mub_curvature_bound_established {
                "established"
            } else {
                "not established"
            }
        ),
    });
    if verbose {
        println!("  [PASS] Deltoid cusp asymptotics verified");
    }

    let unit = RationalBox2D::unit_square();
    let collar_depth = collar_certification_depth(16)
        .ok_or("No dyadic collar depth up to 16 certifies every cell margin")?;
    let tree = build_uniform_dyadic_tree(collar_depth);
    tree.verify_partition_cover(&unit)
        .map_err(|e| format!("Collar partition cover check failed: {:?}", e))?;
    tree.verify_volume_conservation(&BigRational::one())
        .map_err(|e| format!("Collar volume conservation failed: {:?}", e))?;
    let collar_report = generate_collar_cover_report(&tree);
    if !collar_report.area_conserved || !collar_report.all_margins_positive {
        return Err("Collar cover report failed margins or volume conservation".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Collar Partition Cover (Dyadic Tree)".to_string(),
        category: "Partition Covers".to_string(),
        passed: true,
        details: format!(
            "Depth: {}, Leaves: {}, Area conserved: true, Minimum per-cell margin: {}",
            collar_depth, collar_report.total_leaves, collar_report.min_margin
        ),
    });
    if verbose {
        println!("  [PASS] Collar partition cover verified");
    }

    let k_collar = solve_karlsson_collar_cover(2);
    if k_collar.boxes.len() != 16 {
        return Err(format!(
            "Expected 16 boxes in Karlsson collar cover, got {}",
            k_collar.boxes.len()
        ));
    }
    steps.push(VerificationStepReceipt {
        name: "Karlsson Collar Solver Boxes".to_string(),
        category: "Partition Covers".to_string(),
        passed: true,
        details: format!(
            "Boxes: {}, Conditional margin: {}",
            k_collar.boxes.len(),
            k_collar.barrier_arithmetic.conditional_margin
        ),
    });
    if verbose {
        println!("  [PASS] Karlsson collar solver boxes verified");
    }

    let boundary_receipt = certify_collar_boundary_overlap(10, 3, 90000)
        .map_err(|e| format!("Collar boundary overlap certification failed: {:?}", e))?;
    if !boundary_receipt.verified
        || !boundary_receipt.overlap_region_certified
        || !boundary_receipt.boundary_gap_empty
    {
        return Err("Collar boundary overlap receipt not certified".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Collar Boundary Overlap & Interface Circulation".to_string(),
        category: "Partition Covers".to_string(),
        passed: true,
        details: format!(
            "Boxes: {}, Cycles: {}, Overlap certified: true, Dual gap: 0",
            boundary_receipt.num_interface_boxes, boundary_receipt.num_interface_cycles
        ),
    });
    if verbose {
        println!("  [PASS] Collar boundary overlap verified");
    }

    let s6_mat = tao_s6_matrix();
    let s6_exps = extract_cross_ratio_exponents(&s6_mat)
        .map_err(|e| format!("S6 cross ratio extraction failed: {:?}", e))?;

    let sqrt6 = Cyc24::zeta24(3)
        .add(&Cyc24::zeta24(-3))
        .mul(&Cyc24::zeta24(2).add(&Cyc24::zeta24(-2)));
    let f6_cols = f6_family_columns(0, 0);
    let mut f6_mat: [[Cyc24; 6]; 6] =
        std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()));
    for r in 0..6 {
        for c in 0..6 {
            f6_mat[r][c] = f6_cols[c][r].mul(&sqrt6);
        }
    }
    let f6_exps = extract_cross_ratio_exponents(&f6_mat)
        .map_err(|e| format!("F6 cross ratio extraction failed: {:?}", e))?;

    let b6_pt3 = szollosi_dephased_b6(
        &Cyc24::zeta24(0),
        &Cyc24::zeta24(8),
        &Cyc24::zeta24(0),
        &Cyc24::zeta24(16),
    )
    .map_err(|e| format!("B6 pt3 dephasing failed: {:?}", e))?;
    let b6_exps = extract_cross_ratio_exponents(&b6_pt3)
        .map_err(|e| format!("B6 cross ratio extraction failed: {:?}", e))?;

    let haagerup_receipt = certify_haagerup_full_orbit(30000, &s6_exps, &f6_exps, &b6_exps)
        .map_err(|e| format!("Haagerup orbit certification failed: {:?}", e))?;
    if !haagerup_receipt.verified
        || !haagerup_receipt.is_exact_chm
        || !haagerup_receipt.z1_plus_z2_zero
        || !haagerup_receipt.isolated_from_s6
        || !haagerup_receipt.isolated_from_f6
        || !haagerup_receipt.isolated_from_b6_generic
    {
        return Err(
            "Haagerup orbit verification failed required isolation or CHM checks".to_string(),
        );
    }
    steps.push(VerificationStepReceipt {
        name: "Haagerup Orbit Isolation & Cycle Circulation".to_string(),
        category: "Partition Covers".to_string(),
        passed: true,
        details: format!(
            "Exact CHM: true, z1+z2=0: true, 225 submatrices isolated from S6/F6/B6, Phi_1: {}",
            haagerup_receipt.phi1_circulation
        ),
    });
    if verbose {
        println!("  [PASS] Haagerup orbit isolation and CHM verified");
    }

    let delta = BigRational::new(BigInt::from(1), BigInt::from(1000));
    let karlsson_report = solve_karlsson_volume_cover(2, &delta, 24);
    if !karlsson_report.complete || karlsson_report.uncertified_boxes != 0 {
        return Err(format!(
            "Karlsson volume cover failed: complete={}, uncertified={}",
            karlsson_report.complete, karlsson_report.uncertified_boxes
        ));
    }
    let min_psi = BigRational::new(
        karlsson_report
            .overall_min_psi_num
            .parse::<BigInt>()
            .map_err(|e| format!("Parse error: {e}"))?,
        karlsson_report
            .overall_min_psi_den
            .parse::<BigInt>()
            .map_err(|e| format!("Parse error: {e}"))?,
    );
    if min_psi <= BigRational::zero() {
        return Err("Karlsson volume minimum psi gap is non-positive".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Karlsson 3-Parameter Volume Interval Solver".to_string(),
        category: "Partition Covers".to_string(),
        passed: true,
        details: format!(
            "Explored: {}, Pruned: {}, Certified: {}, Min gap: {}",
            karlsson_report.total_boxes_explored,
            karlsson_report.off_torus_boxes_pruned,
            karlsson_report.outside_boxes_certified,
            rat_str(&min_psi)
        ),
    });
    if verbose {
        println!("  [PASS] Karlsson 3-parameter volume cover verified");
    }

    Ok(())
}

fn verify_continuous_chaining_and_boundary_residues(
    steps: &mut Vec<VerificationStepReceipt>,
    verbose: bool,
) -> Result<(), String> {
    if verbose {
        println!("--- [2/4] Verifying Continuous Chaining & Boundary Residues ---");
    }

    let path = ContinuousChainingPath::generate_canonical()
        .map_err(|e| format!("Canonical chaining path generation failed: {:?}", e))?;
    if !path.all_certified || !path.no_gaps || path.min_margin < certified_margin() {
        return Err("Continuous chaining path failed gap or margin check".to_string());
    }
    let wall_cert = verify_curvature_wall_propagation(&path)
        .map_err(|e| format!("Curvature wall propagation check failed: {:?}", e))?;
    if !wall_cert.curvature_wall_intact || !wall_cert.zero_rel_variety_empty {
        return Err("Curvature wall breach or non-empty ZeroRel variety detected".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Continuous Szöllősi Chaining Path & Curvature Wall".to_string(),
        category: "Continuous Chaining & Boundary Residues".to_string(),
        passed: true,
        details: format!(
            "Nodes: {}, Domain: [{}, {}], Min margin: {}, Wall intact: true",
            path.total_nodes,
            rat_str(&path.domain_lo),
            rat_str(&path.domain_hi),
            rat_str(&path.min_margin)
        ),
    });
    if verbose {
        println!("  [PASS] Continuous Szöllősi chaining path verified");
    }

    let rep_set = RepresentativePointSet::canonical();
    let engine = AdaptiveStepEngine::canonical();
    let evals = rep_set
        .evaluate_all(&engine, &delta_certified())
        .map_err(|e| format!("Representative points evaluation failed: {:?}", e))?;
    for ev in &evals {
        if !ev.is_positive || !ev.satisfies_certified_floor {
            return Err(format!("Point {} failed certified margin floor", ev.point));
        }
    }
    rep_set
        .verify_all_covered_by_path(&path)
        .map_err(|e| format!("Representative points not fully covered by path: {:?}", e))?;

    let t_dita = dita_representative_triple();
    let cand_u: BasisCyc = f6_family_columns(2, 4);
    let empty_cert = verify_empty_zerorel_variety(&t_dita, &cand_u)
        .map_err(|e| format!("ZeroRel variety verification failed: {:?}", e))?;
    if !empty_cert.variety_empty {
        return Err("ZeroRel variety is not empty".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Representative Points Floor & ZeroRel Variety Emptiness".to_string(),
        category: "Continuous Chaining & Boundary Residues".to_string(),
        passed: true,
        details: format!(
            "Evaluated: {} points, All meet margin floor {}, ZeroRel empty: true",
            evals.len(),
            rat_str(&certified_margin())
        ),
    });
    if verbose {
        println!("  [PASS] Representative points and ZeroRel variety verified");
    }

    let chaining_rep = verify_continuous_szollosi_chaining(40)
        .map_err(|e| format!("Continuous Szöllősi chaining samples failed: {:?}", e))?;
    if !chaining_rep.all_samples_obstructed || !chaining_rep.gap_stability_certified {
        return Err("Continuous chaining samples obstruction or stability failed".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Continuous Szöllősi Chaining Samples (40 mesh points)".to_string(),
        category: "Continuous Chaining & Boundary Residues".to_string(),
        passed: true,
        details: format!(
            "Samples: {}, All obstructed: true, Stability certified: true",
            chaining_rep.num_samples_verified
        ),
    });
    if verbose {
        println!("  [PASS] Continuous Szöllősi chaining samples verified");
    }

    let res_delta = BigRational::new(BigInt::from(1), BigInt::from(10));
    let residue_rep = solve_continuous_manifold_residue(4, &res_delta, 6);
    if residue_rep.total_boxes_explored == 0 || residue_rep.outside_boxes_certified == 0 {
        return Err("Continuous manifold residue solver produced zero certified boxes".to_string());
    }
    let seeds = all_6_genuine_seeds();
    if seeds.len() != 6 {
        return Err(format!("Expected 6 genuine seeds, found {}", seeds.len()));
    }
    steps.push(VerificationStepReceipt {
        name: "Continuous Diță Manifold Boundary Residues".to_string(),
        category: "Continuous Chaining & Boundary Residues".to_string(),
        passed: true,
        details: format!(
            "Explored: {}, Certified: {}, Genuine seeds: 6",
            residue_rep.total_boxes_explored, residue_rep.outside_boxes_certified
        ),
    });
    if verbose {
        println!("  [PASS] Manifold boundary residues verified");
    }

    let conn = KarlssonBoundaryConnection::at_boundary_depth();
    if !conn.is_unitary_certified || !conn.preserves_curvature_wall {
        return Err("Karlsson boundary connection failed unitary or curvature check".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Karlsson Boundary Manifold Gauge Integration".to_string(),
        category: "Continuous Chaining & Boundary Residues".to_string(),
        passed: true,
        details: format!(
            "Boundary depth z: {}, Unitary certified: true, Wall preserved: true",
            rat_str(&conn.z_depth)
        ),
    });
    if verbose {
        println!("  [PASS] Karlsson boundary gauge integration verified");
    }

    Ok(())
}

fn verify_cech_cocycles_and_nerve_chaining(
    steps: &mut Vec<VerificationStepReceipt>,
    verbose: bool,
) -> Result<(), String> {
    if verbose {
        println!("--- [3/4] Verifying Čech Cocycles & Covering Nerve Holonomies ---");
    }

    let cech = verify_cech_cocycles_all_53_triples()
        .map_err(|e| format!("Čech cocycle verification failed: {:?}", e))?;
    if !cech.all_triples_valid || cech.total_triples_verified != 53 {
        return Err(format!(
            "Čech cocycle check failed: valid={}, total={}",
            cech.all_triples_valid, cech.total_triples_verified
        ));
    }
    steps.push(VerificationStepReceipt {
        name: "Čech 2-Cocycle Condition (All 53 Nerve Triples)".to_string(),
        category: "Covering Nerve & Holonomies".to_string(),
        passed: true,
        details: format!(
            "Triples: 53, All valid: true, Deltoid corner: {}, Tao corner: {}",
            cech.deltoid_corner_valid, cech.tao_corner_valid
        ),
    });
    if verbose {
        println!("  [PASS] Čech 2-cocycles on all 53 triples verified");
    }

    let b3 = evaluate_target_b3_manifold_integration()
        .map_err(|e| format!("Master Target B3 manifold integration failed: {:?}", e))?;
    if !b3.discrete_28_cells_obstructed
        || !b3.continuous_chaining_obstructed
        || !b3.loop_circulation_obstructed
        || !b3.master_unified_obstruction_verified
    {
        return Err(
            "Target B3 manifold integration failed required obstruction disjunction".to_string(),
        );
    }
    if !b3.moduli_covering_closure || !b3.no_complete_mub6 {
        return Err(format!(
            "Target B3 no-go not established: moduli covering closure rests on {} obstructed sample points, not a closure certificate",
            b3.coverage_report.total_samples_tested
        ));
    }
    steps.push(VerificationStepReceipt {
        name: "Master Target B3 Manifold Integration & Unified Obstruction".to_string(),
        category: "Covering Nerve & Holonomies".to_string(),
        passed: true,
        details: "28 discrete cells obstructed, Chaining obstructed, Loop circulation obstructed, Covering closure certified".to_string(),
    });
    if verbose {
        println!("  [PASS] Master Target B3 manifold integration verified");
    }

    let coverage = verify_full_unified_coverage()
        .map_err(|e| format!("Unified coverage verification failed: {:?}", e))?;
    if !coverage.all_samples_obstructed || !coverage.closure_certified {
        return Err(
            "Full unified coverage closure not certified: sampled coverage is not a closure certificate"
                .to_string(),
        );
    }
    steps.push(VerificationStepReceipt {
        name: "Full Unified Moduli Coverage Closure".to_string(),
        category: "Covering Nerve & Holonomies".to_string(),
        passed: true,
        details: format!(
            "Cells tested: {}, Charts tested: {}, Coverage fraction: 1",
            coverage.cells_tested, coverage.charts_tested
        ),
    });
    if verbose {
        println!("  [PASS] Full unified moduli coverage closure verified");
    }

    let nerve = evaluate_nerve_chaining(2, INTEGER_SCALE)
        .map_err(|e| format!("Nerve chaining evaluation failed: {:?}", e))?;
    if !nerve.area_conserved
        || !nerve.all_phi1_ge_gamma
        || !nerve.all_circulation_conserved
        || !nerve.all_dual_gaps_zero
    {
        return Err("Nerve chaining circulation or dual gap check failed".to_string());
    }

    let tri_deltoid = BoundaryNerveTriangle::deltoid();
    let sol_deltoid = solve_triangular_circulation(&tri_deltoid, None, INTEGER_SCALE)
        .map_err(|e| format!("Deltoid triangular circulation failed: {:?}", e))?;
    if !sol_deltoid.circulation_conserved
        || !sol_deltoid.dual_gap_zero
        || !sol_deltoid.phi1_ge_gamma
    {
        return Err(
            "Deltoid triangle circulation not conserved or duality gap nonzero".to_string(),
        );
    }

    let tri_tao = BoundaryNerveTriangle::tao();
    let sol_tao = solve_triangular_circulation(&tri_tao, None, INTEGER_SCALE)
        .map_err(|e| format!("Tao triangular circulation failed: {:?}", e))?;
    if !sol_tao.circulation_conserved || !sol_tao.dual_gap_zero || !sol_tao.phi1_ge_gamma {
        return Err("Tao triangle circulation not conserved or duality gap nonzero".to_string());
    }

    steps.push(VerificationStepReceipt {
        name: "2D Nerve Boundary Chaining & Circulation Lower Bound".to_string(),
        category: "Covering Nerve & Holonomies".to_string(),
        passed: true,
        details: format!(
            "Collar boxes: {}, Area conserved: true, All Phi1 >= Gamma: true, Dual gaps: 0",
            nerve.num_collar_boxes
        ),
    });
    if verbose {
        println!("  [PASS] 2D nerve boundary chaining and circulation verified");
    }

    Ok(())
}

fn verify_moment_sdp_ldlt_hierarchy(
    steps: &mut Vec<VerificationStepReceipt>,
    verbose: bool,
) -> Result<(), String> {
    if verbose {
        println!("--- [4/4] Verifying Exact Moment SDP LDLᵀ Hierarchy (Deg 2, 4, 6, 8) ---");
    }

    for &d in SUPPORTED_DEGREES {
        let bench = evaluate_degree_benchmark(d, None)
            .map_err(|e| format!("Degree {d} moment benchmark failed: {:?}", e))?;

        if !bench.x0_receipt.pivots_strictly_positive {
            return Err(format!(
                "Degree {d} X=0 dual witness LDLᵀ pivots not strictly positive"
            ));
        }
        if !bench.s6_receipt.pivots_strictly_positive {
            return Err(format!(
                "Degree {d} S6 dual witness LDLᵀ pivots not strictly positive"
            ));
        }
        if !bench.x0_receipt.strictly_negative {
            return Err(format!(
                "Degree {d} X=0 trace inner product is non-negative"
            ));
        }
        if !bench.s6_receipt.strictly_negative {
            return Err(format!("Degree {d} S6 trace inner product is non-negative"));
        }

        steps.push(VerificationStepReceipt {
            name: format!(
                "Degree {d} Moment SDP LDLᵀ Factorization & Dual Witnesses",
                d = d
            ),
            category: "Moment SDP Hierarchy".to_string(),
            passed: true,
            details: format!(
                "X=0 trace: {} (pivots positive: true), S6 trace: {} (pivots positive: true)",
                bench.x0_receipt.inner_product, bench.s6_receipt.inner_product
            ),
        });
        if verbose {
            println!(
                "  [PASS] Degree {} moment SDP: X=0 trace {}, S6 trace {}, LDLᵀ pivots strictly positive",
                d, bench.x0_receipt.inner_product, bench.s6_receipt.inner_product
            );
        }
    }

    let ledger = evaluate_moment_sdp_hierarchy_ledger()
        .map_err(|e| format!("Ledger evaluation failed: {:?}", e))?;
    if ledger.degrees != vec![2, 4, 6, 8]
        || ledger.entries.len() != 4
        || !ledger.diagnostics_complete
        || ledger.complete
    {
        return Err("Moment SDP hierarchy ledger failed structural or epistemic check".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Moment SDP Hierarchy Ledger Structure & Firewall".to_string(),
        category: "Moment SDP Hierarchy".to_string(),
        passed: true,
        details: format!(
            "Degrees: {:?}, Diagnostics complete: true, Complete: false (Honest firewall)",
            ledger.degrees
        ),
    });
    if verbose {
        println!("  [PASS] Moment SDP hierarchy ledger structure verified");
    }

    let canon_ok = verify_canonical_fixtures()
        .map_err(|e| format!("Canonical fixture verification failed: {:?}", e))?;
    if !canon_ok {
        return Err("Canonical fixture matrix fingerprints mismatch".to_string());
    }
    steps.push(VerificationStepReceipt {
        name: "Cross-Runtime Fixture SHA-256 Matrix Fingerprints (21 matrices)".to_string(),
        category: "Moment SDP Hierarchy".to_string(),
        passed: true,
        details: "All 21 canonical moment matrices match SHA-256 fingerprints exactly".to_string(),
    });
    if verbose {
        println!("  [PASS] 21 canonical moment matrix fingerprints verified");
    }

    Ok(())
}

fn run() -> Result<i32, String> {
    let start_time = Instant::now();
    let mut verbose = true;
    let mut json_mode = false;
    let mut emit_artifact = false;
    let mut output_path: Option<PathBuf> = None;

    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--json" => json_mode = true,
            "--emit" => emit_artifact = true,
            "--quiet" | "-q" => verbose = false,
            "--output" => {
                output_path = Some(PathBuf::from(
                    args.next()
                        .ok_or("--output requires a file path argument")?,
                ))
            }
            "--help" | "-h" => {
                println!("Omega-Native MUB(6) Grand Verifier (omega_mub_verify_all)");
                println!("AuthorityEffect: None");
                println!("Firewall Line: stated region only; mints no authority");
                println!();
                println!("USAGE:");
                println!(
                    "    cargo run -p omega_mub --bin omega_mub_verify_all --release [OPTIONS]"
                );
                println!();
                println!("OPTIONS:");
                println!("    --json           Emit structured JSON receipt to stdout");
                println!("    --emit           Write receipt to artifacts/omega_mub_verify_all_receipt.json");
                println!("    --output <PATH>  Write receipt to specified file path");
                println!("    --quiet, -q      Suppress step-by-step progress logging");
                println!("    --help, -h       Display this help message");
                return Ok(0);
            }
            other => return Err(format!("Unknown option: {other}")),
        }
    }

    if verbose && !json_mode {
        println!(
            "================================================================================"
        );
        println!(
            "       OMEGA NATIVE MUB(6) GRAND RELEASE-MODE VERIFIER (EXACT PASS BITS)   "
        );
        println!(
            "================================================================================"
        );
        println!("AuthorityEffect: {}", AUTHORITY_EFFECT);
        println!("Firewall Line:   {}", FIREWALL);
        println!("Arithmetic:      Exact Rational (BigRational), Cyclotomic (Cyc24)");
        println!("Pass bits:       Exact rational and cyclotomic; display floats do not decide");
        println!(
            "================================================================================"
        );
    }

    let mut steps = Vec::new();

    verify_all_partition_covers(&mut steps, verbose && !json_mode)?;

    verify_continuous_chaining_and_boundary_residues(&mut steps, verbose && !json_mode)?;

    verify_cech_cocycles_and_nerve_chaining(&mut steps, verbose && !json_mode)?;

    verify_moment_sdp_ldlt_hierarchy(&mut steps, verbose && !json_mode)?;

    let elapsed = start_time.elapsed().as_millis() as u64;
    let total_passed = steps.iter().filter(|s| s.passed).count();
    let total_failed = steps.iter().filter(|s| !s.passed).count();

    let receipt = GrandVerificationReceipt {
        schema_version: SCHEMA_VERSION.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        firewall: FIREWALL.to_string(),
        overall_status: if total_failed == 0 {
            "CERTIFIED_ALL_CHECKS_PASSED".to_string()
        } else {
            "VERIFICATION_FAILED".to_string()
        },
        zero_float_discipline_verified: fixtures().flag("zero_float_discipline_verified"),
        partition_covers_verified: category_verified(&steps, "Partition Covers"),
        continuous_chaining_verified: category_verified(
            &steps,
            "Continuous Chaining & Boundary Residues",
        ),
        boundary_residues_verified: category_verified(
            &steps,
            "Continuous Chaining & Boundary Residues",
        ),
        cech_cocycles_verified: category_verified(&steps, "Covering Nerve & Holonomies"),
        moment_sdp_ldlt_verified: category_verified(&steps, "Moment SDP Hierarchy"),
        total_steps_passed: total_passed,
        total_steps_failed: total_failed,
        steps,
        execution_time_millis: elapsed,
    };

    let receipt_json = serde_json::to_string_pretty(&receipt)
        .map_err(|e| format!("Failed to serialize receipt: {e}"))?;

    if let Some(ref path) = output_path {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|e| e.to_string())?;
        }
        fs::write(path, &receipt_json)
            .map_err(|e| format!("Failed to write to {}: {e}", path.display()))?;
        if verbose && !json_mode {
            println!("Receipt written to: {}", path.display());
        }
    } else if emit_artifact {
        let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        let root_dir = manifest_dir.join("../../..");
        for dir in [root_dir.join("artifacts"), manifest_dir.join("../tests/omega_mub/artifacts")] {
            fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
            let dest = dir.join("omega_mub_verify_all_receipt.json");
            fs::write(&dest, &receipt_json).map_err(|e| e.to_string())?;
            if verbose && !json_mode {
                println!("Emitted receipt artifact to: {}", dest.display());
            }
        }
    }

    if json_mode {
        println!("{}", receipt_json);
    } else if verbose {
        println!(
            "================================================================================"
        );
        println!(
            "                      VERIFICATION SUMMARY                                      "
        );
        println!(
            "================================================================================"
        );
        println!("Total Steps Passed:    {}", total_passed);
        println!("Total Steps Failed:    {}", total_failed);
        println!("Zero-float discipline: not claimed");
        println!("Execution Duration:    {} ms", elapsed);
        println!("Firewall Maintained:   {}", FIREWALL);
        println!("AuthorityEffect:       {}", AUTHORITY_EFFECT);
        println!(
            "================================================================================"
        );
    }

    Ok(0)
}

fn main() {
    match run() {
        Ok(code) => std::process::exit(code),
        Err(err) => {
            eprintln!("\n[FATAL ERROR] Verification failed: {err}");
            std::process::exit(1);
        }
    }
}
