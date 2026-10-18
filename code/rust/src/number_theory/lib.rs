//! `omega_number_theory` — exact number systems for the Omega Engine.
//!
//! Every quantity here is exact: there are no floating-point conversions and no
//! tolerances. The crate owns the arithmetic that quantum physics, MUB
//! constructions and the Weyl–Heisenberg algebra all need, so that no domain crate
//! carries a private copy.
//!
//! - [`rational`]: `Rational = BigRational` constructors, exact and floor square
//!   roots, perfect-square tests, the squarefree part of an integer (bounded trial
//!   division, typed refusal beyond the limit).
//! - [`polynomial`]: dense univariate [`polynomial::Polynomial`] over any exact field of
//!   the scalar tower (division, gcd, extended gcd, resultant, discriminant, squarefree
//!   decomposition); over `Q`: Gauss content, cyclotomic polynomials, Sturm sequences,
//!   exact real-root counts, isolation (rational roots exact) and refinement.
//! - [`quadratic`]: `Q(sqrt D)` with a compile-time radicand ([`quadratic::Quadratic`], exact
//!   order for `D > 0`), one-term real surds ([`quadratic::Surd`]) and run-time-radicand
//!   [`quadratic::QuadraticNumber`] with exact square roots.
//! - [`cyclotomic_field`]: `Q(zeta_n)` for any conductor up to
//!   [`polynomial::MAX_CONDUCTOR`]: run-time [`cyclotomic_field::CyclotomicNumber`] and
//!   compile-time [`cyclotomic_field::Cyclotomic`]; Galois group, trace, norm, real subfield,
//!   `2 cos(2 pi / n)` minimal polynomial, quantum integers, Gauss sums, `sqrt(d)`.
//! - [`real_embedding`]: exact sign, order and rational enclosures of real elements of
//!   `Q(zeta_n)` under each of its `phi(n)/2` real embeddings.
//! - [`cyclotomic`]: `Q(i)`, `Q(zeta_3)`, `Q(zeta_5)`, `Q(zeta_8)`, `Q(zeta_12)` and
//!   `Q(zeta_24)`, with the shared exact scalar tower.
//! - [`cyclotomic28`], [`cyclotomic44`], [`cyclotomic52`], [`cyclotomic120`]:
//!   clean-room `Q(zeta_N)` for the conductors the MUB Gauss-sum proofs need.
//! - [`scalar`]: the `std::ops`, `num_traits` and `linear_algebra::scalars` bridge for the
//!   fixed-conductor types; [`power_basis`]: their shared inversion.
//! - [`finite_field`], [`binary_field`]: `GF(p^k)` and `GF(2^k)`.
//! - [`character_sums`]: additive characters and quadratic Gauss sums valued in an
//!   exact cyclotomic field.
//!
//! AuthorityEffect: None. Not PROVED. Not GlobalGreen.

extern crate self as omega_number_theory;
pub mod binary_field;
pub mod character_sums;
pub mod certified_angles;
pub mod circle_haar;
pub mod cyclotomic;
pub mod cyclotomic120;
pub mod cyclotomic28;
pub mod cyclotomic44;
pub mod cyclotomic52;
pub mod cyclotomic_field;
pub mod cyclotomic_integer;
pub mod cyclotomic_ordered;
pub mod dyadic_presentation;
pub mod finite_field;
pub mod four_squares;
pub mod gaussian_norm;
pub mod gaussian_regular;
pub mod integer_factorization;
pub mod polynomial;
pub mod polynomial_factorization;
pub mod polynomial_map;
pub mod power_basis;
pub mod power_series;
pub mod quadratic;
pub mod radical_sum;
pub mod rational;
pub mod rational_turns;
pub mod real_embedding;
pub mod residue;
pub mod scalar;
pub mod sums_of_squares;
pub mod vanishing_sums;

#[cfg(test)]
pub(crate) mod test_support;

pub use cyclotomic::{Cyc12, Cyc24, Cyc5, Cyc8, EisensteinRat, GaussianRat};
pub use rational::{r_fifth, r_half, r_one, r_third, r_zero, ri, rq, One, Rational, Zero};

pub mod gf2;

pub mod rational_circle;

pub mod algebraic_real;
