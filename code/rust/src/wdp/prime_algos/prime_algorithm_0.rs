
use crate::prime_algos::licensed_lift_gate::{
    step9_licensed_lift_gate, LicensedLiftAdmission, NineUpLiftBits, PaperEr003LiftCertificate,
};
use crate::ddc::dda_alphabet::{DdaOp, DdaStep, DdaTrace, TraceTerminal};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::fmt;

pub use crate::prime_algos::prime_algorithm_0_admission::{admit, AdmissionRefusal, AdmittedDeclaration};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum EvidenceProvenance {
    FixtureDrivenStructuralDemo,
    VerifierProduced,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum PrimeDomain {
    Generic,
    Mub,
    Fsp,
    Coda,
    SymbolGame,
}

impl PrimeDomain {
    pub fn as_str(self) -> &'static str {
        match self {
            PrimeDomain::Generic => "generic",
            PrimeDomain::Mub => "mub",
            PrimeDomain::Fsp => "fsp",
            PrimeDomain::Coda => "coda",
            PrimeDomain::SymbolGame => "symbol_game",
        }
    }
}

impl fmt::Display for PrimeDomain {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum DefectBranch {
    Closed,
    Open,
    StabilizedSurvivor,
    Unset,
}

impl DefectBranch {
    pub fn as_str(self) -> &'static str {
        match self {
            DefectBranch::Closed => "Closed",
            DefectBranch::Open => "Open",
            DefectBranch::StabilizedSurvivor => "StabilizedSurvivor",
            DefectBranch::Unset => "Unset",
        }
    }

    pub fn from_masses(phi1: u64, gamma2: u64) -> Self {
        if phi1 == 0 && gamma2 == 0 {
            DefectBranch::Closed
        } else if gamma2 > 0 {
            DefectBranch::Open
        } else {
            DefectBranch::StabilizedSurvivor
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PrimeTerminal {
    ExactClass,
    ClosedResidual,
    OpenResidual,
    Refusal,
    OracleNeeded,
    Repair,
    Certificate,
    Pending,
}

impl PrimeTerminal {
    pub fn as_str(self) -> &'static str {
        match self {
            PrimeTerminal::ExactClass => "ExactClass",
            PrimeTerminal::ClosedResidual => "ClosedResidual",
            PrimeTerminal::OpenResidual => "OpenResidual",
            PrimeTerminal::Refusal => "Refusal",
            PrimeTerminal::OracleNeeded => "OracleNeeded",
            PrimeTerminal::Repair => "Repair",
            PrimeTerminal::Certificate => "Certificate",
            PrimeTerminal::Pending => "Pending",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CochainSlot {
    BlockedEarly,
    MissingUnjustified,
    Constructed {
        dim_c0: usize,
        dim_c1: usize,
        dim_c2: usize,
        square_zero: bool,
    },
    RefusedNotSquareZero { l1_defect_mass: u64 },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum LiftSearch {
    SkippedClosed,
    SameLevelRepairAttempted,
    LiftAdmitted {
        generators: Vec<String>,
        nine_bits: NineUpLiftBits,
        lean_module: String,
    },
    LiftRefused {
        reason: String,
    },
    OracleGap {
        note: String,
    },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum LiftProposal {
    SkipClosed,
    SameLevelRepair,
    OracleGap {
        note: String,
    },
    Candidate {
        generators: Vec<String>,
        nine_bits: NineUpLiftBits,
        certificate: PaperEr003LiftCertificate,
    },
}

pub fn evaluate_lift_proposal(proposal: LiftProposal) -> LiftSearch {
    match proposal {
        LiftProposal::SkipClosed => LiftSearch::SkippedClosed,
        LiftProposal::SameLevelRepair => LiftSearch::SameLevelRepairAttempted,
        LiftProposal::OracleGap { note } => LiftSearch::OracleGap { note },
        LiftProposal::Candidate {
            generators,
            nine_bits,
            certificate,
        } => match step9_licensed_lift_gate(generators.clone(), nine_bits, certificate) {
            Ok(adm) => LiftSearch::LiftAdmitted {
                generators: adm.generators().to_vec(),
                nine_bits: *adm.nine_bits(),
                lean_module: adm.lean_module().to_string(),
            },
            Err(e) => LiftSearch::LiftRefused {
                reason: e.to_string(),
            },
        },
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DeclarationFill {
    pub carrier: Option<String>,
    pub primitive_difference: Option<String>,
    pub zero_rel: Option<String>,
    pub observer: Option<String>,
    pub witnesses: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CochainWindow {
    pub dim_c0: usize,
    pub dim_c1: usize,
    pub dim_c2: usize,
    pub square_zero: bool,
    pub l1_defect_mass: u64,
}

pub trait DomainAdapter {
    fn domain(&self) -> PrimeDomain;
    fn declaration(&self) -> DeclarationFill;
    fn justify_cochain(&self) -> bool;
    fn cochain_window(&self) -> Option<CochainWindow>;
    fn residual_masses(&self) -> (u64, u64);
    fn lift_proposal(&self, branch: DefectBranch) -> LiftProposal;
    fn literature_note(&self) -> Option<String>;
    fn evidence_provenance(&self) -> EvidenceProvenance {
        EvidenceProvenance::FixtureDrivenStructuralDemo
    }

    fn residual_family_label(&self) -> String {
        format!("{}:default", self.domain())
    }

    fn lift_search(&self, branch: DefectBranch) -> LiftSearch {
        evaluate_lift_proposal(self.lift_proposal(branch))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PrimeAlgorithm0Receipt {
    pub domain: PrimeDomain,
    pub carrier: Option<String>,
    pub primitive_difference: Option<String>,
    pub zero_rel: Option<String>,
    pub cochain: CochainSlot,
    pub q1: Option<String>,
    pub phi1: Option<u64>,
    pub gamma2: Option<u64>,
    pub observer: Option<String>,
    pub witnesses: Vec<String>,
    pub structure_search: LiftSearch,
    pub licensed_lift: Option<LicensedLiftAdmission>,
    pub routing: String,
    pub literature_compare: Option<String>,
    pub branch: DefectBranch,
    pub terminal: PrimeTerminal,
    pub letter_tape: String,
    pub letters_spaced: String,
    pub trace_terminal: String,
    pub residual_family_label: String,
    pub authority_effect: AuthorityEffect,
    pub steps: Vec<PrimeStepRecord>,
    pub evidence_provenance: EvidenceProvenance,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PrimeStepRecord {
    pub prime_step: u8,
    pub op: String,
    pub executed: bool,
    pub message: String,
    pub phi1_after: Option<u64>,
    pub gamma2_after: Option<u64>,
    pub loss_ledger: Option<BTreeMap<String, u64>>,
}

impl PrimeAlgorithm0Receipt {
    pub fn authority_effect(&self) -> &AuthorityEffect {
        &self.authority_effect
    }

    pub fn authority_is_none(&self) -> bool {
        self.authority_effect == AuthorityEffect::None
    }

    pub fn write_files(&self, run_dir: &std::path::Path) -> std::io::Result<()> {
        std::fs::create_dir_all(run_dir)?;
        std::fs::write(
            run_dir.join("letter_tape.txt"),
            format!(
                "{}\nbranch={}\nterminal={}\nauthority_effect={:?}\n",
                self.letter_tape,
                self.branch.as_str(),
                self.terminal.as_str(),
                self.authority_effect
            ),
        )?;
        let json = serde_json::to_vec_pretty(self)
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;
        std::fs::write(run_dir.join("prime_algorithm_0_receipt.json"), &json)?;
        std::fs::write(run_dir.join("oeprmalg0_receipt.json"), &json)?;
        std::fs::write(run_dir.join("prime000_receipt.json"), &json)?;
        Ok(())
    }
}

pub type Oeprmalg0Receipt = PrimeAlgorithm0Receipt;

pub fn run_admitted(
    admitted: &AdmittedDeclaration,
    adapter: &dyn DomainAdapter,
) -> PrimeAlgorithm0Receipt {
    let mut trace = DdaTrace::new();
    let mut steps: Vec<PrimeStepRecord> = Vec::new();
    let family = adapter.residual_family_label();

    let mut emit = |prime_step: u8, op: DdaOp, executed: bool, message: String| {
        if executed {
            trace.emit(DdaStep::executed(op, message.clone()));
        } else {
            trace.emit(DdaStep::refused(op, message.clone()));
        }
        steps.push(PrimeStepRecord {
            prime_step,
            op: op.letter().to_string(),
            executed,
            message,
            phi1_after: None,
            gamma2_after: None,
            loss_ledger: None,
        });
    };

    emit(
        1,
        DdaOp::ContextExposure,
        true,
        format!("declare carrier={}", admitted.carrier()),
    );
    emit(1, DdaOp::Integration, true, "ledger open".into());

    emit(
        2,
        DdaOp::Integration,
        true,
        format!("declare δ={}", admitted.primitive_difference()),
    );

    emit(
        3,
        DdaOp::Integration,
        true,
        format!("declare ZeroRel={}", admitted.zero_rel()),
    );

    let cochain = admitted.cochain().clone();
    if let CochainSlot::Constructed {
        dim_c0,
        dim_c1,
        dim_c2,
        ..
    } = &cochain
    {
        emit(
            4,
            DdaOp::ContextExposure,
            true,
            format!(
                "construct C• dims=({},{},{}) d∘d=0 ok",
                dim_c0, dim_c1, dim_c2
            ),
        );
    }

    let delta = admitted.primitive_difference();
    let q1 = Some(format!("Q1[{delta}]"));
    emit(
        5,
        DdaOp::ResidualProjection,
        true,
        format!("compute Q¹ residual core=[{delta}]"),
    );

    let (p, g) = adapter.residual_masses();
    let phi1 = Some(p);
    let gamma2 = Some(g);
    let branch = DefectBranch::from_masses(p, g);
    emit(
        6,
        DdaOp::Integration,
        true,
        format!("separate Φ₁={p} from Γ₂={g}; branch={}", branch.as_str()),
    );

    let observer = Some(admitted.observer().to_string());
    emit(
        7,
        DdaOp::Integration,
        true,
        format!("declare observer/profile={}", admitted.observer()),
    );

    let witnesses = admitted.witnesses().to_vec();
    emit(
        8,
        DdaOp::Integration,
        true,
        format!("identify witnesses={witnesses:?}"),
    );

    let proposal = adapter.lift_proposal(branch);
    let mut licensed_lift: Option<LicensedLiftAdmission> = None;
    let structure_search = match proposal.clone() {
        LiftProposal::Candidate {
            generators,
            nine_bits,
            certificate,
        } => match step9_licensed_lift_gate(generators, nine_bits, certificate) {
            Ok(adm) => {
                licensed_lift = Some(adm.clone());
                LiftSearch::LiftAdmitted {
                    generators: adm.generators().to_vec(),
                    nine_bits: *adm.nine_bits(),
                    lean_module: adm.lean_module().to_string(),
                }
            }
            Err(e) => LiftSearch::LiftRefused {
                reason: e.to_string(),
            },
        },
        other => evaluate_lift_proposal(other),
    };
    match &structure_search {
        LiftSearch::LiftAdmitted {
            generators,
            lean_module,
            ..
        } => {
            emit(
                9,
                DdaOp::Lift,
                true,
                format!("lift admitted under {lean_module} nine-bit gate: {generators:?}"),
            );
        }
        LiftSearch::LiftRefused { reason } => {
            emit(
                9,
                DdaOp::Refusal,
                false,
                format!("lift refused by step-9 gate: {reason}"),
            );
        }
        LiftSearch::SameLevelRepairAttempted => {
            emit(
                9,
                DdaOp::ExactRepair,
                true,
                "search same-level exact repair for Γ₂>0 open branch".into(),
            );
        }
        LiftSearch::OracleGap { note } => {
            emit(9, DdaOp::Refusal, false, format!("oracle gap: {note}"));
        }
        LiftSearch::SkippedClosed => {
            emit(
                9,
                DdaOp::Integration,
                true,
                "no lift search: branch Closed or Unset".into(),
            );
        }
    }

    let routing = format!(
        "branch={}; survivors={:?}; lift={:?}",
        branch.as_str(),
        q1,
        structure_search
    );
    emit(
        10,
        DdaOp::ResidualProjection,
        true,
        format!("route survivors branch={}", branch.as_str()),
    );

    let term = match (&branch, &structure_search) {
        (DefectBranch::Closed, _) => PrimeTerminal::Certificate,
        (_, LiftSearch::LiftAdmitted { .. }) => PrimeTerminal::Repair,
        (DefectBranch::StabilizedSurvivor, _) => PrimeTerminal::OracleNeeded,
        (DefectBranch::Open, _) => PrimeTerminal::OpenResidual,
        (DefectBranch::Unset, _) => PrimeTerminal::ClosedResidual,
    };
    emit(
        11,
        DdaOp::Terminalize,
        true,
        format!("terminalize {}", term.as_str()),
    );
    let terminal = term;

    let literature_compare = if let Some(note) = adapter.literature_note() {
        emit(
            12,
            DdaOp::Integration,
            true,
            format!(
                "literature compare after terminal={}: {note}",
                terminal.as_str()
            ),
        );
        Some(format!(
            "after_terminal={}; feeds_authority=false; {note}",
            terminal.as_str()
        ))
    } else {
        emit(
            12,
            DdaOp::Integration,
            true,
            "literature compare skipped (no note); still post-terminal only".into(),
        );
        None
    };

    for record in steps.iter_mut() {
        if record.prime_step >= 6 {
            record.phi1_after = phi1;
            record.gamma2_after = gamma2;
        }
    }

    let letter_tape: String = steps.iter().map(|s| s.op.as_str()).collect();
    let letters_spaced = trace.letters();
    let trace_terminal = match trace.terminal() {
        TraceTerminal::Open => "Open".into(),
        TraceTerminal::Terminalized => "Terminalized".into(),
        TraceTerminal::Refused => "Refused".into(),
        TraceTerminal::OracleNeeded { import } => format!("OracleNeeded:{import}"),
        TraceTerminal::UnverifiedTerminal => "UnverifiedTerminal".into(),
    };

    debug_assert_eq!(trace.authority_effect(), AuthorityEffect::None);

    PrimeAlgorithm0Receipt {
        domain: adapter.domain(),
        carrier: Some(admitted.carrier().to_string()),
        primitive_difference: Some(admitted.primitive_difference().to_string()),
        zero_rel: Some(admitted.zero_rel().to_string()),
        cochain,
        q1,
        phi1,
        gamma2,
        observer,
        witnesses,
        structure_search,
        licensed_lift,
        routing,
        literature_compare,
        branch,
        terminal,
        letter_tape,
        letters_spaced,
        trace_terminal,
        residual_family_label: family,
        authority_effect: AuthorityEffect::None,
        steps,
        evidence_provenance: adapter.evidence_provenance(),
    }
}

pub fn run_prime_algorithm_0(adapter: &dyn DomainAdapter) -> PrimeAlgorithm0Receipt {
    let decl = adapter.declaration();
    match crate::prime_algos::prime_algorithm_0_admission::admit(
        &decl,
        adapter.justify_cochain(),
        adapter.cochain_window().as_ref(),
    ) {
        Ok(admitted) => run_admitted(&admitted, adapter),
        Err(refusal) => refusal.to_receipt(adapter),
    }
}

pub use run_prime_algorithm_0 as run_oeprmalg0;

#[cfg(test)]
mod tests {
    use super::*;
    use crate::prime_algos::domain_adapters::{
        CodaResidualAdapter, FspChannelAAdapter, GenericMss0Adapter, MubWallAdapter,
    };

    #[test]
    fn generic_mss0_emits_letter_tape_with_crt() {
        let r = run_prime_algorithm_0(&GenericMss0Adapter);
        assert_eq!(r.authority_effect, AuthorityEffect::None);
        assert!(r.letter_tape.contains('C'));
        assert!(r.letter_tape.contains('R'));
        assert!(r.letter_tape.contains('T'));
        assert_eq!(r.branch, DefectBranch::StabilizedSurvivor);
        assert!(matches!(
            r.terminal,
            PrimeTerminal::Repair | PrimeTerminal::OracleNeeded
        ));
        let lift = r.licensed_lift.expect("generic MSS-0 should admit lift");
        assert!(lift.nine_bits().all_satisfied());
        assert_eq!(lift.lean_module(), "PaperER003.LicensedLiftCertificate");
        assert!(lift.checklist().lift_checklist_complete());
        let last_lit = r.steps.iter().filter(|s| s.prime_step == 12).count();
        assert!(last_lit >= 1);
        let first_t = r.steps.iter().position(|s| s.op == "T").unwrap();
        assert!(r.steps[..first_t].iter().all(|s| s.prime_step != 12));
    }

    #[test]
    fn missing_carrier_refuses() {
        struct Bad;
        impl DomainAdapter for Bad {
            fn domain(&self) -> PrimeDomain {
                PrimeDomain::Generic
            }
            fn declaration(&self) -> DeclarationFill {
                DeclarationFill {
                    carrier: None,
                    primitive_difference: Some("d".into()),
                    zero_rel: Some("z".into()),
                    observer: Some("o".into()),
                    witnesses: vec![],
                }
            }
            fn justify_cochain(&self) -> bool {
                false
            }
            fn cochain_window(&self) -> Option<CochainWindow> {
                None
            }
            fn residual_masses(&self) -> (u64, u64) {
                (0, 0)
            }
            fn lift_proposal(&self, _: DefectBranch) -> LiftProposal {
                LiftProposal::SkipClosed
            }
            fn literature_note(&self) -> Option<String> {
                None
            }
        }
        let r = run_prime_algorithm_0(&Bad);
        assert_eq!(r.terminal, PrimeTerminal::Refusal);
        assert!(r.letter_tape.contains('M'));
        assert!(r.letter_tape.contains('T'));
    }

    #[test]
    fn multi_domain_adapters_all_none_authority() {
        let adapters: Vec<&dyn DomainAdapter> = vec![
            &GenericMss0Adapter,
            &MubWallAdapter,
            &FspChannelAAdapter,
            &CodaResidualAdapter,
        ];
        for a in adapters {
            let r = run_prime_algorithm_0(a);
            assert_eq!(r.authority_effect, AuthorityEffect::None);
            assert!(!r.letter_tape.is_empty());
        }
    }

    #[test]
    fn write_files_emits_letter_tape_and_receipt() {
        let r = run_prime_algorithm_0(&GenericMss0Adapter);
        let dir =
            std::env::temp_dir().join(format!("omega_prime_algorithm_0_{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        r.write_files(&dir).expect("write_files");
        assert!(dir.join("letter_tape.txt").is_file());
        assert!(dir.join("prime_algorithm_0_receipt.json").is_file());
        assert!(dir.join("oeprmalg0_receipt.json").is_file());
        let tape = std::fs::read_to_string(dir.join("letter_tape.txt")).unwrap();
        assert!(tape.starts_with(&r.letter_tape));
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn write_files_still_emits_the_pre_rename_receipt_name() {
        let r = run_prime_algorithm_0(&GenericMss0Adapter);
        let dir = std::env::temp_dir().join(format!(
            "omega_prime_algorithm_0_compat_{}",
            std::process::id()
        ));
        let _ = std::fs::remove_dir_all(&dir);
        r.write_files(&dir).expect("write_files");

        let primary_name = dir.join("prime_algorithm_0_receipt.json");
        let new_name = dir.join("oeprmalg0_receipt.json");
        let old_name = dir.join("prime000_receipt.json");
        assert!(primary_name.is_file(), "primary receipt name was dropped");
        assert!(new_name.is_file(), "oeprmalg0 receipt name was dropped");
        assert!(old_name.is_file(), "pre-rename receipt name was dropped");
        assert_eq!(
            std::fs::read(&primary_name).unwrap(),
            std::fs::read(&old_name).unwrap(),
            "the receipt artifacts must be byte-identical"
        );
        let _ = std::fs::remove_dir_all(&dir);
    }
}
