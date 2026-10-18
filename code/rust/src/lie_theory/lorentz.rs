
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use omega_number_theory::rational::{ri, rq, sqrt_exact, squarefree_part, ArithmeticError};

use crate::cayley::is_special_orthogonal;
use crate::finite_order::{finite_order, FiniteOrderError};
use linear_algebra::exact_field::{elimination, matrix as mx, ExactFieldError};

use crate::QMatrix;

pub const MAX_SPACE_DIMENSION: usize = 5;
pub const MAX_POWER: u64 = 4096;
pub const MAX_CENSUS_M: usize = 64;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum LorentzError {
    #[error("the number of space dimensions must be between 1 and {MAX_SPACE_DIMENSION}, got {0}")]
    SpaceDimension(usize),
    #[error("a square matrix of size 1 + d is required, got {rows}x{cols}")]
    Shape { rows: usize, cols: usize },
    #[error("the matrix does not preserve the Minkowski form: M^T eta M != eta")]
    NotLorentz,
    #[error("the matrix has determinant -1")]
    Improper,
    #[error("the matrix reverses the direction of time (M_00 <= -1)")]
    NotOrthochronous,
    #[error("a direction needs {expected} components of unit Euclidean norm")]
    Direction { expected: usize },
    #[error("the point is not on the future hyperboloid gamma^2 - |w|^2 = 1 with gamma >= 1")]
    OffHyperboloid,
    #[error("the rapidity ratio e^eta must be positive")]
    NonPositiveRatio,
    #[error("the exponent {power} exceeds the bound {max}")]
    PowerTooLarge { power: u64, max: u64 },
    #[error("the matrix is not a rotation of space: it is not of the block form diag(1, R) with R in SO(d)")]
    NotRotation,
    #[error("the census bound m = {0} exceeds {MAX_CENSUS_M}")]
    CensusTooLarge(usize),
    #[error("the matrix is singular")]
    Singular,
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
    #[error(transparent)]
    FiniteOrder(#[from] FiniteOrderError),
    #[error(transparent)]
    Arithmetic(#[from] ArithmeticError),
}

fn check_space_dimension(d: usize) -> Result<(), LorentzError> {
    if d == 0 || d > MAX_SPACE_DIMENSION {
        return Err(LorentzError::SpaceDimension(d));
    }
    Ok(())
}

fn element(m: &QMatrix, r: usize, c: usize) -> &BigRational {
    &m.as_slice()[r * m.cols() + c]
}

fn dot(u: &[BigRational], v: &[BigRational]) -> BigRational {
    u.iter().zip(v).fold(ri(0), |acc, (a, b)| acc + a * b)
}

pub fn minkowski_form(space_dim: usize) -> Result<QMatrix, LorentzError> {
    check_space_dimension(space_dim)?;
    Ok(QMatrix::try_from_fn(space_dim + 1, space_dim + 1, |r, c| {
        if r != c {
            ri(0)
        } else if r == 0 {
            ri(1)
        } else {
            ri(-1)
        }
    })
    .map_err(ExactFieldError::from)?)
}

pub fn space_dimension(m: &QMatrix) -> Result<usize, LorentzError> {
    if m.rows() != m.cols() || m.rows() < 2 {
        return Err(LorentzError::Shape {
            rows: m.rows(),
            cols: m.cols(),
        });
    }
    check_space_dimension(m.rows() - 1)?;
    Ok(m.rows() - 1)
}

pub fn preserves_form(m: &QMatrix) -> Result<bool, LorentzError> {
    let d = space_dimension(m)?;
    let eta = minkowski_form(d)?;
    let product = mx::multiply(&mx::multiply(&mx::transpose(m)?, &eta)?, m)?;
    Ok(product == eta)
}

pub fn is_orthochronous(m: &QMatrix) -> bool {
    m.rows() > 0 && m.cols() > 0 && *element(m, 0, 0) >= ri(1)
}

pub fn check_proper_orthochronous(m: &QMatrix) -> Result<usize, LorentzError> {
    let d = space_dimension(m)?;
    if !preserves_form(m)? {
        return Err(LorentzError::NotLorentz);
    }
    if !elimination::determinant(m)?.is_one() {
        return Err(LorentzError::Improper);
    }
    if !is_orthochronous(m) {
        return Err(LorentzError::NotOrthochronous);
    }
    Ok(d)
}

pub fn boost_from_point(point: &[BigRational]) -> Result<QMatrix, LorentzError> {
    let d = point
        .len()
        .checked_sub(1)
        .ok_or(LorentzError::SpaceDimension(0))?;
    check_space_dimension(d)?;
    let gamma = &point[0];
    let w = &point[1..];
    if *gamma < ri(1) || gamma * gamma - dot(w, w) != ri(1) {
        return Err(LorentzError::OffHyperboloid);
    }
    let denominator = gamma + ri(1);
    Ok(QMatrix::try_from_fn(d + 1, d + 1, |r, c| match (r, c) {
        (0, 0) => gamma.clone(),
        (0, j) => w[j - 1].clone(),
        (i, 0) => w[i - 1].clone(),
        (i, j) => {
            let kronecker = if i == j { ri(1) } else { ri(0) };
            kronecker + &w[i - 1] * &w[j - 1] / &denominator
        }
    })
    .map_err(ExactFieldError::from)?)
}

pub fn boost(
    space_dim: usize,
    ratio: &BigRational,
    direction: &[BigRational],
) -> Result<QMatrix, LorentzError> {
    check_space_dimension(space_dim)?;
    if !ratio.is_positive() {
        return Err(LorentzError::NonPositiveRatio);
    }
    if direction.len() != space_dim || dot(direction, direction) != ri(1) {
        return Err(LorentzError::Direction {
            expected: space_dim,
        });
    }
    let inverse = BigRational::one() / ratio;
    let gamma = (ratio + &inverse) / ri(2);
    let s = (ratio - &inverse) / ri(2);
    let mut point = vec![gamma];
    point.extend(direction.iter().map(|n| &s * n));
    boost_from_point(&point)
}

pub fn boost_point(m: &QMatrix) -> Result<Vec<BigRational>, LorentzError> {
    let d = check_proper_orthochronous(m)?;
    Ok((0..=d).map(|r| element(m, r, 0).clone()).collect())
}

pub fn spatial_rotation(rotation: &QMatrix) -> Result<QMatrix, LorentzError> {
    if rotation.rows() != rotation.cols() || !is_special_orthogonal(rotation) {
        return Err(LorentzError::NotRotation);
    }
    let d = rotation.rows();
    check_space_dimension(d)?;
    Ok(QMatrix::try_from_fn(d + 1, d + 1, |r, c| match (r, c) {
        (0, 0) => ri(1),
        (0, _) | (_, 0) => ri(0),
        (i, j) => element(rotation, i - 1, j - 1).clone(),
    })
    .map_err(ExactFieldError::from)?)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RapidityPoint {
    pub m: usize,
    pub n: usize,
    pub gamma: BigRational,
    pub gamma_beta: BigRational,
}

pub fn rational_hyperbola_points(max_m: usize) -> Vec<RapidityPoint> {
    let mut points = Vec::new();
    for m in 2..=max_m {
        for n in 1..m {
            if m.gcd(&n) == 1 {
                let (mb, nb) = (BigInt::from(m), BigInt::from(n));
                let den = BigInt::from(2) * &mb * &nb;
                points.push(RapidityPoint {
                    m,
                    n,
                    gamma: BigRational::new(&mb * &mb + &nb * &nb, den.clone()),
                    gamma_beta: BigRational::new(&mb * &mb - &nb * &nb, den),
                });
            }
        }
    }
    points
}

pub fn rational_unit_vector_2d(t: &BigRational) -> [BigRational; 2] {
    let t2 = t * t;
    let den = BigRational::one() + &t2;
    [(BigRational::one() - &t2) / &den, (t + t) / den]
}

pub fn rational_unit_vector_3d(s: &BigRational, t: &BigRational) -> [BigRational; 3] {
    let q = s * s + t * t;
    let den = &q + BigRational::one();
    [
        (s + s) / &den,
        (t + t) / &den,
        (&q - BigRational::one()) / den,
    ]
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PolarDecomposition {
    pub space_dim: usize,
    pub boost: QMatrix,
    pub rotation: QMatrix,
    pub spatial_rotation: QMatrix,
}

pub fn polar_decompose(m: &QMatrix) -> Result<PolarDecomposition, LorentzError> {
    let d = check_proper_orthochronous(m)?;
    let point = boost_point(m)?;
    let boost = boost_from_point(&point)?;
    let mut inverse_point = point.clone();
    for w in inverse_point.iter_mut().skip(1) {
        *w = -w.clone();
    }
    let inverse = boost_from_point(&inverse_point)?;
    let rotation = mx::multiply(&inverse, m)?;
    let block = (0..=d).all(|i| {
        let expected = if i == 0 { ri(1) } else { ri(0) };
        *element(&rotation, 0, i) == expected && *element(&rotation, i, 0) == expected
    });
    if !block {
        return Err(LorentzError::NotLorentz);
    }
    let spatial = QMatrix::try_from_fn(d, d, |r, c| element(&rotation, r + 1, c + 1).clone())
        .map_err(ExactFieldError::from)?;
    if !is_special_orthogonal(&spatial) {
        return Err(LorentzError::NotLorentz);
    }
    Ok(PolarDecomposition {
        space_dim: d,
        boost,
        rotation,
        spatial_rotation: spatial,
    })
}

pub fn thomas_wigner_rotation(b1: &QMatrix, b2: &QMatrix) -> Result<QMatrix, LorentzError> {
    check_proper_orthochronous(b1)?;
    check_proper_orthochronous(b2)?;
    let product = mx::multiply(b1, b2)?;
    Ok(polar_decompose(&product)?.spatial_rotation)
}

pub fn composed_gamma(p1: &[BigRational], p2: &[BigRational]) -> Result<BigRational, LorentzError> {
    if p1.len() != p2.len() || p1.len() < 2 {
        return Err(LorentzError::OffHyperboloid);
    }
    Ok(&p1[0] * &p2[0] + dot(&p1[1..], &p2[1..]))
}

pub fn wigner_cosine_closed_form(
    gamma1: &BigRational,
    gamma2: &BigRational,
    gamma: &BigRational,
) -> BigRational {
    let one = BigRational::one();
    let numerator = &one + gamma + gamma1 + gamma2;
    &numerator * &numerator / ((&one + gamma) * (&one + gamma1) * (&one + gamma2)) - one
}

pub fn perpendicular_wigner_cosine(gamma1: &BigRational, gamma2: &BigRational) -> BigRational {
    (gamma1 + gamma2) / (BigRational::one() + gamma1 * gamma2)
}

pub fn rotation_cosine(r: &QMatrix) -> Result<BigRational, LorentzError> {
    if !is_special_orthogonal(r) {
        return Err(LorentzError::NotRotation);
    }
    let trace = mx::trace(r)?;
    match r.rows() {
        2 => Ok(trace / ri(2)),
        3 => Ok((trace - ri(1)) / ri(2)),
        _ => Err(LorentzError::NotRotation),
    }
}

pub fn collinear_power_entries(
    ratio: &BigRational,
    k: u64,
) -> Result<(BigRational, BigRational), LorentzError> {
    if !ratio.is_positive() {
        return Err(LorentzError::NonPositiveRatio);
    }
    if k > MAX_POWER {
        return Err(LorentzError::PowerTooLarge {
            power: k,
            max: MAX_POWER,
        });
    }
    let exponent = u32::try_from(k).map_err(|_| LorentzError::PowerTooLarge {
        power: k,
        max: MAX_POWER,
    })?;
    let (p, q) = (ratio.numer().pow(exponent), ratio.denom().pow(exponent));
    let big = BigRational::new(p, q);
    let small = BigRational::one() / &big;
    Ok(((&big + &small) / ri(2), (&big - &small) / ri(2)))
}

pub fn lorentz_power(m: &QMatrix, k: u64) -> Result<QMatrix, LorentzError> {
    if k > MAX_POWER {
        return Err(LorentzError::PowerTooLarge {
            power: k,
            max: MAX_POWER,
        });
    }
    check_proper_orthochronous(m)?;
    Ok(mx::power(m, k)?)
}

pub fn height(m: &QMatrix) -> BigInt {
    m.as_slice()
        .iter()
        .flat_map(|e| [e.numer().abs(), e.denom().abs()])
        .max()
        .unwrap_or_else(BigInt::zero)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ElementClass {
    Identity,
    Elliptic,
    Parabolic,
    Hyperbolic,
}

pub fn classify_so21(m: &QMatrix) -> Result<ElementClass, LorentzError> {
    if check_proper_orthochronous(m)? != 2 {
        return Err(LorentzError::Shape {
            rows: m.rows(),
            cols: m.cols(),
        });
    }
    if mx::is_identity_matrix(m)? {
        return Ok(ElementClass::Identity);
    }
    let trace = mx::trace(m)?;
    Ok(match trace.cmp(&ri(3)) {
        std::cmp::Ordering::Greater => ElementClass::Hyperbolic,
        std::cmp::Ordering::Equal => ElementClass::Parabolic,
        std::cmp::Ordering::Less => ElementClass::Elliptic,
    })
}

pub fn adjoint_of_gl2(g: &QMatrix) -> Result<QMatrix, LorentzError> {
    if g.shape() != (2, 2) {
        return Err(LorentzError::Shape {
            rows: g.rows(),
            cols: g.cols(),
        });
    }
    let inverse = match elimination::inverse(g) {
        Ok(inverse) => inverse,
        Err(ExactFieldError::Singular { .. }) => return Err(LorentzError::Singular),
        Err(other) => return Err(other.into()),
    };
    let units = [[[0, 1], [-1, 0]], [[1, 0], [0, -1]], [[0, 1], [1, 0]]];
    let mut columns: Vec<[BigRational; 3]> = Vec::with_capacity(3);
    for unit in units {
        let x = QMatrix::from_row_major(2, 2, unit.iter().flatten().map(|&v| ri(v)).collect())
            .map_err(ExactFieldError::from)?;
        let image = mx::multiply(&mx::multiply(g, &x)?, &inverse)?;
        let (e00, e01, e10) = (
            element(&image, 0, 0).clone(),
            element(&image, 0, 1).clone(),
            element(&image, 1, 0).clone(),
        );
        columns.push([(&e01 - &e10) / ri(2), e00, (&e01 + &e10) / ri(2)]);
    }
    Ok(QMatrix::try_from_fn(3, 3, |r, c| columns[c][r].clone()).map_err(ExactFieldError::from)?)
}

pub fn gl2_determinant_class(g: &QMatrix) -> Result<BigInt, LorentzError> {
    if g.shape() != (2, 2) {
        return Err(LorentzError::Shape {
            rows: g.rows(),
            cols: g.cols(),
        });
    }
    let det = elimination::determinant(g)?;
    if det.is_zero() {
        return Err(LorentzError::Singular);
    }
    let (class, _) = squarefree_part(&(det.numer() * det.denom()))?;
    Ok(class)
}

pub fn ratio_of(point: &RapidityPoint) -> BigRational {
    BigRational::new(BigInt::from(point.m), BigInt::from(point.n))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ThomasWignerCensus {
    pub rapidity_count: usize,
    pub direction_count: usize,
    pub pairs: usize,
    pub collinear_pairs: usize,
    pub finite_order_pairs: usize,
    pub finite_order_collinear_pairs: usize,
    pub finite_order_noncollinear_pairs: usize,
}

pub fn thomas_wigner_census(
    max_m: usize,
    directions: &[[BigRational; 2]],
) -> Result<ThomasWignerCensus, LorentzError> {
    if max_m > MAX_CENSUS_M {
        return Err(LorentzError::CensusTooLarge(max_m));
    }
    let points = rational_hyperbola_points(max_m);
    let x_axis = [ri(1), ri(0)];
    let mut census = ThomasWignerCensus {
        rapidity_count: points.len(),
        direction_count: directions.len(),
        pairs: 0,
        collinear_pairs: 0,
        finite_order_pairs: 0,
        finite_order_collinear_pairs: 0,
        finite_order_noncollinear_pairs: 0,
    };
    for p1 in &points {
        let b1 = boost(2, &ratio_of(p1), &x_axis)?;
        for p2 in &points {
            let ratio2 = ratio_of(p2);
            for direction in directions {
                let b2 = boost(2, &ratio2, direction)?;
                let rotation = thomas_wigner_rotation(&b1, &b2)?;
                let collinear = direction[1].is_zero();
                let finite = finite_order(&rotation)?.is_some();
                census.pairs += 1;
                census.collinear_pairs += usize::from(collinear);
                if finite {
                    census.finite_order_pairs += 1;
                    if collinear {
                        census.finite_order_collinear_pairs += 1;
                    } else {
                        census.finite_order_noncollinear_pairs += 1;
                    }
                }
            }
        }
    }
    Ok(census)
}

pub fn standard_plane_directions() -> [[BigRational; 2]; 5] {
    [
        [ri(1), ri(0)],
        [ri(0), ri(1)],
        [rq(3, 5), rq(4, 5)],
        [rq(5, 13), rq(12, 13)],
        [rq(7, 25), rq(24, 25)],
    ]
}

pub fn rapidity_ratio(point: &[BigRational]) -> Option<BigRational> {
    let w = point.get(1..)?;
    Some(point.first()? + sqrt_exact(&dot(w, w))?)
}
