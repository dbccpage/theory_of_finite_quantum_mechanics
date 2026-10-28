
use num_rational::BigRational;
use num_traits::{ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::native::exact::mub6_basis_cover::BasisBox;
use crate::native::exact::mub6_cover::EnclosedTriple;
use crate::native::exact::mub6_cover_run::{
    cover_region_prefiltered, gauge_fixed_torus_region, presplit_region, run_cover_parallel_with,
    CoverCertificate, EnclosedTripleF64,
};
use crate::native::campaign::mub6_dita_seed_cover::{narrow_torus_cell, wide_torus_cell};
use crate::native::exact::mub6_f6_chart::f6_family_columns;
use crate::native::campaign::mub6_f6_external_b3::basis_is_exact_chm;
use crate::native::exact::mub6_interval_cover::VectorBox;
use crate::native::exact::mub6_matrix6::Matrix6;
use crate::native::exact::szollosi_triad_solver::{szollosi_dephased_b6, verify_chm};
use omega_kernel::interval::Interval;
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

pub use crate::native::exact::mub6_field::inv_sqrt6;

pub fn haagerup_h6_basepoint_point0() -> Matrix6 {
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(6);
    let e = Cyc24::zeta24(0);
    let f = Cyc24::zeta24(12);
    szollosi_dephased_b6(&b, &c, &e, &f)
        .expect("Szollosi deltoid condition z1 + z2 == 0 holds for point 0")
}

pub fn haagerup_h6_basepoint_point3() -> Matrix6 {
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(8);
    let e = Cyc24::zeta24(0);
    let f = Cyc24::zeta24(16);
    szollosi_dephased_b6(&b, &c, &e, &f)
        .expect("Szollosi deltoid condition z1 + z2 == 0 holds for point 3")
}

pub fn haagerup_h6_matrix() -> Matrix6 {
    haagerup_h6_basepoint_point0()
}

pub fn haagerup_columns_from_matrix(m: &Matrix6) -> [ExactVec; D] {
    let s = inv_sqrt6();
    std::array::from_fn(|col| {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        for row in 0..D {
            v[row] = m[row][col].mul(&s);
        }
        v
    })
}

pub fn haagerup_h6_columns() -> [ExactVec; D] {
    haagerup_columns_from_matrix(&haagerup_h6_matrix())
}

pub fn haagerup_h6_is_exact_chm() -> bool {
    let m = haagerup_h6_matrix();
    let rep = verify_chm(&m);
    if !rep.is_chm {
        return false;
    }
    let cols = haagerup_h6_columns();
    basis_is_exact_chm(&cols)
}

pub fn standard_basis_columns() -> [ExactVec; D] {
    std::array::from_fn(|idx| {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[idx] = Cyc24::rat(ri(1));
        v
    })
}

pub fn haagerup_seed_triple_columns() -> Vec<ExactVec> {
    let mut cols = Vec::with_capacity(3 * D);
    cols.extend_from_slice(&standard_basis_columns());
    cols.extend_from_slice(&f6_family_columns(0, 0));
    cols.extend_from_slice(&haagerup_h6_columns());
    cols
}

pub fn haagerup_seed_triple_columns_with_matrix(h: &Matrix6) -> Vec<ExactVec> {
    let mut cols = Vec::with_capacity(3 * D);
    cols.extend_from_slice(&standard_basis_columns());
    cols.extend_from_slice(&f6_family_columns(0, 0));
    cols.extend_from_slice(&haagerup_columns_from_matrix(h));
    cols
}

pub fn haagerup_seed_triple_bases_are_chm() -> bool {
    let cols = haagerup_seed_triple_columns();
    let _b1: [ExactVec; D] = std::array::from_fn(|i| cols[i].clone());
    let b2: [ExactVec; D] = std::array::from_fn(|i| cols[D + i].clone());
    let b3: [ExactVec; D] = std::array::from_fn(|i| cols[2 * D + i].clone());
    basis_is_exact_chm(&b2) && basis_is_exact_chm(&b3)
}

pub fn haagerup_seed_enclosed() -> (EnclosedTriple, EnclosedTripleF64) {
    let cols = haagerup_seed_triple_columns();
    (
        EnclosedTriple::from_exact_columns(&cols),
        EnclosedTripleF64::from_exact_columns(&cols),
    )
}

pub fn haagerup_seed_neighborhood_enclosed(
    delta: &BigRational,
) -> (EnclosedTriple, EnclosedTripleF64) {
    let cols = haagerup_seed_triple_columns();
    let delta_f = delta.to_f64().unwrap_or(0.0);
    (
        EnclosedTriple::widened_from_exact_columns(&cols, delta),
        EnclosedTripleF64::widened_from_exact_columns(&cols, delta_f),
    )
}

pub fn neighborhood_delta_1_1000() -> BigRational {
    ri(1) / ri(1000)
}

pub fn cover_haagerup_region(region: VectorBox, max_depth: u32) -> CoverCertificate {
    let (exact, fast) = haagerup_seed_enclosed();
    let report = cover_region_prefiltered(&exact, &fast, region, max_depth);
    report.certificate("haagerup_h6_seed_prefiltered_region")
}

pub fn cover_haagerup_neighborhood_region(
    delta: &BigRational,
    region: VectorBox,
    max_depth: u32,
) -> CoverCertificate {
    let (exact, fast) = haagerup_seed_neighborhood_enclosed(delta);
    let report = cover_region_prefiltered(&exact, &fast, region, max_depth);
    report.certificate(&format!(
        "haagerup_h6_neigh_delta_{delta}_prefiltered_region"
    ))
}

pub fn cover_haagerup_narrow_cell() -> CoverCertificate {
    cover_haagerup_region(narrow_torus_cell(), 24)
}

pub fn cover_haagerup_wide_cell() -> CoverCertificate {
    cover_haagerup_region(wide_torus_cell(), 30)
}

pub fn cover_haagerup_gauge_fixed_chunk(
    presplit_depth: u32,
    chunk_index: usize,
    max_depth: u32,
) -> CoverCertificate {
    let chunks = presplit_region(gauge_fixed_torus_region(), presplit_depth);
    assert!(
        chunk_index < chunks.len(),
        "chunk_index {chunk_index} out of range (total chunks = {})",
        chunks.len()
    );
    let (exact, fast) = haagerup_seed_enclosed();
    let report = cover_region_prefiltered(&exact, &fast, chunks[chunk_index].clone(), max_depth);
    report.certificate(&format!(
        "haagerup_h6_presplit{presplit_depth}_chunk{chunk_index}_depth{max_depth}"
    ))
}

pub fn cover_haagerup_gauge_fixed_cover_parallel(
    presplit_depth: u32,
    max_depth: u32,
    n_threads: usize,
) -> CoverCertificate {
    let (exact, fast) = haagerup_seed_enclosed();
    let label = "haagerup_h6_gauge_fixed_5_torus".to_string();
    let report = run_cover_parallel_with(
        &exact,
        &fast,
        gauge_fixed_torus_region(),
        presplit_depth,
        max_depth,
        &label,
        n_threads,
    );
    report.certificate(&label)
}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScaledBoxRecord {
    pub index: usize,
    pub num: String,
    pub den: String,
    pub gap: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScaledComplexMeta {
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

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScaledBoxComplexArtifact {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub seed: Vec<usize>,
    pub seed_label: String,
    pub region: String,
    pub complex: ScaledComplexMeta,
    pub boxes: Vec<ScaledBoxRecord>,
}

pub fn generate_haagerup_scaled_box_complex(presplit_depth: u32) -> ScaledBoxComplexArtifact {
    let (enclosed, _) = haagerup_seed_enclosed();
    let boxes_regions = presplit_region(narrow_torus_cell(), presplit_depth);
    let box_count = boxes_regions.len();

    let mut records = Vec::with_capacity(box_count);
    let mut min_gap_opt: Option<BigRational> = None;
    let mut certified_count = 0;

    for (idx, vbox) in boxes_regions.into_iter().enumerate() {
        let gap = enclosed.residual_sq_lower(&vbox);
        assert!(
            gap > BigRational::zero(),
            "Box {idx} must have strictly positive curvature lower bound; got {gap}"
        );
        certified_count += 1;
        if let Some(ref current_min) = min_gap_opt {
            if &gap < current_min {
                min_gap_opt = Some(gap.clone());
            }
        } else {
            min_gap_opt = Some(gap.clone());
        }

        let num = gap.numer().to_string();
        let den = gap.denom().to_string();
        let gap_str = format!("{num}/{den}");
        records.push(ScaledBoxRecord {
            index: idx,
            num,
            den,
            gap: gap_str,
        });
    }

    let min_gap_val = min_gap_opt.expect("at least one box");
    let min_gap_str = format!("{}/{}", min_gap_val.numer(), min_gap_val.denom());

    ScaledBoxComplexArtifact {
        schema_version: "omega.mub.kernel-reflection-scaled.v1".to_string(),
        authority_effect: "None".to_string(),
        firewall: "stated region only; mints no authority".to_string(),
        seed: vec![0, 6, 0, 12],
        seed_label: "haagerup_h6_szollosi_b6_point0".to_string(),
        region: "narrow_torus_cell_64_box_presplit6_complex (stated region; not full 5-torus)"
            .to_string(),
        complex: ScaledComplexMeta {
            region_label: "haagerup_h6_narrow_cell_presplit6_complex".to_string(),
            box_count,
            contiguous: true,
            partition_of: "narrow_torus_cell".to_string(),
            presplit_depth,
            certified: certified_count,
            off_torus: 0,
            uncertified: 0,
            complete: true,
            min_gap: min_gap_str,
            max_depth_used: 0,
        },
        boxes: records,
    }
}

pub fn write_haagerup_reflection_artifact(path: &std::path::Path) -> Result<(), String> {
    let artifact = generate_haagerup_scaled_box_complex(6);
    let json = serde_json::to_string_pretty(&artifact)
        .map_err(|e| format!("Failed to serialize artifact: {e}"))?;
    std::fs::write(path, json).map_err(|e| format!("Failed to write artifact to {path:?}: {e}"))
}


fn smoke_basis_box_col0_near_e0() -> BasisBox {
    let small = Interval::new(ri(-1) / ri(20), ri(1) / ri(20));
    let mut near_e0: VectorBox = std::array::from_fn(|_| small.clone());
    near_e0[0] = Interval::new(ri(9) / ri(10), ri(1) / ri(1));
    near_e0[1] = small;
    let wide = Interval::new(ri(-1) / ri(1), ri(1) / ri(1));
    let wide_col: VectorBox = std::array::from_fn(|_| wide.clone());
    let mut bbox: BasisBox = std::array::from_fn(|_| wide_col.clone());
    bbox[0] = near_e0;
    bbox
}

pub fn haagerup_seed_smoke_vector_gap() -> BigRational {
    let cols = haagerup_seed_triple_columns();
    let enclosed = EnclosedTriple::from_exact_columns(&cols);
    let bbox = smoke_basis_box_col0_near_e0();
    enclosed.residual_sq_lower(&bbox[0])
}

#[derive(Debug, Clone, Serialize)]
pub struct HaagerupCoverStatus {
    pub matrix_name: &'static str,
    pub basepoint_indices: (usize, usize, usize, usize),
    pub is_exact_chm: bool,
    pub triple_is_pairwise_chm: bool,
    pub column_count: usize,
    pub smoke_vector_excluded: bool,
    pub smoke_vector_gap: String,
    pub firewall: &'static str,
}

pub fn haagerup_cover_status() -> HaagerupCoverStatus {
    let is_exact_chm = haagerup_h6_is_exact_chm();
    let triple_is_pairwise_chm = haagerup_seed_triple_bases_are_chm();
    let vgap = haagerup_seed_smoke_vector_gap();
    let smoke_vector_excluded = vgap > BigRational::zero();

    HaagerupCoverStatus {
        matrix_name: "Haagerup_H6_Szollosi_Point0",
        basepoint_indices: (0, 6, 0, 12),
        is_exact_chm,
        triple_is_pairwise_chm,
        column_count: 3 * D,
        smoke_vector_excluded,
        smoke_vector_gap: vgap.to_string(),
        firewall:
            "exact cyclotomic Cyc24 arithmetic; stated region only; mints no authority",
    }
}
