//! LGGR V — Soundness check and unsoundness witness.
//!
//! # Soundness Invariant
//!
//! Let $D$ be the carrier difference operator ($m \times n$) and $Q$ be the observer
//! quotient projection ($p \times m$).
//! Soundness holds iff $\operatorname{im}(D) \cap \ker(Q) = \{0\}$.
//! By the dimension formula, this is algebraically equivalent to:
//!
//! \[
//! \operatorname{rank}(Q \cdot D) = \operatorname{rank}(D)
//! \]
//!
//! Over $\mathbb{Q}$, this rank equality is computed exactly via Bareiss / Gauss–Jordan
//! exact row reduction without any numerical tolerance or floating-point approximations.
//!
//! # Unsoundness Witness
//!
//! When $\operatorname{rank}(Q \cdot D) < \operatorname{rank}(D)$, the system is unsound.
//! There exists an unsoundness witness vector $v \in \mathbb{Q}^n$ such that:
//!
//! \[
//! D v \neq 0 \quad \text{and} \quad Q D v = 0
//! \]
//!
//! That is, $v \in \ker(Q \cdot D)$ but $v \notin \ker(D)$, proving that the unobservable
//! non-trivial state $D v$ is invisible to the observer $Q$.
//!
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::Zero;
use omega_linear_algebra::backend::basic_matrix::BasicMatrix;
use omega_linear_algebra::linear_algebra::image_kernel::ExactRowReduction;
use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Maximum matrix cells allowed before returning `BUDGET_UNKNOWN`.
pub const MAX_LGGR_CELLS: usize = 4096;

/// Canonical schema for LGGR V soundness report.
pub const LGGR_SOUNDNESS_SCHEMA: &str = "omega.epk.lggr-soundness.v1";

/// Errors encountered during the LGGR V soundness check.
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

/// The exact soundness verdict report for LGGR V.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LggrSoundnessReport {
    /// True iff rank(Q·D) == rank(D).
    pub sound: bool,
    /// Exact rank of D over ℚ.
    pub d_rank: usize,
    /// Exact rank of Q·D over ℚ.
    pub qd_rank: usize,
    /// If unsound, an exact witness vector v in ℚ^n with D v != 0 and Q D v == 0.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub witness: Option<Vec<BigRational>>,
    /// Canonical authority effect: None.
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

/// Decide LGGR V soundness: rank(Q·D) == rank(D).
///
/// Returns `Ok(LggrSoundnessReport)` with `sound: true` if sound.
/// If unsound, returns `sound: false` and carries an exact witness vector `v`
/// satisfying `D v != 0` and `Q D v == 0`.
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
        // Unsound! Find a witness v in ker(Q·D) such that D·v != 0.
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

/// Verify that a candidate witness satisfies the exact unsoundness condition:
/// `D·v != 0` and `Q·D·v == 0`.
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
        // D is 2x2 identity, Q is 2x2 identity.
        // rank(D) = 2, rank(Q·D) = 2 -> sound.
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
        // D is 2x2 identity: rank(D) = 2.
        // Q is 1x2 projection [1, -1]: ker(Q) is span((1, 1)).
        // Q·D = [1, -1], rank(Q·D) = 1.
        // Unsound! Witness v in ker(Q·D) with D·v != 0.
        // (1, 1) has D·(1, 1) = (1, 1) != 0, and Q·D·(1, 1) = 0.
        let d =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        let q = BasicMatrix::from_row_major(1, 2, vec![r(1, 1), r(-1, 1)]).unwrap();

        let report = check_soundness(&d, &q).unwrap();
        assert!(!report.is_sound());
        assert_eq!(report.d_rank, 2);
        assert_eq!(report.qd_rank, 1);
        let witness = report.witness.as_ref().expect("unsound must carry witness");
        assert_eq!(witness.len(), 2);

        // Verify witness satisfies D·v != 0 and Q·D·v == 0
        let valid = verify_unsoundness_witness(&d, &q, witness).unwrap();
        assert!(valid, "witness must be valid");
    }

    #[test]
    fn witness_break_floating_point_rounding() {
        // Tiny rational entry: 1 / 10^30
        // In f64, 1.0 + 1e-30 rounds to 1.0.
        // Matrix:
        // D = [[1, 0], [0, 1]] (rank 2)
        // Q = [[1, 1], [1, 1 + 1/10^30]]
        // Exactly: det(Q) = 1 + 1/10^30 - 1 = 1/10^30 != 0 -> Q is invertible!
        // rank(Q·D) = 2 == rank(D) -> SOUND.
        // Under f64, Q is [[1, 1], [1, 1]], which has rank 1 -> would incorrectly declare unsound!
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
        // 65 x 65 = 4225 > 4096 cells
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
