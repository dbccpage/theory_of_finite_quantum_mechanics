//! Exact rational-interval finite-cover certificates for MUB(6).
//!
//! This is the artifact whose output IS a global statement: a single certified box rules
//! out a fourth mutually-unbiased vector over the **entire continuum** of configurations
//! inside that box (finite data, infinite conclusion). A finite list of such boxes that
//! covers the candidate space is, via the mechanized `no_four_mub_of_finite_cover`
//! (`lean4/research_programs/mub6/TripleExtensionAssembly.lean`), the global no-extension theorem. Compactness
//! is the finite-to-infinite operator; interval arithmetic is its checkable form.
//!
//! All arithmetic is exact over `Q` (rational interval endpoints) — no floating point, so
//! every lower bound is certified, not estimated.
//!
//! Method. For the canonical triple `T0 = {Z2(x)Z3, X2(x)Q0, Y2(x)Q1}` and a candidate unit
//! vector `v in C^6` written in real coordinates `(x_0,y_0,...,x_5,y_5)`, the curvature
//! against a fixed vector `e_i` is `omega_i(v) = |<e_i,v>|^2 - 1/6` and the
//! Invariant-Systems wall functional is `f(v) = 1 - (6/5) sum_i omega_i(v)^2`. A vector is
//! mutually unbiased to `T0` iff `f(v) = 1` iff every `omega_i = 0`. So a certified
//! **positive lower bound** on `sum_i omega_i^2` over a box proves `f < 1` over that box,
//! i.e. **no MU vector lives in the box**.
//!
//! This module certifies the contribution of the **standard basis `B1`** (the first basis
//! `Z2(x)Z3`), whose residuals `omega_i = (x_i^2 + y_i^2) - 1/6` have **rational**
//! coefficients, so the bound is fully exact with no cyclotomic enclosure. Since the other
//! 15 residuals only add nonnegative terms, the `B1` lower bound is a sound lower bound on
//! the whole obstruction. The cyclotomic enclosure for the `B2/B3` residuals (which widens
//! the certifiable region beyond the `B1`-dominated charts) is the next piece.
//!
//! requires a finite list of boxes that *covers* the whole candidate/triple space and feeds
//! the Lean finite-cover theorem; producing that complete cover is the remaining work. This
//! module mints no authority on its own.

use num_rational::BigRational;
use num_traits::Zero;
use omega_kernel::interval::Interval;
use omega_number_theory::rational::rq;

/// A box of candidate unit vectors in real coordinates `(x_0,y_0,...,x_5,y_5)`: 12
/// intervals.
pub type VectorBox = [Interval; 12];

/// A certified lower bound on `sum_{i in B1} omega_i(v)^2` over the whole box, using only
/// the exact rational standard-basis residuals `omega_i = (x_i^2 + y_i^2) - 1/6`.
pub fn b1_residual_sq_lower(vbox: &VectorBox) -> BigRational {
    let sixth = Interval::point(rq(1, 6));
    let mut total = BigRational::zero();
    for i in 0..6 {
        let xi = &vbox[2 * i];
        let yi = &vbox[2 * i + 1];
        let mod_sq = xi.sq().add(&yi.sq()); // |v_i|^2 over the box
        let omega = mod_sq.sub(&sixth); // omega_i over the box
        total += omega.sq().lo(); // lower bound of omega_i^2
    }
    total
}

/// A patch certificate: a box together with a certified positive gap `1 - f >= gap` proving
/// no MU vector lies in the box.
#[derive(Clone, Debug)]
pub struct NoVectorBox {
    pub vbox: VectorBox,
    /// Certified `1 - f(v) >= f_gap > 0` for every `v` in the box.
    pub f_gap: BigRational,
}

/// Try to certify that no fourth MU vector lies in the box. Returns the certified
/// `1 - f` gap if `sum_{B1} omega^2 > 0` over the box (which forces `f < 1`).
pub fn certify_box_excludes_mu_vector(vbox: &VectorBox) -> Option<NoVectorBox> {
    let b1_lower = b1_residual_sq_lower(vbox);
    if b1_lower > BigRational::zero() {
        // f = 1 - (6/5) sum_all omega^2 <= 1 - (6/5) * b1_lower, and b1_lower <= sum_all.
        let f_gap = rq(6, 5) * b1_lower;
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

    fn iv(lo: (i64, i64), hi: (i64, i64)) -> Interval {
        Interval::new(rq(lo.0, lo.1), rq(hi.0, hi.1))
    }

    #[test]
    fn interval_arithmetic_is_exact() {
        assert_eq!(
            iv((1, 1), (2, 1)).add(&iv((3, 1), (4, 1))),
            iv((4, 1), (6, 1))
        );
        assert_eq!(
            iv((1, 1), (2, 1)).mul(&iv((3, 1), (4, 1))),
            iv((3, 1), (8, 1))
        );
        // square of an interval straddling zero floors at 0.
        assert_eq!(iv((-1, 1), (2, 1)).sq(), iv((0, 1), (4, 1)));
        // square of a positive interval.
        assert_eq!(iv((2, 1), (3, 1)).sq(), iv((4, 1), (9, 1)));
        // square of a negative interval.
        assert_eq!(iv((-3, 1), (-2, 1)).sq(), iv((4, 1), (9, 1)));
    }

    fn small() -> Interval {
        iv((-1, 20), (1, 20)) // [-0.05, 0.05]
    }

    #[test]
    fn box_near_e0_excludes_any_mu_vector() {
        // v concentrated on coordinate 0: x_0 in [0.9, 1], y_0 in [-0.05, 0.05], rest small.
        let mut vbox: VectorBox = std::array::from_fn(|_| small());
        vbox[0] = iv((9, 10), (1, 1)); // x_0
        let cert = certify_box_excludes_mu_vector(&vbox)
            .expect("a box near e_0 must exclude any MU vector");
        // omega_0 in [0.81 - 1/6, ...] is bounded away from 0, so the gap is strictly > 0.
        assert!(cert.f_gap > BigRational::zero());
    }

    #[test]
    fn box_at_an_unbiased_point_is_not_certified_by_b1_alone() {
        // |v_i|^2 = 1/6 on every standard coordinate => omega_i(B1) = 0, so the B1 lower
        // bound is 0 and this honest sub-certificate cannot exclude the box on its own
        // (the B2/B3 cyclotomic residuals are required there).
        // x_i = sqrt(1/6) ~ 0.408; bracket it loosely so |v_i|^2 brackets 1/6.
        let coord = iv((40, 100), (41, 100)); // [0.40, 0.41], 0.40^2..0.41^2 ~ [0.16,0.168]
        let mut vbox: VectorBox = std::array::from_fn(|_| Interval::point(BigRational::zero()));
        for i in 0..6 {
            vbox[2 * i] = coord.clone();
        }
        // |v_i|^2 in [0.16, 0.1681]; omega_i in [0.16-1/6, 0.1681-1/6] straddles 0,
        // so omega_i^2 lower bound is 0 and the B1 certificate abstains.
        assert!(certify_box_excludes_mu_vector(&vbox).is_none());
    }

    #[test]
    fn test_closed_box_bisection_contains_boundary_with_zero_leakage() {
        // Formally test that bisect_closed guarantees [a, m] and [m, b] contain the boundary point m
        // in both closures with zero gap and zero boundary leakage.
        let parent = iv((-3, 7), (11, 5)); // [-3/7, 11/5]
        let (left, right) = parent.bisect_closed();

        assert_eq!(left.lo(), parent.lo());
        assert_eq!(right.hi(), parent.hi());
        assert_eq!(left.hi(), right.lo());

        let mid = left.hi();
        assert!(left.contains(mid));
        assert!(right.contains(mid));
        assert!(parent.contains(mid));

        // Midpoint is exactly (lo + hi)/2:
        let expected_mid = (parent.lo() + parent.hi()) / BigRational::from_integer(2.into());
        assert_eq!(*mid, expected_mid);
    }
}
