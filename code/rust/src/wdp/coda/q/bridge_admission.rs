
use serde::{Deserialize, Serialize};

use super::bridge_packet::{
    profile_factorization_holds, BridgePacket14, DomainId, FactorizationDefect, QueryValue,
};

pub const BRIDGE_ADMISSIBLE_8_STEP_COUNT: usize = 8;

pub const BRIDGE_ADMISSIBLE_8_STEP_NAMES: [&str; BRIDGE_ADMISSIBLE_8_STEP_COUNT] = [
    "finite_packet_validity",
    "tower_coherence",
    "completion_witness",
    "qheld_debts",
    "factorization_evidence",
    "route_independence",
    "reflection_descent",
    "terminal_agreement",
];

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum ObligationState {
    Verified { witness: String },
    Failed { residual: String },
    DeclaredUnverified { note: String },
}

impl ObligationState {
    pub fn verified(witness: impl Into<String>) -> Self {
        Self::Verified {
            witness: witness.into(),
        }
    }

    pub fn failed(residual: impl Into<String>) -> Self {
        Self::Failed {
            residual: residual.into(),
        }
    }

    pub fn declared_unverified(note: impl Into<String>) -> Self {
        Self::DeclaredUnverified { note: note.into() }
    }

    pub fn holds(&self) -> bool {
        matches!(self, Self::Verified { .. })
    }

    pub fn witness_or_residual(&self) -> &str {
        match self {
            Self::Verified { witness } => witness,
            Self::Failed { residual } => residual,
            Self::DeclaredUnverified { note } => note,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FinitePacketValidity {
    pub index_presented: ObligationState,
    #[serde(rename = "each_a_lambda_finite_gtoc")]
    pub each_a_lambda_finite_coda: ObligationState,
    pub nonvacuous_when_indexed: ObligationState,
}

impl FinitePacketValidity {
    pub fn holds(&self) -> bool {
        self.index_presented.holds()
            && self.each_a_lambda_finite_coda.holds()
            && self.nonvacuous_when_indexed.holds()
    }

    pub fn all_verified_demo() -> Self {
        Self {
            index_presented: ObligationState::verified("index set presented"),
            each_a_lambda_finite_coda: ObligationState::verified("each A_lambda finite GTOC"),
            nonvacuous_when_indexed: ObligationState::verified("nonvacuous when indexed"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TowerCoherence {
    pub paste_transitions: ObligationState,
    pub paste_certificates: ObligationState,
    pub profile_commutes: ObligationState,
}

impl TowerCoherence {
    pub fn holds(&self) -> bool {
        self.paste_transitions.holds()
            && self.paste_certificates.holds()
            && self.profile_commutes.holds()
    }

    pub fn all_verified_demo() -> Self {
        Self {
            paste_transitions: ObligationState::verified("F paste"),
            paste_certificates: ObligationState::verified("chi paste"),
            profile_commutes: ObligationState::verified("profile triangle"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompletionWitness {
    pub named_completion: ObligationState,
    pub supplies_carrier: ObligationState,
}

impl CompletionWitness {
    pub fn holds(&self) -> bool {
        self.named_completion.holds() && self.supplies_carrier.holds()
    }

    pub fn all_verified_demo() -> Self {
        Self {
            named_completion: ObligationState::verified("named completion"),
            supplies_carrier: ObligationState::verified("supplies working carrier"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QHeldDebts {
    pub shadow: ObligationState,
    pub monotonicity: ObligationState,
    pub topology: ObligationState,
    pub formula: ObligationState,
    pub trigger: ObligationState,
}

impl QHeldDebts {
    pub fn paid(&self) -> bool {
        self.shadow.holds()
            && self.monotonicity.holds()
            && self.topology.holds()
            && self.formula.holds()
            && self.trigger.holds()
    }

    pub fn all_paid_demo() -> Self {
        Self {
            shadow: ObligationState::verified("finite shadow"),
            monotonicity: ObligationState::verified("refinement monotonicity"),
            topology: ObligationState::verified("declared topology"),
            formula: ObligationState::verified("certificate formula route"),
            trigger: ObligationState::verified("descent trigger"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FactorizationEvidence {
    pub holds: bool,
    pub detail: String,
}

impl FactorizationEvidence {
    pub fn from_packet(packet: &BridgePacket14) -> Self {
        match profile_factorization_holds(packet) {
            Ok(()) => Self {
                holds: true,
                detail: "profile_factorization: q[x] = q_bar[Prof[x]] for all sample x".into(),
            },
            Err(defect) => Self {
                holds: false,
                detail: format!("R_factor: {defect:?}"),
            },
        }
    }

    pub fn holds(&self) -> bool {
        self.holds
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RouteIndependence {
    pub cofinal_routes_admissible: ObligationState,
    pub terminals_equivalent: ObligationState,
}

impl RouteIndependence {
    pub fn holds(&self) -> bool {
        self.cofinal_routes_admissible.holds() && self.terminals_equivalent.holds()
    }

    pub fn all_verified_demo() -> Self {
        Self {
            cofinal_routes_admissible: ObligationState::verified("cofinal routes admissible"),
            terminals_equivalent: ObligationState::verified("route terminals equivalent"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReflectionDescent {
    pub descends_to_carrier: ObligationState,
    pub reflection_commutes: ObligationState,
}

impl ReflectionDescent {
    pub fn holds(&self) -> bool {
        self.descends_to_carrier.holds() && self.reflection_commutes.holds()
    }

    pub fn all_verified_demo() -> Self {
        Self {
            descends_to_carrier: ObligationState::verified("descends to carrier"),
            reflection_commutes: ObligationState::verified("reflection square"),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct NamedTerminalizers {
    pub tau_q: std::collections::BTreeMap<DomainId, QueryValue>,
    pub tau_coda_cs: std::collections::BTreeMap<DomainId, QueryValue>,
    pub domain: Vec<DomainId>,
}

impl NamedTerminalizers {
    pub fn query_via_qbar_prof(packet: &BridgePacket14) -> Result<Self, FactorizationDefect> {
        let domain = packet.sample_domain();
        if domain.is_empty() {
            return Err(FactorizationDefect::EmptyDomain);
        }
        let mut tau_q = std::collections::BTreeMap::new();
        let mut tau_coda_cs = std::collections::BTreeMap::new();
        for x in &domain {
            let q_x = packet
                .q
                .get(*x)
                .ok_or(FactorizationDefect::MissingQuery(*x))?;
            let prof_x = packet
                .prof
                .get(*x)
                .ok_or(FactorizationDefect::MissingProfile(*x))?;
            let q_bar_px = packet
                .q_bar
                .get(prof_x)
                .ok_or(FactorizationDefect::MissingFactor(prof_x))?;
            tau_q.insert(*x, q_x);
            tau_coda_cs.insert(*x, q_bar_px);
        }
        Ok(Self {
            tau_q,
            tau_coda_cs,
            domain,
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TerminalMismatch {
    pub x: DomainId,
    pub tau_q: QueryValue,
    pub tau_coda_cs: QueryValue,
}

pub fn terminalizers_agree(named: &NamedTerminalizers) -> Result<(), TerminalMismatch> {
    for &x in &named.domain {
        let tq = named.tau_q.get(&x).copied();
        let tc = named.tau_coda_cs.get(&x).copied();
        match (tq, tc) {
            (Some(a), Some(b)) if a == b => {}
            (Some(a), Some(b)) => {
                return Err(TerminalMismatch {
                    x,
                    tau_q: a,
                    tau_coda_cs: b,
                });
            }
            _ => {
                return Err(TerminalMismatch {
                    x,
                    tau_q: tq.unwrap_or(u32::MAX),
                    tau_coda_cs: tc.unwrap_or(u32::MAX),
                });
            }
        }
    }
    if named.domain.is_empty() {
        return Err(TerminalMismatch {
            x: 0,
            tau_q: 0,
            tau_coda_cs: 0,
        });
    }
    Ok(())
}

pub fn terminalizers_agree_from_factorization(
    packet: &BridgePacket14,
) -> Result<NamedTerminalizers, BridgeAdmissionError> {
    profile_factorization_holds(packet).map_err(BridgeAdmissionError::Factorization)?;

    let named = NamedTerminalizers::query_via_qbar_prof(packet)
        .map_err(BridgeAdmissionError::Factorization)?;

    terminalizers_agree(&named).map_err(BridgeAdmissionError::TerminalMismatch)?;

    Ok(named)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TerminalAgreement {
    pub named: NamedTerminalizers,
    pub pointwise: bool,
    pub detail: String,
}

impl TerminalAgreement {
    pub fn holds(&self) -> bool {
        self.pointwise && terminalizers_agree(&self.named).is_ok()
    }

    pub fn from_factorization(packet: &BridgePacket14) -> Result<Self, BridgeAdmissionError> {
        let named = terminalizers_agree_from_factorization(packet)?;
        Ok(Self {
            named,
            pointwise: true,
            detail: "factorization_implies_named_terminalizers_agree (query via q_bar∘Prof)".into(),
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BridgeAdmissible8 {
    pub finite_packet_validity: FinitePacketValidity,
    pub tower_coherence: TowerCoherence,
    pub completion_witness: CompletionWitness,
    pub qheld_debts: QHeldDebts,
    pub factorization_evidence: FactorizationEvidence,
    pub route_independence: RouteIndependence,
    pub reflection_descent: ReflectionDescent,
    pub terminal_agreement: TerminalAgreement,
}

impl BridgeAdmissible8 {
    pub const STEP_COUNT: usize = BRIDGE_ADMISSIBLE_8_STEP_COUNT;

    pub fn holds(&self) -> bool {
        self.finite_packet_validity.holds()
            && self.tower_coherence.holds()
            && self.completion_witness.holds()
            && self.qheld_debts.paid()
            && self.factorization_evidence.holds()
            && self.route_independence.holds()
            && self.reflection_descent.holds()
            && self.terminal_agreement.holds()
    }

    pub fn project_finite_packet_validity(&self) -> bool {
        self.finite_packet_validity.holds()
    }

    pub fn project_tower_coherence(&self) -> bool {
        self.tower_coherence.holds()
    }

    pub fn project_completion_witness(&self) -> bool {
        self.completion_witness.holds()
    }

    pub fn project_qheld_debts(&self) -> bool {
        self.qheld_debts.paid()
    }

    pub fn project_factorization_evidence(&self) -> bool {
        self.factorization_evidence.holds()
    }

    pub fn project_route_independence(&self) -> bool {
        self.route_independence.holds()
    }

    pub fn project_reflection_descent(&self) -> bool {
        self.reflection_descent.holds()
    }

    pub fn project_terminal_agreement(&self) -> bool {
        self.terminal_agreement.holds()
    }

    pub fn project_all_eight(&self) -> [bool; 8] {
        [
            self.project_finite_packet_validity(),
            self.project_tower_coherence(),
            self.project_completion_witness(),
            self.project_qheld_debts(),
            self.project_factorization_evidence(),
            self.project_route_independence(),
            self.project_reflection_descent(),
            self.project_terminal_agreement(),
        ]
    }

    pub fn failing_steps(&self) -> Vec<&'static str> {
        let flags = self.project_all_eight();
        BRIDGE_ADMISSIBLE_8_STEP_NAMES
            .iter()
            .zip(flags.iter())
            .filter_map(|(name, ok)| if *ok { None } else { Some(*name) })
            .collect()
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum BridgeAdmissionError {
    Factorization(FactorizationDefect),
    TerminalMismatch(TerminalMismatch),
    ConditionsFailed {
        failing_steps: Vec<String>,
    },
    ForbiddenStep8FromFlags,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BridgeAdmissionDecision {
    pub is_admissible: bool,
    pub authority_effect: &'static str,
    pub global_green: bool,
    pub status: BridgeAdmissionStatus,
    pub admissible: Option<BridgeAdmissible8>,
    pub failing_steps: Vec<String>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum BridgeAdmissionStatus {
    BoundedEvaluationScope,
    AdmissionFailed,
    AdmissionBlockedDeclaredUnverified,
}

pub fn build_admissible8_demo(
    packet: &BridgePacket14,
) -> Result<BridgeAdmissible8, BridgeAdmissionError> {
    let factorization_evidence = FactorizationEvidence::from_packet(packet);
    if !factorization_evidence.holds() {
        return Err(BridgeAdmissionError::ConditionsFailed {
            failing_steps: vec!["factorization_evidence".into()],
        });
    }
    let terminal_agreement = TerminalAgreement::from_factorization(packet)?;
    Ok(BridgeAdmissible8 {
        finite_packet_validity: FinitePacketValidity::all_verified_demo(),
        tower_coherence: TowerCoherence::all_verified_demo(),
        completion_witness: CompletionWitness::all_verified_demo(),
        qheld_debts: QHeldDebts::all_paid_demo(),
        factorization_evidence,
        route_independence: RouteIndependence::all_verified_demo(),
        reflection_descent: ReflectionDescent::all_verified_demo(),
        terminal_agreement,
    })
}

pub fn admit_bridge(
    packet: &BridgePacket14,
    mut conditions: BridgeAdmissible8,
) -> BridgeAdmissionDecision {
    conditions.factorization_evidence = FactorizationEvidence::from_packet(packet);

    if conditions.factorization_evidence.holds() {
        match TerminalAgreement::from_factorization(packet) {
            Ok(ta) => conditions.terminal_agreement = ta,
            Err(_) => {
            }
        }
    }

    let failing: Vec<String> = conditions
        .failing_steps()
        .into_iter()
        .map(str::to_string)
        .collect();

    if failing.is_empty() && conditions.holds() {
        BridgeAdmissionDecision {
            is_admissible: true,
            authority_effect: "None",
            global_green: false,
            status: BridgeAdmissionStatus::BoundedEvaluationScope,
            admissible: Some(conditions),
            failing_steps: Vec::new(),
        }
    } else {
        BridgeAdmissionDecision {
            is_admissible: false,
            authority_effect: "None",
            global_green: false,
            status: BridgeAdmissionStatus::AdmissionFailed,
            admissible: None,
            failing_steps: failing,
        }
    }
}

pub fn step8_from_step5_and_step2(
    factorization_holds: bool,
    tower_holds: bool,
) -> Result<bool, BridgeAdmissionError> {
    let _ = (factorization_holds, tower_holds);
    Err(BridgeAdmissionError::ForbiddenStep8FromFlags)
}

#[cfg(test)]
mod tests {
    use super::super::bridge_packet::{
        BridgePacket14, FiniteFactorMap, FiniteProfileMap, FiniteQueryMap,
    };
    use super::*;

    fn factoring_packet() -> BridgePacket14 {
        let q = FiniteQueryMap::from_pairs([(0, 10), (1, 10), (2, 20), (3, 20)]);
        let prof = FiniteProfileMap::from_pairs([(0, 0), (1, 0), (2, 1), (3, 1)]);
        let q_bar = FiniteFactorMap::from_pairs([(0, 10), (1, 20)]);
        BridgePacket14::finite_demo(q, prof, q_bar)
    }

    fn non_factoring_packet() -> BridgePacket14 {
        let q = FiniteQueryMap::from_pairs([(0, 10), (1, 99)]);
        let prof = FiniteProfileMap::from_pairs([(0, 0), (1, 0)]);
        let q_bar = FiniteFactorMap::from_pairs([(0, 10)]);
        BridgePacket14::finite_demo(q, prof, q_bar)
    }

    #[test]
    fn step_count_is_eight() {
        assert_eq!(BRIDGE_ADMISSIBLE_8_STEP_COUNT, 8);
        assert_eq!(BRIDGE_ADMISSIBLE_8_STEP_NAMES.len(), 8);
        assert_eq!(BridgeAdmissible8::STEP_COUNT, 8);
    }

    #[test]
    fn factorization_implies_named_terminalizers_agree() {
        let packet = factoring_packet();
        let named = terminalizers_agree_from_factorization(&packet)
            .expect("factorization should discharge named terminals");
        assert!(terminalizers_agree(&named).is_ok());
        for &x in &named.domain {
            assert_eq!(named.tau_q.get(&x), named.tau_coda_cs.get(&x));
        }
    }

    #[test]
    fn terminalizers_disagree_without_factorization() {
        let packet = non_factoring_packet();
        assert!(matches!(
            terminalizers_agree_from_factorization(&packet),
            Err(BridgeAdmissionError::Factorization(_))
        ));
    }

    #[test]
    fn terminalizers_not_automatic_from_tower_flags() {
        let mut tau_q = std::collections::BTreeMap::new();
        let mut tau_coda = std::collections::BTreeMap::new();
        tau_q.insert(0, 0);
        tau_coda.insert(0, 1);
        let disagreeing = NamedTerminalizers {
            tau_q,
            tau_coda_cs: tau_coda,
            domain: vec![0],
        };
        let tower_flags_true = true;
        let completion_flags_true = true;
        let route_flags_true = true;
        assert!(tower_flags_true && completion_flags_true && route_flags_true);
        assert!(terminalizers_agree(&disagreeing).is_err());
        assert_eq!(
            step8_from_step5_and_step2(true, true),
            Err(BridgeAdmissionError::ForbiddenStep8FromFlags)
        );
    }

    #[test]
    fn full_admission_succeeds_when_all_eight_hold() {
        let packet = factoring_packet();
        let adm = build_admissible8_demo(&packet).expect("demo admission bundle");
        assert!(adm.holds());
        assert_eq!(adm.project_all_eight(), [true; 8]);
        assert!(adm.failing_steps().is_empty());

        let decision = admit_bridge(&packet, adm);
        assert!(decision.is_admissible);
        assert_eq!(decision.authority_effect, "None");
        assert!(!decision.global_green);
        assert_eq!(
            decision.status,
            BridgeAdmissionStatus::BoundedEvaluationScope
        );
    }

    #[test]
    fn mutation_missing_finite_packet_validity_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.finite_packet_validity.index_presented = ObligationState::failed("index not presented");
        assert!(!adm.holds());
        assert!(adm.failing_steps().contains(&"finite_packet_validity"));
        let decision = admit_bridge(&packet, adm);
        assert!(!decision.is_admissible);
        assert_eq!(decision.authority_effect, "None");
        assert!(!decision.global_green);
    }

    #[test]
    fn mutation_missing_tower_coherence_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.tower_coherence.paste_transitions = ObligationState::failed("F paste broken");
        assert!(!adm.project_tower_coherence());
        assert!(!adm.holds());
        let decision = admit_bridge(&packet, adm);
        assert!(!decision.is_admissible);
        assert!(decision
            .failing_steps
            .iter()
            .any(|s| s == "tower_coherence"));
    }

    #[test]
    fn mutation_missing_completion_witness_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.completion_witness.named_completion =
            ObligationState::declared_unverified("no named completion");
        assert!(!adm.project_completion_witness());
        assert!(!admit_bridge(&packet, adm).is_admissible);
    }

    #[test]
    fn mutation_missing_qheld_debts_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.qheld_debts.shadow = ObligationState::failed("no finite shadow");
        assert!(!adm.project_qheld_debts());
        assert!(!admit_bridge(&packet, adm).is_admissible);
    }

    #[test]
    fn mutation_missing_factorization_fails() {
        let packet = non_factoring_packet();
        assert!(build_admissible8_demo(&packet).is_err());
        let fake_named = NamedTerminalizers {
            tau_q: [(0, 10)].into_iter().collect(),
            tau_coda_cs: [(0, 10)].into_iter().collect(),
            domain: vec![0],
        };
        let adm = BridgeAdmissible8 {
            finite_packet_validity: FinitePacketValidity::all_verified_demo(),
            tower_coherence: TowerCoherence::all_verified_demo(),
            completion_witness: CompletionWitness::all_verified_demo(),
            qheld_debts: QHeldDebts::all_paid_demo(),
            factorization_evidence: FactorizationEvidence {
                holds: true,
                detail: "fake".into(),
            },
            route_independence: RouteIndependence::all_verified_demo(),
            reflection_descent: ReflectionDescent::all_verified_demo(),
            terminal_agreement: TerminalAgreement {
                named: fake_named,
                pointwise: true,
                detail: "fake".into(),
            },
        };
        let decision = admit_bridge(&packet, adm);
        assert!(!decision.is_admissible);
        assert!(decision
            .failing_steps
            .iter()
            .any(|s| s == "factorization_evidence"));
    }

    #[test]
    fn mutation_missing_route_independence_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.route_independence.terminals_equivalent = ObligationState::failed("routes disagree");
        assert!(!adm.project_route_independence());
        assert!(!admit_bridge(&packet, adm).is_admissible);
    }

    #[test]
    fn mutation_missing_reflection_descent_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.reflection_descent.descends_to_carrier = ObligationState::failed("does not descend");
        assert!(!adm.project_reflection_descent());
        assert!(!admit_bridge(&packet, adm).is_admissible);
    }

    #[test]
    fn mutation_missing_terminal_agreement_fails() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.factorization_evidence = FactorizationEvidence {
            holds: false,
            detail: "forced fail".into(),
        };
        adm.terminal_agreement.pointwise = false;
        adm.terminal_agreement.named.tau_coda_cs.insert(0, 999);
        let bad = non_factoring_packet();
        let decision = admit_bridge(&bad, adm);
        assert!(!decision.is_admissible);
        assert_eq!(decision.authority_effect, "None");
    }

    #[test]
    fn terminal_agreement_consumes_factorization_not_flags_alone() {
        let packet = factoring_packet();
        assert!(step8_from_step5_and_step2(true, true).is_err());
        let ta = TerminalAgreement::from_factorization(&packet).unwrap();
        assert!(ta.holds());
        assert!(terminalizers_agree(&ta.named).is_ok());
    }

    #[test]
    fn authority_effect_none_on_all_paths() {
        let good = factoring_packet();
        let bad = non_factoring_packet();
        let adm = build_admissible8_demo(&good).unwrap();
        let d_ok = admit_bridge(&good, adm.clone());
        let d_bad = admit_bridge(&bad, adm);
        assert_eq!(d_ok.authority_effect, "None");
        assert_eq!(d_bad.authority_effect, "None");
        assert!(!d_ok.global_green);
        assert!(!d_bad.global_green);
        assert_eq!(good.authority_effect(), "None");
    }

    #[test]
    fn declared_unverified_blocks_full_admission() {
        let packet = factoring_packet();
        let mut adm = build_admissible8_demo(&packet).unwrap();
        adm.completion_witness.supplies_carrier =
            ObligationState::declared_unverified("completion residual open");
        assert!(!adm.holds());
        assert!(!adm.completion_witness.holds());
    }
}
