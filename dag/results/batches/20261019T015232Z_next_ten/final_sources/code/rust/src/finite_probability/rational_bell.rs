//! Supplied two-qubit tensor/Born interface; exact finite tables, no physical promotion.
use super::bell_separator_extension::{construct_extension, PairData};
use super::pfp_exact::{self as mx, Matrix, Result};
use num_rational::BigRational as Q;
use num_traits::{One, Zero};

fn q(n: i64, d: i64) -> Q {
    Q::new(n.into(), d.into())
}
pub fn projectors(a: &Matrix) -> Result<[Matrix; 2]> {
    mx::validate(a)?;
    if a.len() != 2
        || a[0].len() != 2
        || a != &mx::transpose(a)?
        || mx::multiply(a, a)? != mx::eye(2)
    {
        return Err("symmetric qubit binary involution required");
    }
    Ok([
        mx::scale(&q(1, 2), &mx::add(&mx::eye(2), &mx::scale(&q(-1, 1), a)?)?)?,
        mx::scale(&q(1, 2), &mx::add(&mx::eye(2), a)?)?,
    ])
}
pub fn born_pairs(rho: &Matrix, alice: &[Matrix; 2], bob: &[Matrix; 2]) -> Result<PairData> {
    let a = [projectors(&alice[0])?, projectors(&alice[1])?];
    let b = [projectors(&bob[0])?, projectors(&bob[1])?];
    mx::validate(rho)?;
    if rho.len() != 4 || rho[0].len() != 4 || mx::trace(rho)? != Q::one() || !mx::is_psd(rho)? {
        return Err("positive trace-one two-qubit density required");
    }
    let mut pairs: PairData = std::array::from_fn(|_| std::array::from_fn(|_| Q::zero()));
    for x in 0..2 {
        for y in 0..2 {
            for i in 0..2 {
                for j in 0..2 {
                    pairs[2 * x + y][2 * i + j] =
                        mx::trace(&mx::multiply(rho, &mx::tensor(&a[x][i], &b[y][j])?)?)?;
                }
            }
        }
    }
    super::bell_separator_extension::validate_pairs(&pairs).map_err(|_| "Born pair law failed")?;
    Ok(pairs)
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Certificate {
    pub pairs: PairData,
    pub correlations: [Q; 4],
    pub chsh: Q,
    pub minimum_probability: Q,
    pub support_assignments: usize,
    pub separator_lower: Q,
    pub separator_upper: Q,
    pub violating_mask: Option<u8>,
}
pub fn certify(rho: &Matrix, alice: &[Matrix; 2], bob: &[Matrix; 2]) -> Result<Certificate> {
    let pairs = born_pairs(rho, alice, bob)?;
    let correlations: [Q; 4] =
        std::array::from_fn(|j| &pairs[j][0] - &pairs[j][1] - &pairs[j][2] + &pairs[j][3]);
    let chsh = &correlations[0] + &correlations[1] + &correlations[2] - &correlations[3];
    let minimum_probability = pairs.iter().flatten().min().unwrap().clone();
    let support_assignments = (0..16)
        .filter(|m| {
            (0..2).all(|x| {
                (0..2).all(|y| {
                    pairs[2 * x + y][2 * ((m >> x) & 1) + ((m >> (2 + y)) & 1)] > Q::zero()
                })
            })
        })
        .count();
    let decision = construct_extension(&pairs).map_err(|_| "separator check failed")?;
    Ok(Certificate {
        pairs,
        correlations,
        chsh,
        minimum_probability,
        support_assignments,
        separator_lower: decision.analysis.common_lower,
        separator_upper: decision.analysis.common_upper,
        violating_mask: decision.violating_mask,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn data() -> (Matrix, [Matrix; 2], [Matrix; 2]) {
        let rho = vec![
            vec![q(1, 2), q(0, 1), q(0, 1), q(1, 2)],
            vec![q(0, 1); 4],
            vec![q(0, 1); 4],
            vec![q(1, 2), q(0, 1), q(0, 1), q(1, 2)],
        ];
        let z = vec![vec![q(1, 1), q(0, 1)], vec![q(0, 1), q(-1, 1)]];
        let x = vec![vec![q(0, 1), q(1, 1)], vec![q(1, 1), q(0, 1)]];
        let b0 = vec![vec![q(3, 5), q(4, 5)], vec![q(4, 5), q(-3, 5)]];
        let b1 = vec![vec![q(4, 5), q(-3, 5)], vec![q(-3, 5), q(-4, 5)]];
        (rho, [z, x], [b0, b1])
    }
    #[test]
    fn full_support_does_not_supply_positive_joint_law() {
        let (r, a, b) = data();
        let c = certify(&r, &a, &b).unwrap();
        assert_eq!(c.chsh, q(14, 5));
        assert_eq!(c.minimum_probability, q(1, 20));
        assert_eq!(c.support_assignments, 16);
        assert_eq!(c.violating_mask, Some(8));
        assert!(c.separator_lower > c.separator_upper);
    }
    #[test]
    fn invalid_state_and_noninvolution_are_refused() {
        let (mut r, mut a, b) = data();
        r[0][0] = q(-1, 2);
        assert!(born_pairs(&r, &a, &b).is_err());
        let (r, _, _) = data();
        a[0][0][0] = q(2, 1);
        assert!(born_pairs(&r, &a, &b).is_err());
    }
    #[test]
    fn support_preserving_uniform_control_extends() {
        let (_, a, b) = data();
        let r = mx::scale(&q(1, 4), &mx::eye(4)).unwrap();
        let c = certify(&r, &a, &b).unwrap();
        assert_eq!(c.support_assignments, 16);
        assert_eq!(c.chsh, Q::zero());
        assert_eq!(c.violating_mask, None);
    }
}
