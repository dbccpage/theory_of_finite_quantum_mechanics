
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use omega_number_theory::cyclotomic::Cyc24;

pub use crate::omega_native::exact::mub6_field::{inv_sqrt6, omega3_pow, omega6_pow};
pub const DIM_HILBERT: usize = 6;
pub const NUM_BASES_4: usize = 4;
pub const TOTAL_VECTORS_4: usize = NUM_BASES_4 * DIM_HILBERT;
pub const TAO_PHASES: [[i64; 6]; 6] = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
];
pub fn cyc24_to_rational(c: &Cyc24) -> BigRational {
    if c.a[1..].iter().all(|x| x.is_zero()) {
        c.a[0].clone()
    } else {
        panic!("Cyc24 element {:?} is not purely rational", c);
    }
}
pub fn basis_i6() -> Vec<[Cyc24; DIM_HILBERT]> {
    let mut cols = Vec::with_capacity(DIM_HILBERT);
    for col in 0..DIM_HILBERT {
        let mut v = std::array::from_fn(|_| Cyc24::zero());
        v[col] = Cyc24::rat(BigRational::one());
        cols.push(v);
    }
    cols
}
pub fn basis_f6() -> Vec<[Cyc24; DIM_HILBERT]> {
    let s = inv_sqrt6();
    let mut cols = Vec::with_capacity(DIM_HILBERT);
    for col in 0..DIM_HILBERT {
        let mut v = std::array::from_fn(|_| Cyc24::zero());
        for row in 0..DIM_HILBERT {
            v[row] = omega6_pow((row * col) as i64).mul(&s);
        }
        cols.push(v);
    }
    cols
}
pub fn basis_f6_2() -> Vec<[Cyc24; DIM_HILBERT]> {
    let s = inv_sqrt6();
    let mut cols = Vec::with_capacity(DIM_HILBERT);
    for col in 0..DIM_HILBERT {
        let mut v = std::array::from_fn(|_| Cyc24::zero());
        for row in 0..DIM_HILBERT {
            let exp = (row * col) as i64 + 2 * (row * row) as i64;
            v[row] = omega6_pow(exp).mul(&s);
        }
        cols.push(v);
    }
    cols
}
pub fn basis_s6() -> Vec<[Cyc24; DIM_HILBERT]> {
    let s = inv_sqrt6();
    let mut cols = Vec::with_capacity(DIM_HILBERT);
    for col in 0..DIM_HILBERT {
        let mut v = std::array::from_fn(|_| Cyc24::zero());
        for row in 0..DIM_HILBERT {
            v[row] = omega3_pow(TAO_PHASES[row][col]).mul(&s);
        }
        cols.push(v);
    }
    cols
}
pub fn canonical_candidate_bases() -> [Vec<[Cyc24; DIM_HILBERT]>; NUM_BASES_4] {
    [basis_i6(), basis_f6(), basis_f6_2(), basis_s6()]
}
pub fn inner_product(u: &[Cyc24; DIM_HILBERT], v: &[Cyc24; DIM_HILBERT]) -> Cyc24 {
    let mut sum = Cyc24::zero();
    for k in 0..DIM_HILBERT {
        sum = sum.add(&u[k].conj().mul(&v[k]));
    }
    sum
}
pub fn vector_norm_sq(v: &[Cyc24; DIM_HILBERT]) -> BigRational {
    let ip = inner_product(v, v);
    cyc24_to_rational(&ip)
}
pub fn inner_product_mod_sq(u: &[Cyc24; DIM_HILBERT], v: &[Cyc24; DIM_HILBERT]) -> BigRational {
    let ip = inner_product(u, v);
    let mod_sq_cyc = ip.mul(&ip.conj());
    cyc24_to_rational(&mod_sq_cyc)
}
pub fn inner_product_mod_4th(u: &[Cyc24; DIM_HILBERT], v: &[Cyc24; DIM_HILBERT]) -> BigRational {
    let mod_sq = inner_product_mod_sq(u, v);
    &mod_sq * &mod_sq
}
pub fn ideal_mub_frame_potential(d: usize, k: usize) -> BigRational {
    assert!(d > 0 && k > 0, "dimensions must be positive");
    let d = num_bigint::BigInt::from(d);
    let k = num_bigint::BigInt::from(k);
    BigRational::from_integer(&k * (d + &k - 1))
}
pub fn welch_bound_2(d: usize, m: usize) -> BigRational {
    assert!(d > 0, "dimension must be positive");
    let d = num_bigint::BigInt::from(d);
    let m = num_bigint::BigInt::from(m);
    let num = 2 * &m * &m;
    let den = &d * (&d + 1);
    BigRational::new(num, den)
}
pub fn compute_block_frame_potential(
    b1: &[[Cyc24; DIM_HILBERT]],
    b2: &[[Cyc24; DIM_HILBERT]],
) -> BigRational {
    let mut total = BigRational::zero();
    for u in b1 {
        for v in b2 {
            total += inner_product_mod_4th(u, v);
        }
    }
    total
}
pub fn compute_all_blocks(bases: &[Vec<[Cyc24; DIM_HILBERT]>]) -> Vec<Vec<BigRational>> {
    let k = bases.len();
    let mut mat = vec![vec![BigRational::zero(); k]; k];
    for i in 0..k {
        for j in 0..k {
            mat[i][j] = compute_block_frame_potential(&bases[i], &bases[j]);
        }
    }
    mat
}
pub fn compute_total_frame_potential(bases: &[Vec<[Cyc24; DIM_HILBERT]>]) -> BigRational {
    let mut sum = BigRational::zero();
    for b1 in bases {
        for b2 in bases {
            sum += compute_block_frame_potential(b1, b2);
        }
    }
    sum
}
pub fn etf_welch_coherence_sq(d: usize, m: usize) -> BigRational {
    assert!(d > 0 && m > 1 && m >= d, "invalid frame dimensions");
    let d = num_bigint::BigInt::from(d);
    let m = num_bigint::BigInt::from(m);
    let num = &m - &d;
    let den = &d * (&m - 1);
    BigRational::new(num, den)
}
pub fn mub_coherence_sq(d: usize) -> BigRational {
    assert!(d > 0, "dimension must be positive");
    BigRational::new(1.into(), d.into())
}
pub fn etf_mub_coherence_defect(d: usize, m: usize) -> BigRational {
    let c2 = etf_welch_coherence_sq(d, m);
    let mub = mub_coherence_sq(d);
    if c2 >= mub {
        c2 - mub
    } else {
        mub - c2
    }
}
pub fn non_unitary_povm_intra_penalty(eta: BigRational) -> BigRational {
    BigRational::from_integer(2.into()) * &eta * &eta
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FramePotentialCertificate {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall_line: String,
    pub scope: String,
    pub mub_nonexistence_established: bool,
    pub dimension: usize,
    pub bases_count: usize,
    pub total_vectors: usize,
    pub ideal_frame_potential: String,
    pub computed_frame_potential: String,
    pub frame_potential_defect: String,
    pub epsilon_frame: String,
    pub defect_strictly_positive: bool,
    pub welch_bound_t2: String,
    pub welch_bound_satisfied: bool,
    pub block_matrix: Vec<Vec<String>>,
    pub diagonal_blocks_sum: String,
    pub off_diagonal_blocks_sum: String,
    pub bases_internal_orthonormality: Vec<bool>,
    pub vectors_normalized: bool,
    pub non_unitary_povm_analysis: NonUnitaryPovmAnalysis,
    pub verified_sound: bool,
    pub sha256_digest: Option<String>,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct NonUnitaryPovmAnalysis {
    pub min_intra_orthogonality_penalty_factor: usize,
    pub etf_coherence_sq: String,
    pub mub_coherence_sq: String,
    pub coherence_defect: String,
    pub etf_mub_incompatibility_certified: bool,
    pub example_eta_1_over_10_penalty_positive: bool,
}
fn is_basis_pair_orthonormal(
    i: usize,
    j: usize,
    u: &[Cyc24; DIM_HILBERT],
    v: &[Cyc24; DIM_HILBERT],
) -> bool {
    let ip_sq = inner_product_mod_sq(u, v);
    if i == j {
        ip_sq == BigRational::one()
    } else {
        ip_sq.is_zero()
    }
}

fn check_single_basis(basis: &[[Cyc24; DIM_HILBERT]]) -> (bool, bool) {
    let mut normalized = true;
    let mut ortho = true;
    for (i, u) in basis.iter().enumerate() {
        if vector_norm_sq(u) != BigRational::one() {
            normalized = false;
        }
        for (j, v) in basis.iter().enumerate() {
            if !is_basis_pair_orthonormal(i, j, u, v) {
                ortho = false;
            }
        }
    }
    (normalized, ortho)
}

fn check_all_bases_orthonormality(bases: &[Vec<[Cyc24; DIM_HILBERT]>]) -> (bool, Vec<bool>) {
    let mut vectors_normalized = true;
    let mut bases_internal_orthonormality = Vec::with_capacity(bases.len());
    for basis in bases {
        let (norm_ok, ortho_ok) = check_single_basis(basis);
        if !norm_ok {
            vectors_normalized = false;
        }
        bases_internal_orthonormality.push(ortho_ok);
    }
    (vectors_normalized, bases_internal_orthonormality)
}

fn summarize_block_matrix(
    block_mat: &[Vec<BigRational>],
) -> (BigRational, BigRational, Vec<Vec<String>>) {
    let mut diag_sum = BigRational::zero();
    let mut off_diag_sum = BigRational::zero();
    let mut block_matrix_str = Vec::with_capacity(NUM_BASES_4);
    for i in 0..NUM_BASES_4 {
        let mut row_str = Vec::with_capacity(NUM_BASES_4);
        for j in 0..NUM_BASES_4 {
            let val = &block_mat[i][j];
            row_str.push(val.to_string());
            if i == j {
                diag_sum += val;
            } else {
                off_diag_sum += val;
            }
        }
        block_matrix_str.push(row_str);
    }
    (diag_sum, off_diag_sum, block_matrix_str)
}

fn all_flags_true(flags: &[bool]) -> bool {
    for &f in flags {
        if !f {
            return false;
        }
    }
    true
}

pub fn solve_frame_potential_certificate() -> FramePotentialCertificate {
    let bases = canonical_candidate_bases();
    let (vectors_normalized, bases_internal_orthonormality) =
        check_all_bases_orthonormality(&bases);

    let block_mat = compute_all_blocks(&bases);
    let (diag_sum, off_diag_sum, block_matrix_str) = summarize_block_matrix(&block_mat);

    let total_fp = &diag_sum + &off_diag_sum;
    let ideal_fp = ideal_mub_frame_potential(DIM_HILBERT, NUM_BASES_4);
    let defect = &total_fp - &ideal_fp;
    let defect_strictly_positive = defect > BigRational::zero();

    let welch_bound = welch_bound_2(DIM_HILBERT, TOTAL_VECTORS_4);
    let welch_bound_satisfied = total_fp >= welch_bound;

    let etf_c2 = etf_welch_coherence_sq(DIM_HILBERT, TOTAL_VECTORS_4);
    let mub_c2 = mub_coherence_sq(DIM_HILBERT);
    let coh_defect = etf_mub_coherence_defect(DIM_HILBERT, TOTAL_VECTORS_4);
    let etf_incompatible = coh_defect > BigRational::zero();

    let test_eta = BigRational::new(1.into(), 10.into());
    let test_penalty = non_unitary_povm_intra_penalty(test_eta);
    let povm_defect_pos = test_penalty > BigRational::zero();

    let checks = [
        vectors_normalized,
        all_flags_true(&bases_internal_orthonormality),
        defect_strictly_positive,
        welch_bound_satisfied,
        etf_incompatible,
        povm_defect_pos,
        total_fp == BigRational::from_integer(45.into()),
        ideal_fp == BigRational::from_integer(36.into()),
        defect == BigRational::from_integer(9.into()),
    ];
    let verified_sound = all_flags_true(&checks);

    FramePotentialCertificate {
        schema_version: "omega.mub.frame-potential.v2".to_string(),
        authority_effect: "None".to_string(),
        firewall_line: "stated region only; mints no authority".to_string(),
        scope: "fixed_four_basis_ensemble_and_eta_1_over_10_example".to_string(),
        mub_nonexistence_established: false,
        dimension: DIM_HILBERT,
        bases_count: NUM_BASES_4,
        total_vectors: TOTAL_VECTORS_4,
        ideal_frame_potential: ideal_fp.to_string(),
        computed_frame_potential: total_fp.to_string(),
        frame_potential_defect: defect.to_string(),
        epsilon_frame: "9".to_string(),
        defect_strictly_positive,
        welch_bound_t2: welch_bound.to_string(),
        welch_bound_satisfied,
        block_matrix: block_matrix_str,
        diagonal_blocks_sum: diag_sum.to_string(),
        off_diagonal_blocks_sum: off_diag_sum.to_string(),
        bases_internal_orthonormality,
        vectors_normalized,
        non_unitary_povm_analysis: NonUnitaryPovmAnalysis {
            min_intra_orthogonality_penalty_factor: 2,
            etf_coherence_sq: etf_c2.to_string(),
            mub_coherence_sq: mub_c2.to_string(),
            coherence_defect: coh_defect.to_string(),
            etf_mub_incompatibility_certified: etf_incompatible,
            example_eta_1_over_10_penalty_positive: povm_defect_pos,
        },
        verified_sound,
        sha256_digest: None,
    }
}
pub fn verify_frame_potential_certificate(cert: &FramePotentialCertificate) -> bool {
    let mut supplied = cert.clone();
    supplied.sha256_digest = None;
    supplied == solve_frame_potential_certificate()
}
