
use num_rational::BigRational;
use num_traits::Zero;
use omega_linear_algebra::backend::basic_matrix::BasicMatrix;
use omega_linear_algebra::linear_algebra::image_kernel::ExactRowReduction;
use serde::{Deserialize, Serialize};
use thiserror::Error;

pub const MAX_LGGR_CELLS: usize = 4096;

pub const LGGR_SOUNDNESS_SCHEMA: &str = "omega.epk.lggr-soundness.v1";

#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum LggrSoundnessError {
    #[error("BUDGET_UNKNOWN: matrix cell count exceeds limit {limit} (got {cells})")]
    BudgetUnknown { cells: usize, limit: usize },
    #[error("dimension mismatch: Q cols ({q_cols}) must match D rows ({d_rows})")]
    DimensionMismatch { q_cols: usize, d_rows: usize },
    #[error("empty matrix")]
    EmptyMatrix,
    #[error("linear algebra computation error: {0}")]
    LinearAlgebra(String),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LggrSoundnessReport {
    pub sound: bool,
    pub d_rank: usize,
    pub qd_rank: usize,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub witness: Option<Vec<BigRational>>,
    pub authority_effect: String,
}

impl LggrSoundnessReport {
    pub fn is_sound(&self) -> bool {
        self.sound
    }

    pub fn witness(&self) -> Option<&[BigRational]> {
        self.witness.as_deref()
    }
}

pub fn check_soundness(
    d: &BasicMatrix<BigRational>,
    q: &BasicMatrix<BigRational>,
) -> Result<LggrSoundnessReport, LggrSoundnessError> {
    if d.rows() == 0 || d.cols() == 0 || q.rows() == 0 || q.cols() == 0 {
        return Err(LggrSoundnessError::EmptyMatrix);
    }
    let d_cells = d.rows().saturating_mul(d.cols());
    let q_cells = q.rows().saturating_mul(q.cols());
    if d_cells > MAX_LGGR_CELLS || q_cells > MAX_LGGR_CELLS {
        return Err(LggrSoundnessError::BudgetUnknown {
            cells: d_cells.max(q_cells),
            limit: MAX_LGGR_CELLS,
        });
    }
    if q.cols() != d.rows() {
        return Err(LggrSoundnessError::DimensionMismatch {
            q_cols: q.cols(),
            d_rows: d.rows(),
        });
    }

    let qd = q
        .mul(d)
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let qd_cells = qd.rows().saturating_mul(qd.cols());
    if qd_cells > MAX_LGGR_CELLS {
        return Err(LggrSoundnessError::BudgetUnknown {
            cells: qd_cells,
            limit: MAX_LGGR_CELLS,
        });
    }

    let d_rank = d
        .rank()
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let qd_rank = qd
        .rank()
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;

    if qd_rank == d_rank {
        Ok(LggrSoundnessReport {
            sound: true,
            d_rank,
            qd_rank,
            witness: None,
            authority_effect: "None".to_string(),
        })
    } else {
        let qd_null = qd
            .kernel_basis()
            .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
        let mut found_witness: Option<Vec<BigRational>> = None;
        for basis_vec in qd_null.vectors() {
            let dv = d
                .mul_vec(basis_vec)
                .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
            if dv.iter().any(|val| !val.is_zero()) {
                found_witness = Some(basis_vec.clone());
                break;
            }
        }

        let witness = found_witness.ok_or_else(|| {
            LggrSoundnessError::LinearAlgebra(
                "rank(QD) < rank(D) but no basis vector of ker(QD) outside ker(D) found"
                    .to_string(),
            )
        })?;

        Ok(LggrSoundnessReport {
            sound: false,
            d_rank,
            qd_rank,
            witness: Some(witness),
            authority_effect: "None".to_string(),
        })
    }
}

pub fn verify_unsoundness_witness(
    d: &BasicMatrix<BigRational>,
    q: &BasicMatrix<BigRational>,
    witness: &[BigRational],
) -> Result<bool, LggrSoundnessError> {
    if witness.len() != d.cols() {
        return Ok(false);
    }
    let dv = d
        .mul_vec(witness)
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let dv_nonzero = dv.iter().any(|v| !v.is_zero());
    if !dv_nonzero {
        return Ok(false);
    }
    let qd = q
        .mul(d)
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let qdv = qd
        .mul_vec(witness)
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let qdv_zero = qdv.iter().all(|v| v.is_zero());
    Ok(dv_nonzero && qdv_zero)
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;
    use num_traits::One;

    fn r(n: i64, d: i64) -> BigRational {
        BigRational::new(BigInt::from(n), BigInt::from(d))
    }

    #[test]
    fn exact_soundness_sound_case() {
        let d =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        let q =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();

        let report = check_soundness(&d, &q).unwrap();
        assert!(report.is_sound());
        assert_eq!(report.d_rank, 2);
        assert_eq!(report.qd_rank, 2);
        assert!(report.witness.is_none());
    }

    #[test]
    fn exact_soundness_unsound_with_witness() {
        let d =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        let q = BasicMatrix::from_row_major(1, 2, vec![r(1, 1), r(-1, 1)]).unwrap();

        let report = check_soundness(&d, &q).unwrap();
        assert!(!report.is_sound());
        assert_eq!(report.d_rank, 2);
        assert_eq!(report.qd_rank, 1);
        let witness = report.witness.as_ref().expect("unsound must carry witness");
        assert_eq!(witness.len(), 2);

        let valid = verify_unsoundness_witness(&d, &q, witness).unwrap();
        assert!(valid, "witness must be valid");
    }

    #[test]
    fn witness_break_floating_point_rounding() {
        let tiny = BigRational::new(BigInt::one(), BigInt::from(10).pow(30));
        let d =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        let q = BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(1, 1), r(1, 1), r(1, 1) + tiny])
            .unwrap();

        let report = check_soundness(&d, &q).unwrap();
        assert!(report.is_sound(), "exact arithmetic must recognize rank 2");
        assert_eq!(report.d_rank, 2);
        assert_eq!(report.qd_rank, 2);
    }

    #[test]
    fn oversize_matrix_returns_budget_unknown() {
        let rows = 65;
        let cols = 65;
        let d = BasicMatrix::zero(rows, cols).unwrap();
        let q = BasicMatrix::zero(rows, rows).unwrap();

        let err = check_soundness(&d, &q).unwrap_err();
        match err {
            LggrSoundnessError::BudgetUnknown { cells, limit } => {
                assert_eq!(cells, 4225);
                assert_eq!(limit, MAX_LGGR_CELLS);
            }
            other => panic!("expected BudgetUnknown, got {other:?}"),
        }
    }

    #[test]
    fn dimension_mismatch_refused() {
        let d =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        let q = BasicMatrix::from_row_major(
            2,
            3,
            vec![r(1, 1), r(0, 1), r(0, 1), r(0, 1), r(1, 1), r(0, 1)],
        )
        .unwrap();

        let err = check_soundness(&d, &q).unwrap_err();
        assert!(matches!(err, LggrSoundnessError::DimensionMismatch { .. }));
    }

    #[test]
    fn empty_matrix_refused() {
        let d = BasicMatrix::from_row_major(0, 0, vec![]).unwrap();
        let q = BasicMatrix::from_row_major(0, 0, vec![]).unwrap();

        let err = check_soundness(&d, &q).unwrap_err();
        assert!(matches!(err, LggrSoundnessError::EmptyMatrix));
    }
}
