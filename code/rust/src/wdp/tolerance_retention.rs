
use crate::error::WdpError;
use crate::retention::RetentionPacket;
use omega_category_theory::finite_retention_choices::{
    FiniteRetentionData, ForwardRelationReceipt,
};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ForwardRetentionAnalysis {
    pub state_names: Vec<String>,
    pub report_names: Vec<String>,
    pub receipt: ForwardRelationReceipt,
    native: FiniteRetentionData,
}

fn invalid(detail: &str) -> WdpError {
    WdpError::InvalidInput {
        detail: detail.to_owned(),
    }
}

impl ForwardRetentionAnalysis {
    pub fn from_packet(
        packet: &RetentionPacket,
        report_alphabet: &BTreeSet<String>,
    ) -> Result<Self, WdpError> {
        if packet.memory_carrier.is_empty()
            || packet.report_map.keys().cloned().collect::<BTreeSet<_>>() != packet.memory_carrier
        {
            return Err(invalid("exact nonempty memory/report coverage required"));
        }
        let state_names: Vec<_> = packet.memory_carrier.iter().cloned().collect();
        let labels: Vec<_> = packet.inputs.iter().cloned().collect();
        let report_names: Vec<_> = report_alphabet.iter().cloned().collect();
        let states: BTreeMap<_, _> = state_names
            .iter()
            .enumerate()
            .map(|(i, x)| (x.clone(), i))
            .collect();
        let reports: BTreeMap<_, _> = report_names
            .iter()
            .enumerate()
            .map(|(i, x)| (x.clone(), i))
            .collect();
        let mut updates = vec![vec![0; labels.len()]; state_names.len()];
        if packet.update_map.len() != state_names.len() * labels.len() {
            return Err(invalid("total update map with no extra entries required"));
        }
        for (x, state) in state_names.iter().enumerate() {
            for (i, label) in labels.iter().enumerate() {
                let target = packet
                    .update_map
                    .get(&(state.clone(), label.clone()))
                    .ok_or_else(|| invalid("missing declared update"))?;
                updates[x][i] = *states
                    .get(target)
                    .ok_or_else(|| invalid("update outside memory"))?;
            }
        }
        let report_values = state_names
            .iter()
            .map(|state| {
                reports
                    .get(&packet.report_map[state])
                    .copied()
                    .ok_or_else(|| invalid("readout outside declared report alphabet"))
            })
            .collect::<Result<Vec<_>, _>>()?;
        if packet
            .comparison
            .iter()
            .any(|(a, b)| !reports.contains_key(a) || !reports.contains_key(b))
        {
            return Err(invalid("comparison outside declared report alphabet"));
        }
        let comparison = report_names
            .iter()
            .map(|a| {
                report_names
                    .iter()
                    .map(|b| packet.comparison.contains(&(a.clone(), b.clone())))
                    .collect()
            })
            .collect();
        let native = FiniteRetentionData::new(updates, report_values, comparison, labels.len())
            .map_err(|_| invalid("invalid total retention packet"))?;
        let receipt = native.greatest_forward_relation();
        Ok(Self {
            state_names,
            report_names,
            receipt,
            native,
        })
    }
    pub fn native(&self) -> &FiniteRetentionData {
        &self.native
    }
    pub fn state_quotient_admissible(&self) -> bool {
        self.native.relation_is_equivalence(&self.receipt)
    }
    pub fn literal_report_quotient_admissible(&self) -> bool {
        self.native.raw_report_quotient_admissible(&self.receipt)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn actual_tolerance_packet_refuses_false_equivalence() {
        let names = ["a", "b", "c"].map(str::to_owned);
        let packet = RetentionPacket::new(
            names.clone().into_iter().collect(),
            ["keep".to_owned()].into_iter().collect(),
            names
                .iter()
                .map(|a| ((a.clone(), "keep".to_owned()), a.clone()))
                .collect(),
            names.iter().map(|a| (a.clone(), a.clone())).collect(),
            [
                ("a", "a"),
                ("b", "b"),
                ("c", "c"),
                ("a", "b"),
                ("b", "a"),
                ("b", "c"),
                ("c", "b"),
            ]
            .map(|(a, b)| (a.to_owned(), b.to_owned()))
            .into_iter()
            .collect(),
        )
        .unwrap();
        let analysis =
            ForwardRetentionAnalysis::from_packet(&packet, &names.into_iter().collect()).unwrap();
        assert!(analysis.native().is_reflexive_symmetric_comparison());
        assert!(!analysis.state_quotient_admissible());
        assert!(!analysis.literal_report_quotient_admissible());
    }
}
