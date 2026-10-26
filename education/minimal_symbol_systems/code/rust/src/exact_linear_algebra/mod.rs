//! Exact Linear Algebra and Topological Physics Verification Package.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Unifies exact algebraic representations ported from `omega_linear_algebra`:
//! - Pillar 1: Smith Normal Form & Torsion Extraction over Z.
//! - Pillar 2: Quadratic Field Extensions Q(sqrt(5)) & Mac Lane Pentagon Associator Equations (F^2 = I).
//! - Pillar 3: Discrete Bianchi Holonomies & Parallel Transport in SO(4) and Q(i).

pub mod regge_exact;
pub mod scalars;
pub mod quadratic_extension;
pub mod gaussian_rational;

pub use regge_exact::{CayleyMengerResult, ExactError, So4, Bivector4, cayley_menger, signed_volume_4};
pub use scalars::{CheckedExactField, ExactRing, Field, Ring, Semiring};
pub use quadratic_extension::{QuadraticExtension, Matrix2x2Quadratic, audit_fibonacci_f_matrix_square};
pub use gaussian_rational::{GaussianRational, Simplex4DFrame, verify_bianchi_closure};
