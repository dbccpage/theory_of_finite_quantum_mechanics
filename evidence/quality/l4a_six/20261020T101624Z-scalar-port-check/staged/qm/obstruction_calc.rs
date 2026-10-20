use ::linear_algebra::backend::basic_matrix::BasicMatrix;
use num_traits::{Signed, Zero};
use omega_number_theory::rational::Rational;
use omega_solvers::data_cochain_packet::CochainPacketError;

use crate::qm::campaigns::residual_density::{CoherenceLicense, ResidualLedger};
use omega_quantum_physics::residual_density_calculus::{
    row_stochastic_pushforward, ResidualDensityError,
};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum GomcError {
    #[error("{first} states in one readout, {second} in the other")]
    ReadoutLength { first: usize, second: usize },
    #[error("obstruction point {role} has a negative coordinate")]
    NegativeCoordinate { role: String },
    #[error("observer label {label} is not below the declared class count {classes}")]
    ObserverLabel { label: usize, classes: usize },
    #[error("an observer on {states} states has at most {states} classes, not {classes}")]
    ClassCount { classes: usize, states: usize },
    #[error("matrices must be square of equal size")]
    Shape,
    #[error("residual density refused: {0}")]
    Density(#[from] ResidualDensityError),
    #[error("cochain packet refused: {0}")]
    Packet(#[from] CochainPacketError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObstructionPoint {
    pub phi1: Rational,
    pub gamma2: Rational,
    pub xi: Option<Rational>,
}

impl ObstructionPoint {
    fn validate(&self, role: &str) -> Result<(), GomcError> {
        let negative = self.phi1.is_negative()
            || self.gamma2.is_negative()
            || self.xi.as_ref().is_some_and(Signed::is_negative);
        if negative {
            return Err(GomcError::NegativeCoordinate {
                role: role.to_string(),
            });
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ImprovementTier {
    Phi1,
    Gamma2,
    Xi,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BranchProposal {
    pub label: String,
    pub tier: Option<ImprovementTier>,
    pub mass: Rational,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BranchSearchReport {
    pub proposals: Vec<BranchProposal>,
    pub probabilities: Vec<Rational>,
    pub ranking: Vec<usize>,
}

fn improvement(
    current: &ObstructionPoint,
    candidate: &ObstructionPoint,
) -> (Option<ImprovementTier>, Rational) {
    if candidate.phi1 < current.phi1 {
        return (Some(ImprovementTier::Phi1), &current.phi1 - &candidate.phi1);
    }
    if candidate.phi1 > current.phi1 {
        return (None, Rational::zero());
    }
    if candidate.gamma2 < current.gamma2 {
        return (
            Some(ImprovementTier::Gamma2),
            &current.gamma2 - &candidate.gamma2,
        );
    }
    if candidate.gamma2 > current.gamma2 {
        return (None, Rational::zero());
    }
    match (&current.xi, &candidate.xi) {
        (Some(now), Some(then)) if then < now => (Some(ImprovementTier::Xi), now - then),
        _ => (None, Rational::zero()),
    }
}

fn rank_order(candidates: &[(String, ObstructionPoint)], a: usize, b: usize) -> std::cmp::Ordering {
    let ((label_a, point_a), (label_b, point_b)) = (&candidates[a], &candidates[b]);
    use omega_policy::evaluation_hierarchy::{compare_exact_ranking, ExactRankingKey};
    compare_exact_ranking(
        ExactRankingKey {
            phi1: &point_a.phi1,
            gamma2: &point_a.gamma2,
            xi: point_a.xi.as_ref(),
            label: label_a,
            input_position: a,
        },
        ExactRankingKey {
            phi1: &point_b.phi1,
            gamma2: &point_b.gamma2,
            xi: point_b.xi.as_ref(),
            label: label_b,
            input_position: b,
        },
    )
}

pub fn obstruction_branch_search(
    current: &ObstructionPoint,
    candidates: &[(String, ObstructionPoint)],
) -> Result<BranchSearchReport, GomcError> {
    current.validate("current")?;
    let mut proposals = Vec::with_capacity(candidates.len());
    for (label, point) in candidates {
        point.validate(label)?;
        let (tier, mass) = improvement(current, point);
        proposals.push(BranchProposal {
            label: label.clone(),
            tier,
            mass,
        });
    }
    let best_tier = proposals.iter().filter_map(|p| p.tier).min();
    let total: Rational = proposals
        .iter()
        .filter(|p| p.tier == best_tier)
        .map(|p| p.mass.clone())
        .sum();
    let probabilities = proposals
        .iter()
        .map(|p| {
            if total.is_zero() || p.tier != best_tier {
                Rational::zero()
            } else {
                &p.mass / &total
            }
        })
        .collect();
    let mut ranking: Vec<usize> = (0..proposals.len())
        .filter(|&i| proposals[i].tier.is_some())
        .collect();
    ranking.sort_by(|&a, &b| rank_order(candidates, a, b));
    Ok(BranchSearchReport {
        proposals,
        probabilities,
        ranking,
    })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ReconstructionImport {
    FiniteHilbertCarrier,
    ComplexScalars,
    BornPairing,
    CptpDynamics,
    TensorComposition,
}

pub const RECONSTRUCTION_IMPORTS: [ReconstructionImport; 5] = [
    ReconstructionImport::FiniteHilbertCarrier,
    ReconstructionImport::ComplexScalars,
    ReconstructionImport::BornPairing,
    ReconstructionImport::CptpDynamics,
    ReconstructionImport::TensorComposition,
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReconstructionTerminal {
    Hosted,
    PacketRelativeObstruction { missing: Vec<ReconstructionImport> },
}

pub fn terminalize_reconstruction(declared: &[ReconstructionImport]) -> ReconstructionTerminal {
    let missing: Vec<ReconstructionImport> = RECONSTRUCTION_IMPORTS
        .iter()
        .copied()
        .filter(|i| !declared.contains(i))
        .collect();
    if missing.is_empty() {
        ReconstructionTerminal::Hosted
    } else {
        ReconstructionTerminal::PacketRelativeObstruction { missing }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LiftCandidateEvaluation {
    source_obstruction: bool,
    reduces_phi: bool,
    preserves_closure: bool,
    new_carrier_declared: bool,
    replay_declared: bool,
}

impl LiftCandidateEvaluation {
    pub fn source_obstruction(&self) -> bool {
        self.source_obstruction
    }

    pub fn reduces_phi(&self) -> bool {
        self.reduces_phi
    }

    pub fn preserves_closure(&self) -> bool {
        self.preserves_closure
    }

    pub fn new_carrier_declared(&self) -> bool {
        self.new_carrier_declared
    }

    pub fn replay_declared(&self) -> bool {
        self.replay_declared
    }

    pub fn is_licensed_lift(&self) -> bool {
        self.source_obstruction
            && self.reduces_phi
            && self.preserves_closure
            && self.new_carrier_declared
            && self.replay_declared
    }
}

pub fn evaluate_lift_candidate(
    before: &ObstructionPoint,
    after: &ObstructionPoint,
    new_carrier_declared: bool,
    replay_declared: bool,
) -> Result<LiftCandidateEvaluation, GomcError> {
    before.validate("before")?;
    after.validate("after")?;
    Ok(LiftCandidateEvaluation {
        source_obstruction: before.phi1.is_positive(),
        reduces_phi: after.phi1 < before.phi1,
        preserves_closure: after.gamma2 <= before.gamma2,
        new_carrier_declared,
        replay_declared,
    })
}

pub fn licensed_coherence_lift(
    coherence: &CoherenceLicense,
    lift: &LiftCandidateEvaluation,
) -> bool {
    coherence.is_licensed() && lift.is_licensed_lift()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ReportAuthorityTag {
    #[default]
    None,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GomcReport {
    global_weights: Vec<Rational>,
    observed_weights: Vec<Rational>,
    pushed_weights: Option<Vec<Rational>>,
    branch: Option<BranchSearchReport>,
    authority_effect: ReportAuthorityTag,
}

impl GomcReport {
    pub fn global_weights(&self) -> &[Rational] {
        &self.global_weights
    }

    pub fn observed_weights(&self) -> &[Rational] {
        &self.observed_weights
    }

    pub fn pushed_weights(&self) -> Option<&[Rational]> {
        self.pushed_weights.as_deref()
    }

    pub fn branch(&self) -> Option<&BranchSearchReport> {
        self.branch.as_ref()
    }

    pub fn authority_effect(&self) -> ReportAuthorityTag {
        self.authority_effect
    }
}

fn validate_observer_labels(
    observer: &[usize],
    weights_len: usize,
    classes: usize,
) -> Result<(), GomcError> {
    if observer.len() != weights_len {
        return Err(GomcError::ReadoutLength {
            first: observer.len(),
            second: weights_len,
        });
    }
    if classes > observer.len() {
        return Err(GomcError::ClassCount {
            classes,
            states: observer.len(),
        });
    }
    for &label in observer {
        if label >= classes {
            return Err(GomcError::ObserverLabel { label, classes });
        }
    }
    Ok(())
}

pub fn gomc_report(
    ledger: &ResidualLedger,
    observer: &[usize],
    classes: usize,
    channel: Option<&BasicMatrix<Rational>>,
    search: Option<(&ObstructionPoint, &[(String, ObstructionPoint)])>,
) -> Result<GomcReport, GomcError> {
    let global_weights = ledger.weights();
    validate_observer_labels(observer, global_weights.len(), classes)?;
    let mut observed_weights = vec![Rational::zero(); classes];
    for (s, &label) in observer.iter().enumerate() {
        observed_weights[label] = &observed_weights[label] + &global_weights[s];
    }
    let pushed_weights = match channel {
        Some(k) => Some(row_stochastic_pushforward(k, &global_weights)?),
        None => None,
    };
    let branch = match search {
        Some((current, candidates)) => Some(obstruction_branch_search(current, candidates)?),
        None => None,
    };
    Ok(GomcReport {
        global_weights,
        observed_weights,
        pushed_weights,
        branch,
        authority_effect: ReportAuthorityTag::None,
    })
}
