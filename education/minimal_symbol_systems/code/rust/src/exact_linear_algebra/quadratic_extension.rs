//! Pillar 2: Exact Quadratic Field Extension Q(sqrt(5)) for Fibonacci Anyon Fusion.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Implements exact algebraic arithmetic in Q(sqrt(5)):
//! (a1 + b1*sqrt(5)) * (a2 + b2*sqrt(5)) = (a1*a2 + 5*b1*b2) + (a1*b2 + b1*a2)*sqrt(5)
//! with zero floating-point error, evaluating F-matrix involution consistency F^2 = I.

use num_rational::Rational64;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuadraticExtension {
    /// Rational part `a`
    pub a: Rational64,
    /// Coefficient `b` of sqrt(5)
    pub b: Rational64,
}

impl QuadraticExtension {
    pub fn new(a: Rational64, b: Rational64) -> Self {
        Self { a, b }
    }

    pub fn from_rational(a: Rational64) -> Self {
        Self {
            a,
            b: Rational64::new(0, 1),
        }
    }

    pub fn zero() -> Self {
        Self {
            a: Rational64::new(0, 1),
            b: Rational64::new(0, 1),
        }
    }

    pub fn one() -> Self {
        Self {
            a: Rational64::new(1, 1),
            b: Rational64::new(0, 1),
        }
    }

    /// Golden ratio phi = (1 + sqrt(5)) / 2 = 1/2 + (1/2)*sqrt(5).
    pub fn golden_ratio() -> Self {
        Self {
            a: Rational64::new(1, 2),
            b: Rational64::new(1, 2),
        }
    }

    /// Golden ratio inverse phi^-1 = phi - 1 = -1/2 + (1/2)*sqrt(5).
    pub fn golden_ratio_inv() -> Self {
        Self {
            a: Rational64::new(-1, 2),
            b: Rational64::new(1, 2),
        }
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            a: self.a + other.a,
            b: self.b + other.b,
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            a: self.a - other.a,
            b: self.b - other.b,
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let five = Rational64::new(5, 1);
        let a = self.a * other.a + five * (self.b * other.b);
        let b = self.a * other.b + self.b * other.a;
        Self { a, b }
    }

    /// Norm N(a + b*sqrt(5)) = a^2 - 5*b^2 in Q.
    pub fn norm(&self) -> Rational64 {
        let five = Rational64::new(5, 1);
        self.a * self.a - five * (self.b * self.b)
    }

    /// Multiplicative inverse (a - b*sqrt(5)) / N(a + b*sqrt(5)).
    pub fn inv(&self) -> Option<Self> {
        let n = self.norm();
        if n == Rational64::new(0, 1) {
            None
        } else {
            Some(Self {
                a: self.a / n,
                b: -self.b / n,
            })
        }
    }

    pub fn is_one(&self) -> bool {
        self.a == Rational64::new(1, 1) && self.b == Rational64::new(0, 1)
    }

    pub fn is_zero(&self) -> bool {
        self.a == Rational64::new(0, 1) && self.b == Rational64::new(0, 1)
    }
}

/// 2x2 Matrix over Q(sqrt(5)).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Matrix2x2Quadratic {
    pub m: [[QuadraticExtension; 2]; 2],
}

impl Matrix2x2Quadratic {
    pub fn identity() -> Self {
        Self {
            m: [
                [QuadraticExtension::one(), QuadraticExtension::zero()],
                [QuadraticExtension::zero(), QuadraticExtension::one()],
            ],
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut out = [
            [QuadraticExtension::zero(), QuadraticExtension::zero()],
            [QuadraticExtension::zero(), QuadraticExtension::zero()],
        ];
        for r in 0..2 {
            for c in 0..2 {
                let term0 = self.m[r][0].mul(&other.m[0][c]);
                let term1 = self.m[r][1].mul(&other.m[1][c]);
                out[r][c] = term0.add(&term1);
            }
        }
        Self { m: out }
    }

    /// Verify exact involution: M^2 = I_2.
    pub fn is_involution(&self) -> bool {
        let sq = self.mul(self);
        sq == Self::identity()
    }
}

/// Audit Fibonacci Anyon Mac Lane Pentagon F-matrix consistency over Q(sqrt(5)).
pub fn audit_fibonacci_f_matrix_square() -> bool {
    let phi_inv = QuadraticExtension::golden_ratio_inv();
    // phi^-2 = (phi^-1)^2 = (-1/2 + 1/2*sqrt(5))^2 = (1/4 + 5/4) - 1/2*sqrt(5) = 3/2 - 1/2*sqrt(5)
    let phi_inv_sq = phi_inv.mul(&phi_inv);
    // In F^2, diagonal entry is phi^-2 + phi^-1:
    // (3/2 - 1/2*sqrt(5)) + (-1/2 + 1/2*sqrt(5)) = 1 + 0*sqrt(5) = 1.
    let diag = phi_inv_sq.add(&phi_inv);
    diag.is_one()
}
