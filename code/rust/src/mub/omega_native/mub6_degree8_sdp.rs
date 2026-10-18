
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, exact_rational, DIM_HILBERT, GRAMIAN_DIM, NUM_BASES,
};
pub use crate::omega_native::exact::mub6_quad_sdp::{
    cyc_real_constant_coefficient, cyc_real_rational, get_basis_pairs, get_basis_quadruples,
    get_basis_triples,
};
use linear_algebra::exact_ldlt::ldlt_pivots_strictly_positive_rational;
use omega_number_theory::cyclotomic::Cyc24;

pub const SCHEMA_VERSION: &str = "omega.mub.degree8-diagnostics.v2";
pub const SCOPE_STRING: &str = "experimental_coefficient_projection_only_no_moment_soundness";

pub const DEG8_INVARIANT_DIM: usize = 22;
pub const DEG8_EXTENDED_DIM: usize = 36;

pub fn build_degree8_invariant_diagnostic_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return Err(format!(
            "Gramian dimension must be {}x{}",
            GRAMIAN_DIM, GRAMIAN_DIM
        ));
    }

    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            if g[i][j] != g[j][i].conj() {
                return Err("Input matrix must be Hermitian".into());
            }
        }
    }

    let pairs = get_basis_pairs();
    let triples = get_basis_triples();
    let quadruples = get_basis_quadruples();
    let n = DEG8_INVARIANT_DIM;
    let mut m8 = vec![vec![BigRational::zero(); n]; n];

    m8[0][0] = BigRational::one();

    for a in 0..NUM_BASES {
        let idx_a = 1 + a;
        m8[0][idx_a] = BigRational::one();
        m8[idx_a][0] = BigRational::one();
        m8[idx_a][idx_a] = BigRational::one();
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
                    sum_mod_sq += exact_rational(&mod_sq_cyc)?;
                }
            }
            let val = BigRational::new(1.into(), 6.into()) * sum_mod_sq;
            m8[idx_a][idx_b] = val.clone();
            m8[idx_b][idx_a] = val;
        }
    }

    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let idx_p = 5 + p_idx;
        let idx_q = 11 + p_idx;

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

        let exp_p = BigRational::new(1.into(), 6.into()) * diag_mod_sq;
        let exp_q = BigRational::new(1.into(), 6.into()) * off_mod_sq;

        m8[0][idx_p] = exp_p.clone();
        m8[idx_p][0] = exp_p.clone();
        m8[0][idx_q] = exp_q.clone();
        m8[idx_q][0] = exp_q.clone();

        m8[1 + a][idx_p] = exp_p.clone();
        m8[idx_p][1 + a] = exp_p.clone();
        m8[1 + b][idx_p] = exp_p.clone();
        m8[idx_p][1 + b] = exp_p.clone();

        m8[1 + a][idx_q] = exp_q.clone();
        m8[idx_q][1 + a] = exp_q.clone();
        m8[1 + b][idx_q] = exp_q.clone();
        m8[idx_q][1 + b] = exp_q.clone();

        for c in 0..NUM_BASES {
            if c != a && c != b {
                m8[1 + c][idx_p] = exp_p.clone();
                m8[idx_p][1 + c] = exp_p.clone();
                m8[1 + c][idx_q] = exp_q.clone();
                m8[idx_q][1 + c] = exp_q.clone();
            }
        }

        m8[idx_p][idx_p] = exp_p;
        m8[idx_q][idx_q] = exp_q;
    }

    for (p1, &(a, b)) in pairs.iter().enumerate() {
        for (p2, &(c, d)) in pairs.iter().enumerate() {
            if p1 < p2 {
                let idx1 = 5 + p1;
                let idx2 = 5 + p2;
                let mut val = BigRational::zero();
                for i in 0..DIM_HILBERT {
                    let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
                    let e_cd = &g[c * DIM_HILBERT + i][d * DIM_HILBERT + i];
                    let prod = e_ab.mul(&e_cd.conj());
                    val += cyc_real_constant_coefficient(&prod);
                }
                let cross_val = BigRational::new(1.into(), 6.into()) * val;
                m8[idx1][idx2] = cross_val.clone();
                m8[idx2][idx1] = cross_val;
            }
        }
    }

    for (t_idx, &(a, b, c)) in triples.iter().enumerate() {
        let idx_t = 17 + t_idx;

        let mut bargmann_sum = BigRational::zero();
        let mut diag_cubed_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_ca = &g[c * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let cycle = e_ab.mul(e_bc).mul(e_ca);
            bargmann_sum += cyc_real_constant_coefficient(&cycle);

            let mod_sq = exact_rational(&e_ab.mul(&e_ab.conj()))?
                * exact_rational(&e_bc.mul(&e_bc.conj()))?
                * exact_rational(&e_ca.mul(&e_ca.conj()))?;
            diag_cubed_sum += mod_sq;
        }

        let exp_t = BigRational::new(1.into(), 6.into()) * bargmann_sum;
        let exp_t_diag = BigRational::new(1.into(), 6.into()) * diag_cubed_sum;

        m8[0][idx_t] = exp_t.clone();
        m8[idx_t][0] = exp_t.clone();

        for d in 0..NUM_BASES {
            m8[1 + d][idx_t] = exp_t.clone();
            m8[idx_t][1 + d] = exp_t.clone();
        }

        for (p_idx, &(p_a, p_b)) in pairs.iter().enumerate() {
            let idx_p = 5 + p_idx;
            let idx_q = 11 + p_idx;
            if (p_a == a || p_a == b || p_a == c) && (p_b == a || p_b == b || p_b == c) {
                m8[idx_p][idx_t] = exp_t.clone();
                m8[idx_t][idx_p] = exp_t.clone();
            } else {
                m8[idx_p][idx_t] = BigRational::zero();
                m8[idx_t][idx_p] = BigRational::zero();
            }

            m8[idx_q][idx_t] = &exp_t - &m8[idx_p][idx_t];
            m8[idx_t][idx_q] = m8[idx_q][idx_t].clone();
        }

        m8[idx_t][idx_t] = if exp_t_diag > BigRational::zero() {
            exp_t_diag
        } else {
            exp_t
        };
    }

    for (t1, &(a1, b1, c1)) in triples.iter().enumerate() {
        for (t2, &(a2, b2, c2)) in triples.iter().enumerate() {
            if t1 < t2 {
                let idx1 = 17 + t1;
                let idx2 = 17 + t2;
                let mut cross_val = BigRational::zero();
                for i in 0..DIM_HILBERT {
                    let c1_val = g[a1 * DIM_HILBERT + i][b1 * DIM_HILBERT + i]
                        .mul(&g[b1 * DIM_HILBERT + i][c1 * DIM_HILBERT + i])
                        .mul(&g[c1 * DIM_HILBERT + i][a1 * DIM_HILBERT + i]);
                    let c2_val = g[a2 * DIM_HILBERT + i][b2 * DIM_HILBERT + i]
                        .mul(&g[b2 * DIM_HILBERT + i][c2 * DIM_HILBERT + i])
                        .mul(&g[c2 * DIM_HILBERT + i][a2 * DIM_HILBERT + i]);
                    let prod = c1_val.mul(&c2_val.conj());
                    cross_val += cyc_real_constant_coefficient(&prod);
                }
                let val = BigRational::new(1.into(), 6.into()) * cross_val;
                m8[idx1][idx2] = val.clone();
                m8[idx2][idx1] = val;
            }
        }
    }

    for (q_idx, &(a, b, c, d)) in quadruples.iter().enumerate() {
        let idx_r = 21 + q_idx;

        let mut bargmann_quad_sum = BigRational::zero();
        let mut diag_quad_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_cd = &g[c * DIM_HILBERT + i][d * DIM_HILBERT + i];
            let e_da = &g[d * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let cycle = e_ab.mul(e_bc).mul(e_cd).mul(e_da);
            bargmann_quad_sum += cyc_real_constant_coefficient(&cycle);

            let mod_sq = exact_rational(&e_ab.mul(&e_ab.conj()))?
                * exact_rational(&e_bc.mul(&e_bc.conj()))?
                * exact_rational(&e_cd.mul(&e_cd.conj()))?
                * exact_rational(&e_da.mul(&e_da.conj()))?;
            diag_quad_sum += mod_sq;
        }

        let exp_r = BigRational::new(1.into(), 6.into()) * bargmann_quad_sum;
        let exp_r_diag = BigRational::new(1.into(), 6.into()) * diag_quad_sum;

        m8[0][idx_r] = exp_r.clone();
        m8[idx_r][0] = exp_r.clone();

        for k in 0..NUM_BASES {
            m8[1 + k][idx_r] = exp_r.clone();
            m8[idx_r][1 + k] = exp_r.clone();
        }

        for (p_idx, &(p_a, p_b)) in pairs.iter().enumerate() {
            let idx_p = 5 + p_idx;
            let idx_q = 11 + p_idx;
            if (p_a == a || p_a == b || p_a == c || p_a == d)
                && (p_b == a || p_b == b || p_b == c || p_b == d)
            {
                m8[idx_p][idx_r] = exp_r.clone();
                m8[idx_r][idx_p] = exp_r.clone();
            } else {
                m8[idx_p][idx_r] = BigRational::zero();
                m8[idx_r][idx_p] = BigRational::zero();
            }

            m8[idx_q][idx_r] = &exp_r - &m8[idx_p][idx_r];
            m8[idx_r][idx_q] = m8[idx_q][idx_r].clone();
        }

        for (t_idx, &(t_a, t_b, t_c)) in triples.iter().enumerate() {
            let idx_t = 17 + t_idx;
            if (t_a == a || t_a == b || t_a == c || t_a == d)
                && (t_b == a || t_b == b || t_b == c || t_b == d)
                && (t_c == a || t_c == b || t_c == c || t_c == d)
            {
                m8[idx_t][idx_r] = exp_r.clone();
                m8[idx_r][idx_t] = exp_r.clone();
            } else {
                m8[idx_t][idx_r] = BigRational::zero();
                m8[idx_r][idx_t] = BigRational::zero();
            }
        }

        m8[idx_r][idx_r] = if exp_r_diag > BigRational::zero() {
            exp_r_diag
        } else {
            exp_r
        };
    }

    Ok(m8)
}

pub fn build_degree8_extended_diagnostic_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return Err(format!(
            "Gramian dimension must be {}x{}",
            GRAMIAN_DIM, GRAMIAN_DIM
        ));
    }

    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            if g[i][j] != g[j][i].conj() {
                return Err("Input matrix must be Hermitian".into());
            }
        }
    }

    let pairs = get_basis_pairs();
    let triples = get_basis_triples();
    let quadruples = get_basis_quadruples();
    let n = DEG8_EXTENDED_DIM;
    let mut m8 = vec![vec![BigRational::zero(); n]; n];

    m8[0][0] = BigRational::one();

    for a in 0..NUM_BASES {
        for i in 0..DIM_HILBERT {
            let idx = 1 + a * DIM_HILBERT + i;
            m8[0][idx] = BigRational::new(1.into(), 6.into());
            m8[idx][0] = BigRational::new(1.into(), 6.into());
            m8[idx][idx] = BigRational::new(1.into(), 6.into());
        }
    }

    for a in 0..NUM_BASES {
        for i in 0..DIM_HILBERT {
            let idx_a = 1 + a * DIM_HILBERT + i;
            for b in 0..NUM_BASES {
                for j in 0..DIM_HILBERT {
                    let idx_b = 1 + b * DIM_HILBERT + j;
                    if a == b && i != j {
                        m8[idx_a][idx_b] = BigRational::zero();
                    } else if a != b {
                        let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
                        let val = BigRational::new(1.into(), 6.into())
                            * exact_rational(&entry.mul(&entry.conj()))?;
                        m8[idx_a][idx_b] = val;
                    }
                }
            }
        }
    }

    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let col_p = 25 + p_idx;
        let mut diag_mod_sq = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let mod_sq = exact_rational(&entry.mul(&entry.conj()))?;
            diag_mod_sq += &mod_sq;
            let term = BigRational::new(1.into(), 6.into()) * mod_sq;
            m8[a * DIM_HILBERT + i + 1][col_p] = term.clone();
            m8[col_p][a * DIM_HILBERT + i + 1] = term.clone();
            m8[b * DIM_HILBERT + i + 1][col_p] = term.clone();
            m8[col_p][b * DIM_HILBERT + i + 1] = term;
        }

        let exp_p = BigRational::new(1.into(), 6.into()) * diag_mod_sq;
        m8[0][col_p] = exp_p.clone();
        m8[col_p][0] = exp_p.clone();
        m8[col_p][col_p] = exp_p;
    }

    for (t_idx, &(a, b, c)) in triples.iter().enumerate() {
        let col_t = 31 + t_idx;
        let mut bargmann_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_ca = &g[c * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let cycle = e_ab.mul(e_bc).mul(e_ca);
            let c_val = cyc_real_constant_coefficient(&cycle);
            bargmann_sum += &c_val;

            let term = BigRational::new(1.into(), 6.into()) * c_val;
            m8[a * DIM_HILBERT + i + 1][col_t] = term.clone();
            m8[col_t][a * DIM_HILBERT + i + 1] = term.clone();
            m8[b * DIM_HILBERT + i + 1][col_t] = term.clone();
            m8[col_t][b * DIM_HILBERT + i + 1] = term.clone();
            m8[c * DIM_HILBERT + i + 1][col_t] = term.clone();
            m8[col_t][c * DIM_HILBERT + i + 1] = term;
        }

        let exp_t = BigRational::new(1.into(), 6.into()) * bargmann_sum;
        m8[0][col_t] = exp_t.clone();
        m8[col_t][0] = exp_t.clone();
        m8[col_t][col_t] = if exp_t > BigRational::zero() {
            exp_t
        } else {
            BigRational::zero()
        };
    }

    for (q_idx, &(a, b, c, d)) in quadruples.iter().enumerate() {
        let col_r = 35 + q_idx;
        let mut bargmann_quad_sum = BigRational::zero();
        let mut diag_quad_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_cd = &g[c * DIM_HILBERT + i][d * DIM_HILBERT + i];
            let e_da = &g[d * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let cycle = e_ab.mul(e_bc).mul(e_cd).mul(e_da);
            let c_val = cyc_real_constant_coefficient(&cycle);
            bargmann_quad_sum += &c_val;

            let mod_sq = exact_rational(&e_ab.mul(&e_ab.conj()))?
                * exact_rational(&e_bc.mul(&e_bc.conj()))?
                * exact_rational(&e_cd.mul(&e_cd.conj()))?
                * exact_rational(&e_da.mul(&e_da.conj()))?;
            diag_quad_sum += mod_sq;

            let term = BigRational::new(1.into(), 6.into()) * c_val;
            m8[a * DIM_HILBERT + i + 1][col_r] = term.clone();
            m8[col_r][a * DIM_HILBERT + i + 1] = term.clone();
            m8[b * DIM_HILBERT + i + 1][col_r] = term.clone();
            m8[col_r][b * DIM_HILBERT + i + 1] = term.clone();
            m8[c * DIM_HILBERT + i + 1][col_r] = term.clone();
            m8[col_r][c * DIM_HILBERT + i + 1] = term.clone();
            m8[d * DIM_HILBERT + i + 1][col_r] = term.clone();
            m8[col_r][d * DIM_HILBERT + i + 1] = term;
        }

        let exp_r = BigRational::new(1.into(), 6.into()) * bargmann_quad_sum;
        let exp_r_diag = BigRational::new(1.into(), 6.into()) * diag_quad_sum;

        m8[0][col_r] = exp_r.clone();
        m8[col_r][0] = exp_r.clone();

        for (p_idx, &(p_a, p_b)) in pairs.iter().enumerate() {
            let col_p = 25 + p_idx;
            if (p_a == a || p_a == b || p_a == c || p_a == d)
                && (p_b == a || p_b == b || p_b == c || p_b == d)
            {
                m8[col_p][col_r] = exp_r.clone();
                m8[col_r][col_p] = exp_r.clone();
            }
        }

        for (t_idx, &(t_a, t_b, t_c)) in triples.iter().enumerate() {
            let col_t = 31 + t_idx;
            if (t_a == a || t_a == b || t_a == c || t_a == d)
                && (t_b == a || t_b == b || t_b == c || t_b == d)
                && (t_c == a || t_c == b || t_c == c || t_c == d)
            {
                m8[col_t][col_r] = exp_r.clone();
                m8[col_r][col_t] = exp_r.clone();
            }
        }

        m8[col_r][col_r] = if exp_r_diag > BigRational::zero() {
            exp_r_diag
        } else if exp_r > BigRational::zero() {
            exp_r
        } else {
            BigRational::zero()
        };
    }

    Ok(m8)
}

pub fn build_degree8_invariant_moment_matrix(
    _g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}

pub fn build_degree8_extended_moment_matrix(
    _g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}
pub use crate::omega_native::exact::dual_witness::DualWitnessRational;


pub fn build_invariant_dual_witness_x0(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); DEG8_INVARIANT_DIM];
    z[0] = -BigRational::one();
    z[1] = BigRational::one();
    z[4] = BigRational::one();

    let mut vectors = vec![z];
    let mut weights = vec![BigRational::one()];

    if strict {
        let eps = BigRational::new(1.into(), 50.into());
        for i in 0..DEG8_INVARIANT_DIM {
            let mut e = vec![BigRational::zero(); DEG8_INVARIANT_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational::new(DEG8_INVARIANT_DIM, vectors.len(), vectors, weights)
        .expect("Dual witness X0 construction failed")
}

pub fn build_extended_dual_witness_s6(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); DEG8_EXTENDED_DIM];
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
        for i in 0..DEG8_EXTENDED_DIM {
            let mut e = vec![BigRational::zero(); DEG8_EXTENDED_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational::new(DEG8_EXTENDED_DIM, vectors.len(), vectors, weights)
        .expect("Dual witness S6 construction failed")
}

#[derive(Debug, Clone, Serialize, Deserialize)]
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

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Degree8MomentReport {
    pub invariant_dimension: usize,
    pub extended_dimension: usize,
    pub candidate_x0_refuted: bool,
    pub candidate_s6_refuted: bool,
    pub details: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Degree8DiagnosticReport {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub scope: String,
    pub dimension: usize,
    pub bases_count: usize,
    pub invariant_dim: usize,
    pub extended_dim: usize,
    pub moment_report: Degree8MomentReport,
    pub receipt_x0: DualWitnessReceipt,
    pub receipt_s6: DualWitnessReceipt,
    pub complete: bool,
    pub diagnostics_complete: bool,
    pub moment_semantics_verified: bool,
}

pub fn evaluate_target_q4_diagnostics() -> Result<Degree8DiagnosticReport, String> {
    let g_diag = build_block_diagonal_gramian();
    let m8_diag = build_degree8_invariant_diagnostic_matrix(&g_diag)?;
    let w_x0 = build_invariant_dual_witness_x0(true);
    let inner_x0 = w_x0.trace_inner(&m8_diag)?;
    if inner_x0 >= BigRational::zero() {
        return Err(format!(
            "Dual witness X=0 diagnostic failed: Tr(W * M) = {inner_x0} >= 0"
        ));
    }

    let w_mat_x0 = w_x0.to_full_matrix()?;
    let pivots_x0 = ldlt_pivots_strictly_positive_rational(&w_mat_x0)?;

    let receipt_x0 = DualWitnessReceipt {
        target_description: "Experimental coefficient matrix for the block-diagonal X=0 fixture"
            .into(),
        witness_dimension: DEG8_INVARIANT_DIM,
        inner_product: inner_x0.to_string(),
        inner_product_num: inner_x0.numer().to_string(),
        inner_product_den: inner_x0.denom().to_string(),
        strictly_negative: true,
        pivots_strictly_positive: true,
        pivots: pivots_x0.iter().map(|p| p.to_string()).collect(),
    };

    let g_synth = canonical_quad_gramian();
    let m8_synth = build_degree8_extended_diagnostic_matrix(&g_synth)?;
    let w_s6 = build_extended_dual_witness_s6(true);
    let inner_s6 = w_s6.trace_inner(&m8_synth)?;
    if inner_s6 >= BigRational::zero() {
        return Err(format!(
            "Dual witness S6 diagnostic failed: Tr(W * M) = {inner_s6} >= 0"
        ));
    }

    let w_mat_s6 = w_s6.to_full_matrix()?;
    let pivots_s6 = ldlt_pivots_strictly_positive_rational(&w_mat_s6)?;

    let receipt_s6 = DualWitnessReceipt {
        target_description: "Experimental coefficient matrix for the synthetic S6 fixture".into(),
        witness_dimension: DEG8_EXTENDED_DIM,
        inner_product: inner_s6.to_string(),
        inner_product_num: inner_s6.numer().to_string(),
        inner_product_den: inner_s6.denom().to_string(),
        strictly_negative: true,
        pivots_strictly_positive: true,
        pivots: pivots_s6.iter().map(|p| p.to_string()).collect(),
    };

    let moment_report = Degree8MomentReport {
        invariant_dimension: DEG8_INVARIANT_DIM,
        extended_dimension: DEG8_EXTENDED_DIM,
        candidate_x0_refuted: false,
        candidate_s6_refuted: false,
        details: "Exact matrix diagnostics only. Projector moment identities, positivity preservation, and a Lasserre relaxation are not established.".into(),
    };

    Ok(Degree8DiagnosticReport {
        schema_version: SCHEMA_VERSION.into(),
        firewall: FIREWALL.into(),
        authority_effect: AUTHORITY_EFFECT.into(),
        scope: SCOPE_STRING.into(),
        dimension: DIM_HILBERT,
        bases_count: NUM_BASES,
        invariant_dim: DEG8_INVARIANT_DIM,
        extended_dim: DEG8_EXTENDED_DIM,
        moment_report,
        receipt_x0,
        receipt_s6,
        complete: false,
        diagnostics_complete: true,
        moment_semantics_verified: false,
    })
}

pub fn solve_target_q4_degree8_certificate() -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}
