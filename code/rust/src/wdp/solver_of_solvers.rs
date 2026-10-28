
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};

use crate::coda::coda_gtla::{
    bind_domain_evidence, evaluate_exact, validate_primitive_difference, CodaExactInput,
    CodaGtlaEvaluation, CodaGtlaEvaluationError, DomainEvidenceBindingError,
    PrimitiveDifferenceReceiptError,
};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::{ExactLinearAlgebraError, ExactRowReduction};
use tfqm_functional::gamma2::ExactCochainComplexQ;
use tfqm_functional::phi1::{ExactPhi1Certificate, Phi1Functional, VerifiedExactPhi1};
use tfqm_homotopy_type_theory::primitive_difference::PrimitiveDifference;
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_types::authority::AuthorityEffect;

use crate::phi1_coda_adapter::exact_certificate;
use omega_solvers::solver_lp_exact_simplex::{solve_weighted_l1_projection, L1LpError};
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

pub const MAX_PROJECTION_EDGES: usize = 4096;

const DOMAIN: &str = "crate::solver_of_solvers";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteCarrier2 {
    pub num_vertices: usize,
    pub edges: Vec<CarrierEdge>,
    pub faces: Vec<(usize, usize, usize)>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CarrierEdge {
    pub tail: usize,
    pub head: usize,
    pub weight: i128,
}

#[derive(Debug, thiserror::Error)]
pub enum SolveRefusal {
    #[error("representation invalid: {0}")]
    RepresentationInvalid(String),
    #[error("projection budget: {edges} edges exceeds the exact-enumeration fence of {max}")]
    SizeBudgetExceeded { edges: usize, max: usize },
    #[error(transparent)]
    Solver(#[from] NetworkSimplexError),
    #[error(transparent)]
    Evaluation(#[from] CodaGtlaEvaluationError),
    #[error(transparent)]
    Binding(#[from] DomainEvidenceBindingError),
    #[error(transparent)]
    Primitive(#[from] PrimitiveDifferenceReceiptError),
    #[error("exact linear algebra: {0:?}")]
    Linear(ExactLinearAlgebraError),
    #[error("projection stage found no replay-certifiable minimizer: {0}")]
    JointCertificateSynthesis(String),
    #[error(transparent)]
    Manifest(#[from] serde_json::Error),
    #[error(transparent)]
    Lp(#[from] L1LpError),
}

impl From<ExactLinearAlgebraError> for SolveRefusal {
    fn from(value: ExactLinearAlgebraError) -> Self {
        SolveRefusal::Linear(value)
    }
}

#[derive(Debug)]
pub struct SolveReceipt {
    gauge: CodaGtlaEvaluation,
    joint: Option<VerifiedExactPhi1>,
    closed: Option<ClosedProjection>,
    normal_form_eval: Option<CodaGtlaEvaluation>,
    normal_form: Vec<BigRational>,
    b1_over_q: usize,
    authority_effect: AuthorityEffect,
}

impl SolveReceipt {
    pub fn gauge(&self) -> &CodaGtlaEvaluation {
        &self.gauge
    }

    pub fn joint(&self) -> Option<&VerifiedExactPhi1> {
        self.joint.as_ref()
    }

    pub fn closed(&self) -> Option<&VerifiedExactPhi1> {
        self.closed
            .as_ref()
            .map(|projection| &projection.outcome.witness)
    }

    pub fn final_evaluation(&self) -> &CodaGtlaEvaluation {
        self.normal_form_eval.as_ref().unwrap_or(&self.gauge)
    }

    pub fn status(&self) -> ObstructionDiagnosticClass {
        self.final_evaluation().status()
    }

    pub fn normal_form(&self) -> &[BigRational] {
        &self.normal_form
    }

    pub fn b1_over_q(&self) -> usize {
        self.b1_over_q
    }

    pub fn is_closed_class_survivor(&self) -> bool {
        self.status() == ObstructionDiagnosticClass::ClosedResidual && self.b1_over_q > 0
    }

    pub fn span_distance(&self) -> &BigRational {
        match &self.joint {
            Some(witness) => witness.value(),
            None => self.gauge.phi1().value(),
        }
    }

    pub fn closure_premium(&self) -> BigRational {
        match &self.closed {
            Some(projection) => {
                projection.outcome.witness.value().clone() - self.span_distance().clone()
            }
            None => BigRational::zero(),
        }
    }

    pub fn authority_effect(&self) -> &AuthorityEffect {
        &self.authority_effect
    }
}

#[derive(Debug, PartialEq, Eq)]
struct RationalDelta {
    same_dimension: bool,
    coordinates: Vec<BigRational>,
}

#[derive(Debug)]
struct ResidualDifference;

impl PrimitiveDifference for ResidualDifference {
    type Carrier = Vec<BigRational>;
    type Diff = RationalDelta;

    fn delta(&self, left: &Self::Carrier, right: &Self::Carrier) -> Self::Diff {
        RationalDelta {
            same_dimension: left.len() == right.len(),
            coordinates: left
                .iter()
                .zip(right)
                .map(|(left, right)| left.clone() - right.clone())
                .collect(),
        }
    }

    fn zero(&self, difference: &Self::Diff) -> bool {
        difference.same_dimension && difference.coordinates.iter().all(|value| value.is_zero())
    }
}

fn rational(value: i128) -> BigRational {
    BigRational::from_integer(BigInt::from(value))
}

fn face_row(
    carrier: &FiniteCarrier2,
    face: (usize, usize, usize),
) -> Result<Vec<BigRational>, SolveRefusal> {
    let (u, v, w) = face;
    let mut row = vec![BigRational::zero(); carrier.edges.len()];
    for (x, y) in [(u, v), (v, w), (w, u)] {
        let mut found = false;
        for (index, edge) in carrier.edges.iter().enumerate() {
            if edge.tail == x && edge.head == y {
                row[index] += BigRational::from_integer(BigInt::from(1));
                found = true;
                break;
            }
            if edge.tail == y && edge.head == x {
                row[index] -= BigRational::from_integer(BigInt::from(1));
                found = true;
                break;
            }
        }
        if !found {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "face ({u}, {v}, {w}) side ({x}, {y}) is not a declared edge"
            )));
        }
    }
    Ok(row)
}

fn validate_carrier(carrier: &FiniteCarrier2, omega: &[i128]) -> Result<(), SolveRefusal> {
    if carrier.edges.is_empty() {
        return Err(SolveRefusal::RepresentationInvalid(
            "carrier declares no edges".to_string(),
        ));
    }
    if omega.len() != carrier.edges.len() {
        return Err(SolveRefusal::RepresentationInvalid(format!(
            "residual has {} coordinates but the carrier declares {} edges",
            omega.len(),
            carrier.edges.len()
        )));
    }
    if carrier.num_vertices + carrier.faces.len() > MAX_PROJECTION_EDGES {
        return Err(SolveRefusal::SizeBudgetExceeded {
            edges: carrier.num_vertices + carrier.faces.len(),
            max: MAX_PROJECTION_EDGES,
        });
    }
    let mut seen_pairs: Vec<(usize, usize)> = Vec::with_capacity(carrier.edges.len());
    for (index, edge) in carrier.edges.iter().enumerate() {
        if edge.tail >= carrier.num_vertices || edge.head >= carrier.num_vertices {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "edge {index} endpoint outside the {}-vertex carrier",
                carrier.num_vertices
            )));
        }
        if edge.tail == edge.head {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "edge {index} is a self-loop ({} -> {}); simplicial edges need distinct endpoints",
                edge.tail, edge.head
            )));
        }
        if edge.weight <= 0 {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "edge {index} weight {} is not strictly positive",
                edge.weight
            )));
        }
        let unordered = (edge.tail.min(edge.head), edge.tail.max(edge.head));
        if seen_pairs.contains(&unordered) {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "edge {index} duplicates the unordered pair {unordered:?} (parallel or \
                 reversed duplicate); face incidence would depend on list order"
            )));
        }
        seen_pairs.push(unordered);
    }
    let mut seen_faces: Vec<[usize; 3]> = Vec::with_capacity(carrier.faces.len());
    for &(u, v, w) in &carrier.faces {
        for vertex in [u, v, w] {
            if vertex >= carrier.num_vertices {
                return Err(SolveRefusal::RepresentationInvalid(format!(
                    "face ({u}, {v}, {w}) vertex outside the {}-vertex carrier",
                    carrier.num_vertices
                )));
            }
        }
        if u == v || v == w || u == w {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "face ({u}, {v}, {w}) is degenerate (repeated vertex)"
            )));
        }
        let mut sorted = [u, v, w];
        sorted.sort_unstable();
        if seen_faces.contains(&sorted) {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "face ({u}, {v}, {w}) duplicates an already-declared 2-cell {sorted:?}"
            )));
        }
        seen_faces.push(sorted);
    }
    Ok(())
}

fn boundary1(carrier: &FiniteCarrier2) -> Boundary1 {
    Boundary1 {
        num_vertices: carrier.num_vertices,
        edges: carrier
            .edges
            .iter()
            .map(|edge| BoundaryEdge {
                tail: edge.tail,
                head: edge.head,
                weight: edge.weight,
            })
            .collect(),
    }
}

pub(crate) fn d1_rows_for_binding(
    carrier: &FiniteCarrier2,
) -> Result<Vec<Vec<BigRational>>, SolveRefusal> {
    d1_rows(carrier)
}

fn d1_rows(carrier: &FiniteCarrier2) -> Result<Vec<Vec<BigRational>>, SolveRefusal> {
    carrier
        .faces
        .iter()
        .map(|&face| face_row(carrier, face))
        .collect()
}

fn weighted_l1(z: &[BigRational], weights: &[BigRational]) -> BigRational {
    tfqm_functional::phi1::Phi1Functional::weighted_l1_rational(weights, z)
        .expect("validated carrier gives equal residual and weight dimensions")
}

fn matrix_from_rows(rows: &[Vec<BigRational>]) -> Result<BasicMatrix<BigRational>, SolveRefusal> {
    let height = rows.len();
    let width = rows.first().map(Vec::len).unwrap_or(0);
    let data: Vec<BigRational> = rows.iter().flat_map(|row| row.iter().cloned()).collect();
    BasicMatrix::from_row_major(height, width, data).map_err(|error| {
        SolveRefusal::RepresentationInvalid(format!("matrix construction failed: {error:?}"))
    })
}

fn exact_rank(rows: &[Vec<BigRational>]) -> Result<usize, SolveRefusal> {
    if rows.is_empty() || rows[0].is_empty() {
        return Ok(0);
    }
    Ok(matrix_from_rows(rows)?.rank()?)
}

fn rref_solve(
    rows: &[Vec<BigRational>],
    rhs: &[BigRational],
) -> Result<Option<Vec<BigRational>>, SolveRefusal> {
    let width = rows.first().map(Vec::len).unwrap_or(0);
    if rows.is_empty() {
        return Ok(Some(Vec::new()));
    }
    let augmented: Vec<Vec<BigRational>> = rows
        .iter()
        .zip(rhs)
        .map(|(row, b)| {
            let mut extended = row.clone();
            extended.push(b.clone());
            extended
        })
        .collect();
    let reduction = matrix_from_rows(&augmented)?.rank_and_rref()?;
    if reduction.pivot_columns().contains(&width) {
        return Ok(None);
    }
    let mut solution = vec![BigRational::zero(); width];
    let rref = reduction.rref();
    for (row_index, &pivot_col) in reduction.pivot_columns().iter().enumerate() {
        let value = rref.get(row_index, width).map_err(|error| {
            SolveRefusal::RepresentationInvalid(format!("rref read failed: {error:?}"))
        })?;
        solution[pivot_col] = value;
    }
    Ok(Some(solution))
}

#[allow(dead_code)]
fn for_each_subset<F: FnMut(&[usize]) -> Result<bool, SolveRefusal>>(
    n: usize,
    k: usize,
    mut visit: F,
) -> Result<(), SolveRefusal> {
    if k > n {
        return Ok(());
    }
    let mut indices: Vec<usize> = (0..k).collect();
    loop {
        if !visit(&indices)? {
            return Ok(());
        }
        let mut position = k;
        loop {
            if position == 0 {
                return Ok(());
            }
            position -= 1;
            if indices[position] != position + n - k {
                break;
            }
            if position == 0 {
                return Ok(());
            }
        }
        indices[position] += 1;
        for later in position + 1..k {
            indices[later] = indices[later - 1] + 1;
        }
    }
}

#[derive(Debug)]
struct ProjectionOutcome {
    witness: VerifiedExactPhi1,
    residual: Vec<BigRational>,
    dual: Vec<BigRational>,
}

fn exact_l1_projection(
    target: &[BigRational],
    weights: &[BigRational],
    map_rows: &[Vec<BigRational>],
) -> Result<ProjectionOutcome, SolveRefusal> {
    let m = target.len();
    if m > MAX_PROJECTION_EDGES {
        return Err(SolveRefusal::SizeBudgetExceeded {
            edges: m,
            max: MAX_PROJECTION_EDGES,
        });
    }
    let k = map_rows.first().map(Vec::len).unwrap_or(0);
    let budget = 64 * (m + k) + 1024;
    let solution = solve_weighted_l1_projection(target, weights, map_rows, budget)?;

    let certificate = ExactPhi1Certificate {
        omega: target.to_vec(),
        d0: map_rows.to_vec(),
        weights: weights.to_vec(),
        alpha: solution.coefficients,
        primal_residual: solution.residual.clone(),
        dual_witness: solution.dual.clone(),
        reported_value: solution.value,
    };
    let witness = Phi1Functional::verify_exact_certificate(certificate).map_err(|error| {
        SolveRefusal::JointCertificateSynthesis(format!(
            "the exact LP optimum failed replay: {error}"
        ))
    })?;

    Ok(ProjectionOutcome {
        witness,
        residual: solution.residual,
        dual: solution.dual,
    })
}

#[allow(dead_code)]
fn synthesize_dual(
    map_rows: &[Vec<BigRational>],
    z: &[BigRational],
    weights: &[BigRational],
) -> Result<Option<Vec<BigRational>>, SolveRefusal> {
    let m = z.len();
    let columns = map_rows.first().map(Vec::len).unwrap_or(0);
    let support: Vec<usize> = (0..m).filter(|&edge| !z[edge].is_zero()).collect();
    let zero_set: Vec<usize> = (0..m).filter(|&edge| z[edge].is_zero()).collect();

    let mut fixed = vec![BigRational::zero(); m];
    for &edge in &support {
        let sign = if z[edge].is_positive() {
            BigRational::from_integer(BigInt::from(1))
        } else {
            BigRational::from_integer(BigInt::from(-1))
        };
        fixed[edge] = weights[edge].clone() * sign;
    }

    let rows: Vec<Vec<BigRational>> = (0..columns)
        .map(|column| {
            zero_set
                .iter()
                .map(|&edge| map_rows[edge][column].clone())
                .collect()
        })
        .collect();
    let rhs: Vec<BigRational> = (0..columns)
        .map(|column| {
            -support
                .iter()
                .map(|&edge| map_rows[edge][column].clone() * fixed[edge].clone())
                .sum::<BigRational>()
        })
        .collect();

    let free_values = if columns == 0 {
        vec![BigRational::zero(); zero_set.len()]
    } else {
        match rref_solve(&rows, &rhs)? {
            Some(values) => values,
            None => return Ok(None),
        }
    };
    let mut dual = fixed;
    for (position, &edge) in zero_set.iter().enumerate() {
        dual[edge] = free_values[position].clone();
    }
    for edge in 0..m {
        if dual[edge].abs() > weights[edge] {
            return Ok(None);
        }
    }
    Ok(Some(dual))
}

fn augmented_rows(
    carrier: &FiniteCarrier2,
    d0_rows: &[Vec<BigRational>],
    d1: &[Vec<BigRational>],
) -> Vec<Vec<BigRational>> {
    let m = carrier.edges.len();
    let n = carrier.num_vertices;
    let f = carrier.faces.len();
    (0..m)
        .map(|edge| {
            let mut row = Vec::with_capacity(n + f);
            row.extend(d0_rows[edge].iter().cloned());
            for face_row in d1 {
                row.push(face_row[edge].clone());
            }
            row
        })
        .collect()
}

#[derive(Debug)]
struct ClosedProjection {
    outcome: ProjectionOutcome,
    normal_form: Vec<BigRational>,
    gamma0: Vec<BigRational>,
    y0: Vec<BigRational>,
    kernel: Vec<Vec<BigRational>>,
    shifted: Vec<BigRational>,
}

fn closed_projection(
    omega_q: &[BigRational],
    weights: &[BigRational],
    aug_rows: &[Vec<BigRational>],
    d1: &[Vec<BigRational>],
) -> Result<ClosedProjection, SolveRefusal> {
    let m = omega_q.len();
    let columns = aug_rows.first().map(Vec::len).unwrap_or(0);

    let bf_rows: Vec<Vec<BigRational>> = d1
        .iter()
        .map(|face| {
            (0..columns)
                .map(|column| {
                    (0..m)
                        .map(|edge| face[edge].clone() * aug_rows[edge][column].clone())
                        .sum()
                })
                .collect()
        })
        .collect();
    let t: Vec<BigRational> = d1
        .iter()
        .map(|face| {
            (0..m)
                .map(|edge| face[edge].clone() * omega_q[edge].clone())
                .sum()
        })
        .collect();

    let gamma0 = match rref_solve(&bf_rows, &t)? {
        Some(gamma0) => gamma0,
        None => {
            return Err(SolveRefusal::JointCertificateSynthesis(
                "closed system (d1·B)γ = d1ω reported inconsistent — contrary to rational feasibility for \
                 a span containing im(d1ᵀ); implementation contradiction"
                    .to_string(),
            ));
        }
    };
    let y0: Vec<BigRational> = (0..m)
        .map(|edge| {
            (0..columns)
                .map(|column| aug_rows[edge][column].clone() * gamma0[column].clone())
                .sum()
        })
        .collect();
    let shifted: Vec<BigRational> = omega_q
        .iter()
        .zip(&y0)
        .map(|(observed, base)| observed.clone() - base.clone())
        .collect();

    let kernel = matrix_from_rows(&bf_rows)?.kernel_basis()?;
    let v_columns: Vec<Vec<BigRational>> = kernel
        .vectors()
        .iter()
        .map(|k| {
            (0..m)
                .map(|edge| {
                    (0..columns)
                        .map(|column| aug_rows[edge][column].clone() * k[column].clone())
                        .sum()
                })
                .collect()
        })
        .collect();
    let v_rows: Vec<Vec<BigRational>> = (0..m)
        .map(|edge| {
            v_columns
                .iter()
                .map(|column| column[edge].clone())
                .collect()
        })
        .collect();

    let outcome = exact_l1_projection(&shifted, weights, &v_rows)?;
    let normal_form: Vec<BigRational> = outcome.residual.clone();

    for face in d1 {
        let curl: BigRational = (0..m)
            .map(|edge| face[edge].clone() * normal_form[edge].clone())
            .sum();
        if !curl.is_zero() {
            return Err(SolveRefusal::JointCertificateSynthesis(
                "closed projection returned a non-closed representative".to_string(),
            ));
        }
    }

    Ok(ClosedProjection {
        outcome,
        normal_form,
        gamma0,
        y0,
        kernel: kernel.vectors().to_vec(),
        shifted,
    })
}

fn evaluate(
    stage: &str,
    carrier: &FiniteCarrier2,
    certificate: ExactPhi1Certificate,
    complex: ExactCochainComplexQ,
    bound_residual: &[BigRational],
) -> Result<CodaGtlaEvaluation, SolveRefusal> {
    let carrier_manifest = serde_json::to_vec(&(
        "omega-solvers-sos-carrier-v1",
        carrier.num_vertices,
        carrier
            .edges
            .iter()
            .map(|edge| (edge.tail, edge.head, edge.weight))
            .collect::<Vec<_>>(),
        carrier.faces.clone(),
    ))?;
    let evidence_manifest = serde_json::to_vec(&(
        "omega-solvers-sos-evidence-v1",
        stage,
        &certificate,
        &complex,
    ))?;
    let binding = bind_domain_evidence(DOMAIN, &carrier_manifest, &evidence_manifest)?;

    let zero = vec![BigRational::zero(); bound_residual.len()];
    let primitive_receipt = validate_primitive_difference(
        &ResidualDifference,
        vec![zero, bound_residual.to_vec()],
        binding.carrier_hash().clone(),
    )?;
    let residual = certificate.primal_residual.clone();
    Ok(evaluate_exact(CodaExactInput::new(
        primitive_receipt,
        certificate,
        complex,
        residual,
        binding.into_packet_args(),
    ))?)
}

pub fn solve(carrier: &FiniteCarrier2, omega: &[i128]) -> Result<SolveReceipt, SolveRefusal> {
    validate_carrier(carrier, omega)?;

    let boundary = boundary1(carrier);
    let d1 = d1_rows(carrier)?;
    let weights: Vec<BigRational> = carrier
        .edges
        .iter()
        .map(|edge| rational(edge.weight))
        .collect();
    let omega_q: Vec<BigRational> = omega.iter().copied().map(rational).collect();

    let solution = solve_phi1(&boundary, omega)?;
    let gauge_certificate = exact_certificate(&boundary, omega, &solution);
    let d0_rows: Vec<Vec<BigRational>> = gauge_certificate.d0.clone();
    let complex = ExactCochainComplexQ::try_new(
        carrier.num_vertices,
        carrier.edges.len(),
        d1.len(),
        d0_rows.clone(),
        d1.clone(),
    )
    .map_err(CodaGtlaEvaluationError::from)?;
    let gauge = evaluate(
        "gauge",
        carrier,
        gauge_certificate,
        complex.clone(),
        &omega_q,
    )?;

    let rank_d0 = exact_rank(&d0_rows)?;
    let rank_faces = if carrier.faces.is_empty() {
        0
    } else {
        exact_rank(&d1)?
    };
    let b1_over_q = carrier.edges.len() - rank_d0 - rank_faces;

    let gauge_is_exact = gauge.status() == ObstructionDiagnosticClass::ExactRepair;

    if carrier.faces.is_empty() || gauge_is_exact {
        let normal_form = gauge.phi1().primal_residual().to_vec();
        return Ok(SolveReceipt {
            gauge,
            joint: None,
            closed: None,
            normal_form_eval: None,
            normal_form,
            b1_over_q,
            authority_effect: AuthorityEffect::None,
        });
    }

    let aug = augmented_rows(carrier, &d0_rows, &d1);
    let joint = exact_l1_projection(&omega_q, &weights, &aug)?;
    let v_star = joint.witness.value().clone();

    if v_star.is_zero() {
        let z2 = joint.residual.clone();
        let zero_dual = vec![BigRational::zero(); carrier.edges.len()];
        let normal_form_certificate = ExactPhi1Certificate {
            omega: z2.clone(),
            d0: d0_rows,
            weights: weights.clone(),
            alpha: vec![BigRational::zero(); carrier.num_vertices],
            primal_residual: z2.clone(),
            dual_witness: zero_dual,
            reported_value: BigRational::zero(),
        };
        let normal_form_eval = evaluate(
            "normal-form",
            carrier,
            normal_form_certificate,
            complex,
            &z2,
        )?;
        return Ok(SolveReceipt {
            gauge,
            joint: Some(joint.witness),
            closed: None,
            normal_form_eval: Some(normal_form_eval),
            normal_form: z2,
            b1_over_q,
            authority_effect: AuthorityEffect::None,
        });
    }

    let closed = closed_projection(&omega_q, &weights, &aug, &d1)?;
    let v_closed = closed.outcome.witness.value().clone();

    let (normal_form, nf_dual, nf_value) = if v_closed == v_star {
        (
            closed.normal_form.clone(),
            closed.outcome.dual.clone(),
            v_closed.clone(),
        )
    } else {
        (
            joint.residual.clone(),
            joint.dual.clone(),
            weighted_l1(&joint.residual, &weights),
        )
    };

    let normal_form_certificate = ExactPhi1Certificate {
        omega: normal_form.clone(),
        d0: d0_rows,
        weights: weights.clone(),
        alpha: vec![BigRational::zero(); carrier.num_vertices],
        primal_residual: normal_form.clone(),
        dual_witness: nf_dual,
        reported_value: nf_value,
    };
    let normal_form_eval = evaluate(
        "normal-form",
        carrier,
        normal_form_certificate,
        complex,
        &normal_form,
    )?;

    let expected_closed = v_closed == v_star;
    let classified = normal_form_eval.status();
    let consistent = match classified {
        ObstructionDiagnosticClass::ExactRepair => false,
        ObstructionDiagnosticClass::ClosedResidual => expected_closed,
        ObstructionDiagnosticClass::ActiveClosureFailure => !expected_closed,
    };
    if !consistent {
        return Err(SolveRefusal::JointCertificateSynthesis(format!(
            "value comparison and trichotomy disagree: expected_closed={expected_closed}, \
             classified={classified:?}"
        )));
    }

    let receipt = SolveReceipt {
        gauge,
        joint: Some(joint.witness),
        closed: Some(closed),
        normal_form_eval: Some(normal_form_eval),
        normal_form,
        b1_over_q,
        authority_effect: AuthorityEffect::None,
    };
    replay_solve(carrier, omega, &receipt)?;
    Ok(receipt)
}


#[derive(Debug)]
pub struct ReplayedSolve<'a> {
    receipt: &'a SolveReceipt,
}

impl<'a> ReplayedSolve<'a> {
    pub fn receipt(&self) -> &'a SolveReceipt {
        self.receipt
    }
}

pub fn replay_solve<'a>(
    carrier: &FiniteCarrier2,
    omega: &[i128],
    receipt: &'a SolveReceipt,
) -> Result<ReplayedSolve<'a>, SolveRefusal> {
    let fail = |what: &str| {
        Err(SolveRefusal::JointCertificateSynthesis(format!(
            "replay refused: {what}"
        )))
    };

    validate_carrier(carrier, omega)?;
    let d1 = d1_rows(carrier)?;
    let omega_q: Vec<BigRational> = omega.iter().copied().map(rational).collect();
    let weights: Vec<BigRational> = carrier
        .edges
        .iter()
        .map(|edge| rational(edge.weight))
        .collect();
    let boundary = boundary1(carrier);
    let d0_rows: Vec<Vec<BigRational>> = {
        let mut rows = vec![vec![BigRational::zero(); carrier.num_vertices]; carrier.edges.len()];
        for (row, edge) in rows.iter_mut().zip(&boundary.edges) {
            row[edge.tail] -= BigRational::from_integer(BigInt::from(1));
            row[edge.head] += BigRational::from_integer(BigInt::from(1));
        }
        rows
    };
    let m = carrier.edges.len();

    let gauge_phi1 = receipt.gauge.phi1();
    if gauge_phi1.d0() != d0_rows.as_slice() {
        return fail("gauge certificate d0 is not this carrier's incidence map");
    }
    if weighted_l1(gauge_phi1.primal_residual(), &weights) != *gauge_phi1.value() {
        return fail("gauge certificate value is not the carrier-weighted norm of its residual");
    }
    let alpha = gauge_phi1.alpha();
    for edge in 0..m {
        let repair: BigRational = (0..carrier.num_vertices)
            .map(|vertex| d0_rows[edge][vertex].clone() * alpha[vertex].clone())
            .sum();
        if gauge_phi1.primal_residual()[edge] != omega_q[edge].clone() - repair {
            return fail("gauge certificate residual does not reproduce ω − d0·α on this carrier");
        }
    }

    if let Some(joint) = &receipt.joint {
        let aug = augmented_rows(carrier, &d0_rows, &d1);
        if joint.d0() != aug.as_slice() {
            return fail("joint certificate map is not [d0 | ∂2] of this carrier");
        }
        let joint_alpha = joint.alpha();
        for edge in 0..m {
            let repair: BigRational = (0..aug[edge].len())
                .map(|column| aug[edge][column].clone() * joint_alpha[column].clone())
                .sum();
            if joint.primal_residual()[edge] != omega_q[edge].clone() - repair {
                return fail("joint certificate residual does not reproduce ω − Bγ");
            }
        }
        let v_star = joint.value();
        if weighted_l1(joint.primal_residual(), &weights) != *v_star {
            return fail(
                "joint certificate value is not the carrier-weighted norm of its residual",
            );
        }

        match &receipt.closed {
            Some(closed) => {
                let columns = aug.first().map(Vec::len).unwrap_or(0);
                for (face_index, face) in d1.iter().enumerate() {
                    let lhs: BigRational = (0..columns)
                        .map(|column| {
                            let bf: BigRational = (0..m)
                                .map(|edge| face[edge].clone() * aug[edge][column].clone())
                                .sum();
                            bf * closed.gamma0[column].clone()
                        })
                        .sum();
                    let rhs: BigRational = (0..m)
                        .map(|edge| face[edge].clone() * omega_q[edge].clone())
                        .sum();
                    if lhs != rhs {
                        return fail("closed glue: (d1·B)γ0 ≠ d1·ω");
                    }
                    let _ = face_index;
                }
                for edge in 0..m {
                    let y: BigRational = (0..columns)
                        .map(|column| aug[edge][column].clone() * closed.gamma0[column].clone())
                        .sum();
                    if closed.y0[edge] != y {
                        return fail("closed glue: y0 ≠ B·γ0");
                    }
                    if closed.shifted[edge] != omega_q[edge].clone() - closed.y0[edge].clone() {
                        return fail("closed glue: shifted ≠ ω − y0");
                    }
                }
                let closed_witness = &closed.outcome.witness;
                let witness_rows = closed_witness.d0();
                if witness_rows.len() != m {
                    return fail("closed certificate map has the wrong height");
                }
                for (j, k) in closed.kernel.iter().enumerate() {
                    for face in &d1 {
                        let bfk: BigRational = (0..columns)
                            .map(|column| {
                                let bf: BigRational = (0..m)
                                    .map(|edge| face[edge].clone() * aug[edge][column].clone())
                                    .sum();
                                bf * k[column].clone()
                            })
                            .sum();
                        if !bfk.is_zero() {
                            return fail("closed glue: a kernel vector does not annihilate d1·B");
                        }
                    }
                    for edge in 0..m {
                        let v: BigRational = (0..columns)
                            .map(|column| aug[edge][column].clone() * k[column].clone())
                            .sum();
                        if witness_rows[edge][j] != v {
                            return fail("closed glue: certificate column ≠ B·k");
                        }
                    }
                }
                if closed_witness.primal_residual() != closed.normal_form.as_slice() {
                    return fail("closed certificate residual ≠ recorded closed normal form");
                }
                for edge in 0..m {
                    let expected = closed.shifted[edge].clone();
                    let mapped: BigRational = (0..closed.kernel.len())
                        .map(|j| witness_rows[edge][j].clone() * closed_witness.alpha()[j].clone())
                        .sum();
                    if closed_witness.primal_residual()[edge] != expected - mapped {
                        return fail("closed certificate target ≠ shifted residual");
                    }
                }
                for face in &d1 {
                    let curl: BigRational = (0..m)
                        .map(|edge| face[edge].clone() * closed.normal_form[edge].clone())
                        .sum();
                    if !curl.is_zero() {
                        return fail("closed normal form is not face-closed");
                    }
                }
                let v_closed = closed_witness.value();
                if weighted_l1(closed_witness.primal_residual(), &weights) != *v_closed {
                    return fail(
                        "closed certificate value is not the carrier-weighted norm of its residual",
                    );
                }
                let expected_closed = v_closed == v_star;
                let expected_normal_form: &[BigRational] = if v_star.is_zero() {
                    receipt.normal_form.as_slice()
                } else if expected_closed {
                    closed.normal_form.as_slice()
                } else {
                    joint.primal_residual()
                };
                if receipt.normal_form.as_slice() != expected_normal_form {
                    return fail("normal form is not the branch-selected representative");
                }
                let final_eval = receipt.final_evaluation();
                if final_eval.phi1().primal_residual() != receipt.normal_form.as_slice() {
                    return fail("final evaluation residual ≠ normal form");
                }
                let class = final_eval.status();
                let class_consistent = match class {
                    ObstructionDiagnosticClass::ExactRepair => v_star.is_zero(),
                    ObstructionDiagnosticClass::ClosedResidual => {
                        !v_star.is_zero() && expected_closed
                    }
                    ObstructionDiagnosticClass::ActiveClosureFailure => {
                        !v_star.is_zero() && !expected_closed
                    }
                };
                if !class_consistent {
                    return fail("final class does not match the value comparison");
                }
            }
            None => {
                if !v_star.is_zero() {
                    return fail("v* > 0 but no closed projection was recorded");
                }
                if !receipt.normal_form.iter().all(BigRational::is_zero) {
                    return fail("v* = 0 but the normal form is nonzero");
                }
            }
        }
    } else {
        if !(carrier.faces.is_empty()
            || receipt.gauge.status() == ObstructionDiagnosticClass::ExactRepair)
        {
            return fail("joint stage missing although faces are declared and gauge is not exact");
        }
        if receipt.normal_form.as_slice() != receipt.gauge.phi1().primal_residual() {
            return fail("normal form ≠ gauge residual although no joint stage ran");
        }
    }

    let rank_d0 = exact_rank(&d0_rows)?;
    let rank_faces = if carrier.faces.is_empty() {
        0
    } else {
        exact_rank(&d1)?
    };
    if receipt.b1_over_q != m - rank_d0 - rank_faces {
        return fail("b1 over Q does not re-derive from exact ranks");
    }

    let gauge_hash = receipt.gauge.primitive_receipt().declared_carrier_hash();
    let final_hash = receipt
        .final_evaluation()
        .primitive_receipt()
        .declared_carrier_hash();
    if gauge_hash != final_hash {
        return fail("gauge and final evaluations bind different carrier identities");
    }

    Ok(ReplayedSolve { receipt })
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WindowLift {
    pub added_faces: Vec<(usize, usize, usize)>,
}

impl WindowLift {
    pub fn new(added_faces: Vec<(usize, usize, usize)>) -> Self {
        Self { added_faces }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LiftEffect {
    Resolved,
    Reduced,
    Ineffective,
}

#[derive(Debug)]
pub struct LiftReceipt {
    before: SolveReceipt,
    after: SolveReceipt,
    lifted_carrier: FiniteCarrier2,
    effect: LiftEffect,
    authority_effect: AuthorityEffect,
}

impl LiftReceipt {
    pub fn before(&self) -> &SolveReceipt {
        &self.before
    }

    pub fn after(&self) -> &SolveReceipt {
        &self.after
    }

    pub fn lifted_carrier(&self) -> &FiniteCarrier2 {
        &self.lifted_carrier
    }

    pub fn effect(&self) -> LiftEffect {
        self.effect
    }

    pub fn gain(&self) -> BigRational {
        self.before.span_distance().clone() - self.after.span_distance().clone()
    }

    pub fn b1_drop(&self) -> usize {
        self.before.b1_over_q() - self.after.b1_over_q()
    }

    pub fn authority_effect(&self) -> &AuthorityEffect {
        &self.authority_effect
    }
}

fn escalate(carrier: &FiniteCarrier2, lift: &WindowLift) -> Result<FiniteCarrier2, SolveRefusal> {
    if lift.added_faces.is_empty() {
        return Err(SolveRefusal::RepresentationInvalid(
            "window lift declares no new 2-cells".to_string(),
        ));
    }
    let mut existing: Vec<[usize; 3]> = carrier
        .faces
        .iter()
        .map(|&(u, v, w)| {
            let mut sorted = [u, v, w];
            sorted.sort_unstable();
            sorted
        })
        .collect();
    for &(u, v, w) in &lift.added_faces {
        let mut sorted = [u, v, w];
        sorted.sort_unstable();
        if existing.contains(&sorted) {
            return Err(SolveRefusal::RepresentationInvalid(format!(
                "window lift re-declares the already-present 2-cell {sorted:?}"
            )));
        }
        existing.push(sorted);
    }
    let mut faces = carrier.faces.clone();
    faces.extend(lift.added_faces.iter().copied());
    Ok(FiniteCarrier2 {
        num_vertices: carrier.num_vertices,
        edges: carrier.edges.clone(),
        faces,
    })
}

pub fn lift(
    carrier: &FiniteCarrier2,
    omega: &[i128],
    window: &WindowLift,
) -> Result<LiftReceipt, SolveRefusal> {
    let lifted = escalate(carrier, window)?;

    let before = solve(carrier, omega)?;
    let after = solve(&lifted, omega)?;

    let v_before = before.span_distance().clone();
    let v_after = after.span_distance().clone();

    if v_after > v_before {
        return Err(SolveRefusal::JointCertificateSynthesis(format!(
            "lift monotonicity violated: v* rose from {v_before} to {v_after} \
             although S(P) ⊆ S(P')"
        )));
    }
    if after.b1_over_q() > before.b1_over_q() {
        return Err(SolveRefusal::JointCertificateSynthesis(format!(
            "lift monotonicity violated: b1 rose from {} to {}",
            before.b1_over_q(),
            after.b1_over_q()
        )));
    }

    let effect = if v_after == v_before {
        LiftEffect::Ineffective
    } else if v_after.is_zero() {
        LiftEffect::Resolved
    } else {
        LiftEffect::Reduced
    };

    Ok(LiftReceipt {
        before,
        after,
        lifted_carrier: lifted,
        effect,
        authority_effect: AuthorityEffect::None,
    })
}

#[derive(Debug)]
pub struct LiftProbe {
    candidates: Vec<WindowLift>,
    outcomes: Vec<(usize, LiftReceipt)>,
    refused: Vec<(usize, SolveRefusal)>,
}

impl LiftProbe {
    pub fn candidates(&self) -> &[WindowLift] {
        &self.candidates
    }

    pub fn outcomes(&self) -> &[(usize, LiftReceipt)] {
        &self.outcomes
    }

    pub fn best(&self) -> Option<&LiftReceipt> {
        self.outcomes
            .iter()
            .filter(|(_, receipt)| receipt.effect() != LiftEffect::Ineffective)
            .min_by(|(_, a), (_, b)| a.after().span_distance().cmp(b.after().span_distance()))
            .map(|(_, receipt)| receipt)
    }

    pub fn ineffective(&self) -> Vec<usize> {
        self.outcomes
            .iter()
            .filter(|(_, receipt)| receipt.effect() == LiftEffect::Ineffective)
            .map(|(index, _)| *index)
            .collect()
    }

    pub fn refused(&self) -> &[(usize, SolveRefusal)] {
        &self.refused
    }

    pub fn is_irreducible_within_budget(&self) -> bool {
        self.refused.is_empty()
            && !self.outcomes.is_empty()
            && self.outcomes.len() == self.candidates.len()
            && self
                .outcomes
                .iter()
                .all(|(_, receipt)| receipt.effect() == LiftEffect::Ineffective)
    }
}

pub fn probe_lifts(
    carrier: &FiniteCarrier2,
    omega: &[i128],
    candidates: &[WindowLift],
) -> Result<LiftProbe, SolveRefusal> {
    let mut outcomes = Vec::new();
    let mut refused = Vec::new();

    for (index, candidate) in candidates.iter().enumerate() {
        match lift(carrier, omega, candidate) {
            Ok(receipt) => outcomes.push((index, receipt)),
            Err(error) => refused.push((index, error)),
        }
    }

    Ok(LiftProbe {
        candidates: candidates.to_vec(),
        outcomes,
        refused,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn unit_edges(pairs: &[(usize, usize)]) -> Vec<CarrierEdge> {
        pairs
            .iter()
            .map(|&(tail, head)| CarrierEdge {
                tail,
                head,
                weight: 1,
            })
            .collect()
    }

    fn int(value: i64) -> BigRational {
        BigRational::from_integer(BigInt::from(value))
    }

    fn frac(numerator: i64, denominator: i64) -> BigRational {
        BigRational::new(BigInt::from(numerator), BigInt::from(denominator))
    }

    #[test]
    fn filled_triangle_cyclic_residual_is_exact_after_multi_cycle() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![(0, 1, 2)],
        };
        let receipt = solve(&carrier, &[1, 1, 1]).expect("solve");

        assert_eq!(
            receipt.gauge().status(),
            ObstructionDiagnosticClass::ActiveClosureFailure,
            "gauge stage must see the face curl (the graph-only path cannot)"
        );
        assert_eq!(receipt.gauge().phi1().value(), &int(3));
        assert_eq!(receipt.gauge().gamma2().value(), &int(3));

        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ExactRepair);
        assert!(receipt.normal_form().iter().all(BigRational::is_zero));
        let joint = receipt.joint().expect("joint stage ran");
        assert_eq!(
            joint.value(),
            &int(0),
            "distance to the supplied span is zero"
        );
        assert_eq!(receipt.b1_over_q(), 0);
        assert!(!receipt.is_closed_class_survivor());
        assert!(receipt.authority_effect().is_none());
    }

    #[test]
    fn pure_cycle_is_a_closed_class_survivor() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![],
        };
        let receipt = solve(&carrier, &[1, 1, 1]).expect("solve");

        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ClosedResidual);
        assert_eq!(receipt.gauge().phi1().value(), &int(3));
        assert_eq!(receipt.gauge().gamma2().value(), &int(0));
        assert_eq!(receipt.b1_over_q(), 1);
        assert!(receipt.is_closed_class_survivor());
        assert!(
            receipt.joint().is_none(),
            "no faces: no supplied cycle moves"
        );
        assert_eq!(
            weighted_l1(receipt.normal_form(), &[int(1), int(1), int(1)]),
            int(3),
            "the surviving mass is irreducible"
        );
        assert!(receipt.authority_effect().is_none());
    }

    #[test]
    fn bowtie_with_one_filled_lobe_leaves_a_closed_residual() {
        let carrier = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
            faces: vec![(0, 1, 2)],
        };
        let receipt = solve(&carrier, &[1, 1, 1, 1, 1, 1]).expect("solve");

        assert_eq!(
            receipt.gauge().status(),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
        assert_eq!(receipt.gauge().phi1().value(), &int(6));

        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ClosedResidual);
        assert_eq!(receipt.b1_over_q(), 1);
        assert!(receipt.is_closed_class_survivor());

        let joint = receipt.joint().expect("joint stage ran");
        assert_eq!(joint.value(), &int(3), "only the unfilled lobe survives");
        let closed = receipt.closed().expect("closed projection ran");
        assert_eq!(closed.value(), &int(3), "a closed optimum exists");
        assert_eq!(receipt.final_evaluation().gamma2().value(), &int(0));
        for filled_lobe_edge in 0..3 {
            assert!(
                receipt.normal_form()[filled_lobe_edge].is_zero(),
                "the filled lobe must be fully repaired"
            );
        }
        assert!(receipt.authority_effect().is_none());
    }

    #[test]
    fn review_counterexample_status_is_canonical() {
        let carrier = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[
                (0, 1),
                (0, 2),
                (0, 4),
                (1, 2),
                (1, 3),
                (2, 3),
                (2, 4),
                (3, 4),
            ]),
            faces: vec![(0, 1, 2), (2, 3, 4)],
        };
        let omega = [0, 1, 3, 2, 0, -2, -1, 3];
        let receipt = solve(&carrier, &omega).expect("solve");

        let joint = receipt.joint().expect("joint ran");
        assert_eq!(joint.value(), &int(3));
        let closed = receipt.closed().expect("closed projection ran");
        assert_eq!(
            closed.value(),
            &int(3),
            "a closed optimum exists at the same value"
        );
        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ClosedResidual);
        assert_eq!(receipt.final_evaluation().gamma2().value(), &int(0));
        assert_eq!(receipt.b1_over_q(), 2);
    }

    #[test]
    fn a_certified_strict_closedness_gap_is_an_active_closure_failure() {
        let carrier = FiniteCarrier2 {
            num_vertices: 4,
            edges: vec![
                CarrierEdge {
                    tail: 0,
                    head: 1,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 0,
                    head: 3,
                    weight: 5,
                },
                CarrierEdge {
                    tail: 3,
                    head: 1,
                    weight: 5,
                },
            ],
            faces: vec![(0, 1, 2)],
        };
        let receipt = solve(&carrier, &[-1, 0, 0, 1, 1]).expect("solve");

        let joint = receipt.joint().expect("joint ran");
        assert_eq!(joint.value(), &int(4));
        let closed = receipt.closed().expect("closed projection ran");
        assert_eq!(closed.value(), &frac(16, 3));
        assert_eq!(
            receipt.status(),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
        assert!(receipt.final_evaluation().gamma2().value() > &int(0));
    }

    #[test]
    fn declaration_order_does_not_change_status_or_values() {
        let original = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
            faces: vec![(0, 1, 2)],
        };
        let omega_original = [1, 1, 1, 1, 1, 1];

        let permuted = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(4, 0), (2, 0), (0, 1), (3, 4), (1, 2), (0, 3)]),
            faces: vec![(1, 2, 0)],
        };
        let omega_permuted = [1, 1, 1, 1, 1, 1];

        let receipt_a = solve(&original, &omega_original).expect("solve original");
        let receipt_b = solve(&permuted, &omega_permuted).expect("solve permuted");

        assert_eq!(receipt_a.status(), receipt_b.status());
        assert_eq!(
            receipt_a.joint().map(|w| w.value().clone()),
            receipt_b.joint().map(|w| w.value().clone())
        );
        assert_eq!(
            receipt_a.closed().map(|w| w.value().clone()),
            receipt_b.closed().map(|w| w.value().clone())
        );
        assert_eq!(receipt_a.b1_over_q(), receipt_b.b1_over_q());
    }

    #[test]
    fn the_certificate_chain_shares_one_carrier_identity() {
        let carrier = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
            faces: vec![(0, 1, 2)],
        };
        let receipt = solve(&carrier, &[1, 1, 1, 1, 1, 1]).expect("solve");
        assert!(
            receipt.normal_form_eval.is_some(),
            "fixture must exercise both evaluations"
        );
        assert_eq!(
            receipt.gauge().primitive_receipt().declared_carrier_hash(),
            receipt
                .final_evaluation()
                .primitive_receipt()
                .declared_carrier_hash(),
            "gauge and normal-form evaluations must bind one carrier identity"
        );

        let other = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![],
        };
        let other_receipt = solve(&other, &[1, 1, 1]).expect("solve");
        assert_ne!(
            receipt.gauge().primitive_receipt().declared_carrier_hash(),
            other_receipt
                .gauge()
                .primitive_receipt()
                .declared_carrier_hash()
        );
    }

    #[test]
    fn a_lift_on_an_already_exact_residual_is_ineffective() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![],
        };
        let receipt = lift(&carrier, &[1, 2, -3], &WindowLift::new(vec![(0, 1, 2)])).expect("lift");
        assert_eq!(receipt.before().span_distance(), &int(0));
        assert_eq!(receipt.after().span_distance(), &int(0));
        assert_eq!(receipt.gain(), int(0));
        assert_eq!(
            receipt.effect(),
            LiftEffect::Ineffective,
            "an already-exact residual gives the lift no credit"
        );
    }

    #[test]
    fn replay_refuses_a_tampered_receipt() {
        let carrier = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
            faces: vec![(0, 1, 2)],
        };
        let omega = [1, 1, 1, 1, 1, 1];
        let mut receipt = solve(&carrier, &omega).expect("solve");
        assert!(replay_solve(&carrier, &omega, &receipt).is_ok());

        receipt.normal_form[3] += int(1);
        assert!(
            replay_solve(&carrier, &omega, &receipt).is_err(),
            "a tampered normal form must refuse replay"
        );

        let fresh = solve(&carrier, &omega).expect("solve");
        assert!(replay_solve(&carrier, &[1, 1, 1, 0, 0, 0], &fresh).is_err());
    }

    #[test]
    fn weights_route_the_normal_form() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: vec![
                CarrierEdge {
                    tail: 0,
                    head: 1,
                    weight: 2,
                },
                CarrierEdge {
                    tail: 1,
                    head: 2,
                    weight: 2,
                },
                CarrierEdge {
                    tail: 2,
                    head: 0,
                    weight: 5,
                },
            ],
            faces: vec![],
        };
        let receipt = solve(&carrier, &[1, 1, 1]).expect("solve");
        assert_eq!(receipt.gauge().phi1().value(), &int(6), "3 · min_e w_e");
        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ClosedResidual);
        assert!(
            receipt.normal_form()[2].is_zero(),
            "no minimal representative keeps mass on the weight-5 edge"
        );
    }

    #[test]
    fn on_a_filled_triangle_every_residual_is_exact_after_multi_cycle() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: vec![
                CarrierEdge {
                    tail: 0,
                    head: 1,
                    weight: 3,
                },
                CarrierEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                },
            ],
            faces: vec![(0, 1, 2)],
        };
        for omega in [[1, 0, 0], [7, -2, 5], [0, 0, 11]] {
            let receipt = solve(&carrier, &omega).expect("solve");
            assert_eq!(
                receipt.status(),
                ObstructionDiagnosticClass::ExactRepair,
                "b1 = 0 over Q: the supplied span is the whole cochain space"
            );
            if let Some(joint) = receipt.joint() {
                assert_eq!(joint.value(), &int(0));
            }
        }
    }

    #[test]
    fn a_pure_gradient_is_exact_at_the_gauge_stage() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![(0, 1, 2)],
        };
        let receipt = solve(&carrier, &[1, 2, -3]).expect("solve");
        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ExactRepair);
        assert!(receipt.joint().is_none());
        assert!(receipt.normal_form().iter().all(BigRational::is_zero));
    }

    #[test]
    fn representation_refusals_are_typed() {
        let missing_edge_face = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2)]),
            faces: vec![(0, 1, 2)],
        };
        assert!(matches!(
            solve(&missing_edge_face, &[1, 1]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let bad_weight = FiniteCarrier2 {
            num_vertices: 2,
            edges: vec![CarrierEdge {
                tail: 0,
                head: 1,
                weight: 0,
            }],
            faces: vec![],
        };
        assert!(matches!(
            solve(&bad_weight, &[1]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let wrong_length = FiniteCarrier2 {
            num_vertices: 2,
            edges: unit_edges(&[(0, 1)]),
            faces: vec![],
        };
        assert!(matches!(
            solve(&wrong_length, &[1, 2]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let self_loop = FiniteCarrier2 {
            num_vertices: 2,
            edges: unit_edges(&[(0, 0), (0, 1)]),
            faces: vec![],
        };
        assert!(matches!(
            solve(&self_loop, &[1, 1]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let reversed_duplicate = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 0), (1, 2)]),
            faces: vec![],
        };
        assert!(matches!(
            solve(&reversed_duplicate, &[1, 1, 1]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let degenerate_face = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![(0, 1, 1)],
        };
        assert!(matches!(
            solve(&degenerate_face, &[1, 1, 1]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let duplicate_face = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![(0, 1, 2), (1, 2, 0)],
        };
        assert!(matches!(
            solve(&duplicate_face, &[1, 1, 1]),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));
    }


    fn bowtie() -> FiniteCarrier2 {
        FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
            faces: vec![],
        }
    }

    #[test]
    fn lifting_the_occupied_cycle_resolves_the_residual() {
        let carrier = FiniteCarrier2 {
            num_vertices: 3,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0)]),
            faces: vec![],
        };
        let receipt = lift(&carrier, &[1, 1, 1], &WindowLift::new(vec![(0, 1, 2)])).expect("lift");

        assert_eq!(receipt.before().span_distance(), &int(3));
        assert_eq!(
            receipt.before().status(),
            ObstructionDiagnosticClass::ClosedResidual
        );
        assert_eq!(receipt.effect(), LiftEffect::Resolved);
        assert_eq!(receipt.after().span_distance(), &int(0));
        assert_eq!(
            receipt.after().status(),
            ObstructionDiagnosticClass::ExactRepair
        );
        assert_eq!(receipt.gain(), int(3));
        assert_eq!(receipt.b1_drop(), 1);
        assert!(receipt.authority_effect().is_none());
    }

    #[test]
    fn a_lift_on_an_unoccupied_cycle_is_ineffective() {
        let carrier = bowtie();
        let omega = [1, 1, 1, 0, 0, 0];
        assert_eq!(solve(&carrier, &omega).unwrap().b1_over_q(), 2);

        let receipt = lift(&carrier, &omega, &WindowLift::new(vec![(0, 3, 4)])).expect("lift");

        assert_eq!(receipt.effect(), LiftEffect::Ineffective);
        assert_eq!(receipt.gain(), int(0), "nothing was bought");
        assert_eq!(receipt.b1_drop(), 1, "yet b1 genuinely dropped");
        assert_eq!(receipt.after().span_distance(), &int(3));
        assert_eq!(
            receipt.after().status(),
            ObstructionDiagnosticClass::ClosedResidual
        );
    }

    #[test]
    fn a_partial_lift_is_certified_as_reduced_not_resolved() {
        let carrier = bowtie();
        let omega = [1, 1, 1, 1, 1, 1];
        let receipt = lift(&carrier, &omega, &WindowLift::new(vec![(0, 1, 2)])).expect("lift");

        assert_eq!(receipt.before().span_distance(), &int(6));
        assert_eq!(receipt.effect(), LiftEffect::Reduced);
        assert_eq!(receipt.after().span_distance(), &int(3));
        assert_eq!(receipt.gain(), int(3));
        assert_eq!(receipt.b1_drop(), 1);
        assert!(receipt.after().is_closed_class_survivor());
    }

    #[test]
    fn probing_reports_irreducibility_relative_to_the_declared_budget() {
        let carrier = bowtie();
        let omega = [1, 1, 1, 0, 0, 0];

        let barren =
            probe_lifts(&carrier, &omega, &[WindowLift::new(vec![(0, 3, 4)])]).expect("probe");
        assert!(barren.best().is_none());
        assert_eq!(barren.ineffective(), &[0]);
        assert!(barren.refused().is_empty());
        assert!(barren.is_irreducible_within_budget());

        let widened = probe_lifts(
            &carrier,
            &omega,
            &[
                WindowLift::new(vec![(0, 3, 4)]),
                WindowLift::new(vec![(0, 1, 2)]),
            ],
        )
        .expect("probe");
        assert!(!widened.is_irreducible_within_budget());
        let best = widened.best().expect("a reducing candidate exists");
        assert_eq!(best.effect(), LiftEffect::Resolved);
        assert_eq!(widened.ineffective(), &[0]);
    }

    #[test]
    fn a_refused_candidate_blocks_the_irreducibility_claim() {
        let carrier = FiniteCarrier2 {
            num_vertices: 5,
            edges: unit_edges(&[(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
            faces: vec![(0, 3, 4)],
        };
        let omega = [1, 1, 1, 0, 0, 0];
        let probe = probe_lifts(
            &carrier,
            &omega,
            &[
                WindowLift::new(vec![(0, 3, 4)]),
            ],
        )
        .expect("probe");

        assert!(probe.best().is_none());
        assert!(probe.ineffective().is_empty());
        assert_eq!(probe.refused().len(), 1);
        assert!(
            !probe.is_irreducible_within_budget(),
            "a refusal is not evidence that nothing helps"
        );
    }

    #[test]
    fn malformed_lifts_are_typed_refusals() {
        let carrier = bowtie();
        let omega = [1, 1, 1, 0, 0, 0];

        assert!(matches!(
            lift(&carrier, &omega, &WindowLift::new(vec![])),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));

        let filled = FiniteCarrier2 {
            faces: vec![(0, 1, 2)],
            ..bowtie()
        };
        assert!(
            matches!(
                lift(&filled, &omega, &WindowLift::new(vec![(1, 2, 0)])),
                Err(SolveRefusal::RepresentationInvalid(_))
            ),
            "re-declaring an existing 2-cell (any rotation) is a no-op dressed as a move"
        );

        assert!(matches!(
            lift(&carrier, &omega, &WindowLift::new(vec![(1, 3, 4)])),
            Err(SolveRefusal::RepresentationInvalid(_))
        ));
    }

    #[test]
    fn the_closure_premium_prices_closedness() {
        let closed_survivor = solve(&bowtie(), &[1, 1, 1, 0, 0, 0]).expect("solve");
        assert_eq!(closed_survivor.closure_premium(), int(0));

        let gap_carrier = FiniteCarrier2 {
            num_vertices: 4,
            edges: vec![
                CarrierEdge {
                    tail: 0,
                    head: 1,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                },
                CarrierEdge {
                    tail: 0,
                    head: 3,
                    weight: 5,
                },
                CarrierEdge {
                    tail: 3,
                    head: 1,
                    weight: 5,
                },
            ],
            faces: vec![(0, 1, 2)],
        };
        let gapped = solve(&gap_carrier, &[-1, 0, 0, 1, 1]).expect("solve");
        assert_eq!(
            gapped.closure_premium(),
            frac(4, 3),
            "16/3 - 4: closedness is purchasable, at a certified price"
        );
        assert_eq!(
            gapped.status(),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
    }

    #[test]
    fn carriers_past_the_old_enumeration_fence_now_solve_exactly() {
        let mut edges = Vec::new();
        for spoke in 1..7 {
            edges.push((0, spoke));
        }
        for rim in 1..7 {
            edges.push((rim, if rim == 6 { 1 } else { rim + 1 }));
        }
        edges.push((1, 4));
        let carrier = FiniteCarrier2 {
            num_vertices: 7,
            edges: unit_edges(&edges),
            faces: vec![(0, 1, 2)],
        };
        let mut omega = vec![0i128; 13];
        for rim_edge in 6..12 {
            omega[rim_edge] = 1;
        }
        let receipt = solve(&carrier, &omega).expect("13 edges is no longer fenced");
        assert_eq!(receipt.span_distance(), &int(6));
        assert_eq!(receipt.status(), ObstructionDiagnosticClass::ClosedResidual);
        assert_eq!(receipt.closure_premium(), int(0));
        assert!(receipt.is_closed_class_survivor());
    }

    #[test]
    fn a_thirty_edge_carrier_solves_exactly_with_fractional_optima() {
        let n = 15usize;
        let mut edges: Vec<(usize, usize)> = (0..n).map(|i| (i, (i + 1) % n)).collect();
        for i in 0..n {
            edges.push((i, (i + 2) % n));
        }
        assert_eq!(edges.len(), 30);
        let faces: Vec<(usize, usize, usize)> =
            (0..n).map(|i| (i, (i + 1) % n, (i + 2) % n)).collect();
        let carrier = FiniteCarrier2 {
            num_vertices: n,
            edges: unit_edges(&edges),
            faces,
        };
        let mut omega = vec![0i128; 30];
        for rim in 0..n {
            omega[rim] = 1;
        }

        let receipt = solve(&carrier, &omega).expect("30 edges is well past the old fence");
        assert_eq!(receipt.span_distance(), &frac(15, 2));
        assert_eq!(receipt.closure_premium(), frac(3, 2));
        assert_eq!(
            receipt.status(),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
        assert_eq!(receipt.b1_over_q(), 1);
        assert!(receipt.authority_effect().is_none());
    }
}
