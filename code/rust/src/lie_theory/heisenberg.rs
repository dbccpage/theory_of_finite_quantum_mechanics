
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{matrix as mx, ExactFieldError};
use num_bigint::BigUint;
use omega_number_theory::rational::ri;

use crate::scalar::{dagger, ComplexField};

pub const MAX_DIMENSION: usize = 128;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum HeisenbergError {
    #[error("dimension must be in 2..={MAX_DIMENSION}, got {0}")]
    Dimension(usize),
    #[error("omega does not have the declared primitive order {0}")]
    NonPrimitiveRoot(usize),
    #[error("even dimension needs a primitive 2d-th phase root with tau^2 = omega")]
    PhaseRoot,
    #[error("the finite Stone-von Neumann census needs prime dimension, got {0}")]
    NotPrime(usize),
    #[error("the operator must be a {dimension}x{dimension} matrix")]
    Shape { dimension: usize },
    #[error("Weyl intertwiner premise failed: {0}")]
    IntertwinerPremise(&'static str),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}

fn power<F: ComplexField>(base: &F, mut n: usize) -> F {
    let mut result = F::one();
    let mut base = base.clone();
    while n != 0 {
        if n & 1 == 1 {
            result = result.mul(&base);
        }
        n >>= 1;
        if n != 0 {
            base = base.mul(&base);
        }
    }
    result
}

fn has_order<F: ComplexField>(x: &F, n: usize) -> bool {
    power(x, n) == F::one()
        && (1..n)
            .filter(|k| n % k == 0)
            .all(|k| power(x, k) != F::one())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WeylHeisenberg<F> {
    dimension: usize,
    omega: F,
    tau: F,
    label_period: usize,
}

impl<F: ComplexField> WeylHeisenberg<F> {
    pub fn new(dimension: usize, omega: F) -> Result<Self, HeisenbergError> {
        if dimension < 2 || dimension > MAX_DIMENSION {
            return Err(HeisenbergError::Dimension(dimension));
        }
        if dimension % 2 == 0 {
            return Err(HeisenbergError::PhaseRoot);
        }
        let tau = power(&omega, (dimension + 1) / 2);
        Self::with_phase_root(dimension, omega, tau)
    }

    pub fn with_phase_root(dimension: usize, omega: F, tau: F) -> Result<Self, HeisenbergError> {
        if dimension < 2 || dimension > MAX_DIMENSION {
            return Err(HeisenbergError::Dimension(dimension));
        }
        if !has_order(&omega, dimension) {
            return Err(HeisenbergError::NonPrimitiveRoot(dimension));
        }
        let label_period = if dimension % 2 == 0 {
            2 * dimension
        } else {
            dimension
        };
        if tau.mul(&tau) != omega || !has_order(&tau, label_period) {
            return Err(HeisenbergError::PhaseRoot);
        }
        Ok(Self {
            dimension,
            omega,
            tau,
            label_period,
        })
    }

    pub fn dimension(&self) -> usize {
        self.dimension
    }
    pub fn omega(&self) -> &F {
        &self.omega
    }
    pub fn phase_root(&self) -> &F {
        &self.tau
    }

    pub fn reduce(&self, a: i64, b: i64) -> (usize, usize) {
        let n = self.label_period as i64;
        (a.rem_euclid(n) as usize, b.rem_euclid(n) as usize)
    }

    pub fn shift(&self) -> Result<BasicMatrix<F>, HeisenbergError> {
        self.displacement(1, 0)
    }

    pub fn clock(&self) -> Result<BasicMatrix<F>, HeisenbergError> {
        self.displacement(0, 1)
    }

    pub fn parity(&self) -> Result<BasicMatrix<F>, HeisenbergError> {
        let d = self.dimension;
        Ok(BasicMatrix::try_from_fn_result::<_, ExactFieldError>(
            d,
            d,
            |r, c| {
                Ok(if r == (d - c) % d {
                    F::one()
                } else {
                    F::zero()
                })
            },
        )?)
    }

    pub fn displacement(&self, a: i64, b: i64) -> Result<BasicMatrix<F>, HeisenbergError> {
        let (a, b) = self.reduce(a, b);
        let phase = power(&self.tau, a * b % self.label_period);
        let d = self.dimension;
        Ok(BasicMatrix::try_from_fn_result::<_, ExactFieldError>(
            d,
            d,
            |r, c| {
                Ok(if r == (c + a) % d {
                    phase.mul(&power(&self.omega, b * c % d))
                } else {
                    F::zero()
                })
            },
        )?)
    }

    pub fn product_phase(&self, a: i64, b: i64, c: i64, e: i64) -> F {
        let (a, b) = self.reduce(a, b);
        let (c, e) = self.reduce(c, e);
        let n = self.label_period;
        power(&self.tau, (b * c + n * n - a * e) % n)
    }

    pub fn coefficient(
        &self,
        a: i64,
        b: i64,
        operator: &BasicMatrix<F>,
    ) -> Result<F, HeisenbergError> {
        if operator.shape() != (self.dimension, self.dimension) {
            return Err(HeisenbergError::Shape {
                dimension: self.dimension,
            });
        }
        let (a, b) = self.reduce(a, b);
        let phase = power(&self.tau, a * b % self.label_period);
        let mut trace = F::zero();
        for c in 0..self.dimension {
            let entry = phase.mul(&power(&self.omega, b * c % self.dimension));
            let r = (c + a) % self.dimension;
            trace = trace.add(
                &entry
                    .conjugate()
                    .mul(operator.get_ref(r, c).map_err(ExactFieldError::from)?),
            );
        }
        Ok(trace.mul(&F::from_rational(&(ri(1) / ri(self.dimension as i64)))))
    }

    pub fn reconstruct_operator(
        &self,
        operator: &BasicMatrix<F>,
    ) -> Result<BasicMatrix<F>, HeisenbergError> {
        let d = self.dimension;
        let mut result = mx::zeros::<F>(d, d)?;
        for a in 0..d {
            for b in 0..d {
                let coefficient = self.coefficient(a as i64, b as i64, operator)?;
                let phase = power(&self.tau, a * b % self.label_period);
                for c in 0..d {
                    let r = (c + a) % d;
                    let entry = coefficient.mul(&phase).mul(&power(&self.omega, b * c % d));
                    let sum = result
                        .get_ref(r, c)
                        .map_err(ExactFieldError::from)?
                        .add(&entry);
                    result.set(r, c, sum).map_err(ExactFieldError::from)?;
                }
            }
        }
        Ok(result)
    }

    pub fn displaced_parity(&self, q: i64, p: i64) -> Result<BasicMatrix<F>, HeisenbergError> {
        let d = self.dimension;
        let q = q.rem_euclid(d as i64) as usize;
        let p = p.rem_euclid(d as i64) as usize;
        Ok(BasicMatrix::try_from_fn(d, d, |r, j| {
            if r != (2 * q + d - j) % d {
                F::zero()
            } else {
                power(&self.omega, (2 * p * ((q + d - j) % d)) % d)
            }
        })
        .map_err(ExactFieldError::from)?)
    }

    pub fn parity_pairing(&self, a: &BasicMatrix<F>, q: i64, p: i64) -> Result<F, HeisenbergError> {
        let d = self.dimension;
        if a.shape() != (d, d) {
            return Err(HeisenbergError::Shape { dimension: d });
        }
        let q = q.rem_euclid(d as i64) as usize;
        let p = p.rem_euclid(d as i64) as usize;
        let mut trace = F::zero();
        for j in 0..d {
            let r = (2 * q + d - j) % d;
            trace = trace.add(
                &a.as_slice()[j * d + r].mul(&power(&self.omega, (2 * p * ((q + d - j) % d)) % d)),
            );
        }
        Ok(trace)
    }

    pub fn verify_relations(&self) -> Result<bool, HeisenbergError> {
        let x = self.shift()?;
        let z = self.clock()?;
        let zx = mx::multiply(&z, &x)?;
        let wxz = mx::scale(&mx::multiply(&x, &z)?, &self.omega)?;
        Ok(zx == wxz
            && mx::is_identity_matrix(&mx::power(&x, self.dimension as u64)?)?
            && mx::is_identity_matrix(&mx::power(&z, self.dimension as u64)?)?)
    }

    pub fn intertwiner_from_clock_seed(
        &self,
        shift: &BasicMatrix<F>,
        clock: &BasicMatrix<F>,
        seed: &BasicMatrix<F>,
    ) -> Result<BasicMatrix<F>, HeisenbergError> {
        let d = self.dimension;
        if shift.shape() != (d, d) || clock.shape() != (d, d) || seed.shape() != (d, 1) {
            return Err(HeisenbergError::IntertwinerPremise(
                "expected dxd operators and dx1 seed",
            ));
        }
        let identity = mx::identity::<F>(d)?;
        for operator in [shift, clock] {
            let star = dagger(operator)?;
            if mx::multiply(&star, operator)? != identity
                || mx::multiply(operator, &star)? != identity
            {
                return Err(HeisenbergError::IntertwinerPremise(
                    "operators must be unitary",
                ));
            }
        }
        if mx::multiply(clock, shift)? != mx::scale(&mx::multiply(shift, clock)?, &self.omega)? {
            return Err(HeisenbergError::IntertwinerPremise("ZX = omega XZ"));
        }
        if mx::power(shift, d as u64)? != identity {
            return Err(HeisenbergError::IntertwinerPremise("X^d = I"));
        }
        if mx::multiply(clock, seed)? != *seed
            || mx::multiply(&dagger(seed)?, seed)? != mx::identity::<F>(1)?
        {
            return Err(HeisenbergError::IntertwinerPremise(
                "normalized clock eigenvector at eigenvalue one",
            ));
        }
        let mut columns = Vec::with_capacity(d);
        let mut column = seed.clone();
        for _ in 0..d {
            columns.push(column.clone());
            column = mx::multiply(shift, &column)?;
        }
        let u = BasicMatrix::try_from_fn(d, d, |r, c| columns[c].as_slice()[r].clone())
            .map_err(ExactFieldError::from)?;
        let star = dagger(&u)?;
        if mx::multiply(&star, &u)? != identity
            || mx::multiply(&u, &star)? != identity
            || mx::multiply(shift, &u)? != mx::multiply(&u, &self.shift()?)?
            || mx::multiply(clock, &u)? != mx::multiply(&u, &self.clock()?)?
        {
            return Err(HeisenbergError::IntertwinerPremise(
                "constructed intertwiner failed exact verification",
            ));
        }
        Ok(u)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TraceObstruction<F> {
    pub dimension: usize,
    pub residual_trace: F,
    pub normalized_frobenius_square_lower_bound: F,
    pub obstructed: bool,
}

pub fn trace_obstruction<F: ComplexField>(
    dimension: usize,
    lambda: &F,
) -> Result<TraceObstruction<F>, HeisenbergError> {
    if dimension == 0 || dimension > MAX_DIMENSION {
        return Err(HeisenbergError::Dimension(dimension));
    }
    let trace = lambda.mul(&F::from_rational(&ri(-(dimension as i64))));
    Ok(TraceObstruction {
        dimension,
        residual_trace: trace.clone(),
        normalized_frobenius_square_lower_bound: lambda.mul(&lambda.conjugate()),
        obstructed: trace != F::zero(),
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StoneVonNeumannCensus {
    pub prime: usize,
    pub linear_irreducibles: usize,
    pub nontrivial_central_irreducibles: usize,
    pub nontrivial_dimension: usize,
    pub group_order: BigUint,
}

pub fn stone_von_neumann_census(prime: usize) -> Result<StoneVonNeumannCensus, HeisenbergError> {
    if !(2..=MAX_DIMENSION).contains(&prime) || !omega_number_theory::finite_field::is_prime(prime)
    {
        return Err(HeisenbergError::NotPrime(prime));
    }
    Ok(StoneVonNeumannCensus {
        prime,
        linear_irreducibles: prime * prime,
        nontrivial_central_irreducibles: prime - 1,
        nontrivial_dimension: prime,
        group_order: BigUint::from(prime).pow(3),
    })
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum FiniteHeisenbergError {
    #[error("modulus must be an odd prime at most 127")]
    Prime,
    #[error("coordinate, basis index or character is outside F_p")]
    Coordinates,
    #[error("exhaustive representation check exceeds its p^7 budget")]
    Budget,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteHeisenberg {
    prime: u64,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct HeisenbergElement {
    pub q: u64,
    pub p_coord: u64,
    pub z: u64,
}

impl HeisenbergElement {
    pub fn new(q: u64, p_coord: u64, z: u64) -> Self {
        Self { q, p_coord, z }
    }
}

impl FiniteHeisenberg {
    pub fn new(prime: u64) -> Result<Self, FiniteHeisenbergError> {
        if prime < 3
            || prime > 127
            || prime % 2 == 0
            || !omega_number_theory::finite_field::is_prime(prime as usize)
        {
            return Err(FiniteHeisenbergError::Prime);
        }
        Ok(Self { prime })
    }
    pub fn prime(&self) -> u64 {
        self.prime
    }
    fn check(&self, g: HeisenbergElement) -> Result<(), FiniteHeisenbergError> {
        if g.q >= self.prime || g.p_coord >= self.prime || g.z >= self.prime {
            Err(FiniteHeisenbergError::Coordinates)
        } else {
            Ok(())
        }
    }
    pub fn multiply(
        &self,
        g1: HeisenbergElement,
        g2: HeisenbergElement,
    ) -> Result<HeisenbergElement, FiniteHeisenbergError> {
        let p = self.prime;
        self.check(g1)?;
        self.check(g2)?;
        let modulus = u128::from(p);
        let inv2 = u128::from(p.div_ceil(2));
        let q1_p2 = (u128::from(g1.q) * u128::from(g2.p_coord)) % modulus;
        let p1_q2 = (u128::from(g1.p_coord) * u128::from(g2.q)) % modulus;
        let omega = (q1_p2 + modulus - p1_q2) % modulus;
        let cocycle = (inv2 * omega) % modulus;

        Ok(HeisenbergElement {
            q: ((u128::from(g1.q) + u128::from(g2.q)) % modulus) as u64,
            p_coord: ((u128::from(g1.p_coord) + u128::from(g2.p_coord)) % modulus) as u64,
            z: ((u128::from(g1.z) + u128::from(g2.z) + cocycle) % modulus) as u64,
        })
    }

    pub fn basis_action(
        &self,
        g: HeisenbergElement,
        x: u64,
        c: u64,
    ) -> Result<(u64, u64), FiniteHeisenbergError> {
        let p = self.prime;
        self.check(g)?;
        if x >= p || c >= p {
            return Err(FiniteHeisenbergError::Coordinates);
        }
        let modulus = u128::from(p);
        let rx = (u128::from(g.p_coord) * u128::from(x)) % modulus;
        let qr = (u128::from(g.q) * u128::from(g.p_coord)) % modulus;
        let half_qr = (u128::from(p.div_ceil(2)) * qr) % modulus;
        let exponent = (u128::from(g.z) + 2 * modulus - rx - half_qr) % modulus;
        Ok((
            ((u128::from(x) + u128::from(g.q)) % modulus) as u64,
            ((u128::from(c) * exponent) % modulus) as u64,
        ))
    }

    pub fn check_representation_law(&self, c: u64) -> Result<bool, FiniteHeisenbergError> {
        let p = self.prime;
        if c >= p {
            return Err(FiniteHeisenbergError::Coordinates);
        }
        if p > 7 {
            return Err(FiniteHeisenbergError::Budget);
        }
        let elements: Vec<_> = (0..p)
            .flat_map(|q| {
                (0..p).flat_map(move |r| (0..p).map(move |z| HeisenbergElement::new(q, r, z)))
            })
            .collect();
        for &g in &elements {
            for &h in &elements {
                let product = self.multiply(g, h)?;
                for x in 0..p {
                    let (y, b) = self.basis_action(h, x, c)?;
                    let (z, a) = self.basis_action(g, y, c)?;
                    if self.basis_action(product, x, c)? != (z, (a + b) % p) {
                        return Ok(false);
                    }
                }
            }
        }
        Ok(true)
    }
}

#[derive(Debug, Clone)]
pub struct PrimeCharacteristicCcr {
    pub characteristic: usize,
    pub multiplication: BasicMatrix<omega_number_theory::finite_field::FieldElement>,
    pub derivative: BasicMatrix<omega_number_theory::finite_field::FieldElement>,
    pub commutator: BasicMatrix<omega_number_theory::finite_field::FieldElement>,
    pub identity_trace: omega_number_theory::finite_field::FieldElement,
}

pub fn prime_characteristic_ccr(p: usize) -> Result<PrimeCharacteristicCcr, HeisenbergError> {
    if !(2..=31).contains(&p) {
        return Err(HeisenbergError::Dimension(p));
    }
    let field = omega_number_theory::finite_field::FiniteField::prime_field(p)
        .ok_or(HeisenbergError::Dimension(p))?;
    let multiplication = BasicMatrix::try_from_fn(p, p, |r, c| {
        if r == c + 1 {
            field.one()
        } else {
            field.zero()
        }
    })
    .map_err(ExactFieldError::from)?;
    let derivative = BasicMatrix::try_from_fn(p, p, |r, c| {
        if c == r + 1 {
            field.base(c)
        } else {
            field.zero()
        }
    })
    .map_err(ExactFieldError::from)?;
    let commutator = BasicMatrix::try_from_fn(p, p, |r, c| {
        let mut dx = field.zero();
        let mut xd = field.zero();
        for k in 0..p {
            dx = field.add(
                &dx,
                &field.mul(
                    &derivative.as_slice()[r * p + k],
                    &multiplication.as_slice()[k * p + c],
                ),
            );
            xd = field.add(
                &xd,
                &field.mul(
                    &multiplication.as_slice()[r * p + k],
                    &derivative.as_slice()[k * p + c],
                ),
            );
        }
        field.sub(&dx, &xd)
    })
    .map_err(ExactFieldError::from)?;
    let identity_trace = (0..p).fold(field.zero(), |a, i| {
        field.add(&a, &commutator.as_slice()[i * p + i])
    });
    Ok(PrimeCharacteristicCcr {
        characteristic: p,
        multiplication,
        derivative,
        commutator,
        identity_trace,
    })
}
