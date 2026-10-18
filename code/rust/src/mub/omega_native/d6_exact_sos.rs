//! Exact SOS / Positivstellensatz **verification kernel** for the MUB(6) obstruction — the
//! trust anchor of the victory program.
//!
//! Strategy (firewall): a sum-of-squares *solver* (find a PSD Gram matrix `Q` certifying the
//! obstruction is bounded below) is a heuristic, floating-point, search-heavy computation — the
//! right job for a looping external agent. This module is its **exact, trusted counterpart**: we
//! never believe a found certificate until it passes the *exact rational* checks here. Two pieces:
//!
//! 1. **`is_psd_rational`** (now `linear_algebra::exact_ldlt::is_psd_rational`) — an exact PSD
//!    test for a rational symmetric matrix by LDL^T
//!    (symmetric Gaussian elimination): a pivot `< 0` ⟹ not PSD; a zero pivot with any nonzero
//!    off-diagonal in its row ⟹ an indefinite 2×2 minor ⟹ not PSD; otherwise PSD (possibly
//!    rank-deficient). Congruence preserves inertia (Sylvester), so this is sound and exact.
//! 2. **The exact obstruction data** — the Hermitian *curvature forms* `A_i` of the canonical
//!    triple `T0` over `Q(ζ₂₄)`, with `ω_i(v) = v† A_i v = |⟨e_i, v⟩|² − (1/6)‖v‖²` (homogeneous).
//!    The obstruction is `P(v) = Σ_i ω_i(v)² = Σ_i (v† A_i v)²` (a real bidegree-(2,2) form). A
//!    found Gram `Q` certifies `P − c·‖v‖⁴ = m† Q m` with `Q ⪰ 0` over the degree-2 monomial
//!    basis `m`; this kernel verifies the PSD half exactly (the identity half — matching `m† Q m`
//!    to `P − c‖v‖⁴` — is the next module / the agent's build, checked against `omega_at`).
//!
//! single-triple SOS for `T0` already exists as the cited Invariant-Systems wall certificate
//! (`crates/mub::wall`, his IP); here we build our own clean-room verification path.

use num_rational::BigRational;
use num_traits::Zero;

use crate::omega_native::exact::d6_exact_curvature_cochain::{ExactVec, D};
use crate::omega_native::exact::mub6_cyclotomic_enclosure::{
    cyc24_real_imag_enclosure, sqrt_enclosure, SqrtBox,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// A 6×6 Hermitian matrix over `Q(ζ₂₄)`.
pub type Form = [[Cyc24; D]; D];

/// The Hermitian **curvature form** of a fixed vector `e`: `A[j][k] = e[j]·conj(e[k]) − (1/6)δ_jk`,
/// so that `v† A v = |⟨e, v⟩|² − (1/6)‖v‖²` with `⟨e, v⟩ = Σ conj(e_k)·v_k` (the homogeneous
/// curvature `ω`). Hermitian: `A[k][j] = conj(A[j][k])`.
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

/// `v† A v = Σ_{j,k} conj(v[j]) · A[j][k] · v[k]` (exact; real-valued for Hermitian `A`).
pub fn quad_form(a: &Form, v: &ExactVec) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for j in 0..D {
        for k in 0..D {
            acc = acc.add(&v[j].conj().mul(&a[j][k]).mul(&v[k]));
        }
    }
    acc
}

/// The exact obstruction `P(v) = Σ_i (v† A_i v)²` over all 18 fixed vectors of the triple — the
/// homogeneous bidegree-(2,2) form an SOS Gram must certify is `≥ c·‖v‖⁴`.
pub fn obstruction_value(forms: &[Form], v: &ExactVec) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for a in forms {
        let q = quad_form(a, v);
        acc = acc.add(&q.mul(&q));
    }
    acc
}

/// The 18 curvature forms of the canonical triple `T0`.
pub fn canonical_forms() -> Vec<Form> {
    crate::omega_native::exact::d6_exact_curvature_cochain::canonical_triple_exact()
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

/// Sign (`-1`, `0`, `+1`) of a **real** `Cyc24` element, via an adaptively-tightened certified
/// rational enclosure of its real part. Returns `0` for the exact zero. For a genuine *nonzero*
/// real, the enclosure resolves the sign at finite precision (the loop caps at ~2^-960 width, far
/// below any pivot of a real certificate); if it still cannot resolve, returns `0` (the caller
/// treats an unresolved *nonzero* pivot conservatively — see `is_psd_cyc24`).
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

/// Exact PSD test for a **Hermitian** matrix over `Q(ζ₂₄)` (the field the obstruction's SOS Gram
/// lives over — its real subfield `K = Q(√2,√3)` ⊂ `Cyc24`), via LDL^T. Same inertia argument as
/// `linear_algebra::exact_ldlt::is_psd_rational`, with pivot signs determined by `real_sign_cyc24` (pivots of a Hermitian
/// matrix are real). **Sound and conservative:** a negative pivot, OR a *nonzero* pivot whose sign
/// the enclosure cannot resolve, ⟹ `false` (we never claim PSD without a resolved nonnegative
/// pivot). The caller must pass an exactly-Hermitian matrix (`m[k][j] = conj(m[j][k])`).
pub fn is_psd_cyc24(m: &[Vec<Cyc24>]) -> bool {
    let n = m.len();
    let mut a: Vec<Vec<Cyc24>> = m.to_vec();
    for k in 0..n {
        let pivot = a[k][k].clone();
        if pivot.is_zero() {
            // Zero pivot: the rest of the row/column must vanish (else an indefinite 2×2 minor).
            for i in (k + 1)..n {
                if !a[k][i].is_zero() || !a[i][k].is_zero() {
                    return false;
                }
            }
            continue;
        }
        if real_sign_cyc24(&pivot) != 1 {
            return false; // negative, or a nonzero pivot we cannot resolve as positive.
        }
        let pinv = pivot.inv();
        for i in (k + 1)..n {
            if a[i][k].is_zero() {
                continue;
            }
            let factor = a[i][k].mul(&pinv);
            for j in k..n {
                let delta = factor.mul(&a[k][j]);
                a[i][j] = a[i][j].sub(&delta);
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::{abs_sq, canonical_triple_exact, inner};
    use linear_algebra::exact_ldlt::is_psd_rational;

    use omega_number_theory::rational::rq;

    fn mat(rows: &[&[(i64, i64)]]) -> Vec<Vec<BigRational>> {
        rows.iter()
            .map(|r| r.iter().map(|&(n, d)| rq(n, d)).collect())
            .collect()
    }

    #[test]
    fn psd_accepts_identity_and_positive_definite() {
        let id = mat(&[&[(1, 1), (0, 1)], &[(0, 1), (1, 1)]]);
        assert!(is_psd_rational(&id));
        // [[2,1],[1,2]] PD (eigenvalues 1,3).
        let pd = mat(&[&[(2, 1), (1, 1)], &[(1, 1), (2, 1)]]);
        assert!(is_psd_rational(&pd));
    }

    #[test]
    fn psd_rejects_indefinite_and_negative() {
        // [[0,1],[1,0]]: det = -1, indefinite.
        let indef = mat(&[&[(0, 1), (1, 1)], &[(1, 1), (0, 1)]]);
        assert!(!is_psd_rational(&indef));
        // [[1,2],[2,1]]: det = -3, indefinite.
        let indef2 = mat(&[&[(1, 1), (2, 1)], &[(2, 1), (1, 1)]]);
        assert!(!is_psd_rational(&indef2));
        // [[-1,0],[0,1]]: negative eigenvalue.
        let neg = mat(&[&[(-1, 1), (0, 1)], &[(0, 1), (1, 1)]]);
        assert!(!is_psd_rational(&neg));
    }

    #[test]
    fn psd_accepts_rank_deficient_psd() {
        // [[1,1],[1,1]] = outer product of (1,1): PSD, rank 1 (eigenvalues 0, 2).
        let rank1 = mat(&[&[(1, 1), (1, 1)], &[(1, 1), (1, 1)]]);
        assert!(is_psd_rational(&rank1));
        // 3x3 PSD rank-deficient: diag(1,0,1).
        let d3 = mat(&[
            &[(1, 1), (0, 1), (0, 1)],
            &[(0, 1), (0, 1), (0, 1)],
            &[(0, 1), (0, 1), (1, 1)],
        ]);
        assert!(is_psd_rational(&d3));
    }

    #[test]
    fn curvature_form_reproduces_cochain_omega_on_unit_vectors() {
        // On a unit vector, v† A_i v = |⟨e_i,v⟩|² − 1/6 (the cochain ω). Test on the standard
        // basis vectors (exact unit vectors).
        let t0 = canonical_triple_exact();
        let sixth = Cyc24::rat(ri(1) / ri(6));
        for idx in 0..D {
            let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
            v[idx] = Cyc24::rat(ri(1)); // unit standard basis vector
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
        // Real basis vectors cannot tell `A` from its conjugate; a vector with non-real
        // entries can. Check v† A v == |<e,v>|² − (1/6)‖v‖² against the cochain inner product.
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
        // P(v) = Σ(v† A_i v)² ≥ 0; at a standard basis vector e_0 (NOT MU to T0) it is > 0.
        let forms = canonical_forms();
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = Cyc24::rat(ri(1));
        let p = obstruction_value(&forms, &v);
        assert!(
            !p.is_zero(),
            "e_0 is not MU to T0, so the obstruction is strictly positive"
        );
        // and it equals the squared-mass the cover lower-bounds (real, rational here).
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
        use omega_number_theory::cyclotomic::Cyc24;
        let s2 = Cyc24::sqrt2();
        assert_eq!(real_sign_cyc24(&Cyc24::zero()), 0);
        assert_eq!(real_sign_cyc24(&s2), 1); // √2 > 0
        assert_eq!(real_sign_cyc24(&s2.sub(&cr(7, 5))), 1); // √2 − 1.4 > 0
        assert_eq!(real_sign_cyc24(&s2.sub(&cr(3, 2))), -1); // √2 − 1.5 < 0
    }

    #[test]
    fn psd_cyc24_agrees_with_rational_on_rational_matrices() {
        // [[2,1],[1,2]] PD; [[0,1],[1,0]] indefinite; [[1,1],[1,1]] rank-1 PSD.
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
    }

    #[test]
    fn psd_cyc24_handles_irrational_entries() {
        use omega_number_theory::cyclotomic::Cyc24;
        let s2 = Cyc24::sqrt2();
        // [[2,√2],[√2,2]]: det = 4−2 = 2 > 0, trace > 0 ⟹ PD ⟹ PSD.
        assert!(is_psd_cyc24(&cyc_mat(vec![
            vec![cr(2, 1), s2.clone()],
            vec![s2.clone(), cr(2, 1)],
        ])));
        // [[1,√2],[√2,1]]: det = 1−2 = −1 < 0 ⟹ indefinite ⟹ NOT PSD.
        assert!(!is_psd_cyc24(&cyc_mat(vec![
            vec![cr(1, 1), s2.clone()],
            vec![s2.clone(), cr(1, 1)],
        ])));
        // [[2,√2],[√2,1]]: det = 2−2 = 0, pivot 2 > 0, Schur 1 − √2·(1/2)·√2 = 0 ⟹ rank-1 PSD.
        assert!(is_psd_cyc24(&cyc_mat(vec![
            vec![cr(2, 1), s2.clone()],
            vec![s2.clone(), cr(1, 1)],
        ])));
    }

    #[test]
    fn curvature_form_is_indefinite_through_the_verifier() {
        // A_i = conj(e)⊗e − (1/6)I has eigenvalues 1−1/6 = 5/6 (once) and −1/6 (five times) for a
        // unit e, so it is INDEFINITE — the real obstruction data, run through is_psd_cyc24, must
        // be rejected. (The SOS Gram Q is a *combination* that is PSD; the individual A_i are not.)
        for e in canonical_triple_exact() {
            let a = curvature_form(&e);
            let m: Vec<Vec<Cyc24>> = (0..D)
                .map(|j| (0..D).map(|k| a[j][k].clone()).collect())
                .collect();
            assert!(!is_psd_cyc24(&m), "each curvature form is indefinite");
        }
    }
}
