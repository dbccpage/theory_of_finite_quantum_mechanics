

use crate::linear_algebra::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::{
    solve_in_image, ExactRowReduction, ImageMembership,
};
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use omega_functional::gamma2::ExactCochainComplexQ;
use omega_number_theory::rational::Rational;
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_quantum_physics::repair_capacity::{windows_to_exceed, RepairBudget};
use omega_solvers::data_cochain_packet::certified_trichotomy;

use omega_quantum_physics::threshold_repair_certificate::ThresholdScaling;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceKind {
    Theorem,
    Experiment,
    Simulation,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PairingBound {
    Measured(Rational),
    Scaling(ThresholdScaling),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ClaimScope {
    FiniteBenchmark { windows: u64, visibility: Rational },
    HumanSignificantScale {
        visibility: Rational,
        max_distance: u32,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PacketTerminal {
    FailureNotEstablished {
        windows: u64,
    },
    ResidualForced {
        windows: BigInt,
    },
    ConditionalSurvival {
        least_distance: u32,
    },
    ActiveClosureFailure {
        gamma2: Rational,
    },
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct RealizationPacket {
    pub physical_carrier: Option<String>,
    pub logical_distinction: Option<String>,
    pub repair_space: Option<usize>,
    pub defect_space: Option<usize>,
    pub repair_boundary: Option<Vec<Vec<Rational>>>,
    pub repair_image: Option<Vec<Vec<Rational>>>,
    pub residual_quotient: Option<usize>,
    pub closure_map: Option<Vec<Vec<Rational>>>,
    pub defect_history: Option<Vec<Rational>>,
    pub repair_capacity: Option<Rational>,
    pub defect_rate: Option<Rational>,
    pub mixing_bound: Option<Rational>,
    pub logical_witnesses: Option<Vec<Vec<Rational>>>,
    pub pairing_bound: Option<PairingBound>,
    pub evidence: Option<Vec<EvidenceKind>>,
    pub accepted_overhead: Option<String>,
    pub claim: Option<ClaimScope>,
    pub claimed_terminal: Option<PacketTerminal>,
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum PacketRefusal {
    #[error("NoPhysicalCarrier: hardware and operating regime are not declared")]
    NoPhysicalCarrier,
    #[error("NoLogicalDistinction: no encoded computational distinction is named")]
    NoLogicalDistinction,
    #[error("NoRepairSpace: admissible repairs are not declared")]
    NoRepairSpace,
    #[error("NoDefectSpace: the defect carrier is undeclared or empty")]
    NoDefectSpace,
    #[error("NoRepairBoundary: d0 is missing or is not a C^1 x C^0 matrix")]
    NoRepairBoundary,
    #[error("NoRepairImage: the declared repair image does not span exactly im d0")]
    NoRepairImage,
    #[error("NoResidualQuotient: the declared dim Q^1 is missing or differs from {computed}")]
    NoResidualQuotient { computed: usize },
    #[error("NoClosureMap: d1 is missing, misshapen, or d1 d0 != 0")]
    NoClosureMap,
    #[error("NoProjectionDefectModel: no defect history in C^1")]
    NoProjectionDefectModel,
    #[error("NoRepairCapacityBound: mu is missing or negative")]
    NoRepairCapacityBound,
    #[error("NoDefectProductionBound: lambda is missing or negative")]
    NoDefectProductionBound,
    #[error("NoMixingBound: epsilon is missing or negative")]
    NoMixingBound,
    #[error("NoLogicalWitnessFamily: witness {index:?} is missing or does not vanish on im d0")]
    NoLogicalWitnessFamily { index: Option<usize> },
    #[error("NoPairingBound: no logical-pairing bound in [0, 1]")]
    NoPairingBound,
    #[error("NoEvidenceTerminalizer: the evidence pipeline is not declared")]
    NoEvidenceTerminalizer,
    #[error("NoAcceptedOverhead: the resource class is not stated")]
    NoAcceptedOverhead,
    #[error("NoHumanSignificantScale: the workload scope or visibility threshold is undefined")]
    NoHumanSignificantScale,
    #[error("ClaimOverreach: the packet does not certify the claim at human-significant scale")]
    ClaimOverreach,
    #[error("TerminalMismatch: claimed {claimed:?}, computed {computed:?}")]
    TerminalMismatch {
        claimed: PacketTerminal,
        computed: PacketTerminal,
    },
    #[error("replay refused: {0}")]
    Replay(String),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PacketReport {
    repair_rank: usize,
    quotient_dimension: usize,
    class: ObstructionDiagnosticClass,
    residual_mass: Rational,
    closure_defect: Rational,
    witness_pairings: Vec<Rational>,
    gap: Rational,
    terminal: PacketTerminal,
}

impl PacketReport {
    pub fn repair_rank(&self) -> usize {
        self.repair_rank
    }

    pub fn quotient_dimension(&self) -> usize {
        self.quotient_dimension
    }

    pub fn class(&self) -> ObstructionDiagnosticClass {
        self.class
    }

    pub fn residual_mass(&self) -> &Rational {
        &self.residual_mass
    }

    pub fn closure_defect(&self) -> &Rational {
        &self.closure_defect
    }

    pub fn witness_pairings(&self) -> &[Rational] {
        &self.witness_pairings
    }

    pub fn gap(&self) -> &Rational {
        &self.gap
    }

    pub fn terminal(&self) -> &PacketTerminal {
        &self.terminal
    }
}

impl RealizationPacket {
    pub fn from_threshold_theorem(
        scaling: &ThresholdScaling,
        repair_space: usize,
        repair_boundary: Vec<Vec<Rational>>,
        logical_witnesses: Vec<Vec<Rational>>,
        accepted_overhead: &str,
    ) -> Result<Self, PacketRefusal> {
        let defect_space = repair_boundary.len();
        if repair_boundary.iter().any(|row| row.len() != repair_space) {
            return Err(PacketRefusal::NoRepairBoundary);
        }
        let residual_quotient = defect_space - rank(&repair_boundary, repair_space)?;
        Ok(Self {
            repair_space: Some(repair_space),
            defect_space: Some(defect_space),
            repair_boundary: Some(repair_boundary),
            residual_quotient: Some(residual_quotient),
            defect_rate: Some(scaling.physical_rate().clone()),
            repair_capacity: Some(scaling.threshold_rate().clone()),
            logical_witnesses: Some(logical_witnesses),
            pairing_bound: Some(PairingBound::Scaling(scaling.clone())),
            evidence: Some(vec![EvidenceKind::Theorem]),
            accepted_overhead: Some(accepted_overhead.to_string()),
            ..Self::default()
        })
    }
}

fn rank(rows: &[Vec<Rational>], cols: usize) -> Result<usize, PacketRefusal> {
    if rows.is_empty() || cols == 0 {
        return Ok(0);
    }
    let data = rows.iter().flat_map(|row| row.iter().cloned()).collect();
    BasicMatrix::from_row_major(rows.len(), cols, data)
        .map_err(|e| PacketRefusal::Replay(format!("{e:?}")))?
        .rank()
        .map_err(|e| PacketRefusal::Replay(e.to_string()))
}

fn in_image(d0: &[Vec<Rational>], c0: usize, v: &[Rational]) -> Result<bool, PacketRefusal> {
    if c0 == 0 {
        return Ok(v.iter().all(Zero::is_zero));
    }
    let data = d0.iter().flat_map(|row| row.iter().cloned()).collect();
    let matrix = BasicMatrix::from_row_major(d0.len(), c0, data)
        .map_err(|e| PacketRefusal::Replay(format!("{e:?}")))?;
    match solve_in_image(&matrix, v).map_err(|e| PacketRefusal::Replay(e.to_string()))? {
        ImageMembership::InImage(_) => Ok(true),
        ImageMembership::NotInImage { .. } => Ok(false),
    }
}

fn dot(a: &[Rational], b: &[Rational]) -> Rational {
    a.iter().zip(b).map(|(x, y)| x * y).sum()
}

fn present(text: &Option<String>) -> bool {
    text.as_deref().is_some_and(|t| !t.trim().is_empty())
}

fn nonnegative(value: &Option<Rational>) -> Option<Rational> {
    value.clone().filter(|v| !v.is_negative())
}

pub fn terminalize(packet: &RealizationPacket) -> Result<PacketReport, PacketRefusal> {
    use PacketRefusal::*;
    if !present(&packet.physical_carrier) {
        return Err(NoPhysicalCarrier);
    }
    if !present(&packet.logical_distinction) {
        return Err(NoLogicalDistinction);
    }
    let c0 = packet.repair_space.ok_or(NoRepairSpace)?;
    let c1 = packet
        .defect_space
        .filter(|&c| c > 0)
        .ok_or(NoDefectSpace)?;
    let d0 = packet
        .repair_boundary
        .as_ref()
        .filter(|d0| d0.len() == c1 && d0.iter().all(|row| row.len() == c0))
        .ok_or(NoRepairBoundary)?;
    let repair_rank = rank(d0, c0)?;
    let image = packet.repair_image.as_ref().ok_or(NoRepairImage)?;
    if image.iter().any(|v| v.len() != c1) {
        return Err(NoRepairImage);
    }
    for v in image {
        if !in_image(d0, c0, v)? {
            return Err(NoRepairImage);
        }
    }
    if rank(image, c1)? != repair_rank {
        return Err(NoRepairImage);
    }
    let quotient_dimension = c1 - repair_rank;
    if packet.residual_quotient != Some(quotient_dimension) {
        return Err(NoResidualQuotient {
            computed: quotient_dimension,
        });
    }
    let d1 = packet
        .closure_map
        .as_ref()
        .filter(|rows| !rows.is_empty())
        .ok_or(NoClosureMap)?;
    ExactCochainComplexQ::try_new(c0, c1, d1.len(), d0.clone(), d1.clone())
        .map_err(|_| NoClosureMap)?;
    let omega = packet
        .defect_history
        .as_ref()
        .filter(|w| w.len() == c1)
        .ok_or(NoProjectionDefectModel)?;
    let mu = nonnegative(&packet.repair_capacity).ok_or(NoRepairCapacityBound)?;
    let lambda = nonnegative(&packet.defect_rate).ok_or(NoDefectProductionBound)?;
    let epsilon = nonnegative(&packet.mixing_bound).ok_or(NoMixingBound)?;
    let witnesses = packet
        .logical_witnesses
        .as_ref()
        .filter(|w| !w.is_empty())
        .ok_or(NoLogicalWitnessFamily { index: None })?;
    for (index, z) in witnesses.iter().enumerate() {
        let vanishes = z.len() == c1
            && (0..c0).all(|j| {
                d0.iter()
                    .zip(z)
                    .map(|(row, zi)| &row[j] * zi)
                    .sum::<Rational>()
                    .is_zero()
            });
        if !vanishes || z.iter().all(Zero::is_zero) {
            return Err(NoLogicalWitnessFamily { index: Some(index) });
        }
    }
    let pairing = packet.pairing_bound.as_ref().ok_or(NoPairingBound)?;
    if let PairingBound::Measured(value) = pairing {
        if value.is_negative() || value > &Rational::one() {
            return Err(NoPairingBound);
        }
    }
    let evidence = packet
        .evidence
        .as_ref()
        .filter(|kinds| !kinds.is_empty())
        .ok_or(NoEvidenceTerminalizer)?;
    if !present(&packet.accepted_overhead) {
        return Err(NoAcceptedOverhead);
    }
    let claim = packet.claim.as_ref().ok_or(NoHumanSignificantScale)?;

    let weights = vec![Rational::one(); c1];
    let trichotomy =
        certified_trichotomy(c0, d0, d1, &weights, omega).map_err(|e| Replay(e.to_string()))?;
    let residual_mass = trichotomy.phi1_value().clone();
    let budget = RepairBudget::new(lambda, mu, epsilon).map_err(|e| Replay(e.to_string()))?;
    let gap = budget.persistent_gap();

    let (ClaimScope::FiniteBenchmark { visibility, .. }
    | ClaimScope::HumanSignificantScale { visibility, .. }) = claim;
    if !visibility.is_positive() {
        return Err(NoHumanSignificantScale);
    }

    let terminal =
        if trichotomy.diagnostic_class() == ObstructionDiagnosticClass::ActiveClosureFailure {
            PacketTerminal::ActiveClosureFailure {
                gamma2: trichotomy.gamma2_value().clone(),
            }
        } else {
            match claim {
                ClaimScope::FiniteBenchmark {
                    windows,
                    visibility,
                } => {
                    match windows_to_exceed(&residual_mass, &budget, visibility)
                        .map_err(|e| Replay(e.to_string()))?
                    {
                        Some(forced) if forced <= BigInt::from(*windows) => {
                            PacketTerminal::ResidualForced { windows: forced }
                        }
                        _ => PacketTerminal::FailureNotEstablished { windows: *windows },
                    }
                }
                ClaimScope::HumanSignificantScale {
                    visibility,
                    max_distance,
                } => {
                    let theorem_backed = evidence.contains(&EvidenceKind::Theorem);
                    match pairing {
                        PairingBound::Scaling(scaling)
                            if theorem_backed
                                && scaling.ratio() < Rational::one()
                                && !gap.is_positive() =>
                        {
                            match scaling.least_distance_below(visibility, *max_distance) {
                                Ok(Some(least_distance)) => {
                                    PacketTerminal::ConditionalSurvival { least_distance }
                                }
                                _ => return Err(ClaimOverreach),
                            }
                        }
                        _ => return Err(ClaimOverreach),
                    }
                }
            }
        };
    if let Some(claimed) = &packet.claimed_terminal {
        if claimed != &terminal {
            return Err(TerminalMismatch {
                claimed: claimed.clone(),
                computed: terminal,
            });
        }
    }
    Ok(PacketReport {
        repair_rank,
        quotient_dimension,
        class: trichotomy.diagnostic_class(),
        residual_mass,
        closure_defect: trichotomy.gamma2_value().clone(),
        witness_pairings: witnesses.iter().map(|z| dot(z, omega)).collect(),
        gap,
        terminal,
    })
}
