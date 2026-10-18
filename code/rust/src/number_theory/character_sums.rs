

use super::cyclotomic::{Cyc12, Cyc24, Cyc5, Cyc8};
use super::cyclotomic120::Cyc120;
use super::cyclotomic28::Cyc28;
use super::cyclotomic44::Cyc44;
use super::cyclotomic52::Cyc52;
use super::finite_field::{FieldElement, FiniteField};

pub trait CyclotomicField:
    crate::scalar::RationalEmbedding + linear_algebra::exact_field::involution::Involution
{
    const CONDUCTOR: usize;

    fn zeta_power(k: i64) -> Self;
}

macro_rules! cyclotomic_field {
    ($ty:ty, $n:expr, $zeta:path) => {
        impl CyclotomicField for $ty {
            const CONDUCTOR: usize = $n;
            fn zeta_power(k: i64) -> Self {
                $zeta(k.rem_euclid($n as i64) as i32)
            }
        }
    };
}

cyclotomic_field!(Cyc5, 5, Cyc5::zeta5);
cyclotomic_field!(Cyc8, 8, Cyc8::zeta8);
cyclotomic_field!(Cyc12, 12, Cyc12::zeta12);
cyclotomic_field!(Cyc24, 24, Cyc24::zeta24);
cyclotomic_field!(Cyc28, 28, Cyc28::zeta);
cyclotomic_field!(Cyc44, 44, Cyc44::zeta);
cyclotomic_field!(Cyc52, 52, Cyc52::zeta);
cyclotomic_field!(Cyc120, 120, Cyc120::zeta);

pub fn additive_character<F: CyclotomicField>(
    field: &FiniteField,
    x: &FieldElement,
) -> Result<F, String> {
    let p = field.prime();
    if F::CONDUCTOR % p != 0 {
        return Err(format!(
            "Q(zeta_{}) does not contain the {p}-th roots of unity",
            F::CONDUCTOR
        ));
    }
    let trace = field.trace_value(x)?;
    Ok(F::zeta_power(((F::CONDUCTOR / p) * trace) as i64))
}

pub fn linear_character_sum<F: CyclotomicField>(
    field: &FiniteField,
    coefficient: &FieldElement,
) -> Result<F, String> {
    field.elements().iter().try_fold(F::zero(), |sum, x| {
        Ok(sum.add(&additive_character::<F>(field, &field.mul(coefficient, x))?))
    })
}

pub fn quadratic_gauss_sum<F: CyclotomicField>(
    field: &FiniteField,
    quadratic: &FieldElement,
    linear: &FieldElement,
) -> Result<F, String> {
    field.elements().iter().try_fold(F::zero(), |sum, x| {
        let phase = field.add(
            &field.mul(quadratic, &field.mul(x, x)),
            &field.mul(linear, x),
        );
        Ok(sum.add(&additive_character::<F>(field, &phase)?))
    })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CharacterSumCertificate {
    pub field_order: usize,
    pub linear_sums_checked: usize,
    pub gauss_sums_checked: usize,
}

pub fn verify_character_sum_identities<F: CyclotomicField>(
    field: &FiniteField,
) -> Result<CharacterSumCertificate, String> {
    let q = field.order();
    let zero = F::zero();
    let q_value = F::from_rational(&num_rational::BigRational::from_integer(q.into()));

    let mut linear_sums_checked = 0;
    for coefficient in field.elements().iter().filter(|e| !e.is_zero()) {
        if linear_character_sum::<F>(field, coefficient)? != zero {
            return Err(format!(
                "nontrivial GF({q}) character sum did not vanish for coefficient {:?}",
                coefficient.coeffs
            ));
        }
        linear_sums_checked += 1;
    }

    let mut gauss_sums_checked = 0;
    for quadratic in field.elements().iter().filter(|e| !e.is_zero()) {
        for linear in field.elements() {
            let gauss = quadratic_gauss_sum::<F>(field, quadratic, linear)?;
            if gauss.mul(&gauss.conjugate()) != q_value {
                return Err(format!(
                    "GF({q}) Gauss norm mismatch for quadratic {:?}, linear {:?}",
                    quadratic.coeffs, linear.coeffs
                ));
            }
            gauss_sums_checked += 1;
        }
    }

    Ok(CharacterSumCertificate {
        field_order: q,
        linear_sums_checked,
        gauss_sums_checked,
    })
}
