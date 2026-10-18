use num_rational::BigRational;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[allow(non_camel_case_types)]
#[repr(u8)]
pub enum LayerId {
    FOC = 1,
    MUR = 2,
    CS = 3,
    CS_Q = 4,
    Q = 5,
    A = 6,
    OR = 7,
    FDA = 8,
    #[serde(rename = "GTLA")]
    CODA_GTLA = 9,
}

impl LayerId {
    pub fn name(&self) -> &'static str {
        match self {
            LayerId::FOC => "FOC",
            LayerId::MUR => "MUR",
            LayerId::CS => "CS",
            LayerId::CS_Q => "CS_Q",
            LayerId::Q => "Q",
            LayerId::A => "A",
            LayerId::OR => "OR",
            LayerId::FDA => "FDA",
            LayerId::CODA_GTLA => "GTLA",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LayerExecutionRecord {
    pub layer_id: LayerId,
    pub succeeded: bool,
    pub diagnostic_message: String,
    pub defect_mass: BigRational,
    pub metadata: BTreeMap<String, serde_json::Value>,
}

impl LayerExecutionRecord {
    pub fn new(
        layer_id: LayerId,
        succeeded: bool,
        diagnostic_message: impl Into<String>,
        defect_mass: BigRational,
    ) -> Self {
        Self {
            layer_id,
            succeeded,
            diagnostic_message: diagnostic_message.into(),
            defect_mass,
            metadata: BTreeMap::new(),
        }
    }

    pub fn with_metadata(mut self, key: impl Into<String>, value: serde_json::Value) -> Self {
        self.metadata.insert(key.into(), value);
        self
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitness {
    pub vector: Vec<BigRational>,
    pub linfty_norm: BigRational,
    pub pairing_value: BigRational,
}

impl DualWitness {
    pub fn new(vector: Vec<BigRational>, pairing_value: BigRational) -> Self {
        let mut max_abs = BigRational::from_integer(0.into());
        for v in &vector {
            let abs_v = if v < &BigRational::from_integer(0.into()) {
                -v.clone()
            } else {
                v.clone()
            };
            if abs_v > max_abs {
                max_abs = abs_v;
            }
        }
        Self {
            vector,
            linfty_norm: max_abs,
            pairing_value,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum FirewallDecision {
    PermitAuthorized,
    RouteClosedResidual,
    RouteRefused,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum TerminalKind {
    Authorized,
    ClosedResidual,
    Refused,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuthorityToken {
    pub token_id: String,
    pub granted_externally: bool,
    pub grantee: String,
    pub evidence_digest: String,
    pub timestamp_iso: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ResidualPair {
    pub phi1: BigRational,
    pub gamma2: BigRational,
}

impl ResidualPair {
    pub fn new(phi1: BigRational, gamma2: BigRational) -> Self {
        Self { phi1, gamma2 }
    }

    pub fn is_exact_zero(&self) -> bool {
        self.phi1 == BigRational::from_integer(0.into())
            && self.gamma2 == BigRational::from_integer(0.into())
    }

    pub fn is_coherent(&self) -> bool {
        self.gamma2 == BigRational::from_integer(0.into())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExternalAuthorityGrant {
    pub grant_id: String,
    pub signature_hex: String,
    pub grantee: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ProblemInstance {
    pub problem_id: String,
    pub raw_data: String,
    pub candidate_sieve: Vec<String>,
    pub coarse_profile: Vec<i64>,
    pub fine_profile: Vec<i64>,
    pub projection_map: BTreeMap<i64, i64>,
    pub local_sections: BTreeMap<String, Vec<BigRational>>,
    pub overlaps: BTreeMap<(String, String), bool>,
    pub d0: Vec<Vec<BigRational>>,
    pub d1: Vec<Vec<BigRational>>,
    pub defect_cochain: Vec<BigRational>,
    pub fda_license_granted: bool,
    pub enclosure_interval: (BigRational, BigRational),
}

impl ProblemInstance {
    pub fn new(problem_id: impl Into<String>) -> Self {
        Self {
            problem_id: problem_id.into(),
            raw_data: String::new(),
            candidate_sieve: Vec::new(),
            coarse_profile: Vec::new(),
            fine_profile: Vec::new(),
            projection_map: BTreeMap::new(),
            local_sections: BTreeMap::new(),
            overlaps: BTreeMap::new(),
            d0: Vec::new(),
            d1: Vec::new(),
            defect_cochain: Vec::new(),
            fda_license_granted: false,
            enclosure_interval: (
                BigRational::from_integer(0.into()),
                BigRational::from_integer(1.into()),
            ),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MasterNormalFormOutcome {
    pub problem_id: String,
    pub terminal_kind: TerminalKind,
    pub residual_pair: Option<ResidualPair>,
    pub dual_witness: Option<DualWitness>,
    pub authority_token: Option<AuthorityToken>,
    pub layer_records: Vec<LayerExecutionRecord>,
    pub firewall_decision: FirewallDecision,
    pub reason: String,
    pub primal_repair: Option<Vec<BigRational>>,
    pub evidence_digest: String,
}

impl MasterNormalFormOutcome {
    pub fn is_authorized(&self) -> bool {
        self.terminal_kind == TerminalKind::Authorized
    }

    pub fn is_closed_residual(&self) -> bool {
        self.terminal_kind == TerminalKind::ClosedResidual
    }

    pub fn is_refused(&self) -> bool {
        self.terminal_kind == TerminalKind::Refused
    }
}
