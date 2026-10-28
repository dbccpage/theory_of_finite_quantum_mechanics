//! Conductor labels are not colimits or field-minimality proofs.
use num_integer::Integer;
use num_rational::BigRational as Q;
use tfqm_number_theory::cyclotomic_field::{CyclotomicError, CyclotomicNumber as C};
use tfqm_number_theory::polynomial::cyclotomic_polynomial;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Sample {
    pub source: usize,
    pub intermediate: usize,
    pub target: usize,
    pub source_polynomial: Vec<Q>,
    pub target_polynomial: Vec<Q>,
    pub arrays: Vec<Vec<Q>>,
}
fn validate_conductor_chain(n: usize, mid: usize, target: usize) -> Result<(), CyclotomicError> {
    if n == 0 || mid == 0 || target == 0 || mid % n != 0 || target % mid != 0 {
        return Err(CyclotomicError::ConductorMismatch {
            left: n,
            right: target,
        });
    }
    Ok(())
}

fn parse_canonical_operands(
    n: usize,
    a: Vec<Q>,
    b: Vec<Q>,
) -> Result<(C, C), CyclotomicError> {
    super::pfp_exact::validate(&vec![a.clone()])
        .map_err(|_| CyclotomicError::Inconsistent("canonical source coefficients required"))?;
    super::pfp_exact::validate(&vec![b.clone()])
        .map_err(|_| CyclotomicError::Inconsistent("canonical source coefficients required"))?;
    let ca = C::from_coefficients(n, a)?;
    let cb = C::from_coefficients(n, b)?;
    Ok((ca, cb))
}

fn lift_and_norm(
    a: &C,
    b: &C,
    mid: usize,
    target: usize,
) -> Result<(C, C, C, C, C), CyclotomicError> {
    let ea = a.lift(target)?;
    let eb = b.lift(target)?;
    let ca = a.conjugate();
    let norm = a.mul(&ca)?;
    let via = a.lift(mid)?.lift(target)?;
    Ok((ea, eb, ca, norm, via))
}

fn compute_sample_arrays(
    a: &C,
    b: &C,
    ea: &C,
    eb: &C,
    ca: &C,
    norm: &C,
    via: &C,
    target: usize,
) -> Result<Vec<Vec<Q>>, CyclotomicError> {
    let norm_lift = norm.lift(target)?;
    let ea_norm = ea.mul(&ea.conjugate())?;
    let ab_lift = a.add(b)?.lift(target)?;
    let eab_add = ea.add(eb)?;
    let ab_mul_lift = a.mul(b)?.lift(target)?;
    let eab_mul = ea.mul(eb)?;
    let ca_lift = ca.lift(target)?;
    let ea_conj = ea.conjugate();
    Ok(vec![
        a.coefficients().to_vec(),
        ca.coefficients().to_vec(),
        norm.coefficients().to_vec(),
        ea.coefficients().to_vec(),
        via.coefficients().to_vec(),
        norm_lift.coefficients().to_vec(),
        ea_norm.coefficients().to_vec(),
        ab_lift.coefficients().to_vec(),
        eab_add.coefficients().to_vec(),
        ab_mul_lift.coefficients().to_vec(),
        eab_mul.coefficients().to_vec(),
        ca_lift.coefficients().to_vec(),
        ea_conj.coefficients().to_vec(),
    ])
}

fn validate_lift_consistency(arrays: &[Vec<Q>], norm: &C) -> Result<(), CyclotomicError> {
    if !norm.is_real() {
        return Err(CyclotomicError::Inconsistent(
            "selected lift composition/norm failed",
        ));
    }
    let pairs = [(3, 4), (5, 6), (7, 8), (9, 10), (11, 12)];
    if pairs.iter().any(|&(i, j)| arrays[i] != arrays[j]) {
        return Err(CyclotomicError::Inconsistent(
            "selected lift composition/norm failed",
        ));
    }
    Ok(())
}

fn get_sample_polynomials(n: usize, target: usize) -> Result<(Vec<Q>, Vec<Q>), CyclotomicError> {
    let src = cyclotomic_polynomial(n)?.coefficients().to_vec();
    let tgt = cyclotomic_polynomial(target)?.coefficients().to_vec();
    Ok((src, tgt))
}

pub fn certify_sample(
    n: usize,
    mid: usize,
    target: usize,
    a: Vec<Q>,
    b: Vec<Q>,
) -> Result<Sample, CyclotomicError> {
    validate_conductor_chain(n, mid, target)?;
    let (a, b) = parse_canonical_operands(n, a, b)?;
    let (ea, eb, ca, norm, via) = lift_and_norm(&a, &b, mid, target)?;
    let arrays = compute_sample_arrays(&a, &b, &ea, &eb, &ca, &norm, &via, target)?;
    validate_lift_consistency(&arrays, &norm)?;
    let (source_polynomial, target_polynomial) = get_sample_polynomials(n, target)?;
    Ok(Sample {
        source: n,
        intermediate: mid,
        target,
        source_polynomial,
        target_polynomial,
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
