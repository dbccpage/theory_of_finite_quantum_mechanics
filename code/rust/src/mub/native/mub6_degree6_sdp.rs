
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, exact_rational, DIM_HILBERT, GRAMIAN_DIM, NUM_BASES,
};
pub use crate::native::exact::mub6_quad_sdp::{
    cyc_real_constant_coefficient, cyc_real_rational, get_basis_pairs, get_basis_triples,
};
use linear_algebra::exact_ldlt::ldlt_pivots_strictly_positive_rational;
use engine_number_theory::cyclotomic::Cyc24;

pub const SCHEMA_VERSION: &str = "omega.mub.degree6-diagnostics.v2";
pub const SCOPE_STRING: &str = "experimental_coefficient_projection_only_no_moment_soundness";

pub const DEG6_INVARIANT_DIM: usize = 21;
pub const DEG6_EXTENDED_DIM: usize = 35;

fn validate_deg6_gramian_shape(g: &[Vec<Cyc24>]) -> Result<(), String> {
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

fn validate_deg6_hermitian_gramian(g: &[Vec<Cyc24>]) -> Result<(), String> {
    validate_deg6_gramian_shape(g)?;
    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            if g[i][j] != g[j][i].conj() {
                return Err("Input matrix must be Hermitian".into());
            }
        }
    }
    Ok(())
}

fn sum_deg6_block_mod_sq(g: &[Vec<Cyc24>], a: usize, b: usize) -> Result<BigRational, String> {
    let mut sum_mod_sq = BigRational::zero();
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
            sum_mod_sq += exact_rational(&entry.mul(&entry.conj()))?;
        }
    }
    Ok(sum_mod_sq)
}

fn sum_deg6_diag_and_off_mod_sq(
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

fn populate_deg6_inv_pair_expectations(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
) -> Result<(), String> {
    let sixth = BigRational::new(1.into(), 6.into());
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let idx_p = 5 + p_idx;
        let idx_q = 11 + p_idx;
        let (diag_mod_sq, off_mod_sq) = sum_deg6_diag_and_off_mod_sq(g, a, b)?;
        let exp_p = &sixth * &diag_mod_sq;
        let exp_q = &sixth * &off_mod_sq;

        m6[0][idx_p] = exp_p.clone();
        m6[idx_p][0] = exp_p.clone();
        m6[0][idx_q] = exp_q.clone();
        m6[idx_q][0] = exp_q.clone();

        for c in 0..NUM_BASES {
            m6[1 + c][idx_p] = exp_p.clone();
            m6[idx_p][1 + c] = exp_p.clone();
            m6[1 + c][idx_q] = exp_q.clone();
            m6[idx_q][1 + c] = exp_q.clone();
        }

        m6[idx_p][idx_p] = exp_p;
        m6[idx_q][idx_q] = exp_q;
    }
    Ok(())
}

fn pair_cross_real_sum(g: &[Vec<Cyc24>], a1: usize, b1: usize, a2: usize, b2: usize) -> BigRational {
    let mut val = BigRational::zero();
    for i in 0..DIM_HILBERT {
        let e1 = &g[a1 * DIM_HILBERT + i][b1 * DIM_HILBERT + i];
        let e2 = &g[a2 * DIM_HILBERT + i][b2 * DIM_HILBERT + i];
        val += cyc_real_constant_coefficient(&e1.mul(&e2.conj()));
    }
    val / BigRational::from_integer(6.into())
}

fn populate_deg6_inv_pair_cross(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
) {
    for (p1, &(a1, b1)) in pairs.iter().enumerate() {
        for (p2, &(a2, b2)) in pairs.iter().enumerate() {
            if p1 < p2 {
                let val = pair_cross_real_sum(g, a1, b1, a2, b2);
                m6[5 + p1][5 + p2] = val.clone();
                m6[5 + p2][5 + p1] = val;
            }
        }
    }
}

fn triple_bargmann_and_diag_cubed(
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
    c: usize,
) -> Result<(BigRational, BigRational), String> {
    let mut bargmann_sum = BigRational::zero();
    let mut diag_cubed_sum = BigRational::zero();
    for i in 0..DIM_HILBERT {
        let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
        let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
        let e_ca = &g[c * DIM_HILBERT + i][a * DIM_HILBERT + i];
        let cycle = e_ab.mul(e_bc).mul(e_ca);
        bargmann_sum += cyc_real_constant_coefficient(&cycle);
        diag_cubed_sum += exact_rational(&e_ab.mul(&e_ab.conj()))?
            * exact_rational(&e_bc.mul(&e_bc.conj()))?
            * exact_rational(&e_ca.mul(&e_ca.conj()))?;
    }
    Ok((bargmann_sum, diag_cubed_sum))
}

fn pair_in_triple(p_a: usize, p_b: usize, triple: (usize, usize, usize)) -> bool {
    let (a, b, c) = triple;
    let pa_in = p_a == a || p_a == b || p_a == c;
    let pb_in = p_b == a || p_b == b || p_b == c;
    pa_in && pb_in
}

fn populate_deg6_inv_triples(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    triples: &[(usize, usize, usize)],
) -> Result<(), String> {
    let sixth = BigRational::new(1.into(), 6.into());
    for (t_idx, &triple) in triples.iter().enumerate() {
        let idx_t = 17 + t_idx;
        let (bargmann_sum, diag_cubed_sum) =
            triple_bargmann_and_diag_cubed(g, triple.0, triple.1, triple.2)?;
        let exp_t = &sixth * &bargmann_sum;

        m6[0][idx_t] = exp_t.clone();
        m6[idx_t][0] = exp_t.clone();
        for d in 0..NUM_BASES {
            m6[1 + d][idx_t] = exp_t.clone();
            m6[idx_t][1 + d] = exp_t.clone();
        }

        for (p_idx, &(p_a, p_b)) in pairs.iter().enumerate() {
            let idx_p = 5 + p_idx;
            let idx_q = 11 + p_idx;
            let p_val = if pair_in_triple(p_a, p_b, triple) {
                exp_t.clone()
            } else {
                BigRational::zero()
            };
            let q_val = &exp_t - &p_val;
            m6[idx_p][idx_t] = p_val.clone();
            m6[idx_t][idx_p] = p_val;
            m6[idx_q][idx_t] = q_val.clone();
            m6[idx_t][idx_q] = q_val;
        }

        let exp_t_diag = &sixth * diag_cubed_sum;
        m6[idx_t][idx_t] = if exp_t_diag > BigRational::zero() {
            exp_t_diag
        } else {
            exp_t
        };
    }
    Ok(())
}

fn triple_cross_real_sum(
    g: &[Vec<Cyc24>],
    t1: (usize, usize, usize),
    t2: (usize, usize, usize),
) -> BigRational {
    let (a1, b1, c1) = t1;
    let (a2, b2, c2) = t2;
    let mut val = BigRational::zero();
    for i in 0..DIM_HILBERT {
        let cycle1 = g[a1 * 6 + i][b1 * 6 + i]
            .mul(&g[b1 * 6 + i][c1 * 6 + i])
            .mul(&g[c1 * 6 + i][a1 * 6 + i]);
        let cycle2 = g[a2 * 6 + i][b2 * 6 + i]
            .mul(&g[b2 * 6 + i][c2 * 6 + i])
            .mul(&g[c2 * 6 + i][a2 * 6 + i]);
        val += cyc_real_constant_coefficient(&cycle1.mul(&cycle2.conj()));
    }
    BigRational::new(1.into(), 6.into()) * val
}

fn populate_deg6_inv_triple_cross(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    triples: &[(usize, usize, usize)],
) {
    for (t1, &tr1) in triples.iter().enumerate() {
        for (t2, &tr2) in triples.iter().enumerate() {
            if t1 < t2 {
                let val = triple_cross_real_sum(g, tr1, tr2);
                m6[17 + t1][17 + t2] = val.clone();
                m6[17 + t2][17 + t1] = val;
            }
        }
    }
}

pub fn build_degree6_invariant_diagnostic_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_deg6_hermitian_gramian(g)?;
    let pairs = get_basis_pairs();
    let triples = get_basis_triples();
    let n = DEG6_INVARIANT_DIM;
    let mut m6 = vec![vec![BigRational::zero(); n]; n];

    m6[0][0] = BigRational::one();
    for a in 0..NUM_BASES {
        let idx_a = 1 + a;
        m6[0][idx_a] = BigRational::one();
        m6[idx_a][0] = BigRational::one();
        m6[idx_a][idx_a] = BigRational::one();
    }

    let sixth = BigRational::new(1.into(), 6.into());
    for a in 0..NUM_BASES {
        for b in (a + 1)..NUM_BASES {
            let val = &sixth * sum_deg6_block_mod_sq(g, a, b)?;
            m6[1 + a][1 + b] = val.clone();
            m6[1 + b][1 + a] = val;
        }
    }

    populate_deg6_inv_pair_expectations(&mut m6, g, &pairs)?;
    populate_deg6_inv_pair_cross(&mut m6, g, &pairs);
    populate_deg6_inv_triples(&mut m6, g, &pairs, &triples)?;
    populate_deg6_inv_triple_cross(&mut m6, g, &triples);
    Ok(m6)
}

fn deg6_ext_basis_entry(
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

fn populate_deg6_ext_basis_block(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    a: usize,
    b: usize,
    sixth: &BigRational,
) -> Result<(), String> {
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let row_idx = a * DIM_HILBERT + i + 1;
            let col_idx = b * DIM_HILBERT + j + 1;
            m6[row_idx][col_idx] = deg6_ext_basis_entry(g, a, b, i, j, sixth)?;
        }
    }
    Ok(())
}

fn populate_deg6_ext_pairs(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    pairs: &[(usize, usize)],
    sixth: &BigRational,
) -> Result<(), String> {
    for (p_idx, &(a, b)) in pairs.iter().enumerate() {
        let col_p = 25 + p_idx;
        let mut diag_mod_sq = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let mod_sq = exact_rational(&entry.mul(&entry.conj()))?;
            diag_mod_sq += &mod_sq;
            let term = sixth * mod_sq;
            m6[a * DIM_HILBERT + i + 1][col_p] = term.clone();
            m6[col_p][a * DIM_HILBERT + i + 1] = term.clone();
            m6[b * DIM_HILBERT + i + 1][col_p] = term.clone();
            m6[col_p][b * DIM_HILBERT + i + 1] = term;
        }
        let exp_p = sixth * diag_mod_sq;
        m6[0][col_p] = exp_p.clone();
        m6[col_p][0] = exp_p.clone();
        m6[col_p][col_p] = exp_p;
    }
    Ok(())
}

fn populate_deg6_ext_triples(
    m6: &mut [Vec<BigRational>],
    g: &[Vec<Cyc24>],
    triples: &[(usize, usize, usize)],
    sixth: &BigRational,
) {
    for (t_idx, &(a, b, c)) in triples.iter().enumerate() {
        let col_t = 31 + t_idx;
        let mut bargmann_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_ca = &g[c * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let c_val = cyc_real_constant_coefficient(&e_ab.mul(e_bc).mul(e_ca));
            bargmann_sum += &c_val;
            let term = sixth * c_val;
            for base in [a, b, c] {
                m6[base * DIM_HILBERT + i + 1][col_t] = term.clone();
                m6[col_t][base * DIM_HILBERT + i + 1] = term.clone();
            }
        }
        let exp_t = sixth * bargmann_sum;
        m6[0][col_t] = exp_t.clone();
        m6[col_t][0] = exp_t.clone();
        m6[col_t][col_t] = if exp_t > BigRational::zero() {
            exp_t
        } else {
            BigRational::zero()
        };
    }
}

pub fn build_degree6_extended_diagnostic_matrix(
    g: &[Vec<Cyc24>],
) -> Result<Vec<Vec<BigRational>>, String> {
    validate_deg6_hermitian_gramian(g)?;
    let pairs = get_basis_pairs();
    let triples = get_basis_triples();
    let n = DEG6_EXTENDED_DIM;
    let mut m6 = vec![vec![BigRational::zero(); n]; n];
    let sixth = BigRational::new(1.into(), 6.into());

    m6[0][0] = BigRational::one();
    for idx in 0..GRAMIAN_DIM {
        m6[0][idx + 1] = sixth.clone();
        m6[idx + 1][0] = sixth.clone();
    }

    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            populate_deg6_ext_basis_block(&mut m6, g, a, b, &sixth)?;
        }
    }

    populate_deg6_ext_pairs(&mut m6, g, &pairs, &sixth)?;
    populate_deg6_ext_triples(&mut m6, g, &triples, &sixth);
    Ok(m6)
}
pub use crate::native::exact::dual_witness::DualWitnessRational;


pub fn build_invariant_dual_witness_x0(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); DEG6_INVARIANT_DIM];
    z[0] = -BigRational::one();
    z[1] = BigRational::one();
    z[4] = BigRational::one();

    let mut vectors = vec![z];
    let mut weights = vec![BigRational::one()];

    if strict {
        let eps = BigRational::new(1.into(), 50.into());
        for i in 0..DEG6_INVARIANT_DIM {
            let mut e = vec![BigRational::zero(); DEG6_INVARIANT_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational {
        dim: DEG6_INVARIANT_DIM,
        num_modes: vectors.len(),
        vectors,
        weights,
    }
}

pub fn build_extended_dual_witness_s6(strict: bool) -> DualWitnessRational {
    let mut z = vec![BigRational::zero(); DEG6_EXTENDED_DIM];
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
        for i in 0..DEG6_EXTENDED_DIM {
            let mut e = vec![BigRational::zero(); DEG6_EXTENDED_DIM];
            e[i] = BigRational::one();
            vectors.push(e);
            weights.push(eps.clone());
        }
    }

    DualWitnessRational {
        dim: DEG6_EXTENDED_DIM,
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
pub struct Degree6MomentReport {
    pub invariant_dimension: usize,
    pub extended_dimension: usize,
    pub candidate_x0_refuted: bool,
    pub candidate_s6_refuted: bool,
    pub details: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Degree6DiagnosticReport {
    pub schema_version: String,
    pub firewall: String,
    pub authority_effect: String,
    pub scope: String,
    pub dimension: usize,
    pub bases_count: usize,
    pub invariant_dim: usize,
    pub extended_dim: usize,
    pub moment_report: Degree6MomentReport,
    pub receipt_x0: DualWitnessReceipt,
    pub receipt_s6: DualWitnessReceipt,
    pub complete: bool,
    pub diagnostics_complete: bool,
    pub moment_semantics_verified: bool,
}

fn evaluate_deg6_witness_receipt(
    w: &DualWitnessRational,
    m6: &[Vec<BigRational>],
    dim: usize,
    label: &str,
    description: &str,
) -> Result<DualWitnessReceipt, String> {
    let inner = w.trace_inner(m6)?;
    if inner >= BigRational::zero() {
        return Err(format!(
            "Dual witness {label} matrix diagnostic failed: Tr(W * M) = {inner} >= 0"
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

pub fn evaluate_target_q3_diagnostics() -> Result<Degree6DiagnosticReport, String> {
    let g_diag = build_block_diagonal_gramian();
    let m6_diag = build_degree6_invariant_diagnostic_matrix(&g_diag)?;
    let w_x0 = build_invariant_dual_witness_x0(true);
    let receipt_x0 = evaluate_deg6_witness_receipt(
        &w_x0,
        &m6_diag,
        DEG6_INVARIANT_DIM,
        "X=0",
        "Experimental coefficient matrix for the block-diagonal X=0 fixture",
    )?;

    let g_synth = canonical_quad_gramian();
    let m6_synth = build_degree6_extended_diagnostic_matrix(&g_synth)?;
    let w_s6 = build_extended_dual_witness_s6(true);
    let receipt_s6 = evaluate_deg6_witness_receipt(
        &w_s6,
        &m6_synth,
        DEG6_EXTENDED_DIM,
        "S6",
        "Experimental coefficient matrix for the synthetic S6 fixture",
    )?;

    let moment_report = Degree6MomentReport {
        invariant_dimension: DEG6_INVARIANT_DIM,
        extended_dimension: DEG6_EXTENDED_DIM,
        candidate_x0_refuted: false,
        candidate_s6_refuted: false,
        details: "Exact matrix diagnostics only. Projector moment identities, positivity preservation, and a Lasserre relaxation are not established.".into(),
    };

    Ok(Degree6DiagnosticReport {
        schema_version: SCHEMA_VERSION.into(),
        firewall: FIREWALL.into(),
        authority_effect: AUTHORITY_EFFECT.into(),
        scope: SCOPE_STRING.into(),
        dimension: DIM_HILBERT,
        bases_count: NUM_BASES,
        invariant_dim: DEG6_INVARIANT_DIM,
        extended_dim: DEG6_EXTENDED_DIM,
        moment_report,
        receipt_x0,
        receipt_s6,
        complete: false,
        diagnostics_complete: true,
        moment_semantics_verified: false,
    })
}

pub fn solve_target_q3_degree6_certificate() -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}

pub fn build_degree6_invariant_moment_matrix(_g: &[Vec<Cyc24>]) -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}

pub fn build_degree6_extended_moment_matrix(_g: &[Vec<Cyc24>]) -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}
