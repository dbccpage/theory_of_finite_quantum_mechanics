//! `omega_lie_theory` -- exact finite groups, Lie groups and Lie algebras.
//!
//! Every quantity is exact: rationals, cyclotomic and quadratic number fields. There is no
//! floating point and no tolerance; a computation that would need one is refused with a
//! typed error. Scalars come from `omega_number_theory`, matrices and elimination from
//! `linear_algebra`; this crate adds the group and Lie-algebra structure.
//!
//! - [`finite_group`]: Cayley tables, generation with a declared bound, conjugacy classes,
//!   the class equation, commuting pairs, quotients, flux and holonomy operators, and
//!   character tables over `Z[zeta_e]` (Dixon), with McKay matrices.
//! Character values use `omega_number_theory::cyclotomic_integer`, the canonical
//! integral cyclotomic ring for a runtime conductor.
//! - [`cayley`]: Cayley charts of `so(n)` over `Q` and of the unit circle of `Q(i)`.
//! - [`su2`]: quaternions, the adjoint cover `SU(2) -> SO(3)`, spinor norms and spin lifts,
//!   `sl(2)` spin representations, Clebsch-Gordan coefficients, the binary polyhedral groups.
//! - [`rotation`]: the finite subgroups `C_m`, `D_m`, `T`, `O`, `I` of `SO(3, K)`.
//! - [`lorentz`]: `SO+(1, d; Q)`: boosts, polar decomposition, Thomas-Wigner rotation,
//!   `SO+(1, 2; Q) = PGL(2, Q)`.
//! - [`finite_order`]: the exact decision whether a rational matrix has finite order.
//! - [`lie_algebra`]: structure constants, Jacobi, Killing form, Chevalley-Eilenberg cohomology.
//! - [`scalar`]: exact complex scalars (conjugation, `i`, `1/sqrt 2`) for the unitary
//!   constructions still to come.
//!
//! AuthorityEffect: None. Not PROVED. Not GlobalGreen.

extern crate self as omega_lie_theory;
pub mod cayley;
pub mod cayley_unitary;
pub mod clifford;
pub mod finite_group;
pub mod finite_groupoid_algebra;
pub mod finite_path_algebra;
pub mod twisted_abelian_algebra;
pub mod finite_order;
pub mod heisenberg;
pub mod lie_algebra;
pub mod lorentz;
pub mod pauli_symplectic;
pub mod rotation;
pub mod scalar;
pub mod su2;
pub mod su2_matrix;
pub mod su_n;

/// An exact rational matrix: the carrier of the constructions over `Q`.
pub(crate) type QMatrix =
    linear_algebra::backend::basic_matrix::BasicMatrix<num_rational::BigRational>;

pub mod weyl_operators;

use num_rational::Ratio;
use num_traits::Zero;

/// Verifies that a 2x2 matrix is traceless (sl_2 condition) over exact rationals.
pub fn is_sl2_traceless(a11: Ratio<i64>, a22: Ratio<i64>) -> bool {
    (a11 + a22).is_zero()
}

#[cfg(test)]
mod lie_tests {
    use super::*;

    #[test]
    fn test_sl2() {
        assert!(is_sl2_traceless(Ratio::new(3, 5), Ratio::new(-3, 5)));
        assert!(!is_sl2_traceless(Ratio::new(1, 2), Ratio::new(1, 2)));
    }
}
