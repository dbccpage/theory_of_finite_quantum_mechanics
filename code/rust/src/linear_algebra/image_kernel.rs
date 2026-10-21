use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError};
use crate::linear_algebra::scalars::CheckedExactField;
use num_rational::Rational64;
use thiserror::Error;

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum ExactLinearAlgebraError {
    #[error("scalar arithmetic: {0}")]
    Scalar(#[from] crate::linear_algebra::scalars::ScalarError),
    #[error("matrix error: {0}")]
    Matrix(#[from] MatrixError),
    #[error("dimension mismatch: expected {expected}, got {got}")]
    DimensionMismatch { expected: usize, got: usize },
    #[error(
        "exact arithmetic exceeded fixed-width representation during {operation} at row {row}, \
         column {col}: the exact result is not representable in i64 numerator/denominator \
         (use a BigRational backend for arbitrary-precision theorem-grade arithmetic)"
    )]
    OverflowCeiling {
        operation: &'static str,
        row: usize,
        col: usize,
    },

    #[error(
        "image-membership certificate is internally inconsistent: rank equality \
         (rank_a = {rank_a}, rank_augmented = {rank_augmented}) established membership, \
         but the exact replay A·potential != target"
    )]
    MembershipReplayInconsistent {
        rank_a: usize,
        rank_augmented: usize,
    },
}

fn mul_exact<T: CheckedExactField>(
    a: &T,
    b: &T,
    row: usize,
    col: usize,
) -> Result<T, ExactLinearAlgebraError> {
    a.try_mul(b).map_err(|error| match error {
        crate::linear_algebra::scalars::ScalarError::OutOfRange { .. } => {
            ExactLinearAlgebraError::OverflowCeiling {
                operation: "multiply",
                row,
                col,
            }
        }
        other => ExactLinearAlgebraError::Scalar(other),
    })
}

fn sub_exact<T: CheckedExactField>(
    a: &T,
    b: &T,
    row: usize,
    col: usize,
) -> Result<T, ExactLinearAlgebraError> {
    a.try_sub(b).map_err(|error| match error {
        crate::linear_algebra::scalars::ScalarError::OutOfRange { .. } => {
            ExactLinearAlgebraError::OverflowCeiling {
                operation: "subtract",
                row,
                col,
            }
        }
        other => ExactLinearAlgebraError::Scalar(other),
    })
}

fn add_exact<T: CheckedExactField>(
    a: &T,
    b: &T,
    row: usize,
    col: usize,
) -> Result<T, ExactLinearAlgebraError> {
    a.try_add(b).map_err(|error| match error {
        crate::linear_algebra::scalars::ScalarError::OutOfRange { .. } => {
            ExactLinearAlgebraError::OverflowCeiling {
                operation: "add",
                row,
                col,
            }
        }
        other => ExactLinearAlgebraError::Scalar(other),
    })
}

fn div_exact<T: CheckedExactField>(
    a: &T,
    b: &T,
    row: usize,
    col: usize,
) -> Result<T, ExactLinearAlgebraError> {
    a.try_div(b).map_err(|error| match error {
        crate::linear_algebra::scalars::ScalarError::OutOfRange { .. } => {
            ExactLinearAlgebraError::OverflowCeiling {
                operation: "divide",
                row,
                col,
            }
        }
        other => ExactLinearAlgebraError::Scalar(other),
    })
}

fn neg_exact<T: CheckedExactField>(
    a: &T,
    row: usize,
    col: usize,
) -> Result<T, ExactLinearAlgebraError> {
    a.try_neg().map_err(|error| match error {
        crate::linear_algebra::scalars::ScalarError::OutOfRange { .. } => {
            ExactLinearAlgebraError::OverflowCeiling {
                operation: "negate",
                row,
                col,
            }
        }
        other => ExactLinearAlgebraError::Scalar(other),
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RankRref<T: CheckedExactField = Rational64> {
    rank: usize,
    rref: BasicMatrix<T>,
    pivot_columns: Vec<usize>,
}

impl<T: CheckedExactField> RankRref<T> {
    pub fn rank(&self) -> usize {
        self.rank
    }

    pub fn rref(&self) -> &BasicMatrix<T> {
        &self.rref
    }

    pub fn pivot_columns(&self) -> &[usize] {
        &self.pivot_columns
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawSubspaceBasis<T: CheckedExactField = Rational64> {
    vectors: Vec<Vec<T>>,
}

impl<T: CheckedExactField> std::ops::Index<usize> for RawSubspaceBasis<T> {
    type Output = Vec<T>;
    fn index(&self, idx: usize) -> &Self::Output {
        &self.vectors[idx]
    }
}

impl<T: CheckedExactField> RawSubspaceBasis<T> {
    pub fn vectors(&self) -> &[Vec<T>] {
        &self.vectors
    }

    pub fn is_empty(&self) -> bool {
        self.vectors.is_empty()
    }

    pub fn len(&self) -> usize {
        self.vectors.len()
    }
}

/// Rank, reduced row echelon form, image, and kernel for a [`CheckedExactField`].
///
/// `i64` is not a `CheckedExactField`. The positive example uses the same imports
/// as the refusal, so a bad import cannot be what makes the refusal fail.
///
/// ```
/// use theory_of_finite_qm::linear_algebra::basic_matrix::BasicMatrix;
/// use theory_of_finite_qm::linear_algebra::image_kernel::ExactRowReduction;
/// use num_rational::Rational64;
/// let a = BasicMatrix::from_row_major(2, 2, vec![
///     Rational64::new(2, 1),
///     Rational64::new(1, 1),
///     Rational64::new(1, 1),
///     Rational64::new(0, 1),
/// ]).unwrap();
/// assert_eq!(a.rank().unwrap(), 2);
/// ```
///
/// ```compile_fail,E0277
/// use theory_of_finite_qm::linear_algebra::basic_matrix::BasicMatrix;
/// use theory_of_finite_qm::linear_algebra::image_kernel::ExactRowReduction;
/// let a = BasicMatrix::from_row_major(2, 2, vec![2_i64, 1, 1, 0]).unwrap();
/// let _ = a.rank();
/// ```
pub trait ExactRowReduction<T: CheckedExactField = Rational64> {
    fn rank_and_rref(&self) -> Result<RankRref<T>, ExactLinearAlgebraError>;

    fn rank(&self) -> Result<usize, ExactLinearAlgebraError> {
        Ok(self.rank_and_rref()?.rank())
    }

    fn image_basis(&self) -> Result<RawSubspaceBasis<T>, ExactLinearAlgebraError>;

    fn kernel_basis(&self) -> Result<RawSubspaceBasis<T>, ExactLinearAlgebraError>;
}

fn find_pivot_row<T: CheckedExactField>(
    m: &BasicMatrix<T>,
    pivot_row: usize,
    col: usize,
) -> Result<Option<usize>, ExactLinearAlgebraError> {
    for row in pivot_row..m.rows() {
        if !m.get(row, col)?.try_is_zero()? {
            return Ok(Some(row));
        }
    }
    Ok(None)
}

fn swap_matrix_rows<T: CheckedExactField>(
    m: &mut BasicMatrix<T>,
    r1: usize,
    r2: usize,
) -> Result<(), ExactLinearAlgebraError> {
    if r1 != r2 {
        for c in 0..m.cols() {
            let tmp = m.get(r1, c)?;
            let other = m.get(r2, c)?;
            m.set(r1, c, other)?;
            m.set(r2, c, tmp)?;
        }
    }
    Ok(())
}

fn scale_pivot_row<T: CheckedExactField>(
    m: &mut BasicMatrix<T>,
    pivot_row: usize,
    col: usize,
) -> Result<(), ExactLinearAlgebraError> {
    let pivot_val = m.get(pivot_row, col)?;
    debug_assert!(!pivot_val.try_is_zero()?);
    for c in 0..m.cols() {
        let v = div_exact(&m.get(pivot_row, c)?, &pivot_val, pivot_row, c)?;
        m.set(pivot_row, c, v)?;
    }
    Ok(())
}

fn eliminate_single_row<T: CheckedExactField>(
    m: &mut BasicMatrix<T>,
    row: usize,
    pivot_row: usize,
    col: usize,
) -> Result<(), ExactLinearAlgebraError> {
    let factor = m.get(row, col)?;
    if factor.try_is_zero()? {
        return Ok(());
    }
    for c in 0..m.cols() {
        let scaled = mul_exact(&factor, &m.get(pivot_row, c)?, row, c)?;
        let v = sub_exact(&m.get(row, c)?, &scaled, row, c)?;
        m.set(row, c, v)?;
    }
    Ok(())
}

fn eliminate_matrix_rows<T: CheckedExactField>(
    m: &mut BasicMatrix<T>,
    pivot_row: usize,
    col: usize,
) -> Result<(), ExactLinearAlgebraError> {
    for row in 0..m.rows() {
        if row != pivot_row {
            eliminate_single_row(m, row, pivot_row, col)?;
        }
    }
    Ok(())
}

impl<T: CheckedExactField> ExactRowReduction<T> for BasicMatrix<T> {
    fn rank_and_rref(&self) -> Result<RankRref<T>, ExactLinearAlgebraError> {
        let mut m = self.clone();
        let mut pivot_row = 0usize;
        let mut pivot_columns = Vec::new();

        for col in 0..m.cols() {
            let Some(swap_row) = find_pivot_row(&m, pivot_row, col)? else {
                continue;
            };

            swap_matrix_rows(&mut m, pivot_row, swap_row)?;
            scale_pivot_row(&mut m, pivot_row, col)?;
            eliminate_matrix_rows(&mut m, pivot_row, col)?;

            pivot_columns.push(col);
            pivot_row += 1;

            if pivot_row == m.rows() {
                break;
            }
        }

        Ok(RankRref {
            rank: pivot_row,
            rref: m,
            pivot_columns,
        })
    }

    fn image_basis(&self) -> Result<RawSubspaceBasis<T>, ExactLinearAlgebraError> {
        let reduction = self.rank_and_rref()?;

        let mut basis = Vec::with_capacity(reduction.rank());

        for &col in reduction.pivot_columns() {
            let vector = (0..self.rows())
                .map(|row| self.get(row, col))
                .collect::<Result<Vec<_>, _>>()?;

            basis.push(vector);
        }

        Ok(RawSubspaceBasis { vectors: basis })
    }

    fn kernel_basis(&self) -> Result<RawSubspaceBasis<T>, ExactLinearAlgebraError> {
        let reduction = self.rank_and_rref()?;
        let rref = reduction.rref();
        let pivot_columns = reduction.pivot_columns();

        let mut is_pivot = vec![false; self.cols()];
        for &col in pivot_columns {
            is_pivot[col] = true;
        }

        let free_columns = (0..self.cols())
            .filter(|&col| !is_pivot[col])
            .collect::<Vec<_>>();

        let mut basis = Vec::with_capacity(free_columns.len());

        for &free in &free_columns {
            let mut v = vec![T::zero(); self.cols()];
            v[free] = T::one();

            for (row, &pcol) in pivot_columns.iter().enumerate() {
                v[pcol] = neg_exact(&rref.get(row, free)?, row, free)?;
            }

            basis.push(v);
        }

        Ok(RawSubspaceBasis { vectors: basis })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ImageMembership<T> {
    InImage(ImageMembershipWitness<T>),
    NotInImage {
        rank_a: usize,
        rank_augmented: usize,
    },
}

impl<T> ImageMembership<T> {
    pub fn is_in_image(&self) -> bool {
        matches!(self, ImageMembership::InImage(_))
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ImageMembershipWitness<T> {
    pub potential: Vec<T>,
    pub image: Vec<T>,
}

fn matvec<T: CheckedExactField>(
    a: &BasicMatrix<T>,
    x: &[T],
) -> Result<Vec<T>, ExactLinearAlgebraError> {
    let mut out = vec![T::zero(); a.rows()];
    for (row, slot) in out.iter_mut().enumerate() {
        let mut acc = T::zero();
        for (col, xc) in x.iter().enumerate() {
            let term = mul_exact(&a.get(row, col)?, xc, row, col)?;
            acc = add_exact(&acc, &term, row, col)?;
        }
        *slot = acc;
    }
    Ok(out)
}

fn build_augmented_matrix<T: CheckedExactField>(
    d0: &BasicMatrix<T>,
    target: &[T],
    rows: usize,
    cols: usize,
) -> Result<BasicMatrix<T>, ExactLinearAlgebraError> {
    let mut aug_data = Vec::with_capacity(rows * (cols + 1));
    for (row, t) in target.iter().enumerate().take(rows) {
        for col in 0..cols {
            aug_data.push(d0.get(row, col)?);
        }
        aug_data.push(t.clone());
    }
    Ok(BasicMatrix::from_row_major(rows, cols + 1, aug_data)?)
}

fn extract_potential<T: CheckedExactField>(
    aug_red: &RankRref<T>,
    cols: usize,
) -> Result<Vec<T>, ExactLinearAlgebraError> {
    let rref = aug_red.rref();
    let mut potential = vec![T::zero(); cols];
    for (pivot_row, &pcol) in aug_red.pivot_columns().iter().enumerate() {
        if pcol < cols {
            potential[pcol] = rref.get(pivot_row, cols)?;
        }
    }
    Ok(potential)
}

pub fn solve_in_image<T: CheckedExactField>(
    d0: &BasicMatrix<T>,
    target: &[T],
) -> Result<ImageMembership<T>, ExactLinearAlgebraError> {
    let rows = d0.rows();
    let cols = d0.cols();
    if target.len() != rows {
        return Err(ExactLinearAlgebraError::DimensionMismatch {
            expected: rows,
            got: target.len(),
        });
    }

    let rank_a = d0.rank()?;
    let aug = build_augmented_matrix(d0, target, rows, cols)?;
    let aug_red = aug.rank_and_rref()?;
    let rank_augmented = aug_red.rank();

    if rank_augmented > rank_a {
        return Ok(ImageMembership::NotInImage {
            rank_a,
            rank_augmented,
        });
    }

    let potential = extract_potential(&aug_red, cols)?;
    let image = matvec(d0, &potential)?;
    if image.as_slice() != target {
        return Err(ExactLinearAlgebraError::MembershipReplayInconsistent {
            rank_a,
            rank_augmented,
        });
    }

    Ok(ImageMembership::InImage(ImageMembershipWitness {
        potential,
        image,
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;
    use num_rational::{BigRational, Rational64};

    fn r(n: i64, d: i64) -> Rational64 {
        Rational64::new(n, d)
    }

    fn br(n: i64, d: i64) -> BigRational {
        BigRational::new(BigInt::from(n), BigInt::from(d))
    }

    #[test]
    fn integer_division_counterexample_matrix_has_rank_2() {
        let m_r64 =
            BasicMatrix::from_row_major(2, 2, vec![r(2, 1), r(1, 1), r(1, 1), r(0, 1)]).unwrap();
        assert_eq!(m_r64.rank().unwrap(), 2);

        let m_big = BasicMatrix::from_row_major(2, 2, vec![br(2, 1), br(1, 1), br(1, 1), br(0, 1)])
            .unwrap();
        assert_eq!(m_big.rank().unwrap(), 2);
    }

    #[test]
    fn big_rational_rref_rank_nullity_and_replay() {
        let m = BasicMatrix::from_row_major(
            2,
            3,
            vec![br(1, 1), br(2, 1), br(3, 1), br(2, 1), br(4, 1), br(7, 1)],
        )
        .unwrap();

        let reduction = m
            .rank_and_rref()
            .expect("BigRational row reduction succeeds");
        assert_eq!(reduction.rank(), 2);

        let kernel = m.kernel_basis().expect("BigRational kernel basis");

        assert_eq!(reduction.rank() + kernel.len(), m.cols());

        for k_vec in kernel.vectors() {
            let prod = matvec(&m, k_vec).expect("BigRational matvec");
            for val in prod {
                assert_eq!(val, br(0, 1));
            }
        }
    }

    #[test]
    fn rational64_and_big_rational_cross_domain_agreement() {
        let m_r64 = BasicMatrix::from_row_major(
            3,
            3,
            vec![
                r(1, 2),
                r(3, 4),
                r(5, 6),
                r(7, 8),
                r(9, 10),
                r(11, 12),
                r(13, 14),
                r(15, 16),
                r(17, 18),
            ],
        )
        .unwrap();

        let m_big = BasicMatrix::from_row_major(
            3,
            3,
            vec![
                br(1, 2),
                br(3, 4),
                br(5, 6),
                br(7, 8),
                br(9, 10),
                br(11, 12),
                br(13, 14),
                br(15, 16),
                br(17, 18),
            ],
        )
        .unwrap();

        let red_r64 = m_r64.rank_and_rref().unwrap();
        let red_big = m_big.rank_and_rref().unwrap();

        assert_eq!(red_r64.rank(), red_big.rank());
        assert_eq!(red_r64.pivot_columns(), red_big.pivot_columns());
    }

    #[test]
    fn test_rational_overflow_returns_ceiling_error() {
        let m = BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(i64::MAX, 1), r(2, 1), r(1, 1)])
            .unwrap();

        let error = m.rank_and_rref().expect_err("overflow must be refused");
        assert!(
            matches!(
                error,
                ExactLinearAlgebraError::OverflowCeiling {
                    operation: "multiply",
                    ..
                }
            ),
            "expected a typed multiply ceiling, got {error:?}"
        );
        assert!(
            format!("{error}").contains("BigRational"),
            "ceiling error should point at the unbounded backend: {error}"
        );
    }

    #[test]
    fn ordinary_matrices_do_not_hit_the_ceiling() {
        let m = BasicMatrix::from_row_major(
            3,
            3,
            vec![
                r(2, 3),
                r(-4, 5),
                r(7, 2),
                r(1, 6),
                r(3, 1),
                r(-2, 7),
                r(5, 4),
                r(0, 1),
                r(9, 8),
            ],
        )
        .unwrap();
        let reduction = m.rank_and_rref().expect("ordinary fractions stay in range");
        assert_eq!(reduction.rank(), 3);
    }

    #[test]
    fn image_membership_surfaces_the_ceiling_instead_of_deciding() {
        let d0 = BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(i64::MAX, 1), r(2, 1), r(1, 1)])
            .unwrap();
        let target = vec![r(1, 1), r(1, 1)];

        let error = solve_in_image(&d0, &target).expect_err("overflow must propagate");
        assert!(
            matches!(error, ExactLinearAlgebraError::OverflowCeiling { .. }),
            "an overflow must never be reported as a decided NotInImage: {error:?}"
        );
    }

    #[test]
    fn rank_zero_matrix_is_zero() {
        let m = BasicMatrix::from_row_major(2, 2, vec![r(0, 1); 4]).unwrap();
        assert_eq!(m.rank().unwrap(), 0);
    }

    #[test]
    fn rank_identity_is_n() {
        let m =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        assert_eq!(m.rank().unwrap(), 2);
    }

    #[test]
    fn rref_identity_is_identity() {
        let m =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        let rr = m.rank_and_rref().unwrap();
        assert_eq!(rr.rank(), 2);
        assert_eq!(rr.rref().as_slice(), m.as_slice());
    }

    #[test]
    fn rref_known_matrix() {
        let m =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(2, 1), r(3, 1), r(6, 1)]).unwrap();
        let rr = m.rank_and_rref().unwrap();
        assert_eq!(rr.rank(), 1);
        let expected = vec![r(1, 1), r(2, 1), r(0, 1), r(0, 1)];
        assert_eq!(rr.rref().as_slice(), expected.as_slice());
    }

    #[test]
    fn image_basis_uses_original_pivot_columns() {
        let m =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(2, 1), r(3, 1), r(6, 1)]).unwrap();
        let image = m.image_basis().unwrap();
        assert_eq!(image.len(), 1);
        assert_eq!(image[0], vec![r(1, 1), r(3, 1)]);
    }

    #[test]
    fn kernel_basis_for_full_rank_matrix_is_empty() {
        let m =
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap();
        assert!(m.kernel_basis().unwrap().is_empty());
    }

    #[test]
    fn kernel_basis_for_zero_matrix_is_standard_basis() {
        let m = BasicMatrix::from_row_major(2, 2, vec![r(0, 1); 4]).unwrap();
        let kb = m.kernel_basis().unwrap();
        assert_eq!(kb.len(), 2);
        assert_eq!(kb[0], vec![r(1, 1), r(0, 1)]);
        assert_eq!(kb[1], vec![r(0, 1), r(1, 1)]);
    }

    #[test]
    fn kernel_basis_known_example() {
        let m = BasicMatrix::from_row_major(2, 2, vec![r(1, 1); 4]).unwrap();
        let kb = m.kernel_basis().unwrap();
        assert_eq!(kb.len(), 1);
        assert_eq!(kb[0], vec![r(-1, 1), r(1, 1)]);
    }

    #[test]
    fn kernel_basis_known_example_wide() {
        let m = BasicMatrix::from_row_major(1, 3, vec![r(1, 1), r(2, 1), r(3, 1)]).unwrap();
        let kb = m.kernel_basis().unwrap();
        assert_eq!(kb.len(), 2);
        assert_eq!(kb[0], vec![r(-2, 1), r(1, 1), r(0, 1)]);
        assert_eq!(kb[1], vec![r(-3, 1), r(0, 1), r(1, 1)]);
    }

    #[test]
    fn rank_rectangular_tall_matrix() {
        let m = BasicMatrix::from_row_major(
            3,
            2,
            vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1), r(1, 1), r(1, 1)],
        )
        .unwrap();
        assert_eq!(m.rank().unwrap(), 2);
    }

    #[test]
    fn rank_rectangular_wide_matrix() {
        let m = BasicMatrix::from_row_major(
            2,
            3,
            vec![r(1, 1), r(0, 1), r(1, 1), r(0, 1), r(1, 1), r(1, 1)],
        )
        .unwrap();
        assert_eq!(m.rank().unwrap(), 2);
    }

    fn d0_edge() -> BasicMatrix<Rational64> {
        BasicMatrix::from_row_major(2, 1, vec![r(1, 1), r(-1, 1)]).unwrap()
    }

    #[test]
    fn image_membership_accepts_in_image_target() {
        let target = vec![r(3, 1), r(-3, 1)];
        match solve_in_image(&d0_edge(), &target).unwrap() {
            ImageMembership::InImage(w) => assert_eq!(w.image, target),
            other => panic!("expected InImage, got {other:?}"),
        }
    }

    #[test]
    fn image_membership_rejects_out_of_image_target() {
        let target = vec![r(1, 1), r(1, 1)];
        match solve_in_image(&d0_edge(), &target).unwrap() {
            ImageMembership::NotInImage {
                rank_a,
                rank_augmented,
            } => {
                assert_eq!(rank_a, 1);
                assert_eq!(rank_augmented, 2);
            }
            other => panic!("expected NotInImage, got {other:?}"),
        }
    }

    #[test]
    fn image_membership_witness_replays_exactly() {
        let target = vec![r(5, 1), r(-5, 1)];
        match solve_in_image(&d0_edge(), &target).unwrap() {
            ImageMembership::InImage(w) => {
                let replay = matvec(&d0_edge(), &w.potential).unwrap();
                assert_eq!(replay, target);
                assert_eq!(w.image, target);
            }
            other => panic!("expected InImage, got {other:?}"),
        }
    }

    #[test]
    fn rank_augmented_detects_nonmembership() {
        let d0 = d0_edge();
        assert!(solve_in_image(&d0, &[r(0, 1), r(0, 1)])
            .unwrap()
            .is_in_image());
        assert!(!solve_in_image(&d0, &[r(2, 1), r(1, 1)])
            .unwrap()
            .is_in_image());
    }

    #[test]
    fn image_membership_rejects_dimension_mismatch() {
        let err = solve_in_image(&d0_edge(), &[r(1, 1)]).unwrap_err();
        assert_eq!(
            err,
            ExactLinearAlgebraError::DimensionMismatch {
                expected: 2,
                got: 1
            }
        );
    }

    #[test]
    fn not_in_image_always_witnesses_strict_rank_growth() {
        let matrices: Vec<BasicMatrix<Rational64>> = vec![
            d0_edge(),
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap(),
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(2, 1), r(2, 1), r(4, 1)]).unwrap(),
            BasicMatrix::from_row_major(
                2,
                3,
                vec![r(1, 1), r(1, 1), r(0, 1), r(1, 1), r(1, 1), r(0, 1)],
            )
            .unwrap(),
            BasicMatrix::from_row_major(2, 1, vec![r(0, 1), r(0, 1)]).unwrap(),
            BasicMatrix::from_row_major(
                3,
                2,
                vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1), r(1, 1), r(1, 1)],
            )
            .unwrap(),
        ];
        let targets_2 = [
            vec![r(0, 1), r(0, 1)],
            vec![r(1, 1), r(-1, 1)],
            vec![r(1, 1), r(1, 1)],
            vec![r(3, 1), r(7, 2)],
            vec![r(-5, 3), r(5, 3)],
        ];
        let targets_3 = [
            vec![r(0, 1), r(0, 1), r(0, 1)],
            vec![r(1, 1), r(1, 1), r(2, 1)],
            vec![r(1, 1), r(0, 1), r(0, 1)],
        ];

        let mut saw_in = 0usize;
        let mut saw_out = 0usize;
        for m in &matrices {
            let targets: &[Vec<Rational64>] = if m.rows() == 2 {
                &targets_2
            } else {
                &targets_3
            };
            for t in targets {
                match solve_in_image(m, t).expect("no overflow in this corpus") {
                    ImageMembership::InImage(w) => {
                        saw_in += 1;
                        assert_eq!(matvec(m, &w.potential).unwrap(), *t);
                    }
                    ImageMembership::NotInImage {
                        rank_a,
                        rank_augmented,
                    } => {
                        saw_out += 1;
                        assert!(
                            rank_augmented > rank_a,
                            "NotInImage returned with rank_augmented = {rank_augmented} <= \
                             rank_a = {rank_a} — the verdict contradicts its own evidence, \
                             which is what MembershipReplayInconsistent exists to prevent"
                        );
                    }
                }
            }
        }
        assert!(
            saw_in > 0 && saw_out > 0,
            "sweep covered only one branch ({saw_in} in, {saw_out} out)"
        );
    }

    #[test]
    fn replay_inconsistency_error_reports_the_contradicting_ranks() {
        let e: ExactLinearAlgebraError = ExactLinearAlgebraError::MembershipReplayInconsistent {
            rank_a: 2,
            rank_augmented: 2,
        };
        let msg = e.to_string();
        assert!(
            msg.contains("rank_a = 2"),
            "message must name rank_a: {msg}"
        );
        assert!(
            msg.contains("rank_augmented = 2"),
            "message must name rank_augmented: {msg}"
        );
        assert_ne!(
            e,
            ExactLinearAlgebraError::MembershipReplayInconsistent {
                rank_a: 2,
                rank_augmented: 3
            },
            "the ranks must be part of the value, not decoration"
        );
    }

    #[test]
    fn rank_plus_nullity_equals_domain_dimension() {
        let matrices: [BasicMatrix<Rational64>; 6] = [
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1)]).unwrap(),
            BasicMatrix::from_row_major(2, 2, vec![r(0, 1); 4]).unwrap(),
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1); 4]).unwrap(),
            BasicMatrix::from_row_major(1, 3, vec![r(1, 1), r(2, 1), r(3, 1)]).unwrap(),
            BasicMatrix::from_row_major(
                2,
                3,
                vec![r(1, 1), r(2, 1), r(3, 1), r(2, 1), r(4, 1), r(7, 1)],
            )
            .unwrap(),
            BasicMatrix::from_row_major(
                3,
                2,
                vec![r(1, 1), r(0, 1), r(0, 1), r(1, 1), r(1, 1), r(1, 1)],
            )
            .unwrap(),
        ];
        for m in &matrices {
            let rank = m.rank().unwrap();
            let nullity = m.kernel_basis().unwrap().len();
            assert_eq!(
                rank + nullity,
                m.cols(),
                "rank {rank} + nullity {nullity} != cols {}",
                m.cols()
            );
        }
    }

    #[test]
    fn kernel_basis_vectors_map_to_zero() {
        let matrices: [BasicMatrix<Rational64>; 3] = [
            BasicMatrix::from_row_major(2, 2, vec![r(1, 1); 4]).unwrap(),
            BasicMatrix::from_row_major(1, 3, vec![r(1, 1), r(2, 1), r(3, 1)]).unwrap(),
            BasicMatrix::from_row_major(
                2,
                3,
                vec![r(1, 1), r(2, 1), r(3, 1), r(2, 1), r(4, 1), r(7, 1)],
            )
            .unwrap(),
        ];
        for m in &matrices {
            let kb = m.kernel_basis().unwrap();
            assert!(
                !kb.is_empty(),
                "rank-deficient fixtures must have a nonempty kernel"
            );
            for v in kb.vectors() {
                let prod = matvec(m, v).unwrap();
                for val in &prod {
                    assert_eq!(*val, r(0, 1));
                }
                assert!(
                    v.iter().any(|x| *x != r(0, 1)),
                    "kernel basis must not contain the zero vector"
                );
            }
        }
    }

    fn stack_vectors_as_columns(
        dim: usize,
        vectors: &[Vec<Rational64>],
    ) -> BasicMatrix<Rational64> {
        let mut data = Vec::with_capacity(dim * vectors.len());
        for row in 0..dim {
            for v in vectors {
                data.push(v[row].clone());
            }
        }
        BasicMatrix::from_row_major(dim, vectors.len(), data).unwrap()
    }

    #[test]
    fn image_basis_vectors_are_linearly_independent() {
        let m = BasicMatrix::from_row_major(
            2,
            3,
            vec![r(1, 1), r(2, 1), r(3, 1), r(2, 1), r(4, 1), r(7, 1)],
        )
        .unwrap();
        let image = m.image_basis().unwrap();
        assert_eq!(image.len(), m.rank().unwrap());
        assert_eq!(image.len(), 2);
        let stacked = stack_vectors_as_columns(m.rows(), image.vectors());
        assert_eq!(stacked.rank().unwrap(), image.len());
    }

    #[test]
    fn kernel_basis_vectors_are_linearly_independent() {
        let m = BasicMatrix::from_row_major(1, 3, vec![r(1, 1), r(2, 1), r(3, 1)]).unwrap();
        let kb = m.kernel_basis().unwrap();
        assert_eq!(kb.len(), 2);
        let stacked = stack_vectors_as_columns(m.cols(), kb.vectors());
        assert_eq!(stacked.rank().unwrap(), kb.len());
    }

    #[test]
    fn rank_and_rref_is_deterministic() {
        let m = BasicMatrix::from_row_major(
            2,
            3,
            vec![r(1, 1), r(2, 1), r(3, 1), r(2, 1), r(4, 1), r(7, 1)],
        )
        .unwrap();
        let first = m.rank_and_rref().unwrap();
        let second = m.rank_and_rref().unwrap();
        assert_eq!(first, second);
        assert_eq!(m.image_basis().unwrap(), m.image_basis().unwrap());
        assert_eq!(m.kernel_basis().unwrap(), m.kernel_basis().unwrap());
    }
}
