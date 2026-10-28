
use serde::Serialize;

use crate::native::campaign::mub6_dita_seed_cover::dita_seed_triple_is_pairwise_mu;
use crate::native::exact::mub6_f6_chart::f6_point_is_exact_chm;
use crate::native::campaign::mub6_f6_external_b3::{
    basis_is_exact_chm, chirp_fourier6_columns, external_b3_product_corpus,
    external_b3_swapped_product_corpus, genuine_dita_y2q1_triple_seeds,
    genuine_dita_y2q2_triple_seeds, product_y2_qa_columns,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ChartStatus {
    ExactChmDeclared,
    ExactMuTripleDeclared,
    PointFullTorusCoverComplete,
    NeighborhoodFullTorusCoverComplete,
    FiniteCorpusDiagnostic,
    ClaimNotReplayed,
    OpenResidual,
}

#[derive(Debug, Clone, Serialize)]
pub struct ChmLocusRecord {
    pub id: &'static str,
    pub kind: &'static str,
    pub recorded_status: ChartStatus,
    pub replayed_status: ChartStatus,
    pub status: ChartStatus,
    pub dimension: &'static str,
    pub evidence: &'static str,
    pub notes: &'static str,
}

#[derive(Debug, Clone, Serialize)]
pub struct ChmRegistryReport {
    pub schema_version: &'static str,
    pub enc_residual: &'static str,
    pub charted: Vec<ChmLocusRecord>,
    pub open_residual: Vec<ChmLocusRecord>,
    pub charted_count: usize,
    pub open_residual_count: usize,
    pub mechanical_checks_ok: bool,
    pub mechanical_check_detail: Vec<String>,
    pub terminal: &'static str,
    pub firewall: &'static str,
}

fn check_f6_affine_chm_sample(checks: &mut Vec<String>) -> bool {
    let mut f6_ok = true;
    for dx in [0i64, 4, 8, 12, 16, 20] {
        for dy in [0i64, 4, 8, 12, 16, 20] {
            if !f6_point_is_exact_chm(dx, dy) {
                f6_ok = false;
                checks.push(format!("F6({dx},{dy}) failed exact CHM"));
            }
        }
    }
    if f6_ok {
        checks.push("F6 affine family: 6×6 root-of-unity sample all exact CHM".into());
    }
    f6_ok
}

fn check_product_and_chirp_chm(checks: &mut Vec<String>) -> bool {
    let mut prod_ok = true;
    for c in external_b3_product_corpus()
        .into_iter()
        .chain(external_b3_swapped_product_corpus())
    {
        if !basis_is_exact_chm(&c.columns) {
            prod_ok = false;
            checks.push(format!("{} failed exact CHM", c.id));
        }
    }
    if prod_ok {
        checks.push("product + swapped-product corpus: all exact CHM".into());
    }

    let mut chirp_ok = true;
    for alpha in 0..6i64 {
        if !basis_is_exact_chm(&chirp_fourier6_columns(alpha)) {
            chirp_ok = false;
            checks.push(format!("chirp_fourier6({alpha}) failed exact CHM"));
        }
    }
    if chirp_ok {
        checks.push("chirp-Fourier order-6 samples: all exact CHM".into());
    }
    prod_ok && chirp_ok
}

fn check_dita_seeds_and_tao_s6_chm(checks: &mut Vec<String>) -> bool {
    let mut seeds_ok = true;
    for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
        if !dita_seed_triple_is_pairwise_mu(dx, dy) {
            seeds_ok = false;
            checks.push(format!("seed F6({dx},{dy})+Y2Q1 not pairwise MU"));
        }
    }
    for &(dx, dy) in &genuine_dita_y2q2_triple_seeds() {
        if !dita_seed_triple_is_pairwise_mu(dx, dy) {
            seeds_ok = false;
            checks.push(format!("seed F6({dx},{dy})+Y2Q2 not pairwise MU"));
        }
    }
    if !basis_is_exact_chm(&product_y2_qa_columns(1)) {
        seeds_ok = false;
        checks.push("Y2⊗Q1 failed exact CHM".into());
    }
    if !basis_is_exact_chm(&product_y2_qa_columns(2)) {
        seeds_ok = false;
        checks.push("Y2⊗Q2 failed exact CHM".into());
    }
    if seeds_ok {
        checks.push("six genuine Dita seeds: pairwise MU + Y2⊗Q1/Q2 CHM".into());
    }

    let s6 = crate::native::exact::szollosi_triad_solver::tao_s6_matrix();
    let s6_ok = crate::native::exact::szollosi_triad_solver::verify_chm(&s6).is_chm;
    if !s6_ok {
        checks.push("Tao S6 matrix failed exact CHM".into());
    } else {
        checks.push("Tao S6 isolated matrix: exact CHM verified over Q(zeta_24)".into());
    }
    seeds_ok && s6_ok
}

pub fn current_chm_registry() -> ChmRegistryReport {
    let mut checks = Vec::new();
    let f6_ok = check_f6_affine_chm_sample(&mut checks);
    let prod_chirp_ok = check_product_and_chirp_chm(&mut checks);
    let seeds_s6_ok = check_dita_seeds_and_tao_s6_chm(&mut checks);
    let ok = f6_ok && prod_chirp_ok && seeds_s6_ok;

    let charted = vec![
        ChmLocusRecord {
            id: "T0_product_triple",
            kind: "mu_triple",
            recorded_status: ChartStatus::NeighborhoodFullTorusCoverComplete,
            replayed_status: ChartStatus::ClaimNotReplayed,
            status: ChartStatus::ClaimNotReplayed,
            dimension: "point + δ=1/1000 neighborhood of product triple T0",
            evidence:
                "mub6_moduli_atlas T0 neighborhood artifact; historical fixed-tuple cover PR #975/#978",
            notes: "canonical product triple; not a full CHM classification",
        },
        ChmLocusRecord {
            id: "F6_affine_dita_family",
            kind: "chm_pair_family",
            recorded_status: ChartStatus::ExactChmDeclared,
            replayed_status: ChartStatus::ExactChmDeclared,
            status: ChartStatus::ExactChmDeclared,
            dimension: "2-parameter (x,y) / root-of-unity (dx,dy) lattice",
            evidence: "mub6_f6_chart::f6_point_is_exact_chm",
            notes: "MU pair {I,F6}; internal F6 pairs never MU (PR #981); not MU-triple cover",
        },
        ChmLocusRecord {
            id: "dita_seed_F6_0_8_Y2Q1",
            kind: "mu_triple",
            recorded_status: ChartStatus::NeighborhoodFullTorusCoverComplete,
            replayed_status: ChartStatus::ExactMuTripleDeclared,
            status: ChartStatus::ExactMuTripleDeclared,
            dimension: "point + δ=1/1000 full gauge-fixed 5-torus",
            evidence:
                "artifacts/dita_seed_F6_0_8_*_merged_complete.json (point + neigh)",
            notes: "genuine-new seed; external B3 = Y2⊗Q1",
        },
        ChmLocusRecord {
            id: "dita_seed_F6_8_0_Y2Q1",
            kind: "mu_triple",
            recorded_status: ChartStatus::NeighborhoodFullTorusCoverComplete,
            replayed_status: ChartStatus::ExactMuTripleDeclared,
            status: ChartStatus::ExactMuTripleDeclared,
            dimension: "point + δ=1/1000 full gauge-fixed 5-torus",
            evidence:
                "artifacts/dita_seed_F6_8_0_*_merged_complete.json (point + neigh)",
            notes: "genuine-new seed; external B3 = Y2⊗Q1",
        },
        ChmLocusRecord {
            id: "dita_seed_F6_16_16_Y2Q1",
            kind: "mu_triple",
            recorded_status: ChartStatus::NeighborhoodFullTorusCoverComplete,
            replayed_status: ChartStatus::ExactMuTripleDeclared,
            status: ChartStatus::ExactMuTripleDeclared,
            dimension: "point + δ=1/1000 full gauge-fixed 5-torus",
            evidence:
                "artifacts/dita_seed_F6_16_16_*_merged_complete.json (point + neigh)",
            notes: "genuine-new seed; external B3 = Y2⊗Q1",
        },
        ChmLocusRecord {
            id: "dita_seed_F6_0_16_Y2Q2",
            kind: "mu_triple",
            recorded_status: ChartStatus::PointFullTorusCoverComplete,
            replayed_status: ChartStatus::ExactMuTripleDeclared,
            status: ChartStatus::ExactMuTripleDeclared,
            dimension: "point full gauge-fixed 5-torus (δ=0); nbhd DEFERRED",
            evidence: "artifacts/dita_seed_f6_0_16_gauge_fixed_5_torus_presplit6_merged_complete.json",
            notes: "genuine-new dual-orbit seed; external B3 = Y2⊗Q2; δ=1/1000 nbhd not farmed",
        },
        ChmLocusRecord {
            id: "dita_seed_F6_8_8_Y2Q2",
            kind: "mu_triple",
            recorded_status: ChartStatus::PointFullTorusCoverComplete,
            replayed_status: ChartStatus::ExactMuTripleDeclared,
            status: ChartStatus::ExactMuTripleDeclared,
            dimension: "point full gauge-fixed 5-torus (δ=0); nbhd DEFERRED",
            evidence: "artifacts/dita_seed_f6_8_8_gauge_fixed_5_torus_presplit6_merged_complete.json",
            notes: "genuine-new dual-orbit seed; external B3 = Y2⊗Q2; δ=1/1000 nbhd not farmed",
        },
        ChmLocusRecord {
            id: "dita_seed_F6_16_0_Y2Q2",
            kind: "mu_triple",
            recorded_status: ChartStatus::PointFullTorusCoverComplete,
            replayed_status: ChartStatus::ExactMuTripleDeclared,
            status: ChartStatus::ExactMuTripleDeclared,
            dimension: "point full gauge-fixed 5-torus (δ=0); nbhd DEFERRED",
            evidence: "artifacts/dita_seed_f6_16_0_gauge_fixed_5_torus_presplit6_merged_complete.json",
            notes: "genuine-new dual-orbit seed; external B3 = Y2⊗Q2; δ=1/1000 nbhd not farmed",
        },
        ChmLocusRecord {
            id: "dita_y2q1_lattice_orbit_locked",
            kind: "mu_triple_lattice_orbit",
            recorded_status: ChartStatus::ExactMuTripleDeclared,
            replayed_status: ChartStatus::ClaimNotReplayed,
            status: ChartStatus::ClaimNotReplayed,
            dimension: "ζ24 lattice F6(dx,dy)×Y2⊗Q1 genuine-new phases",
            evidence:
                "artifacts/f6_y2q_base_mu_lattice_exhaustion_24x24_20260724.json; genuine={(0,8),(8,0),(16,16)}",
            notes: "full 24×24 census: genuine-new set equals locked Y2Q1 seeds exactly",
        },
        ChmLocusRecord {
            id: "dita_y2q2_lattice_orbit_locked",
            kind: "mu_triple_lattice_orbit",
            recorded_status: ChartStatus::ExactMuTripleDeclared,
            replayed_status: ChartStatus::ClaimNotReplayed,
            status: ChartStatus::ClaimNotReplayed,
            dimension: "ζ24 lattice F6(dx,dy)×Y2⊗Q2 genuine-new phases",
            evidence:
                "artifacts/f6_y2q_base_mu_lattice_exhaustion_24x24_20260724.json; genuine={(0,16),(8,8),(16,0)}",
            notes: "dual orbit to Y2Q1; point covers on main; δ=1/1000 nbhd DEFERRED (hygiene)",
        },
        ChmLocusRecord {
            id: "product_qubit_qutrit_X2_Y2_Qa",
            kind: "chm_family_finite",
            recorded_status: ChartStatus::FiniteCorpusDiagnostic,
            replayed_status: ChartStatus::FiniteCorpusDiagnostic,
            status: ChartStatus::FiniteCorpusDiagnostic,
            dimension: "finite a∈{0,1,2} × {X2,Y2}",
            evidence: "mub6_f6_external_b3::external_b3_product_corpus",
            notes: "finite product CHMs; not continuous moduli cover",
        },
        ChmLocusRecord {
            id: "product_swapped_qutrit_qubit",
            kind: "chm_family_finite",
            recorded_status: ChartStatus::FiniteCorpusDiagnostic,
            replayed_status: ChartStatus::FiniteCorpusDiagnostic,
            status: ChartStatus::FiniteCorpusDiagnostic,
            dimension: "finite Q_a/F3 ⊗ X2/Y2 samples",
            evidence: "mub6_f6_external_b3::external_b3_swapped_product_corpus",
            notes: "finite diagnostic; not continuous chart",
        },
        ChmLocusRecord {
            id: "chirp_fourier6_butson_samples",
            kind: "chm_family_finite",
            recorded_status: ChartStatus::FiniteCorpusDiagnostic,
            replayed_status: ChartStatus::FiniteCorpusDiagnostic,
            status: ChartStatus::FiniteCorpusDiagnostic,
            dimension: "order-6 chirp α∈{0..5}",
            evidence: "mub6_f6_external_b3::chirp_fourier6_columns",
            notes: "Butson-type samples over Q(ζ24); diagnostic only",
        },
        ChmLocusRecord {
            id: "tao_s6_isolated_matrix",
            kind: "chm_isolated",
            recorded_status: ChartStatus::ExactChmDeclared,
            replayed_status: ChartStatus::ExactChmDeclared,
            status: ChartStatus::ExactChmDeclared,
            dimension: "discrete point over Z3 / Q(zeta_24)",
            evidence: "szollosi_triad_solver::tao_s6_matrix",
            notes: "Chernyavsky-Tao isolated spectral matrix S6; internally non-MU (diagonal=36)",
        },
        ChmLocusRecord {
            id: "szollosi_b6_discrete_family",
            kind: "chm_2circulant_family",
            recorded_status: ChartStatus::ExactChmDeclared,
            replayed_status: ChartStatus::ClaimNotReplayed,
            status: ChartStatus::ClaimNotReplayed,
            dimension: "discrete root-of-unity samples (360 points in mu_24^4)",
            evidence: "szollosi_triad_solver::search_discrete_szollosi_chm_points",
            notes: "Szollosi 2-circulant family; exact z1 + z2 = 0 deltoid condition over Q(zeta_24)",
        },
        ChmLocusRecord {
            id: "szollosi_tao_triad_search",
            kind: "mu_triple_discrete_search",
            recorded_status: ChartStatus::FiniteCorpusDiagnostic,
            replayed_status: ChartStatus::ClaimNotReplayed,
            status: ChartStatus::ClaimNotReplayed,
            dimension: "exhaustive 331,776 tuples in mu_24^4 + Tao S6 permutation orbits",
            evidence: "artifacts/szollosi_triad_search_receipt.json",
            notes: "verified 0 MU triads between S6 and discrete B6 points; exact obstruction boundaries recorded",
        },
    ];

    let open_residual = vec![
        ChmLocusRecord {
            id: "R1_F6_xy_external_B3_continuous",
            kind: "mu_triple_locus_continuous",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "continuous (x,y)×external B3 beyond 6 locked lattice seeds",
            evidence: "mub6_f6_external_b3; lattice 24×24 locks only 6 genuine seeds",
            notes: "taxonomy R1; finite corpus residual; not continuous no-go",
        },
        ChmLocusRecord {
            id: "R2_Y2Q2_delta_1_1000_nbhd_deferred",
            kind: "local_cover_hygiene",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "δ=1/1000 full 5-torus nbhd on Y2Q2 three seeds only",
            evidence: "mub_y2q2_neigh_receipt_20260724.md DEFERRED",
            notes: "taxonomy R2; host wall-time residual — NOT global MUB wall; de-ranked Q1",
        },
        ChmLocusRecord {
            id: "R3_dephased_CHM_moduli_outside_delta_patches",
            kind: "mu_triple_moduli",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "entrywise dephased CHM moduli outside recorded δ-patches",
            evidence: "mub6_moduli_atlas OpenResidual; C2 pairwise only",
            notes: "taxonomy R3; patches pairwise disjoint ≠ exhaustion",
        },
        ChmLocusRecord {
            id: "R4_basis_gluing_and_psi_bridge",
            kind: "proof_obligation",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "vector walls → Ψ_basis / basis-gluing gate obligations",
            evidence: "basis_gluing_gate MissingProofObligation; ENC-1149 wiring needs inputs",
            notes: "taxonomy R4; local vector covers do not mint 4-MUB no-go",
        },
        ChmLocusRecord {
            id: "R5_C2_full_atlas_glue",
            kind: "atlas_coherence",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "multi-patch patches_glue + transport + ZeroRel preservation",
            evidence: "mub6_atlas_c2 pairwise ProvenDisjoint only",
            notes: "taxonomy R5; not discharged by seed distance charts",
        },
        ChmLocusRecord {
            id: "R6_sporadic_6x6_CHM_literature_classes",
            kind: "chm_classification",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "literature sporadic / non-affine classes (no Omega certificates)",
            evidence: "none in Omega; literature only",
            notes: "taxonomy R6; named residual only — no imported authority",
        },
        ChmLocusRecord {
            id: "R7_ENC-1147_full_6x6_CHM_exhaustion",
            kind: "classification_wall",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "all equivalence classes of 6×6 complex Hadamard matrices",
            evidence: "frontier hardness map; open classification problem",
            notes: "taxonomy R7; irreducible global residual for pure cover-route MUB(6)≤3",
        },
        ChmLocusRecord {
            id: "R8_lean_kernel_reflection_scale",
            kind: "mechanization_gap",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "~1e6 cover leaves → Lean reflection / stratified manifest",
            evidence: "kernel_reflection_pilot_* JSON only; LEAN_BUILD_STALE honesty",
            notes: "taxonomy R8; cert shape redesign if full in-kernel replay infeasible",
        },
        ChmLocusRecord {
            id: "R9_path_b_invariant_survivor",
            kind: "rigidity_route",
            recorded_status: ChartStatus::OpenResidual,
            replayed_status: ChartStatus::OpenResidual,
            status: ChartStatus::OpenResidual,
            dimension: "I(T) with Gate A∧B on exact basepoints (incl. Dita second basepoints)",
            evidence: "d6_exact_deformation_invariance_probe*; d6_exact_second_basepoint_probe",
            notes: "taxonomy R9; cohomological candidates fail A on T0; campaign ongoing",
        },
    ];

    let charted_count = charted.len();
    let open_residual_count = open_residual.len();

    ChmRegistryReport {
        schema_version: "omega.mub.chm-registry.v2",
        enc_residual: "ENC-1147",
        charted,
        open_residual,
        charted_count,
        open_residual_count,
        mechanical_checks_ok: ok,
        mechanical_check_detail: checks,
        terminal: "OpenResidual",
        firewall:
            "registry is status only; charted loci ≠ moduli exhaustion; stated region only; mints no authority",
    }
}

pub fn write_chm_registry_artifact() -> Result<std::path::PathBuf, String> {
    let report = current_chm_registry();
    if !report.mechanical_checks_ok {
        return Err(format!(
            "refusing to write registry with failed mechanical checks: {:?}",
            report.mechanical_check_detail
        ));
    }
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("mub6_chm_registry_enc1147_20260724.json");
    let json = serde_json::to_string_pretty(&report).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn registry_mechanical_checks_pass() {
        let r = current_chm_registry();
        assert!(
            r.mechanical_checks_ok,
            "checks failed: {:?}",
            r.mechanical_check_detail
        );
        assert_eq!(r.terminal, "OpenResidual");
        assert!(r.firewall.contains("mints no authority"));
        assert!(r.firewall.contains("stated region only"));
    }

    #[test]
    fn registry_separates_charted_from_open() {
        let r = current_chm_registry();
        assert!(r.charted_count >= 5);
        assert!(r.open_residual_count >= 3);
        assert!(r
            .open_residual
            .iter()
            .any(|l| l.id.contains("ENC-1147") || l.id.contains("exhaustion")));
        assert!(r.charted.iter().any(|l| l.id.contains("dita_seed_F6_0_8")));
        assert!(r.charted.iter().all(|l| l.status == l.replayed_status));
        assert!(r.charted.iter().all(|l| !matches!(
            l.replayed_status,
            ChartStatus::OpenResidual
                | ChartStatus::PointFullTorusCoverComplete
                | ChartStatus::NeighborhoodFullTorusCoverComplete
        )));
        assert!(r.charted.iter().any(|l| {
            matches!(
                l.recorded_status,
                ChartStatus::PointFullTorusCoverComplete
                    | ChartStatus::NeighborhoodFullTorusCoverComplete
            ) && l.replayed_status != l.recorded_status
        }));
        assert!(r
            .open_residual
            .iter()
            .all(|l| l.recorded_status == ChartStatus::OpenResidual
                && l.replayed_status == ChartStatus::OpenResidual));
    }

    #[test]
    fn write_registry_artifact() {
        let p = write_chm_registry_artifact().expect("write registry");
        assert!(p.exists());
        let raw = std::fs::read_to_string(&p).unwrap();
        assert!(raw.contains("ENC-1147"));
        assert!(raw.contains("omega.mub.chm-registry.v2"));
        let value: serde_json::Value = serde_json::from_str(&raw).unwrap();
        for locus in value["charted"].as_array().unwrap() {
            let replayed = locus["replayed_status"].as_str().unwrap();
            assert_ne!(replayed, "PointFullTorusCoverComplete");
            assert_ne!(replayed, "NeighborhoodFullTorusCoverComplete");
            assert_eq!(locus["status"].as_str(), Some(replayed));
        }
    }
}
