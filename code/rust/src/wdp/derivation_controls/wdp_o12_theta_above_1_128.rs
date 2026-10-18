
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Frac {
    pub num: i64,
    pub den: i64,
}

impl Frac {
    pub const fn new(num: i64, den: i64) -> Self {
        assert!(den != 0, "zero denominator");
        let sign = if den < 0 { -1 } else { 1 };
        let n = num * sign;
        let d = den * sign;
        let g = Self::gcd(n.unsigned_abs(), d.unsigned_abs()) as i64;
        Self {
            num: n / g,
            den: d / g,
        }
    }

    const fn gcd(mut a: u64, mut b: u64) -> u64 {
        while b != 0 {
            let t = a % b;
            a = b;
            b = t;
        }
        if a == 0 { 1 } else { a }
    }

    pub const fn add(self, other: Self) -> Self {
        Self::new(self.num * other.den + other.num * self.den, self.den * other.den)
    }

    pub const fn sub(self, other: Self) -> Self {
        Self::new(self.num * other.den - other.num * self.den, self.den * other.den)
    }

    pub const fn mul(self, other: Self) -> Self {
        Self::new(self.num * other.num, self.den * other.den)
    }

    pub const fn pow(self, exp: u32) -> Self {
        let mut out = Self::new(1, 1);
        let mut i = 0;
        while i < exp {
            out = out.mul(self);
            i += 1;
        }
        out
    }
}

pub fn lift_error_bound(length: u32, theta: Frac) -> Result<Frac, &'static str> {
    if length < 4 || length % 2 != 0 {
        return Err("L must be even and >= 4");
    }
    let abs_num = theta.num.abs();
    if abs_num * 128 >= theta.den {
        return Err("lift_error_bound is undefined for |theta| >= 1/128");
    }
    let four_m1 = Frac::new(98304, 43);
    let base = Frac::new(128 * abs_num, theta.den);
    Ok(four_m1.mul(Frac::new(length as i64, 1)).mul(base.pow(length)))
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Witness {
    pub ratio_128_over_192: Frac,
    pub gap_128_minus_192: Frac,
    pub polymer_bond_label_norm: Frac,
    pub polymer_source_label_norm: Frac,
    pub image_ratio_at_128: Frac,
    pub geometric_wrap_tail: Frac,
    pub wrap_factor_total: Frac,
    pub wrap_margin_below_4: Frac,
    pub formal_endpoint_prefactor: Frac,
    pub formal_endpoint_l4: Frac,
    pub bound_at_l4_theta_1_192: Frac,
}

pub fn witness() -> Witness {
    let ratio_128_192 = Frac::new(128, 192);
    let gap = Frac::new(1, 128).sub(Frac::new(1, 192));
    let bond_norm = Frac::new(3, 4).mul(Frac::new(1, 96));
    let src_norm = Frac::new(1, 64).mul(Frac::new(1, 2));
    let img_ratio = Frac::new(96, 128);
    let r4 = img_ratio.pow(4);
    let denom = Frac::new(1, 1).sub(r4);
    let wrap_tail = Frac::new(2 * denom.den, denom.num);
    let wrap_total = Frac::new(1, 1).add(wrap_tail);
    let wrap_margin = Frac::new(4, 1).sub(wrap_total);
    let four_m1 = Frac::new(4 * 24576, 43);
    let formal_l4 = four_m1.mul(Frac::new(4, 1));
    let bound_192 = lift_error_bound(4, Frac::new(1, 192)).expect("valid at 1/192");

    Witness {
        ratio_128_over_192: ratio_128_192,
        gap_128_minus_192: gap,
        polymer_bond_label_norm: bond_norm,
        polymer_source_label_norm: src_norm,
        image_ratio_at_128: img_ratio,
        geometric_wrap_tail: wrap_tail,
        wrap_factor_total: wrap_total,
        wrap_margin_below_4: wrap_margin,
        formal_endpoint_prefactor: four_m1,
        formal_endpoint_l4: formal_l4,
        bound_at_l4_theta_1_192: bound_192,
    }
}

#[cfg(test)]
mod tests {
    use super::{lift_error_bound, witness, Frac};

    #[test]
    fn closed_disk_and_endpoint_ratios_are_exact() {
        let w = witness();
        assert_eq!(w.ratio_128_over_192, Frac::new(2, 3));
        assert_eq!(w.gap_128_minus_192, Frac::new(1, 384));
        assert_eq!(w.polymer_bond_label_norm, Frac::new(1, 128));
        assert_eq!(w.polymer_source_label_norm, Frac::new(1, 128));
        assert_eq!(w.image_ratio_at_128, Frac::new(3, 4));
        assert_eq!(w.geometric_wrap_tail, Frac::new(512, 175));
        assert_eq!(w.wrap_factor_total, Frac::new(687, 175));
        assert_eq!(w.wrap_margin_below_4, Frac::new(13, 175));
        assert_eq!(w.formal_endpoint_prefactor, Frac::new(98304, 43));
        assert_eq!(w.formal_endpoint_l4, Frac::new(393216, 43));
    }

    #[test]
    fn lift_error_bound_refuses_at_and_above_1_128() {
        assert!(lift_error_bound(10, Frac::new(1, 128)).is_err());
        assert!(lift_error_bound(10, Frac::new(1, 96)).is_err());
    }
}
