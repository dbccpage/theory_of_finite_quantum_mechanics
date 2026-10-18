//! R1-S1 parametric cover **design scaffold**: family
//! `T(x,y; a=1) = { I, F6(x,y), Y2⊗Q1 }`.
//!
//! This module declares chart domain, pilot tubes around genuine Y2Q1 seeds, and a
//! cost/readiness report. It does **not** run a full continuous base×fiber cover farm.
//!
//! Design doc: `012_mutually_unbiased_bases/mub6_r1_parametric_cover_design.md`.

use serde::Serialize;

use crate::omega_native::campaign::mub6_dita_seed_cover::dita_seed_triple_is_pairwise_mu;
use crate::omega_native::exact::mub6_f6_chart::f6_point_is_exact_chm;
use crate::omega_native::campaign::mub6_f6_external_b3::genuine_dita_y2q1_triple_seeds;

/// Continuous base domain kind for R1-S1.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum R1BaseDomainKind {
    /// Positive-measure tubes around lattice seeds (pilot).
    SeedTubesLatticeStep,
    /// Full \([0,2π)²` — explicitly out of v0 budget.
    FullTorusDeferred,
}

/// One pilot base tube in lattice coordinates (exact \(\zeta_{24}\) chart).
#[derive(Debug, Clone, Serialize)]
pub struct R1SeedTube {
    pub seed_dx: i64,
    pub seed_dy: i64,
    /// Half-width in lattice steps (1 = one \(\zeta_{24}\) step each side, continuous lift).
    pub half_width_lattice_steps: u32,
    pub external_qa: i64,
    pub seed_is_exact_chm: bool,
    pub seed_triple_pairwise_mu: bool,
}

/// Cost model row (planning bounds, not a timing proof).
#[derive(Debug, Clone, Serialize)]
pub struct R1CostModelRow {
    pub scenario: &'static str,
    pub relative_to_one_point_cover: &'static str,
    pub covers_positive_measure_base: bool,
    pub v0_allowed: bool,
}

/// Readiness / design report for R1-S1.
#[derive(Debug, Clone, Serialize)]
pub struct R1ParametricCoverDesignReport {
    pub schema_version: &'static str,
    pub slice_id: &'static str,
    pub residual_class: &'static str,
    pub family: &'static str,
    pub base_domain_kind: R1BaseDomainKind,
    pub fiber: &'static str,
    pub pilot_tubes: Vec<R1SeedTube>,
    pub cost_model: Vec<R1CostModelRow>,
    pub milestones: Vec<&'static str>,
    pub month3_design_status: &'static str,
    pub computational_next: &'static str,
    pub terminal: &'static str,
    pub firewall: &'static str,
}

/// Lattice half-width for pilot tubes (one \(\zeta_{24}\) step).
pub const R1_PILOT_HALF_WIDTH_LATTICE_STEPS: u32 = 1;

/// Build the R1-S1 design report (exact seed checks only; no cover farm).
pub fn r1_s1_design_report() -> R1ParametricCoverDesignReport {
    let mut tubes = Vec::new();
    for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
        tubes.push(R1SeedTube {
            seed_dx: dx,
            seed_dy: dy,
            half_width_lattice_steps: R1_PILOT_HALF_WIDTH_LATTICE_STEPS,
            external_qa: 1,
            seed_is_exact_chm: f6_point_is_exact_chm(dx, dy),
            seed_triple_pairwise_mu: dita_seed_triple_is_pairwise_mu(dx, dy),
        });
    }

    let cost_model = vec![
        R1CostModelRow {
            scenario: "seed_spray_N_lattice_points",
            relative_to_one_point_cover: "N x C_pt",
            covers_positive_measure_base: false,
            v0_allowed: false, // not the parametric design
        },
        R1CostModelRow {
            scenario: "three_seed_tubes_small_delta_base",
            relative_to_one_point_cover:
                "~3 x C_fiber(delta_base); hope ~3 x C_pt when delta small",
            covers_positive_measure_base: true,
            v0_allowed: true,
        },
        R1CostModelRow {
            scenario: "full_base_torus_fine_grid",
            relative_to_one_point_cover: ">> 10 x host budget without thinner gauge",
            covers_positive_measure_base: true,
            v0_allowed: false,
        },
    ];

    R1ParametricCoverDesignReport {
        schema_version: "omega.mub.r1-parametric-design.v1",
        slice_id: "R1-S1",
        residual_class: "R1",
        family: "T(x,y;a=1) = {I, F6(x,y), Y2⊗Q1}",
        base_domain_kind: R1BaseDomainKind::SeedTubesLatticeStep,
        fiber: "gauge-fixed 5-torus fourth-vector cover (existing Dita engines)",
        pilot_tubes: tubes,
        cost_model,
        milestones: vec![
            "M1 design+scaffold (this report)",
            "M2 one base box delta_base>0 complete fiber cover",
            "M3 three seed tubes complete",
            "M4 widen or dual-orbit a=2 copy",
        ],
        month3_design_status: "DESIGN_LANDED_not_seed_spray",
        computational_next: "Implement base-box enclosure + single-tube fiber cover (M2); do not start full torus grid",
        terminal: "OpenResidual",
        firewall:
            "R1-S1 design only; positive-measure tubes not yet certified; stated region only; mints no authority",
    }
}

/// Write design JSON under `artifacts/`.
pub fn write_r1_design_artifact() -> Result<std::path::PathBuf, String> {
    let report = r1_s1_design_report();
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("mub6_r1_parametric_cover_design_20260725.json");
    let json = serde_json::to_string_pretty(&report).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn r1_design_is_parametric_not_seed_spray() {
        let r = r1_s1_design_report();
        assert_eq!(r.slice_id, "R1-S1");
        assert_eq!(r.terminal, "OpenResidual");
        assert_eq!(r.month3_design_status, "DESIGN_LANDED_not_seed_spray");
        assert_eq!(r.pilot_tubes.len(), 3);
        assert!(r
            .pilot_tubes
            .iter()
            .all(|t| t.seed_is_exact_chm && t.seed_triple_pairwise_mu));
        assert!(r
            .cost_model
            .iter()
            .any(|c| c.covers_positive_measure_base && c.v0_allowed));
        assert!(r
            .cost_model
            .iter()
            .any(|c| c.scenario.contains("seed_spray") && !c.v0_allowed));
        assert!(r.firewall.contains("stated region only"));
    }

    #[test]
    fn write_r1_design_artifact_ok() {
        let p = write_r1_design_artifact().expect("write");
        assert!(p.exists());
        let raw = std::fs::read_to_string(&p).unwrap();
        assert!(raw.contains("R1-S1"));
        assert!(raw.contains("OpenResidual"));
    }
}
