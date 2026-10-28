
extern crate self as tfqm_general_relativity;
pub mod bi_crossed_product;
pub mod causal_dynamical_triangulation;
pub mod causal_set;
pub mod certified_dihedral;
pub mod cayley_menger;
pub mod connection;
pub mod cosmological_constant;
pub mod curvature_tensor;
pub mod dec_laplacian;
pub mod dihedral_angles;
pub mod dirac_operator_discrete;
pub mod discrete_spacetime;
pub mod einstein_hilbert_action;
pub mod exact_regge;
pub mod field_equation;
pub mod gauge_transformation;
pub mod hamiltonian_constraint;
pub mod holonomy;
pub mod initial_value_formulation;
pub mod loop_quantum_gravity;
pub mod metric_hinge_transport;
pub mod quantum_group_symmetry;
pub mod quantum_regge;
pub mod regge_4d;
pub mod regge_action;
pub mod regge_calculus;
pub mod regge_deficit_holonomy;
pub mod ricci_curvature;
pub mod scalar_curvature;
pub mod schlafli;
pub mod spectral_triple;
pub mod spin_connection;
pub mod spin_foam;
pub mod spinor_field;
pub mod tetrad_formalism;

#[cfg(test)]
mod certified_authority_fence;

pub mod simplicial_dynamics;

use num_rational::Ratio;

pub fn verify_surface_euler_characteristic(vertices: usize, edges: usize, faces: usize, expected_chi: i64) -> bool {
    let chi = (vertices as i64) - (edges as i64) + (faces as i64);
    chi == expected_chi
}

#[cfg(test)]
mod gr_tests {
    use super::*;

    #[test]
    fn test_tetrahedron_euler() {
        assert!(verify_surface_euler_characteristic(4, 6, 4, 2));
    }
}
