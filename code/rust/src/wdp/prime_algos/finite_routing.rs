use crate::coda::diagnostic_routing::{
    propose_value_edit, DiagnosticPacket, Proposal, ProposalPolicy,
};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::finite_cochain_map::{CochainMap, CochainWindow};
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use omega_functional::phi1::ExactPhi1Certificate;
use omega_policy::trichotomy::ObstructionDiagnosticClass;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FiniteTerminal {
    Hold,
    ExactCertified,
    ClosedCertified,
    ActiveCertified,
    StabilizedSurvivor,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TerminalPolicy {
    pub rows: [Option<FiniteTerminal>; 3],
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FiniteRefusal {
    MissingPolicy,
    MissingPolicyRow,
    IncompatibleTerminal,
    MissingLift,
    InvalidLift,
    MissingGuard,
    InvalidDamageBudget,
    NoStrictDescent,
    ClosureDamageExceeded,
    MissingStabilization,
    InvalidStabilization,
    ReplayFailed,
}
fn row(packet: &DiagnosticPacket) -> usize {
    match packet.classification().diagnostic_class() {
        ObstructionDiagnosticClass::ExactRepair => 0,
        ObstructionDiagnosticClass::ClosedResidual => 1,
        ObstructionDiagnosticClass::ActiveClosureFailure => 2,
    }
}
fn replay(packet: &DiagnosticPacket) -> Result<DiagnosticPacket, FiniteRefusal> {
    DiagnosticPacket::replay(
        packet.system().clone(),
        packet.phi1().certificate().clone(),
        packet.closure_map().to_vec(),
    )
    .map_err(|_| FiniteRefusal::ReplayFailed)
}
fn matrix(
    rows: usize,
    cols: usize,
    data: &[Vec<BigRational>],
) -> Result<BasicMatrix<BigRational>, FiniteRefusal> {
    if data.len() != rows || data.iter().any(|r| r.len() != cols) {
        return Err(FiniteRefusal::InvalidLift);
    }
    BasicMatrix::try_from_fn(rows, cols, |i, j| data[i][j].clone())
        .map_err(|_| FiniteRefusal::InvalidLift)
}
fn window(packet: &DiagnosticPacket) -> Result<CochainWindow<BigRational>, FiniteRefusal> {
    let n0 = packet.phi1().alpha().len();
    let n1 = packet.phi1().primal_residual().len();
    let n2 = packet.closure_map().len();
    CochainWindow::try_new(
        [n0, n1, n2],
        matrix(n1, n0, packet.phi1().d0())?,
        matrix(n2, n1, packet.closure_map())?,
    )
    .map_err(|_| FiniteRefusal::InvalidLift)
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LiftContract {
    pub map: CochainMap<BigRational>,
    pub require_coordinate_inclusion: bool,
}
pub fn check_lift(
    source: &DiagnosticPacket,
    target: &DiagnosticPacket,
    contract: Option<&LiftContract>,
) -> Result<(), FiniteRefusal> {
    replay(source)?;
    replay(target)?;
    let contract = contract.ok_or(FiniteRefusal::MissingLift)?;
    if contract.map.source() != &window(source)? || contract.map.target() != &window(target)? {
        return Err(FiniteRefusal::InvalidLift);
    }
    if contract.require_coordinate_inclusion {
        for m in contract.map.maps() {
            let mut used = std::collections::BTreeSet::new();
            for j in 0..m.cols() {
                let mut selected = None;
                for i in 0..m.rows() {
                    let x = m.get_ref(i, j).map_err(|_| FiniteRefusal::InvalidLift)?;
                    if x == &BigRational::one() {
                        if selected.replace(i).is_some() {
                            return Err(FiniteRefusal::InvalidLift);
                        }
                    } else if !x.is_zero() {
                        return Err(FiniteRefusal::InvalidLift);
                    }
                }
                if !used.insert(selected.ok_or(FiniteRefusal::InvalidLift)?) {
                    return Err(FiniteRefusal::InvalidLift);
                }
            }
        }
    }
    let omega = &source.phi1().certificate().omega;
    let column = BasicMatrix::try_from_fn(omega.len(), 1, |i, _| omega[i].clone())
        .map_err(|_| FiniteRefusal::InvalidLift)?;
    let image = contract
        .map
        .transport(1, &column)
        .map_err(|_| FiniteRefusal::InvalidLift)?;
    if image.rows() != target.phi1().certificate().omega.len() {
        return Err(FiniteRefusal::InvalidLift);
    }
    for i in 0..image.rows() {
        if image
            .get_ref(i, 0)
            .map_err(|_| FiniteRefusal::InvalidLift)?
            != &target.phi1().certificate().omega[i]
        {
            return Err(FiniteRefusal::InvalidLift);
        }
    }
    Ok(())
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClosureGuard {
    pub max_gamma_increase: BigRational,
}
pub fn guarded_edit(
    before: &DiagnosticPacket,
    candidate: ExactPhi1Certificate,
    guard: Option<&ClosureGuard>,
) -> Result<DiagnosticPacket, FiniteRefusal> {
    replay(before)?;
    let guard = guard.ok_or(FiniteRefusal::MissingGuard)?;
    if guard.max_gamma_increase.is_negative() {
        return Err(FiniteRefusal::InvalidDamageBudget);
    }
    let after = match propose_value_edit(
        before,
        ProposalPolicy {
            allow_profile_coarsening: false,
            allow_value_edits: true,
        },
        candidate,
    )
    .map_err(|_| FiniteRefusal::ReplayFailed)?
    {
        Proposal::ValueEdit { after, .. } => *after,
        _ => return Err(FiniteRefusal::NoStrictDescent),
    };
    if after.classification().gamma2_value() - before.classification().gamma2_value()
        > guard.max_gamma_increase
    {
        return Err(FiniteRefusal::ClosureDamageExceeded);
    }
    Ok(after)
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteDynamics {
    pub packets: Vec<DiagnosticPacket>,
    pub next: Vec<usize>,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FixedPointWitness {
    pub state: usize,
}
fn check_fixed(
    packet: &DiagnosticPacket,
    dynamics: &FiniteDynamics,
    witness: FixedPointWitness,
) -> Result<(), FiniteRefusal> {
    if dynamics.packets.is_empty()
        || dynamics.next.len() != dynamics.packets.len()
        || dynamics.next.iter().any(|&i| i >= dynamics.packets.len())
    {
        return Err(FiniteRefusal::InvalidStabilization);
    }
    for p in &dynamics.packets {
        replay(p)?;
    }
    if dynamics.packets.get(witness.state) != Some(packet)
        || dynamics.next.get(witness.state) != Some(&witness.state)
    {
        return Err(FiniteRefusal::InvalidStabilization);
    }
    Ok(())
}
pub fn terminalize(
    packet: &DiagnosticPacket,
    policy: Option<&TerminalPolicy>,
    stabilization: Option<(&FiniteDynamics, FixedPointWitness)>,
) -> Result<FiniteTerminal, FiniteRefusal> {
    replay(packet)?;
    let terminal = policy.ok_or(FiniteRefusal::MissingPolicy)?.rows[row(packet)]
        .ok_or(FiniteRefusal::MissingPolicyRow)?;
    match terminal {
        FiniteTerminal::Hold => {}
        FiniteTerminal::ExactCertified if row(packet) == 0 => {}
        FiniteTerminal::ClosedCertified if row(packet) == 1 => {}
        FiniteTerminal::ActiveCertified if row(packet) == 2 => {}
        FiniteTerminal::StabilizedSurvivor if row(packet) == 1 => {
            let (d, w) = stabilization.ok_or(FiniteRefusal::MissingStabilization)?;
            check_fixed(packet, d, w)?;
        }
        _ => return Err(FiniteRefusal::IncompatibleTerminal),
    }
    Ok(terminal)
}
