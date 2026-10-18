
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RelationalError {
    EmptyCarrier,
    TransitionShape,
    TransitionOutsideCarrier,
    DuplicateSuccessor,
    InvalidPartition,
    InvalidBoundedMap,
    RelationOutsideCarrier,
    StateOutsideCarrier,
}

impl std::fmt::Display for RelationalError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for RelationalError {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinitePreorder {
    relation: Vec<Vec<bool>>,
}

fn close_transitively(relation: &mut [Vec<bool>]) {
    let n = relation.len();
    for via in 0..n {
        for x in 0..n {
            for y in 0..n {
                relation[x][y] |= relation[x][via] && relation[via][y];
            }
        }
    }
}

impl FinitePreorder {
    pub fn from_edges(size: usize, edges: &[(usize, usize)]) -> Result<Self, RelationalError> {
        if edges.iter().any(|&(x, y)| x >= size || y >= size) {
            return Err(RelationalError::RelationOutsideCarrier);
        }
        let mut relation = vec![vec![false; size]; size];
        for (i, row) in relation.iter_mut().enumerate() {
            row[i] = true;
        }
        for &(x, y) in edges {
            relation[x][y] = true;
        }
        close_transitively(&mut relation);
        Ok(Self { relation })
    }

    pub fn relation(&self) -> &[Vec<bool>] {
        &self.relation
    }

    pub fn leq(&self, x: usize, y: usize) -> Result<bool, RelationalError> {
        self.relation
            .get(x)
            .and_then(|row| row.get(y))
            .copied()
            .ok_or(RelationalError::StateOutsideCarrier)
    }

    pub fn is_partial_order(&self) -> bool {
        (0..self.relation.len())
            .all(|x| (0..x).all(|y| !(self.relation[x][y] && self.relation[y][x])))
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteRelational {
    reports: Vec<usize>,
    successors: Vec<Vec<Vec<usize>>>,
    label_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RelationalQuotient {
    pub partitions: Vec<Vec<usize>>,
    pub state_to_block: Vec<usize>,
    pub quotient: FiniteRelational,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SuccessionClassification {
    pub nonempty_reachability: Vec<Vec<bool>>,
    pub acyclic: bool,
    pub state_to_component: Vec<usize>,
    pub component_strict_order: Vec<Vec<bool>>,
}

fn normalize<T: Ord>(values: Vec<T>) -> Vec<usize> {
    let mut classes = BTreeMap::new();
    values
        .into_iter()
        .map(|value| {
            let fresh = classes.len();
            *classes.entry(value).or_insert(fresh)
        })
        .collect()
}

impl FiniteRelational {
    pub fn new(
        reports: Vec<usize>,
        mut successors: Vec<Vec<Vec<usize>>>,
        label_count: usize,
    ) -> Result<Self, RelationalError> {
        let n = reports.len();
        if n == 0 {
            return Err(RelationalError::EmptyCarrier);
        }
        if successors.len() != n || successors.iter().any(|row| row.len() != label_count) {
            return Err(RelationalError::TransitionShape);
        }
        for next in successors.iter_mut().flatten() {
            if next.iter().any(|&state| state >= n) {
                return Err(RelationalError::TransitionOutsideCarrier);
            }
            next.sort_unstable();
            if next.windows(2).any(|pair| pair[0] == pair[1]) {
                return Err(RelationalError::DuplicateSuccessor);
            }
        }
        Ok(Self {
            reports,
            successors,
            label_count,
        })
    }

    pub fn reports(&self) -> &[usize] {
        &self.reports
    }
    pub fn successors(&self) -> &[Vec<Vec<usize>>] {
        &self.successors
    }
    pub fn label_count(&self) -> usize {
        self.label_count
    }
    pub fn state_count(&self) -> usize {
        self.reports.len()
    }

    fn block_successors(&self, state: usize, label: usize, partition: &[usize]) -> BTreeSet<usize> {
        self.successors[state][label]
            .iter()
            .map(|&next| partition[next])
            .collect()
    }

    fn refine(&self, partition: &[usize]) -> Vec<usize> {
        normalize(
            (0..self.state_count())
                .map(|state| {
                    (
                        partition[state],
                        (0..self.label_count)
                            .map(|label| self.block_successors(state, label, partition))
                            .collect::<Vec<_>>(),
                    )
                })
                .collect(),
        )
    }

    pub fn is_report_bisimulation_partition(&self, partition: &[usize]) -> bool {
        if partition.len() != self.state_count() {
            return false;
        }
        for x in 0..self.state_count() {
            for y in 0..self.state_count() {
                if partition[x] == partition[y] {
                    if self.reports[x] != self.reports[y] {
                        return false;
                    }
                    for label in 0..self.label_count {
                        if self.block_successors(x, label, partition)
                            != self.block_successors(y, label, partition)
                        {
                            return false;
                        }
                    }
                }
            }
        }
        true
    }

    pub fn bisimulation_quotient(&self) -> RelationalQuotient {
        let mut partition = normalize(self.reports.clone());
        let mut partitions = vec![partition.clone()];
        loop {
            let next = self.refine(&partition);
            if next == partition {
                break;
            }
            partition = next;
            partitions.push(partition.clone());
        }
        let blocks = 1 + partition.iter().copied().max().unwrap();
        let mut representatives = vec![0; blocks];
        for state in (0..self.state_count()).rev() {
            representatives[partition[state]] = state;
        }
        let reports = representatives
            .iter()
            .map(|&state| self.reports[state])
            .collect();
        let successors = representatives
            .iter()
            .map(|&state| {
                (0..self.label_count)
                    .map(|label| {
                        self.block_successors(state, label, &partition)
                            .into_iter()
                            .collect()
                    })
                    .collect()
            })
            .collect();
        let quotient = FiniteRelational::new(reports, successors, self.label_count)
            .expect("refinement constructs a nonempty well-typed quotient");
        RelationalQuotient {
            partitions,
            state_to_block: partition,
            quotient,
        }
    }

    pub fn verify_quotient(&self, receipt: &RelationalQuotient) -> bool {
        &self.bisimulation_quotient() == receipt
    }

    pub fn same_behavior_set(&self, other: &Self) -> bool {
        if self.label_count != other.label_count {
            return false;
        }
        let offset = self.state_count();
        let mut reports = self.reports.clone();
        reports.extend_from_slice(&other.reports);
        let mut successors = self.successors.clone();
        successors.extend(other.successors.iter().map(|row| {
            row.iter()
                .map(|next| next.iter().map(|state| state + offset).collect())
                .collect()
        }));
        let combined = Self::new(reports, successors, self.label_count)
            .expect("disjoint union of validated finite relational systems");
        let classes = combined.bisimulation_quotient().state_to_block;
        classes[..offset].iter().copied().collect::<BTreeSet<_>>()
            == classes[offset..].iter().copied().collect::<BTreeSet<_>>()
    }

    pub fn factor_through_bounded_quotient(
        &self,
        target: &Self,
        map: &[usize],
    ) -> Result<Vec<usize>, RelationalError> {
        if map.len() != self.state_count()
            || target.label_count != self.label_count
            || map.iter().any(|&state| state >= target.state_count())
            || map.iter().copied().collect::<BTreeSet<_>>().len() != target.state_count()
        {
            return Err(RelationalError::InvalidBoundedMap);
        }
        for state in 0..self.state_count() {
            if self.reports[state] != target.reports[map[state]] {
                return Err(RelationalError::InvalidBoundedMap);
            }
            for label in 0..self.label_count {
                let image: BTreeSet<_> = self.successors[state][label]
                    .iter()
                    .map(|&next| map[next])
                    .collect();
                let expected: BTreeSet<_> = target.successors[map[state]][label]
                    .iter()
                    .copied()
                    .collect();
                if image != expected {
                    return Err(RelationalError::InvalidBoundedMap);
                }
            }
        }
        let stable = self.bisimulation_quotient().state_to_block;
        let mut factor = vec![None; target.state_count()];
        for state in 0..self.state_count() {
            match factor[map[state]] {
                Some(block) if block != stable[state] => {
                    return Err(RelationalError::InvalidBoundedMap)
                }
                _ => factor[map[state]] = Some(stable[state]),
            }
        }
        Ok(factor
            .into_iter()
            .map(|block| block.expect("surjective map"))
            .collect())
    }

    pub fn succession_classification(&self) -> SuccessionClassification {
        let n = self.state_count();
        let mut reach = vec![vec![false; n]; n];
        for (state, row) in self.successors.iter().enumerate() {
            for &next in row.iter().flatten() {
                reach[state][next] = true;
            }
        }
        close_transitively(&mut reach);
        let acyclic = (0..n).all(|state| !reach[state][state]);
        let mut component = vec![usize::MAX; n];
        let mut representatives = Vec::new();
        for x in 0..n {
            if component[x] != usize::MAX {
                continue;
            }
            let block = representatives.len();
            representatives.push(x);
            for y in x..n {
                if x == y || (reach[x][y] && reach[y][x]) {
                    component[y] = block;
                }
            }
        }
        let order = representatives
            .iter()
            .enumerate()
            .map(|(i, &x)| {
                representatives
                    .iter()
                    .enumerate()
                    .map(|(j, &y)| i != j && reach[x][y])
                    .collect()
            })
            .collect();
        SuccessionClassification {
            nonempty_reachability: reach,
            acyclic,
            state_to_component: component,
            component_strict_order: order,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn branching_deadlock_and_replay_boundaries() {
        let machine = FiniteRelational::new(
            vec![0, 0, 1],
            vec![vec![vec![1, 2]], vec![vec![2]], vec![vec![]]],
            1,
        )
        .unwrap();
        let quotient = machine.bisimulation_quotient();
        assert_eq!(quotient.state_to_block, vec![0, 1, 2]);
        assert!(machine.verify_quotient(&quotient));
        let mut forged = quotient.clone();
        forged.partitions.clear();
        assert!(!machine.verify_quotient(&forged));
        let blind =
            FiniteRelational::new(vec![0, 0], vec![vec![vec![]], vec![vec![1]]], 1).unwrap();
        assert_eq!(blind.bisimulation_quotient().state_to_block, vec![0, 1]);
        assert!(FiniteRelational::new(vec![0], vec![vec![vec![0, 0]]], 1).is_err());
    }

    #[test]
    fn bounded_maps_require_back_condition() {
        let source =
            FiniteRelational::new(vec![0, 0], vec![vec![vec![]], vec![vec![1]]], 1).unwrap();
        let target = FiniteRelational::new(vec![0], vec![vec![vec![0]]], 1).unwrap();
        assert!(source
            .factor_through_bounded_quotient(&target, &[0, 0])
            .is_err());
        let q = source.bisimulation_quotient();
        let factor = source
            .factor_through_bounded_quotient(&q.quotient, &q.state_to_block)
            .unwrap();
        assert_eq!(factor, vec![0, 1]);
    }

    #[test]
    fn fork_cycle_and_condensation() {
        let fork = FiniteRelational::new(
            vec![0; 3],
            vec![vec![vec![1, 2]], vec![vec![]], vec![vec![]]],
            1,
        )
        .unwrap();
        let s = fork.succession_classification();
        assert!(s.acyclic);
        assert!(!s.nonempty_reachability[1][2]);
        assert!(!s.nonempty_reachability[2][1]);
        let cycle = FiniteRelational::new(
            vec![0; 3],
            vec![vec![vec![1]], vec![vec![0, 2]], vec![vec![]]],
            1,
        )
        .unwrap();
        let s = cycle.succession_classification();
        assert!(!s.acyclic);
        assert_eq!(s.state_to_component, vec![0, 0, 1]);
        assert_eq!(
            s.component_strict_order,
            vec![vec![false, true], vec![false, false]]
        );
    }

    #[test]
    fn relabelling_changes_identifiers_but_not_classification() {
        let source = FiniteRelational::new(
            vec![0, 1, 1],
            vec![vec![vec![1, 2]], vec![vec![]], vec![vec![]]],
            1,
        )
        .unwrap();
        let renamed = FiniteRelational::new(
            vec![1, 0, 1],
            vec![vec![vec![]], vec![vec![0, 2]], vec![vec![]]],
            1,
        )
        .unwrap();
        assert!(source.same_behavior_set(&renamed));
        assert!(source.same_behavior_set(&source.bisimulation_quotient().quotient));
        let different = FiniteRelational::new(vec![0], vec![vec![vec![]]], 1).unwrap();
        assert!(!source.same_behavior_set(&different));
    }

    #[test]
    fn exhaustive_three_state_relations_greatest_bisimulation() {
        let partitions = [
            vec![0, 0, 0],
            vec![0, 0, 1],
            vec![0, 1, 0],
            vec![0, 1, 1],
            vec![0, 1, 2],
        ];
        for reports in 0..8 {
            for edges in 0..512 {
                let machine = FiniteRelational::new(
                    (0..3).map(|x| (reports >> x) & 1).collect(),
                    (0..3)
                        .map(|x| vec![(0..3).filter(|y| edges & (1 << (3 * x + y)) != 0).collect()])
                        .collect(),
                    1,
                )
                .unwrap();
                let q = machine.bisimulation_quotient();
                assert!(q.partitions.len() <= 3);
                assert!(machine.is_report_bisimulation_partition(&q.state_to_block));
                assert!(machine.verify_quotient(&q));
                for candidate in &partitions {
                    if machine.is_report_bisimulation_partition(candidate) {
                        for x in 0..3 {
                            for y in 0..3 {
                                if candidate[x] == candidate[y] {
                                    assert_eq!(q.state_to_block[x], q.state_to_block[y]);
                                }
                            }
                        }
                    }
                }
                let succession = machine.succession_classification();
                assert_eq!(
                    succession.acyclic,
                    q.quotient.succession_classification().acyclic
                );
                let order = &succession.component_strict_order;
                for x in 0..order.len() {
                    assert!(!order[x][x]);
                    for y in 0..order.len() {
                        for z in 0..order.len() {
                            if order[x][y] && order[y][z] {
                                assert!(order[x][z]);
                            }
                        }
                    }
                }
            }
        }
    }
}
