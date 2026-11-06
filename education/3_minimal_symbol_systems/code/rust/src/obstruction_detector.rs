//! MSS-N Obstruction Detector, Active Demand Pressure, and the Two Boxed Laws.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Formalizes the obstruction detector `obstP` as the active measurement of
//! unbridged structural demand pressure (W_n^active), governed by the Two Boxed Laws:
//! 1. S(n+1) may contain only structure forced by an unresolved Genesis obstruction at S(n).
//! 2. A mathematical realization R(S(n)) has no authority to extend S(n).

use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ObstructionError {
    ErrZeroObstructionDemand(String),
    ErrUnforcedStructure(String),
    ErrCirculationFluxDefect(String),
    ErrCurvatureHolonomyDefect(String),
    ErrEpistemicContinuumFence(String),
    MalformedState(String),
}

impl std::fmt::Display for ObstructionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ObstructionError::ErrZeroObstructionDemand(msg) => {
                write!(f, "ERR_ZERO_OBSTRUCTION_DEMAND: {}", msg)
            }
            ObstructionError::ErrUnforcedStructure(msg) => {
                write!(f, "ERR_UNFORCED_STRUCTURE: {}", msg)
            }
            ObstructionError::ErrCirculationFluxDefect(msg) => {
                write!(f, "ERR_CIRCULATION_FLUX_DEFECT: {}", msg)
            }
            ObstructionError::ErrCurvatureHolonomyDefect(msg) => {
                write!(f, "ERR_CURVATURE_HOLONOMY_DEFECT: {}", msg)
            }
            ObstructionError::ErrEpistemicContinuumFence(msg) => {
                write!(f, "ERR_EPISTEMIC_CONTINUUM_FENCE: {}", msg)
            }
            ObstructionError::MalformedState(msg) => {
                write!(f, "MALFORMED_STATE: {}", msg)
            }
        }
    }
}

impl std::error::Error for ObstructionError {}

/// Primitive Passage State (PState)
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ObstructionState {
    pub wit: BTreeSet<(usize, usize)>,
    pub prot: BTreeSet<(usize, usize)>,
    pub obs: Option<Vec<BTreeSet<usize>>>,
}

impl ObstructionState {
    pub fn new() -> Self {
        Self {
            wit: BTreeSet::new(),
            prot: BTreeSet::new(),
            obs: None,
        }
    }

    /// Gate 1: The pair (i, j) is retained in the witness store.
    pub fn retained_p(&self, i: usize, j: usize) -> bool {
        self.wit.contains(&(i, j))
    }

    /// Gate 2: The pair (i, j) carries a protected demand.
    pub fn protected_p(&self, i: usize, j: usize) -> bool {
        self.prot.contains(&(i, j))
    }

    /// Gate 3: An observation is formally declared.
    pub fn declared_p(&self) -> bool {
        self.obs.is_some()
    }

    /// Gate 4: The declared observation does not separate the pair (vacuous true before declaration).
    pub fn zero_decl_p(&self, i: usize, j: usize) -> bool {
        match &self.obs {
            None => true,
            Some(cols) => cols.iter().any(|c| c.contains(&i) && c.contains(&j)),
        }
    }

    /// The Active Obstruction Detector `obstP`.
    /// Product of retained, protected, and non-separated observation.
    pub fn obst_p(&self, i: usize, j: usize) -> bool {
        let zero_strict = match &self.obs {
            None => false,
            Some(cols) => cols.iter().any(|c| c.contains(&i) && c.contains(&j)),
        };
        self.retained_p(i, j) && self.protected_p(i, j) && zero_strict
    }

    /// Exact Four-Gate Factorization Check.
    pub fn verify_four_gate_factorization(&self, i: usize, j: usize) -> bool {
        let factors = self.retained_p(i, j)
            && self.protected_p(i, j)
            && self.declared_p()
            && self.zero_decl_p(i, j);
        self.obst_p(i, j) == factors
    }

    /// Compute active demand pressure W_n^active.
    pub fn active_demand_pressure(&self, domain: &[(usize, usize)]) -> usize {
        domain.iter().filter(|(i, j)| self.obst_p(*i, *j)).count()
    }
}

/// Candidate Lift Structure submitted to the Evaluator.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CandidateLift {
    pub from_stage: usize,
    pub to_stage: usize,
    pub targeted_obstructions: Vec<(usize, usize)>,
    pub adjoined_structure_description: String,
    pub unforced_structure_flag: bool,
    pub verified_retraction: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LiftReceipt {
    pub status: String,
    pub from_stage: usize,
    pub to_stage: usize,
    pub active_demand_pressure: usize,
    pub resolved_obstructions: usize,
    pub retraction_verified: bool,
}

/// Evaluates a candidate lift against the Two Boxed Laws.
pub fn evaluate_two_boxed_laws_gate(
    state: &ObstructionState,
    candidate: &CandidateLift,
    domain: &[(usize, usize)],
) -> Result<LiftReceipt, ObstructionError> {
    let w_active = state.active_demand_pressure(domain);

    // Boxed Law 1: S(n+1) may contain only structure forced by an unresolved Genesis obstruction at S(n)
    if w_active == 0 {
        return Err(ObstructionError::ErrZeroObstructionDemand(format!(
            "Stage {} has zero active obstruction pressure (W_{}^active = 0). Lift to Stage {} prohibited by Law 1.",
            candidate.from_stage, candidate.from_stage, candidate.to_stage
        )));
    }

    // Boxed Law 2: A mathematical realization R(S(n)) has no authority to extend S(n)
    if candidate.unforced_structure_flag {
        return Err(ObstructionError::ErrUnforcedStructure(format!(
            "Candidate lift introduces unforced structure '{}' not mandated by active obstructions. Prohibited by Law 2.",
            candidate.adjoined_structure_description
        )));
    }

    if !candidate.verified_retraction {
        return Err(ObstructionError::ErrUnforcedStructure(
            "Candidate lift lacks verified retraction onto base stage carrier.".to_string(),
        ));
    }

    let resolved_count = candidate
        .targeted_obstructions
        .iter()
        .filter(|(i, j)| state.obst_p(*i, *j))
        .count();

    Ok(LiftReceipt {
        status: "PASS".to_string(),
        from_stage: candidate.from_stage,
        to_stage: candidate.to_stage,
        active_demand_pressure: w_active,
        resolved_obstructions: resolved_count,
        retraction_verified: true,
    })
}

// ---------------------------------------------------------------------------
// Physical & Geometric Obstruction Layers
// ---------------------------------------------------------------------------

/// Layer 1: 0-Dimensional Topological Chasm (Level 02).
/// Detects unbridged topological gap between two distinct points under collapse.
pub fn audit_layer_1_topological_chasm(
    state: &ObstructionState,
    i: usize,
    j: usize,
) -> Result<bool, ObstructionError> {
    if i == j {
        return Ok(false); // No chasm between identical points
    }
    if state.obst_p(i, j) {
        // Active obstruction represents non-zero H~_0({a, b})
        Ok(true)
    } else {
        Ok(false)
    }
}

/// Layer 2: 1-Dimensional Circulation Functional (Levels 12 & 18).
/// Evaluates loop circulation I(x) = sum_{e in z} x_e on triangle loop a -> b -> c -> a.
pub fn audit_layer_2_circulation_flux(
    x_ab: i64,
    x_bc: i64,
    x_ca: i64,
) -> Result<i64, ObstructionError> {
    let circulation = x_ab + x_bc + x_ca;
    if circulation != 0 {
        // Non-zero circulation: no exact scalar potential g exists with d0 g = x
        Ok(circulation)
    } else {
        Ok(0)
    }
}

/// Layer 3: Curvature Deficits and Gauge Field Strengths (Levels 21, 61-64).
pub fn audit_layer_3_curvature_deficit(
    deficit_angle_numer: i64,
    deficit_angle_denom: i64,
) -> Result<bool, ObstructionError> {
    if deficit_angle_denom == 0 {
        return Err(ObstructionError::MalformedState("Zero denominator in deficit angle".to_string()));
    }
    // Deficit angle != 0 indicates curvature obstruction
    Ok(deficit_angle_numer != 0)
}

/// Layer 4: Epistemic Recovery Fences (Levels 71-73).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum EpistemicContinuumFence {
    ContinuumMetricObstruction,
    UncountableContinuumObstruction,
    DiscreteLatticeAdmitted,
}

pub fn audit_layer_4_epistemic_fence(
    claims_smooth_manifold: bool,
    claims_uncountable_continuum: bool,
) -> Result<EpistemicContinuumFence, ObstructionError> {
    if claims_uncountable_continuum {
        return Err(ObstructionError::ErrEpistemicContinuumFence(
            "Epistemic Firewall: Discrete rational lattice cannot claim uncountable continuum without unearned reals."
                .to_string(),
        ));
    }
    if claims_smooth_manifold {
        return Err(ObstructionError::ErrEpistemicContinuumFence(
            "Epistemic Firewall: Discrete simplicial complex cannot claim smooth Riemannian metric without unearned continuous charts."
                .to_string(),
        ));
    }
    Ok(EpistemicContinuumFence::DiscreteLatticeAdmitted)
}
