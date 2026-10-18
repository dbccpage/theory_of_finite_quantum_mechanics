
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Frac {
    pub num: i128,
    pub den: i128,
}

impl Frac {
    pub const fn new(num: i128, den: i128) -> Self {
        assert!(den != 0, "zero denominator");
        let sign = if den < 0 { -1 } else { 1 };
        let n = num * sign;
        let d = den * sign;
        let g = Self::gcd(n.unsigned_abs(), d.unsigned_abs()) as i128;
        Self {
            num: n / g,
            den: d / g,
        }
    }

    const fn gcd(mut a: u128, mut b: u128) -> u128 {
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

    pub const fn mul(self, other: Self) -> Self {
        Self::new(self.num * other.num, self.den * other.den)
    }

    pub const fn div(self, other: Self) -> Self {
        Self::new(self.num * other.den, self.den * other.num)
    }
}

pub fn lambda_1(r: Frac) -> Frac {
    let r2 = r.mul(r);
    let r4 = r2.mul(r2);
    let num = Frac::new(-1, 1).mul(r4);
    let factor1 = r.add(Frac::new(2, 1));
    let factor2 = r2.add(Frac::new(4, 1).mul(r)).add(Frac::new(8, 1));
    let den = Frac::new(4, 1).mul(factor1).mul(factor2);
    num.div(den)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Witness {
    pub r_at_192: Frac,
    pub lambda_1_at_1_192: Frac,
    pub poly_den_at_1_192: Frac,
    pub s1_constant: Frac,
    pub m1_constant: Frac,
    pub gate_e_quadratic: Frac,
}

pub fn witness() -> Witness {
    let r = Frac::new(1, 192);
    let r2 = r.mul(r);
    let r3 = r2.mul(r);
    let poly_den = Frac::new(64, 1)
        .add(Frac::new(64, 1).mul(r))
        .add(Frac::new(24, 1).mul(r2))
        .add(Frac::new(4, 1).mul(r3));
    let s1 = Frac::new(3, 43);
    let m1 = Frac::new(2 * 4096, 1).mul(s1);

    Witness {
        r_at_192: r,
        lambda_1_at_1_192: lambda_1(r),
        poly_den_at_1_192: poly_den,
        s1_constant: s1,
        m1_constant: m1,
        gate_e_quadratic: Frac::new(-1, 88305),
    }
}

pub fn reject_uniform_volume_promotion(claim: &str) -> Result<(), &'static str> {
    if claim.contains("uniform in L for G_M")
        || claim.contains("O.12 discharges Appendix W")
        || claim.contains("-1/87426958080 bounds all volumes")
    {
        Err("fixed L=4 one-period eigenvalue and O.12 Euclidean row-sum do not supply a uniform-in-L Trotter bound on G_M")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{ reject_uniform_volume_promotion, witness, Frac };

    #[test]
    fn lambda_1_at_1_192_and_m1_are_exact() {
        let w = witness();
        assert_eq!(w.lambda_1_at_1_192, Frac::new(-1, 87_426_958_080));
        assert_eq!(w.poly_den_at_1_192, Frac::new(455_348_740, 192 * 192 * 192));
        assert_eq!(w.m1_constant, Frac::new(24576, 43));
    }

    #[test]
    fn uniform_volume_promotions_are_refused() {
        assert!(reject_uniform_volume_promotion("uniform in L for G_M").is_err());
        assert!(reject_uniform_volume_promotion("O.12 discharges Appendix W").is_err());
    }
}
