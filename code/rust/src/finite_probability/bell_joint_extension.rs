//! Exact CHSH certificates for a supplied positive normalized joint law.
//! Bit order: A0, A1, B0, B1 (least significant first); set bit means +1.
//! Origin: FQ-BELL-CLASSICAL-JOINT-EXTENSION. AuthorityEffect: None.

use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum JointBellError {
    #[error("the joint law must have exactly 16 weights")]
    WrongCarrier,
    #[error("the response map must have exactly 16 rows")]
    WrongResponseCarrier,
    #[error("response ({0},{1}) is not a canonical rational")]
    InvalidResponseRational(usize, usize),
    #[error("certificate does not match the supplied joint law")]
    CertificateMismatch,
    #[error("weight {0} is not reduced with a positive denominator")]
    InvalidRational(usize),
    #[error("weight {0} is negative")]
    NegativeWeight(usize),
    #[error("joint weights must sum to one")]
    NotNormalized,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointBellCertificate {
    /// E00, E01, E10, E11.
    pub correlators: [Q; 4],
    pub chsh: Q,
    pub positive_score_mass: Q,
    pub negative_score_mass: Q,
    pub lower_slack: Q,
    pub upper_slack: Q,
}

pub fn deterministic_chsh([a0, a1, b0, b1]: [bool; 4]) -> i32 {
    let s = |b| if b { 1 } else { -1 };
    s(a0) * (s(b0) + s(b1)) + s(a1) * (s(b0) - s(b1))
}

pub fn certify_joint_law(weights: &[Q]) -> Result<JointBellCertificate, JointBellError> {
    if weights.len() != 16 {
        return Err(JointBellError::WrongCarrier);
    }
    for (index, weight) in weights.iter().enumerate() {
        if !weight.denom().is_positive() || !weight.numer().gcd(weight.denom()).is_one() {
            return Err(JointBellError::InvalidRational(index));
        }
        if weight.is_negative() {
            return Err(JointBellError::NegativeWeight(index));
        }
    }
    if weights.iter().cloned().sum::<Q>() != Q::one() {
        return Err(JointBellError::NotNormalized);
    }
    let mut correlators: [Q; 4] = std::array::from_fn(|_| Q::zero());
    let mut plus = Q::zero();
    let mut minus = Q::zero();
    for (mask, weight) in weights.iter().enumerate() {
        let assignment = std::array::from_fn(|j| mask & (1 << j) != 0);
        let [a0, a1, b0, b1] = assignment.map(|b| if b { 1 } else { -1 });
        for (j, product) in [a0 * b0, a0 * b1, a1 * b0, a1 * b1].into_iter().enumerate() {
            correlators[j] += weight * Q::from_integer(product.into());
        }
        if deterministic_chsh(assignment) == 2 {
            plus += weight;
        } else {
            minus += weight;
        }
    }
    let chsh = &correlators[0] + &correlators[1] + &correlators[2] - &correlators[3];
    let two = Q::from_integer(2.into());
    Ok(JointBellCertificate {
        lower_slack: &two + &chsh,
        upper_slack: &two - &chsh,
        correlators,
        chsh,
        positive_score_mass: plus,
        negative_score_mass: minus,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn q(n: i64, d: i64) -> Q {
        Q::new(n.into(), d.into())
    }
    fn checked(weights: &[Q]) -> JointBellCertificate {
        let c = certify_joint_law(weights).unwrap();
        assert_eq!(&c.positive_score_mass + &c.negative_score_mass, Q::one());
        assert_eq!(
            c.chsh,
            q(2, 1) * (&c.positive_score_mass - &c.negative_score_mass)
        );
        assert_eq!(c.lower_slack, q(4, 1) * &c.positive_score_mass);
        assert_eq!(c.upper_slack, q(4, 1) * &c.negative_score_mass);
        assert!(!c.lower_slack.is_negative() && !c.upper_slack.is_negative());
        c
    }
    #[test]
    fn all_vertices_and_both_saturations() {
        let mut positive = 0;
        for mask in 0..16 {
            let mut weights = vec![Q::zero(); 16];
            weights[mask] = Q::one();
            let c = checked(&weights);
            let signs: [i32; 4] =
                std::array::from_fn(|j| if mask & (1 << j) != 0 { 1 } else { -1 });
            let [a0, a1, b0, b1] = signs;
            let expected = if b0 == b1 { 2 * a0 * b0 } else { 2 * a1 * b0 };
            assert_eq!(c.chsh, q(expected.into(), 1));
            assert_eq!(
                c.correlators,
                [a0 * b0, a0 * b1, a1 * b0, a1 * b1].map(|n| q(n.into(), 1))
            );
            positive += usize::from(expected == 2);
        }
        assert_eq!(positive, 8);
    }
    #[test]
    fn uniform_asymmetric_and_all_pair_mixtures() {
        assert_eq!(checked(&vec![q(1, 16); 16]).chsh, Q::zero());
        assert_eq!(
            checked(&(1..=16).map(|n| q(n, 136)).collect::<Vec<_>>()).chsh,
            Q::zero()
        );
        for i in 0..16 {
            for j in 0..16 {
                for p in [q(1, 7), q(2, 5), q(11, 13)] {
                    let mut weights = vec![Q::zero(); 16];
                    weights[i] += &p;
                    weights[j] += Q::one() - p;
                    checked(&weights);
                }
            }
        }
    }
    #[test]
    fn arbitrary_precision_control() {
        let d = num_bigint::BigInt::from(10u32).pow(100) + num_bigint::BigInt::from(3);
        let mut weights = vec![Q::zero(); 16];
        weights[1] = Q::new(1.into(), d.clone());
        weights[0] = Q::one() - &weights[1];
        assert_eq!(checked(&weights).chsh, q(2, 1) - Q::new(4.into(), d));
    }
    #[test]
    fn signed_normalized_near_miss_is_refused() {
        let mut weights = vec![Q::zero(); 16];
        weights[0] = q(3, 2);
        weights[1] = q(-1, 2);
        assert_eq!(weights.iter().cloned().sum::<Q>(), Q::one());
        assert_eq!(q(2, 1) * &weights[0] - q(2, 1) * &weights[1], q(4, 1));
        assert_eq!(
            certify_joint_law(&weights),
            Err(JointBellError::NegativeWeight(1))
        );
    }
    #[test]
    fn wrong_mass_and_wrong_carrier_are_refused() {
        assert_eq!(
            certify_joint_law(&vec![Q::zero(); 16]),
            Err(JointBellError::NotNormalized)
        );
        let mut weights = vec![Q::zero(); 16];
        weights[0] = q(2, 1);
        assert_eq!(
            certify_joint_law(&weights),
            Err(JointBellError::NotNormalized)
        );
        assert_eq!(
            certify_joint_law(&vec![q(1, 15); 15]),
            Err(JointBellError::WrongCarrier)
        );
    }
    #[test]
    fn malformed_raw_rationals_are_refused_before_arithmetic() {
        for raw in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw((-1).into(), (-1).into()),
            Q::new_raw(2.into(), 2.into()),
        ] {
            let mut weights = vec![Q::zero(); 16];
            weights[0] = raw;
            assert_eq!(
                certify_joint_law(&weights),
                Err(JointBellError::InvalidRational(0))
            );
        }
    }
    #[test]
    fn wrong_sign_decoy_is_distinguished_from_chsh() {
        let mut weights = vec![Q::zero(); 16];
        weights[0] = Q::one();
        let c = checked(&weights);
        assert_eq!(c.correlators.iter().cloned().sum::<Q>(), q(4, 1));
        assert_eq!(c.chsh, q(2, 1));
    }
}

/// Nullary generator, with rows ordered by the A0,A1,B0,B1 bit mask.
pub fn response_products() -> [[i32; 4]; 16] {
    std::array::from_fn(|mask| {
        let [a0, a1, b0, b1] = std::array::from_fn(|j| if mask & (1 << j) == 0 { -1 } else { 1 });
        [a0 * b0, a0 * b1, a1 * b0, a1 * b1]
    })
}

fn canonical(q: &Q) -> bool {
    q.denom().is_positive() && q.numer().gcd(q.denom()).is_one()
}

fn joint_weights(weights: &[Q]) -> Result<(), JointBellError> {
    if weights.len() != 16 {
        return Err(JointBellError::WrongCarrier);
    }
    for (i, q) in weights.iter().enumerate() {
        if !canonical(q) {
            return Err(JointBellError::InvalidRational(i));
        }
        if q.is_negative() {
            return Err(JointBellError::NegativeWeight(i));
        }
    }
    if weights.iter().cloned().sum::<Q>() != Q::one() {
        return Err(JointBellError::NotNormalized);
    }
    Ok(())
}

/// Binary generator on a single joint law and an arbitrary exact Q^4 table.
/// The Bell bound requires response_products(), rather than an arbitrary table.
pub fn joint_expectation(weights: &[Q], responses: &[[Q; 4]]) -> Result<[Q; 4], JointBellError> {
    joint_weights(weights)?;
    if responses.len() != 16 {
        return Err(JointBellError::WrongResponseCarrier);
    }
    for (i, row) in responses.iter().enumerate() {
        for (j, q) in row.iter().enumerate() {
            if !canonical(q) {
                return Err(JointBellError::InvalidResponseRational(i, j));
            }
        }
    }
    Ok(std::array::from_fn(|j| {
        weights
            .iter()
            .zip(responses)
            .map(|(p, row)| p * &row[j])
            .sum()
    }))
}

/// Unary generator. A scalar value alone is not a Bell certificate.
pub fn chsh_linear(e: &[Q; 4]) -> Result<Q, JointBellError> {
    for (j, q) in e.iter().enumerate() {
        if !canonical(q) {
            return Err(JointBellError::InvalidResponseRational(0, j));
        }
    }
    Ok(&e[0] + &e[1] + &e[2] - &e[3])
}

/// Independently recompute every field; does not call the certificate producer.
pub fn verify_joint_certificate(
    weights: &[Q],
    certificate: &JointBellCertificate,
) -> Result<(), JointBellError> {
    joint_weights(weights)?;
    if certificate
        .correlators
        .iter()
        .chain([
            &certificate.chsh,
            &certificate.positive_score_mass,
            &certificate.negative_score_mass,
            &certificate.lower_slack,
            &certificate.upper_slack,
        ])
        .any(|q| !canonical(q))
    {
        return Err(JointBellError::CertificateMismatch);
    }
    let products = response_products();
    let e: [Q; 4] = std::array::from_fn(|j| {
        (0..16)
            .map(|m| &weights[m] * Q::from_integer(products[m][j].into()))
            .sum()
    });
    let mut plus = Q::zero();
    let mut minus = Q::zero();
    for (m, row) in products.iter().enumerate() {
        if row[0] + row[1] + row[2] - row[3] == 2 {
            plus += &weights[m];
        } else {
            minus += &weights[m];
        }
    }
    let s = &e[0] + &e[1] + &e[2] - &e[3];
    let two = Q::from_integer(2.into());
    let independent = JointBellCertificate {
        correlators: e,
        lower_slack: &two + &s,
        upper_slack: &two - &s,
        chsh: s,
        positive_score_mass: plus,
        negative_score_mass: minus,
    };
    if *certificate != independent {
        return Err(JointBellError::CertificateMismatch);
    }
    Ok(())
}

#[cfg(test)]
mod operad_tests {
    use super::*;
    fn q(n: i64, d: i64) -> Q {
        Q::new(n.into(), d.into())
    }
    #[test]
    fn generic_linearity_and_bell_composition() {
        let law: Vec<Q> = (1..=16).map(|i| q(i, 136)).collect();
        let table: Vec<[Q; 4]> = (0..16)
            .map(|i| std::array::from_fn(|j| q((i + 1) * (j as i64 - 2), i + j as i64 + 3)))
            .collect();
        let left = chsh_linear(&joint_expectation(&law, &table).unwrap()).unwrap();
        let right: Q = law
            .iter()
            .zip(&table)
            .map(|(p, row)| p * chsh_linear(row).unwrap())
            .sum();
        assert_eq!(left, right);
        let products: Vec<[Q; 4]> = response_products()
            .iter()
            .map(|row| row.map(|n| q(n.into(), 1)))
            .collect();
        let c = certify_joint_law(&law).unwrap();
        assert_eq!(joint_expectation(&law, &products).unwrap(), c.correlators);
        assert_eq!(chsh_linear(&c.correlators).unwrap(), c.chsh);
        assert_eq!(
            chsh_linear(
                &joint_expectation(&law, &vec![[q(2, 1), q(2, 1), q(2, 1), q(2, 1)]; 16]).unwrap()
            )
            .unwrap(),
            q(4, 1)
        );
    }
    #[test]
    fn malformed_response_and_certificate_are_rejected_before_arithmetic() {
        let law = vec![q(1, 16); 16];
        let mut table = vec![[q(1, 1), q(1, 1), q(1, 1), q(1, 1)]; 16];
        assert_eq!(
            joint_expectation(&law, &table[..15]),
            Err(JointBellError::WrongResponseCarrier)
        );
        table[7][2] = Q::new_raw(1.into(), 0.into());
        assert_eq!(
            joint_expectation(&law, &table),
            Err(JointBellError::InvalidResponseRational(7, 2))
        );
        let mut c = certify_joint_law(&law).unwrap();
        c.chsh = Q::new_raw(1.into(), 0.into());
        assert_eq!(
            verify_joint_certificate(&law, &c),
            Err(JointBellError::CertificateMismatch)
        );
    }
    #[test]
    fn each_forged_component_is_rejected_and_all_mixtures_are_accepted() {
        let law = vec![q(1, 16); 16];
        let c = certify_joint_law(&law).unwrap();
        verify_joint_certificate(&law, &c).unwrap();
        for k in 0..9 {
            let mut bad = c.clone();
            match k {
                0..=3 => bad.correlators[k] += q(1, 1),
                4 => bad.chsh += q(1, 1),
                5 => bad.positive_score_mass += q(1, 1),
                6 => bad.negative_score_mass += q(1, 1),
                7 => bad.lower_slack += q(1, 1),
                _ => bad.upper_slack += q(1, 1),
            }
            assert_eq!(
                verify_joint_certificate(&law, &bad),
                Err(JointBellError::CertificateMismatch)
            );
        }
        for i in 0..16 {
            for j in 0..16 {
                for p in [q(1, 7), q(2, 5), q(11, 13)] {
                    let mut law = vec![Q::zero(); 16];
                    law[i] += &p;
                    law[j] += Q::one() - p;
                    verify_joint_certificate(&law, &certify_joint_law(&law).unwrap()).unwrap();
                }
            }
        }
    }
}
