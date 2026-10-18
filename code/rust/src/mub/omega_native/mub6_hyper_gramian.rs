//! Exact diagnostics for the single synthetic block matrix constructed below.
//! The blocks are independently prescribed; they are not a parameterization of
//! every MUB system. See research/mub6_frontier_synthesis.md and the matching
//! test_*_verifier.rs for the scope and exact replay checks.
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, inner};
pub use crate::omega_native::exact::mub6_field::{inv_sqrt6, omega3_pow, omega6_pow, sqrt6};
pub use crate::omega_native::exact::mub6_quad_sdp::tao_s6_block;
use crate::omega_native::exact::mub6_quad_sdp::{exact_rational, ldlt_pivots_rational};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
pub const DIM_HILBERT: usize = 6;
pub const NUM_BASES_5: usize = 5;
pub const GRAMIAN_DIM_5: usize = NUM_BASES_5 * DIM_HILBERT;
pub const NUM_BASES_6: usize = 6;
pub const GRAMIAN_DIM_6: usize = NUM_BASES_6 * DIM_HILBERT;
pub const TAO_PHASES: [[i64; 6]; 6] = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
];
pub fn fourier6_block() -> Vec<Vec<Cyc24>> {
    let s = inv_sqrt6();
    let mut mat = vec![vec![Cyc24::zero(); DIM_HILBERT]; DIM_HILBERT];
    for j in 0..DIM_HILBERT {
        for k in 0..DIM_HILBERT {
            mat[j][k] = omega6_pow((j * k) as i64).mul(&s);
        }
    }
    mat
}
pub fn chirp_fourier6_block(alpha: i64) -> Vec<Vec<Cyc24>> {
    let s = inv_sqrt6();
    let mut mat = vec![vec![Cyc24::zero(); DIM_HILBERT]; DIM_HILBERT];
    for j in 0..DIM_HILBERT {
        for k in 0..DIM_HILBERT {
            let exp = (j * k) as i64 + alpha.rem_euclid(6) * (j * j) as i64;
            mat[j][k] = omega6_pow(exp).mul(&s);
        }
    }
    mat
}
pub fn dita_d6_block(dx: i64, dy: i64) -> Vec<Vec<Cyc24>> {
    let s = inv_sqrt6();
    let dphase = [
        Cyc24::rat(BigRational::one()),
        Cyc24::zeta24(dx.rem_euclid(24) as i32),
        Cyc24::zeta24(dy.rem_euclid(24) as i32),
    ];
    let mut mat = vec![vec![Cyc24::zero(); DIM_HILBERT]; DIM_HILBERT];
    for col in 0..DIM_HILBERT {
        if col < 3 {
            for j in 0..3 {
                let e = omega3_pow((j * col) as i64).mul(&s);
                mat[j][col] = e.clone();
                mat[j + 3][col] = e;
            }
        } else {
            let m = col - 3;
            for j in 0..3 {
                let e = dphase[j].mul(&omega3_pow((j * m) as i64)).mul(&s);
                mat[j][col] = e.clone();
                mat[j + 3][col] = e.neg();
            }
        }
    }
    mat
}
pub fn canonical_5mub_gramian() -> Vec<Vec<Cyc24>> {
    let cols = canonical_triple_exact(); // 18 columns: 0..6 B0, 6..12 B1, 12..18 B2
    let s6 = tao_s6_block();
    let d6 = dita_d6_block(0, 0);
    let mut g = vec![vec![Cyc24::zero(); GRAMIAN_DIM_5]; GRAMIAN_DIM_5];

    // Blocks 0, 1, 2: pairwise Gramian from canonical triple T0
    for a in 0..3 {
        for b in 0..3 {
            for j in 0..DIM_HILBERT {
                for k in 0..DIM_HILBERT {
                    let u_col = &cols[a * DIM_HILBERT + j];
                    let v_col = &cols[b * DIM_HILBERT + k];
                    g[a * DIM_HILBERT + j][b * DIM_HILBERT + k] = inner(u_col, v_col);
                }
            }
        }
    }

    // Diagonal identity for blocks 3 and 4
    let one = Cyc24::rat(BigRational::one());
    for b in 3..5 {
        for j in 0..DIM_HILBERT {
            g[b * DIM_HILBERT + j][b * DIM_HILBERT + j] = one.clone();
        }
    }

    // Off-diagonal block 3: G_a3 = S6 and G_3a = S6^\dagger for a in 0..3
    for a in 0..3 {
        for j in 0..DIM_HILBERT {
            for k in 0..DIM_HILBERT {
                let entry = s6[j][k].clone();
                g[a * DIM_HILBERT + j][3 * DIM_HILBERT + k] = entry.clone();
                g[3 * DIM_HILBERT + k][a * DIM_HILBERT + j] = entry.conj();
            }
        }
    }

    // Off-diagonal block 4: G_a4 = D6(0, 0) and G_4a = D6(0, 0)^\dagger for a in 0..4
    for a in 0..4 {
        for j in 0..DIM_HILBERT {
            for k in 0..DIM_HILBERT {
                let entry = d6[j][k].clone();
                g[a * DIM_HILBERT + j][4 * DIM_HILBERT + k] = entry.clone();
                g[4 * DIM_HILBERT + k][a * DIM_HILBERT + j] = entry.conj();
            }
        }
    }

    g
}
pub fn canonical_6mub_gramian() -> Vec<Vec<Cyc24>> {
    let g5 = canonical_5mub_gramian();
    let f6_1 = chirp_fourier6_block(1);
    let mut g = vec![vec![Cyc24::zero(); GRAMIAN_DIM_6]; GRAMIAN_DIM_6];

    // Copy leading 30 x 30 block from G^(5)
    for i in 0..GRAMIAN_DIM_5 {
        for j in 0..GRAMIAN_DIM_5 {
            g[i][j] = g5[i][j].clone();
        }
    }

    // Diagonal identity for block 5
    let one = Cyc24::rat(BigRational::one());
    for j in 0..DIM_HILBERT {
        g[5 * DIM_HILBERT + j][5 * DIM_HILBERT + j] = one.clone();
    }

    // Off-diagonal block 5: G_a5 = F6^(1) and G_5a = (F6^(1))^\dagger for a in 0..5
    for a in 0..5 {
        for j in 0..DIM_HILBERT {
            for k in 0..DIM_HILBERT {
                let entry = f6_1[j][k].clone();
                g[a * DIM_HILBERT + j][5 * DIM_HILBERT + k] = entry.clone();
                g[5 * DIM_HILBERT + k][a * DIM_HILBERT + j] = entry.conj();
            }
        }
    }

    g
}
pub fn dual_witness_vector_5() -> Vec<Cyc24> {
    let mut v = vec![Cyc24::zero(); GRAMIAN_DIM_5];

    let v1_int = [-3i64, 1, -2, -2, 2, 1];
    for (i, &val) in v1_int.iter().enumerate() {
        v[DIM_HILBERT + i] = Cyc24::rat(ri(val));
    }

    let v2_int = [-3i64, 1, 1, -1, 3, 3];
    for (i, &val) in v2_int.iter().enumerate() {
        v[2 * DIM_HILBERT + i] = Cyc24::rat(ri(val));
    }

    let s6 = sqrt6();
    let v3_int = [-1i64, 1, 1, 1, 1, 1];
    for (i, &val) in v3_int.iter().enumerate() {
        v[3 * DIM_HILBERT + i] = s6.mul(&Cyc24::rat(ri(val)));
    }

    v
}
pub fn dual_witness_vector_6() -> Vec<Cyc24> {
    let mut v = vec![Cyc24::zero(); GRAMIAN_DIM_6];

    let v1_int = [-3i64, 1, -2, -2, 2, 1];
    for (i, &val) in v1_int.iter().enumerate() {
        v[DIM_HILBERT + i] = Cyc24::rat(ri(val));
    }

    let v2_int = [-3i64, 1, 1, -1, 3, 3];
    for (i, &val) in v2_int.iter().enumerate() {
        v[2 * DIM_HILBERT + i] = Cyc24::rat(ri(val));
    }

    let s6 = sqrt6();
    let v3_int = [-1i64, 1, 1, 1, 1, 1];
    for (i, &val) in v3_int.iter().enumerate() {
        v[3 * DIM_HILBERT + i] = s6.mul(&Cyc24::rat(ri(val)));
    }

    v
}
pub fn dual_certificate_matrix_5(strict: bool) -> Vec<Vec<Cyc24>> {
    let v = dual_witness_vector_5();
    let mut w = vec![vec![Cyc24::zero(); GRAMIAN_DIM_5]; GRAMIAN_DIM_5];

    for i in 0..GRAMIAN_DIM_5 {
        for j in 0..GRAMIAN_DIM_5 {
            w[i][j] = v[i].mul(&v[j].conj());
        }
    }

    if strict {
        let eps = Cyc24::rat(BigRational::new(1.into(), 30.into()));
        for i in 0..GRAMIAN_DIM_5 {
            w[i][i] = w[i][i].add(&eps);
        }
    }

    w
}
pub fn dual_certificate_matrix_6(strict: bool) -> Vec<Vec<Cyc24>> {
    let v = dual_witness_vector_6();
    let mut w = vec![vec![Cyc24::zero(); GRAMIAN_DIM_6]; GRAMIAN_DIM_6];

    for i in 0..GRAMIAN_DIM_6 {
        for j in 0..GRAMIAN_DIM_6 {
            w[i][j] = v[i].mul(&v[j].conj());
        }
    }

    if strict {
        let eps = Cyc24::rat(BigRational::new(1.into(), 36.into()));
        for i in 0..GRAMIAN_DIM_6 {
            w[i][i] = w[i][i].add(&eps);
        }
    }

    w
}
pub fn trace_inner_product(w: &[Vec<Cyc24>], g: &[Vec<Cyc24>]) -> Cyc24 {
    let n = w.len();
    let mut acc = Cyc24::zero();
    for i in 0..n {
        for j in 0..n {
            acc = acc.add(&w[i][j].mul(&g[j][i]));
        }
    }
    acc
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GramianStructureReport {
    pub bases_count: usize,
    pub gramian_dim: usize,
    pub diagonal_blocks_identity: bool,
    pub off_diagonal_blocks_modulus_sixth: bool,
    pub hermitian_exact: bool,
    pub verified_sound: bool,
}
pub fn verify_hyper_gramian_structure(
    g: &[Vec<Cyc24>],
    num_bases: usize,
) -> GramianStructureReport {
    let Some(expected_dim) = num_bases.checked_mul(DIM_HILBERT) else {
        return GramianStructureReport {
            bases_count: num_bases,
            gramian_dim: 0,
            diagonal_blocks_identity: false,
            off_diagonal_blocks_modulus_sixth: false,
            hermitian_exact: false,
            verified_sound: false,
        };
    };
    if num_bases == 0 || g.len() != expected_dim || g.iter().any(|row| row.len() != expected_dim) {
        return GramianStructureReport {
            bases_count: num_bases,
            gramian_dim: expected_dim,
            diagonal_blocks_identity: false,
            off_diagonal_blocks_modulus_sixth: false,
            hermitian_exact: false,
            verified_sound: false,
        };
    }
    let sixth = Cyc24::rat(BigRational::new(1.into(), 6.into()));
    let one = Cyc24::rat(BigRational::one());
    let zero = Cyc24::zero();
    let dim = num_bases * DIM_HILBERT;

    // 1. Diagonal blocks are identity
    let mut diag_ok = true;
    for a in 0..num_bases {
        for i in 0..DIM_HILBERT {
            for j in 0..DIM_HILBERT {
                let idx_i = a * DIM_HILBERT + i;
                let idx_j = a * DIM_HILBERT + j;
                if i == j {
                    if g[idx_i][idx_j] != one {
                        diag_ok = false;
                    }
                } else if g[idx_i][idx_j] != zero {
                    diag_ok = false;
                }
            }
        }
    }

    // 2. Off-diagonal blocks have modulus squared = 1/6
    let mut modulus_ok = true;
    for a in 0..num_bases {
        for b in 0..num_bases {
            if a == b {
                continue;
            }
            for i in 0..DIM_HILBERT {
                for j in 0..DIM_HILBERT {
                    let idx_i = a * DIM_HILBERT + i;
                    let idx_j = b * DIM_HILBERT + j;
                    let entry = &g[idx_i][idx_j];
                    let mod_sq = entry.mul(&entry.conj());
                    if mod_sq != sixth {
                        modulus_ok = false;
                    }
                }
            }
        }
    }

    // 3. Exactly Hermitian
    let mut herm_ok = true;
    for i in 0..dim {
        for j in 0..dim {
            if g[j][i] != g[i][j].conj() {
                herm_ok = false;
            }
        }
    }

    let sound = diag_ok && modulus_ok && herm_ok;
    GramianStructureReport {
        bases_count: num_bases,
        gramian_dim: dim,
        diagonal_blocks_identity: diag_ok,
        off_diagonal_blocks_modulus_sixth: modulus_ok,
        hermitian_exact: herm_ok,
        verified_sound: sound,
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MubHyperGramianCertificate {
    pub schema_version: &'static str,
    pub dimension: usize,
    pub bases_count_5: usize,
    pub gramian_dim_5: usize,
    pub bases_count_6: usize,
    pub gramian_dim_6: usize,
    pub gramian_5_structure: GramianStructureReport,
    pub gramian_6_structure: GramianStructureReport,

    // 5-MUB certificates
    pub mub5_rank1_inner_product: String,
    pub mub5_rank1_strictly_negative: bool,
    pub mub5_strict_inner_product: String,
    pub mub5_strict_strictly_negative: bool,
    pub mub5_strict_regularizer: String,
    pub mub5_rank1_pivots: Vec<String>,
    pub mub5_rank1_pivots_nonnegative: bool,
    pub mub5_strict_pivots: Vec<String>,
    pub mub5_strict_pivots_strictly_positive: bool,

    // 6-MUB certificates
    pub mub6_rank1_inner_product: String,
    pub mub6_rank1_strictly_negative: bool,
    pub mub6_strict_inner_product: String,
    pub mub6_strict_strictly_negative: bool,
    pub mub6_strict_regularizer: String,
    pub mub6_rank1_pivots: Vec<String>,
    pub mub6_rank1_pivots_nonnegative: bool,
    pub mub6_strict_pivots: Vec<String>,
    pub mub6_strict_pivots_strictly_positive: bool,

    // Global assertions
    pub dual_certificates_psd_certified: bool,
    pub fixed_matrix_5_witness_checked: bool,
    pub fixed_matrix_6_witness_checked: bool,
    pub constructed_matrix_5_not_psd: bool,
    pub constructed_matrix_6_not_psd: bool,
    pub complete: bool,
    pub scope: &'static str,
    pub mub_nonexistence_established: bool,
    pub firewall: &'static str,
    pub authority_effect: &'static str,
    pub sha256_digest: Option<String>,
}
pub fn solve_hyper_gramian_certificate() -> MubHyperGramianCertificate {
    // 1. 5-MUB formulation and verification
    let g5 = canonical_5mub_gramian();
    let struct5 = verify_hyper_gramian_structure(&g5, NUM_BASES_5);

    let w5_rank1 = dual_certificate_matrix_5(false);
    let w5_strict = dual_certificate_matrix_5(true);

    let inner5_rank1 = trace_inner_product(&w5_rank1, &g5);
    let inner5_strict = trace_inner_product(&w5_strict, &g5);

    let rat5_rank1 = exact_rational(&inner5_rank1).expect("fixed witness trace must be rational");
    let rat5_strict = exact_rational(&inner5_strict).expect("fixed witness trace must be rational");

    let rank1_5_neg = rat5_rank1 < BigRational::zero();
    let strict_5_neg = rat5_strict < BigRational::zero();

    let pivots5_rank1 =
        ldlt_pivots_rational(&w5_rank1).expect("LDL^T decomposition failed for W_rank1^(5)");
    let all_nonneg5 = pivots5_rank1.iter().all(|p| p >= &BigRational::zero());

    let pivots5_strict =
        ldlt_pivots_rational(&w5_strict).expect("LDL^T decomposition failed for W_strict^(5)");
    let all_pos5 = pivots5_strict.iter().all(|p| p > &BigRational::zero());

    // 2. 6-MUB formulation and verification
    let g6 = canonical_6mub_gramian();
    let struct6 = verify_hyper_gramian_structure(&g6, NUM_BASES_6);

    let w6_rank1 = dual_certificate_matrix_6(false);
    let w6_strict = dual_certificate_matrix_6(true);

    let inner6_rank1 = trace_inner_product(&w6_rank1, &g6);
    let inner6_strict = trace_inner_product(&w6_strict, &g6);

    let rat6_rank1 = exact_rational(&inner6_rank1).expect("fixed witness trace must be rational");
    let rat6_strict = exact_rational(&inner6_strict).expect("fixed witness trace must be rational");

    let rank1_6_neg = rat6_rank1 < BigRational::zero();
    let strict_6_neg = rat6_strict < BigRational::zero();

    let pivots6_rank1 =
        ldlt_pivots_rational(&w6_rank1).expect("LDL^T decomposition failed for W_rank1^(6)");
    let all_nonneg6 = pivots6_rank1.iter().all(|p| p >= &BigRational::zero());

    let pivots6_strict =
        ldlt_pivots_rational(&w6_strict).expect("LDL^T decomposition failed for W_strict^(6)");
    let all_pos6 = pivots6_strict.iter().all(|p| p > &BigRational::zero());

    let psd_ok = all_nonneg5 && all_pos5 && all_nonneg6 && all_pos6;
    let contra5 = struct5.verified_sound && rank1_5_neg && strict_5_neg && all_pos5;
    let contra6 = struct6.verified_sound && rank1_6_neg && strict_6_neg && all_pos6;
    let complete = contra5 && contra6;

    MubHyperGramianCertificate {
        schema_version: "omega.mub.hyper-gramian-sdp.v2",
        dimension: DIM_HILBERT,
        bases_count_5: NUM_BASES_5,
        gramian_dim_5: GRAMIAN_DIM_5,
        bases_count_6: NUM_BASES_6,
        gramian_dim_6: GRAMIAN_DIM_6,
        gramian_5_structure: struct5,
        gramian_6_structure: struct6,

        mub5_rank1_inner_product: rat5_rank1.to_string(),
        mub5_rank1_strictly_negative: rank1_5_neg,
        mub5_strict_inner_product: rat5_strict.to_string(),
        mub5_strict_strictly_negative: strict_5_neg,
        mub5_strict_regularizer: "1/30".to_string(),
        mub5_rank1_pivots: pivots5_rank1.iter().map(|p| p.to_string()).collect(),
        mub5_rank1_pivots_nonnegative: all_nonneg5,
        mub5_strict_pivots: pivots5_strict.iter().map(|p| p.to_string()).collect(),
        mub5_strict_pivots_strictly_positive: all_pos5,

        mub6_rank1_inner_product: rat6_rank1.to_string(),
        mub6_rank1_strictly_negative: rank1_6_neg,
        mub6_strict_inner_product: rat6_strict.to_string(),
        mub6_strict_strictly_negative: strict_6_neg,
        mub6_strict_regularizer: "1/36".to_string(),
        mub6_rank1_pivots: pivots6_rank1.iter().map(|p| p.to_string()).collect(),
        mub6_rank1_pivots_nonnegative: all_nonneg6,
        mub6_strict_pivots: pivots6_strict.iter().map(|p| p.to_string()).collect(),
        mub6_strict_pivots_strictly_positive: all_pos6,

        dual_certificates_psd_certified: psd_ok,
        fixed_matrix_5_witness_checked: contra5,
        fixed_matrix_6_witness_checked: contra6,
        constructed_matrix_5_not_psd: contra5,
        constructed_matrix_6_not_psd: contra6,
        complete,
        scope: "two_synthetic_block_matrices",
        mub_nonexistence_established: false,
        firewall: "stated region only; mints no authority",
        authority_effect: "None",
        sha256_digest: None,
    }
}
