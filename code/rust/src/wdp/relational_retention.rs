
use crate::error::WdpError;
use tfqm_category_theory::finite_relational::{
    FiniteRelational, RelationalQuotient, SuccessionClassification,
};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RelationalRetentionPacket {
    pub state_names: Vec<String>,
    pub labels: Vec<String>,
    native: FiniteRelational,
}

fn invalid(detail: &str) -> WdpError {
    WdpError::InvalidInput {
        detail: detail.to_owned(),
    }
}

impl RelationalRetentionPacket {
    pub fn new(
        memory: BTreeSet<String>,
        labels: BTreeSet<String>,
        updates: BTreeSet<(String, String, String)>,
        reports: BTreeMap<String, String>,
        comparison: Option<BTreeSet<(String, String)>>,
    ) -> Result<Self, WdpError> {
        if memory.is_empty() || reports.keys().cloned().collect::<BTreeSet<_>>() != memory {
            return Err(invalid(
                "nonempty memory and exactly one report per memory state required",
            ));
        }
        let state_names: Vec<_> = memory.into_iter().collect();
        let labels: Vec<_> = labels.into_iter().collect();
        let states: BTreeMap<_, _> = state_names
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, s)| (s, i))
            .collect();
        let label_ids: BTreeMap<_, _> = labels
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, s)| (s, i))
            .collect();
        let report_names: Vec<_> = reports
            .values()
            .cloned()
            .collect::<BTreeSet<_>>()
            .into_iter()
            .collect();
        let comparison = comparison.unwrap_or_else(|| {
            report_names
                .iter()
                .map(|r| (r.clone(), r.clone()))
                .collect()
        });
        let report_set: BTreeSet<_> = report_names.iter().cloned().collect();
        if comparison
            .iter()
            .any(|(a, b)| !report_set.contains(a) || !report_set.contains(b))
        {
            return Err(invalid(
                "comparison references a report outside this packet",
            ));
        }
        for a in &report_names {
            if !comparison.contains(&(a.clone(), a.clone())) {
                return Err(invalid("report comparison is not reflexive"));
            }
            for b in &report_names {
                if comparison.contains(&(a.clone(), b.clone()))
                    != comparison.contains(&(b.clone(), a.clone()))
                {
                    return Err(invalid("report comparison is not symmetric"));
                }
                for c in &report_names {
                    if comparison.contains(&(a.clone(), b.clone()))
                        && comparison.contains(&(b.clone(), c.clone()))
                        && !comparison.contains(&(a.clone(), c.clone()))
                    {
                        return Err(invalid("report comparison is not transitive"));
                    }
                }
            }
        }
        let report_ids: BTreeMap<_, _> = report_names
            .iter()
            .map(|a| {
                let representative = report_names
                    .iter()
                    .position(|b| comparison.contains(&(a.clone(), b.clone())))
                    .expect("reflexive comparison");
                (a.clone(), representative)
            })
            .collect();
        let mut successors = vec![vec![Vec::new(); labels.len()]; state_names.len()];
        for (source, label, target) in updates {
            let (&source, &label, &target) = (
                states
                    .get(&source)
                    .ok_or_else(|| invalid("update source outside memory"))?,
                label_ids
                    .get(&label)
                    .ok_or_else(|| invalid("update label outside alphabet"))?,
                states
                    .get(&target)
                    .ok_or_else(|| invalid("update target outside memory"))?,
            );
            successors[source][label].push(target);
        }
        let report_values = state_names
            .iter()
            .map(|state| report_ids[&reports[state]])
            .collect();
        let native = FiniteRelational::new(report_values, successors, labels.len())
            .map_err(|_| invalid("invalid finite relational retention data"))?;
        Ok(Self {
            state_names,
            labels,
            native,
        })
    }

    pub fn native(&self) -> &FiniteRelational {
        &self.native
    }
    pub fn behavioral_quotient(&self) -> RelationalQuotient {
        self.native.bisimulation_quotient()
    }
    pub fn verify_quotient(&self, receipt: &RelationalQuotient) -> bool {
        self.native.verify_quotient(receipt)
    }
    pub fn succession_classification(&self) -> SuccessionClassification {
        self.native.succession_classification()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fork_has_partial_succession_and_branching_behavior() {
        let packet = RelationalRetentionPacket::new(
            ["a", "b", "c"].map(str::to_owned).into_iter().collect(),
            ["step"].map(str::to_owned).into_iter().collect(),
            [("a", "step", "b"), ("a", "step", "c")]
                .map(|(a, i, b)| (a.to_owned(), i.to_owned(), b.to_owned()))
                .into_iter()
                .collect(),
            [("a", "r"), ("b", "r"), ("c", "r")]
                .map(|(a, r)| (a.to_owned(), r.to_owned()))
                .into_iter()
                .collect(),
            None,
        )
        .unwrap();
        let q = packet.behavioral_quotient();
        assert_eq!(q.state_to_block, vec![0, 1, 1]);
        assert!(packet.verify_quotient(&q));
        let order = packet.succession_classification();
        assert!(order.acyclic);
        assert!(!order.nonempty_reachability[1][2]);
    }

    #[test]
    fn comparison_tolerance_is_not_silently_closed() {
        let names = ["a", "b", "c"].map(str::to_owned);
        let comparison = [
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
        .collect();
        let result = RelationalRetentionPacket::new(
            names.clone().into_iter().collect(),
            BTreeSet::new(),
            BTreeSet::new(),
            names.into_iter().map(|a| (a.clone(), a)).collect(),
            Some(comparison),
        );
        assert!(result.is_err());
    }
}
