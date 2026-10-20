

use num_traits::Zero;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::composition_tomography::LocalTomographyReport;
use omega_quantum_physics::separating_predictions::MerminPeresSquare;

use crate::qm::quantum_packet::{verify, M2Refusal};
use omega_quantum_physics::gauge_cochain_complex::M2Packet;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransitionStatus {
    Derived,
    Imported,
    Conditional,
    Refused,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum CandidateInterface {
    ScalarL1,
    RotationalL1L2,
    ClassicalContextualGluing,
    GptConvex,
    RealHilbertRebit,
    QuaternionicGuarded,
    ComplexHilbertCptp,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DeclaredCandidate {
    pub interface: CandidateInterface,
    pub composite_rule_declared: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FailureWitness {
    NoStateEffectStructure,
    NoBornPairingOrCptp,
    NoGlobalSection {
        assignments_checked: usize,
    },
    LocalTomography {
        local: usize,
        joint: usize,
    },
    M2Replay(M2Refusal),
    BornDefect {
        entry: usize,
        defect: Rational,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RegistryTerminal {
    Fail(FailureWitness),
    Refuse,
    Resolve,
}

pub fn declared_registry() -> Vec<DeclaredCandidate> {
    use CandidateInterface::*;
    [
        ScalarL1,
        RotationalL1L2,
        ClassicalContextualGluing,
        GptConvex,
        RealHilbertRebit,
        QuaternionicGuarded,
        ComplexHilbertCptp,
    ]
    .into_iter()
    .map(|interface| DeclaredCandidate {
        interface,
        composite_rule_declared: !matches!(interface, GptConvex | QuaternionicGuarded),
    })
    .collect()
}

fn adjudicate_classical_gluing() -> RegistryTerminal {
    let square = MerminPeresSquare::standard();
    match square.verify_no_noncontextual_assignment() {
        Ok(true) => RegistryTerminal::Fail(FailureWitness::NoGlobalSection {
            assignments_checked: 1 << square.observables().len(),
        }),
        Ok(false) => RegistryTerminal::Resolve,
        Err(_) => RegistryTerminal::Refuse,
    }
}

fn adjudicate_real_rebit() -> RegistryTerminal {
    let Ok(report) = LocalTomographyReport::real_product_params(2, 2) else {
        return RegistryTerminal::Refuse;
    };
    if report.identity_holds {
        RegistryTerminal::Resolve
    } else {
        RegistryTerminal::Fail(FailureWitness::LocalTomography {
            local: report.local_param_a * report.local_param_b,
            joint: report.joint_param,
        })
    }
}

pub fn adjudicate(candidate: &DeclaredCandidate, m2: &M2Packet) -> RegistryTerminal {
    use CandidateInterface::*;
    match candidate.interface {
        ScalarL1 => RegistryTerminal::Fail(FailureWitness::NoStateEffectStructure),
        RotationalL1L2 => RegistryTerminal::Fail(FailureWitness::NoBornPairingOrCptp),
        ClassicalContextualGluing => adjudicate_classical_gluing(),
        GptConvex | QuaternionicGuarded => RegistryTerminal::Refuse,
        RealHilbertRebit => adjudicate_real_rebit(),
        ComplexHilbertCptp => complex_packet_terminal(m2),
    }
}

fn complex_packet_terminal(m2: &M2Packet) -> RegistryTerminal {
    let verified = match verify(m2.clone()) {
        Ok(verified) => verified,
        Err(refusal) => return RegistryTerminal::Fail(FailureWitness::M2Replay(refusal)),
    };
    match verified
        .born_residuals()
        .into_iter()
        .enumerate()
        .find(|(_, defect)| !defect.is_zero())
    {
        Some((entry, defect)) => {
            RegistryTerminal::Fail(FailureWitness::BornDefect { entry, defect })
        }
        None => RegistryTerminal::Resolve,
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RegistryAudit {
    pub rows: Vec<(CandidateInterface, RegistryTerminal)>,
}

impl RegistryAudit {
    pub fn minimal_interface(&self) -> Option<CandidateInterface> {
        let mut resolvers = self
            .rows
            .iter()
            .filter(|(_, t)| *t == RegistryTerminal::Resolve);
        let first = resolvers.next()?;
        resolvers.next().is_none().then_some(first.0)
    }
}

pub fn audit_registry(candidates: &[DeclaredCandidate], m2: &M2Packet) -> RegistryAudit {
    RegistryAudit {
        rows: candidates
            .iter()
            .map(|c| (c.interface, adjudicate(c, m2)))
            .collect(),
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ForcedLiftPrerequisites {
    pub open_comm: bool,
    pub lift_protocol: bool,
    pub admissible: bool,
    pub valid_transport: bool,
    pub resolves: bool,
    pub minimality: Option<RegistryAudit>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Prerequisite {
    OpenComm,
    LiftProtocol,
    Admissible,
    ValidTransport,
    Resolve,
    MinimalInterface,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ForcedLiftScope {
    ConditionalOnMinimality,
    DeclaredRegistryOnly(CandidateInterface),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LedgerRow {
    pub transition: &'static str,
    pub status: TransitionStatus,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TowerWalkLedger {
    pub rows: Vec<LedgerRow>,
    pub forced_lift_scope: ForcedLiftScope,
    pub universal_forced_lift_proved: bool,
    pub origin_derivation_proved: bool,
    pub full_survives_descent_claim: bool,
    pub external_sealed_terminal_supplied: bool,
}

pub fn validate_tower_walk(
    pre: &ForcedLiftPrerequisites,
) -> Result<TowerWalkLedger, Vec<Prerequisite>> {
    let mut missing = Vec::new();
    for (present, which) in [
        (pre.open_comm, Prerequisite::OpenComm),
        (pre.lift_protocol, Prerequisite::LiftProtocol),
        (pre.admissible, Prerequisite::Admissible),
        (pre.valid_transport, Prerequisite::ValidTransport),
        (pre.resolves, Prerequisite::Resolve),
    ] {
        if !present {
            missing.push(which);
        }
    }
    let scope = match &pre.minimality {
        None => ForcedLiftScope::ConditionalOnMinimality,
        Some(audit) => match audit.minimal_interface() {
            Some(interface) => ForcedLiftScope::DeclaredRegistryOnly(interface),
            None => {
                missing.push(Prerequisite::MinimalInterface);
                ForcedLiftScope::ConditionalOnMinimality
            }
        },
    };
    if !missing.is_empty() {
        return Err(missing);
    }
    use TransitionStatus::*;
    let rows = vec![
        LedgerRow { transition: "D(x,y) = y - x", status: Derived },
        LedgerRow { transition: "C0 -> C1 -> C2 with d1 d0 = 0", status: Imported },
        LedgerRow { transition: "Phi1(q) > 0 => LicensedLift", status: Refused },
        LedgerRow { transition: "LiftTrigger => LicensedLift", status: Refused },
        LedgerRow { transition: "[Hol, Hol'] != 0 => CPTP", status: Refused },
        LedgerRow {
            transition: "Open_comm + LiftProtocol + ValidTransport + Resolve + MinimalInterface => ForcedLift",
            status: Conditional,
        },
        LedgerRow {
            transition: "F_Q + CPTP + trace-distance axioms + edge additivity => l1(E; ||.||_1 / 2)",
            status: Conditional,
        },
        LedgerRow { transition: "StructureDerived => IsAuth", status: Refused },
    ];
    Ok(TowerWalkLedger {
        rows,
        forced_lift_scope: scope,
        universal_forced_lift_proved: false,
        origin_derivation_proved: false,
        full_survives_descent_claim: false,
        external_sealed_terminal_supplied: false,
    })
}

pub fn canonical_prerequisites(m2: &M2Packet) -> ForcedLiftPrerequisites {
    ForcedLiftPrerequisites {
        open_comm: matches!(
            MerminPeresSquare::standard().verify_no_noncontextual_assignment(),
            Ok(true)
        ),
        lift_protocol: true,
        admissible: true,
        valid_transport: true,
        resolves: complex_packet_terminal(m2) == RegistryTerminal::Resolve,
        minimality: Some(audit_registry(&declared_registry(), m2)),
    }
}
