// AuthorityEffect: None.

//! The registry-relative tower walk: obstruction, lift pressure, a declared lift
//! registry, and a transition ledger that refuses when a prerequisite is absent.
//!
//! - [`find_lift_trigger`] searches a finite carrier for `x, y, c` with
//!   `p(x) = p(y)` but `p(rho_c x) != p(rho_c y)`. A witness is lift *pressure*:
//!   its terminal is `LiftRequired`, and nothing here turns it into a licensed lift.
//! - [`holonomy_commutator`] returns `[Hol_a, Hol_b]` from `omega_holonomy`. A
//!   nonzero commutator is pressure on the representation, not a channel.
//! - [`audit_registry`] adjudicates the declared seven-row interface registry.
//!   Three rows are computed: the classical contextual packet fails on an
//!   exhaustive Mermin–Peres search, the rebit packet on the local-tomography
//!   count `3 * 3 != 10`, and the complex Hilbert/CPTP packet resolves only if
//!   its `M_2` declarations replay *and* every declared Born probability equals
//!   `Tr(E rho)`; a Born defect is an open obstruction and dominates. The scalar
//!   and rotational rows fail by their declared witnesses, and the GPT and
//!   quaternionic rows are refused while no composite rule is declared.
//!   Minimality is relative to the rows given.
//! - [`validate_tower_walk`] emits either a registry-relative conclusion or a
//!   conclusion explicitly conditional on the still-unproved minimality
//!   premise. It never reports an unconditional forced lift while minimality
//!   is open.
//! - Norm branches: scalar `sum w |x|`, internal `SO(k)` `sum w ||x||_2`
//!   (an exact sum of surds), and `(1/2)||X||_1` for Hermitian `2 x 2` `X`.
//!
//! The walk derives no Hilbert space, Born rule or CPTP law; those are imports
//! of the complex packet. Registry-relative minimality is not universal
//! uniqueness, and no ledger row is an authority terminal.

use num_traits::Zero;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::composition_tomography::LocalTomographyReport;
use omega_quantum_physics::separating_preds::MerminPeresSquare;

use crate::m2_quantum_packet::{verify, M2Refusal};
use omega_quantum_physics::gauge_cochain_complex::M2Packet;

/// The status attached to each transition of the walk.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransitionStatus {
    Derived,
    Imported,
    Conditional,
    Refused,
}

/// The seven declared candidate interfaces of the registry.
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

/// One registry row: an interface and whether its composite rule is declared.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DeclaredCandidate {
    pub interface: CandidateInterface,
    pub composite_rule_declared: bool,
}

/// Why a candidate fails under its own declared rules.
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
    /// The packet replays, but its declared Born probability at `entry`
    /// differs from `Tr(E rho)` by `defect`: an active closure failure.
    BornDefect {
        entry: usize,
        defect: Rational,
    },
}

/// The registry terminal of one candidate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RegistryTerminal {
    Fail(FailureWitness),
    /// Refused because its composite rule is undeclared, not refuted.
    Refuse,
    Resolve,
}

/// The declared seven-row registry.
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

/// Adjudicate one candidate under the registry's declared rules.
pub fn adjudicate(candidate: &DeclaredCandidate, m2: &M2Packet) -> RegistryTerminal {
    use CandidateInterface::*;
    match candidate.interface {
        ScalarL1 => RegistryTerminal::Fail(FailureWitness::NoStateEffectStructure),
        RotationalL1L2 => RegistryTerminal::Fail(FailureWitness::NoBornPairingOrCptp),
        ClassicalContextualGluing => {
            let square = MerminPeresSquare::standard();
            match square.verify_no_noncontextual_assignment() {
                Ok(true) => RegistryTerminal::Fail(FailureWitness::NoGlobalSection {
                    assignments_checked: 1 << square.observables().len(),
                }),
                Ok(false) => RegistryTerminal::Resolve,
                Err(_) => RegistryTerminal::Refuse,
            }
        }
        GptConvex | QuaternionicGuarded => {
            // A declaration flag carries no composite replay, effect pairing,
            // or channel witness, so it cannot license a resolving row.
            RegistryTerminal::Refuse
        }
        RealHilbertRebit => {
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
        ComplexHilbertCptp => complex_packet_terminal(m2),
    }
}

/// The complex packet resolves only when its declarations replay and its
/// declared Born residual is zero. That residual has `dE = drho = 0`, so `d1`
/// of it is its Born part: a nonzero defect is never closed, and so is an
/// active closure failure that dominates resolution.
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

/// The adjudicated registry.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RegistryAudit {
    pub rows: Vec<(CandidateInterface, RegistryTerminal)>,
}

impl RegistryAudit {
    /// The unique resolving candidate, if exactly one row resolves.
    pub fn minimal_interface(&self) -> Option<CandidateInterface> {
        let mut resolvers = self
            .rows
            .iter()
            .filter(|(_, t)| *t == RegistryTerminal::Resolve);
        let first = resolvers.next()?;
        resolvers.next().is_none().then_some(first.0)
    }
}

/// Adjudicate every declared row against the declared `M_2` packet.
pub fn audit_registry(candidates: &[DeclaredCandidate], m2: &M2Packet) -> RegistryAudit {
    RegistryAudit {
        rows: candidates
            .iter()
            .map(|c| (c.interface, adjudicate(c, m2)))
            .collect(),
    }
}

/// The five named antecedents and the minimality evidence of `ForcedLift`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ForcedLiftPrerequisites {
    pub open_comm: bool,
    pub lift_protocol: bool,
    pub admissible: bool,
    pub valid_transport: bool,
    pub resolves: bool,
    /// `None` is an explicitly open minimality proof.
    pub minimality: Option<RegistryAudit>,
}

/// A forced-lift prerequisite that the validator found absent.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Prerequisite {
    OpenComm,
    LiftProtocol,
    Admissible,
    ValidTransport,
    Resolve,
    MinimalInterface,
}

/// The scope in which a forced lift was recorded.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ForcedLiftScope {
    /// The other antecedents hold, but minimality has not been supplied. The
    /// ledger is therefore conditional on that unresolved premise.
    ConditionalOnMinimality,
    DeclaredRegistryOnly(CandidateInterface),
}

/// One ledger row.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LedgerRow {
    pub transition: &'static str,
    pub status: TransitionStatus,
}

/// The emitted transition ledger. The four flags are the walk's stated
/// non-claims; the validator has no path that sets them.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TowerWalkLedger {
    pub rows: Vec<LedgerRow>,
    pub forced_lift_scope: ForcedLiftScope,
    pub universal_forced_lift_proved: bool,
    pub origin_derivation_proved: bool,
    pub full_survives_descent_claim: bool,
    pub external_sealed_terminal_supplied: bool,
}

/// Emit the ledger, or refuse with every missing prerequisite.
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

/// The canonical walk: `Open_comm` from the exhaustive Mermin–Peres search,
/// `Resolve` from the complex packet's registry terminal (replay and a zero
/// Born defect), the registry audit as minimality evidence; protocol,
/// admissibility and transport are declared.
pub fn canonical_prerequisites(m2: &M2Packet) -> ForcedLiftPrerequisites {
    ForcedLiftPrerequisites {
        // A refused search leaves `Open_comm` unestablished (fail closed).
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
