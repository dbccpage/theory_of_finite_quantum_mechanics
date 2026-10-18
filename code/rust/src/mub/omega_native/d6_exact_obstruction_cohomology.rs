//! Exact obstruction cohomology `H^1 / H^2` of the MUB(6) tangent-obstruction complex,
//! over the native field `Q(zeta_24)`.
//!
//! Increment 3 of the real deformation algebra. It completes the three-term cochain
//! complex begun in [`super::d6_exact_tangent_obstruction`] and computes its cohomology
//! as exact integer dimensions over the field — the obstruction **class**, not a scalar.
//!
//! ```text
//!     C^0 = R^12  --d0=J-->  C^1 = R^18  --d1-->  C^2 = R^2
//! ```
//!
//! * `d0 = J` is the exact linearized-MU Jacobian (see the tangent module).
//! * `d1` is the **linearized Bianchi map**: the three per-basis curvature sums
//!   `sum_{i in B_b} omega_i` are all equal to `||v||^2 - 1`, so on linearized residuals
//!   their pairwise differences vanish. `d1(delta_omega) = (S_1 - S_2, S_1 - S_3)` with
//!   `S_b = sum_{i in B_b} delta_omega_i`. This is the closure datum of the cochain
//!   complex.
//!
//! Because every `delta_omega = J delta_v` has `S_1 = S_2 = S_3 = grad||v||^2 . delta_v`,
//! we have `d1 . d0 = 0` **exactly** (the Bianchi identity), verified term-by-term in
//! `Cyc24`. Hence
//!
//! ```text
//!     H^1 = ker(d1) / im(d0),    dim H^1 = (18 - rank d1) - rank d0,
//!     H^2 = C^2 / im(d1),        dim H^2 = 2 - rank d1.
//! ```
//!
//! `H^1` is the genuine first-order obstruction: curvature residual directions that are
//! **closed** (respect the Bianchi closure) but **not exact** (not achievable by deforming
//! `v`). Since `rank(d1) = 2` and `rank(d0) = rank(J) <= 11`, we get `dim H^1 >= 5` — a
//! deformation-invariant lower bound on the obstruction that the scalar `Phi_1` cannot see.
//!
//! exact obstruction cohomology of the *local* tangent complex at a single candidate
//! vector; the lift/repair algebra and the deformation-invariance across the Hadamard
//! family build on it (subsequent increments).

use crate::omega_native::exact::d6_exact_curvature_cochain::{ExactVec, BASIS_COUNT, COLUMN_COUNT, D};
use crate::omega_native::exact::d6_exact_tangent_obstruction::{
    curvature_jacobian, mat_vec, rank_cyc24, REAL_DIM,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// Dimension of `C^2 = R^{BASIS_COUNT - 1}` (the linearized-Bianchi target).
pub const C2_DIM: usize = BASIS_COUNT - 1;

/// The exact linearized Bianchi map `d1 : C^1 = R^18 -> C^2 = R^2`.
/// Row 0 = `(sum over B1) - (sum over B2)`; row 1 = `(sum over B1) - (sum over B3)`.
pub fn bianchi_d1() -> Vec<Vec<Cyc24>> {
    let one = Cyc24::rat(ri(1));
    let neg_one = one.neg();
    let mut row0 = vec![Cyc24::zero(); COLUMN_COUNT];
    let mut row1 = vec![Cyc24::zero(); COLUMN_COUNT];
    for i in 0..D {
        row0[i] = one.clone(); // B1
        row1[i] = one.clone();
    }
    for i in D..2 * D {
        row0[i] = neg_one.clone(); // B2
    }
    for i in 2 * D..3 * D {
        row1[i] = neg_one.clone(); // B3
    }
    vec![row0, row1]
}

/// Exact obstruction-cohomology dimensions of the tangent complex at `v`.
pub struct ObstructionCohomology {
    /// `rank(d0) = rank(J)` — first-order reachable curvature directions.
    pub d0_rank: usize,
    /// `rank(d1)` — the linearized-Bianchi rank (`= 2` when all three bases participate).
    pub d1_rank: usize,
    /// `dim H^1 = dim ker(d1) - rank(d0)` when im(d0) subset ker(d1); None if d1 . d0 != 0.
    pub h1_dim: Option<usize>,
    /// `dim H^2 = dim C^2 - rank(d1)`.
    pub h2_dim: usize,
    /// `true` iff `d1 . d0 = 0` was verified exactly (`im(d0) subset ker(d1)`).
    pub d1_after_d0_zero: bool,
}

/// Compute the exact obstruction cohomology of the local tangent complex at `v`.
pub fn obstruction_cohomology(columns: &[ExactVec], v: &ExactVec) -> ObstructionCohomology {
    let d0 = curvature_jacobian(columns, v); // 18 rows x 12 cols
    let d0_rank = rank_cyc24(&d0).expect("jacobian rows are rectangular");
    let d1 = bianchi_d1(); // 2 rows x 18 cols
    let d1_rank = rank_cyc24(&d1).expect("Bianchi rows are rectangular");

    // Verify im(d0) subset ker(d1): d1 applied to every column of d0 must vanish.
    // Column k of d0 is the image `d0 . e_k`; its span is im(d0).
    let mut d1_after_d0_zero = true;
    for k in 0..REAL_DIM {
        let col: Vec<Cyc24> = d0.iter().map(|row| row[k].clone()).collect();
        if !mat_vec(&d1, &col)
            .expect("Bianchi row width matches a jacobian column")
            .iter()
            .all(|z| z.is_zero())
        {
            d1_after_d0_zero = false;
            break;
        }
    }

    let ker_d1 = COLUMN_COUNT - d1_rank;
    let h1_dim = if d1_after_d0_zero {
        Some(ker_d1.saturating_sub(d0_rank))
    } else {
        None
    };
    ObstructionCohomology {
        d0_rank,
        d1_rank,
        h1_dim,
        h2_dim: C2_DIM - d1_rank,
        d1_after_d0_zero,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::canonical_triple_exact;

    fn rat(num: i64, den: i64) -> Cyc24 {
        Cyc24::rat(ri(num) / ri(den))
    }

    /// A generic exact unit vector `(1/sqrt2)(e_0 + i e_1)`.
    fn generic_unit() -> ExactVec {
        let s = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3)).mul(&rat(1, 2)); // 1/sqrt2
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = s.clone();
        v[1] = Cyc24::zeta24(6).mul(&s);
        v
    }

    #[test]
    fn bianchi_d1_has_rank_two() {
        assert_eq!(rank_cyc24(&bianchi_d1()).expect("rectangular"), 2);
    }

    #[test]
    fn d1_after_d0_is_exactly_zero() {
        // The Bianchi identity d1 . d0 = 0 must hold exactly at every candidate.
        let cols = canonical_triple_exact();
        let report = obstruction_cohomology(&cols, &generic_unit());
        assert!(
            report.d1_after_d0_zero,
            "linearized Bianchi identity d1 . d0 = 0 must hold exactly"
        );
    }

    #[test]
    fn obstruction_cohomology_is_well_formed_and_large() {
        let cols = canonical_triple_exact();
        let report = obstruction_cohomology(&cols, &generic_unit());
        assert_eq!(report.d1_rank, 2);
        assert_eq!(report.h2_dim, 0, "C^2 = R^2 is fully hit by d1");
        // dim H^1 = (18 - 2) - rank(J) = 16 - rank(J); rank(J) <= 11 => H^1 >= 5.
        assert!(
            report.d0_rank <= 11,
            "rank(J) = {} exceeds the tangent sphere",
            report.d0_rank
        );
        assert_eq!(
            report.h1_dim,
            Some(COLUMN_COUNT - report.d1_rank - report.d0_rank)
        );
        assert!(
            report.h1_dim.unwrap() >= 5,
            "obstruction cohomology H^1 = {:?} unexpectedly small",
            report.h1_dim
        );
    }

    #[test]
    fn invalid_chain_yields_none_h1() {
        // Multiply first column by 2, breaking MU orthogonality and Bianchi identity.
        let mut cols = canonical_triple_exact();
        for k in 0..6 {
            cols[0][k] = cols[0][k].mul(&rat(2, 1));
        }
        let report = obstruction_cohomology(&cols, &generic_unit());
        assert!(
            !report.d1_after_d0_zero,
            "d1 . d0 should not vanish on deformed columns"
        );
        assert_eq!(report.h1_dim, None, "H^1 must be None when d1 . d0 != 0");
    }
}
