
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub const SCHEMA_VERSION: &str = "omega.mub.flat-extension-certifier.v1";
pub const SCOPE_STRING: &str = "curto_fialkow_flat_extension_rank_testing";

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

fn find_pivot_row(mat: &[Vec<BigRational>], pivot_row: usize, col: usize) -> Option<usize> {
    (pivot_row..mat.len()).find(|&r| !mat[r][col].is_zero())
}

fn normalize_pivot_row(row: &mut [BigRational], col: usize) {
    let pivot_val = row[col].clone();
    for val in &mut row[col..] {
        *val = &*val / &pivot_val;
    }
}

fn subtract_scaled_row(
    target: &mut [BigRational],
    pivot: &[BigRational],
    col: usize,
    factor: &BigRational,
) {
    for c in col..target.len() {
        let sub = &pivot[c] * factor;
        target[c] = &target[c] - &sub;
    }
}

fn eliminate_below_pivot(mat: &mut [Vec<BigRational>], pivot_row: usize, col: usize) {
    let pivot_slice = mat[pivot_row].clone();
    for row in &mut mat[(pivot_row + 1)..] {
        let factor = row[col].clone();
        if !factor.is_zero() {
            subtract_scaled_row(row, &pivot_slice, col, &factor);
        }
    }
}

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
        let Some(r) = find_pivot_row(&mat, pivot_row, col) else {
            continue;
        };

        mat.swap(pivot_row, r);
        normalize_pivot_row(&mut mat[pivot_row], col);
        eliminate_below_pivot(&mut mat, pivot_row, col);
        pivot_row += 1;
    }

    pivot_row
}

pub fn matrix_fingerprint(m: &[Vec<BigRational>]) -> String {
    let mut hasher = Sha256::new();
    for row in m {
        for val in row {
            hasher.update(format!("{}/{}\n", val.numer(), val.denom()).as_bytes());
        }
    }
    format!("{:x}", hasher.finalize())
}

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
