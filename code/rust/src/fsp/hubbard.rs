//! Exact rational Hubbard determinants: 4x4 plaquette, attractive Hubbard square-root symmetry,
//! and palindromic spectra over Q.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};

/// Exact rational matrix determinant via Gaussian elimination over Q.
pub fn exact_determinant(mat: &[Vec<BigRational>]) -> Result<BigRational, &'static str> {
    let n = mat.len();
    if n == 0 {
        return Ok(BigRational::one());
    }
    for row in mat {
        if row.len() != n {
            return Err("matrix must be square for determinant");
        }
    }
    let mut a: Vec<Vec<BigRational>> = mat.to_vec();
    let mut det = BigRational::one();
    let mut sign_flips = 0;

    for col in 0..n {
        let mut pivot = None;
        for row in col..n {
            if !a[row][col].is_zero() {
                pivot = Some(row);
                break;
            }
        }
        let pivot_row = match pivot {
            Some(r) => r,
            None => return Ok(BigRational::zero()), // Singular matrix
        };

        if pivot_row != col {
            a.swap(col, pivot_row);
            sign_flips ^= 1;
        }

        let p_val = a[col][col].clone();
        det = det * &p_val;

        for r in (col + 1)..n {
            if !a[r][col].is_zero() {
                let factor = &a[r][col] / &p_val;
                for c in col..n {
                    let term = &factor * &a[col][c];
                    a[r][c] = &a[r][c] - term;
                }
            }
        }
    }

    if sign_flips == 1 {
        det = -det;
    }
    Ok(det)
}

/// Multiply two square matrices over Q.
pub fn exact_matrix_mul(
    a: &[Vec<BigRational>],
    b: &[Vec<BigRational>],
) -> Result<Vec<Vec<BigRational>>, &'static str> {
    let n = a.len();
    if n == 0 || b.len() != n {
        return Err("matrix dimension mismatch in multiplication");
    }
    for row in a {
        if row.len() != n {
            return Err("matrix A is not square");
        }
    }
    for row in b {
        if row.len() != n {
            return Err("matrix B is not square");
        }
    }
    let mut c = vec![vec![BigRational::zero(); n]; n];
    for i in 0..n {
        for k in 0..n {
            if a[i][k].is_zero() {
                continue;
            }
            for j in 0..n {
                let term = &a[i][k] * &b[k][j];
                c[i][j] = &c[i][j] + term;
            }
        }
    }
    Ok(c)
}

/// Compute palindromic kinetic matrix over Q:
/// Product of bond exponentials in forward then reverse order:
/// K = \prod_{e} B_e \prod_{e^rev} B_e
/// where r = exp(dtau * t / 2) is exact rational parameter.
pub fn exact_kinetic_matrix(
    sites: usize,
    bonds: &[(usize, usize)],
    r: &BigRational,
) -> Result<Vec<Vec<BigRational>>, &'static str> {
    if sites == 0 {
        return Err("sites must be positive");
    }
    if r <= &BigRational::zero() {
        return Err("r parameter must be strictly positive");
    }
    let r_inv = BigRational::one() / r;
    let two = BigRational::from(BigInt::from(2));
    let cosh_val = (r + &r_inv) / &two;
    let sinh_val = (r - &r_inv) / &two;

    let mut k_mat = vec![vec![BigRational::zero(); sites]; sites];
    for i in 0..sites {
        k_mat[i][i] = BigRational::one();
    }

    // Schedule: bonds forward, then bonds reverse
    let mut schedule = bonds.to_vec();
    let mut rev = bonds.to_vec();
    rev.reverse();
    schedule.extend(rev);

    for &(u, v) in &schedule {
        if u >= sites || v >= sites || u == v {
            return Err("invalid bond endpoint");
        }
        let mut b = vec![vec![BigRational::zero(); sites]; sites];
        for i in 0..sites {
            b[i][i] = BigRational::one();
        }
        b[u][u] = cosh_val.clone();
        b[v][v] = cosh_val.clone();
        b[u][v] = sinh_val.clone();
        b[v][u] = sinh_val.clone();

        k_mat = exact_matrix_mul(&b, &k_mat)?;
    }

    Ok(k_mat)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HubbardDeterminantReceipt {
    pub mask: usize,
    pub det_up: BigRational,
    pub det_down: BigRational,
    pub total_weight: BigRational,
    pub is_strictly_positive: bool,
    pub attractive_symmetry_holds: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HubbardEnsembleSummary {
    pub sites: usize,
    pub slices: usize,
    pub total_fields: usize,
    pub negative_fields_count: usize,
    pub zero_fields_count: usize,
    pub total_determinant_sum: BigRational,
    pub absolute_determinant_sum: BigRational,
    pub average_sign: BigRational,
    pub attractive_square_root_protected: bool,
}

/// Compute exact auxiliary-field Hubbard determinants for declared field masks.
pub fn evaluate_hubbard_determinants(
    sites: usize,
    bonds: &[(usize, usize)],
    slices: usize,
    r: &BigRational,
    hs: &BigRational,
    fugacity: &BigRational,
    attractive: bool,
    field_masks: &[usize],
) -> Result<HubbardEnsembleSummary, &'static str> {
    if sites == 0 || slices == 0 {
        return Err("sites and slices must be positive");
    }
    if field_masks.is_empty() {
        return Err("at least one field mask required");
    }

    let k_mat = exact_kinetic_matrix(sites, bonds, r)?;
    let mut receipts = Vec::with_capacity(field_masks.len());
    let mut total_sum = BigRational::zero();
    let mut abs_sum = BigRational::zero();
    let mut neg_count = 0;
    let mut zero_count = 0;
    let mut all_attractive_protected = true;

    for &mask in field_masks {
        // Build product across all slices for spin up (0) and spin down (1)
        let mut b_up = vec![vec![BigRational::zero(); sites]; sites];
        let mut b_down = vec![vec![BigRational::zero(); sites]; sites];
        for i in 0..sites {
            b_up[i][i] = BigRational::one();
            b_down[i][i] = BigRational::one();
        }

        for time in 0..slices {
            // Diagonal field operator V_t for up and down
            let mut v_up = vec![vec![BigRational::zero(); sites]; sites];
            let mut v_down = vec![vec![BigRational::zero(); sites]; sites];

            for j in 0..sites {
                let bit = (mask >> (time * sites + j)) & 1;
                let s_val = if bit == 1 { 1 } else { -1 };

                // alpha for spin up: +1
                // alpha for spin down: +1 if attractive else -1
                let exp_up = s_val;
                let exp_down = if attractive { s_val } else { -s_val };

                let hs_up = if exp_up == 1 {
                    hs.clone()
                } else {
                    BigRational::one() / hs
                };
                let hs_down = if exp_down == 1 {
                    hs.clone()
                } else {
                    BigRational::one() / hs
                };

                v_up[j][j] = fugacity * hs_up;
                v_down[j][j] = fugacity * hs_down;
            }

            let slice_up = exact_matrix_mul(&k_mat, &v_up)?;
            let slice_down = exact_matrix_mul(&k_mat, &v_down)?;

            b_up = exact_matrix_mul(&slice_up, &b_up)?;
            b_down = exact_matrix_mul(&slice_down, &b_down)?;
        }

        // Add identity: I + B_sigma
        for i in 0..sites {
            b_up[i][i] = &b_up[i][i] + BigRational::one();
            b_down[i][i] = &b_down[i][i] + BigRational::one();
        }

        let det_up = exact_determinant(&b_up)?;
        let det_down = exact_determinant(&b_down)?;

        let symmetry_holds = if attractive {
            det_up == det_down
        } else {
            true
        };
        if attractive && !symmetry_holds {
            all_attractive_protected = false;
        }

        let weight = &det_up * &det_down;
        if weight.is_zero() {
            zero_count += 1;
        } else if weight < BigRational::zero() {
            neg_count += 1;
        }

        total_sum = total_sum + &weight;
        abs_sum = abs_sum + weight.abs();

        receipts.push(HubbardDeterminantReceipt {
            mask,
            det_up,
            det_down,
            total_weight: weight.clone(),
            is_strictly_positive: weight > BigRational::zero(),
            attractive_symmetry_holds: symmetry_holds,
        });
    }

    let avg_sign = if abs_sum.is_zero() {
        BigRational::zero()
    } else {
        &total_sum / &abs_sum
    };

    Ok(HubbardEnsembleSummary {
        sites,
        slices,
        total_fields: field_masks.len(),
        negative_fields_count: neg_count,
        zero_fields_count: zero_count,
        total_determinant_sum: total_sum,
        absolute_determinant_sum: abs_sum,
        average_sign: avg_sign,
        attractive_square_root_protected: all_attractive_protected && attractive,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exact_determinant_2x2_and_3x3() {
        // [ [1, 2], [3, 4] ] -> 4 - 6 = -2
        let m2 = vec![
            vec![BigRational::from(BigInt::from(1)), BigRational::from(BigInt::from(2))],
            vec![BigRational::from(BigInt::from(3)), BigRational::from(BigInt::from(4))],
        ];
        assert_eq!(exact_determinant(&m2).unwrap(), -BigRational::from(BigInt::from(2)));

        // Identity 3x3
        let mut m3 = vec![vec![BigRational::zero(); 3]; 3];
        for i in 0..3 {
            m3[i][i] = BigRational::one();
        }
        assert_eq!(exact_determinant(&m3).unwrap(), BigRational::one());
    }

    #[test]
    fn attractive_hubbard_square_root_symmetry_on_square_plaquette() {
        // 4 sites, square plaquette
        let bonds = vec![(0, 1), (1, 2), (2, 3), (3, 0)];
        let r = BigRational::new(BigInt::from(3), BigInt::from(2));
        let hs = BigRational::from(BigInt::from(2));
        let fugacity = BigRational::one();
        let masks = vec![0, 1, 5, 15]; // Sample fields

        let summary = evaluate_hubbard_determinants(
            4,
            &bonds,
            1,
            &r,
            &hs,
            &fugacity,
            true, // attractive Hubbard
            &masks,
        )
        .unwrap();

        assert_eq!(summary.negative_fields_count, 0);
        assert!(summary.attractive_square_root_protected);
        assert_eq!(summary.average_sign, BigRational::one());
    }
}
