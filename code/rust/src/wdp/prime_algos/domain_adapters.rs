
use crate::prime_algos::licensed_lift_gate::{
    certificate_from_labels, NineUpLiftBits, PaperEr003LiftCertificate,
};
use crate::prime_algos::prime_algorithm_0::{
    CochainWindow, DeclarationFill, DefectBranch, DomainAdapter, LiftProposal,
    PrimeDomain,
};

fn licensed_nine() -> NineUpLiftBits {
    NineUpLiftBits::all_true()
}

fn resolve_cert(residual: &str, operator: &str) -> PaperEr003LiftCertificate {
    certificate_from_labels(
        residual,
        &format!("mss1:{residual}"),
        operator,
        true,
        true,
        true,
        false,
    )
}

pub struct GenericMss0Adapter;

impl DomainAdapter for GenericMss0Adapter {
    fn domain(&self) -> PrimeDomain {
        PrimeDomain::Generic
    }

    fn declaration(&self) -> DeclarationFill {
        DeclarationFill {
            carrier: Some("finite_token_set:{delta_0}".into()),
            primitive_difference: Some("delta_0".into()),
            zero_rel: Some("exact_collapse_of_declared_sameness_only".into()),
            observer: Some("unit_weight_l1_profile".into()),
            witnesses: vec!["replay:exhaust_trace".into(), "hash:toy".into()],
        }
    }

    fn justify_cochain(&self) -> bool {
        true
    }

    fn cochain_window(&self) -> Option<CochainWindow> {
        Some(CochainWindow {
            dim_c0: 2,
            dim_c1: 1,
            dim_c2: 0,
            square_zero: true,
            l1_defect_mass: 0,
        })
    }

    fn residual_masses(&self) -> (u64, u64) {
        (1, 0)
    }

    fn lift_proposal(&self, branch: DefectBranch) -> LiftProposal {
        match branch {
            DefectBranch::StabilizedSurvivor => LiftProposal::Candidate {
                generators: vec!["resolve_delta_0".into()],
                nine_bits: licensed_nine(),
                certificate: resolve_cert("delta_0", "resolve_delta_0"),
            },
            DefectBranch::Open => LiftProposal::SameLevelRepair,
            _ => LiftProposal::SkipClosed,
        }
    }

    fn literature_note(&self) -> Option<String> {
        Some("FOC Anomalon boundary; GOMC LGGR; MSS reconstruction spine".into())
    }

    fn residual_family_label(&self) -> String {
        "generic:anomalon_delta0".into()
    }
}

pub struct MubWallAdapter;

impl DomainAdapter for MubWallAdapter {
    fn domain(&self) -> PrimeDomain {
        PrimeDomain::Mub
    }

    fn declaration(&self) -> DeclarationFill {
        DeclarationFill {
            carrier: Some(
                "Declared finite product triple + candidate fourth vector search in C^d".into(),
            ),
            primitive_difference: Some(
                "Non-sameness of exact MU ZeroRel vs candidate stationarity residual".into(),
            ),
            zero_rel: Some(
                "Exact |<e_i,v>|^2 = 1/d for fixed vectors (not float tolerance as theorem)".into(),
            ),
            observer: Some("Declared wall functional / chart — not View-from-Nowhere".into()),
            witnesses: vec![
                "crates/mub share packs".into(),
                "public-export receipts".into(),
            ],
        }
    }

    fn justify_cochain(&self) -> bool {
        false
    }

    fn cochain_window(&self) -> Option<CochainWindow> {
        None
    }

    fn residual_masses(&self) -> (u64, u64) {
        (1, 0)
    }

    fn lift_proposal(&self, _: DefectBranch) -> LiftProposal {
        LiftProposal::OracleGap {
            note: "Global MUB(6)=3 remains OPEN; no finite lift admitted".into(),
        }
    }

    fn literature_note(&self) -> Option<String> {
        Some("ONLY after terminal — Zauner/Renes etc. do not mint theorem".into())
    }

    fn residual_family_label(&self) -> String {
        "mub:wall_open_mub6".into()
    }
}

pub struct FspChannelAAdapter;

impl DomainAdapter for FspChannelAAdapter {
    fn domain(&self) -> PrimeDomain {
        PrimeDomain::Fsp
    }

    fn declaration(&self) -> DeclarationFill {
        DeclarationFill {
            carrier: Some("Channel A parity: F2^V, F2^E, F2^F finite graph".into()),
            primitive_difference: Some(
                "Packet-local delta on declared finite sign configurations".into(),
            ),
            zero_rel: Some("LocalRepairRel / CochainZeroRel as declared in Paper 042".into()),
            observer: Some("Declared observer O with typed readout".into()),
            witnesses: vec![
                "Lean PaperQF partial kernels".into(),
                "replay commands".into(),
            ],
        }
    }

    fn justify_cochain(&self) -> bool {
        true
    }

    fn cochain_window(&self) -> Option<CochainWindow> {
        Some(CochainWindow {
            dim_c0: 3,
            dim_c1: 3,
            dim_c2: 1,
            square_zero: true,
            l1_defect_mass: 0,
        })
    }

    fn residual_masses(&self) -> (u64, u64) {
        (1, 1)
    }

    fn lift_proposal(&self, branch: DefectBranch) -> LiftProposal {
        match branch {
            DefectBranch::Open => LiftProposal::SameLevelRepair,
            DefectBranch::StabilizedSurvivor => LiftProposal::OracleGap {
                note: "general FSP not solved".into(),
            },
            _ => LiftProposal::SkipClosed,
        }
    }

    fn literature_note(&self) -> Option<String> {
        Some("ONLY after terminal — Troyer-Wiese 2005 NP-hardness remains".into())
    }

    fn residual_family_label(&self) -> String {
        "fsp:channel_a_sign_class".into()
    }
}

pub struct CodaResidualAdapter;

impl DomainAdapter for CodaResidualAdapter {
    fn domain(&self) -> PrimeDomain {
        PrimeDomain::Coda
    }

    fn declaration(&self) -> DeclarationFill {
        DeclarationFill {
            carrier: Some("GTOC finite cover packet / residual ledger host".into()),
            primitive_difference: Some(
                "carrier-Structure vs residual-Structure non-sameness".into(),
            ),
            zero_rel: Some("declared exact residual collapse under FOC repair class".into()),
            observer: Some("declared GTOC ℓ¹ unit-weight observer".into()),
            witnesses: vec![
                "PaperER003 residual terminalizer contracts".into(),
                "encyclopedia residual ledgers".into(),
            ],
        }
    }

    fn justify_cochain(&self) -> bool {
        true
    }

    fn cochain_window(&self) -> Option<CochainWindow> {
        Some(CochainWindow {
            dim_c0: 2,
            dim_c1: 1,
            dim_c2: 0,
            square_zero: true,
            l1_defect_mass: 0,
        })
    }

    fn residual_masses(&self) -> (u64, u64) {
        (1, 0)
    }

    fn lift_proposal(&self, branch: DefectBranch) -> LiftProposal {
        match branch {
            DefectBranch::StabilizedSurvivor => LiftProposal::Candidate {
                generators: vec!["coda_residual_refine".into()],
                nine_bits: licensed_nine(),
                certificate: resolve_cert("coda_q1", "coda_residual_refine"),
            },
            DefectBranch::Open => LiftProposal::SameLevelRepair,
            _ => LiftProposal::SkipClosed,
        }
    }

    fn literature_note(&self) -> Option<String> {
        Some("CODA carrier/residual firewall; Q quarantine non-promotion".into())
    }

    fn residual_family_label(&self) -> String {
        "coda:q1_residual_firewall".into()
    }
}

#[derive(Debug, Clone)]
pub struct SymbolGameExpressivityAdapter {
    pub phi1: u64,
    pub gamma2: u64,
    pub square_zero: bool,
    pub problem_label: String,
}

impl Default for SymbolGameExpressivityAdapter {
    fn default() -> Self {
        Self {
            phi1: 3,
            gamma2: 0,
            square_zero: true,
            problem_label: "expressivity_obstructed_default".into(),
        }
    }
}

impl DomainAdapter for SymbolGameExpressivityAdapter {
    fn domain(&self) -> PrimeDomain {
        PrimeDomain::SymbolGame
    }

    fn declaration(&self) -> DeclarationFill {
        DeclarationFill {
            carrier: Some(format!("symbol_game::expressivity:{}", self.problem_label)),
            primitive_difference: Some(
                "local patch naming non-sameness on overlap discrepancies".into(),
            ),
            zero_rel: Some("ContextuallyGlueable (o_n = 0 in im d0)".into()),
            observer: Some("expressivity_norm_face / unit ℓ¹ diagnostic".into()),
            witnesses: vec![
                "omega_symbol_game::expressivity".into(),
                "engine_functional exact Phi1/Gamma2 rails".into(),
            ],
        }
    }

    fn justify_cochain(&self) -> bool {
        true
    }

    fn cochain_window(&self) -> Option<CochainWindow> {
        Some(CochainWindow {
            dim_c0: 3,
            dim_c1: 3,
            dim_c2: 0,
            square_zero: self.square_zero,
            l1_defect_mass: if self.square_zero { 0 } else { 1 },
        })
    }

    fn residual_masses(&self) -> (u64, u64) {
        (self.phi1, self.gamma2)
    }

    fn lift_proposal(&self, branch: DefectBranch) -> LiftProposal {
        match branch {
            DefectBranch::StabilizedSurvivor if self.phi1 > 0 => LiftProposal::Candidate {
                generators: vec!["expressivity_meta_norm".into()],
                nine_bits: licensed_nine(),
                certificate: resolve_cert(&self.problem_label, "expressivity_meta_norm"),
            },
            DefectBranch::Open => LiftProposal::SameLevelRepair,
            DefectBranch::Closed => LiftProposal::SkipClosed,
            _ => LiftProposal::OracleGap {
                note: "expressivity obstruction unresolved".into(),
            },
        }
    }

    fn literature_note(&self) -> Option<String> {
        Some("Symbol Game math spine; FOC Čech gate; ENC-0891 no Phi1 authority".into())
    }

    fn residual_family_label(&self) -> String {
        format!("symbol_game:{}", self.problem_label)
    }
}

pub fn builtin_adapter_roster() -> Vec<Box<dyn DomainAdapter>> {
    vec![
        Box::new(GenericMss0Adapter),
        Box::new(MubWallAdapter),
        Box::new(FspChannelAAdapter),
        Box::new(CodaResidualAdapter),
        Box::new(SymbolGameExpressivityAdapter::default()),
    ]
}
