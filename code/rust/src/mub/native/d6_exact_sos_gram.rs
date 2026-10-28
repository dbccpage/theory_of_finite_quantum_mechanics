
use num_rational::BigRational;

use crate::native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::native::exact::d6_exact_sos::canonical_forms;
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;

pub fn monomials() -> Vec<(usize, usize)> {
    let mut m = Vec::new();
    for j in 0..D {
        for k in j..D {
            m.push((j, k));
        }
    }
    m
}

pub fn mon_index(j: usize, k: usize) -> usize {
    let (a, b) = if j <= k { (j, k) } else { (k, j) };
    (0..a).map(|i| D - i).sum::<usize>() + (b - a)
}

fn accumulate_form_pair_into_gram(
    g: &mut [Vec<Cyc24>],
    a: &crate::native::exact::d6_exact_sos::Form,
    p: usize,
    q: usize,
) {
    for r in 0..D {
        let ma = mon_index(p, r);
        for s in 0..D {
            let mb = mon_index(q, s);
            let coeff = a[p][q].mul(&a[r][s]);
            g[ma][mb] = g[ma][mb].add(&coeff);
        }
    }
}

pub fn obstruction_gram() -> Vec<Vec<Cyc24>> {
    let forms = canonical_forms();
    let n = monomials().len();
    let mut g = vec![vec![Cyc24::zero(); n]; n];
    for a in &forms {
        for p in 0..D {
            for q in 0..D {
                accumulate_form_pair_into_gram(&mut g, a, p, q);
            }
        }
    }
    g
}

pub fn norm4_gram() -> Vec<Vec<Cyc24>> {
    let n = monomials().len();
    let mut g = vec![vec![Cyc24::zero(); n]; n];
    let one = Cyc24::rat(ri(1));
    for p in 0..D {
        for r in 0..D {
            let idx = mon_index(p, r);
            g[idx][idx] = g[idx][idx].add(&one);
        }
    }
    g
}

pub fn eval_gram(g: &[Vec<Cyc24>], v: &ExactVec) -> Cyc24 {
    let mons = monomials();
    let mvec: Vec<Cyc24> = mons.iter().map(|&(j, k)| v[j].mul(&v[k])).collect();
    let mvec_conj: Vec<Cyc24> = mvec.iter().map(|m| m.conj()).collect();
    let mut acc = Cyc24::zero();
    for a in 0..mvec.len() {
        for b in 0..mvec.len() {
            acc = acc.add(&mvec_conj[a].mul(&g[a][b]).mul(&mvec[b]));
        }
    }
    acc
}

pub fn gram_minus_c_norm4(
    g_p: &[Vec<Cyc24>],
    g4: &[Vec<Cyc24>],
    c: &BigRational,
) -> Vec<Vec<Cyc24>> {
    let cc = Cyc24::rat(c.clone());
    g_p.iter()
        .zip(g4.iter())
        .map(|(rp, r4)| {
            rp.iter()
                .zip(r4.iter())
                .map(|(xp, x4)| xp.sub(&cc.mul(x4)))
                .collect()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, norm_sq};
    use crate::native::exact::d6_exact_sos::{is_psd_cyc24, obstruction_value};

    use engine_number_theory::rational::rq;

    fn sample_vecs() -> Vec<ExactVec> {
        let mut out = Vec::new();
        for idx in 0..D {
            let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
            v[idx] = Cyc24::rat(ri(1));
            out.push(v);
        }
        let mut v1: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v1[0] = Cyc24::rat(rq(1, 2));
        v1[1] = Cyc24::rat(rq(1, 3));
        v1[3] = Cyc24::rat(rq(-2, 5));
        out.push(v1);
        let mut v2: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v2[0] = Cyc24::rat(rq(1, 2));
        v2[2] = Cyc24::zeta24(2).mul(&Cyc24::rat(rq(1, 3)));
        v2[4] = Cyc24::rat(rq(1, 4));
        out.push(v2);
        out
    }

    #[test]
    fn mon_index_matches_monomial_order_without_underflow() {
        let mons = monomials();
        for (idx, &(j, k)) in mons.iter().enumerate() {
            assert_eq!(mon_index(j, k), idx);
            assert_eq!(mon_index(k, j), idx);
        }
        assert_eq!(mon_index(0, 0), 0);
        assert_eq!(mon_index(0, D - 1), D - 1);
    }

    #[test]
    #[allow(non_snake_case)]
    fn obstruction_gram_reproduces_P() {
        let forms = canonical_forms();
        let g = obstruction_gram();
        for v in sample_vecs() {
            assert_eq!(
                eval_gram(&g, &v),
                obstruction_value(&forms, &v),
                "m† G_P m = P(v)"
            );
        }
    }

    #[test]
    fn norm4_gram_reproduces_norm_squared_squared() {
        let g4 = norm4_gram();
        for v in sample_vecs() {
            let ns = norm_sq(&v);
            assert_eq!(eval_gram(&g4, &v), ns.mul(&ns), "m† G_4 m = ‖v‖⁴");
        }
    }

    #[test]
    fn obstruction_gram_is_hermitian() {
        let g = obstruction_gram();
        let n = g.len();
        for a in 0..n {
            for b in 0..n {
                assert_eq!(g[a][b], g[b][a].conj(), "G_P Hermitian");
            }
        }
    }

    #[test]
    fn bare_gram_psd_margin_experiment() {
        let g_p = obstruction_gram();
        let g4 = norm4_gram();
        let psd_at = |c: BigRational| is_psd_cyc24(&gram_minus_c_norm4(&g_p, &g4, &c));
        for (num, den) in [
            (0i64, 1i64),
            (1, 1000),
            (1, 100),
            (1, 40),
            (1, 20),
            (1, 10),
            (1, 1),
        ] {
            let res = psd_at(rq(num, den));
            eprintln!("BARE_GRAM_PSD c={num}/{den}: {res}");
        }
        assert!(
            !psd_at(rq(0, 1)),
            "forced holomorphic Gram of P is not PSD (PSD-SOS gap)"
        );
        assert!(!psd_at(rq(1, 1)), "and a fortiori not at any c > 0");
        assert_eq!(canonical_triple_exact().len(), 18);
    }
}
