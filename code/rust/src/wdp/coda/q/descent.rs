use engine_types::q_continuum::{
    holonomy_ladder_descent_ledger, AuthorityScope, DescentGate, DescentObligation, DescentResult,
    FiniteProjection, LeanWitness, QContinuumLedger,
};

use super::packet::ValidatedQPacket;

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct QDescentGate {
    inner: DescentGate,
}

impl QDescentGate {
    pub fn new() -> Self {
        Self {
            inner: DescentGate::new(),
        }
    }

    pub fn project_packet(&self, packet: &ValidatedQPacket) -> FiniteProjection {
        let packet = packet.packet();
        FiniteProjection {
            id: format!("{}:projection:q", packet.id),
            source_id: packet.id.clone(),
            carrier: packet.carrier.clone().unwrap_or_default(),
            zero_relation: "same finite shadow under declared observer and transport".to_string(),
            scope: AuthorityScope::new(format!("q-packet:{}", packet.id)),
            finite_description: format!(
                "composition: {}; observer: {}; finite_predictions: {}",
                packet.composition.as_deref().unwrap_or_default(),
                packet.observer.as_deref().unwrap_or_default(),
                packet.finite_predictions.join("; ")
            ),
        }
    }

    pub fn obligations_for_packet(&self, packet: &ValidatedQPacket) -> Vec<DescentObligation> {
        let projection = self.project_packet(packet);
        self.inner.obligations_for_projection(&projection)
    }

    pub fn verify_lean_witness(
        &self,
        obligation_id: impl Into<String>,
        scope: AuthorityScope,
        witness: &LeanWitness,
    ) -> DescentResult {
        self.inner
            .verify_lean_witness(obligation_id, scope, witness)
    }

    pub fn accept_results(
        &self,
        ledger: &mut QContinuumLedger,
        about: impl Into<String>,
        results: Vec<DescentResult>,
    ) {
        self.inner.accept_results(ledger, about, results);
    }

    pub fn holonomy_ladder_ledger() -> QContinuumLedger {
        holonomy_ladder_descent_ledger()
    }
}
