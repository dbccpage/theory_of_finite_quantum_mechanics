//! Branch-and-bound finite-cover driver for the MUB(6) no-extension theorem.
//!
//! This consumes the complete per-patch certificate (`mub6_cyclotomic_enclosure`) to *cover*
//! a region of candidate vectors: it recursively subdivides a box until every sub-box is
//! certified to contain no fourth MU vector, or a depth budget is hit (leaving honestly
//! reported uncertified residue). The output — a finite list of certified boxes with positive
//! `1 - f` gaps covering a stated region — is exactly the data the mechanized Lean theorem
//! `MUB.no_four_mub_of_finite_cover` (`lean4/research_programs/mub6/TripleExtensionAssembly.lean`) consumes. This
//! is the engine that turns the local "finite proves infinite" certificate into a global one.
//!
//! ## The reduced search space (why a cover is feasible at all)
//!
//! A fourth MU vector `v` must be unbiased to the standard basis `B1`, i.e. `|v_i|^2 = 1/6`
//! for every coordinate. That pins all six moduli, leaving only the **phases** — and global
//! phase is gauge — so the candidate set is a compact **5-torus**, not the 11-dimensional
//! sphere. In `(x_i, y_i)` real coordinates each `v_i` lies on the circle `x_i^2 + y_i^2 =
//! 1/6`, so a torus cell is a product of arc-bracketing boxes, all with rational endpoints
//! (no transcendental angle enclosure needed). A box whose `(x_i^2 + y_i^2)` interval does
//! **not** contain `1/6` holds no `B1`-unbiased vector and is discarded without certification.
//!
//! The Invariant-Systems wall `max f = W = (88+3 sqrt6)/100 < 1` guarantees the obstruction
//! `sum_i omega_i^2 >= (4 - sqrt6)/40 > 0` on the entire torus, so the subdivision terminates:
//! once boxes are small enough that interval slop drops below that floor, every box certifies.
//!
//! product over all cells (a heavy but finite computation). It mints no authority and is not
//! itself the claim `MUB(6) <= 3`; it is the assembly engine whose completed output, fed to
//! the Lean bridge, would be the global no-(4th-vector) theorem for the canonical triple.

use num_rational::BigRational;
use num_traits::Zero;

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::omega_native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::omega_native::exact::mub6_interval_cover::{NoVectorBox, VectorBox};
use omega_kernel::interval::Interval;
use omega_number_theory::rational::ri;

fn sixth() -> BigRational {
    ri(1) / ri(6)
}

/// Exact rational error bounds certifying the scope of a ±delta widening.
///
/// Non-claim:
/// - AuthorityEffect: None
/// - stated region only; mints no authority
/// - Restricted words: forced, minimal, free, canonical, equivalent, universal, complete require proof or explicit conditional scope.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct WideningScopeBounds {
    /// The exact rational widening radius delta (e.g. 1/1000).
    pub delta: BigRational,
    /// Maximum coordinate error |Re(E') - Re(E)| <= delta and |Im(E') - Im(E)| <= delta.
    pub max_coord_error: BigRational,
    /// Maximum entrywise squared modulus deviation |E' - E|^2 = (Delta x)^2 + (Delta y)^2 <= 2 * delta^2.
    pub max_entry_mod_sq_bound: BigRational,
    /// Maximum column L2 norm squared deviation sum_{k=0}^5 |E'_k - E_k|^2 <= 12 * delta^2.
    pub max_col_l2_sq_bound: BigRational,
    /// Maximum inner product squared perturbation |<E' - E, v>|^2 <= 12 * delta^2 for any unit vector v.
    pub max_inner_product_error_sq: BigRational,
    /// Formal scope declaration: Cartesian entrywise L^inf ball of radius delta in the fixed gauge.
    pub scope_description: &'static str,
    /// Gauge firewall: does not quotient by ray or column phase equivalence classes.
    pub firewall: &'static str,
}

/// Refusal to calculate widening bounds for an invalid radius.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error)]
pub enum WideningBoundsError {
    #[error("widening delta must be non-negative")]
    NegativeDelta,
}

/// The 18 fixed vectors with each entry's conjugate **pre-enclosed** as `(real, imag)`
/// rational intervals. Precomputing the cyclotomic enclosure once turns the per-box residual
/// into pure rational-interval arithmetic — the hot path of the cover.
pub struct EnclosedTriple {
    cols: Vec<[(Interval, Interval); D]>,
}

impl EnclosedTriple {
    pub fn standard() -> Self {
        Self::from_exact_columns(&canonical_triple_exact())
    }

    /// Enclose an arbitrary exact 18-column MU triple (or any fixed-vector list) for cover use.
    ///
    /// Used by the genuine Dita-seed cover lane (`mub6_dita_seed_cover`) to drive the same
    /// residual kernel against `{I, F6(dx,dy), Y2⊗Q1}` rather than only the canonical `T0`.
    pub fn from_exact_columns(columns: &[ExactVec]) -> Self {
        let sb = SqrtBox::standard();
        let cols = columns
            .iter()
            .map(|e| std::array::from_fn(|k| cyc24_real_imag_enclosure(&e[k].conj(), &sb)))
            .collect();
        EnclosedTriple { cols }
    }

    /// Certified lower bound on `sum_i omega_i(v)^2` over the box (all 18 fixed vectors).
    pub fn residual_sq_lower(&self, vbox: &VectorBox) -> BigRational {
        let target = Interval::point(sixth());
        let mut total = BigRational::zero();
        for col in &self.cols {
            let mut re = Interval::point(BigRational::zero());
            let mut im = Interval::point(BigRational::zero());
            for k in 0..D {
                let (a, b) = &col[k];
                let x = &vbox[2 * k];
                let y = &vbox[2 * k + 1];
                // <e,v> term: (A + iB)(x + iy) = (A x - B y) + i (A y + B x)
                re = re.add(&a.mul(x).sub(&b.mul(y)));
                im = im.add(&a.mul(y).add(&b.mul(x)));
            }
            let mod_sq = re.sq().add(&im.sq());
            let omega = mod_sq.sub(&target);
            total += omega.sq().lo();
        }
        total
    }

    /// Compute exact rational error bounds certifying the formal scope of a ±delta widening.
    pub fn widening_error_bounds(
        delta: &BigRational,
    ) -> Result<WideningScopeBounds, WideningBoundsError> {
        if delta < &BigRational::zero() {
            return Err(WideningBoundsError::NegativeDelta);
        }
        let two = BigRational::from_integer(2.into());
        let twelve = BigRational::from_integer(12.into());
        let delta_sq = delta * delta;
        Ok(WideningScopeBounds {
            delta: delta.clone(),
            max_coord_error: delta.clone(),
            max_entry_mod_sq_bound: &two * &delta_sq,
            max_col_l2_sq_bound: &twelve * &delta_sq,
            max_inner_product_error_sq: &twelve * &delta_sq,
            scope_description: "Cartesian entrywise L^inf neighborhood B_delta(T) = { T' in C^(18x6) : max_{ci in B2,B3} max_k max(|Re(T'_{ci,k}) - Re(T_{ci,k})|, |Im(T'_{ci,k}) - Im(T_{ci,k})|) <= delta } in fixed gauge representation",
            firewall: "AuthorityEffect: None. Scoped strictly to Cartesian entrywise L^inf ball. Phase-equivalent triples with column phase rotations theta > arcsin(delta * sqrt(6)) are NOT contained in this Cartesian enclosure; mints no authority.",
        })
    }

    /// The standard triple `T0`, widened by `±delta` on the non-identity bases (`B2` and `B3`).
    ///
    /// Soundness: widening can only widen the residual interval, so the certified lower bound is
    /// `≤` the exact one — the widened cover is a strictly *sound* test over a *superset* of the
    /// valid MUB triples near `T0`.
    pub fn widened(delta: &BigRational) -> Self {
        Self::widened_from_exact_columns(&canonical_triple_exact(), delta)
    }

    /// Same as [`Self::widened`], but centered at an arbitrary exact 18-column triple
    /// (e.g. a genuine Dita seed `{I, F6(dx,dy), Y2⊗Q1}`). `B1` columns stay exact; `B2`/`B3`
    /// entries widen by `±delta`.
    ///
    /// Formally scoped under [`WideningScopeBounds`]:
    /// Entrywise deviations are strictly bounded by `max_coord_error = delta` and
    /// `max_col_l2_sq_bound = 12 * delta^2`. Completeness of a cover against this enclosure is a
    /// neighborhood no-go for that center in the fixed coordinate gauge — not moduli exhaustion
    /// and not `MUB(6)=3`.
    pub fn widened_from_exact_columns(columns: &[ExactVec], delta: &BigRational) -> Self {
        assert!(
            delta >= &BigRational::zero(),
            "widening delta must be non-negative"
        );
        let base = Self::from_exact_columns(columns);
        let d = Interval::new(-delta.clone(), delta.clone());
        let cols = base
            .cols
            .iter()
            .enumerate()
            .map(|(ci, col)| {
                std::array::from_fn(|k| {
                    let (re, im) = &col[k];
                    if ci < D {
                        // B1 columns 0..6: exact standard basis, not part of the moduli.
                        (re.clone(), im.clone())
                    } else {
                        // B2/B3 columns 6..18: widen to enclose the moduli neighborhood.
                        (re.add(&d), im.add(&d))
                    }
                })
            })
            .collect();
        EnclosedTriple { cols }
    }

    /// Certify a single box: `Some(gap)` iff the full obstruction is provably positive over it.
    pub fn certify(&self, vbox: &VectorBox) -> Option<NoVectorBox> {
        let lower = self.residual_sq_lower(vbox);
        if lower > BigRational::zero() {
            Some(NoVectorBox {
                vbox: vbox.clone(),
                f_gap: ri(6) / ri(5) * lower,
            })
        } else {
            None
        }
    }
}

/// `true` iff the box can hold a `B1`-unbiased vector — i.e. for every coordinate the interval
/// `x_i^2 + y_i^2` contains `1/6`. Boxes failing this hold no fourth MU vector and need no
/// certification (they are off the torus).
pub fn box_touches_torus(vbox: &VectorBox) -> bool {
    let t = sixth();
    (0..D).all(|k| {
        let mod_sq = vbox[2 * k].sq().add(&vbox[2 * k + 1].sq());
        mod_sq.lo() <= &t && t <= *mod_sq.hi()
    })
}

fn split_widest(vbox: &VectorBox) -> (VectorBox, VectorBox) {
    let mut wi = 0;
    let mut width = vbox[0].hi() - vbox[0].lo();
    for i in 1..2 * D {
        let w = vbox[i].hi() - vbox[i].lo();
        if w > width {
            width = w;
            wi = i;
        }
    }
    let (left, right) = vbox[wi].bisect_closed();
    debug_assert_eq!(left.hi(), right.lo());
    debug_assert!(left.contains(left.hi()));
    debug_assert!(right.contains(right.lo()));
    let mut a = vbox.clone();
    let mut b = vbox.clone();
    a[wi] = left;
    b[wi] = right;
    (a, b)
}

/// The result of covering a region by subdivision.
#[derive(Debug)]
pub struct CoverReport {
    /// Number of certified boxes whose union (with the off-torus discards) covers the region.
    pub certified: usize,
    /// Boxes pruned as off-torus (cannot hold a `B1`-unbiased vector).
    pub off_torus: usize,
    /// Boxes that hit the depth budget without certifying — the honest residue (empty = the
    /// region is fully covered: no fourth MU vector anywhere in it).
    pub uncertified: Vec<VectorBox>,
    /// The smallest certified `1 - f` gap encountered (a witness of how tight the cover is).
    pub min_gap: Option<BigRational>,
    /// Maximum subdivision depth actually used.
    pub max_depth_used: u32,
}

impl CoverReport {
    pub fn is_complete(&self) -> bool {
        self.uncertified.is_empty()
    }
}

/// Cover `region` by branch-and-bound subdivision: certify, else discard if off-torus, else
/// split the widest coordinate and recurse until certified or `max_depth` is exhausted.
pub fn cover_region(enc: &EnclosedTriple, region: VectorBox, max_depth: u32) -> CoverReport {
    let mut stack = vec![(region, 0u32)];
    let mut report = CoverReport {
        certified: 0,
        off_torus: 0,
        uncertified: Vec::new(),
        min_gap: None,
        max_depth_used: 0,
    };
    while let Some((vbox, depth)) = stack.pop() {
        if depth > report.max_depth_used {
            report.max_depth_used = depth;
        }
        if !box_touches_torus(&vbox) {
            report.off_torus += 1;
            continue;
        }
        if let Some(c) = enc.certify(&vbox) {
            report.certified += 1;
            report.min_gap = Some(match report.min_gap.take() {
                Some(g) if g <= c.f_gap => g,
                _ => c.f_gap,
            });
        } else if depth >= max_depth {
            report.uncertified.push(vbox);
        } else {
            let (a, b) = split_widest(&vbox);
            stack.push((a, depth + 1));
            stack.push((b, depth + 1));
        }
    }
    report
}

#[cfg(test)]
mod tests {
    use super::*;

    fn coord(lo: (i64, i64), hi: (i64, i64)) -> Interval {
        Interval::new(ri(lo.0) / ri(lo.1), ri(hi.0) / ri(hi.1))
    }

    /// A torus cell: every coordinate `v_i` bracketed near angle 45 deg on the circle of
    /// radius `1/sqrt6` (`x_i = y_i ~ 0.2887`). `x^2 + y^2` ranges over [0.125, 0.205] ∋ 1/6.
    fn torus_cell(half: (i64, i64)) -> VectorBox {
        let lo = ri(28) / ri(100) - ri(half.0) / ri(half.1);
        let hi = ri(28) / ri(100) + ri(half.0) / ri(half.1);
        std::array::from_fn(|_| Interval::new(lo.clone(), hi.clone()))
    }

    #[test]
    fn off_torus_box_is_pruned() {
        // A box far from the circle (|v_i|^2 ~ 1 >> 1/6) cannot hold a B1-unbiased vector.
        let vbox: VectorBox = std::array::from_fn(|_| coord((9, 10), (1, 1)));
        assert!(!box_touches_torus(&vbox));
        let enc = EnclosedTriple::standard();
        let report = cover_region(&enc, vbox, 4);
        assert_eq!(report.off_torus, 1);
        assert_eq!(report.certified, 0);
        assert!(report.is_complete());
    }

    #[test]
    fn small_torus_cell_is_fully_covered() {
        // A narrow torus cell: the per-patch certificate excludes it (possibly after a few
        // splits), so the region provably contains no fourth MU vector.
        let enc = EnclosedTriple::standard();
        let report = cover_region(&enc, torus_cell((2, 100)), 24);
        assert!(
            report.is_complete(),
            "narrow cell fully covered: {report:?}"
        );
        assert!(report.certified >= 1);
        assert!(report.min_gap.unwrap() > BigRational::zero());
    }

    #[test]
    fn wide_cell_subdivides_prunes_and_fully_covers() {
        // A cell too wide (half = 0.18) for the top box to certify (interval slop exceeds the
        // obstruction floor), so the driver must subdivide. Sub-boxes that cannot reach the
        // torus (|v_i|^2 = 1/6 on every coordinate) are pruned, the rest certify. Exercises
        // branch-and-bound, off-torus pruning, and full coverage together.
        let enc = EnclosedTriple::standard();
        let wide = torus_cell((18, 100));
        assert!(
            enc.certify(&wide).is_none(),
            "the wide cell must not certify at the top box"
        );

        let report = cover_region(&enc, wide, 30);
        assert!(report.is_complete(), "region fully covered: {report:?}");
        assert!(
            report.certified > 1,
            "branch-and-bound produced multiple certified boxes"
        );
        assert!(report.off_torus > 0, "off-torus sub-boxes were pruned");
        assert!(report.max_depth_used >= 1, "subdivision occurred");
        assert!(report.min_gap.unwrap() > BigRational::zero());
    }

    #[test]
    fn split_widest_halves_the_widest_coordinate() {
        let narrow = Interval::new(ri(26) / ri(100), ri(30) / ri(100));
        let mut vbox: VectorBox = std::array::from_fn(|_| narrow.clone());
        vbox[7] = Interval::new(ri(0), ri(1)); // the widest coordinate
        let (a, b) = split_widest(&vbox);
        // The widest coordinate (index 7) is halved; the union of the two halves is the whole.
        assert_eq!(a[7], Interval::new(ri(0), ri(1) / ri(2)));
        assert_eq!(b[7], Interval::new(ri(1) / ri(2), ri(1)));
        // Every other coordinate is unchanged.
        for i in 0..2 * D {
            if i != 7 {
                assert_eq!(a[i], narrow);
                assert_eq!(b[i], narrow);
            }
        }
    }

    #[test]
    fn widening_scope_bounds_exact_rational_computation() {
        let delta = ri(1) / ri(1000);
        let bounds = EnclosedTriple::widening_error_bounds(&delta).unwrap();
        assert_eq!(bounds.delta, delta);
        assert_eq!(bounds.max_coord_error, delta);
        // max_entry_mod_sq_bound = 2 * (1/1000)^2 = 2 / 1_000_000 = 1 / 500_000
        assert_eq!(bounds.max_entry_mod_sq_bound, ri(1) / ri(500_000));
        // max_col_l2_sq_bound = 12 * (1/1000)^2 = 12 / 1_000_000 = 3 / 250_000
        assert_eq!(bounds.max_col_l2_sq_bound, ri(3) / ri(250_000));
        assert_eq!(bounds.max_inner_product_error_sq, ri(3) / ri(250_000));
        assert!(bounds.firewall.contains("mints no authority"));
        assert!(bounds.firewall.contains("AuthorityEffect: None"));
    }

    #[test]
    fn widening_error_bounds_rejects_negative_delta() {
        let neg_delta = ri(-1) / ri(1000);
        assert_eq!(
            EnclosedTriple::widening_error_bounds(&neg_delta),
            Err(WideningBoundsError::NegativeDelta)
        );
    }

    #[test]
    fn widening_error_bounds_accepts_zero_delta() {
        let bounds = EnclosedTriple::widening_error_bounds(&BigRational::zero()).unwrap();
        assert_eq!(bounds.max_coord_error, BigRational::zero());
        assert_eq!(bounds.max_entry_mod_sq_bound, BigRational::zero());
        assert_eq!(bounds.max_col_l2_sq_bound, BigRational::zero());
        assert_eq!(bounds.max_inner_product_error_sq, BigRational::zero());
    }
}
