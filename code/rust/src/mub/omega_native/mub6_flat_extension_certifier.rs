//! Target Q6 / Step 3.1: Curto-Fialkow Flat Extension Rank Tester Engine.
//!
//! AuthorityEffect: None.
//!
//!
//! This module evaluates exact rational row-echelon rank of truncated moment matrices
//! M_1 and M_2 across candidate pseudo-expectations over `num_rational::BigRational`.
//! If rank(M_2) = rank(M_1), the Curto-Fialkow flat extension condition holds.
//! If rank(M_2) > rank(M_1), flat extension is strictly obstructed, proving that
//! degree-2 pseudo-expectation refutations fail rank-loop closure.

use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub const SCHEMA_VERSION: &str = "omega.mub.flat-extension-certifier.v1";
pub const SCOPE_STRING: &str = "curto_fialkow_flat_extension_rank_testing";

/// Result of evaluating flat extension rank loop over moment blocks M1 and M2.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlatExtensionRankReport {
    pub schema_version: String,
    pub scope: String,
    pub candidate_id: String,
    pub rank_m1: usize,
    pub rank_m2: usize,
    pub rank_gap: usize,
    pub is_flat_extension_satisfied: bool,
    pub is_rank_gap_certified: bool,
    pub matrix_m1_fingerprint: String,
    pub matrix_m2_fingerprint: String,
    pub status: String,
}

/// Compute exact rational row-echelon rank of a dense BigRational matrix.
pub fn compute_exact_rational_rank(matrix: &[Vec<BigRational>]) -> usize {
    if matrix.is_empty() || matrix[0].is_empty() {
        return 0;
    }
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut mat = matrix.to_vec();

    let mut pivot_row = 0;
    for col in 0..cols {
        if pivot_row >= rows {
            break;
        }
        // Find non-zero pivot in this column
        let mut selected = None;
        for r in pivot_row..rows {
            if !mat[r][col].is_zero() {
                selected = Some(r);
                break;
            }
        }
        let r = match selected {
            Some(row_idx) => row_idx,
            None => continue,
        };

        // Swap selected row to pivot_row
        mat.swap(pivot_row, r);

        // Normalize pivot row
        let pivot_val = mat[pivot_row][col].clone();
        for c in col..cols {
            mat[pivot_row][c] = &mat[pivot_row][c] / &pivot_val;
        }

        // Eliminate column entries in lower rows
        for r_below in (pivot_row + 1)..rows {
            let factor = mat[r_below][col].clone();
            if !factor.is_zero() {
                for c in col..cols {
                    let sub = &mat[pivot_row][c] * &factor;
                    mat[r_below][c] = &mat[r_below][c] - &sub;
                }
            }
        }
        pivot_row += 1;
    }

    pivot_row
}

/// Compute SHA-256 fingerprint for a rational matrix.
pub fn matrix_fingerprint(m: &[Vec<BigRational>]) -> String {
    let mut hasher = Sha256::new();
    for row in m {
        for val in row {
            hasher.update(format!("{}/{}\n", val.numer(), val.denom()).as_bytes());
        }
    }
    format!("{:x}", hasher.finalize())
}

/// Evaluate Curto-Fialkow flat extension rank condition on moment matrix blocks M1 and M2.
pub fn evaluate_flat_extension_rank(
    candidate_id: &str,
    m1: &[Vec<BigRational>],
    m2: &[Vec<BigRational>],
) -> FlatExtensionRankReport {
    let rank_m1 = compute_exact_rational_rank(m1);
    let rank_m2 = compute_exact_rational_rank(m2);

    let (rank_gap, is_flat, is_gap) = if rank_m2 >= rank_m1 {
        let gap = rank_m2 - rank_m1;
        (gap, gap == 0, gap > 0)
    } else {
        (0, false, false)
    };

    let status = if is_flat {
        "RANK_LOOP_CLOSED_FLAT_EXTENSION"
    } else {
        "FLAT_EXTENSION_OBSTRUCTED_RANK_GAP"
    };

    FlatExtensionRankReport {
        schema_version: SCHEMA_VERSION.to_string(),
        scope: SCOPE_STRING.to_string(),
        candidate_id: candidate_id.to_string(),
        rank_m1,
        rank_m2,
        rank_gap,
        is_flat_extension_satisfied: is_flat,
        is_rank_gap_certified: is_gap,
        matrix_m1_fingerprint: matrix_fingerprint(m1),
        matrix_m2_fingerprint: matrix_fingerprint(m2),
        status: status.to_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::One;

    #[test]
    fn test_exact_rational_rank_identity() {
        let m1 = vec![
            vec![BigRational::one(), BigRational::zero()],
            vec![BigRational::zero(), BigRational::one()],
        ];
        assert_eq!(compute_exact_rational_rank(&m1), 2);
    }

    #[test]
    fn test_exact_rational_rank_dependent() {
        let m = vec![
            vec![BigRational::new(1.into(), 1.into()), BigRational::new(2.into(), 1.into())],
            vec![BigRational::new(2.into(), 1.into()), BigRational::new(4.into(), 1.into())],
        ];
        assert_eq!(compute_exact_rational_rank(&m), 1);
    }

    #[test]
    fn test_flat_extension_evaluation() {
        let m1 = vec![
            vec![BigRational::one(), BigRational::zero()],
            vec![BigRational::zero(), BigRational::one()],
        ];
        let m2 = vec![
            vec![BigRational::one(), BigRational::zero(), BigRational::zero()],
            vec![BigRational::zero(), BigRational::one(), BigRational::zero()],
            vec![BigRational::zero(), BigRational::zero(), BigRational::one()],
        ];
        let report = evaluate_flat_extension_rank("test_candidate", &m1, &m2);
        assert_eq!(report.rank_m1, 2);
        assert_eq!(report.rank_m2, 3);
        assert_eq!(report.rank_gap, 1);
        assert!(!report.is_flat_extension_satisfied);
        assert!(report.is_rank_gap_certified);
        assert_eq!(report.status, "FLAT_EXTENSION_OBSTRUCTED_RANK_GAP");
    }
}
