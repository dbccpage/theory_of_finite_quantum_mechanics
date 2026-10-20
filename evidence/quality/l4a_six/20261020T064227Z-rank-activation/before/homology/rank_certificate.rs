//! Exact rank certificates over Q. AuthorityEffect: None.
//!
//! For M=UV, LU=I_r and VR=I_r, rank(M)=r: factorization gives the
//! upper bound and the two split maps give the lower bound. The checker uses
//! matrix identities only; it does not trust the producer's elimination result.
//! Trust boundary: exact rational arithmetic and checked dense matrix operations.

use super::errors::HomologicalError;
use super::hashing::{hash_matrix, Hash256};
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::basic_matrix::MatrixError;
use crate::linear_algebra::image_kernel::ExactLinearAlgebraError;
use crate::linear_algebra::scalars::{q, Q};
use crate::linear_algebra::ExactFieldError;

/// Per-matrix element admission and aggregate field-operation admission for one
/// producer/checker call. Conservative phase bounds are charged without refunds.
/// Counts do not bound scalar bit sizes, hashing, parsing,
/// allocator internals, total process memory or elapsed time.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RankLimits {
    pub max_matrix_cells: usize,
    pub max_scalar_operations: usize,
}
impl Default for RankLimits {
    fn default() -> Self {
        Self {
            max_matrix_cells: 4096,
            max_scalar_operations: 1_000_000,
        }
    }
}

struct RankBudget {
    limits: RankLimits,
    spent: usize,
}
impl RankBudget {
    fn new(limits: RankLimits) -> Self {
        Self { limits, spent: 0 }
    }
    fn cells(&self, rows: usize, cols: usize) -> Result<usize, MatrixError> {
        let count = rows
            .checked_mul(cols)
            .ok_or(MatrixError::DimensionOverflow { rows, cols })?;
        if count > self.limits.max_matrix_cells {
            return Err(MatrixError::AllocationLimitExceeded {
                requested: count,
                limit: self.limits.max_matrix_cells,
            });
        }
        Ok(count)
    }
    fn requested(&self, operations: usize) -> Result<usize, MatrixError> {
        let requested = self
            .spent
            .checked_add(operations)
            .ok_or(MatrixError::OperationCountOverflow)?;
        if requested > self.limits.max_scalar_operations {
            return Err(MatrixError::OperationLimitExceeded {
                requested,
                limit: self.limits.max_scalar_operations,
            });
        }
        Ok(requested)
    }
    fn charge(&mut self, operations: usize) -> Result<(), MatrixError> {
        self.spent = self.requested(operations)?;
        Ok(())
    }
}

/// Untrusted candidate. Public fields permit transport and adversarial checking.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RankCandidate {
    pub image: BasicMatrix<Q>,
    pub coordinates: BasicMatrix<Q>,
    pub image_retraction: BasicMatrix<Q>,
    pub coordinate_section: BasicMatrix<Q>,
}

/// Immutable evidence, obtainable only by replaying all three exact identities.
/// ```compile_fail
/// use theory_of_finite_qm::homology::rank_certificate::RankCertificate;
/// use theory_of_finite_qm::homology::hashing::Hash256;
/// let _ = RankCertificate { matrix_hash: Hash256([0; 32]), rank: 999,
///     candidate: panic!("private construction is forbidden") };
/// ```
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RankCertificate {
    matrix_hash: Hash256,
    rank: usize,
    candidate: RankCandidate,
}

impl RankCertificate {
    pub fn try_admit(
        matrix: &BasicMatrix<Q>,
        candidate: RankCandidate,
    ) -> Result<Self, HomologicalError> {
        Self::try_admit_with_limits(matrix, candidate, RankLimits::default())
    }

    pub fn try_admit_with_limits(
        matrix: &BasicMatrix<Q>,
        candidate: RankCandidate,
        limits: RankLimits,
    ) -> Result<Self, HomologicalError> {
        Self::admit_with_budget(matrix, candidate, &mut RankBudget::new(limits))
    }

    fn admit_with_budget(
        matrix: &BasicMatrix<Q>,
        candidate: RankCandidate,
        budget: &mut RankBudget,
    ) -> Result<Self, HomologicalError> {
        check_candidate(matrix, &candidate, budget)?;
        Ok(Self {
            matrix_hash: hash_matrix(matrix)?,
            rank: candidate.image.cols(),
            candidate,
        })
    }

    pub fn rank(&self) -> usize {
        self.rank
    }
    pub fn matrix_hash(&self) -> &Hash256 {
        &self.matrix_hash
    }
    pub fn candidate(&self) -> &RankCandidate {
        &self.candidate
    }

    /// Replaying against another matrix requires both its binding and its identities.
    pub fn verify_against(&self, matrix: &BasicMatrix<Q>) -> Result<(), HomologicalError> {
        self.verify_against_with_limits(matrix, RankLimits::default())
    }

    pub fn verify_against_with_limits(
        &self,
        matrix: &BasicMatrix<Q>,
        limits: RankLimits,
    ) -> Result<(), HomologicalError> {
        let mut budget = RankBudget::new(limits);
        budget.cells(matrix.rows(), matrix.cols())?;
        if self.matrix_hash != hash_matrix(matrix)? {
            return Err(HomologicalError::CertificateMismatch {
                identity: "matrix binding",
            });
        }
        check_candidate(matrix, &self.candidate, &mut budget)
    }
}

fn check_candidate(
    matrix: &BasicMatrix<Q>,
    candidate: &RankCandidate,
    budget: &mut RankBudget,
) -> Result<(), HomologicalError> {
    check_coefficients(matrix, candidate)?;
    let rank = candidate.image.cols();
    check_shapes(matrix, candidate, rank)?;
    for input in [
        matrix,
        &candidate.image,
        &candidate.coordinates,
        &candidate.image_retraction,
        &candidate.coordinate_section,
    ] {
        budget.cells(input.rows(), input.cols())?;
    }
    check_split_identities(matrix, candidate, rank, budget)
}

fn check_split_identities(
    matrix: &BasicMatrix<Q>,
    candidate: &RankCandidate,
    rank: usize,
    budget: &mut RankBudget,
) -> Result<(), HomologicalError> {
    if rank == 0 {
        if !matrix.as_slice().iter().all(num_traits::Zero::is_zero) {
            return Err(HomologicalError::CertificateMismatch { identity: "M=UV" });
        }
        // Admitted shapes make U,V,L,R empty for rank zero. M=0 is the
        // only nonvacuous identity; LU=VR=I_0 holds without dense loops.
        return Ok(());
    }
    preflight_split_work(matrix, rank, budget)?;
    let identity = identity(rank, budget)?;
    check_positive_split_identities(matrix, candidate, &identity, budget)
}

fn check_positive_split_identities(
    matrix: &BasicMatrix<Q>,
    candidate: &RankCandidate,
    identity: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<(), HomologicalError> {
    require_equal(
        &multiply(&candidate.image, &candidate.coordinates, budget)?,
        matrix,
        "M=UV",
    )?;
    require_equal(
        &multiply(&candidate.image_retraction, &candidate.image, budget)?,
        identity,
        "LU=I",
    )?;
    require_equal(
        &multiply(
            &candidate.coordinates,
            &candidate.coordinate_section,
            budget,
        )?,
        identity,
        "VR=I",
    )?;
    Ok(())
}

fn product_work(rows: usize, cols: usize, inner: usize) -> Result<usize, MatrixError> {
    rows.checked_mul(cols)
        .and_then(|n| n.checked_mul(inner))
        .and_then(|n| n.checked_mul(2))
        .ok_or(MatrixError::OperationCountOverflow)
}

fn preflight_split_work(
    matrix: &BasicMatrix<Q>,
    rank: usize,
    budget: &RankBudget,
) -> Result<(), MatrixError> {
    let factorization = product_work(matrix.rows(), matrix.cols(), rank)?;
    let retraction = product_work(rank, rank, matrix.rows())?;
    let section = product_work(rank, rank, matrix.cols())?;
    let total = factorization
        .checked_add(retraction)
        .and_then(|n| n.checked_add(section))
        .ok_or(MatrixError::OperationCountOverflow)?;
    // These three costs are known after shape admission. Check their aggregate
    // before allocating even I_r; individual products then charge the same sum.
    budget.requested(total).map(|_| ())
}

fn shape(matrix: &BasicMatrix<Q>, expected: (usize, usize)) -> Result<(), HomologicalError> {
    if matrix.shape() != expected {
        return Err(HomologicalError::ShapeMismatch {
            expected,
            got: matrix.shape(),
        });
    }
    Ok(())
}

fn check_shapes(
    m: &BasicMatrix<Q>,
    c: &RankCandidate,
    rank: usize,
) -> Result<(), HomologicalError> {
    if rank > m.rows().min(m.cols()) {
        return Err(HomologicalError::CertificateMismatch {
            identity: "rank dimension",
        });
    }
    shape(&c.image, (m.rows(), rank))?;
    shape(&c.coordinates, (rank, m.cols()))?;
    shape(&c.image_retraction, (rank, m.rows()))?;
    shape(&c.coordinate_section, (m.cols(), rank))
}

fn require_equal(
    left: &BasicMatrix<Q>,
    right: &BasicMatrix<Q>,
    identity: &'static str,
) -> Result<(), HomologicalError> {
    if left != right {
        return Err(HomologicalError::CertificateMismatch { identity });
    }
    Ok(())
}

fn identity(n: usize, budget: &RankBudget) -> Result<BasicMatrix<Q>, HomologicalError> {
    budget.cells(n, n)?;
    Ok(BasicMatrix::try_from_fn(n, n, |i, j| q(i64::from(i == j)))?)
}

/// Produce a rank factorization by elimination, then independently check it.
/// Gram matrices are invertible over Q because the columns/rows are independent.
/// Matrix and inversion refusals propagate as typed errors; failure emits no
/// certificate. Standard rational arithmetic and allocator behavior remain in
/// the declared runtime trust boundary.
/// Dense work is polynomial in matrix dimensions, with rational bit growth.
pub fn certify_rank(matrix: &BasicMatrix<Q>) -> Result<RankCertificate, HomologicalError> {
    certify_rank_with_limits(matrix, RankLimits::default())
}

pub fn certify_rank_with_limits(
    matrix: &BasicMatrix<Q>,
    limits: RankLimits,
) -> Result<RankCertificate, HomologicalError> {
    let mut budget = RankBudget::new(limits);
    budget.cells(matrix.rows(), matrix.cols())?;
    super::exact_scalar::admit_matrix(matrix)?;
    if matrix.as_slice().iter().all(num_traits::Zero::is_zero) {
        return RankCertificate::admit_with_budget(matrix, empty_candidate(matrix)?, &mut budget);
    }
    let (image, coordinates) = factorization(matrix, &mut budget)?;
    let image_retraction = left_inverse(&image, &mut budget)?;
    let coordinate_section =
        left_inverse(&coordinates.try_transpose()?, &mut budget)?.try_transpose()?;
    RankCertificate::admit_with_budget(
        matrix,
        RankCandidate {
            image,
            coordinates,
            image_retraction,
            coordinate_section,
        },
        &mut budget,
    )
}

fn empty_candidate(matrix: &BasicMatrix<Q>) -> Result<RankCandidate, HomologicalError> {
    Ok(RankCandidate {
        image: BasicMatrix::from_row_major(matrix.rows(), 0, vec![])?,
        coordinates: BasicMatrix::from_row_major(0, matrix.cols(), vec![])?,
        image_retraction: BasicMatrix::from_row_major(0, matrix.rows(), vec![])?,
        coordinate_section: BasicMatrix::from_row_major(matrix.cols(), 0, vec![])?,
    })
}

fn check_coefficients(m: &BasicMatrix<Q>, c: &RankCandidate) -> Result<(), HomologicalError> {
    for matrix in [
        m,
        &c.image,
        &c.coordinates,
        &c.image_retraction,
        &c.coordinate_section,
    ] {
        super::exact_scalar::admit_matrix(matrix)?;
    }
    Ok(())
}

fn factorization(
    matrix: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<(BasicMatrix<Q>, BasicMatrix<Q>), HomologicalError> {
    let (reduction, pivots) =
        rational_rref(matrix, budget).map_err(|source| HomologicalError::RankReductionFailed {
            source: ExactLinearAlgebraError::Matrix(source),
        })?;
    let rank = pivots.len();
    let image = BasicMatrix::try_from_fn_result(matrix.rows(), rank, |i, j| {
        let col = pivots.get(j).ok_or(HomologicalError::CertificateMismatch {
            identity: "pivot bounds",
        })?;
        Ok::<_, HomologicalError>(matrix.get(i, *col)?)
    })?;
    let coordinates = reduction.into_prefix_matrix(rank)?;
    Ok((image, coordinates))
}

/// (U^T U)^-1 U^T is a left inverse for a full-column-rank rational U.
fn left_inverse(
    image: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<BasicMatrix<Q>, HomologicalError> {
    let transpose = image.try_transpose()?;
    let gram = multiply(&transpose, image, budget)?;
    let inverse = inverse_with_budget(&gram, budget)?;
    multiply(&inverse, &transpose, budget)
}

/// Private closed-domain product: callers admit canonical coefficients and
/// shapes before entry. Borrowed dot products avoid cloning their operands.
fn multiply(
    left: &BasicMatrix<Q>,
    right: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<BasicMatrix<Q>, HomologicalError> {
    admit_rank_product(left, right, budget)?;
    if left.rows() == 0 || right.cols() == 0 {
        return Ok(BasicMatrix::from_row_major(
            left.rows(),
            right.cols(),
            vec![],
        )?);
    }
    Ok(BasicMatrix::try_from_fn_result(
        left.rows(),
        right.cols(),
        |row, col| {
            let mut sum = q(0);
            for inner in 0..left.cols() {
                sum += left.get_ref(row, inner)? * right.get_ref(inner, col)?;
            }
            Ok::<_, MatrixError>(sum)
        },
    )?)
}

fn admit_rank_product(
    left: &BasicMatrix<Q>,
    right: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<(), MatrixError> {
    if left.cols() != right.rows() {
        return Err(MatrixError::DimensionMismatch {
            left: left.shape(),
            right: right.shape(),
        });
    }
    budget.cells(left.rows(), right.cols())?;
    let operations = product_work(left.rows(), right.cols(), left.cols())?;
    budget.charge(operations)
}

fn inverse(matrix: &BasicMatrix<Q>) -> Result<BasicMatrix<Q>, HomologicalError> {
    inverse_with_budget(matrix, &mut RankBudget::new(RankLimits::default()))
}

fn inverse_with_budget(
    matrix: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<BasicMatrix<Q>, HomologicalError> {
    rational_inverse(matrix, budget)
        .map_err(|source| HomologicalError::RankInverseFailed { source })
}

fn rational_buffer<T>(count: usize) -> Result<Vec<T>, MatrixError> {
    let mut buffer = Vec::new();
    buffer
        .try_reserve_exact(count)
        .map_err(|_| MatrixError::AllocationFailed { requested: count })?;
    Ok(buffer)
}

fn reduction_work(rows: usize, cols: usize, width: usize) -> Result<usize, MatrixError> {
    if rows == 0 || cols == 0 {
        return Ok(0);
    }
    // At most min(rows,width) pivots. Each pivot normalizes <=cols entries
    // and performs <=rows*cols multiply/subtract pairs. Comparisons, scalar
    // representation costs and hashing are deliberately outside this count.
    rows.checked_mul(2)
        .and_then(|n| n.checked_add(1))
        .and_then(|n| n.checked_mul(cols))
        .and_then(|n| n.checked_mul(rows.min(width)))
        .ok_or(MatrixError::OperationCountOverflow)
}

/// Private, closed-Q elimination storage. Shape admission proves data.len() is
/// rows*cols. Only columns <width<=cols and rows <rows reach its kernels.
/// Earlier pivot columns are zero in every later pivot row. Pivot selection
/// supplies a nonzero divisor; all operations preserve canonical Q.
struct RationalRows {
    rows: usize,
    cols: usize,
    data: Vec<Q>,
}
impl RationalRows {
    fn copy(matrix: &BasicMatrix<Q>, budget: &RankBudget) -> Result<Self, MatrixError> {
        let count = budget.cells(matrix.rows(), matrix.cols())?;
        let mut data = rational_buffer(count)?;
        data.extend_from_slice(matrix.as_slice());
        Ok(Self {
            rows: matrix.rows(),
            cols: matrix.cols(),
            data,
        })
    }
    fn augmented_identity(
        matrix: &BasicMatrix<Q>,
        budget: &RankBudget,
    ) -> Result<Self, MatrixError> {
        let n = matrix.rows();
        let cols = n
            .checked_mul(2)
            .ok_or(MatrixError::DimensionOverflow { rows: n, cols: n })?;
        let count = budget.cells(n, cols)?;
        let mut data = rational_buffer(count)?;
        for index in 0..count {
            let (row, col) = (index / cols, index % cols);
            let value = if col < n {
                matrix.as_slice()[row * n + col].clone()
            } else {
                q(i64::from(col - n == row))
            };
            data.push(value);
        }
        Ok(Self {
            rows: n,
            cols,
            data,
        })
    }
    fn at(&self, row: usize, col: usize) -> &Q {
        &self.data[row * self.cols + col]
    }
    fn swap_rows(&mut self, first: usize, second: usize) {
        if first == second {
            return;
        }
        for col in 0..self.cols {
            self.data
                .swap(first * self.cols + col, second * self.cols + col);
        }
    }
    fn normalize(&mut self, row: usize, col: usize) {
        let start = row * self.cols;
        let pivot = std::mem::replace(&mut self.data[start + col], q(1));
        for value in &mut self.data[start + col + 1..start + self.cols] {
            *value /= &pivot;
        }
    }
    fn clear_row(&mut self, target: usize, pivot: usize, col: usize) {
        let (target, pivot) = distinct_rational_rows(&mut self.data, self.cols, target, pivot);
        let factor = std::mem::replace(&mut target[col], q(0));
        if num_traits::Zero::is_zero(&factor) {
            return;
        }
        for (entry, pivot_entry) in target[col + 1..].iter_mut().zip(&pivot[col + 1..]) {
            *entry -= &factor * pivot_entry;
        }
    }
    fn reduce_column(&mut self, row: usize, col: usize) -> bool {
        let Some(found) = (row..self.rows).find(|&r| !num_traits::Zero::is_zero(self.at(r, col)))
        else {
            return false;
        };
        self.swap_rows(row, found);
        self.normalize(row, col);
        for target in 0..self.rows {
            if target != row {
                self.clear_row(target, row, col);
            }
        }
        true
    }
    fn reduce(&mut self, width: usize) -> Result<Vec<usize>, MatrixError> {
        let mut pivots = rational_buffer(self.rows.min(width))?;
        for col in 0..width {
            if pivots.len() == self.rows {
                break;
            }
            if self.reduce_column(pivots.len(), col) {
                pivots.push(col);
            }
        }
        Ok(pivots)
    }
    fn into_prefix_matrix(mut self, rows: usize) -> Result<BasicMatrix<Q>, MatrixError> {
        // Caller passes rank<=original rows, hence rows*cols<=data.len().
        self.data.truncate(rows * self.cols);
        BasicMatrix::from_row_major(rows, self.cols, self.data)
    }
    fn into_right_block(self) -> Result<BasicMatrix<Q>, MatrixError> {
        let n = self.rows;
        let mut output = rational_buffer(n * n)?;
        for (index, value) in self.data.into_iter().enumerate() {
            if index % self.cols >= n {
                output.push(value);
            }
        }
        BasicMatrix::from_row_major(n, n, output)
    }
}

/// target!=pivot is established by reduce_column. Splitting at the later row
/// yields disjoint slices; every range lies within the admitted flat storage.
fn distinct_rational_rows(
    data: &mut [Q],
    cols: usize,
    target: usize,
    pivot: usize,
) -> (&mut [Q], &[Q]) {
    let split = target.max(pivot) * cols;
    let (before, after) = data.split_at_mut(split);
    if target < pivot {
        (
            &mut before[target * cols..(target + 1) * cols],
            &after[..cols],
        )
    } else {
        (
            &mut after[..cols],
            &before[pivot * cols..(pivot + 1) * cols],
        )
    }
}

fn rational_rref(
    matrix: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<(RationalRows, Vec<usize>), MatrixError> {
    budget.charge(reduction_work(matrix.rows(), matrix.cols(), matrix.cols())?)?;
    let mut workspace = RationalRows::copy(matrix, budget)?;
    let pivots = workspace.reduce(matrix.cols())?;
    Ok((workspace, pivots))
}

fn rational_inverse(
    matrix: &BasicMatrix<Q>,
    budget: &mut RankBudget,
) -> Result<BasicMatrix<Q>, ExactFieldError> {
    let n = matrix.rows();
    if n != matrix.cols() {
        return Err(ExactFieldError::NotSquare {
            operation: "rank certificate inverse",
            rows: n,
            cols: matrix.cols(),
        });
    }
    let cols = n
        .checked_mul(2)
        .ok_or(MatrixError::DimensionOverflow { rows: n, cols: n })?;
    budget.cells(n, cols)?;
    budget.charge(reduction_work(n, cols, n)?)?;
    let mut workspace = RationalRows::augmented_identity(matrix, budget)?;
    let pivots = workspace.reduce(n)?;
    if pivots.len() != n {
        return Err(ExactFieldError::Singular {
            rank: pivots.len(),
            size: n,
        });
    }
    Ok(workspace.into_right_block()?)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn inversion_failures_retain_a_typed_source() {
        let zero = BasicMatrix::zero(1, 1).unwrap();
        let error = inverse(&zero).unwrap_err();
        assert!(
            std::error::Error::source(&error).is_some(),
            "lost producer error: {error}"
        );
        assert!(matches!(
            error,
            HomologicalError::RankInverseFailed {
                source: crate::linear_algebra::ExactFieldError::Singular { rank: 0, size: 1 }
            }
        ));
        let rectangular = BasicMatrix::zero(1, 2).unwrap();
        assert!(matches!(
            inverse(&rectangular),
            Err(HomologicalError::RankInverseFailed {
                source: crate::linear_algebra::ExactFieldError::NotSquare {
                    rows: 1,
                    cols: 2,
                    ..
                }
            })
        ));
    }

    #[test]
    fn empty_shapes_with_huge_metadata_do_not_enumerate_the_shape() {
        let (send, receive) = std::sync::mpsc::channel();
        let worker = std::thread::spawn(move || {
            let mut ranks = Vec::new();
            for (rows, cols) in [(0, usize::MAX), (usize::MAX, 0), (0, 0), (0, 7), (7, 0)] {
                let matrix = BasicMatrix::from_row_major(rows, cols, Vec::<Q>::new()).unwrap();
                let certificate = certify_rank(&matrix).unwrap();
                certificate.verify_against(&matrix).unwrap();
                ranks.push(certificate.rank());
            }
            let _ = send.send(ranks);
        });
        let result = receive.recv_timeout(std::time::Duration::from_secs(2));
        assert!(
            result.is_ok(),
            "rank-zero producer enumerated a zero-area shape"
        );
        assert_eq!(result.unwrap(), vec![0; 5]);
        worker.join().unwrap();
    }

    fn matrix(rows: usize, cols: usize, values: Vec<Q>) -> BasicMatrix<Q> {
        BasicMatrix::from_row_major(rows, cols, values).unwrap()
    }
    fn independent_candidate() -> RankCandidate {
        let qr =
            |n, d| crate::linear_algebra::scalars::qr(n, d).expect("nonzero fixture denominator");
        RankCandidate {
            image: matrix(2, 1, vec![q(3), q(5)]),
            coordinates: matrix(1, 2, vec![q(2), q(3)]),
            image_retraction: matrix(1, 2, vec![qr(1, 3), q(0)]),
            coordinate_section: matrix(2, 1, vec![qr(1, 2), q(0)]),
        }
    }
    fn input() -> BasicMatrix<Q> {
        matrix(2, 2, vec![q(6), q(9), q(10), q(15)])
    }

    #[test]
    fn hand_constructed_certificate_and_each_independent_split_identity() {
        let m = input();
        let candidate = independent_candidate();
        let certificate = RankCertificate::try_admit(&m, candidate.clone()).unwrap();
        assert_eq!(certificate.rank(), 1);
        assert_eq!(certificate.candidate(), &candidate);
        certificate.verify_against(&m).unwrap();
        let mut bad = candidate.clone();
        bad.image_retraction = BasicMatrix::zero(1, 2).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&m, bad),
            Err(HomologicalError::CertificateMismatch { identity: "LU=I" })
        ));
        let mut bad = candidate.clone();
        bad.coordinate_section = BasicMatrix::zero(2, 1).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&m, bad),
            Err(HomologicalError::CertificateMismatch { identity: "VR=I" })
        ));
        let zero = BasicMatrix::zero(2, 2).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&zero, candidate),
            Err(HomologicalError::CertificateMismatch { identity: "M=UV" })
        ));
        assert!(certificate.verify_against(&zero).is_err());
    }

    #[test]
    fn every_candidate_role_enforces_shape_and_canonical_rationals() {
        for role in 0..4 {
            let mut candidate = independent_candidate();
            let bad = BasicMatrix::zero(1, 1).unwrap();
            match role {
                0 => candidate.image = bad,
                1 => candidate.coordinates = bad,
                2 => candidate.image_retraction = bad,
                _ => candidate.coordinate_section = bad,
            }
            assert!(matches!(
                RankCertificate::try_admit(&input(), candidate),
                Err(HomologicalError::ShapeMismatch { .. })
            ));
        }
        for bad in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(2.into(), 4.into()),
            Q::new_raw(1.into(), (-2).into()),
            Q::new_raw(0.into(), 2.into()),
        ] {
            let bad_input = matrix(1, 1, vec![bad.clone()]);
            assert!(matches!(
                certify_rank(&bad_input),
                Err(HomologicalError::InvalidRational { index: 0 })
            ));
            for role in 0..5 {
                let mut m = input();
                let mut candidate = independent_candidate();
                let target = match role {
                    0 => &mut m,
                    1 => &mut candidate.image,
                    2 => &mut candidate.coordinates,
                    3 => &mut candidate.image_retraction,
                    _ => &mut candidate.coordinate_section,
                };
                target.set(0, 0, bad.clone()).unwrap();
                assert!(
                    matches!(
                        RankCertificate::try_admit(&m, candidate),
                        Err(HomologicalError::InvalidRational { index: 0 })
                    ),
                    "role {role}"
                );
            }
        }
    }

    #[test]
    fn impossible_rank_is_refused_before_identity_allocation() {
        let candidate = RankCandidate {
            image: BasicMatrix::zero(0, usize::MAX).unwrap(),
            coordinates: BasicMatrix::zero(usize::MAX, 0).unwrap(),
            image_retraction: BasicMatrix::zero(usize::MAX, 0).unwrap(),
            coordinate_section: BasicMatrix::zero(0, usize::MAX).unwrap(),
        };
        assert!(matches!(
            RankCertificate::try_admit(&BasicMatrix::zero(0, 0).unwrap(), candidate),
            Err(HomologicalError::CertificateMismatch {
                identity: "rank dimension"
            })
        ));
    }
}

#[cfg(test)]
mod zero_rank_challenges {
    use super::*;
    #[test]
    fn zero_rank_handles_extreme_empty_metadata_without_dense_loops() {
        for (rows, cols) in [(usize::MAX, 0), (0, usize::MAX), (0, 0), (3, 4)] {
            let matrix = BasicMatrix::from_row_major(
                rows,
                cols,
                vec![q(0); rows.checked_mul(cols).unwrap()],
            )
            .unwrap();
            let certificate = certify_rank(&matrix).unwrap();
            assert_eq!(certificate.rank(), 0);
            assert_eq!(certificate.candidate().image.shape(), (rows, 0));
            assert_eq!(certificate.candidate().coordinates.shape(), (0, cols));
            assert_eq!(certificate.candidate().image_retraction.shape(), (0, rows));
            assert_eq!(
                certificate.candidate().coordinate_section.shape(),
                (cols, 0)
            );
            assert_eq!(certificate.verify_against(&matrix), Ok(()));
        }
    }
    #[test]
    fn zero_rank_shortcut_preserves_nonvacuous_identity_and_shape_checks() {
        let nonzero = BasicMatrix::from_row_major(1, 1, vec![q(1)]).unwrap();
        assert_eq!(
            RankCertificate::try_admit(&nonzero, empty_candidate(&nonzero).unwrap()).err(),
            Some(HomologicalError::CertificateMismatch { identity: "M=UV" })
        );
        let zero = BasicMatrix::from_row_major(2, 3, vec![q(0); 6]).unwrap();
        let mut candidate = empty_candidate(&zero).unwrap();
        candidate.coordinate_section = BasicMatrix::from_row_major(0, 0, vec![]).unwrap();
        assert!(matches!(
            RankCertificate::try_admit(&zero, candidate),
            Err(HomologicalError::ShapeMismatch { .. })
        ));
    }
}

#[cfg(test)]
mod producer_admission_challenges {
    use super::*;

    fn limits(cells: usize, operations: usize) -> RankLimits {
        RankLimits {
            max_matrix_cells: cells,
            max_scalar_operations: operations,
        }
    }
    fn scalar(value: i64) -> BasicMatrix<Q> {
        BasicMatrix::from_row_major(1, 1, vec![q(value)]).unwrap()
    }
    #[test]
    fn producer_and_checker_budgets_are_aggregate_and_inclusive() {
        let input = scalar(2);
        let certificate = certify_rank_with_limits(&input, limits(2, 29)).unwrap();
        assert_eq!(certificate.rank(), 1);
        assert!(matches!(
            certify_rank_with_limits(&input, limits(2, 28)),
            Err(HomologicalError::MatrixError(
                MatrixError::OperationLimitExceeded {
                    requested: 29,
                    limit: 28
                }
            ))
        ));
        assert_eq!(
            certificate.verify_against_with_limits(&input, limits(1, 6)),
            Ok(())
        );
        assert!(matches!(
            certificate.verify_against_with_limits(&input, limits(1, 5)),
            Err(HomologicalError::MatrixError(
                MatrixError::OperationLimitExceeded {
                    requested: 6,
                    limit: 5
                }
            ))
        ));
        assert!(matches!(
            certify_rank_with_limits(&input, limits(1, 29)),
            Err(HomologicalError::RankInverseFailed {
                source: ExactFieldError::Matrix(MatrixError::AllocationLimitExceeded {
                    requested: 2,
                    limit: 1
                })
            })
        ));
        assert_eq!(input, scalar(2));
    }
    #[test]
    fn zero_rank_requires_no_field_work_and_empty_shapes_require_no_cells() {
        for (rows, cols) in [(usize::MAX, 0), (0, usize::MAX), (0, 0)] {
            let matrix = BasicMatrix::from_row_major(rows, cols, vec![]).unwrap();
            let certificate = certify_rank_with_limits(&matrix, limits(0, 0)).unwrap();
            assert_eq!(
                certificate.verify_against_with_limits(&matrix, limits(0, 0)),
                Ok(())
            );
        }
        let zero = BasicMatrix::from_row_major(65, 65, vec![q(0); 4225]).unwrap();
        assert!(certify_rank(&zero).is_err());
        assert_eq!(
            certify_rank_with_limits(&zero, limits(4225, 0))
                .unwrap()
                .rank(),
            0
        );
    }
    #[test]
    fn failed_budget_charges_preserve_the_counter_and_reject_overflow() {
        let mut budget = RankBudget::new(limits(0, 3));
        budget.charge(3).unwrap();
        assert!(budget.charge(1).is_err());
        assert_eq!(budget.spent, 3);
        budget.spent = usize::MAX;
        assert_eq!(budget.charge(1), Err(MatrixError::OperationCountOverflow));
        assert_eq!(budget.spent, usize::MAX);
        assert_eq!(
            budget.cells(usize::MAX, 2),
            Err(MatrixError::DimensionOverflow {
                rows: usize::MAX,
                cols: 2
            })
        );
        assert_eq!(
            reduction_work(usize::MAX, 1, 1),
            Err(MatrixError::OperationCountOverflow)
        );
    }
    #[test]
    fn binding_refusal_has_its_declared_diagnostic_before_identity_replay() {
        let input = scalar(2);
        let certificate = certify_rank(&input).unwrap();
        assert_eq!(
            certificate.verify_against(&scalar(0)),
            Err(HomologicalError::CertificateMismatch {
                identity: "matrix binding"
            })
        );
        let raw = BasicMatrix::from_row_major(1, 1, vec![Q::new_raw(4.into(), 2.into())]).unwrap();
        assert_eq!(
            certificate.verify_against(&raw),
            Err(HomologicalError::InvalidRational { index: 0 })
        );
    }
    fn ternary_entries(mut code: usize) -> [i64; 6] {
        std::array::from_fn(|_| {
            let value = (code % 3) as i64 - 1;
            code /= 3;
            value
        })
    }
    fn minor_rank(entries: [i64; 6]) -> usize {
        let has_minor = [(0, 1), (0, 2), (1, 2)]
            .into_iter()
            .any(|(a, b)| entries[a] * entries[3 + b] - entries[b] * entries[3 + a] != 0);
        if has_minor {
            2
        } else {
            usize::from(entries.iter().any(|value| *value != 0))
        }
    }
    #[test]
    fn rectangular_rank_matches_independent_integer_minors() {
        for code in 0..729 {
            let entries = ternary_entries(code);
            let input = BasicMatrix::from_row_major(2, 3, entries.map(q).to_vec()).unwrap();
            let expected = minor_rank(entries);
            assert_eq!(certify_rank(&input).unwrap().rank(), expected);
            let transposed = input.try_transpose().unwrap();
            assert_eq!(certify_rank(&transposed).unwrap().rank(), expected);
        }
    }
    #[test]
    fn inverse_matches_integer_adjugates_without_using_matrix_multiplication() {
        for code in 0..81usize {
            let mut remaining = code;
            let [a, b, c, d] = std::array::from_fn(|_| {
                let value = (remaining % 3) as i64 - 1;
                remaining /= 3;
                value
            });
            check_adjugate(a, b, c, d);
        }
    }
    fn check_adjugate(a: i64, b: i64, c: i64, d: i64) {
        let input = BasicMatrix::from_row_major(2, 2, [a, b, c, d].map(q).to_vec()).unwrap();
        let determinant = a * d - b * c;
        if determinant == 0 {
            assert!(inverse(&input).is_err());
            return;
        }
        let expected = [d, -b, -c, a]
            .map(|value| crate::linear_algebra::scalars::qr(value, determinant).unwrap());
        assert_eq!(inverse(&input).unwrap().as_slice(), expected.as_slice());
    }
}
