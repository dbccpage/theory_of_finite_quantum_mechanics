
use std::collections::BTreeSet;

use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use omega_number_theory::rational::Rational;

use crate::error::ClassicalShadowError;
use crate::finite_set::{checked_size_product, FinN};

pub(crate) fn rational_pow(base: &Rational, exponent: u32) -> Rational {
    let mut result = Rational::one();
    let mut square = base.clone();
    let mut remaining = exponent;
    while remaining > 0 {
        if remaining & 1 == 1 {
            result = &result * &square;
        }
        remaining >>= 1;
        if remaining > 0 {
            square = &square * &square;
        }
    }
    result
}

#[derive(Debug, Clone)]
pub struct ProbabilitySimplex {
    probs: Vec<Rational>,
    label: String,
}

impl PartialEq for ProbabilitySimplex {
    fn eq(&self, other: &Self) -> bool {
        self.probs == other.probs
    }
}

impl Eq for ProbabilitySimplex {}

fn check_masses(probs: &[Rational]) -> Result<(), ClassicalShadowError> {
    if probs.is_empty() {
        return Err(ClassicalShadowError::Empty);
    }
    let mut sum = Rational::zero();
    for (index, p) in probs.iter().enumerate() {
        if !p.denom().is_positive() {
            return Err(ClassicalShadowError::InvalidDenominator { index });
        }
        if p.is_negative() {
            return Err(ClassicalShadowError::NegativeEntry { index });
        }
        sum += p;
    }
    if !sum.is_one() {
        return Err(ClassicalShadowError::NotNormalized { sum });
    }
    Ok(())
}

impl ProbabilitySimplex {
    pub fn try_from_probs(
        carrier: &FinN,
        probs: Vec<Rational>,
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        if probs.is_empty() {
            return Err(ClassicalShadowError::Empty);
        }
        if probs.len() != carrier.cardinality() {
            return Err(ClassicalShadowError::DimensionMismatch {
                expected: carrier.cardinality(),
                actual: probs.len(),
            });
        }
        check_masses(&probs)?;
        Ok(Self {
            probs,
            label: label.into(),
        })
    }

    pub fn try_new(probs: Vec<Rational>) -> Result<Self, ClassicalShadowError> {
        check_masses(&probs)?;
        Ok(Self {
            probs,
            label: String::new(),
        })
    }

    pub fn try_from_weights(weights: Vec<Rational>) -> Result<Self, ClassicalShadowError> {
        if weights.is_empty() {
            return Err(ClassicalShadowError::Empty);
        }
        let mut total = Rational::zero();
        for (index, w) in weights.iter().enumerate() {
            if !w.denom().is_positive() {
                return Err(ClassicalShadowError::InvalidDenominator { index });
            }
            if w.is_negative() {
                return Err(ClassicalShadowError::NegativeEntry { index });
            }
            total += w;
        }
        if total.is_zero() {
            return Err(ClassicalShadowError::ZeroTotalWeight);
        }
        let probs = weights.iter().map(|w| w / &total).collect();
        Ok(Self {
            probs,
            label: String::new(),
        })
    }

    pub fn dirac(
        carrier: &FinN,
        index: usize,
        label: impl Into<String>,
    ) -> Result<Self, ClassicalShadowError> {
        if !carrier.contains(index) {
            return Err(ClassicalShadowError::IndexOutOfRange {
                index,
                bound: carrier.cardinality(),
            });
        }
        let mut probs = vec![Rational::zero(); carrier.cardinality()];
        probs[index] = Rational::one();
        Self::try_from_probs(carrier, probs, label)
    }

    pub fn uniform(carrier: &FinN, label: impl Into<String>) -> Result<Self, ClassicalShadowError> {
        let mass = Rational::new(BigInt::one(), BigInt::from(carrier.cardinality()));
        Self::try_from_probs(carrier, vec![mass; carrier.cardinality()], label)
    }

    pub fn n(&self) -> usize {
        self.probs.len()
    }

    pub fn probs(&self) -> &[Rational] {
        &self.probs
    }

    pub fn get(&self, index: usize) -> Option<&Rational> {
        self.probs.get(index)
    }

    pub fn label(&self) -> &str {
        &self.label
    }

    pub fn support_size(&self) -> usize {
        self.probs.iter().filter(|p| p.is_positive()).count()
    }

    pub fn support(&self) -> Vec<usize> {
        self.probs
            .iter()
            .enumerate()
            .filter(|(_, p)| p.is_positive())
            .map(|(i, _)| i)
            .collect()
    }

    pub fn max_probability(&self) -> Rational {
        self.probs.iter().fold(
            Rational::zero(),
            |best, p| {
                if *p > best {
                    p.clone()
                } else {
                    best
                }
            },
        )
    }

    pub fn is_dirac(&self) -> bool {
        self.support_size() == 1
    }

    pub fn is_uniform(&self) -> bool {
        self.probs.windows(2).all(|pair| pair[0] == pair[1])
    }

    pub fn probability_of(&self, event: &[usize]) -> Result<Rational, ClassicalShadowError> {
        let mut members = BTreeSet::new();
        for &index in event {
            if index >= self.probs.len() {
                return Err(ClassicalShadowError::IndexOutOfRange {
                    index,
                    bound: self.probs.len(),
                });
            }
            members.insert(index);
        }
        Ok(members.iter().map(|&i| &self.probs[i]).sum())
    }

    pub fn expectation(&self, values: &[Rational]) -> Result<Rational, ClassicalShadowError> {
        if values.len() != self.probs.len() {
            return Err(ClassicalShadowError::DimensionMismatch {
                expected: self.probs.len(),
                actual: values.len(),
            });
        }
        if let Some(index) = values.iter().position(|value| !value.denom().is_positive()) {
            return Err(ClassicalShadowError::InvalidDenominator { index });
        }
        Ok(self.probs.iter().zip(values).map(|(p, f)| p * f).sum())
    }

    pub fn total_variation(&self, other: &Self) -> Result<Rational, ClassicalShadowError> {
        if self.probs.len() != other.probs.len() {
            return Err(ClassicalShadowError::ShapeMismatch {
                left: self.probs.len(),
                right: other.probs.len(),
            });
        }
        let l1: Rational = self
            .probs
            .iter()
            .zip(&other.probs)
            .map(|(p, q)| (p - q).abs())
            .sum();
        Ok(l1 / Rational::from_integer(BigInt::from(2)))
    }

    pub fn product(&self, other: &Self) -> Result<Self, ClassicalShadowError> {
        let size = checked_size_product(self.probs.len(), other.probs.len())?;
        let mut probs = Vec::with_capacity(size);
        for p in &self.probs {
            for q in &other.probs {
                probs.push(p * q);
            }
        }
        Ok(Self {
            probs,
            label: format!("{} x {}", self.label, other.label),
        })
    }

    pub fn convex_combination(
        parts: &[(Rational, ProbabilitySimplex)],
    ) -> Result<Self, ClassicalShadowError> {
        let first = parts.first().ok_or(ClassicalShadowError::Empty)?;
        let n = first.1.n();
        let mut weight_sum = Rational::zero();
        let mut probs = vec![Rational::zero(); n];
        for (index, (w, part)) in parts.iter().enumerate() {
            if !w.denom().is_positive() {
                return Err(ClassicalShadowError::InvalidDenominator { index });
            }
            if w.is_negative() {
                return Err(ClassicalShadowError::NegativeEntry { index });
            }
            if part.n() != n {
                return Err(ClassicalShadowError::ShapeMismatch {
                    left: n,
                    right: part.n(),
                });
            }
            weight_sum += w;
            for (acc, p) in probs.iter_mut().zip(&part.probs) {
                *acc += w * p;
            }
        }
        if !weight_sum.is_one() {
            return Err(ClassicalShadowError::NotNormalized { sum: weight_sum });
        }
        Ok(Self {
            probs,
            label: String::new(),
        })
    }

    pub fn power_sum(&self, alpha: u32) -> Rational {
        self.probs
            .iter()
            .filter(|p| p.is_positive())
            .map(|p| rational_pow(p, alpha))
            .sum()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::{grid_simplices, simplex};
    use omega_number_theory::rational::{ri, rq};

    fn carrier(n: usize) -> FinN {
        FinN::try_new(n).unwrap()
    }

    #[test]
    fn uniform_and_dirac_have_the_expected_masses_and_supports() {
        let f = carrier(3);
        let u = ProbabilitySimplex::uniform(&f, "u").unwrap();
        assert_eq!(u.probs(), &[rq(1, 3), rq(1, 3), rq(1, 3)]);
        assert_eq!(u.support_size(), 3);
        assert!(u.is_uniform());
        assert!(!u.is_dirac());

        let d = ProbabilitySimplex::dirac(&f, 1, "d1").unwrap();
        assert_eq!(d.probs(), &[ri(0), ri(1), ri(0)]);
        assert_eq!(d.support_size(), 1);
        assert_eq!(d.support(), vec![1]);
        assert!(d.is_dirac());
        assert_eq!(d.label(), "d1");
    }

    #[test]
    fn a_vector_not_summing_to_one_is_refused_with_its_exact_sum() {
        let err = ProbabilitySimplex::try_from_probs(&carrier(2), vec![rq(1, 2), rq(1, 3)], "bad");
        assert_eq!(
            err,
            Err(ClassicalShadowError::NotNormalized { sum: rq(5, 6) })
        );
    }

    #[test]
    fn a_negative_mass_is_refused_at_its_index() {
        let err = ProbabilitySimplex::try_from_probs(&carrier(2), vec![rq(-1, 2), rq(3, 2)], "neg");
        assert_eq!(err, Err(ClassicalShadowError::NegativeEntry { index: 0 }));
    }

    #[test]
    fn raw_nonpositive_denominators_are_refused_before_mass_arithmetic() {
        let point = ProbabilitySimplex::dirac(&carrier(2), 1, "point").unwrap();
        for (numerator, denominator) in [(0, 0), (1, 0), (-1, 0), (0, -1), (-1, -1)] {
            let raw = Rational::new_raw(numerator.into(), denominator.into());
            let expected = Err(ClassicalShadowError::InvalidDenominator { index: 1 });
            assert_eq!(
                ProbabilitySimplex::try_new(vec![ri(1), raw.clone()]),
                expected
            );
            assert_eq!(
                ProbabilitySimplex::try_from_probs(&carrier(2), vec![ri(1), raw.clone()], "raw"),
                expected
            );
            assert_eq!(
                ProbabilitySimplex::try_from_weights(vec![ri(1), raw.clone()]),
                expected
            );
            assert_eq!(
                ProbabilitySimplex::convex_combination(&[
                    (ri(0), point.clone()),
                    (raw.clone(), point.clone())
                ]),
                expected
            );
            assert_eq!(
                point.expectation(&[ri(1), raw]),
                Err(ClassicalShadowError::InvalidDenominator { index: 1 })
            );
        }
        let canonical = Rational::new((-1).into(), (-1).into());
        assert_eq!(
            ProbabilitySimplex::try_new(vec![canonical]).unwrap().probs(),
            &[ri(1)]
        );
    }

    #[test]
    fn empty_and_wrongly_sized_masses_are_refused() {
        assert_eq!(
            ProbabilitySimplex::try_from_probs(&carrier(2), vec![], "x"),
            Err(ClassicalShadowError::Empty)
        );
        assert_eq!(
            ProbabilitySimplex::try_from_probs(&carrier(3), vec![rq(1, 2), rq(1, 2)], "x"),
            Err(ClassicalShadowError::DimensionMismatch {
                expected: 3,
                actual: 2
            })
        );
        assert_eq!(
            ProbabilitySimplex::try_new(vec![]),
            Err(ClassicalShadowError::Empty)
        );
    }

    #[test]
    fn a_dirac_point_outside_the_carrier_is_refused() {
        assert_eq!(
            ProbabilitySimplex::dirac(&carrier(3), 3, "x"),
            Err(ClassicalShadowError::IndexOutOfRange { index: 3, bound: 3 })
        );
    }

    #[test]
    fn weights_are_normalised_exactly_and_a_zero_total_is_refused() {
        let p = ProbabilitySimplex::try_from_weights(vec![ri(8), ri(4), ri(2), ri(1)]).unwrap();
        assert_eq!(p.probs(), &[rq(8, 15), rq(4, 15), rq(2, 15), rq(1, 15)]);
        assert_eq!(
            ProbabilitySimplex::try_from_weights(vec![ri(0), ri(0)]),
            Err(ClassicalShadowError::ZeroTotalWeight)
        );
        assert_eq!(
            ProbabilitySimplex::try_from_weights(vec![ri(1), ri(-1), ri(3)]),
            Err(ClassicalShadowError::NegativeEntry { index: 1 })
        );
        assert_eq!(
            ProbabilitySimplex::try_from_weights(vec![]),
            Err(ClassicalShadowError::Empty)
        );
    }

    #[test]
    fn labels_are_provenance_and_do_not_affect_equality() {
        let f = carrier(2);
        let a = ProbabilitySimplex::try_from_probs(&f, vec![rq(1, 4), rq(3, 4)], "a").unwrap();
        let b = ProbabilitySimplex::try_from_probs(&f, vec![rq(1, 4), rq(3, 4)], "b").unwrap();
        let c = ProbabilitySimplex::try_from_probs(&f, vec![rq(1, 2), rq(1, 2)], "a").unwrap();
        assert_eq!(a, b);
        assert_ne!(a, c);
    }

    #[test]
    fn events_are_additive_over_disjoint_events_and_count_repeats_once() {
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        assert_eq!(p.probability_of(&[0]).unwrap(), rq(1, 2));
        assert_eq!(p.probability_of(&[0, 2]).unwrap(), rq(2, 3));
        assert_eq!(p.probability_of(&[0, 0, 2, 2]).unwrap(), rq(2, 3));
        assert_eq!(p.probability_of(&[]).unwrap(), ri(0));
        assert_eq!(p.probability_of(&[0, 1, 2]).unwrap(), ri(1));
        assert_eq!(
            p.probability_of(&[0, 3]),
            Err(ClassicalShadowError::IndexOutOfRange { index: 3, bound: 3 })
        );
    }

    #[test]
    fn expectation_is_linear_and_matches_a_hand_value() {
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let f = vec![ri(2), ri(-3), ri(6)];
        let g = vec![ri(1), ri(1), ri(1)];
        assert_eq!(p.expectation(&f).unwrap(), ri(1));
        assert_eq!(p.expectation(&g).unwrap(), ri(1));
        let combo: Vec<Rational> = f
            .iter()
            .zip(&g)
            .map(|(a, b)| ri(3) * a + ri(5) * b)
            .collect();
        assert_eq!(
            p.expectation(&combo).unwrap(),
            ri(3) * p.expectation(&f).unwrap() + ri(5) * p.expectation(&g).unwrap()
        );
        assert_eq!(
            p.expectation(&[ri(1)]),
            Err(ClassicalShadowError::DimensionMismatch {
                expected: 3,
                actual: 1
            })
        );
    }

    #[test]
    fn total_variation_is_the_largest_event_gap_on_every_grid_pair() {
        let all = grid_simplices(4, 4);
        for p in &all {
            for q in &all {
                let mut best = ri(0);
                for mask in 0u32..(1 << 4) {
                    let event: Vec<usize> = (0..4).filter(|i| mask >> i & 1 == 1).collect();
                    let gap = (p.probability_of(&event).unwrap()
                        - q.probability_of(&event).unwrap())
                    .abs();
                    if gap > best {
                        best = gap;
                    }
                }
                assert_eq!(
                    p.total_variation(q).unwrap(),
                    best,
                    "{:?} vs {:?}",
                    p.probs(),
                    q.probs()
                );
            }
        }
    }

    #[test]
    fn total_variation_is_a_metric_on_the_three_point_grid() {
        let all = grid_simplices(4, 3);
        for p in &all {
            assert_eq!(p.total_variation(p).unwrap(), ri(0));
            for q in &all {
                let d = p.total_variation(q).unwrap();
                assert_eq!(d, q.total_variation(p).unwrap(), "symmetry");
                assert!(d >= ri(0) && d <= ri(1), "range");
                assert_eq!(d.is_zero(), p == q, "zero iff equal");
                for r in &all {
                    assert!(
                        d <= p.total_variation(r).unwrap() + r.total_variation(q).unwrap(),
                        "triangle inequality"
                    );
                }
            }
        }
    }

    #[test]
    fn total_variation_of_disjoint_supports_is_one_and_sizes_must_agree() {
        let a = simplex(&[(1, 1), (0, 1)]);
        let b = simplex(&[(0, 1), (1, 1)]);
        assert_eq!(a.total_variation(&b).unwrap(), ri(1));
        let c = simplex(&[(1, 3), (1, 3), (1, 3)]);
        assert_eq!(
            a.total_variation(&c),
            Err(ClassicalShadowError::ShapeMismatch { left: 2, right: 3 })
        );
    }

    #[test]
    fn a_product_distribution_multiplies_masses_and_has_the_factors_as_marginals() {
        let p = simplex(&[(1, 4), (3, 4)]);
        let q = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let pq = p.product(&q).unwrap();
        assert_eq!(pq.n(), 6);
        for i in 0..2 {
            for j in 0..3 {
                assert_eq!(
                    pq.get(i * 3 + j).unwrap(),
                    &(p.get(i).unwrap() * q.get(j).unwrap())
                );
            }
        }
        for i in 0..2 {
            let row: Rational = (0..3).map(|j| pq.get(i * 3 + j).unwrap()).sum();
            assert_eq!(&row, p.get(i).unwrap());
        }
        for j in 0..3 {
            let col: Rational = (0..2).map(|i| pq.get(i * 3 + j).unwrap()).sum();
            assert_eq!(&col, q.get(j).unwrap());
        }
    }

    #[test]
    fn a_convex_combination_is_a_simplex_and_bad_weights_are_refused() {
        let a = simplex(&[(1, 1), (0, 1)]);
        let b = simplex(&[(0, 1), (1, 1)]);
        let mix =
            ProbabilitySimplex::convex_combination(&[(rq(1, 4), a.clone()), (rq(3, 4), b.clone())])
                .unwrap();
        assert_eq!(mix.probs(), &[rq(1, 4), rq(3, 4)]);
        assert_eq!(
            ProbabilitySimplex::convex_combination(&[]),
            Err(ClassicalShadowError::Empty)
        );
        assert_eq!(
            ProbabilitySimplex::convex_combination(&[
                (rq(3, 2), a.clone()),
                (rq(-1, 2), b.clone())
            ]),
            Err(ClassicalShadowError::NegativeEntry { index: 1 })
        );
        assert_eq!(
            ProbabilitySimplex::convex_combination(&[(rq(1, 2), a.clone()), (rq(1, 4), b)]),
            Err(ClassicalShadowError::NotNormalized { sum: rq(3, 4) })
        );
        let wide = simplex(&[(1, 3), (1, 3), (1, 3)]);
        assert_eq!(
            ProbabilitySimplex::convex_combination(&[(rq(1, 2), a), (rq(1, 2), wide)]),
            Err(ClassicalShadowError::ShapeMismatch { left: 2, right: 3 })
        );
    }

    #[test]
    fn power_sums_are_the_rational_moments_and_purity_is_the_second() {
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        assert_eq!(p.power_sum(0), ri(3));
        assert_eq!(p.power_sum(1), ri(1));
        assert_eq!(p.power_sum(2), rq(7, 18));
        assert_eq!(p.power_sum(3), rq(1, 6));
        let q = simplex(&[(1, 2), (1, 2), (0, 1)]);
        assert_eq!(q.power_sum(0), ri(2));
        assert_eq!(q.power_sum(2), rq(1, 2));
        for n in 1..=7usize {
            let u = ProbabilitySimplex::uniform(&carrier(n), "u").unwrap();
            assert_eq!(
                u.power_sum(2),
                Rational::new(BigInt::one(), BigInt::from(n))
            );
        }
    }

    #[test]
    fn rational_pow_agrees_with_repeated_multiplication() {
        let base = rq(-3, 5);
        let mut acc = ri(1);
        for e in 0..12u32 {
            assert_eq!(rational_pow(&base, e), acc, "exponent {e}");
            acc = &acc * &base;
        }
    }

    #[test]
    fn the_maximum_mass_and_the_dirac_and_uniform_tests_match_the_support() {
        let p = simplex(&[(1, 6), (1, 2), (1, 3)]);
        assert_eq!(p.max_probability(), rq(1, 2));
        assert!(!p.is_uniform());
        assert!(!p.is_dirac());
    }
}
