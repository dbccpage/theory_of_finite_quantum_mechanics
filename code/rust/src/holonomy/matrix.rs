
use crate::error::HolonomyError;
use num_bigint::BigInt;
use num_rational::{BigRational, Rational64};
use num_traits::{One, Zero};
use omega_kernel::resource_limits::{check_and_reserve, OperationLimits};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fmt::{Debug, Display};

pub trait ExactScalar:
    Clone
    + PartialEq
    + Eq
    + Zero
    + One
    + std::ops::Add<Output = Self>
    + std::ops::Sub<Output = Self>
    + std::ops::Mul<Output = Self>
    + std::ops::Div<Output = Self>
    + std::ops::Neg<Output = Self>
    + std::ops::AddAssign
    + std::ops::SubAssign
    + std::ops::MulAssign
    + Debug
    + Display
    + Send
    + Sync
    + 'static
{
    fn exact_inv(&self) -> Result<Self, HolonomyError>;
    fn conjugate(&self) -> Self {
        self.clone()
    }
    fn from_i64(val: i64) -> Self;
}

impl ExactScalar for BigRational {
    fn exact_inv(&self) -> Result<Self, HolonomyError> {
        if self.is_zero() {
            Err(HolonomyError::ZeroDivision)
        } else {
            Ok(self.recip())
        }
    }
    fn from_i64(val: i64) -> Self {
        BigRational::from_integer(BigInt::from(val))
    }
}

impl ExactScalar for Rational64 {
    fn exact_inv(&self) -> Result<Self, HolonomyError> {
        if self.is_zero() {
            Err(HolonomyError::ZeroDivision)
        } else {
            Ok(self.recip())
        }
    }
    fn from_i64(val: i64) -> Self {
        Rational64::from_integer(val)
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct GaussianRational<T: ExactScalar> {
    pub re: T,
    pub im: T,
}

impl<T: ExactScalar> GaussianRational<T> {
    pub fn new(re: T, im: T) -> Self {
        Self { re, im }
    }

    pub fn i() -> Self {
        Self {
            re: T::zero(),
            im: T::one(),
        }
    }

    pub fn norm_sq(&self) -> T {
        self.re.clone() * self.re.clone() + self.im.clone() * self.im.clone()
    }
}

impl<T: ExactScalar> Display for GaussianRational<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}+{}i", self.re, self.im)
    }
}

impl<T: ExactScalar> Zero for GaussianRational<T> {
    fn zero() -> Self {
        Self {
            re: T::zero(),
            im: T::zero(),
        }
    }
    fn is_zero(&self) -> bool {
        self.re.is_zero() && self.im.is_zero()
    }
}

impl<T: ExactScalar> One for GaussianRational<T> {
    fn one() -> Self {
        Self {
            re: T::one(),
            im: T::zero(),
        }
    }
}

impl<T: ExactScalar> std::ops::Add for GaussianRational<T> {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Self {
            re: self.re + rhs.re,
            im: self.im + rhs.im,
        }
    }
}

impl<T: ExactScalar> std::ops::Sub for GaussianRational<T> {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        Self {
            re: self.re - rhs.re,
            im: self.im - rhs.im,
        }
    }
}

impl<T: ExactScalar> std::ops::Mul for GaussianRational<T> {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Self {
            re: self.re.clone() * rhs.re.clone() - self.im.clone() * rhs.im.clone(),
            im: self.re * rhs.im + self.im * rhs.re,
        }
    }
}

impl<T: ExactScalar> std::ops::Div for GaussianRational<T> {
    type Output = Self;
    #[allow(clippy::suspicious_arithmetic_impl)]
    fn div(self, rhs: Self) -> Self {
        let inv = rhs.exact_inv().expect("division by zero");
        self * inv
    }
}

impl<T: ExactScalar> std::ops::Neg for GaussianRational<T> {
    type Output = Self;
    fn neg(self) -> Self {
        Self {
            re: -self.re,
            im: -self.im,
        }
    }
}

impl<T: ExactScalar> std::ops::AddAssign for GaussianRational<T> {
    fn add_assign(&mut self, rhs: Self) {
        self.re += rhs.re;
        self.im += rhs.im;
    }
}

impl<T: ExactScalar> std::ops::SubAssign for GaussianRational<T> {
    fn sub_assign(&mut self, rhs: Self) {
        self.re -= rhs.re;
        self.im -= rhs.im;
    }
}

impl<T: ExactScalar> std::ops::MulAssign for GaussianRational<T> {
    fn mul_assign(&mut self, rhs: Self) {
        let res = self.clone() * rhs;
        *self = res;
    }
}

impl<T: ExactScalar> ExactScalar for GaussianRational<T> {
    fn exact_inv(&self) -> Result<Self, HolonomyError> {
        let n_sq = self.norm_sq();
        if n_sq.is_zero() {
            return Err(HolonomyError::ZeroDivision);
        }
        let inv_norm = n_sq.exact_inv()?;
        Ok(Self {
            re: self.re.clone() * inv_norm.clone(),
            im: -self.im.clone() * inv_norm,
        })
    }

    fn conjugate(&self) -> Self {
        Self {
            re: self.re.clone(),
            im: -self.im.clone(),
        }
    }

    fn from_i64(val: i64) -> Self {
        Self {
            re: T::from_i64(val),
            im: T::zero(),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactMatrix<T: ExactScalar> {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<T>,
}

impl<T: ExactScalar> ExactMatrix<T> {
    pub fn try_new(rows: usize, cols: usize, data: Vec<T>) -> Result<Self, HolonomyError> {
        let expected = rows
            .checked_mul(cols)
            .ok_or(HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Matrix dimensions overflow usize".into(),
            })?;
        if expected != data.len() {
            return Err(HolonomyError::DimensionMismatch {
                expected,
                actual: data.len(),
            });
        }
        Ok(Self { rows, cols, data })
    }

    pub fn try_identity(n: usize) -> Result<Self, HolonomyError> {
        let total = n.checked_mul(n).ok_or(HolonomyError::AllocationFailure {
            requested: usize::MAX,
            detail: "Identity matrix dimension overflow".into(),
        })?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, total)?;
        for r in 0..n {
            for c in 0..n {
                data.push(if r == c { T::one() } else { T::zero() });
            }
        }
        Ok(Self {
            rows: n,
            cols: n,
            data,
        })
    }

    pub fn identity(n: usize, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        if n > limits.max_dimension {
            return Err(HolonomyError::AllocationFailure {
                requested: n,
                detail: format!(
                    "Requested dimension {n} > max_dimension {}",
                    limits.max_dimension
                ),
            });
        }
        Self::try_identity(n)
    }

    pub fn try_zero(rows: usize, cols: usize) -> Result<Self, HolonomyError> {
        let total = rows
            .checked_mul(cols)
            .ok_or(HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Zero matrix dimension overflow".into(),
            })?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, total)?;
        for _ in 0..total {
            data.push(T::zero());
        }
        Ok(Self { rows, cols, data })
    }

    pub fn from_vec(
        rows: usize,
        cols: usize,
        data: Vec<T>,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        if rows > limits.max_dimension || cols > limits.max_dimension {
            return Err(HolonomyError::AllocationFailure {
                requested: rows.max(cols),
                detail: format!(
                    "Matrix dimensions ({rows}x{cols}) exceed max_dimension {}",
                    limits.max_dimension
                ),
            });
        }
        Self::try_new(rows, cols, data)
    }

    #[inline(always)]
    pub fn get(&self, r: usize, c: usize) -> &T {
        &self.data[r * self.cols + c]
    }

    #[inline(always)]
    pub fn get_mut(&mut self, r: usize, c: usize) -> &mut T {
        &mut self.data[r * self.cols + c]
    }

    pub fn matmul(&self, other: &Self) -> Result<Self, HolonomyError> {
        if self.cols != other.rows {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.cols,
                actual: other.rows,
            });
        }
        let total = self
            .rows
            .checked_mul(other.cols)
            .ok_or(HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Matmul result dimension overflow".into(),
            })?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, total)?;

        for r in 0..self.rows {
            for c in 0..other.cols {
                let mut acc = T::zero();
                for k in 0..self.cols {
                    acc += self.get(r, k).clone() * other.get(k, c).clone();
                }
                data.push(acc);
            }
        }
        Ok(Self {
            rows: self.rows,
            cols: other.cols,
            data,
        })
    }

    pub fn matmul_with_limits(
        &self,
        other: &Self,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        if self.rows > limits.max_dimension || other.cols > limits.max_dimension {
            return Err(HolonomyError::AllocationFailure {
                requested: self.rows.max(other.cols),
                detail: format!(
                    "Matmul result exceeds max_dimension {}",
                    limits.max_dimension
                ),
            });
        }
        self.matmul(other)
    }

    pub fn transpose(&self) -> Result<Self, HolonomyError> {
        let total = self
            .rows
            .checked_mul(self.cols)
            .ok_or(HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Transpose dimension overflow".into(),
            })?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, total)?;
        for c in 0..self.cols {
            for r in 0..self.rows {
                data.push(self.get(r, c).clone());
            }
        }
        Ok(Self {
            rows: self.cols,
            cols: self.rows,
            data,
        })
    }

    pub fn conjugate_transpose(&self) -> Result<Self, HolonomyError> {
        let total = self
            .rows
            .checked_mul(self.cols)
            .ok_or(HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Conjugate transpose dimension overflow".into(),
            })?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, total)?;
        for c in 0..self.cols {
            for r in 0..self.rows {
                data.push(self.get(r, c).conjugate());
            }
        }
        Ok(Self {
            rows: self.cols,
            cols: self.rows,
            data,
        })
    }

    pub fn trace(&self) -> Result<T, HolonomyError> {
        if self.rows != self.cols {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.rows,
                actual: self.cols,
            });
        }
        let mut tr = T::zero();
        for i in 0..self.rows {
            tr += self.get(i, i).clone();
        }
        Ok(tr)
    }

    pub fn determinant(&self) -> Result<T, HolonomyError> {
        if self.rows != self.cols {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.rows,
                actual: self.cols,
            });
        }
        let n = self.rows;
        let mut mat = self.clone();
        let mut det = T::one();

        for i in 0..n {
            let mut pivot = i;
            while pivot < n && mat.get(pivot, i).is_zero() {
                pivot += 1;
            }
            if pivot == n {
                return Ok(T::zero());
            }
            if pivot != i {
                for c in 0..n {
                    mat.data.swap(i * n + c, pivot * n + c);
                }
                det = -det;
            }
            let pivot_val = mat.get(i, i).clone();
            det *= pivot_val.clone();
            let inv_p = pivot_val.exact_inv()?;

            for r in (i + 1)..n {
                let factor = mat.get(r, i).clone();
                if !factor.is_zero() {
                    let scale = factor * inv_p.clone();
                    for c in i..n {
                        let sub_val = scale.clone() * mat.get(i, c).clone();
                        *mat.get_mut(r, c) -= sub_val;
                    }
                }
            }
        }
        Ok(det)
    }

    pub fn inverse(&self) -> Result<Self, HolonomyError> {
        if self.rows != self.cols {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.rows,
                actual: self.cols,
            });
        }
        let n = self.rows;
        let stride = 2 * n;
        let total_aug = n
            .checked_mul(stride)
            .ok_or(HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Augmented matrix overflow".into(),
            })?;

        let mut aug = Vec::new();
        check_and_reserve(&mut aug, total_aug, total_aug)?;

        for r in 0..n {
            for c in 0..n {
                aug.push(self.get(r, c).clone());
            }
            for c in 0..n {
                aug.push(if r == c { T::one() } else { T::zero() });
            }
        }

        for i in 0..n {
            let mut pivot = i;
            while pivot < n && aug[pivot * stride + i].is_zero() {
                pivot += 1;
            }
            if pivot == n {
                return Err(HolonomyError::SingularMatrix {
                    detail: format!("Zero pivot encountered at row {i}; matrix is non-invertible"),
                });
            }
            if pivot != i {
                for c in 0..stride {
                    aug.swap(i * stride + c, pivot * stride + c);
                }
            }
            let pivot_val = aug[i * stride + i].clone();
            let inv_p = pivot_val.exact_inv()?;
            for c in 0..stride {
                aug[i * stride + c] *= inv_p.clone();
            }
            for r in 0..n {
                if r != i {
                    let factor = aug[r * stride + i].clone();
                    if !factor.is_zero() {
                        for c in 0..stride {
                            let sub_val = factor.clone() * aug[i * stride + c].clone();
                            aug[r * stride + c] -= sub_val;
                        }
                    }
                }
            }
        }

        let total_inv = n * n;
        let mut inv_data = Vec::new();
        check_and_reserve(&mut inv_data, total_inv, total_inv)?;
        for r in 0..n {
            for c in 0..n {
                inv_data.push(aug[r * stride + (c + n)].clone());
            }
        }
        Ok(Self {
            rows: n,
            cols: n,
            data: inv_data,
        })
    }

    pub fn is_symmetric(&self) -> bool {
        if self.rows != self.cols {
            return false;
        }
        for r in 0..self.rows {
            for c in (r + 1)..self.cols {
                if self.get(r, c) != self.get(c, r) {
                    return false;
                }
            }
        }
        true
    }

    pub fn is_hermitian(&self) -> bool {
        if self.rows != self.cols {
            return false;
        }
        for r in 0..self.rows {
            for c in r..self.cols {
                if *self.get(r, c) != self.get(c, r).conjugate() {
                    return false;
                }
            }
        }
        true
    }

    pub fn rank(&self) -> usize {
        let mut mat = self.clone();
        let rows = mat.rows;
        let cols = mat.cols;
        let mut r_lead = 0;

        for c in 0..cols {
            if r_lead >= rows {
                break;
            }
            let mut pivot = r_lead;
            while pivot < rows && mat.get(pivot, c).is_zero() {
                pivot += 1;
            }
            if pivot == rows {
                continue;
            }
            if pivot != r_lead {
                for col_idx in 0..cols {
                    mat.data
                        .swap(r_lead * cols + col_idx, pivot * cols + col_idx);
                }
            }
            let pivot_val = mat.get(r_lead, c).clone();
            let inv_p = match pivot_val.exact_inv() {
                Ok(inv) => inv,
                Err(_) => continue,
            };
            for col_idx in 0..cols {
                *mat.get_mut(r_lead, col_idx) *= inv_p.clone();
            }
            for r in 0..rows {
                if r != r_lead {
                    let factor = mat.get(r, c).clone();
                    if !factor.is_zero() {
                        for col_idx in 0..cols {
                            let sub = factor.clone() * mat.get(r_lead, col_idx).clone();
                            *mat.get_mut(r, col_idx) -= sub;
                        }
                    }
                }
            }
            r_lead += 1;
        }
        r_lead
    }

    pub fn sha256_digest(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(format!("Matrix:{}x{}:", self.rows, self.cols).as_bytes());
        for entry in &self.data {
            hasher.update(format!("{entry};").as_bytes());
        }
        hex::encode(hasher.finalize())
    }
}

mod hex {
    pub fn encode(bytes: impl AsRef<[u8]>) -> String {
        bytes
            .as_ref()
            .iter()
            .map(|b| format!("{:02x}", b))
            .collect()
    }
}

pub type RationalMatrix = ExactMatrix<BigRational>;
