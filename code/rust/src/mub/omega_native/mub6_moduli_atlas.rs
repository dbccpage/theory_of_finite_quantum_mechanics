//! MUB(6) moduli atlas — the cochain moved one degree up: the TRIPLE becomes the carrier.
//!
//! The fixed-tuple packet (`mub6_basis_extension_packet`) holds the triple `T0` fixed and asks
//! whether a fourth basis extends it. This module **moves the cochain one left**: the triple `T`
//! stops being the fixed background and becomes the new carrier `C0` — a point of the *moduli of
//! MU triples* — and the extension obstruction `Psi_basis(T)` becomes a *function on that
//! carrier*. The frontier `MUB(6) <= 3` is exactly
//!
//! ```text
//!   Psi_basis(T) > 0  for EVERY MU triple T
//!     <=>  a finite certified cover (an ATLAS) of the moduli by neighborhood patches,
//!          each certifying "no fourth MU basis" over its region.
//! ```
//!
//! The observer never moves: `T0` stays the base point; the moduli *arises* around it as the
//! enclosure widens. Each arising is recorded as a `ModuliCoverPatch`. The atlas is the recorded
//! walk; the un-arisen rest of the moduli is the open residual (ENC-1147: the 6x6 complex-Hadamard
//! classification).
//!
//! The cochain, one degree up:
//! * `C0` = MU triples `T` (the moduli is the ground);
//! * `delta` = variation of `T`; `ZeroRel` = same triple up to the dephasing/permutation/phase
//!   gauge (`MUB.TripleGaugeReduction` / `TripleHadamardDephase`);
//! * `C1` = how `Psi_basis(T)` varies as `T` moves — its certified *moduli margin* is the new
//!   invariant read off the lift (the delta-robustness of the no-go);
//! * `C2` = whether the patches glue: a Cech cover (overlap-compatible, gap-free) of the moduli.
//!
//! This **extends the `global_atlas` gate with real accepted patches**: that gate reports
//! `MissingProofObligation` with 0 patches; here we accept the first patch (the `delta = 1/1000`
//! moduli cover, a certified neighborhood of `T0`) while keeping the terminal honestly
//! `OpenResidual`, because one neighborhood is not the whole moduli.
//!
//! Trust + firewall: each patch rests on the exact-interval cover ENGINE (trusted Rust, NOT a
//! Lean reflection of the boxes); the atlas is NOT exhaustive; this is NOT `MUB(6)=3`; mints no
//! authority.

use serde::Serialize;

use crate::omega_native::exact::mub6_atlas_c2::{dita_seed_atlas_c2_report, AtlasC2Report};
use crate::omega_native::exact::mub6_cover_run::CoverCertificate;

/// One arising recorded in the algebra: a neighborhood patch of the moduli, certified complete by
/// an exact interval cover (no fourth MU vector for any triple in the patch, hence — via the
/// kernel-checked `FiniteVectorCover`/`FiniteBasisCover` bridges — no fourth MU basis).
#[derive(Debug, Clone, Serialize)]
pub struct ModuliCoverPatch {
    pub patch_id: String,
    /// The representative triple at the patch center (the base point of the neighborhood).
    pub center: &'static str,
    /// The moduli radius: the patch covers every triple within `delta` (entry-wise) of `center`.
    /// `"0"` is the point patch (`T0` only); `"1/1000"` is the certified neighborhood.
    pub delta: &'static str,
    /// The loaded exact cover certificate proving the patch is complete (0 uncertified).
    pub cover: CoverCertificate,
    /// `true` iff the cover is complete (0 uncertified) with an exact `min_gap` witness.
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

/// Path to the committed `delta = 1/1000` moduli cover certificate (a certified neighborhood of
/// `T0` in the moduli of MU triples).
pub const T0_MODULI_COVER_PATH: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/omega_mub/artifacts/gauge_fixed_5_torus_moduli_delta_1_1000_cover_certificate_20260621.json"
);

/// Path to a completed **point** full gauge-fixed 5-torus cover for a genuine Dita seed
/// (`delta = 0` — fixed triple only).
pub fn dita_seed_point_cover_path(dx: i64, dy: i64) -> String {
    format!(
        "{}/../tests/omega_mub/artifacts/dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged_complete.json",
        env!("CARGO_MANIFEST_DIR")
    )
}

/// Load the `delta = 1/1000` moduli cover as the first atlas patch (a certified neighborhood of
/// `T0`). Returns an error if the artifact is missing or unparseable — it never fabricates a patch.
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

/// Load a completed Dita seed **point** cover (`delta = "0"`) as an atlas patch.
/// Never fabricates completeness — the on-disk certificate must already be complete.
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

/// The three genuine Dita seed point patches currently on disk (2026-07-24k).
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

/// Path to a completed **neighborhood** full gauge-fixed 5-torus cover for a Dita seed
/// (`delta = 1/1000`).
pub fn dita_seed_neighborhood_cover_path(dx: i64, dy: i64, delta_tag: &str) -> String {
    format!(
        "{}/../tests/omega_mub/artifacts/dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_gauge_fixed_5_torus_presplit6_merged_complete.json",
        env!("CARGO_MANIFEST_DIR")
    )
}

/// Load a completed Dita seed **neighborhood** cover as an atlas patch.
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

/// Neighborhood patches currently on disk (delta=1/1000 full-torus per genuine seed).
/// Loads whichever merged certificates are present; never fabricates.
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

/// Terminal status of the moduli atlas.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum AtlasTerminal {
    /// The atlas has certified patches but does NOT yet cover the whole moduli of MU triples. The
    /// un-charted region (ENC-1147, the 6x6 complex-Hadamard classification) is the open frontier.
    OpenResidual,
}

/// The moduli atlas: the recorded walk of certified neighborhood patches, the new margin invariant
/// read off the lift, and the honest residual (the rest of the moduli not yet covered).
#[derive(Debug, Clone, Serialize)]
pub struct Mub6ModuliAtlas {
    pub patches: Vec<ModuliCoverPatch>,
    /// `true` iff the patches provably cover the WHOLE moduli of MU triples (they do not yet).
    pub exhaustive_moduli_cover: bool,
    /// `C2` — full multi-patch Čech gluing of the **entire** atlas (including T0 ↔ Dita).
    /// Remains false until cross-family gluing and moduli exhaustion discharge.
    pub patches_glue: bool,
    /// Partial C2 analysis on the genuine-Dita sub-atlas (nested containment + pairwise
    /// neighborhood separation). See `mub6_atlas_c2`.
    pub dita_c2: AtlasC2Report,
    /// The new `C1` invariant read off the lift: the certified *moduli margin* recorded by the
    /// committed full gauge-fixed five-torus neighborhood certificate.
    pub certified_moduli_margin: &'static str,
    pub open_obligation: &'static str,
    pub terminal: AtlasTerminal,
    pub trust_anchor: &'static str,
    pub firewall: &'static str,
}

/// Build the current moduli atlas: load the certified patches we hold
/// (`T0` neighborhood + three Dita **point** covers + any Dita **neighborhood** covers),
/// record the margin invariant, and seal honestly as `OpenResidual`.
///
/// Multiple patches without a discharged Cech gluing check: `patches_glue = false`.
pub fn current_moduli_atlas() -> Result<Mub6ModuliAtlas, String> {
    let patch0 = load_t0_neighborhood_patch()?;
    let mut patches = vec![patch0];
    patches.extend(load_dita_seed_point_patches()?);
    patches.extend(load_dita_seed_neighborhood_patches()?);
    let dita_c2 = dita_seed_atlas_c2_report();
    Ok(Mub6ModuliAtlas {
        patches,
        // Recorded patches are not the whole moduli of MU triples.
        exhaustive_moduli_cover: false,
        // Full atlas C2 remains open (T0 ↔ Dita + ENC-1147) even if Dita pairs are disjoint.
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
        // T0 + 3 point + N neighborhood patches (N grows as farms complete).
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
