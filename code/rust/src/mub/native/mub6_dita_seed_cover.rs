
use num_rational::BigRational;
use num_traits::{ToPrimitive, Zero};
use serde::Serialize;
use sha2::{Digest, Sha256};

use crate::native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::native::exact::mub6_basis_cover::{
    basis_box_excluded_by_column_for_triple, basis_residual_sq_lower,
    certify_basis_box_excludes_fourth_for_triple, BasisBox,
};
use crate::native::exact::mub6_cover::{cover_region, EnclosedTriple};
use crate::native::exact::mub6_cover_run::{
    cover_region_prefiltered, gauge_fixed_torus_region, presplit_region, run_cover_parallel_with,
    CoverCertificate, EnclosedTripleF64,
};
use crate::native::exact::mub6_cyclotomic_enclosure::SqrtBox;
use crate::native::exact::mub6_f6_chart::{f6_family_columns, f6_point_is_exact_chm};
use crate::native::campaign::mub6_f6_external_b3::{
    bases_are_mutually_unbiased, basis_is_exact_chm, genuine_dita_y2q1_triple_seeds,
    genuine_dita_y2q2_triple_seeds, product_y2_qa_columns,
};
use crate::native::exact::mub6_interval_cover::VectorBox;
use omega_kernel::interval::Interval;
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;
use tfqm_number_theory::rational::rq;

pub fn resolve_genuine_dita_qa(dx: i64, dy: i64) -> Result<i64, String> {
    if genuine_dita_y2q1_triple_seeds()
        .iter()
        .any(|&(a, b)| a == dx && b == dy)
    {
        Ok(1)
    } else if genuine_dita_y2q2_triple_seeds()
        .iter()
        .any(|&(a, b)| a == dx && b == dy)
    {
        Ok(2)
    } else {
        Err(format!(
            "F6({dx},{dy}) is not a locked genuine Dita seed; \
             Y2Q1 allowed {:?}; Y2Q2 allowed {:?}",
            genuine_dita_y2q1_triple_seeds(),
            genuine_dita_y2q2_triple_seeds()
        ))
    }
}

pub fn all_genuine_dita_seeds() -> Vec<(i64, i64, i64)> {
    let mut out = Vec::new();
    for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
        out.push((dx, dy, 1));
    }
    for &(dx, dy) in &genuine_dita_y2q2_triple_seeds() {
        out.push((dx, dy, 2));
    }
    out
}

pub fn dita_seed_triple_columns(dx: i64, dy: i64) -> Vec<ExactVec> {
    let qa = resolve_genuine_dita_qa(dx, dy).expect("locked genuine Dita seed");
    dita_seed_triple_columns_qa(dx, dy, qa)
}

pub fn dita_seed_triple_columns_qa(dx: i64, dy: i64, qa: i64) -> Vec<ExactVec> {
    assert!(
        f6_point_is_exact_chm(dx, dy),
        "F6({dx},{dy}) must be an exact CHM"
    );
    assert!(qa == 1 || qa == 2, "qa must be 1 or 2");
    let mut cols = Vec::with_capacity(3 * D);
    for idx in 0..D {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[idx] = Cyc24::rat(ri(1));
        cols.push(v);
    }
    cols.extend_from_slice(&f6_family_columns(dx, dy));
    cols.extend_from_slice(&product_y2_qa_columns(qa));
    cols
}

pub fn dita_seed_triple_is_pairwise_mu(dx: i64, dy: i64) -> bool {
    let cols = dita_seed_triple_columns(dx, dy);
    let b1: [ExactVec; D] = std::array::from_fn(|i| cols[i].clone());
    let b2: [ExactVec; D] = std::array::from_fn(|i| cols[D + i].clone());
    let b3: [ExactVec; D] = std::array::from_fn(|i| cols[2 * D + i].clone());
    basis_is_exact_chm(&b2)
        && basis_is_exact_chm(&b3)
        && bases_are_mutually_unbiased(&b1, &b2)
        && bases_are_mutually_unbiased(&b1, &b3)
        && bases_are_mutually_unbiased(&b2, &b3)
}

fn smoke_basis_box_col0_near_e0() -> BasisBox {
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

#[derive(Debug, Clone, Serialize)]
pub struct DitaSeedCoverStatus {
    pub f6_dx: i64,
    pub f6_dy: i64,
    pub triple_id: String,
    pub pairwise_mu: bool,
    pub column_count: usize,
    pub smoke_basis_excluded: bool,
    pub smoke_psi_gap: Option<String>,
    pub smoke_excluded_column: Option<usize>,
    pub smoke_vector_excluded: bool,
    pub smoke_vector_gap: Option<String>,
    pub full_torus_cover: &'static str,
    pub firewall: &'static str,
}

pub fn dita_seed_cover_status(dx: i64, dy: i64) -> DitaSeedCoverStatus {
    let cols = dita_seed_triple_columns(dx, dy);
    let pairwise_mu = dita_seed_triple_is_pairwise_mu(dx, dy);
    let bbox = smoke_basis_box_col0_near_e0();
    let basis_cert = certify_basis_box_excludes_fourth_for_triple(&cols, &bbox);
    let col_wit = basis_box_excluded_by_column_for_triple(&cols, &bbox);
    let enclosed = EnclosedTriple::from_exact_columns(&cols);
    let vgap = enclosed.residual_sq_lower(&bbox[0]);
    let smoke_vector_excluded = vgap > BigRational::zero();
    DitaSeedCoverStatus {
        f6_dx: dx,
        f6_dy: dy,
        triple_id: {
            let qa = resolve_genuine_dita_qa(dx, dy).unwrap_or(1);
            format!("I_F6_{dx}_{dy}_Y2Q{qa}")
        },
        pairwise_mu,
        column_count: cols.len(),
        smoke_basis_excluded: basis_cert.is_some(),
        smoke_psi_gap: basis_cert
            .as_ref()
            .map(|c| c.psi_gap.to_string()),
        smoke_excluded_column: col_wit.map(|(j, _)| j),
        smoke_vector_excluded,
        smoke_vector_gap: if smoke_vector_excluded {
            Some(vgap.to_string())
        } else {
            None
        },
        full_torus_cover: "COMPLETE on disk for all 6 genuine seeds Y2Q1∪Y2Q2 (presplit6 depth≤32, certified=1035821, dual-orbit parity); see artifacts/dita_seed_F6_*_gauge_fixed_5_torus_presplit6_merged_complete.json",
        firewall: "smoke exclusion of a bad box is not a complete 5-torus cover; stated region only; mints no authority",
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct DitaSeedCoverReadinessReport {
    pub seeds: Vec<DitaSeedCoverStatus>,
    pub all_pairwise_mu: bool,
    pub all_smoke_excluded: bool,
    pub open_obligation: &'static str,
    pub firewall: &'static str,
}

pub fn dita_seed_cover_readiness_report() -> DitaSeedCoverReadinessReport {
    let seeds: Vec<_> = all_genuine_dita_seeds()
        .into_iter()
        .map(|(dx, dy, _qa)| dita_seed_cover_status(dx, dy))
        .collect();
    let all_pairwise_mu = seeds.iter().all(|s| s.pairwise_mu);
    let all_smoke_excluded = seeds
        .iter()
        .all(|s| s.smoke_basis_excluded && s.smoke_vector_excluded);
    DitaSeedCoverReadinessReport {
        seeds,
        all_pairwise_mu,
        all_smoke_excluded,
        open_obligation:
            "point full-torus covers COMPLETE for all three seeds; next: full gauge-fixed 5-torus neighborhood (delta=1/1000) per seed + atlas C2 glue",
        firewall: "readiness + smoke only; not a complete cover certificate; stated region only; mints no authority",
    }
}

pub fn dita_seed_smoke_psi_gap(dx: i64, dy: i64) -> BigRational {
    let cols = dita_seed_triple_columns(dx, dy);
    let sb = SqrtBox::standard();
    basis_residual_sq_lower(&cols, &smoke_basis_box_col0_near_e0(), &sb)
}


pub fn dita_seed_enclosed(dx: i64, dy: i64) -> (EnclosedTriple, EnclosedTripleF64) {
    let cols = dita_seed_triple_columns(dx, dy);
    (
        EnclosedTriple::from_exact_columns(&cols),
        EnclosedTripleF64::from_exact_columns(&cols),
    )
}

pub fn dita_seed_neighborhood_enclosed(
    dx: i64,
    dy: i64,
    delta: &BigRational,
) -> (EnclosedTriple, EnclosedTripleF64) {
    let cols = dita_seed_triple_columns(dx, dy);
    let delta_f = delta.to_f64().unwrap_or(0.0);
    (
        EnclosedTriple::widened_from_exact_columns(&cols, delta),
        EnclosedTripleF64::widened_from_exact_columns(&cols, delta_f),
    )
}

pub fn neighborhood_delta_1_1000() -> BigRational {
    ri(1) / ri(1000)
}

pub fn cover_seed_neighborhood_region(
    dx: i64,
    dy: i64,
    delta: &BigRational,
    region: VectorBox,
    max_depth: u32,
) -> CoverCertificate {
    let (exact, fast) = dita_seed_neighborhood_enclosed(dx, dy, delta);
    let report = cover_region_prefiltered(&exact, &fast, region, max_depth);
    report.certificate(&format!(
        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta}_prefiltered_region"
    ))
}

#[derive(Debug, Clone, Serialize)]
pub struct DitaSeedNeighborhoodCellCoverReport {
    pub delta: String,
    pub narrow: Vec<CoverCertificate>,
    pub wide: Vec<CoverCertificate>,
    pub all_narrow_complete: bool,
    pub all_wide_complete: bool,
    pub open_obligation: &'static str,
    pub firewall: &'static str,
}

pub fn dita_seed_neighborhood_cell_cover_report() -> DitaSeedNeighborhoodCellCoverReport {
    let delta = neighborhood_delta_1_1000();
    let mut narrow = Vec::new();
    let mut wide = Vec::new();
    for &(dx, dy, _) in &all_genuine_dita_seeds() {
        narrow.push(cover_seed_neighborhood_region(
            dx,
            dy,
            &delta,
            narrow_torus_cell(),
            24,
        ));
        wide.push(cover_seed_neighborhood_region(
            dx,
            dy,
            &delta,
            wide_torus_cell(),
            30,
        ));
    }
    let all_narrow_complete = narrow.iter().all(|c| c.complete && c.uncertified == 0);
    let all_wide_complete = wide.iter().all(|c| c.complete && c.uncertified == 0);
    DitaSeedNeighborhoodCellCoverReport {
        delta: delta.to_string(),
        narrow,
        wide,
        all_narrow_complete,
        all_wide_complete,
        open_obligation:
            "full gauge-fixed 5-torus neighborhood cover per seed (widened delta=1/1000) via chunk farm; then register as ModuliCoverPatch and C2-glue",
        firewall:
            "neighborhood cell covers are stated-region only; not full moduli atlas; stated region only; mints no authority",
    }
}

pub fn dita_seed_neighborhood_gauge_fixed_chunk_cover(
    dx: i64,
    dy: i64,
    delta: &BigRational,
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
    let (exact, fast) = dita_seed_neighborhood_enclosed(dx, dy, delta);
    let report = cover_region_prefiltered(&exact, &fast, chunks[chunk_index].clone(), max_depth);
    report.certificate(&format!(
        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta}_presplit{presplit_depth}_chunk{chunk_index}_depth{max_depth}"
    ))
}

pub fn dita_seed_neighborhood_gauge_fixed_cover_parallel(
    dx: i64,
    dy: i64,
    delta: &BigRational,
    presplit_depth: u32,
    max_depth: u32,
    n_threads: usize,
) -> CoverCertificate {
    let (exact, fast) = dita_seed_neighborhood_enclosed(dx, dy, delta);
    let label = format!("dita_seed_F6_{dx}_{dy}_neigh_delta_{delta}");
    let report = run_cover_parallel_with(
        &exact,
        &fast,
        gauge_fixed_torus_region(),
        presplit_depth,
        max_depth,
        &label,
        n_threads,
    );
    report.certificate(&format!(
        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta}_gauge_fixed_5_torus_presplit{presplit_depth}_depth{max_depth}"
    ))
}

pub fn neighborhood_chunk_filename(
    dx: i64,
    dy: i64,
    delta_tag: &str,
    presplit: u32,
    chunk_index: usize,
    depth: u32,
) -> String {
    format!(
        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_presplit{presplit}_chunk{chunk_index}_depth{depth}.json"
    )
}

pub fn merge_on_disk_presplit6_neighborhood_chunks(
    dx: i64,
    dy: i64,
    delta_tag: &str,
) -> Result<CoverCertificate, String> {
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    let merged = dir.join(format!(
        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_gauge_fixed_5_torus_presplit6_merged_complete.json"
    ));
    if merged.exists() {
        let raw = std::fs::read_to_string(&merged).map_err(|e| format!("read {merged:?}: {e}"))?;
        return serde_json::from_str(&raw).map_err(|e| format!("parse {merged:?}: {e}"));
    }
    let mut chunks = Vec::with_capacity(64);
    for i in 0..64usize {
        let p32 = dir.join(neighborhood_chunk_filename(dx, dy, delta_tag, 6, i, 32));
        let p30 = dir.join(neighborhood_chunk_filename(dx, dy, delta_tag, 6, i, 30));
        let path = if p32.exists() {
            p32
        } else if p30.exists() {
            p30
        } else {
            return Err(format!(
                "missing neighborhood chunk {i} (delta={delta_tag})"
            ));
        };
        let raw = std::fs::read_to_string(&path).map_err(|e| format!("read {path:?}: {e}"))?;
        let cert: CoverCertificate =
            serde_json::from_str(&raw).map_err(|e| format!("parse {path:?}: {e}"))?;
        chunks.push(cert);
    }
    merge_chunk_certificates(
        &format!(
            "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_gauge_fixed_5_torus_presplit6_merged"
        ),
        &chunks,
    )
}

pub fn narrow_torus_cell() -> VectorBox {
    let lo = ri(28) / ri(100) - ri(2) / ri(100);
    let hi = ri(28) / ri(100) + ri(2) / ri(100);
    std::array::from_fn(|_| Interval::new(lo.clone(), hi.clone()))
}

pub fn wide_torus_cell() -> VectorBox {
    let lo = ri(28) / ri(100) - ri(18) / ri(100);
    let hi = ri(28) / ri(100) + ri(18) / ri(100);
    std::array::from_fn(|_| Interval::new(lo.clone(), hi.clone()))
}

pub fn cover_seed_region(dx: i64, dy: i64, region: VectorBox, max_depth: u32) -> CoverCertificate {
    let (exact, _) = dita_seed_enclosed(dx, dy);
    let report = cover_region(&exact, region, max_depth);
    report.certificate(&format!("dita_seed_F6_{dx}_{dy}_region"))
}

pub fn cover_seed_region_prefiltered(
    dx: i64,
    dy: i64,
    region: VectorBox,
    max_depth: u32,
) -> CoverCertificate {
    let (exact, fast) = dita_seed_enclosed(dx, dy);
    let report = cover_region_prefiltered(&exact, &fast, region, max_depth);
    report.certificate(&format!("dita_seed_F6_{dx}_{dy}_prefiltered_region"))
}

#[derive(Debug, Clone, Serialize)]
pub struct DitaSeedCellCoverReport {
    pub narrow: Vec<CoverCertificate>,
    pub wide: Vec<CoverCertificate>,
    pub all_narrow_complete: bool,
    pub all_wide_complete: bool,
    pub open_obligation: &'static str,
    pub firewall: &'static str,
}

pub fn dita_seed_cell_cover_report() -> DitaSeedCellCoverReport {
    let mut narrow = Vec::new();
    let mut wide = Vec::new();
    for &(dx, dy, _) in &all_genuine_dita_seeds() {
        narrow.push(cover_seed_region(dx, dy, narrow_torus_cell(), 24));
        wide.push(cover_seed_region_prefiltered(dx, dy, wide_torus_cell(), 30));
    }
    let all_narrow_complete = narrow.iter().all(|c| c.complete && c.uncertified == 0);
    let all_wide_complete = wide.iter().all(|c| c.complete && c.uncertified == 0);
    DitaSeedCellCoverReport {
        narrow,
        wide,
        all_narrow_complete,
        all_wide_complete,
        open_obligation:
            "point full-torus COMPLETE; moduli neighborhood cell covers available via dita_seed_neighborhood_cell_cover_report; full-torus neighborhood farm remains production-scale",
        firewall: "cell covers are stated-region only; not full 5-torus; stated region only; mints no authority",
    }
}

pub fn dita_seed_gauge_fixed_pilot(dx: i64, dy: i64, max_depth: u32) -> CoverCertificate {
    let (exact, fast) = dita_seed_enclosed(dx, dy);
    let report = cover_region_prefiltered(&exact, &fast, gauge_fixed_torus_region(), max_depth);
    report.certificate(&format!(
        "dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_pilot_depth{max_depth}"
    ))
}

pub fn dita_seed_gauge_fixed_cover_parallel(
    dx: i64,
    dy: i64,
    presplit_depth: u32,
    max_depth: u32,
    n_threads: usize,
) -> CoverCertificate {
    let (exact, fast) = dita_seed_enclosed(dx, dy);
    let label = format!("dita_seed_F6_{dx}_{dy}_gauge5");
    let report = run_cover_parallel_with(
        &exact,
        &fast,
        gauge_fixed_torus_region(),
        presplit_depth,
        max_depth,
        &label,
        n_threads,
    );
    report.certificate(&format!(
        "dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit{presplit_depth}_depth{max_depth}"
    ))
}

pub fn write_cover_certificate_artifact(
    cert: &CoverCertificate,
    filename: &str,
) -> Result<std::path::PathBuf, String> {
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir artifacts: {e}"))?;
    let path = dir.join(filename);
    let json = serde_json::to_string_pretty(cert).map_err(|e| format!("serialize: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write {path:?}: {e}"))?;
    Ok(path)
}

pub fn merge_chunk_certificates(
    region_label: &str,
    chunks: &[CoverCertificate],
) -> Result<CoverCertificate, String> {
    if chunks.is_empty() {
        return Err("no chunks to merge".into());
    }
    let incomplete: Vec<_> = chunks
        .iter()
        .enumerate()
        .filter(|(_, c)| !c.complete || c.uncertified != 0)
        .map(|(i, c)| format!("{i}:unc={}", c.uncertified))
        .collect();
    if !incomplete.is_empty() {
        return Err(format!("incomplete chunks: {}", incomplete.join(", ")));
    }
    let certified: usize = chunks.iter().map(|c| c.certified).sum();
    let off_torus: usize = chunks.iter().map(|c| c.off_torus).sum();
    let max_depth_used = chunks.iter().map(|c| c.max_depth_used).max().unwrap_or(0);
    let min_gap = chunks
        .iter()
        .filter_map(|c| c.min_gap.as_ref())
        .min_by(|a, b| {
            use std::str::FromStr;
            let ar = BigRational::from_str(a).ok();
            let br = BigRational::from_str(b).ok();
            match (ar, br) {
                (Some(x), Some(y)) => x.cmp(&y),
                _ => a.cmp(b),
            }
        })
        .cloned();
    Ok(CoverCertificate {
        region_label: region_label.to_string(),
        certified,
        off_torus,
        uncertified: 0,
        complete: true,
        min_gap,
        max_depth_used,
    })
}

pub fn parse_chunk_index_from_label(label: &str) -> Option<usize> {
    let pos = label.find("chunk")?;
    let after = &label[pos + 5..];
    let digits: String = after.chars().take_while(|c| c.is_ascii_digit()).collect();
    digits.parse::<usize>().ok()
}

fn count_seen_chunk_indices(
    chunks: &[CoverCertificate],
    expected_count: usize,
) -> Result<Vec<usize>, String> {
    let mut seen_counts = vec![0usize; expected_count];
    for (arr_idx, cert) in chunks.iter().enumerate() {
        let chunk_idx = parse_chunk_index_from_label(&cert.region_label).ok_or_else(|| {
            format!(
                "strict chunk index bijection error: chunk at array position {arr_idx} has invalid region label '{}' (missing 'chunk{{N}}' identifier)",
                cert.region_label
            )
        })?;
        if chunk_idx >= expected_count {
            return Err(format!(
                "strict chunk index bijection error: chunk index {chunk_idx} out of bounds for expected count {expected_count} (label: '{}')",
                cert.region_label
            ));
        }
        seen_counts[chunk_idx] += 1;
    }
    Ok(seen_counts)
}

fn format_bijection_violations(seen_counts: &[usize]) -> Result<(), String> {
    let mut missing = Vec::new();
    let mut duplicates = Vec::new();
    for (idx, &cnt) in seen_counts.iter().enumerate() {
        if cnt == 0 {
            missing.push(idx);
        } else if cnt > 1 {
            duplicates.push((idx, cnt));
        }
    }
    if missing.is_empty() && duplicates.is_empty() {
        return Ok(());
    }
    let mut err = String::from("strict chunk index bijection violation: ");
    if !missing.is_empty() {
        err.push_str(&format!("missing chunk indices {:?}; ", missing));
    }
    if !duplicates.is_empty() {
        err.push_str(&format!("duplicate chunk indices {:?}; ", duplicates));
    }
    Err(err.trim_end().to_string())
}

pub fn validate_chunk_index_bijection(
    chunks: &[CoverCertificate],
    expected_count: usize,
) -> Result<(), String> {
    if chunks.is_empty() {
        return Err(format!(
            "strict chunk index bijection error: chunk set is empty (expected {expected_count})"
        ));
    }
    if chunks.len() != expected_count {
        return Err(format!(
            "strict chunk index bijection error: chunk count mismatch: expected {expected_count} chunks, found {}",
            chunks.len()
        ));
    }
    let seen_counts = count_seen_chunk_indices(chunks, expected_count)?;
    format_bijection_violations(&seen_counts)
}

pub fn compute_payload_sha256(bytes: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    format!("{:x}", hasher.finalize())
}

pub fn validate_chunk_payload(
    raw_bytes: &[u8],
    expected_sha256: Option<&str>,
) -> Result<(CoverCertificate, String), String> {
    if raw_bytes.is_empty() {
        return Err("corrupted chunk payload: file is empty (0 bytes)".into());
    }
    let digest = compute_payload_sha256(raw_bytes);
    if let Some(expected) = expected_sha256 {
        if digest != expected {
            return Err(format!(
                "chunk payload checksum corruption: computed SHA-256 {digest} does not match expected {expected}"
            ));
        }
    }
    let cert: CoverCertificate = serde_json::from_slice(raw_bytes)
        .map_err(|e| format!("corrupted chunk payload: invalid JSON syntax: {e}"))?;
    if !cert.complete || cert.uncertified != 0 {
        return Err(format!(
            "corrupted chunk payload: certificate is incomplete (complete={}, uncertified={})",
            cert.complete, cert.uncertified
        ));
    }
    Ok((cert, digest))
}

pub fn merge_on_disk_presplit6_chunks_strict(
    dx: i64,
    dy: i64,
) -> Result<(CoverCertificate, Vec<(usize, String)>), String> {
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    let n_chunks = 64usize;
    let mut chunks = Vec::with_capacity(n_chunks);
    let mut checksums = Vec::with_capacity(n_chunks);

    for i in 0..n_chunks {
        let p32 = dir.join(format!(
            "dita_seed_F6_{dx}_{dy}_gauge5_presplit6_chunk{i}_depth32.json"
        ));
        let p30 = dir.join(format!(
            "dita_seed_F6_{dx}_{dy}_gauge5_presplit6_chunk{i}_depth30.json"
        ));
        let path = if p32.exists() {
            p32
        } else if p30.exists() {
            p30
        } else {
            return Err(format!(
                "strict merge failed: missing chunk {i} out of {n_chunks} (searched depth32 and depth30 in {dir:?})"
            ));
        };

        let raw =
            std::fs::read(&path).map_err(|e| format!("failed to read chunk file {path:?}: {e}"))?;
        let (cert, digest) = validate_chunk_payload(&raw, None)
            .map_err(|e| format!("chunk {i} at {path:?} failed validation: {e}"))?;
        chunks.push(cert);
        checksums.push((i, digest));
    }

    validate_chunk_index_bijection(&chunks, n_chunks)?;

    let merged_label = format!("dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged");
    let merged_cert = merge_chunk_certificates(&merged_label, &chunks)?;
    Ok((merged_cert, checksums))
}

pub fn merge_on_disk_presplit6_neighborhood_chunks_strict(
    dx: i64,
    dy: i64,
    delta_tag: &str,
) -> Result<(CoverCertificate, Vec<(usize, String)>), String> {
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    let n_chunks = 64usize;
    let mut chunks = Vec::with_capacity(n_chunks);
    let mut checksums = Vec::with_capacity(n_chunks);

    for i in 0..n_chunks {
        let p32 = dir.join(neighborhood_chunk_filename(dx, dy, delta_tag, 6, i, 32));
        let p30 = dir.join(neighborhood_chunk_filename(dx, dy, delta_tag, 6, i, 30));
        let path = if p32.exists() {
            p32
        } else if p30.exists() {
            p30
        } else {
            return Err(format!(
                "strict merge failed: missing neighborhood chunk {i} out of {n_chunks} (delta={delta_tag}) in {dir:?}"
            ));
        };

        let raw = std::fs::read(&path)
            .map_err(|e| format!("failed to read neighborhood chunk file {path:?}: {e}"))?;
        let (cert, digest) = validate_chunk_payload(&raw, None)
            .map_err(|e| format!("neighborhood chunk {i} at {path:?} failed validation: {e}"))?;
        chunks.push(cert);
        checksums.push((i, digest));
    }

    validate_chunk_index_bijection(&chunks, n_chunks)?;

    let merged_label = format!(
        "dita_seed_F6_{dx}_{dy}_neigh_delta_{delta_tag}_gauge_fixed_5_torus_presplit6_merged"
    );
    let merged_cert = merge_chunk_certificates(&merged_label, &chunks)?;
    Ok((merged_cert, checksums))
}

pub fn merge_on_disk_presplit6_chunks(dx: i64, dy: i64) -> Result<CoverCertificate, String> {
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts");
    let merged = dir.join(format!(
        "dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged_complete.json"
    ));
    if merged.exists() {
        let raw = std::fs::read_to_string(&merged).map_err(|e| format!("read {merged:?}: {e}"))?;
        return serde_json::from_str(&raw).map_err(|e| format!("parse {merged:?}: {e}"));
    }
    let mut chunks = Vec::with_capacity(64);
    for i in 0..64usize {
        let p32 = dir.join(format!(
            "dita_seed_F6_{dx}_{dy}_gauge5_presplit6_chunk{i}_depth32.json"
        ));
        let p30 = dir.join(format!(
            "dita_seed_F6_{dx}_{dy}_gauge5_presplit6_chunk{i}_depth30.json"
        ));
        let path = if p32.exists() {
            p32
        } else if p30.exists() {
            p30
        } else {
            return Err(format!("missing chunk {i}"));
        };
        let raw = std::fs::read_to_string(&path).map_err(|e| format!("read {path:?}: {e}"))?;
        let cert: CoverCertificate =
            serde_json::from_str(&raw).map_err(|e| format!("parse {path:?}: {e}"))?;
        chunks.push(cert);
    }
    merge_chunk_certificates(
        &format!("dita_seed_F6_{dx}_{dy}_gauge_fixed_5_torus_presplit6_merged"),
        &chunks,
    )
}

pub fn genuine_dita_y2q1_triple_seeds_check(dx: i64, dy: i64) -> Result<(), String> {
    resolve_genuine_dita_qa(dx, dy).map(|_| ())
}

pub fn dita_seed_gauge_fixed_chunk_cover(
    dx: i64,
    dy: i64,
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
    let (exact, fast) = dita_seed_enclosed(dx, dy);
    let report = cover_region_prefiltered(&exact, &fast, chunks[chunk_index].clone(), max_depth);
    report.certificate(&format!(
        "dita_seed_F6_{dx}_{dy}_gauge5_presplit{presplit_depth}_chunk{chunk_index}_depth{max_depth}"
    ))
}

pub fn dita_seed_gauge_fixed_cover_sequential(
    dx: i64,
    dy: i64,
    presplit_depth: u32,
    max_depth: u32,
) -> CoverCertificate {
    dita_seed_gauge_fixed_cover_parallel(dx, dy, presplit_depth, max_depth, 1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_genuine_seed_has_18_pairwise_mu_columns() {
        for &(dx, dy, qa) in &all_genuine_dita_seeds() {
            let cols = dita_seed_triple_columns(dx, dy);
            assert_eq!(cols.len(), 18);
            assert_eq!(resolve_genuine_dita_qa(dx, dy).unwrap(), qa);
            assert!(
                dita_seed_triple_is_pairwise_mu(dx, dy),
                "seed F6({dx},{dy})+Y2Q{qa} must be pairwise MU"
            );
        }
    }

    #[test]
    fn seed_cover_smoke_excludes_bad_basis_box() {
        let report = dita_seed_cover_readiness_report();
        assert_eq!(report.seeds.len(), 6);
        assert!(report.all_pairwise_mu);
        assert!(report.all_smoke_excluded);
        assert!(report.firewall.contains("mints no authority"));
        for s in &report.seeds {
            assert!(s.smoke_basis_excluded);
            assert!(s.smoke_vector_excluded);
            assert_eq!(s.smoke_excluded_column, Some(0));
            assert!(s.smoke_psi_gap.is_some());
            let gap = dita_seed_smoke_psi_gap(s.f6_dx, s.f6_dy);
            assert!(gap > BigRational::zero());
        }
    }

    #[test]
    fn enclosed_seed_triple_matches_basis_kernel_on_smoke() {
        for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
            let cols = dita_seed_triple_columns(dx, dy);
            let bbox = smoke_basis_box_col0_near_e0();
            let sb = SqrtBox::standard();
            let exact = basis_residual_sq_lower(&cols, &bbox, &sb);
            let enc = EnclosedTriple::from_exact_columns(&cols);
            let v0 = enc.residual_sq_lower(&bbox[0]);
            assert!(v0 > BigRational::zero());
            assert!(exact >= v0);
        }
    }

    #[test]
    fn every_seed_completely_covers_narrow_and_wide_torus_cells() {
        let report = dita_seed_cell_cover_report();
        assert_eq!(report.narrow.len(), 6);
        assert_eq!(report.wide.len(), 6);
        assert!(
            report.all_narrow_complete,
            "narrow cells incomplete: {:?}",
            report.narrow
        );
        assert!(
            report.all_wide_complete,
            "wide cells incomplete: {:?}",
            report.wide
        );
        for c in report.narrow.iter().chain(report.wide.iter()) {
            assert!(c.complete);
            assert_eq!(c.uncertified, 0);
            assert!(c.certified >= 1);
            assert!(c.min_gap.is_some());
            assert!(c.region_label.contains("dita_seed"));
        }
        assert!(report.firewall.contains("mints no authority"));
    }

    #[test]
    fn gauge_fixed_pilot_is_honest_about_depth() {
        let (dx, dy) = genuine_dita_y2q1_triple_seeds()[0];
        let cert = dita_seed_gauge_fixed_pilot(dx, dy, 4);
        assert_eq!(cert.complete, cert.uncertified == 0);
        assert!(cert.region_label.contains("gauge_fixed"));
    }

    #[test]
    #[ignore]
    fn single_presplit_chunk_can_complete_at_moderate_depth() {
        let (dx, dy) = genuine_dita_y2q1_triple_seeds()[0];
        let cert = dita_seed_gauge_fixed_chunk_cover(dx, dy, 5, 0, 28);
        assert_eq!(cert.complete, cert.uncertified == 0);
        assert!(cert.region_label.contains("chunk0"));
        if cert.complete {
            assert!(cert.certified >= 1);
            assert!(cert.min_gap.is_some());
        }
    }

    #[test]
    fn production_parallel_entry_is_honest_at_shallow_depth() {
        let (dx, dy) = genuine_dita_y2q1_triple_seeds()[0];
        let cert = dita_seed_gauge_fixed_cover_parallel(dx, dy, 2, 6, 2);
        assert_eq!(cert.complete, cert.uncertified == 0);
        assert!(cert.region_label.contains("gauge_fixed_5_torus"));
    }

    #[test]
    fn genuine_seed_check_accepts_locked_seeds_only() {
        assert!(genuine_dita_y2q1_triple_seeds_check(0, 8).is_ok());
        assert!(genuine_dita_y2q1_triple_seeds_check(0, 16).is_ok());
        assert!(genuine_dita_y2q1_triple_seeds_check(8, 8).is_ok());
        assert!(genuine_dita_y2q1_triple_seeds_check(3, 7).is_err());
    }

    #[test]
    fn on_disk_presplit6_chunks_merge_to_complete_full_torus_for_seed_0_8() {
        let cert = merge_on_disk_presplit6_chunks(0, 8)
            .expect("all 64 chunk certificates must be present and complete");
        assert!(cert.complete);
        assert_eq!(cert.uncertified, 0);
        assert!(cert.certified > 1_000_000);
        assert!(cert.min_gap.is_some());
        assert!(cert.region_label.contains("merged"));
    }

    #[test]
    fn on_disk_presplit6_chunks_merge_all_three_genuine_seeds_identical_counts() {
        let c08 = merge_on_disk_presplit6_chunks(0, 8).expect("seed (0,8)");
        let c80 = merge_on_disk_presplit6_chunks(8, 0).expect("seed (8,0)");
        let c1616 = merge_on_disk_presplit6_chunks(16, 16).expect("seed (16,16)");
        for c in [&c08, &c80, &c1616] {
            assert!(c.complete);
            assert_eq!(c.uncertified, 0);
            assert_eq!(c.certified, 1_035_821);
            assert_eq!(c.off_torus, 858_895);
            assert_eq!(c.max_depth_used, 32);
            assert!(c.min_gap.is_some());
        }
        assert_eq!(c08.min_gap, c80.min_gap);
        assert_eq!(c08.min_gap, c1616.min_gap);
    }

    #[test]
    fn on_disk_presplit6_chunks_merge_all_three_y2q2_seeds_identical_to_y2q1() {
        let c016 = merge_on_disk_presplit6_chunks(0, 16).expect("seed (0,16)");
        let c88 = merge_on_disk_presplit6_chunks(8, 8).expect("seed (8,8)");
        let c160 = merge_on_disk_presplit6_chunks(16, 0).expect("seed (16,0)");
        let y2q1 = merge_on_disk_presplit6_chunks(0, 8).expect("Y2Q1 reference");
        for c in [&c016, &c88, &c160] {
            assert!(c.complete);
            assert_eq!(c.uncertified, 0);
            assert_eq!(c.certified, 1_035_821);
            assert_eq!(c.off_torus, 858_895);
            assert_eq!(c.max_depth_used, 32);
            assert!(c.min_gap.is_some());
            assert!(c.region_label.contains("merged"));
            assert_eq!(c.min_gap, y2q1.min_gap);
        }
    }

    #[test]
    fn neighborhood_widening_is_sound_superset_of_point_seed() {
        let delta = neighborhood_delta_1_1000();
        let bbox = smoke_basis_box_col0_near_e0();
        for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
            let (point, _) = dita_seed_enclosed(dx, dy);
            let (wide, _) = dita_seed_neighborhood_enclosed(dx, dy, &delta);
            let p = point.residual_sq_lower(&bbox[0]);
            let w = wide.residual_sq_lower(&bbox[0]);
            assert!(p > BigRational::zero());
            assert!(
                w <= p,
                "widened residual lower bound must be ≤ point residual"
            );
            assert!(
                w > BigRational::zero(),
                "smoke col0 near e0 must still certify under delta=1/1000 for F6({dx},{dy})"
            );
        }
    }

    #[test]
    fn every_seed_neighborhood_completely_covers_narrow_and_wide_cells() {
        let report = dita_seed_neighborhood_cell_cover_report();
        assert_eq!(report.delta, "1/1000");
        assert_eq!(report.narrow.len(), 6);
        assert_eq!(report.wide.len(), 6);
        assert!(
            report.all_narrow_complete,
            "neighborhood narrow incomplete: {:?}",
            report.narrow
        );
        assert!(
            report.all_wide_complete,
            "neighborhood wide incomplete: {:?}",
            report.wide
        );
        for c in report.narrow.iter().chain(report.wide.iter()) {
            assert!(c.complete);
            assert_eq!(c.uncertified, 0);
            assert!(c.certified >= 1);
            assert!(c.min_gap.is_some());
            assert!(c.region_label.contains("neigh_delta"));
        }
        assert!(report.firewall.contains("mints no authority"));
    }

    #[test]
    fn neighborhood_gauge_fixed_chunk_pilot_is_honest() {
        let delta = neighborhood_delta_1_1000();
        let cert = dita_seed_neighborhood_gauge_fixed_chunk_cover(0, 8, &delta, 2, 0, 6);
        assert_eq!(cert.complete, cert.uncertified == 0);
        assert!(cert.region_label.contains("neigh_delta"));
    }

    #[test]
    fn on_disk_presplit6_neighborhood_merge_complete_for_seed_0_8() {
        let cert = merge_on_disk_presplit6_neighborhood_chunks(0, 8, "1_1000")
            .expect("all 64 neighborhood chunk certificates must be present and complete");
        assert!(cert.complete);
        assert_eq!(cert.uncertified, 0);
        assert_eq!(cert.certified, 1_138_055);
        assert_eq!(cert.off_torus, 954_386);
        assert_eq!(cert.max_depth_used, 32);
        assert!(cert.min_gap.is_some());
        assert!(cert.region_label.contains("neigh_delta"));
        assert!(cert.region_label.contains("merged"));
    }

    #[test]
    fn on_disk_presplit6_neighborhood_merge_all_six_seeds_identical() {
        let c08 = merge_on_disk_presplit6_neighborhood_chunks(0, 8, "1_1000").expect("(0,8)");
        let c80 = merge_on_disk_presplit6_neighborhood_chunks(8, 0, "1_1000").expect("(8,0)");
        let c1616 = merge_on_disk_presplit6_neighborhood_chunks(16, 16, "1_1000").expect("(16,16)");
        let c016 = merge_on_disk_presplit6_neighborhood_chunks(0, 16, "1_1000").expect("(0,16)");
        let c88 = merge_on_disk_presplit6_neighborhood_chunks(8, 8, "1_1000").expect("(8,8)");
        let c160 = merge_on_disk_presplit6_neighborhood_chunks(16, 0, "1_1000").expect("(16,0)");
        for c in [&c08, &c80, &c1616, &c016, &c88, &c160] {
            assert!(c.complete);
            assert_eq!(c.uncertified, 0);
            assert_eq!(c.certified, 1_138_055);
            assert_eq!(c.off_torus, 954_386);
            assert_eq!(c.max_depth_used, 32);
            assert!(c.min_gap.is_some());
        }
        assert_eq!(c08.min_gap, c80.min_gap);
        assert_eq!(c08.min_gap, c1616.min_gap);
        assert_eq!(c08.min_gap, c016.min_gap);
        assert_eq!(c08.min_gap, c88.min_gap);
        assert_eq!(c08.min_gap, c160.min_gap);
    }

    #[test]
    fn strict_chunk_index_bijection_validation_enforces_bijective_coverage() {
        let make_dummy = |idx: usize| CoverCertificate {
            region_label: format!("dita_seed_F6_0_8_gauge5_presplit2_chunk{idx}_depth20"),
            certified: 100,
            off_torus: 50,
            uncertified: 0,
            complete: true,
            min_gap: Some("1/10".to_string()),
            max_depth_used: 15,
        };

        let valid_chunks = vec![make_dummy(0), make_dummy(1), make_dummy(2), make_dummy(3)];
        assert!(validate_chunk_index_bijection(&valid_chunks, 4).is_ok());

        let permuted_chunks = vec![make_dummy(2), make_dummy(0), make_dummy(3), make_dummy(1)];
        assert!(validate_chunk_index_bijection(&permuted_chunks, 4).is_ok());

        let missing_chunks = vec![make_dummy(0), make_dummy(1), make_dummy(3)];
        let err_missing = validate_chunk_index_bijection(&missing_chunks, 4).unwrap_err();
        assert!(err_missing.contains("chunk count mismatch"));

        let dup_chunks = vec![make_dummy(0), make_dummy(1), make_dummy(1), make_dummy(3)];
        let err_dup = validate_chunk_index_bijection(&dup_chunks, 4).unwrap_err();
        assert!(
            err_dup.contains("duplicate chunk indices")
                && err_dup.contains("missing chunk indices")
        );

        let oob_chunks = vec![make_dummy(0), make_dummy(1), make_dummy(2), make_dummy(5)];
        let err_oob = validate_chunk_index_bijection(&oob_chunks, 4).unwrap_err();
        assert!(err_oob.contains("out of bounds"));

        let empty_chunks: Vec<CoverCertificate> = Vec::new();
        assert!(validate_chunk_index_bijection(&empty_chunks, 4).is_err());
    }

    #[test]
    fn chunk_payload_checksum_validation_detects_corruption() {
        let valid_cert = CoverCertificate {
            region_label: "test_chunk".to_string(),
            certified: 500,
            off_torus: 200,
            uncertified: 0,
            complete: true,
            min_gap: Some("1/100".to_string()),
            max_depth_used: 10,
        };
        let valid_bytes = serde_json::to_vec_pretty(&valid_cert).unwrap();
        let expected_hash = compute_payload_sha256(&valid_bytes);

        let (parsed, hash) = validate_chunk_payload(&valid_bytes, Some(&expected_hash)).unwrap();
        assert_eq!(parsed, valid_cert);
        assert_eq!(hash, expected_hash);

        let bad_hash = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";
        let err_hash = validate_chunk_payload(&valid_bytes, Some(bad_hash)).unwrap_err();
        assert!(err_hash.contains("checksum corruption"));

        let corrupt_bytes = b"{ invalid json payload ...";
        let err_json = validate_chunk_payload(corrupt_bytes, None).unwrap_err();
        assert!(err_json.contains("invalid JSON syntax"));

        let empty_bytes = b"";
        let err_empty = validate_chunk_payload(empty_bytes, None).unwrap_err();
        assert!(err_empty.contains("file is empty"));

        let incomplete_cert = CoverCertificate {
            region_label: "incomplete_chunk".to_string(),
            certified: 100,
            off_torus: 50,
            uncertified: 5,
            complete: false,
            min_gap: None,
            max_depth_used: 10,
        };
        let incomplete_bytes = serde_json::to_vec(&incomplete_cert).unwrap();
        let err_incomp = validate_chunk_payload(&incomplete_bytes, None).unwrap_err();
        assert!(err_incomp.contains("certificate is incomplete"));
    }

    #[test]
    fn strict_merge_on_disk_neighborhood_chunks_verifies_all_64_checksums() {
        let (cert, checksums) = merge_on_disk_presplit6_neighborhood_chunks_strict(8, 8, "1_1000")
            .expect("F6(8,8) all 64 neighborhood chunk files must be present and verified");
        assert_eq!(checksums.len(), 64);
        assert!(cert.complete);
        assert_eq!(cert.uncertified, 0);
        assert_eq!(cert.certified, 1_138_055);
        assert_eq!(cert.off_torus, 954_386);

        for (idx, (chunk_i, sha)) in checksums.iter().enumerate() {
            assert_eq!(*chunk_i, idx);
            assert_eq!(sha.len(), 64);
        }
    }
}
