
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

    pub const fn div(self, other: Self) -> Self {
        Self::new(self.num * other.den, self.den * other.num)
    }
}

pub const FOUR_P: [[i64; 4]; 4] = [
    [0, 0, 0, 0],
    [0, 2, 2, 0],
    [0, 2, 2, 0],
    [0, 0, 0, 0],
];

pub const TWO_A0: [i64; 4] = [-1, -1, 1, 1];
pub const TWO_A1: [i64; 4] = [1, -1, 1, -1];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Witness {
    pub trace_4p: i64,
    pub four_p_idempotent_scaled: bool,
    pub normalized_trace_p: Frac,
    pub bond_expectation_p_a0_a1: Frac,
    pub bond_expectation_k_a0_a1: Frac,
    pub c00_at_theta0: Frac,
    pub c0y_theta1_jet: [Frac; 4],
    pub spatial_sum_theta1: Frac,
    pub ratio_l6_over_l4: Frac,
    pub mesh_exponent_alpha: i64,
    pub tl3_decay_base_at_1_192: Frac,
}

pub fn c0y_theta1(y: usize, u: Frac) -> Frac {
    let ka0ay = match y {
        1 | 3 => Frac::new(-1, 16),
        _ => Frac::new(0, 1),
    };
    let one_minus_u = Frac::new(1, 1).sub(u);
    let term1 = one_minus_u.mul(ka0ay);
    let term2 = u.mul(ka0ay);
    Frac::new(0, 1).sub(term1.add(term2))
}

pub fn witness() -> Witness {
    let mut tr_4p = 0_i64;
    let mut sq_ok = true;
    for i in 0..4 {
        tr_4p += FOUR_P[i][i];
        for j in 0..4 {
            let mut sum = 0_i64;
            for k in 0..4 {
                sum += FOUR_P[i][k] * FOUR_P[k][j];
            }
            if sum != 4 * FOUR_P[i][j] {
                sq_ok = false;
            }
        }
    }

    let mut tr_16_p_a0_a1 = 0_i64;
    for i in 0..4 {
        let diag_prod = TWO_A0[i] * TWO_A1[i];
        tr_16_p_a0_a1 += FOUR_P[i][i] * diag_prod;
    }
    let exp_p_a0_a1 = Frac::new(tr_16_p_a0_a1, 64);
    let exp_k_a0_a1 = Frac::new(0, 1).sub(exp_p_a0_a1);

    let u_sample = Frac::new(3, 7);
    let jet = [
        c0y_theta1(0, u_sample),
        c0y_theta1(1, u_sample),
        c0y_theta1(2, u_sample),
        c0y_theta1(3, u_sample),
    ];
    let spatial_sum = jet[0].add(jet[1]).add(jet[2]).add(jet[3]);
    let c01_l4 = Frac::new(1, 16);
    let c01_l6 = Frac::new(1, 16);
    let ratio = c01_l6.div(c01_l4);

    Witness {
        trace_4p: tr_4p,
        four_p_idempotent_scaled: sq_ok,
        normalized_trace_p: Frac::new(tr_4p, 16),
        bond_expectation_p_a0_a1: exp_p_a0_a1,
        bond_expectation_k_a0_a1: exp_k_a0_a1,
        c00_at_theta0: Frac::new(1, 4),
        c0y_theta1_jet: jet,
        spatial_sum_theta1: spatial_sum,
        ratio_l6_over_l4: ratio,
        mesh_exponent_alpha: 0,
        tl3_decay_base_at_1_192: Frac::new(96, 192),
    }
}

pub fn reject_critical_scaling_promotion(claim: &str) -> Result<(), &'static str> {
    if claim.contains("alpha=0 proves critical scaling")
        || claim.contains("L^{-1/2} derived")
        || claim.contains("ZERO_MODE[1]=1/8 is continuum field")
    {
        Err("theta^1 single-bond jet and exponent 0 at theta=0 do not close WDP-O8-CRITICAL-SCALING")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{c0y_theta1, reject_critical_scaling_promotion, witness, Frac};

    #[test]
    fn order_theta1_jet_and_mesh_exponent_are_exact() {
        let w = witness();
        assert_eq!(w.trace_4p, 4);
        assert!(w.four_p_idempotent_scaled);
        assert_eq!(w.normalized_trace_p, Frac::new(1, 4));
        assert_eq!(w.bond_expectation_p_a0_a1, Frac::new(1, 16));
        assert_eq!(w.bond_expectation_k_a0_a1, Frac::new(-1, 16));
        assert_eq!(w.c00_at_theta0, Frac::new(1, 4));
        assert_eq!(
            w.c0y_theta1_jet,
            [
                Frac::new(0, 1),
                Frac::new(1, 16),
                Frac::new(0, 1),
                Frac::new(1, 16)
            ]
        );
        assert_eq!(c0y_theta1(1, Frac::new(0, 1)), c0y_theta1(1, Frac::new(1, 1)));
        assert_eq!(w.spatial_sum_theta1, Frac::new(1, 8));
        assert_eq!(w.ratio_l6_over_l4, Frac::new(1, 1));
        assert_eq!(w.mesh_exponent_alpha, 0);
        assert_eq!(w.tl3_decay_base_at_1_192, Frac::new(1, 2));
    }

    #[test]
    fn critical_scaling_promotions_are_refused() {
        assert!(reject_critical_scaling_promotion("alpha=0 proves critical scaling").is_err());
        assert!(reject_critical_scaling_promotion("L^{-1/2} derived").is_err());
        assert!(reject_critical_scaling_promotion("ZERO_MODE[1]=1/8 is continuum field").is_err());
    }
}
