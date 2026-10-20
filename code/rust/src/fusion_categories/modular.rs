use std::cmp::Ordering;

use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_bigint::BigInt;
use omega_number_theory::rational::Rational;
use thiserror::Error;

use crate::braided::RibbonFusionCategory;
use crate::error::FusionError;
use crate::fusion_ring::FusionRing;
use crate::scalar::{root_of_unity_data, FusionScalar};
use linear_algebra::exact_field::{elimination, involution, matrix};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Error)]
pub enum ModularDefect {
    #[error("S~ is not symmetric at ({a}, {b})")]
    NotSymmetric { a: usize, b: usize },
    #[error("the braiding is degenerate: S~ has rank {rank} of {size}")]
    Degenerate { rank: usize, size: usize },
    #[error("S~^2 differs from D^2 C at ({a}, {b})")]
    SSquared { a: usize, b: usize },
    #[error("S~ S~^dagger differs from D^2 I at ({a}, {b})")]
    Unitarity { a: usize, b: usize },
    #[error("(S~ T)^3 differs from p_+ S~^2 at ({a}, {b})")]
    Relation { a: usize, b: usize },
    #[error("the Verlinde formula fails at ({a}, {b}, {c})")]
    Verlinde { a: usize, b: usize, c: usize },
    #[error("the global dimension squared is zero")]
    ZeroGlobalDimension,
    #[error("the Frobenius-Schur sum of label {label} is not -1, 0 or 1")]
    FrobeniusSchur { label: usize },
    #[error("the supplied dimension D does not satisfy D^2 = sum_a d_a^2")]
    WrongGlobalDimension,
    #[error("the supplied dimension D is not positive")]
    NonPositiveDimension,
}

#[derive(Debug, Clone, PartialEq)]
pub struct ModularData<K> {
    ring: FusionRing,
    dimensions: Vec<K>,
    twists: Vec<K>,
    s_tilde: BasicMatrix<K>,
    d_squared: K,
    p_plus: K,
}

impl<K: FusionScalar> ModularData<K> {
    pub fn from_ribbon(ribbon: &RibbonFusionCategory<K>) -> Result<Self, FusionError> {
        let s_tilde = Self::ribbon_s_matrix(ribbon.ring(), ribbon.dimensions(), ribbon.twists())?;
        Ok(Self {
            ring: ribbon.ring().clone(),
            dimensions: ribbon.dimensions().to_vec(),
            twists: ribbon.twists().to_vec(),
            s_tilde,
            d_squared: ribbon.global_dimension_squared(),
            p_plus: ribbon.gauss_sum(),
        })
    }

    fn ribbon_s_matrix(
        ring: &FusionRing,
        dimensions: &[K],
        twists: &[K],
    ) -> Result<BasicMatrix<K>, FusionError> {
        let n = ring.rank();
        let inverses = twists
            .iter()
            .map(|theta| omega_number_theory::scalar::inverse(theta).map_err(FusionError::from))
            .collect::<Result<Vec<_>, _>>()?;
        let weighted = dimensions
            .iter()
            .zip(twists)
            .map(|(d, t)| d.mul(t))
            .collect::<Vec<_>>();
        let duals = (0..n)
            .map(|b| ring.dual(b))
            .collect::<Result<Vec<_>, _>>()?;
        BasicMatrix::try_from_fn_result(n, n, |a, b| {
            let total = Self::fusion_sum(ring, a, duals[b], &weighted)?;
            Ok(total.mul(&inverses[a]).mul(&inverses[b]))
        })
    }

    fn add_multiple(total: K, value: &K, multiplicity: u64) -> Result<K, FusionError> {
        match multiplicity {
            0 => Ok(total),
            1 => Ok(total.add(value)),
            _ => {
                let weight = omega_number_theory::scalar::from_i64::<K>(
                    i64::try_from(multiplicity).map_err(|_| FusionError::Overflow {
                        context: "embedding a fusion coefficient",
                    })?,
                );
                Ok(total.add(&weight.mul(value)))
            }
        }
    }

    fn fusion_sum(ring: &FusionRing, a: usize, b: usize, values: &[K]) -> Result<K, FusionError> {
        let mut total = K::zero();
        for (c, value) in values.iter().enumerate() {
            total = Self::add_multiple(total, value, ring.n(a, b, c))?;
        }
        Ok(total)
    }

    pub fn verified(ribbon: &RibbonFusionCategory<K>) -> Result<Self, FusionError> {
        let data = Self::from_ribbon(ribbon)?;
        data.verify()?;
        Ok(data)
    }

    pub fn rank(&self) -> usize {
        self.ring.rank()
    }

    pub fn ring(&self) -> &FusionRing {
        &self.ring
    }

    pub fn dimensions(&self) -> &[K] {
        &self.dimensions
    }

    pub fn twists(&self) -> &[K] {
        &self.twists
    }

    pub fn s_tilde(&self) -> &BasicMatrix<K> {
        &self.s_tilde
    }

    pub fn d_squared(&self) -> &K {
        &self.d_squared
    }

    pub fn p_plus(&self) -> &K {
        &self.p_plus
    }

    pub fn topological_entanglement_entropy_dimension_squared(&self) -> &K {
        &self.d_squared
    }

    pub fn t_matrix(&self) -> Result<BasicMatrix<K>, FusionError> {
        matrix::diagonal(&self.twists).map_err(FusionError::from)
    }

    pub fn charge_conjugation(&self) -> Result<BasicMatrix<K>, FusionError> {
        self.scaled_charge_conjugation(&K::one())
    }

    fn scaled_charge_conjugation(&self, scale: &K) -> Result<BasicMatrix<K>, FusionError> {
        let n = self.rank();
        BasicMatrix::try_from_fn_result(n, n, |a, b| {
            Ok(if self.ring.dual(a)? == b {
                scale.clone()
            } else {
                K::zero()
            })
        })
    }

    fn scaled_identity(&self, scale: &K) -> Result<BasicMatrix<K>, FusionError> {
        let n = self.rank();
        BasicMatrix::try_from_fn(n, n, |a, b| if a == b { scale.clone() } else { K::zero() })
            .map_err(FusionError::from)
    }

    fn first_difference(
        left: &BasicMatrix<K>,
        right: &BasicMatrix<K>,
    ) -> Result<Option<(usize, usize)>, FusionError> {
        if left.shape() != right.shape() {
            return Err(FusionError::Shape {
                operation: "comparing modular matrices",
                left: left.shape(),
                right: right.shape(),
            });
        }
        for a in 0..left.rows() {
            for b in 0..left.cols() {
                if left.get_ref(a, b)? != right.get_ref(a, b)? {
                    return Ok(Some((a, b)));
                }
            }
        }
        Ok(None)
    }

    pub fn verify(&self) -> Result<(), FusionError> {
        if self.d_squared.is_zero() {
            return Err(FusionError::Modular(ModularDefect::ZeroGlobalDimension));
        }
        self.verify_symmetry()?;
        self.verify_nondegenerate()?;
        let squared = self.verify_square()?;
        self.verify_unitarity()?;
        self.verify_relation(&squared)?;
        self.verify_verlinde()
    }

    fn require_equal(
        left: &BasicMatrix<K>,
        right: &BasicMatrix<K>,
        defect: impl FnOnce(usize, usize) -> ModularDefect,
    ) -> Result<(), FusionError> {
        if let Some((a, b)) = Self::first_difference(left, right)? {
            return Err(FusionError::Modular(defect(a, b)));
        }
        Ok(())
    }

    fn verify_symmetry(&self) -> Result<(), FusionError> {
        for a in 0..self.rank() {
            for b in a + 1..self.rank() {
                if self.s_tilde.get_ref(a, b)? != self.s_tilde.get_ref(b, a)? {
                    return Err(FusionError::Modular(ModularDefect::NotSymmetric { a, b }));
                }
            }
        }
        Ok(())
    }

    fn verify_nondegenerate(&self) -> Result<(), FusionError> {
        let rank = elimination::rank(&self.s_tilde).map_err(FusionError::from)?;
        if rank < self.rank() {
            return Err(FusionError::Modular(ModularDefect::Degenerate {
                rank,
                size: self.rank(),
            }));
        }
        Ok(())
    }

    fn verify_square(&self) -> Result<BasicMatrix<K>, FusionError> {
        let squared = matrix::multiply(&self.s_tilde, &self.s_tilde).map_err(FusionError::from)?;
        Self::require_equal(
            &squared,
            &self.scaled_charge_conjugation(&self.d_squared)?,
            |a, b| ModularDefect::SSquared { a, b },
        )?;
        Ok(squared)
    }

    fn verify_unitarity(&self) -> Result<(), FusionError> {
        let actual = matrix::multiply(
            &self.s_tilde,
            &involution::adjoint(&self.s_tilde).map_err(FusionError::from)?,
        )
        .map_err(FusionError::from)?;
        Self::require_equal(&actual, &self.scaled_identity(&self.d_squared)?, |a, b| {
            ModularDefect::Unitarity { a, b }
        })
    }

    fn st_matrix(&self) -> Result<BasicMatrix<K>, FusionError> {
        let n = self.rank();
        BasicMatrix::try_from_fn_result(n, n, |a, b| {
            Ok(self.s_tilde.get_ref(a, b)?.mul(&self.twists[b]))
        })
    }

    fn verify_relation(&self, squared: &BasicMatrix<K>) -> Result<(), FusionError> {
        let st = self.st_matrix()?;
        let square = matrix::multiply(&st, &st).map_err(FusionError::from)?;
        let cube = matrix::multiply(&square, &st).map_err(FusionError::from)?;
        let expected = matrix::scale(squared, &self.p_plus).map_err(FusionError::from)?;
        Self::require_equal(&cube, &expected, |a, b| ModularDefect::Relation { a, b })
    }

    fn verify_verlinde(&self) -> Result<(), FusionError> {
        if let Some(&[a, b, c]) = self
            .ring
            .verlinde_defects(&self.s_tilde, &self.d_squared)?
            .first()
        {
            return Err(FusionError::Modular(ModularDefect::Verlinde { a, b, c }));
        }
        Ok(())
    }

    pub fn central_charge_mod_4(&self) -> Result<Rational, FusionError> {
        let ratio =
            omega_number_theory::scalar::divide(&self.p_plus.mul(&self.p_plus), &self.d_squared)
                .map_err(FusionError::from)?;
        let (n, k) = root_of_unity_data(&ratio).ok_or(FusionError::NotInSubfield {
            what: "p_+^2 / D^2",
            expected: "a root of unity",
        })?;
        Ok(Rational::new(
            BigInt::from(4 * u64::from(k)),
            BigInt::from(n),
        ))
    }

    pub fn central_charge_mod_8(&self, total_dimension: &K) -> Result<Rational, FusionError> {
        if total_dimension.mul(total_dimension) != self.d_squared {
            return Err(FusionError::Modular(ModularDefect::WrongGlobalDimension));
        }
        match total_dimension.real_sign() {
            Some(Ordering::Greater) => {}
            Some(_) => return Err(FusionError::Modular(ModularDefect::NonPositiveDimension)),
            None => {
                return Err(FusionError::SignUndecided {
                    context: "the global dimension D",
                })
            }
        }
        let ratio = omega_number_theory::scalar::divide(&self.p_plus, total_dimension)
            .map_err(FusionError::from)?;
        let (n, k) = root_of_unity_data(&ratio).ok_or(FusionError::NotInSubfield {
            what: "p_+ / D",
            expected: "a root of unity",
        })?;
        Ok(Rational::new(
            BigInt::from(8 * u64::from(k)),
            BigInt::from(n),
        ))
    }

    pub fn frobenius_schur_indicator(&self, a: usize) -> Result<i8, FusionError> {
        let n = self.rank();
        if a >= n {
            return Err(FusionError::Label { label: a, rank: n });
        }
        let weights = self.indicator_weights()?;
        let mut total = K::zero();
        for b in 0..n {
            total = total.add(&self.indicator_row(a, b, &weights)?);
        }
        let value = omega_number_theory::scalar::divide(&total, &self.d_squared)
            .map_err(FusionError::from)?;
        Self::indicator_result(a, &value)
    }

    fn indicator_weights(&self) -> Result<Vec<(K, K)>, FusionError> {
        self.dimensions
            .iter()
            .zip(&self.twists)
            .map(|(d, t)| {
                let square = t.mul(t);
                Ok((
                    d.mul(&square),
                    omega_number_theory::scalar::divide(d, &square).map_err(FusionError::from)?,
                ))
            })
            .collect()
    }

    fn indicator_row(&self, a: usize, b: usize, weights: &[(K, K)]) -> Result<K, FusionError> {
        let mut total = K::zero();
        for (c, (_, right)) in weights.iter().enumerate() {
            let multiplicity = self.ring.n(b, c, a);
            if multiplicity == 0 {
                continue;
            }
            total = Self::add_multiple(total, &weights[b].0.mul(right), multiplicity)?;
        }
        Ok(total)
    }

    fn indicator_result(a: usize, value: &K) -> Result<i8, FusionError> {
        if *value == K::one() {
            Ok(1)
        } else if *value == K::one().neg() {
            Ok(-1)
        } else if value.is_zero() {
            Ok(0)
        } else {
            Err(FusionError::Modular(ModularDefect::FrobeniusSchur {
                label: a,
            }))
        }
    }

    pub fn ground_state_degeneracy(&self, genus: u32) -> Result<BigInt, FusionError> {
        let exponent = Self::genus_exponent(genus)?;
        let mut total = K::zero();
        for (ratio, multiplicity) in self.dimension_ratios()? {
            let value =
                omega_number_theory::scalar::power(&ratio, exponent).map_err(FusionError::from)?;
            total = Self::add_multiple(total, &value, multiplicity)?;
        }
        let rational = total.to_rational().ok_or(FusionError::NotInSubfield {
            what: "the ground-state degeneracy",
            expected: "a rational number",
        })?;
        if !rational.is_integer() || rational < Rational::from_integer(BigInt::from(0)) {
            return Err(FusionError::NotInSubfield {
                what: "the ground-state degeneracy",
                expected: "a non-negative integer",
            });
        }
        Ok(rational.to_integer())
    }
    fn genus_exponent(genus: u32) -> Result<i64, FusionError> {
        let exponent = i64::from(genus) - 1;
        let requested = exponent.unsigned_abs();
        let limit = omega_number_theory::scalar::MAX_SCALAR_EXPONENT;
        if requested > limit {
            return Err(FusionError::Budget {
                what: "ground-state exponent",
                requested: requested as u128,
                limit: limit as u128,
            });
        }
        Ok(exponent)
    }

    fn dimension_ratios(&self) -> Result<Vec<(K, u64)>, FusionError> {
        let mut squares: Vec<(K, u64)> = Vec::new();
        for d in &self.dimensions {
            let square = d.mul(d);
            if let Some((_, count)) = squares.iter_mut().find(|(s, _)| *s == square) {
                *count += 1;
            } else {
                squares.push((square, 1));
            }
        }
        for (square, _) in &mut squares {
            *square = omega_number_theory::scalar::divide(&self.d_squared, square)
                .map_err(FusionError::from)?;
        }
        Ok(squares)
    }
}
