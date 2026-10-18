
use num_rational::BigRational;
use num_traits::Zero;

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::omega_native::exact::mub6_interval_cover::{NoVectorBox, VectorBox};
use omega_kernel::interval::Interval;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_number_theory::rational::rq;

pub fn sqrt_enclosure(n: i64, iters: u32) -> Interval {
    assert!(n >= 1, "sqrt_enclosure expects n >= 1");
    let target = ri(n);
    let mut lo = ri(1);
    let mut hi = ri(n);
    for _ in 0..iters {
        let mid = (&lo + &hi) / ri(2);
        if &mid * &mid <= target {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    Interval::new(lo, hi)
}

#[derive(Clone, Debug)]
pub struct SqrtBox {
    pub sqrt2: Interval,
    pub sqrt3: Interval,
    pub sqrt6: Interval,
}

impl SqrtBox {
    pub fn standard() -> Self {
        SqrtBox {
            sqrt2: sqrt_enclosure(2, 50),
            sqrt3: sqrt_enclosure(3, 50),
            sqrt6: sqrt_enclosure(6, 50),
        }
    }
}

fn cos_coeffs(k: usize) -> [BigRational; 4] {
    let z = BigRational::zero;
    match k {
        0 => [ri(1), z(), z(), z()],
        1 => [z(), rq(1, 4), z(), rq(1, 4)],
        2 => [z(), z(), rq(1, 2), z()],
        3 => [z(), rq(1, 2), z(), z()],
        4 => [rq(1, 2), z(), z(), z()],
        5 => [z(), rq(-1, 4), z(), rq(1, 4)],
        6 => [z(), z(), z(), z()],
        7 => [z(), rq(1, 4), z(), rq(-1, 4)],
        _ => unreachable!("Cyc24 reduced basis is k < 8"),
    }
}

fn sin_coeffs(k: usize) -> [BigRational; 4] {
    let z = BigRational::zero;
    match k {
        0 => [z(), z(), z(), z()],
        1 => [z(), rq(-1, 4), z(), rq(1, 4)],
        2 => [rq(1, 2), z(), z(), z()],
        3 => [z(), rq(1, 2), z(), z()],
        4 => [z(), z(), rq(1, 2), z()],
        5 => [z(), rq(1, 4), z(), rq(1, 4)],
        6 => [ri(1), z(), z(), z()],
        7 => [z(), rq(1, 4), z(), rq(1, 4)],
        _ => unreachable!("Cyc24 reduced basis is k < 8"),
    }
}

pub fn real_imag_decompose(z: &Cyc24) -> ([BigRational; 4], [BigRational; 4]) {
    let mut re = [
        BigRational::zero(),
        BigRational::zero(),
        BigRational::zero(),
        BigRational::zero(),
    ];
    let mut im = re.clone();
    for k in 0..8 {
        let a = &z.a[k];
        if a.is_zero() {
            continue;
        }
        let c = cos_coeffs(k);
        let s = sin_coeffs(k);
        for t in 0..4 {
            re[t] += a * &c[t];
            im[t] += a * &s[t];
        }
    }
    (re, im)
}

fn enclose_subfield(r: &[BigRational; 4], sb: &SqrtBox) -> Interval {
    Interval::point(r[0].clone())
        .add(&Interval::point(r[1].clone()).mul(&sb.sqrt2))
        .add(&Interval::point(r[2].clone()).mul(&sb.sqrt3))
        .add(&Interval::point(r[3].clone()).mul(&sb.sqrt6))
}

pub fn cyc24_real_imag_enclosure(z: &Cyc24, sb: &SqrtBox) -> (Interval, Interval) {
    let (re, im) = real_imag_decompose(z);
    (enclose_subfield(&re, sb), enclose_subfield(&im, sb))
}

fn column_residual_sq_lower(e: &ExactVec, vbox: &VectorBox, sb: &SqrtBox) -> BigRational {
    let mut re = Interval::point(BigRational::zero());
    let mut im = Interval::point(BigRational::zero());
    for k in 0..D {
        let c = e[k].conj();
        let (a, b) = cyc24_real_imag_enclosure(&c, sb);
        let x = &vbox[2 * k];
        let y = &vbox[2 * k + 1];
        re = re.add(&a.mul(x).sub(&b.mul(y)));
        im = im.add(&a.mul(y).add(&b.mul(x)));
    }
    let mod_sq = re.sq().add(&im.sq());
    let omega = mod_sq.sub(&Interval::point(rq(1, 6)));
    omega.sq().into_endpoints().0
}

pub fn full_residual_sq_lower(columns: &[ExactVec], vbox: &VectorBox, sb: &SqrtBox) -> BigRational {
    let mut total = BigRational::zero();
    for e in columns {
        total += column_residual_sq_lower(e, vbox, sb);
    }
    total
}

pub fn certify_box_excludes_mu_vector_full(vbox: &VectorBox) -> Option<NoVectorBox> {
    let sb = SqrtBox::standard();
    let columns = canonical_triple_exact();
    let lower = full_residual_sq_lower(&columns, vbox, &sb);
    if lower > BigRational::zero() {
        let f_gap = rq(6, 5) * lower;
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
    use crate::omega_native::exact::mub6_interval_cover::b1_residual_sq_lower;

    fn point_box(coords: [BigRational; 12]) -> VectorBox {
        coords.map(Interval::point)
    }

    #[test]
    fn sqrt_enclosures_are_sound_and_tight() {
        for &n in &[2i64, 3, 6] {
            let iv = sqrt_enclosure(n, 50);
            assert!(iv.lo() * iv.lo() <= ri(n), "lo^2 <= {n}");
            assert!(iv.hi() * iv.hi() >= ri(n), "hi^2 >= {n}");
            assert!(
                iv.hi() - iv.lo() < rq(1, 1_000_000_000_000),
                "width tight for {n}"
            );
        }
    }

    #[test]
    fn real_imag_decomposition_is_exact_over_cyc24() {
        let sq2c = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3));
        let sq3c = Cyc24::zeta24(2).add(&Cyc24::zeta24(-2));
        let sq6c = sq2c.mul(&sq3c);
        let i = Cyc24::zeta24(6);

        let rebuild = |r: &[BigRational; 4]| -> Cyc24 {
            Cyc24::rat(r[0].clone() * ri(2))
                .add(&Cyc24::rat(r[1].clone() * ri(2)).mul(&sq2c))
                .add(&Cyc24::rat(r[2].clone() * ri(2)).mul(&sq3c))
                .add(&Cyc24::rat(r[3].clone() * ri(2)).mul(&sq6c))
        };

        let mut samples: Vec<Cyc24> = (0..8).map(|k| Cyc24::zeta24(k)).collect();
        for e in canonical_triple_exact() {
            for c in e {
                samples.push(c);
            }
        }
        for z in &samples {
            let (re, im) = real_imag_decompose(z);
            assert_eq!(rebuild(&re), z.add(&z.conj()), "2 real(z) = z + conj(z)");
            assert_eq!(
                i.mul(&rebuild(&im)),
                z.sub(&z.conj()),
                "2 i imag(z) = z - conj(z)"
            );
        }
    }

    #[test]
    fn enclosure_contains_known_values() {
        let sb = SqrtBox::standard();
        let (re, im) = cyc24_real_imag_enclosure(&Cyc24::zeta24(2), &sb);
        assert!(
            re.lo() > &rq(866, 1000) && re.hi() < &rq(867, 1000),
            "real ~ 0.8660"
        );
        assert_eq!(im, Interval::point(rq(1, 2)), "imag = 1/2 exactly");
        let (re_i, im_i) = cyc24_real_imag_enclosure(&Cyc24::zeta24(6), &sb);
        assert_eq!(re_i, Interval::point(BigRational::zero()));
        assert_eq!(im_i, Interval::point(ri(1)));
    }

    #[test]
    fn full_residual_dominates_b1_and_certifies_e0() {
        let mut coords: [BigRational; 12] = std::array::from_fn(|_| BigRational::zero());
        coords[0] = ri(1);
        let vbox = point_box(coords);

        let b1 = b1_residual_sq_lower(&vbox);
        let sb = SqrtBox::standard();
        let full = full_residual_sq_lower(&canonical_triple_exact(), &vbox, &sb);

        assert_eq!(b1, rq(5, 6));
        assert!(
            full >= b1,
            "full obstruction dominates the B1 sub-certificate"
        );
        let cert = certify_box_excludes_mu_vector_full(&vbox).expect("e_0 box excluded");
        assert!(cert.f_gap > BigRational::zero());
    }

    #[test]
    fn full_residual_certifies_a_b1_unbiased_box() {
        let coord = Interval::new(rq(40, 100), rq(41, 100));
        let mut vbox: VectorBox = std::array::from_fn(|_| Interval::point(BigRational::zero()));
        for i in 0..6 {
            vbox[2 * i] = coord.clone();
        }
        assert!(
            b1_residual_sq_lower(&vbox) == BigRational::zero(),
            "B1 abstains on this box"
        );
        let sb = SqrtBox::standard();
        let full = full_residual_sq_lower(&canonical_triple_exact(), &vbox, &sb);
        assert!(
            full > BigRational::zero(),
            "full residual certifies where B1 abstains"
        );
    }
}
