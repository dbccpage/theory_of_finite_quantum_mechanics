
use std::collections::BTreeMap;

use crate::native::exact::d6_exact_curvature_cochain::D;
use crate::native::exact::d6_exact_sos::{canonical_forms, quad_form, Form};
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

pub const RDIM: usize = 2 * D;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MomentKernelTerm {
    pub row: usize,
    pub col: usize,
    pub value: Cyc24,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MomentKernelElement {
    pub terms: Vec<MomentKernelTerm>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RealSosAffineSpace {
    pub base_gram: Vec<Vec<Cyc24>>,
    pub norm4_gram: Vec<Vec<Cyc24>>,
    pub moment_kernel_basis: Vec<MomentKernelElement>,
}

pub fn real_monomials() -> Vec<(usize, usize)> {
    let mut m = Vec::new();
    for p in 0..RDIM {
        for q in p..RDIM {
            m.push((p, q));
        }
    }
    m
}

pub fn rmon_index(p: usize, q: usize) -> usize {
    let (a, b) = if p <= q { (p, q) } else { (q, p) };
    (0..a).map(|i| RDIM - i).sum::<usize>() + (b - a)
}

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

fn v_of_z(z: &[Cyc24; RDIM]) -> [Cyc24; D] {
    let i = Cyc24::zeta24(6);
    std::array::from_fn(|j| z[2 * j].add(&i.mul(&z[2 * j + 1])))
}

fn unit(p: usize) -> [Cyc24; RDIM] {
    let mut z: [Cyc24; RDIM] = std::array::from_fn(|_| Cyc24::zero());
    z[p] = Cyc24::rat(ri(1));
    z
}

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
                z[q] = Cyc24::rat(ri(1));
                omega(&z).sub(&diag[p]).sub(&diag[q])
            }
        })
        .collect()
}

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

pub fn real_obstruction_gram() -> Vec<Vec<Cyc24>> {
    let n = real_monomials().len();
    let mut q = vec![vec![Cyc24::zero(); n]; n];
    for a in &canonical_forms() {
        let c = omega_coeff_vector(a);
        add_into(&mut q, &outer(&c));
    }
    q
}

pub fn real_norm4_gram() -> Vec<Vec<Cyc24>> {
    outer(&norm_sq_coeff())
}

pub fn real_monomial_values(z: &[Cyc24; RDIM]) -> Vec<Cyc24> {
    real_monomials()
        .iter()
        .map(|&(p, q)| z[p].mul(&z[q]))
        .collect()
}

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

pub fn real_sos_affine_space() -> RealSosAffineSpace {
    RealSosAffineSpace {
        base_gram: real_obstruction_gram(),
        norm4_gram: real_norm4_gram(),
        moment_kernel_basis: real_moment_kernel_basis(),
    }
}

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
    use crate::native::exact::d6_exact_curvature_cochain::norm_sq;
    use crate::native::exact::d6_exact_sos::{is_psd_cyc24, obstruction_value};

    use tfqm_number_theory::rational::rq;

    fn sample_z() -> Vec<[Cyc24; RDIM]> {
        let mut out = Vec::new();
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
        assert!(
            is_psd_cyc24(&real_obstruction_gram()),
            "Q_P is PSD (manifest SOS of P)"
        );
    }

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
