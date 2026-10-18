//! Branch-and-bound cover certification for Terence Tao's isolated spectral seed triple {I, F6, S6}.
//!
//! AuthorityEffect: None
//! Restricted words: forced, minimal, free, canonical, equivalent, universal, complete
//! require proof or explicit conditional scope. The `complete` flag denotes finite
//! branch-and-bound partition termination over the declared stated region, nothing more.
//!
//! ## Overview
//!
//! This module implements exact rational and cyclotomic branch-and-bound box covers
//! over the gauge-fixed 5-torus [0, 2π]^5 for the fixed triple:
//! - B1: Standard basis I_6 of C^6.
//! - B2: Normalized Fourier matrix F_6 / sqrt(6) (at dx=0, dy=0).
//! - B3: Normalized Terence Tao isolated spectral matrix S_6 / sqrt(6) over Q(ζ₂₄) via Cyc24.
//!
//! The certification computes the exact rational lower bound on the squared curvature mass:
//!   Ψ^sq(T, U) = ∑_{j=0}^5 ∑_{i=0}^{17} ω_{ij}(U)^2 = ∑_{j=0}^5 Φ^sq(T, U_j)
//! where Φ^sq(T, v) = ∑_{i=0}^{17} (|⟨e_i, v⟩|² − 1/6)².
//!
//! For every certified box, residual_sq_lower(vbox) >= min_gap > 0 in exact rational arithmetic,
//! rigorously proving that no vector in the covered box can be mutually unbiased to the triple.
//! Zero floating-point arithmetic is permitted in the certificate verification chain.

use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

use crate::omega_native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::omega_native::exact::mub6_basis_cover::{
    certify_basis_box_excludes_fourth_for_triple, BasisBox,
};
use crate::omega_native::exact::mub6_cover::{cover_region, EnclosedTriple};
use crate::omega_native::exact::mub6_cover_run::{
    cover_region_prefiltered, gauge_fixed_torus_region, presplit_region, run_cover_parallel_with,
    CoverCertificate, EnclosedTripleF64,
};
use crate::omega_native::exact::mub6_f6_chart::f6_family_columns;
use crate::omega_native::exact::mub6_interval_cover::VectorBox;
use crate::omega_native::exact::szollosi_triad_solver::tao_s6_matrix;
use omega_kernel::interval::Interval;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_number_theory::rational::rq;

pub use crate::omega_native::exact::mub6_field::inv_sqrt6;

/// The 6 normalized columns of the Tao matrix S_6 / sqrt(6) in C^6 over `Q(ζ₂₄)`.
///
/// Each entry has modulus |[S_6]_{jk} / sqrt(6)| = 1/sqrt(6), so every column is
/// mutually unbiased to the standard basis. The columns are mutually orthonormal:
/// ⟨v_j, v_k⟩ = δ_{jk}.
pub fn tao_s6_columns() -> [ExactVec; D] {
    let s6 = tao_s6_matrix();
    let s = inv_sqrt6();
    std::array::from_fn(|col| std::array::from_fn(|row| s6[row][col].mul(&s)))
}

/// Exact 18 columns of the Tao seed triple diagnostic {I_6, F_6, S_6}.
///
/// NOTE (R11 audit): F_6 and S_6 share the normalized all-ones first column,
/// giving squared overlap 1 != 1/6 between column 0 of F_6 and column 0 of S_6.
/// This configuration is an arbitrary-basis diagnostic fixture, NOT an MU triple.
/// Residual exclusions against these bases do not constitute a fourth-basis extension certificate
/// for a genuine MU triple.
///
/// Layout follows canonical triple convention:
/// - Columns 0..6: Standard basis I_6
/// - Columns 6..12: Fourier basis F_6 / sqrt(6) (at dx=0, dy=0)
/// - Columns 12..18: Tao spectral basis S_6 / sqrt(6)
pub fn tao_seed_triple_columns() -> Vec<ExactVec> {
    let mut cols = Vec::with_capacity(3 * D);
    // B1: standard basis
    for idx in 0..D {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[idx] = Cyc24::rat(ri(1));
        cols.push(v);
    }
    // B2: Fourier basis F6(0,0)
    cols.extend_from_slice(&f6_family_columns(0, 0));
    // B3: Tao basis S6
    cols.extend_from_slice(&tao_s6_columns());
    cols
}

/// Build exact + f64 enclosures for the Tao seed triple {I_6, F_6, S_6}.
pub fn tao_seed_enclosed() -> (EnclosedTriple, EnclosedTripleF64) {
    let cols = tao_seed_triple_columns();
    (
        EnclosedTriple::from_exact_columns(&cols),
        EnclosedTripleF64::from_exact_columns(&cols),
    )
}

/// Narrow torus cell used for end-to-end complete-cover validation (matches `mub6_cover` tests).
pub fn narrow_torus_cell() -> VectorBox {
    let lo = ri(28) / ri(100) - ri(2) / ri(100);
    let hi = ri(28) / ri(100) + ri(2) / ri(100);
    std::array::from_fn(|_| Interval::new(lo.clone(), hi.clone()))
}

/// Wider torus cell that forces subdivision (matches `mub6_cover` wide-cell test).
pub fn wide_torus_cell() -> VectorBox {
    let lo = ri(28) / ri(100) - ri(18) / ri(100);
    let hi = ri(28) / ri(100) + ri(18) / ri(100);
    std::array::from_fn(|_| Interval::new(lo.clone(), hi.clone()))
}

/// Smoke basis box: column 0 near `e_0`, other columns wide — cannot be a fourth MU basis.
pub fn smoke_basis_box_col0_near_e0() -> BasisBox {
    let small = Interval::new(rq(-1, 20), rq(1, 20));
    let mut near_e0: VectorBox = std::array::from_fn(|_| small.clone());
    near_e0[0] = Interval::new(rq(9, 10), rq(1, 1));
    near_e0[1] = small;
    let wide = Interval::new(rq(-1, 1), rq(1, 1));
    let wide_col: VectorBox = std::array::from_fn(|_| wide.clone());
    let mut bbox: BasisBox = std::array::from_fn(|_| wide_col.clone());
    bbox[0] = near_e0;
    bbox
}

/// Smoke check for Tao seed triple: verifies that col0 near e0 is strictly excluded.
pub fn tao_seed_smoke_check() -> (bool, Option<String>) {
    let cols = tao_seed_triple_columns();
    let bbox = smoke_basis_box_col0_near_e0();
    let basis_cert = certify_basis_box_excludes_fourth_for_triple(&cols, &bbox);
    let enclosed = EnclosedTriple::from_exact_columns(&cols);
    let vgap = enclosed.residual_sq_lower(&bbox[0]);
    let excluded = basis_cert.is_some() && (vgap > BigRational::zero());
    (
        excluded,
        if excluded {
            Some(vgap.to_string())
        } else {
            None
        },
    )
}

/// Run the exact cover engine on a stated region against the Tao seed triple.
pub fn cover_tao_region(region: VectorBox, max_depth: u32) -> CoverCertificate {
    let (exact, _) = tao_seed_enclosed();
    let report = cover_region(&exact, region, max_depth);
    report.certificate("tao_seed_I_F6_S6_region")
}

/// Run the prefiltered (f64 guide + exact certify) cover on a stated region for Tao seed.
pub fn cover_tao_region_prefiltered(region: VectorBox, max_depth: u32) -> CoverCertificate {
    let (exact, fast) = tao_seed_enclosed();
    let report = cover_region_prefiltered(&exact, &fast, region, max_depth);
    report.certificate("tao_seed_I_F6_S6_prefiltered_region")
}

/// Run complete finite cover of the standard narrow torus cell for Tao seed.
pub fn cover_tao_narrow_cell(max_depth: u32) -> CoverCertificate {
    cover_tao_region(narrow_torus_cell(), max_depth)
}

/// Run complete finite cover of the standard wide torus cell for Tao seed.
pub fn cover_tao_wide_cell(max_depth: u32) -> CoverCertificate {
    cover_tao_region_prefiltered(wide_torus_cell(), max_depth)
}

/// Single-chunk unit of the full gauge-fixed 5-torus under the Tao seed triple.
pub fn tao_gauge_fixed_chunk_cover(
    presplit_depth: u32,
    chunk_index: usize,
    max_depth: u32,
) -> CoverCertificate {
    let chunks = presplit_region(gauge_fixed_torus_region(), presplit_depth);
    assert!(
        chunk_index < chunks.len(),
        "chunk_index {chunk_index} out of range (n={})",
        chunks.len()
    );
    let (exact, fast) = tao_seed_enclosed();
    let report = cover_region_prefiltered(&exact, &fast, chunks[chunk_index].clone(), max_depth);
    report.certificate(&format!(
        "tao_seed_I_F6_S6_presplit{presplit_depth}_chunk{chunk_index}_depth{max_depth}"
    ))
}

/// Parallel full gauge-fixed 5-torus cover against the Tao seed triple.
pub fn tao_gauge_fixed_cover_parallel(
    presplit_depth: u32,
    max_depth: u32,
    n_threads: usize,
) -> CoverCertificate {
    let (exact, fast) = tao_seed_enclosed();
    let label = "tao_seed_I_F6_S6";
    let report = run_cover_parallel_with(
        &exact,
        &fast,
        gauge_fixed_torus_region(),
        presplit_depth,
        max_depth,
        label,
        n_threads,
    );
    report.certificate(&format!(
        "tao_seed_I_F6_S6_gauge_fixed_5_torus_presplit{presplit_depth}_depth{max_depth}"
    ))
}

// ---------------------------------------------------------------------------
// Scaled Multi-Box Reflection Complex Schema for Lane V1d & Independent Verifiers
// ---------------------------------------------------------------------------

/// A single certified box record with exact rational bounds.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BoxRecord {
    pub index: usize,
    pub num: String,
    pub den: String,
    pub gap: String,
}

/// Metadata describing the multi-box complex geometry and coverage.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ComplexMetadata {
    pub region_label: String,
    pub box_count: usize,
    pub contiguous: bool,
    pub partition_of: String,
    pub presplit_depth: u32,
    pub certified: usize,
    pub off_torus: usize,
    pub uncertified: usize,
    pub complete: bool,
    pub min_gap: String,
    pub max_depth_used: u32,
}

/// Scaled kernel reflection multi-box certificate artifact matching
/// schema version `omega.mub.kernel-reflection-scaled.v1`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KernelReflectionScaledArtifact {
    pub schema_version: String,
    pub seed: (i64, i64),
    pub seed_name: String,
    pub authority_effect: String,
    pub region: String,
    pub complex: ComplexMetadata,
    pub cover: CoverCertificate,
    pub lean_consume_target: String,
    pub held_out_claim: String,
    pub firewall: String,
    pub boxes: Vec<BoxRecord>,
}

/// Build the scaled kernel reflection complex on `narrow_torus_cell()` at `presplit_depth`.
///
/// Evaluates every leaf box in exact rational interval arithmetic over Cyc24.
/// Asserts that every leaf box satisfies `gap > 0`.
pub fn build_kernel_reflection_tao_s6_complex(
    presplit_depth: u32,
) -> KernelReflectionScaledArtifact {
    let (exact, _) = tao_seed_enclosed();
    let parent_region = narrow_torus_cell();
    let boxes = presplit_region(parent_region, presplit_depth);
    let box_count = boxes.len();
    let mut records = Vec::with_capacity(box_count);
    let mut min_gap: Option<BigRational> = None;

    for (index, vbox) in boxes.iter().enumerate() {
        let gap = exact.residual_sq_lower(vbox);
        assert!(
            gap > BigRational::zero(),
            "Certification failure: box {index} has non-positive gap {gap}"
        );
        if let Some(ref cur_min) = min_gap {
            if &gap < cur_min {
                min_gap = Some(gap.clone());
            }
        } else {
            min_gap = Some(gap.clone());
        }
        records.push(BoxRecord {
            index,
            num: gap.numer().to_string(),
            den: gap.denom().to_string(),
            gap: format!("{}/{}", gap.numer(), gap.denom()),
        });
    }

    let min_gap_rat = min_gap.expect("boxes non-empty");
    let min_gap_str = format!("{}/{}", min_gap_rat.numer(), min_gap_rat.denom());

    let region_label = format!("tao_seed_I_F6_S6_narrow_cell_presplit{presplit_depth}_complex");

    let complex = ComplexMetadata {
        region_label: region_label.clone(),
        box_count,
        contiguous: true,
        partition_of: "narrow_torus_cell".to_string(),
        presplit_depth,
        certified: box_count,
        off_torus: 0,
        uncertified: 0,
        complete: true,
        min_gap: min_gap_str.clone(),
        max_depth_used: 0,
    };

    let cover = CoverCertificate {
        region_label,
        certified: box_count,
        off_torus: 0,
        uncertified: 0,
        complete: true,
        min_gap: Some(min_gap_str),
        max_depth_used: 0,
    };

    KernelReflectionScaledArtifact {
        schema_version: "omega.mub.kernel-reflection-scaled.v1".to_string(),
        seed: (0, 0),
        seed_name: "tao_s6".to_string(),
        authority_effect: "None".to_string(),
        region: format!("narrow_torus_cell_{box_count}_box_presplit{presplit_depth}_complex (stated region; not full 5-torus)"),
        complex,
        cover,
        lean_consume_target: "MUB.FiniteVectorCover.no_mu_vector_in_cover / MUB.KernelReflectionTaoHaagerup".to_string(),
        held_out_claim: "complete stated-region cover of the narrow torus cell against the Tao S6 seed triple {I, F6, S6}; min_gap > 0 is the exact positivity witness for every leaf in that region".to_string(),
        firewall: "AuthorityEffect: None; stated region only; not full 5-torus reflection; mints no authority".to_string(),
        boxes: records,
    }
}

/// Write the certified Tao S6 kernel reflection JSON artifact under `artifacts/`.
pub fn write_kernel_reflection_tao_s6_artifact(presplit_depth: u32) -> Result<PathBuf, String> {
    let artifact = build_kernel_reflection_tao_s6_complex(presplit_depth);
    if !artifact.complex.complete || artifact.complex.uncertified != 0 {
        return Err(format!(
            "refusing incomplete artifact: complete={} uncertified={}",
            artifact.complex.complete, artifact.complex.uncertified
        ));
    }
    let dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("kernel_reflection_tao_s6_box_cover.json");
    let json = serde_json::to_string_pretty(&artifact).map_err(|e| format!("serde: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tao_s6_columns_orthonormal_and_mu_to_standard() {
        let cols = tao_s6_columns();
        assert_eq!(cols.len(), D);
        let one = Cyc24::rat(ri(1));
        let sixth = Cyc24::rat(ri(1) / ri(6));

        for j in 0..D {
            // Check norm 1
            let mut norm_sq = Cyc24::zero();
            for k in 0..D {
                norm_sq = norm_sq.add(&cols[j][k].mul(&cols[j][k].conj()));
            }
            assert_eq!(norm_sq, one, "Column {j} must have norm 1");

            // Check orthogonal to other columns
            for k in (j + 1)..D {
                let mut ip = Cyc24::zero();
                for r in 0..D {
                    ip = ip.add(&cols[j][r].conj().mul(&cols[k][r]));
                }
                assert_eq!(ip, Cyc24::zero(), "Columns {j} and {k} must be orthogonal");
            }

            // Check mutually unbiased to standard basis
            for r in 0..D {
                let entry_mod_sq = cols[j][r].mul(&cols[j][r].conj());
                assert_eq!(
                    entry_mod_sq, sixth,
                    "Entry ({r}, {j}) squared modulus must be exactly 1/6"
                );
            }
        }
    }

    #[test]
    fn test_tao_seed_triple_smoke_check() {
        let (excluded, gap) = tao_seed_smoke_check();
        assert!(excluded, "Tao seed smoke box must be strictly excluded");
        assert!(gap.is_some());
    }

    #[test]
    fn test_tao_narrow_cell_cover_complete() {
        let cert = cover_tao_narrow_cell(24);
        assert!(cert.complete, "Narrow cell cover must be complete");
        assert_eq!(cert.uncertified, 0, "No uncertified cells allowed");
        assert!(cert.min_gap.is_some(), "Must report exact rational min_gap");
    }

    #[test]
    fn test_tao_scaled_reflection_complex_64_boxes() {
        let complex = build_kernel_reflection_tao_s6_complex(6);
        assert_eq!(complex.complex.box_count, 64);
        assert_eq!(complex.boxes.len(), 64);
        assert!(complex.complex.complete);
        assert_eq!(complex.complex.uncertified, 0);
        for b in &complex.boxes {
            let num: num_bigint::BigInt = b.num.parse().unwrap();
            let den: num_bigint::BigInt = b.den.parse().unwrap();
            assert!(num > num_bigint::BigInt::zero());
            assert!(den > num_bigint::BigInt::zero());
        }
    }
}
