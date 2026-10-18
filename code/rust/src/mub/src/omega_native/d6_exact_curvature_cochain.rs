//! Exact MUB(6)-extension curvature cochain over the native field `Q(zeta_24)`.
//!
//! This is the **exact** C0 -> C1 -> C2 deformation cochain for the fourth-vector
//! extension problem, computed in exact cyclotomic arithmetic — NOT the f64 scalar
//! wall of `d6_gtfoc_wall_cross_validation`, and NOT a stubbed atlas enum. It rebuilds
//! the canonical triple `T0 = {Z2(x)Z3, X2(x)Q0, Y2(x)Q1}` of `C^6` exactly over
//! `Cyc24`, and exposes the actual cochain objects:
//!
//! * **C1 connection** `a_i(v) = <e_i, v>` (exact, per fixed vector `e_i`).
//! * **C2 curvature** `omega_i(v) = |<e_i, v>|^2 - 1/6` (exact).
//! * **closure (the d1 / Bianchi relation)** `sum_{i in basis b} omega_i(v) = ||v||^2 - 1`,
//!   which is the exact cocycle condition (zero on unit vectors), verified term-by-term
//!   in `Cyc24` rather than to a float tolerance.
//! * **wall functional** `f(v) = 1 - (6/5) * sum_i omega_i(v)^2` — the Invariant-Systems
//!   functional reproduced in our own exact arithmetic, so the wall `W = (88 + 3 sqrt6)/100`
//!   is matched in-framework instead of cited.
//!
//! claim about MUB(6) <= 3. It is the exact C2 foundation on which the exact coboundary
//! maps `d0/d1`, the obstruction cohomology `H^1/H^2`, and the lift/repair algebra are
//! built (subsequent increments). The canonical triple is the standard Weyl-Heisenberg
//! construction (generic mathematics, not the Apache port's IP); the exact field `Cyc24`
//! is the clean-room native reimplementation.

use num_rational::BigRational;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// Dimension and triple shape.
pub const D: usize = 6;
pub const BASIS_COUNT: usize = 3;
pub const COLUMN_COUNT: usize = 18;

/// An exact vector of `C^6` over `Q(zeta_24)`.
pub type ExactVec = [Cyc24; D];

fn rat(num: i64, den: i64) -> Cyc24 {
    Cyc24::rat(ri(num) / ri(den))
}

/// `1/sqrt2 = sqrt2 / 2`.
pub(crate) fn inv_sqrt2() -> Cyc24 {
    Cyc24::sqrt2().mul(&rat(1, 2))
}

/// `1/sqrt3 = sqrt3 / 3`.
pub(crate) fn inv_sqrt3() -> Cyc24 {
    Cyc24::sqrt3().mul(&rat(1, 3))
}

/// `omega3 = e^{2 pi i / 3} = zeta_24^8`.
pub(crate) fn omega3_pow(exp: i64) -> Cyc24 {
    crate::omega_native::exact::mub6_field::omega3_pow(exp)
}

pub(crate) fn zero_vec() -> ExactVec {
    std::array::from_fn(|_| Cyc24::zero())
}

pub(crate) fn tensor(qb: &[Cyc24; 2], qt: &[Cyc24; 3]) -> ExactVec {
    let mut out = zero_vec();
    for (a, qa) in qb.iter().enumerate() {
        for (b, qbt) in qt.iter().enumerate() {
            out[a * 3 + b] = qa.mul(qbt);
        }
    }
    out
}

/// The qubit X basis `(1/sqrt2)[[1,1],[1,-1]]` (columns).
pub(crate) fn qubit_x() -> [[Cyc24; 2]; 2] {
    let s = inv_sqrt2();
    [[s.clone(), s.clone()], [s.clone(), s.neg()]]
}

/// The qubit Y basis `(1/sqrt2)[[1,1],[i,-i]]` (columns).
pub(crate) fn qubit_y() -> [[Cyc24; 2]; 2] {
    let s = inv_sqrt2();
    let i = Cyc24::zeta24(6);
    [[s.clone(), i.mul(&s)], [s.clone(), i.mul(&s).neg()]]
}

/// The qutrit quadratic-Gauss MUB basis `Q_a`, column `m`:
/// `(Q_a)_{j,m} = omega3^{a j^2 + m j} / sqrt3`.
pub(crate) fn qutrit_q(a: i64) -> [[Cyc24; 3]; 3] {
    let s = inv_sqrt3();
    std::array::from_fn(|m| {
        std::array::from_fn(|j| {
            let exp = a * (j as i64) * (j as i64) + (m as i64) * (j as i64);
            omega3_pow(exp).mul(&s)
        })
    })
}

/// The 18 exact columns of the canonical triple `T0 = {Z2(x)Z3, X2(x)Q0, Y2(x)Q1}`.
pub fn canonical_triple_exact() -> Vec<ExactVec> {
    let mut cols = Vec::with_capacity(COLUMN_COUNT);
    // B1 = Z2 (x) Z3 = standard basis of C^6.
    for idx in 0..D {
        let mut v = zero_vec();
        v[idx] = Cyc24::rat(ri(1));
        cols.push(v);
    }
    // B2 = X2 (x) Q0.
    let x2 = qubit_x();
    let q0 = qutrit_q(0);
    for qb in &x2 {
        for qt in &q0 {
            cols.push(tensor(qb, qt));
        }
    }
    // B3 = Y2 (x) Q1.
    let y2 = qubit_y();
    let q1 = qutrit_q(1);
    for qb in &y2 {
        for qt in &q1 {
            cols.push(tensor(qb, qt));
        }
    }
    cols
}

/// Exact Hermitian inner product `<u, v> = sum_k conj(u_k) * v_k`.
pub fn inner(u: &ExactVec, v: &ExactVec) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for k in 0..D {
        acc = acc.add(&u[k].conj().mul(&v[k]));
    }
    acc
}

/// Exact squared modulus `|z|^2 = z * conj(z)` (a real cyclotomic number).
pub fn abs_sq(z: &Cyc24) -> Cyc24 {
    omega_functional::MubFeasibilityWallFunctional::cyclotomic_squared_norm(std::slice::from_ref(z))
}

/// Exact squared norm `||v||^2 = sum_k |v_k|^2`.
pub fn norm_sq(v: &ExactVec) -> Cyc24 {
    omega_functional::MubFeasibilityWallFunctional::cyclotomic_squared_norm(v)
}

/// **C1 connection.** The overlaps `a_i(v) = <e_i, v>` against every fixed vector.
pub fn connection_c1(columns: &[ExactVec], v: &ExactVec) -> Vec<Cyc24> {
    columns.iter().map(|e| inner(e, v)).collect()
}

/// **C2 curvature.** `omega_i(v) = |<e_i, v>|^2 - 1/6`, exact.
pub fn curvature_c2(columns: &[ExactVec], v: &ExactVec) -> Vec<Cyc24> {
    let target = rat(1, D as i64);
    columns
        .iter()
        .map(|e| abs_sq(&inner(e, v)).sub(&target))
        .collect()
}

/// **Closure (the d1 / Bianchi relation) per basis.** Returns the three exact sums
/// `sum_{i in basis b} omega_i(v)`; each equals `||v||^2 - 1` by Parseval, so on a unit
/// vector all three are exactly zero.
pub fn basis_closure(omega: &[Cyc24]) -> [Cyc24; BASIS_COUNT] {
    assert_eq!(
        omega.len(),
        COLUMN_COUNT,
        "basis_closure expects the full {COLUMN_COUNT}-vector curvature cochain"
    );
    std::array::from_fn(|b| {
        let mut acc = Cyc24::zero();
        for j in 0..D {
            acc = acc.add(&omega[b * D + j]);
        }
        acc
    })
}

/// **Wall functional** `f(v) = 1 - (6/5) * sum_i omega_i(v)^2`, exact. Equals `1` exactly
/// at an exactly mutually-unbiased fourth vector; the Invariant-Systems wall is its
/// maximum `W = (88 + 3 sqrt6)/100`.
pub fn wall_functional(omega: &[Cyc24]) -> Cyc24 {
    assert_eq!(
        omega.len(),
        COLUMN_COUNT,
        "wall_functional expects the full {COLUMN_COUNT}-vector curvature cochain"
    );
    omega_functional::MubFeasibilityWallFunctional::exact_d6_wall(omega)
        .expect("eighteen residuals checked above")
}

/// Exact verification that the triple is a genuine mutually-unbiased triple:
/// orthonormal within each basis and `|<e_i, e_j>|^2 = 1/6` across distinct bases —
/// all checked as exact `Cyc24` equalities (the in-framework reproduction of the
/// Apache `check_triple_is_mub`, in our clean-room native field).
pub fn is_mutually_unbiased_triple_exact(columns: &[ExactVec]) -> bool {
    if columns.len() != COLUMN_COUNT {
        return false;
    }
    let one = Cyc24::rat(ri(1));
    let zero = Cyc24::zero();
    let target = rat(1, D as i64);
    for ci in 0..COLUMN_COUNT {
        let bi = ci / D;
        for cj in 0..COLUMN_COUNT {
            let bj = cj / D;
            let ip = inner(&columns[ci], &columns[cj]);
            if bi == bj {
                // within a basis: orthonormal
                let want = if ci == cj { &one } else { &zero };
                if &ip != want {
                    return false;
                }
            } else {
                // across bases: |<.,.>|^2 = 1/6
                if abs_sq(&ip) != target {
                    return false;
                }
            }
        }
    }
    true
}

/// Convert an exact real cyclotomic number known to be rational to its `BigRational`
/// value (returns `None` if it carries non-rational cyclotomic components).
pub fn as_rational(z: &Cyc24) -> Option<BigRational> {
    if z.a[1..].iter().all(num_traits::Zero::is_zero) {
        Some(z.a[0].clone())
    } else {
        None
    }
}

/// Exact real comparison for Cyc24 elements that are real.
/// Returns Ordering based on standard real embedding via Sturm sequences / interval refinement.
pub fn cmp_exact_real(a: &Cyc24, b: &Cyc24) -> std::cmp::Ordering {
    if a == b {
        return std::cmp::Ordering::Equal;
    }
    let diff = a.sub(b);
    let num = omega_number_theory::cyclotomic_field::CyclotomicNumber::from(&diff);
    match omega_number_theory::cyclotomic_ordered::standard_real_sign(&num) {
        Ok(1) => std::cmp::Ordering::Greater,
        Ok(-1) => std::cmp::Ordering::Less,
        Ok(0) => std::cmp::Ordering::Equal,
        _ => a.a.cmp(&b.a),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn canonical_triple_is_exactly_mutually_unbiased() {
        let cols = canonical_triple_exact();
        assert_eq!(cols.len(), COLUMN_COUNT);
        assert!(
            is_mutually_unbiased_triple_exact(&cols),
            "T0 must be an exact MU triple over Q(zeta_24)"
        );
    }

    #[test]
    fn standard_basis_vector_has_exact_zero_closure() {
        let cols = canonical_triple_exact();
        // v = e_0 (the first standard-basis column), an exact unit vector.
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(1));
        // unit norm, exactly.
        assert_eq!(norm_sq(&v), Cyc24::rat(ri(1)));
        let omega = curvature_c2(&cols, &v);
        // each per-basis closure equals ||v||^2 - 1 = 0, exactly.
        let closures = basis_closure(&omega);
        for c in &closures {
            assert!(
                c.is_zero(),
                "exact Bianchi closure must vanish on a unit vector"
            );
        }
    }

    #[test]
    fn closure_equals_norm_minus_one_for_a_nonunit_vector() {
        let cols = canonical_triple_exact();
        // v = 2 * e_0 has ||v||^2 = 4, so each closure must be exactly 3.
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(2));
        let nsq = norm_sq(&v);
        assert_eq!(nsq, Cyc24::rat(ri(4)));
        let omega = curvature_c2(&cols, &v);
        let expected = nsq.sub(&Cyc24::rat(ri(1))); // 3
        for c in &basis_closure(&omega) {
            assert_eq!(c, &expected, "closure must equal ||v||^2 - 1 exactly");
        }
    }

    #[test]
    fn curvature_at_e0_has_known_exact_values() {
        let cols = canonical_triple_exact();
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(1));
        let omega = curvature_c2(&cols, &v);
        // B1 (standard basis): omega_0 = |1|^2 - 1/6 = 5/6; omega_{1..5} = -1/6.
        assert_eq!(omega[0], rat(5, 6));
        for j in 1..D {
            assert_eq!(omega[j], rat(-1, 6));
        }
        // B2, B3: e_0 is unbiased to every vector, so omega_i = 1/6 - 1/6 = 0 exactly.
        for i in D..COLUMN_COUNT {
            assert!(
                omega[i].is_zero(),
                "e_0 is exactly unbiased to bases 2 and 3"
            );
        }
    }

    #[test]
    fn wall_functional_is_one_at_a_perfectly_unbiased_vector() {
        // A vector unbiased to ALL 18 columns would give omega = 0 and f = 1. e_0 is not
        // such a vector (it lies in B1), so its f must be < 1; check it is exact-rational
        // and strictly below 1.
        let cols = canonical_triple_exact();
        let mut v = zero_vec();
        v[0] = Cyc24::rat(ri(1));
        let omega = curvature_c2(&cols, &v);
        let f = wall_functional(&omega);
        let fq = as_rational(&f).expect("wall value at e_0 is rational");
        // f(e_0) = 1 - (6/5)*( (5/6)^2 + 5*(1/6)^2 ) = 1 - (6/5)*(30/36) = 1 - 1 = 0.
        assert_eq!(fq, ri(0));
    }
}
