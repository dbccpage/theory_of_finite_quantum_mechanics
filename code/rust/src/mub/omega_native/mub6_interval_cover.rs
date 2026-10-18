
use num_rational::BigRational;
use num_traits::Zero;
use omega_kernel::interval::Interval;
use omega_number_theory::rational::rq;

pub type VectorBox = [Interval; 12];

pub fn b1_residual_sq_lower(vbox: &VectorBox) -> BigRational {
    let sixth = Interval::point(rq(1, 6));
    let mut total = BigRational::zero();
    for i in 0..6 {
        let xi = &vbox[2 * i];
        let yi = &vbox[2 * i + 1];
        let mod_sq = xi.sq().add(&yi.sq());
        let omega = mod_sq.sub(&sixth);
        total += omega.sq().lo();
    }
    total
}

#[derive(Clone, Debug)]
pub struct NoVectorBox {
    pub vbox: VectorBox,
    pub f_gap: BigRational,
}

pub fn certify_box_excludes_mu_vector(vbox: &VectorBox) -> Option<NoVectorBox> {
    let b1_lower = b1_residual_sq_lower(vbox);
    if b1_lower > BigRational::zero() {
        let f_gap = rq(6, 5) * b1_lower;
        Some(NoVectorBox {
            vbox: vbox.clone(),
            f_gap,
        })
    } else {
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn iv(lo: (i64, i64), hi: (i64, i64)) -> Interval {
        Interval::new(rq(lo.0, lo.1), rq(hi.0, hi.1))
    }

    #[test]
    fn interval_arithmetic_is_exact() {
        assert_eq!(
            iv((1, 1), (2, 1)).add(&iv((3, 1), (4, 1))),
            iv((4, 1), (6, 1))
        );
        assert_eq!(
            iv((1, 1), (2, 1)).mul(&iv((3, 1), (4, 1))),
            iv((3, 1), (8, 1))
        );
        assert_eq!(iv((-1, 1), (2, 1)).sq(), iv((0, 1), (4, 1)));
        assert_eq!(iv((2, 1), (3, 1)).sq(), iv((4, 1), (9, 1)));
        assert_eq!(iv((-3, 1), (-2, 1)).sq(), iv((4, 1), (9, 1)));
    }

    fn small() -> Interval {
        iv((-1, 20), (1, 20))
    }

    #[test]
    fn box_near_e0_excludes_any_mu_vector() {
        let mut vbox: VectorBox = std::array::from_fn(|_| small());
        vbox[0] = iv((9, 10), (1, 1));
        let cert = certify_box_excludes_mu_vector(&vbox)
            .expect("a box near e_0 must exclude any MU vector");
        assert!(cert.f_gap > BigRational::zero());
    }

    #[test]
    fn box_at_an_unbiased_point_is_not_certified_by_b1_alone() {
        let coord = iv((40, 100), (41, 100));
        let mut vbox: VectorBox = std::array::from_fn(|_| Interval::point(BigRational::zero()));
        for i in 0..6 {
            vbox[2 * i] = coord.clone();
        }
        assert!(certify_box_excludes_mu_vector(&vbox).is_none());
    }

    #[test]
    fn test_closed_box_bisection_contains_boundary_with_zero_leakage() {
        let parent = iv((-3, 7), (11, 5));
        let (left, right) = parent.bisect_closed();

        assert_eq!(left.lo(), parent.lo());
        assert_eq!(right.hi(), parent.hi());
        assert_eq!(left.hi(), right.lo());

        let mid = left.hi();
        assert!(left.contains(mid));
        assert!(right.contains(mid));
        assert!(parent.contains(mid));

        let expected_mid = (parent.lo() + parent.hi()) / BigRational::from_integer(2.into());
        assert_eq!(*mid, expected_mid);
    }
}
