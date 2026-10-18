
use linear_algebra::exact_field::matrix::{from_rows, multiply_vector};
use linear_algebra::exact_field::pseudoinverse::pseudoinverse;
use linear_algebra::exact_field::ExactFieldError;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use omega_functional::phi1::{ExactPhi1CertificateError, Phi1Functional, VerifiedExactPhi1};
use omega_kernel::{exact_wire, exact_wire_vec};
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1};
use serde::Serialize;

pub const D_SEL_RULE_ID: &str = "d-sel.network-simplex-vertex.v1";

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct DSelReceipt {
    pub rule_id: String,
    pub phi: i128,
    pub delta_irr: Vec<i128>,
    pub potential: Vec<i128>,
    pub dual_witness: Vec<i128>,
    #[serde(with = "exact_wire_vec")]
    pub vertex_load: Vec<BigRational>,
    #[serde(with = "exact_wire")]
    pub mean_load: BigRational,
    #[serde(with = "exact_wire")]
    pub peak_load: BigRational,
}

#[derive(Debug, Clone, PartialEq)]
pub enum DSelError {
    Solver(NetworkSimplexError),
    Certificate(ExactPhi1CertificateError),
    ExactLinearAlgebra(ExactFieldError),
    OmegaLengthMismatch { expected: usize, found: usize },
    EndpointOutOfRange { edge: usize, vertex: usize },
    SelfLoop { edge: usize },
    EmptyCarrier,
}

impl From<NetworkSimplexError> for DSelError {
    fn from(error: NetworkSimplexError) -> Self {
        DSelError::Solver(error)
    }
}

impl From<ExactPhi1CertificateError> for DSelError {
    fn from(error: ExactPhi1CertificateError) -> Self {
        DSelError::Certificate(error)
    }
}

impl From<ExactFieldError> for DSelError {
    fn from(error: ExactFieldError) -> Self {
        DSelError::ExactLinearAlgebra(error)
    }
}

fn defect_loads(
    boundary: &Boundary1,
    delta: &[BigRational],
) -> (Vec<BigRational>, BigRational, BigRational) {
    let mut vertex_load = vec![BigRational::zero(); boundary.num_vertices];
    for (edge, value) in boundary.edges.iter().zip(delta) {
        let magnitude = value.abs();
        vertex_load[edge.tail] += &magnitude;
        vertex_load[edge.head] += &magnitude;
    }
    let total: BigRational = vertex_load.iter().sum();
    let count = BigRational::from_integer(BigInt::from(boundary.num_vertices));
    let mean_load = total / count;
    let peak_load = vertex_load
        .iter()
        .max()
        .cloned()
        .unwrap_or_else(BigRational::zero);
    (vertex_load, mean_load, peak_load)
}

fn integer(value: i128) -> BigRational {
    BigRational::from_integer(BigInt::from(value))
}

fn select_verified(
    boundary: &Boundary1,
    omega: &[i128],
) -> Result<(DSelReceipt, VerifiedExactPhi1), DSelError> {
    if boundary.num_vertices == 0 {
        return Err(DSelError::EmptyCarrier);
    }
    if boundary.edges.len() != omega.len() {
        return Err(DSelError::OmegaLengthMismatch {
            expected: boundary.edges.len(),
            found: omega.len(),
        });
    }
    for (index, edge) in boundary.edges.iter().enumerate() {
        if edge.tail == edge.head {
            return Err(DSelError::SelfLoop { edge: index });
        }
        for vertex in [edge.tail, edge.head] {
            if vertex >= boundary.num_vertices {
                return Err(DSelError::EndpointOutOfRange {
                    edge: index,
                    vertex,
                });
            }
        }
    }

    let solution = solve_phi1(boundary, omega)?;
    let certificate = crate::phi1_coda_adapter::exact_certificate(boundary, omega, &solution);
    let verified = Phi1Functional::verify_exact_certificate(certificate)?;

    let delta: Vec<BigRational> = solution.z.iter().copied().map(integer).collect();
    let (vertex_load, mean_load, peak_load) = defect_loads(boundary, &delta);

    let receipt = DSelReceipt {
        rule_id: D_SEL_RULE_ID.to_string(),
        phi: solution.objective,
        delta_irr: solution.z,
        potential: solution.vertex_potential,
        dual_witness: solution.reduced_costs,
        vertex_load,
        mean_load,
        peak_load,
    };
    Ok((receipt, verified))
}

pub fn select_delta_irr(boundary: &Boundary1, omega: &[i128]) -> Result<DSelReceipt, DSelError> {
    select_verified(boundary, omega).map(|(receipt, _)| receipt)
}

impl DSelReceipt {
    pub fn e7a_lower_bound(&self, lambda2: &BigRational) -> Option<BigRational> {
        if !lambda2.is_positive() {
            return None;
        }
        let denominator = lambda2 + &self.mean_load + &self.peak_load;
        if !denominator.is_positive() {
            return None;
        }
        Some(lambda2 * &self.mean_load / denominator)
    }

    pub fn e7_upper_bound(&self) -> BigRational {
        self.mean_load.clone()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_solvers::solver_lp_phi1_boundary::BoundaryEdge;

    fn unit_edge(tail: usize, head: usize) -> BoundaryEdge {
        BoundaryEdge {
            tail,
            head,
            weight: 1,
        }
    }

    fn q(n: i64, d: i64) -> BigRational {
        BigRational::new(n.into(), d.into())
    }

    #[test]
    fn refuses_self_loop() {
        let boundary = Boundary1 {
            num_vertices: 2,
            edges: vec![unit_edge(0, 0)],
        };
        assert_eq!(
            select_delta_irr(&boundary, &[1]),
            Err(DSelError::SelfLoop { edge: 0 })
        );
    }

    #[test]
    fn refuses_length_mismatch_and_empty_carrier() {
        let boundary = Boundary1 {
            num_vertices: 2,
            edges: vec![unit_edge(0, 1)],
        };
        assert_eq!(
            select_delta_irr(&boundary, &[1, 2]),
            Err(DSelError::OmegaLengthMismatch {
                expected: 1,
                found: 2
            })
        );
        let empty = Boundary1 {
            num_vertices: 0,
            edges: vec![],
        };
        assert_eq!(select_delta_irr(&empty, &[]), Err(DSelError::EmptyCarrier));
        assert_eq!(
            select_delta_irr_l2(&empty, &[]),
            Err(DSelError::EmptyCarrier)
        );
    }

    #[test]
    fn bound_refuses_nonpositive_fiedler_value() {
        let boundary = Boundary1 {
            num_vertices: 2,
            edges: vec![unit_edge(0, 1)],
        };
        let receipt = select_delta_irr(&boundary, &[3]).expect("select");
        assert_eq!(receipt.e7a_lower_bound(&q(0, 1)), None);
        assert_eq!(receipt.e7a_lower_bound(&q(-1, 1)), None);
    }

    #[test]
    fn loads_are_exact_and_serialize_canonically() {
        let boundary = Boundary1 {
            num_vertices: 3,
            edges: vec![unit_edge(0, 1), unit_edge(1, 2), unit_edge(2, 0)],
        };
        let receipt = select_delta_irr(&boundary, &[1, 1, 1]).expect("select");
        assert_eq!(receipt.mean_load, q(2, 1));
        assert_eq!(receipt.peak_load, q(2, 1));
        assert_eq!(receipt.e7_upper_bound(), q(2, 1));
        assert_eq!(receipt.e7a_lower_bound(&q(3, 1)), Some(q(6, 7)));
        let json = serde_json::to_value(&receipt).expect("serialize");
        assert_eq!(json["mean_load"], serde_json::json!("2"));
        assert_eq!(json["peak_load"], serde_json::json!("2"));
        assert_eq!(json["vertex_load"], serde_json::json!(["2", "2", "2"]));

        let path = Boundary1 {
            num_vertices: 4,
            edges: vec![unit_edge(0, 1)],
        };
        let l2 = select_delta_irr_l2(&path, &[1]).expect("select l2");
        assert_eq!(l2.mean_load, q(0, 1));
        let star = Boundary1 {
            num_vertices: 4,
            edges: vec![unit_edge(0, 1), unit_edge(1, 2), unit_edge(2, 0)],
        };
        let r = select_delta_irr(&star, &[1, 1, 1]).expect("select");
        assert_eq!(r.mean_load, q(3, 2));
        let json = serde_json::to_value(&r).expect("serialize");
        assert_eq!(json["mean_load"], serde_json::json!("3/2"));
        assert_eq!(json["vertex_load"], serde_json::json!(["2", "2", "2", "0"]));
    }

    #[test]
    fn harmonic_selection_decides_l1_optimality_exactly() {
        let c3 = Boundary1 {
            num_vertices: 3,
            edges: vec![unit_edge(0, 1), unit_edge(1, 2), unit_edge(2, 0)],
        };
        let receipt = select_delta_irr_l2(&c3, &[3, 0, 0]).expect("select l2");
        assert_eq!(receipt.delta_harmonic, vec![q(1, 1); 3]);
        assert_eq!(receipt.phi_l1_min, q(3, 1));
        assert!(receipt.is_l1_optimal);
        let sealed = receipt.optimality_certificate.as_ref().expect("sealed");
        assert_eq!(sealed.value(), &q(3, 1));
        assert_eq!(sealed.primal_residual(), receipt.delta_harmonic.as_slice());

        let bowtie = Boundary1 {
            num_vertices: 4,
            edges: vec![
                unit_edge(0, 1),
                unit_edge(1, 2),
                unit_edge(2, 0),
                unit_edge(1, 3),
                unit_edge(3, 2),
            ],
        };
        let receipt = select_delta_irr_l2(&bowtie, &[0, 1, 0, 0, 0]).expect("select l2");
        assert_eq!(receipt.phi_l1_min, q(1, 1));
        assert!(receipt.l1_of_harmonic > receipt.phi_l1_min);
        assert!(!receipt.is_l1_optimal);
        assert!(receipt.optimality_certificate.is_none());
    }
}


pub const D_SEL_L2_RULE_ID: &str = "d-sel-l2.harmonic-projection.v1";

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct DSelL2Receipt {
    pub rule_id: String,
    #[serde(with = "exact_wire_vec")]
    pub harmonic_potential: Vec<BigRational>,
    #[serde(with = "exact_wire_vec")]
    pub delta_harmonic: Vec<BigRational>,
    #[serde(with = "exact_wire")]
    pub l1_of_harmonic: BigRational,
    #[serde(with = "exact_wire")]
    pub phi_l1_min: BigRational,
    pub is_l1_optimal: bool,
    #[serde(skip)]
    pub optimality_certificate: Option<VerifiedExactPhi1>,
    #[serde(with = "exact_wire_vec")]
    pub vertex_load: Vec<BigRational>,
    #[serde(with = "exact_wire")]
    pub mean_load: BigRational,
    #[serde(with = "exact_wire")]
    pub peak_load: BigRational,
}

pub fn select_delta_irr_l2(
    boundary: &Boundary1,
    omega: &[i128],
) -> Result<DSelL2Receipt, DSelError> {
    let (_, verified) = select_verified(boundary, omega)?;
    let certificate = verified.certificate();
    let phi_l1_min = verified.value().clone();

    let harmonic_potential = if certificate.d0.is_empty() {
        vec![BigRational::zero(); boundary.num_vertices]
    } else {
        let d0 = from_rows(certificate.d0.clone())?;
        let d0_plus = pseudoinverse(&d0)?;
        multiply_vector(&d0_plus, &certificate.omega)?
    };

    let (delta_harmonic, l1_of_harmonic) = Phi1Functional::evaluate_representative(
        &certificate.omega,
        &certificate.d0,
        &certificate.weights,
        &harmonic_potential,
    )?;

    let optimality_certificate = match Phi1Functional::evaluate_exact_witness(
        &certificate.omega,
        &certificate.d0,
        &certificate.weights,
        &harmonic_potential,
        &certificate.dual_witness,
    ) {
        Ok(sealed) => Some(sealed),
        Err(ExactPhi1CertificateError::DualValueMismatch) => None,
        Err(other) => return Err(other.into()),
    };
    let is_l1_optimal = optimality_certificate.is_some();

    let (vertex_load, mean_load, peak_load) = defect_loads(boundary, &delta_harmonic);

    Ok(DSelL2Receipt {
        rule_id: D_SEL_L2_RULE_ID.to_string(),
        harmonic_potential,
        delta_harmonic,
        l1_of_harmonic,
        phi_l1_min,
        is_l1_optimal,
        optimality_certificate,
        vertex_load,
        mean_load,
        peak_load,
    })
}
