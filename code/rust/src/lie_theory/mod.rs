
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

pub(crate) type QMatrix =
    linear_algebra::backend::basic_matrix::BasicMatrix<num_rational::BigRational>;

pub mod weyl_operators;

use num_rational::Ratio;
use num_traits::Zero;

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
