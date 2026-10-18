// AuthorityEffect: None.

//! Finite firewall statements of the General Obstruction Management Calculus,
//! computed exactly.
//!
//! - Observer quotients: [`omega_types::observer_quotient::hidden_separation`] finds two states an observer
//!   identifies while a hidden readout separates them, so the joint readout
//!   cannot factor through the observer; [`omega_types::observer_quotient::pair_observer`] composes two
//!   observers, and a hidden glue coordinate can still separate states the pair
//!   identifies ("Local Green != Global Red absence").
//! - [`omega_solvers::solver_cohomology_quotient_phi1::lggr_cochain_witness`]: two edge cochains with the same
//!   orientation-blind edge masses whose quotient classes differ, decided by
//!   `omega_functional`'s trichotomy.
//! - [`omega_quantum_physics::pairing_audit::born_pairing`] versus [`omega_quantum_physics::pairing_audit::dephased_pairing`]: both are normalised on POVMs
//!   and nonnegative on states and effects, they agree on all diagonal data, and
//!   they differ off it, so `L1` simplex readouts do not select the Born pairing.
//! - [`obstruction_branch_search`]: exact lexicographic descent on
//!   `(Phi1, Gamma2, Xi)`; each strict proposal gets the positive improvement of
//!   its first improving coordinate as mass, and the ranking orders strict
//!   proposals by their own points, lexicographically. The masses are not
//!   comparable across tiers, so the ranking does not follow them. Ranking a
//!   branch accepts nothing.
//! - [`terminalize_reconstruction`]: a missing import yields a packet-relative
//!   obstruction naming it, never an impossibility verdict.
//! - [`evaluate_lift_candidate`]: source obstruction, `Phi1` reduction and
//!   closure preservation are computed from obstruction points; new carrier and
//!   replay are declared. A complete coherence license does not supply them.
//! - [`GomcReport`]: the composed diagnostics. Its authority tag is a
//!   one-variant [`ReportAuthorityTag`], `None` on every path.
//!
//! The `f64` engine `omega_engines::obstruction_branch_search` remains the
//! production diagnostic; this module is the exact face used for the claims.

use crate::linear_algebra::basic_matrix::BasicMatrix;
use num_traits::{Signed, Zero};
use omega_number_theory::rational::Rational;
use omega_solvers::data_cochain_packet::CochainPacketError;

use crate::qm::campaigns::residual_density::{CoherenceLicense, ResidualLedger};
use omega_quantum_physics::residual_density::{
    row_stochastic_pushforward, ResidualDensityError,
};

/// Refusals for GOMC inputs.
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

/// An obstruction point `(Phi1, Gamma2, Xi)`; `Xi` may be undeclared.
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

/// The first coordinate in which a candidate strictly improves.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ImprovementTier {
    Phi1,
    Gamma2,
    Xi,
}

/// One evaluated branch.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BranchProposal {
    pub label: String,
    pub tier: Option<ImprovementTier>,
    pub mass: Rational,
}

/// The branch search report: proposals, normalised proposal probabilities and a
/// ranking. There is no acceptance field.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BranchSearchReport {
    pub proposals: Vec<BranchProposal>,
    pub probabilities: Vec<Rational>,
    /// Indices of strict proposals, lexicographically least point first:
    /// `Phi1`, then `Gamma2`, then `Xi` (a declared `Xi` before an undeclared
    /// one), then the label, then the input position. A strict total order.
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

/// The strict total order behind [`BranchSearchReport::ranking`]: least `Phi1`,
/// then least `Gamma2`, then a declared `Xi` before an undeclared one (and the
/// least declared `Xi` first), then the label, then the input position.
///
/// `Xi` used to be compared only when both points declared it and treated as
/// `Equal` otherwise, with the label breaking the tie. That relation is not
/// transitive: at equal `(Phi1, Gamma2)`, labels z, m, a with `Xi` `Some(1)`,
/// `None`, `Some(2)` gave z before m (label), m before a (label) and a before z
/// (`Xi`). The resulting ranking depended on the input order, and
/// `slice::sort_by` documents that it may panic on a non-total order. Ranking an
/// undeclared `Xi` after every declared one is a convention of the tie-break
/// only: it does not change which proposals are strict.
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

/// Exact lexicographic obstruction branch search.
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

/// The imports a finite quantum reconstruction packet must declare.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ReconstructionImport {
    FiniteHilbertCarrier,
    ComplexScalars,
    BornPairing,
    CptpDynamics,
    TensorComposition,
}

/// Every import the reconstruction needs.
pub const RECONSTRUCTION_IMPORTS: [ReconstructionImport; 5] = [
    ReconstructionImport::FiniteHilbertCarrier,
    ReconstructionImport::ComplexScalars,
    ReconstructionImport::BornPairing,
    ReconstructionImport::CptpDynamics,
    ReconstructionImport::TensorComposition,
];

/// The terminal of a reconstruction packet. There is no impossibility variant.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReconstructionTerminal {
    Hosted,
    PacketRelativeObstruction { missing: Vec<ReconstructionImport> },
}

/// `Hosted` when every import is declared; otherwise the missing ones, sorted.
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

/// The primitive-lift checklist for a candidate move `before -> after`. The
/// fields are private, so a checklist exists only as [`evaluate_lift_candidate`]
/// computed it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LiftCandidateEvaluation {
    source_obstruction: bool,
    reduces_phi: bool,
    preserves_closure: bool,
    new_carrier_declared: bool,
    replay_declared: bool,
}

impl LiftCandidateEvaluation {
    /// Computed: `Phi1(before) > 0`.
    pub fn source_obstruction(&self) -> bool {
        self.source_obstruction
    }

    /// Computed: `Phi1(after) < Phi1(before)`.
    pub fn reduces_phi(&self) -> bool {
        self.reduces_phi
    }

    /// Computed: `Gamma2(after) <= Gamma2(before)`.
    pub fn preserves_closure(&self) -> bool {
        self.preserves_closure
    }

    /// Declared by the caller.
    pub fn new_carrier_declared(&self) -> bool {
        self.new_carrier_declared
    }

    /// Declared by the caller.
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

/// Evaluate a lift candidate from its obstruction points, refusing negative
/// coordinates as the branch search does.
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

/// A licensed coherence lift needs both a complete coherence license and a licensed lift.
pub fn licensed_coherence_lift(
    coherence: &CoherenceLicense,
    lift: &LiftCandidateEvaluation,
) -> bool {
    coherence.is_licensed() && lift.is_licensed_lift()
}

/// Authority tag of a GOMC report. It has exactly one variant, so a report
/// cannot represent authority. Deliberately not `omega_types::AuthorityEffect`:
/// that crate stays unnameable here (see `certified_authority_fence`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ReportAuthorityTag {
    #[default]
    None,
}

/// The composed GOMC diagnostics for one ledger.
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

    /// Weights coarse-grained by the observer's classes.
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

/// Compose the diagnostics: global weights, observer marginal, optional
/// channel pushforward and optional branch search.
pub fn gomc_report(
    ledger: &ResidualLedger,
    observer: &[usize],
    classes: usize,
    channel: Option<&BasicMatrix<Rational>>,
    search: Option<(&ObstructionPoint, &[(String, ObstructionPoint)])>,
) -> Result<GomcReport, GomcError> {
    let global_weights = ledger.weights();
    if observer.len() != global_weights.len() {
        return Err(GomcError::ReadoutLength {
            first: observer.len(),
            second: global_weights.len(),
        });
    }
    if classes > observer.len() {
        return Err(GomcError::ClassCount {
            classes,
            states: observer.len(),
        });
    }
    if let Some(&label) = observer.iter().find(|&&label| label >= classes) {
        return Err(GomcError::ObserverLabel { label, classes });
    }
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
