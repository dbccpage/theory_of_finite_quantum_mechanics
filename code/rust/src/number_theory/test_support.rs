
use linear_algebra::scalars::{ExactRing, Field};

pub(crate) fn check_field_axioms<F: Field + ExactRing>(samples: &[F]) {
    let zero = F::zero();
    let one = F::one();
    assert!(zero.is_zero(), "zero is zero");
    assert!(!one.is_zero(), "one is not zero");
    for a in samples {
        assert_eq!(a.add(&zero), *a, "additive identity");
        assert_eq!(a.mul(&one), *a, "multiplicative identity");
        assert!(a.mul(&zero).is_zero(), "multiplication by zero");
        assert!(a.add(&a.neg()).is_zero(), "additive inverse");
        assert_eq!(a.sub(a), zero, "a - a = 0");
        assert_eq!(a.neg().neg(), *a, "double negation");
        if a.is_zero() {
            assert!(a.try_inv().is_none(), "zero has no inverse");
            assert!(one.try_div(a).is_none(), "division by zero is refused");
        } else {
            let inverse = a.try_inv().expect("a nonzero element is invertible");
            assert_eq!(a.mul(&inverse), one, "a * a^-1 = 1");
            assert_eq!(inverse.mul(a), one, "a^-1 * a = 1");
            assert_eq!(a.try_div(a), Some(one.clone()), "a / a = 1");
            assert_eq!(inverse.try_inv().as_ref(), Some(a), "(a^-1)^-1 = a");
        }
        for b in samples {
            assert_eq!(a.add(b), b.add(a), "commutative addition");
            assert_eq!(a.mul(b), b.mul(a), "commutative multiplication");
            assert_eq!(
                a.sub(b),
                a.add(&b.neg()),
                "subtraction is adding the negative"
            );
            if !b.is_zero() {
                let quotient = a.try_div(b).expect("division by a nonzero element");
                assert_eq!(quotient.mul(b), *a, "(a / b) * b = a");
            }
            for c in samples {
                assert_eq!(a.add(b).add(c), a.add(&b.add(c)), "associative addition");
                assert_eq!(
                    a.mul(b).mul(c),
                    a.mul(&b.mul(c)),
                    "associative multiplication"
                );
                assert_eq!(a.mul(&b.add(c)), a.mul(b).add(&a.mul(c)), "distributivity");
            }
        }
    }
}

pub(crate) struct Lcg(u64);

impl Lcg {
    pub(crate) fn new(seed: u64) -> Self {
        Self(seed)
    }

    pub(crate) fn next_signed(&mut self, bound: i64) -> i64 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let span = u64::try_from(2 * bound + 1).expect("bound is non-negative");
        i64::try_from((self.0 >> 33) % span).expect("fits") - bound
    }

    pub(crate) fn next_below(&mut self, bound: u64) -> u64 {
        self.0 = self
            .0
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        (self.0 >> 33) % bound
    }
}
