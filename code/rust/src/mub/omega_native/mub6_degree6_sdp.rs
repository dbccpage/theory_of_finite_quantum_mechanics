//! Target Q3: experimental rational coefficient-matrix diagnostics.
//!
//! AuthorityEffect: None.
//!
//! The proposed lifts are not validated projector moment matrices. They fail a
//! repeated-standard-basis positivity control, and their real cyclotomic terms need
//! not be rational. Diagnostic builders explicitly project onto the constant
//! power-basis coefficient. This is not an ordered-field embedding or a
//! positivity-preserving map. Negative traces concern only the constructed rational
//! matrices; they do not certify a candidate or a Lasserre relaxation.
//! The former certification entry points fail closed.

use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, exact_rational, DIM_HILBERT, GRAMIAN_DIM, NUM_BASES,
};
pub use crate::omega_native::exact::mub6_quad_sdp::{
    cyc_real_constant_coefficient, cyc_real_rational, get_basis_pairs, get_basis_triples,
};
use linear_algebra::exact_ldlt::ldlt_pivots_strictly_positive_rational;
use omega_number_theory::cyclotomic::Cyc24;

pub const SCHEMA_VERSION: &str = "omega.mub.degree6-diagnostics.v2";
pub const SCOPE_STRING: &str = "experimental_coefficient_projection_only_no_moment_soundness";

pub const DEG6_INVARIANT_DIM: usize = 21;
pub const DEG6_EXTENDED_DIM: usize = 35;

/// Experimental 21x21 coefficient matrix; projector moment semantics are unverified.
pub fn build_degree6_invariant_diagnostic_matrix(
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
    let n = DEG6_INVARIANT_DIM;
    let mut m6 = vec![vec![BigRational::zero(); n]; n];

    // 1. Base identity <1>
    m6[0][0] = BigRational::one();

    // 2. Linear projector sums A_a (indices 1..4)
    for a in 0..NUM_BASES {
        let idx_a = 1 + a;
        m6[0][idx_a] = BigRational::one();
        m6[idx_a][0] = BigRational::one();
        m6[idx_a][idx_a] = BigRational::one();
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
            m6[idx_a][idx_b] = val.clone();
            m6[idx_b][idx_a] = val;
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
        m6[0][idx_p] = exp_p.clone();
        m6[idx_p][0] = exp_p.clone();
        m6[0][idx_q] = exp_q.clone();
        m6[idx_q][0] = exp_q.clone();

        // Moments with A_a and A_b
        m6[1 + a][idx_p] = exp_p.clone();
        m6[idx_p][1 + a] = exp_p.clone();
        m6[1 + b][idx_p] = exp_p.clone();
        m6[idx_p][1 + b] = exp_p.clone();

        m6[1 + a][idx_q] = exp_q.clone();
        m6[idx_q][1 + a] = exp_q.clone();
        m6[1 + b][idx_q] = exp_q.clone();
        m6[idx_q][1 + b] = exp_q.clone();

        for c in 0..NUM_BASES {
            if c != a && c != b {
                m6[1 + c][idx_p] = exp_p.clone();
                m6[idx_p][1 + c] = exp_p.clone();
                m6[1 + c][idx_q] = exp_q.clone();
                m6[idx_q][1 + c] = exp_q.clone();
            }
        }

        // Diagonal moments <P_{ab}^2> and <Q_{ab}^2>
        m6[idx_p][idx_p] = exp_p;
        m6[idx_q][idx_q] = exp_q;
    }

    // Cross-pair interactions
    for (p1, &(a1, b1)) in pairs.iter().enumerate() {
        for (p2, &(a2, b2)) in pairs.iter().enumerate() {
            if p1 < p2 {
                let idx_p1 = 5 + p1;
                let idx_p2 = 5 + p2;
                let mut val = BigRational::zero();
                for i in 0..DIM_HILBERT {
                    let e1 = &g[a1 * DIM_HILBERT + i][b1 * DIM_HILBERT + i];
                    let e2 = &g[a2 * DIM_HILBERT + i][b2 * DIM_HILBERT + i];
                    val += cyc_real_constant_coefficient(&e1.mul(&e2.conj()));
                }
                let val = val / BigRational::from_integer(6.into());
                m6[idx_p1][idx_p2] = val.clone();
                m6[idx_p2][idx_p1] = val;
            }
        }
    }

    // 4. Degree-3 Triples T_{abc} (indices 17..20)
    let sixth = BigRational::new(1.into(), 6.into());
    for (t_idx, &(a, b, c)) in triples.iter().enumerate() {
        let idx_t = 17 + t_idx;

        let mut bargmann_sum = BigRational::zero();
        let mut diag_cubed_sum = BigRational::zero();
        for i in 0..DIM_HILBERT {
            let e_ab = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + i];
            let e_bc = &g[b * DIM_HILBERT + i][c * DIM_HILBERT + i];
            let e_ca = &g[c * DIM_HILBERT + i][a * DIM_HILBERT + i];
            let cycle = e_ab.mul(e_bc).mul(e_ca);
            let c_val = cyc_real_constant_coefficient(&cycle);
            bargmann_sum += c_val;
            diag_cubed_sum += exact_rational(&e_ab.mul(&e_ab.conj()))?
                * exact_rational(&e_bc.mul(&e_bc.conj()))?
                * exact_rational(&e_ca.mul(&e_ca.conj()))?;
        }

        let exp_t = &sixth * &bargmann_sum;

        // Moment with 1
        m6[0][idx_t] = exp_t.clone();
        m6[idx_t][0] = exp_t.clone();

        // Moment with A_d
        for d in 0..NUM_BASES {
            m6[1 + d][idx_t] = exp_t.clone();
            m6[idx_t][1 + d] = exp_t.clone();
        }

        // Moment with P_{ab}
        for (p_idx, &(p_a, p_b)) in pairs.iter().enumerate() {
            let idx_p = 5 + p_idx;
            let idx_q = 11 + p_idx;
            if (p_a == a || p_a == b || p_a == c) && (p_b == a || p_b == b || p_b == c) {
                m6[idx_p][idx_t] = exp_t.clone();
                m6[idx_t][idx_p] = exp_t.clone();
            } else {
                m6[idx_p][idx_t] = BigRational::zero();
                m6[idx_t][idx_p] = BigRational::zero();
            }

            let q_val = &exp_t - &m6[idx_p][idx_t];
            m6[idx_q][idx_t] = q_val.clone();
            m6[idx_t][idx_q] = q_val;
        }

        // Diagonal moment <T_{abc}^2>
        let exp_t_diag = &sixth * diag_cubed_sum;
        m6[idx_t][idx_t] = if exp_t_diag > BigRational::zero() {
            exp_t_diag
        } else {
            exp_t
        };
    }

    for (t1, &(a1, b1, c1)) in triples.iter().enumerate() {
        for (t2, &(a2, b2, c2)) in triples.iter().enumerate() {
            if t1 < t2 {
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
                let val = &sixth * val;
                m6[17 + t1][17 + t2] = val.clone();
                m6[17 + t2][17 + t1] = val;
            }
        }
    }
    Ok(m6)
}

/// Experimental 35x35 coefficient matrix; projector moment semantics are unverified.
pub fn build_degree6_extended_diagnostic_matrix(
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
    let n = DEG6_EXTENDED_DIM;
    let mut m6 = vec![vec![BigRational::zero(); n]; n];
    let sixth = BigRational::new(1.into(), 6.into());

    // 1. 25x25 Degree-2 block
    m6[0][0] = BigRational::one();
    for idx in 0..GRAMIAN_DIM {
        m6[0][idx + 1] = sixth.clone();
        m6[idx + 1][0] = sixth.clone();
    }

    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            for i in 0..DIM_HILBERT {
                for j in 0..DIM_HILBERT {
                    let row_idx = a * DIM_HILBERT + i + 1;
                    let col_idx = b * DIM_HILBERT + j + 1;
                    if a == b {
                        m6[row_idx][col_idx] = if i == j {
                            sixth.clone()
                        } else {
                            BigRational::zero()
                        };
                    } else {
                        let g_entry = &g[a * DIM_HILBERT + i][b * DIM_HILBERT + j];
                        let mod_sq = exact_rational(&g_entry.mul(&g_entry.conj()))?;
                        m6[row_idx][col_idx] = &sixth * &mod_sq;
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

            m6[a * DIM_HILBERT + i + 1][col_p] = &sixth * &mod_sq;
            m6[col_p][a * DIM_HILBERT + i + 1] = &sixth * &mod_sq;
            m6[b * DIM_HILBERT + i + 1][col_p] = &sixth * &mod_sq;
            m6[col_p][b * DIM_HILBERT + i + 1] = &sixth * &mod_sq;
        }

        let exp_p = &sixth * &diag_mod_sq;
        m6[0][col_p] = exp_p.clone();
        m6[col_p][0] = exp_p.clone();
        m6[col_p][col_p] = exp_p;
    }

    // 3. Triple blocks T_{abc} (indices 31..34)
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

            m6[a * DIM_HILBERT + i + 1][col_t] = &sixth * &c_val;
            m6[col_t][a * DIM_HILBERT + i + 1] = &sixth * &c_val;
            m6[b * DIM_HILBERT + i + 1][col_t] = &sixth * &c_val;
            m6[col_t][b * DIM_HILBERT + i + 1] = &sixth * &c_val;
            m6[c * DIM_HILBERT + i + 1][col_t] = &sixth * &c_val;
            m6[col_t][c * DIM_HILBERT + i + 1] = &sixth * &c_val;
        }

        let exp_t = &sixth * &bargmann_sum;
        m6[0][col_t] = exp_t.clone();
        m6[col_t][0] = exp_t.clone();
        m6[col_t][col_t] = if exp_t > BigRational::zero() {
            exp_t
        } else {
            BigRational::zero()
        };
    }

    Ok(m6)
}
pub use crate::omega_native::exact::dual_witness::DualWitnessRational;


/// PSD weight matrix for the experimental X=0 coefficient matrix.
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

/// PSD weight matrix for the experimental S6 coefficient matrix.
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

/// Exact trace and positive-pivot diagnostics for a specified rational matrix.
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

/// Moment report.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Degree6MomentReport {
    pub invariant_dimension: usize,
    pub extended_dimension: usize,
    pub candidate_x0_refuted: bool,
    pub candidate_s6_refuted: bool,
    pub details: String,
}

/// Diagnostic receipt; complete and moment_semantics_verified remain false.
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

/// Evaluate two experimental coefficient matrices without candidate certification.
pub fn evaluate_target_q3_diagnostics() -> Result<Degree6DiagnosticReport, String> {
    // 1. Diagnose the X=0 coefficient matrix
    let g_diag = build_block_diagonal_gramian();
    let m6_diag = build_degree6_invariant_diagnostic_matrix(&g_diag)?;
    let w_x0 = build_invariant_dual_witness_x0(true);
    let inner_x0 = w_x0.trace_inner(&m6_diag)?;
    if inner_x0 >= BigRational::zero() {
        return Err(format!(
            "Dual witness X=0 matrix diagnostic failed: Tr(W * M) = {} >= 0",
            inner_x0
        ));
    }

    let w_mat_x0 = w_x0.to_full_matrix()?;
    let pivots_x0 = ldlt_pivots_strictly_positive_rational(&w_mat_x0)?;

    let receipt_x0 = DualWitnessReceipt {
        target_description: "Experimental coefficient matrix for the block-diagonal X=0 fixture"
            .into(),
        witness_dimension: DEG6_INVARIANT_DIM,
        inner_product: inner_x0.to_string(),
        inner_product_num: inner_x0.numer().to_string(),
        inner_product_den: inner_x0.denom().to_string(),
        strictly_negative: true,
        pivots_strictly_positive: true,
        pivots: pivots_x0.iter().map(|p| p.to_string()).collect(),
    };

    // 2. Diagnose the synthetic S6 coefficient matrix
    let g_synth = canonical_quad_gramian();
    let m6_synth = build_degree6_extended_diagnostic_matrix(&g_synth)?;
    let w_s6 = build_extended_dual_witness_s6(true);
    let inner_s6 = w_s6.trace_inner(&m6_synth)?;
    if inner_s6 >= BigRational::zero() {
        return Err(format!(
            "Dual witness S6 matrix diagnostic failed: Tr(W * M) = {} >= 0",
            inner_s6
        ));
    }

    let w_mat_s6 = w_s6.to_full_matrix()?;
    let pivots_s6 = ldlt_pivots_strictly_positive_rational(&w_mat_s6)?;

    let receipt_s6 = DualWitnessReceipt {
        target_description: "Experimental coefficient matrix for the synthetic S6 fixture".into(),
        witness_dimension: DEG6_EXTENDED_DIM,
        inner_product: inner_s6.to_string(),
        inner_product_num: inner_s6.numer().to_string(),
        inner_product_den: inner_s6.denom().to_string(),
        strictly_negative: true,
        pivots_strictly_positive: true,
        pivots: pivots_s6.iter().map(|p| p.to_string()).collect(),
    };

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

/// Certification is unavailable; use evaluate_target_q3_diagnostics for exploration.
pub fn solve_target_q3_degree6_certificate() -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}

/// No sound projector-moment construction is supplied.
pub fn build_degree6_invariant_moment_matrix(_g: &[Vec<Cyc24>]) -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}

/// No sound projector-moment construction is supplied.
pub fn build_degree6_extended_moment_matrix(_g: &[Vec<Cyc24>]) -> Result<(), String> {
    Err("MissingProofObligation: valid projector moment identities and a positivity-preserving exact field representation are required".into())
}
