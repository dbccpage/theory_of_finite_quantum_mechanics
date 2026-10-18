
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashMap, HashSet};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MoveNode {
    pub state_id: String,
    pub phi1: i64,
    pub gamma2: i64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MoveEdge {
    pub from_state: String,
    pub to_state: String,
    pub action_rune: String,
    pub token_cost: u64,
    pub delta_phi1: i64,
    pub delta_gamma2: i64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FutileCycle {
    pub cycle_path: Vec<String>,
    pub actions: Vec<String>,
    pub total_token_cost: u64,
    pub net_delta_phi1: i64,
    pub net_delta_gamma2: i64,
    pub traversal_count: usize,
    pub is_futile: bool,
}

#[derive(Debug, Default, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MoveNetwork {
    pub nodes: BTreeMap<String, MoveNode>,
    pub edges: Vec<MoveEdge>,
}

impl MoveNetwork {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn add_node(&mut self, state_id: &str, phi1: i64, gamma2: i64) {
        self.nodes.insert(
            state_id.to_string(),
            MoveNode {
                state_id: state_id.to_string(),
                phi1,
                gamma2,
            },
        );
    }

    #[allow(clippy::too_many_arguments)]
    pub fn add_transition(
        &mut self,
        from_state: &str,
        to_state: &str,
        action_rune: &str,
        token_cost: u64,
        from_phi1: i64,
        to_phi1: i64,
        from_gamma2: i64,
        to_gamma2: i64,
    ) {
        self.add_node(from_state, from_phi1, from_gamma2);
        self.add_node(to_state, to_phi1, to_gamma2);

        self.edges.push(MoveEdge {
            from_state: from_state.to_string(),
            to_state: to_state.to_string(),
            action_rune: action_rune.to_string(),
            token_cost,
            delta_phi1: to_phi1 - from_phi1,
            delta_gamma2: to_gamma2 - from_gamma2,
        });
    }

    pub fn detect_futile_cycles(&self) -> Vec<FutileCycle> {
        let mut adj: HashMap<&str, Vec<&MoveEdge>> = HashMap::new();
        for edge in &self.edges {
            adj.entry(edge.from_state.as_str()).or_default().push(edge);
        }

        let mut futile_cycles = Vec::new();
        let mut seen_cycles: HashSet<Vec<String>> = HashSet::new();

        for start_node in self.nodes.keys() {
            let mut path: Vec<(&str, &MoveEdge)> = Vec::new();
            let mut in_path: HashSet<&str> = HashSet::new();
            self.dfs_find_cycles(
                start_node.as_str(),
                start_node.as_str(),
                &adj,
                &mut path,
                &mut in_path,
                &mut seen_cycles,
                &mut futile_cycles,
            );
        }

        futile_cycles
    }

    #[allow(clippy::too_many_arguments)]
    fn dfs_find_cycles<'a>(
        &'a self,
        current: &'a str,
        target: &'a str,
        adj: &HashMap<&'a str, Vec<&'a MoveEdge>>,
        path: &mut Vec<(&'a str, &'a MoveEdge)>,
        in_path: &mut HashSet<&'a str>,
        seen_cycles: &mut HashSet<Vec<String>>,
        results: &mut Vec<FutileCycle>,
    ) {
        if path.len() > 8 {
            return;
        }

        if let Some(edges) = adj.get(current) {
            for &edge in edges {
                let next = edge.to_state.as_str();
                if next == target && !path.is_empty() {
                    let mut cycle_nodes = vec![target.to_string()];
                    let mut actions = Vec::new();
                    let mut total_tokens = 0;
                    let mut net_phi1 = 0;
                    let mut net_gamma2 = 0;

                    for &(step_node, step_edge) in path.iter() {
                        cycle_nodes.push(step_node.to_string());
                        actions.push(step_edge.action_rune.clone());
                        total_tokens += step_edge.token_cost;
                        net_phi1 += step_edge.delta_phi1;
                        net_gamma2 += step_edge.delta_gamma2;
                    }
                    actions.push(edge.action_rune.clone());
                    total_tokens += edge.token_cost;
                    net_phi1 += edge.delta_phi1;
                    net_gamma2 += edge.delta_gamma2;

                    let min_idx = cycle_nodes
                        .iter()
                        .enumerate()
                        .min_by_key(|(_, s)| *s)
                        .map(|(i, _)| i)
                        .unwrap_or(0);
                    let mut canonical = cycle_nodes[min_idx..].to_vec();
                    canonical.extend_from_slice(&cycle_nodes[..min_idx]);

                    if seen_cycles.insert(canonical) {
                        let is_futile = net_phi1 == 0 && net_gamma2 == 0 && total_tokens > 0;
                        if is_futile {
                            results.push(FutileCycle {
                                cycle_path: cycle_nodes,
                                actions,
                                total_token_cost: total_tokens,
                                net_delta_phi1: net_phi1,
                                net_delta_gamma2: net_gamma2,
                                traversal_count: 1,
                                is_futile: true,
                            });
                        }
                    }
                } else if !in_path.contains(next) && next != target {
                    in_path.insert(next);
                    path.push((next, edge));
                    self.dfs_find_cycles(
                        next,
                        target,
                        adj,
                        path,
                        in_path,
                        seen_cycles,
                        results,
                    );
                    path.pop();
                    in_path.remove(next);
                }
            }
        }
    }

    pub fn count_cycle_traversals(
        &self,
        trajectory: &[&str],
        cycle: &[&str],
    ) -> usize {
        if cycle.len() < 2 || trajectory.len() < cycle.len() {
            return 0;
        }

        let m = cycle.len() - 1;
        let mut count = 0;
        let mut i = 0;

        while i + m <= trajectory.len() {
            let mut matches = true;
            for j in 0..=m {
                if trajectory[i + j] != cycle[j % cycle.len()] {
                    matches = false;
                    break;
                }
            }
            if matches {
                count += 1;
                i += m;
            } else {
                i += 1;
            }
        }

        count
    }
}
