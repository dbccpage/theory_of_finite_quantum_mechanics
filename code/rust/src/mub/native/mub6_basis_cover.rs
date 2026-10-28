
use num_rational::BigRational;
use num_traits::Zero;

use crate::native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::native::exact::mub6_cyclotomic_enclosure::{
    cyc24_real_imag_enclosure, full_residual_sq_lower, SqrtBox,
};
use crate::native::exact::mub6_interval_cover::VectorBox;
use omega_kernel::interval::Interval;

pub type BasisBox = [VectorBox; D];

pub fn basis_residual_sq_lower(columns: &[ExactVec], bbox: &BasisBox, sb: &SqrtBox) -> BigRational {
    let mut total = BigRational::zero();
    for col_box in bbox.iter() {
        total += full_residual_sq_lower(columns, col_box, sb);
    }
    total
}

#[derive(Clone, Debug)]
pub struct NoBasisBox {
    pub bbox: BasisBox,
    pub psi_gap: BigRational,
}

pub fn certify_basis_box_excludes_fourth_for_triple(
    columns: &[ExactVec],
    bbox: &BasisBox,
) -> Option<NoBasisBox> {
    let sb = SqrtBox::standard();
    let lower = basis_residual_sq_lower(columns, bbox, &sb);
    if lower > BigRational::zero() {
        Some(NoBasisBox {
            bbox: bbox.clone(),
            psi_gap: lower,
        })
    } else {
        None
    }
}

pub fn certify_basis_box_excludes_fourth(bbox: &BasisBox) -> Option<NoBasisBox> {
    certify_basis_box_excludes_fourth_for_triple(&canonical_triple_exact(), bbox)
}

pub fn basis_box_excluded_by_column_for_triple(
    columns: &[ExactVec],
    bbox: &BasisBox,
) -> Option<(usize, BigRational)> {
    let sb = SqrtBox::standard();
    for (j, col_box) in bbox.iter().enumerate() {
        let lower = full_residual_sq_lower(columns, col_box, &sb);
        if lower > BigRational::zero() {
            return Some((j, lower));
        }
    }
    None
}

pub fn basis_box_excluded_by_column(bbox: &BasisBox) -> Option<(usize, BigRational)> {
    basis_box_excluded_by_column_for_triple(&canonical_triple_exact(), bbox)
}


pub fn bisect_closed_interval(parent: &Interval) -> (Interval, Interval) {
    parent.bisect_closed()
}

pub fn verify_closed_box_bisection_soundness(
    parent: &Interval,
    left: &Interval,
    right: &Interval,
) -> bool {
    left.lo() == parent.lo()
        && right.hi() == parent.hi()
        && left.hi() == right.lo()
        && left.contains(left.hi())
        && right.contains(right.lo())
        && parent.contains(left.hi())
        && left.lo() <= left.hi()
        && right.lo() <= right.hi()
}

pub fn bisect_closed_vector_box(vbox: &VectorBox) -> (VectorBox, VectorBox) {
    let mut wi = 0;
    let mut width = vbox[0].hi() - vbox[0].lo();
    for i in 1..2 * D {
        let w = vbox[i].hi() - vbox[i].lo();
        if w > width {
            width = w;
            wi = i;
        }
    }
    let (left_ival, right_ival) = vbox[wi].bisect_closed();
    debug_assert!(verify_closed_box_bisection_soundness(
        &vbox[wi],
        &left_ival,
        &right_ival
    ));
    let mut a = vbox.clone();
    let mut b = vbox.clone();
    a[wi] = left_ival;
    b[wi] = right_ival;
    (a, b)
}

pub fn bisect_closed_basis_box(bbox: &BasisBox) -> (BasisBox, BasisBox) {
    let mut best_col = 0;
    let mut best_coord = 0;
    let mut max_width = bbox[0][0].hi() - bbox[0][0].lo();

    for (col_idx, vbox) in bbox.iter().enumerate() {
        for coord_idx in 0..2 * D {
            let w = vbox[coord_idx].hi() - vbox[coord_idx].lo();
            if w > max_width {
                max_width = w;
                best_col = col_idx;
                best_coord = coord_idx;
            }
        }
    }

    let (left_ival, right_ival) = bbox[best_col][best_coord].bisect_closed();
    debug_assert!(verify_closed_box_bisection_soundness(
        &bbox[best_col][best_coord],
        &left_ival,
        &right_ival
    ));
    let mut a = bbox.clone();
    let mut b = bbox.clone();
    a[best_col][best_coord] = left_ival;
    b[best_col][best_coord] = right_ival;
    (a, b)
}


#[derive(Clone, Debug)]
pub struct CIval {
    pub re: Interval,
    pub im: Interval,
}

impl CIval {
    pub fn conj(&self) -> CIval {
        let zero = Interval::point(BigRational::zero());
        CIval {
            re: self.re.clone(),
            im: zero.sub(&self.im),
        }
    }

    pub fn widen(&self, delta: &BigRational) -> CIval {
        let d = Interval::new(-delta.clone(), delta.clone());
        CIval {
            re: self.re.add(&d),
            im: self.im.add(&d),
        }
    }
}

pub type BoxedVec = [CIval; D];

pub fn enclose_exact_vec(e: &ExactVec, sb: &SqrtBox) -> BoxedVec {
    std::array::from_fn(|k| {
        let (re, im) = cyc24_real_imag_enclosure(&e[k], sb);
        CIval { re, im }
    })
}

pub fn enclose_canonical_triple(sb: &SqrtBox) -> Vec<BoxedVec> {
    canonical_triple_exact()
        .iter()
        .map(|e| enclose_exact_vec(e, sb))
        .collect()
}

pub fn widen_triple(triple: &[BoxedVec], delta: &BigRational) -> Vec<BoxedVec> {
    triple
        .iter()
        .map(|e| std::array::from_fn(|k| e[k].widen(delta)))
        .collect()
}

pub fn column_box_to_civals(vbox: &VectorBox) -> BoxedVec {
    std::array::from_fn(|k| CIval {
        re: vbox[2 * k].clone(),
        im: vbox[2 * k + 1].clone(),
    })
}

fn overlap_abs_sq(e: &BoxedVec, u: &BoxedVec) -> Interval {
    let mut re = Interval::point(BigRational::zero());
    let mut im = Interval::point(BigRational::zero());
    for k in 0..D {
        let c = e[k].conj();
        let x = &u[k].re;
        let y = &u[k].im;
        re = re.add(&c.re.mul(x).sub(&c.im.mul(y)));
        im = im.add(&c.re.mul(y).add(&c.im.mul(x)));
    }
    re.sq().add(&im.sq())
}

pub fn boxed_basis_residual_sq_lower(triple: &[BoxedVec], bbox: &BasisBox) -> BigRational {
    let sixth = Interval::point(BigRational::new(1.into(), 6.into()));
    let cols: Vec<BoxedVec> = bbox.iter().map(column_box_to_civals).collect();
    let mut total = BigRational::zero();
    for e in triple {
        for u in &cols {
            let mod_sq = overlap_abs_sq(e, u);
            let omega = mod_sq.sub(&sixth);
            total += omega.sq().lo();
        }
    }
    total
}

pub fn certify_moduli_box_excludes_fourth(
    triple: &[BoxedVec],
    bbox: &BasisBox,
) -> Option<BigRational> {
    let lower = boxed_basis_residual_sq_lower(triple, bbox);
    if lower > BigRational::zero() {
        Some(lower)
    } else {
        None
    }
}

pub fn certify_basis_moduli_box_excludes_fourth(
    delta: &BigRational,
    bbox: &BasisBox,
) -> Option<BigRational> {
    let sb = SqrtBox::standard();
    let triple = widen_triple(&enclose_canonical_triple(&sb), delta);
    certify_moduli_box_excludes_fourth(&triple, bbox)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::native::exact::mub6_interval_cover::VectorBox;

    use tfqm_number_theory::rational::rq;

    fn near_standard_vector(idx: usize) -> VectorBox {
        let small = Interval::new(rq(-1, 20), rq(1, 20));
        let mut vbox: VectorBox = std::array::from_fn(|_| small.clone());
        vbox[2 * idx] = Interval::new(rq(9, 10), rq(1, 1));
        vbox[2 * idx + 1] = small;
        vbox
    }

    fn basis_box_with_col0_near_e0() -> BasisBox {
        let wide = Interval::new(rq(-1, 1), rq(1, 1));
        let wide_col: VectorBox = std::array::from_fn(|_| wide.clone());
        let mut bbox: BasisBox = std::array::from_fn(|_| wide_col.clone());
        bbox[0] = near_standard_vector(0);
        bbox
    }

    #[test]
    fn per_column_decomposition_holds() {
        let sb = SqrtBox::standard();
        let columns = canonical_triple_exact();
        let bbox = basis_box_with_col0_near_e0();
        let whole = basis_residual_sq_lower(&columns, &bbox, &sb);
        let per_column: BigRational = bbox
            .iter()
            .map(|c| full_residual_sq_lower(&columns, c, &sb))
            .sum();
        assert_eq!(
            whole, per_column,
            "basis mass is the sum of the column masses"
        );
    }

    #[test]
    fn basis_box_with_one_bad_column_is_excluded() {
        let bbox = basis_box_with_col0_near_e0();
        let cert = certify_basis_box_excludes_fourth(&bbox)
            .expect("a basis whose first column is near e_0 cannot be a fourth MU basis");
        assert!(cert.psi_gap > BigRational::zero());
        let (j, gap) = basis_box_excluded_by_column(&bbox).expect("column 0 is vector-excluded");
        assert_eq!(j, 0);
        assert!(gap > BigRational::zero());
    }

    #[test]
    fn moduli_kernel_matches_exact_at_zero_widening() {
        let sb = SqrtBox::standard();
        let columns = canonical_triple_exact();
        let bbox = basis_box_with_col0_near_e0();
        let exact = basis_residual_sq_lower(&columns, &bbox, &sb);
        let triple = enclose_canonical_triple(&sb);
        let boxed = boxed_basis_residual_sq_lower(&triple, &bbox);
        assert_eq!(
            exact, boxed,
            "moduli kernel agrees with the exact kernel at zero widening"
        );
    }

    #[test]
    fn moduli_neighborhood_of_t0_still_excludes_a_bad_basis() {
        let sb = SqrtBox::standard();
        let triple = enclose_canonical_triple(&sb);
        let widened = widen_triple(&triple, &rq(1, 1000));
        let bbox = basis_box_with_col0_near_e0();
        let gap = certify_moduli_box_excludes_fourth(&widened, &bbox)
            .expect("the bad-column basis is excluded over the whole moduli neighborhood");
        assert!(gap > BigRational::zero());
    }

    #[test]
    fn basis_moduli_certify_excludes_bad_basis() {
        let gap =
            certify_basis_moduli_box_excludes_fourth(&rq(1, 1000), &basis_box_with_col0_near_e0())
                .expect("bad basis excluded over the whole moduli neighborhood at the basis level");
        assert!(gap > BigRational::zero());
    }

    #[test]
    fn basis_moduli_residual_is_a_sound_superset() {
        let sb = SqrtBox::standard();
        let base = enclose_canonical_triple(&sb);
        let widened = widen_triple(&base, &rq(1, 1000));
        let bbox = basis_box_with_col0_near_e0();
        assert!(
            boxed_basis_residual_sq_lower(&widened, &bbox)
                <= boxed_basis_residual_sq_lower(&base, &bbox),
            "widened basis mass is a sound lower bound (<= exact)"
        );
    }

    #[test]
    fn residual_length_is_18_by_6() {
        use crate::native::exact::d6_exact_curvature_cochain::COLUMN_COUNT;
        assert_eq!(COLUMN_COUNT, 18);
        assert_eq!(D, 6);
    }

    #[test]
    fn closed_box_spatial_bisections_guarantee_boundary_containment_and_zero_leakage() {
        let parent = Interval::new(rq(-5, 9), rq(7, 3));
        let (left, right) = bisect_closed_interval(&parent);
        assert!(verify_closed_box_bisection_soundness(
            &parent, &left, &right
        ));

        let vbox: VectorBox = std::array::from_fn(|i| {
            if i == 3 {
                Interval::new(rq(-2, 1), rq(4, 1))
            } else {
                Interval::new(rq(0, 1), rq(1, 1))
            }
        });
        let (va, vb) = bisect_closed_vector_box(&vbox);
        assert_eq!(va[3].hi(), vb[3].lo());
        assert!(va[3].contains(va[3].hi()));
        assert!(vb[3].contains(vb[3].lo()));
        assert_eq!(*va[3].hi(), rq(1, 1));

        for i in 0..2 * D {
            if i != 3 {
                assert_eq!(va[i], vbox[i]);
                assert_eq!(vb[i], vbox[i]);
            }
        }

        let mut bbox: BasisBox = std::array::from_fn(|_| vbox.clone());
        bbox[4][5] = Interval::new(rq(0, 1), rq(10, 1));
        let (ba, bb) = bisect_closed_basis_box(&bbox);
        assert_eq!(ba[4][5].hi(), bb[4][5].lo());
        assert_eq!(*ba[4][5].hi(), rq(5, 1));
        assert!(ba[4][5].contains(&rq(5, 1)));
        assert!(bb[4][5].contains(&rq(5, 1)));
        assert!(verify_closed_box_bisection_soundness(
            &bbox[4][5],
            &ba[4][5],
            &bb[4][5]
        ));
    }
}
