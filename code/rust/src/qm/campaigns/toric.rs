// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Surface code toric topology, lattice operators, and anyon braiding phase.
//!
//! Models the 2x2 toric lattice with:
//!   - 4 vertices, 8 physical edge qubits, 4 plaquette faces (Euler characteristic chi = 0).
//!   - 4 star operators A_s (product of 4 X edges incident to vertex s).
//!   - 4 plaquette operators B_p (product of 4 Z edges bounding face p).
//!   - 2 independent non-contractible Wilson loops W_X1, W_X2 and dual loops W_Z1, W_Z2.
//!   - Exact symplectic intersection check evaluating W_X1 W_Z1 = - W_Z1 W_X1 (braiding phase -1).

use omega_homology::matrix_reduction::{is_zero_z2, multiply_z2, rank_z2};
use omega_quantum_physics::pauli::{pauli_anticommutes, pauli_commutes, Pauli};
use serde::{Deserialize, Serialize};

pub type Pauli8 = [Pauli; 8];

/// Exact lattice representation of the 2x2 toric code.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ToricCode2x2 {
    pub n_vertices: usize,
    pub n_edges: usize,
    pub n_faces: usize,
    pub euler_characteristic: i32,
    pub k_logical: usize,
    pub ground_state_degeneracy: usize,
    #[serde(default)]
    pub homology_boundary_law_verified: bool,
    #[serde(default)]
    pub h0_dimension: usize,
    #[serde(default)]
    pub h1_dimension: usize,
    pub star_plaquette_all_commute: bool,
    pub stars_mutually_commute: bool,
    pub plaquettes_mutually_commute: bool,
    pub logical_operators_commute_with_stabilizers: bool,
    pub logical_homology_braiding_phase: i32,
    pub cross_loop_commutes: bool,
}

impl Default for ToricCode2x2 {
    fn default() -> Self {
        Self::new()
    }
}

impl ToricCode2x2 {
    fn homology() -> (bool, usize, usize) {
        // Boundary map C_1 -> C_0 for the periodic 2x2 cellulation over Z_2.
        let d1 = vec![
            vec![1, 1, 0, 0, 1, 0, 1, 0],
            vec![1, 1, 0, 0, 0, 1, 0, 1],
            vec![0, 0, 1, 1, 1, 0, 1, 0],
            vec![0, 0, 1, 1, 0, 1, 0, 1],
        ];

        // Face boundaries C_2 -> C_1 over Z_2. Signs coincide modulo two.
        let d2 = vec![
            vec![1, 0, 1, 0],
            vec![0, 1, 0, 1],
            vec![1, 0, 1, 0],
            vec![0, 1, 0, 1],
            vec![1, 1, 0, 0],
            vec![1, 1, 0, 0],
            vec![0, 0, 1, 1],
            vec![0, 0, 1, 1],
        ];

        let boundary_composite =
            multiply_z2(&d1, &d2).expect("the fixed torus boundary-map dimensions must compose");
        let boundary_law = is_zero_z2(&boundary_composite);
        let rank_d1 = rank_z2(&d1).expect("the fixed torus incidence matrix is rectangular");
        let rank_d2 = rank_z2(&d2).expect("the fixed torus face matrix is rectangular");
        let h0 = d1.len() - rank_d1;
        let h1 = d1[0].len() - rank_d1 - rank_d2;
        (boundary_law, h0, h1)
    }

    /// Constructs the 4 star operators A_s on the 2x2 torus.
    pub fn star_operators() -> [Pauli8; 4] {
        // Vertex 0: incident edges {0, 1, 4, 6}
        let mut a0 = [Pauli::I; 8];
        a0[0] = Pauli::X;
        a0[1] = Pauli::X;
        a0[4] = Pauli::X;
        a0[6] = Pauli::X;

        // Vertex 1: incident edges {0, 1, 5, 7}
        let mut a1 = [Pauli::I; 8];
        a1[0] = Pauli::X;
        a1[1] = Pauli::X;
        a1[5] = Pauli::X;
        a1[7] = Pauli::X;

        // Vertex 2: incident edges {2, 3, 4, 6}
        let mut a2 = [Pauli::I; 8];
        a2[2] = Pauli::X;
        a2[3] = Pauli::X;
        a2[4] = Pauli::X;
        a2[6] = Pauli::X;

        // Vertex 3: incident edges {2, 3, 5, 7}
        let mut a3 = [Pauli::I; 8];
        a3[2] = Pauli::X;
        a3[3] = Pauli::X;
        a3[5] = Pauli::X;
        a3[7] = Pauli::X;

        [a0, a1, a2, a3]
    }

    /// Constructs the 4 plaquette operators B_p on the 2x2 torus.
    pub fn plaquette_operators() -> [Pauli8; 4] {
        // Face 0: boundary edges {0, 2, 4, 5}
        let mut b0 = [Pauli::I; 8];
        b0[0] = Pauli::Z;
        b0[2] = Pauli::Z;
        b0[4] = Pauli::Z;
        b0[5] = Pauli::Z;

        // Face 1: boundary edges {1, 3, 4, 5}
        let mut b1 = [Pauli::I; 8];
        b1[1] = Pauli::Z;
        b1[3] = Pauli::Z;
        b1[4] = Pauli::Z;
        b1[5] = Pauli::Z;

        // Face 2: boundary edges {0, 2, 6, 7}
        let mut b2 = [Pauli::I; 8];
        b2[0] = Pauli::Z;
        b2[2] = Pauli::Z;
        b2[6] = Pauli::Z;
        b2[7] = Pauli::Z;

        // Face 3: boundary edges {1, 3, 6, 7}
        let mut b3 = [Pauli::I; 8];
        b3[1] = Pauli::Z;
        b3[3] = Pauli::Z;
        b3[6] = Pauli::Z;
        b3[7] = Pauli::Z;

        [b0, b1, b2, b3]
    }

    /// Constructs the logical non-contractible Wilson loop operators:
    /// (W_X1, W_Z1) and (W_X2, W_Z2).
    pub fn logical_operators() -> (Pauli8, Pauli8, Pauli8, Pauli8) {
        // Logical 1:
        // W_X1 along vertical dual cut {0, 2}
        let mut wx1 = [Pauli::I; 8];
        wx1[0] = Pauli::X;
        wx1[2] = Pauli::X;

        // W_Z1 along horizontal primal cycle {0, 1}
        let mut wz1 = [Pauli::I; 8];
        wz1[0] = Pauli::Z;
        wz1[1] = Pauli::Z;

        // Logical 2:
        // W_X2 along horizontal dual cut {4, 5}
        let mut wx2 = [Pauli::I; 8];
        wx2[4] = Pauli::X;
        wx2[5] = Pauli::X;

        // W_Z2 along vertical primal cycle {4, 6}
        let mut wz2 = [Pauli::I; 8];
        wz2[4] = Pauli::Z;
        wz2[6] = Pauli::Z;

        (wx1, wz1, wx2, wz2)
    }

    /// Creates and verifies 2x2 toric code lattice on T^2 and anyon braiding.
    pub fn new() -> Self {
        let v = 4;
        let e = 8;
        let f = 4;
        let chi = (v as i32) - (e as i32) + (f as i32); // 4 - 8 + 4 = 0
        let (boundary_law, h0, h1) = Self::homology();
        assert!(
            boundary_law,
            "torus boundary maps must satisfy d1*d2 = 0 over Z_2"
        );
        let k = h1;
        let degen = 1usize
            .checked_shl(k as u32)
            .expect("logical-qubit count must fit the finite lattice size");

        let stars = Self::star_operators();
        let plaquettes = Self::plaquette_operators();
        let (wx1, wz1, wx2, wz2) = Self::logical_operators();

        // 1. Verify all 4 stars pairwise commute
        let mut stars_commute = true;
        for i in 0..4 {
            for j in (i + 1)..4 {
                if !pauli_commutes(&stars[i], &stars[j]) {
                    stars_commute = false;
                }
            }
        }

        // 2. Verify all 4 plaquettes pairwise commute
        let mut plaqs_commute = true;
        for i in 0..4 {
            for j in (i + 1)..4 {
                if !pauli_commutes(&plaquettes[i], &plaquettes[j]) {
                    plaqs_commute = false;
                }
            }
        }

        // 3. Verify every star commutes with every plaquette (16 pairs)
        let mut star_plaq_all_commute = true;
        for s in 0..4 {
            for p in 0..4 {
                if !pauli_commutes(&stars[s], &plaquettes[p]) {
                    star_plaq_all_commute = false;
                }
            }
        }

        // 4. Verify logical operators commute with all stars and plaquettes
        let mut log_commutes_stabs = true;
        let logs = [&wx1, &wz1, &wx2, &wz2];
        for &l in &logs {
            for s in 0..4 {
                if !pauli_commutes(l, &stars[s]) {
                    log_commutes_stabs = false;
                }
            }
            for p in 0..4 {
                if !pauli_commutes(l, &plaquettes[p]) {
                    log_commutes_stabs = false;
                }
            }
        }

        // 5. Verify logical braiding phase: W_X1 and W_Z1 anticommute (phase -1 = e^{i pi})
        let anticommutes_w1 = pauli_anticommutes(&wx1, &wz1);
        let braiding_phase = if anticommutes_w1 { -1 } else { 1 };

        // 6. Cross-loop commutation: W_X1 and W_Z2 commute
        let cross_commutes = pauli_commutes(&wx1, &wz2);

        Self {
            n_vertices: v,
            n_edges: e,
            n_faces: f,
            euler_characteristic: chi,
            k_logical: k,
            ground_state_degeneracy: degen,
            homology_boundary_law_verified: boundary_law,
            h0_dimension: h0,
            h1_dimension: h1,
            star_plaquette_all_commute: star_plaq_all_commute,
            stars_mutually_commute: stars_commute,
            plaquettes_mutually_commute: plaqs_commute,
            logical_operators_commute_with_stabilizers: log_commutes_stabs,
            logical_homology_braiding_phase: braiding_phase,
            cross_loop_commutes: cross_commutes,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_toric_code_topology_and_braiding() {
        let t = ToricCode2x2::new();
        assert_eq!(t.euler_characteristic, 0);
        assert_eq!(t.k_logical, 2);
        assert_eq!(t.ground_state_degeneracy, 4);
        assert!(t.homology_boundary_law_verified);
        assert_eq!(t.h0_dimension, 1);
        assert_eq!(t.h1_dimension, 2);
        assert!(t.stars_mutually_commute);
        assert!(t.plaquettes_mutually_commute);
        assert!(t.star_plaquette_all_commute);
        assert!(t.logical_operators_commute_with_stabilizers);
        assert_eq!(t.logical_homology_braiding_phase, -1);
        assert!(t.cross_loop_commutes);
    }
}
