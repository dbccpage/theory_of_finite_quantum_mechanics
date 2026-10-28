

use crate::heisenberg::WeylHeisenberg;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use tfqm_number_theory::cyclotomic::{Cyc24, Cyc5};

fn system_d3() -> WeylHeisenberg<Cyc24> {
    WeylHeisenberg::new(3, Cyc24::zeta3()).expect("declared primitive third root")
}

fn system_d5() -> WeylHeisenberg<Cyc5> {
    WeylHeisenberg::new(5, Cyc5::zeta5(1)).expect("declared primitive fifth root")
}

pub fn weyl_x_d3() -> BasicMatrix<Cyc24> {
    system_d3().shift().expect("fixed 3 by 3 matrix")
}

pub fn weyl_z_d3() -> BasicMatrix<Cyc24> {
    system_d3().clock().expect("fixed 3 by 3 matrix")
}

pub fn weyl_parity_d3() -> BasicMatrix<Cyc24> {
    system_d3().parity().expect("fixed 3 by 3 matrix")
}

pub fn weyl_displacement_d3(a: i64, b: i64) -> BasicMatrix<Cyc24> {
    system_d3().displacement(a, b).expect("fixed 3 by 3 matrix")
}

pub fn weyl_x_d5() -> BasicMatrix<Cyc5> {
    system_d5().shift().expect("fixed 5 by 5 matrix")
}

pub fn weyl_z_d5() -> BasicMatrix<Cyc5> {
    system_d5().clock().expect("fixed 5 by 5 matrix")
}

pub fn weyl_parity_d5() -> BasicMatrix<Cyc5> {
    system_d5().parity().expect("fixed 5 by 5 matrix")
}

pub fn weyl_displacement_d5(q: i64, p: i64) -> BasicMatrix<Cyc5> {
    system_d5().displacement(q, p).expect("fixed 5 by 5 matrix")
}

#[cfg(test)]
mod tests {
    use super::*;
    use linear_algebra::exact_field::{involution, matrix as mx};
    use tfqm_number_theory::cyclotomic::GaussianRat;
    use tfqm_number_theory::rational::ri;

    #[test]
    fn test_d3_weyl_commutation_relation() {
        let x = weyl_x_d3();
        let z = weyl_z_d3();
        let zx = mx::multiply(&z, &x).unwrap();
        let xz = mx::multiply(&x, &z).unwrap();
        assert_eq!(zx, mx::scale(&xz, &Cyc24::zeta3()).unwrap());
    }

    #[test]
    fn test_d3_displacement_orthogonality() {
        for a in 0..3 {
            for b in 0..3 {
                let d = weyl_displacement_d3(a, b);
                let tr = mx::trace(&d).unwrap();
                assert_eq!(
                    tr,
                    if a == 0 && b == 0 {
                        Cyc24::from_int(3)
                    } else {
                        Cyc24::zero()
                    }
                );
            }
        }
    }

    #[test]
    fn test_d5_weyl_commutation_relation() {
        let x = weyl_x_d5();
        let z = weyl_z_d5();
        let zx = mx::multiply(&z, &x).unwrap();
        let xz = mx::multiply(&x, &z).unwrap();
        assert_eq!(zx, mx::scale(&xz, &Cyc5::zeta5(1)).unwrap());
    }

    #[test]
    fn test_d5_displacement_orthogonality() {
        for q in 0..5 {
            for p in 0..5 {
                let d = weyl_displacement_d5(q, p);
                let tr = mx::trace(&d).unwrap();
                assert_eq!(
                    tr,
                    if q == 0 && p == 0 {
                        Cyc5::rat(ri(5))
                    } else {
                        Cyc5::zero()
                    }
                );
            }
        }
    }

    #[test]
    fn test_rectangular_add_and_sub_keep_shape() {
        let a = mx::from_fn(2, 3, |r, c| ri((r * 3 + c) as i64)).unwrap();
        let b = mx::from_fn(2, 3, |_, _| ri(1)).unwrap();
        let sum = mx::add(&a, &b).unwrap();
        assert_eq!((sum.rows(), sum.cols()), (2, 3));
        assert_eq!(*sum.get_ref(1, 2).unwrap(), ri(6));
        assert_eq!(mx::sub(&sum, &b).unwrap(), a);
    }

    #[test]
    fn test_gaussian_rational_matrix_pauli_y() {
        let y = mx::from_rows(vec![
            vec![GaussianRat::zero(), GaussianRat::from_ints(0, -1)],
            vec![GaussianRat::from_ints(0, 1), GaussianRat::zero()],
        ])
        .unwrap();
        assert_eq!(involution::adjoint(&y).unwrap(), y);
        assert_eq!(mx::multiply(&y, &y).unwrap(), mx::identity(2).unwrap());
    }
}
