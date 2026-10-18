
use serde::Serialize;

use crate::omega_native::exact::mub6_atlas_c2::{dita_seed_atlas_c2_report, AtlasC2Report};
use crate::omega_native::exact::mub6_cover_run::CoverCertificate;

#[derive(Debug, Clone, Serialize)]
pub struct ModuliCoverPatch {
    pub patch_id: String,
    pub center: &'static str,
    pub delta: &'static str,
    pub cover: CoverCertificate,
    pub certified_complete: bool,
}

impl ModuliCoverPatch {
    fn from_cover(
        patch_id: impl Into<String>,
        center: &'static str,
        delta: &'static str,
        cover: CoverCertificate,
    ) -> Self {
        let certified_complete =
            cover.complete && cover.uncertified == 0 && cover.min_gap.is_some();
        Self {
            patch_id: patch_id.into(),
            center,
            delta,
            cover,
            certified_complete,
        }
    }
}

pub const T0_MODULI_COVER_PATH: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/omega_mub/artifacts/gauge_fixed_5_torus_moduli_delta_1_1000_cover_certificate_20260621.json"
);

pub fn dita_seed_point_cover_path(dx: i64, dy: i64) -> String {
    format!(
        "{}/../tests/omega_mub/artifacts/dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged_complete.json",
        env!("CARGO_MANIFEST_DIR")
    )
}

pub fn load_t0_neighborhood_patch() -> Result<ModuliCoverPatch, String> {
    let raw = std::fs::read_to_string(T0_MODULI_COVER_PATH)
        .map_err(|e| format!("read {T0_MODULI_COVER_PATH}: {e}"))?;
    let cover: CoverCertificate =
        serde_json::from_str(&raw).map_err(|e| format!("parse moduli cover certificate: {e}"))?;
    Ok(ModuliCoverPatch::from_cover(
        "t0-neighborhood-delta-1/1000",
        "canonical_triple_T0",
        "1/1000",
        cover,
    ))
}

pub fn load_dita_seed_point_patch(
    dx: i64,
    dy: i64,
    center: &'static str,
    patch_id: impl Into<String>,
) -> Result<ModuliCoverPatch, String> {
    let path = dita_seed_point_cover_path(dx, dy);
    let raw = std::fs::read_to_string(&path).map_err(|e| format!("read {path}: {e}"))?;
    let cover: CoverCertificate =
        serde_json::from_str(&raw).map_err(|e| format!("parse {path}: {e}"))?;
    if !cover.complete || cover.uncertified != 0 {
        return Err(format!(
            "refusing incomplete seed cover {path}: complete={} uncertified={}",
            cover.complete, cover.uncertified
        ));
    }
    Ok(ModuliCoverPatch::from_cover(patch_id, center, "0", cover))
}

pub fn load_dita_seed_point_patches() -> Result<Vec<ModuliCoverPatch>, String> {
    Ok(vec![
        load_dita_seed_point_patch(0, 8, "I_F6_0_8_Y2Q1", "dita-seed-F6-0-8-point-full-torus")?,
        load_dita_seed_point_patch(8, 0, "I_F6_8_0_Y2Q1", "dita-seed-F6-8-0-point-full-torus")?,
        load_dita_seed_point_patch(
            16,
            16,
            "I_F6_16_16_Y2Q1",
            "dita-seed-F6-16-16-point-full-torus",
        )?,
    ])
}

pub fn dita_seed_neighborhood_cover_path(dx: i64, dy: i64, delta_tag: &str) -> String {
    format!(
        "{}/../tests/omega_mub/artifacts/dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_gauge_fixed_5_torus_presplit6_merged_complete.json",
        env!("CARGO_MANIFEST_DIR")
    )
}

pub fn load_dita_seed_neighborhood_patch(
    dx: i64,
    dy: i64,
    delta_tag: &str,
    delta_display: &'static str,
    center: &'static str,
    patch_id: impl Into<String>,
) -> Result<ModuliCoverPatch, String> {
    let path = dita_seed_neighborhood_cover_path(dx, dy, delta_tag);
    let raw = std::fs::read_to_string(&path).map_err(|e| format!("read {path}: {e}"))?;
    let cover: CoverCertificate =
        serde_json::from_str(&raw).map_err(|e| format!("parse {path}: {e}"))?;
    if !cover.complete || cover.uncertified != 0 {
        return Err(format!(
            "refusing incomplete neighborhood cover {path}: complete={} uncertified={}",
            cover.complete, cover.uncertified
        ));
    }
    Ok(ModuliCoverPatch::from_cover(
        patch_id,
        center,
        delta_display,
        cover,
    ))
}

pub fn load_dita_seed_neighborhood_patches() -> Result<Vec<ModuliCoverPatch>, String> {
    let candidates: &[(i64, i64, &str, &str)] = &[
        (
            0,
            8,
            "I_F6_0_8_Y2Q1",
            "dita-seed-F6-0-8-neighborhood-delta-1/1000",
        ),
        (
            8,
            0,
            "I_F6_8_0_Y2Q1",
            "dita-seed-F6-8-0-neighborhood-delta-1/1000",
        ),
        (
            16,
            16,
            "I_F6_16_16_Y2Q1",
            "dita-seed-F6-16-16-neighborhood-delta-1/1000",
        ),
    ];
    let mut out = Vec::new();
    for &(dx, dy, center, id) in candidates {
        let path = dita_seed_neighborhood_cover_path(dx, dy, "1_1000");
        if !std::path::Path::new(&path).exists() {
            continue;
        }
        out.push(load_dita_seed_neighborhood_patch(
            dx, dy, "1_1000", "1/1000", center, id,
        )?);
    }
    if out.is_empty() {
        return Err("no Dita seed neighborhood merged certificates on disk".into());
    }
    Ok(out)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum AtlasTerminal {
    OpenResidual,
}

#[derive(Debug, Clone, Serialize)]
pub struct Mub6ModuliAtlas {
    pub patches: Vec<ModuliCoverPatch>,
    pub exhaustive_moduli_cover: bool,
    pub patches_glue: bool,
    pub dita_c2: AtlasC2Report,
    pub certified_moduli_margin: &'static str,
    pub open_obligation: &'static str,
    pub terminal: AtlasTerminal,
    pub trust_anchor: &'static str,
    pub firewall: &'static str,
}

pub fn current_moduli_atlas() -> Result<Mub6ModuliAtlas, String> {
    let patch0 = load_t0_neighborhood_patch()?;
    let mut patches = vec![patch0];
    patches.extend(load_dita_seed_point_patches()?);
    patches.extend(load_dita_seed_neighborhood_patches()?);
    let dita_c2 = dita_seed_atlas_c2_report();
    Ok(Mub6ModuliAtlas {
        patches,
        exhaustive_moduli_cover: false,
        patches_glue: false,
        dita_c2,
        certified_moduli_margin:
            "T0 neighborhood delta=1/1000; Dita point covers ×3 (certified=1035821 each); Dita neighborhood delta=1/1000 covers (certified=1138055 each); partial C2 on Dita sub-atlas via mub6_atlas_c2",
        open_obligation:
            "ENC-1147 CHM exhaustion; basis-gluing theorem; kernel-reflection of full 5-torus leaves (narrow+wide cell pilots exist); C2 pairwise neighborhood separation charted for T0 and Dita",
        terminal: AtlasTerminal::OpenResidual,
        trust_anchor:
            "each patch rests on the exact-interval cover engine (mub6_cover / mub6_interval_cover / mub6_cyclotomic_enclosure); box-level Lean reflection is pilot-only (narrow cell)",
        firewall:
            "atlas NOT exhaustive; stated region only; full multi-patch C2 open; partial Dita C2 is diagnostic; mints no authority",
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn t0_neighborhood_patch_loads_certified_complete() {
        let p = load_t0_neighborhood_patch().expect("committed moduli cover artifact loads");
        assert!(
            p.certified_complete,
            "the neighborhood cover is complete and exact"
        );
        assert_eq!(
            p.cover.uncertified, 0,
            "no uncertified residue in the neighborhood"
        );
        assert_eq!(p.cover.certified, 987_058);
        assert_eq!(p.delta, "1/1000");
        assert!(
            p.cover.min_gap.is_some(),
            "exact rational tightness witness present"
        );
    }

    #[test]
    fn moduli_atlas_records_first_arising_and_stays_open_residual() {
        let atlas = current_moduli_atlas().expect("atlas builds from the held patches");
        assert!(
            atlas.patches.len() >= 5,
            "at least T0 + 3 points + 1 neighborhood expected, got {}",
            atlas.patches.len()
        );
        assert!(atlas.patches.iter().all(|p| p.certified_complete));
        assert!(!atlas.exhaustive_moduli_cover);
        assert!(!atlas.patches_glue);
        assert_eq!(atlas.terminal, AtlasTerminal::OpenResidual);
        assert!(atlas.firewall.contains("stated region only"));
        assert!(atlas.dita_c2.all_nested_discharged);
        assert!(!atlas.dita_c2.full_atlas_c2_discharged);
        assert_eq!(atlas.patches[0].delta, "1/1000");
        for p in &atlas.patches[1..4] {
            assert_eq!(p.delta, "0");
            assert_eq!(p.cover.certified, 1_035_821);
        }
        for p in &atlas.patches[4..] {
            assert_eq!(p.delta, "1/1000");
            assert_eq!(p.cover.certified, 1_138_055);
            assert_eq!(p.cover.uncertified, 0);
        }
    }

    #[test]
    fn dita_seed_point_patches_load_complete() {
        let patches = load_dita_seed_point_patches().expect("three seed point covers on disk");
        assert_eq!(patches.len(), 3);
        for p in patches {
            assert!(p.certified_complete);
            assert_eq!(p.delta, "0");
            assert_eq!(p.cover.certified, 1_035_821);
            assert_eq!(p.cover.uncertified, 0);
            assert!(p.cover.min_gap.is_some());
        }
    }

    #[test]
    fn dita_seed_neighborhood_patches_load_complete_when_present() {
        let patches =
            load_dita_seed_neighborhood_patches().expect("at least one neighborhood on disk");
        assert!(!patches.is_empty());
        for p in patches {
            assert!(p.certified_complete);
            assert_eq!(p.delta, "1/1000");
            assert_eq!(p.cover.certified, 1_138_055);
            assert_eq!(p.cover.uncertified, 0);
            assert_eq!(p.cover.max_depth_used, 32);
            assert!(p.cover.min_gap.is_some());
        }
    }
}
