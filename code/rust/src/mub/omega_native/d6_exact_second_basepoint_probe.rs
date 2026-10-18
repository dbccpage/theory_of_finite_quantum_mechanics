
use serde::Serialize;

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec};
use crate::omega_native::exact::d6_exact_deformation_invariance_probe::{
    run_probe_on_columns, SampleCategory,
};
use crate::omega_native::campaign::mub6_dita_seed_cover::{
    all_genuine_dita_seeds, dita_seed_triple_columns, dita_seed_triple_is_pairwise_mu,
};

crate::fixture_set!(fixtures, "d6_exact_second_basepoint_probe");

#[derive(Debug, Clone, Serialize)]
pub struct BasepointFingerprint {
    pub id: String,
    pub kind: &'static str,
    pub pairwise_mu: bool,
    pub structural_ok: bool,
    pub gate_a_pass: bool,
    pub gate_b_pass: bool,
    pub far_control_pair: (usize, Option<usize>),
    pub modal_flat_pair: Option<(usize, Option<usize>)>,
    pub wall_sample_count: usize,
    pub min_h1: Option<usize>,
    pub max_h1: Option<usize>,
    pub gate_a_reason: String,
    pub gate_b_reason: String,
    pub is_presentation_fixed: bool,
    pub presentation_dependence_warning: &'static str,
}

#[derive(Debug, Clone, Serialize)]
pub struct SecondBasepointCampaignReport {
    pub schema_version: &'static str,
    pub programme: &'static str,
    pub basepoints: Vec<BasepointFingerprint>,
    pub dita_seeds_usable_as_exact_second_basepoints: bool,
    pub triple_level_fingerprint_differs_from_t0: bool,
    pub any_basepoint_gate_a_and_b: bool,
    pub verdict: &'static str,
    pub kill_note: String,
    pub is_presentation_fixed: bool,
    pub terminal: &'static str,
    pub firewall: &'static str,
}

fn modal_pair(pairs: &[(usize, Option<usize>)]) -> Option<(usize, Option<usize>)> {
    let mut best: Option<((usize, Option<usize>), usize)> = None;
    for &p in pairs {
        let count = pairs.iter().filter(|&&q| q == p).count();
        match best {
            Some((_, bc)) if bc >= count => {}
            _ => best = Some((p, count)),
        }
    }
    best.map(|(p, _)| p)
}

fn fingerprint(
    id: String,
    kind: &'static str,
    pairwise_mu: bool,
    columns: &[ExactVec],
) -> BasepointFingerprint {
    let report = run_probe_on_columns(columns);
    let structural_ok = report
        .rows
        .iter()
        .all(|r| r.is_unit && r.phase_gauge_in_kernel && r.d1_after_d0_zero);
    let far_pairs: Vec<(usize, Option<usize>)> = report
        .rows
        .iter()
        .filter(|r| r.category == SampleCategory::FarControl)
        .map(|r| r.invariant_pair())
        .collect();
    let flat_pairs: Vec<(usize, Option<usize>)> = report
        .rows
        .iter()
        .filter(|r| r.category == SampleCategory::FlatTorus)
        .map(|r| r.invariant_pair())
        .collect();
    let far_control_pair = far_pairs.first().copied().unwrap_or((0, None));
    let min_h1 = report.rows.iter().filter_map(|r| r.h1_dim).min();
    let max_h1 = report.rows.iter().filter_map(|r| r.h1_dim).max();
    BasepointFingerprint {
        id,
        kind,
        pairwise_mu,
        structural_ok,
        gate_a_pass: report.gate_a_pass,
        gate_b_pass: report.gate_b_pass,
        far_control_pair,
        modal_flat_pair: modal_pair(&flat_pairs),
        wall_sample_count: report.wall_samples.len(),
        min_h1,
        max_h1,
        gate_a_reason: report.gate_a_reason,
        gate_b_reason: report.gate_b_reason,
        is_presentation_fixed: true,
        presentation_dependence_warning: "Fixed-sample fingerprints are presentation-dependent (not gauge-invariant across triples without covariant transport of candidate vectors, R03).",
    }
}

pub fn run_second_basepoint_campaign() -> SecondBasepointCampaignReport {
    let mut basepoints = Vec::new();

    let t0_cols = canonical_triple_exact();
    basepoints.push(fingerprint(
        "T0_product".into(),
        "canonical_product",
        fixtures().flag("t0_pairwise_mu"),
        &t0_cols,
    ));

    for (dx, dy, qa) in all_genuine_dita_seeds() {
        let id = format!("dita_F6_{dx}_{dy}_Y2Q{qa}");
        let mu = dita_seed_triple_is_pairwise_mu(dx, dy);
        let cols = dita_seed_triple_columns(dx, dy);
        basepoints.push(fingerprint(id, "dita_seed", mu, &cols));
    }

    let t0 = basepoints
        .iter()
        .find(|b| b.id == "T0_product")
        .expect("T0 present");
    let dita: Vec<&BasepointFingerprint> = basepoints
        .iter()
        .filter(|b| b.kind == "dita_seed")
        .collect();

    let dita_seeds_usable_as_exact_second_basepoints =
        dita.iter().all(|b| b.pairwise_mu && b.structural_ok);

    let triple_level_fingerprint_differs_from_t0 = dita.iter().any(|b| {
        b.far_control_pair != t0.far_control_pair
            || b.modal_flat_pair != t0.modal_flat_pair
            || b.gate_a_pass != t0.gate_a_pass
            || b.gate_b_pass != t0.gate_b_pass
            || b.min_h1 != t0.min_h1
            || b.max_h1 != t0.max_h1
    });

    let any_basepoint_gate_a_and_b = basepoints.iter().any(|b| b.gate_a_pass && b.gate_b_pass);

    let (verdict, kill_note) = if !dita_seeds_usable_as_exact_second_basepoints {
        (
            "SECOND_BASEPOINT_UNUSABLE",
            "At least one Dita seed failed pairwise MU or structural probe checks; \
             Path B Month-2 kill risk: no usable second exact basepoint."
                .to_string(),
        )
    } else if any_basepoint_gate_a_and_b {
        (
            "GATE_A_AND_B_SIGNAL_ON_SOME_BASEPOINT",
            "A basepoint shows Gate A∧B signal for (rank_j,h1); escalate that invariant \
             family — still OpenResidual, not Path B closed."
                .to_string(),
        )
    } else if triple_level_fingerprint_differs_from_t0 {
        (
            "SECOND_BASEPOINT_USABLE_FINGERPRINT_DIFFERS",
            "Dita seeds are exact second basepoints and differ from T0 on probe fingerprint; \
             but cohomological (rank_j,h1) still fails Gate A∧B jointly on all basepoints \
             (same failure mode class as T0 unless gates flipped). Continue B0 only with \
             new I candidates or accept cohomological tombstone on these basepoints."
                .to_string(),
        )
    } else {
        (
            "SECOND_BASEPOINT_USABLE_SAME_FAILURE_MODE",
            "Dita seeds are usable as exact second basepoints, but their vector-level \
             (rank_j,h1) Gate A/B fingerprint matches T0's failure mode (Gate A FAIL; \
             Gate B wall or rigid-blind). Second basepoints do NOT rescue this I family. \
             Month-4 kill: need a different I or Path B tombstone for cohomological pair."
                .to_string(),
        )
    };

    SecondBasepointCampaignReport {
        schema_version: "omega.mub.second-basepoint.v1",
        programme: "MUB-Q1-PathB-B0",
        basepoints,
        dita_seeds_usable_as_exact_second_basepoints,
        triple_level_fingerprint_differs_from_t0,
        any_basepoint_gate_a_and_b,
        verdict,
        kill_note,
        is_presentation_fixed: true,
        terminal: "OpenResidual",
        firewall: "second-basepoint campaign is diagnostic; stated region only; mints no Path B theorem; mints no authority",
    }
}

pub fn write_second_basepoint_artifact() -> Result<std::path::PathBuf, String> {
    let report = run_second_basepoint_campaign();
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("mub6_second_basepoint_campaign_20260725.json");
    let json = serde_json::to_string_pretty(&report).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn dita_seeds_are_pairwise_mu() {
        for (dx, dy, _) in all_genuine_dita_seeds() {
            assert!(
                dita_seed_triple_is_pairwise_mu(dx, dy),
                "seed F6({dx},{dy}) must be pairwise MU"
            );
        }
    }

    #[test]
    fn representative_second_basepoints_structural_and_open_residual() {
        let t0 = fingerprint(
            "T0_product".into(),
            "canonical_product",
            true,
            &canonical_triple_exact(),
        );
        assert!(t0.structural_ok);
        assert!(!t0.gate_a_pass, "T0 cohomological Gate A stays FAIL");

        let y2q1 = fingerprint(
            "dita_F6_0_8_Y2Q1".into(),
            "dita_seed",
            dita_seed_triple_is_pairwise_mu(0, 8),
            &dita_seed_triple_columns(0, 8),
        );
        assert!(y2q1.pairwise_mu && y2q1.structural_ok);

        let y2q2 = fingerprint(
            "dita_F6_0_16_Y2Q2".into(),
            "dita_seed",
            dita_seed_triple_is_pairwise_mu(0, 16),
            &dita_seed_triple_columns(0, 16),
        );
        assert!(y2q2.pairwise_mu && y2q2.structural_ok);

        assert!(y2q1.pairwise_mu && y2q2.pairwise_mu);
    }

    #[test]
    fn full_second_basepoint_campaign_usable_and_open() {
        let r = run_second_basepoint_campaign();
        assert_eq!(r.terminal, "OpenResidual");
        assert!(r.firewall.contains("stated region only"));
        assert_eq!(r.basepoints.len(), 1 + 6);
        assert!(
            r.dita_seeds_usable_as_exact_second_basepoints,
            "all Dita seeds must be usable exact second basepoints"
        );
        assert!(
            !r.any_basepoint_gate_a_and_b,
            "unexpected Gate A∧B survivor — update campaign ledger if this flips"
        );
        assert!(
            r.verdict == "SECOND_BASEPOINT_USABLE_SAME_FAILURE_MODE"
                || r.verdict == "SECOND_BASEPOINT_USABLE_FINGERPRINT_DIFFERS",
            "unexpected verdict {}",
            r.verdict
        );
    }

    #[test]
    fn write_campaign_artifact() {
        let p = write_second_basepoint_artifact().expect("write");
        assert!(p.exists());
        let raw = std::fs::read_to_string(&p).unwrap();
        assert!(raw.contains("OpenResidual"));
        assert!(raw.contains("dita_F6_"));
    }
}
