//! Canonical finite sums of normalized real radicals. AuthorityEffect: None.
use crate::quadratic::Surd;
use crate::rational::Rational;
use num_bigint::BigInt;
use num_traits::Zero;
use std::collections::BTreeMap;
/// An exact finite sum `sum c_r sqrt(r)` over distinct squarefree radicands.
/// Such sums are equal exactly when their coefficients are, because square roots
/// of distinct squarefree integers are linearly independent over `Q`.
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SurdSum {
    terms: BTreeMap<BigInt, Rational>,
}

impl SurdSum {
    pub fn terms(&self) -> &BTreeMap<BigInt, Rational> {
        &self.terms
    }
    pub fn add_surd(&mut self, surd: &Surd) {
        if surd.is_zero() {
            return;
        }
        let entry = self
            .terms
            .entry(surd.radicand().clone())
            .or_insert_with(Rational::zero);
        *entry = &*entry + surd.coefficient();
        if entry.is_zero() {
            self.terms.remove(surd.radicand());
        }
    }

    /// The value when it is rational (only the radicand `1` survives).
    pub fn as_rational(&self) -> Option<Rational> {
        match self.terms.len() {
            0 => Some(Rational::zero()),
            1 => self.terms.get(&BigInt::from(1)).cloned(),
            _ => None,
        }
    }
}

#[cfg(test)]
mod dynamics_laws {

    use super::*;
    use crate::rational::{ri, rq};
    #[test]
    fn normalized_radicals_coalesce_and_exact_cancellation_is_rational() {
        let mut sum = SurdSum::default();
        sum.add_surd(&Surd::new(ri(1), &ri(8)).unwrap());
        sum.add_surd(&Surd::new(ri(-2), &ri(2)).unwrap());
        assert_eq!(sum.as_rational(), Some(ri(0)));
        sum.add_surd(&Surd::new(rq(1, 3), &ri(9)).unwrap());
        assert_eq!(sum.as_rational(), Some(ri(1)));
        sum.add_surd(&Surd::new(ri(1), &ri(3)).unwrap());
        assert_eq!(sum.as_rational(), None);
    }
}
