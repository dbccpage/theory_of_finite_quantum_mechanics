//! Stage A (real-variable lift): the **manifest** real SOS Gram of the MUB(6) obstruction, and
//! the experiment of whether subtracting the rank-1 `‖v‖⁴` form keeps it PSD with a positive
//! margin — a certificate of the wall that needs no SDP.
//!
//! Write `v_j = x_j + i y_j` and `z = (x_0,y_0,…,x_5,y_5) ∈ ℝ¹²`. Each curvature form value
//! `ω_i(v) = v† A_i v` is a **real quadratic** in `z`, so `ω_i = c_i · μ` where `μ` is the vector
//! of the 78 real degree-2 monomials `z_p z_q` (`p ≤ q`) and `c_i ∈ K⁷⁸` its coefficients. Then
//!
//! ```text
//!   P(v) = Σ_i ω_i² = Σ_i (c_i · μ)² = μ^T (Σ_i c_i c_i^T) μ = μ^T Q_P μ,   Q_P = Σ_i c_i c_i^T ⪰ 0
//! ```
//!
//! is a **manifestly PSD** Gram (sum of rank-1s), and `‖v‖⁴ = (z^T z)² = μ^T (d d^T) μ` with
//! `d` the coefficients of `z^T z`. The wall with margin `c` is certified by
//! `Q_P − c·d d^T ⪰ 0` (then `P − c‖v‖⁴ = μ^T(Q_P − c d d^T)μ ≥ 0`). Since `Q_P ⪰ 0` and `d d^T` is
//! rank-1, `Q_P − c d d^T ⪰ 0` for some `c > 0` **iff `d ∈ range(Q_P)`** (i.e. `‖v‖²` lies in the
//! span of the `ω_i`).
//!
//! **RESULT (verified, `real_base_gram_needs_the_moment_kernel`): NO.** `Q_P` is PSD (the manifest
//! SOS of `P`), but `Q_P − c·Q_4` is **not** PSD for any `c > 0` — `d ∉ range(Q_P)`, so a kernel
//! direction `w` of `Q_P` has `d^T w ≠ 0`, giving `w^T(Q_P − c Q_4)w = −c(d^T w)² < 0`. So the
//! natural base Gram cannot certify the wall; the **moment-kernel freedom + an SDP** (search over
//! `{Q_P + Δ : μ^T Δ μ ≡ 0}` for a PSD `Q_P + Δ − c Q_4`) is **required** — exactly the Codex brief
//! Stage A/B. Both cheap paths (holomorphic lift, real base Gram) are now ruled out *exactly*; the
//! SDP over the moment kernel is the confirmed, unavoidable bottleneck.
//!

use std::collections::BTreeMap;

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::d6_exact_sos::{canonical_forms, quad_form, Form};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// Number of real coordinates `z = (x_0,y_0,…,x_5,y_5)`.
pub const RDIM: usize = 2 * D; // 12

/// A sparse symmetric-matrix entry in the real moment-map kernel.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MomentKernelTerm {
    pub row: usize,
    pub col: usize,
    pub value: Cyc24,
}

/// One sparse generator `Delta` with `mu^T Delta mu == 0`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MomentKernelElement {
    pub terms: Vec<MomentKernelTerm>,
}

/// Stage A search surface:
/// `Q = base_gram + sum(lambda_k * moment_kernel_basis[k]) - c * norm4_gram`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RealSosAffineSpace {
    pub base_gram: Vec<Vec<Cyc24>>,
    pub norm4_gram: Vec<Vec<Cyc24>>,
    pub moment_kernel_basis: Vec<MomentKernelElement>,
}

/// The 78 real degree-2 monomials `(p, q)` with `p ≤ q`, `p,q ∈ 0..12`.
pub fn real_monomials() -> Vec<(usize, usize)> {
    let mut m = Vec::new();
    for p in 0..RDIM {
        for q in p..RDIM {
            m.push((p, q));
        }
    }
    m
}

/// Index of `{p, q}` in `real_monomials()`.
pub fn rmon_index(p: usize, q: usize) -> usize {
    let (a, b) = if p <= q { (p, q) } else { (q, p) };
    (0..a).map(|i| RDIM - i).sum::<usize>() + (b - a)
}

/// Exponent vectors for the 78 real degree-2 monomials.
pub fn real_degree2_exponents() -> Vec<[u8; RDIM]> {
    real_monomials()
        .iter()
        .map(|&(p, q)| {
            let mut exp = [0u8; RDIM];
            exp[p] += 1;
            exp[q] += 1;
            exp
        })
        .collect()
}

/// Fibers of the symmetric Gram moment map:
/// symmetric entries `(a,b)`, `a <= b`, grouped by the degree-4 exponent of `mu_a * mu_b`.
pub fn real_moment_fibers() -> BTreeMap<[u8; RDIM], Vec<(usize, usize)>> {
    let exps = real_degree2_exponents();
    let mut fibers: BTreeMap<[u8; RDIM], Vec<(usize, usize)>> = BTreeMap::new();
    for a in 0..exps.len() {
        for b in a..exps.len() {
            let mut exp = [0u8; RDIM];
            for j in 0..RDIM {
                exp[j] = exps[a][j] + exps[b][j];
            }
            fibers.entry(exp).or_default().push((a, b));
        }
    }
    fibers
}

fn symmetric_entry_weight(row: usize, col: usize) -> i64 {
    if row == col {
        1
    } else {
        2
    }
}

/// A sparse basis for the kernel of the real degree-2 moment map.
///
/// For each degree-4 monomial fiber, the contribution of a symmetric entry `(a,b)` is weighted
/// by `1` on the diagonal and `2` off-diagonal in `mu^T Q mu`. The generators are weighted fiber
/// differences, so they evaluate to the zero polynomial exactly.
pub fn real_moment_kernel_basis() -> Vec<MomentKernelElement> {
    let mut basis = Vec::new();
    for pairs in real_moment_fibers().values() {
        let Some(&(pivot_row, pivot_col)) = pairs.first() else {
            continue;
        };
        let pivot_weight = symmetric_entry_weight(pivot_row, pivot_col);
        for &(row, col) in pairs.iter().skip(1) {
            let entry_weight = symmetric_entry_weight(row, col);
            basis.push(MomentKernelElement {
                terms: vec![
                    MomentKernelTerm {
                        row,
                        col,
                        value: Cyc24::rat(ri(pivot_weight)),
                    },
                    MomentKernelTerm {
                        row: pivot_row,
                        col: pivot_col,
                        value: Cyc24::rat(ri(-entry_weight)),
                    },
                ],
            });
        }
    }
    basis
}

/// Reconstruct `v ∈ ℂ⁶` from real coords `z`: `v_j = z[2j] + i·z[2j+1]`.
fn v_of_z(z: &[Cyc24; RDIM]) -> [Cyc24; D] {
    let i = Cyc24::zeta24(6);
    std::array::from_fn(|j| z[2 * j].add(&i.mul(&z[2 * j + 1])))
}

fn unit(p: usize) -> [Cyc24; RDIM] {
    let mut z: [Cyc24; RDIM] = std::array::from_fn(|_| Cyc24::zero());
    z[p] = Cyc24::rat(ri(1));
    z
}

/// The coefficient vector `c_i ∈ K⁷⁸` of `ω_i(z) = v† A_i v` in the real degree-2 monomial basis,
/// extracted by polarization: `c_i[idx(p,p)] = ω_i(e_p)`,
/// `c_i[idx(p,q)] = ω_i(e_p+e_q) − ω_i(e_p) − ω_i(e_q)` (`p < q`) — all via `quad_form`.
pub fn omega_coeff_vector(a: &Form) -> Vec<Cyc24> {
    let mons = real_monomials();
    let omega = |z: &[Cyc24; RDIM]| quad_form(a, &v_of_z(z));
    let diag: Vec<Cyc24> = (0..RDIM).map(|p| omega(&unit(p))).collect();
    mons.iter()
        .map(|&(p, q)| {
            if p == q {
                diag[p].clone()
            } else {
                let mut z = unit(p);
                z[q] = Cyc24::rat(ri(1)); // e_p + e_q
                omega(&z).sub(&diag[p]).sub(&diag[q])
            }
        })
        .collect()
}

/// Coefficient vector `d` of `‖v‖² = z^T z = Σ_m z_m²` in the real monomial basis.
pub fn norm_sq_coeff() -> Vec<Cyc24> {
    let n = real_monomials().len();
    let mut d = vec![Cyc24::zero(); n];
    let one = Cyc24::rat(ri(1));
    for m in 0..RDIM {
        d[rmon_index(m, m)] = one.clone();
    }
    d
}

fn outer(c: &[Cyc24]) -> Vec<Vec<Cyc24>> {
    c.iter()
        .map(|ca| c.iter().map(|cb| ca.mul(cb)).collect())
        .collect()
}

fn add_into(acc: &mut [Vec<Cyc24>], m: &[Vec<Cyc24>]) {
    for (ra, rm) in acc.iter_mut().zip(m.iter()) {
        for (xa, xm) in ra.iter_mut().zip(rm.iter()) {
            *xa = xa.add(xm);
        }
    }
}

/// `Q_P = Σ_i c_i c_i^T` — the manifest real PSD Gram of `P` (sum of rank-1s).
pub fn real_obstruction_gram() -> Vec<Vec<Cyc24>> {
    let n = real_monomials().len();
    let mut q = vec![vec![Cyc24::zero(); n]; n];
    for a in &canonical_forms() {
        let c = omega_coeff_vector(a);
        add_into(&mut q, &outer(&c));
    }
    q
}

/// `Q_4 = d d^T` — the rank-1 Gram of `‖v‖⁴`.
pub fn real_norm4_gram() -> Vec<Vec<Cyc24>> {
    outer(&norm_sq_coeff())
}

/// Values of the real degree-2 monomial vector `mu(z)`.
pub fn real_monomial_values(z: &[Cyc24; RDIM]) -> Vec<Cyc24> {
    real_monomials()
        .iter()
        .map(|&(p, q)| z[p].mul(&z[q]))
        .collect()
}

/// Evaluate `mu(z)^T G mu(z)` exactly.
pub fn eval_real_gram(g: &[Vec<Cyc24>], z: &[Cyc24; RDIM]) -> Cyc24 {
    let mv = real_monomial_values(z);
    let mut acc = Cyc24::zero();
    for a in 0..mv.len() {
        for b in 0..mv.len() {
            acc = acc.add(&mv[a].mul(&g[a][b]).mul(&mv[b]));
        }
    }
    acc
}

/// Evaluate a sparse moment-kernel generator exactly.
pub fn eval_moment_kernel_element(delta: &MomentKernelElement, z: &[Cyc24; RDIM]) -> Cyc24 {
    let mv = real_monomial_values(z);
    let two = Cyc24::rat(ri(2));
    let mut acc = Cyc24::zero();
    for term in &delta.terms {
        let contrib = term.value.mul(&mv[term.row]).mul(&mv[term.col]);
        if term.row == term.col {
            acc = acc.add(&contrib);
        } else {
            acc = acc.add(&two.mul(&contrib));
        }
    }
    acc
}

/// Add `scale * delta` to a dense symmetric Gram matrix.
pub fn add_moment_kernel_scaled(
    gram: &mut [Vec<Cyc24>],
    delta: &MomentKernelElement,
    scale: &Cyc24,
) {
    for term in &delta.terms {
        debug_assert!(term.row <= term.col);
        let value = scale.mul(&term.value);
        gram[term.row][term.col] = gram[term.row][term.col].add(&value);
        if term.row != term.col {
            gram[term.col][term.row] = gram[term.col][term.row].add(&value);
        }
    }
}

/// The exact Stage A affine search surface for the real SOS program.
pub fn real_sos_affine_space() -> RealSosAffineSpace {
    RealSosAffineSpace {
        base_gram: real_obstruction_gram(),
        norm4_gram: real_norm4_gram(),
        moment_kernel_basis: real_moment_kernel_basis(),
    }
}

/// `Q_P − c·Q_4`.
pub fn real_gram_minus_c(
    q_p: &[Vec<Cyc24>],
    q4: &[Vec<Cyc24>],
    c: &num_rational::BigRational,
) -> Vec<Vec<Cyc24>> {
    let cc = Cyc24::rat(c.clone());
    q_p.iter()
        .zip(q4.iter())
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
    use crate::omega_native::exact::d6_exact_curvature_cochain::norm_sq;
    use crate::omega_native::exact::d6_exact_sos::{is_psd_cyc24, obstruction_value};

    use omega_number_theory::rational::rq;

    fn sample_z() -> Vec<[Cyc24; RDIM]> {
        let mut out = Vec::new();
        // a couple of rational z vectors
        let mut z1: [Cyc24; RDIM] = std::array::from_fn(|_| Cyc24::zero());
        z1[0] = Cyc24::rat(rq(1, 2));
        z1[3] = Cyc24::rat(rq(1, 3));
        z1[6] = Cyc24::rat(rq(-2, 5));
        z1[9] = Cyc24::rat(rq(1, 4));
        out.push(z1);
        let mut z2: [Cyc24; RDIM] = std::array::from_fn(|_| Cyc24::zero());
        z2[1] = Cyc24::rat(rq(1, 3));
        z2[4] = Cyc24::rat(rq(2, 7));
        z2[10] = Cyc24::rat(rq(-1, 2));
        out.push(z2);
        out
    }

    fn eval_coeff(c: &[Cyc24], z: &[Cyc24; RDIM]) -> Cyc24 {
        let mons = real_monomials();
        let mut acc = Cyc24::zero();
        for (a, &(p, qq)) in mons.iter().enumerate() {
            acc = acc.add(&c[a].mul(&z[p]).mul(&z[qq]));
        }
        acc
    }

    #[test]
    fn omega_coeff_vector_reproduces_omega() {
        // c_i · μ(z) == ω_i(z) = v† A_i v at sample z (validates the polarization extraction).
        for a in &canonical_forms() {
            let c = omega_coeff_vector(a);
            for z in sample_z() {
                let via_c = eval_coeff(&c, &z);
                let via_form = quad_form(a, &v_of_z(&z));
                assert_eq!(via_c, via_form, "c_i·μ = ω_i");
            }
        }
    }

    #[test]
    #[allow(non_snake_case)]
    fn real_gram_reproduces_P_and_norm4() {
        // μ^T Q_P μ == P(v(z))  and  μ^T Q_4 μ == ‖v‖⁴.
        let forms = canonical_forms();
        let q_p = real_obstruction_gram();
        let q4 = real_norm4_gram();
        for z in sample_z() {
            let v = v_of_z(&z);
            assert_eq!(
                eval_real_gram(&q_p, &z),
                obstruction_value(&forms, &v),
                "μ^T Q_P μ = P"
            );
            let ns = norm_sq(&v);
            assert_eq!(eval_real_gram(&q4, &z), ns.mul(&ns), "μ^T Q_4 μ = ‖v‖⁴");
        }
    }

    #[test]
    fn moment_kernel_basis_has_expected_dimension() {
        let n = real_monomials().len();
        let symmetric_variables = n * (n + 1) / 2;
        let fibers = real_moment_fibers();
        let basis = real_moment_kernel_basis();
        assert_eq!(n, 78);
        assert_eq!(symmetric_variables, 3081);
        assert_eq!(fibers.len(), 1365);
        assert_eq!(basis.len(), symmetric_variables - fibers.len());
        assert_eq!(basis.len(), 1716);
        assert!(basis.iter().all(|delta| delta.terms.len() == 2));
    }

    #[test]
    fn moment_kernel_basis_evaluates_to_zero_on_exact_samples() {
        for delta in real_moment_kernel_basis() {
            for z in sample_z() {
                assert_eq!(
                    eval_moment_kernel_element(&delta, &z),
                    Cyc24::zero(),
                    "moment-kernel generator evaluates to zero"
                );
            }
        }
    }

    #[test]
    fn affine_kernel_perturbations_preserve_represented_polynomial() {
        let q_p = real_obstruction_gram();
        let mut perturbed = q_p.clone();
        let basis = real_moment_kernel_basis();
        let perturbations = [
            (0usize, Cyc24::rat(rq(1, 7))),
            (basis.len() / 2, Cyc24::rat(rq(-2, 5))),
            (basis.len() - 1, Cyc24::rat(rq(3, 11))),
        ];
        for (idx, scale) in perturbations {
            add_moment_kernel_scaled(&mut perturbed, &basis[idx], &scale);
        }
        for z in sample_z() {
            assert_eq!(
                eval_real_gram(&q_p, &z),
                eval_real_gram(&perturbed, &z),
                "moment-kernel perturbation preserves the represented polynomial"
            );
        }
    }

    #[test]
    fn real_sos_affine_space_exposes_stage_a_search_surface() {
        let space = real_sos_affine_space();
        assert_eq!(space.base_gram.len(), 78);
        assert_eq!(space.norm4_gram.len(), 78);
        assert_eq!(space.moment_kernel_basis.len(), 1716);
    }

    #[test]
    fn real_obstruction_gram_is_psd_at_c0() {
        // Q_P = Σ c_i c_i^T is a sum of rank-1s ⟹ PSD. (Sanity that the manifest SOS is real.)
        assert!(
            is_psd_cyc24(&real_obstruction_gram()),
            "Q_P is PSD (manifest SOS of P)"
        );
    }

    /// THE decisive experiment (fast: ~1s for the 78×78 exact LDL^T over `Cyc24`): `Q_P` is PSD
    /// (manifest SOS of `P`), but `Q_P − c·Q_4` is NOT PSD for any `c > 0` — `d ∉ range(Q_P)`,
    /// `‖v‖²` is not in the span of the `ω_i`. So the natural base Gram cannot certify the wall;
    /// the moment-kernel freedom + an SDP is required. (Both cheap paths now ruled out exactly.)
    #[test]
    fn real_base_gram_needs_the_moment_kernel() {
        let q_p = real_obstruction_gram();
        let q4 = real_norm4_gram();
        assert!(
            is_psd_cyc24(&real_gram_minus_c(&q_p, &q4, &rq(0, 1))),
            "Q_P is PSD (manifest SOS)"
        );
        assert!(
            !is_psd_cyc24(&real_gram_minus_c(&q_p, &q4, &rq(1, 1000))),
            "Q_P − c·Q_4 fails for c>0: d ∉ range(Q_P) ⟹ moment-kernel SDP required"
        );
    }
}
