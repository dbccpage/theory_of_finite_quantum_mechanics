
use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum HolonomyError {
    UnclosedPath,
    EmptyLoop,
    SingularElement,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalQuaternion {
    pub a: Ratio<i64>,
    pub b: Ratio<i64>,
    pub c: Ratio<i64>,
    pub d: Ratio<i64>,
}

impl RationalQuaternion {
    pub fn one() -> Self {
        Self {
            a: Ratio::one(),
            b: Ratio::zero(),
            c: Ratio::zero(),
            d: Ratio::zero(),
        }
    }

    pub fn new(a: Ratio<i64>, b: Ratio<i64>, c: Ratio<i64>, d: Ratio<i64>) -> Self {
        Self { a, b, c, d }
    }

    pub fn multiply(&self, rhs: &Self) -> Self {
        Self {
            a: self.a * rhs.a - self.b * rhs.b - self.c * rhs.c - self.d * rhs.d,
            b: self.a * rhs.b + self.b * rhs.a + self.c * rhs.d - self.d * rhs.c,
            c: self.a * rhs.c - self.b * rhs.d + self.c * rhs.a + self.d * rhs.b,
            d: self.a * rhs.d + self.b * rhs.c - self.c * rhs.b + self.d * rhs.a,
        }
    }

    pub fn norm_sq(&self) -> Ratio<i64> {
        self.a * self.a + self.b * self.b + self.c * self.c + self.d * self.d
    }

    pub fn trace(&self) -> Ratio<i64> {
        Ratio::from_integer(2) * self.a
    }
}

pub fn compute_path_ordered_holonomy(transports: &[RationalQuaternion]) -> Result<RationalQuaternion, HolonomyError> {
    if transports.is_empty() {
        return Err(HolonomyError::EmptyLoop);
    }
    let mut hol = RationalQuaternion::one();
    for t in transports {
        hol = hol.multiply(t);
    }
    Ok(hol)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quaternion_holonomy() {
        let q1 = RationalQuaternion::new(Ratio::new(3, 5), Ratio::new(4, 5), Ratio::zero(), Ratio::zero());
        assert_eq!(q1.norm_sq(), Ratio::one());
        let q1_inv = RationalQuaternion::new(Ratio::new(3, 5), Ratio::new(-4, 5), Ratio::zero(), Ratio::zero());
        let hol = compute_path_ordered_holonomy(&[q1, q1_inv]).unwrap();
        assert_eq!(hol, RationalQuaternion::one());
        assert_eq!(hol.trace(), Ratio::from_integer(2));
    }
}
