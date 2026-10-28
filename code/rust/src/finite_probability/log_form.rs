
use std::cmp::Ordering;
use std::collections::BTreeMap;

use num_bigint::{BigInt, BigUint};

use num_traits::{One, Signed, ToPrimitive, Zero};
use engine_kernel::elementary::{ln_enclosure, ElementaryError};
use engine_kernel::interval::Interval;
use tfqm_number_theory::integer_factorization::{
    factor_natural, is_prime_u64, FactorizationBudget, FactorizationError,
};
use tfqm_number_theory::rational::Rational;

use crate::error::ClassicalShadowError;
use crate::joint_table::{JointTable, WeightTableError};
use crate::simplex::ProbabilitySimplex;

pub const DEFAULT_FACTOR_BOUND: u32 = 1_000_000;

pub const MAX_FACTOR_BOUND: u32 = 10_000_000;

pub const MAX_ENCLOSURE_BITS: u32 = 2048;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum LogFormError {
    #[error("the logarithm of a non-positive number is undefined")]
    NonPositiveArgument,
    #[error(transparent)]
    Factorization(#[from] FactorizationError),
    #[error("the exact logarithm basis requires a prime representable in u64, got {bits} bits")]
    PrimeTooLarge { bits: u64 },
    #[error(
        "the factorisation of a {bits}-bit integer is undecided: no prime factor up to {bound} \
         remains, but the cofactor is not below {bound}^2 and is not a 64-bit prime"
    )]
    FactorisationUndecided { bits: u64, bound: u32 },
    #[error("factorization operation budget {bound} exceeds the supported maximum {max}")]
    BoundTooLarge { bound: u32, max: u32 },
    #[error("{value} is not prime")]
    NotPrime { value: u64 },
    #[error("the relative entropy is infinite: q_{index} = 0 while p_{index} > 0")]
    InfiniteRelativeEntropy { index: usize },
    #[error("distributions of sizes {left} and {right} cannot be compared")]
    SizeMismatch { left: usize, right: usize },
    #[error("precision {requested} bits exceeds the limit {limit}")]
    PrecisionTooLarge { requested: u32, limit: u32 },
    #[error("the sign of the difference is undecided at {bits} bits")]
    SignUndecided { bits: u32 },
    #[error("an enclosure had misordered endpoints")]
    InconsistentEnclosure,
    #[error(transparent)]
    Elementary(#[from] ElementaryError),
    #[error("probability refusal: {0}")]
    Probability(#[from] ClassicalShadowError),
    #[error("table refusal: {0}")]
    Table(#[from] WeightTableError),
}


fn round_outward(lo: &Rational, hi: &Rational, fractional_bits: u32) -> (Rational, Rational) {
    let scale = BigInt::one() << fractional_bits;
    let factor = Rational::from_integer(scale.clone());
    let scaled_lo = (lo * &factor).floor().to_integer();
    let scaled_hi = (hi * &factor).ceil().to_integer();
    (
        Rational::new(scaled_lo, scale.clone()),
        Rational::new(scaled_hi, scale),
    )
}


#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct LogForm {
    terms: BTreeMap<u64, Rational>,
}

impl LogForm {
    pub fn zero() -> Self {
        Self::default()
    }

    pub fn ln_of_prime(prime: u64) -> Result<Self, LogFormError> {
        if !is_prime_u64(prime, FactorizationBudget::default())? {
            return Err(LogFormError::NotPrime { value: prime });
        }
        let mut terms = BTreeMap::new();
        terms.insert(prime, Rational::one());
        Ok(Self { terms })
    }

    pub fn ln_of_positive_integer(n: &BigUint, bound: u32) -> Result<Self, LogFormError> {
        if bound > MAX_FACTOR_BOUND {
            return Err(LogFormError::BoundTooLarge {
                bound,
                max: MAX_FACTOR_BOUND,
            });
        }
        if n.is_zero() {
            return Err(LogFormError::NonPositiveArgument);
        }
        let factors = factor_natural(
            n,
            FactorizationBudget {
                max_operations: u64::from(bound),
            },
        )?;
        let mut terms = BTreeMap::new();
        for (prime, exponent) in factors {
            let key = prime
                .to_u64()
                .ok_or(LogFormError::PrimeTooLarge { bits: prime.bits() })?;
            terms.insert(key, Rational::from_integer(BigInt::from(exponent)));
        }
        Ok(Self { terms })
    }

    pub fn ln_of_positive_rational(q: &Rational, bound: u32) -> Result<Self, LogFormError> {
        if !q.is_positive() {
            return Err(LogFormError::NonPositiveArgument);
        }
        let q = q.reduced();
        let numerator = LogForm::ln_of_positive_integer(q.numer().magnitude(), bound)?;
        let denominator = LogForm::ln_of_positive_integer(q.denom().magnitude(), bound)?;
        Ok(numerator.sub(&denominator))
    }

    pub fn is_zero(&self) -> bool {
        self.terms.is_empty()
    }

    pub fn terms(&self) -> &BTreeMap<u64, Rational> {
        &self.terms
    }

    pub fn coefficient(&self, prime: u64) -> Rational {
        self.terms
            .get(&prime)
            .cloned()
            .unwrap_or_else(Rational::zero)
    }

    pub fn add(&self, other: &Self) -> Self {
        let mut terms = self.terms.clone();
        for (prime, coefficient) in &other.terms {
            add_term(&mut terms, *prime, coefficient);
        }
        Self { terms }
    }

    pub fn sub(&self, other: &Self) -> Self {
        self.add(&other.neg())
    }

    pub fn neg(&self) -> Self {
        Self {
            terms: self.terms.iter().map(|(p, c)| (*p, -c)).collect(),
        }
    }

    pub fn scale(&self, k: &Rational) -> Self {
        if k.is_zero() {
            return Self::zero();
        }
        Self {
            terms: self.terms.iter().map(|(p, c)| (*p, c * k)).collect(),
        }
    }

    pub fn enclosure(&self, bits: u32) -> Result<Interval, LogFormError> {
        if bits > MAX_ENCLOSURE_BITS {
            return Err(LogFormError::PrecisionTooLarge {
                requested: bits,
                limit: MAX_ENCLOSURE_BITS,
            });
        }
        if self.terms.is_empty() {
            return Ok(Interval::point(Rational::zero()));
        }
        let gamma_total: Rational = self.terms.values().map(Signed::abs).sum();
        let g = gamma_total.ceil().to_integer().bits();
        let per_prime_bits = u32::try_from(u64::from(bits) + g + 1).map_err(|_| {
            LogFormError::PrecisionTooLarge {
                requested: bits,
                limit: MAX_ENCLOSURE_BITS,
            }
        })?;
        let mut total = Interval::point(Rational::zero());
        for (prime, gamma) in &self.terms {
            let ln_prime = ln_enclosure(
                &Rational::from_integer(BigInt::from(*prime)),
                per_prime_bits,
            )?;
            total = total.add(&ln_prime.mul_scalar(gamma));
        }
        let (lo, hi) = round_outward(total.lo(), total.hi(), bits + 2);
        Interval::try_new(lo, hi).map_err(|_| LogFormError::InconsistentEnclosure)
    }

    pub fn compare(&self, other: &Self, max_bits: u32) -> Result<Ordering, LogFormError> {
        if self == other {
            return Ok(Ordering::Equal);
        }
        let difference = self.sub(other);
        let mut bits = 16u32.min(max_bits);
        loop {
            let enclosure = difference.enclosure(bits)?;
            if enclosure.lo().is_positive() {
                return Ok(Ordering::Greater);
            }
            if enclosure.hi().is_negative() {
                return Ok(Ordering::Less);
            }
            if bits >= max_bits {
                return Err(LogFormError::SignUndecided { bits });
            }
            bits = bits.saturating_mul(2).min(max_bits);
        }
    }
}

fn add_term(terms: &mut BTreeMap<u64, Rational>, prime: u64, coefficient: &Rational) {
    let entry = terms.entry(prime).or_insert_with(Rational::zero);
    *entry += coefficient;
    if entry.is_zero() {
        terms.remove(&prime);
    }
}


pub fn shannon_entropy_form(p: &ProbabilitySimplex) -> Result<LogForm, LogFormError> {
    shannon_entropy_form_with_bound(p, DEFAULT_FACTOR_BOUND)
}

pub fn shannon_entropy_form_with_bound(
    p: &ProbabilitySimplex,
    bound: u32,
) -> Result<LogForm, LogFormError> {
    let mut form = LogForm::zero();
    for mass in p.probs().iter().filter(|m| m.is_positive()) {
        let ln_mass = LogForm::ln_of_positive_rational(mass, bound)?;
        form = form.sub(&ln_mass.scale(mass));
    }
    Ok(form)
}

pub fn relative_entropy_form(
    p: &ProbabilitySimplex,
    q: &ProbabilitySimplex,
) -> Result<LogForm, LogFormError> {
    relative_entropy_form_with_bound(p, q, DEFAULT_FACTOR_BOUND)
}

pub fn relative_entropy_form_with_bound(
    p: &ProbabilitySimplex,
    q: &ProbabilitySimplex,
    bound: u32,
) -> Result<LogForm, LogFormError> {
    if p.n() != q.n() {
        return Err(LogFormError::SizeMismatch {
            left: p.n(),
            right: q.n(),
        });
    }
    let mut form = LogForm::zero();
    for (index, (mass_p, mass_q)) in p.probs().iter().zip(q.probs()).enumerate() {
        if !mass_p.is_positive() {
            continue;
        }
        if !mass_q.is_positive() {
            return Err(LogFormError::InfiniteRelativeEntropy { index });
        }
        let log_ratio = LogForm::ln_of_positive_rational(&(mass_p / mass_q), bound)?;
        form = form.add(&log_ratio.scale(mass_p));
    }
    Ok(form)
}

pub fn renyi_entropy_form(p: &ProbabilitySimplex, alpha: u32) -> Result<LogForm, LogFormError> {
    renyi_entropy_form_with_bound(p, alpha, DEFAULT_FACTOR_BOUND)
}

pub fn renyi_entropy_form_with_bound(
    p: &ProbabilitySimplex,
    alpha: u32,
    bound: u32,
) -> Result<LogForm, LogFormError> {
    match alpha {
        0 => LogForm::ln_of_positive_integer(&BigUint::from(p.support_size()), bound),
        1 => shannon_entropy_form_with_bound(p, bound),
        _ => {
            let trace = p.power_sum(alpha);
            let order = Rational::new(BigInt::one(), BigInt::from(1) - BigInt::from(alpha));
            Ok(LogForm::ln_of_positive_rational(&trace, bound)?.scale(&order))
        }
    }
}

pub fn min_entropy_form(p: &ProbabilitySimplex) -> Result<LogForm, LogFormError> {
    Ok(LogForm::ln_of_positive_rational(&p.max_probability(), DEFAULT_FACTOR_BOUND)?.neg())
}

pub fn joint_entropy_form(table: &JointTable) -> Result<LogForm, LogFormError> {
    shannon_entropy_form(&table.to_simplex()?)
}

pub fn conditional_entropy_form(table: &JointTable) -> Result<LogForm, LogFormError> {
    let joint = joint_entropy_form(table)?;
    let marginal = shannon_entropy_form(&table.marginal_distribution_a()?)?;
    Ok(joint.sub(&marginal))
}

pub fn total_correlation_form(table: &JointTable) -> Result<LogForm, LogFormError> {
    let ha = shannon_entropy_form(&table.marginal_distribution_a()?)?;
    let hb = shannon_entropy_form(&table.marginal_distribution_b()?)?;
    Ok(ha.add(&hb).sub(&joint_entropy_form(table)?))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::{grid_simplices, simplex};
    use tfqm_number_theory::rational::{ri, rq};

    fn decimal(text: &str) -> Rational {
        let (whole, fraction) = text.split_once('.').unwrap_or((text, ""));
        let digits = format!("{whole}{fraction}");
        let numerator: BigInt = digits.parse().unwrap();
        Rational::new(
            numerator,
            BigInt::from(10u8).pow(u32::try_from(fraction.len()).unwrap()),
        )
    }

    fn big(n: u64) -> BigUint {
        BigUint::from(n)
    }

    fn assert_value(form: &LogForm, bits: u32, reference: &str) {
        let enclosure = form.enclosure(bits).unwrap();
        let value = decimal(reference);
        let slack = Rational::new(BigInt::one(), BigInt::from(10u8).pow(40));
        assert!(
            enclosure.diam() <= Rational::new(BigInt::one(), BigInt::one() << bits),
            "width {} at {bits} bits",
            enclosure.diam()
        );
        assert!(
            enclosure.lo() <= &(&value + &slack) && enclosure.hi() >= &(&value - &slack),
            "enclosure [{}, {}] misses {reference}",
            enclosure.lo(),
            enclosure.hi()
        );
    }

    fn assert_factors(n: u64, expected: &[(u64, u32)]) {
        let form = LogForm::ln_of_positive_integer(&big(n), DEFAULT_FACTOR_BOUND).unwrap();
        let expected: BTreeMap<u64, Rational> = expected
            .iter()
            .map(|(p, e)| (*p, Rational::from_integer((*e).into())))
            .collect();
        assert_eq!(form.terms(), &expected);
    }
    #[test]
    fn small_integers_factor_into_the_expected_primes() {
        for (n, factors) in [
            (1, vec![]),
            (360, vec![(2, 3), (3, 2), (5, 1)]),
            (1001, vec![(7, 1), (11, 1), (13, 1)]),
            (1 << 40, vec![(2, 40)]),
        ] {
            assert_factors(n, &factors);
        }
    }
    #[test]
    fn the_factors_multiply_back_and_each_is_prime_for_every_integer_up_to_five_thousand() {
        for n in 1u64..=5000 {
            let f = LogForm::ln_of_positive_integer(&big(n), DEFAULT_FACTOR_BOUND).unwrap();
            let mut product = BigUint::one();
            for (p, e) in f.terms() {
                assert!(e.is_integer());
                let exponent = e.to_integer().to_u32().unwrap();
                product *= BigUint::from(*p).pow(exponent);
                assert!(is_prime_u64(*p, FactorizationBudget::default()).unwrap());
            }
            assert_eq!(product, big(n));
        }
    }
    #[test]
    fn a_cofactor_above_the_bound_squared_is_decided_by_miller_rabin_when_it_fits_64_bits() {
        let mersenne = (1u64 << 61) - 1;
        assert_factors(mersenne, &[(mersenne, 1)]);
        assert_factors(3 * 1_000_003, &[(3, 1), (1_000_003, 1)]);
    }
    #[test]
    fn an_undecidable_cofactor_is_refused_and_a_larger_bound_decides_it() {
        let semiprime = big(1_000_003u64 * 1_000_033);
        assert!(matches!(
            LogForm::ln_of_positive_integer(&semiprime, 1),
            Err(LogFormError::Factorization(
                FactorizationError::Exhausted { .. }
            ))
        ));
        assert_factors(1_000_003u64 * 1_000_033, &[(1_000_003, 1), (1_000_033, 1)]);
        let huge = BigUint::from(10u8).pow(40) + 1u8;
        assert!(matches!(
            LogForm::ln_of_positive_integer(&huge, 10),
            Err(LogFormError::Factorization(
                FactorizationError::Exhausted { .. }
            ))
        ));
    }
    #[test]
    fn zero_has_no_factorisation_and_an_excessive_bound_is_refused() {
        assert_eq!(
            LogForm::ln_of_positive_integer(&big(0), 100),
            Err(LogFormError::NonPositiveArgument)
        );
        assert_eq!(
            LogForm::ln_of_positive_integer(&big(12), MAX_FACTOR_BOUND + 1),
            Err(LogFormError::BoundTooLarge {
                bound: MAX_FACTOR_BOUND + 1,
                max: MAX_FACTOR_BOUND
            })
        );
    }
    #[test]
    fn the_miller_rabin_test_agrees_with_trial_division_below_ten_thousand_and_on_strong_pseudoprimes(
    ) {
        for n in 0u64..10_000 {
            let by_division = n >= 2 && (2..n).take_while(|d| d * d <= n).all(|d| n % d != 0);
            assert_eq!(
                is_prime_u64(n, FactorizationBudget::default()).unwrap(),
                by_division
            );
        }
        for n in [
            561u64,
            1105,
            1729,
            2047,
            1_373_653,
            25_326_001,
            3_215_031_751,
            u64::MAX,
        ] {
            assert!(!is_prime_u64(n, FactorizationBudget::default()).unwrap());
        }
    }


    #[test]
    fn a_form_is_canonical_arithmetic_cancels_and_equal_values_have_equal_forms() {
        let ln2 = LogForm::ln_of_prime(2).unwrap();
        let ln3 = LogForm::ln_of_prime(3).unwrap();
        let ln6 = LogForm::ln_of_positive_integer(&big(6), 1000).unwrap();
        assert_eq!(ln2.add(&ln3), ln6);
        assert_eq!(ln6.sub(&ln3), ln2);
        assert!(ln6.sub(&ln2).sub(&ln3).is_zero());
        assert_eq!(ln2.neg().add(&ln2), LogForm::zero());
        assert_eq!(
            ln2.scale(&ri(3)),
            LogForm::ln_of_positive_integer(&big(8), 1000).unwrap()
        );
        assert_eq!(ln2.scale(&ri(0)), LogForm::zero());
        assert_eq!(
            LogForm::ln_of_positive_rational(&rq(9, 4), 1000).unwrap(),
            ln3.scale(&ri(2)).sub(&ln2.scale(&ri(2)))
        );
        let unreduced = num_rational::Ratio::new_raw(BigInt::from(18), BigInt::from(8));
        assert_eq!(
            LogForm::ln_of_positive_rational(&unreduced, 1000).unwrap(),
            LogForm::ln_of_positive_rational(&rq(9, 4), 1000).unwrap()
        );
        assert_eq!(ln6.coefficient(2), ri(1));
        assert_eq!(ln6.coefficient(5), ri(0));
    }

    #[test]
    fn a_non_prime_or_non_positive_argument_is_refused() {
        assert_eq!(
            LogForm::ln_of_prime(1),
            Err(LogFormError::NotPrime { value: 1 })
        );
        assert_eq!(
            LogForm::ln_of_prime(0),
            Err(LogFormError::NotPrime { value: 0 })
        );
        assert_eq!(
            LogForm::ln_of_prime(91),
            Err(LogFormError::NotPrime { value: 91 })
        );
        assert_eq!(
            LogForm::ln_of_positive_rational(&ri(0), 1000),
            Err(LogFormError::NonPositiveArgument)
        );
        assert_eq!(
            LogForm::ln_of_positive_rational(&rq(-1, 2), 1000),
            Err(LogFormError::NonPositiveArgument)
        );
        assert!(LogForm::ln_of_positive_rational(&ri(1), 1000)
            .unwrap()
            .is_zero());
    }


    #[test]
    fn the_logarithms_of_small_primes_are_enclosed_to_the_requested_width() {
        let references = [
            (
                2u64,
                "0.6931471805599453094172321214581765680755001343602552541206800094933936",
            ),
            (
                3,
                "1.098612288668109691395245236922525704647490557822749451734694333637494",
            ),
            (
                5,
                "1.609437912434100374600759333226187639525601354268517721912647891474179",
            ),
            (
                7,
                "1.945910149055313305105352743443179729637084729581861188459390149937580",
            ),
            (
                11,
                "2.397895272798370544061943577965129299821706853937417175218567709130574",
            ),
            (
                13,
                "2.564949357461536736053487441565318604805267944760207116419045510663465",
            ),
        ];
        for (prime, reference) in references {
            let form = LogForm::ln_of_prime(prime).unwrap();
            for bits in [8u32, 64, 100, 140] {
                assert_value(&form, bits, reference);
            }
        }
    }

    #[test]
    fn the_enclosure_of_a_composite_by_range_reduction_agrees_with_the_sum_of_its_prime_logarithms()
    {
        for n in 2u64..=200 {
            let direct = ln_enclosure(&Rational::from_integer(BigInt::from(n)), 120).unwrap();
            let via_primes = LogForm::ln_of_positive_integer(&big(n), 1000)
                .unwrap()
                .enclosure(120)
                .unwrap();
            assert!(!direct.is_disjoint_from(&via_primes), "n = {n}");
            assert!(direct.diam() <= Rational::new(BigInt::one(), BigInt::one() << 120u32));
        }
        assert_eq!(ln_enclosure(&ri(1), 50).unwrap(), Interval::point(ri(0)));
    }

    #[test]
    fn the_zero_form_encloses_zero_and_precision_above_the_limit_is_refused() {
        assert_eq!(
            LogForm::zero().enclosure(10).unwrap(),
            Interval::point(ri(0))
        );
        assert_eq!(
            LogForm::ln_of_prime(2)
                .unwrap()
                .enclosure(MAX_ENCLOSURE_BITS + 1),
            Err(LogFormError::PrecisionTooLarge {
                requested: MAX_ENCLOSURE_BITS + 1,
                limit: MAX_ENCLOSURE_BITS
            })
        );
    }

    #[test]
    fn large_coefficients_keep_the_enclosure_within_its_width() {
        let form = LogForm::ln_of_prime(2)
            .unwrap()
            .scale(&ri(1_000_000))
            .sub(&LogForm::ln_of_prime(3).unwrap().scale(&ri(700_000)));
        let enclosure = form.enclosure(60).unwrap();
        assert!(enclosure.diam() <= Rational::new(BigInt::one(), BigInt::one() << 60u32));
        let value = decimal("0.6931471805599453094172321214581765680755") * ri(1_000_000)
            - decimal("1.0986122886681096913952452369225257046475") * ri(700_000);
        assert!(enclosure.contains(&value));
    }

    #[test]
    fn compare_orders_forms_by_value_and_refuses_when_precision_cannot_separate_them() {
        let ln = |n: u64| LogForm::ln_of_positive_integer(&big(n), 1000).unwrap();
        assert_eq!(ln(6).compare(&ln(5), 64).unwrap(), Ordering::Greater);
        assert_eq!(ln(5).compare(&ln(6), 64).unwrap(), Ordering::Less);
        assert_eq!(
            ln(6).compare(&ln(2).add(&ln(3)), 64).unwrap(),
            Ordering::Equal
        );
        assert_eq!(ln(8).compare(&ln(9), 64).unwrap(), Ordering::Less);
        assert_eq!(ln(1001).compare(&ln(1000), 64).unwrap(), Ordering::Greater);
        assert_eq!(
            ln(1001).compare(&ln(1000), 4),
            Err(LogFormError::SignUndecided { bits: 4 })
        );
        assert_eq!(
            ln(1001).compare(&ln(1000), 0),
            Err(LogFormError::SignUndecided { bits: 0 })
        );
    }


    fn form_of(pairs: &[(u64, (i64, i64))]) -> LogForm {
        let mut form = LogForm::zero();
        for &(prime, (n, d)) in pairs {
            form = form.add(&LogForm::ln_of_prime(prime).unwrap().scale(&rq(n, d)));
        }
        form
    }

    #[test]
    fn the_shannon_entropy_forms_of_the_documented_distributions_are_pinned() {
        let two_point = shannon_entropy_form(&simplex(&[(3, 4), (1, 4)])).unwrap();
        assert_eq!(two_point, form_of(&[(2, (2, 1)), (3, (-3, 4))]));
        assert_value(
            &two_point,
            100,
            "0.5623351446188083502880303152244588576653823503534484194403392687586666",
        );
        let ladder = shannon_entropy_form(&simplex(&[(8, 15), (4, 15), (2, 15), (1, 15)])).unwrap();
        assert_eq!(ladder, form_of(&[(2, (-34, 15)), (3, (1, 1)), (5, (1, 1))]));
        assert_value(
            &ladder,
            100,
            "1.136916591833000697983611761510179789868624940874688597640467536926648",
        );
        let seven = shannon_entropy_form(&simplex(&[(4, 7), (2, 7), (1, 7)])).unwrap();
        assert_eq!(seven, form_of(&[(2, (-10, 7)), (7, (1, 1))]));
        assert_value(
            &seven,
            100,
            "0.9556998911125342916521639985029274895292273947814965397155615649470175",
        );
        let uniform = shannon_entropy_form(&simplex(&[(1, 3), (1, 3), (1, 3)])).unwrap();
        assert_eq!(uniform, form_of(&[(3, (1, 1))]));
        assert_eq!(
            shannon_entropy_form(&simplex(&[(1, 4); 4])).unwrap(),
            form_of(&[(2, (2, 1))])
        );
    }

    #[test]
    fn the_entropy_form_is_zero_exactly_for_deterministic_distributions() {
        for n in 1..=4usize {
            for p in grid_simplices(6, n) {
                let form = shannon_entropy_form(&p).unwrap();
                assert_eq!(form.is_zero(), p.is_dirac(), "{:?}", p.probs());
            }
        }
    }

    #[test]
    fn the_entropy_form_does_not_depend_on_the_order_of_the_masses() {
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        let q = simplex(&[(1, 6), (1, 2), (1, 3)]);
        assert_eq!(
            shannon_entropy_form(&p).unwrap(),
            shannon_entropy_form(&q).unwrap()
        );
    }

    #[test]
    fn relative_entropy_has_its_hand_value_vanishes_on_equal_distributions_and_refuses_infinity() {
        let p = simplex(&[(1, 2), (1, 2)]);
        let q = simplex(&[(1, 4), (3, 4)]);
        let d = relative_entropy_form(&p, &q).unwrap();
        assert_eq!(d, form_of(&[(2, (1, 1)), (3, (-1, 2))]));
        assert_value(
            &d,
            100,
            "0.1438410362258904637196095029969137157517548554488805282533328426746465",
        );
        assert!(relative_entropy_form(&p, &p).unwrap().is_zero());
        let point = simplex(&[(1, 1), (0, 1)]);
        assert_eq!(
            relative_entropy_form(&p, &point),
            Err(LogFormError::InfiniteRelativeEntropy { index: 1 })
        );
        assert!(relative_entropy_form(&point, &point).unwrap().is_zero());
        assert_eq!(
            relative_entropy_form(&p, &simplex(&[(1, 3), (1, 3), (1, 3)])),
            Err(LogFormError::SizeMismatch { left: 2, right: 3 })
        );
    }

    #[test]
    fn renyi_forms_have_their_hand_values_and_the_expected_special_cases() {
        let p = simplex(&[(1, 2), (1, 3), (1, 6)]);
        assert_eq!(renyi_entropy_form(&p, 0).unwrap(), form_of(&[(3, (1, 1))]));
        assert_eq!(
            renyi_entropy_form(&p, 1).unwrap(),
            shannon_entropy_form(&p).unwrap()
        );
        assert_eq!(
            renyi_entropy_form(&p, 2).unwrap(),
            form_of(&[(2, (1, 1)), (3, (2, 1)), (7, (-1, 1))])
        );
        assert_eq!(min_entropy_form(&p).unwrap(), form_of(&[(2, (1, 1))]));
        let u = simplex(&[(1, 5); 5]);
        for alpha in [0u32, 1, 2, 3, 7] {
            assert_eq!(
                renyi_entropy_form(&u, alpha).unwrap(),
                form_of(&[(5, (1, 1))]),
                "alpha {alpha}"
            );
        }
        assert_eq!(min_entropy_form(&u).unwrap(), form_of(&[(5, (1, 1))]));
    }
}
