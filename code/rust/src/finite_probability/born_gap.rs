//! Exact finite rivals and dimension guards; uniqueness remains imported.
use super::pfp_exact::{self as m, Matrix, Result};
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
use std::collections::BTreeSet;
pub fn weak_contract(w: Vec<Q>, e: Vec<Q>) -> Result<Vec<Q>> {
    if w.len() != 2 || e.len() != 2 {
        return Err("two labels required");
    }
    m::validate(&vec![w.clone(), e.clone()])?;
    let total = w.iter().cloned().sum::<Q>();
    if total <= Q::zero()
        || w.iter().any(|x| x < &Q::zero())
        || e.iter().any(|x| x < &Q::zero() || x > &Q::one())
    {
        return Err("nonnegative nonzero weights and effects required");
    }
    let p: Vec<_> = w.iter().map(|x| x / &total).collect();
    let b = &p[0] * &e[0] + &p[1] * &e[1];
    let s = &p[0] * &e[1] + &p[1] * &e[0];
    Ok(vec![
        p[0].clone(),
        p[1].clone(),
        b.clone(),
        s.clone(),
        Q::one(),
        Q::one(),
        b - s,
    ])
}
pub struct FrameCertificate {
    pub dimension: usize,
    pub grams: Vec<Matrix>,
    pub determinants: Vec<Q>,
    pub quadratic: Vec<Vec<Q>>,
    pub quartic: Vec<Vec<Q>>,
    pub quadratic_sums: Vec<Q>,
    pub quartic_sums: Vec<Q>,
    pub deficit: Q,
}
pub fn frame(psi: Vec<Q>, frames: Vec<Matrix>) -> Result<FrameCertificate> {
    let n = psi.len();
    if !(2..=3).contains(&n) || frames.len() != 2 {
        return Err("two complete frames of dimension2 or3 required");
    }
    m::validate(&vec![psi.clone()])?;
    let norm = psi.iter().map(|x| x * x).sum::<Q>();
    if norm <= Q::zero() {
        return Err("nonzero state required");
    }
    let mut grams = vec![];
    let mut determinants = vec![];
    let mut quadratic = vec![];
    let mut quartic = vec![];
    for f in frames {
        m::validate(&f)?;
        if f.len() != n || f[0].len() != n {
            return Err("complete frame required");
        }
        let gram = m::multiply(&f, &m::transpose(&f)?)?;
        if (0..n)
            .any(|i| gram[i][i] <= Q::zero() || (0..n).any(|j| i != j && !gram[i][j].is_zero()))
        {
            return Err("orthogonal nonzero frame required");
        }
        let q: Vec<Q> = f
            .iter()
            .enumerate()
            .map(|(i, v)| {
                let d = v.iter().zip(&psi).map(|(x, y)| x * y).sum::<Q>();
                &d * &d / (&norm * &gram[i][i])
            })
            .collect();
        quartic.push(q.iter().map(|x| x * x).collect());
        quadratic.push(q);
        determinants.push(m::determinant(&f)?);
        grams.push(gram);
    }
    let quadratic_sums: Vec<Q> = quadratic.iter().map(|q| q.iter().cloned().sum()).collect();
    let quartic_sums: Vec<Q> = quartic
        .iter()
        .map(|q: &Vec<Q>| q.iter().cloned().sum())
        .collect();
    let deficit = &quartic_sums[0] - &quartic_sums[1];
    Ok(FrameCertificate {
        dimension: n,
        grams,
        determinants,
        quadratic,
        quartic,
        quadratic_sums,
        quartic_sums,
        deficit,
    })
}
pub fn dimension(labels: &[String]) -> Result<(usize, usize, bool)> {
    if labels.is_empty() {
        return Err("explicit labels required");
    }
    let n = labels.iter().collect::<BTreeSet<_>>().len();
    Ok((labels.len(), n, n >= 3))
}
#[cfg(test)]
mod tests {
    use super::*;
    fn q(n: i64) -> Q {
        Q::from_integer(n.into())
    }
    #[test]
    fn normalized_weak_contract_disagrees() {
        let r = weak_contract(vec![q(4), q(1)], vec![q(1), q(0)]).unwrap();
        assert_eq!(r[2], Q::new(4.into(), 5.into()));
        assert_eq!(r[3], Q::new(1.into(), 5.into()));
    }
    #[test]
    fn duplicate_labels_do_not_pay_dimension() {
        let ls = vec!["false".into(), "true".into(), "false".into()];
        assert_eq!(dimension(&ls).unwrap(), (3, 2, false));
    }
    #[test]
    fn quartic_rival_fails_actual_rotated_frame() {
        let c = frame(
            vec![q(5), q(0)],
            vec![
                vec![vec![q(5), q(0)], vec![q(0), q(5)]],
                vec![vec![q(3), q(4)], vec![q(-4), q(3)]],
            ],
        )
        .unwrap();
        assert_eq!(c.quadratic_sums, vec![q(1), q(1)]);
        assert_eq!(c.deficit, Q::new(288.into(), 625.into()));
    }
}
