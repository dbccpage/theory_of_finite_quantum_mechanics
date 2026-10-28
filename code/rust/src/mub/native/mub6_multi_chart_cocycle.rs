
use num_rational::BigRational;
use serde::{Deserialize, Serialize};

use crate::native::exact::mub6_matrix6::{eye3, mul_mat3};
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge, Phi1Solution};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AffineCorner4D {
    pub a: Cyc24,
    pub b: Cyc24,
    pub c: Cyc24,
    pub d: Cyc24,
}

impl AffineCorner4D {
    pub fn new(a: Cyc24, b: Cyc24, c: Cyc24, d: Cyc24) -> Self {
        Self { a, b, c, d }
    }

    pub fn corner_matrix(&self) -> [[Cyc24; 3]; 3] {
        let one = Cyc24::rat(ri(1));
        [
            [one.clone(), one.clone(), one],
            [Cyc24::rat(ri(1)), self.a.clone(), self.b.clone()],
            [Cyc24::rat(ri(1)), self.c.clone(), self.d.clone()],
        ]
    }

    pub fn corner_det(&self) -> Cyc24 {
        let ad = self.a.mul(&self.d);
        let bc = self.b.mul(&self.c);
        let term1 = ad.sub(&bc);
        let term2 = self.d.sub(&self.b);
        let term3 = self.c.sub(&self.a);
        term1.sub(&term2).add(&term3)
    }

    pub fn is_regular(&self) -> bool {
        !self.corner_det().is_zero()
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ChartTransition4D {
    pub phi1: Cyc24,
    pub phi2: Cyc24,
    pub perm: [usize; 3],
}

impl ChartTransition4D {
    pub fn identity() -> Self {
        Self {
            phi1: Cyc24::rat(ri(1)),
            phi2: Cyc24::rat(ri(1)),
            perm: [0, 1, 2],
        }
    }

    pub fn phases(phi1: Cyc24, phi2: Cyc24) -> Self {
        Self {
            phi1,
            phi2,
            perm: [0, 1, 2],
        }
    }

    pub fn permutation(perm: [usize; 3]) -> Self {
        Self {
            phi1: Cyc24::rat(ri(1)),
            phi2: Cyc24::rat(ri(1)),
            perm,
        }
    }

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

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MultiChartCycle4D {
    pub charts: [AffineCorner4D; 3],
    pub transitions: [ChartTransition4D; 3],
    pub edge_defects: [BigRational; 3],
}

impl MultiChartCycle4D {
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

    pub fn transition_product(&self) -> [[Cyc24; 3]; 3] {
        let t01 = self.transitions[0].transition_matrix();
        let t12 = self.transitions[1].transition_matrix();
        let t20 = self.transitions[2].transition_matrix();
        mul_mat3(&mul_mat3(&t01, &t12), &t20)
    }

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
                },
                BoundaryEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                },
                BoundaryEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                },
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

    pub fn solve_network_simplex_obstruction(
        &self,
        scale: i128,
        base_gap: i128,
    ) -> Result<Phi1Solution, NetworkSimplexError> {
        let (boundary, omega) = self.build_cycle_boundary_and_cochain(scale, base_gap);
        solve_phi1(&boundary, &omega)
    }
}

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

pub fn evaluate_multi_chart_circulation_extension(
    cycle: &MultiChartCycle4D,
    scale: i128,
    base_gap: i128,
) -> Result<MultiChartCirculationReport, NetworkSimplexError> {
    let (boundary, omega) = cycle.build_cycle_boundary_and_cochain(scale, base_gap);
    let phi1_sol = solve_phi1(&boundary, &omega)?;

    let net_circulation: i128 = omega.iter().sum();

    let d_alpha_sum: i128 = boundary
        .edges
        .iter()
        .map(|e| phi1_sol.vertex_potential[e.head] - phi1_sol.vertex_potential[e.tail])
        .sum();

    let dual_gap_zero = phi1_sol.verified_phi1().is_some();

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
