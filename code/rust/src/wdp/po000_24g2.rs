//! PO-000 §5.2--§5.4.1 and §5.8 (J = 1): the `24 g^2` short-time defect
//! chain, computed exactly on declared qubit instances.
//!
//! Paper: `projection_obstruction.md` (external atlas, paper 002).
//!
//! * Lemma 5.2: the support-counting constants `2g`, `8g^2`, `24g^2` are
//!   *computed* by [`counting_constants`] from the counting rules (a
//!   commutator with a term costs a factor `2||h_X||`; each nested commutator
//!   grows the support by at most `k_max - 1 = 1` site). The `F_e''` bound
//!   `24 + 8 + 2(2)(2) + 8 = 48` and the Taylor coefficient `48 / 2 = 24`
//!   come out of the same function. Lemma 5.4 gives a second, independent
//!   route to `24` ([`theorem55_remainder_coeff`] at `J = 1`).
//! * On each declared instance the code computes, exactly over Gaussian
//!   rationals: `rho(0)`, the Taylor jets `rho^(k)(0)`, `rho_e(0)`,
//!   `L_e = rho_e'(0)`, the tangent projection `P_e`, `n_e = Q_e L_e`, the
//!   residual jets `F_e^(j)(0)`, the per-term normal contributions of
//!   Lemma 5.3, the instance branch counts behind Lemma 5.2, and `g`.
//! * Irrational spectral quantities (`nu_e`, operator norms, `D_e(t)`) are
//!   rational intervals certified by Sturm sequences (`po000_exact`).
//! * `D_e(t)` at rational `t` is enclosed by an exact truncated Taylor
//!   series of `rho(t)` plus the rigorous exponential tail bound
//!   `sum_{k>K} (w t)^k / k!` with `w >= ||generator||_{1->1}`. This tail bound
//!   is independent of the paper's lemmas.
//!
//! Scope: everything here is a finite-instance computation. The general
//! theorem for all finite graphs and all `t` is not established by
//! computation. The branch-count bound `||ad_H^2(A_S)|| <= c2(S)` used for
//! "all `s`" is the paper's triangle-inequality argument; the code computes
//! its instance constant exactly and spot-checks it against exact
//! `||ad_H^2(A_S)||` for Pauli `A_S` and against `||F_e''(0)||_1`.

use super::po000_exact::{
    embed, op_norm, ptrace, qi, qr, trace_norm, two_pow_neg, Cx, ExactError, Iv, Mat, Q,
};
use num_bigint::BigInt;
use num_traits::{One, Zero};

pub const ORIGIN: &str = "Origin: code/rust/src/wdp/po000_24g2.rs";
pub const CLAIM: &str = "Claim: on declared finite qubit instances, the Lemma 5.2 counting constants, the Lemma 5.3 tangent isolation, and the Theorem 5.1 / Theorem 5.5 (J=1) inequalities D_e(t) >= nu_e t - 24 g^2 t^2 and |D_e(t) - nu_e t| <= 24 g^2 t^2 hold, computed exactly; no general theorem is established by computation";
pub const AUTHORITY_EFFECT_TEXT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

// ---------------------------------------------------------------------------
// Lemma 5.2 / Appendix B / Lemma 5.4: constants from support counting.
// ---------------------------------------------------------------------------

/// Support-counting constants, in units of the incident strength.
///
/// `unit` is the factor one commutator contributes per unit of incident norm:
/// `2` for Hamiltonian terms measured by `g` (`||[h, A]|| <= 2||h|| ||A||`),
/// and `1` for the Lindblad strength `Lambda_*` of §5.4.1, which already
/// contains that factor. `k_max` is the largest interaction support.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CountingConstants {
    pub unit: u64,
    pub k_max: u64,
    /// `||L^dag(A_a)|| <= first_one_site * g` for `|S| = 1`.
    pub first_one_site: u64,
    /// `||(L^dag)^2(A_a)|| <= second_one_site * g^2`.
    pub second_one_site: u64,
    /// `||(L^dag)^2(A_ab)|| <= second_two_site * g^2`.
    pub second_two_site: u64,
    /// `||F_e''|| <= residual_second * g^2` (product rule, Appendix B).
    pub residual_second: u64,
    /// Taylor coefficient `residual_second / 2` in `D_e >= nu t - c g^2 t^2`.
    pub theorem_coeff: Q,
}

/// First commutator: terms meeting `S` have total norm `<= |S| g`.
pub fn support_count_first(unit: u64, s: u64) -> u64 {
    unit * s
}

/// Second commutator: after a term `X` meets `S`, the support `S cup X` has at
/// most `|S| + k_max - 1` sites, so the outer sum is `<= (|S| + k_max - 1) g`.
pub fn support_count_second(unit: u64, s: u64, k_max: u64) -> u64 {
    (unit * s) * (unit * (s + k_max - 1))
}

pub fn counting_constants(unit: u64, k_max: u64) -> CountingConstants {
    let first_one_site = support_count_first(unit, 1);
    let second_one_site = support_count_second(unit, 1, k_max);
    let second_two_site = support_count_second(unit, 2, k_max);
    // F'' = rho_e'' - rho_a'' (x) rho_b - 2 rho_a' (x) rho_b' - rho_a (x) rho_b''.
    let residual_second =
        second_two_site + second_one_site + 2 * first_one_site * first_one_site + second_one_site;
    CountingConstants {
        unit,
        k_max,
        first_one_site,
        second_one_site,
        second_two_site,
        residual_second,
        theorem_coeff: Q::from_integer(BigInt::from(residual_second)) / qi(2),
    }
}

fn factorial(n: u64) -> BigInt {
    (1..=n).fold(BigInt::one(), |acc, k| acc * BigInt::from(k))
}

fn binom(n: u64, k: u64) -> BigInt {
    factorial(n) / (factorial(k) * factorial(n - k))
}

/// Lemma 5.4: `||rho_S^(j)||_1 <= (2g)^j k(k+1)...(k+j-1)` (coefficient of `g^j`).
pub fn lemma54_site_coeff(k: u64, j: u64) -> BigInt {
    (0..j).fold(BigInt::one(), |acc, r| acc * BigInt::from(2 * (k + r)))
}

/// Lemma 5.4: two-site bound plus the Leibniz sum for `rho_a (x) rho_b`.
pub fn lemma54_residual_coeff(j: u64) -> BigInt {
    let product: BigInt = (0..=j)
        .map(|m| binom(j, m) * lemma54_site_coeff(1, m) * lemma54_site_coeff(1, j - m))
        .sum();
    lemma54_site_coeff(2, j) + product
}

/// Theorem 5.5: `R_J(t) = c_J g^{J+1} t^{J+1}`, `c_J = ||F^(J+1)|| / (J+1)!`.
pub fn theorem55_remainder_coeff(big_j: u64) -> Q {
    Q::new(lemma54_residual_coeff(big_j + 1), factorial(big_j + 1))
}

// ---------------------------------------------------------------------------
// Instances.
// ---------------------------------------------------------------------------

/// A local operator `op` on the sorted site list `support`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Local {
    pub support: Vec<usize>,
    pub op: Mat,
}

/// A Lindblad jump operator with a nonnegative rate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Jump {
    pub local: Local,
    pub rate: Q,
}

/// A declared qubit instance: one- and two-site Hermitian terms, optional
/// one- or two-site jumps, and one 2x2 density matrix per site.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Instance {
    pub name: &'static str,
    pub sites: usize,
    pub terms: Vec<Local>,
    pub jumps: Vec<Jump>,
    pub states: Vec<Mat>,
}

fn eps() -> Q {
    two_pow_neg(48)
}

fn valid_support(s: &[usize], n: usize) -> bool {
    !s.is_empty() && s.len() <= 2 && s.windows(2).all(|w| w[0] < w[1]) && s.iter().all(|&x| x < n)
}

fn valid_qubit_state(r: &Mat) -> bool {
    // 2x2 Hermitian, trace one, nonnegative diagonal and determinant.
    if r.dim() != 2 || !r.is_hermitian() {
        return false;
    }
    let (a, d, b) = (&r.get(0, 0).re, &r.get(1, 1).re, r.get(0, 1));
    let det = a * d - (&b.re * &b.re + &b.im * &b.im);
    a + d == Q::one() && *a >= Q::zero() && *d >= Q::zero() && det >= Q::zero()
}

/// Exact precomputation for one instance: merged terms `h_X` (one per
/// support), their full-space embeddings, the jumps and `rho(0)`.
#[derive(Debug, Clone)]
pub struct Prepared {
    pub inst: Instance,
    /// `(X, h_X)`, all terms with the same support summed.
    pub merged: Vec<Local>,
    h_full: Vec<Mat>,
    jumps_full: Vec<(Mat, Mat, Mat, Q)>,
    pub rho0: Mat,
}

impl Prepared {
    pub fn new(inst: Instance) -> Result<Self, ExactError> {
        let n = inst.sites;
        if n == 0 || n > 6 || inst.states.len() != n || !inst.states.iter().all(valid_qubit_state) {
            return Err(ExactError::InvalidInstance("states"));
        }
        let mut merged: Vec<Local> = Vec::new();
        for t in &inst.terms {
            if !valid_support(&t.support, n) || t.op.dim() != 1 << t.support.len() || !t.op.is_hermitian() {
                return Err(ExactError::InvalidInstance("term"));
            }
            match merged.iter_mut().find(|m| m.support == t.support) {
                Some(m) => m.op = m.op.add(&t.op),
                None => merged.push(t.clone()),
            }
        }
        let h_full = merged.iter().map(|m| embed(&m.op, &m.support, n)).collect::<Result<Vec<_>, _>>()?;
        let mut jumps_full = Vec::new();
        for j in &inst.jumps {
            let s = &j.local.support;
            if !valid_support(s, n) || j.local.op.dim() != 1 << s.len() || j.rate < Q::zero() {
                return Err(ExactError::InvalidInstance("jump"));
            }
            let l = embed(&j.local.op, s, n)?;
            let ld = l.dagger();
            let ldl = ld.mul(&l);
            jumps_full.push((l, ld, ldl, j.rate.clone()));
        }
        let rho0 = inst.states.iter().skip(1).fold(inst.states[0].clone(), |acc, r| acc.kron(r));
        Ok(Self { inst, merged, h_full, jumps_full, rho0 })
    }

    fn hamiltonian_part(&self, rho: &Mat, which: Option<usize>) -> Mat {
        let mut out = Mat::zeros(rho.dim());
        for (k, h) in self.h_full.iter().enumerate() {
            if which.map_or(true, |w| w == k) {
                out = out.add(&h.comm(rho).mul_neg_i());
            }
        }
        out
    }

    fn dissipator_part(&self, rho: &Mat, which: Option<usize>) -> Mat {
        let mut out = Mat::zeros(rho.dim());
        for (k, (l, ld, ldl, g)) in self.jumps_full.iter().enumerate() {
            if which.map_or(true, |w| w == k) {
                let d = l.mul(rho).mul(ld).sub(&ldl.anti(rho).scale(&qr(1, 2)));
                out = out.add(&d.scale(g));
            }
        }
        out
    }

    /// The generator `L(rho) = -i[H, rho] + sum_a gamma_a D_{L_a}(rho)`.
    pub fn generator(&self, rho: &Mat) -> Mat {
        self.hamiltonian_part(rho, None).add(&self.dissipator_part(rho, None))
    }

    /// Exact Taylor jets `rho^(k)(0) = L^k(rho(0))`, `k = 0..=order`.
    pub fn jets(&self, order: usize) -> Vec<Mat> {
        let mut out = vec![self.rho0.clone()];
        for _ in 0..order {
            let next = self.generator(&out[out.len() - 1]);
            out.push(next);
        }
        out
    }

    /// Exact operator norms `||h_X||` (merged), as enclosures.
    pub fn term_norms(&self) -> Result<Vec<Iv>, ExactError> {
        self.merged.iter().map(|m| op_norm(&m.op, &eps())).collect()
    }

    /// `g = max_v sum_{X ni v} ||h_X||` (§5.1), optionally dropping one-local
    /// fields (the deliberately wrong "missing incident term" variant).
    pub fn incident_norm(&self, include_fields: bool) -> Result<Iv, ExactError> {
        let norms = self.term_norms()?;
        let mut g = Iv::zero();
        for v in 0..self.inst.sites {
            let mut sum = Iv::zero();
            for (m, nx) in self.merged.iter().zip(norms.iter()) {
                if m.support.contains(&v) && (include_fields || m.support.len() == 2) {
                    sum = sum.add(nx);
                }
            }
            g = g.max(&sum);
        }
        Ok(g)
    }

    /// Local strengths `s_X`: `2||h_X||` plus, for §5.4.1,
    /// `2 sum_{supp L_a = X} gamma_a ||L_a||^2`. Without jumps, `s_X = 2||h_X||`.
    pub fn strengths(&self) -> Result<Vec<(Vec<usize>, Iv)>, ExactError> {
        let norms = self.term_norms()?;
        let mut out: Vec<(Vec<usize>, Iv)> =
            self.merged.iter().zip(norms).map(|(m, n)| (m.support.clone(), n.scale_nonneg(&qi(2)))).collect();
        for j in &self.inst.jumps {
            let l = &j.local.op;
            let lsq = op_norm(&l.dagger().mul(l), &eps())?;
            let add = lsq.scale_nonneg(&(&j.rate * qi(2)));
            match out.iter_mut().find(|(s, _)| *s == j.local.support) {
                Some((_, iv)) => *iv = iv.add(&add),
                None => out.push((j.local.support.clone(), add)),
            }
        }
        Ok(out)
    }

    /// `max_v sum_{X ni v} s_X` (= `2g` without jumps, `Lambda_*` with jumps).
    pub fn incident_strength(&self) -> Result<Iv, ExactError> {
        let st = self.strengths()?;
        Ok((0..self.inst.sites).fold(Iv::zero(), |g, v| {
            g.max(&st.iter().filter(|(s, _)| s.contains(&v)).fold(Iv::zero(), |a, (_, x)| a.add(x)))
        }))
    }

    /// Instance branch count `c1(S) = sum_{X cap S != 0} s_X >= ||L^dag(A_S)||`.
    pub fn branch_first(&self, s: &[usize]) -> Result<Iv, ExactError> {
        let st = self.strengths()?;
        Ok(st.iter().filter(|(x, _)| x.iter().any(|v| s.contains(v))).fold(Iv::zero(), |a, (_, n)| a.add(n)))
    }

    /// Instance branch count `c2(S) = sum_{X cap S != 0} s_X c1(S cup X)`.
    pub fn branch_second(&self, s: &[usize]) -> Result<Iv, ExactError> {
        let mut total = Iv::zero();
        for (x, n) in self.strengths()?.iter().filter(|(x, _)| x.iter().any(|v| s.contains(v))) {
            let mut union: Vec<usize> = s.to_vec();
            union.extend(x.iter().filter(|v| !s.contains(v)));
            total = total.add(&n.mul_nonneg(&self.branch_first(&union)?));
        }
        Ok(total)
    }

    /// Instance constant `K_e = c2(ab) + c2(a) + c2(b) + 2 c1(a) c1(b)`, an
    /// upper bound for `sup_s ||F_e''(s)||_1` on this instance.
    pub fn residual_branch_bound(&self, (a, b): (usize, usize)) -> Result<Iv, ExactError> {
        let ca = self.branch_first(&[a])?;
        let cb = self.branch_first(&[b])?;
        Ok(self
            .branch_second(&[a, b])?
            .add(&self.branch_second(&[a])?)
            .add(&self.branch_second(&[b])?)
            .add(&ca.mul_nonneg(&cb).scale_nonneg(&qi(2))))
    }

    /// Exact `ad_H^2(A_S) = [H, [H, A_S]]` on the full space.
    pub fn double_commutator(&self, a_local: &Local) -> Result<Mat, ExactError> {
        let a = embed(&a_local.op, &a_local.support, self.inst.sites)?;
        let h = self.h_full.iter().fold(Mat::zeros(a.dim()), |acc, x| acc.add(x));
        Ok(h.comm(&h.comm(&a)))
    }

    /// Upper bound `w >= ||L||_{1 -> 1}`: `sum_X 2||h_X|| + sum_a 2 gamma_a ||L_a||^2`.
    pub fn generator_bound(&self) -> Result<Q, ExactError> {
        Ok(self.strengths()?.iter().fold(Q::zero(), |a, (_, x)| a + &x.hi))
    }
}

// ---------------------------------------------------------------------------
// Edge data: reduced jets, P_e / Q_e, n_e, nu_e, F_e^(j)(0).
// ---------------------------------------------------------------------------

/// Reduce a full-space operator to the edge `(a, b)` and its two sites.
pub fn reduce(m: &Mat, (a, b): (usize, usize), n: usize) -> Result<(Mat, Mat, Mat), ExactError> {
    let e = ptrace(m, &[a, b], n)?;
    let ra = ptrace(&e, &[0], 2)?;
    let rb = ptrace(&e, &[1], 2)?;
    Ok((e, ra, rb))
}

/// Tangent projection `P_e Z = Tr_b(Z) (x) rho_b + rho_a (x) Tr_a(Z)` (§5.1).
pub fn tangent(z: &Mat, ra: &Mat, rb: &Mat) -> Result<Mat, ExactError> {
    Ok(ptrace(z, &[0], 2)?.kron(rb).add(&ra.kron(&ptrace(z, &[1], 2)?)))
}

/// Exact first-order data of one edge.
#[derive(Debug, Clone)]
pub struct EdgeRate {
    pub rho_e: Mat,
    pub l_e: Mat,
    pub p_l: Mat,
    pub n_e: Mat,
    pub nu: Iv,
    /// `||L_e||_1`: the raw, un-projected rate (a deliberately wrong variant).
    pub raw: Iv,
}

pub fn edge_rate(p: &Prepared, e: (usize, usize)) -> Result<EdgeRate, ExactError> {
    let n = p.inst.sites;
    let (rho_e, ra, rb) = reduce(&p.rho0, e, n)?;
    let (l_e, _, _) = reduce(&p.generator(&p.rho0), e, n)?;
    let p_l = tangent(&l_e, &ra, &rb)?;
    let n_e = l_e.sub(&p_l);
    let nu = trace_norm(&n_e, &eps())?;
    let raw = trace_norm(&l_e, &eps())?;
    Ok(EdgeRate { rho_e, l_e, p_l, n_e, nu, raw })
}

/// `F_e^(j)(0) = rho_e^(j) - sum_m C(j,m) rho_a^(m) (x) rho_b^(j-m)`.
pub fn residual_jets(jets: &[Mat], e: (usize, usize), n: usize) -> Result<Vec<Mat>, ExactError> {
    let red = jets.iter().map(|m| reduce(m, e, n)).collect::<Result<Vec<_>, _>>()?;
    let mut out = Vec::new();
    for j in 0..red.len() {
        let mut f = red[j].0.clone();
        for m in 0..=j {
            let c = Q::from_integer(binom(j as u64, m as u64));
            f = f.sub(&red[m].1.kron(&red[j - m].2).scale(&c));
        }
        out.push(f);
    }
    Ok(out)
}

/// Lemma 5.3 data: for each merged term and each jump, whether its
/// first-order edge contribution is purely tangent (`Q_e L_e^X = 0`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TermNormal {
    pub support: Vec<usize>,
    pub is_jump: bool,
    pub normal_is_zero: bool,
}

pub fn per_term_normal(p: &Prepared, e: (usize, usize)) -> Result<Vec<TermNormal>, ExactError> {
    let n = p.inst.sites;
    let (_, ra, rb) = reduce(&p.rho0, e, n)?;
    let mut out = Vec::new();
    let pieces = p
        .merged
        .iter()
        .enumerate()
        .map(|(k, m)| (m.support.clone(), false, p.hamiltonian_part(&p.rho0, Some(k))))
        .chain(p.inst.jumps.iter().enumerate().map(|(k, j)| {
            (j.local.support.clone(), true, p.dissipator_part(&p.rho0, Some(k)))
        }));
    for (support, is_jump, full) in pieces {
        let (l, _, _) = reduce(&full, e, n)?;
        let normal = l.sub(&tangent(&l, &ra, &rb)?);
        out.push(TermNormal { support, is_jump, normal_is_zero: normal.is_zero() });
    }
    Ok(out)
}

// ---------------------------------------------------------------------------
// D_e(t) at rational t: exact truncated series plus rigorous tail.
// ---------------------------------------------------------------------------

/// Smallest `K` with `x^{K+1}/(K+1)! / (1 - x/(K+2)) <= tol`, and that tail.
pub fn series_order(x: &Q, tol: &Q) -> Result<(usize, Q), ExactError> {
    let mut term = x.clone(); // x^{K+1}/(K+1)! for K = 0
    for k in 0..200usize {
        let ratio = x / qi(k as i64 + 2);
        if ratio < Q::one() {
            let tail = &term / (Q::one() - ratio);
            if tail <= *tol {
                return Ok((k, tail));
            }
        }
        term = term * x / qi(k as i64 + 2);
    }
    Err(ExactError::SeriesOrder)
}

/// Enclosure of `D_e(t)`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DefectEnclosure {
    pub t: Q,
    pub order: usize,
    /// `delta >= ||rho(t) - sum_{k<=K} t^k rho^(k)(0)/k!||_1`.
    pub delta: Q,
    pub d: Iv,
}

pub fn defect_at(p: &Prepared, jets: &[Mat], e: (usize, usize), t: &Q) -> Result<DefectEnclosure, ExactError> {
    let x = p.generator_bound()? * t;
    let (order, delta) = series_order(&x, &qr(1, 1_000_000_000_000))?;
    if order >= jets.len() {
        return Err(ExactError::SeriesOrder);
    }
    let mut sigma = Mat::zeros(p.rho0.dim());
    let mut coef = Q::one();
    for (k, jet) in jets.iter().enumerate().take(order + 1) {
        if k > 0 {
            coef = coef * t / qi(k as i64);
        }
        sigma = sigma.add(&jet.scale(&coef));
    }
    let (se, sa, sb) = reduce(&sigma, e, p.inst.sites)?;
    let fk = trace_norm(&se.sub(&sa.kron(&sb)), &eps())?;
    // ||F - F_K|| <= delta + delta + delta (1 + delta) = delta (3 + delta).
    let err = &delta * (qi(3) + &delta);
    let lo = &fk.lo - &err;
    let lo = if lo < Q::zero() { Q::zero() } else { lo };
    Ok(DefectEnclosure { t: t.clone(), order, delta, d: Iv::new(lo, &fk.hi + &err) })
}

/// Rigorous check of `D >= rate t - c G^2 t^2` and the two-sided
/// `|D - rate t| <= c G^2 t^2`, using worst-case interval endpoints.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundCheck {
    pub lower_holds: bool,
    pub two_sided_holds: bool,
    /// Certified violation of the lower bound: `D_hi < rate_lo t - c G_hi^2 t^2`.
    pub lower_violated: bool,
}

pub fn check_bound(d: &Iv, rate: &Iv, coeff: &Q, g: &Iv, t: &Q) -> BoundCheck {
    let t2 = t * t;
    let rem_lo = coeff * &g.lo * &g.lo * &t2;
    let rem_hi = coeff * &g.hi * &g.hi * &t2;
    let lower_holds = d.lo >= &rate.hi * t - &rem_lo;
    let two_sided_holds = &d.hi - &rate.lo * t <= rem_lo && &rate.hi * t - &d.lo <= rem_lo;
    let lower_violated = d.hi < &rate.lo * t - rem_hi;
    BoundCheck { lower_holds, two_sided_holds, lower_violated }
}

/// Upper enclosure of the constant an instance actually needs at time `t`:
/// `|D - nu t| / (g^2 t^2)` (sharpness probe; never used as proof).
pub fn needed_coeff_hi(d: &Iv, nu: &Iv, g: &Iv, t: &Q) -> Q {
    let a = &d.hi - &nu.lo * t;
    let b = &nu.hi * t - &d.lo;
    let m = if a > b { a } else { b };
    let m = if m < Q::zero() { Q::zero() } else { m };
    m / (&g.lo * &g.lo * t * t)
}

// ---------------------------------------------------------------------------
// Declared instances (fixtures).
// ---------------------------------------------------------------------------

pub fn pauli(c: char) -> Mat {
    let (o, z) = (Cx::one(), Cx::zero());
    let e = match c {
        'X' => vec![z.clone(), o.clone(), o, z],
        'Y' => vec![z.clone(), Cx::i().scale(&qi(-1)), Cx::i(), z],
        'Z' => vec![o, z.clone(), z, Cx::real(qi(-1))],
        _ => vec![o.clone(), z.clone(), z, o],
    };
    Mat::from_fn(2, |i, j| e[2 * i + j].clone())
}

fn pp(a: char, b: char) -> Mat {
    pauli(a).kron(&pauli(b))
}

fn term(support: &[usize], op: Mat, c: Q) -> Local {
    Local { support: support.to_vec(), op: op.scale(&c) }
}

fn state(a: Q, b_re: Q, b_im: Q) -> Mat {
    let d = Q::one() - &a;
    Mat::from_fn(2, |i, j| match (i, j) {
        (0, 0) => Cx::real(a.clone()),
        (1, 1) => Cx::real(d.clone()),
        (0, 1) => Cx::new(b_re.clone(), b_im.clone()),
        _ => Cx::new(b_re.clone(), -b_im.clone()),
    })
}

fn ket0() -> Mat {
    state(qi(1), Q::zero(), Q::zero())
}

fn plus() -> Mat {
    state(qr(1, 2), qr(1, 2), Q::zero())
}

fn instance(name: &'static str, sites: usize, terms: Vec<Local>, jumps: Vec<Jump>, states: Vec<Mat>) -> Instance {
    Instance { name, sites, terms, jumps, states }
}

/// §6.1: `H = X (x) X`, `|00>`. Paper: `nu = 2|J|`.
pub fn xx_pair() -> Instance {
    instance("xx_pair", 2, vec![term(&[0, 1], pp('X', 'X'), qi(1))], vec![], vec![ket0(), ket0()])
}

/// §6.2: TFIM `H = -sum Z Z - (1/2) sum X` on a 4-site chain, `|+>^4`.
pub fn tfim_chain4() -> Instance {
    let mut terms: Vec<Local> = (0..3).map(|i| term(&[i, i + 1], pp('Z', 'Z'), qi(-1))).collect();
    terms.extend((0..4).map(|i| term(&[i], pauli('X'), qr(-1, 2))));
    instance("tfim_chain4", 4, terms, vec![], vec![plus(); 4])
}

/// 3-site chain: Heisenberg bond, XX+ZZ bond, tilted and Y fields; mixed
/// Gaussian-rational product state.
pub fn mixed_chain3() -> Instance {
    let heis = pp('X', 'X').add(&pp('Y', 'Y')).add(&pp('Z', 'Z'));
    let xz = pp('X', 'X').add(&pp('Z', 'Z'));
    let tilted = pauli('X').scale(&qr(3, 5)).add(&pauli('Z').scale(&qr(4, 5)));
    let terms = vec![
        term(&[0, 1], heis, qr(1, 2)),
        term(&[1, 2], xz, qr(1, 3)),
        term(&[0], tilted, qi(1)),
        term(&[2], pauli('Y'), qr(1, 2)),
    ];
    let states = vec![
        state(qr(2, 3), qr(1, 6), qr(1, 6)),
        state(qr(3, 4), Q::zero(), qr(-1, 4)),
        state(qr(1, 2), qr(1, 4), Q::zero()),
    ];
    instance("mixed_chain3", 3, terms, vec![], states)
}

/// §5.7(1) tangent direction: `H = Z (x) Z + X (x) I`, `|0> (x) |+>`, `nu = 0`.
pub fn tangent_pair() -> Instance {
    let terms = vec![term(&[0, 1], pp('Z', 'Z'), qi(1)), term(&[0], pauli('X'), qi(1))];
    instance("tangent_pair", 2, terms, vec![], vec![ket0(), plus()])
}

/// `H = Z (x) Z`, `|0> (x) |+>`: the state stays a product, `D = 0`, while the
/// raw commutator rate `||L_e||_1 = 2`.
pub fn zz_product_pair() -> Instance {
    instance("zz_product_pair", 2, vec![term(&[0, 1], pp('Z', 'Z'), qi(1))], vec![], vec![ket0(), plus()])
}

/// Weak bond, strong fields: `H = (1/40) X X + Z I + I Z`, `|00>`.
pub fn strong_field_pair() -> Instance {
    let terms = vec![
        term(&[0, 1], pp('X', 'X'), qr(1, 40)),
        term(&[0], pauli('Z'), qi(1)),
        term(&[1], pauli('Z'), qi(1)),
    ];
    instance("strong_field_pair", 2, terms, vec![], vec![ket0(), ket0()])
}

/// §5.4.1: `H = (1/2) X X`, amplitude damping on site 0 (rate 1/4) and
/// dephasing on site 1 (rate 1/5); mixed product state. (`|+>` on site 0
/// would give `nu = 0`: it is an `X` eigenstate, so the centered bond vanishes.)
pub fn damped_pair() -> Instance {
    let lower = Mat::from_fn(2, |i, j| if i == 0 && j == 1 { Cx::one() } else { Cx::zero() });
    let jumps = vec![
        Jump { local: Local { support: vec![0], op: lower }, rate: qr(1, 4) },
        Jump { local: Local { support: vec![1], op: pauli('Z') }, rate: qr(1, 5) },
    ];
    let terms = vec![term(&[0, 1], pp('X', 'X'), qr(1, 2))];
    instance("damped_pair", 2, terms, jumps, vec![state(qr(3, 4), qr(1, 4), Q::zero()), state(qr(2, 3), qr(1, 6), qr(1, 6))])
}

pub fn edges(inst: &Instance) -> Vec<(usize, usize)> {
    let mut out: Vec<(usize, usize)> = Vec::new();
    for t in &inst.terms {
        if let [a, b] = t.support[..] {
            if !out.contains(&(a, b)) {
                out.push((a, b));
            }
        }
    }
    out
}

// ---------------------------------------------------------------------------
// Tests.
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    type R = Result<(), String>;

    fn show(e: ExactError) -> String {
        format!("{e:?}")
    }

    fn need(cond: bool, msg: &str) -> R {
        if cond {
            Ok(())
        } else {
            Err(msg.to_string())
        }
    }

    fn hamiltonian_instances() -> Vec<Instance> {
        vec![xx_pair(), tfim_chain4(), mixed_chain3(), tangent_pair(), strong_field_pair()]
    }

    // ----- Lemma 5.2 / Appendix B / Lemma 5.4 constants -----

    #[test]
    fn unit_lemma52_counting_yields_2_8_24_48_24() -> R {
        let c = counting_constants(2, 2);
        need(c.first_one_site == 2, "first one-site constant")?;
        need(c.second_one_site == 8, "second one-site constant")?;
        need(c.second_two_site == 24, "second two-site constant")?;
        need(c.residual_second == 48, "F'' constant 24+8+8+8")?;
        need(c.theorem_coeff == qi(24), "Theorem 5.1 coefficient 48/2")?;
        need(c.theorem_coeff != qi(23), "a 23 g^2 coefficient is not what the counting gives")
    }

    #[test]
    fn unit_lemma54_route_also_gives_24() -> R {
        for j in 0..9u64 {
            let expected = BigInt::from(2u64.pow(j as u32 + 1)) * factorial(j + 1);
            need(lemma54_residual_coeff(j) == expected, "||F^(j)|| <= 2^{j+1}(j+1)! g^j")?;
        }
        for big_j in 1..7u64 {
            let expected = qi(2i64.pow(big_j as u32 + 2) * (big_j as i64 + 2));
            need(theorem55_remainder_coeff(big_j) == expected, "R_J = 2^{J+2}(J+2)")?;
        }
        need(lemma54_residual_coeff(2) == BigInt::from(48), "j = 2 route gives 48")?;
        need(theorem55_remainder_coeff(1) == counting_constants(2, 2).theorem_coeff, "both routes give 24")
    }

    #[test]
    fn unit_lindblad_counting_yields_12_and_6() -> R {
        let c = counting_constants(1, 2);
        need((c.first_one_site, c.second_one_site, c.second_two_site) == (1, 2, 6), "Lambda constants 1,2,6")?;
        need(c.residual_second == 12, "F'' <= (6+2+2+2) Lambda^2")?;
        need(c.theorem_coeff == qi(6), "D >= nu t - 6 Lambda^2 t^2")?;
        // With no jumps Lambda = 2g, so 6 Lambda^2 = 24 g^2.
        need(c.theorem_coeff * qi(4) == counting_constants(2, 2).theorem_coeff, "6 (2g)^2 = 24 g^2")
    }

    // ----- Instance data: rho_e(0), L_e, P_e/Q_e, nu_e, g -----

    #[test]
    fn integration_paper_examples_nu_and_g_exact() -> R {
        let p = Prepared::new(xx_pair()).map_err(show)?;
        let r = edge_rate(&p, (0, 1)).map_err(show)?;
        need(r.nu == Iv::point(qi(2)), "§6.1 nu = 2|J| exactly")?;
        need(p.incident_norm(true).map_err(show)? == Iv::point(qi(1)), "§6.1 g = 1")?;
        let p = Prepared::new(tfim_chain4()).map_err(show)?;
        need(p.incident_norm(true).map_err(show)? == Iv::point(qr(5, 2)), "§6.2 g = 2|J| + |h|")?;
        for e in edges(&p.inst) {
            let r = edge_rate(&p, e).map_err(show)?;
            need(r.nu == Iv::point(qi(2)), "§6.2 nu_e = 2|J| on every bond")?;
            need(r.p_l.is_zero(), "§6.2 P_e annihilates L_e")?;
        }
        let p = Prepared::new(mixed_chain3()).map_err(show)?;
        let norms = p.term_norms().map_err(show)?;
        need(norms == vec![Iv::point(qr(3, 2)), Iv::point(qr(2, 3)), Iv::point(qi(1)), Iv::point(qr(1, 2))], "exact term norms")?;
        need(p.incident_norm(true).map_err(show)? == Iv::point(qr(5, 2)), "mixed chain g = 5/2")
    }

    #[test]
    fn integration_tangent_split_is_exact_projection() -> R {
        for inst in hamiltonian_instances().into_iter().chain([damped_pair()]) {
            let p = Prepared::new(inst).map_err(show)?;
            let n = p.inst.sites;
            for e in edges(&p.inst) {
                let r = edge_rate(&p, e).map_err(show)?;
                let (_, ra, rb) = reduce(&p.rho0, e, n).map_err(show)?;
                need(r.rho_e == ra.kron(&rb), "rho_e(0) is the product of marginals")?;
                need(r.l_e.trace().is_zero(), "Tr L_e = 0")?;
                need(tangent(&r.p_l, &ra, &rb).map_err(show)? == r.p_l, "P_e is idempotent on L_e")?;
                need(ptrace(&r.n_e, &[0], 2).map_err(show)?.is_zero(), "Tr_b n_e = 0")?;
                need(ptrace(&r.n_e, &[1], 2).map_err(show)?.is_zero(), "Tr_a n_e = 0")?;
                let f = residual_jets(&p.jets(1), e, n).map_err(show)?;
                need(f[0].is_zero(), "F_e(0) = 0")?;
                need(f[1] == r.n_e, "F_e'(0) = Q_e L_e = n_e exactly")?;
            }
        }
        Ok(())
    }

    // ----- Lemma 5.3 -----

    #[test]
    fn integration_lemma53_only_edge_support_reaches_normal() -> R {
        for inst in hamiltonian_instances().into_iter().chain([damped_pair()]) {
            let p = Prepared::new(inst).map_err(show)?;
            for e in edges(&p.inst) {
                let rows = per_term_normal(&p, e).map_err(show)?;
                for row in &rows {
                    if row.support != vec![e.0, e.1] {
                        need(row.normal_is_zero, "term not supported on {a,b} is tangent")?;
                    }
                }
                // The normal rate equals the edge term's own normal part.
                let r = edge_rate(&p, e).map_err(show)?;
                let only_edge = Instance {
                    terms: p.inst.terms.iter().filter(|t| t.support == vec![e.0, e.1]).cloned().collect(),
                    jumps: vec![],
                    ..p.inst.clone()
                };
                let q = Prepared::new(only_edge).map_err(show)?;
                need(edge_rate(&q, e).map_err(show)?.n_e == r.n_e, "n_e unchanged after deleting non-edge terms")?;
            }
        }
        Ok(())
    }

    // ----- Lemma 5.2 on instances -----

    #[test]
    fn integration_lemma52_branch_counts_on_instances() -> R {
        for inst in hamiltonian_instances() {
            let p = Prepared::new(inst).map_err(show)?;
            let g = p.incident_norm(true).map_err(show)?;
            let g2 = &g.lo * &g.lo;
            for v in 0..p.inst.sites {
                need(p.branch_first(&[v]).map_err(show)?.hi <= qi(2) * &g.lo, "c1(v) <= 2g")?;
                need(p.branch_second(&[v]).map_err(show)?.hi <= qi(8) * &g2, "c2(v) <= 8g^2")?;
            }
            let jets = p.jets(2);
            for e in edges(&p.inst) {
                need(p.branch_second(&[e.0, e.1]).map_err(show)?.hi <= qi(24) * &g2, "c2(e) <= 24g^2")?;
                let k_e = p.residual_branch_bound(e).map_err(show)?;
                need(k_e.hi <= qi(48) * &g2, "K_e <= 48 g^2")?;
                let (d2e, d2a, _) = reduce(&jets[2], e, p.inst.sites).map_err(show)?;
                let (_, d1a, _) = reduce(&jets[1], e, p.inst.sites).map_err(show)?;
                need(trace_norm(&d2e, &eps()).map_err(show)?.hi <= qi(24) * &g2, "||rho_e''(0)|| <= 24g^2")?;
                need(trace_norm(&d2a, &eps()).map_err(show)?.hi <= qi(8) * &g2, "||rho_a''(0)|| <= 8g^2")?;
                need(trace_norm(&d1a, &eps()).map_err(show)?.hi <= qi(2) * &g.lo, "||rho_a'(0)|| <= 2g")?;
                let f2 = &residual_jets(&jets, e, p.inst.sites).map_err(show)?[2];
                need(trace_norm(f2, &eps()).map_err(show)?.hi <= k_e.lo, "||F_e''(0)|| <= K_e")?;
            }
        }
        Ok(())
    }

    #[test]
    fn integration_lemma52_exact_double_commutators_on_mixed_chain() -> R {
        let p = Prepared::new(mixed_chain3()).map_err(show)?;
        let g = p.incident_norm(true).map_err(show)?;
        for (support, op) in [
            (vec![0], pauli('X')),
            (vec![1], pauli('Z')),
            (vec![2], pauli('Y')),
            (vec![0, 1], pp('X', 'Y')),
            (vec![1, 2], pp('Z', 'Z')),
            (vec![0, 1], pp('Y', 'Z')),
        ] {
            let a = Local { support: support.clone(), op };
            let norm = op_norm(&p.double_commutator(&a).map_err(show)?, &eps()).map_err(show)?;
            let c2 = p.branch_second(&support).map_err(show)?;
            let lemma = if support.len() == 1 { qi(8) } else { qi(24) };
            need(norm.hi <= c2.lo, "||ad_H^2 A_S|| <= instance c2(S)")?;
            need(c2.hi <= lemma * &g.lo * &g.lo, "c2(S) <= Lemma 5.2 constant")?;
        }
        Ok(())
    }

    // ----- Theorem 5.1 and Theorem 5.5 (J = 1) -----

    fn times() -> Vec<Q> {
        vec![qr(1, 100), qr(1, 30), qr(1, 10), qr(1, 4)]
    }

    #[test]
    fn e2e_theorem51_and_two_sided_on_instances() -> R {
        let coeff = counting_constants(2, 2).theorem_coeff;
        for inst in hamiltonian_instances() {
            let p = Prepared::new(inst).map_err(show)?;
            let g = p.incident_norm(true).map_err(show)?;
            let w = p.generator_bound().map_err(show)?;
            let t_max = times().into_iter().fold(Q::zero(), |m, t| if t > m { t } else { m });
            let (order, _) = series_order(&(w * t_max), &qr(1, 1_000_000_000_000)).map_err(show)?;
            let jets = p.jets(order);
            for e in edges(&p.inst) {
                let r = edge_rate(&p, e).map_err(show)?;
                for t in times() {
                    let d = defect_at(&p, &jets, e, &t).map_err(show)?;
                    let c = check_bound(&d.d, &r.nu, &coeff, &g, &t);
                    need(c.lower_holds, "Theorem 5.1 lower bound on instance")?;
                    need(c.two_sided_holds, "Theorem 5.5 (J=1) two-sided bound on instance")?;
                }
            }
        }
        Ok(())
    }

    #[test]
    fn e2e_half_slope_window_on_tfim() -> R {
        // t = nu_min / (48 g^2) = 2 / (48 * 25/4) = 1/150, D >= nu t / 2.
        let p = Prepared::new(tfim_chain4()).map_err(show)?;
        let g = p.incident_norm(true).map_err(show)?;
        let jets = p.jets(12);
        for e in edges(&p.inst) {
            let r = edge_rate(&p, e).map_err(show)?;
            let t = &r.nu.lo / (qi(48) * &g.hi * &g.hi);
            need(t == qr(1, 150), "window endpoint 1/150")?;
            let d = defect_at(&p, &jets, e, &t).map_err(show)?;
            need(d.d.lo >= &r.nu.hi * &t / qi(2), "D >= nu t / 2 inside the window")?;
        }
        Ok(())
    }

    #[test]
    fn e2e_tangent_direction_nu_zero_and_quadratic_defect() -> R {
        let p = Prepared::new(tangent_pair()).map_err(show)?;
        let g = p.incident_norm(true).map_err(show)?;
        need(g == Iv::point(qi(2)), "g = 2")?;
        let r = edge_rate(&p, (0, 1)).map_err(show)?;
        need(r.n_e.is_zero() && r.nu == Iv::zero(), "nu_e = 0 exactly")?;
        need(!r.l_e.is_zero(), "but L_e != 0 (tangent motion only)")?;
        let jets = p.jets(30);
        let f2 = trace_norm(&residual_jets(&jets, (0, 1), 2).map_err(show)?[2], &eps()).map_err(show)?;
        need(f2.lo > Q::zero(), "F_e''(0) != 0: quadratic onset")?;
        for t in times() {
            let d = defect_at(&p, &jets, (0, 1), &t).map_err(show)?;
            need(d.d.hi <= qi(24) * &g.lo * &g.lo * &t * &t, "nu = 0 implies D <= 24 g^2 t^2")?;
        }
        let d = defect_at(&p, &jets, (0, 1), &qr(1, 4)).map_err(show)?;
        need(d.d.lo > Q::zero(), "defect is strictly positive at t = 1/4")
    }

    // ----- Wrong variants are caught -----

    #[test]
    fn negative_missing_field_in_g_is_a_certified_counterexample() -> R {
        let p = Prepared::new(strong_field_pair()).map_err(show)?;
        let g_full = p.incident_norm(true).map_err(show)?;
        let g_bond = p.incident_norm(false).map_err(show)?;
        need(g_full == Iv::point(qr(41, 40)) && g_bond == Iv::point(qr(1, 40)), "g with and without fields")?;
        let r = edge_rate(&p, (0, 1)).map_err(show)?;
        need(r.nu == Iv::point(qr(1, 20)), "nu = 2 J = 1/20")?;
        let t = qr(4, 5);
        let x = p.generator_bound().map_err(show)? * &t;
        let (order, _) = series_order(&x, &qr(1, 1_000_000_000_000)).map_err(show)?;
        let jets = p.jets(order);
        let d = defect_at(&p, &jets, (0, 1), &t).map_err(show)?;
        let coeff = qi(24);
        let wrong = check_bound(&d.d, &r.nu, &coeff, &g_bond, &t);
        need(wrong.lower_violated, "dropping one-local fields from g breaks the bound")?;
        let right = check_bound(&d.d, &r.nu, &coeff, &g_full, &t);
        need(right.lower_holds && right.two_sided_holds, "the full incident norm restores it")
    }

    #[test]
    fn negative_raw_commutator_rate_is_a_certified_counterexample() -> R {
        let p = Prepared::new(zz_product_pair()).map_err(show)?;
        let g = p.incident_norm(true).map_err(show)?;
        let r = edge_rate(&p, (0, 1)).map_err(show)?;
        need(r.raw == Iv::point(qi(2)) && r.nu == Iv::zero(), "raw rate 2, normal rate 0")?;
        let t = qr(1, 50);
        let jets = p.jets(30);
        let d = defect_at(&p, &jets, (0, 1), &t).map_err(show)?;
        let wrong = check_bound(&d.d, &r.raw, &qi(24), &g, &t);
        need(wrong.lower_violated, "using ||L_e|| instead of ||Q_e L_e|| breaks the bound")?;
        let right = check_bound(&d.d, &r.nu, &qi(24), &g, &t);
        need(right.lower_holds && right.two_sided_holds, "Q_e restores it")
    }

    #[test]
    fn negative_constant_23_is_not_caught_on_these_instances() -> R {
        // Honest sharpness probe: the constant each instance needs stays far
        // below 23, so a wrong 23 g^2 would pass here too. 24 is sufficient,
        // not shown sharp, by these instances.
        let mut worst = Q::zero();
        for inst in hamiltonian_instances() {
            let p = Prepared::new(inst).map_err(show)?;
            let g = p.incident_norm(true).map_err(show)?;
            let jets = p.jets(30);
            for e in edges(&p.inst) {
                let r = edge_rate(&p, e).map_err(show)?;
                for t in [qr(1, 100), qr(1, 10)] {
                    let d = defect_at(&p, &jets, e, &t).map_err(show)?;
                    let c = needed_coeff_hi(&d.d, &r.nu, &g, &t);
                    if c > worst {
                        worst = c;
                    }
                }
            }
        }
        let milli = (&worst * qi(1000)).ceil();
        eprintln!("po000_24g2 sharpness probe: needed constant <= {milli}/1000 (rational upper bound)");
        need(worst < qi(23), "needed constant < 23 on every tested instance")
    }

    // ----- §5.4.1 Lindblad -----

    #[test]
    fn e2e_lindblad_bound_6_lambda_squared_on_damped_pair() -> R {
        let p = Prepared::new(damped_pair()).map_err(show)?;
        let lam = p.incident_strength().map_err(show)?;
        need(lam == Iv::point(qr(3, 2)), "Lambda_* = 1 + 1/2")?;
        let e = (0, 1);
        let rows = per_term_normal(&p, e).map_err(show)?;
        need(rows.iter().filter(|r| r.is_jump).all(|r| r.normal_is_zero), "one-site jumps are tangent")?;
        let k_e = p.residual_branch_bound(e).map_err(show)?;
        need(k_e.hi <= qi(12) * &lam.lo * &lam.lo, "K_e <= 12 Lambda^2")?;
        let jets = p.jets(30);
        let f2 = trace_norm(&residual_jets(&jets, e, 2).map_err(show)?[2], &eps()).map_err(show)?;
        need(f2.hi <= k_e.lo, "||F''(0)|| <= K_e")?;
        let r = edge_rate(&p, e).map_err(show)?;
        need(r.nu.lo > Q::zero(), "active edge")?;
        let coeff = counting_constants(1, 2).theorem_coeff;
        for t in times() {
            let d = defect_at(&p, &jets, e, &t).map_err(show)?;
            let c = check_bound(&d.d, &r.nu, &coeff, &lam, &t);
            need(c.lower_holds && c.two_sided_holds, "D >= nu t - 6 Lambda^2 t^2 on instance")?;
        }
        // Without jumps the Lindblad strength is exactly 2g.
        let no_jumps = Prepared::new(Instance { jumps: vec![], ..damped_pair() }).map_err(show)?;
        let two_g = no_jumps.incident_norm(true).map_err(show)?.scale_nonneg(&qi(2));
        need(no_jumps.incident_strength().map_err(show)? == two_g, "Lambda = 2g without jumps")
    }

    #[test]
    fn negative_invalid_instances_are_refused() {
        let bad_state = Instance { states: vec![state(qi(2), Q::zero(), Q::zero()), ket0()], ..xx_pair() };
        assert!(Prepared::new(bad_state).is_err());
        let bad_support = Instance { terms: vec![term(&[1, 0], pp('X', 'X'), qi(1))], ..xx_pair() };
        assert!(Prepared::new(bad_support).is_err());
        let bad_rate = Instance { jumps: vec![Jump { local: Local { support: vec![0], op: pauli('Z') }, rate: qi(-1) }], ..xx_pair() };
        assert!(Prepared::new(bad_rate).is_err());
    }
}
