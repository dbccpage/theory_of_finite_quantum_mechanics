
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use std::fmt;

use crate::native::exact::d6_exact_curvature_cochain::{inner, ExactVec, D};
use crate::native::exact::mub6_zerorel_variety::{
    exact_norm_sq_rat, squared_norm, BasisCyc, MuTripleCyc,
};
use engine_kernel::interval::{Interval, IntervalBox};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::rq;

pub const TOTAL_MUB_RELATIONS: usize = 108;

pub const SMALE_ALPHA_THRESHOLD_NUM: i64 = 157;
pub const SMALE_ALPHA_THRESHOLD_DEN: i64 = 1000;

pub fn smale_alpha_threshold() -> BigRational {
    rq(SMALE_ALPHA_THRESHOLD_NUM, SMALE_ALPHA_THRESHOLD_DEN)
}


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

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalMatrix {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<Vec<BigRational>>,
}

impl RationalMatrix {
    pub fn zeros(rows: usize, cols: usize) -> Self {
        let data = vec![vec![BigRational::zero(); cols]; rows];
        Self { rows, cols, data }
    }

    pub fn identity(n: usize) -> Self {
        let mut mat = Self::zeros(n, n);
        let one = BigRational::one();
        for i in 0..n {
            mat.data[i][i] = one.clone();
        }
        mat
    }

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

    pub fn transpose(&self) -> RationalMatrix {
        let mut res = RationalMatrix::zeros(self.cols, self.rows);
        for r in 0..self.rows {
            for c in 0..self.cols {
                res.data[c][r] = self.data[r][c].clone();
            }
        }
        res
    }

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

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactRationalLu {
    pub n: usize,
    pub lu: Vec<Vec<BigRational>>,
    pub p: Vec<usize>,
    pub num_swaps: usize,
}

impl ExactRationalLu {
    fn find_max_lu_pivot_row(lu: &[Vec<BigRational>], k: usize, n: usize) -> Option<usize> {
        let mut pivot_row = None;
        let mut max_pivot_abs = BigRational::zero();
        for (r, row) in lu.iter().enumerate().take(n).skip(k) {
            let abs_val = row[k].abs();
            if !abs_val.is_zero() && abs_val > max_pivot_abs {
                max_pivot_abs = abs_val;
                pivot_row = Some(r);
            }
        }
        pivot_row
    }

    fn eliminate_lu_row(row_r: &mut [BigRational], row_k: &[BigRational], k: usize, n: usize) {
        if row_r[k].is_zero() {
            return;
        }
        let factor = row_r[k].clone() / &row_k[k];
        row_r[k] = factor.clone();
        for c in (k + 1)..n {
            let delta = &factor * &row_k[c];
            row_r[c] -= delta;
        }
    }

    fn eliminate_lu_column(lu: &mut [Vec<BigRational>], k: usize, n: usize) {
        let row_k = lu[k].clone();
        for row_r in lu.iter_mut().take(n).skip(k + 1) {
            Self::eliminate_lu_row(row_r, &row_k, k, n);
        }
    }

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
            let Some(pivot_row) = Self::find_max_lu_pivot_row(&lu, k, n) else {
                return Err(LuError::ZeroPivotAt(k));
            };
            if pivot_row != k {
                lu.swap(k, pivot_row);
                p.swap(k, pivot_row);
                num_swaps += 1;
            }
            Self::eliminate_lu_column(&mut lu, k, n);
        }

        Ok(Self {
            n,
            lu,
            p,
            num_swaps,
        })
    }

    fn forward_substitute(&self, b: &[BigRational]) -> Vec<BigRational> {
        let mut y: Vec<BigRational> = (0..self.n).map(|i| b[self.p[i]].clone()).collect();
        for i in 0..self.n {
            for j in 0..i {
                if !self.lu[i][j].is_zero() {
                    let delta = &self.lu[i][j] * &y[j];
                    y[i] -= delta;
                }
            }
        }
        y
    }

    fn back_substitute_row(&self, i: usize, y_i: &BigRational, x: &[BigRational]) -> BigRational {
        let mut sum = y_i.clone();
        for j in (i + 1)..self.n {
            if !self.lu[i][j].is_zero() {
                sum -= &self.lu[i][j] * &x[j];
            }
        }
        sum
    }

    pub fn solve(&self, b: &[BigRational]) -> Result<Vec<BigRational>, LuError> {
        if b.len() != self.n {
            return Err(LuError::DimensionMismatch {
                expected: self.n,
                found: b.len(),
            });
        }

        let y = self.forward_substitute(b);
        let mut x = vec![BigRational::zero(); self.n];
        for i in (0..self.n).rev() {
            if self.lu[i][i].is_zero() {
                return Err(LuError::ZeroPivotAt(i));
            }
            let sum = self.back_substitute_row(i, &y[i], &x);
            x[i] = sum / &self.lu[i][i];
        }

        Ok(x)
    }

    pub fn inverse(&self) -> Result<RationalMatrix, LuError> {
        let mut inv_cols = Vec::with_capacity(self.n);
        for col in 0..self.n {
            let mut e = vec![BigRational::zero(); self.n];
            e[col] = BigRational::one();
            let x = self.solve(&e)?;
            inv_cols.push(x);
        }

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



#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuadraticComponent {
    pub constant: BigRational,
    pub linear: Vec<BigRational>,
    pub hessian: RationalMatrix,
}

impl QuadraticComponent {
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

    pub fn eval(&self, x: &[BigRational]) -> BigRational {
        let n = x.len();
        let mut res = self.constant.clone();

        for j in 0..n {
            res += &self.linear[j] * &x[j];
        }

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

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SquarePolynomialSystem {
    pub dim: usize,
    pub components: Vec<QuadraticComponent>,
}

impl SquarePolynomialSystem {
    pub fn new(components: Vec<QuadraticComponent>) -> Self {
        let dim = components.len();
        for c in &components {
            assert_eq!(c.linear.len(), dim);
            assert_eq!(c.hessian.rows, dim);
            assert_eq!(c.hessian.cols, dim);
        }
        Self { dim, components }
    }

    pub fn eval(&self, x: &[BigRational]) -> Vec<BigRational> {
        self.components.iter().map(|comp| comp.eval(x)).collect()
    }

    pub fn jacobian(&self, x: &[BigRational]) -> RationalMatrix {
        let rows = self.components.iter().map(|comp| comp.grad(x)).collect();
        RationalMatrix::from_rows(rows)
    }

    pub fn jacobian_interval(&self, x_box: &IntervalBox) -> Vec<Vec<Interval>> {
        self.components
            .iter()
            .map(|comp| comp.grad_interval(x_box))
            .collect()
    }
}


#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MubRelIndex {
    pub basis: usize,
    pub row: usize,
    pub col: usize,
}

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

fn append_basis_mub_relations(
    basis_idx: usize,
    basis: &BasisCyc,
    cand_u: &BasisCyc,
    one_sixth: &BigRational,
    results: &mut Vec<(MubRelIndex, BigRational)>,
) {
    for (row, v_i) in basis.iter().enumerate().take(D) {
        for (col, u_j) in cand_u.iter().enumerate().take(D) {
            let ip = inner(v_i, u_j);
            let sq = squared_norm(&ip);
            let norm_sq = sq.as_rational().unwrap_or_else(|| sq.a[0].clone());
            let residual = norm_sq - one_sixth;
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

pub fn eval_108_mub_relations(
    triple: &MuTripleCyc,
    cand_u: &BasisCyc,
) -> Vec<(MubRelIndex, BigRational)> {
    let mut results = Vec::with_capacity(TOTAL_MUB_RELATIONS);
    let one_sixth = rq(1, 6);
    let bases = [&triple.b0, &triple.b1, &triple.b2];
    for (basis_idx, basis) in bases.iter().enumerate() {
        append_basis_mub_relations(basis_idx, basis, cand_u, &one_sixth, &mut results);
    }
    results
}

pub fn try_eval_single_mub_relation(v: &ExactVec, u: &ExactVec) -> Result<BigRational, String> {
    let ip = inner(v, u);
    let norm_sq = exact_norm_sq_rat(&ip)?;
    Ok(norm_sq - rq(1, 6))
}

pub fn eval_single_mub_defect_cyc(v: &ExactVec, u: &ExactVec) -> Cyc24 {
    let ip = inner(v, u);
    let sixth = Cyc24::rat(rq(1, 6));
    squared_norm(&ip).sub(&sixth)
}

pub fn eval_single_mub_relation(v: &ExactVec, u: &ExactVec) -> BigRational {
    try_eval_single_mub_relation(v, u).unwrap_or_else(|_| {
        let ip = inner(v, u);
        squared_norm(&ip).a[0].clone() - rq(1, 6)
    })
}

pub fn eval_single_mub_relation_cyc24(v: &[Cyc24; D], u: &[Cyc24; D]) -> BigRational {
    eval_single_mub_relation(v, u)
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SmaleInvariants {
    pub beta: BigRational,
    pub gamma: BigRational,
    pub alpha: BigRational,
    pub threshold: BigRational,
    pub is_certified_approx_zero: bool,
}

fn compute_smale_q_entry(
    system: &SquarePolynomialSystem,
    y_row: &[BigRational],
    j: usize,
    k: usize,
    half: &BigRational,
) -> BigRational {
    let mut q_ijk = BigRational::zero();
    for (p, y_ip) in y_row.iter().enumerate() {
        let h_p_jk = &system.components[p].hessian.data[j][k];
        if !y_ip.is_zero() && !h_p_jk.is_zero() {
            q_ijk += y_ip * h_p_jk;
        }
    }
    (q_ijk * half).abs()
}

fn compute_smale_gamma_row(
    system: &SquarePolynomialSystem,
    y_row: &[BigRational],
    n: usize,
    half: &BigRational,
) -> BigRational {
    let mut row_abs_sum = BigRational::zero();
    for j in 0..n {
        for k in 0..n {
            row_abs_sum += compute_smale_q_entry(system, y_row, j, k, half);
        }
    }
    row_abs_sum
}

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

    let fx = system.eval(x_0);
    let df = system.jacobian(x_0);
    let lu = ExactRationalLu::factorize(&df)?;

    let delta_x = lu.solve(&fx)?;
    let beta = vec_norm_inf(&delta_x);
    let y_mat = lu.inverse()?;

    let mut gamma = BigRational::zero();
    let half = rq(1, 2);
    for i in 0..n {
        let row_abs_sum = compute_smale_gamma_row(system, &y_mat.data[i], n, &half);
        if row_abs_sum > gamma {
            gamma = row_abs_sum;
        }
    }

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

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct KrawczykResult {
    pub krawczyk_box: IntervalBox,
    pub is_strictly_contracted: bool,
    pub is_disjoint: bool,
}

fn resolve_krawczyk_center(
    x_box: &IntervalBox,
    custom_x0: Option<&[BigRational]>,
    n: usize,
) -> Result<Vec<BigRational>, LuError> {
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
    Ok(x_0)
}

fn compute_krawczyk_m_entry(
    y_row: &[BigRational],
    df_iv: &[Vec<Interval>],
    i: usize,
    k: usize,
    n: usize,
) -> Interval {
    let mut prod_sum = Interval::point(BigRational::zero());
    for (j, df_row) in df_iv.iter().enumerate().take(n) {
        let y_ij = &y_row[j];
        if !y_ij.is_zero() {
            prod_sum = prod_sum.add(&df_row[k].mul_scalar(y_ij));
        }
    }
    let delta = if i == k {
        Interval::point(BigRational::one())
    } else {
        Interval::point(BigRational::zero())
    };
    delta.sub(&prod_sum)
}

fn build_krawczyk_m_matrix(
    y_mat: &RationalMatrix,
    df_iv: &[Vec<Interval>],
    n: usize,
) -> Vec<Vec<Interval>> {
    let mut m_matrix = vec![vec![Interval::point(BigRational::zero()); n]; n];
    for (i, m_row) in m_matrix.iter_mut().enumerate().take(n) {
        for (k, m_ik) in m_row.iter_mut().enumerate().take(n) {
            *m_ik = compute_krawczyk_m_entry(&y_mat.data[i], df_iv, i, k, n);
        }
    }
    m_matrix
}

fn assemble_krawczyk_intervals(
    x_newton: &[BigRational],
    m_matrix: &[Vec<Interval>],
    delta_x_iv: &[Interval],
    n: usize,
) -> Vec<Interval> {
    let mut k_intervals = Vec::with_capacity(n);
    for (i, m_row) in m_matrix.iter().enumerate().take(n) {
        let mut coord_iv = Interval::point(x_newton[i].clone());
        for (k, m_ik) in m_row.iter().enumerate().take(n) {
            coord_iv = coord_iv.add(&m_ik.mul(&delta_x_iv[k]));
        }
        k_intervals.push(coord_iv);
    }
    k_intervals
}

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

    let x_0 = resolve_krawczyk_center(x_box, custom_x0, n)?;
    let fx = system.eval(&x_0);
    let df = system.jacobian(&x_0);

    let lu = ExactRationalLu::factorize(&df)?;
    let y_mat = lu.inverse()?;

    let newton_step = lu.solve(&fx)?;
    let x_newton: Vec<BigRational> = (0..n).map(|i| &x_0[i] - &newton_step[i]).collect();

    let df_iv = system.jacobian_interval(x_box);
    let m_matrix = build_krawczyk_m_matrix(&y_mat, &df_iv, n);

    let delta_x_iv: Vec<Interval> = (0..n)
        .map(|k| x_box.intervals[k].sub(&Interval::point(x_0[k].clone())))
        .collect();
    let k_intervals = assemble_krawczyk_intervals(&x_newton, &m_matrix, &delta_x_iv, n);

    let krawczyk_box = IntervalBox::new(k_intervals);
    let is_strictly_contracted = krawczyk_box.strict_interior_subset_of(x_box);
    let is_disjoint = krawczyk_box.is_disjoint_from(x_box);

    Ok(KrawczykResult {
        krawczyk_box,
        is_strictly_contracted,
        is_disjoint,
    })
}

pub fn krawczyk_contractor_custom_center(
    system: &SquarePolynomialSystem,
    x_box: &IntervalBox,
    center: &[BigRational],
) -> Result<KrawczykResult, LuError> {
    krawczyk_contractor(system, x_box, Some(center))
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CertifiedLeafCell {
    pub cell_id: String,
    pub center: Vec<BigRational>,
    pub radius: BigRational,
    pub residual_margin: BigRational,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SentryScanSummary {
    pub all_positive: bool,
    pub scanned_count: usize,
    pub min_margin: BigRational,
    pub zero_or_negative_margin_cells: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum SentryRootInspection {
    RootCertified {
        alpha: BigRational,
        beta: BigRational,
        gamma: BigRational,
        isolating_box: IntervalBox,
        krawczyk_box: IntervalBox,
    },
    RootUncertified { alpha: BigRational, reason: String },
}

pub struct SmaleSentry;

impl SmaleSentry {
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
