use crate::linear_algebra::involution::Involution;
use crate::linear_algebra::ordered::{HermitianOrdered, OrderedExactField};
use crate::linear_algebra::scalars::{ExactRing, Field};
use crate::linear_algebra::ExactFieldError;

fn violated(law: &'static str) -> Result<(), ExactFieldError> {
    Err(ExactFieldError::LawViolated { law })
}

pub fn check_field_axioms<F: Field + ExactRing>(samples: &[F]) -> Result<(), ExactFieldError> {
    let (zero, one) = (F::zero(), F::one());
    check_zero_and_one(&zero, &one)?;
    check_identities_and_inverses(samples, &zero, &one)?;
    check_commutativity_and_division(samples)?;
    check_associativity_and_distributivity(samples)
}

fn check_zero_and_one<F: Field + ExactRing>(zero: &F, one: &F) -> Result<(), ExactFieldError> {
    if !zero.try_is_zero()? {
        return violated("zero is zero");
    }
    if one == zero || one.try_is_zero()? {
        return violated("a field has 0 != 1");
    }
    Ok(())
}

fn check_identities_and_inverses<F: Field + ExactRing>(
    samples: &[F],
    zero: &F,
    one: &F,
) -> Result<(), ExactFieldError> {
    check_identities(samples, zero, one)?;
    check_inverses(samples, zero, one)
}

fn check_identities<F: Field + ExactRing>(
    samples: &[F],
    zero: &F,
    one: &F,
) -> Result<(), ExactFieldError> {
    check_additive_and_multiplicative_identity(samples, zero, one)?;
    check_additive_inverse_and_zero(samples, zero)
}

fn check_additive_and_multiplicative_identity<F: Field + ExactRing>(
    samples: &[F],
    zero: &F,
    one: &F,
) -> Result<(), ExactFieldError> {
    for a in samples {
        if a.try_add(zero)? != *a {
            return violated("0 is the additive identity");
        }
        if a.try_mul(one)? != *a {
            return violated("1 is the multiplicative identity");
        }
    }
    Ok(())
}

fn check_additive_inverse_and_zero<F: Field + ExactRing>(
    samples: &[F],
    zero: &F,
) -> Result<(), ExactFieldError> {
    for a in samples {
        let sum = a.try_add(&a.try_neg()?)?;
        if sum != *zero || !sum.try_is_zero()? {
            return violated("a + (-a) = 0");
        }
        if a.try_is_zero()? != (*a == *zero) {
            return violated("is_zero agrees with equality to zero");
        }
    }
    Ok(())
}

fn check_inverses<F: Field + ExactRing>(
    samples: &[F],
    _zero: &F,
    one: &F,
) -> Result<(), ExactFieldError> {
    for a in samples {
        check_single_inverse(a, one)?;
    }
    Ok(())
}

fn check_single_inverse<F: Field + ExactRing>(
    a: &F,
    one: &F,
) -> Result<(), ExactFieldError> {
    let is_zero = a.try_is_zero()?;
    let inv_res = a.try_inv();
    validate_inverse_result(a, one, is_zero, inv_res)
}

fn validate_inverse_result<F: Field + ExactRing>(
    a: &F,
    one: &F,
    is_zero: bool,
    inv_res: Result<F, crate::linear_algebra::scalars::ScalarError>,
) -> Result<(), ExactFieldError> {
    match inv_res {
        Err(crate::linear_algebra::scalars::ScalarError::DivisionByZero) => {
            if !is_zero {
                violated("every nonzero element has an inverse")
            } else {
                Ok(())
            }
        }
        Ok(inverse) => {
            if is_zero {
                violated("zero has no inverse")
            } else if a.try_mul(&inverse)? != *one {
                violated("a · a⁻¹ = 1")
            } else {
                Ok(())
            }
        }
        Err(error) => Err(error.into()),
    }
}

fn check_commutativity_and_division<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    check_commutativity(samples)?;
    check_division(samples)
}

fn check_commutativity<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            if a.try_add(b)? != b.try_add(a)? {
                return violated("addition is commutative");
            }
            if a.try_mul(b)? != b.try_mul(a)? {
                return violated("multiplication is commutative");
            }
        }
    }
    Ok(())
}

fn check_division<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            check_single_division(a, b)?;
        }
    }
    Ok(())
}

fn check_single_division<F: Field + ExactRing>(
    a: &F,
    b: &F,
) -> Result<(), ExactFieldError> {
    match (b.try_is_zero()?, a.try_div(b)) {
        (true, Ok(_)) => violated("division by zero is undefined"),
        (false, Err(crate::linear_algebra::scalars::ScalarError::DivisionByZero)) => {
            violated("division by a nonzero element is defined")
        }
        (false, Ok(quotient)) if quotient.try_mul(b)? != *a => {
            violated("(a / b) · b = a")
        }
        (true, Err(crate::linear_algebra::scalars::ScalarError::DivisionByZero)) => Ok(()),
        (_, Err(error)) => Err(error.into()),
        _ => Ok(()),
    }
}

fn check_associativity_and_distributivity<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    check_associativity(samples)?;
    check_distributivity(samples)
}

fn check_associativity<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    check_additive_associativity(samples)?;
    check_multiplicative_associativity(samples)
}

fn check_additive_associativity<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            for c in samples {
                if a.try_add(b)?.try_add(c)? != a.try_add(&b.try_add(c)?)? {
                    return violated("addition is associative");
                }
            }
        }
    }
    Ok(())
}

fn check_multiplicative_associativity<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            for c in samples {
                if a.try_mul(b)?.try_mul(c)? != a.try_mul(&b.try_mul(c)?)? {
                    return violated("multiplication is associative");
                }
            }
        }
    }
    Ok(())
}

fn check_distributivity<F: Field + ExactRing>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            for c in samples {
                if a.try_mul(&b.try_add(c)?)? != a.try_mul(b)?.try_add(&a.try_mul(c)?)? {
                    return violated("multiplication distributes over addition");
                }
            }
        }
    }
    Ok(())
}

pub fn check_involution_axioms<F: Involution>(samples: &[F]) -> Result<(), ExactFieldError> {
    check_involution_additive(samples)?;
    check_involution_multiplicative(samples)?;
    check_involution_involution(samples)
}

fn check_involution_additive<F: Involution>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            if a.try_add(b)?.try_conj()? != a.try_conj()?.try_add(&b.try_conj()?)? {
                return violated("conjugation is additive");
            }
        }
    }
    Ok(())
}

fn check_involution_multiplicative<F: Involution>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            if a.try_mul(b)?.try_conj()? != a.try_conj()?.try_mul(&b.try_conj()?)? {
                return violated("conjugation is multiplicative");
            }
        }
    }
    Ok(())
}

fn check_involution_involution<F: Involution>(samples: &[F]) -> Result<(), ExactFieldError> {
    if F::one().try_conj()? != F::one() {
        return violated("conjugation fixes 1");
    }
    for a in samples {
        if a.try_conj()?.try_conj()? != *a {
            return violated("conjugation has order at most two");
        }
    }
    Ok(())
}

pub fn check_ordered_axioms<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    check_ordered_signs(samples)?;
    check_ordered_cones(samples)
}

fn check_ordered_signs<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    check_ordered_sign_values(samples)?;
    check_ordered_sign_negations(samples)
}

fn check_ordered_sign_values<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        if !(-1..=1).contains(&a.try_signum()?) {
            return violated("a sign is -1, 0 or 1");
        }
        if (a.try_signum()? == 0) != a.try_is_zero()? {
            return violated("a sign is zero exactly for zero");
        }
    }
    Ok(())
}

fn check_ordered_sign_negations<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        if a.try_neg()?.try_signum()? != -a.try_signum()? {
            return violated("the sign of a negation is the negated sign");
        }
    }
    Ok(())
}

fn check_ordered_cones<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    check_ordered_positive_sums(samples)?;
    check_ordered_positive_products(samples)
}

fn check_ordered_positive_sums<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            if a.try_signum()? > 0 && b.try_signum()? > 0 && a.try_add(b)?.try_signum()? <= 0 {
                return violated("a sum of positive elements is positive");
            }
        }
    }
    Ok(())
}

fn check_ordered_positive_products<F: OrderedExactField>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        for b in samples {
            if a.try_signum()? > 0 && b.try_signum()? > 0 && a.try_mul(b)?.try_signum()? <= 0 {
                return violated("a product of positive elements is positive");
            }
        }
    }
    Ok(())
}

pub fn check_hermitian_ordered_axioms<F: HermitianOrdered>(
    samples: &[F],
) -> Result<(), ExactFieldError> {
    check_hermitian_sign_domain(samples)?;
    let fixed = collect_hermitian_fixed(samples)?;
    check_hermitian_fixed_negation(&fixed)?;
    check_hermitian_fixed_cones(&fixed)?;
    check_hermitian_norms(samples)
}

fn check_hermitian_sign_domain<F: HermitianOrdered>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        check_single_hermitian_sign(a)?;
    }
    Ok(())
}

fn check_single_hermitian_sign<F: HermitianOrdered>(a: &F) -> Result<(), ExactFieldError> {
    let fixed = a.try_conj()? == *a;
    let sign_opt = a.try_fixed_field_sign()?;
    let is_zero = a.try_is_zero()?;
    validate_hermitian_sign(fixed, sign_opt, is_zero)
}

fn validate_hermitian_sign(
    fixed: bool,
    sign_opt: Option<i8>,
    is_zero: bool,
) -> Result<(), ExactFieldError> {
    match sign_opt {
        None if fixed => violated("fixed_field_sign is None exactly for non-fixed elements"),
        Some(_) if !fixed => violated("fixed_field_sign is None exactly for non-fixed elements"),
        Some(sign) if !(-1..=1).contains(&sign) => violated("a fixed-field sign is -1, 0 or 1"),
        Some(sign) if (sign == 0) != is_zero => {
            violated("a fixed-field sign is zero exactly for zero")
        }
        _ => Ok(()),
    }
}

fn collect_hermitian_fixed<F: HermitianOrdered>(samples: &[F]) -> Result<Vec<&F>, ExactFieldError> {
    let mut fixed: Vec<&F> = super::reserve(samples.len())?;
    for a in samples {
        if a.try_conj()? == *a {
            fixed.push(a);
        }
    }
    Ok(fixed)
}

fn check_hermitian_fixed_negation<F: HermitianOrdered>(fixed: &[&F]) -> Result<(), ExactFieldError> {
    for a in fixed {
        if a.try_neg()?.try_fixed_field_sign()? != a.try_fixed_field_sign()?.map(|s| -s) {
            return violated("the sign of a negation is the negated sign on the fixed field");
        }
    }
    Ok(())
}

fn check_hermitian_fixed_cones<F: HermitianOrdered>(fixed: &[&F]) -> Result<(), ExactFieldError> {
    check_hermitian_fixed_sums(fixed)?;
    check_hermitian_fixed_products(fixed)
}

fn check_hermitian_fixed_sums<F: HermitianOrdered>(fixed: &[&F]) -> Result<(), ExactFieldError> {
    for a in fixed {
        for b in fixed {
            if a.try_fixed_field_sign()? == Some(1) && b.try_fixed_field_sign()? == Some(1) {
                if a.try_add(b)?.try_fixed_field_sign()? != Some(1) {
                    return violated("a sum of positive fixed elements is positive");
                }
            }
        }
    }
    Ok(())
}

fn check_hermitian_fixed_products<F: HermitianOrdered>(fixed: &[&F]) -> Result<(), ExactFieldError> {
    for a in fixed {
        for b in fixed {
            if a.try_fixed_field_sign()? == Some(1) && b.try_fixed_field_sign()? == Some(1) {
                if a.try_mul(b)?.try_fixed_field_sign()? != Some(1) {
                    return violated("a product of positive fixed elements is positive");
                }
            }
        }
    }
    Ok(())
}

fn check_hermitian_norms<F: HermitianOrdered>(samples: &[F]) -> Result<(), ExactFieldError> {
    for a in samples {
        check_single_hermitian_norm(a)?;
    }
    Ok(())
}

fn check_single_hermitian_norm<F: HermitianOrdered>(a: &F) -> Result<(), ExactFieldError> {
    let norm = a.try_mul(&a.try_conj()?)?;
    match norm.try_fixed_field_sign()? {
        Some(0) if a.try_is_zero()? => Ok(()),
        Some(1) if !a.try_is_zero()? => Ok(()),
        _ => violated("a norm x · conj(x) is nonnegative and zero only for zero"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::test_support::{
        gi, gq, q, qs, qsi, Fp, GaussianRational, QSqrt2, Shaky, Z6,
    };
    use num_rational::BigRational;

    fn rationals() -> Vec<BigRational> {
        vec![
            q(0, 1),
            q(1, 1),
            q(-1, 1),
            q(1, 2),
            q(-3, 7),
            q(22, 5),
            q(-10, 3),
        ]
    }

    fn assert_law(result: Result<(), ExactFieldError>, law: &'static str) {
        assert_eq!(result, Err(ExactFieldError::LawViolated { law }));
    }

    #[test]
    fn bigrational_satisfies_the_field_involution_and_order_obligations() {
        let s = rationals();
        check_field_axioms(&s).unwrap();
        check_involution_axioms(&s).unwrap();
        check_ordered_axioms(&s).unwrap();
        check_hermitian_ordered_axioms(&s).unwrap();
    }

    #[test]
    fn finite_fields_satisfy_the_field_axioms_and_the_identity_is_an_involution() {
        fn all<const P: u64>() -> Vec<Fp<P>> {
            (0..P as i64).map(Fp::<P>::new).collect()
        }
        check_field_axioms(&all::<2>()).unwrap();
        check_field_axioms(&all::<3>()).unwrap();
        check_field_axioms(&all::<7>()).unwrap();
        check_involution_axioms(&all::<7>()).unwrap();
    }

    #[test]
    fn the_gaussian_rationals_and_q_sqrt2_satisfy_their_obligations() {
        let g: Vec<GaussianRational> = vec![
            gi(0, 0),
            gi(1, 0),
            gi(0, 1),
            gi(-2, 3),
            gq(q(1, 2), q(-3, 5)),
            gq(q(7, 3), q(2, 7)),
        ];
        check_field_axioms(&g).unwrap();
        check_involution_axioms(&g).unwrap();
        check_hermitian_ordered_axioms(&g).unwrap();

        let s: Vec<QSqrt2> = vec![
            qsi(0, 0),
            qsi(1, 0),
            qsi(0, 1),
            qsi(1, -1),
            qsi(3, -2),
            qs(q(1, 2), q(-3, 5)),
            qsi(-5, 4),
        ];
        check_field_axioms(&s).unwrap();
        check_involution_axioms(&s).unwrap();
        check_ordered_axioms(&s).unwrap();
        check_hermitian_ordered_axioms(&s).unwrap();
    }

    #[test]
    fn a_ring_with_zero_divisors_fails_the_field_axioms() {
        let all: Vec<Z6> = (0..6).map(Z6::new).collect();
        assert_law(
            check_field_axioms(&all),
            "every nonzero element has an inverse",
        );
    }

    #[test]
    fn a_wrong_inverse_is_caught_and_named() {
        let s: Vec<Shaky<8>> = [0, 1, 2].iter().map(|&x| Shaky::<8>(q(x, 1))).collect();
        assert_law(check_field_axioms(&s), "a · a⁻¹ = 1");
    }

    #[test]
    fn a_defective_involution_is_caught_and_named() {
        let s = |v: &[i64]| -> Vec<Shaky<3>> { v.iter().map(|&x| Shaky::<3>(q(x, 1))).collect() };
        assert_law(
            check_involution_axioms(&s(&[0, 1, 2])),
            "conjugation is additive",
        );
        let t: Vec<Shaky<4>> = [1, 2, 3].iter().map(|&x| Shaky::<4>(q(x, 1))).collect();
        assert_law(check_involution_axioms(&t), "conjugation is multiplicative");
        let none: Vec<Shaky<4>> = Vec::new();
        assert_law(check_involution_axioms(&none), "conjugation fixes 1");
    }

    #[test]
    fn a_defective_order_is_caught_and_named() {
        let pos = |v: &[i64]| v.iter().map(|&x| q(x, 1)).collect::<Vec<_>>();
        let s1: Vec<Shaky<1>> = pos(&[0, 1, -1]).into_iter().map(Shaky::<1>).collect();
        assert_law(check_ordered_axioms(&s1), "a sign is -1, 0 or 1");
        let s2: Vec<Shaky<2>> = pos(&[0, 1, -1]).into_iter().map(Shaky::<2>).collect();
        assert_law(check_ordered_axioms(&s2), "a sign is zero exactly for zero");
        let s7: Vec<Shaky<7>> = pos(&[0, 1, -1]).into_iter().map(Shaky::<7>).collect();
        assert_law(
            check_ordered_axioms(&s7),
            "the sign of a negation is the negated sign",
        );
    }

    #[test]
    fn a_defective_hermitian_sign_is_caught_and_named() {
        let s5: Vec<Shaky<5>> = [0, 1, -1].iter().map(|&x| Shaky::<5>(q(x, 1))).collect();
        assert_law(
            check_hermitian_ordered_axioms(&s5),
            "fixed_field_sign is None exactly for non-fixed elements",
        );
        let s6: Vec<Shaky<6>> = [0, 1, -1].iter().map(|&x| Shaky::<6>(q(x, 1))).collect();
        assert_law(
            check_hermitian_ordered_axioms(&s6),
            "a fixed-field sign is -1, 0 or 1",
        );
    }

    #[test]
    fn a_negative_norm_violates_the_hermitian_order_obligations() {
        #[derive(Debug, Clone, PartialEq, Eq)]
        struct Galois(QSqrt2);
        use crate::linear_algebra::scalars::{Ring, Semiring};
        impl Semiring for Galois {
            fn zero() -> Self {
                Galois(<QSqrt2 as Semiring>::zero())
            }
            fn one() -> Self {
                Galois(<QSqrt2 as Semiring>::one())
            }
            fn try_add(&self, rhs: &Self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| Galois(Semiring::try_add(&self.0, &rhs.0).unwrap()))())
            }
            fn try_mul(&self, rhs: &Self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| Galois(Semiring::try_mul(&self.0, &rhs.0).unwrap()))())
            }
            fn try_is_zero(&self) -> crate::linear_algebra::scalars::ScalarResult<bool> {
                Ok((|| Semiring::try_is_zero(&self.0).unwrap())())
            }

            fn validate(&self) -> crate::linear_algebra::scalars::ScalarResult<()> {
                Ok(())
            }
        }
        impl Ring for Galois {
            fn try_neg(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| Galois(Ring::try_neg(&self.0).unwrap()))())
            }
        }
        impl Field for Galois {
            fn try_inv(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                self.0.try_inv().map(Galois)
            }
        }
        impl ExactRing for Galois {}
        impl Involution for Galois {
            fn try_conj(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| Galois(qs(self.0.a.clone(), -self.0.b.clone())))())
            }
        }
        impl HermitianOrdered for Galois {
            fn try_fixed_field_sign(
                &self,
            ) -> crate::linear_algebra::scalars::ScalarResult<Option<i8>> {
                Ok((|| {
                    if num_traits::Zero::is_zero(&self.0.b) {
                        Some(crate::linear_algebra::test_support::sign_of_rational(
                            &self.0.a,
                        ))
                    } else {
                        None
                    }
                })())
            }
        }
        let samples: Vec<Galois> = vec![
            Galois(qsi(0, 0)),
            Galois(qsi(1, 0)),
            Galois(qsi(0, 1)),
            Galois(qsi(2, 0)),
        ];
        check_field_axioms(&samples).unwrap();
        check_involution_axioms(&samples).unwrap();
        assert_law(
            check_hermitian_ordered_axioms(&samples),
            "a norm x · conj(x) is nonnegative and zero only for zero",
        );
    }

    #[test]
    fn a_false_zero_does_not_excuse_a_broken_additive_inverse() {
        #[derive(Clone, Debug, PartialEq, Eq)]
        struct Defect(BigRational);
        use crate::linear_algebra::scalars::{Ring, Semiring};
        impl Semiring for Defect {
            fn zero() -> Self {
                Defect(q(0, 1))
            }
            fn one() -> Self {
                Defect(q(1, 1))
            }
            fn try_add(&self, rhs: &Self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| Defect(&self.0 + &rhs.0))())
            }
            fn try_mul(&self, rhs: &Self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| Defect(&self.0 * &rhs.0))())
            }
            fn try_is_zero(&self) -> crate::linear_algebra::scalars::ScalarResult<bool> {
                Ok((|| self.0 == q(0, 1) || self.0 == q(42, 1))())
            }

            fn validate(&self) -> crate::linear_algebra::scalars::ScalarResult<()> {
                Ok(())
            }
        }
        impl Ring for Defect {
            fn try_neg(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| {
                    if self.0 == q(2, 1) {
                        Defect(q(40, 1))
                    } else {
                        Defect(-&self.0)
                    }
                })())
            }
        }
        impl Field for Defect {
            fn try_inv(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                (|| -> Option<Self> {
                    if self.try_is_zero().unwrap() {
                        None
                    } else {
                        Some(Defect(self.0.clone().recip()))
                    }
                })()
                .ok_or(crate::linear_algebra::scalars::ScalarError::DivisionByZero)
            }
        }
        impl ExactRing for Defect {}
        let samples = [-1, 0, 1, 2].map(|n| Defect(q(n, 1)));
        assert_law(check_field_axioms(&samples), "a + (-a) = 0");
    }

    #[test]
    fn a_norm_sign_of_two_is_not_nonnegative_unit_sign() {
        #[derive(Clone, Debug, PartialEq, Eq)]
        struct SignAtNine(BigRational);
        use crate::linear_algebra::scalars::{Ring, Semiring};
        impl Semiring for SignAtNine {
            fn zero() -> Self {
                SignAtNine(q(0, 1))
            }
            fn one() -> Self {
                SignAtNine(q(1, 1))
            }
            fn try_add(&self, rhs: &Self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| SignAtNine(&self.0 + &rhs.0))())
            }
            fn try_mul(&self, rhs: &Self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| SignAtNine(&self.0 * &rhs.0))())
            }
            fn try_is_zero(&self) -> crate::linear_algebra::scalars::ScalarResult<bool> {
                Ok((|| num_traits::Zero::is_zero(&self.0))())
            }

            fn validate(&self) -> crate::linear_algebra::scalars::ScalarResult<()> {
                Ok(())
            }
        }
        impl Ring for SignAtNine {
            fn try_neg(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| SignAtNine(-&self.0))())
            }
        }
        impl Field for SignAtNine {
            fn try_inv(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                (|| -> Option<Self> {
                    if self.try_is_zero().unwrap() {
                        None
                    } else {
                        Some(SignAtNine(self.0.clone().recip()))
                    }
                })()
                .ok_or(crate::linear_algebra::scalars::ScalarError::DivisionByZero)
            }
        }
        impl ExactRing for SignAtNine {}
        impl Involution for SignAtNine {
            fn try_conj(&self) -> crate::linear_algebra::scalars::ScalarResult<Self> {
                Ok((|| self.clone())())
            }
        }
        impl HermitianOrdered for SignAtNine {
            fn try_fixed_field_sign(
                &self,
            ) -> crate::linear_algebra::scalars::ScalarResult<Option<i8>> {
                Ok((|| {
                    if self.0 == q(9, 1) {
                        Some(2)
                    } else {
                        Some(crate::linear_algebra::test_support::sign_of_rational(
                            &self.0,
                        ))
                    }
                })())
            }
        }
        let samples = [0, 1, -1, -3].map(|n| SignAtNine(q(n, 1)));
        assert_law(
            check_hermitian_ordered_axioms(&samples),
            "a norm x · conj(x) is nonnegative and zero only for zero",
        );
    }
}
