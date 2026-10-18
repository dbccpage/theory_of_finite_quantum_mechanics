
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::{inner, ExactVec, D};
use crate::omega_native::exact::mub6_constants::base_gap;
use crate::omega_native::exact::mub6_f6_chart::f6_family_columns;
use crate::omega_native::exact::mub6_matrix6::Matrix6;
use crate::omega_native::exact::mub6_tao_chart::tao_s6_matrix;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;

pub const TOTAL_ZEROREL_EQUATIONS: usize = 108;

pub type BasisCyc = [ExactVec; D];

#[derive(Clone, Debug)]
pub struct MuTripleCyc {
    pub b0: BasisCyc,
    pub b1: BasisCyc,
    pub b2: BasisCyc,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RelIndex {
    pub basis: usize,
    pub row: usize,
    pub col: usize,
}

pub fn standard_basis() -> BasisCyc {
    std::array::from_fn(|col| {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[col] = Cyc24::zeta24(0);
        v
    })
}

pub use crate::omega_native::exact::mub6_field::inv_sqrt6;

pub fn transpose_matrix(m: &Matrix6) -> Matrix6 {
    std::array::from_fn(|r| std::array::from_fn(|c| m[c][r].clone()))
}

pub fn matrix_to_basis(m: &Matrix6, scale: &Cyc24) -> BasisCyc {
    std::array::from_fn(|col| std::array::from_fn(|row| m[row][col].mul(scale)))
}

pub fn dita_representative_triple() -> MuTripleCyc {
    let b0 = standard_basis();
    let b1 = f6_family_columns(0, 0);
    let f6_cols = f6_family_columns(0, 0);
    let f6_mat: Matrix6 = std::array::from_fn(|r| std::array::from_fn(|c| f6_cols[c][r].clone()));
    let b2: BasisCyc =
        std::array::from_fn(|col| std::array::from_fn(|row| f6_mat[col][row].clone()));
    MuTripleCyc { b0, b1, b2 }
}

pub fn tao_representative_triple() -> MuTripleCyc {
    let b0 = standard_basis();
    let s6 = tao_s6_matrix();
    let s = inv_sqrt6();
    let b1 = matrix_to_basis(&s6, &s);
    let s6_t = transpose_matrix(&s6);
    let b2 = matrix_to_basis(&s6_t, &s);
    MuTripleCyc { b0, b1, b2 }
}

pub fn szollosi_representative_triple() -> MuTripleCyc {
    let b0 = standard_basis();
    let b1 = f6_family_columns(0, 0);
    let b2 = f6_family_columns(0, 8);
    MuTripleCyc { b0, b1, b2 }
}

pub fn validate_mu_triple(triple: &MuTripleCyc) -> Result<(), String> {
    let bases = [&triple.b0, &triple.b1, &triple.b2];
    let one = Cyc24::one();
    let zero = Cyc24::zero();
    let sixth = Cyc24::rat(rq(1, 6));

    for (b_idx, b) in bases.iter().enumerate() {
        for i in 0..D {
            for j in 0..D {
                let ip = inner(&b[i], &b[j]);
                let expected = if i == j { &one } else { &zero };
                if ip != *expected {
                    return Err(format!(
                        "Basis {} not orthonormal at ({}, {}): found {:?}",
                        b_idx, i, j, ip
                    ));
                }
            }
        }
    }

    for b1_idx in 0..3 {
        for b2_idx in (b1_idx + 1)..3 {
            for i in 0..D {
                for j in 0..D {
                    let ip = inner(&bases[b1_idx][i], &bases[b2_idx][j]);
                    let sq = squared_norm(&ip);
                    if sq != sixth {
                        return Err(format!(
                            "Bases ({}, {}) not mutually unbiased at ({}, {}): squared overlap is not 1/6",
                            b1_idx, b2_idx, i, j
                        ));
                    }
                }
            }
        }
    }
    Ok(())
}

pub fn margin_dita() -> BigRational {
    base_gap()
}

pub fn margin_szollosi() -> BigRational {
    base_gap()
}

pub fn margin_tao_chart_distance() -> BigRational {
    rq(527, 576)
}

pub fn margin_tao() -> BigRational {
    rq(527, 576)
}

pub fn squared_norm(z: &Cyc24) -> Cyc24 {
    omega_functional::MubFeasibilityWallFunctional::cyclotomic_squared_norm(std::slice::from_ref(z))
}

pub fn exact_norm_sq_rat(z: &Cyc24) -> Result<BigRational, String> {
    squared_norm(z)
        .as_rational()
        .ok_or_else(|| "squared norm is not rational".to_string())
}

#[cfg(test)]
fn coefficient_square_mass(z: &Cyc24) -> BigRational {
    omega_functional::MubFeasibilityWallFunctional::cyclotomic_coefficient_energy(
        std::slice::from_ref(z),
    )
}

pub fn eval_zerorel_defect_cyc(triple: &MuTripleCyc, cand_u: &BasisCyc, rel: RelIndex) -> Cyc24 {
    let basis = match rel.basis {
        0 => &triple.b0,
        1 => &triple.b1,
        2 => &triple.b2,
        _ => panic!("basis index out of bounds: {}", rel.basis),
    };

    let v_i = &basis[rel.row];
    let u_j = &cand_u[rel.col];
    let ip = inner(v_i, u_j);
    let sixth = Cyc24::rat(rq(1, 6));
    squared_norm(&ip).sub(&sixth)
}

pub fn eval_all_zerorel_defects_cyc(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
) -> Vec<(RelIndex, Cyc24)> {
    let mut res = Vec::with_capacity(TOTAL_ZEROREL_EQUATIONS);
    for basis in 0..3 {
        for row in 0..D {
            for col in 0..D {
                let rel = RelIndex { basis, row, col };
                let r = eval_zerorel_defect_cyc(triple, cand_u, rel);
                res.push((rel, r));
            }
        }
    }
    res
}

pub fn eval_zerorel_residual(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
    rel: RelIndex,
) -> BigRational {
    let basis = match rel.basis {
        0 => &triple.b0,
        1 => &triple.b1,
        2 => &triple.b2,
        _ => panic!("basis index out of bounds: {}", rel.basis),
    };

    let v_i = &basis[rel.row];
    let u_j = &cand_u[rel.col];
    let ip = inner(v_i, u_j);
    let sq = squared_norm(&ip);
    let norm_sq = sq.as_rational().unwrap_or_else(|| sq.a[0].clone());
    let one_sixth = rq(1, 6);
    norm_sq - one_sixth
}

pub fn eval_all_zerorel_residuals(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
) -> Vec<(RelIndex, BigRational)> {
    let mut res = Vec::with_capacity(TOTAL_ZEROREL_EQUATIONS);
    for basis in 0..3 {
        for row in 0..D {
            for col in 0..D {
                let rel = RelIndex { basis, row, col };
                let r = eval_zerorel_residual(triple, cand_u, rel);
                res.push((rel, r));
            }
        }
    }
    res
}

pub fn eval_artin_schreier_curvature(triple: &MuTripleCyc, cand_u: &BasisCyc) -> BigRational {
    let sixth = Cyc24::rat(rq(1, 6));
    let mut residuals = Vec::with_capacity(3 * D * D);
    for basis_idx in 0..3 {
        let basis = match basis_idx {
            0 => &triple.b0,
            1 => &triple.b1,
            2 => &triple.b2,
            _ => unreachable!(),
        };
        for v_i in basis.iter().take(D) {
            for u_j in cand_u.iter().take(D) {
                let defect = squared_norm(&inner(v_i, u_j)).sub(&sixth);
                residuals.push(defect);
            }
        }
    }
    omega_functional::MubFeasibilityWallFunctional::cyclotomic_coefficient_energy(&residuals)
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurvatureCertificateWitness {
    pub class_name: String,
    pub margin_num: i64,
    pub margin_den: i64,
    pub verified_bound: bool,
}

pub fn verify_curvature_bound(triple: &MuTripleCyc, cand_u: &BasisCyc, eps: &BigRational) -> bool {
    if *eps <= BigRational::zero() {
        return false;
    }
    let psi_sq = eval_artin_schreier_curvature(triple, cand_u);
    psi_sq >= *eps
}

pub fn apply_unitary_to_basis(v: &Matrix6, basis: &BasisCyc) -> BasisCyc {
    std::array::from_fn(|col| {
        let u = &basis[col];
        std::array::from_fn(|row| {
            let mut acc = Cyc24::zero();
            for k in 0..D {
                acc = acc.add(&v[row][k].mul(&u[k]));
            }
            acc
        })
    })
}

pub fn apply_unitary_to_triple(v: &Matrix6, triple: &MuTripleCyc) -> MuTripleCyc {
    MuTripleCyc {
        b0: apply_unitary_to_basis(v, &triple.b0),
        b1: apply_unitary_to_basis(v, &triple.b1),
        b2: apply_unitary_to_basis(v, &triple.b2),
    }
}

pub fn verify_unitary_gauge_invariance(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
    v: &Matrix6,
) -> bool {
    let orig_psi = eval_artin_schreier_curvature(triple, cand_u);
    let trans_triple = apply_unitary_to_triple(v, triple);
    let trans_u = apply_unitary_to_basis(v, cand_u);
    let trans_psi = eval_artin_schreier_curvature(&trans_triple, &trans_u);
    orig_psi == trans_psi
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn squared_norm_of_a_root_of_unity_stays_rational() {
        assert_eq!(exact_norm_sq_rat(&Cyc24::zeta24(1)).unwrap(), rq(1, 1));
        assert_eq!(exact_norm_sq_rat(&Cyc24::one()).unwrap(), rq(1, 1));
    }

    #[test]
    fn squared_norm_refuses_to_drop_non_rational_coefficients() {
        let z = Cyc24::one().add(&Cyc24::zeta24(1));
        assert!(exact_norm_sq_rat(&z).is_err());
        let defect = squared_norm(&z).sub(&Cyc24::rat(rq(1, 6)));
        assert!(coefficient_square_mass(&defect) > BigRational::zero());
    }
}
