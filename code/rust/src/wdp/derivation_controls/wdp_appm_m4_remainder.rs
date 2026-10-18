
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Rational {
    pub num: i64,
    pub den: i64,
}

impl Rational {
    pub fn new(num: i64, den: i64) -> Self {
        Self::reduced(i128::from(num), i128::from(den))
    }

    fn reduced(mut num: i128, mut den: i128) -> Self {
        assert!(den != 0, "rational denominator is zero");
        if den < 0 {
            num = -num;
            den = -den;
        }
        let g = gcd(num.abs(), den);
        num /= g;
        den /= g;
        assert!(num <= i128::from(i64::MAX) && num >= i128::from(i64::MIN));
        assert!(den <= i128::from(i64::MAX));
        Self {
            num: num as i64,
            den: den as i64,
        }
    }

    pub fn zero() -> Self {
        Self::new(0, 1)
    }

    pub fn add(self, other: Self) -> Self {
        Self::reduced(
            i128::from(self.num) * i128::from(other.den) + i128::from(other.num) * i128::from(self.den),
            i128::from(self.den) * i128::from(other.den),
        )
    }

    pub fn sub(self, other: Self) -> Self {
        self.add(other.neg())
    }

    pub fn mul(self, other: Self) -> Self {
        Self::reduced(
            i128::from(self.num) * i128::from(other.num),
            i128::from(self.den) * i128::from(other.den),
        )
    }

    pub fn neg(self) -> Self {
        Self::new(-self.num, self.den)
    }

    pub fn abs(self) -> Self {
        if self.num < 0 { self.neg() } else { self }
    }

    pub fn div(self, other: Self) -> Self {
        assert!(other.num != 0, "rational division by zero");
        self.mul(Self::new(other.den, other.num))
    }

    pub fn cmp_ord(self, other: Self) -> i8 {
        let left = i128::from(self.num) * i128::from(other.den);
        let right = i128::from(other.num) * i128::from(self.den);
        if left < right {
            -1
        } else if left > right {
            1
        } else {
            0
        }
    }

    pub fn ge(self, other: Self) -> bool {
        self.cmp_ord(other) >= 0
    }
}

fn gcd(mut a: i128, mut b: i128) -> i128 {
    while b != 0 {
        let rest = a % b;
        a = b;
        b = rest;
    }
    a
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub repetitions: i64,
    pub q: i64,
    pub lengths: [i64; 3],
    pub occupation_states: [i64; 3],
    pub occupation_traces: [i64; 3],
    pub nodes: [Rational; 3],
    pub weights: [Rational; 3],
    pub moments: [Rational; 3],
    pub h_at_zero: Rational,
    pub absolute_weight_sum: Rational,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Extrapolation {
    pub hat_f: Rational,
    pub difference: Rational,
    pub weighted_remainder: Rational,
    pub radius: Rational,
}

fn lagrange_at_zero(nodes: [Rational; 3], index: usize) -> Rational {
    let mut numerator = Rational::new(1, 1);
    let mut denominator = Rational::new(1, 1);
    for (j, node) in nodes.iter().enumerate() {
        if j == index {
            continue;
        }
        numerator = numerator.mul(*node);
        denominator = denominator.mul(nodes[index].sub(*node));
    }
    numerator.div(denominator)
}

pub fn witness() -> Witness {
    let lengths = [4_i64, 6, 8];
    let mut nodes = [Rational::zero(); 3];
    let mut occupation_states = [0_i64; 3];
    for i in 0..3 {
        let length = lengths[i];
        nodes[i] = Rational::new(1, length * length);
        let bits = match u8::try_from(length) {
            Ok(bits) if bits < 32 => bits,
            _ => panic!("occupation length is outside 2^L"),
        };
        occupation_states[i] = 1_i64 << bits;
    }
    let mut weights = [Rational::zero(); 3];
    for i in 0..3 {
        weights[i] = lagrange_at_zero(nodes, i);
    }
    let mut moments = [Rational::zero(); 3];
    let mut absolute_weight_sum = Rational::zero();
    for i in 0..3 {
        let x = nodes[i];
        moments[0] = moments[0].add(weights[i]);
        moments[1] = moments[1].add(weights[i].mul(x));
        moments[2] = moments[2].add(weights[i].mul(x).mul(x));
        absolute_weight_sum = absolute_weight_sum.add(weights[i].abs());
    }
    let mut h_at_zero = Rational::new(1, 1);
    for node in nodes {
        h_at_zero = h_at_zero.mul(Rational::zero().sub(node));
    }
    Witness {
        repetitions: 2,
        q: 3,
        lengths,
        occupation_states,
        occupation_traces: [912, 33012, 973824],
        nodes,
        weights,
        moments,
        h_at_zero,
        absolute_weight_sum,
    }
}

pub fn h_at(x: Rational) -> Rational {
    let mut value = Rational::new(1, 1);
    for node in witness().nodes {
        value = value.mul(x.sub(node));
    }
    value
}

pub fn extrapolate(
    f: Rational,
    c1: Rational,
    c2: Rational,
    remainders: [Rational; 3],
    bounds: [Rational; 3],
) -> Result<Extrapolation, &'static str> {
    let carrier = witness();
    let mut hat_f = Rational::zero();
    let mut weighted_remainder = Rational::zero();
    let mut triangle = Rational::zero();
    let mut radius = Rational::zero();
    for i in 0..3 {
        if bounds[i].num < 0 {
            return Err("a declared bound b_i must be nonnegative");
        }
        let remainder_abs = remainders[i].abs();
        if !bounds[i].ge(remainder_abs) {
            return Err("declared bound does not cover the remainder");
        }
        let x = carrier.nodes[i];
        let g = f
            .add(c1.mul(x))
            .add(c2.mul(x).mul(x))
            .add(remainders[i]);
        let weight = carrier.weights[i];
        hat_f = hat_f.add(weight.mul(g));
        weighted_remainder = weighted_remainder.add(weight.mul(remainders[i]));
        triangle = triangle.add(weight.abs().mul(remainder_abs));
        radius = radius.add(weight.abs().mul(bounds[i]));
    }
    let difference = hat_f.sub(f);
    if difference != weighted_remainder {
        return Err("moment cancellation failed for these weights");
    }
    if !triangle.ge(difference.abs()) || !radius.ge(triangle) {
        return Err("triangle bound failed for these inputs");
    }
    Ok(Extrapolation {
        hat_f,
        difference,
        weighted_remainder,
        radius,
    })
}

pub fn proved_scaling_remainder(bounds: [Rational; 3]) -> Result<Rational, &'static str> {
    let _ = (bounds, witness().h_at_zero);
    Err("the verification record carries no independently justified scaling remainder")
}

pub fn remainder_bounds_from_samples() -> Result<[Rational; 3], &'static str> {
    let gap = witness().h_at_zero;
    if gap != Rational::new(-1, 36864) {
        return Err("node gap is not H(0)=-1/36864");
    }
    Err("three samples do not determine b_i; H(0)=-1/36864 moves the value at zero")
}

pub fn refuse_higher_dimensional_sum(dimension: i64) -> Result<(), &'static str> {
    let _trace = witness().occupation_traces[0];
    if dimension >= 2 {
        Err("do not copy the one-dimensional trace 912 into a higher-dimensional sum")
    } else {
        Err("this carrier does not define a dimensional sum of occupation traces")
    }
}

pub fn refuse_continuum_limit() -> Result<(), &'static str> {
    Err("a finite model on L=(4,6,8) does not establish a continuum limit")
}

#[cfg(test)]
mod tests {
    use super::{
        extrapolate, h_at, proved_scaling_remainder, refuse_continuum_limit,
        refuse_higher_dimensional_sum, remainder_bounds_from_samples, witness, Rational,
    };

    #[test]
    fn exact_weights_moments_node_gap_and_conditional_bound() {
        let carrier = witness();
        assert_eq!(carrier.repetitions, 2);
        assert_eq!(carrier.q, 3);
        assert_eq!(carrier.lengths, [4, 6, 8]);
        assert_eq!(carrier.occupation_states, [16, 64, 256]);
        assert_eq!(carrier.occupation_traces, [912, 33012, 973824]);
        assert_eq!(carrier.nodes, [
            Rational::new(1, 16),
            Rational::new(1, 36),
            Rational::new(1, 64),
        ]);
        assert_eq!(carrier.weights, [
            Rational::new(4, 15),
            Rational::new(-81, 35),
            Rational::new(64, 21),
        ]);
        assert_eq!(carrier.moments, [
            Rational::new(1, 1),
            Rational::new(0, 1),
            Rational::new(0, 1),
        ]);
        assert_eq!(carrier.h_at_zero, Rational::new(-1, 36864));
        assert_eq!(h_at(Rational::zero()), Rational::new(-1, 36864));
        for node in carrier.nodes {
            assert_eq!(h_at(node), Rational::zero());
        }
        assert_eq!(carrier.absolute_weight_sum, Rational::new(197, 35));

        let f = Rational::new(3, 2);
        let c1 = Rational::new(4, 1);
        let c2 = Rational::new(-7, 1);
        let bounds = [Rational::new(1, 2), Rational::new(1, 3), Rational::new(1, 5)];
        let sharp = extrapolate(
            f,
            c1,
            c2,
            [Rational::new(1, 2), Rational::new(-1, 3), Rational::new(1, 5)],
            bounds,
        )
        .expect("sharp external bounds cover the remainders");
        assert_eq!(sharp.difference, Rational::new(53, 35));
        assert_eq!(sharp.weighted_remainder, Rational::new(53, 35));
        assert_eq!(sharp.radius, Rational::new(53, 35));
        assert_eq!(sharp.hat_f, Rational::new(211, 70));

        let strict = extrapolate(
            f,
            c1,
            c2,
            [Rational::new(1, 2), Rational::new(1, 3), Rational::new(1, 5)],
            bounds,
        )
        .expect("strict external bounds cover the remainders");
        assert_eq!(strict.difference, Rational::new(-1, 35));
        assert_eq!(strict.weighted_remainder, strict.difference);
        assert_eq!(strict.radius, Rational::new(53, 35));
        assert_eq!(strict.hat_f, Rational::new(103, 70));
        assert!(strict.radius.ge(strict.difference.abs()));

        let cancelled = extrapolate(f, c1, c2, [Rational::zero(); 3], [Rational::zero(); 3])
            .expect("zero remainders cancel");
        assert_eq!(cancelled.difference, Rational::zero());
        assert_eq!(cancelled.hat_f, f);
        assert_eq!(cancelled.radius, Rational::zero());

        let unit = extrapolate(
            Rational::zero(),
            Rational::zero(),
            Rational::zero(),
            [Rational::new(1, 1), Rational::new(-1, 1), Rational::new(1, 1)],
            [Rational::new(1, 1); 3],
        )
        .expect("unit external bounds");
        assert_eq!(unit.difference, Rational::new(197, 35));
        assert_eq!(unit.radius, Rational::new(197, 35));

        assert!(extrapolate(
            f,
            c1,
            c2,
            [Rational::new(1, 1), Rational::zero(), Rational::zero()],
            [Rational::new(1, 2), Rational::zero(), Rational::zero()],
        )
        .is_err());
        assert!(extrapolate(
            f,
            c1,
            c2,
            [Rational::zero(); 3],
            [Rational::new(-1, 1), Rational::zero(), Rational::zero()],
        )
        .is_err());
    }

    #[test]
    fn samples_do_not_determine_remainder_bounds() {
        assert!(proved_scaling_remainder([
            Rational::new(1, 100),
            Rational::new(1, 200),
            Rational::new(1, 400),
        ])
        .is_err());
        assert!(proved_scaling_remainder([
            Rational::new(197, 35),
            Rational::new(197, 35),
            Rational::new(197, 35),
        ])
        .is_err());
        assert!(remainder_bounds_from_samples().is_err());
        assert!(refuse_higher_dimensional_sum(2).is_err());
        assert!(refuse_higher_dimensional_sum(3).is_err());
        assert!(refuse_higher_dimensional_sum(4).is_err());
        assert!(refuse_continuum_limit().is_err());

        let carrier = witness();
        let t = Rational::new(6, 1).mul(Rational::new(36864, 1));
        let shift = t.mul(carrier.h_at_zero);
        assert_eq!(shift, Rational::new(-6, 1));
        assert_eq!(shift.abs().cmp_ord(Rational::new(197, 35)), 1);
        for node in carrier.nodes {
            assert_eq!(t.mul(h_at(node)), Rational::zero());
        }
    }
}
