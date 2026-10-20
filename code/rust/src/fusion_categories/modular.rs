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
        let ring = ribbon.ring().clone();
        let n = ring.rank();
        let dimensions = ribbon.dimensions().to_vec();
        let twists = ribbon.twists().to_vec();
        let s_tilde = BasicMatrix::try_from_fn_result(n, n, |a, b| -> Result<K, FusionError> {
            let b_star = ring.dual(b)?;
            let theta_a = twists
                .get(a)
                .ok_or(FusionError::Label { label: a, rank: n })?;
            let theta_b = twists
                .get(b)
                .ok_or(FusionError::Label { label: b, rank: n })?;
            let scale = omega_number_theory::scalar::inverse(&theta_a.mul(theta_b))
                .map_err(FusionError::from)?;
            let mut total = K::zero();
            for c in 0..n {
                let multiplicity = ring.n(a, b_star, c);
                if multiplicity > 0 {
                    let d_c = dimensions
                        .get(c)
                        .ok_or(FusionError::Label { label: c, rank: n })?;
                    let theta_c = twists
                        .get(c)
                        .ok_or(FusionError::Label { label: c, rank: n })?;
                    let weight = omega_number_theory::scalar::from_i64::<K>(
                        i64::try_from(multiplicity).map_err(|_| FusionError::Overflow {
                            context: "embedding a fusion coefficient",
                        })?,
                    );
                    total = total.add(&weight.mul(d_c).mul(theta_c));
                }
            }
            Ok(total.mul(&scale))
        })?;
        Ok(Self {
            d_squared: ribbon.global_dimension_squared(),
            p_plus: ribbon.gauss_sum(),
            ring,
            dimensions,
            twists,
            s_tilde,
        })
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
        let n = self.rank();
        BasicMatrix::try_from_fn_result(n, n, |a, b| -> Result<K, FusionError> {
            Ok(if self.ring.dual(a)? == b {
                K::one()
            } else {
                K::zero()
            })
        })
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
        let n = self.rank();
        let fail = |defect: ModularDefect| Err(FusionError::Modular(defect));
        if self.d_squared.is_zero() {
            return fail(ModularDefect::ZeroGlobalDimension);
        }
        let s = &self.s_tilde;
        for a in 0..n {
            for b in a + 1..n {
                if s.get_ref(a, b)? != s.get_ref(b, a)? {
                    return fail(ModularDefect::NotSymmetric { a, b });
                }
            }
        }
        let rank = elimination::rank(s).map_err(FusionError::from)?;
        if rank < n {
            return fail(ModularDefect::Degenerate { rank, size: n });
        }
        let s_squared = matrix::multiply(s, s).map_err(FusionError::from)?;
        let expected = matrix::scale(&self.charge_conjugation()?, &self.d_squared)
            .map_err(FusionError::from)?;
        if let Some((a, b)) = Self::first_difference(&s_squared, &expected)? {
            return fail(ModularDefect::SSquared { a, b });
        }
        let unitarity = matrix::multiply(s, &involution::adjoint(s).map_err(FusionError::from)?)
            .map_err(FusionError::from)?;
        let expected = matrix::scale(
            &matrix::identity::<K>(n).map_err(FusionError::from)?,
            &self.d_squared,
        )
        .map_err(FusionError::from)?;
        if let Some((a, b)) = Self::first_difference(&unitarity, &expected)? {
            return fail(ModularDefect::Unitarity { a, b });
        }
        let st = matrix::multiply(s, &self.t_matrix()?).map_err(FusionError::from)?;
        let st_cubed = matrix::power(&st, 3).map_err(FusionError::from)?;
        let expected = matrix::scale(&s_squared, &self.p_plus).map_err(FusionError::from)?;
        if let Some((a, b)) = Self::first_difference(&st_cubed, &expected)? {
            return fail(ModularDefect::Relation { a, b });
        }
        if let Some(&[a, b, c]) = self.ring.verlinde_defects(s, &self.d_squared)?.first() {
            return fail(ModularDefect::Verlinde { a, b, c });
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
        let mut total = K::zero();
        for b in 0..n {
            for c in 0..n {
                let multiplicity = self.ring.n(b, c, a);
                if multiplicity == 0 {
                    continue;
                }
                let weight = omega_number_theory::scalar::from_i64::<K>(
                    i64::try_from(multiplicity).map_err(|_| FusionError::Overflow {
                        context: "embedding a fusion coefficient",
                    })?,
                );
                let ratio = omega_number_theory::scalar::divide(
                    self.twists
                        .get(b)
                        .ok_or(FusionError::Label { label: b, rank: n })?,
                    self.twists
                        .get(c)
                        .ok_or(FusionError::Label { label: c, rank: n })?,
                )
                .map_err(FusionError::from)?;
                let d_b = self
                    .dimensions
                    .get(b)
                    .ok_or(FusionError::Label { label: b, rank: n })?;
                let d_c = self
                    .dimensions
                    .get(c)
                    .ok_or(FusionError::Label { label: c, rank: n })?;
                total = total.add(&weight.mul(d_b).mul(d_c).mul(&ratio.mul(&ratio)));
            }
        }
        let value = omega_number_theory::scalar::divide(&total, &self.d_squared)
            .map_err(FusionError::from)?;
        if value == K::one() {
            Ok(1)
        } else if value == K::one().neg() {
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
        let exponent = i64::from(genus) - 1;
        let mut total = K::zero();
        for d in &self.dimensions {
            let ratio = omega_number_theory::scalar::divide(&self.d_squared, &d.mul(d))
                .map_err(FusionError::from)?;
            total = total.add(
                &omega_number_theory::scalar::power(&ratio, exponent).map_err(FusionError::from)?,
            );
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
}
