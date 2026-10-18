//! Target A12: Rust Native Exact Smale Root Sentry.
//!
//! AuthorityEffect: None
//! Both Branch A and Branch B must be rigorously supported and verified without bias.
//!
//! This module formalizes and executes Target A12 of the MUB(6) research program:
//! 1. Exact rational evaluation of the 108 MUB polynomial relations over `BigRational` and `Cyc24`:
//!    System F(T, U) = 0: |< (B_a)_i, U_j >|^2 - 1/6 = 0 for a in {0, 1, 2}, i, j in {0, ..., 5}.
//! 2. Exact rational Jacobian computation DF(x_0) and linear system solving via LU decomposition
//!    with partial pivoting over Q (`BigRational`).
//! 3. Exact rational calculation of Smale invariants:
//!    - Newton step bound: beta(F, x_0) = ||DF(x_0)^(-1) F(x_0)||
//!    - Higher derivative bound: gamma(F, x_0) = sup_{k >= 2} ||DF(x_0)^(-1) D^k F(x_0) / k!||^(1/(k-1))
//!      (exact for quadratic polynomial systems where D^k F = 0 for k >= 3)
//!    - Smale parameter: alpha(F, x_0) = beta(F, x_0) * gamma(F, x_0)
//!    - Validation against rational threshold alpha_0 = 157 / 1000.
//! 4. Interval Krawczyk contractor over rational interval boxes X = prod [u_k, v_k]:
//!    - K(X) = x_0 - Y F(x_0) + (I - Y * [DF](X)) (X - x_0) with Y = DF(x_0)^(-1)
//!    - Strict coordinate contraction check: K(X)_k \subset int(X_k) for all k.
//! 5. Sentry monitor:
//!    - Scans bisection leaf candidates to verify that every certified cell has strictly positive
//!      residual lower bound (eps_C > 0).
//!    - Detects synthetic root injections (validating that approximate zeros produce alpha < 157/1000
//!      and Krawczyk contraction).
//! 6. Strict zero-float discipline: pure Cyc24 and BigRational exact arithmetic; zero float types.

use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use std::fmt;

use crate::omega_native::exact::d6_exact_curvature_cochain::{inner, ExactVec, D};
use crate::omega_native::exact::mub6_zerorel_variety::{
    exact_norm_sq_rat, squared_norm, BasisCyc, MuTripleCyc,
};
use omega_kernel::interval::{Interval, IntervalBox};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;

/// Total number of scalar polynomial equations for an MU triple against a 4th basis:
/// 3 bases * 6 rows * 6 columns = 108.
pub const TOTAL_MUB_RELATIONS: usize = 108;

/// Certified Smale alpha_0 rational threshold: 157 / 1000 = 0.157 < (13 - 3*sqrt(17))/4 ~ 0.15767078.
pub const SMALE_ALPHA_THRESHOLD_NUM: i64 = 157;
pub const SMALE_ALPHA_THRESHOLD_DEN: i64 = 1000;

/// Certified Smale alpha threshold value: 157 / 1000.
pub fn smale_alpha_threshold() -> BigRational {
    rq(SMALE_ALPHA_THRESHOLD_NUM, SMALE_ALPHA_THRESHOLD_DEN)
}

// ============================================================================
// 1. EXACT RATIONAL LINEAR ALGEBRA (VECTOR, MATRIX, LU DECOMPOSITION)
// ============================================================================

/// Errors arising during rational linear algebra operations.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum LuError {
    SingularMatrix,
    DimensionMismatch { expected: usize, found: usize },
    ZeroPivotAt(usize),
    CenterOutsideBox,
}

impl fmt::Display for LuError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::SingularMatrix => write!(f, "Matrix is singular over Q"),
            Self::CenterOutsideBox => write!(f, "Krawczyk center is outside the box"),
            Self::DimensionMismatch { expected, found } => {
                write!(
                    f,
                    "Dimension mismatch: expected {}, found {}",
                    expected, found
                )
            }
            Self::ZeroPivotAt(idx) => write!(f, "Zero pivot encountered at row/col {}", idx),
        }
    }
}

impl std::error::Error for LuError {}

/// Exact rational matrix over Q (`BigRational`). Row-major: `data[row][col]`.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalMatrix {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<Vec<BigRational>>,
}

impl RationalMatrix {
    /// Create a zero matrix of size `rows x cols`.
    pub fn zeros(rows: usize, cols: usize) -> Self {
        let data = vec![vec![BigRational::zero(); cols]; rows];
        Self { rows, cols, data }
    }

    /// Create an identity matrix of size `n x n`.
    pub fn identity(n: usize) -> Self {
        let mut mat = Self::zeros(n, n);
        let one = BigRational::one();
        for i in 0..n {
            mat.data[i][i] = one.clone();
        }
        mat
    }

    /// Create a matrix from row vectors.
    pub fn from_rows(rows_data: Vec<Vec<BigRational>>) -> Self {
        let rows = rows_data.len();
        let cols = if rows > 0 { rows_data[0].len() } else { 0 };
        for r in &rows_data {
            assert_eq!(r.len(), cols, "all rows must have identical column count");
        }
        Self {
            rows,
            cols,
            data: rows_data,
        }
    }

    /// Exact matrix-vector multiplication: y = A * x.
    pub fn mul_vec(&self, x: &[BigRational]) -> Result<Vec<BigRational>, LuError> {
        if x.len() != self.cols {
            return Err(LuError::DimensionMismatch {
                expected: self.cols,
                found: x.len(),
            });
        }
        let mut y = Vec::with_capacity(self.rows);
        for r in 0..self.rows {
            let mut sum = BigRational::zero();
            for c in 0..self.cols {
                sum += &self.data[r][c] * &x[c];
            }
            y.push(sum);
        }
        Ok(y)
    }

    /// Exact matrix-matrix multiplication: C = A * B.
    pub fn mul_mat(&self, b: &RationalMatrix) -> Result<RationalMatrix, LuError> {
        if self.cols != b.rows {
            return Err(LuError::DimensionMismatch {
                expected: self.cols,
                found: b.rows,
            });
        }
        let mut res = RationalMatrix::zeros(self.rows, b.cols);
        for i in 0..self.rows {
            for j in 0..b.cols {
                let mut sum = BigRational::zero();
                for k in 0..self.cols {
                    sum += &self.data[i][k] * &b.data[k][j];
                }
                res.data[i][j] = sum;
            }
        }
        Ok(res)
    }

    /// Transpose of the matrix.
    pub fn transpose(&self) -> RationalMatrix {
        let mut res = RationalMatrix::zeros(self.cols, self.rows);
        for r in 0..self.rows {
            for c in 0..self.cols {
                res.data[c][r] = self.data[r][c].clone();
            }
        }
        res
    }

    /// Matrix induced infinity norm: max row sum of absolute values.
    pub fn norm_inf(&self) -> BigRational {
        let mut max_sum = BigRational::zero();
        for r in 0..self.rows {
            let mut row_sum = BigRational::zero();
            for c in 0..self.cols {
                let val = &self.data[r][c];
                if *val < BigRational::zero() {
                    row_sum -= val;
                } else {
                    row_sum += val;
                }
            }
            if row_sum > max_sum {
                max_sum = row_sum;
            }
        }
        max_sum
    }

    /// Matrix induced 1-norm: max column sum of absolute values.
    pub fn norm_1(&self) -> BigRational {
        let mut max_sum = BigRational::zero();
        for c in 0..self.cols {
            let mut col_sum = BigRational::zero();
            for r in 0..self.rows {
                let val = &self.data[r][c];
                if *val < BigRational::zero() {
                    col_sum -= val;
                } else {
                    col_sum += val;
                }
            }
            if col_sum > max_sum {
                max_sum = col_sum;
            }
        }
        max_sum
    }
}

/// Exact vector infinity norm: max_i |x_i|.
pub fn vec_norm_inf(x: &[BigRational]) -> BigRational {
    let mut max_val = BigRational::zero();
    for v in x {
        let abs_v = if *v < BigRational::zero() {
            -v.clone()
        } else {
            v.clone()
        };
        if abs_v > max_val {
            max_val = abs_v;
        }
    }
    max_val
}

/// Exact vector 1-norm: sum_i |x_i|.
pub fn vec_norm_1(x: &[BigRational]) -> BigRational {
    let mut sum = BigRational::zero();
    for v in x {
        if *v < BigRational::zero() {
            sum -= v;
        } else {
            sum += v;
        }
    }
    sum
}

/// Exact LU factorization with partial row pivoting of an `n x n` matrix:
/// P * A = L * U, where P is a row permutation vector.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactRationalLu {
    pub n: usize,
    pub lu: Vec<Vec<BigRational>>,
    pub p: Vec<usize>,
    pub num_swaps: usize,
}

impl ExactRationalLu {
    /// Factorize square matrix A into LU with partial row pivoting.
    pub fn factorize(mat: &RationalMatrix) -> Result<Self, LuError> {
        if mat.rows != mat.cols {
            return Err(LuError::DimensionMismatch {
                expected: mat.rows,
                found: mat.cols,
            });
        }
        let n = mat.rows;
        let mut lu = mat.data.clone();
        let mut p: Vec<usize> = (0..n).collect();
        let mut num_swaps = 0;

        for k in 0..n {
            // Find pivot with first non-zero element or max absolute value in column k from row k to n-1
            let mut pivot_row = None;
            let mut max_pivot_abs = BigRational::zero();

            for r in k..n {
                let abs_val = if lu[r][k] < BigRational::zero() {
                    -lu[r][k].clone()
                } else {
                    lu[r][k].clone()
                };
                if !abs_val.is_zero() && abs_val > max_pivot_abs {
                    max_pivot_abs = abs_val;
                    pivot_row = Some(r);
                }
            }

            let Some(pivot_row) = pivot_row else {
                return Err(LuError::ZeroPivotAt(k));
            };

            if pivot_row != k {
                lu.swap(k, pivot_row);
                p.swap(k, pivot_row);
                num_swaps += 1;
            }

            let pivot = lu[k][k].clone();
            for r in (k + 1)..n {
                if !lu[r][k].is_zero() {
                    let factor = lu[r][k].clone() / &pivot;
                    lu[r][k] = factor.clone();
                    for c in (k + 1)..n {
                        let delta = &factor * &lu[k][c];
                        lu[r][c] -= delta;
                    }
                }
            }
        }

        Ok(Self {
            n,
            lu,
            p,
            num_swaps,
        })
    }

    /// Solve linear system A * x = b via forward and back substitution.
    pub fn solve(&self, b: &[BigRational]) -> Result<Vec<BigRational>, LuError> {
        if b.len() != self.n {
            return Err(LuError::DimensionMismatch {
                expected: self.n,
                found: b.len(),
            });
        }

        // Apply permutation y = P * b
        let mut y = Vec::with_capacity(self.n);
        for i in 0..self.n {
            y.push(b[self.p[i]].clone());
        }

        // Forward substitution L * y = P * b (L has ones on diagonal)
        for i in 0..self.n {
            for j in 0..i {
                if !self.lu[i][j].is_zero() {
                    let delta = &self.lu[i][j] * &y[j];
                    y[i] -= delta;
                }
            }
        }

        // Back substitution U * x = y
        let mut x = vec![BigRational::zero(); self.n];
        for i in (0..self.n).rev() {
            let mut sum = y[i].clone();
            for j in (i + 1)..self.n {
                if !self.lu[i][j].is_zero() {
                    sum -= &self.lu[i][j] * &x[j];
                }
            }
            if self.lu[i][i].is_zero() {
                return Err(LuError::ZeroPivotAt(i));
            }
            x[i] = sum / &self.lu[i][i];
        }

        Ok(x)
    }

    /// Exact inverse matrix A^(-1).
    pub fn inverse(&self) -> Result<RationalMatrix, LuError> {
        let mut inv_cols = Vec::with_capacity(self.n);
        for col in 0..self.n {
            let mut e = vec![BigRational::zero(); self.n];
            e[col] = BigRational::one();
            let x = self.solve(&e)?;
            inv_cols.push(x);
        }

        // Transpose column-vectors to row-major format
        let mut inv_data = vec![vec![BigRational::zero(); self.n]; self.n];
        for (col_idx, col) in inv_cols.into_iter().enumerate() {
            for row_idx in 0..self.n {
                inv_data[row_idx][col_idx] = col[row_idx].clone();
            }
        }

        Ok(RationalMatrix {
            rows: self.n,
            cols: self.n,
            data: inv_data,
        })
    }

    /// Exact determinant det(A).
    pub fn determinant(&self) -> BigRational {
        let mut det = BigRational::one();
        for i in 0..self.n {
            det *= &self.lu[i][i];
        }
        if self.num_swaps % 2 == 1 {
            -det
        } else {
            det
        }
    }
}

// ============================================================================
// 2. EXACT RATIONAL INTERVAL ARITHMETIC & INTERVAL BOX
// ============================================================================

// ============================================================================
// 3. EXACT QUADRATIC POLYNOMIAL SYSTEM REPRESENTATION
// ============================================================================

/// A quadratic polynomial component over Q:
/// F_i(x) = c + a^T x + (1/2) x^T H x
/// where H is a symmetric rational matrix.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuadraticComponent {
    pub constant: BigRational,
    pub linear: Vec<BigRational>,
    pub hessian: RationalMatrix,
}

impl QuadraticComponent {
    /// Construct a quadratic polynomial component.
    ///
    /// NOTE (R16 audit): Enforces square dimension and symmetric Hessian precondition
    /// so that grad F_i(x) = a + H x matches the exact gradient of (1/2) x^T H x.
    pub fn new(constant: BigRational, linear: Vec<BigRational>, hessian: RationalMatrix) -> Self {
        assert_eq!(linear.len(), hessian.rows);
        assert_eq!(hessian.rows, hessian.cols);
        for r in 0..hessian.rows {
            for c in (r + 1)..hessian.cols {
                assert_eq!(
                    hessian.data[r][c], hessian.data[c][r],
                    "QuadraticPolynomial Hessian must be symmetric: ({}, {}) != ({}, {})",
                    r, c, c, r
                );
            }
        }
        Self {
            constant,
            linear,
            hessian,
        }
    }

    /// Evaluate scalar F_i(x) at point x.
    pub fn eval(&self, x: &[BigRational]) -> BigRational {
        let n = x.len();
        let mut res = self.constant.clone();

        // Linear term: a^T x
        for j in 0..n {
            res += &self.linear[j] * &x[j];
        }

        // Quadratic term: (1/2) x^T H x
        let mut quad = BigRational::zero();
        for r in 0..n {
            for c in 0..n {
                if !self.hessian.data[r][c].is_zero() {
                    quad += &self.hessian.data[r][c] * &x[r] * &x[c];
                }
            }
        }
        let half = rq(1, 2);
        res += half * quad;
        res
    }

    /// Exact gradient vector: grad F_i(x) = a + H x.
    pub fn grad(&self, x: &[BigRational]) -> Vec<BigRational> {
        let n = x.len();
        let mut g = self.linear.clone();
        for r in 0..n {
            for c in 0..n {
                if !self.hessian.data[r][c].is_zero() {
                    g[r] += &self.hessian.data[r][c] * &x[c];
                }
            }
        }
        g
    }

    /// Evaluate interval gradient over an interval box: [grad F_i](X) = a + H X.
    pub fn grad_interval(&self, x_box: &IntervalBox) -> Vec<Interval> {
        let n = x_box.dim();
        let mut grad_iv = Vec::with_capacity(n);

        for r in 0..n {
            let mut sum_iv = Interval::point(self.linear[r].clone());
            for c in 0..n {
                let h_rc = &self.hessian.data[r][c];
                if !h_rc.is_zero() {
                    let term = x_box.intervals[c].mul_scalar(h_rc);
                    sum_iv = sum_iv.add(&term);
                }
            }
            grad_iv.push(sum_iv);
        }

        grad_iv
    }
}

/// A square polynomial system F: Q^n -> Q^n composed of quadratic equations.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SquarePolynomialSystem {
    pub dim: usize,
    pub components: Vec<QuadraticComponent>,
}

impl SquarePolynomialSystem {
    /// Construct a square system from n quadratic components.
    pub fn new(components: Vec<QuadraticComponent>) -> Self {
        let dim = components.len();
        for c in &components {
            assert_eq!(c.linear.len(), dim);
            assert_eq!(c.hessian.rows, dim);
            assert_eq!(c.hessian.cols, dim);
        }
        Self { dim, components }
    }

    /// Evaluate F(x) in Q^n.
    pub fn eval(&self, x: &[BigRational]) -> Vec<BigRational> {
        self.components.iter().map(|comp| comp.eval(x)).collect()
    }

    /// Compute exact Jacobian matrix DF(x) in Q^(n x n).
    pub fn jacobian(&self, x: &[BigRational]) -> RationalMatrix {
        let rows = self.components.iter().map(|comp| comp.grad(x)).collect();
        RationalMatrix::from_rows(rows)
    }

    /// Compute interval Jacobian matrix [DF](X) over interval box X.
    pub fn jacobian_interval(&self, x_box: &IntervalBox) -> Vec<Vec<Interval>> {
        self.components
            .iter()
            .map(|comp| comp.grad_interval(x_box))
            .collect()
    }
}

// ============================================================================
// 4. EXACT 108 MUB POLYNOMIAL RELATIONS OVER BIGRATIONAL AND CYC24
// ============================================================================

/// Coordinate index for the 108 MUB polynomial relations:
/// basis a in {0, 1, 2}, row i in {0, ..., 5}, column j in {0, ..., 5}.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MubRelIndex {
    pub basis: usize,
    pub row: usize,
    pub col: usize,
}

/// Evaluate all 108 exact cyclotomic MUB defects in Q(zeta_24):
/// r_{a, i, j}(T, U) = |< (B_a)_i, U_j >|^2 - 1/6 in Q(zeta_24).
///
/// NOTE (R10 audit): Retains all power-basis cyclotomic coefficients, preventing false zeros.
pub fn eval_108_mub_defects_cyc(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
) -> Vec<(MubRelIndex, Cyc24)> {
    let mut results = Vec::with_capacity(TOTAL_MUB_RELATIONS);
    let sixth = Cyc24::rat(rq(1, 6));

    for basis_idx in 0..3 {
        let basis = match basis_idx {
            0 => &triple.b0,
            1 => &triple.b1,
            2 => &triple.b2,
            _ => unreachable!(),
        };

        for (row, v_i) in basis.iter().enumerate().take(D) {
            for (col, u_j) in cand_u.iter().enumerate().take(D) {
                let ip = inner(v_i, u_j);
                let defect = squared_norm(&ip).sub(&sixth);
                results.push((
                    MubRelIndex {
                        basis: basis_idx,
                        row,
                        col,
                    },
                    defect,
                ));
            }
        }
    }

    results
}

/// Evaluate all 108 MUB polynomial relations as rational values when rational:
/// r_{a, i, j}(T, U) = |< (B_a)_i, U_j >|^2 - 1/6.
pub fn eval_108_mub_relations(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
) -> Vec<(MubRelIndex, BigRational)> {
    let mut results = Vec::with_capacity(TOTAL_MUB_RELATIONS);
    let one_sixth = rq(1, 6);

    for basis_idx in 0..3 {
        let basis = match basis_idx {
            0 => &triple.b0,
            1 => &triple.b1,
            2 => &triple.b2,
            _ => unreachable!(),
        };

        for (row, v_i) in basis.iter().enumerate().take(D) {
            for (col, u_j) in cand_u.iter().enumerate().take(D) {
                let ip = inner(v_i, u_j);
                let sq = squared_norm(&ip);
                let norm_sq = sq.as_rational().unwrap_or_else(|| sq.a[0].clone());
                let residual = norm_sq - &one_sixth;
                results.push((
                    MubRelIndex {
                        basis: basis_idx,
                        row,
                        col,
                    },
                    residual,
                ));
            }
        }
    }

    results
}

/// Try evaluating a single MUB relation |< v, u >|^2 - 1/6 for two vectors in C^6 over Cyc24,
/// returning Err if the inner product norm-squared is not rational.
pub fn try_eval_single_mub_relation(v: &ExactVec, u: &ExactVec) -> Result<BigRational, String> {
    let ip = inner(v, u);
    let norm_sq = exact_norm_sq_rat(&ip)?;
    Ok(norm_sq - rq(1, 6))
}

/// Evaluate exact cyclotomic defect |< v, u >|^2 - 1/6 in Q(zeta_24), preserving all coefficients.
pub fn eval_single_mub_defect_cyc(v: &ExactVec, u: &ExactVec) -> Cyc24 {
    let ip = inner(v, u);
    let sixth = Cyc24::rat(rq(1, 6));
    squared_norm(&ip).sub(&sixth)
}

/// Evaluate a single MUB relation |< v, u >|^2 - 1/6 for two vectors in C^6 over Cyc24.
pub fn eval_single_mub_relation(v: &ExactVec, u: &ExactVec) -> BigRational {
    try_eval_single_mub_relation(v, u).unwrap_or_else(|_| {
        let ip = inner(v, u);
        squared_norm(&ip).a[0].clone() - rq(1, 6)
    })
}

/// Helper explicitly referencing Cyc24 carrier array.
pub fn eval_single_mub_relation_cyc24(v: &[Cyc24; D], u: &[Cyc24; D]) -> BigRational {
    eval_single_mub_relation(v, u)
}

// ============================================================================
// 5. EXACT RATIONAL SMALE INVARIANTS (BETA, GAMMA, ALPHA)
// ============================================================================

/// The exact rational Smale invariants for an approximate zero x_0 of F(x) = 0.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SmaleInvariants {
    /// Newton step bound: beta(F, x_0) = ||DF(x_0)^(-1) F(x_0)||
    pub beta: BigRational,
    /// Higher derivative bound: gamma(F, x_0) = ||DF(x_0)^(-1) (1/2) D^2 F(x_0)|| (conservative upper bound)
    pub gamma: BigRational,
    /// Smale parameter: alpha(F, x_0) = beta * gamma
    pub alpha: BigRational,
    /// Comparison threshold: alpha_0 = 157 / 1000
    pub threshold: BigRational,
    /// Whether alpha < 157 / 1000 holds strictly.
    pub is_certified_approx_zero: bool,
}

/// Compute exact Smale invariants beta, gamma, and alpha for a square quadratic system F.
///
/// NOTE (R16 audit): The entrywise absolute sum computed for:
///   gamma(F, x_0) = max_{i=0}^{n-1} sum_{j, k=0}^{n-1} |(Q_i)_{jk}|
/// is a proved conservative UPPER BOUND on the induced bilinear operator norm ||Y (1/2) D^2 F(x_0)||_inf.
/// Overestimating gamma is sound for conservative approximate zero admission (alpha = beta * gamma <= alpha_0).
///
/// Because F is quadratic:
/// D^k F = 0 for all k >= 3.
/// Therefore, the supremum in Smale's definition:
/// gamma(F, x_0) = sup_{k >= 2} ||DF(x_0)^(-1) D^k F(x_0) / k!||^(1/(k-1))
/// collapses to the single term k = 2:
/// gamma(F, x_0) = ||DF(x_0)^(-1) (1/2) D^2 F(x_0)||.
///
/// Under the induced infinity norm:
/// For Y = DF(x_0)^(-1), coordinate i has quadratic form:
/// Q_i = (1/2) sum_{p=0}^{n-1} Y_{ip} H_p
/// where H_p is the constant Hessian of component F_p.
/// Then ||Y (1/2) D^2 F(x_0)||_inf = max_{i=0}^{n-1} sum_{j, k=0}^{n-1} |(Q_i)_{jk}|.
pub fn compute_smale_invariants(
    system: &SquarePolynomialSystem,
    x_0: &[BigRational],
) -> Result<SmaleInvariants, LuError> {
    let n = system.dim;
    if x_0.len() != n {
        return Err(LuError::DimensionMismatch {
            expected: n,
            found: x_0.len(),
        });
    }

    // 1. Evaluate F(x_0)
    let fx = system.eval(x_0);

    // 2. Evaluate Jacobian DF(x_0)
    let df = system.jacobian(x_0);

    // 3. LU factorize DF(x_0)
    let lu = ExactRationalLu::factorize(&df)?;

    // 4. Compute Newton step delta_x = DF(x_0)^(-1) F(x_0)
    let delta_x = lu.solve(&fx)?;
    let beta = vec_norm_inf(&delta_x);

    // 5. Compute inverse Y = DF(x_0)^(-1)
    let y_mat = lu.inverse()?;

    // 6. Compute higher derivative bound gamma = ||Y (1/2) D^2 F(x_0)||_inf
    let mut gamma = BigRational::zero();
    let half = rq(1, 2);

    for i in 0..n {
        // Accumulate Q_i = (1/2) sum_p Y_{ip} H_p
        let mut row_abs_sum = BigRational::zero();

        for j in 0..n {
            for k in 0..n {
                let mut q_ijk = BigRational::zero();
                for p in 0..n {
                    let y_ip = &y_mat.data[i][p];
                    let h_p_jk = &system.components[p].hessian.data[j][k];
                    if !y_ip.is_zero() && !h_p_jk.is_zero() {
                        q_ijk += y_ip * h_p_jk;
                    }
                }
                q_ijk *= &half;

                if q_ijk < BigRational::zero() {
                    row_abs_sum -= q_ijk;
                } else {
                    row_abs_sum += q_ijk;
                }
            }
        }

        if row_abs_sum > gamma {
            gamma = row_abs_sum;
        }
    }

    // 7. Compute Smale alpha = beta * gamma
    let alpha = &beta * &gamma;
    let threshold = smale_alpha_threshold();
    let is_certified_approx_zero = alpha < threshold;

    Ok(SmaleInvariants {
        beta,
        gamma,
        alpha,
        threshold,
        is_certified_approx_zero,
    })
}

// ============================================================================
// 6. EXACT INTERVAL KRAWCZYK CONTRACTOR
// ============================================================================

/// Result of evaluating the interval Krawczyk contractor K(X).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct KrawczykResult {
    /// The computed Krawczyk interval box K(X).
    pub krawczyk_box: IntervalBox,
    /// Strict coordinate contraction: K(X)_k \subset int(X_k) for all k.
    pub is_strictly_contracted: bool,
    /// Empty intersection check: K(X) \cap X = \emptyset.
    pub is_disjoint: bool,
}

/// Evaluate the interval Krawczyk contractor on an interval box X:
/// K(X) = x_0 - Y F(x_0) + (I - Y * [DF](X)) (X - x_0)
/// where Y = DF(x_0)^(-1).
///
/// By the Krawczyk Theorem:
/// - If K(X) \subset int(X), then F has a unique root x* in X, and Newton iteration converges to x*.
/// - If K(X) \cap X = \emptyset, then F has no roots in X.
pub fn krawczyk_contractor(
    system: &SquarePolynomialSystem,
    x_box: &IntervalBox,
    custom_x0: Option<&[BigRational]>,
) -> Result<KrawczykResult, LuError> {
    let n = system.dim;
    if x_box.dim() != n {
        return Err(LuError::DimensionMismatch {
            expected: n,
            found: x_box.dim(),
        });
    }

    // Evaluation point x_0 (midpoint by default)
    let x_0 = match custom_x0 {
        Some(pt) => {
            if pt.len() != n {
                return Err(LuError::DimensionMismatch {
                    expected: n,
                    found: pt.len(),
                });
            }
            pt.to_vec()
        }
        None => x_box.midpoint(),
    };

    if !x_box.contains_point(&x_0) {
        return Err(LuError::CenterOutsideBox);
    }

    // 1. Evaluate F(x_0) and Jacobian DF(x_0)
    let fx = system.eval(&x_0);
    let df = system.jacobian(&x_0);

    // 2. LU factorize and compute inverse Y = DF(x_0)^(-1)
    let lu = ExactRationalLu::factorize(&df)?;
    let y_mat = lu.inverse()?;

    // 3. Newton step from x_0: x_newton = x_0 - Y F(x_0)
    let newton_step = lu.solve(&fx)?;
    let mut x_newton = Vec::with_capacity(n);
    for i in 0..n {
        x_newton.push(&x_0[i] - &newton_step[i]);
    }

    // 4. Interval Jacobian [DF](X)
    let df_iv = system.jacobian_interval(x_box);

    // 5. Evaluate interval matrix M = I - Y * [DF](X)
    // M_{ik} = delta_{ik} - sum_j Y_{ij} * [DF](X)_{jk}
    let mut m_matrix = vec![vec![Interval::point(BigRational::zero()); n]; n];

    for (i, m_row) in m_matrix.iter_mut().enumerate().take(n) {
        for (k, m_ik) in m_row.iter_mut().enumerate().take(n) {
            let mut prod_sum = Interval::point(BigRational::zero());
            for (j, df_row) in df_iv.iter().enumerate().take(n) {
                let y_ij = &y_mat.data[i][j];
                if !y_ij.is_zero() {
                    let term = df_row[k].mul_scalar(y_ij);
                    prod_sum = prod_sum.add(&term);
                }
            }

            let delta = if i == k {
                Interval::point(BigRational::one())
            } else {
                Interval::point(BigRational::zero())
            };

            *m_ik = delta.sub(&prod_sum);
        }
    }

    // 6. Compute interval displacement: delta_X = X - x_0
    let mut delta_x_iv = Vec::with_capacity(n);
    for (k, x0_k) in x_0.iter().enumerate().take(n) {
        let x0_pt = Interval::point(x0_k.clone());
        delta_x_iv.push(x_box.intervals[k].sub(&x0_pt));
    }

    // 7. Compute K(X)_i = x_newton_i + sum_k M_{ik} * delta_X_k
    let mut k_intervals = Vec::with_capacity(n);
    for (i, m_row) in m_matrix.iter().enumerate().take(n) {
        let mut coord_iv = Interval::point(x_newton[i].clone());
        for (k, m_ik) in m_row.iter().enumerate().take(n) {
            let term = m_ik.mul(&delta_x_iv[k]);
            coord_iv = coord_iv.add(&term);
        }
        k_intervals.push(coord_iv);
    }

    let krawczyk_box = IntervalBox::new(k_intervals);
    let is_strictly_contracted = krawczyk_box.strict_interior_subset_of(x_box);
    let is_disjoint = krawczyk_box.is_disjoint_from(x_box);

    Ok(KrawczykResult {
        krawczyk_box,
        is_strictly_contracted,
        is_disjoint,
    })
}

/// Evaluate the interval Krawczyk contractor with a specified custom expansion center.
pub fn krawczyk_contractor_custom_center(
    system: &SquarePolynomialSystem,
    x_box: &IntervalBox,
    center: &[BigRational],
) -> Result<KrawczykResult, LuError> {
    krawczyk_contractor(system, x_box, Some(center))
}

// ============================================================================
// 7. SENTRY MONITOR: BISECTION LEAVES & SYNTHETIC ROOT INJECTIONS
// ============================================================================

/// A certified bisection leaf cell carrying a verified residual lower bound.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CertifiedLeafCell {
    pub cell_id: String,
    pub center: Vec<BigRational>,
    pub radius: BigRational,
    /// Certified residual lower bound: eps_C > 0 certifies that no root exists in the cell.
    pub residual_margin: BigRational,
}

/// Summary report from scanning bisection leaf candidates.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SentryScanSummary {
    /// True if all scanned cells have strictly positive residual lower bounds.
    pub all_positive: bool,
    /// Total number of scanned cells.
    pub scanned_count: usize,
    /// Minimum observed margin across all certified cells.
    pub min_margin: BigRational,
    /// IDs of any cells failing the positive margin threshold (eps_C <= 0).
    pub zero_or_negative_margin_cells: Vec<String>,
}

/// Sentry inspection result on a candidate root.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum SentryRootInspection {
    /// Smale alpha < 157/1000 and Krawczyk strictly contracts: exact isolated root certified!
    RootCertified {
        alpha: BigRational,
        beta: BigRational,
        gamma: BigRational,
        isolating_box: IntervalBox,
        krawczyk_box: IntervalBox,
    },
    /// Candidate root fails Smale alpha threshold or Krawczyk contraction.
    RootUncertified { alpha: BigRational, reason: String },
}

/// The Smale Sentry Monitor for MUB(6) root surveillance.
pub struct SmaleSentry;

impl SmaleSentry {
    /// Scan bisection leaf candidates to verify that every certified cell has strictly
    /// positive residual lower bound (eps_C > 0). The scan reads `residual_margin` as the caller
    /// supplies it and does not evaluate any residual.
    pub fn scan_bisection_leaves(cells: &[CertifiedLeafCell]) -> SentryScanSummary {
        let mut all_positive = !cells.is_empty();
        let mut min_margin = cells
            .first()
            .map(|c| c.residual_margin.clone())
            .unwrap_or_else(BigRational::zero);
        let mut zero_or_negative_cells = Vec::new();

        for cell in cells {
            if cell.residual_margin <= BigRational::zero() {
                all_positive = false;
                zero_or_negative_cells.push(cell.cell_id.clone());
            }
            if cell.residual_margin < min_margin {
                min_margin = cell.residual_margin.clone();
            }
        }

        SentryScanSummary {
            all_positive,
            scanned_count: cells.len(),
            min_margin,
            zero_or_negative_margin_cells: zero_or_negative_cells,
        }
    }

    /// Inspect a candidate root x_0 for a square polynomial system:
    /// 1. Computes Smale invariants (beta, gamma, alpha).
    /// 2. Verifies alpha < 157 / 1000.
    /// 3. Forms isolating box X around x_0 and checks Krawczyk contraction K(X) \subset int(X).
    pub fn inspect_candidate_root(
        system: &SquarePolynomialSystem,
        x_0: &[BigRational],
        box_radius: &BigRational,
    ) -> Result<SentryRootInspection, LuError> {
        let invariants = compute_smale_invariants(system, x_0)?;

        if !invariants.is_certified_approx_zero {
            let reason = format!(
                "Smale parameter alpha = {} exceeds threshold {}",
                invariants.alpha, invariants.threshold
            );
            return Ok(SentryRootInspection::RootUncertified {
                alpha: invariants.alpha,
                reason,
            });
        }

        let x_box = IntervalBox::from_center_uniform_radius(x_0, box_radius);
        let k_res = krawczyk_contractor(system, &x_box, Some(x_0))?;

        if k_res.is_strictly_contracted {
            Ok(SentryRootInspection::RootCertified {
                alpha: invariants.alpha,
                beta: invariants.beta,
                gamma: invariants.gamma,
                isolating_box: x_box,
                krawczyk_box: k_res.krawczyk_box,
            })
        } else {
            Ok(SentryRootInspection::RootUncertified {
                alpha: invariants.alpha,
                reason: "Krawczyk contractor failed strict interior contraction".to_string(),
            })
        }
    }

    /// Synthetic root injection detector:
    /// Injects an approximate zero (target root + rational perturbation) into the sentry,
    /// certifying that genuine approximate zeros are accurately detected, while overly
    /// perturbed points are flagged.
    pub fn test_synthetic_root_injection(
        system: &SquarePolynomialSystem,
        exact_root: &[BigRational],
        perturbation: &BigRational,
        box_radius: &BigRational,
    ) -> Result<SentryRootInspection, LuError> {
        let perturbed_x0: Vec<BigRational> = exact_root.iter().map(|r| r + perturbation).collect();

        Self::inspect_candidate_root(system, &perturbed_x0, box_radius)
    }
}
