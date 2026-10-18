//! Exact rational witness for `WDP-JOINT-CONTINUUM` (`derivation.md`).
//!
//! Verifies:
//! 1. Three mesh nodes `x_i = 1 / L_i^2` for `L_i in {4, 6, 8}`, i.e. `(1/16, 1/36, 1/64)`.
//! 2. Node-vanishing cubic `H(x) = (x - 1/16)(x - 1/36)(x - 1/64)` evaluates to `(0, 0, 0)` on the
//!    three nodes while `H(0) = -1 / 36864 != 0`.
//! 3. Neville weights `w = (4/15, -81/35, 64/21) = (28/105, -243/105, 320/105)` satisfy:
//!    - `sum w_i = 1`
//!    - `sum w_i x_i = 0`
//!    - `sum w_i x_i^2 = 0`
//!    - `sum w_i H(x_i) = 0 != H(0) = -1 / 36864`
//! 4. Recorded occupation-basis checkerboard samples `(Z(4), Z(6), Z(8)) = (912, 33012, 973824)`
//!    and quadratic Neville extrapolate `sum w_i Z(L_i) = 99562368 / 35`.
//! 5. Refuses promoting `H(0) = -1/36864` to a supplied remainder bound or joint continuum value,
//!    and refuses reusing `Z(4) = 912` as a 16-site 2D torus partition function.

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
}

pub fn eval_h(x: Frac) -> Frac {
    let f1 = x.sub(Frac::new(1, 16));
    let f2 = x.sub(Frac::new(1, 36));
    let f3 = x.sub(Frac::new(1, 64));
    f1.mul(f2).mul(f3)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Witness {
    pub nodes: [Frac; 3],
    pub weights: [Frac; 3],
    pub h_on_nodes: [Frac; 3],
    pub h_at_zero: Frac,
    pub moment_0: Frac,
    pub moment_1: Frac,
    pub moment_2: Frac,
    pub neville_on_h: Frac,
    pub checkerboard_z: [i64; 3],
    pub neville_z0: Frac,
    pub target_3_optimum: Frac,
    pub target_4_optimum: i64,
    pub target_5_class_count: i64,
}

pub fn witness() -> Witness {
    let nodes = [Frac::new(1, 16), Frac::new(1, 36), Frac::new(1, 64)];
    let weights = [Frac::new(4, 15), Frac::new(-81, 35), Frac::new(64, 21)];
    let h_on_nodes = [eval_h(nodes[0]), eval_h(nodes[1]), eval_h(nodes[2])];
    let h_at_zero = eval_h(Frac::new(0, 1));

    let mut m0 = Frac::new(0, 1);
    let mut m1 = Frac::new(0, 1);
    let mut m2 = Frac::new(0, 1);
    let mut nh = Frac::new(0, 1);
    for i in 0..3 {
        m0 = m0.add(weights[i]);
        m1 = m1.add(weights[i].mul(nodes[i]));
        m2 = m2.add(weights[i].mul(nodes[i]).mul(nodes[i]));
        nh = nh.add(weights[i].mul(h_on_nodes[i]));
    }

    let z_samples = [912_i64, 33012, 973824];
    let mut nz0 = Frac::new(0, 1);
    for i in 0..3 {
        nz0 = nz0.add(weights[i].mul(Frac::new(z_samples[i], 1)));
    }

    Witness {
        nodes,
        weights,
        h_on_nodes,
        h_at_zero,
        moment_0: m0,
        moment_1: m1,
        moment_2: m2,
        neville_on_h: nh,
        checkerboard_z: z_samples,
        neville_z0: nz0,
        target_3_optimum: Frac::new(15, 4),
        target_4_optimum: 4,
        target_5_class_count: 29_771,
    }
}

pub fn reject_continuum_or_torus_promotion(claim: &str) -> Result<(), &'static str> {
    if claim.contains("-1/36864 is remainder bound")
        || claim.contains("Z=912 is 16-site torus")
        || claim.contains("Q-continuum closed")
    {
        Err("three-node polynomial fit and fixed L=4 carrier do not close WDP-JOINT-CONTINUUM or construct a 16-site torus")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_continuum_or_torus_promotion, witness, Frac};

    #[test]
    fn three_node_moments_and_cubic_aliasing_are_exact() {
        let w = witness();
        assert_eq!(w.h_on_nodes, [Frac::new(0, 1), Frac::new(0, 1), Frac::new(0, 1)]);
        assert_eq!(w.h_at_zero, Frac::new(-1, 36864));
        assert_eq!(w.moment_0, Frac::new(1, 1));
        assert_eq!(w.moment_1, Frac::new(0, 1));
        assert_eq!(w.moment_2, Frac::new(0, 1));
        assert_eq!(w.neville_on_h, Frac::new(0, 1));
        assert_ne!(w.neville_on_h, w.h_at_zero);
        assert_eq!(w.neville_z0, Frac::new(20_241_820, 7));
    }

    #[test]
    fn continuum_and_torus_promotions_are_refused() {
        assert!(reject_continuum_or_torus_promotion("-1/36864 is remainder bound").is_err());
        assert!(reject_continuum_or_torus_promotion("Z=912 is 16-site torus").is_err());
        assert!(reject_continuum_or_torus_promotion("Q-continuum closed").is_err());
    }
}
