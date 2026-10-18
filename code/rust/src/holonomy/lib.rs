//! omega_holonomy — Exact Discrete Gauge Holonomy, Connection Laplacians,
//! and Curvature Commutators for the Omega Engine.
//!
//! AuthorityEffect: None.
//! Governing Rule: RULE[user_global] (Strict Zero-Float Law, Soviet Builder discipline).

extern crate self as omega_holonomy;
pub mod connection;
pub mod curvature;
pub mod error;
pub mod gauge_fixing;
pub mod gauge_quotient;
pub mod graph;
pub mod holonomy;
pub mod laplacian;
pub mod matrix;

pub use connection::{Connection, DiscreteConnection};
pub use curvature::{
    curvature_commutator, curvature_commutator_vanishes, group_commutator, plaquette_curvature,
    verify_discrete_bianchi_identity, CurvatureEngine,
};
pub use error::HolonomyError;
pub use graph::{CellComplex, Edge, Face, OrientedStep, Vertex};
pub use holonomy::{
    compute_loop_holonomy, compute_path_holonomy, cycle_homology_pairing, is_flat,
    wilson_loop_trace, HolonomyEngine, HolonomyLoop,
};
pub use laplacian::{
    compute_connection_laplacian, ConnectionLaplacian, PerturbationCertificate, RealDiagonal,
};
pub use matrix::{ExactMatrix, ExactScalar, GaussianRational, RationalMatrix};

pub mod signed_transport;

pub mod prelude {
    pub use crate::{
        compute_connection_laplacian, compute_loop_holonomy, compute_path_holonomy,
        curvature_commutator, curvature_commutator_vanishes, cycle_homology_pairing, is_flat,
        plaquette_curvature, verify_discrete_bianchi_identity, wilson_loop_trace, CellComplex,
        Connection, ConnectionLaplacian, CurvatureEngine, DiscreteConnection, Edge, ExactMatrix,
        ExactScalar, Face, GaussianRational, HolonomyEngine, HolonomyError, HolonomyLoop,
        RationalMatrix,
    };
}
pub mod functional_graph;
