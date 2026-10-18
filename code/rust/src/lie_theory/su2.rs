
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::scalars::{ExactRing, Field};
use num_bigint::BigInt;
use num_rational::BigRational;
use omega_number_theory::quadratic::Quadratic;
use omega_number_theory::rational::{ri, rq, sqrt_exact, squarefree_part, ArithmeticError};

use crate::cayley::is_special_orthogonal;
use crate::finite_group::{FiniteGroup, GroupError};
use linear_algebra::exact_field::{matrix as mx, ExactFieldError};

use crate::QMatrix;

pub const MAX_TWICE_SPIN: u32 = 64;
pub const MAX_COMMUTANT_SIZE: usize = 12;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum Su2Error {
    #[error("the quaternion has zero norm and no inverse")]
    NotInvertible,
    #[error("the quaternion has squared norm {0}, not 1")]
    NotUnitQuaternion(BigRational),
    #[error("the matrix is not a rotation: R^T R != I or det R != 1 (or not 3x3)")]
    NotRotation,
    #[error(
        "the rotation has spinor norm class {class}: its lifts need the square root of {class}"
    )]
    NoRationalLift { class: BigInt },
    #[error("the matrices are not all square of one size between 1 and {MAX_COMMUTANT_SIZE}")]
    Shape,
    #[error("2j = {twice_spin} exceeds the bound {MAX_TWICE_SPIN}")]
    SpinTooLarge { twice_spin: u32 },
    #[error("the quantum numbers do not satisfy 2j, 2m of one parity with |m| <= j")]
    InvalidQuantumNumber,
    #[error(transparent)]
    Arithmetic(#[from] ArithmeticError),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
    #[error(transparent)]
    Group(#[from] GroupError),
}


#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Quaternion<F> {
    pub w: F,
    pub x: F,
    pub y: F,
    pub z: F,
}

impl<F: Field + ExactRing> Quaternion<F> {
    pub fn new(w: F, x: F, y: F, z: F) -> Self {
        Self { w, x, y, z }
    }

    pub fn identity() -> Self {
        Self::new(F::one(), F::zero(), F::zero(), F::zero())
    }

    pub fn is_zero(&self) -> bool {
        self.w.is_zero() && self.x.is_zero() && self.y.is_zero() && self.z.is_zero()
    }

    pub fn add(&self, other: &Self) -> Self {
        Self::new(
            self.w.add(&other.w),
            self.x.add(&other.x),
            self.y.add(&other.y),
            self.z.add(&other.z),
        )
    }

    pub fn neg(&self) -> Self {
        Self::new(self.w.neg(), self.x.neg(), self.y.neg(), self.z.neg())
    }

    pub fn scale(&self, k: &F) -> Self {
        Self::new(
            k.mul(&self.w),
            k.mul(&self.x),
            k.mul(&self.y),
            k.mul(&self.z),
        )
    }

    pub fn mul(&self, o: &Self) -> Self {
        let (a, b) = (self, o);
        let prod = |p: &F, q: &F| p.mul(q);
        Self::new(
            prod(&a.w, &b.w)
                .sub(&prod(&a.x, &b.x))
                .sub(&prod(&a.y, &b.y))
                .sub(&prod(&a.z, &b.z)),
            prod(&a.w, &b.x)
                .add(&prod(&a.x, &b.w))
                .add(&prod(&a.y, &b.z))
                .sub(&prod(&a.z, &b.y)),
            prod(&a.w, &b.y)
                .sub(&prod(&a.x, &b.z))
                .add(&prod(&a.y, &b.w))
                .add(&prod(&a.z, &b.x)),
            prod(&a.w, &b.z)
                .add(&prod(&a.x, &b.y))
                .sub(&prod(&a.y, &b.x))
                .add(&prod(&a.z, &b.w)),
        )
    }

    pub fn conjugate(&self) -> Self {
        Self::new(self.w.clone(), self.x.neg(), self.y.neg(), self.z.neg())
    }

    pub fn norm_squared(&self) -> F {
        self.w
            .mul(&self.w)
            .add(&self.x.mul(&self.x))
            .add(&self.y.mul(&self.y))
            .add(&self.z.mul(&self.z))
    }

    pub fn inverse(&self) -> Result<Self, Su2Error> {
        let n = self.norm_squared();
        let inv = n.try_inv().ok_or(Su2Error::NotInvertible)?;
        Ok(self.conjugate().scale(&inv))
    }
}

pub fn rational_quaternion(
    w: BigRational,
    x: BigRational,
    y: BigRational,
    z: BigRational,
) -> Quaternion<BigRational> {
    Quaternion::new(w, x, y, z)
}

pub fn integer_quaternion(w: i64, x: i64, y: i64, z: i64) -> Quaternion<BigRational> {
    Quaternion::new(ri(w), ri(x), ri(y), ri(z))
}

pub fn rotation_of_quaternion<F: Field + ExactRing>(
    q: &Quaternion<F>,
) -> Result<BasicMatrix<F>, Su2Error> {
    let n = q.norm_squared();
    let inv = n.try_inv().ok_or(Su2Error::NotInvertible)?;
    let two = F::one().add(&F::one());
    let sq = |a: &F| a.mul(a);
    let (w, x, y, z) = (&q.w, &q.x, &q.y, &q.z);
    let p = |a: &F, b: &F| two.mul(&a.mul(b));
    let entries = [
        sq(w).add(&sq(x)).sub(&sq(y)).sub(&sq(z)),
        p(x, y).sub(&p(w, z)),
        p(x, z).add(&p(w, y)),
        p(x, y).add(&p(w, z)),
        sq(w).sub(&sq(x)).add(&sq(y)).sub(&sq(z)),
        p(y, z).sub(&p(w, x)),
        p(x, z).sub(&p(w, y)),
        p(y, z).add(&p(w, x)),
        sq(w).sub(&sq(x)).sub(&sq(y)).add(&sq(z)),
    ];
    let data: Vec<F> = entries.iter().map(|e| e.mul(&inv)).collect();
    BasicMatrix::from_row_major(3, 3, data).map_err(|e| Su2Error::Matrix(e.into()))
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RodriguesQuaternion {
    pub vector: [BigRational; 4],
    pub norm_class: BigInt,
}

fn squared_length(v: &[BigRational; 4]) -> BigRational {
    v.iter().map(|x| x * x).fold(ri(0), |acc, x| acc + x)
}

pub fn square_class(value: &BigRational) -> Result<BigInt, Su2Error> {
    let (class, _) = squarefree_part(&(value.numer() * value.denom()))?;
    Ok(class)
}

pub fn rodrigues_quaternion(r: &QMatrix) -> Result<RodriguesQuaternion, Su2Error> {
    if r.shape() != (3, 3) || !is_special_orthogonal(r) {
        return Err(Su2Error::NotRotation);
    }
    let e = |i: usize, j: usize| r.as_slice()[3 * i + j].clone();
    let one = ri(1);
    let columns: [[BigRational; 4]; 4] = [
        [
            &one + e(0, 0) + e(1, 1) + e(2, 2),
            e(2, 1) - e(1, 2),
            e(0, 2) - e(2, 0),
            e(1, 0) - e(0, 1),
        ],
        [
            e(2, 1) - e(1, 2),
            &one + e(0, 0) - e(1, 1) - e(2, 2),
            e(0, 1) + e(1, 0),
            e(0, 2) + e(2, 0),
        ],
        [
            e(0, 2) - e(2, 0),
            e(0, 1) + e(1, 0),
            &one - e(0, 0) + e(1, 1) - e(2, 2),
            e(1, 2) + e(2, 1),
        ],
        [
            e(1, 0) - e(0, 1),
            e(0, 2) + e(2, 0),
            e(1, 2) + e(2, 1),
            &one - e(0, 0) - e(1, 1) + e(2, 2),
        ],
    ];
    let vector = columns
        .into_iter()
        .find(|v| v.iter().any(|x| *x != ri(0)))
        .ok_or(Su2Error::NotRotation)?;
    let norm_class = square_class(&squared_length(&vector))?;
    Ok(RodriguesQuaternion { vector, norm_class })
}

pub fn spinor_norm_class(r: &QMatrix) -> Result<BigInt, Su2Error> {
    Ok(rodrigues_quaternion(r)?.norm_class)
}

pub fn spin_lift(r: &QMatrix) -> Result<Quaternion<BigRational>, Su2Error> {
    let rodrigues = rodrigues_quaternion(r)?;
    if rodrigues.norm_class != BigInt::from(1) {
        return Err(Su2Error::NoRationalLift {
            class: rodrigues.norm_class,
        });
    }
    let length = sqrt_exact(&squared_length(&rodrigues.vector)).ok_or(Su2Error::NotRotation)?;
    let [w, x, y, z] = rodrigues.vector;
    Ok(Quaternion::new(
        w / &length,
        x / &length,
        y / &length,
        z / &length,
    ))
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SpinRepresentation {
    twice_spin: u32,
    j_z: QMatrix,
    j_plus: QMatrix,
    j_minus: QMatrix,
}

impl SpinRepresentation {
    pub fn new(twice_spin: u32) -> Result<Self, Su2Error> {
        if twice_spin > MAX_TWICE_SPIN {
            return Err(Su2Error::SpinTooLarge { twice_spin });
        }
        let n = i64::from(twice_spin);
        let dimension = twice_spin as usize + 1;
        let mut j_z = mx::zeros::<BigRational>(dimension, dimension)?;
        let mut j_plus = j_z.clone();
        let mut j_minus = j_z.clone();
        for k in 0..dimension {
            let kk = k as i64;
            j_z.set(k, k, rq(n - 2 * kk, 2))
                .map_err(ExactFieldError::from)?;
            if k >= 1 {
                j_plus
                    .set(k - 1, k, ri(kk))
                    .map_err(ExactFieldError::from)?;
            }
            if k + 1 < dimension {
                j_minus
                    .set(k + 1, k, ri(n - kk))
                    .map_err(ExactFieldError::from)?;
            }
        }
        Ok(Self {
            twice_spin,
            j_z,
            j_plus,
            j_minus,
        })
    }

    pub fn twice_spin(&self) -> u32 {
        self.twice_spin
    }

    pub fn dimension(&self) -> usize {
        self.twice_spin as usize + 1
    }

    pub fn generators(&self) -> [&QMatrix; 3] {
        [&self.j_z, &self.j_plus, &self.j_minus]
    }
}

fn common_size(matrices: &[&QMatrix]) -> Result<usize, Su2Error> {
    let d = matrices.first().ok_or(Su2Error::Shape)?.rows();
    if d == 0
        || d > MAX_COMMUTANT_SIZE.max(MAX_TWICE_SPIN as usize + 1)
        || matrices.iter().any(|m| m.rows() != d || m.cols() != d)
    {
        return Err(Su2Error::Shape);
    }
    Ok(d)
}

fn commutator(a: &QMatrix, b: &QMatrix) -> Result<QMatrix, Su2Error> {
    Ok(mx::commutator(a, b)?)
}

pub fn bracket_defects(generators: [&QMatrix; 3]) -> Result<[QMatrix; 3], Su2Error> {
    common_size(&generators)?;
    let [j_z, j_plus, j_minus] = generators;
    Ok([
        mx::sub(&commutator(j_z, j_plus)?, j_plus)?,
        mx::add(&commutator(j_z, j_minus)?, j_minus)?,
        mx::sub(&commutator(j_plus, j_minus)?, &mx::scale(j_z, &ri(2))?)?,
    ])
}

pub fn casimir(generators: [&QMatrix; 3]) -> Result<QMatrix, Su2Error> {
    common_size(&generators)?;
    let [j_z, j_plus, j_minus] = generators;
    let anticommutator = mx::anticommutator(j_plus, j_minus)?;
    Ok(mx::add(
        &mx::multiply(j_z, j_z)?,
        &mx::scale(&anticommutator, &rq(1, 2))?,
    )?)
}

pub fn commutant_dimension(matrices: &[&QMatrix]) -> Result<usize, Su2Error> {
    let d = common_size(matrices)?;
    if d > MAX_COMMUTANT_SIZE {
        return Err(Su2Error::Shape);
    }
    let family = matrices.iter().map(|m| (*m).clone()).collect::<Vec<_>>();
    Ok(
        linear_algebra::exact_field::commutant::commutant_dimension_with_limits(
            d,
            &family,
            linear_algebra::backend::basic_matrix::OperationLimits {
                max_elements: 1_000_000,
                max_scalar_ops: 100_000_000,
            },
        )?,
    )
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClebschGordan {
    pub sign: i8,
    pub square: BigRational,
}

impl ClebschGordan {
    pub fn is_zero(&self) -> bool {
        self.sign == 0
    }
}

fn factorial(n: i64) -> BigInt {
    (1..=n).fold(BigInt::from(1), |acc, k| acc * k)
}

pub fn clebsch_gordan(
    twice_j1: u32,
    twice_m1: i32,
    twice_j2: u32,
    twice_m2: i32,
    twice_j: u32,
    twice_m: i32,
) -> Result<ClebschGordan, Su2Error> {
    let valid =
        |tj: u32, tm: i32| tm.unsigned_abs() <= tj && (i64::from(tj) - i64::from(tm)) % 2 == 0;
    if !(valid(twice_j1, twice_m1) && valid(twice_j2, twice_m2) && valid(twice_j, twice_m)) {
        return Err(Su2Error::InvalidQuantumNumber);
    }
    let (n1, n2, nj) = (i64::from(twice_j1), i64::from(twice_j2), i64::from(twice_j));
    let (a1, a2, am) = (i64::from(twice_m1), i64::from(twice_m2), i64::from(twice_m));
    let zero = ClebschGordan {
        sign: 0,
        square: ri(0),
    };
    if am != a1 + a2 || (n1 + n2 + nj) % 2 != 0 || nj > n1 + n2 || nj < (n1 - n2).abs() {
        return Ok(zero);
    }
    let s1 = (n1 + n2 - nj) / 2;
    let s2 = (n1 - n2 + nj) / 2;
    let s3 = (-n1 + n2 + nj) / 2;
    let s4 = (n1 + n2 + nj) / 2 + 1;
    let prefactor = BigRational::new(
        BigInt::from(nj + 1) * factorial(s1) * factorial(s2) * factorial(s3),
        factorial(s4),
    );
    let f = |v: i64| factorial(v / 2);
    let weights = f(nj + am) * f(nj - am) * f(n1 - a1) * f(n1 + a1) * f(n2 - a2) * f(n2 + a2);
    let (t1, t2, t3, t4) = (
        (n1 - a1) / 2,
        (n2 + a2) / 2,
        (nj - n2 + a1) / 2,
        (nj - n1 - a2) / 2,
    );
    let k_min = 0.max(-t3).max(-t4);
    let k_max = s1.min(t1).min(t2);
    let mut sum = ri(0);
    for k in k_min..=k_max {
        let denominator = factorial(k)
            * factorial(s1 - k)
            * factorial(t1 - k)
            * factorial(t2 - k)
            * factorial(t3 + k)
            * factorial(t4 + k);
        let term = BigRational::new(BigInt::from(1), denominator);
        if k % 2 == 0 {
            sum += term;
        } else {
            sum -= term;
        }
    }
    if sum == ri(0) {
        return Ok(zero);
    }
    let sign = if sum < ri(0) { -1 } else { 1 };
    let square = prefactor * BigRational::from_integer(weights) * &sum * &sum;
    Ok(ClebschGordan { sign, square })
}


fn quaternion_key(
    q: &Quaternion<BigRational>,
) -> (BigRational, BigRational, BigRational, BigRational) {
    (q.w.clone(), q.x.clone(), q.y.clone(), q.z.clone())
}

fn quaternion_group_from(
    generators: &[Quaternion<BigRational>],
    bound: usize,
) -> Result<FiniteGroup<Quaternion<BigRational>>, Su2Error> {
    Ok(FiniteGroup::generated(
        generators,
        Quaternion::identity(),
        |a, b| a.mul(b),
        quaternion_key,
        bound,
    )?)
}

pub fn quaternion_group() -> Result<FiniteGroup<Quaternion<BigRational>>, Su2Error> {
    quaternion_group_from(
        &[
            integer_quaternion(0, 1, 0, 0),
            integer_quaternion(0, 0, 1, 0),
        ],
        8,
    )
}

pub fn binary_tetrahedral_group() -> Result<FiniteGroup<Quaternion<BigRational>>, Su2Error> {
    let half = rq(1, 2);
    quaternion_group_from(
        &[
            integer_quaternion(0, 1, 0, 0),
            integer_quaternion(0, 0, 1, 0),
            Quaternion::new(half.clone(), half.clone(), half.clone(), half),
        ],
        24,
    )
}

pub fn binary_octahedral_group() -> Result<FiniteGroup<Quaternion<Quadratic<2>>>, Su2Error> {
    let q = |n: i64| Quadratic::<2>::from_ints(n, 0);
    let half = Quadratic::<2>::new(rq(1, 2), ri(0));
    let root_half = Quadratic::<2>::new(ri(0), rq(1, 2));
    let generators = [
        Quaternion::new(q(0), q(1), q(0), q(0)),
        Quaternion::new(q(0), q(0), q(1), q(0)),
        Quaternion::new(half.clone(), half.clone(), half.clone(), half),
        Quaternion::new(root_half.clone(), root_half, q(0), q(0)),
    ];
    Ok(FiniteGroup::generated(
        &generators,
        Quaternion::identity(),
        |a, b| a.mul(b),
        |x| x.clone(),
        48,
    )?)
}

pub fn binary_icosahedral_group() -> Result<FiniteGroup<Quaternion<Quadratic<5>>>, Su2Error> {
    let q = |n: i64| Quadratic::<5>::from_ints(n, 0);
    let half = Quadratic::<5>::new(rq(1, 2), ri(0));
    let phi = Quadratic::<5>::golden_ratio();
    let phi_conjugate = Quadratic::<5>::golden_ratio_conjugate();
    let generators = [
        Quaternion::new(half.clone(), half.clone(), half.clone(), half.clone()),
        Quaternion::new(q(0), q(1), q(0), q(0)),
        Quaternion::new(
            phi_conjugate.scale(&rq(1, 2)),
            phi.neg().scale(&rq(1, 2)),
            half,
            q(0),
        ),
    ];
    Ok(FiniteGroup::generated(
        &generators,
        Quaternion::identity(),
        |a, b| a.mul(b),
        |x| x.clone(),
        120,
    )?)
}

pub fn is_unit_quaternion<F: Field + ExactRing>(q: &Quaternion<F>) -> bool {
    q.norm_squared() == F::one()
}

pub fn same_rotation(
    a: &Quaternion<BigRational>,
    b: &Quaternion<BigRational>,
) -> Result<bool, Su2Error> {
    Ok(rotation_of_quaternion(a)? == rotation_of_quaternion(b)?)
}
