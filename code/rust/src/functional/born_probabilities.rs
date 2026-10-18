
use num_complex::Complex;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum ProbabilityComponent {
    Weight,
    Real,
    Imaginary,
}

#[derive(Debug, Clone, thiserror::Error, PartialEq, Eq)]
pub enum BornProbabilityError {
    #[error("BORN_EMPTY_INPUT")]
    EmptyInput,
    #[error("BORN_ZERO_DENOMINATOR: index {index}, component {component:?}")]
    ZeroDenominator {
        index: usize,
        component: ProbabilityComponent,
    },
    #[error("BORN_NEGATIVE_WEIGHT: index {index}")]
    NegativeWeight { index: usize },
    #[error("BORN_ZERO_TOTAL_WEIGHT")]
    ZeroTotalWeight,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BornProbabilities {
    probabilities: Vec<BigRational>,
}

fn canonical_rational(
    value: &BigRational,
    index: usize,
    component: ProbabilityComponent,
) -> Result<BigRational, BornProbabilityError> {
    if value.denom().is_zero() {
        return Err(BornProbabilityError::ZeroDenominator { index, component });
    }
    Ok(BigRational::new(value.numer().clone(), value.denom().clone()))
}

impl BornProbabilities {
    pub fn from_weights(weights: &[BigRational]) -> Result<Self, BornProbabilityError> {
        if weights.is_empty() {
            return Err(BornProbabilityError::EmptyInput);
        }
        let canonical = weights
            .iter()
            .enumerate()
            .map(|(index, value)| {
                let weight = canonical_rational(value, index, ProbabilityComponent::Weight)?;
                if weight.is_negative() {
                    return Err(BornProbabilityError::NegativeWeight { index });
                }
                Ok(weight)
            })
            .collect::<Result<Vec<_>, _>>()?;
        let total = canonical.iter().cloned().sum::<BigRational>();
        if total.is_zero() {
            return Err(BornProbabilityError::ZeroTotalWeight);
        }
        Ok(Self {
            probabilities: canonical
                .into_iter()
                .map(|weight| weight / &total)
                .collect(),
        })
    }

    pub fn from_amplitudes(
        amplitudes: &[Complex<BigRational>],
    ) -> Result<Self, BornProbabilityError> {
        let weights = amplitudes
            .iter()
            .enumerate()
            .map(|(index, amplitude)| {
                let real = canonical_rational(&amplitude.re, index, ProbabilityComponent::Real)?;
                let imaginary =
                    canonical_rational(&amplitude.im, index, ProbabilityComponent::Imaginary)?;
                Ok(&real * &real + &imaginary * &imaginary)
            })
            .collect::<Result<Vec<_>, BornProbabilityError>>()?;
        Self::from_weights(&weights)
    }

    pub fn probabilities(&self) -> &[BigRational] {
        &self.probabilities
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    fn q(numerator: i64, denominator: i64) -> BigRational {
        BigRational::new(numerator.into(), denominator.into())
    }

    #[test]
    fn exact_nonnegative_weights_normalize_without_rounding() {
        let result = BornProbabilities::from_weights(&[q(1, 1), q(2, 1), q(3, 1)]).unwrap();
        assert_eq!(result.probabilities(), [q(1, 6), q(1, 3), q(1, 2)]);
        assert_eq!(
            result.probabilities().iter().cloned().sum::<BigRational>(),
            q(1, 1)
        );
    }

    #[test]
    fn complex_squared_modulus_uses_both_components() {
        let result = BornProbabilities::from_amplitudes(&[
            Complex::new(q(3, 1), q(4, 1)),
            Complex::new(q(5, 1), q(0, 1)),
        ])
        .unwrap();
        assert_eq!(result.probabilities(), [q(1, 2), q(1, 2)]);
    }

    #[test]
    fn common_nonzero_scale_and_phase_preserve_distribution() {
        let amplitudes = [
            Complex::new(q(1, 1), q(2, 1)),
            Complex::new(q(-3, 1), q(1, 1)),
        ];
        let original = BornProbabilities::from_amplitudes(&amplitudes).unwrap();
        let changed = amplitudes.map(|a| Complex::new(-a.im * q(7, 1), a.re * q(7, 1)));
        assert_eq!(
            BornProbabilities::from_amplitudes(&changed).unwrap(),
            original
        );
    }

    #[test]
    fn empty_and_all_zero_inputs_have_distinct_refusals() {
        assert_eq!(
            BornProbabilities::from_weights(&[]),
            Err(BornProbabilityError::EmptyInput)
        );
        assert_eq!(
            BornProbabilities::from_amplitudes(&[]),
            Err(BornProbabilityError::EmptyInput)
        );
        assert_eq!(
            BornProbabilities::from_weights(&[q(0, 1)]),
            Err(BornProbabilityError::ZeroTotalWeight)
        );
        assert_eq!(
            BornProbabilities::from_amplitudes(&[Complex::new(q(0, 1), q(0, 1))]),
            Err(BornProbabilityError::ZeroTotalWeight)
        );
    }

    #[test]
    fn negative_weight_is_refused_after_sign_canonicalization() {
        let negative = BigRational::new_raw(1.into(), (-2).into());
        assert_eq!(
            BornProbabilities::from_weights(&[q(1, 1), negative]),
            Err(BornProbabilityError::NegativeWeight { index: 1 })
        );
        let positive = BigRational::new_raw((-2).into(), (-4).into());
        assert_eq!(
            BornProbabilities::from_weights(&[positive, q(1, 2)])
                .unwrap()
                .probabilities(),
            [q(1, 2), q(1, 2)]
        );
    }

    #[test]
    fn invalid_rationals_are_refused_before_weight_or_amplitude_arithmetic() {
        let invalid = BigRational::new_raw(1.into(), 0.into());
        assert_eq!(
            BornProbabilities::from_weights(&[q(1, 1), invalid.clone()]),
            Err(BornProbabilityError::ZeroDenominator {
                index: 1,
                component: ProbabilityComponent::Weight
            })
        );
        for (component, amplitude) in [
            (
                ProbabilityComponent::Real,
                Complex::new(invalid.clone(), q(0, 1)),
            ),
            (
                ProbabilityComponent::Imaginary,
                Complex::new(q(1, 1), invalid),
            ),
        ] {
            assert_eq!(
                BornProbabilities::from_amplitudes(&[amplitude]),
                Err(BornProbabilityError::ZeroDenominator {
                    index: 0,
                    component
                })
            );
        }
    }

    #[test]
    fn extreme_exact_weights_neither_overflow_nor_disappear() {
        let large = BigRational::from_integer(BigInt::from(1) << 4096);
        let tiny = BigRational::new(BigInt::from(1), BigInt::from(1) << 4096);
        let expected_tiny = &tiny / (&large + &tiny);
        let result = BornProbabilities::from_weights(&[large, tiny]).unwrap();
        assert_eq!(result.probabilities()[1], expected_tiny);
        assert!(!result.probabilities()[1].is_zero());
        assert_eq!(
            result.probabilities().iter().cloned().sum::<BigRational>(),
            q(1, 1)
        );
    }
}
