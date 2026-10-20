
use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum GtorGttcLayer {
    GtorComparisonEnvelope,
    GttcContinuumShadow,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum GtorGttcGateStatus {
    AuthorityAccepted,
    DiscardedNonCreating,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GtorRepresentationEdge {
    pub tail: usize,
    pub head: usize,
    pub scope: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GtorGttcGateInputs {
    pub finite_component_count: usize,
    pub terminalized_component_count: usize,
    pub edge_certificate_count: usize,
    pub edges: Vec<GtorRepresentationEdge>,
    pub directed_gluing_present: bool,
    pub query_relative_authority_present: bool,
    pub uniform_certificate_family_present: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GtorGttcGateReport {
    pub layer: GtorGttcLayer,
    pub status: GtorGttcGateStatus,
    pub finite_component_count: usize,
    pub terminalized_component_count: usize,
    pub edge_certificate_count: usize,
    pub required_edge_certificate_count: usize,
    pub directed_gluing_present: bool,
    pub query_relative_authority_present: bool,
    pub uniform_certificate_family_present: bool,
    pub checked_structure: Vec<&'static str>,
    pub missing_obligations: Vec<&'static str>,
    pub rejected_escalations: Vec<&'static str>,
    pub boundary: &'static str,
    pub error: Option<String>,
}

pub fn verify_gtor_gttc_gates(inputs: GtorGttcGateInputs) -> Vec<GtorGttcGateReport> {
    vec![verify_gtor_gate(&inputs), verify_gttc_gate(&inputs)]
}

fn verify_gtor_gate(inputs: &GtorGttcGateInputs) -> GtorGttcGateReport {
    let required_edge_certificate_count = inputs.finite_component_count.saturating_sub(1);
    let mut missing = Vec::new();
    if inputs.terminalized_component_count < inputs.finite_component_count {
        missing.push("terminalized descent certificate for every comparison component");
    }
    if let Some(obligation) = representation_edge_obligation(inputs) {
        missing.push(obligation);
    }
    if !inputs.directed_gluing_present {
        missing.push("directed finite-shape gluing theorem for the comparison envelope");
    }
    if !inputs.query_relative_authority_present {
        missing.push("query-relative authority proof for the target MUB theorem");
    }

    build_report(
        GtorGttcLayer::GtorComparisonEnvelope,
        inputs,
        required_edge_certificate_count,
        missing,
        vec![
            "finite benchmark components can be listed in one comparison envelope",
            "component membership is bookkeeping only",
        ],
        vec![
            "comparison-envelope membership does not terminalize any component",
            "comparison-envelope membership does not certify representation edges",
            "comparison-envelope completion does not prove MUB(6), MUB(10), or MUB(n)",
        ],
        "CODA-OR comparison envelope is discarded as non-creating without terminalized descent and certified gluing",
    )
}

fn verify_gttc_gate(inputs: &GtorGttcGateInputs) -> GtorGttcGateReport {
    let required_edge_certificate_count = inputs.finite_component_count.saturating_sub(1);
    let mut missing = Vec::new();
    if inputs.terminalized_component_count < inputs.finite_component_count {
        missing.push("terminalized finite shadow for every declared dimension component");
    }
    if let Some(obligation) = representation_edge_obligation(inputs) {
        missing.push(obligation);
    }
    if !inputs.uniform_certificate_family_present {
        missing.push("uniform certificate family over the dimension-indexed shadow");
    }
    if !inputs.directed_gluing_present {
        missing.push("certified descent from the continuum shadow to finite MUB targets");
    }
    if !inputs.query_relative_authority_present {
        missing.push("query-relative authority proof for the all-N statement");
    }

    build_report(
        GtorGttcLayer::GttcContinuumShadow,
        inputs,
        required_edge_certificate_count,
        missing,
        vec![
            "dimension-indexed components can be embedded into a continuum shadow",
            "continuum membership is bookkeeping only",
        ],
        vec![
            "continuum shadow does not terminalize finite dimensions",
            "continuum shadow does not supply a uniform certificate family",
            "continuum shadow does not prove a general MUB(n) theorem",
        ],
        "CODA-CS continuum shadow is discarded as non-creating without finite-shadow terminalization and a certificate family",
    )
}

fn uf_find(parent: &mut [usize], mut node: usize) -> usize {
    while parent[node] != node {
        parent[node] = parent[parent[node]];
        node = parent[node];
    }
    node
}

fn edge_endpoints_valid(scope: &str, tail: usize, head: usize, count: usize) -> bool {
    !scope.is_empty() && tail < count && head < count && tail != head
}

fn all_components_connected(parent: &mut [usize], count: usize) -> bool {
    let root = uf_find(parent, 0);
    for start in 1..count {
        if uf_find(parent, start) != root {
            return false;
        }
    }
    true
}

fn representation_edge_obligation(inputs: &GtorGttcGateInputs) -> Option<&'static str> {
    if inputs.finite_component_count == 0 {
        return Some("declared component set is empty");
    }
    if inputs.edges.len() != inputs.edge_certificate_count {
        return Some("edge certificate count does not match the supplied edge records");
    }
    let required = inputs.finite_component_count.saturating_sub(1);
    if inputs.edge_certificate_count < required {
        return Some("certified representation edge for every comparison-gluing edge");
    }
    let mut parent: Vec<usize> = (0..inputs.finite_component_count).collect();
    for edge in &inputs.edges {
        if !edge_endpoints_valid(
            edge.scope,
            edge.tail,
            edge.head,
            inputs.finite_component_count,
        ) {
            return Some(
                "representation edge endpoints or scope are outside the declared components",
            );
        }
        let left = uf_find(&mut parent, edge.tail);
        let right = uf_find(&mut parent, edge.head);
        parent[right] = left;
    }
    if !all_components_connected(&mut parent, inputs.finite_component_count) {
        return Some("representation edges do not connect the declared components");
    }
    None
}

fn build_report(
    layer: GtorGttcLayer,
    inputs: &GtorGttcGateInputs,
    required_edge_certificate_count: usize,
    missing_obligations: Vec<&'static str>,
    checked_structure: Vec<&'static str>,
    rejected_escalations: Vec<&'static str>,
    discard_boundary: &'static str,
) -> GtorGttcGateReport {
    let status = if missing_obligations.is_empty() {
        GtorGttcGateStatus::AuthorityAccepted
    } else {
        GtorGttcGateStatus::DiscardedNonCreating
    };

    GtorGttcGateReport {
        layer,
        status,
        finite_component_count: inputs.finite_component_count,
        terminalized_component_count: inputs.terminalized_component_count,
        edge_certificate_count: inputs.edge_certificate_count,
        required_edge_certificate_count,
        directed_gluing_present: inputs.directed_gluing_present,
        query_relative_authority_present: inputs.query_relative_authority_present,
        uniform_certificate_family_present: inputs.uniform_certificate_family_present,
        checked_structure,
        missing_obligations,
        rejected_escalations,
        boundary: if status == GtorGttcGateStatus::AuthorityAccepted {
            "comparison/continuum gate accepted only because all terminalization and gluing obligations are present"
        } else {
            discard_boundary
        },
        error: if status == GtorGttcGateStatus::AuthorityAccepted {
            None
        } else {
            Some("non-creating abstraction gate lacks terminalized descent".to_string())
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn gtor_gttc_gates_reject_unterminalized_components() {
        let reports = verify_gtor_gttc_gates(GtorGttcGateInputs {
            finite_component_count: 6,
            terminalized_component_count: 4,
            edge_certificate_count: 0,
            edges: vec![],
            directed_gluing_present: false,
            query_relative_authority_present: false,
            uniform_certificate_family_present: false,
        });
        assert_eq!(reports.len(), 2);
        assert!(reports
            .iter()
            .all(|report| report.status == GtorGttcGateStatus::DiscardedNonCreating));
        assert!(reports.iter().any(|report| {
            report.layer == GtorGttcLayer::GtorComparisonEnvelope
                && report
                    .missing_obligations
                    .iter()
                    .any(|obligation| obligation.contains("edge"))
        }));
        assert!(reports.iter().any(|report| {
            report.layer == GtorGttcLayer::GttcContinuumShadow
                && report
                    .missing_obligations
                    .iter()
                    .any(|obligation| obligation.contains("uniform certificate"))
        }));
    }

    #[test]
    fn gtor_gttc_gates_accept_only_when_all_obligations_present() {
        let reports = verify_gtor_gttc_gates(GtorGttcGateInputs {
            finite_component_count: 3,
            terminalized_component_count: 3,
            edge_certificate_count: 2,
            edges: vec![
                GtorRepresentationEdge {
                    tail: 0,
                    head: 1,
                    scope: "component-0-to-1",
                },
                GtorRepresentationEdge {
                    tail: 1,
                    head: 2,
                    scope: "component-1-to-2",
                },
            ],
            directed_gluing_present: true,
            query_relative_authority_present: true,
            uniform_certificate_family_present: true,
        });
        assert!(reports
            .iter()
            .all(|report| report.status == GtorGttcGateStatus::AuthorityAccepted));
        assert!(reports
            .iter()
            .all(|report| report.missing_obligations.is_empty()));
    }

    #[test]
    fn continuum_gate_rejects_a_terminalized_triple_with_no_edges() {
        let reports = verify_gtor_gttc_gates(GtorGttcGateInputs {
            finite_component_count: 3,
            terminalized_component_count: 3,
            edge_certificate_count: 0,
            edges: vec![],
            directed_gluing_present: true,
            query_relative_authority_present: true,
            uniform_certificate_family_present: true,
        });
        assert!(reports
            .iter()
            .all(|report| report.status == GtorGttcGateStatus::DiscardedNonCreating));
        assert!(reports.iter().all(|report| {
            report
                .missing_obligations
                .iter()
                .any(|obligation| obligation.contains("edge"))
        }));
    }
}
