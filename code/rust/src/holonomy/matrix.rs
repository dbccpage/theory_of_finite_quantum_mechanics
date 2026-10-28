use crate::error::HolonomyError;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use engine_kernel::resource_limits::{check_and_reserve, OperationLimits};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fmt::{Debug, Display};

mod sealed {
    pub trait Scalar {}
    pub trait Rational {}
}

impl sealed::Scalar for BigRational {}
impl sealed::Rational for BigRational {}

/// Closed exact scalar domain: canonical arbitrary-precision rationals and Q(i).
/// Bounded rationals cannot implement this trait because their operators overflow.
pub trait ExactScalar:
    sealed::Scalar
    + Clone
    + PartialEq
    + Eq
    + Zero
    + One
    + std::ops::Add<Output = Self>
    + std::ops::Sub<Output = Self>
    + std::ops::Mul<Output = Self>
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
    fn validate_exact(&self) -> Result<(), HolonomyError>;
    fn add_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> Self;
    fn sub_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> Self;
    fn mul_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> Self;
    fn conjugate_eq_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> bool;
    fn exact_inv(&self) -> Result<Self, HolonomyError>;
    fn conjugate(&self) -> Self {
        self.clone()
    }
    fn from_i64(val: i64) -> Self;
}

impl ExactScalar for BigRational {
    fn add_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> Self {
        left.value + right.value
    }
    fn sub_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> Self {
        left.value - right.value
    }
    fn mul_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> Self {
        left.value * right.value
    }
    fn conjugate_eq_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> bool {
        left.value == right.value
    }
    fn validate_exact(&self) -> Result<(), HolonomyError> {
        if self.denom() <= &BigInt::zero() {
            return Err(HolonomyError::InvalidScalar {
                detail: "rational denominator must be positive".into(),
            });
        }
        let reduced = self.reduced();
        if self.numer() != reduced.numer() || self.denom() != reduced.denom() {
            return Err(HolonomyError::InvalidScalar {
                detail: "rational must be reduced".into(),
            });
        }
        Ok(())
    }
    fn exact_inv(&self) -> Result<Self, HolonomyError> {
        self.validate_exact()?;
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

/// Real components of Q(i). This sealed bound excludes iterated complex extensions.
pub trait RationalComponent: ExactScalar + sealed::Rational {
    fn opposite_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> bool;
}
impl RationalComponent for BigRational {
    fn opposite_admitted(left: ScalarRef<'_, Self>, right: ScalarRef<'_, Self>) -> bool {
        let (left, right) = (left.value, right.value);
        left.denom() == right.denom()
            && left.numer().magnitude() == right.numer().magnitude()
            && (left.numer().is_zero() || left.numer().sign() != right.numer().sign())
    }
}

/// An immutable borrow whose exact scalar domain has been admitted. Its private
/// field and immutable lifetime prevent forged or subsequently mutated values.
/// ```compile_fail
/// use num_rational::BigRational;
/// use tfqm_holonomy::matrix::ScalarRef;
/// let raw = BigRational::new_raw(1.into(), 0.into());
/// let _ = ScalarRef { value: &raw };
/// ```
pub struct ScalarRef<'a, T: ExactScalar> {
    value: &'a T,
}
impl<T: ExactScalar> Copy for ScalarRef<'_, T> {}
impl<T: ExactScalar> Clone for ScalarRef<'_, T> {
    fn clone(&self) -> Self {
        *self
    }
}
impl<'a, T: ExactScalar> ScalarRef<'a, T> {
    pub fn try_new(value: &'a T) -> Result<Self, HolonomyError> {
        value.validate_exact()?;
        Ok(Self { value })
    }
    pub fn value(self) -> &'a T {
        self.value
    }
    pub fn add(self, rhs: Self) -> T {
        T::add_admitted(self, rhs)
    }
    pub fn sub(self, rhs: Self) -> T {
        T::sub_admitted(self, rhs)
    }
    pub fn mul(self, rhs: Self) -> T {
        T::mul_admitted(self, rhs)
    }
    pub fn conjugate_eq(self, rhs: Self) -> bool {
        T::conjugate_eq_admitted(self, rhs)
    }
}

// Only admitted immutable matrix/Gaussian fields and closed arithmetic results
// reach these internal borrow constructors. External raw values use try_new.
fn add_ref<T: ExactScalar>(a: &T, b: &T) -> T {
    T::add_admitted(ScalarRef { value: a }, ScalarRef { value: b })
}
fn sub_ref<T: ExactScalar>(a: &T, b: &T) -> T {
    T::sub_admitted(ScalarRef { value: a }, ScalarRef { value: b })
}
fn mul_ref<T: ExactScalar>(a: &T, b: &T) -> T {
    T::mul_admitted(ScalarRef { value: a }, ScalarRef { value: b })
}
fn conjugate_eq<T: ExactScalar>(a: &T, b: &T) -> bool {
    T::conjugate_eq_admitted(ScalarRef { value: a }, ScalarRef { value: b })
}

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize)]
pub struct GaussianRational<T: RationalComponent = BigRational> {
    re: T,
    im: T,
}

impl<T: RationalComponent> GaussianRational<T> {
    pub fn new(re: T, im: T) -> Result<Self, HolonomyError> {
        re.validate_exact()?;
        im.validate_exact()?;
        Ok(Self { re, im })
    }

    pub fn real(&self) -> &T {
        &self.re
    }
    pub fn imag(&self) -> &T {
        &self.im
    }

    pub fn try_div(&self, rhs: &Self) -> Result<Self, HolonomyError> {
        Ok(mul_ref(self, &rhs.exact_inv()?))
    }

    pub fn i() -> Self {
        Self {
            re: T::zero(),
            im: T::one(),
        }
    }

    pub fn norm_sq(&self) -> T {
        add_ref(&mul_ref(&self.re, &self.re), &mul_ref(&self.im, &self.im))
    }
}

impl<T: RationalComponent> Display for GaussianRational<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}+{}i", self.re, self.im)
    }
}

impl<T: RationalComponent> Zero for GaussianRational<T> {
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

impl<T: RationalComponent> One for GaussianRational<T> {
    fn one() -> Self {
        Self {
            re: T::one(),
            im: T::zero(),
        }
    }
}

impl<T: RationalComponent> std::ops::Add for GaussianRational<T> {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        add_ref(&self, &rhs)
    }
}
impl<T: RationalComponent> std::ops::Sub for GaussianRational<T> {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        sub_ref(&self, &rhs)
    }
}
impl<T: RationalComponent> std::ops::Mul for GaussianRational<T> {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        mul_ref(&self, &rhs)
    }
}

impl<T: RationalComponent> std::ops::Div for GaussianRational<T> {
    type Output = Result<Self, HolonomyError>;
    fn div(self, rhs: Self) -> Self::Output {
        self.try_div(&rhs)
    }
}

impl<T: RationalComponent> std::ops::Neg for GaussianRational<T> {
    type Output = Self;
    fn neg(self) -> Self {
        Self {
            re: -self.re,
            im: -self.im,
        }
    }
}

impl<T: RationalComponent> std::ops::AddAssign for GaussianRational<T> {
    fn add_assign(&mut self, rhs: Self) {
        self.re += rhs.re;
        self.im += rhs.im;
    }
}

impl<T: RationalComponent> std::ops::SubAssign for GaussianRational<T> {
    fn sub_assign(&mut self, rhs: Self) {
        self.re -= rhs.re;
        self.im -= rhs.im;
    }
}

impl<T: RationalComponent> std::ops::MulAssign for GaussianRational<T> {
    fn mul_assign(&mut self, rhs: Self) {
        *self = mul_ref(self, &rhs);
    }
}

impl<T: RationalComponent> sealed::Scalar for GaussianRational<T> {}

impl<T: RationalComponent> ExactScalar for GaussianRational<T> {
    fn add_admitted(a: ScalarRef<'_, Self>, b: ScalarRef<'_, Self>) -> Self {
        Self {
            re: add_ref(&a.value.re, &b.value.re),
            im: add_ref(&a.value.im, &b.value.im),
        }
    }
    fn sub_admitted(a: ScalarRef<'_, Self>, b: ScalarRef<'_, Self>) -> Self {
        Self {
            re: sub_ref(&a.value.re, &b.value.re),
            im: sub_ref(&a.value.im, &b.value.im),
        }
    }
    fn mul_admitted(a: ScalarRef<'_, Self>, b: ScalarRef<'_, Self>) -> Self {
        let (a, b) = (a.value, b.value);
        Self {
            re: sub_ref(&mul_ref(&a.re, &b.re), &mul_ref(&a.im, &b.im)),
            im: add_ref(&mul_ref(&a.re, &b.im), &mul_ref(&a.im, &b.re)),
        }
    }
    fn conjugate_eq_admitted(a: ScalarRef<'_, Self>, b: ScalarRef<'_, Self>) -> bool {
        a.value.re == b.value.re
            && T::opposite_admitted(
                ScalarRef { value: &a.value.im },
                ScalarRef { value: &b.value.im },
            )
    }
    fn validate_exact(&self) -> Result<(), HolonomyError> {
        self.re.validate_exact()?;
        self.im.validate_exact()
    }
    fn exact_inv(&self) -> Result<Self, HolonomyError> {
        let n_sq = self.norm_sq();
        if n_sq.is_zero() {
            return Err(HolonomyError::ZeroDivision);
        }
        let inv_norm = n_sq.exact_inv()?;
        Ok(Self {
            re: mul_ref(&self.re, &inv_norm),
            im: -mul_ref(&self.im, &inv_norm),
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

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct GaussianWire<T> {
    re: T,
    im: T,
}

impl<'de, T: RationalComponent + Deserialize<'de>> Deserialize<'de> for GaussianRational<T> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let wire = GaussianWire::<T>::deserialize(deserializer)?;
        Self::new(wire.re, wire.im).map_err(serde::de::Error::custom)
    }
}

/// An admitted immutable shape/storage pair over the closed exact scalar domain.
/// Checked setters preserve scalar admission; decoding uses the same constructor.
///
/// External implementations cannot enlarge the trusted scalar domain:
/// ```compile_fail
/// struct Unchecked;
/// impl tfqm_holonomy::matrix::sealed::Scalar for Unchecked {}
/// ```
/// External callers cannot forge the shape/storage invariant:
/// ```compile_fail
/// use num_rational::BigRational;
/// use tfqm_holonomy::ExactMatrix;
/// let _ = ExactMatrix::<BigRational> { rows: 1, cols: 1, data: vec![] };
/// ```
/// Machine-bounded rationals are excluded before arithmetic:
/// ```compile_fail
/// use num_rational::Rational64;
/// use tfqm_holonomy::ExactMatrix;
/// let _ = ExactMatrix::try_new(1, 1, vec![Rational64::from_integer(i64::MAX)]);
/// ```
/// The corresponding admitted construction compiles and has checked access:
/// ```
/// use num_rational::BigRational;
/// use tfqm_holonomy::ExactMatrix;
/// let matrix = ExactMatrix::try_new(1, 1, vec![BigRational::from_integer(1.into())])?;
/// assert_eq!(matrix.get(0, 0)?, &BigRational::from_integer(1.into()));
/// # Ok::<(), tfqm_holonomy::HolonomyError>(())
/// ```
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct ExactMatrix<T: ExactScalar> {
    rows: usize,
    cols: usize,
    data: Vec<T>,
}

impl<T: ExactScalar> ExactMatrix<T> {
    pub fn try_new(rows: usize, cols: usize, data: Vec<T>) -> Result<Self, HolonomyError> {
        Self::try_new_with_limits(rows, cols, data, &OperationLimits::holonomy())
    }

    pub fn try_new_with_limits(
        rows: usize,
        cols: usize,
        data: Vec<T>,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        let expected = admit_cells(rows, cols, limits)?;
        if expected != data.len() {
            return Err(HolonomyError::DimensionMismatch {
                expected,
                actual: data.len(),
            });
        }
        admit_work(expected, limits)?;
        data.iter().try_for_each(ExactScalar::validate_exact)?;
        Ok(Self { rows, cols, data })
    }

    pub fn try_identity(n: usize) -> Result<Self, HolonomyError> {
        Self::build_identity(n, &OperationLimits::holonomy())
    }

    fn build_identity(n: usize, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        let total = admit_cells(n, n, limits)?;
        admit_work(total, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
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
        admit_dimensions(n, n, limits)?;
        Self::build_identity(n, limits)
    }

    pub fn try_zero(rows: usize, cols: usize) -> Result<Self, HolonomyError> {
        Self::try_zero_with_limits(rows, cols, &OperationLimits::holonomy())
    }

    pub fn try_zero_with_limits(
        rows: usize,
        cols: usize,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        let total = admit_cells(rows, cols, limits)?;
        admit_work(total, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
        data.resize_with(total, T::zero);
        Ok(Self { rows, cols, data })
    }

    pub fn from_vec(
        rows: usize,
        cols: usize,
        data: Vec<T>,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        admit_dimensions(rows, cols, limits)?;
        Self::try_new_with_limits(rows, cols, data, limits)
    }

    #[inline(always)]
    // Bounds proof: only this module calls at/at_mut, with coordinates from
    // 0..rows and 0..cols on immutable, constructor-admitted storage. Therefore
    // r*cols+c < rows*cols == data.len(), and index arithmetic cannot overflow.
    fn at(&self, r: usize, c: usize) -> &T {
        &self.data[r * self.cols + c]
    }

    #[inline(always)]
    fn at_mut(&mut self, r: usize, c: usize) -> &mut T {
        &mut self.data[r * self.cols + c]
    }

    pub fn rows(&self) -> usize {
        self.rows
    }
    pub fn cols(&self) -> usize {
        self.cols
    }
    pub fn shape(&self) -> (usize, usize) {
        (self.rows, self.cols)
    }
    pub fn as_slice(&self) -> &[T] {
        &self.data
    }

    fn index(&self, row: usize, col: usize) -> Result<usize, HolonomyError> {
        if row >= self.rows || col >= self.cols {
            return Err(HolonomyError::MatrixIndexOutOfBounds {
                row,
                col,
                rows: self.rows,
                cols: self.cols,
            });
        }
        // The admitted shape establishes row*cols+col < data.len() <= usize::MAX.
        Ok(row * self.cols + col)
    }

    pub fn get(&self, row: usize, col: usize) -> Result<&T, HolonomyError> {
        Ok(&self.data[self.index(row, col)?])
    }

    pub fn get_scalar(&self, row: usize, col: usize) -> Result<ScalarRef<'_, T>, HolonomyError> {
        Ok(ScalarRef {
            value: self.get(row, col)?,
        })
    }

    pub fn set(&mut self, row: usize, col: usize, value: T) -> Result<(), HolonomyError> {
        let index = self.index(row, col)?;
        value.validate_exact()?;
        self.data[index] = value;
        Ok(())
    }

    pub fn matmul(&self, other: &Self) -> Result<Self, HolonomyError> {
        self.multiply(other, &OperationLimits::holonomy())
    }

    fn admit_product(
        &self,
        other: &Self,
        limits: &OperationLimits,
    ) -> Result<usize, HolonomyError> {
        if self.cols != other.rows {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.cols,
                actual: other.rows,
            });
        }
        admit_cells(self.rows, self.cols, limits)?;
        admit_cells(other.rows, other.cols, limits)?;
        let total = admit_cells(self.rows, other.cols, limits)?;
        let work = total
            .checked_mul(self.cols)
            .and_then(|n| n.checked_mul(2))
            .ok_or(HolonomyError::ResourceCountOverflow)?;
        admit_work(work, limits)?;
        Ok(total)
    }

    fn multiply(&self, other: &Self, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        let total = self.admit_product(other, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
        if total == 0 {
            return Ok(Self {
                rows: self.rows,
                cols: other.cols,
                data,
            });
        }

        for r in 0..self.rows {
            for c in 0..other.cols {
                let mut acc = T::zero();
                for k in 0..self.cols {
                    acc = add_ref(&acc, &mul_ref(self.at(r, k), other.at(k, c)));
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
        admit_dimensions(self.rows, other.cols, limits)?;
        self.multiply(other, limits)
    }

    pub fn transpose(&self) -> Result<Self, HolonomyError> {
        self.transpose_with_limits(&OperationLimits::holonomy())
    }

    pub fn transpose_with_limits(&self, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        if self.data.is_empty() {
            return Ok(Self {
                rows: self.cols,
                cols: self.rows,
                data: Vec::new(),
            });
        }
        let total = admit_cells(self.rows, self.cols, limits)?;
        admit_work(total, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
        for c in 0..self.cols {
            for r in 0..self.rows {
                data.push(self.at(r, c).clone());
            }
        }
        Ok(Self {
            rows: self.cols,
            cols: self.rows,
            data,
        })
    }

    pub fn conjugate_transpose(&self) -> Result<Self, HolonomyError> {
        self.conjugate_transpose_with_limits(&OperationLimits::holonomy())
    }

    pub fn conjugate_transpose_with_limits(
        &self,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        if self.data.is_empty() {
            return Ok(Self {
                rows: self.cols,
                cols: self.rows,
                data: Vec::new(),
            });
        }
        let total = admit_cells(self.rows, self.cols, limits)?;
        admit_work(total, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
        for c in 0..self.cols {
            for r in 0..self.rows {
                data.push(self.at(r, c).conjugate());
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
            tr += self.at(i, i).clone();
        }
        Ok(tr)
    }

    pub fn determinant(&self) -> Result<T, HolonomyError> {
        self.determinant_with_limits(&OperationLimits::holonomy())
    }

    pub fn determinant_with_limits(&self, limits: &OperationLimits) -> Result<T, HolonomyError> {
        let n = self.square_dimension()?;
        self.preflight_elimination(limits)?;
        let mut mat = self.try_clone_with_limits(limits)?;
        let mut determinant = T::one();
        for column in 0..n {
            let Some(pivot) = mat.find_pivot(column, column) else {
                return Ok(T::zero());
            };
            if pivot != column {
                mat.swap_rows(pivot, column);
                determinant = -determinant;
            }
            let value = mat.at(column, column);
            determinant = mul_ref(&determinant, value);
            let inverse = value.exact_inv()?;
            mat.eliminate_below(column, &inverse);
        }
        Ok(determinant)
    }

    pub fn inverse(&self) -> Result<Self, HolonomyError> {
        self.inverse_with_limits(&OperationLimits::holonomy())
    }

    pub fn inverse_with_limits(&self, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        let n = self.square_dimension()?;
        let mut augmented = self.augmented_identity(n, limits)?;
        for column in 0..n {
            let pivot = augmented.find_pivot(column, column).ok_or_else(|| {
                HolonomyError::SingularMatrix {
                    detail: format!("zero pivot in column {column}"),
                }
            })?;
            augmented.swap_rows(column, pivot);
            let inverse = augmented.at(column, column).exact_inv()?;
            augmented.scale_row(column, &inverse);
            augmented.eliminate_column(column, column);
        }
        augmented.right_block(n, limits)
    }

    pub fn is_symmetric(&self) -> bool {
        if self.rows != self.cols {
            return false;
        }
        for r in 0..self.rows {
            for c in (r + 1)..self.cols {
                if self.at(r, c) != self.at(c, r) {
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
                if !conjugate_eq(self.at(r, c), self.at(c, r)) {
                    return false;
                }
            }
        }
        true
    }

    pub fn rank(&self) -> Result<usize, HolonomyError> {
        self.rank_with_limits(&OperationLimits::holonomy())
    }

    pub fn rank_with_limits(&self, limits: &OperationLimits) -> Result<usize, HolonomyError> {
        if self.data.is_empty() {
            return Ok(0);
        }
        self.preflight_elimination(limits)?;
        let mut mat = self.try_clone_with_limits(limits)?;
        let mut rank = 0;
        for column in 0..self.cols {
            if rank == self.rows {
                break;
            }
            let Some(pivot) = mat.find_pivot(rank, column) else {
                continue;
            };
            mat.swap_rows(rank, pivot);
            let inverse = mat.at(rank, column).exact_inv()?;
            mat.scale_row(rank, &inverse);
            mat.eliminate_column(rank, column);
            rank += 1;
        }
        Ok(rank)
    }

    fn square_dimension(&self) -> Result<usize, HolonomyError> {
        if self.rows != self.cols {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.rows,
                actual: self.cols,
            });
        }
        Ok(self.rows)
    }

    fn try_clone_with_limits(&self, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        let cells = admit_cells(self.rows, self.cols, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, cells, limits.max_cells)?;
        data.extend_from_slice(&self.data);
        Ok(Self {
            rows: self.rows,
            cols: self.cols,
            data,
        })
    }

    fn find_pivot(&self, start: usize, column: usize) -> Option<usize> {
        (start..self.rows).find(|&row| !self.at(row, column).is_zero())
    }

    fn swap_rows(&mut self, first: usize, second: usize) {
        for column in 0..self.cols {
            self.data
                .swap(first * self.cols + column, second * self.cols + column);
        }
    }

    fn scale_row(&mut self, row: usize, factor: &T) {
        for column in 0..self.cols {
            let value = mul_ref(self.at(row, column), factor);
            *self.at_mut(row, column) = value;
        }
    }

    fn subtract_scaled_row(&mut self, target: usize, source: usize, factor: &T, start: usize) {
        for column in start..self.cols {
            let delta = mul_ref(factor, self.at(source, column));
            let value = sub_ref(self.at(target, column), &delta);
            *self.at_mut(target, column) = value;
        }
    }

    fn eliminate_below(&mut self, column: usize, pivot_inverse: &T) {
        for row in column + 1..self.rows {
            if !self.at(row, column).is_zero() {
                let factor = mul_ref(self.at(row, column), pivot_inverse);
                self.subtract_scaled_row(row, column, &factor, column);
            }
        }
    }

    fn eliminate_column(&mut self, pivot: usize, column: usize) {
        for row in 0..self.rows {
            if row != pivot {
                let factor = self.at(row, column).clone();
                if !factor.is_zero() {
                    self.subtract_scaled_row(row, pivot, &factor, 0);
                }
            }
        }
    }

    fn augmented_entry(&self, row: usize, column: usize) -> T {
        if column < self.cols {
            return self.at(row, column).clone();
        }
        if column - self.cols == row {
            T::one()
        } else {
            T::zero()
        }
    }

    fn augmented_identity(
        &self,
        n: usize,
        limits: &OperationLimits,
    ) -> Result<Self, HolonomyError> {
        let cols = n
            .checked_mul(2)
            .ok_or(HolonomyError::ResourceCountOverflow)?;
        let total = admit_cells(n, cols, limits)?;
        admit_work(elimination_work(n, cols)?, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
        for row in 0..n {
            for column in 0..cols {
                data.push(self.augmented_entry(row, column));
            }
        }
        Ok(Self {
            rows: n,
            cols,
            data,
        })
    }

    fn right_block(self, n: usize, limits: &OperationLimits) -> Result<Self, HolonomyError> {
        let total = admit_cells(n, n, limits)?;
        let mut data = Vec::new();
        check_and_reserve(&mut data, total, limits.max_cells)?;
        if n == 0 {
            return Ok(Self {
                rows: 0,
                cols: 0,
                data,
            });
        }
        // Only inverse calls this helper: self has shape (n, 2n). Thus cols is
        // positive here; selecting the second n cells of each row yields n*n.
        for (index, value) in self.data.into_iter().enumerate() {
            if index % self.cols >= n {
                data.push(value);
            }
        }
        Ok(Self {
            rows: n,
            cols: n,
            data,
        })
    }

    fn preflight_elimination(&self, limits: &OperationLimits) -> Result<(), HolonomyError> {
        admit_cells(self.rows, self.cols, limits)?;
        admit_work(elimination_work(self.rows, self.cols)?, limits)
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

// Budgets count dense cells, construction/copy visits, and a conservative
// scalar addition/multiplication/subtraction/inversion bound for elimination.
// They do not bound BigInt bit lengths, process memory, or elapsed time.
fn admit_cells(rows: usize, cols: usize, limits: &OperationLimits) -> Result<usize, HolonomyError> {
    let requested = rows
        .checked_mul(cols)
        .ok_or(HolonomyError::ResourceCountOverflow)?;
    if requested > limits.max_cells {
        return Err(HolonomyError::MatrixCellLimitExceeded {
            requested,
            limit: limits.max_cells,
        });
    }
    Ok(requested)
}

fn admit_work(requested: usize, limits: &OperationLimits) -> Result<(), HolonomyError> {
    if requested > limits.max_operations {
        return Err(HolonomyError::OperationLimitExceeded {
            requested,
            limit: limits.max_operations,
        });
    }
    Ok(())
}

fn admit_dimensions(
    rows: usize,
    cols: usize,
    limits: &OperationLimits,
) -> Result<(), HolonomyError> {
    let requested = rows.max(cols);
    if requested > limits.max_dimension {
        return Err(HolonomyError::DimensionMismatch {
            expected: limits.max_dimension,
            actual: requested,
        });
    }
    Ok(())
}

fn elimination_work(rows: usize, cols: usize) -> Result<usize, HolonomyError> {
    rows.checked_mul(cols)
        .and_then(|v| v.checked_mul(rows.min(cols)))
        .and_then(|v| v.checked_mul(3))
        .and_then(|v| v.checked_add(rows.min(cols)))
        .ok_or(HolonomyError::ResourceCountOverflow)
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct MatrixWire<T> {
    rows: usize,
    cols: usize,
    data: Vec<T>,
}

impl<'de, T: ExactScalar + Deserialize<'de>> Deserialize<'de> for ExactMatrix<T> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let wire = MatrixWire::<T>::deserialize(deserializer)?;
        Self::try_new(wire.rows, wire.cols, wire.data).map_err(serde::de::Error::custom)
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
