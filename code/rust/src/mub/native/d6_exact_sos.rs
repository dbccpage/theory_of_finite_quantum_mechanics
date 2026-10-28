
use num_rational::BigRational;
use num_traits::Zero;

use crate::native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::native::exact::mub6_cyclotomic_enclosure::{
    cyc24_real_imag_enclosure, sqrt_enclosure, SqrtBox,
};
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

pub type Form = [[Cyc24; D]; D];

pub fn curvature_form(e: &ExactVec) -> Form {
    let sixth = Cyc24::rat(ri(1) / ri(6));
    std::array::from_fn(|j| {
        std::array::from_fn(|k| {
            let mut a = e[j].mul(&e[k].conj());
            if j == k {
                a = a.sub(&sixth);
            }
            a
        })
    })
}

pub fn quad_form(a: &Form, v: &ExactVec) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for j in 0..D {
        for k in 0..D {
            acc = acc.add(&v[j].conj().mul(&a[j][k]).mul(&v[k]));
        }
    }
    acc
}

pub fn obstruction_value(forms: &[Form], v: &ExactVec) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for a in forms {
        let q = quad_form(a, v);
        acc = acc.add(&q.mul(&q));
    }
    acc
}

pub fn canonical_forms() -> Vec<Form> {
    crate::native::exact::d6_exact_curvature_cochain::canonical_triple_exact()
        .iter()
        .map(curvature_form)
        .collect()
}

fn sqrtbox_prec(iters: u32) -> SqrtBox {
    SqrtBox {
        sqrt2: sqrt_enclosure(2, iters),
        sqrt3: sqrt_enclosure(3, iters),
        sqrt6: sqrt_enclosure(6, iters),
    }
}

pub fn real_sign_cyc24(z: &Cyc24) -> i32 {
    if z.is_zero() {
        return 0;
    }
    for &iters in &[60u32, 120, 240, 480, 960] {
        let sb = sqrtbox_prec(iters);
        let (re, _im) = cyc24_real_imag_enclosure(z, &sb);
        if re.lo() > &BigRational::zero() {
            return 1;
        }
        if re.hi() < &BigRational::zero() {
            return -1;
        }
    }
    0
}

fn zero_pivot_off_diagonal_clean(a: &[Vec<Cyc24>], k: usize, n: usize) -> bool {
    for i in (k + 1)..n {
        if !a[k][i].is_zero() || !a[i][k].is_zero() {
            return false;
        }
    }
    true
}

fn schur_update_cyc24(a: &mut [Vec<Cyc24>], k: usize, n: usize, pinv: &Cyc24) {
    for i in (k + 1)..n {
        if a[i][k].is_zero() {
            continue;
        }
        let factor = a[i][k].mul(pinv);
        for j in k..n {
            let delta = factor.mul(&a[k][j]);
            a[i][j] = a[i][j].sub(&delta);
        }
    }
}

pub fn is_psd_cyc24(m: &[Vec<Cyc24>]) -> bool {
    let n = m.len();
    if m.iter().any(|row| row.len() != n) {
        return false;
    }
    let mut a: Vec<Vec<Cyc24>> = m.to_vec();
    for k in 0..n {
        let pivot = a[k][k].clone();
        if pivot.is_zero() {
            if !zero_pivot_off_diagonal_clean(&a, k, n) {
                return false;
            }
            continue;
        }
        if real_sign_cyc24(&pivot) != 1 {
            return false;
        }
        let pinv = pivot.inv();
        schur_update_cyc24(&mut a, k, n, &pinv);
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::native::exact::d6_exact_curvature_cochain::{abs_sq, canonical_triple_exact, inner};
    use linear_algebra::exact_ldlt::is_psd_rational;

    use tfqm_number_theory::rational::rq;

    fn mat(rows: &[&[(i64, i64)]]) -> Vec<Vec<BigRational>> {
        rows.iter()
            .map(|r| r.iter().map(|&(n, d)| rq(n, d)).collect())
            .collect()
    }

    #[test]
    fn psd_accepts_identity_and_positive_definite() {
        let id = mat(&[&[(1, 1), (0, 1)], &[(0, 1), (1, 1)]]);
        assert!(is_psd_rational(&id));
        let pd = mat(&[&[(2, 1), (1, 1)], &[(1, 1), (2, 1)]]);
        assert!(is_psd_rational(&pd));
    }

    #[test]
    fn psd_rejects_indefinite_and_negative() {
        let indef = mat(&[&[(0, 1), (1, 1)], &[(1, 1), (0, 1)]]);
        assert!(!is_psd_rational(&indef));
        let indef2 = mat(&[&[(1, 1), (2, 1)], &[(2, 1), (1, 1)]]);
        assert!(!is_psd_rational(&indef2));
        let neg = mat(&[&[(-1, 1), (0, 1)], &[(0, 1), (1, 1)]]);
        assert!(!is_psd_rational(&neg));
    }

    #[test]
    fn psd_accepts_rank_deficient_psd() {
        let rank1 = mat(&[&[(1, 1), (1, 1)], &[(1, 1), (1, 1)]]);
        assert!(is_psd_rational(&rank1));
        let d3 = mat(&[
            &[(1, 1), (0, 1), (0, 1)],
            &[(0, 1), (0, 1), (0, 1)],
            &[(0, 1), (0, 1), (1, 1)],
        ]);
        assert!(is_psd_rational(&d3));
    }

    #[test]
    fn curvature_form_reproduces_cochain_omega_on_unit_vectors() {
        let t0 = canonical_triple_exact();
        let sixth = Cyc24::rat(ri(1) / ri(6));
        for idx in 0..D {
            let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
            v[idx] = Cyc24::rat(ri(1));
            for e in &t0 {
                let a = curvature_form(e);
                let viaform = quad_form(&a, &v);
                let viacochain = abs_sq(&inner(e, &v)).sub(&sixth);
                assert_eq!(viaform, viacochain, "v† A v == |<e,v>|² − 1/6 on unit v");
            }
        }
    }

    #[test]
    fn curvature_form_reproduces_cochain_omega_on_complex_vectors() {
        let t0 = canonical_triple_exact();
        let v: ExactVec = std::array::from_fn(|k| Cyc24::zeta24(5 * k as i32 + 1));
        let norm_sq = v.iter().fold(Cyc24::zero(), |acc, z| acc.add(&abs_sq(z)));
        let target = norm_sq.mul(&Cyc24::rat(ri(1) / ri(6)));
        for e in &t0 {
            let viaform = quad_form(&curvature_form(e), &v);
            let viacochain = abs_sq(&inner(e, &v)).sub(&target);
            assert_eq!(viaform, viacochain, "v† A v == |<e,v>|² − ‖v‖²/6 on complex v");
        }
    }

    #[test]
    fn obstruction_is_zero_only_at_mu_vectors_sample() {
        let forms = canonical_forms();
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = Cyc24::rat(ri(1));
        let p = obstruction_value(&forms, &v);
        assert!(
            !p.is_zero(),
            "e_0 is not MU to T0, so the obstruction is strictly positive"
        );
        assert_eq!(forms.len(), 18);
    }

    fn cr(n: i64, d: i64) -> Cyc24 {
        Cyc24::rat(rq(n, d))
    }

    fn cyc_mat(rows: Vec<Vec<Cyc24>>) -> Vec<Vec<Cyc24>> {
        rows
    }

    #[test]
    fn real_sign_cyc24_resolves_known_values() {
        use tfqm_number_theory::cyclotomic::Cyc24;
        let s2 = Cyc24::sqrt2();
        assert_eq!(real_sign_cyc24(&Cyc24::zero()), 0);
        assert_eq!(real_sign_cyc24(&s2), 1);
        assert_eq!(real_sign_cyc24(&s2.sub(&cr(7, 5))), 1);
        assert_eq!(real_sign_cyc24(&s2.sub(&cr(3, 2))), -1);
    }

    #[test]
    fn psd_cyc24_agrees_with_rational_on_rational_matrices() {
        assert!(is_psd_cyc24(&cyc_mat(vec![
            vec![cr(2, 1), cr(1, 1)],
            vec![cr(1, 1), cr(2, 1)]
        ])));
        assert!(!is_psd_cyc24(&cyc_mat(vec![
            vec![cr(0, 1), cr(1, 1)],
            vec![cr(1, 1), cr(0, 1)]
        ])));
        assert!(is_psd_cyc24(&cyc_mat(vec![
            vec![cr(1, 1), cr(1, 1)],
            vec![cr(1, 1), cr(1, 1)]
        ])));
        assert!(!is_psd_cyc24(&cyc_mat(vec![
            vec![cr(1, 1)],
            vec![cr(1, 1), cr(1, 1)]
        ])));
    }

    #[test]
    fn psd_cyc24_handles_irrational_entries() {
        use tfqm_number_theory::cyclotomic::Cyc24;
        let s2 = Cyc24::sqrt2();
        assert!(is_psd_cyc24(&cyc_mat(vec![
            vec![cr(2, 1), s2.clone()],
            vec![s2.clone(), cr(2, 1)],
        ])));
        assert!(!is_psd_cyc24(&cyc_mat(vec![
            vec![cr(1, 1), s2.clone()],
            vec![s2.clone(), cr(1, 1)],
        ])));
        assert!(is_psd_cyc24(&cyc_mat(vec![
            vec![cr(2, 1), s2.clone()],
            vec![s2.clone(), cr(1, 1)],
        ])));
    }

    #[test]
    fn curvature_form_is_indefinite_through_the_verifier() {
        for e in canonical_triple_exact() {
            let a = curvature_form(&e);
            let m: Vec<Vec<Cyc24>> = (0..D)
                .map(|j| (0..D).map(|k| a[j][k].clone()).collect())
                .collect();
            assert!(!is_psd_cyc24(&m), "each curvature form is indefinite");
        }
    }
}
