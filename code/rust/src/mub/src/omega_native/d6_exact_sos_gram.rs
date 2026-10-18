//! Stage A of the SOS victory program: the **exact bare Hermitian Gram** of the MUB(6)
//! obstruction on the degree-2 monomial basis, and the experiment of whether it already
//! certifies a positive margin.
//!
//! The obstruction `P(v) = Σ_i (v† A_i v)²` is a real bidegree-(2,2) form. On the basis of the
//! 21 degree-2 monomials `m_a = v_{j}v_{k}` (`j ≤ k`), the monomials `conj(m_a)·m_b` are in
//! bijection with bidegree-(2,2) monomials, so `P` has a **unique** Hermitian Gram `G_P`:
//! `P(v) = m(v)† G_P m(v)`. Likewise `‖v‖⁴ = m† G_4 m`. A certificate of the wall is then a
//! margin `c > 0` with `G_P − c·G_4 ⪰ 0` (Hermitian PSD) — which, by `is_psd_cyc24`, makes
//! `P − c‖v‖⁴ = m†(G_P − c G_4)m ≥ 0`, i.e. `P ≥ c‖v‖⁴`, the no-fourth-MU-vector wall with margin `c`.
//!
//! On this holomorphic lift the Gram is **forced** (the `conj(m_a)·m_b` are independent
//! monomials, so there is *no* freedom): `G_P − c·G_4 ⪰ 0` would be a sufficient certificate, but
//! it is the only candidate, so if it fails the lift cannot certify at all.
//!
//! **RESULT (verified, `bare_gram_psd_margin_experiment`): `G_P` is NOT PSD even at `c = 0`.**
//! This is the genuine PSD-vs-SOS gap: `P = m† G_P m` is nonnegative only on the Veronese variety
//! `{m(v)}`, not as a holomorphic sum of squares, and the freedom-less holomorphic lift cannot
//! bridge it. **So the certificate requires the *real-variable* SOS lift** — a real symmetric Gram
//! on the 78 real degree-2 monomials in `(x_0,y_0,…,x_5,y_5)`, where the moment map has a nontrivial
//! kernel (genuine freedom) and an SDP search over it is required (the Codex brief, Stage A/B). The
//! same verifier `is_psd_cyc24` checks that real Gram (a real symmetric matrix is Hermitian with
//! real entries). This module's exact `obstruction_gram`/`eval_gram` infrastructure carries over.
//!
//! Either way this is decisive and exact: it *rules out* the cheap holomorphic path and pins the
//! work to the real-variable SDP.
//!
//! `MUB(6) ≤ 3` claim.

use num_rational::BigRational;

use crate::omega_native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::omega_native::exact::d6_exact_sos::canonical_forms;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// The 21 degree-2 monomials `(j, k)` with `j ≤ k`.
pub fn monomials() -> Vec<(usize, usize)> {
    let mut m = Vec::new();
    for j in 0..D {
        for k in j..D {
            m.push((j, k));
        }
    }
    m
}

/// Index of the (unordered) degree-2 monomial `{j, k}` in `monomials()`.
pub fn mon_index(j: usize, k: usize) -> usize {
    let (a, b) = if j <= k { (j, k) } else { (k, j) };
    (0..a).map(|i| D - i).sum::<usize>() + (b - a)
}

/// The exact Hermitian Gram `G_P` of the obstruction `P = Σ_i (v† A_i v)²`:
/// `G_P[idx(p,r)][idx(q,s)] += (A_i)_{pq} (A_i)_{rs}` summed over `i` and all `(p,q,r,s)`
/// (the term `(A_i)_{pq}(A_i)_{rs} · v̄_p v̄_r v_q v_s = (A_i)_{pq}(A_i)_{rs} · conj(m_{pr}) m_{qs}`).
pub fn obstruction_gram() -> Vec<Vec<Cyc24>> {
    let forms = canonical_forms();
    let n = monomials().len();
    let mut g = vec![vec![Cyc24::zero(); n]; n];
    for a in &forms {
        for p in 0..D {
            for q in 0..D {
                for r in 0..D {
                    for s in 0..D {
                        let ma = mon_index(p, r);
                        let mb = mon_index(q, s);
                        let coeff = a[p][q].mul(&a[r][s]);
                        g[ma][mb] = g[ma][mb].add(&coeff);
                    }
                }
            }
        }
    }
    g
}

/// The exact Hermitian Gram `G_4` of `‖v‖⁴ = Σ_{p,r} v̄_p v̄_r v_p v_r`.
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

/// Evaluate `m(v)† G m(v)` exactly (the Gram applied to the monomial vector at `v`).
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

/// `G_P − c·G_4` (the candidate certificate matrix at margin `c`).
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
    use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, norm_sq};
    use crate::omega_native::exact::d6_exact_sos::{is_psd_cyc24, obstruction_value};

    use omega_number_theory::rational::rq;

    /// A few exact sample vectors (not necessarily unit) to test the polynomial identities.
    fn sample_vecs() -> Vec<ExactVec> {
        let mut out = Vec::new();
        // standard basis vectors
        for idx in 0..D {
            let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
            v[idx] = Cyc24::rat(ri(1));
            out.push(v);
        }
        // a couple of mixed rational vectors
        let mut v1: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v1[0] = Cyc24::rat(rq(1, 2));
        v1[1] = Cyc24::rat(rq(1, 3));
        v1[3] = Cyc24::rat(rq(-2, 5));
        out.push(v1);
        // one with a cyclotomic entry
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
        // THE experiment: is the (forced) bare Hermitian Gram G_P − c·G_4 PSD for some c > 0?
        // If yes at some c>0, that is our own clean-room SOS certificate of the wall (closes T1).
        let g_p = obstruction_gram();
        let g4 = norm4_gram();
        // c = 0: G_P itself. c = 1: far above any possible margin (must be non-PSD).
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
        // THE FINDING: the forced holomorphic Gram is NOT PSD even at c = 0. P = m† G_P m is
        // nonnegative only on the Veronese variety {m(v)}, not as a holomorphic SOS, and this
        // freedom-less lift cannot bridge the PSD-SOS gap — so it cannot certify the wall at ANY
        // c ≥ 0. The certificate therefore needs the REAL-variable SOS lift (with moment freedom +
        // SDP). This rules out the cheap path exactly.
        assert!(
            !psd_at(rq(0, 1)),
            "forced holomorphic Gram of P is not PSD (PSD-SOS gap)"
        );
        assert!(!psd_at(rq(1, 1)), "and a fortiori not at any c > 0");
        // Sanity: the forms are the canonical 18.
        assert_eq!(canonical_triple_exact().len(), 18);
    }
}
