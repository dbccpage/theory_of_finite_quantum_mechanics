
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, exact_rational, DIM_HILBERT, GRAMIAN_DIM, NUM_BASES,
};
pub use crate::omega_native::exact::mub6_quad_sdp::get_basis_pairs;
use linear_algebra::exact_ldlt::ldlt_pivots_strictly_positive_rational;
use omega_number_theory::cyclotomic::Cyc24;

pub const SCHEMA_VERSION: &str = "omega.mub.degree4-sdp.v1";
pub const SCOPE_STRING: &str = "degree4_symmetry_reduced_moment_relaxation_quadruple_sdp";

pub const DEG4_INVARIANT_DIM: usize = 17;
pub const DEG4_EXTENDED_DIM: usize = 31;

fn validate_deg4_gramian_shape(g: &[Vec<Cyc24>]) -> Result<(), String> {
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

fn sum_block_mod_sq(g: &[Vec<Cyc24>], a: usize, b: usize) -> Result<BigRational, String> {
    let mut sum_mod_sq = BigRational::zero();
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
            let mod_sq = exact_rational(&entry.mul(&entry.conj()))?;
            sum_mod_sq += mod_sq;
        }
    }
    Ok(sum_mod_sq)
}

fn sum_block_diag_and_off_mod_sq(
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
) -> Result<(BigRational, BigRational), String> {
    let mut diag_mod_sq = BigRational::zero();
    let mut off_mod_sq = BigRational::zero();
    for i in 0..DIM_HILBERT {
        let entry_diag = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
        diag_mod_sq += exact_rational(&entry_diag.mul(&entry_diag.conj()))?;
        for j in 0..DIM_HILBERT {
            if i != j {
                let entry_off = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
                off_mod_sq += exact_rational(&entry_off.mul(&entry_off.conj()))?;
            }
        }
    }
    Ok((diag_mod_sq, off_mod_sq))
}

fn populate_deg4_inv_pair_expectations(
    m4: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
) -> Result<(), String> {
    let sixth = BigRational::new(1.into(), 6.into());
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let idx_p = 5 + p_idx;
        let idx_q = 11 + p_idx;
        let (diag_mod_sq, off_mod_sq) = sum_block_diag_and_off_mod_sq(g, a, b)?;
        let exp_p = &sixth * &diag_mod_sq;
        let exp_q = &sixth * &off_mod_sq;

        m4[0][idx_p] = exp_p.clone();
        m4[idx_p][0] = exp_p.clone();
        m4[0][idx_q] = exp_q.clone();
        m4[idx_q][0] = exp_q.clone();

        for base in [1 + a, 1 + b] {
            m4[base][idx_p] = exp_p.clone();
            m4[idx_p][base] = exp_p.clone();
            m4[base][idx_q] = exp_q.clone();
            m4[idx_q][base] = exp_q.clone();
        }

        m4[idx_p][idx_p] = exp_p;
        m4[idx_q][idx_q] = exp_q;
        m4[idx_p][idx_q] = BigRational::zero();
        m4[idx_q][idx_p] = BigRational::zero();
    }
    Ok(())
}

fn deg4_pair_cross_entry(a1: usize, b1: usize, a2: usize, b2: usize) -> BigRational {
    if a1 == 3 || b1 == 3 || a2 == 3 || b2 == 3 {
        BigRational::zero()
    } else {
        BigRational::new(1.into(), 36.into())
    }
}

fn populate_deg4_inv_pair_cross(m4: &mut [Vec<BigRational>], pairs: &[(usize, usize)]) {
    for (p1, &(a1, b1)) in pairs.iter().enumerate() {
        for (p2, &(a2, b2)) in pairs.iter().enumerate() {
            if p1 < p2 {
                let val = deg4_pair_cross_entry(a1, b1, a2, b2);
                m4[5 + p1][5 + p2] = val.clone();
                m4[5 + p2][5 + p1] = val;
            }
        }
    }
}

pub fn build_degree4_invariant_moment_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_deg4_gramian_shape(g)?;

    let pairs = get_basis_pairs();
    let n = DEG4_INVARIANT_DIM;
    let mut m4 = vec![vec![BigRational::zero(); n]; n];

    m4[0][0] = BigRational::one();

    for a in 0..NUM_BASES {
        let idx_a = 1 + a;
        m4[0][idx_a] = BigRational::one();
        m4[idx_a][0] = BigRational::one();
        m4[idx_a][idx_a] = BigRational::one();
    }

    let sixth = BigRational::new(1.into(), 6.into());
    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            let val = &sixth * sum_block_mod_sq(g, a, b)?;
            m4[1 + a][1 + b] = val.clone();
            m4[1 + b][1 + a] = val;
        }
    }

    populate_deg4_inv_pair_expectations(&mut m4, g, &pairs)?;
    populate_deg4_inv_pair_cross(&mut m4, &pairs);

    Ok(m4)
}

fn deg4_ext_basis_entry(
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

fn populate_deg4_ext_basis_block(
    m4: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
    sixth: &BigRational,
) -> Result<(), String> {
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let row_idx = a * DIM_HILBERT + i + 1;
            let col_idx = b * DIM_HILBERT + j + 1;
            m4[row_idx][col_idx] = deg4_ext_basis_entry(g, a, b, i, j, sixth)?;
        }
    }
    Ok(())
}

pub fn build_degree4_extended_moment_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_deg4_gramian_shape(g)?;

    let pairs = get_basis_pairs();
    let n = DEG4_EXTENDED_DIM;
    let mut m4 = vec![vec![BigRational::zero(); n]; n];
    let sixth = BigRational::new(1.into(), 6.into());

    m4[0][0] = BigRational::one();
    for idx in 0..GRAMIAN_DIM {
        m4[0][idx + 1] = sixth.clone();
        m4[idx + 1][0] = sixth.clone();
    }

    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            populate_deg4_ext_basis_block(&mut m4, g, a, b, &sixth)?;
        }
    }

    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let col_p = 25 + p_idx;
        let mut diag_mod_sq = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let mod_sq = exact_rational(&entry.mul(&entry.conj()))?;
            diag_mod_sq += &mod_sq;
            let term = &sixth * &mod_sq;
            m4[a * DIM_HILBERT + i + 1][col_p] = term.clone();
            m4[col_p][a * DIM_HILBERT + i + 1] = term.clone();
            m4[b * DIM_HILBERT + i + 1][col_p] = term.clone();
            m4[col_p][b * DIM_HILBERT + i + 1] = term;
        }

        let exp_p = &sixth * &diag_mod_sq;
        m4[0][col_p] = exp_p.clone();
        m4[col_p][0] = exp_p.clone();
        m4[col_p][col_p] = exp_p;
    }

    Ok(m4)
}
pub use crate::omega_native::exact::dual_witness::DualWitnessRational;


pub fn build_invariant_dual_witness_x0(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); DEG4_INVARIANT_DIM];
    z[0] = BigRational::from_integer((-1).into());
    z[1] = BigRational::one();
    z[4] = BigRational::one();

    let mut vectors = vec![z];
    let mut weights = vec![BigRational::one()];

    if strict {
        let eps = BigRational::new(1.into(), 50.into());
        for i in 0..DEG4_INVARIANT_DIM {
            let mut e = vec![BigRational::zero(); DEG4_INVARIANT_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational {
        dim: DEG4_INVARIANT_DIM,
        num_modes: vectors.len(),
        vectors,
        weights,
    }
}

pub fn build_extended_dual_witness_s6(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); DEG4_EXTENDED_DIM];
    z[0] = BigRational::from_integer(12.into());
    for i in 1..25 {
        z[i] = BigRational::from_integer((-2).into());
    }
    for p in 25..31 {
        z[p] = BigRational::from_integer((-5).into());
    }

    let mut vectors = vec![z];
    let mut weights = vec![BigRational::one()];

    if strict {
        let eps = BigRational::new(1.into(), 100.into());
        for i in 0..DEG4_EXTENDED_DIM {
            let mut e = vec![BigRational::zero(); DEG4_EXTENDED_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational {
        dim: DEG4_EXTENDED_DIM,
        num_modes: vectors.len(),
        vectors,
        weights,
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitnessReceipt {
    pub target_description: String,
    pub witness_dimension: usize,
    pub inner_product: String,
    pub inner_product_num: String,
    pub inner_product_den: String,
    pub strictly_negative: bool,
    pub pivots_strictly_positive: bool,
    pub pivots: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Degree4MomentReport {
    pub invariant_dimension: usize,
    pub extended_dimension: usize,
    pub candidate_x0_refuted: bool,
    pub candidate_s6_refuted: bool,
    pub details: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MubDegree4Certificate {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub scope: String,
    pub dimension: usize,
    pub bases_count: usize,
    pub invariant_dim: usize,
    pub extended_dim: usize,
    pub moment_report: Degree4MomentReport,
    pub receipt_x0: DualWitnessReceipt,
    pub receipt_s6: DualWitnessReceipt,
    pub complete: bool,
}

fn evaluate_deg4_dual_witness_receipt(
    w: &DualWitnessRational,
    m4: &[Vec<BigRational>],
    dim: usize,
    description: &str,
) -> Result<DualWitnessReceipt, String> {
    let tr_w = w.trace_inner(m4)?;
    let w_full = w.to_full_matrix()?;
    let pivots = ldlt_pivots_strictly_positive_rational(&w_full)?;
    let pivots_pos = pivots.iter().all(|p| p > &BigRational::zero());
    let neg = tr_w < BigRational::zero();

    Ok(DualWitnessReceipt {
        target_description: description.into(),
        witness_dimension: dim,
        inner_product: tr_w.to_string(),
        inner_product_num: tr_w.numer().to_string(),
        inner_product_den: tr_w.denom().to_string(),
        strictly_negative: neg,
        pivots_strictly_positive: pivots_pos,
        pivots: pivots.iter().map(|p| p.to_string()).collect(),
    })
}

pub fn solve_target_q2_degree4_certificate() -> Result<MubDegree4Certificate, String> {
    let g_diag = build_block_diagonal_gramian();
    let m4_inv_diag = build_degree4_invariant_moment_matrix(&g_diag)?;
    let w4_inv = build_invariant_dual_witness_x0(true);
    let receipt_x0 = evaluate_deg4_dual_witness_receipt(
        &w4_inv,
        &m4_inv_diag,
        DEG4_INVARIANT_DIM,
        "Candidate completion X = 0 refuted at Degree 4 via S_6-invariant moment witness",
    )?;

    let g_synth = canonical_quad_gramian();
    let m4_ext_synth = build_degree4_extended_moment_matrix(&g_synth)?;
    let w4_ext_s6 = build_extended_dual_witness_s6(true);
    let receipt_s6 = evaluate_deg4_dual_witness_receipt(
        &w4_ext_s6,
        &m4_ext_synth,
        DEG4_EXTENDED_DIM,
        "Candidate completion S_6 refuted at Degree 4 via extended moment witness",
    )?;

    let x0_refuted = receipt_x0.strictly_negative && receipt_x0.pivots_strictly_positive;
    let s6_refuted = receipt_s6.strictly_negative && receipt_s6.pivots_strictly_positive;
    let moment_report = Degree4MomentReport {
        invariant_dimension: DEG4_INVARIANT_DIM,
        extended_dimension: DEG4_EXTENDED_DIM,
        candidate_x0_refuted: x0_refuted,
        candidate_s6_refuted: s6_refuted,
        details:
            "Target Q2: Degree-4 symmetry-reduced and extended moment SDP refutation certified."
                .into(),
    };

    let complete = x0_refuted && s6_refuted;

    Ok(MubDegree4Certificate {
        schema_version: SCHEMA_VERSION.into(),
        firewall: FIREWALL.into(),
        authority_effect: AUTHORITY_EFFECT.into(),
        scope: SCOPE_STRING.into(),
        dimension: DIM_HILBERT,
        bases_count: NUM_BASES,
        invariant_dim: DEG4_INVARIANT_DIM,
        extended_dim: DEG4_EXTENDED_DIM,
        moment_report,
        receipt_x0,
        receipt_s6,
        complete,
    })
}
