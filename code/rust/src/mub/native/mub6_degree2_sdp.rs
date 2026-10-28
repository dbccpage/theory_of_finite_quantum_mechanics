
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, inner};
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, dual_certificate_matrix, exact_rational, ldlt_pivots_rational,
    trace_inner_product,
};
pub use crate::native::exact::mub6_quad_sdp::{DIM_HILBERT, GRAMIAN_DIM, NUM_BASES};
use linear_algebra::exact_ldlt::ldlt_pivots_strictly_positive_rational;
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

pub const SCHEMA_VERSION: &str = "omega.mub.degree2-sdp.v1";
pub const SCOPE_STRING: &str = "degree2_moment_relaxation_quadruple_sdp";
pub const MOMENT_DIM: usize = 1 + GRAMIAN_DIM;


fn push_submatrix_cols_for_row_pair(
    r0: usize,
    r1: usize,
    d: usize,
    submatrices: &mut Vec<(usize, usize, usize, usize)>,
) {
    for c0 in 0..d {
        for c1 in (c0 + 1)..d {
            submatrices.push((r0, r1, c0, c1));
        }
    }
}

pub fn enumerate_225_submatrices(d: usize) -> Vec<(usize, usize, usize, usize)> {
    let mut submatrices = Vec::with_capacity(225);
    for r0 in 0..d {
        for r1 in (r0 + 1)..d {
            push_submatrix_cols_for_row_pair(r0, r1, d, &mut submatrices);
        }
    }
    submatrices
}

pub fn cross_ratio_at(m: &[Vec<Cyc24>], r0: usize, r1: usize, c0: usize, c1: usize) -> Cyc24 {
    let a = &m[r0][c0];
    let b = &m[r0][c1];
    let c = &m[r1][c0];
    let d = &m[r1][c1];
    a.mul(d).mul(&b.conj()).mul(&c.conj())
}

pub fn evaluate_block_cross_ratios(m: &[Vec<Cyc24>]) -> Vec<Cyc24> {
    let submatrices = enumerate_225_submatrices(DIM_HILBERT);
    submatrices
        .into_iter()
        .map(|(r0, r1, c0, c1)| cross_ratio_at(m, r0, r1, c0, c1))
        .collect()
}

pub fn extract_block_from_gramian(
    g: &[Vec<Cyc24>],
    basis_a: usize,
    basis_b: usize,
) -> Vec<Vec<Cyc24>> {
    let mut block = vec![vec![Cyc24::zero(); DIM_HILBERT]; DIM_HILBERT];
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            block[i][j] = g[basis_a * DIM_HILBERT + i][basis_b * DIM_HILBERT + j].clone();
        }
    }
    block
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct PairwiseCrossRatioSummary {
    pub basis_a: usize,
    pub basis_b: usize,
    pub total_submatrices: usize,
    pub all_modulus_thirty_sixth: bool,
    pub all_normalized_modulus_one: bool,
    pub violations_count: usize,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CrossRatioVerificationReport {
    pub total_pairs: usize,
    pub total_cross_ratios_evaluated: usize,
    pub all_pairs_sound: bool,
    pub pair_summaries: Vec<PairwiseCrossRatioSummary>,
}

fn summarize_pair_cross_ratios(
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
    one_thirty_sixth_sq: &BigRational,
) -> PairwiseCrossRatioSummary {
    let block = extract_block_from_gramian(g, a, b);
    let crs = evaluate_block_cross_ratios(&block);
    let mut mod_ok = true;
    let mut violations = 0;

    for cr in &crs {
        let mod_sq_cyc = cr.mul(&cr.conj());
        let mod_sq = match exact_rational(&mod_sq_cyc) {
            Ok(r) => r,
            Err(_) => BigRational::from_integer((-1).into()),
        };
        if &mod_sq != one_thirty_sixth_sq {
            mod_ok = false;
            violations += 1;
        }
    }

    PairwiseCrossRatioSummary {
        basis_a: a,
        basis_b: b,
        total_submatrices: crs.len(),
        all_modulus_thirty_sixth: mod_ok,
        all_normalized_modulus_one: mod_ok,
        violations_count: violations,
    }
}

pub fn verify_pairwise_cross_ratios(g: &[Vec<Cyc24>]) -> CrossRatioVerificationReport {
    let one_thirty_sixth_sq = BigRational::new(1.into(), 1296.into());
    let mut pair_summaries = Vec::new();
    let mut total_evaluated = 0;
    let mut all_sound = true;

    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            let summary = summarize_pair_cross_ratios(g, a, b, &one_thirty_sixth_sq);
            total_evaluated += summary.total_submatrices;
            if !summary.all_modulus_thirty_sixth {
                all_sound = false;
            }
            pair_summaries.push(summary);
        }
    }

    CrossRatioVerificationReport {
        total_pairs: pair_summaries.len(),
        total_cross_ratios_evaluated: total_evaluated,
        all_pairs_sound: all_sound,
        pair_summaries,
    }
}

fn validate_gramian_shape(g: &[Vec<Cyc24>]) -> Result<(), String> {
    if g.len() != GRAMIAN_DIM {
        return Err(format!(
            "Gramian dimension must be {}x{}",
            GRAMIAN_DIM, GRAMIAN_DIM
        ));
    }
    for row in g {
        if row.len() != GRAMIAN_DIM {
            return Err(format!(
                "Gramian dimension must be {}x{}",
                GRAMIAN_DIM, GRAMIAN_DIM
            ));
        }
    }
    Ok(())
}

fn m2_basis_pair_entry(
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
    i: usize,
    j: usize,
    sixth: &BigRational,
) -> Result<BigRational, String> {
    if a == b {
        Ok(if i == j {
            sixth.clone()
        } else {
            BigRational::zero()
        })
    } else {
        let g_entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
        let mod_sq = exact_rational(&g_entry.mul(&g_entry.conj()))?;
        Ok(sixth * mod_sq)
    }
}

fn populate_m2_basis_pair_block(
    m2: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
    sixth: &BigRational,
) -> Result<(), String> {
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let row_idx = a * DIM_HILBERT + i + 1;
            let col_idx = b * DIM_HILBERT + j + 1;
            m2[row_idx][col_idx] = m2_basis_pair_entry(g, a, b, i, j, sixth)?;
        }
    }
    Ok(())
}

pub fn build_degree2_projector_moment_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_gramian_shape(g)?;

    let sixth = BigRational::new(1.into(), 6.into());
    let mut m2 = vec![vec![BigRational::zero(); MOMENT_DIM]; MOMENT_DIM];

    m2[0][0] = BigRational::one();
    for idx in 0..GRAMIAN_DIM {
        m2[0][idx + 1] = sixth.clone();
        m2[idx + 1][0] = sixth.clone();
    }

    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            populate_m2_basis_pair_block(&mut m2, g, a, b, &sixth)?;
        }
    }

    Ok(m2)
}
pub use crate::native::exact::dual_witness::DualWitnessRational;


pub fn build_block_diag_dual_witness(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); MOMENT_DIM];
    z[0] = BigRational::from_integer((-2).into());
    z[1] = BigRational::one();
    let two = BigRational::from_integer(2.into());
    for j in 0..DIM_HILBERT {
        z[3 * DIM_HILBERT + j + 1] = two.clone();
    }

    let mut vectors = vec![z];
    let mut weights = vec![BigRational::one()];

    if strict {
        let eps = BigRational::new(1.into(), 100.into());
        for i in 0..MOMENT_DIM {
            let mut e = vec![BigRational::zero(); MOMENT_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational {
        dim: MOMENT_DIM,
        num_modes: vectors.len(),
        vectors,
        weights,
    }
}

fn populate_gramian_pair_block(
    g: &mut [Vec<Cyc24>],
    cols: &[[Cyc24; 6]],
    a: usize,
    b: usize,
) {
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let u = &cols[a * DIM_HILBERT + i];
            let v = &cols[b * DIM_HILBERT + j];
            g[a * DIM_HILBERT + i][b * DIM_HILBERT + j] = inner(u, v);
        }
    }
}

pub fn build_block_diagonal_gramian() -> Vec<Vec<Cyc24>> {
    let cols = canonical_triple_exact();
    let mut g = vec![vec![Cyc24::zero(); GRAMIAN_DIM]; GRAMIAN_DIM];

    for a in 0..3 {
        for b in 0..3 {
            populate_gramian_pair_block(&mut g, &cols, a, b);
        }
    }

    let one = Cyc24::rat(ri(1));
    for j in 0..DIM_HILBERT {
        g[3 * DIM_HILBERT + j][3 * DIM_HILBERT + j] = one.clone();
    }

    g
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitnessReceipt {
    pub target_description: &'static str,
    pub witness_dimension: usize,
    pub inner_product: String,
    pub inner_product_num: String,
    pub inner_product_den: String,
    pub strictly_negative: bool,
    pub pivots_strictly_positive: bool,
    pub pivots: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Degree2MomentReport {
    pub moment_dimension: usize,
    pub affine_completeness_holds: bool,
    pub modulus_squared_matches_sixth: bool,
    pub candidate_x0_refuted_by_dual_witness: bool,
    pub details: &'static str,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MubDegree2Certificate {
    pub schema_version: &'static str,
    pub firewall: &'static str,
    pub authority_effect: &'static str,
    pub scope: &'static str,
    pub dimension: usize,
    pub bases_count: usize,
    pub gramian_dim: usize,
    pub moment_dim: usize,
    pub cross_ratio_report: CrossRatioVerificationReport,
    pub moment_report: Degree2MomentReport,
    pub receipt_violating_modulus_x0: DualWitnessReceipt,
    pub receipt_violating_psd_s6: DualWitnessReceipt,
    pub complete: bool,
}

pub fn solve_target_q1_degree2_certificate() -> MubDegree2Certificate {
    let g_diag = build_block_diagonal_gramian();
    let m2_diag =
        build_degree2_projector_moment_matrix(&g_diag).expect("M_2(G_diag) construction failed");

    let w2_strict = build_block_diag_dual_witness(true);
    let tr_w2 = w2_strict
        .trace_inner(&m2_diag)
        .expect("trace inner product failed");
    let w2_full = w2_strict.to_full_matrix().expect("canonical witness shape");
    let w2_pivots = ldlt_pivots_strictly_positive_rational(&w2_full)
        .expect("LDL^T decomposition failed for W_2");
    let w2_pivots_pos = w2_pivots.iter().all(|p| p > &BigRational::zero());
    let w2_neg = tr_w2 < BigRational::zero();

    let receipt_x0 = DualWitnessReceipt {
        target_description: "Candidate completion X = 0 (violating modulus |G_{ab}|^2 = 1/6)",
        witness_dimension: MOMENT_DIM,
        inner_product: tr_w2.to_string(),
        inner_product_num: tr_w2.numer().to_string(),
        inner_product_den: tr_w2.denom().to_string(),
        strictly_negative: w2_neg,
        pivots_strictly_positive: w2_pivots_pos,
        pivots: w2_pivots.iter().map(|p| p.to_string()).collect(),
    };

    let g_synth = canonical_quad_gramian();
    let w_gram_strict = dual_certificate_matrix(true);
    let inner_synth = trace_inner_product(&w_gram_strict, &g_synth);
    let rat_synth = exact_rational(&inner_synth).expect("trace must be rational");
    let gram_pivots = ldlt_pivots_rational(&w_gram_strict).expect("LDL^T failed for W_gram");
    let gram_pivots_pos = gram_pivots.iter().all(|p| p > &BigRational::zero());
    let gram_neg = rat_synth < BigRational::zero();

    let receipt_s6 = DualWitnessReceipt {
        target_description: "Candidate completion S_6 (satisfying modulus, violating PSD)",
        witness_dimension: GRAMIAN_DIM,
        inner_product: rat_synth.to_string(),
        inner_product_num: rat_synth.numer().to_string(),
        inner_product_den: rat_synth.denom().to_string(),
        strictly_negative: gram_neg,
        pivots_strictly_positive: gram_pivots_pos,
        pivots: gram_pivots.iter().map(|p| p.to_string()).collect(),
    };

    let cr_report_synth = verify_pairwise_cross_ratios(&g_synth);

    let moment_report = Degree2MomentReport {
        moment_dimension: MOMENT_DIM,
        affine_completeness_holds: false,
        modulus_squared_matches_sixth: false,
        candidate_x0_refuted_by_dual_witness: w2_neg && w2_pivots_pos,
        details: "Linear degree-1 completion X = 0 refuted at Degree 2 via strictly positive dual witness.",
    };

    let complete = receipt_x0.strictly_negative
        && receipt_x0.pivots_strictly_positive
        && receipt_s6.strictly_negative
        && receipt_s6.pivots_strictly_positive
        && cr_report_synth.all_pairs_sound;

    MubDegree2Certificate {
        schema_version: SCHEMA_VERSION,
        firewall: FIREWALL,
        authority_effect: AUTHORITY_EFFECT,
        scope: SCOPE_STRING,
        dimension: DIM_HILBERT,
        bases_count: NUM_BASES,
        gramian_dim: GRAMIAN_DIM,
        moment_dim: MOMENT_DIM,
        cross_ratio_report: cr_report_synth,
        moment_report,
        receipt_violating_modulus_x0: receipt_x0,
        receipt_violating_psd_s6: receipt_s6,
        complete,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_moment_matrix_dimensions_and_baseline_entries() {
        let g_diag = build_block_diagonal_gramian();
        let m2 = build_degree2_projector_moment_matrix(&g_diag).expect("M_2(G_diag) build failed");

        assert_eq!(m2.len(), MOMENT_DIM);
        assert_eq!(m2[0].len(), MOMENT_DIM);

        assert_eq!(m2[0][0], BigRational::one());
        let sixth = BigRational::new(1.into(), 6.into());
        for i in 1..MOMENT_DIM {
            assert_eq!(m2[0][i], sixth);
            assert_eq!(m2[i][0], sixth);
            assert_eq!(m2[i][i], sixth);
        }
    }

    #[test]
    fn test_block_diagonal_dual_witness_strictly_negative() {
        let g_diag = build_block_diagonal_gramian();
        let m2_diag = build_degree2_projector_moment_matrix(&g_diag).expect("M_2 build failed");

        let w2_rank1 = build_block_diag_dual_witness(false);
        assert!(w2_rank1.is_valid());
        let tr_rank1 = w2_rank1.trace_inner(&m2_diag).expect("trace failed");
        assert_eq!(tr_rank1, BigRational::new((-1).into(), 2.into()));

        let w2_strict = build_block_diag_dual_witness(true);
        assert!(w2_strict.is_valid());
        let tr_strict = w2_strict.trace_inner(&m2_diag).expect("trace failed");
        assert_eq!(tr_strict, BigRational::new((-9).into(), 20.into()));
    }

    #[test]
    fn test_strict_dual_witness_all_pivots_positive() {
        let w2_strict = build_block_diag_dual_witness(true);
        let w_mat = w2_strict.to_full_matrix().expect("canonical witness shape");
        let pivots = ldlt_pivots_strictly_positive_rational(&w_mat)
            .expect("strict witness must factorize with positive pivots");
        assert_eq!(pivots.len(), MOMENT_DIM);
        assert!(pivots.iter().all(|p| p > &BigRational::zero()));
    }

    #[test]
    fn test_certificate_solver_complete() {
        let cert = solve_target_q1_degree2_certificate();
        assert!(cert.complete);
        assert_eq!(cert.schema_version, SCHEMA_VERSION);
        assert_eq!(cert.firewall, FIREWALL);
        assert_eq!(cert.authority_effect, AUTHORITY_EFFECT);
        assert!(cert.receipt_violating_modulus_x0.strictly_negative);
        assert!(cert.receipt_violating_modulus_x0.pivots_strictly_positive);
        assert!(cert.receipt_violating_psd_s6.strictly_negative);
        assert!(cert.receipt_violating_psd_s6.pivots_strictly_positive);
        assert!(cert.cross_ratio_report.all_pairs_sound);
    }
}
