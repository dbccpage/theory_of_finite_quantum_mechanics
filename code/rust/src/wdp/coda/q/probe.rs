use engine_types::q_continuum::{generate_probe_plan, ProbePlan, QIdea};

use super::packet::ValidatedQPacket;

pub fn probe_plan_for_packet(packet: &ValidatedQPacket) -> ProbePlan {
    let packet = packet.packet();
    let body = format!(
        "carrier: {}; composition: {}; observer: {}; predictions: {}",
        packet.carrier.as_deref().unwrap_or_default(),
        packet.composition.as_deref().unwrap_or_default(),
        packet.observer.as_deref().unwrap_or_default(),
        packet.finite_predictions.join("; ")
    );
    let idea = QIdea::new(
        format!("q-packet:{}", packet.id),
        body,
        "crate::coda::q::probe_plan_for_packet",
    )
    .with_tag("omega_q")
    .with_tag("packet");

    generate_probe_plan(&idea)
}
