
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum NineCondition {
    Exhaustion,
    Refusal,
    Traceability,
    Preservation,
    Conservativity,
    ObstructionResolution,
    GeneratorMinimality,
    Replay,
    AuthorityFence,
}

impl NineCondition {
    pub const ALL: [NineCondition; 9] = [
        NineCondition::Exhaustion,
        NineCondition::Refusal,
        NineCondition::Traceability,
        NineCondition::Preservation,
        NineCondition::Conservativity,
        NineCondition::ObstructionResolution,
        NineCondition::GeneratorMinimality,
        NineCondition::Replay,
        NineCondition::AuthorityFence,
    ];

    pub const fn slot_name(self) -> &'static str {
        match self {
            NineCondition::Exhaustion => "exhaustion",
            NineCondition::Refusal => "refusal",
            NineCondition::Traceability => "traceability",
            NineCondition::Preservation => "preservation",
            NineCondition::Conservativity => "conservativity",
            NineCondition::ObstructionResolution => "obstruction_resolution",
            NineCondition::GeneratorMinimality => "generator_minimality",
            NineCondition::Replay => "replay",
            NineCondition::AuthorityFence => "authority_fence",
        }
    }

    pub const fn receipt_kind(self) -> &'static str {
        match self {
            NineCondition::Exhaustion => "exhaustion",
            NineCondition::Refusal => "refusal",
            NineCondition::Traceability => "traceability",
            NineCondition::Preservation => "preservation",
            NineCondition::Conservativity => "conservativity",
            NineCondition::ObstructionResolution => "obstruction_resolution",
            NineCondition::GeneratorMinimality => "minimality",
            NineCondition::Replay => "replay",
            NineCondition::AuthorityFence => "authority_fence",
        }
    }

    pub const fn expected_witness_kind(self) -> WitnessKind {
        match self {
            NineCondition::Exhaustion => WitnessKind::ExhaustionTrace,
            NineCondition::Refusal => WitnessKind::PrimitiveDifference,
            NineCondition::Traceability => WitnessKind::PrimitiveDifference,
            NineCondition::Preservation => WitnessKind::ConservativeEmbedding,
            NineCondition::Conservativity => WitnessKind::ConservativeEmbedding,
            NineCondition::ObstructionResolution => WitnessKind::PrimitiveDifference,
            NineCondition::GeneratorMinimality => WitnessKind::MinimalityProof,
            NineCondition::Replay => WitnessKind::ReplayReceipt,
            NineCondition::AuthorityFence => WitnessKind::ReplayReceipt,
        }
    }

    pub const fn index(self) -> u8 {
        match self {
            NineCondition::Exhaustion => 1,
            NineCondition::Refusal => 2,
            NineCondition::Traceability => 3,
            NineCondition::Preservation => 4,
            NineCondition::Conservativity => 5,
            NineCondition::ObstructionResolution => 6,
            NineCondition::GeneratorMinimality => 7,
            NineCondition::Replay => 8,
            NineCondition::AuthorityFence => 9,
        }
    }
}

impl std::fmt::Display for NineCondition {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.slot_name())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum WitnessKind {
    ExhaustionTrace,
    PrimitiveDifference,
    ConservativeEmbedding,
    MinimalityProof,
    ReplayReceipt,
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum ConditionWitness {
    ExhaustionTrace { steps: Vec<String>, closed: bool },
    PrimitiveDifference {
        left: String,
        right: String,
        delta_id: String,
    },
    ConservativeEmbedding {
        source: String,
        target: String,
        loss_ledger_ref: String,
    },
    MinimalityProof {
        candidate: String,
        competitors_ruled_out: Vec<String>,
    },
    ReplayReceipt {
        content_hash: String,
        replay_ok: bool,
    },
    Missing { residual: String },
}

impl ConditionWitness {
    pub fn kind(&self) -> Option<WitnessKind> {
        match self {
            ConditionWitness::ExhaustionTrace { .. } => Some(WitnessKind::ExhaustionTrace),
            ConditionWitness::PrimitiveDifference { .. } => Some(WitnessKind::PrimitiveDifference),
            ConditionWitness::ConservativeEmbedding { .. } => {
                Some(WitnessKind::ConservativeEmbedding)
            }
            ConditionWitness::MinimalityProof { .. } => Some(WitnessKind::MinimalityProof),
            ConditionWitness::ReplayReceipt { .. } => Some(WitnessKind::ReplayReceipt),
            ConditionWitness::Missing { .. } => None,
        }
    }

    pub fn is_missing(&self) -> bool {
        matches!(self, ConditionWitness::Missing { .. })
    }

    pub fn payload_satisfied(&self) -> bool {
        match self {
            ConditionWitness::ExhaustionTrace { steps, closed } => {
                *closed && !steps.is_empty() && steps.iter().all(|s| !s.trim().is_empty())
            }
            ConditionWitness::PrimitiveDifference {
                left,
                right,
                delta_id,
            } => !left.trim().is_empty() && !right.trim().is_empty() && !delta_id.trim().is_empty(),
            ConditionWitness::ConservativeEmbedding {
                source,
                target,
                loss_ledger_ref,
            } => {
                !source.trim().is_empty()
                    && !target.trim().is_empty()
                    && !loss_ledger_ref.trim().is_empty()
            }
            ConditionWitness::MinimalityProof {
                candidate,
                competitors_ruled_out,
            } => {
                !candidate.trim().is_empty()
                    && competitors_ruled_out.iter().all(|c| !c.trim().is_empty())
            }
            ConditionWitness::ReplayReceipt {
                content_hash,
                replay_ok,
            } => *replay_ok && !content_hash.trim().is_empty(),
            ConditionWitness::Missing { .. } => false,
        }
    }

    pub fn satisfies_condition(&self, condition: NineCondition) -> bool {
        match self.kind() {
            Some(k) if k == condition.expected_witness_kind() => self.payload_satisfied(),
            _ => false,
        }
    }

    pub fn failure_reason(&self, condition: NineCondition) -> Option<String> {
        if let ConditionWitness::Missing { residual } = self {
            return Some(format!(
                "slot {} missing: {}",
                condition.slot_name(),
                residual
            ));
        }
        match self.kind() {
            Some(k) if k != condition.expected_witness_kind() => Some(format!(
                "slot {} kind mismatch: got {:?}, expected {:?}",
                condition.slot_name(),
                k,
                condition.expected_witness_kind()
            )),
            Some(_) if !self.payload_satisfied() => Some(format!(
                "slot {} witness payload unsatisfied",
                condition.slot_name()
            )),
            Some(_) => None,
            None => Some(format!("slot {} missing residual", condition.slot_name())),
        }
    }

    pub fn missing(residual: impl Into<String>) -> Self {
        ConditionWitness::Missing {
            residual: residual.into(),
        }
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ConditionSlot {
    pub condition: NineCondition,
    pub witness: ConditionWitness,
}

impl ConditionSlot {
    pub fn new(condition: NineCondition, witness: ConditionWitness) -> Self {
        Self { condition, witness }
    }

    pub fn is_satisfied(&self) -> bool {
        self.witness.satisfies_condition(self.condition)
    }

    pub fn failure_reason(&self) -> Option<String> {
        self.witness.failure_reason(self.condition)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct NineConditionUpliftPacket {
    pub source_stage_id: Option<String>,
    pub target_stage_id: Option<String>,
    pub exhaustion: ConditionWitness,
    pub refusal: ConditionWitness,
    pub traceability: ConditionWitness,
    pub preservation: ConditionWitness,
    pub conservativity: ConditionWitness,
    pub obstruction_resolution: ConditionWitness,
    pub generator_minimality: ConditionWitness,
    pub replay: ConditionWitness,
    pub authority_fence: ConditionWitness,
}

impl NineConditionUpliftPacket {
    pub fn empty() -> Self {
        Self {
            source_stage_id: None,
            target_stage_id: None,
            exhaustion: ConditionWitness::missing("exhaustion not supplied"),
            refusal: ConditionWitness::missing("refusal not supplied"),
            traceability: ConditionWitness::missing("traceability not supplied"),
            preservation: ConditionWitness::missing("preservation not supplied"),
            conservativity: ConditionWitness::missing("conservativity not supplied"),
            obstruction_resolution: ConditionWitness::missing(
                "obstruction_resolution not supplied",
            ),
            generator_minimality: ConditionWitness::missing("generator_minimality not supplied"),
            replay: ConditionWitness::missing("replay not supplied"),
            authority_fence: ConditionWitness::missing("authority_fence not supplied"),
        }
    }

    pub fn diagnostic_fixture() -> Self {
        Self {
            source_stage_id: Some("fixture.mss.0".into()),
            target_stage_id: Some("fixture.mss.1".into()),
            exhaustion: ConditionWitness::ExhaustionTrace {
                steps: vec![
                    "attempt same-level repair A".into(),
                    "attempt same-level quotient B".into(),
                    "exhaustion closed".into(),
                ],
                closed: true,
            },
            refusal: ConditionWitness::PrimitiveDifference {
                left: "same_level_closure".into(),
                right: "obstruction_residue".into(),
                delta_id: "delta:refusal:fixture.0".into(),
            },
            traceability: ConditionWitness::PrimitiveDifference {
                left: "generator.fixture.0".into(),
                right: "obstruction.fixture.0".into(),
                delta_id: "delta:trace:fixture.0".into(),
            },
            preservation: ConditionWitness::ConservativeEmbedding {
                source: "fixture.mss.0".into(),
                target: "fixture.mss.1".into(),
                loss_ledger_ref: "ledger:preservation:fixture.0".into(),
            },
            conservativity: ConditionWitness::ConservativeEmbedding {
                source: "fixture.mss.0/vocabulary".into(),
                target: "fixture.mss.1/restricted".into(),
                loss_ledger_ref: "ledger:conservativity:fixture.0".into(),
            },
            obstruction_resolution: ConditionWitness::PrimitiveDifference {
                left: "obstruction.fixture.0/pre".into(),
                right: "obstruction.fixture.0/refined".into(),
                delta_id: "delta:resolve:fixture.0".into(),
            },
            generator_minimality: ConditionWitness::MinimalityProof {
                candidate: "generator.fixture.0".into(),
                competitors_ruled_out: vec!["generator.alt.1".into(), "generator.alt.2".into()],
            },
            replay: ConditionWitness::ReplayReceipt {
                content_hash: "digest:fixture:replay".into(),
                replay_ok: true,
            },
            authority_fence: ConditionWitness::ReplayReceipt {
                content_hash: "digest:fixture:authority_fence:None".into(),
                replay_ok: true,
            },
        }
    }

    pub fn slots(&self) -> [ConditionSlot; 9] {
        [
            ConditionSlot::new(NineCondition::Exhaustion, self.exhaustion.clone()),
            ConditionSlot::new(NineCondition::Refusal, self.refusal.clone()),
            ConditionSlot::new(NineCondition::Traceability, self.traceability.clone()),
            ConditionSlot::new(NineCondition::Preservation, self.preservation.clone()),
            ConditionSlot::new(NineCondition::Conservativity, self.conservativity.clone()),
            ConditionSlot::new(
                NineCondition::ObstructionResolution,
                self.obstruction_resolution.clone(),
            ),
            ConditionSlot::new(
                NineCondition::GeneratorMinimality,
                self.generator_minimality.clone(),
            ),
            ConditionSlot::new(NineCondition::Replay, self.replay.clone()),
            ConditionSlot::new(NineCondition::AuthorityFence, self.authority_fence.clone()),
        ]
    }

    pub fn witness_mut(&mut self, condition: NineCondition) -> &mut ConditionWitness {
        match condition {
            NineCondition::Exhaustion => &mut self.exhaustion,
            NineCondition::Refusal => &mut self.refusal,
            NineCondition::Traceability => &mut self.traceability,
            NineCondition::Preservation => &mut self.preservation,
            NineCondition::Conservativity => &mut self.conservativity,
            NineCondition::ObstructionResolution => &mut self.obstruction_resolution,
            NineCondition::GeneratorMinimality => &mut self.generator_minimality,
            NineCondition::Replay => &mut self.replay,
            NineCondition::AuthorityFence => &mut self.authority_fence,
        }
    }

    pub fn witness(&self, condition: NineCondition) -> &ConditionWitness {
        match condition {
            NineCondition::Exhaustion => &self.exhaustion,
            NineCondition::Refusal => &self.refusal,
            NineCondition::Traceability => &self.traceability,
            NineCondition::Preservation => &self.preservation,
            NineCondition::Conservativity => &self.conservativity,
            NineCondition::ObstructionResolution => &self.obstruction_resolution,
            NineCondition::GeneratorMinimality => &self.generator_minimality,
            NineCondition::Replay => &self.replay,
            NineCondition::AuthorityFence => &self.authority_fence,
        }
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub fn evaluate(&self) -> UpliftEvaluation {
        let mut failed: Vec<FailedSlot> = Vec::new();
        for slot in self.slots() {
            if let Some(reason) = slot.failure_reason() {
                failed.push(FailedSlot {
                    condition: slot.condition,
                    slot_name: slot.condition.slot_name().to_string(),
                    reason,
                    missing: slot.witness.is_missing(),
                });
            }
        }

        debug_assert_eq!(self.authority_effect(), AuthorityEffect::None);

        if failed.is_empty() {
            UpliftEvaluation::AcceptDiagnostic {
                message: "all nine witnessed conditions satisfied (diagnostic only; \
                          not a Lean uplift proof; AuthorityEffect::None)"
                    .into(),
                authority_effect: AuthorityEffect::None,
                conditions_ok: NineCondition::ALL
                    .iter()
                    .map(|c| c.slot_name().to_string())
                    .collect(),
            }
        } else {
            UpliftEvaluation::RejectUntilPatched {
                failed_slots: failed,
                authority_effect: AuthorityEffect::None,
            }
        }
    }

    pub fn evaluation_matrix(&self) -> Vec<ConditionMatrixRow> {
        self.slots()
            .into_iter()
            .map(|slot| ConditionMatrixRow {
                condition: slot.condition,
                slot_name: slot.condition.slot_name(),
                expected_kind: slot.condition.expected_witness_kind(),
                actual_kind: slot.witness.kind(),
                satisfied: slot.is_satisfied(),
                missing: slot.witness.is_missing(),
            })
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ConditionMatrixRow {
    pub condition: NineCondition,
    pub slot_name: &'static str,
    pub expected_kind: WitnessKind,
    pub actual_kind: Option<WitnessKind>,
    pub satisfied: bool,
    pub missing: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FailedSlot {
    pub condition: NineCondition,
    pub slot_name: String,
    pub reason: String,
    pub missing: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "verdict", rename_all = "snake_case")]
pub enum UpliftEvaluation {
    AcceptDiagnostic {
        message: String,
        authority_effect: AuthorityEffect,
        conditions_ok: Vec<String>,
    },
    RejectUntilPatched {
        failed_slots: Vec<FailedSlot>,
        authority_effect: AuthorityEffect,
    },
}

impl UpliftEvaluation {
    pub fn is_accept(&self) -> bool {
        matches!(self, UpliftEvaluation::AcceptDiagnostic { .. })
    }

    pub fn is_reject(&self) -> bool {
        matches!(self, UpliftEvaluation::RejectUntilPatched { .. })
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        match self {
            UpliftEvaluation::AcceptDiagnostic {
                authority_effect, ..
            }
            | UpliftEvaluation::RejectUntilPatched {
                authority_effect, ..
            } => authority_effect.clone(),
        }
    }

    pub fn failed_slot_names(&self) -> Vec<String> {
        match self {
            UpliftEvaluation::AcceptDiagnostic { .. } => Vec::new(),
            UpliftEvaluation::RejectUntilPatched { failed_slots, .. } => {
                failed_slots.iter().map(|f| f.slot_name.clone()).collect()
            }
        }
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, Default)]
pub struct LegacyNineBooleans {
    pub exhaustion_trace: bool,
    pub refusal_or_failure_witness: bool,
    pub generator_traceability: bool,
    pub preservation: bool,
    pub conservativity: bool,
    pub obstruction_resolution: bool,
    pub minimality: bool,
    pub replayability: bool,
    pub authority_preservation: bool,
}

impl LegacyNineBooleans {
    pub fn all_true() -> Self {
        Self {
            exhaustion_trace: true,
            refusal_or_failure_witness: true,
            generator_traceability: true,
            preservation: true,
            conservativity: true,
            obstruction_resolution: true,
            minimality: true,
            replayability: true,
            authority_preservation: true,
        }
    }

    pub fn all_satisfied_as_bools(&self) -> bool {
        self.exhaustion_trace
            && self.refusal_or_failure_witness
            && self.generator_traceability
            && self.preservation
            && self.conservativity
            && self.obstruction_resolution
            && self.minimality
            && self.replayability
            && self.authority_preservation
    }

    pub fn into_witnessed_packet(self) -> NineConditionUpliftPacket {
        fn bit_residual(name: &str, bit: bool) -> ConditionWitness {
            if bit {
                ConditionWitness::missing(format!(
                    "legacy boolean {name}=true does not constitute a witness; \
                     supply a typed ConditionWitness"
                ))
            } else {
                ConditionWitness::missing(format!("legacy boolean {name}=false"))
            }
        }

        NineConditionUpliftPacket {
            source_stage_id: None,
            target_stage_id: None,
            exhaustion: bit_residual("exhaustion_trace", self.exhaustion_trace),
            refusal: bit_residual(
                "refusal_or_failure_witness",
                self.refusal_or_failure_witness,
            ),
            traceability: bit_residual("generator_traceability", self.generator_traceability),
            preservation: bit_residual("preservation", self.preservation),
            conservativity: bit_residual("conservativity", self.conservativity),
            obstruction_resolution: bit_residual(
                "obstruction_resolution",
                self.obstruction_resolution,
            ),
            generator_minimality: bit_residual("minimality", self.minimality),
            replay: bit_residual("replayability", self.replayability),
            authority_fence: bit_residual("authority_preservation", self.authority_preservation),
        }
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn nine_conditions_match_lean_field_order() {
        let names: Vec<_> = NineCondition::ALL.iter().map(|c| c.slot_name()).collect();
        assert_eq!(
            names,
            vec![
                "exhaustion",
                "refusal",
                "traceability",
                "preservation",
                "conservativity",
                "obstruction_resolution",
                "generator_minimality",
                "replay",
                "authority_fence",
            ]
        );
        for (i, c) in NineCondition::ALL.iter().enumerate() {
            assert_eq!(c.index() as usize, i + 1);
        }
    }

    #[test]
    fn diagnostic_fixture_accepts_with_authority_none() {
        let packet = NineConditionUpliftPacket::diagnostic_fixture();
        let eval = packet.evaluate();
        assert!(
            eval.is_accept(),
            "fixture should accept diagnostically: {eval:?}"
        );
        assert_eq!(eval.authority_effect(), AuthorityEffect::None);
        assert_eq!(packet.authority_effect(), AuthorityEffect::None);

        match eval {
            UpliftEvaluation::AcceptDiagnostic { conditions_ok, .. } => {
                assert_eq!(conditions_ok.len(), 9);
            }
            other => panic!("expected AcceptDiagnostic, got {other:?}"),
        }

        let matrix = packet.evaluation_matrix();
        assert_eq!(matrix.len(), 9);
        assert!(matrix.iter().all(|row| row.satisfied && !row.missing));
    }

    #[test]
    fn empty_packet_rejects_all_nine() {
        let packet = NineConditionUpliftPacket::empty();
        let eval = packet.evaluate();
        assert!(eval.is_reject());
        assert_eq!(eval.authority_effect(), AuthorityEffect::None);
        let failed = eval.failed_slot_names();
        assert_eq!(failed.len(), 9);
        for c in NineCondition::ALL {
            assert!(
                failed.iter().any(|n| n == c.slot_name()),
                "missing failure for {}",
                c.slot_name()
            );
        }
    }

    #[test]
    fn mutation_negative_flipping_any_slot_to_missing_fails() {
        for condition in NineCondition::ALL {
            let mut packet = NineConditionUpliftPacket::diagnostic_fixture();
            *packet.witness_mut(condition) =
                ConditionWitness::missing(format!("mutated {} to Missing", condition.slot_name()));
            let eval = packet.evaluate();
            assert!(
                eval.is_reject(),
                "flipping {} to Missing must reject",
                condition.slot_name()
            );
            let failed = eval.failed_slot_names();
            assert_eq!(
                failed,
                vec![condition.slot_name().to_string()],
                "only {} should fail after mutation",
                condition.slot_name()
            );
            assert_eq!(eval.authority_effect(), AuthorityEffect::None);
        }
    }

    #[test]
    fn mutation_negative_unclosed_exhaustion_fails() {
        let mut packet = NineConditionUpliftPacket::diagnostic_fixture();
        packet.exhaustion = ConditionWitness::ExhaustionTrace {
            steps: vec!["partial step".into()],
            closed: false,
        };
        let eval = packet.evaluate();
        assert!(eval.is_reject());
        assert_eq!(eval.failed_slot_names(), vec!["exhaustion".to_string()]);
    }

    #[test]
    fn mutation_negative_replay_not_ok_fails() {
        let mut packet = NineConditionUpliftPacket::diagnostic_fixture();
        packet.replay = ConditionWitness::ReplayReceipt {
            content_hash: "digest:x".into(),
            replay_ok: false,
        };
        let eval = packet.evaluate();
        assert!(eval.is_reject());
        assert_eq!(eval.failed_slot_names(), vec!["replay".to_string()]);
    }

    #[test]
    fn kind_mismatch_fails_closed() {
        let mut packet = NineConditionUpliftPacket::diagnostic_fixture();
        packet.exhaustion = ConditionWitness::ReplayReceipt {
            content_hash: "digest:wrong-kind".into(),
            replay_ok: true,
        };
        let eval = packet.evaluate();
        assert!(eval.is_reject());
        assert_eq!(eval.failed_slot_names(), vec!["exhaustion".to_string()]);
        match eval {
            UpliftEvaluation::RejectUntilPatched { failed_slots, .. } => {
                assert!(failed_slots[0].reason.contains("kind mismatch"));
            }
            _ => unreachable!(),
        }
    }

    #[test]
    fn boolean_only_legacy_path_must_not_auto_accept() {
        let legacy = LegacyNineBooleans::all_true();
        assert!(
            legacy.all_satisfied_as_bools(),
            "legacy checklist claims all true"
        );
        let packet = legacy.into_witnessed_packet();
        let eval = packet.evaluate();
        assert!(
            eval.is_reject(),
            "boolean-only legacy path must not auto-accept: {eval:?}"
        );
        assert_eq!(eval.failed_slot_names().len(), 9);
        assert_eq!(eval.authority_effect(), AuthorityEffect::None);

        for slot in packet.slots() {
            match slot.witness {
                ConditionWitness::Missing { residual } => {
                    assert!(
                        residual.contains("does not constitute a witness")
                            || residual.contains("=false"),
                        "unexpected residual: {residual}"
                    );
                }
                other => panic!("legacy path must yield Missing, got {other:?}"),
            }
        }
    }

    #[test]
    fn empty_payload_fields_fail() {
        let mut packet = NineConditionUpliftPacket::diagnostic_fixture();
        packet.refusal = ConditionWitness::PrimitiveDifference {
            left: "".into(),
            right: "r".into(),
            delta_id: "d".into(),
        };
        assert!(packet.evaluate().is_reject());

        packet = NineConditionUpliftPacket::diagnostic_fixture();
        packet.generator_minimality = ConditionWitness::MinimalityProof {
            candidate: "   ".into(),
            competitors_ruled_out: vec![],
        };
        assert!(packet.evaluate().is_reject());
    }

    #[test]
    fn accept_never_mints_authority() {
        let packet = NineConditionUpliftPacket::diagnostic_fixture();
        let eval = packet.evaluate();
        assert!(eval.is_accept());
        assert_eq!(eval.authority_effect(), AuthorityEffect::None);
        assert!(matches!(eval.authority_effect(), AuthorityEffect::None));
    }

    #[test]
    fn evaluation_matrix_reports_expected_kinds() {
        let packet = NineConditionUpliftPacket::diagnostic_fixture();
        let matrix = packet.evaluation_matrix();
        let expected = [
            (NineCondition::Exhaustion, WitnessKind::ExhaustionTrace),
            (NineCondition::Refusal, WitnessKind::PrimitiveDifference),
            (
                NineCondition::Traceability,
                WitnessKind::PrimitiveDifference,
            ),
            (
                NineCondition::Preservation,
                WitnessKind::ConservativeEmbedding,
            ),
            (
                NineCondition::Conservativity,
                WitnessKind::ConservativeEmbedding,
            ),
            (
                NineCondition::ObstructionResolution,
                WitnessKind::PrimitiveDifference,
            ),
            (
                NineCondition::GeneratorMinimality,
                WitnessKind::MinimalityProof,
            ),
            (NineCondition::Replay, WitnessKind::ReplayReceipt),
            (NineCondition::AuthorityFence, WitnessKind::ReplayReceipt),
        ];
        for (row, (cond, kind)) in matrix.iter().zip(expected.iter()) {
            assert_eq!(row.condition, *cond);
            assert_eq!(row.expected_kind, *kind);
            assert_eq!(row.actual_kind, Some(*kind));
            assert!(row.satisfied);
        }
    }
}
