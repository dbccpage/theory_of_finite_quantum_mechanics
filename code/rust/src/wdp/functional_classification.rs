//! Named WDP adapters for sovereign finite component classifications.
//!
//! CH03 uses the existing property-vector meanings, adding active updates.
//! CH14 distinguishes manuscript report stability from the legacy presentation
//! stability flag. Missing context/target data are refused, not defaulted.
//! Exact calibration means equality to caller-declared targets, not physical truth.

use std::collections::{BTreeMap, BTreeSet};

use omega_category_theory::finite_functional_classification::{
    realize_retention, FiniteFunctionalModel, FiniteRetentionModel, FunctionalSignature,
    RetentionSignature,
};

use crate::error::WdpError;
use crate::observer::{audit_functional_observer_relations, FunctionalObserverProfile};
use crate::retention::{analyze_retention_packet, RetentionPacket};
use crate::types::AuthorityEffect;

fn invalid(detail: &str) -> WdpError {
    WdpError::InvalidInput {
        detail: detail.to_owned(),
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RetentionClassification {
    pub signature: RetentionSignature,
    pub quotient_size: usize,
    pub authority_effect: AuthorityEffect,
}

/// Validate the legacy packet and comparison, then delegate finite mathematics.
pub fn classify_retention_packet(
    packet: &RetentionPacket,
) -> Result<RetentionClassification, WdpError> {
    let legacy = analyze_retention_packet(packet)?;
    let report_labels: Vec<_> = packet
        .report_map
        .values()
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    let raw_ids: BTreeMap<_, _> = report_labels
        .iter()
        .enumerate()
        .map(|(i, label)| (label.clone(), i))
        .collect();
    let states: Vec<_> = packet.memory_carrier.iter().cloned().collect();
    let state_ids: BTreeMap<_, _> = states
        .iter()
        .enumerate()
        .map(|(i, state)| (state.clone(), i))
        .collect();
    let mut comparison_ids = BTreeMap::new();
    let mut recognized_by_label = BTreeMap::new();
    for label in &report_labels {
        let row: Vec<_> = report_labels
            .iter()
            .map(|other| packet.are_equivalent(label, other))
            .collect();
        let fresh = comparison_ids.len();
        let id = *comparison_ids.entry(row).or_insert(fresh);
        recognized_by_label.insert(label.clone(), id);
    }
    let raw = states
        .iter()
        .map(|state| raw_ids[&packet.report_map[state]])
        .collect();
    let recognized = states
        .iter()
        .map(|state| recognized_by_label[&packet.report_map[state]])
        .collect();
    let transitions = states
        .iter()
        .map(|state| {
            packet
                .inputs
                .iter()
                .map(|input| state_ids[&packet.update_map[&(state.clone(), input.clone())]])
                .collect()
        })
        .collect();
    let model = FiniteRetentionModel::new(raw, recognized, transitions, packet.inputs.len())
        .map_err(|_| invalid("invalid finite retention classification model"))?;
    let signature = model.signature();
    if signature.nontrivial != legacy.is_nontrivial_carrier
        || signature.reversible != legacy.is_fully_reversible
        || signature.observable != legacy.is_observable
        || signature.tolerance != legacy.has_nontrivial_tolerance
        || signature.minimal != legacy.is_minimal
    {
        return Err(invalid(
            "legacy and sovereign retention invariants disagree",
        ));
    }
    Ok(RetentionClassification {
        signature,
        quotient_size: legacy.quotient_size,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn construct_retention_witness(
    signature: RetentionSignature,
) -> Result<RetentionPacket, WdpError> {
    let model =
        realize_retention(signature).map_err(|_| invalid("impossible retention signature"))?;
    let n = model.moore().state_count();
    let states: Vec<_> = (0..n).map(|i| format!("m{i}")).collect();
    let inputs: Vec<_> = (0..model.moore().input_count())
        .map(|i| format!("i{i}"))
        .collect();
    let update = states
        .iter()
        .enumerate()
        .flat_map(|(x, state)| {
            inputs
                .iter()
                .enumerate()
                .map(|(i, input)| {
                    (
                        (state.clone(), input.clone()),
                        states[model.moore().transitions()[x][i]].clone(),
                    )
                })
                .collect::<Vec<_>>()
        })
        .collect();
    let report = states
        .iter()
        .enumerate()
        .map(|(x, state)| (state.clone(), format!("r{}", model.raw_reports()[x])))
        .collect();
    let mut comparison = BTreeSet::new();
    for x in 0..n {
        for y in 0..n {
            if model.moore().reports()[x] == model.moore().reports()[y] {
                comparison.insert((
                    format!("r{}", model.raw_reports()[x]),
                    format!("r{}", model.raw_reports()[y]),
                ));
            }
        }
    }
    RetentionPacket::new(
        states.into_iter().collect(),
        inputs.into_iter().collect(),
        update,
        report,
        comparison,
    )
}

/// All maps must be total on exactly the nonempty, duplicate-free named carrier.
pub fn classify_functional_maps(
    carrier: &[String],
    presentation: &BTreeMap<String, String>,
    self_report: &BTreeMap<String, String>,
    context: &BTreeMap<String, String>,
    target: &BTreeMap<String, String>,
) -> Result<FunctionalSignature, WdpError> {
    let domain: BTreeSet<_> = carrier.iter().cloned().collect();
    if domain.is_empty()
        || domain.len() != carrier.len()
        || [presentation, self_report, context, target]
            .iter()
            .any(|map| map.keys().cloned().collect::<BTreeSet<_>>() != domain)
    {
        return Err(invalid(
            "functional maps must have exactly the declared nonempty carrier domain",
        ));
    }
    let ids: BTreeMap<_, _> = carrier
        .iter()
        .enumerate()
        .map(|(i, x)| (x.clone(), i))
        .collect();
    if context.values().any(|value| !domain.contains(value)) {
        return Err(invalid("context leaves the declared carrier"));
    }
    let pids: BTreeMap<_, _> = presentation
        .values()
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .enumerate()
        .map(|(i, x)| (x, i))
        .collect();
    let rids: BTreeMap<_, _> = self_report
        .values()
        .chain(target.values())
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .enumerate()
        .map(|(i, x)| (x, i))
        .collect();
    let model = FiniteFunctionalModel::new(
        carrier.iter().map(|x| pids[&presentation[x]]).collect(),
        carrier.iter().map(|x| rids[&self_report[x]]).collect(),
        carrier.iter().map(|x| ids[&context[x]]).collect(),
        carrier.iter().map(|x| rids[&target[x]]).collect(),
    )
    .map_err(|_| invalid("invalid finite functional model"))?;
    Ok(model.signature())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FunctionalClassification {
    pub signature: FunctionalSignature,
    pub legacy_audit: FunctionalObserverProfile,
    pub authority_effect: AuthorityEffect,
}

/// Checked adapter to the legacy report-on-presentations API. Here linking is
/// structural (s=hq), not an independent predicate. Supply complete context and
/// targets; the legacy missing-data defaults are deliberately unavailable.
pub fn classify_existing_functional_packet(
    carrier: &[String],
    presentation: &BTreeMap<String, String>,
    report_on_presentations: &BTreeMap<String, String>,
    context: &BTreeMap<String, String>,
    target: &BTreeMap<String, String>,
) -> Result<FunctionalClassification, WdpError> {
    let realized: BTreeSet<_> = presentation.values().cloned().collect();
    if report_on_presentations
        .keys()
        .cloned()
        .collect::<BTreeSet<_>>()
        != realized
    {
        return Err(invalid(
            "report map must be total exactly on realized presentations",
        ));
    }
    let self_report = presentation
        .iter()
        .map(|(x, q)| (x.clone(), report_on_presentations[q].clone()))
        .collect();
    let signature = classify_functional_maps(carrier, presentation, &self_report, context, target)?;
    let legacy_audit = audit_functional_observer_relations(
        carrier,
        presentation,
        report_on_presentations,
        Some(context),
        Some(target),
    )?;
    Ok(FunctionalClassification {
        signature,
        legacy_audit,
        authority_effect: AuthorityEffect::None,
    })
}
