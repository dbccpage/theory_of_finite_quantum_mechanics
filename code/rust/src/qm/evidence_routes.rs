// AuthorityEffect: None.

//! Evidence routes for finite quantum packets: exact replay versus scoped
//! tolerance, as disjoint classes.
//!
//! [`route_evidence`] takes the certified obstruction values `(Phi_Q, Gamma_Q)`
//! of a packet residual and an optional declared tolerance:
//!
//! - no tolerance (exact symbolic replay) and `Phi_Q = Gamma_Q = 0`:
//!   `ExactQuantumReplay`, the only member of the exact class here;
//! - a declared tolerance with both values inside it: `ApproxQuantumReplay`;
//! - `Gamma_Q = 0` with `Phi_Q` outside the (possibly zero) tolerance:
//!   `QuantumSurvivor`, a closed but non-exact residual;
//! - otherwise the route is refused as an open obstruction: either `Gamma_Q`
//!   is outside the envelope, or it is inside but nonzero while `Phi_Q` is
//!   outside, so the residual is neither within tolerance nor closed.
//!
//! The approximate and survivor routes form the scoped class. Every input gets
//! exactly one route, so the classes cannot overlap. A packet that declares a
//! tolerance never reaches the exact class, even at zero error: empirical
//! evidence stays scoped. No route is an authority terminal.

use num_traits::{Signed, Zero};
use omega_number_theory::rational::Rational;

/// A declared tolerance envelope `(eps_Phi, eps_Gamma)`.
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

/// Exact closure and witnessed nonzero obstruction are distinct even inside tolerance.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClosureStatus {
    ExactClosed,
    WitnessedNonzeroGamma,
}

/// The evidence route of one replay.
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

/// The two historical classes.
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

/// Why no route was granted.
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

/// Route a replay by its certified `(Phi_Q, Gamma_Q)` and declared tolerance.
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
        return Ok(match tolerance {
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
        });
    }
    if gamma.is_zero() {
        return Ok(EvidenceRoute::QuantumSurvivor { phi: phi.clone() });
    }
    Err(RouteRefusal::OpenObstructionOutsidePhiTolerance {
        phi: Box::new(phi.clone()),
        gamma: Box::new(gamma.clone()),
    })
}
