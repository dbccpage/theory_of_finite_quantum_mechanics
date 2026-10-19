//! Exact positive rays of weight vectors. Relative amplitude phases are forgotten.
use super::pfp_exact::{validate, Result};
use num_rational::BigRational as Q;
use num_traits::{Signed, Zero};

fn weights(w: &[Q]) -> Result<()> {
    validate(&vec![w.to_vec()])?;
    if w.iter().any(Signed::is_negative) || w.iter().cloned().sum::<Q>() <= Q::zero() {
        return Err("nonnegative nonzero weights required");
    }
    Ok(())
}
pub fn normalize(w: &[Q]) -> Result<Vec<Q>> {
    weights(w)?;
    let total: Q = w.iter().cloned().sum();
    Ok(w.iter().map(|x| x / &total).collect())
}
pub fn born_weights(a: &[[Q; 2]]) -> Result<Vec<Q>> {
    let mut result = Vec::new();
    for pair in a {
        validate(&vec![pair.to_vec()])?;
        result.push(&pair[0] * &pair[0] + &pair[1] * &pair[1]);
    }
    weights(&result)?;
    Ok(result)
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Certificate {
    pub left_sum: Q,
    pub right_sum: Q,
    pub normalized: Vec<Q>,
    pub normalized_twice: Vec<Q>,
    pub normalized_scaled: Vec<Q>,
    pub same_weight_ray: bool,
    pub ray_scale: Option<Q>,
    pub separating_minor: Option<(usize, usize, Q)>,
}
pub fn certify(left: &[Q], right: &[Q], scale: &Q) -> Result<Certificate> {
    weights(left)?;
    weights(right)?;
    validate(&vec![vec![scale.clone()]])?;
    if left.len() != right.len() {
        return Err("same weight carrier required");
    }
    if scale <= &Q::zero() {
        return Err("positive scale required");
    }
    let normalized = normalize(left)?;
    let nr = normalize(right)?;
    let same_weight_ray = normalized == nr;
    let left_sum: Q = left.iter().cloned().sum();
    let right_sum: Q = right.iter().cloned().sum();
    let ray_scale = if same_weight_ray {
        Some(&right_sum / &left_sum)
    } else {
        None
    };
    let mut separating_minor = None;
    if !same_weight_ray {
        'search: for i in 0..left.len() {
            for j in i + 1..left.len() {
                let d = &right[i] * &left[j] - &left[i] * &right[j];
                if !d.is_zero() {
                    separating_minor = Some((i, j, d));
                    break 'search;
                }
            }
        }
        if separating_minor.is_none() {
            return Err("missing nonzero minor");
        }
    }
    Ok(Certificate {
        left_sum,
        right_sum,
        normalized_twice: normalize(&normalized)?,
        normalized_scaled: normalize(&left.iter().map(|x| x * scale).collect::<Vec<_>>())?,
        normalized,
        same_weight_ray,
        ray_scale,
        separating_minor,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::One;
    fn q(n: i64) -> Q {
        Q::from_integer(n.into())
    }
    #[test]
    fn grid_classification_is_bound_to_actual_scalars_or_minors() {
        let vectors: Vec<Vec<Q>> = (0..4)
            .flat_map(|a| {
                (0..4).flat_map(move |b| {
                    (0..4).filter_map(move |c| {
                        if a + b + c > 0 {
                            Some(vec![q(a), q(b), q(c)])
                        } else {
                            None
                        }
                    })
                })
            })
            .collect();
        for a in &vectors {
            for b in &vectors {
                let c = certify(a, b, &q(7)).unwrap();
                assert_eq!(c.normalized, c.normalized_twice);
                assert_eq!(c.normalized, c.normalized_scaled);
                if let Some(s) = c.ray_scale {
                    assert!(s > Q::zero());
                    assert_eq!(b, &a.iter().map(|x| x * &s).collect::<Vec<_>>());
                } else {
                    let (i, j, d) = c.separating_minor.unwrap();
                    assert_eq!(d, &b[i] * &a[j] - &a[i] * &b[j]);
                    assert!(!d.is_zero());
                }
            }
        }
    }
    #[test]
    fn zero_negative_and_nonpositive_scale_are_refused() {
        assert!(normalize(&[q(0), q(0)]).is_err());
        assert!(normalize(&[q(-1), q(2)]).is_err());
        assert!(certify(&[q(1)], &[q(2)], &q(0)).is_err());
    }
    #[test]
    fn weight_rays_do_not_classify_amplitude_rays() {
        let a = [[q(1), q(0)], [q(1), q(0)]];
        let b = [[q(1), q(0)], [q(-1), q(0)]];
        assert_eq!(born_weights(&a).unwrap(), born_weights(&b).unwrap());
        assert_ne!(&a[0][0] * &b[1][0] - &a[1][0] * &b[0][0], Q::zero());
        assert_eq!(
            normalize(&born_weights(&a).unwrap()).unwrap(),
            vec![Q::one() / q(2); 2]
        );
    }
}
