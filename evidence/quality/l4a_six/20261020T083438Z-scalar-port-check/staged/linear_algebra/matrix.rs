
use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use crate::linear_algebra::{
    charge, element_count, plus, require_same_shape, require_square, reserve, times,
    ExactFieldError,
};
use crate::linear_algebra::scalars::{ExactRing, Field};
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::{BigRational, Rational64};
use num_traits::{Signed, ToPrimitive, Zero};


pub fn identity<F: Field + ExactRing>(n: usize) -> Result<BasicMatrix<F>, ExactFieldError> {
    identity_with_limits(n, OperationLimits::UNLIMITED)
}

pub fn identity_with_limits<F: Field + ExactRing>(
    n: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    charge(limits, element_count(n, n)?, 0)?;
    Ok(BasicMatrix::try_from_fn_with_limit(
        n,
        n,
        limits.max_elements,
        |r, c| if r == c { F::one() } else { F::zero() },
    )?)
}

pub fn zeros<F: Field + ExactRing>(
    rows: usize,
    cols: usize,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    zeros_with_limits(rows, cols, OperationLimits::UNLIMITED)
}

pub fn zeros_with_limits<F: Field + ExactRing>(
    rows: usize,
    cols: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    charge(limits, element_count(rows, cols)?, 0)?;
    Ok(BasicMatrix::try_from_fn_with_limit(
        rows,
        cols,
        limits.max_elements,
        |_, _| F::zero(),
    )?)
}

pub fn diagonal<F: Field + ExactRing>(entries: &[F]) -> Result<BasicMatrix<F>, ExactFieldError> {
    let n = entries.len();
    let mut data: Vec<F> = reserve(element_count(n, n)?)?;
    for r in 0..n {
        for c in 0..n {
            data.push(match entries.get(r) {
                Some(entry) if r == c => entry.clone(),
                _ => F::zero(),
            });
        }
    }
    Ok(BasicMatrix::from_row_major(n, n, data)?)
}

pub fn from_rows<F: Field + ExactRing>(
    rows: Vec<Vec<F>>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let cols = rows.first().map_or(0, Vec::len);
    let row_count = rows.len();
    if let Some((index, row)) = rows.iter().enumerate().find(|(_, row)| row.len() != cols) {
        return Err(ExactFieldError::RaggedRows {
            row: index,
            len: row.len(),
            expected: cols,
        });
    }
    let mut data: Vec<F> = reserve(element_count(row_count, cols)?)?;
    for row in rows {
        data.extend(row);
    }
    Ok(BasicMatrix::from_row_major(row_count, cols, data)?)
}

/// Rows of `m`. A `0×n` matrix has no rows, so the result is `[]` and does not
/// retain `n`. `from_rows` of that result is `0×0`. The round trip holds when
/// `m.rows() > 0` or `m.cols() == 0`.
pub fn to_rows<F: Field + ExactRing>(m: &BasicMatrix<F>) -> Result<Vec<Vec<F>>, ExactFieldError> {
    let mut rows = reserve(m.rows())?;
    for r in 0..m.rows() {
        rows.push(row(m, r)?);
    }
    Ok(rows)
}

pub fn from_fn<F, G>(rows: usize, cols: usize, f: G) -> Result<BasicMatrix<F>, ExactFieldError>
where
    F: Field + ExactRing,
    G: FnMut(usize, usize) -> F,
{
    from_fn_with_limits(rows, cols, OperationLimits::UNLIMITED, f)
}

pub fn from_fn_with_limits<F, G>(
    rows: usize,
    cols: usize,
    limits: OperationLimits,
    f: G,
) -> Result<BasicMatrix<F>, ExactFieldError>
where
    F: Field + ExactRing,
    G: FnMut(usize, usize) -> F,
{
    charge(limits, element_count(rows, cols)?, 0)?;
    Ok(BasicMatrix::try_from_fn_with_limit(
        rows,
        cols,
        limits.max_elements,
        f,
    )?)
}

fn axis_out_of_bounds(row: usize, col: usize, rows: usize, cols: usize) -> ExactFieldError {
    ExactFieldError::Matrix(MatrixError::IndexOutOfBounds {
        row,
        col,
        rows,
        cols,
    })
}

pub(crate) fn try_from_fn_with_limits<F, G>(
    rows: usize, cols: usize, limits: OperationLimits, mut f: G,
) -> Result<BasicMatrix<F>, ExactFieldError>
where
    F: Field + ExactRing,
    G: FnMut(usize, usize) -> Result<F, ExactFieldError>,
{
    let count = element_count(rows, cols)?;
    charge(limits, count, 0)?;
    let mut data = reserve(count)?;
    if count != 0 {
        for r in 0..rows {
            for c in 0..cols {
                let value = f(r, c)?;
                value.validate()?;
                data.push(value);
            }
        }
    }
    Ok(BasicMatrix::from_row_major(rows, cols, data)?)
}

pub fn row<F: Field + ExactRing>(m: &BasicMatrix<F>, r: usize) -> Result<Vec<F>, ExactFieldError> {
    if r >= m.rows() {
        return Err(axis_out_of_bounds(r, 0, m.rows(), m.cols()));
    }
    let mut out = reserve(m.cols())?;
    for c in 0..m.cols() {
        out.push(m.get_ref(r, c)?.clone());
    }
    Ok(out)
}

pub fn column<F: Field + ExactRing>(
    m: &BasicMatrix<F>,
    c: usize,
) -> Result<Vec<F>, ExactFieldError> {
    if c >= m.cols() {
        return Err(axis_out_of_bounds(0, c, m.rows(), m.cols()));
    }
    let mut out = reserve(m.rows())?;
    for r in 0..m.rows() {
        out.push(m.get_ref(r, c)?.clone());
    }
    Ok(out)
}

fn canonical_bigint_fraction(numer: &BigInt, denom: &BigInt) -> Option<(BigInt, BigInt)> {
    if denom.is_zero() {
        return None;
    }
    let g = numer.gcd(denom);
    let mut n = numer / &g;
    let mut d = denom / &g;
    if d.is_negative() {
        n = -n;
        d = -d;
    }
    if d.is_zero() {
        None
    } else {
        Some((n, d))
    }
}

pub fn widen_rational64(
    a: &BasicMatrix<Rational64>,
) -> Result<BasicMatrix<BigRational>, ExactFieldError> {
    let cols = a.cols();
    let mut data = reserve(a.as_slice().len())?;
    for (index, x) in a.as_slice().iter().enumerate() {
        let Some((n, d)) =
            canonical_bigint_fraction(&BigInt::from(*x.numer()), &BigInt::from(*x.denom()))
        else {
            return Err(ExactFieldError::NotRepresentable {
                row: index / cols.max(1),
                col: index % cols.max(1),
            });
        };
        data.push(BigRational::new(n, d));
    }
    Ok(BasicMatrix::from_row_major(a.rows(), a.cols(), data)?)
}

pub fn narrow_to_rational64(
    a: &BasicMatrix<BigRational>,
) -> Result<BasicMatrix<Rational64>, ExactFieldError> {
    let cols = a.cols();
    let mut data = reserve(a.as_slice().len())?;
    for (index, x) in a.as_slice().iter().enumerate() {
        let Some((n, d)) = canonical_bigint_fraction(x.numer(), x.denom()) else {
            return Err(ExactFieldError::NotRepresentable {
                row: index / cols.max(1),
                col: index % cols.max(1),
            });
        };
        match (n.to_i64(), d.to_i64()) {
            (Some(n), Some(d)) => data.push(Rational64::new(n, d)),
            _ => {
                return Err(ExactFieldError::NotRepresentable {
                    row: index / cols.max(1),
                    col: index % cols.max(1),
                })
            }
        }
    }
    Ok(BasicMatrix::from_row_major(a.rows(), a.cols(), data)?)
}


fn zip_entries<F, G>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
    g: G,
) -> Result<BasicMatrix<F>, ExactFieldError>
where
    F: Field + ExactRing,
    G: Fn(&F, &F) -> Result<F, crate::linear_algebra::scalars::ScalarError>,
{
    let mut data = reserve(a.as_slice().len())?;
    for (x, y) in a.as_slice().iter().zip(b.as_slice()) {
        data.push(g(x, y)?);
    }
    Ok(BasicMatrix::from_row_major(a.rows(), a.cols(), data)?)
}

pub fn add<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    require_same_shape("add", a, b)?;
    zip_entries(a, b, |x, y| x.try_add(y))
}

pub fn sub<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    require_same_shape("sub", a, b)?;
    zip_entries(a, b, |x, y| x.try_sub(y))
}

pub fn neg<F: Field + ExactRing>(m: &BasicMatrix<F>) -> Result<BasicMatrix<F>, ExactFieldError> {
    let mut data = reserve(m.as_slice().len())?;
    for x in m.as_slice() {
        data.push(x.try_neg()?);
    }
    Ok(BasicMatrix::from_row_major(m.rows(), m.cols(), data)?)
}

pub fn scale<F: Field + ExactRing>(
    m: &BasicMatrix<F>,
    s: &F,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let mut data = reserve(m.as_slice().len())?;
    for x in m.as_slice() {
        data.push(s.try_mul(x)?);
    }
    Ok(BasicMatrix::from_row_major(m.rows(), m.cols(), data)?)
}

pub fn transpose<F: Field + ExactRing>(
    m: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    Ok(m.try_transpose()?)
}

pub fn trace<F: Field + ExactRing>(m: &BasicMatrix<F>) -> Result<F, ExactFieldError> {
    let n = require_square("trace", m)?;
    let mut acc = F::zero();
    for i in 0..n {
        acc = acc.try_add(m.get_ref(i, i)?)?;
    }
    Ok(acc)
}

pub fn dot<F: Field + ExactRing>(u: &[F], v: &[F]) -> Result<F, ExactFieldError> {
    if u.len() != v.len() {
        return Err(ExactFieldError::VectorLength {
            operation: "dot",
            expected: u.len(),
            got: v.len(),
        });
    }
    let mut acc = F::zero();
    for (x, y) in u.iter().zip(v) {
        acc = acc.try_add(&x.try_mul(y)?)?;
    }
    Ok(acc)
}


fn multiply_slices<F: Field + ExactRing>(
    a: &[F],
    m: usize,
    k: usize,
    b: &[F],
    n: usize,
) -> Result<Vec<F>, ExactFieldError> {
    let len = element_count(m, n)?;
    let mut out: Vec<F> = reserve(len)?;
    out.resize(len, F::zero());
    for i in 0..m {
        for inner in 0..k {
            let a_ik = &a[i * k + inner];
            if a_ik.try_is_zero()? {
                continue;
            }
            for j in 0..n {
                let term = a_ik.try_mul(&b[inner * n + j])?;
                let updated = out[i * n + j].try_add(&term)?;
                out[i * n + j] = updated;
            }
        }
    }
    Ok(out)
}

pub fn multiply<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    multiply_with_limits(a, b, OperationLimits::UNLIMITED)
}

pub fn multiply_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    if a.cols() != b.rows() {
        return Err(ExactFieldError::ShapeMismatch {
            operation: "multiply",
            left: a.shape(),
            right: b.shape(),
        });
    }
    let elements = element_count(a.rows(), b.cols())?;
    charge(limits, elements, times(times(2, elements)?, a.cols())?)?;
    let data = multiply_slices(a.as_slice(), a.rows(), a.cols(), b.as_slice(), b.cols())?;
    Ok(BasicMatrix::from_row_major(a.rows(), b.cols(), data)?)
}

pub fn multiply_vector<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    v: &[F],
) -> Result<Vec<F>, ExactFieldError> {
    multiply_vector_with_limits(a, v, OperationLimits::UNLIMITED)
}

pub fn multiply_vector_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    v: &[F],
    limits: OperationLimits,
) -> Result<Vec<F>, ExactFieldError> {
    if v.len() != a.cols() {
        return Err(ExactFieldError::VectorLength {
            operation: "multiply_vector",
            expected: a.cols(),
            got: v.len(),
        });
    }
    charge(limits, a.rows(), times(times(2, a.rows())?, a.cols())?)?;
    multiply_slices(a.as_slice(), a.rows(), a.cols(), v, 1)
}

pub fn kronecker<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    kronecker_with_limits(a, b, OperationLimits::UNLIMITED)
}

pub fn kronecker_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let (m, n) = a.shape();
    let (p, q) = b.shape();
    let out_rows = m
        .checked_mul(p)
        .ok_or(MatrixError::DimensionOverflow { rows: m, cols: p })?;
    let out_cols = n
        .checked_mul(q)
        .ok_or(MatrixError::DimensionOverflow { rows: n, cols: q })?;
    let elements = element_count(out_rows, out_cols)?;
    charge(limits, elements, elements)?;
    BasicMatrix::try_from_fn_result_with_limit(out_rows, out_cols, limits.max_elements, |r, c| {
        let (i, k) = (r / p, r % p);
        let (j, l) = (c / q, c % q);
        Ok(a.get_ref(i, j)?.try_mul(b.get_ref(k, l)?)?)
    })
}

pub fn commutator<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    require_operator_pair("commutator", a, b)?;
    sub(&multiply(a, b)?, &multiply(b, a)?)
}

pub fn anticommutator<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    require_operator_pair("anticommutator", a, b)?;
    add(&multiply(a, b)?, &multiply(b, a)?)
}

pub fn commutes<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<bool, ExactFieldError> {
    require_operator_pair("commutes", a, b)?;
    Ok(multiply(a, b)? == multiply(b, a)?)
}

fn require_operator_pair<F>(
    operation: &'static str,
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<(), ExactFieldError> {
    require_square(operation, a)?;
    require_square(operation, b)?;
    require_same_shape(operation, a, b)
}

pub fn power<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    exponent: u64,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    power_with_limits(a, exponent, OperationLimits::UNLIMITED)
}

pub fn power_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    exponent: u64,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let n = require_square("power", a)?;
    let elements = element_count(n, n)?;
    let bits = usize::try_from(u64::BITS - exponent.leading_zeros())
        .map_err(|_| MatrixError::OperationCountOverflow)?;
    let per_product = times(2, times(elements, n)?)?;
    charge(limits, elements, times(times(2, bits)?, per_product)?)?;

    let mut result: Vec<F> = reserve(elements)?;
    for r in 0..n {
        for c in 0..n {
            result.push(if r == c { F::one() } else { F::zero() });
        }
    }
    let mut base: Vec<F> = reserve(elements)?;
    base.extend_from_slice(a.as_slice());
    let mut remaining = exponent;
    while remaining > 0 {
        if remaining & 1 == 1 {
            result = multiply_slices(&result, n, n, &base, n)?;
        }
        remaining >>= 1;
        if remaining > 0 {
            base = multiply_slices(&base, n, n, &base, n)?;
        }
    }
    Ok(BasicMatrix::from_row_major(n, n, result)?)
}


pub fn block_diagonal<F: Field + ExactRing>(
    blocks: &[BasicMatrix<F>],
) -> Result<BasicMatrix<F>, ExactFieldError> {
    block_diagonal_with_limits(blocks, OperationLimits::UNLIMITED)
}

pub fn block_diagonal_with_limits<F: Field + ExactRing>(
    blocks: &[BasicMatrix<F>],
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let (mut rows, mut cols) = (0usize, 0usize);
    for block in blocks {
        rows = rows
            .checked_add(block.rows())
            .ok_or(MatrixError::DimensionOverflow {
                rows,
                cols: block.rows(),
            })?;
        cols = cols
            .checked_add(block.cols())
            .ok_or(MatrixError::DimensionOverflow {
                rows: cols,
                cols: block.cols(),
            })?;
    }
    let elements = element_count(rows, cols)?;
    charge(limits, elements, 0)?;
    let mut out: Vec<F> = reserve(elements)?;
    out.resize(elements, F::zero());
    let (mut row_offset, mut col_offset) = (0usize, 0usize);
    for block in blocks {
        let (block_rows, block_cols) = block.shape();
        for r in 0..block_rows {
            for c in 0..block_cols {
                out[(row_offset + r) * cols + col_offset + c] =
                    block.as_slice()[r * block_cols + c].clone();
            }
        }
        row_offset += block_rows;
        col_offset += block_cols;
    }
    Ok(BasicMatrix::from_row_major(rows, cols, out)?)
}

pub fn direct_sum<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    block_diagonal(&[a.clone(), b.clone()])
}

pub fn hstack<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    if a.rows() != b.rows() {
        return Err(ExactFieldError::ShapeMismatch {
            operation: "hstack",
            left: a.shape(),
            right: b.shape(),
        });
    }
    let cols = plus_dimension(a.cols(), b.cols())?;
    BasicMatrix::try_from_fn_result(a.rows(), cols, |r, c| {
        Ok(if c < a.cols() {
            a.get_ref(r, c)?.clone()
        } else {
            b.get_ref(r, c - a.cols())?.clone()
        })
    })
}

pub fn vstack<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    b: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    if a.cols() != b.cols() {
        return Err(ExactFieldError::ShapeMismatch {
            operation: "vstack",
            left: a.shape(),
            right: b.shape(),
        });
    }
    let rows = plus_dimension(a.rows(), b.rows())?;
    BasicMatrix::try_from_fn_result(rows, a.cols(), |r, c| {
        Ok(if r < a.rows() {
            a.get_ref(r, c)?.clone()
        } else {
            b.get_ref(r - a.rows(), c)?.clone()
        })
    })
}

fn plus_dimension(a: usize, b: usize) -> Result<usize, ExactFieldError> {
    plus(a, b).map_err(|_| MatrixError::DimensionOverflow { rows: a, cols: b }.into())
}


pub fn is_zero_matrix<F: Field + ExactRing>(m: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    let mut zero = true;
    for value in m.as_slice() {
        zero &= value.try_is_zero()?;
    }
    Ok(zero)
}

pub fn is_scalar_matrix<F: Field + ExactRing>(m: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    let n = require_square("is_scalar_matrix", m)?;
    if n == 0 {
        return Ok(true);
    }
    let diagonal = m.get_ref(0, 0)?;
    let zero = F::zero();
    for r in 0..n {
        for c in 0..n {
            let expected = if r == c { diagonal } else { &zero };
            if m.get_ref(r, c)? != expected {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

pub fn is_identity_matrix<F: Field + ExactRing>(
    m: &BasicMatrix<F>,
) -> Result<bool, ExactFieldError> {
    let n = require_square("is_identity_matrix", m)?;
    let (one, zero) = (F::one(), F::zero());
    for r in 0..n {
        for c in 0..n {
            let expected = if r == c { &one } else { &zero };
            if m.get_ref(r, c)? != expected {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

pub fn is_symmetric<F: Field + ExactRing>(m: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    let n = require_square("is_symmetric", m)?;
    for r in 0..n {
        for c in (r + 1)..n {
            if m.get_ref(r, c)? != m.get_ref(c, r)? {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::test_support::{m, q, random_matrix, Fp, Rng};
    use linear_algebra::tensor::tensor::kronecker_matrices;
    use num_bigint::BigInt;
    use num_rational::{BigRational, Rational64};

    type Q = BigRational;

    fn rat(v: &[&[i64]]) -> BasicMatrix<Q> {
        m(v)
    }

    #[test]
    fn scalar_matrix_predicate_checks_all_entries_and_refuses_rectangles() {
        assert!(is_scalar_matrix(&rat(&[&[3, 0], &[0, 3]])).unwrap());
        assert!(!is_scalar_matrix(&rat(&[&[3, 0], &[0, 4]])).unwrap());
        assert!(!is_scalar_matrix(&rat(&[&[3, 0], &[1, 3]])).unwrap());
        assert!(matches!(
            is_scalar_matrix(&rat(&[&[3, 0, 0], &[0, 3, 0]])),
            Err(ExactFieldError::NotSquare { .. })
        ));
        assert!(is_scalar_matrix(&zeros::<Q>(0, 0).unwrap()).unwrap());
        let z = crate::linear_algebra::test_support::gq(q(2, 3), q(-4, 5));
        let complex = scale(&identity(3).unwrap(), &z).unwrap();
        assert!(is_scalar_matrix(&complex).unwrap());
        let mut changed = complex;
        changed.set(0, 2, z).unwrap();
        assert!(!is_scalar_matrix(&changed).unwrap());
    }


    #[test]
    fn identity_is_the_two_sided_unit_of_multiplication() {
        let mut rng = Rng::new(11);
        let a = random_matrix(&mut rng, 3, 4, 9);
        let left = multiply(&identity::<Q>(3).unwrap(), &a).unwrap();
        let right = multiply(&a, &identity::<Q>(4).unwrap()).unwrap();
        assert_eq!(left, a);
        assert_eq!(right, a);
    }

    #[test]
    fn identity_and_zeros_of_size_zero_are_empty_matrices() {
        let i0 = identity::<Q>(0).unwrap();
        assert_eq!(i0.shape(), (0, 0));
        assert_eq!(zeros::<Q>(0, 5).unwrap().shape(), (0, 5));
        assert_eq!(zeros::<Q>(5, 0).unwrap().shape(), (5, 0));
        assert!(is_identity_matrix(&i0).unwrap());
        assert!(is_zero_matrix(&zeros::<Q>(2, 3).unwrap()).unwrap());
    }

    #[test]
    fn diagonal_places_each_entry_at_its_own_position_only() {
        let d = diagonal(&[q(2, 1), q(-3, 1), q(5, 7)]).unwrap();
        let expected = from_rows(vec![
            vec![q(2, 1), q(0, 1), q(0, 1)],
            vec![q(0, 1), q(-3, 1), q(0, 1)],
            vec![q(0, 1), q(0, 1), q(5, 7)],
        ])
        .unwrap();
        assert_eq!(d, expected);
        assert_eq!(diagonal::<Q>(&[]).unwrap().shape(), (0, 0));
    }

    #[test]
    fn from_rows_refuses_ragged_input_and_names_the_row() {
        let ragged = vec![vec![q(1, 1), q(2, 1)], vec![q(3, 1)]];
        assert_eq!(
            from_rows(ragged),
            Err(ExactFieldError::RaggedRows {
                row: 1,
                len: 1,
                expected: 2
            })
        );
        let ragged_long = vec![vec![q(1, 1)], vec![q(2, 1)], vec![q(3, 1), q(4, 1)]];
        assert_eq!(
            from_rows(ragged_long),
            Err(ExactFieldError::RaggedRows {
                row: 2,
                len: 2,
                expected: 1
            })
        );
    }

    #[test]
    fn from_rows_and_to_rows_are_inverse_including_empty_shapes() {
        let a = rat(&[&[1, 2, 3], &[4, 5, 6]]);
        assert_eq!(from_rows(to_rows(&a).unwrap()).unwrap(), a);
        assert_eq!(from_rows::<Q>(vec![]).unwrap().shape(), (0, 0));
        assert_eq!(
            from_rows::<Q>(vec![vec![], vec![], vec![]])
                .unwrap()
                .shape(),
            (3, 0)
        );
        assert_eq!(
            to_rows(&zeros::<Q>(3, 0).unwrap()).unwrap(),
            vec![Vec::<Q>::new(); 3]
        );
        let wide_empty = zeros::<Q>(0, 4).unwrap();
        assert_eq!(to_rows(&wide_empty).unwrap(), Vec::<Vec<Q>>::new());
        assert_eq!(
            from_rows(to_rows(&wide_empty).unwrap()).unwrap().shape(),
            (0, 0)
        );
    }

    #[test]
    fn an_empty_axis_still_rejects_a_missing_row_or_column() {
        let rows_only = zeros::<Q>(2, 0).unwrap();
        assert_eq!(row(&rows_only, 0).unwrap(), Vec::<Q>::new());
        assert_eq!(row(&rows_only, 1).unwrap(), Vec::<Q>::new());
        assert!(matches!(
            row(&rows_only, 2),
            Err(ExactFieldError::Matrix(MatrixError::IndexOutOfBounds {
                row: 2,
                rows: 2,
                cols: 0,
                ..
            }))
        ));
        let cols_only = zeros::<Q>(0, 2).unwrap();
        assert_eq!(column(&cols_only, 0).unwrap(), Vec::<Q>::new());
        assert_eq!(column(&cols_only, 1).unwrap(), Vec::<Q>::new());
        assert!(matches!(
            column(&cols_only, 2),
            Err(ExactFieldError::Matrix(MatrixError::IndexOutOfBounds {
                col: 2,
                rows: 0,
                cols: 2,
                ..
            }))
        ));
        let empty = zeros::<Q>(0, 0).unwrap();
        assert!(row(&empty, 0).is_err());
        assert!(column(&empty, 0).is_err());
    }

    #[test]
    fn rational_conversion_reduces_before_the_fit_check_and_rejects_a_zero_denominator() {
        let unreduced = BigRational::new_raw(BigInt::from(i64::MAX) * 2, BigInt::from(2));
        let narrowed = narrow_to_rational64(&from_rows(vec![vec![unreduced]]).unwrap()).unwrap();
        assert_eq!(narrowed.as_slice()[0], Rational64::from_integer(i64::MAX));
        let zero_denom = BigRational::new_raw(BigInt::from(1), BigInt::zero());
        assert_eq!(
            narrow_to_rational64(&from_rows(vec![vec![zero_denom]]).unwrap()),
            Err(ExactFieldError::NotRepresentable { row: 0, col: 0 })
        );
        let raw = BasicMatrix::from_row_major(1, 1, vec![Rational64::new_raw(1, 0)]).unwrap();
        assert_eq!(
            widen_rational64(&raw),
            Err(ExactFieldError::NotRepresentable { row: 0, col: 0 })
        );
    }

    #[test]
    fn from_fn_is_row_major_and_respects_the_budget() {
        let a = from_fn(2, 3, |r, c| q((10 * r + c) as i64, 1)).unwrap();
        assert_eq!(a, rat(&[&[0, 1, 2], &[10, 11, 12]]));

        let mut calls = 0;
        let refused = from_fn_with_limits(
            2,
            3,
            OperationLimits {
                max_elements: 5,
                max_scalar_ops: usize::MAX,
            },
            |_, _| {
                calls += 1;
                q(0, 1)
            },
        );
        assert_eq!(
            refused,
            Err(ExactFieldError::Matrix(
                MatrixError::AllocationLimitExceeded {
                    requested: 6,
                    limit: 5
                }
            ))
        );
        assert_eq!(calls, 0);
    }

    #[test]
    fn element_budget_boundary_is_inclusive() {
        let at_limit = OperationLimits {
            max_elements: 9,
            max_scalar_ops: usize::MAX,
        };
        assert!(identity_with_limits::<Q>(3, at_limit).is_ok());
        assert!(zeros_with_limits::<Q>(3, 3, at_limit).is_ok());
        assert_eq!(
            identity_with_limits::<Q>(4, at_limit),
            Err(ExactFieldError::Matrix(
                MatrixError::AllocationLimitExceeded {
                    requested: 16,
                    limit: 9
                }
            ))
        );
    }

    #[test]
    fn dimension_overflow_is_a_typed_error_not_a_panic() {
        assert_eq!(
            zeros::<Q>(usize::MAX, 2),
            Err(ExactFieldError::Matrix(MatrixError::DimensionOverflow {
                rows: usize::MAX,
                cols: 2
            }))
        );
    }

    #[test]
    fn row_and_column_extract_entries_and_refuse_out_of_range() {
        let a = rat(&[&[1, 2, 3], &[4, 5, 6]]);
        assert_eq!(row(&a, 1).unwrap(), vec![q(4, 1), q(5, 1), q(6, 1)]);
        assert_eq!(column(&a, 2).unwrap(), vec![q(3, 1), q(6, 1)]);
        assert!(matches!(
            row(&a, 2),
            Err(ExactFieldError::Matrix(
                MatrixError::IndexOutOfBounds { .. }
            ))
        ));
        assert!(matches!(
            column(&a, 3),
            Err(ExactFieldError::Matrix(
                MatrixError::IndexOutOfBounds { .. }
            ))
        ));
    }

    #[test]
    fn rational64_conversions_round_trip_and_refuse_overflow() {
        let small = BasicMatrix::from_row_major(
            2,
            2,
            vec![
                Rational64::new(1, 2),
                Rational64::new(-3, 7),
                Rational64::new(i64::MIN, 1),
                Rational64::new(5, i64::MAX),
            ],
        )
        .unwrap();
        let wide = widen_rational64(&small).unwrap();
        assert_eq!(
            wide.get(1, 0).unwrap(),
            BigRational::from_integer(BigInt::from(i64::MIN))
        );
        assert_eq!(narrow_to_rational64(&wide).unwrap(), small);

        let huge = BigRational::from_integer(BigInt::from(i64::MAX) + BigInt::from(1));
        let too_big = from_rows(vec![vec![q(1, 1), q(2, 1)], vec![q(3, 1), huge]]).unwrap();
        assert_eq!(
            narrow_to_rational64(&too_big),
            Err(ExactFieldError::NotRepresentable { row: 1, col: 1 })
        );
        let huge = BigRational::from_integer(BigInt::from(i64::MAX) + BigInt::from(1));
        let wide = from_rows(vec![
            vec![q(1, 1), q(2, 1), q(3, 1)],
            vec![huge.clone(), q(5, 1), q(6, 1)],
        ])
        .unwrap();
        assert_eq!(
            narrow_to_rational64(&wide),
            Err(ExactFieldError::NotRepresentable { row: 1, col: 0 })
        );
        let wide_last = from_rows(vec![
            vec![q(1, 1), q(2, 1), huge],
            vec![q(4, 1), q(5, 1), q(6, 1)],
        ])
        .unwrap();
        assert_eq!(
            narrow_to_rational64(&wide_last),
            Err(ExactFieldError::NotRepresentable { row: 0, col: 2 })
        );
        let tiny = BigRational::new(BigInt::from(1), BigInt::from(i64::MAX) + BigInt::from(2));
        assert_eq!(
            narrow_to_rational64(&from_rows(vec![vec![tiny]]).unwrap()),
            Err(ExactFieldError::NotRepresentable { row: 0, col: 0 })
        );
        assert_eq!(
            narrow_to_rational64(&zeros::<Q>(0, 0).unwrap())
                .unwrap()
                .shape(),
            (0, 0)
        );
    }


    #[test]
    fn subtraction_has_the_documented_orientation() {
        let a = rat(&[&[1, 2], &[3, 4]]);
        let b = rat(&[&[4, 3], &[2, 1]]);
        assert_eq!(sub(&a, &b).unwrap(), rat(&[&[-3, -1], &[1, 3]]));
        assert_eq!(add(&a, &b).unwrap(), rat(&[&[5, 5], &[5, 5]]));
    }

    #[test]
    fn additive_group_and_scalar_laws_hold() {
        let mut rng = Rng::new(3);
        let a = random_matrix(&mut rng, 3, 3, 7);
        let b = random_matrix(&mut rng, 3, 3, 7);
        let s = q(-5, 3);
        assert_eq!(add(&a, &b).unwrap(), add(&b, &a).unwrap());
        assert!(is_zero_matrix(&sub(&a, &a).unwrap()).unwrap());
        assert!(is_zero_matrix(&add(&a, &neg(&a).unwrap()).unwrap()).unwrap());
        assert_eq!(
            scale(&add(&a, &b).unwrap(), &s).unwrap(),
            add(&scale(&a, &s).unwrap(), &scale(&b, &s).unwrap()).unwrap()
        );
        assert_eq!(scale(&a, &q(-1, 1)).unwrap(), neg(&a).unwrap());
    }

    #[test]
    fn add_and_sub_refuse_unequal_shapes() {
        let a = zeros::<Q>(2, 2).unwrap();
        let b = zeros::<Q>(2, 3).unwrap();
        let expected = ExactFieldError::ShapeMismatch {
            operation: "add",
            left: (2, 2),
            right: (2, 3),
        };
        assert_eq!(add(&a, &b), Err(expected));
        assert!(matches!(
            sub(&a, &b),
            Err(ExactFieldError::ShapeMismatch {
                operation: "sub",
                ..
            })
        ));
    }


    #[test]
    fn multiplication_matches_hand_computed_products() {
        let a = rat(&[&[1, 2], &[3, 4]]);
        let b = rat(&[&[5, 6], &[7, 8]]);
        assert_eq!(multiply(&a, &b).unwrap(), rat(&[&[19, 22], &[43, 50]]));
        assert_eq!(multiply(&b, &a).unwrap(), rat(&[&[23, 34], &[31, 46]]));
        let r = rat(&[&[1, 0, 2], &[0, 1, 3]]);
        let s = rat(&[&[1, 1], &[2, 0], &[0, 5]]);
        assert_eq!(multiply(&r, &s).unwrap(), rat(&[&[1, 11], &[2, 15]]));
        assert_eq!(multiply(&s, &r).unwrap().shape(), (3, 3));
    }

    #[test]
    fn multiplication_is_associative_and_distributive_and_agrees_with_the_std_ops_product() {
        let mut rng = Rng::new(5);
        let a = random_matrix(&mut rng, 3, 4, 6);
        let b = random_matrix(&mut rng, 4, 2, 6);
        let c = random_matrix(&mut rng, 2, 5, 6);
        let d = random_matrix(&mut rng, 4, 2, 6);
        let ab_c = multiply(&multiply(&a, &b).unwrap(), &c).unwrap();
        let a_bc = multiply(&a, &multiply(&b, &c).unwrap()).unwrap();
        assert_eq!(ab_c, a_bc);
        assert_eq!(
            multiply(&a, &add(&b, &d).unwrap()).unwrap(),
            add(&multiply(&a, &b).unwrap(), &multiply(&a, &d).unwrap()).unwrap()
        );
        assert_eq!(multiply(&a, &b).unwrap(), a.mul(&b).unwrap().unwrap());
    }

    #[test]
    fn multiplication_refuses_inner_dimension_mismatch() {
        let a = zeros::<Q>(2, 3).unwrap();
        let b = zeros::<Q>(2, 3).unwrap();
        assert_eq!(
            multiply(&a, &b),
            Err(ExactFieldError::ShapeMismatch {
                operation: "multiply",
                left: (2, 3),
                right: (2, 3)
            })
        );
    }

    #[test]
    fn multiply_budget_charges_two_ops_per_inner_product_term() {
        let a = rat(&[&[1, 2], &[3, 4]]);
        let exact = OperationLimits {
            max_elements: 4,
            max_scalar_ops: 16,
        };
        assert!(multiply_with_limits(&a, &a, exact).is_ok());
        let tight = OperationLimits {
            max_scalar_ops: 15,
            ..exact
        };
        assert_eq!(
            multiply_with_limits(&a, &a, tight),
            Err(ExactFieldError::Matrix(
                MatrixError::OperationLimitExceeded {
                    requested: 16,
                    limit: 15
                }
            ))
        );
    }

    #[test]
    fn matrix_vector_and_kronecker_budgets_charge_their_documented_costs() {
        let a = rat(&[&[1, 2, 3], &[4, 5, 6]]);
        let v = vec![q(1, 1), q(1, 1), q(1, 1)];
        let exact = OperationLimits {
            max_elements: 2,
            max_scalar_ops: 12,
        };
        assert_eq!(
            multiply_vector_with_limits(&a, &v, exact).unwrap(),
            vec![q(6, 1), q(15, 1)]
        );
        assert_eq!(
            multiply_vector_with_limits(
                &a,
                &v,
                OperationLimits {
                    max_scalar_ops: 11,
                    ..exact
                }
            ),
            Err(ExactFieldError::Matrix(
                MatrixError::OperationLimitExceeded {
                    requested: 12,
                    limit: 11
                }
            ))
        );
        assert!(matches!(
            multiply_vector_with_limits(
                &a,
                &v,
                OperationLimits {
                    max_elements: 1,
                    ..exact
                }
            ),
            Err(ExactFieldError::Matrix(
                MatrixError::AllocationLimitExceeded {
                    requested: 2,
                    limit: 1
                }
            ))
        ));

        let i3 = identity::<Q>(3).unwrap();
        let kron_exact = OperationLimits {
            max_elements: 81,
            max_scalar_ops: 81,
        };
        assert!(kronecker_with_limits(&i3, &i3, kron_exact).is_ok());
        assert_eq!(
            kronecker_with_limits(
                &i3,
                &i3,
                OperationLimits {
                    max_scalar_ops: 80,
                    ..kron_exact
                }
            ),
            Err(ExactFieldError::Matrix(
                MatrixError::OperationLimitExceeded {
                    requested: 81,
                    limit: 80
                }
            ))
        );
    }

    #[test]
    fn multiply_vector_agrees_with_a_column_matrix_product() {
        let a = rat(&[&[1, 2, 3], &[4, 5, 6]]);
        let v = vec![q(1, 1), q(0, 1), q(-2, 1)];
        let as_column = from_rows(v.iter().map(|x| vec![x.clone()]).collect()).unwrap();
        let product = multiply(&a, &as_column).unwrap();
        assert_eq!(
            multiply_vector(&a, &v).unwrap(),
            column(&product, 0).unwrap()
        );
        assert_eq!(multiply_vector(&a, &v).unwrap(), vec![q(-5, 1), q(-8, 1)]);
        assert_eq!(
            multiply_vector(&a, &v[..2]),
            Err(ExactFieldError::VectorLength {
                operation: "multiply_vector",
                expected: 3,
                got: 2
            })
        );
    }

    #[test]
    fn transpose_reverses_the_order_of_a_product() {
        let mut rng = Rng::new(17);
        let a = random_matrix(&mut rng, 2, 3, 5);
        let b = random_matrix(&mut rng, 3, 4, 5);
        let lhs = transpose(&multiply(&a, &b).unwrap()).unwrap();
        let rhs = multiply(&transpose(&b).unwrap(), &transpose(&a).unwrap()).unwrap();
        assert_eq!(lhs, rhs);
        assert_eq!(transpose(&transpose(&a).unwrap()).unwrap(), a);
    }

    #[test]
    fn trace_is_cyclic_and_needs_a_square_matrix() {
        let mut rng = Rng::new(23);
        let a = random_matrix(&mut rng, 2, 3, 5);
        let b = random_matrix(&mut rng, 3, 2, 5);
        assert_eq!(
            trace(&multiply(&a, &b).unwrap()).unwrap(),
            trace(&multiply(&b, &a).unwrap()).unwrap()
        );
        assert_eq!(trace(&rat(&[&[1, 9], &[8, 4]])).unwrap(), q(5, 1));
        assert_eq!(
            trace(&a),
            Err(ExactFieldError::NotSquare {
                operation: "trace",
                rows: 2,
                cols: 3
            })
        );
    }

    #[test]
    fn dot_is_the_bilinear_sum_and_checks_lengths() {
        let u = vec![q(1, 2), q(3, 1)];
        let v = vec![q(4, 1), q(-1, 3)];
        assert_eq!(dot(&u, &v).unwrap(), q(1, 1));
        assert!(matches!(
            dot(&u, &v[..1]),
            Err(ExactFieldError::VectorLength {
                operation: "dot",
                ..
            })
        ));
    }


    #[test]
    fn kronecker_entries_follow_the_block_definition() {
        let mut rng = Rng::new(31);
        let a = random_matrix(&mut rng, 2, 3, 4);
        let b = random_matrix(&mut rng, 3, 2, 4);
        let k = kronecker(&a, &b).unwrap();
        assert_eq!(k.shape(), (6, 6));
        for i in 0..2 {
            for j in 0..3 {
                for r in 0..3 {
                    for s in 0..2 {
                        let expected = a.get(i, j).unwrap() * b.get(r, s).unwrap();
                        assert_eq!(k.get(i * 3 + r, j * 2 + s).unwrap(), expected);
                    }
                }
            }
        }
    }

    #[test]
    fn kronecker_satisfies_the_mixed_product_law() {
        let mut rng = Rng::new(37);
        let a = random_matrix(&mut rng, 2, 3, 4);
        let b = random_matrix(&mut rng, 3, 2, 4);
        let c = random_matrix(&mut rng, 3, 2, 4);
        let d = random_matrix(&mut rng, 2, 3, 4);
        let lhs = multiply(&kronecker(&a, &b).unwrap(), &kronecker(&c, &d).unwrap()).unwrap();
        let rhs = kronecker(&multiply(&a, &c).unwrap(), &multiply(&b, &d).unwrap()).unwrap();
        assert_eq!(lhs, rhs);
        let s = random_matrix(&mut rng, 3, 3, 4);
        let t = random_matrix(&mut rng, 2, 2, 4);
        assert_eq!(
            trace(&kronecker(&s, &t).unwrap()).unwrap(),
            trace(&s).unwrap() * trace(&t).unwrap()
        );
    }

    #[test]
    fn kronecker_agrees_with_the_tensor_module_product() {
        let mut rng = Rng::new(41);
        let a = random_matrix(&mut rng, 2, 3, 5);
        let b = random_matrix(&mut rng, 4, 2, 5);
        assert_eq!(
            kronecker(&a, &b).unwrap(),
            kronecker_matrices(&a, &b).unwrap()
        );
    }

    #[test]
    fn kronecker_with_a_zero_sized_factor_is_empty_and_budget_refuses_large_output() {
        let empty = zeros::<Q>(0, 2).unwrap();
        let b = identity::<Q>(3).unwrap();
        assert_eq!(kronecker(&empty, &b).unwrap().shape(), (0, 6));
        let big = identity::<Q>(3).unwrap();
        let refused = kronecker_with_limits(
            &big,
            &big,
            OperationLimits {
                max_elements: 80,
                max_scalar_ops: usize::MAX,
            },
        );
        assert_eq!(
            refused,
            Err(ExactFieldError::Matrix(
                MatrixError::AllocationLimitExceeded {
                    requested: 81,
                    limit: 80
                }
            ))
        );
    }

    #[test]
    fn kronecker_output_dimension_overflow_is_refused() {
        let wide = zeros::<Q>(0, usize::MAX).unwrap();
        let two = zeros::<Q>(0, 2).unwrap();
        assert_eq!(
            kronecker(&wide, &two),
            Err(ExactFieldError::Matrix(MatrixError::DimensionOverflow {
                rows: usize::MAX,
                cols: 2
            }))
        );
    }


    #[test]
    fn commutator_has_the_lie_bracket_properties() {
        let e12 = rat(&[&[0, 1], &[0, 0]]);
        let e21 = rat(&[&[0, 0], &[1, 0]]);
        assert_eq!(commutator(&e12, &e21).unwrap(), rat(&[&[1, 0], &[0, -1]]));

        let mut rng = Rng::new(43);
        let a = random_matrix(&mut rng, 3, 3, 4);
        let b = random_matrix(&mut rng, 3, 3, 4);
        let c = random_matrix(&mut rng, 3, 3, 4);
        assert_eq!(
            commutator(&a, &b).unwrap(),
            neg(&commutator(&b, &a).unwrap()).unwrap()
        );
        assert!(trace(&commutator(&a, &b).unwrap()).unwrap() == q(0, 1));
        let jacobi = add(
            &add(
                &commutator(&a, &commutator(&b, &c).unwrap()).unwrap(),
                &commutator(&b, &commutator(&c, &a).unwrap()).unwrap(),
            )
            .unwrap(),
            &commutator(&c, &commutator(&a, &b).unwrap()).unwrap(),
        )
        .unwrap();
        assert!(is_zero_matrix(&jacobi).unwrap());
    }

    #[test]
    fn anticommutator_is_symmetric_and_completes_the_product_identity() {
        let mut rng = Rng::new(47);
        let a = random_matrix(&mut rng, 3, 3, 4);
        let b = random_matrix(&mut rng, 3, 3, 4);
        assert_eq!(
            anticommutator(&a, &b).unwrap(),
            anticommutator(&b, &a).unwrap()
        );
        let two_ab = scale(&multiply(&a, &b).unwrap(), &q(2, 1)).unwrap();
        assert_eq!(
            add(
                &commutator(&a, &b).unwrap(),
                &anticommutator(&a, &b).unwrap()
            )
            .unwrap(),
            two_ab
        );
        assert!(matches!(
            commutator(&zeros::<Q>(2, 3).unwrap(), &zeros::<Q>(2, 3).unwrap()),
            Err(ExactFieldError::NotSquare {
                operation: "commutator",
                ..
            })
        ));
        assert!(matches!(
            anticommutator(&identity::<Q>(2).unwrap(), &identity::<Q>(3).unwrap()),
            Err(ExactFieldError::ShapeMismatch {
                operation: "anticommutator",
                ..
            })
        ));
    }

    #[test]
    fn commutes_decides_the_vanishing_of_the_commutator() {
        let d1 = rat(&[&[1, 0], &[0, 2]]);
        let d2 = rat(&[&[3, 0], &[0, 5]]);
        assert!(commutes(&d1, &d2).unwrap());
        let e12 = rat(&[&[0, 1], &[0, 0]]);
        let e21 = rat(&[&[0, 0], &[1, 0]]);
        assert!(!commutes(&e12, &e21).unwrap());
        let mut rng = Rng::new(61);
        let a = random_matrix(&mut rng, 3, 3, 4);
        assert!(commutes(&a, &a).unwrap());
        assert!(commutes(&a, &identity::<Q>(3).unwrap()).unwrap());
        assert!(matches!(
            commutes(&a, &identity::<Q>(2).unwrap()),
            Err(ExactFieldError::ShapeMismatch {
                operation: "commutes",
                ..
            })
        ));
    }


    #[test]
    fn power_equals_repeated_multiplication_for_small_exponents() {
        let mut rng = Rng::new(53);
        let a = random_matrix(&mut rng, 3, 3, 3);
        let mut expected = identity::<Q>(3).unwrap();
        for e in 0..=13u64 {
            assert_eq!(power(&a, e).unwrap(), expected, "exponent {e}");
            expected = multiply(&expected, &a).unwrap();
        }
    }

    #[test]
    fn power_zero_is_the_identity_even_for_the_zero_matrix_and_powers_add() {
        let z = zeros::<Q>(3, 3).unwrap();
        assert!(is_identity_matrix(&power(&z, 0).unwrap()).unwrap());
        assert!(is_zero_matrix(&power(&z, 5).unwrap()).unwrap());
        let mut rng = Rng::new(59);
        let a = random_matrix(&mut rng, 2, 2, 3);
        assert_eq!(
            multiply(&power(&a, 9).unwrap(), &power(&a, 14).unwrap()).unwrap(),
            power(&a, 23).unwrap()
        );
    }

    #[test]
    fn power_reproduces_fibonacci_numbers_beyond_f64_precision() {
        let fib = rat(&[&[1, 1], &[1, 0]]);
        let p = power(&fib, 90).unwrap();
        let big = |s: &str| -> Q { Q::from_integer(s.parse::<num_bigint::BigInt>().unwrap()) };
        assert_eq!(p.get(0, 0).unwrap(), big("4660046610375530309"));
        assert_eq!(p.get(0, 1).unwrap(), big("2880067194370816120"));
        assert_eq!(p.get(1, 0).unwrap(), big("2880067194370816120"));
        assert_eq!(p.get(1, 1).unwrap(), big("1779979416004714189"));
    }

    #[test]
    fn power_handles_the_largest_exponent_by_periodicity() {
        let p = rat(&[&[0, 1, 0], &[0, 0, 1], &[1, 0, 0]]);
        assert_eq!(u64::MAX % 3, 0);
        assert!(is_identity_matrix(&power(&p, u64::MAX).unwrap()).unwrap());
        assert_eq!(power(&p, u64::MAX - 1).unwrap(), power(&p, 2).unwrap());
    }

    #[test]
    fn power_refuses_non_square_input_and_unaffordable_work() {
        assert!(matches!(
            power(&zeros::<Q>(2, 3).unwrap(), 2),
            Err(ExactFieldError::NotSquare {
                operation: "power",
                ..
            })
        ));
        let a = identity::<Q>(4).unwrap();
        let exact = OperationLimits {
            max_elements: 16,
            max_scalar_ops: 6 * 128,
        };
        assert!(power_with_limits(&a, 5, exact).is_ok());
        let tight = OperationLimits {
            max_scalar_ops: 6 * 128 - 1,
            ..exact
        };
        assert!(matches!(
            power_with_limits(&a, 5, tight),
            Err(ExactFieldError::Matrix(
                MatrixError::OperationLimitExceeded { .. }
            ))
        ));
    }


    #[test]
    fn block_diagonal_places_rectangular_blocks_and_zero_fills_the_rest() {
        let a = rat(&[&[1, 2]]);
        let b = rat(&[&[3], &[4]]);
        let d = direct_sum(&a, &b).unwrap();
        assert_eq!(d, rat(&[&[1, 2, 0], &[0, 0, 3], &[0, 0, 4]]));
        let many = block_diagonal(&[a.clone(), b.clone(), identity::<Q>(1).unwrap()]).unwrap();
        assert_eq!(many.shape(), (4, 4));
        assert_eq!(many.get(3, 3).unwrap(), q(1, 1));
        assert_eq!(block_diagonal::<Q>(&[]).unwrap().shape(), (0, 0));
        let refused = block_diagonal_with_limits(
            &[a, b],
            OperationLimits {
                max_elements: 8,
                max_scalar_ops: usize::MAX,
            },
        );
        assert!(matches!(
            refused,
            Err(ExactFieldError::Matrix(
                MatrixError::AllocationLimitExceeded {
                    requested: 9,
                    limit: 8
                }
            ))
        ));
    }

    #[test]
    fn stacking_concatenates_and_checks_shapes() {
        let a = rat(&[&[1, 2], &[3, 4]]);
        let b = rat(&[&[5], &[6]]);
        assert_eq!(hstack(&a, &b).unwrap(), rat(&[&[1, 2, 5], &[3, 4, 6]]));
        let c = rat(&[&[7, 8]]);
        assert_eq!(vstack(&a, &c).unwrap(), rat(&[&[1, 2], &[3, 4], &[7, 8]]));
        assert!(matches!(
            hstack(&a, &c),
            Err(ExactFieldError::ShapeMismatch {
                operation: "hstack",
                ..
            })
        ));
        assert!(matches!(
            vstack(&a, &b),
            Err(ExactFieldError::ShapeMismatch {
                operation: "vstack",
                ..
            })
        ));
    }

    #[test]
    fn predicates_answer_exactly_and_refuse_non_square_input() {
        assert!(is_symmetric(&rat(&[&[1, 2], &[2, 5]])).unwrap());
        assert!(!is_symmetric(&rat(&[&[1, 2], &[3, 5]])).unwrap());
        assert!(!is_identity_matrix(&rat(&[&[1, 0], &[0, 2]])).unwrap());
        assert!(!is_identity_matrix(&rat(&[&[1, 1], &[0, 1]])).unwrap());
        assert!(!is_zero_matrix(&rat(&[&[0, 0], &[0, 1]])).unwrap());
        assert!(matches!(
            is_symmetric(&zeros::<Q>(2, 3).unwrap()),
            Err(ExactFieldError::NotSquare {
                operation: "is_symmetric",
                ..
            })
        ));
        assert!(matches!(
            is_identity_matrix(&zeros::<Q>(3, 2).unwrap()),
            Err(ExactFieldError::NotSquare {
                operation: "is_identity_matrix",
                ..
            })
        ));
    }


    #[test]
    fn multiplication_reduces_modulo_p_over_a_prime_field() {
        type F5 = Fp<5>;
        let a = from_rows(vec![
            vec![F5::new(2), F5::new(3)],
            vec![F5::new(4), F5::new(1)],
        ])
        .unwrap();
        let expected = from_rows(vec![
            vec![F5::new(1), F5::new(4)],
            vec![F5::new(2), F5::new(3)],
        ])
        .unwrap();
        assert_eq!(multiply(&a, &a).unwrap(), expected);
        assert_eq!(power(&a, 2).unwrap(), expected);
        assert_eq!(a.mul(&a).unwrap(), expected);
    }

    #[test]
    fn a_transvection_is_an_involution_in_characteristic_two() {
        type F2 = Fp<2>;
        let t = from_rows(vec![
            vec![F2::new(1), F2::new(1)],
            vec![F2::new(0), F2::new(1)],
        ])
        .unwrap();
        assert!(is_identity_matrix(&power(&t, 2).unwrap()).unwrap());
        assert!(!is_identity_matrix(&t).unwrap());
    }
}
