//! 4D Regge simplicial calculus over `Q`.
//!
//! What this module evaluates exactly:
//! squared edge lengths, Cayley-Menger volume squares, triangle area bivectors
//! in `∧² Q^4`, the Barrett-Crane simplicity condition `Σ ∧ Σ = 0`, transition
//! matrices that have been certified in `SO(4, Q)`, hinge holonomy products,
//! the contracted closure identity on each tetrahedron, the Coxeter-Freudenthal
//! 1-to-16 refinement, and the rational predicate `(S - S_EH)² ≤ (C a²)²`.
//!
//! What this module does not evaluate: the classical Regge sum `Σ A_h ε_h`.
//! The deficit angle `ε_h` is an arccosine and is not an element of `Q`.
//! The rational proxy below is `Σ A_h² κ_h`, where `κ_h = ||U_h - I||_F²`.
//! On a flat chart every supplied holonomy is the identity, the proxy is `0`,
//! and the flat Einstein-Hilbert value used for the bound is the rational `0`.
//! `einstein_hilbert_fence` returns that proxy. A chart is admitted as flat
//! only when the decision equals `flat_einstein_hilbert`. `|S| < 1e-6` is not
//! that decision.
//! That is not a numerical value of the round 4-sphere Einstein-Hilbert action.
//! This module does not call the surrounding crate's `f64` modules
//! `cayley_menger`, `regge_4d`, `regge_action`, or `regge_calculus`.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

pub mod action;
pub mod closure;
pub mod connection;
pub mod manifold;
pub mod orientation;
mod permute;
pub mod refinement;
pub mod simplicity;
pub mod sphere;

pub use action::{
    area_squared_in_pentatope, defect_bound_holds, einstein_hilbert_fence, flat_chart_admitted,
    flat_einstein_hilbert, rational_regge_proxy, RationalReggeProxy,
};
pub use closure::{all_tetra_closures_vanish, contracted_closure_in_pentatope};
pub use connection::{
    hinge_holonomy, identity_transition, pythagorean_so4, pythagorean_so4_inverse, try_transition,
};
pub use manifold::{ManifoldError, PentatopeChart, SimplicialManifold4D};
pub use orientation::{tetra_boundary_of_pentatope, triangle_boundary_of_tetra};
pub use refinement::freudenthal_refine_16;
pub use simplicity::{
    all_hinges_simple, hinge_bivector_in_pentatope, simplicity_holds_in_pentatope,
};
pub use sphere::{closed_s4_cube_boundary, orthogonal_pentatope};
