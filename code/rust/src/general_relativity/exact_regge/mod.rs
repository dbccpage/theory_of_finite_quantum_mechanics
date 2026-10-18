
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
