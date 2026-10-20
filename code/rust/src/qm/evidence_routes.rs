

use num_traits::{Signed, Zero};
use omega_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredTolerance {
    phi: Rational,
    gamma: Rational,
}

impl DeclaredTolerance {
    pub fn new(phi: Rational, gamma: Rational) -> Result<Self, RouteRefusal> {
        if phi.is_negative() || gamma.is_negative() {
            return Err(RouteRefusal::NegativeTolerance);
        }
        Ok(Self { phi, gamma })
    }
    pub fn phi(&self) -> &Rational {
        &self.phi
    }
    pub fn gamma(&self) -> &Rational {
        &self.gamma
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClosureStatus {
    ExactClosed,
    WitnessedNonzeroGamma,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EvidenceRoute {
    ExactQuantumReplay,
    ApproxQuantumReplay {
        phi: Rational,
        gamma: Rational,
        tolerance: DeclaredTolerance,
        closure: ClosureStatus,
    },
    QuantumSurvivor {
        phi: Rational,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceClass {
    Exact,
    Scoped,
}

impl EvidenceRoute {
    pub fn class(&self) -> EvidenceClass {
        match self {
            EvidenceRoute::ExactQuantumReplay => EvidenceClass::Exact,
            EvidenceRoute::ApproxQuantumReplay { .. } | EvidenceRoute::QuantumSurvivor { .. } => {
                EvidenceClass::Scoped
            }
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum RouteRefusal {
    #[error("obstruction values must be nonnegative")]
    NegativeValue,
    #[error("a tolerance must be nonnegative")]
    NegativeTolerance,
    #[error("open obstruction: Gamma_Q = {gamma} is outside the declared envelope")]
    OpenObstruction { gamma: Rational },
    #[error(
        "open obstruction: Gamma_Q = {gamma} is within the envelope but nonzero, and Phi_Q = {phi} is outside it, \
         so the residual is neither within tolerance nor closed"
    )]
    OpenObstructionOutsidePhiTolerance {
        phi: Box<Rational>,
        gamma: Box<Rational>,
    },
}

fn build_within_phi_route(
    phi: &Rational,
    gamma: &Rational,
    tolerance: Option<&DeclaredTolerance>,
) -> EvidenceRoute {
    match tolerance {
        None => EvidenceRoute::ExactQuantumReplay,
        Some(tolerance) => EvidenceRoute::ApproxQuantumReplay {
            phi: phi.clone(),
            gamma: gamma.clone(),
            tolerance: tolerance.clone(),
            closure: if gamma.is_zero() {
                ClosureStatus::ExactClosed
            } else {
                ClosureStatus::WitnessedNonzeroGamma
            },
        },
    }
}

pub fn route_evidence(
    phi: &Rational,
    gamma: &Rational,
    tolerance: Option<&DeclaredTolerance>,
) -> Result<EvidenceRoute, RouteRefusal> {
    if phi.is_negative() || gamma.is_negative() {
        return Err(RouteRefusal::NegativeValue);
    }
    let zero = Rational::zero();
    let (eps_phi, eps_gamma) = match tolerance {
        Some(t) => (&t.phi, &t.gamma),
        None => (&zero, &zero),
    };
    if gamma > eps_gamma {
        return Err(RouteRefusal::OpenObstruction {
            gamma: gamma.clone(),
        });
    }
    if phi <= eps_phi {
        return Ok(build_within_phi_route(phi, gamma, tolerance));
    }
    if gamma.is_zero() {
        return Ok(EvidenceRoute::QuantumSurvivor { phi: phi.clone() });
    }
    Err(RouteRefusal::OpenObstructionOutsidePhiTolerance {
        phi: Box::new(phi.clone()),
        gamma: Box::new(gamma.clone()),
    })
}
