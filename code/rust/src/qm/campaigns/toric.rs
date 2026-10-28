

use engine_homology::matrix_reduction::{is_zero_z2, multiply_z2, rank_z2};
use engine_quantum_physics::pauli::{pauli_anticommutes, pauli_commutes, Pauli};
use serde::{Deserialize, Serialize};

pub type Pauli8 = [Pauli; 8];

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
        let d1 = vec![
            vec![1, 1, 0, 0, 1, 0, 1, 0],
            vec![1, 1, 0, 0, 0, 1, 0, 1],
            vec![0, 0, 1, 1, 1, 0, 1, 0],
            vec![0, 0, 1, 1, 0, 1, 0, 1],
        ];

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

    pub fn star_operators() -> [Pauli8; 4] {
        let mut a0 = [Pauli::I; 8];
        a0[0] = Pauli::X;
        a0[1] = Pauli::X;
        a0[4] = Pauli::X;
        a0[6] = Pauli::X;

        let mut a1 = [Pauli::I; 8];
        a1[0] = Pauli::X;
        a1[1] = Pauli::X;
        a1[5] = Pauli::X;
        a1[7] = Pauli::X;

        let mut a2 = [Pauli::I; 8];
        a2[2] = Pauli::X;
        a2[3] = Pauli::X;
        a2[4] = Pauli::X;
        a2[6] = Pauli::X;

        let mut a3 = [Pauli::I; 8];
        a3[2] = Pauli::X;
        a3[3] = Pauli::X;
        a3[5] = Pauli::X;
        a3[7] = Pauli::X;

        [a0, a1, a2, a3]
    }

    pub fn plaquette_operators() -> [Pauli8; 4] {
        let mut b0 = [Pauli::I; 8];
        b0[0] = Pauli::Z;
        b0[2] = Pauli::Z;
        b0[4] = Pauli::Z;
        b0[5] = Pauli::Z;

        let mut b1 = [Pauli::I; 8];
        b1[1] = Pauli::Z;
        b1[3] = Pauli::Z;
        b1[4] = Pauli::Z;
        b1[5] = Pauli::Z;

        let mut b2 = [Pauli::I; 8];
        b2[0] = Pauli::Z;
        b2[2] = Pauli::Z;
        b2[6] = Pauli::Z;
        b2[7] = Pauli::Z;

        let mut b3 = [Pauli::I; 8];
        b3[1] = Pauli::Z;
        b3[3] = Pauli::Z;
        b3[6] = Pauli::Z;
        b3[7] = Pauli::Z;

        [b0, b1, b2, b3]
    }

    pub fn logical_operators() -> (Pauli8, Pauli8, Pauli8, Pauli8) {
        let mut wx1 = [Pauli::I; 8];
        wx1[0] = Pauli::X;
        wx1[2] = Pauli::X;

        let mut wz1 = [Pauli::I; 8];
        wz1[0] = Pauli::Z;
        wz1[1] = Pauli::Z;

        let mut wx2 = [Pauli::I; 8];
        wx2[4] = Pauli::X;
        wx2[5] = Pauli::X;

        let mut wz2 = [Pauli::I; 8];
        wz2[4] = Pauli::Z;
        wz2[6] = Pauli::Z;

        (wx1, wz1, wx2, wz2)
    }

    fn are_mutually_commuting(ops: &[Pauli8; 4]) -> bool {
        for i in 0..4 {
            for j in (i + 1)..4 {
                if !pauli_commutes(&ops[i], &ops[j]) {
                    return false;
                }
            }
        }
        true
    }

    fn do_sets_commute(set_a: &[Pauli8; 4], set_b: &[Pauli8; 4]) -> bool {
        for a in set_a {
            for b in set_b {
                if !pauli_commutes(a, b) {
                    return false;
                }
            }
        }
        true
    }

    fn logicals_commute_with_stabilizers(
        logs: &[&Pauli8; 4],
        stars: &[Pauli8; 4],
        plaquettes: &[Pauli8; 4],
    ) -> bool {
        for &l in logs {
            if !stars.iter().all(|s| pauli_commutes(l, s))
                || !plaquettes.iter().all(|p| pauli_commutes(l, p))
            {
                return false;
            }
        }
        true
    }

    pub fn new() -> Self {
        let v = 4;
        let e = 8;
        let f = 4;
        let chi = (v as i32) - (e as i32) + (f as i32);
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

        let stars_commute = Self::are_mutually_commuting(&stars);
        let plaqs_commute = Self::are_mutually_commuting(&plaquettes);
        let star_plaq_all_commute = Self::do_sets_commute(&stars, &plaquettes);
        let logs = [&wx1, &wz1, &wx2, &wz2];
        let log_commutes_stabs =
            Self::logicals_commute_with_stabilizers(&logs, &stars, &plaquettes);

        let braiding_phase = if pauli_anticommutes(&wx1, &wz1) { -1 } else { 1 };
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
