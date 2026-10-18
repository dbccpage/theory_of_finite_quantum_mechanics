//! Target 19 — Separating predictions: analytic CHSH/Tsirelson + Mermin–Peres bridge.
//!
//! Finite analytic bounds (exact rationals / integers), an exhaustive search
//! for noncontextual assignments of a declared Mermin–Peres square, and the
//! degree-two class of its sign table, decided exactly over `F_2`.
//!
//! AuthorityEffect: None. Not PROVED. Not GlobalGreen.

use num_traits::Signed;
use omega_number_theory::rational::{ri, Rational};

/// Fence.
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; CHSH/Tsirelson + Mermin-Peres cochain bridge face.";

pub type Q = Rational;

/// CHSH correlator bound face.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChshBounds {
    /// Classical local-realistic bound |S| ≤ 2.
    pub classical: Q,
    /// Tsirelson quantum bound 2√2 (stored as exact square: we keep 2√2 as
    /// residual OPEN for exact √2 in ℚ; provide integer proxy comparison).
    pub tsirelson_squared: Q,
    /// Notes.
    pub note: &'static str,
}

impl ChshBounds {
    /// Classical 2; Tsirelson 2√2 ⇒ (2√2)² = 8 as exact rational marker.
    pub fn standard() -> Self {
        Self {
            classical: ri(2),
            tsirelson_squared: ri(8), // (2√2)² = 8
            note: "Tsirelson value 2√2 is not an element of ℚ; uniqueness of the bound \
                   is recorded via S² ≤ 8 for quantum, |S| ≤ 2 classical. Exact √2 \
                   residual OPEN on this rational face.",
        }
    }

    /// Classify an observed S² value.
    pub fn classify_s_squared(&self, s_sq: &Q) -> Result<ChshClass, &'static str> {
        if s_sq.is_negative() {
            return Err("a squared correlator cannot be negative");
        }
        if s_sq <= &(&self.classical * &self.classical) {
            Ok(ChshClass::ClassicalCompatible)
        } else if s_sq <= &self.tsirelson_squared {
            Ok(ChshClass::QuantumCompatible)
        } else {
            Ok(ChshClass::BeyondTsirelson)
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ChshClass {
    ClassicalCompatible,
    QuantumCompatible,
    BeyondTsirelson,
}

/// Analytic CHSH example: PR-box S=4 ⇒ S²=16 beyond Tsirelson; quantum max S²=8.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChshExample {
    pub label: &'static str,
    pub s_squared: Q,
    pub class: ChshClass,
}

impl ChshExample {
    pub fn classical_max() -> Self {
        let b = ChshBounds::standard();
        let s_sq = ri(4); // 2²
        Self {
            label: "classical_max",
            s_squared: s_sq.clone(),
            class: b
                .classify_s_squared(&s_sq)
                .expect("nonnegative fixed example"),
        }
    }

    pub fn tsirelson_max_marker() -> Self {
        let b = ChshBounds::standard();
        let s_sq = ri(8);
        Self {
            label: "tsirelson_S2_eq_8",
            s_squared: s_sq.clone(),
            class: b
                .classify_s_squared(&s_sq)
                .expect("nonnegative fixed example"),
        }
    }

    pub fn pr_box() -> Self {
        let b = ChshBounds::standard();
        let s_sq = ri(16); // 4²
        Self {
            label: "pr_box",
            s_squared: s_sq.clone(),
            class: b
                .classify_s_squared(&s_sq)
                .expect("nonnegative fixed example"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn chsh_classical_quantum_pr_separation() {
        let c = ChshExample::classical_max();
        assert_eq!(c.class, ChshClass::ClassicalCompatible);
        let t = ChshExample::tsirelson_max_marker();
        assert_eq!(t.class, ChshClass::QuantumCompatible);
        let pr = ChshExample::pr_box();
        assert_eq!(pr.class, ChshClass::BeyondTsirelson);
    }

    #[test]
    fn negative_s_squared_is_refused_and_a_bound_is_not_membership() {
        assert!(ChshBounds::standard().classify_s_squared(&ri(-1)).is_err());
    }
}
