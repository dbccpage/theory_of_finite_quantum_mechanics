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

fn bigint_identity(n: usize) -> BasicMatrix<BigInt> {
    BasicMatrix::<BigInt>::try_from_fn(n, n, |i, j| {
        if i == j {
            BigInt::from(1)
        } else {
            BigInt::from(0)
        }
    })
    .expect("identity creation should succeed")
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

#[allow(clippy::needless_range_loop)]
fn smith_normal_form_checked_with_iteration_limit(
    matrix: &BasicMatrix<BigInt>,
    iteration_limit: usize,
) -> Result<SmithNormalForm, SmithError> {
    let m = matrix.rows();
    let n = matrix.cols();
    let zero = BigInt::from(0);

    if m == 0 || n == 0 {
        let diag = SmithDiagonal { invariants: vec![] };
        let d_mat = BasicMatrix::<BigInt>::try_from_fn(m, n, |_, _| zero.clone())
            .map_err(SmithError::Matrix)?;
        let u = bigint_identity(m);
        let v = bigint_identity(n);
        return Ok(SmithNormalForm {
            diagonal: diag,
            diagonal_matrix: d_mat,
            u,
            v,
        });
    }

    let mut d: Vec<Vec<BigInt>> = (0..m)
        .map(|i| (0..n).map(|j| matrix.get(i, j).unwrap()).collect())
        .collect();
    let mut u_rows: Vec<Vec<BigInt>> = (0..m)
        .map(|i| {
            (0..m)
                .map(|j| {
                    if i == j {
                        BigInt::from(1)
                    } else {
                        zero.clone()
                    }
                })
                .collect()
        })
        .collect();
    let mut v_cols: Vec<Vec<BigInt>> = (0..n)
        .map(|j| {
            (0..n)
                .map(|i| {
                    if i == j {
                        BigInt::from(1)
                    } else {
                        zero.clone()
                    }
                })
                .collect()
        })
        .collect();

    let r = m.min(n);

    for k in 0..r {
        let mut iterations = 0;
        loop {
            let mut pivot = None;
            let mut pivot_abs: Option<BigInt> = None;
            for i in k..m {
                for j in k..n {
                    if d[i][j] != zero {
                        let a = bigint_abs(&d[i][j]);
                        if pivot_abs.is_none() || a < *pivot_abs.as_ref().unwrap() {
                            pivot = Some((i, j));
                            pivot_abs = Some(a);
                        }
                    }
                }
            }

            let Some((pi, pj)) = pivot else { break };

            if iterations == iteration_limit {
                return Err(SmithError::IterationLimitExceeded {
                    pivot: k,
                    iterations,
                    limit: iteration_limit,
                });
            }
            iterations += 1;

            if pi != k {
                d.swap(pi, k);
                u_rows.swap(pi, k);
            }
            if pj != k {
                for row in &mut d {
                    row.swap(pj, k);
                }
                v_cols.swap(pj, k);
            }

            if d[k][k] < zero {
                for j in 0..n {
                    d[k][j] = -d[k][j].clone();
                }
                for j in 0..m {
                    u_rows[k][j] = -u_rows[k][j].clone();
                }
            }

            let mut changed = false;

            for i in (k + 1)..m {
                if d[i][k] != zero {
                    if &d[i][k] % &d[k][k] == zero {
                        let q = &d[i][k] / &d[k][k];
                        let row_k = d[k].clone();
                        for j in 0..n {
                            d[i][j] = d[i][j].clone() - &q * &row_k[j];
                        }

                        let u_k = u_rows[k].clone();
                        for j in 0..m {
                            u_rows[i][j] = u_rows[i][j].clone() - &q * &u_k[j];
                        }
                    } else {
                        let (g, x, y) = egcd(d[k][k].clone(), d[i][k].clone());
                        let q1 = &d[k][k] / &g;
                        let q2 = &d[i][k] / &g;

                        let row_k = d[k].clone();
                        let row_i = d[i].clone();
                        for j in 0..n {
                            d[k][j] = &x * &row_k[j] + &y * &row_i[j];
                            d[i][j] = -&q2 * &row_k[j] + &q1 * &row_i[j];
                        }

                        let u_k = u_rows[k].clone();
                        let u_i = u_rows[i].clone();
                        for j in 0..m {
                            u_rows[k][j] = &x * &u_k[j] + &y * &u_i[j];
                            u_rows[i][j] = -&q2 * &u_k[j] + &q1 * &u_i[j];
                        }
                    }
                    changed = true;
                }
            }

            for j in (k + 1)..n {
                if d[k][j] != zero {
                    if &d[k][j] % &d[k][k] == zero {
                        let q = &d[k][j] / &d[k][k];
                        for i in 0..m {
                            let val_k = d[i][k].clone();
                            d[i][j] = d[i][j].clone() - &q * &val_k;
                        }

                        let v_k = v_cols[k].clone();
                        for i in 0..n {
                            v_cols[j][i] = v_cols[j][i].clone() - &q * &v_k[i];
                        }
                    } else {
                        let (g, x, y) = egcd(d[k][k].clone(), d[k][j].clone());
                        let q1 = &d[k][k] / &g;
                        let q2 = &d[k][j] / &g;

                        for i in 0..m {
                            let val_k = d[i][k].clone();
                            let val_j = d[i][j].clone();
                            d[i][k] = &x * &val_k + &y * &val_j;
                            d[i][j] = -&q2 * &val_k + &q1 * &val_j;
                        }

                        for i in 0..n {
                            let val_k = v_cols[k][i].clone();
                            let val_j = v_cols[j][i].clone();
                            v_cols[k][i] = &x * &val_k + &y * &val_j;
                            v_cols[j][i] = -&q2 * &val_k + &q1 * &val_j;
                        }
                    }
                    changed = true;
                }
            }

            let mut divides_all = true;
            'outer: for i in (k + 1)..m {
                for j in (k + 1)..n {
                    if d[i][j] != zero && &d[i][j] % &d[k][k] != zero {
                        for col in 0..n {
                            let add_val = d[i][col].clone();
                            d[k][col] += add_val;
                        }
                        for col in 0..m {
                            let add_u = u_rows[i][col].clone();
                            u_rows[k][col] += add_u;
                        }
                        divides_all = false;
                        changed = true;
                        break 'outer;
                    }
                }
            }

            if !changed && divides_all {
                break;
            }
        }
    }

    let rank = (0..r).filter(|&k| d[k][k] != zero).count();

    let invariants: Vec<BigInt> = (0..rank)
        .map(|k| {
            let val = d[k][k].clone();
            if val < zero {
                -val
            } else {
                val
            }
        })
        .collect();

    let diagonal = if invariants.is_empty() {
        SmithDiagonal { invariants: vec![] }
    } else {
        SmithDiagonal::new_checked(invariants)?
    };

    let d_mat = BasicMatrix::<BigInt>::try_from_fn(m, n, |i, j| {
        if i == j && i < rank {
            d[i][i].clone()
        } else {
            zero.clone()
        }
    })
    .map_err(SmithError::Matrix)?;

    let u_mat = BasicMatrix::<BigInt>::try_from_fn(m, m, |i, j| u_rows[i][j].clone())
        .map_err(SmithError::Matrix)?;

    let v_mat = BasicMatrix::<BigInt>::try_from_fn(n, n, |i, j| v_cols[j][i].clone())
        .map_err(SmithError::Matrix)?;

    let ua = u_mat.mul(matrix).map_err(SmithError::Matrix)?;
    let uav = ua.mul(&v_mat).map_err(SmithError::Matrix)?;
    if uav.as_slice() != d_mat.as_slice() {
        return Err(SmithError::VerificationFailed);
    }

    Ok(SmithNormalForm {
        diagonal,
        diagonal_matrix: d_mat,
        u: u_mat,
        v: v_mat,
    })
}

fn integer_numerator_i64(val: &Rational64) -> Option<i64> {
    use num_traits::{One, Zero};
    if val.denom().is_zero() {
        return None;
    }
    let reduced = val.reduced();
    if !reduced.denom().is_one() {
        return None;
    }
    Some(*reduced.numer())
}

fn integer_numerator_big(val: &num_rational::BigRational) -> Option<BigInt> {
    use num_traits::{One, Zero};
    if val.denom().is_zero() {
        return None;
    }
    let reduced = val.reduced();
    if !reduced.denom().is_one() {
        return None;
    }
    Some(reduced.numer().clone())
}

pub fn from_rational64_integer_matrix(
    m: &BasicMatrix<Rational64>,
) -> Result<BasicMatrix<BigInt>, SmithError> {
    BasicMatrix::<BigInt>::try_from_fn_result(m.rows(), m.cols(), |row, col| {
        let val = m.get(row, col)?;
        integer_numerator_i64(&val)
            .map(BigInt::from)
            .ok_or(SmithError::NonIntegerEntry { row, col })
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

    pub fn to_dense(&self) -> BasicMatrix<BigInt> {
        let mut data = vec![BigInt::from(0); self.rows * self.cols];
        for (j, col) in self.columns.iter().enumerate() {
            for (row, val) in col {
                data[row * self.cols + j] = val.clone();
            }
        }
        BasicMatrix::from_row_major(self.rows, self.cols, data)
            .expect("dimensions already validated")
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
    let zero = BigInt::from(0);
    if b == zero {
        let one = BigInt::from(1);
        let neg_one = BigInt::from(-1);
        let sign = if a >= zero { one } else { neg_one };
        let abs_a = if a >= zero { a } else { -a };
        (abs_a, sign, zero)
    } else {
        let (g, x, y) = egcd(b.clone(), &a % &b);
        let y_clone = y.clone();
        (g, y, x - (a / b) * y_clone)
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


    fn verify_snf(matrix: &BasicMatrix<BigInt>, snf: &SmithNormalForm) {
        let ua = snf.u().mul(matrix).expect("U*A");
        let uav = ua.mul(snf.v()).expect("U*A*V");
        assert_eq!(
            uav.as_slice(),
            snf.diagonal_matrix().as_slice(),
            "U*A*V != D"
        );
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
        let recovered = sparse.to_dense();
        assert_eq!(dense.as_slice(), recovered.as_slice());
        assert_eq!(dense.rows(), recovered.rows());
        assert_eq!(dense.cols(), recovered.cols());
    }

    #[test]
    fn sparse_col_to_dense_zero_matrix() {
        let dense = BasicMatrix::<BigInt>::try_from_fn(3, 2, |_, _| BigInt::from(0)).unwrap();
        let sparse = SparseColMatrix::from_dense(&dense);
        let recovered = sparse.to_dense();
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
}
