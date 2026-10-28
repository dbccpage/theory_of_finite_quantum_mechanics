
use num_rational::BigRational;
use num_traits::Zero;

use crate::native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::native::exact::mub6_interval_cover::{NoVectorBox, VectorBox};
use omega_kernel::interval::Interval;
use tfqm_number_theory::rational::ri;

fn sixth() -> BigRational {
    ri(1) / ri(6)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct WideningScopeBounds {
    pub delta: BigRational,
    pub max_coord_error: BigRational,
    pub max_entry_mod_sq_bound: BigRational,
    pub max_col_l2_sq_bound: BigRational,
    pub max_inner_product_error_sq: BigRational,
    pub scope_description: &'static str,
    pub firewall: &'static str,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error)]
pub enum WideningBoundsError {
    #[error("widening delta must be non-negative")]
    NegativeDelta,
}

pub struct EnclosedTriple {
    cols: Vec<[(Interval, Interval); D]>,
}

impl EnclosedTriple {
    pub fn standard() -> Self {
        Self::from_exact_columns(&canonical_triple_exact())
    }

    pub fn from_exact_columns(columns: &[ExactVec]) -> Self {
        let sb = SqrtBox::standard();
        let cols = columns
            .iter()
            .map(|e| std::array::from_fn(|k| cyc24_real_imag_enclosure(&e[k].conj(), &sb)))
            .collect();
        EnclosedTriple { cols }
    }

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
                re = re.add(&a.mul(x).sub(&b.mul(y)));
                im = im.add(&a.mul(y).add(&b.mul(x)));
            }
            let mod_sq = re.sq().add(&im.sq());
            let omega = mod_sq.sub(&target);
            total += omega.sq().lo();
        }
        total
    }

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

    pub fn widened(delta: &BigRational) -> Self {
        Self::widened_from_exact_columns(&canonical_triple_exact(), delta)
    }

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
                        (re.clone(), im.clone())
                    } else {
                        (re.add(&d), im.add(&d))
                    }
                })
            })
            .collect();
        EnclosedTriple { cols }
    }

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

#[derive(Debug)]
pub struct CoverReport {
    pub certified: usize,
    pub off_torus: usize,
    pub uncertified: Vec<VectorBox>,
    pub min_gap: Option<BigRational>,
    pub max_depth_used: u32,
}

impl CoverReport {
    pub fn is_complete(&self) -> bool {
        self.uncertified.is_empty()
    }
}

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

    fn torus_cell(half: (i64, i64)) -> VectorBox {
        let lo = ri(28) / ri(100) - ri(half.0) / ri(half.1);
        let hi = ri(28) / ri(100) + ri(half.0) / ri(half.1);
        std::array::from_fn(|_| Interval::new(lo.clone(), hi.clone()))
    }

    #[test]
    fn off_torus_box_is_pruned() {
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
        vbox[7] = Interval::new(ri(0), ri(1));
        let (a, b) = split_widest(&vbox);
        assert_eq!(a[7], Interval::new(ri(0), ri(1) / ri(2)));
        assert_eq!(b[7], Interval::new(ri(1) / ri(2), ri(1)));
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
        assert_eq!(bounds.max_entry_mod_sq_bound, ri(1) / ri(500_000));
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
