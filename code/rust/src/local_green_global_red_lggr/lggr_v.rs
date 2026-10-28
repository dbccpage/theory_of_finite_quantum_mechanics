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
use num_traits::{One, Zero};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::{ExactRowReduction, RankRref};
use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Maximum cells in each input and in the declared QD product profile.
/// This bounds element counts, not rational bit sizes or total runtime.
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
    #[error("{input} contains a noncanonical rational at flat index {index}")]
    InvalidRational { input: String, index: usize },
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

fn preflight_soundness(
    d: &BasicMatrix<BigRational>,
    q: &BasicMatrix<BigRational>,
) -> Result<(), LggrSoundnessError> {
    if [d.rows(), d.cols(), q.rows(), q.cols()].contains(&0) {
        return Err(LggrSoundnessError::EmptyMatrix);
    }
    let d_cells = cells(d.rows(), d.cols())?;
    let q_cells = cells(q.rows(), q.cols())?;
    admit_cell_count(d_cells.max(q_cells))?;
    if q.cols() != d.rows() {
        return Err(LggrSoundnessError::DimensionMismatch {
            q_cols: q.cols(),
            d_rows: d.rows(),
        });
    }

    admit_cell_count(cells(q.rows(), d.cols())?)?;
    admit_coefficients("D", d.as_slice())?;
    admit_coefficients("Q", q.as_slice())
}

fn cells(rows: usize, cols: usize) -> Result<usize, LggrSoundnessError> {
    rows.checked_mul(cols).ok_or_else(|| {
        LggrSoundnessError::LinearAlgebra("matrix cell count overflows usize".into())
    })
}

fn admit_cell_count(cells: usize) -> Result<(), LggrSoundnessError> {
    if cells > MAX_LGGR_CELLS {
        return Err(LggrSoundnessError::BudgetUnknown {
            cells,
            limit: MAX_LGGR_CELLS,
        });
    }
    Ok(())
}

fn canonical(value: &BigRational) -> bool {
    if value.denom() <= &0.into() {
        return false;
    }
    let reduced = value.reduced();
    value.numer() == reduced.numer() && value.denom() == reduced.denom()
}

fn admit_coefficients(input: &str, values: &[BigRational]) -> Result<(), LggrSoundnessError> {
    for (index, value) in values.iter().enumerate() {
        if !canonical(value) {
            return Err(LggrSoundnessError::InvalidRational {
                input: input.into(),
                index,
            });
        }
    }
    Ok(())
}

/// Decide LGGR V soundness: rank(Q·D) == rank(D).
///
/// Both inputs and QD's shape are admitted before arithmetic. If unsound, the
/// report carries an exact witness `v` with `D v != 0` and `Q D v == 0`.
pub fn check_soundness(
    d: &BasicMatrix<BigRational>,
    q: &BasicMatrix<BigRational>,
) -> Result<LggrSoundnessReport, LggrSoundnessError> {
    preflight_soundness(d, q)?;
    let qd = q
        .checked_mul_with_limit(d, MAX_LGGR_CELLS)
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let d_rank = d
        .rank()
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let qd_reduction = qd
        .rank_and_rref()
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let qd_rank = qd_reduction.rank();

    if qd_rank == d_rank {
        Ok(LggrSoundnessReport {
            sound: true,
            d_rank,
            qd_rank,
            witness: None,
            authority_effect: "None".to_string(),
        })
    } else {
        let witness = first_unsoundness_witness(d, &qd_reduction)?.ok_or_else(|| {
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

fn first_unsoundness_witness(
    d: &BasicMatrix<BigRational>,
    reduction: &RankRref<BigRational>,
) -> Result<Option<Vec<BigRational>>, LggrSoundnessError> {
    let mut is_pivot = vec![false; d.cols()];
    for &pivot in reduction.pivot_columns() {
        is_pivot[pivot] = true;
    }
    // Same basis order as kernel_basis(), retaining only one candidate at a time.
    for free in 0..d.cols() {
        if is_pivot[free] {
            continue;
        }
        let mut witness = vec![BigRational::zero(); d.cols()];
        witness[free] = BigRational::one();
        for (row, &pivot) in reduction.pivot_columns().iter().enumerate() {
            witness[pivot] = -reduction
                .rref()
                .get(row, free)
                .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
        }
        let image = d
            .checked_mul_vec_with_limit(&witness, MAX_LGGR_CELLS)
            .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
        if image.iter().any(|entry| !entry.is_zero()) {
            return Ok(Some(witness));
        }
    }
    Ok(None)
}

/// Verify that a candidate witness satisfies the exact unsoundness condition:
/// `D·v != 0` and `Q·D·v == 0`.
///
/// Uses the decision API's input/product-shape admission profile before checking
/// witness length or value. Oversized or malformed shapes return a typed error;
/// an invalid witness on an admitted shape returns false. Q(Dv) avoids forming QD.
pub fn verify_unsoundness_witness(
    d: &BasicMatrix<BigRational>,
    q: &BasicMatrix<BigRational>,
    witness: &[BigRational],
) -> Result<bool, LggrSoundnessError> {
    preflight_soundness(d, q)?;
    if witness.len() != d.cols() {
        return Ok(false);
    }
    admit_coefficients("witness", witness)?;
    let dv = d
        .checked_mul_vec_with_limit(witness, MAX_LGGR_CELLS)
        .map_err(|e| LggrSoundnessError::LinearAlgebra(e.to_string()))?;
    let dv_nonzero = dv.iter().any(|v| !v.is_zero());
    if !dv_nonzero {
        return Ok(false);
    }
    let qdv = q
        .checked_mul_vec_with_limit(&dv, MAX_LGGR_CELLS)
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

    #[test]
    fn admission_precedes_candidate_length_and_preserves_error_order() {
        let empty = BasicMatrix::<BigRational>::from_row_major(0, 1, vec![]).unwrap();
        let large = BasicMatrix::<BigRational>::zero(65, 65).unwrap();
        assert_eq!(
            verify_unsoundness_witness(&empty, &large, &[]),
            Err(LggrSoundnessError::EmptyMatrix)
        );
        let d = BasicMatrix::<BigRational>::zero(1, 65).unwrap();
        let q = BasicMatrix::<BigRational>::zero(65, 1).unwrap();
        assert_eq!(
            verify_unsoundness_witness(&d, &q, &[]),
            Err(LggrSoundnessError::BudgetUnknown {
                cells: 4225,
                limit: MAX_LGGR_CELLS
            })
        );
        let wrong = BasicMatrix::<BigRational>::zero(65, 2).unwrap();
        assert_eq!(
            verify_unsoundness_witness(&d, &wrong, &[]),
            Err(LggrSoundnessError::DimensionMismatch {
                q_cols: 2,
                d_rows: 1
            })
        );
        assert!(matches!(
            verify_unsoundness_witness(&d, &large, &[]),
            Err(LggrSoundnessError::BudgetUnknown { .. })
        ));
    }

    #[test]
    fn unchecked_rationals_are_refused_before_arithmetic() {
        let one = BasicMatrix::from_row_major(1, 1, vec![r(1, 1)]).unwrap();
        for bad in [
            BigRational::new_raw(1.into(), 0.into()),
            BigRational::new_raw(1.into(), (-1).into()),
            BigRational::new_raw(2.into(), 2.into()),
        ] {
            let candidate = BasicMatrix::from_row_major(1, 1, vec![bad.clone()]).unwrap();
            assert_eq!(
                check_soundness(&candidate, &one),
                Err(LggrSoundnessError::InvalidRational {
                    input: "D".into(),
                    index: 0
                })
            );
            assert_eq!(
                check_soundness(&one, &candidate),
                Err(LggrSoundnessError::InvalidRational {
                    input: "Q".into(),
                    index: 0
                })
            );
            assert_eq!(
                verify_unsoundness_witness(&one, &one, &[bad]),
                Err(LggrSoundnessError::InvalidRational {
                    input: "witness".into(),
                    index: 0
                })
            );
        }
    }

    #[test]
    fn witness_verifier_rejects_zero_image_nonzero_observation_and_wrong_length() {
        let identity =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        assert_eq!(
            verify_unsoundness_witness(&identity, &identity, &[r(0, 1), r(0, 1)]),
            Ok(false)
        );
        assert_eq!(
            verify_unsoundness_witness(&identity, &identity, &[r(1, 1), r(0, 1)]),
            Ok(false)
        );
        assert_eq!(
            verify_unsoundness_witness(&identity, &identity, &[r(1, 1)]),
            Ok(false)
        );
        let projection = BasicMatrix::from_row_major(1, 2, vec![r(1, 1), r(0, 1)]).unwrap();
        assert_eq!(
            verify_unsoundness_witness(&identity, &projection, &[r(0, 1), r(1, 1)]),
            Ok(true)
        );
    }

    #[test]
    fn exact_product_ceiling_is_inclusive() {
        let d = BasicMatrix::from_row_major(1, 64, vec![r(1, 1); 64]).unwrap();
        let q = BasicMatrix::from_row_major(64, 1, vec![r(1, 1); 64]).unwrap();
        let report = check_soundness(&d, &q).unwrap();
        assert!(report.sound);
        assert_eq!((report.d_rank, report.qd_rank), (1, 1));
        assert_eq!(verify_unsoundness_witness(&d, &q, &[]), Ok(false));
    }

    fn ternary_vector(mut code: usize, count: usize) -> Vec<i64> {
        (0..count)
            .map(|_| {
                let value = (code % 3) as i64 - 1;
                code /= 3;
                value
            })
            .collect()
    }

    #[test]
    fn exhaustive_small_grid_matches_integer_minors_and_direct_witness_equations() {
        for d_code in 0..729 {
            let entries = ternary_vector(d_code, 6);
            let d = BasicMatrix::from_row_major(2, 3, entries.iter().map(|&v| r(v, 1)).collect())
                .unwrap();
            let has_minor = (0..3).any(|i| {
                (i + 1..3).any(|j| entries[i] * entries[3 + j] != entries[j] * entries[3 + i])
            });
            let expected_d_rank = if has_minor {
                2
            } else {
                usize::from(entries.iter().any(|&v| v != 0))
            };
            for q_code in 0..9 {
                let observer = ternary_vector(q_code, 2);
                let q =
                    BasicMatrix::from_row_major(1, 2, observer.iter().map(|&v| r(v, 1)).collect())
                        .unwrap();
                let expected_qd_rank = usize::from(
                    (0..3).any(|j| observer[0] * entries[j] + observer[1] * entries[3 + j] != 0),
                );
                let report = check_soundness(&d, &q).unwrap();
                assert_eq!(
                    (report.d_rank, report.qd_rank),
                    (expected_d_rank, expected_qd_rank),
                    "D={entries:?}, Q={observer:?}"
                );
                assert_eq!(report.sound, expected_d_rank == expected_qd_rank);
                assert_eq!(report.authority_effect, "None");
                if report.sound {
                    assert!(report.witness.is_none());
                } else {
                    let v = report.witness.unwrap();
                    let image: Vec<BigRational> = (0..2)
                        .map(|row| {
                            (0..3)
                                .map(|col| r(entries[row * 3 + col], 1) * &v[col])
                                .sum()
                        })
                        .collect();
                    assert!(image.iter().any(|x| !x.is_zero()));
                    assert!(
                        (r(observer[0], 1) * &image[0] + r(observer[1], 1) * &image[1]).is_zero()
                    );
                    assert_eq!(verify_unsoundness_witness(&d, &q, &v), Ok(true));
                }
            }
        }
    }
}
