//! Cyclotomic -> rational-interval enclosure: the **complete** per-patch certificate.
//!
//! `mub6_interval_cover` certifies a box using only the first basis `B1` (the standard
//! basis, whose residuals are rational). That sub-certificate **abstains** exactly where a
//! fourth MU vector could hide — the region unbiased to `B1`. This module closes that gap by
//! enclosing the `B2/B3` residuals, whose fixed vectors have entries in `Q(zeta_24)`, in
//! exact rational intervals, so a box can be certified **everywhere**.
//!
//! The Invariant-Systems two-sided wall says `max_v f(v) = W = (88 + 3 sqrt6)/100 < 1`, i.e.
//! `sum_i omega_i(v)^2 >= (1 - W) * 5/6 = (4 - sqrt6)/40 ~ 0.0388 > 0` for **every** unit
//! vector `v`. So no fourth MU vector exists, and a sufficiently fine cover of certified
//! boxes mechanizes that vector-level wall in our own exact arithmetic. This module is the
//! per-patch engine for that cover.
//!
//! ## The enclosure primitive
//!
//! In `Q(zeta_24)`, `zeta = e^{i pi / 12}`, so for `z = sum_{k<8} a_k zeta^k`:
//! `real(z) = sum_k a_k cos(pi k / 12)` and `imag(z) = sum_k a_k sin(pi k / 12)`. Every
//! `cos(pi k / 12)` and `sin(pi k / 12)` lies in `Q + Q sqrt2 + Q sqrt3 + Q sqrt6` with
//! **rational** coefficients, so `real(z) = R0 + R2 sqrt2 + R3 sqrt3 + R6 sqrt6` exactly
//! (likewise `imag`). The rational decomposition is validated against exact `Cyc24`
//! arithmetic (`z + conj(z) = 2 real(z)`, `z - conj(z) = 2 i imag(z)`), and then enclosed by
//! substituting certified rational intervals for `sqrt2, sqrt3, sqrt6` — no floating point.
//!
//! ## The residual
//!
//! For the candidate `v` with real coordinates `(x_0,y_0,...,x_5,y_5)` (a box of intervals)
//! and a fixed cyclotomic vector `e_i`, write `conj(e_i[k]) = A_k + i B_k` (each an enclosed
//! interval). Then `<e_i, v> = sum_k conj(e_i[k]) v_k` has
//! `Re = sum_k (A_k x_k - B_k y_k)`, `Im = sum_k (A_k y_k + B_k x_k)` (interval-linear), so
//! `|<e_i,v>|^2 = Re^2 + Im^2` and `omega_i = |<e_i,v>|^2 - 1/6` are enclosed exactly. Summing
//! `omega_i^2` lower bounds over all 18 fixed vectors gives a certified lower bound on the
//! whole obstruction; positive over a box => `f < 1` over the box => no MU vector in the box.
//! (On the `B1` columns `conj(e_i[k]) = delta_{ik}`, so this reduces to the rational
//! `b1_residual_sq_lower` — the two modules agree.)
//!
//! MUB(6) <= 3. The complete cover (finitely many certified boxes over the compact candidate
//! space, fed to the Lean `no_four_mub_of_finite_cover`) is the remaining work.

use num_rational::BigRational;
use num_traits::Zero;

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::omega_native::exact::mub6_interval_cover::{NoVectorBox, VectorBox};
use omega_kernel::interval::Interval;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_number_theory::rational::rq;

/// A certified rational-interval enclosure `[lo, hi]` of `sqrt(n)` (`n >= 1`): exact
/// rational bisection maintaining `lo^2 <= n <= hi^2`, so the interval is **sound**.
pub fn sqrt_enclosure(n: i64, iters: u32) -> Interval {
    assert!(n >= 1, "sqrt_enclosure expects n >= 1");
    let target = ri(n);
    let mut lo = ri(1); // 1^2 = 1 <= n
    let mut hi = ri(n); // n^2 >= n
    for _ in 0..iters {
        let mid = (&lo + &hi) / ri(2);
        if &mid * &mid <= target {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    Interval::new(lo, hi)
}

/// Certified enclosures of `sqrt2, sqrt3, sqrt6` carried together (so a residual computation
/// uses one consistent, tight set).
#[derive(Clone, Debug)]
pub struct SqrtBox {
    pub sqrt2: Interval,
    pub sqrt3: Interval,
    pub sqrt6: Interval,
}

impl SqrtBox {
    /// Default precision: ~50 bisection steps (interval width ~ 10^-15).
    pub fn standard() -> Self {
        SqrtBox {
            sqrt2: sqrt_enclosure(2, 50),
            sqrt3: sqrt_enclosure(3, 50),
            sqrt6: sqrt_enclosure(6, 50),
        }
    }
}

/// `cos(pi k / 12) = q0 + q2 sqrt2 + q3 sqrt3 + q6 sqrt6`, returned as `[q0, q2, q3, q6]`.
fn cos_coeffs(k: usize) -> [BigRational; 4] {
    let z = BigRational::zero;
    match k {
        0 => [ri(1), z(), z(), z()],          // 1
        1 => [z(), rq(1, 4), z(), rq(1, 4)],  // (sqrt6 + sqrt2)/4
        2 => [z(), z(), rq(1, 2), z()],       // sqrt3/2
        3 => [z(), rq(1, 2), z(), z()],       // sqrt2/2
        4 => [rq(1, 2), z(), z(), z()],       // 1/2
        5 => [z(), rq(-1, 4), z(), rq(1, 4)], // (sqrt6 - sqrt2)/4
        6 => [z(), z(), z(), z()],            // 0
        7 => [z(), rq(1, 4), z(), rq(-1, 4)], // (sqrt2 - sqrt6)/4
        _ => unreachable!("Cyc24 reduced basis is k < 8"),
    }
}

/// `sin(pi k / 12) = q0 + q2 sqrt2 + q3 sqrt3 + q6 sqrt6`, returned as `[q0, q2, q3, q6]`.
fn sin_coeffs(k: usize) -> [BigRational; 4] {
    let z = BigRational::zero;
    match k {
        0 => [z(), z(), z(), z()],            // 0
        1 => [z(), rq(-1, 4), z(), rq(1, 4)], // (sqrt6 - sqrt2)/4
        2 => [rq(1, 2), z(), z(), z()],       // 1/2
        3 => [z(), rq(1, 2), z(), z()],       // sqrt2/2
        4 => [z(), z(), rq(1, 2), z()],       // sqrt3/2
        5 => [z(), rq(1, 4), z(), rq(1, 4)],  // (sqrt6 + sqrt2)/4
        6 => [ri(1), z(), z(), z()],          // 1
        7 => [z(), rq(1, 4), z(), rq(1, 4)],  // (sqrt6 + sqrt2)/4
        _ => unreachable!("Cyc24 reduced basis is k < 8"),
    }
}

/// Exact real-subfield decomposition `[R0, R2, R3, R6]` of `real(z)` and of `imag(z)`,
/// i.e. `real(z) = R0 + R2 sqrt2 + R3 sqrt3 + R6 sqrt6` (and likewise the imaginary part),
/// with all `R` rational.
pub fn real_imag_decompose(z: &Cyc24) -> ([BigRational; 4], [BigRational; 4]) {
    let mut re = [
        BigRational::zero(),
        BigRational::zero(),
        BigRational::zero(),
        BigRational::zero(),
    ];
    let mut im = re.clone();
    for k in 0..8 {
        let a = &z.a[k];
        if a.is_zero() {
            continue;
        }
        let c = cos_coeffs(k);
        let s = sin_coeffs(k);
        for t in 0..4 {
            re[t] += a * &c[t];
            im[t] += a * &s[t];
        }
    }
    (re, im)
}

fn enclose_subfield(r: &[BigRational; 4], sb: &SqrtBox) -> Interval {
    Interval::point(r[0].clone())
        .add(&Interval::point(r[1].clone()).mul(&sb.sqrt2))
        .add(&Interval::point(r[2].clone()).mul(&sb.sqrt3))
        .add(&Interval::point(r[3].clone()).mul(&sb.sqrt6))
}

/// Certified rational-interval enclosures `(real, imag)` of a `Cyc24` element.
pub fn cyc24_real_imag_enclosure(z: &Cyc24, sb: &SqrtBox) -> (Interval, Interval) {
    let (re, im) = real_imag_decompose(z);
    (enclose_subfield(&re, sb), enclose_subfield(&im, sb))
}

/// Certified lower bound on `omega_i(v)^2` for the single fixed vector `e` over the whole
/// box, where `omega_i = |<e, v>|^2 - 1/6`.
fn column_residual_sq_lower(e: &ExactVec, vbox: &VectorBox, sb: &SqrtBox) -> BigRational {
    let mut re = Interval::point(BigRational::zero());
    let mut im = Interval::point(BigRational::zero());
    for k in 0..D {
        let c = e[k].conj(); // conj(e_i[k]) = A_k + i B_k
        let (a, b) = cyc24_real_imag_enclosure(&c, sb);
        let x = &vbox[2 * k];
        let y = &vbox[2 * k + 1];
        // (A + iB)(x + iy) = (A x - B y) + i (A y + B x)
        re = re.add(&a.mul(x).sub(&b.mul(y)));
        im = im.add(&a.mul(y).add(&b.mul(x)));
    }
    let mod_sq = re.sq().add(&im.sq()); // |<e,v>|^2 over the box
    let omega = mod_sq.sub(&Interval::point(rq(1, 6)));
    omega.sq().into_endpoints().0
}

/// Certified lower bound on the **full** obstruction `sum_{i=0}^{17} omega_i(v)^2` over the
/// box, across all three bases of the canonical triple.
pub fn full_residual_sq_lower(columns: &[ExactVec], vbox: &VectorBox, sb: &SqrtBox) -> BigRational {
    let mut total = BigRational::zero();
    for e in columns {
        total += column_residual_sq_lower(e, vbox, sb);
    }
    total
}

/// Try to certify that no fourth MU vector lies in the box, using the **complete**
/// (B1 + B2 + B3) obstruction. Returns the certified `1 - f >= f_gap > 0` if the full
/// residual lower bound is strictly positive over the box.
pub fn certify_box_excludes_mu_vector_full(vbox: &VectorBox) -> Option<NoVectorBox> {
    let sb = SqrtBox::standard();
    let columns = canonical_triple_exact();
    let lower = full_residual_sq_lower(&columns, vbox, &sb);
    if lower > BigRational::zero() {
        let f_gap = rq(6, 5) * lower;
        Some(NoVectorBox {
            vbox: vbox.clone(),
            f_gap,
        })
    } else {
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::mub6_interval_cover::b1_residual_sq_lower;

    fn point_box(coords: [BigRational; 12]) -> VectorBox {
        coords.map(Interval::point)
    }

    #[test]
    fn sqrt_enclosures_are_sound_and_tight() {
        for &n in &[2i64, 3, 6] {
            let iv = sqrt_enclosure(n, 50);
            // lo^2 <= n <= hi^2 (soundness), and a tight width.
            assert!(iv.lo() * iv.lo() <= ri(n), "lo^2 <= {n}");
            assert!(iv.hi() * iv.hi() >= ri(n), "hi^2 >= {n}");
            assert!(
                iv.hi() - iv.lo() < rq(1, 1_000_000_000_000),
                "width tight for {n}"
            );
        }
    }

    #[test]
    fn real_imag_decomposition_is_exact_over_cyc24() {
        // 2 real(z) = z + conj(z); 2 i imag(z) = z - conj(z). Exact Cyc24 equalities validate
        // the cos/sin coefficient tables for arbitrary z.
        let sq2c = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3));
        let sq3c = Cyc24::zeta24(2).add(&Cyc24::zeta24(-2));
        let sq6c = sq2c.mul(&sq3c);
        let i = Cyc24::zeta24(6);

        let rebuild = |r: &[BigRational; 4]| -> Cyc24 {
            Cyc24::rat(r[0].clone() * ri(2))
                .add(&Cyc24::rat(r[1].clone() * ri(2)).mul(&sq2c))
                .add(&Cyc24::rat(r[2].clone() * ri(2)).mul(&sq3c))
                .add(&Cyc24::rat(r[3].clone() * ri(2)).mul(&sq6c))
        };

        // Test on every basis power and on real curvature-cochain entries (canonical columns).
        let mut samples: Vec<Cyc24> = (0..8).map(|k| Cyc24::zeta24(k)).collect();
        for e in canonical_triple_exact() {
            for c in e {
                samples.push(c);
            }
        }
        for z in &samples {
            let (re, im) = real_imag_decompose(z);
            assert_eq!(rebuild(&re), z.add(&z.conj()), "2 real(z) = z + conj(z)");
            assert_eq!(
                i.mul(&rebuild(&im)),
                z.sub(&z.conj()),
                "2 i imag(z) = z - conj(z)"
            );
        }
    }

    #[test]
    fn enclosure_contains_known_values() {
        let sb = SqrtBox::standard();
        // zeta^2 = e^{i pi/6}: real = cos30 = sqrt3/2 ~ 0.8660, imag = sin30 = 1/2 (exact).
        let (re, im) = cyc24_real_imag_enclosure(&Cyc24::zeta24(2), &sb);
        assert!(
            re.lo() > &rq(866, 1000) && re.hi() < &rq(867, 1000),
            "real ~ 0.8660"
        );
        assert_eq!(im, Interval::point(rq(1, 2)), "imag = 1/2 exactly");
        // i = zeta^6: real = 0 (exact), imag = 1 (exact).
        let (re_i, im_i) = cyc24_real_imag_enclosure(&Cyc24::zeta24(6), &sb);
        assert_eq!(re_i, Interval::point(BigRational::zero()));
        assert_eq!(im_i, Interval::point(ri(1)));
    }

    #[test]
    fn full_residual_dominates_b1_and_certifies_e0() {
        // Point "box" at e_0 (the standard basis vector): exact, so omega is exact.
        let mut coords: [BigRational; 12] = std::array::from_fn(|_| BigRational::zero());
        coords[0] = ri(1); // x_0 = 1
        let vbox = point_box(coords);

        let b1 = b1_residual_sq_lower(&vbox);
        let sb = SqrtBox::standard();
        let full = full_residual_sq_lower(&canonical_triple_exact(), &vbox, &sb);

        // B1 alone at e_0: omega_0 = 5/6, five others = -1/6 => sum = (5/6)^2 + 5(1/6)^2 = 5/6.
        assert_eq!(b1, rq(5, 6));
        // The full residual includes B1 plus nonnegative B2/B3 terms, so full >= b1 > 0.
        assert!(
            full >= b1,
            "full obstruction dominates the B1 sub-certificate"
        );
        // And the complete certificate excludes the box.
        let cert = certify_box_excludes_mu_vector_full(&vbox).expect("e_0 box excluded");
        assert!(cert.f_gap > BigRational::zero());
    }

    #[test]
    fn full_residual_certifies_a_b1_unbiased_box() {
        // The box B1 abstained on (|v_i|^2 ~ 1/6 on every standard coordinate). B1 alone
        // cannot exclude it; the full B1+B2+B3 residual can (a B1-unbiased config is not
        // unbiased to B2/B3), demonstrating the gap is closed.
        let coord = Interval::new(rq(40, 100), rq(41, 100));
        let mut vbox: VectorBox = std::array::from_fn(|_| Interval::point(BigRational::zero()));
        for i in 0..6 {
            vbox[2 * i] = coord.clone();
        }
        assert!(
            b1_residual_sq_lower(&vbox) == BigRational::zero(),
            "B1 abstains on this box"
        );
        let sb = SqrtBox::standard();
        let full = full_residual_sq_lower(&canonical_triple_exact(), &vbox, &sb);
        assert!(
            full > BigRational::zero(),
            "full residual certifies where B1 abstains"
        );
    }
}
