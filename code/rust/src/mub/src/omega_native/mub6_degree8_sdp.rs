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

fn one_sixth() -> BigRational {
    BigRational::new(1.into(), 6.into())
}

fn set_symmetric(m: &mut [Vec<BigRational>], r: usize, c: usize, val: BigRational) {
    m[r][c] = val.clone();
    m[c][r] = val;
}

fn validate_hermitian_gramian(g: &[Vec<Cyc24>]) -> Result<(), String> {
    if g.len() != GRAMIAN_DIM || g.iter().any(|row| row.len() != GRAMIAN_DIM) {
        return Err(format!(
            "Gramian dimension must be {}x{}",
            GRAMIAN_DIM, GRAMIAN_DIM
        ));
    }
    for (i, row) in g.iter().enumerate() {
        for (j, cell) in row.iter().enumerate() {
            if *cell != g[j][i].conj() {
                return Err("Input matrix must be Hermitian".into());
            }
        }
    }
    Ok(())
}

fn block_mod_sq_sum(g: &[Vec<Cyc24>], a: usize, b: usize) -> Result<BigRational, String> {
    let mut sum_mod_sq = BigRational::zero();
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
            sum_mod_sq += exact_rational(&entry.mul(&entry.conj()))?;
        }
    }
    Ok(one_sixth() * sum_mod_sq)
}

fn pair_diag_and_off_mod_sq(
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
) -> Result<(BigRational, BigRational), String> {
    let mut diag_mod_sq = BigRational::zero();
    let mut off_mod_sq = BigRational::zero();
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
            let sq = exact_rational(&entry.mul(&entry.conj()))?;
            if i == j {
                diag_mod_sq += sq;
            } else {
                off_mod_sq += sq;
            }
        }
    }
    Ok((one_sixth() * diag_mod_sq, one_sixth() * off_mod_sq))
}

fn populate_inv_basis_and_pairs(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
) -> Result<(), String> {
    m8[0][0] = BigRational::one();
    for a in 0..NUM_BASES {
        let idx_a = 1 + a;
        set_symmetric(m8, 0, idx_a, BigRational::one());
        m8[idx_a][idx_a] = BigRational::one();
        for b in (a + 1)..NUM_BASES {
            let val = block_mod_sq_sum(g, a, b)?;
            set_symmetric(m8, idx_a, 1 + b, val);
        }
    }
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let idx_p = 5 + p_idx;
        let idx_q = 11 + p_idx;
        let (exp_p, exp_q) = pair_diag_and_off_mod_sq(g, a, b)?;
        set_symmetric(m8, 0, idx_p, exp_p.clone());
        set_symmetric(m8, 0, idx_q, exp_q.clone());
        for c in 0..NUM_BASES {
            set_symmetric(m8, 1 + c, idx_p, exp_p.clone());
            set_symmetric(m8, 1 + c, idx_q, exp_q.clone());
        }
        m8[idx_p][idx_p] = exp_p;
        m8[idx_q][idx_q] = exp_q;
    }
    Ok(())
}

fn pair_cross_correlation(g: &[Vec<Cyc24>], p1: (usize, usize), p2: (usize, usize)) -> BigRational {
    let (a, b) = p1;
    let (c, d) = p2;
    let mut val = BigRational::zero();
    for i in 0..DIM_HILBERT {
        let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
        let e_cd = &g[c * DIM_HILBERT + i][d * DIM_HILBERT + i];
        val += cyc_real_constant_coefficient(&e_ab.mul(&e_cd.conj()));
    }
    one_sixth() * val
}

fn populate_inv_pair_cross(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
) {
    for (p1, &ab) in pairs.iter().enumerate() {
        for (p2, &cd) in pairs.iter().enumerate().skip(p1 + 1) {
            let cross_val = pair_cross_correlation(g, ab, cd);
            set_symmetric(m8, 5 + p1, 5 + p2, cross_val);
        }
    }
}

fn triple_bargmann_and_diag(
    g: &[Vec<Cyc24>],
    triple: (usize, usize, usize),
) -> Result<(BigRational, BigRational), String> {
    let (a, b, c) = triple;
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
    Ok((one_sixth() * bargmann_sum, one_sixth() * diag_cubed_sum))
}

fn pair_in_slice(pair: (usize, usize), set: &[usize]) -> bool {
    set.contains(&pair.0) && set.contains(&pair.1)
}

fn triple_in_slice(triple: (usize, usize, usize), set: &[usize]) -> bool {
    set.contains(&triple.0) && set.contains(&triple.1) && set.contains(&triple.2)
}

fn populate_inv_triples(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
) -> Result<(), String> {
    for (t_idx, &triple) in triples.iter().enumerate() {
        let idx_t = 17 + t_idx;
        let (exp_t, exp_t_diag) = triple_bargmann_and_diag(g, triple)?;
        set_symmetric(m8, 0, idx_t, exp_t.clone());
        for d in 0..NUM_BASES {
            set_symmetric(m8, 1 + d, idx_t, exp_t.clone());
        }
        let t_slice = [triple.0, triple.1, triple.2];
        for (p_idx, &pair) in pairs.iter().enumerate() {
            let idx_p = 5 + p_idx;
            let idx_q = 11 + p_idx;
            let p_val = if pair_in_slice(pair, &t_slice) {
                exp_t.clone()
            } else {
                BigRational::zero()
            };
            let q_val = &exp_t - &p_val;
            set_symmetric(m8, idx_p, idx_t, p_val);
            set_symmetric(m8, idx_q, idx_t, q_val);
        }
        m8[idx_t][idx_t] = if exp_t_diag > BigRational::zero() {
            exp_t_diag
        } else {
            exp_t
        };
    }
    Ok(())
}

fn triple_cross_correlation(
    g: &[Vec<Cyc24>],
    t1: (usize, usize, usize),
    t2: (usize, usize, usize),
) -> BigRational {
    let (a1, b1, c1) = t1;
    let (a2, b2, c2) = t2;
    let mut cross_val = BigRational::zero();
    for i in 0..DIM_HILBERT {
        let c1_val = g[a1 * DIM_HILBERT + i][b1 * DIM_HILBERT + i]
            .mul(&g[b1 * DIM_HILBERT + i][c1 * DIM_HILBERT + i])
            .mul(&g[c1 * DIM_HILBERT + i][a1 * DIM_HILBERT + i]);
        let c2_val = g[a2 * DIM_HILBERT + i][b2 * DIM_HILBERT + i]
            .mul(&g[b2 * DIM_HILBERT + i][c2 * DIM_HILBERT + i])
            .mul(&g[c2 * DIM_HILBERT + i][a2 * DIM_HILBERT + i]);
        cross_val += cyc_real_constant_coefficient(&c1_val.mul(&c2_val.conj()));
    }
    one_sixth() * cross_val
}

fn populate_inv_triple_cross(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    triples: &[(usize, usize, usize)],
) {
    for (t1, &tr1) in triples.iter().enumerate() {
        for (t2, &tr2) in triples.iter().enumerate().skip(t1 + 1) {
            let val = triple_cross_correlation(g, tr1, tr2);
            set_symmetric(m8, 17 + t1, 17 + t2, val);
        }
    }
}

fn quad_bargmann_and_diag(
    g: &[Vec<Cyc24>],
    quad: (usize, usize, usize, usize),
) -> Result<(BigRational, BigRational), String> {
    let (a, b, c, d) = quad;
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
    Ok((one_sixth() * bargmann_quad_sum, one_sixth() * diag_quad_sum))
}

fn populate_single_inv_quadruple(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
    q_idx: usize,
    quad: (usize, usize, usize, usize),
) -> Result<(), String> {
    let idx_r = 21 + q_idx;
    let (exp_r, exp_r_diag) = quad_bargmann_and_diag(g, quad)?;
    set_symmetric(m8, 0, idx_r, exp_r.clone());
    for k in 0..NUM_BASES {
        set_symmetric(m8, 1 + k, idx_r, exp_r.clone());
    }
    let q_slice = [quad.0, quad.1, quad.2, quad.3];
    for (p_idx, &pair) in pairs.iter().enumerate() {
        let p_val = if pair_in_slice(pair, &q_slice) {
            exp_r.clone()
        } else {
            BigRational::zero()
        };
        let q_val = &exp_r - &p_val;
        set_symmetric(m8, 5 + p_idx, idx_r, p_val);
        set_symmetric(m8, 11 + p_idx, idx_r, q_val);
    }
    for (t_idx, &triple) in triples.iter().enumerate() {
        let t_val = if triple_in_slice(triple, &q_slice) {
            exp_r.clone()
        } else {
            BigRational::zero()
        };
        set_symmetric(m8, 17 + t_idx, idx_r, t_val);
    }
    m8[idx_r][idx_r] = if exp_r_diag > BigRational::zero() {
        exp_r_diag
    } else {
        exp_r
    };
    Ok(())
}

fn populate_inv_quadruples(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
    quadruples: &[(usize, usize, usize, usize)],
) -> Result<(), String> {
    for (q_idx, &quad) in quadruples.iter().enumerate() {
        populate_single_inv_quadruple(m8, g, pairs, triples, q_idx, quad)?;
    }
    Ok(())
}

pub fn build_degree8_invariant_diagnostic_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_hermitian_gramian(g)?;
    let pairs = get_basis_pairs();
    let triples = get_basis_triples();
    let quadruples = get_basis_quadruples();
    let mut m8 = vec![vec![BigRational::zero(); DEG8_INVARIANT_DIM]; DEG8_INVARIANT_DIM];

    populate_inv_basis_and_pairs(&mut m8, g, &pairs)?;
    populate_inv_pair_cross(&mut m8, g, &pairs);
    populate_inv_triples(&mut m8, g, &pairs, &triples)?;
    populate_inv_triple_cross(&mut m8, g, &triples);
    populate_inv_quadruples(&mut m8, g, &pairs, &triples, &quadruples)?;

    Ok(m8)
}

fn populate_ext_basis_blocks(m8: &mut [Vec<BigRational>], g: &[Vec<Cyc24>]) -> Result<(), String> {
    m8[0][0] = BigRational::one();
    let sixth = one_sixth();
    for idx in 1..=(NUM_BASES * DIM_HILBERT) {
        set_symmetric(m8, 0, idx, sixth.clone());
        m8[idx][idx] = sixth.clone();
    }
    for idx_a in 0..(NUM_BASES * DIM_HILBERT) {
        let a = idx_a / DIM_HILBERT;
        for idx_b in 0..(NUM_BASES * DIM_HILBERT) {
            let b = idx_b / DIM_HILBERT;
            if a != b {
                let entry = &g[idx_a][idx_b];
                m8[1 + idx_a][1 + idx_b] = &sixth * exact_rational(&entry.mul(&entry.conj()))?;
            }
        }
    }
    Ok(())
}

fn populate_ext_pairs_and_triples(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
) -> Result<(), String> {
    let sixth = one_sixth();
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let col_p = 25 + p_idx;
        let mut diag_mod_sq = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let mod_sq = exact_rational(&entry.mul(&entry.conj()))?;
            diag_mod_sq += &mod_sq;
            let term = &sixth * mod_sq;
            set_symmetric(m8, a * DIM_HILBERT + i + 1, col_p, term.clone());
            set_symmetric(m8, b * DIM_HILBERT + i + 1, col_p, term);
        }
        let exp_p = &sixth * diag_mod_sq;
        set_symmetric(m8, 0, col_p, exp_p.clone());
        m8[col_p][col_p] = exp_p;
    }

    for (t_idx, &(a, b, c)) in triples.iter().enumerate() {
        let col_t = 31 + t_idx;
        let mut bargmann_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_ca = &g[c * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let c_val = cyc_real_constant_coefficient(&e_ab.mul(e_bc).mul(e_ca));
            bargmann_sum += &c_val;
            let term = &sixth * c_val;
            for base in [a, b, c] {
                set_symmetric(m8, base * DIM_HILBERT + i + 1, col_t, term.clone());
            }
        }
        let exp_t = &sixth * bargmann_sum;
        set_symmetric(m8, 0, col_t, exp_t.clone());
        m8[col_t][col_t] = if exp_t > BigRational::zero() {
            exp_t
        } else {
            BigRational::zero()
        };
    }
    Ok(())
}

fn populate_ext_quadruple_basis_entries(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    quad: (usize, usize, usize, usize),
    col_r: usize,
) {
    let (a, b, c, d) = quad;
    let sixth = one_sixth();
    for i in 0..DIM_HILBERT {
        let cycle = g[a * DIM_HILBERT + i][b * DIM_HILBERT + i]
            .mul(&g[b * DIM_HILBERT + i][c * DIM_HILBERT + i])
            .mul(&g[c * DIM_HILBERT + i][d * DIM_HILBERT + i])
            .mul(&g[d * DIM_HILBERT + i][a * DIM_HILBERT + i]);
        let term = &sixth * cyc_real_constant_coefficient(&cycle);
        for base in [a, b, c, d] {
            set_symmetric(m8, base * DIM_HILBERT + i + 1, col_r, term.clone());
        }
    }
}

fn populate_single_ext_quadruple(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
    q_idx: usize,
    quad: (usize, usize, usize, usize),
) -> Result<(), String> {
    let col_r = 35 + q_idx;
    let (exp_r, exp_r_diag) = quad_bargmann_and_diag(g, quad)?;
    populate_ext_quadruple_basis_entries(m8, g, quad, col_r);
    set_symmetric(m8, 0, col_r, exp_r.clone());
    let q_slice = [quad.0, quad.1, quad.2, quad.3];
    for (p_idx, &pair) in pairs.iter().enumerate() {
        if pair_in_slice(pair, &q_slice) {
            set_symmetric(m8, 25 + p_idx, col_r, exp_r.clone());
        }
    }
    for (t_idx, &triple) in triples.iter().enumerate() {
        if triple_in_slice(triple, &q_slice) {
            set_symmetric(m8, 31 + t_idx, col_r, exp_r.clone());
        }
    }
    m8[col_r][col_r] = if exp_r_diag > BigRational::zero() {
        exp_r_diag
    } else if exp_r > BigRational::zero() {
        exp_r
    } else {
        BigRational::zero()
    };
    Ok(())
}

fn populate_ext_quadruples(
    m8: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
    quadruples: &[(usize, usize, usize, usize)],
) -> Result<(), String> {
    for (q_idx, &quad) in quadruples.iter().enumerate() {
        populate_single_ext_quadruple(m8, g, pairs, triples, q_idx, quad)?;
    }
    Ok(())
}

pub fn build_degree8_extended_diagnostic_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_hermitian_gramian(g)?;
    let pairs = get_basis_pairs();
    let triples = get_basis_triples();
    let quadruples = get_basis_quadruples();
    let mut m8 = vec![vec![BigRational::zero(); DEG8_EXTENDED_DIM]; DEG8_EXTENDED_DIM];

    populate_ext_basis_blocks(&mut m8, g)?;
    populate_ext_pairs_and_triples(&mut m8, g, &pairs, &triples)?;
    populate_ext_quadruples(&mut m8, g, &pairs, &triples, &quadruples)?;

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
    for item in z.iter_mut().take(25).skip(1) {
        *item = BigRational::from_integer((-2).into());
    }
    for item in z.iter_mut().take(31).skip(25) {
        *item = BigRational::from_integer((-5).into());
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

fn evaluate_deg8_witness_receipt(
    w: &DualWitnessRational,
    m8: &[Vec<BigRational>],
    dim: usize,
    label: &str,
    description: &str,
) -> Result<DualWitnessReceipt, String> {
    let inner = w.trace_inner(m8)?;
    if inner >= BigRational::zero() {
        return Err(format!(
            "Dual witness {label} diagnostic failed: Tr(W * M) = {inner} >= 0"
        ));
    }
    let w_mat = w.to_full_matrix()?;
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat)?;
    Ok(DualWitnessReceipt {
        target_description: description.into(),
        witness_dimension: dim,
        inner_product: inner.to_string(),
        inner_product_num: inner.numer().to_string(),
        inner_product_den: inner.denom().to_string(),
        strictly_negative: true,
        pivots_strictly_positive: true,
        pivots: pivots.iter().map(|p| p.to_string()).collect(),
    })
}

pub fn evaluate_target_q4_diagnostics() -> Result<Degree8DiagnosticReport, String> {
    let g_diag = build_block_diagonal_gramian();
    let m8_diag = build_degree8_invariant_diagnostic_matrix(&g_diag)?;
    let w_x0 = build_invariant_dual_witness_x0(true);
    let receipt_x0 = evaluate_deg8_witness_receipt(
        &w_x0,
        &m8_diag,
        DEG8_INVARIANT_DIM,
        "X=0",
        "Experimental coefficient matrix for the block-diagonal X=0 fixture",
    )?;

    let g_synth = canonical_quad_gramian();
    let m8_synth = build_degree8_extended_diagnostic_matrix(&g_synth)?;
    let w_s6 = build_extended_dual_witness_s6(true);
    let receipt_s6 = evaluate_deg8_witness_receipt(
        &w_s6,
        &m8_synth,
        DEG8_EXTENDED_DIM,
        "S6",
        "Experimental coefficient matrix for the synthetic S6 fixture",
    )?;

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
