//! Basis-level exact interval finite-cover certificates for MUB(6).
//!
//! `mub6_interval_cover` / `mub6_cyclotomic_enclosure` certify, per box and in exact rational
//! arithmetic, that no fourth mutually-unbiased **vector** lives in a region — the vector-level
//! `Phi_1` obstruction. This module lifts that certificate to the **basis-level `Psi_basis`**
//! obstruction: a candidate fourth basis is a full unitary `U in U(6)` whose six columns `U_j`
//! must EACH be mutually unbiased to the 18 fixed vectors `e_i` of the canonical triple
//! `T0 = {Z2(x)Z3, X2(x)Q0, Y2(x)Q1}`. The basis-extension residual is
//!
//! ```text
//!   omega_ij(U) = |<e_i, U_j>|^2 - 1/6        (i < 18 fixed vectors, j < 6 columns)
//! ```
//!
//! and the squared curvature mass is `Psi^sq(T, U) = sum_ij omega_ij^2`. A certified positive
//! lower bound on `Psi^sq` over a box of candidate bases proves **no fourth MU basis lives in
//! the box**. The Lean consume-target is `lean4/research_programs/mub6/FiniteBasisCover.lean`
//! (`no_fourth_basis_of_cover` / `psi_basis_pos_of_cover`), the basis-level analog of
//! `FiniteVectorCover.no_fourth_mu_vector_T0_of_cover`.
//!
//! ## Per-column decomposition (the key reduction)
//!
//! The basis-level squared mass factorizes over the columns:
//!
//! ```text
//!   Psi^sq(T, U) = sum_{j<6} sum_{i<18} omega_ij^2
//!                = sum_{j<6} [ sum_i (|<e_i, U_j>|^2 - 1/6)^2 ]
//!                = sum_{j<6} Phi^sq(T, U_j),
//! ```
//!
//! i.e. the basis mass is the **sum of the vector masses of the six columns**. So a certified
//! lower bound on the basis mass over a product box `[U_0-box, .., U_5-box]` is the sum of the
//! per-column vector lower bounds (`mub6_cyclotomic_enclosure::full_residual_sq_lower`), and
//! the basis box is excluded as soon as ANY single column box is vector-excluded. This makes
//! the basis-level cover **no harder than the vector-level cover** for a fixed triple, and
//! exposes the bound `Psi_basis(T) >= 6 * Phi_1(T)` (each column is a unit vector, so its
//! vector mass is at least the vector-level minimum) — so `Phi_1(T) > 0 => Psi_basis(T) > 0`.
//!
//! ## Moduli-aware kernel (the template for the open frontier)
//!
//! For the FIXED triple T0 the basis cover is implied by the (strictly stronger) vector cover.
//! The genuinely-open content is the cover over the **moduli of triples** — varying `T` over
//! the dephased complex-Hadamard slice (`MUB.TripleHadamardDephase`), where the fixed vectors
//! `e_i` are no longer constant. The `BoxedTriple` kernel below encloses the fixed vectors as
//! **complex intervals**, so the SAME certificate fires over a box of triples × a box of
//! candidate bases. It is exact (rational interval arithmetic) and certifies exclusion robustly
//! under moduli variation; producing a cover of the WHOLE dephased moduli slice over ALL
//! triples requires the open 6x6 complex-Hadamard classification (ENC-1147).
//!
//! certifies its own region; the moduli kernel certifies a triple-box × basis-box region.

use num_rational::BigRational;
use num_traits::Zero;

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::omega_native::exact::mub6_cyclotomic_enclosure::{
    cyc24_real_imag_enclosure, full_residual_sq_lower, SqrtBox,
};
use crate::omega_native::exact::mub6_interval_cover::VectorBox;
use omega_kernel::interval::Interval;

/// A box of candidate fourth bases: six independent candidate-column boxes `U_0..U_5`, each a
/// `VectorBox` (12 real-coordinate intervals `(x_0,y_0,..,x_5,y_5)`). The product is a box in
/// the real coordinates of `U(6)`; the within-basis orthonormality constraint is a separate
/// prune (a sound cover may certify a superset of the unitaries, which only helps the no-go).
pub type BasisBox = [VectorBox; D];

/// Certified lower bound on the basis-level squared curvature mass
/// `Psi^sq(T, U) = sum_j sum_i (|<e_i, U_j>|^2 - 1/6)^2` over the whole basis box, equal to the
/// sum of the six per-column vector lower bounds (`full_residual_sq_lower`).
pub fn basis_residual_sq_lower(columns: &[ExactVec], bbox: &BasisBox, sb: &SqrtBox) -> BigRational {
    let mut total = BigRational::zero();
    for col_box in bbox.iter() {
        total += full_residual_sq_lower(columns, col_box, sb);
    }
    total
}

/// A basis-level patch certificate: a basis box together with a certified positive lower bound
/// on `Psi^sq` proving no fourth MU basis lies in the box.
#[derive(Clone, Debug)]
pub struct NoBasisBox {
    pub bbox: BasisBox,
    /// Certified `Psi^sq(T, U) >= psi_gap > 0` for every candidate basis `U` in the box.
    pub psi_gap: BigRational,
}

/// Try to certify that no fourth MU basis lies in the basis box against an arbitrary fixed
/// triple (`columns`, typically 18 exact vectors). Returns the certified `Psi^sq` lower bound
/// if it is strictly positive over the box.
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

/// Try to certify that no fourth MU basis lies in the basis box (against the canonical triple
/// `T0`). Returns the certified `Psi^sq` lower bound if it is strictly positive over the box.
pub fn certify_basis_box_excludes_fourth(bbox: &BasisBox) -> Option<NoBasisBox> {
    certify_basis_box_excludes_fourth_for_triple(&canonical_triple_exact(), bbox)
}

/// Stronger single-column witness for the per-column decomposition against an arbitrary triple.
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

/// Stronger single-column witness for the per-column decomposition: if ANY one column box is
/// vector-excluded (its `Phi^sq` lower bound is positive), the whole basis box is excluded —
/// that column cannot be an MU vector, so `U` cannot be an MU basis. Returns the index of the
/// first excluded column and its certified vector gap.
pub fn basis_box_excluded_by_column(bbox: &BasisBox) -> Option<(usize, BigRational)> {
    basis_box_excluded_by_column_for_triple(&canonical_triple_exact(), bbox)
}

// ---------------------------------------------------------------------------------------------
// Closed-box spatial bisections: zero boundary leakage guarantee
// ---------------------------------------------------------------------------------------------

/// Closed-box spatial bisection of an interval `[lo, hi]` at midpoint `m = (lo + hi)/2`.
///
/// Invariance & Non-Leakage Contract:
/// 1. `left.lo == parent.lo` and `right.hi == parent.hi`.
/// 2. `left.hi == m` and `right.lo == m` (zero gap: `left.hi == right.lo`).
/// 3. Boundary containment: `m in left` and `m in right` (both closures contain the interface point).
/// 4. Union equality: `left U right == parent` with zero boundary leakage.
pub fn bisect_closed_interval(parent: &Interval) -> (Interval, Interval) {
    parent.bisect_closed()
}

/// Formally assert and verify closed-box boundary containment and zero boundary leakage.
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

/// Closed-box spatial bisection of a `VectorBox` (12 real intervals) at its widest coordinate.
///
/// Guarantees that the bisected coordinate splits into `[lo, m]` and `[m, hi]` with `m = (lo + hi)/2`.
/// All other 11 coordinates are identical closed intervals.
/// Zero boundary leakage: any point on the boundary interface belongs to both child closures.
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

/// Closed-box spatial bisection of a `BasisBox` (6 `VectorBox`es, 72 real coordinates).
///
/// Finds the widest coordinate across all 6 columns and bisects it into closed child intervals.
/// Guarantees zero boundary leakage: the boundary interface point is enclosed by both child closures.
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

// ---------------------------------------------------------------------------------------------
// Moduli-aware kernel: box the FIXED VECTORS (the triple's moduli) as complex intervals.
// ---------------------------------------------------------------------------------------------

/// A complex number enclosed as a pair of certified rational intervals `(re, im)`.
#[derive(Clone, Debug)]
pub struct CIval {
    pub re: Interval,
    pub im: Interval,
}

impl CIval {
    /// Complex conjugate `(re, -im)`.
    pub fn conj(&self) -> CIval {
        let zero = Interval::point(BigRational::zero());
        CIval {
            re: self.re.clone(),
            im: zero.sub(&self.im),
        }
    }

    /// Widen both the real and imaginary intervals by a nonnegative rational radius `delta`
    /// (models a neighborhood in the moduli of triples).
    pub fn widen(&self, delta: &BigRational) -> CIval {
        let d = Interval::new(-delta.clone(), delta.clone());
        CIval {
            re: self.re.add(&d),
            im: self.im.add(&d),
        }
    }
}

/// A fixed vector of the boxed triple, entries enclosed as complex intervals (so the triple's
/// moduli may vary over a box). For the canonical triple these are point/narrow enclosures of
/// the `Cyc24` entries; widening them models a neighborhood in the moduli of triples.
pub type BoxedVec = [CIval; D];

/// Enclose an exact `ExactVec` (`Cyc24` entries) as a `BoxedVec` via the certified cyclotomic
/// real/imag enclosure.
pub fn enclose_exact_vec(e: &ExactVec, sb: &SqrtBox) -> BoxedVec {
    std::array::from_fn(|k| {
        let (re, im) = cyc24_real_imag_enclosure(&e[k], sb);
        CIval { re, im }
    })
}

/// Enclose the whole canonical triple `T0` as boxed (complex-interval) fixed vectors.
pub fn enclose_canonical_triple(sb: &SqrtBox) -> Vec<BoxedVec> {
    canonical_triple_exact()
        .iter()
        .map(|e| enclose_exact_vec(e, sb))
        .collect()
}

/// Widen every entry of a boxed triple by `delta` — a moduli neighborhood of the triple.
pub fn widen_triple(triple: &[BoxedVec], delta: &BigRational) -> Vec<BoxedVec> {
    triple
        .iter()
        .map(|e| std::array::from_fn(|k| e[k].widen(delta)))
        .collect()
}

/// View a real-coordinate candidate-column box `(x_0,y_0,..,x_5,y_5)` as complex-interval
/// columns `(x_k + i y_k)`.
pub fn column_box_to_civals(vbox: &VectorBox) -> BoxedVec {
    std::array::from_fn(|k| CIval {
        re: vbox[2 * k].clone(),
        im: vbox[2 * k + 1].clone(),
    })
}

/// `|<e, u>|^2 = |sum_k conj(e_k) u_k|^2`, enclosed over the boxes.
fn overlap_abs_sq(e: &BoxedVec, u: &BoxedVec) -> Interval {
    let mut re = Interval::point(BigRational::zero());
    let mut im = Interval::point(BigRational::zero());
    for k in 0..D {
        let c = e[k].conj(); // conj(e_k) = (e.re, -e.im)
        let x = &u[k].re;
        let y = &u[k].im;
        // (c.re + i c.im)(x + i y) = (c.re x - c.im y) + i (c.re y + c.im x)
        re = re.add(&c.re.mul(x).sub(&c.im.mul(y)));
        im = im.add(&c.re.mul(y).add(&c.im.mul(x)));
    }
    re.sq().add(&im.sq())
}

/// Certified lower bound on the basis-level squared curvature mass
/// `sum_ij (|<e_i, U_j>|^2 - 1/6)^2` over a **boxed triple** (moduli interval) and a basis box.
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

/// Try to certify, over a boxed triple (moduli neighborhood) and a basis box, that no fourth MU
/// basis lies in the region. Returns the certified `Psi^sq` lower bound if strictly positive.
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

/// Certify, over the `delta`-neighborhood of the canonical triple `T0` (each fixed-vector entry
/// widened by `±delta`) and a basis box, that no fourth MU basis lies in the region — the
/// **basis-level** analog of `mub6_cover_run::run_moduli_cover`. A strictly positive `Psi^sq`
/// lower bound means no candidate basis in the box is a fourth MU basis for **any** triple within
/// `delta` of `T0`. This is the basis-level moduli certificate the Lean consume-target
/// `MUB.FiniteBasisCover.psi_basis_pos_over_family` assembles into `Psi_basis(e) > 0` on the
/// family.
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
    use crate::omega_native::exact::mub6_interval_cover::VectorBox;

    use omega_number_theory::rational::rq;

    /// A tight box concentrated near the standard basis vector `e_idx` (`x_idx ~ 1`, rest small).
    fn near_standard_vector(idx: usize) -> VectorBox {
        let small = Interval::new(rq(-1, 20), rq(1, 20)); // [-0.05, 0.05]
        let mut vbox: VectorBox = std::array::from_fn(|_| small.clone());
        vbox[2 * idx] = Interval::new(rq(9, 10), rq(1, 1)); // x_idx in [0.9, 1]
        vbox[2 * idx + 1] = small; // y_idx
        vbox
    }

    fn basis_box_with_col0_near_e0() -> BasisBox {
        // Column 0 concentrated near e_0 (clearly not MU to T0); other columns unconstrained
        // (full [-1,1] coordinate boxes) — the certificate must still fire on column 0 alone.
        let wide = Interval::new(rq(-1, 1), rq(1, 1));
        let wide_col: VectorBox = std::array::from_fn(|_| wide.clone());
        let mut bbox: BasisBox = std::array::from_fn(|_| wide_col.clone());
        bbox[0] = near_standard_vector(0);
        bbox
    }

    #[test]
    fn per_column_decomposition_holds() {
        // Psi^sq over the basis box = sum of the six per-column vector lower bounds.
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
        // The whole-basis certificate fires...
        let cert = certify_basis_box_excludes_fourth(&bbox)
            .expect("a basis whose first column is near e_0 cannot be a fourth MU basis");
        assert!(cert.psi_gap > BigRational::zero());
        // ...and the single-column witness pinpoints column 0.
        let (j, gap) = basis_box_excluded_by_column(&bbox).expect("column 0 is vector-excluded");
        assert_eq!(j, 0);
        assert!(gap > BigRational::zero());
    }

    #[test]
    fn moduli_kernel_matches_exact_at_zero_widening() {
        // At zero widening the boxed-triple kernel reproduces the exact cyclotomic-enclosure
        // basis mass bit-for-bit (both use the same `cyc24_real_imag_enclosure`).
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
        // Widen the triple by delta = 1/1000 (a genuine neighborhood in the moduli of triples).
        // A candidate basis whose first column sits near the FIXED standard vector e_0 stays
        // excluded across the whole moduli box, because B1 (the standard basis among the fixed
        // vectors) does not move under the moduli — a certified LOCAL moduli-cover step.
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
        // The delta-tied basis-level moduli certificate: a candidate basis whose first column is
        // near e_0 is excluded for ANY triple within delta = 1/1000 of T0 (the basis-level analog
        // of run_moduli_cover; what the Lean psi_basis_pos_over_family consumes).
        let gap =
            certify_basis_moduli_box_excludes_fourth(&rq(1, 1000), &basis_box_with_col0_near_e0())
                .expect("bad basis excluded over the whole moduli neighborhood at the basis level");
        assert!(gap > BigRational::zero());
    }

    #[test]
    fn basis_moduli_residual_is_a_sound_superset() {
        // Widening the triple can only widen the residual interval, so the moduli (widened) basis
        // mass lower bound is <= the exact T0 basis mass on any box — a sound superset test.
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
        use crate::omega_native::exact::d6_exact_curvature_cochain::COLUMN_COUNT;
        // Sanity: the basis residual ranges over 18 fixed vectors x 6 columns.
        assert_eq!(COLUMN_COUNT, 18);
        assert_eq!(D, 6);
    }

    #[test]
    fn closed_box_spatial_bisections_guarantee_boundary_containment_and_zero_leakage() {
        // Test interval bisection:
        let parent = Interval::new(rq(-5, 9), rq(7, 3));
        let (left, right) = bisect_closed_interval(&parent);
        assert!(verify_closed_box_bisection_soundness(
            &parent, &left, &right
        ));

        // Test VectorBox bisection:
        let vbox: VectorBox = std::array::from_fn(|i| {
            if i == 3 {
                Interval::new(rq(-2, 1), rq(4, 1)) // width = 6
            } else {
                Interval::new(rq(0, 1), rq(1, 1)) // width = 1
            }
        });
        let (va, vb) = bisect_closed_vector_box(&vbox);
        assert_eq!(va[3].hi(), vb[3].lo());
        assert!(va[3].contains(va[3].hi()));
        assert!(vb[3].contains(vb[3].lo()));
        assert_eq!(*va[3].hi(), rq(1, 1)); // mid of [-2, 4] is 1

        // Other coordinates untouched:
        for i in 0..2 * D {
            if i != 3 {
                assert_eq!(va[i], vbox[i]);
                assert_eq!(vb[i], vbox[i]);
            }
        }

        // Test BasisBox bisection:
        let mut bbox: BasisBox = std::array::from_fn(|_| vbox.clone());
        bbox[4][5] = Interval::new(rq(0, 1), rq(10, 1)); // widest: column 4, coordinate 5 (width 10)
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
