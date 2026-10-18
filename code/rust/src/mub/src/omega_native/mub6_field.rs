
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

pub fn sqrt6() -> Cyc24 {
    Cyc24::sqrt2().mul(&Cyc24::sqrt3())
}

pub fn inv_sqrt6() -> Cyc24 {
    sqrt6().mul(&Cyc24::rat(ri(1) / ri(6)))
}

pub fn omega3_pow(exp: i64) -> Cyc24 {
    Cyc24::zeta24((8 * exp.rem_euclid(3)).rem_euclid(24) as i32)
}

pub fn omega6_pow(exp: i64) -> Cyc24 {
    Cyc24::zeta24((4 * exp.rem_euclid(6)).rem_euclid(24) as i32)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sqrt_helpers_match_the_handwritten_cosine_sums() {
        let sqrt2 = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3));
        let sqrt3 = Cyc24::zeta24(2).add(&Cyc24::zeta24(-2));
        assert_eq!(Cyc24::sqrt2(), sqrt2);
        assert_eq!(Cyc24::sqrt3(), sqrt3);
        let handwritten = sqrt2.mul(&sqrt3).mul(&Cyc24::rat(ri(1) / ri(6)));
        assert_eq!(inv_sqrt6(), handwritten);
    }

    #[test]
    fn omega3_powers_agree_for_negative_exponents() {
        let direct = Cyc24::zeta24((8 * -1_i64).rem_euclid(24) as i32);
        assert_eq!(omega3_pow(-1), direct);
    }
}
