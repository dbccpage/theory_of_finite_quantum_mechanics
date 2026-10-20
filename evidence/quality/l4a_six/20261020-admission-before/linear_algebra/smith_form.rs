use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError};
use num_bigint::BigInt;
use num_rational::Rational64;
use thiserror::Error;

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum SmithError {
    #[error("matrix error: {0}")]
    Matrix(#[from] MatrixError),

    #[error("empty matrix unsupported")]
    EmptyMatrixUnsupported,

    #[error("integer overflow")]
    Overflow,

    #[error("non-integer entry at row {row}, column {col}")]
    NonIntegerEntry { row: usize, col: usize },

    #[error("invalid Smith invariant; invariants must be positive")]
    InvalidInvariant,

    #[error("Smith divisibility violation: {left} does not divide {right}")]
    DivisibilityViolation { left: BigInt, right: BigInt },

    #[error("Smith normal form verification failed")]
    VerificationFailed,

    #[error("Smith normal form algorithm is incomplete")]
    AlgorithmIncomplete,

    #[error(
        "Smith normal form exceeded per-pivot iteration limit {limit} at pivot {pivot} after {iterations} iterations"
    )]
    IterationLimitExceeded {
        pivot: usize,
        iterations: usize,
        limit: usize,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SmithDiagonal {
    invariants: Vec<BigInt>,
}

impl SmithDiagonal {
    pub fn new_checked(invariants: Vec<BigInt>) -> Result<Self, SmithError> {
        let zero = BigInt::from(0);
        for d in &invariants {
            if d <= &zero {
                return Err(SmithError::InvalidInvariant);
            }
        }

        for pair in invariants.windows(2) {
            if (&pair[1] % &pair[0]) != zero {
                return Err(SmithError::DivisibilityViolation {
                    left: pair[0].clone(),
                    right: pair[1].clone(),
                });
            }
        }

        Ok(Self { invariants })
    }

    pub fn invariants(&self) -> &[BigInt] {
        &self.invariants
    }

    pub fn rank(&self) -> usize {
        self.invariants.len()
    }
}

pub struct SmithNormalForm {
    diagonal: SmithDiagonal,
    diagonal_matrix: BasicMatrix<BigInt>,
    u: BasicMatrix<BigInt>,
    v: BasicMatrix<BigInt>,
}

impl SmithNormalForm {
    pub fn diagonal(&self) -> &SmithDiagonal {
        &self.diagonal
    }

    pub fn diagonal_matrix(&self) -> &BasicMatrix<BigInt> {
        &self.diagonal_matrix
    }

    pub fn u(&self) -> &BasicMatrix<BigInt> {
        &self.u
    }

    pub fn v(&self) -> &BasicMatrix<BigInt> {
        &self.v
    }
}

fn bigint_abs(x: &BigInt) -> BigInt {
    if *x < BigInt::from(0) {
        -x.clone()
    } else {
        x.clone()
    }
}

const DEFAULT_SNF_PIVOT_ITERATION_LIMIT: usize = 10_000;

#[allow(clippy::needless_range_loop)]
pub fn smith_normal_form_checked(
    matrix: &BasicMatrix<BigInt>,
) -> Result<SmithNormalForm, SmithError> {
    smith_normal_form_checked_with_iteration_limit(matrix, DEFAULT_SNF_PIVOT_ITERATION_LIMIT)
}

/// Dense workspace limits count D, U and V cells together, before allocation.
/// They do not bound BigInt bit lengths, total process memory or elapsed time.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SmithLimits {
    pub max_workspace_cells: usize,
    pub max_pivot_iterations: usize,
}
impl Default for SmithLimits {
    fn default() -> Self {
        Self {
            max_workspace_cells: 4096,
            max_pivot_iterations: DEFAULT_SNF_PIVOT_ITERATION_LIMIT,
        }
    }
}

pub fn smith_normal_form_with_limits(
    matrix: &BasicMatrix<BigInt>,
    limits: SmithLimits,
) -> Result<SmithNormalForm, SmithError> {
    let mut workspace = SmithWorkspace::new(matrix, limits)?;
    for pivot in 0..matrix.rows().min(matrix.cols()) {
        workspace.reduce_pivot(pivot, limits.max_pivot_iterations)?;
    }
    workspace.finish(matrix)
}

fn smith_normal_form_checked_with_iteration_limit(
    matrix: &BasicMatrix<BigInt>,
    iteration_limit: usize,
) -> Result<SmithNormalForm, SmithError> {
    smith_normal_form_with_limits(
        matrix,
        SmithLimits {
            max_pivot_iterations: iteration_limit,
            ..SmithLimits::default()
        },
    )
}

fn admit_smith_workspace(m: usize, n: usize, limit: usize) -> Result<(), SmithError> {
    let cells = m
        .checked_mul(n)
        .and_then(|v| m.checked_mul(m).and_then(|u| v.checked_add(u)))
        .and_then(|v| n.checked_mul(n).and_then(|w| v.checked_add(w)))
        .ok_or(SmithError::Overflow)?;
    if cells > limit {
        return Err(SmithError::Matrix(MatrixError::AllocationLimitExceeded {
            requested: cells,
            limit,
        }));
    }
    Ok(())
}

fn integer_rows(
    rows: usize,
    cols: usize,
    mut value: impl FnMut(usize, usize) -> Result<BigInt, MatrixError>,
) -> Result<Vec<Vec<BigInt>>, SmithError> {
    let mut result = Vec::new();
    result
        .try_reserve_exact(rows)
        .map_err(|_| MatrixError::AllocationFailed { requested: rows })?;
    for row in 0..rows {
        let mut entries = Vec::new();
        entries
            .try_reserve_exact(cols)
            .map_err(|_| MatrixError::AllocationFailed { requested: cols })?;
        for col in 0..cols {
            entries.push(value(row, col)?);
        }
        result.push(entries);
    }
    Ok(result)
}

struct SmithWorkspace {
    d: Vec<Vec<BigInt>>,
    u: Vec<Vec<BigInt>>,
    // V is stored by columns. The same elementary row helper then updates V's columns.
    v: Vec<Vec<BigInt>>,
    m: usize,
    n: usize,
}
impl SmithWorkspace {
    fn new(matrix: &BasicMatrix<BigInt>, limits: SmithLimits) -> Result<Self, SmithError> {
        let (m, n) = matrix.shape();
        admit_smith_workspace(m, n, limits.max_workspace_cells)?;
        let d = integer_rows(m, n, |i, j| matrix.get(i, j))?;
        let u = integer_rows(m, m, |i, j| Ok(BigInt::from(usize::from(i == j))))?;
        let v = integer_rows(n, n, |i, j| Ok(BigInt::from(usize::from(i == j))))?;
        Ok(Self { d, u, v, m, n })
    }

    fn smallest_pivot(&self, k: usize) -> Option<(usize, usize)> {
        let mut best: Option<(BigInt, usize, usize)> = None;
        for i in k..self.m {
            for j in k..self.n {
                let value = &self.d[i][j];
                if value != &BigInt::from(0) {
                    let magnitude = bigint_abs(value);
                    consider_smith_pivot(&mut best, magnitude, i, j);
                }
            }
        }
        best.map(|(_, i, j)| (i, j))
    }

    fn position_pivot(&mut self, k: usize, i: usize, j: usize) {
        self.d.swap(i, k);
        self.u.swap(i, k);
        for row in &mut self.d {
            row.swap(j, k);
        }
        self.v.swap(j, k);
        if self.d[k][k] < BigInt::from(0) {
            negate_integer_row(&mut self.d[k]);
            negate_integer_row(&mut self.u[k]);
        }
    }

    fn clear_column(&mut self, k: usize) -> bool {
        let mut changed = false;
        for i in (k + 1)..self.m {
            if self.d[i][k] != BigInt::from(0) {
                let transformation = integer_pair_transform(&self.d[k][k], &self.d[i][k]);
                apply_integer_rows(&mut self.d, k, i, &transformation);
                apply_integer_rows(&mut self.u, k, i, &transformation);
                changed = true;
            }
        }
        changed
    }

    fn clear_row(&mut self, k: usize) -> bool {
        let mut changed = false;
        for j in (k + 1)..self.n {
            if self.d[k][j] != BigInt::from(0) {
                let transformation = integer_pair_transform(&self.d[k][k], &self.d[k][j]);
                for row in &mut self.d {
                    apply_integer_pair(row, k, j, &transformation);
                }
                apply_integer_rows(&mut self.v, k, j, &transformation);
                changed = true;
            }
        }
        changed
    }

    fn nondivisible_row(&self, k: usize) -> Option<usize> {
        for i in (k + 1)..self.m {
            for j in (k + 1)..self.n {
                if &self.d[i][j] % &self.d[k][k] != BigInt::from(0) {
                    return Some(i);
                }
            }
        }
        None
    }

    fn repair_divisibility(&mut self, k: usize) -> bool {
        let Some(i) = self.nondivisible_row(k) else {
            return false;
        };
        add_integer_row(&mut self.d, k, i);
        add_integer_row(&mut self.u, k, i);
        true
    }

    fn reduce_pivot(&mut self, k: usize, limit: usize) -> Result<(), SmithError> {
        let mut iterations = 0;
        while let Some((i, j)) = self.smallest_pivot(k) {
            if iterations == limit {
                return Err(SmithError::IterationLimitExceeded {
                    pivot: k,
                    iterations,
                    limit,
                });
            }
            iterations += 1;
            self.position_pivot(k, i, j);
            let column_changed = self.clear_column(k);
            let row_changed = self.clear_row(k);
            let repaired = self.repair_divisibility(k);
            if !column_changed && !row_changed && !repaired {
                break;
            }
        }
        Ok(())
    }

    fn finish(self, matrix: &BasicMatrix<BigInt>) -> Result<SmithNormalForm, SmithError> {
        let rank = (0..self.m.min(self.n))
            .filter(|&k| self.d[k][k] != BigInt::from(0))
            .count();
        let invariants = (0..rank).map(|k| bigint_abs(&self.d[k][k])).collect();
        let diagonal = SmithDiagonal::new_checked(invariants)?;
        let d_mat = BasicMatrix::try_from_fn(self.m, self.n, |i, j| {
            if i == j && i < rank {
                self.d[i][i].clone()
            } else {
                BigInt::from(0)
            }
        })?;
        let u = BasicMatrix::try_from_fn(self.m, self.m, |i, j| self.u[i][j].clone())?;
        let v = BasicMatrix::try_from_fn(self.n, self.n, |i, j| self.v[j][i].clone())?;
        verify_smith_identity(matrix, &u, &v, &d_mat)?;
        Ok(SmithNormalForm {
            diagonal,
            diagonal_matrix: d_mat,
            u,
            v,
        })
    }
}

// Each pair operation has first < second. Callers choose k and an index in k+1..dim.
// All row lengths and matrix indices come from the private, admitted workspace.
enum IntegerPairTransform {
    Subtract(BigInt),
    Bezout {
        x: BigInt,
        y: BigInt,
        q1: BigInt,
        q2: BigInt,
    },
}
fn integer_pair_transform(a: &BigInt, b: &BigInt) -> IntegerPairTransform {
    if b % a == BigInt::from(0) {
        return IntegerPairTransform::Subtract(b / a);
    }
    let (g, x, y) = egcd(a.clone(), b.clone());
    IntegerPairTransform::Bezout {
        x,
        y,
        q1: a / &g,
        q2: b / &g,
    }
}
fn apply_integer_values(a: &mut BigInt, b: &mut BigInt, t: &IntegerPairTransform) {
    match t {
        IntegerPairTransform::Subtract(q) => *b -= q * &*a,
        IntegerPairTransform::Bezout { x, y, q1, q2 } => {
            let left = x * &*a + y * &*b;
            let right = -q2 * &*a + q1 * &*b;
            *a = left;
            *b = right;
        }
    }
}
fn apply_integer_pair(row: &mut [BigInt], first: usize, second: usize, t: &IntegerPairTransform) {
    let (head, tail) = row.split_at_mut(second);
    apply_integer_values(&mut head[first], &mut tail[0], t);
}
fn apply_integer_rows(
    rows: &mut [Vec<BigInt>],
    first: usize,
    second: usize,
    t: &IntegerPairTransform,
) {
    let (head, tail) = rows.split_at_mut(second);
    for (left, right) in head[first].iter_mut().zip(tail[0].iter_mut()) {
        apply_integer_values(left, right, t);
    }
}
fn consider_smith_pivot(
    best: &mut Option<(BigInt, usize, usize)>,
    magnitude: BigInt,
    i: usize,
    j: usize,
) {
    if best.as_ref().map_or(true, |(old, _, _)| &magnitude < old) {
        *best = Some((magnitude, i, j));
    }
}

fn add_integer_row(rows: &mut [Vec<BigInt>], target: usize, source: usize) {
    let (head, tail) = rows.split_at_mut(source);
    for (left, right) in head[target].iter_mut().zip(tail[0].iter()) {
        *left += right;
    }
}
fn negate_integer_row(row: &mut [BigInt]) {
    for value in row {
        *value = -std::mem::take(value);
    }
}
fn verify_smith_identity(
    matrix: &BasicMatrix<BigInt>,
    u: &BasicMatrix<BigInt>,
    v: &BasicMatrix<BigInt>,
    d: &BasicMatrix<BigInt>,
) -> Result<(), SmithError> {
    if u.mul(matrix)?.mul(v)?.as_slice() != d.as_slice() {
        return Err(SmithError::VerificationFailed);
    }
    Ok(())
}

fn integer_numerator_from_rational64(val: &Rational64) -> Option<BigInt> {
    use num_traits::Zero;
    let d = *val.denom();
    if d == 0 {
        return None;
    }
    let n_big = BigInt::from(*val.numer());
    let d_big = BigInt::from(d);
    if (&n_big % &d_big).is_zero() {
        Some(n_big / d_big)
    } else {
        None
    }
}

fn integer_numerator_big(val: &num_rational::BigRational) -> Option<BigInt> {
    use num_traits::Zero;
    if val.denom().is_zero() {
        return None;
    }
    let n = val.numer();
    let d = val.denom();
    if (n % d).is_zero() {
        Some(n / d)
    } else {
        None
    }
}

pub fn from_rational64_integer_matrix(
    m: &BasicMatrix<Rational64>,
) -> Result<BasicMatrix<BigInt>, SmithError> {
    BasicMatrix::<BigInt>::try_from_fn_result(m.rows(), m.cols(), |row, col| {
        let val = m.get(row, col)?;
        integer_numerator_from_rational64(&val).ok_or(SmithError::NonIntegerEntry { row, col })
    })
}

pub fn from_bigrational_integer_matrix(
    m: &BasicMatrix<num_rational::BigRational>,
) -> Result<BasicMatrix<BigInt>, SmithError> {
    BasicMatrix::<BigInt>::try_from_fn_result(m.rows(), m.cols(), |row, col| {
        let val = m.get(row, col)?;
        integer_numerator_big(&val).ok_or(SmithError::NonIntegerEntry { row, col })
    })
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum SparseMatrixError {
    #[error("column count mismatch: expected {expected}, actual {actual}")]
    ColumnCountMismatch { expected: usize, actual: usize },

    #[error("row index out of bounds: row={row}, rows={rows}")]
    RowIndexOutOfBounds { row: usize, rows: usize },

    #[error("zero entry stored in sparse matrix")]
    ZeroEntryStored,

    #[error("duplicate row in sparse column: col={col}, row={row}")]
    DuplicateRowInColumn { col: usize, row: usize },

    #[error("dense conversion shape overflow: rows={rows}, cols={cols}")]
    ShapeOverflow { rows: usize, cols: usize },

    #[error("matrix error: {0}")]
    Matrix(#[from] MatrixError),
}

pub struct SparseColMatrix {
    rows: usize,
    cols: usize,
    columns: Vec<Vec<(usize, BigInt)>>,
}

impl SparseColMatrix {
    pub fn new_checked(
        rows: usize,
        cols: usize,
        mut columns: Vec<Vec<(usize, BigInt)>>,
    ) -> Result<Self, SparseMatrixError> {
        if columns.len() != cols {
            return Err(SparseMatrixError::ColumnCountMismatch {
                expected: cols,
                actual: columns.len(),
            });
        }

        let zero = BigInt::from(0);

        for (j, col) in columns.iter_mut().enumerate() {
            col.sort_by_key(|(row, _)| *row);

            let mut prev = None;
            for (row, value) in col.iter() {
                if *row >= rows {
                    return Err(SparseMatrixError::RowIndexOutOfBounds { row: *row, rows });
                }

                if value == &zero {
                    return Err(SparseMatrixError::ZeroEntryStored);
                }

                if prev == Some(*row) {
                    return Err(SparseMatrixError::DuplicateRowInColumn { col: j, row: *row });
                }

                prev = Some(*row);
            }
        }

        Ok(Self {
            rows,
            cols,
            columns,
        })
    }

    pub fn rows(&self) -> usize {
        self.rows
    }

    pub fn cols(&self) -> usize {
        self.cols
    }

    pub fn columns(&self) -> &[Vec<(usize, BigInt)>] {
        &self.columns
    }

    pub fn mul_vec(&self, v: &[BigInt]) -> Result<Vec<BigInt>, SparseMatrixError> {
        if v.len() != self.cols {
            return Err(SparseMatrixError::ColumnCountMismatch {
                expected: self.cols,
                actual: v.len(),
            });
        }
        let mut result = vec![BigInt::from(0); self.rows];
        for (j, col) in self.columns.iter().enumerate() {
            for (row, val) in col {
                result[*row] += val * &v[j];
            }
        }
        Ok(result)
    }

    pub fn to_dense(&self) -> Result<BasicMatrix<BigInt>, SparseMatrixError> {
        let total = self
            .rows
            .checked_mul(self.cols)
            .ok_or(SparseMatrixError::ShapeOverflow {
                rows: self.rows,
                cols: self.cols,
            })?;
        let mut data = vec![BigInt::from(0); total];
        for (j, col) in self.columns.iter().enumerate() {
            for (row, val) in col {
                let idx = row
                    .checked_mul(self.cols)
                    .and_then(|rc| rc.checked_add(j))
                    .ok_or(SparseMatrixError::ShapeOverflow {
                        rows: self.rows,
                        cols: self.cols,
                    })?;
                data[idx] = val.clone();
            }
        }
        BasicMatrix::from_row_major(self.rows, self.cols, data).map_err(SparseMatrixError::Matrix)
    }

    pub fn from_dense(m: &BasicMatrix<BigInt>) -> Self {
        let zero = BigInt::from(0);
        let mut columns = Vec::with_capacity(m.cols());
        for j in 0..m.cols() {
            let mut col = Vec::new();
            for i in 0..m.rows() {
                let val = m.get(i, j).expect("index in bounds");
                if val != zero {
                    col.push((i, val));
                }
            }
            columns.push(col);
        }
        Self {
            rows: m.rows(),
            cols: m.cols(),
            columns,
        }
    }
}

pub struct SparseColumnGcdProfile {
    pub values: Vec<BigInt>,
    pub warning: &'static str,
}

fn egcd(a: BigInt, b: BigInt) -> (BigInt, BigInt, BigInt) {
    let (mut old_r, mut r) = (a, b);
    let (mut old_x, mut x) = (BigInt::from(1), BigInt::from(0));
    let (mut old_y, mut y) = (BigInt::from(0), BigInt::from(1));
    while r != BigInt::from(0) {
        let q = &old_r / &r;
        let next_r = &old_r - &q * &r;
        let next_x = &old_x - &q * &x;
        let next_y = &old_y - &q * &y;
        (old_r, r) = (r, next_r);
        (old_x, x) = (x, next_x);
        (old_y, y) = (y, next_y);
    }
    if old_r < BigInt::from(0) {
        (-old_r, -old_x, -old_y)
    } else {
        (old_r, old_x, old_y)
    }
}

pub fn sparse_column_gcd_heuristic(matrix: &SparseColMatrix) -> SparseColumnGcdProfile {
    let mut cols = matrix.columns.to_vec();
    let mut invariants = Vec::new();

    let mut active = cols.len();
    let zero = BigInt::from(0);

    while active > 0 {
        let mut pivot = None;
        for (j, col) in cols.iter().enumerate().take(active) {
            if !col.is_empty() {
                pivot = Some(j);
                break;
            }
        }

        let Some(pj) = pivot else {
            break;
        };

        let pivot_col = cols.swap_remove(pj);
        active -= 1;

        let mut d = if pivot_col[0].1 >= zero {
            pivot_col[0].1.clone()
        } else {
            -pivot_col[0].1.clone()
        };

        for (_, v) in &pivot_col {
            let abs_v = if v >= &zero { v.clone() } else { -v.clone() };
            d = egcd(d, abs_v).0;
        }

        if d == zero {
            continue;
        }

        invariants.push(d);

        for col in &mut cols[..active] {
            col.retain(|(r, _v)| !pivot_col.iter().any(|(pr, _)| pr == r));
        }
    }

    SparseColumnGcdProfile {
        values: invariants,
        warning: "This is a heuristic and does not necessarily produce certified Smith invariants.",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn integer_matrix_conversion_accepts_unreduced_integers_and_refuses_fractions() {
        use num_rational::{BigRational, Rational64};

        let rational64 = BasicMatrix::from_row_major(
            1,
            3,
            vec![
                Rational64::new_raw(4, 2),
                Rational64::new_raw(2, -1),
                Rational64::new_raw(0, 5),
            ],
        )
        .unwrap();
        let converted = from_rational64_integer_matrix(&rational64).unwrap();
        assert_eq!(converted.get(0, 0).unwrap(), BigInt::from(2));
        assert_eq!(converted.get(0, 1).unwrap(), BigInt::from(-2));
        assert_eq!(converted.get(0, 2).unwrap(), BigInt::from(0));

        let fraction = BasicMatrix::from_row_major(1, 1, vec![Rational64::new(1, 2)]).unwrap();
        assert_eq!(
            from_rational64_integer_matrix(&fraction).unwrap_err(),
            SmithError::NonIntegerEntry { row: 0, col: 0 }
        );
        let zero_denom =
            BasicMatrix::from_row_major(1, 1, vec![Rational64::new_raw(1, 0)]).unwrap();
        assert!(matches!(
            from_rational64_integer_matrix(&zero_denom),
            Err(SmithError::NonIntegerEntry { row: 0, col: 0 })
        ));

        let big = BasicMatrix::from_row_major(
            1,
            1,
            vec![BigRational::new_raw(BigInt::from(6), BigInt::from(3))],
        )
        .unwrap();
        let converted = from_bigrational_integer_matrix(&big).unwrap();
        assert_eq!(converted.get(0, 0).unwrap(), BigInt::from(2));
        let big_fraction = BasicMatrix::from_row_major(
            1,
            1,
            vec![BigRational::new(BigInt::from(1), BigInt::from(3))],
        )
        .unwrap();
        assert_eq!(
            from_bigrational_integer_matrix(&big_fraction).unwrap_err(),
            SmithError::NonIntegerEntry { row: 0, col: 0 }
        );
    }

    #[test]
    fn smith_diagonal_rejects_nonpositive_invariants() {
        let invariants = vec![BigInt::from(0), BigInt::from(2)];
        let result = SmithDiagonal::new_checked(invariants);
        assert!(matches!(result, Err(SmithError::InvalidInvariant)));

        let invariants_neg = vec![BigInt::from(-2), BigInt::from(4)];
        let result_neg = SmithDiagonal::new_checked(invariants_neg);
        assert!(matches!(result_neg, Err(SmithError::InvalidInvariant)));
    }

    #[test]
    fn smith_diagonal_rejects_divisibility_failure() {
        let invariants = vec![BigInt::from(2), BigInt::from(3)];
        let result = SmithDiagonal::new_checked(invariants);
        assert!(matches!(
            result,
            Err(SmithError::DivisibilityViolation { .. })
        ));
    }

    #[test]
    fn smith_diagonal_accepts_2_6_30() {
        let invariants = vec![BigInt::from(2), BigInt::from(6), BigInt::from(30)];
        let result = SmithDiagonal::new_checked(invariants);
        assert!(result.is_ok());
    }

    #[test]
    fn sparse_matrix_rejects_bad_column_count() {
        let columns = vec![vec![(0, BigInt::from(1))]];
        let result = SparseColMatrix::new_checked(2, 2, columns);
        assert!(matches!(
            result,
            Err(SparseMatrixError::ColumnCountMismatch { .. })
        ));
    }

    #[test]
    fn sparse_matrix_rejects_row_out_of_bounds() {
        let columns = vec![vec![(2, BigInt::from(1))]];
        let result = SparseColMatrix::new_checked(2, 1, columns);
        assert!(matches!(
            result,
            Err(SparseMatrixError::RowIndexOutOfBounds { .. })
        ));
    }

    #[test]
    fn sparse_matrix_rejects_zero_entry() {
        let columns = vec![vec![(0, BigInt::from(0))]];
        let result = SparseColMatrix::new_checked(2, 1, columns);
        assert!(matches!(result, Err(SparseMatrixError::ZeroEntryStored)));
    }

    #[test]
    fn sparse_matrix_rejects_duplicate_row() {
        let columns = vec![vec![(0, BigInt::from(1)), (0, BigInt::from(2))]];
        let result = SparseColMatrix::new_checked(2, 1, columns);
        assert!(matches!(
            result,
            Err(SparseMatrixError::DuplicateRowInColumn { .. })
        ));
    }

    #[test]
    fn sparse_column_gcd_heuristic_is_not_certified() {
        let columns = vec![vec![(0, BigInt::from(2)), (1, BigInt::from(4))]];
        let matrix = SparseColMatrix::new_checked(2, 1, columns).unwrap();
        let profile = sparse_column_gcd_heuristic(&matrix);
        assert_eq!(
            profile.warning,
            "This is a heuristic and does not necessarily produce certified Smith invariants."
        );
    }

    fn check_unimodular(m: &BasicMatrix<BigInt>) {
        let n = m.rows();
        assert_eq!(n, m.cols(), "transformation matrix must be square");
        if n == 0 {
            return;
        }
        let m_q = BasicMatrix::<num_rational::BigRational>::try_from_fn(n, n, |i, j| {
            num_rational::BigRational::from_integer(m.get(i, j).unwrap())
        })
        .expect("matrix conversion to BigRational");
        let det = crate::linear_algebra::elimination::determinant(&m_q).expect("det computation");
        let one = num_rational::BigRational::from_integer(BigInt::from(1));
        let neg_one = num_rational::BigRational::from_integer(BigInt::from(-1));
        assert!(
            det == one || det == neg_one,
            "transformation matrix must be unimodular (det in {{-1, 1}}), got {det}"
        );
    }

    fn verify_snf(matrix: &BasicMatrix<BigInt>, snf: &SmithNormalForm) {
        let ua = snf.u().mul(matrix).expect("U*A");
        let uav = ua.mul(snf.v()).expect("U*A*V");
        assert_eq!(
            uav.as_slice(),
            snf.diagonal_matrix().as_slice(),
            "U*A*V != D"
        );
        check_unimodular(snf.u());
        check_unimodular(snf.v());
    }

    fn triangle_incidence_matrix() -> BasicMatrix<BigInt> {
        BasicMatrix::from_row_major(
            3,
            3,
            vec![
                BigInt::from(-1),
                BigInt::from(1),
                BigInt::from(0),
                BigInt::from(0),
                BigInt::from(-1),
                BigInt::from(1),
                BigInt::from(-1),
                BigInt::from(0),
                BigInt::from(1),
            ],
        )
        .unwrap()
    }

    #[test]
    fn snf_zero_matrix() {
        let m = BasicMatrix::<BigInt>::try_from_fn(2, 2, |_, _| BigInt::from(0)).unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 0);
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_non_divisible_2x2() {
        let m = BasicMatrix::from_row_major(
            2,
            2,
            vec![
                BigInt::from(2),
                BigInt::from(0),
                BigInt::from(0),
                BigInt::from(3),
            ],
        )
        .unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 2);
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(1), BigInt::from(6)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_identity_2x2() {
        let m = BasicMatrix::<BigInt>::try_from_fn(2, 2, |i, j| {
            if i == j {
                BigInt::from(1)
            } else {
                BigInt::from(0)
            }
        })
        .unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 2);
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(1), BigInt::from(1)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_identity_3x3() {
        let m = BasicMatrix::<BigInt>::try_from_fn(3, 3, |i, j| {
            if i == j {
                BigInt::from(1)
            } else {
                BigInt::from(0)
            }
        })
        .unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 3);
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(1), BigInt::from(1), BigInt::from(1)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_2x4_6x8() {
        let m = BasicMatrix::from_row_major(
            2,
            2,
            vec![
                BigInt::from(2),
                BigInt::from(4),
                BigInt::from(6),
                BigInt::from(8),
            ],
        )
        .unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 2);
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(2), BigInt::from(4)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_rectangular_2x3() {
        let m = BasicMatrix::from_row_major(
            2,
            3,
            vec![
                BigInt::from(1),
                BigInt::from(2),
                BigInt::from(3),
                BigInt::from(4),
                BigInt::from(5),
                BigInt::from(6),
            ],
        )
        .unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 2);
        verify_snf(&m, &snf);
        let invs = snf.diagonal().invariants();
        assert_eq!(&invs[1] % &invs[0], BigInt::from(0));
    }

    #[test]
    fn snf_rectangular_3x2() {
        let m = BasicMatrix::from_row_major(
            3,
            2,
            vec![
                BigInt::from(1),
                BigInt::from(2),
                BigInt::from(3),
                BigInt::from(4),
                BigInt::from(5),
                BigInt::from(6),
            ],
        )
        .unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 2);
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_triangle_incidence() {
        let m = triangle_incidence_matrix();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 2);
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(1), BigInt::from(1)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_triangle_incidence_completes_with_bounded_pivot_budget() {
        let m = triangle_incidence_matrix();
        let snf = smith_normal_form_checked_with_iteration_limit(&m, 16)
            .expect("triangle incidence should not exhaust a bounded pivot budget");
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(1), BigInt::from(1)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_iteration_limit_is_a_typed_refusal() {
        let m = BasicMatrix::from_row_major(1, 1, vec![BigInt::from(7)]).unwrap();
        let error = match smith_normal_form_checked_with_iteration_limit(&m, 0) {
            Err(error) => error,
            Ok(_) => panic!("zero pivot budget must refuse a nonzero matrix"),
        };
        assert_eq!(
            error,
            SmithError::IterationLimitExceeded {
                pivot: 0,
                iterations: 0,
                limit: 0,
            }
        );
    }

    #[test]
    fn snf_iteration_limit_allows_one_pivot_pass() {
        let m = BasicMatrix::from_row_major(1, 1, vec![BigInt::from(7)]).unwrap();
        let snf = smith_normal_form_checked_with_iteration_limit(&m, 1)
            .expect("one populated pivot should fit a budget of one");
        assert_eq!(snf.diagonal().invariants(), &[BigInt::from(7)]);
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_iteration_limit_counts_repeated_pivot_repairs() {
        let m = BasicMatrix::from_row_major(
            2,
            2,
            vec![
                BigInt::from(1),
                BigInt::from(1),
                BigInt::from(0),
                BigInt::from(1),
            ],
        )
        .unwrap();

        let error = match smith_normal_form_checked_with_iteration_limit(&m, 1) {
            Err(error) => error,
            Ok(_) => panic!("one pivot pass must not certify a matrix that needs two"),
        };
        assert_eq!(
            error,
            SmithError::IterationLimitExceeded {
                pivot: 0,
                iterations: 1,
                limit: 1,
            }
        );

        let snf = smith_normal_form_checked_with_iteration_limit(&m, 2)
            .expect("two pivot passes should certify the matrix");
        assert_eq!(
            snf.diagonal().invariants(),
            &[BigInt::from(1), BigInt::from(1)]
        );
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_single_entry() {
        let m = BasicMatrix::from_row_major(1, 1, vec![BigInt::from(7)]).unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 1);
        assert_eq!(snf.diagonal().invariants(), &[BigInt::from(7)]);
        verify_snf(&m, &snf);
    }

    #[test]
    fn snf_empty_matrix() {
        let m = BasicMatrix::<BigInt>::try_from_fn(0, 0, |_, _| BigInt::from(0)).unwrap();
        let snf = smith_normal_form_checked(&m).unwrap();
        assert_eq!(snf.diagonal().rank(), 0);
    }

    #[test]
    fn sparse_col_mul_vec_identity_2x2() {
        let columns = vec![vec![(0, BigInt::from(1))], vec![(1, BigInt::from(1))]];
        let m = SparseColMatrix::new_checked(2, 2, columns).unwrap();
        let v = vec![BigInt::from(3), BigInt::from(7)];
        let result = m.mul_vec(&v).unwrap();
        assert_eq!(result, vec![BigInt::from(3), BigInt::from(7)]);
    }

    #[test]
    fn sparse_col_mul_vec_known_values() {
        let columns = vec![vec![(0, BigInt::from(2))], vec![(1, BigInt::from(3))]];
        let m = SparseColMatrix::new_checked(2, 2, columns).unwrap();
        let v = vec![BigInt::from(4), BigInt::from(5)];
        let result = m.mul_vec(&v).unwrap();
        assert_eq!(result, vec![BigInt::from(8), BigInt::from(15)]);
    }

    #[test]
    fn sparse_col_mul_vec_rectangular() {
        let columns = vec![
            vec![(0, BigInt::from(1))],
            vec![(1, BigInt::from(3))],
            vec![(0, BigInt::from(2))],
        ];
        let m = SparseColMatrix::new_checked(2, 3, columns).unwrap();
        let v = vec![BigInt::from(1), BigInt::from(2), BigInt::from(3)];
        let result = m.mul_vec(&v).unwrap();
        assert_eq!(result, vec![BigInt::from(7), BigInt::from(6)]);
    }

    #[test]
    fn sparse_col_mul_vec_dimension_mismatch() {
        let columns = vec![vec![(0, BigInt::from(1))]];
        let m = SparseColMatrix::new_checked(1, 1, columns).unwrap();
        let v = vec![BigInt::from(1), BigInt::from(2)];
        assert!(matches!(
            m.mul_vec(&v),
            Err(SparseMatrixError::ColumnCountMismatch { .. })
        ));
    }

    #[test]
    fn sparse_col_to_dense_roundtrip() {
        let dense = BasicMatrix::from_row_major(
            2,
            3,
            vec![
                BigInt::from(1),
                BigInt::from(0),
                BigInt::from(3),
                BigInt::from(0),
                BigInt::from(2),
                BigInt::from(0),
            ],
        )
        .unwrap();
        let sparse = SparseColMatrix::from_dense(&dense);
        let recovered = sparse.to_dense().unwrap();
        assert_eq!(dense.as_slice(), recovered.as_slice());
        assert_eq!(dense.rows(), recovered.rows());
        assert_eq!(dense.cols(), recovered.cols());
    }

    #[test]
    fn sparse_col_to_dense_zero_matrix() {
        let dense = BasicMatrix::<BigInt>::try_from_fn(3, 2, |_, _| BigInt::from(0)).unwrap();
        let sparse = SparseColMatrix::from_dense(&dense);
        let recovered = sparse.to_dense().unwrap();
        assert_eq!(dense.as_slice(), recovered.as_slice());
        for col in sparse.columns() {
            assert!(col.is_empty());
        }
    }

    #[test]
    fn sparse_col_mul_vec_matches_dense() {
        let dense = BasicMatrix::from_row_major(
            2,
            2,
            vec![
                BigInt::from(1),
                BigInt::from(-2),
                BigInt::from(3),
                BigInt::from(4),
            ],
        )
        .unwrap();
        let sparse = SparseColMatrix::from_dense(&dense);
        let v = vec![BigInt::from(5), BigInt::from(6)];
        let sparse_result = sparse.mul_vec(&v).unwrap();

        let v_mat = BasicMatrix::from_row_major(2, 1, v).unwrap();
        let dense_result = dense.mul(&v_mat).unwrap();
        assert_eq!(sparse_result[0], dense_result.as_slice()[0]);
        assert_eq!(sparse_result[1], dense_result.as_slice()[1]);
    }

    #[test]
    fn sparse_col_to_dense_overflow_refused() {
        let rows = 1usize << (usize::BITS - 1);
        let sparse =
            SparseColMatrix::new_checked(rows, 2, vec![vec![(0, BigInt::from(1))], vec![]])
                .unwrap();
        let res = sparse.to_dense();
        assert!(matches!(res, Err(SparseMatrixError::ShapeOverflow { .. })));
    }

    #[test]
    fn integer_matrix_conversion_handles_i64_extremes_and_negative_denominators() {
        // (MIN, -1) -> 2^63
        let r1 = Rational64::new_raw(i64::MIN, -1);
        let expected1 = BigInt::from(i64::MAX) + BigInt::from(1);
        assert_eq!(integer_numerator_from_rational64(&r1), Some(expected1));

        // (MIN, 1) -> -2^63
        let r2 = Rational64::new_raw(i64::MIN, 1);
        let expected2 = BigInt::from(i64::MIN);
        assert_eq!(integer_numerator_from_rational64(&r2), Some(expected2));

        // (MIN, MIN) -> 1
        let r3 = Rational64::new_raw(i64::MIN, i64::MIN);
        assert_eq!(
            integer_numerator_from_rational64(&r3),
            Some(BigInt::from(1))
        );

        // (1, MIN) -> not an integer
        let r4 = Rational64::new_raw(1, i64::MIN);
        assert_eq!(integer_numerator_from_rational64(&r4), None);

        // Denominator 0 -> None
        let r5 = Rational64::new_raw(5, 0);
        assert_eq!(integer_numerator_from_rational64(&r5), None);
    }

    #[test]
    fn snf_empty_rectangular_matrices() {
        let m03 = BasicMatrix::<BigInt>::try_from_fn(0, 3, |_, _| BigInt::from(0)).unwrap();
        let snf03 = smith_normal_form_checked(&m03).unwrap();
        assert_eq!(snf03.diagonal().rank(), 0);
        assert_eq!(snf03.u().shape(), (0, 0));
        assert_eq!(snf03.v().shape(), (3, 3));
        verify_snf(&m03, &snf03);

        let m30 = BasicMatrix::<BigInt>::try_from_fn(3, 0, |_, _| BigInt::from(0)).unwrap();
        let snf30 = smith_normal_form_checked(&m30).unwrap();
        assert_eq!(snf30.diagonal().rank(), 0);
        assert_eq!(snf30.u().shape(), (3, 3));
        assert_eq!(snf30.v().shape(), (0, 0));
        verify_snf(&m30, &snf30);
    }

    #[test]
    fn unimodularity_verifier_rejects_non_unimodular_matrix() {
        let non_unimodular = BasicMatrix::from_row_major(1, 1, vec![BigInt::from(2)]).unwrap();
        let m_q = BasicMatrix::<num_rational::BigRational>::try_from_fn(1, 1, |i, j| {
            num_rational::BigRational::from_integer(non_unimodular.get(i, j).unwrap())
        })
        .unwrap();
        let det = crate::linear_algebra::elimination::determinant(&m_q).unwrap();
        assert_eq!(
            det,
            num_rational::BigRational::from_integer(BigInt::from(2))
        );
    }
}

#[cfg(test)]
mod admitted_smith_challenges {
    use super::*;
    use num_integer::Integer;
    use num_traits::Signed;

    #[test]
    fn smith_identity_checker_rejects_a_false_diagonal() {
        let identity = BasicMatrix::from_row_major(1, 1, vec![BigInt::from(1)]).unwrap();
        let zero = BasicMatrix::from_row_major(1, 1, vec![BigInt::from(0)]).unwrap();
        assert_eq!(
            verify_smith_identity(&identity, &identity, &identity, &zero),
            Err(SmithError::VerificationFailed)
        );
    }

    fn det_three(m: &BasicMatrix<BigInt>) -> BigInt {
        let v = m.as_slice();
        &v[0] * (&v[4] * &v[8] - &v[5] * &v[7]) - &v[1] * (&v[3] * &v[8] - &v[5] * &v[6])
            + &v[2] * (&v[3] * &v[7] - &v[4] * &v[6])
    }
    fn expected_two_by_three(v: [i64; 6]) -> Vec<BigInt> {
        let first = v.iter().fold(0i64, |g, x| g.gcd(x));
        if first == 0 {
            return vec![];
        }
        let minors = [
            v[0] * v[4] - v[1] * v[3],
            v[0] * v[5] - v[2] * v[3],
            v[1] * v[5] - v[2] * v[4],
        ];
        let product = minors.iter().fold(0i64, |g, x| g.gcd(x));
        if product == 0 {
            vec![first.into()]
        } else {
            vec![first.into(), (product / first).into()]
        }
    }
    #[test]
    fn smith_grid_matches_determinantal_divisors_and_unimodular_transforms() {
        for mut code in 0..729 {
            let entries: [i64; 6] = std::array::from_fn(|_| {
                let n = code % 3 - 1;
                code /= 3;
                n
            });
            let matrix =
                BasicMatrix::from_row_major(2, 3, entries.into_iter().map(BigInt::from).collect())
                    .unwrap();
            let snf = smith_normal_form_checked(&matrix).unwrap();
            assert_eq!(snf.diagonal().invariants(), expected_two_by_three(entries));
            let u = snf.u().as_slice();
            assert_eq!((&u[0] * &u[3] - &u[1] * &u[2]).abs(), BigInt::from(1));
            assert_eq!(det_three(snf.v()).abs(), BigInt::from(1));
        }
    }
    #[test]
    fn smith_workspace_budget_is_aggregate_inclusive_and_precedes_allocation() {
        let matrix = BasicMatrix::from_row_major(2, 3, vec![BigInt::from(1); 6]).unwrap();
        let limits = SmithLimits {
            max_workspace_cells: 19,
            ..SmithLimits::default()
        };
        assert!(smith_normal_form_with_limits(&matrix, limits).is_ok());
        let error = smith_normal_form_with_limits(
            &matrix,
            SmithLimits {
                max_workspace_cells: 18,
                ..limits
            },
        )
        .err()
        .unwrap();
        assert_eq!(
            error,
            SmithError::Matrix(MatrixError::AllocationLimitExceeded {
                requested: 19,
                limit: 18
            })
        );
        let huge = BasicMatrix::from_row_major(usize::MAX, 0, vec![]).unwrap();
        assert_eq!(
            smith_normal_form_checked(&huge).err(),
            Some(SmithError::Overflow)
        );
    }
    #[test]
    fn iterative_bezout_matches_signed_integer_gcd() {
        for a in -32i64..=32 {
            for b in -32i64..=32 {
                let (g, x, y) = egcd(a.into(), b.into());
                assert_eq!(g, BigInt::from(a.gcd(&b)));
                assert_eq!(&x * BigInt::from(a) + &y * BigInt::from(b), g);
            }
        }
    }
    #[test]
    fn iterative_bezout_handles_long_euclidean_chains() {
        let (mut a, mut b) = (BigInt::from(0), BigInt::from(1));
        for _ in 0..2000 {
            let next = &a + &b;
            a = b;
            b = next;
        }
        let (g, x, y) = egcd(a.clone(), b.clone());
        assert_eq!(g, BigInt::from(1));
        assert_eq!(x * a + y * b, g);
    }
}
