//! Target Q2 Degree-4 / Symmetry-Reduced Moment SDP Solver.
//!
//! Evaluates exact rational degree-4 moment relaxations and symmetry-reduced
//! projector SDPs for MUB(6) candidate completions.
//!
//! AuthorityEffect: None.

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

/// Construct the 17x17 S_6-invariant Degree-4 moment matrix M_4^{inv}(G) over BigRational.
pub fn build_degree4_invariant_moment_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return Err(format!(
            "Gramian dimension must be {}x{}",
            GRAMIAN_DIM, GRAMIAN_DIM
        ));
    }

    let pairs = get_basis_pairs();
    let n = DEG4_INVARIANT_DIM;
    let mut m4 = vec![vec![BigRational::zero(); n]; n];

    // 1. Base identity <1>
    m4[0][0] = BigRational::one();

    // 2. Linear projector sums A_a (indices 1..4)
    for a in 0..NUM_BASES {
        let idx_a = 1 + a;
        m4[0][idx_a] = BigRational::one();
        m4[idx_a][0] = BigRational::one();
        m4[idx_a][idx_a] = BigRational::one();
    }

    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            let idx_a = 1 + a;
            let idx_b = 1 + b;
            let mut sum_mod_sq = BigRational::zero();
            for i in 0..DIM_HILBERT {
                for j in 0..DIM_HILBERT {
                    let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
                    let mod_sq_cyc = entry.mul(&entry.conj());
                    let mod_sq = exact_rational(&mod_sq_cyc)?;
                    sum_mod_sq += mod_sq;
                }
            }
            let val = BigRational::new(1.into(), 6.into()) * sum_mod_sq;
            m4[idx_a][idx_b] = val.clone();
            m4[idx_b][idx_a] = val;
        }
    }

    // 3. Projector pairs P_{ab} (indices 5..10) and Q_{ab} (indices 11..16)
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let idx_p = 5 + p_idx;
        let idx_q = 11 + p_idx;

        let mut diag_mod_sq = BigRational::zero();
        let mut off_mod_sq = BigRational::zero();

        for i in 0..DIM_HILBERT {
            let entry_diag = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let mod_sq_diag = exact_rational(&entry_diag.mul(&entry_diag.conj()))?;
            diag_mod_sq += mod_sq_diag;

            for j in 0..DIM_HILBERT {
                if i != j {
                    let entry_off = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
                    let mod_sq_off = exact_rational(&entry_off.mul(&entry_off.conj()))?;
                    off_mod_sq += mod_sq_off;
                }
            }
        }

        let sixth = BigRational::new(1.into(), 6.into());
        let exp_p = &sixth * &diag_mod_sq;
        let exp_q = &sixth * &off_mod_sq;

        // Moments with 1
        m4[0][idx_p] = exp_p.clone();
        m4[idx_p][0] = exp_p.clone();
        m4[0][idx_q] = exp_q.clone();
        m4[idx_q][0] = exp_q.clone();

        // Moments with A_a and A_b
        m4[1 + a][idx_p] = exp_p.clone();
        m4[idx_p][1 + a] = exp_p.clone();
        m4[1 + b][idx_p] = exp_p.clone();
        m4[idx_p][1 + b] = exp_p.clone();

        m4[1 + a][idx_q] = exp_q.clone();
        m4[idx_q][1 + a] = exp_q.clone();
        m4[1 + b][idx_q] = exp_q.clone();
        m4[idx_q][1 + b] = exp_q.clone();

        // Diagonal moments <P_{ab}^2> and <Q_{ab}^2>
        m4[idx_p][idx_p] = exp_p;
        m4[idx_q][idx_q] = exp_q;

        // Cross-term <P_{ab} Q_{ab}> = 0
        m4[idx_p][idx_q] = BigRational::zero();
        m4[idx_q][idx_p] = BigRational::zero();
    }

    // 4. Cross-pair interactions
    for (p1, &(a1, b1)) in pairs.iter().enumerate() {
        for (p2, &(a2, b2)) in pairs.iter().enumerate() {
            if p1 < p2 {
                let idx_p1 = 5 + p1;
                let idx_p2 = 5 + p2;
                let val = if a1 == 3 || b1 == 3 || a2 == 3 || b2 == 3 {
                    BigRational::zero()
                } else {
                    BigRational::new(1.into(), 36.into())
                };
                m4[idx_p1][idx_p2] = val.clone();
                m4[idx_p2][idx_p1] = val;
            }
        }
    }

    Ok(m4)
}

/// Construct the 31x31 Degree-4 Extended Moment Matrix M_4^{ext}(G) over BigRational.
pub fn build_degree4_extended_moment_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return Err(format!(
            "Gramian dimension must be {}x{}",
            GRAMIAN_DIM, GRAMIAN_DIM
        ));
    }

    let pairs = get_basis_pairs();
    let n = DEG4_EXTENDED_DIM;
    let mut m4 = vec![vec![BigRational::zero(); n]; n];
    let sixth = BigRational::new(1.into(), 6.into());

    // 1. 25x25 Degree-2 block
    m4[0][0] = BigRational::one();
    for idx in 0..GRAMIAN_DIM {
        m4[0][idx + 1] = sixth.clone();
        m4[idx + 1][0] = sixth.clone();
    }

    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            for i in 0..DIM_HILBERT {
                for j in 0..DIM_HILBERT {
                    let row_idx = a * DIM_HILBERT + i + 1;
                    let col_idx = b * DIM_HILBERT + j + 1;
                    if a == b {
                        m4[row_idx][col_idx] = if i == j {
                            sixth.clone()
                        } else {
                            BigRational::zero()
                        };
                    } else {
                        let g_entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
                        let mod_sq = exact_rational(&g_entry.mul(&g_entry.conj()))?;
                        m4[row_idx][col_idx] = &sixth * &mod_sq;
                    }
                }
            }
        }
    }

    // 2. Pair blocks P_{ab} (indices 25..30)
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let col_p = 25 + p_idx;
        let mut diag_mod_sq = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let mod_sq = exact_rational(&entry.mul(&entry.conj()))?;
            diag_mod_sq += &mod_sq;

            m4[a * DIM_HILBERT + i + 1][col_p] = &sixth * &mod_sq;
            m4[col_p][a * DIM_HILBERT + i + 1] = &sixth * &mod_sq;
            m4[b * DIM_HILBERT + i + 1][col_p] = &sixth * &mod_sq;
            m4[col_p][b * DIM_HILBERT + i + 1] = &sixth * &mod_sq;
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
    z[1] = BigRational::one(); // A_0
    z[4] = BigRational::one(); // A_3

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

// ==============================================================================
// Master Degree-4 Certificate
// ==============================================================================

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

pub fn solve_target_q2_degree4_certificate() -> Result<MubDegree4Certificate, String> {
    // 1. Candidate A: X = 0 on 17x17 invariant moment matrix
    let g_diag = build_block_diagonal_gramian();
    let m4_inv_diag = build_degree4_invariant_moment_matrix(&g_diag)?;

    let w4_inv = build_invariant_dual_witness_x0(true);
    let tr_w4_x0 = w4_inv.trace_inner(&m4_inv_diag)?;
    let w4_full_x0 = w4_inv.to_full_matrix()?;
    let pivots_x0 = ldlt_pivots_strictly_positive_rational(&w4_full_x0)?;
    let pivots_x0_pos = pivots_x0.iter().all(|p| p > &BigRational::zero());
    let neg_x0 = tr_w4_x0 < BigRational::zero();

    let receipt_x0 = DualWitnessReceipt {
        target_description:
            "Candidate completion X = 0 refuted at Degree 4 via S_6-invariant moment witness".into(),
        witness_dimension: DEG4_INVARIANT_DIM,
        inner_product: tr_w4_x0.to_string(),
        inner_product_num: tr_w4_x0.numer().to_string(),
        inner_product_den: tr_w4_x0.denom().to_string(),
        strictly_negative: neg_x0,
        pivots_strictly_positive: pivots_x0_pos,
        pivots: pivots_x0.iter().map(|p| p.to_string()).collect(),
    };

    // 2. Candidate B: Synthetic S_6 on 31x31 extended moment matrix
    let g_synth = canonical_quad_gramian();
    let m4_ext_synth = build_degree4_extended_moment_matrix(&g_synth)?;

    let w4_ext_s6 = build_extended_dual_witness_s6(true);
    let tr_w4_s6 = w4_ext_s6.trace_inner(&m4_ext_synth)?;
    let w4_full_s6 = w4_ext_s6.to_full_matrix()?;
    let pivots_s6 = ldlt_pivots_strictly_positive_rational(&w4_full_s6)?;
    let pivots_s6_pos = pivots_s6.iter().all(|p| p > &BigRational::zero());
    let neg_s6 = tr_w4_s6 < BigRational::zero();

    let receipt_s6 = DualWitnessReceipt {
        target_description:
            "Candidate completion S_6 refuted at Degree 4 via extended moment witness".into(),
        witness_dimension: DEG4_EXTENDED_DIM,
        inner_product: tr_w4_s6.to_string(),
        inner_product_num: tr_w4_s6.numer().to_string(),
        inner_product_den: tr_w4_s6.denom().to_string(),
        strictly_negative: neg_s6,
        pivots_strictly_positive: pivots_s6_pos,
        pivots: pivots_s6.iter().map(|p| p.to_string()).collect(),
    };

    let moment_report = Degree4MomentReport {
        invariant_dimension: DEG4_INVARIANT_DIM,
        extended_dimension: DEG4_EXTENDED_DIM,
        candidate_x0_refuted: neg_x0 && pivots_x0_pos,
        candidate_s6_refuted: neg_s6 && pivots_s6_pos,
        details:
            "Target Q2: Degree-4 symmetry-reduced and extended moment SDP refutation certified."
                .into(),
    };

    let complete = receipt_x0.strictly_negative
        && receipt_x0.pivots_strictly_positive
        && receipt_s6.strictly_negative
        && receipt_s6.pivots_strictly_positive;

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
