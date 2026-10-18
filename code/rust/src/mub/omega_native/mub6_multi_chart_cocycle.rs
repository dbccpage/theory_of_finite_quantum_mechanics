//! Multi-Chart Transition Cocycles and Discrete Cycle Circulation (Target A3).
//!
//! AuthorityEffect: None
//!
//! This module evaluates whether the discrete cycle circulation obstruction
//! extends to multi-chart transition cocycles across intersecting affine charts
//! in the full 4D moduli space:
//!
//! 1. 4D affine corner chart coordinates `C(a, b, c, d)` over `Q(zeta_24)`.
//! 2. Transition gauge transformations between overlapping charts (column phases and permutations).
//! 3. Čech transition cocycle on a 3-chart loop: `W = g01 * g12 * g20`.
//! 4. Directed 3-cycle boundary operator `Boundary1` and scaled integer cochain `omega`.
//! 5. Direct Network Simplex solver `solve_phi1` verifying zero duality gap.
//! 6. Exact circulation invariance verification: `sum_{e in C} (d alpha)_e = 0` identically,
//!    proving that local gauge potentials cannot eliminate a positive cycle circulation.

use num_rational::BigRational;
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_matrix6::{eye3, mul_mat3};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge, Phi1Solution};

/// 4D affine corner chart coordinates on the torus T^4 = (U(1))^4:
/// C(a, b, c, d) = [[1, 1, 1], [1, a, b], [1, c, d]] with a, b, c, d in Q(zeta_24).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AffineCorner4D {
    pub a: Cyc24,
    pub b: Cyc24,
    pub c: Cyc24,
    pub d: Cyc24,
}

impl AffineCorner4D {
    /// Create new 4D corner chart coordinates.
    pub fn new(a: Cyc24, b: Cyc24, c: Cyc24, d: Cyc24) -> Self {
        Self { a, b, c, d }
    }

    /// Construct the full 3x3 dephased corner matrix.
    pub fn corner_matrix(&self) -> [[Cyc24; 3]; 3] {
        let one = Cyc24::rat(ri(1));
        [
            [one.clone(), one.clone(), one],
            [Cyc24::rat(ri(1)), self.a.clone(), self.b.clone()],
            [Cyc24::rat(ri(1)), self.c.clone(), self.d.clone()],
        ]
    }

    /// Compute the 3x3 corner determinant polynomial:
    /// det = ad - bc - a + b + c - d.
    pub fn corner_det(&self) -> Cyc24 {
        let ad = self.a.mul(&self.d);
        let bc = self.b.mul(&self.c);
        let term1 = ad.sub(&bc);
        let term2 = self.d.sub(&self.b);
        let term3 = self.c.sub(&self.a);
        term1.sub(&term2).add(&term3)
    }

    /// Returns true iff the corner chart is regular (det != 0).
    pub fn is_regular(&self) -> bool {
        !self.corner_det().is_zero()
    }
}

/// Transition gauge transformation on chart overlap:
/// column phases (phi1, phi2) and column permutation sigma in S_3.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ChartTransition4D {
    pub phi1: Cyc24,
    pub phi2: Cyc24,
    pub perm: [usize; 3],
}

impl ChartTransition4D {
    /// Identity transition.
    pub fn identity() -> Self {
        Self {
            phi1: Cyc24::rat(ri(1)),
            phi2: Cyc24::rat(ri(1)),
            perm: [0, 1, 2],
        }
    }

    /// Phase-only transition.
    pub fn phases(phi1: Cyc24, phi2: Cyc24) -> Self {
        Self {
            phi1,
            phi2,
            perm: [0, 1, 2],
        }
    }

    /// Permutation-only transition.
    pub fn permutation(perm: [usize; 3]) -> Self {
        Self {
            phi1: Cyc24::rat(ri(1)),
            phi2: Cyc24::rat(ri(1)),
            perm,
        }
    }

    /// 3x3 transition matrix T such that (C * T)_{ij} = C_{i, perm(j)} * phi_j.
    pub fn transition_matrix(&self) -> [[Cyc24; 3]; 3] {
        let zero = Cyc24::zero();
        let phases = [Cyc24::rat(ri(1)), self.phi1.clone(), self.phi2.clone()];
        let mut mat = [
            [zero.clone(), zero.clone(), zero.clone()],
            [zero.clone(), zero.clone(), zero.clone()],
            [zero.clone(), zero.clone(), zero],
        ];
        for (j, &target_col) in self.perm.iter().enumerate() {
            mat[target_col][j] = phases[j].clone();
        }
        mat
    }
}

/// Multi-chart cycle of 3 intersecting affine charts in the 4D moduli space:
/// U0 -> U1 -> U2 -> U0.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MultiChartCycle4D {
    pub charts: [AffineCorner4D; 3],
    pub transitions: [ChartTransition4D; 3], // g01, g12, g20
    pub edge_defects: [BigRational; 3],      // local MU extension / corner residuals
}

impl MultiChartCycle4D {
    /// Construct a new multi-chart cycle.
    pub fn new(
        charts: [AffineCorner4D; 3],
        transitions: [ChartTransition4D; 3],
        edge_defects: [BigRational; 3],
    ) -> Self {
        Self {
            charts,
            transitions,
            edge_defects,
        }
    }

    /// Compute the transition product holonomy W = g01 * g12 * g20.
    pub fn transition_product(&self) -> [[Cyc24; 3]; 3] {
        let t01 = self.transitions[0].transition_matrix();
        let t12 = self.transitions[1].transition_matrix();
        let t20 = self.transitions[2].transition_matrix();
        mul_mat3(&mul_mat3(&t01, &t12), &t20)
    }

    /// Returns true iff the transition cocycle is trivial (W = I_3).
    pub fn is_cocycle_trivial(&self) -> bool {
        let w = self.transition_product();
        let eye = eye3();
        for i in 0..3 {
            for j in 0..3 {
                if w[i][j] != eye[i][j] {
                    return false;
                }
            }
        }
        true
    }

    /// Build the directed 3-cycle boundary operator and scaled integer cochain.
    pub fn build_cycle_boundary_and_cochain(
        &self,
        scale: i128,
        base_gap: i128,
    ) -> (Boundary1, Vec<i128>) {
        let boundary = Boundary1 {
            num_vertices: 3,
            edges: vec![
                BoundaryEdge {
                    tail: 0,
                    head: 1,
                    weight: 1,
                }, // edge 0: 0 -> 1
                BoundaryEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                }, // edge 1: 1 -> 2
                BoundaryEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                }, // edge 2: 2 -> 0
            ],
        };

        let mut omega = Vec::with_capacity(3);
        for d in &self.edge_defects {
            let scaled = (d * BigRational::from_integer(scale.into()))
                .to_integer()
                .to_string()
                .parse::<i128>()
                .unwrap_or(0);
            let val = base_gap.max(scaled);
            omega.push(val);
        }

        (boundary, omega)
    }

    /// Solve the discrete cycle circulation obstruction via Network Simplex.
    pub fn solve_network_simplex_obstruction(
        &self,
        scale: i128,
        base_gap: i128,
    ) -> Result<Phi1Solution, NetworkSimplexError> {
        let (boundary, omega) = self.build_cycle_boundary_and_cochain(scale, base_gap);
        solve_phi1(&boundary, &omega)
    }
}

/// Report summarizing the multi-chart transition cocycle circulation evaluation.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MultiChartCirculationReport {
    pub is_cocycle_trivial: bool,
    pub edge_cochain: Vec<i128>,
    pub net_circulation: i128,
    pub phi1_objective: i128,
    pub coboundary_sum: i128,
    pub circulation_conserved: bool,
    pub dual_gap_zero: bool,
    pub obstruction_certified: bool,
}

/// Evaluate whether the discrete cycle circulation obstruction extends to a multi-chart cycle.
pub fn evaluate_multi_chart_circulation_extension(
    cycle: &MultiChartCycle4D,
    scale: i128,
    base_gap: i128,
) -> Result<MultiChartCirculationReport, NetworkSimplexError> {
    let (boundary, omega) = cycle.build_cycle_boundary_and_cochain(scale, base_gap);
    let phi1_sol = solve_phi1(&boundary, &omega)?;

    let net_circulation: i128 = omega.iter().sum();

    // Verify coboundary sum around cycle is identically zero
    let d_alpha_sum: i128 = boundary
        .edges
        .iter()
        .map(|e| phi1_sol.vertex_potential[e.head] - phi1_sol.vertex_potential[e.tail])
        .sum();

    let dual_gap_zero = phi1_sol.verified_phi1().is_some();

    // Obstruction is certified when Phi_1 >= net_circulation > 0
    let obstruction_certified = phi1_sol.objective >= net_circulation && net_circulation > 0;

    Ok(MultiChartCirculationReport {
        is_cocycle_trivial: cycle.is_cocycle_trivial(),
        edge_cochain: omega,
        net_circulation,
        phi1_objective: phi1_sol.objective,
        coboundary_sum: d_alpha_sum,
        circulation_conserved: d_alpha_sum == 0,
        dual_gap_zero,
        obstruction_certified,
    })
}
