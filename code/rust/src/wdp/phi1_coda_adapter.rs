//! Shared CODA/CODA_GTLA adapter for the exact integer Phi1 solver.
//!
//! `solve_phi1` owns candidate construction. This module converts its exact
//! primal/dual result into the canonical rational certificate, validates a
//! finite primitive-difference carrier, runs `crate::coda::coda_gtla`, and
//! registers only stabilized survivor families. It does not define another
//! obstruction classifier or authority path.

use crate::coda::coda_gtla::{
    bind_domain_evidence, evaluate_exact, validate_primitive_difference, CodaExactInput,
    CodaGtlaEvaluation, CodaGtlaEvaluationError, DomainEvidenceBindingError,
    PrimitiveDifferenceReceiptError,
};
use num_bigint::BigInt;
use num_rational::BigRational;
use omega_functional::gamma2::{ExactCochainComplexQ, ExactGamma2Error};
use omega_functional::phi1::ExactPhi1Certificate;
use omega_homotopy_type_theory::primitive_difference::PrimitiveDifference;
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_epk::residual_families::{
    reconcile_verified, shape_signature_from_exact_complex, FamilyCollision, FamilyRegistry,
    FamilyResolution, ShapeSignatureError,
};
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_types::observer::{Observer, ObserverKind};

use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, Phi1Solution};

#[derive(Debug, PartialEq, Eq)]
struct PotentialDelta {
    same_dimension: bool,
    coordinates: Vec<BigInt>,
}

#[derive(Debug)]
struct PotentialDifference;

impl PrimitiveDifference for PotentialDifference {
    type Carrier = Vec<BigInt>;
    type Diff = PotentialDelta;

    fn delta(&self, left: &Self::Carrier, right: &Self::Carrier) -> Self::Diff {
        PotentialDelta {
            same_dimension: left.len() == right.len(),
            coordinates: left
                .iter()
                .zip(right)
                .map(|(left, right)| left - right)
                .collect(),
        }
    }

    fn zero(&self, difference: &Self::Diff) -> bool {
        difference.same_dimension
            && difference
                .coordinates
                .iter()
                .all(|value| value == &BigInt::from(0))
    }
}

/// Failure in the solver-to-shared-runtime conversion.
#[derive(Debug, thiserror::Error)]
pub enum Phi1CodaAdapterError {
    #[error(transparent)]
    Solver(#[from] NetworkSimplexError),
    #[error("edge {edge} endpoint {endpoint} is outside the {num_vertices}-vertex carrier")]
    InvalidEndpoint {
        edge: usize,
        endpoint: usize,
        num_vertices: usize,
    },
    #[error(transparent)]
    Manifest(#[from] serde_json::Error),
    #[error(transparent)]
    Binding(#[from] DomainEvidenceBindingError),
    #[error(transparent)]
    Primitive(#[from] PrimitiveDifferenceReceiptError),
    #[error(transparent)]
    Complex(#[from] ExactGamma2Error),
    #[error(transparent)]
    Shape(#[from] ShapeSignatureError),
    #[error(transparent)]
    Evaluation(#[from] CodaGtlaEvaluationError),
    #[error(transparent)]
    Family(#[from] FamilyCollision),
}

/// Solver output bound to the sole shared exact obstruction evaluation.
#[derive(Debug)]
pub struct Phi1CodaSolution {
    solution: Phi1Solution,
    evaluation: CodaGtlaEvaluation,
    residual_family: Option<FamilyResolution>,
}

impl Phi1CodaSolution {
    pub fn solution(&self) -> &Phi1Solution {
        &self.solution
    }

    pub fn evaluation(&self) -> &CodaGtlaEvaluation {
        &self.evaluation
    }

    /// Present only for a shared `ClosedResidual` classification.
    pub fn residual_family(&self) -> Option<&FamilyResolution> {
        self.residual_family.as_ref()
    }
}

fn rational(value: i128) -> BigRational {
    BigRational::from_integer(BigInt::from(value))
}

fn validate_endpoints(boundary: &Boundary1) -> Result<(), Phi1CodaAdapterError> {
    for (index, edge) in boundary.edges.iter().enumerate() {
        for endpoint in [edge.tail, edge.head] {
            if endpoint >= boundary.num_vertices {
                return Err(Phi1CodaAdapterError::InvalidEndpoint {
                    edge: index,
                    endpoint,
                    num_vertices: boundary.num_vertices,
                });
            }
        }
    }
    Ok(())
}

/// Pack an exact `solve_phi1` solution into the canonical rational
/// [`ExactPhi1Certificate`] (incidence `d₀`, the minimizing `α*`, primal
/// residual, and dual witness). Shared with the [`super::emitter`] so the
/// constructive Φ₁ path does not re-derive the packing.
pub fn exact_certificate(
    boundary: &Boundary1,
    omega: &[i128],
    solution: &Phi1Solution,
) -> ExactPhi1Certificate {
    let mut d0 = vec![vec![rational(0); boundary.num_vertices]; boundary.edges.len()];
    for (row, edge) in d0.iter_mut().zip(&boundary.edges) {
        row[edge.tail] -= rational(1);
        row[edge.head] += rational(1);
    }

    ExactPhi1Certificate {
        omega: omega.iter().copied().map(rational).collect(),
        d0,
        weights: boundary
            .edges
            .iter()
            .map(|edge| rational(edge.weight))
            .collect(),
        alpha: solution
            .vertex_potential
            .iter()
            .copied()
            .map(rational)
            .collect(),
        primal_residual: solution.z.iter().copied().map(rational).collect(),
        dual_witness: solution
            .reduced_costs
            .iter()
            .copied()
            .map(rational)
            .collect(),
        reported_value: rational(solution.objective),
    }
}

/// Solve one boundary problem and run its exact evidence through the shared
/// CODA/CODA_GTLA runtime. The family registry is consulted before exact replay;
/// only a verified stabilized survivor is reconciled into it.
pub fn solve_phi1_coda(
    boundary: &Boundary1,
    omega: &[i128],
    registry: &mut FamilyRegistry,
) -> Result<Phi1CodaSolution, Phi1CodaAdapterError> {
    validate_endpoints(boundary)?;
    let solution = solve_phi1(boundary, omega)?;
    let certificate = exact_certificate(boundary, omega, &solution);
    let complex = ExactCochainComplexQ::try_new(
        boundary.num_vertices,
        boundary.edges.len(),
        1,
        certificate.d0.clone(),
        vec![vec![rational(0); boundary.edges.len()]],
    )?;

    let signature = shape_signature_from_exact_complex("omega_solvers::phi1_boundary", &complex)?;
    let consultation = registry.consult(signature);

    let carrier_manifest = serde_json::to_vec(&(
        "omega-solvers-phi1-boundary-v1",
        boundary.num_vertices,
        boundary
            .edges
            .iter()
            .map(|edge| (edge.tail, edge.head, edge.weight))
            .collect::<Vec<_>>(),
    ))?;
    let evidence_manifest = serde_json::to_vec(&(
        "omega-solvers-phi1-evidence-v1",
        omega,
        &certificate,
        &complex,
    ))?;
    let binding = bind_domain_evidence(
        "omega_solvers::phi1_boundary",
        &carrier_manifest,
        &evidence_manifest,
    )?;

    let zero = vec![BigInt::from(0); boundary.num_vertices];
    let solved = solution
        .vertex_potential
        .iter()
        .copied()
        .map(BigInt::from)
        .collect();
    let primitive_receipt = validate_primitive_difference(
        &PotentialDifference,
        vec![zero, solved],
        binding.carrier_hash().clone(),
    )?;
    let residual = certificate.primal_residual.clone();
    let evaluation = evaluate_exact(CodaExactInput::new(
        primitive_receipt,
        certificate,
        complex,
        residual,
        binding.into_packet_args(),
    ))?;

    let residual_family = if evaluation.status() == ObstructionDiagnosticClass::ClosedResidual {
        let observer = Observer {
            id: omega_kernel::ObserverId::parse("omega_solvers_phi1_v1")
                .expect("static observer id is canonical"),
            kind: ObserverKind::Custom("solver".to_string()),
        };
        Some(reconcile_verified(
            registry,
            consultation,
            evaluation.phi1(),
            evaluation.gamma2(),
            &observer,
        )?)
    } else {
        None
    };

    Ok(Phi1CodaSolution {
        solution,
        evaluation,
        residual_family,
    })
}
