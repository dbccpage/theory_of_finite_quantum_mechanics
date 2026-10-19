//! Conductor labels are not colimits or field-minimality proofs.
use num_integer::Integer;
use num_rational::BigRational as Q;
use omega_number_theory::cyclotomic_field::{CyclotomicError, CyclotomicNumber as C};
use omega_number_theory::polynomial::cyclotomic_polynomial;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Sample {
    pub source: usize,
    pub intermediate: usize,
    pub target: usize,
    pub source_polynomial: Vec<Q>,
    pub target_polynomial: Vec<Q>,
    pub arrays: Vec<Vec<Q>>,
}
pub fn certify_sample(
    n: usize,
    mid: usize,
    target: usize,
    a: Vec<Q>,
    b: Vec<Q>,
) -> Result<Sample, CyclotomicError> {
    if n == 0 || mid == 0 || target == 0 || mid % n != 0 || target % mid != 0 {
        return Err(CyclotomicError::ConductorMismatch {
            left: n,
            right: target,
        });
    }
    super::pfp_exact::validate(&vec![a.clone()])
        .map_err(|_| CyclotomicError::Inconsistent("canonical source coefficients required"))?;
    super::pfp_exact::validate(&vec![b.clone()])
        .map_err(|_| CyclotomicError::Inconsistent("canonical source coefficients required"))?;
    let a = C::from_coefficients(n, a)?;
    let b = C::from_coefficients(n, b)?;
    let ea = a.lift(target)?;
    let eb = b.lift(target)?;
    let ca = a.conjugate();
    let norm = a.mul(&ca)?;
    let via = a.lift(mid)?.lift(target)?;
    let arrays = vec![
        a.coefficients().to_vec(),
        ca.coefficients().to_vec(),
        norm.coefficients().to_vec(),
        ea.coefficients().to_vec(),
        via.coefficients().to_vec(),
        norm.lift(target)?.coefficients().to_vec(),
        ea.mul(&ea.conjugate())?.coefficients().to_vec(),
        a.add(&b)?.lift(target)?.coefficients().to_vec(),
        ea.add(&eb)?.coefficients().to_vec(),
        a.mul(&b)?.lift(target)?.coefficients().to_vec(),
        ea.mul(&eb)?.coefficients().to_vec(),
        ca.lift(target)?.coefficients().to_vec(),
        ea.conjugate().coefficients().to_vec(),
    ];
    if arrays[3] != arrays[4]
        || arrays[5] != arrays[6]
        || arrays[7] != arrays[8]
        || arrays[9] != arrays[10]
        || arrays[11] != arrays[12]
        || !norm.is_real()
    {
        return Err(CyclotomicError::Inconsistent(
            "selected lift composition/norm failed",
        ));
    }
    Ok(Sample {
        source: n,
        intermediate: mid,
        target,
        source_polynomial: cyclotomic_polynomial(n)?.coefficients().to_vec(),
        target_polynomial: cyclotomic_polynomial(target)?.coefficients().to_vec(),
        arrays,
    })
}
pub fn label_lcm(values: &[usize]) -> Option<usize> {
    values.iter().try_fold(1usize, |x, &y| {
        if y == 0 {
            None
        } else {
            x.checked_mul(y / x.gcd(&y))
        }
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::Zero;
    #[test]
    fn label_lcm_does_not_claim_field_minimality() {
        assert_eq!(label_lcm(&[1, 2, 3, 4, 5, 8, 12]), Some(120));
        assert_eq!(label_lcm(&[2]), Some(2));
        assert_eq!(label_lcm(&[0]), None);
    }
    #[test]
    fn invalid_divisibility_chain_is_refused() {
        assert!(certify_sample(3, 4, 120, vec![Q::zero(); 2], vec![Q::zero(); 2]).is_err());
    }
    #[test]
    fn actual_quadratic_embedding_norm_is_fixed() {
        let a = vec![Q::from_integer(2.into()), Q::from_integer(1.into())];
        let b = vec![Q::from_integer(1.into()), Q::from_integer((-1).into())];
        let c = certify_sample(3, 6, 120, a, b).unwrap();
        assert_eq!(c.arrays[3], c.arrays[4]);
        assert_eq!(c.arrays[5], c.arrays[6]);
    }
}
