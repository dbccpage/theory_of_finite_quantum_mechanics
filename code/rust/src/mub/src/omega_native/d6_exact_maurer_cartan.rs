//! Exact second-order Maurer-Cartan obstruction for the MUB(6) tangent complex, over the
//! native field `Q(zeta_24)`.
//!
//! Increment 5 of the real deformation algebra: the **quadratic bracket** and the
//! second-order (Kuranishi) obstruction that Codex/operator named — `MC(a) = d1 a +
//! (1/2)[a,a]`, the part the linear `d0` and the scalar `Phi_1` cannot express.
//!
//! Expand the curvature along a deformation `v -> v + delta_v` (exactly):
//!
//! ```text
//!   omega_i(v + delta_v) = omega_i(v) + (J . delta_v)_i + |<e_i, delta_v>|^2.
//! ```
//!
//! The quadratic term `Q_i(delta_v) = |<e_i, delta_v>|^2` is the Maurer-Cartan bracket
//! `(1/2)[delta_v, delta_v]` in `C^2`. If `delta_v` is a first-order repair
//! (`J . delta_v = -omega(v)`, the lift of increment 4), the residual at second order is
//! exactly `Q(delta_v)`, and the **Kuranishi obstruction** is its class
//! `Q(delta_v) mod im(d0)`: the deformation extends to second order iff `Q in im(d0)`.
//!
//! Two exact structural facts:
//! * **Parseval / Bianchi closure of the bracket:** `sum_{i in B_b} Q_i(delta_v) =
//!   ||delta_v||^2` for every basis `b` (each basis is orthonormal-complete), so
//!   `d1(Q) = 0` exactly — the MC term is Bianchi-closed, hence lives in the same
//!   `ker(d1)` as `im(d0)`; its obstruction is precisely its `H^1`-class.
//! * the second-order absorbability `Q in im(d0)` is decided exactly by the field solver.
//!
//! exact local MC obstruction; the global/deformation-invariance argument is the open
//! research increment.

use crate::omega_native::exact::d6_exact_curvature_cochain::{abs_sq, curvature_c2, inner, ExactVec, D};
use crate::omega_native::exact::d6_exact_lift_repair::solve_exact;
use crate::omega_native::exact::d6_exact_obstruction_cohomology::bianchi_d1;
use crate::omega_native::exact::d6_exact_tangent_obstruction::{
    curvature_jacobian, im, mat_vec, re, REAL_DIM,
};
use omega_number_theory::cyclotomic::Cyc24;

/// **The Maurer-Cartan quadratic bracket** `Q_i(delta_v) = |<e_i, delta_v>|^2`, exact.
/// This is the degree-2 (curvature) term of the deformation; it is real and nonnegative.
pub fn quadratic_bracket(columns: &[ExactVec], dv: &ExactVec) -> Vec<Cyc24> {
    columns.iter().map(|e| abs_sq(&inner(e, dv))).collect()
}

/// The exact second-order Maurer-Cartan obstruction at base point `v`, deformation `dv`.
pub struct SecondOrderObstruction {
    /// `Q(dv)` — the exact quadratic MC term in `C^2 = R^18`.
    pub bracket: Vec<Cyc24>,
    /// `true` iff `d1(Q) = 0` (the bracket is Bianchi-closed; Parseval), verified exactly.
    pub bianchi_closed: bool,
    /// `true` iff `Q in im(d0)` — a second-order correction absorbs the quadratic term.
    /// Note: image membership alone does not guarantee a formal curve extension without
    /// lower-order admissibility (J * dv == 0 or J * dv == -omega(v)).
    pub quadratic_in_jacobian_image: bool,
    /// `true` iff J dv == 0 and omega(v) == 0 (tangent to a zero).
    pub is_first_order_tangent: bool,
    /// `true` iff J dv == -omega(v) (first-order repair).
    pub is_first_order_repair: bool,
    /// `true` iff lower-order admissibility holds AND quadratic term is in jacobian image.
    pub formal_extension_valid: bool,
    /// Backward-compatible alias for quadratic image membership `Q in im(d0)`.
    pub second_order_absorbable: bool,
}

/// Compute the exact second-order MC obstruction for a deformation `dv` at `v`.
pub fn second_order_obstruction(
    columns: &[ExactVec],
    v: &ExactVec,
    dv: &ExactVec,
) -> SecondOrderObstruction {
    let q = quadratic_bracket(columns, dv);
    let bianchi_closed = mat_vec(&bianchi_d1(), &q)
        .expect("Bianchi row width matches the quadratic bracket")
        .iter()
        .all(|z| z.is_zero());
    let j = curvature_jacobian(columns, v);
    let neg_q: Vec<Cyc24> = q.iter().map(|x| x.neg()).collect();
    let quadratic_in_jacobian_image = matches!(solve_exact(&j, &neg_q), Ok(Some(_)));

    let omega = curvature_c2(columns, v);
    let neg_omega: Vec<Cyc24> = omega.iter().map(|w| w.neg()).collect();
    let mut dv_real = vec![Cyc24::zero(); REAL_DIM];
    for k in 0..D {
        dv_real[2 * k] = re(&dv[k]);
        dv_real[2 * k + 1] = im(&dv[k]);
    }
    let j_dv = mat_vec(&j, &dv_real).expect("jacobian row width matches the deformation");
    let is_first_order_tangent =
        j_dv.iter().all(|z| z.is_zero()) && omega.iter().all(|z| z.is_zero());
    let is_first_order_repair = j_dv == neg_omega;
    let formal_extension_valid =
        (is_first_order_tangent || is_first_order_repair) && quadratic_in_jacobian_image;

    SecondOrderObstruction {
        bracket: q,
        bianchi_closed,
        quadratic_in_jacobian_image,
        is_first_order_tangent,
        is_first_order_repair,
        formal_extension_valid,
        second_order_absorbable: quadratic_in_jacobian_image,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::{
        canonical_triple_exact, norm_sq, BASIS_COUNT, COLUMN_COUNT, D,
    };
    use omega_number_theory::rational::ri;

    fn rat(num: i64, den: i64) -> Cyc24 {
        Cyc24::rat(ri(num) / ri(den))
    }

    fn e0() -> ExactVec {
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = Cyc24::rat(ri(1));
        v
    }

    fn generic_unit() -> ExactVec {
        let s = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3)).mul(&rat(1, 2)); // 1/sqrt2
        let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
        v[0] = s.clone();
        v[1] = Cyc24::zeta24(6).mul(&s);
        v
    }

    #[test]
    fn quadratic_bracket_at_e0_has_known_values() {
        let cols = canonical_triple_exact();
        let q = quadratic_bracket(&cols, &e0());
        // B1: |<e_m, e_0>|^2 = delta_{m,0} => [1,0,0,0,0,0].
        assert_eq!(q[0], Cyc24::rat(ri(1)));
        for j in 1..D {
            assert!(q[j].is_zero());
        }
        // B2, B3: e_0 is unbiased => |<.,e_0>|^2 = 1/6.
        for i in D..COLUMN_COUNT {
            assert_eq!(q[i], rat(1, D as i64));
        }
    }

    #[test]
    fn bracket_respects_bianchi_via_parseval() {
        // sum_{i in B_b} Q_i(dv) = ||dv||^2 for every basis, so d1(Q) = 0 exactly.
        let cols = canonical_triple_exact();
        for dv in [e0(), generic_unit()] {
            let q = quadratic_bracket(&cols, &dv);
            let nsq = norm_sq(&dv);
            for b in 0..BASIS_COUNT {
                let mut s = Cyc24::zero();
                for j in 0..D {
                    s = s.add(&q[b * D + j]);
                }
                assert_eq!(
                    s, nsq,
                    "Parseval: per-basis bracket sum must equal ||dv||^2"
                );
            }
            // hence the bracket is Bianchi-closed.
            assert!(mat_vec(&bianchi_d1(), &q)
                .expect("rectangular")
                .iter()
                .all(|z| z.is_zero()));
        }
    }

    #[test]
    fn second_order_obstruction_is_well_formed_and_bianchi_closed() {
        let cols = canonical_triple_exact();
        let report = second_order_obstruction(&cols, &generic_unit(), &e0());
        assert_eq!(report.bracket.len(), COLUMN_COUNT);
        assert!(
            report.bianchi_closed,
            "the MC quadratic term is Bianchi-closed (Parseval)"
        );
        // absorbability is an exact boolean verdict; assert it is internally consistent
        // with the solver (re-derive it).
        let j = curvature_jacobian(&cols, &generic_unit());
        let neg_q: Vec<Cyc24> = report.bracket.iter().map(|x| x.neg()).collect();
        assert_eq!(
            report.second_order_absorbable,
            matches!(solve_exact(&j, &neg_q), Ok(Some(_)))
        );
    }
}
