//! MUB(6) moduli atlas — PIECE 1: the affine Fourier (Dita) chart `F6(x,y)`.
//!
//! The moduli-atlas packet (`mub6_moduli_atlas`) recorded PIECE 0 (a neighborhood of `T0`). This
//! module declares PIECE 1: a chart of a *different* street of the moduli — the two-parameter
//! affine family of 6x6 complex Hadamard matrices through the Fourier matrix. Declaring a chart is
//! the carrier-coordinate sub-step of the walk: we state the chart variables, the chart map, the
//! parameter domain, and the gauge — BEFORE running the (compute-heavy) cover over the box.
//!
//! ## The family (the Dita construction, exact over `Q(zeta_24)`)
//!
//! With `F3` the 3x3 Fourier matrix (`[F3]_{jk} = eta^{jk}`, `eta = e^{2pi i/3} = zeta_24^8`) and
//! `D = diag(1, e^{ix}, e^{iy})`, the chart map is the 6x6 (2x2 block of 3x3 blocks) matrix
//!
//! ```text
//!   F6(x,y) = (1/sqrt6) [ F3    D F3 ]
//!                       [ F3   -D F3 ]
//! ```
//!
//! `F6(x,y)` is a complex Hadamard matrix for **every** `(x,y)` — its columns are orthonormal and
//! every entry has modulus `1/sqrt6` (so it is unbiased to the standard basis). The orthogonality is
//! elementary and holds for all `D`:
//! * two left (or two right) columns `i, j`: `<.,.> = 2<F3_i, F3_j> = 2*3*delta_ij` (D is unitary);
//! * a left and a right column: `<F3_i, D F3_m> + <F3_i, -D F3_m> = 0`.
//!
//! At root-of-unity phases `e^{ix} = zeta_24^{dx}`, `e^{iy} = zeta_24^{dy}` every entry lives in
//! `Q(zeta_24)`, so the Hadamard property is checked as an EXACT `Cyc24` identity
//! (`f6_point_is_exact_chm`) — the oracle that pins this chart. A wrong chart map would fail it.
//!
//! ## What this charts (honest scope)
//!
//! `F6(x,y)` is the family of 6x6 CHMs = the MU PAIRS `{I, F6(x,y)/sqrt6}` (one basis unbiased to
//! the standard basis). The moduli of MU TRIPLES is the MU-compatible locus inside a PRODUCT of two
//! such CHM factors (`B2`, `B3` with `B2^dagger B3` also a CHM). This module is the single-factor
//! building block: the chart of one CHM factor. PIECE 1's cover step boxes the `(x,y)` parameters
//! into a `BoxedTriple` (via `mub6_basis_cover`) and runs the exact interval cover over it — that run,
//! and the triple-compatibility coordinate, are the next sub-steps, not done here.
//!
//! runs no cover, charts a 2-parameter slice (not the whole moduli), and mints no authority.

use serde::Serialize;

use crate::omega_native::exact::d6_exact_curvature_cochain::{abs_sq, inner, ExactVec, D};
use crate::omega_native::exact::mub6_field::inv_sqrt6;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// `F3` entry `(j,k) = eta^{jk}` with `eta = zeta_24^8 = e^{2pi i/3}`.
fn f3(j: usize, k: usize) -> Cyc24 {
    Cyc24::zeta24(((8 * j * k) % 24) as i32)
}

/// The affine Fourier (Dita) family `F6(x,y)` at root-of-unity phases `e^{ix} = zeta_24^{dx}`,
/// `e^{iy} = zeta_24^{dy}`, returned as the 6 normalized columns of `C^6`. Hadamard for ALL
/// `(dx, dy)` (see the module doc); `(dx, dy) = (0, 0)` is the plain Fourier matrix `F6`.
pub fn f6_family_columns(dx: i64, dy: i64) -> [ExactVec; D] {
    let s = inv_sqrt6();
    let dphase = [
        Cyc24::rat(ri(1)),
        Cyc24::zeta24(dx as i32),
        Cyc24::zeta24(dy as i32),
    ];
    std::array::from_fn(|col| {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        if col < 3 {
            // left block columns: rows 0..3 = F3[:,col], rows 3..6 = F3[:,col].
            for j in 0..3 {
                let e = f3(j, col).mul(&s);
                v[j] = e.clone();
                v[j + 3] = e;
            }
        } else {
            // right block columns: rows 0..3 = (D F3)[:,m], rows 3..6 = -(D F3)[:,m].
            let m = col - 3;
            for j in 0..3 {
                let e = dphase[j].mul(&f3(j, m)).mul(&s);
                v[j] = e.clone();
                v[j + 3] = e.neg();
            }
        }
        v
    })
}

/// EXACT oracle: `F6(dx,dy)` is a complex Hadamard matrix unbiased to the standard basis — every
/// entry has modulus^2 = 1/6, and the columns are orthonormal — all checked as `Cyc24` equalities.
/// This is the safety net pinning the chart map: a wrong family map fails it.
pub fn f6_point_is_exact_chm(dx: i64, dy: i64) -> bool {
    let cols = f6_family_columns(dx, dy);
    let target = Cyc24::rat(ri(1) / ri(D as i64));
    // unbiased to the standard basis: |<e_i, col_j>|^2 = |(col_j)_i|^2 = 1/6.
    for col in &cols {
        for entry in col {
            if abs_sq(entry) != target {
                return false;
            }
        }
    }
    // orthonormal columns: <col_i, col_j> = delta_ij.
    let one = Cyc24::rat(ri(1));
    let zero = Cyc24::zero();
    for i in 0..D {
        for j in 0..D {
            let ip = inner(&cols[i], &cols[j]);
            let want = if i == j { &one } else { &zero };
            if &ip != want {
                return false;
            }
        }
    }
    true
}

/// The declared PIECE-1 chart: carrier coordinates of the affine Fourier slice of the moduli.
#[derive(Debug, Clone, Serialize)]
pub struct F6Chart {
    pub chart_id: &'static str,
    pub family: &'static str,
    pub params: &'static str,
    /// Proven (and exactly test-verified): `F6(x,y)` is Hadamard for every `(x,y)`.
    pub hadamard_for_all_params: bool,
    /// Every entry has modulus^2 = 1/6 — the basis is unbiased to the standard basis.
    pub unbiased_to_standard: bool,
    pub charts: &'static str,
    pub cover_obligation: &'static str,
    pub firewall: &'static str,
}

/// Declare the PIECE-1 `F6(x,y)` chart. The Hadamard/unbiased flags are not assertions: they are
/// witnessed exactly by `f6_point_is_exact_chm` (the orthogonality proof is uniform in `(x,y)`).
pub fn declare_f6_chart() -> F6Chart {
    F6Chart {
        chart_id: "mub6-moduli-piece1-affine-fourier-F6",
        family: "Dita affine Fourier family F6(x,y) = (1/sqrt6)[[F3, D F3],[F3, -D F3]], D=diag(1,e^{ix},e^{iy})",
        params: "(x,y) phases; exact at e^{ix}=zeta_24^{dx}, e^{iy}=zeta_24^{dy}",
        hadamard_for_all_params: true,
        unbiased_to_standard: true,
        charts: "the 2-parameter affine Fourier slice of 6x6 CHMs = MU pairs {I, F6(x,y)/sqrt6}; one CHM factor of an MU triple",
        cover_obligation: "the no-go cover needs a TRIPLE; F6(x,y) is one CHM factor (B2). EXACT finding (f6_family_pair_is_mutually_unbiased): the family is internally NON-mutually-unbiased -- distinct members share their first 3 columns and have vanishing cross-block overlaps -- so NO MU triple lives inside it. A no-go cover requires a third basis B3 mutually unbiased to {I, F6(x,y)} from OUTSIDE the family (or a proof none exists); that external B3 is the gating coordinate before mub6_basis_cover can run over the (x,y) box",
        firewall: "declares a chart + proves it Hadamard exactly + records the exact self-non-MU finding (the interval cover is not yet runnable: no triple lives inside the family); charts a 2-parameter slice, NOT the whole moduli; stated region only; mints no authority",
    }
}

/// The exact cross-overlap `<B_i, B'_j>` between column `i` of `F6(dx,dy)` and column `j` of
/// `F6(dxp,dyp)` (normalized members), over `Q(zeta_24)`.
pub fn f6_cross_overlap(dx: i64, dy: i64, dxp: i64, dyp: i64, i: usize, j: usize) -> Cyc24 {
    let b = f6_family_columns(dx, dy);
    let bp = f6_family_columns(dxp, dyp);
    inner(&b[i], &bp[j])
}

/// EXACT structural finding (the honest result of trying to run the no-go cover over the F6 box):
/// the affine Fourier family is **internally non-mutually-unbiased**. Two members `F6(dx,dy)` and
/// `F6(dxp,dyp)` are never an MU pair: their left 3 columns are identical (the block `[F3; F3]` is
/// independent of the phases), and every cross-block overlap (`i < 3` xor `j < 3`) vanishes
/// exactly, so `|<B_i, B'_j>|^2 = 0 != 1/6`. Hence NO MU triple lives inside the family, and a
/// no-go cover over the F6 box requires a third basis from OUTSIDE it. Returns `true` only if the
/// two members are mutually unbiased (they are not, for any phases).
pub fn f6_family_pair_is_mutually_unbiased(dx: i64, dy: i64, dxp: i64, dyp: i64) -> bool {
    let b = f6_family_columns(dx, dy);
    let bp = f6_family_columns(dxp, dyp);
    let target = Cyc24::rat(ri(1) / ri(D as i64));
    for i in 0..D {
        for j in 0..D {
            if abs_sq(&inner(&b[i], &bp[j])) != target {
                return false;
            }
        }
    }
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn f6_base_point_is_exact_complex_hadamard() {
        // (0,0) is the plain Fourier matrix F6: an exact CHM unbiased to the standard basis.
        assert!(f6_point_is_exact_chm(0, 0));
    }

    #[test]
    fn f6_nontrivial_points_stay_exact_hadamard() {
        // a genuine 2-parameter deformation D = diag(1, eta, eta^2), eta = zeta_24^8:
        assert!(f6_point_is_exact_chm(8, 16));
        // arbitrary root-of-unity phases must also stay Hadamard (uniform orthogonality proof):
        assert!(f6_point_is_exact_chm(3, 7));
        assert!(f6_point_is_exact_chm(11, 23));
    }

    #[test]
    fn declared_chart_records_exactly_witnessed_properties() {
        let c = declare_f6_chart();
        assert!(c.hadamard_for_all_params && f6_point_is_exact_chm(5, 13));
        assert!(c.unbiased_to_standard);
        assert!(c.firewall.contains("NOT the whole moduli"));
        assert!(c.cover_obligation.contains("third basis B3"));
    }

    #[test]
    fn f6_family_is_internally_non_mu_so_no_triple_inside() {
        for (a, b, c, d) in [(0, 0, 8, 16), (3, 7, 11, 23), (0, 0, 5, 13)] {
            // distinct Fourier-family members are NEVER mutually unbiased:
            assert!(!f6_family_pair_is_mutually_unbiased(a, b, c, d));
            // exact witness 1: their first columns are identical (overlap 1, not 1/6):
            assert_eq!(f6_cross_overlap(a, b, c, d, 0, 0), Cyc24::rat(ri(1)));
            // exact witness 2: a cross-block overlap vanishes exactly (0, not 1/6):
            assert!(f6_cross_overlap(a, b, c, d, 0, 3).is_zero());
            assert!(f6_cross_overlap(a, b, c, d, 3, 0).is_zero());
        }
    }
}
