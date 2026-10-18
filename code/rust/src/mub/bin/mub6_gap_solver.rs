//! `mub6_gap_solver` — frontier planning report with scoped registry and catalog checks.
//!
//! AuthorityEffect: None
//!
//! This binary:
//! 1. Reads the current ENC-1147 CHM registry summary and mechanical checks.
//! 2. Classifies the declared catalog candidates with the decision-tree classifier.
//! 3. Ranks a fixed list of frontier targets by declared integer heuristic points.
//! 4. Lists proposed certificate types; it does not verify those certificates.
//! 5. Emits a structured JSON frontier report to stdout and artifacts/.
//!
//! Usage:
//!   cargo run --bin mub6_gap_solver
//!   cargo run --bin mub6_gap_solver -- --target R7
//!   cargo run --bin mub6_gap_solver -- --verify-catalog

use omega_mub::omega_native::exact::mub6_chm_registry::current_chm_registry;
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_g1_variety::{
    verify_cross_orbit_triad_circulation, CrossOrbitTriad,
};
use omega_mub::omega_native::exact::mub6_orbit_exhaustiveness::{
    canonical_catalog_candidates, certify_catalog_exhaustiveness,
};

use serde::Serialize;
use sha2::{Digest, Sha256};

omega_mub::fixture_set!(fixtures, "mub6_gap_solver");

/// A declared frontier target with integer heuristic points and a proposed certificate type.
#[derive(Debug, Clone, Serialize)]
pub struct FrontierTarget {
    pub id: String,
    pub residual_class: String,
    pub heuristic_priority_points: u8,
    pub priority_rank: usize,
    pub description: String,
    pub certificate_type: CertificateType,
    pub dependencies: Vec<String>,
    pub blocks: Vec<String>,
    pub status: TargetStatus,
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq, PartialOrd, Ord)]
pub enum CertificateType {
    /// Exact Nullstellensatz polynomial identity refuting a branch.
    NullstellensatzRefutation {
        ideal_dimension: usize,
        witness_degree: usize,
    },
    /// Exact Positivstellensatz SOS certificate refuting real solutions in a region.
    PositivstellensatzSos { bound_type: String },
    /// Continuous branch-and-bound cover closing a parameter region.
    BranchAndBoundCover {
        parameter_dimension: usize,
        estimated_cells: usize,
    },
    /// Cross-ratio spectrum invariant distinguishing an orbit.
    CrossRatioSpectrumCertificate { orbit: String },
    /// Triad compatibility obstruction certificate.
    TriadObstruction { orbits: (String, String) },
    /// Global moduli algebraic elimination (full ideal decomposition).
    AlgebraicElimination { variables: usize, equations: usize },
    /// Deferred neighborhood widening.
    NeighborhoodWidening { delta: String },
}

#[derive(Debug, Clone, Copy, Serialize, PartialEq, Eq, PartialOrd, Ord)]
pub enum TargetStatus {
    Open,
    Partial,
    Blocked,
}

/// Snapshot of frontier targets and declared-catalog checks.
#[derive(Debug, Clone, Serialize)]
pub struct FrontierReport {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub timestamp: String,
    pub registry_summary: RegistrySummary,
    pub declared_catalog_classification: CatalogSummary,
    pub cross_orbit_circulation: Vec<CirculationSummary>,
    pub frontier_targets: Vec<FrontierTarget>,
    pub total_open: usize,
    pub total_partial: usize,
    pub total_blocked: usize,
    pub highest_priority_target: Option<String>,
    pub recommended_next_action: String,
    pub sha256_digest: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct RegistrySummary {
    pub charted_count: usize,
    pub open_residual_count: usize,
    pub mechanical_checks_ok: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct CatalogSummary {
    pub total_candidates: usize,
    pub fourier_count: usize,
    pub tao_count: usize,
    pub haagerup_count: usize,
    pub szollosi_count: usize,
    pub unassigned: usize,
    pub all_declared_candidates_classified: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct CirculationSummary {
    pub triad: String,
    pub phi1: String,
    pub gamma: String,
    pub is_obstructed: bool,
}

fn declared_frontier_targets() -> Vec<FrontierTarget> {
    let mut targets = Vec::new();

    // R7 is the irreducible global residual — closing it would discharge G1 entirely.
    targets.push(FrontierTarget {
        id: "G1-MASTER".to_string(),
        residual_class: "R7".to_string(),
        heuristic_priority_points: 100,
        priority_rank: 0,
        description: "Full moduli variety classification: prove every 6×6 CHM \
            belongs to {F₆, B₆(θ), K₆⁽³⁾, S₆, H₆}. This is the irreducible \
            core of Premise G1. Approach: algebraic elimination of the \
            50-variable / 55-polynomial ideal I(H₆) into its irreducible \
            components, or formalization of Beauchamp-Nicoara + Szöllősi + \
            Karlsson classification results."
            .to_string(),
        certificate_type: CertificateType::AlgebraicElimination {
            variables: 50,
            equations: 55,
        },
        dependencies: vec!["R6-literature-classes".to_string()],
        blocks: vec![
            "R1".to_string(),
            "R3".to_string(),
            "R4".to_string(),
            "R5".to_string(),
            "G2-bridge".to_string(),
            "G3-enclosures".to_string(),
            "G4-cochains".to_string(),
        ],
        status: TargetStatus::Open,
    });

    // R6: sporadic literature classes — prerequisite for R7.
    targets.push(FrontierTarget {
        id: "G1-R6-LITERATURE".to_string(),
        residual_class: "R6".to_string(),
        heuristic_priority_points: 90,
        priority_rank: 1,
        description: "Formalize that all known sporadic / non-affine 6×6 CHM classes \
            from the literature (Beauchamp-Nicoara, Szöllősi, Karlsson, Cárdenes Wuttig–Tindall) \
            are either equivalent to the 5 cataloged families or provably empty. \
            Approach: for each literature class, construct an explicit Cyc24 representative \
            and run it through classify_orbit to verify it lands in the catalog."
            .to_string(),
        certificate_type: CertificateType::CrossRatioSpectrumCertificate {
            orbit: "all-literature-classes".to_string(),
        },
        dependencies: vec![],
        blocks: vec!["R7".to_string()],
        status: TargetStatus::Open,
    });

    // R1: F6 external B3 continuous locus beyond the 6 locked lattice seeds.
    targets.push(FrontierTarget {
        id: "G1-R1-F6-CONTINUOUS".to_string(),
        residual_class: "R1".to_string(),
        heuristic_priority_points: 75,
        priority_rank: 2,
        description: "Extend F₆ external B₃ coverage from 6 locked lattice seeds to \
            the full continuous (x,y) parameter space. Approach: parametric branch-and-bound \
            cover over the 2-torus T², using the existing f6_chart infrastructure to verify \
            that at every (x,y) the external B₃ candidates either are MU or produce \
            a certified obstruction."
            .to_string(),
        certificate_type: CertificateType::BranchAndBoundCover {
            parameter_dimension: 2,
            estimated_cells: 10000,
        },
        dependencies: vec![],
        blocks: vec![],
        status: TargetStatus::Partial,
    });

    // R3: dephased CHM moduli outside delta-patches — covered by R7 but can be attacked independently.
    targets.push(FrontierTarget {
        id: "G1-R3-MODULI-OUTSIDE-PATCHES".to_string(),
        residual_class: "R3".to_string(),
        heuristic_priority_points: 70,
        priority_rank: 3,
        description: "Close the gap between recorded δ-patches and full moduli. \
            Currently the atlas covers neighborhoods of known points but not \
            the intervening parameter space. Approach: continuous Szöllősi arc \
            chaining from θ=0 to θ=π with collar-style 2D periodic cover."
            .to_string(),
        certificate_type: CertificateType::BranchAndBoundCover {
            parameter_dimension: 1,
            estimated_cells: 5000,
        },
        dependencies: vec![],
        blocks: vec![],
        status: TargetStatus::Partial,
    });

    // R2: Y2Q2 delta neighborhood deferred.
    targets.push(FrontierTarget {
        id: "G1-R2-Y2Q2-NEIGHBORHOOD".to_string(),
        residual_class: "R2".to_string(),
        heuristic_priority_points: 50,
        priority_rank: 4,
        description: "Complete the δ=1/1000 full 5-torus neighborhood cover on \
            Y₂⊗Q₂ three seeds. The Y₂⊗Q₁ orbit point covers are complete; \
            the Y₂⊗Q₂ dual orbit δ-widening was deferred due to wall-time. \
            Approach: run mub6_dita_seed_cover with δ=1/1000 on the 3 Y₂⊗Q₂ seeds."
            .to_string(),
        certificate_type: CertificateType::NeighborhoodWidening {
            delta: "1/1000".to_string(),
        },
        dependencies: vec![],
        blocks: vec![],
        status: TargetStatus::Open,
    });

    // R4: basis gluing and Ψ bridge.
    targets.push(FrontierTarget {
        id: "G1-R4-BASIS-GLUING".to_string(),
        residual_class: "R4".to_string(),
        heuristic_priority_points: 65,
        priority_rank: 5,
        description: "Discharge the basis_gluing_gate MissingProofObligation: \
            construct the Ψ_basis bridge from vector wall covers to the \
            basis-extension packet. Approach: for each chart in the moduli atlas, \
            verify that the transition from vector-level MU obstruction to \
            basis-level extension impossibility is algebraically valid."
            .to_string(),
        certificate_type: CertificateType::TriadObstruction {
            orbits: ("F6-triples".to_string(), "all-orbits".to_string()),
        },
        dependencies: vec!["R7".to_string()],
        blocks: vec![],
        status: TargetStatus::Blocked,
    });

    // R5: C2 full atlas glue.
    targets.push(FrontierTarget {
        id: "G1-R5-ATLAS-COHERENCE".to_string(),
        residual_class: "R5".to_string(),
        heuristic_priority_points: 60,
        priority_rank: 6,
        description: "Prove atlas coherence: multi-patch gluing with transport \
            and ZeroRel preservation. Currently only pairwise disjointness is proven. \
            Approach: verify Čech cocycle condition on all triple intersections \
            and confirm holonomy is identity on all non-contractible loops."
            .to_string(),
        certificate_type: CertificateType::BranchAndBoundCover {
            parameter_dimension: 2,
            estimated_cells: 1000,
        },
        dependencies: vec!["R3".to_string()],
        blocks: vec![],
        status: TargetStatus::Partial,
    });

    // R9: Path B invariant survivor (cohomological deformation route).
    targets.push(FrontierTarget {
        id: "G1-R9-PATH-B-INVARIANT".to_string(),
        residual_class: "R9".to_string(),
        heuristic_priority_points: 40,
        priority_rank: 7,
        description: "Path B: rigidity-route obstruction via exact deformation \
            invariance probes at basepoints including Diță second basepoints. \
            Currently Gate A fails on T₀. If Gate A∧B passes anywhere, it would \
            indicate a potential 4th MUB root (Branch B of the Decisive Bifurcation). \
            Approach: extend d6_exact_deformation_invariance_probe to additional \
            basepoints on the Szöllősi arc."
            .to_string(),
        certificate_type: CertificateType::CrossRatioSpectrumCertificate {
            orbit: "path-b-deformation".to_string(),
        },
        dependencies: vec![],
        blocks: vec![],
        status: TargetStatus::Open,
    });

    // R8: Lean kernel reflection scale.
    targets.push(FrontierTarget {
        id: "G1-R8-LEAN-SCALE".to_string(),
        residual_class: "R8".to_string(),
        heuristic_priority_points: 30,
        priority_rank: 8,
        description: "Scale the Lean 4 kernel reflection from pilot JSON to \
            full ~1M cover leaf verification. This is a mechanization gap, \
            not a mathematical gap. Approach: stratified manifest with batch \
            reflection or redesigned certificate shape."
            .to_string(),
        certificate_type: CertificateType::AlgebraicElimination {
            variables: 0,
            equations: 0,
        },
        dependencies: vec!["R7".to_string()],
        blocks: vec![],
        status: TargetStatus::Blocked,
    });

    // Sort by declared heuristic points descending.
    targets.sort_by(|a, b| {
        b.heuristic_priority_points
            .cmp(&a.heuristic_priority_points)
    });
    for (i, t) in targets.iter_mut().enumerate() {
        t.priority_rank = i;
    }

    targets
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let verify_catalog = args.iter().any(|a| a == "--verify-catalog");
    let target_filter: Option<&str> = args
        .iter()
        .position(|a| a == "--target")
        .and_then(|i| args.get(i + 1))
        .map(|s| s.as_str());

    eprintln!("═══════════════════════════════════════════════════════════════════");
    eprintln!("  MUB(6) Gap Solver — Frontier Target Finder");
    eprintln!("  Firewall: {FIREWALL}");
    eprintln!("  AuthorityEffect: {AUTHORITY_EFFECT}");
    eprintln!("═══════════════════════════════════════════════════════════════════");
    eprintln!();

    // 1. Read CHM registry.
    eprintln!("[1/4] Reading ENC-1147 CHM registry...");
    let registry = current_chm_registry();
    eprintln!("  Charted loci: {}", registry.charted_count);
    eprintln!("  Open residuals: {}", registry.open_residual_count);
    eprintln!(
        "  Mechanical checks: {}",
        if registry.mechanical_checks_ok {
            "PASS"
        } else {
            "FAIL"
        }
    );
    if !registry.mechanical_checks_ok {
        for detail in &registry.mechanical_check_detail {
            eprintln!("    ✗ {detail}");
        }
    }
    eprintln!();

    let reg_summary = RegistrySummary {
        charted_count: registry.charted_count,
        open_residual_count: registry.open_residual_count,
        mechanical_checks_ok: registry.mechanical_checks_ok,
    };

    // 2. Classify the declared catalog candidates.
    eprintln!("[2/4] Classifying declared catalog candidates...");
    let catalog = canonical_catalog_candidates();
    let exhaustiveness = certify_catalog_exhaustiveness(&catalog);
    eprintln!(
        "  Candidates tested: {}",
        exhaustiveness.total_candidates_tested
    );
    eprintln!(
        "  Fourier: {} | Tao: {} | Haagerup: {} | Szöllősi: {}",
        exhaustiveness.fourier_count,
        exhaustiveness.tao_count,
        exhaustiveness.haagerup_count,
        exhaustiveness.szollosi_count
    );
    eprintln!("  Unassigned: {}", exhaustiveness.unassigned_residual_count);
    eprintln!(
        "  All declared catalog candidates classified: {}",
        exhaustiveness.is_exhaustive
    );

    if verify_catalog {
        for r in &exhaustiveness.candidate_results {
            let mark = if r.matches_expected { "✓" } else { "✗" };
            eprintln!(
                "    {mark} {} → {:?} (expected {:?})",
                r.candidate_name, r.assigned_class, r.expected_class
            );
        }
    }
    eprintln!();

    let cat_summary = CatalogSummary {
        total_candidates: exhaustiveness.total_candidates_tested,
        fourier_count: exhaustiveness.fourier_count,
        tao_count: exhaustiveness.tao_count,
        haagerup_count: exhaustiveness.haagerup_count,
        szollosi_count: exhaustiveness.szollosi_count,
        unassigned: exhaustiveness.unassigned_residual_count,
        all_declared_candidates_classified: exhaustiveness.is_exhaustive,
    };

    // 3. Cross-orbit circulation checks.
    eprintln!("[3/4] Verifying cross-orbit triad circulations...");
    let triads = [
        CrossOrbitTriad::TaoSzollosi,
        CrossOrbitTriad::TaoTao,
        CrossOrbitTriad::SzollosiSzollosi,
        CrossOrbitTriad::HaagerupTao,
    ];
    let mut circ_summaries = Vec::new();
    for t in &triads {
        let r = verify_cross_orbit_triad_circulation(*t);
        eprintln!(
            "  {:?}: Φ₁={} ≥ Γ={} → obstructed={}",
            t, r.circulation_phi1, r.threshold_gamma, r.is_obstructed
        );
        circ_summaries.push(CirculationSummary {
            triad: format!("{t:?}"),
            phi1: r.circulation_phi1.to_string(),
            gamma: r.threshold_gamma.to_string(),
            is_obstructed: r.is_obstructed,
        });
    }
    eprintln!();

    // 4. Compute frontier targets.
    eprintln!("[4/4] Ranking declared frontier targets...");
    let mut targets = declared_frontier_targets();

    if let Some(filter) = target_filter {
        targets.retain(|t| t.residual_class == filter || t.id.contains(filter));
    }

    let total_open = targets
        .iter()
        .filter(|t| t.status == TargetStatus::Open)
        .count();
    let total_partial = targets
        .iter()
        .filter(|t| t.status == TargetStatus::Partial)
        .count();
    let total_blocked = targets
        .iter()
        .filter(|t| t.status == TargetStatus::Blocked)
        .count();
    let highest = targets.first().map(|t| t.id.clone());

    eprintln!();
    eprintln!("╔══════════════════════════════════════════════════════════════════╗");
    eprintln!("║                    FRONTIER TARGET RANKING                       ║");
    eprintln!("╠══════════════════════════════════════════════════════════════════╣");
    for t in &targets {
        let status_mark = match t.status {
            TargetStatus::Open => "🔴",
            TargetStatus::Partial => "🟡",
            TargetStatus::Blocked => "⬜",
        };
        eprintln!(
            "║ {status_mark} #{} [{} points] {} ({})",
            t.priority_rank, t.heuristic_priority_points, t.id, t.residual_class
        );
        if !t.blocks.is_empty() {
            eprintln!("║        Blocks: {}", t.blocks.join(", "));
        }
    }
    eprintln!("╠══════════════════════════════════════════════════════════════════╣");
    eprintln!("║ Open: {total_open} | Partial: {total_partial} | Blocked: {total_blocked}");
    eprintln!(
        "║ Highest priority: {}",
        highest.as_deref().unwrap_or("none")
    );
    eprintln!("╚══════════════════════════════════════════════════════════════════╝");

    let recommended = if let Some(ref h) = highest {
        format!(
            "Target {h}: The irreducible core of G1. Two viable approaches: \
            (A) Formalize the Beauchamp-Nicoara / Szöllősi / Karlsson / Cárdenes Wuttig-Tindall \
            classification theorem by constructing explicit Cyc24 representatives for each \
            literature class and proving they exhaust the 50-variable variety. \
            (B) Perform direct algebraic elimination of the 55-polynomial ideal in 50 variables \
            via Gröbner basis computation over Q(zeta_24), decomposing the variety into \
            irreducible components matching the 5 known families."
        )
    } else {
        "No open targets.".to_string()
    };

    // Build report.
    let report = FrontierReport {
        schema_version: "omega.mub6.frontier-report.v2".to_string(),
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        timestamp: chrono_stub(),
        registry_summary: reg_summary,
        declared_catalog_classification: cat_summary,
        cross_orbit_circulation: circ_summaries,
        frontier_targets: targets,
        total_open,
        total_partial,
        total_blocked,
        highest_priority_target: highest,
        recommended_next_action: recommended.clone(),
        sha256_digest: String::new(),
    };

    // Compute content hash.
    let json = serde_json::to_string_pretty(&report).expect("serialize");
    let mut hasher = Sha256::new();
    hasher.update(json.as_bytes());
    let digest = format!("{:x}", hasher.finalize());

    // Re-serialize with hash (two-pass).
    let mut report = report;
    report.sha256_digest = digest.clone();
    let json_final = serde_json::to_string_pretty(&report).expect("serialize");

    // Write to stdout.
    println!("{json_final}");

    // Write to artifacts/ if CARGO_MANIFEST_DIR is set.
    if let Ok(manifest) = std::env::var("CARGO_MANIFEST_DIR") {
        let dir = std::path::PathBuf::from(manifest).join("../tests/omega_mub/artifacts");
        let _ = std::fs::create_dir_all(&dir);
        let path = dir.join("mub6_frontier_report.json");
        if std::fs::write(&path, &json_final).is_ok() {
            eprintln!("\nReport written to: {}", path.display());
        }
    }

    eprintln!("\nRecommended next action:");
    eprintln!("{recommended}");
}

// fixture: a fixed string, not the time of the run.
fn chrono_stub() -> String {
    fixtures().text("report_timestamp")
}
