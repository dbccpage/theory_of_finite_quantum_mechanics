// AuthorityEffect: None.

//! Finite checks behind the U(1)-selector argument.
//!
//! - Pairings on `Q(i)`. For a field automorphism `sigma` of `Q(i)` (the
//!   identity or complex conjugation; `x^2 = -1` has only the roots `+-i`) the
//!   pairing `B(a, b) = sigma(a) b` has cross term
//!   `X(a, b) = B(a+b, a+b) - B(a, a) - B(b, b) = sigma(a) b + sigma(b) a`. A
//!   global phase `u` multiplies `X` by `sigma(u) u`: by `|u|^2 = 1` for every
//!   unit under conjugation, and by `u^2` under the identity, which is `1` only
//!   for `u = +-1`.
//! The phase-group order, closure, conjugacy and regular-representation
//! algorithms are owned directly by Lie theory and number theory. This module
//! retains the physical pairing choice and its measured interference term.

use omega_number_theory::cyclotomic::GaussianRat;

/// The field automorphism entering the left slot of a pairing on `Q(i)`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PairingInvolution {
    Identity,
    Conjugation,
}

impl PairingInvolution {
    pub fn apply(self, z: &GaussianRat) -> GaussianRat {
        match self {
            Self::Identity => z.clone(),
            Self::Conjugation => z.conj(),
        }
    }

    /// `B(a, b) = sigma(a) b`.
    pub fn pairing(self, a: &GaussianRat, b: &GaussianRat) -> GaussianRat {
        self.apply(a).mul(b)
    }

    /// `X(a, b) = B(a+b, a+b) - B(a, a) - B(b, b)`.
    pub fn cross_term(self, a: &GaussianRat, b: &GaussianRat) -> GaussianRat {
        let sum = a.add(b);
        self.pairing(&sum, &sum)
            .sub(&self.pairing(a, a))
            .sub(&self.pairing(b, b))
    }

    /// `sigma(u) u`, the factor a global phase `u` puts on every cross term.
    pub fn phase_factor(self, u: &GaussianRat) -> GaussianRat {
        self.apply(u).mul(u)
    }
}
