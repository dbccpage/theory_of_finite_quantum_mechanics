
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MooreError {
    EmptyCarrier,
    TransitionShape,
    TransitionOutsideCarrier,
    InvalidPartition,
    InvalidQuotientMap,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteMoore {
    reports: Vec<usize>,
    transitions: Vec<Vec<usize>>,
    input_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MooreQuotient {
    pub partitions: Vec<Vec<usize>>,
    pub state_to_block: Vec<usize>,
    pub quotient: FiniteMoore,
}

fn normalize<T: Ord>(signatures: Vec<T>) -> Vec<usize> {
    let mut ids = BTreeMap::new();
    signatures
        .into_iter()
        .map(|signature| {
            let fresh = ids.len();
            *ids.entry(signature).or_insert(fresh)
        })
        .collect()
}

impl FiniteMoore {
    pub fn new(
        reports: Vec<usize>,
        transitions: Vec<Vec<usize>>,
        input_count: usize,
    ) -> Result<Self, MooreError> {
        if reports.is_empty() {
            return Err(MooreError::EmptyCarrier);
        }
        if transitions.len() != reports.len()
            || transitions.iter().any(|row| row.len() != input_count)
        {
            return Err(MooreError::TransitionShape);
        }
        if transitions
            .iter()
            .flatten()
            .any(|&state| state >= reports.len())
        {
            return Err(MooreError::TransitionOutsideCarrier);
        }
        Ok(Self {
            reports,
            transitions,
            input_count,
        })
    }

    pub fn reports(&self) -> &[usize] {
        &self.reports
    }
    pub fn transitions(&self) -> &[Vec<usize>] {
        &self.transitions
    }
    pub fn input_count(&self) -> usize {
        self.input_count
    }
    pub fn state_count(&self) -> usize {
        self.reports.len()
    }

    fn initial_partition(&self) -> Vec<usize> {
        normalize(self.reports.clone())
    }

    fn refine(&self, partition: &[usize]) -> Vec<usize> {
        normalize(
            (0..self.state_count())
                .map(|state| {
                    let mut signature = vec![partition[state]];
                    signature.extend(self.transitions[state].iter().map(|&next| partition[next]));
                    signature
                })
                .collect(),
        )
    }

    pub fn is_report_congruence(&self, partition: &[usize]) -> bool {
        if partition.len() != self.state_count() {
            return false;
        }
        for s in 0..self.state_count() {
            for t in 0..s {
                if partition[s] == partition[t]
                    && (self.reports[s] != self.reports[t]
                        || (0..self.input_count).any(|i| {
                            partition[self.transitions[s][i]] != partition[self.transitions[t][i]]
                        }))
                {
                    return false;
                }
            }
        }
        true
    }

    pub fn behavioral_quotient(&self) -> MooreQuotient {
        let mut partitions = vec![self.initial_partition()];
        loop {
            let next = self.refine(partitions.last().unwrap());
            if next == *partitions.last().unwrap() {
                break;
            }
            partitions.push(next);
        }
        let state_to_block = partitions.last().unwrap().clone();
        let count = state_to_block.iter().copied().max().unwrap() + 1;
        let mut representatives = vec![None; count];
        for (state, &block) in state_to_block.iter().enumerate() {
            if representatives[block].is_none() {
                representatives[block] = Some(state);
            }
        }
        let representatives: Vec<_> = representatives.into_iter().map(Option::unwrap).collect();
        let quotient = Self::new(
            representatives.iter().map(|&s| self.reports[s]).collect(),
            representatives
                .iter()
                .map(|&s| {
                    self.transitions[s]
                        .iter()
                        .map(|&t| state_to_block[t])
                        .collect()
                })
                .collect(),
            self.input_count,
        )
        .expect("stable partition defines a total quotient");
        MooreQuotient {
            partitions,
            state_to_block,
            quotient,
        }
    }

    pub fn verify_quotient(&self, receipt: &MooreQuotient) -> bool {
        if receipt.partitions.first() != Some(&self.initial_partition()) {
            return false;
        }
        for pair in receipt.partitions.windows(2) {
            if pair[0].len() != self.state_count()
                || self.refine(&pair[0]) != pair[1]
                || pair[0] == pair[1]
            {
                return false;
            }
        }
        let Some(last) = receipt.partitions.last() else {
            return false;
        };
        if last.len() != self.state_count()
            || self.refine(last) != *last
            || receipt.state_to_block != *last
        {
            return false;
        }
        let checked = self.behavioral_quotient();
        receipt.quotient == checked.quotient
    }

    pub fn factor_surjective_quotient(
        &self,
        target: &Self,
        map: &[usize],
    ) -> Result<Vec<usize>, MooreError> {
        if self.input_count != target.input_count
            || map.len() != self.state_count()
            || map.iter().any(|&n| n >= target.state_count())
            || map.iter().copied().collect::<BTreeSet<_>>().len() != target.state_count()
        {
            return Err(MooreError::InvalidQuotientMap);
        }
        for m in 0..self.state_count() {
            if self.reports[m] != target.reports[map[m]]
                || (0..self.input_count)
                    .any(|i| map[self.transitions[m][i]] != target.transitions[map[m]][i])
            {
                return Err(MooreError::InvalidQuotientMap);
            }
        }
        let minimal = self.behavioral_quotient();
        let mut factor = vec![None; target.state_count()];
        for m in 0..self.state_count() {
            let block = minimal.state_to_block[m];
            match factor[map[m]] {
                Some(prior) if prior != block => return Err(MooreError::InvalidQuotientMap),
                _ => factor[map[m]] = Some(block),
            }
        }
        Ok(factor.into_iter().map(Option::unwrap).collect())
    }

    pub fn same_behavior_set(&self, other: &Self) -> bool {
        if self.input_count != other.input_count {
            return false;
        }
        let offset = self.state_count();
        let mut reports = self.reports.clone();
        reports.extend_from_slice(&other.reports);
        let mut transitions = self.transitions.clone();
        transitions.extend(
            other
                .transitions
                .iter()
                .map(|row| row.iter().map(|&s| s + offset).collect()),
        );
        let union = Self::new(reports, transitions, self.input_count).unwrap();
        let blocks = union.behavioral_quotient().state_to_block;
        blocks[..offset].iter().copied().collect::<BTreeSet<_>>()
            == blocks[offset..].iter().copied().collect::<BTreeSet<_>>()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn delayed_distinctions_and_nontrivial_blocks() {
        let m = FiniteMoore::new(
            vec![0, 0, 0, 0, 1, 1],
            vec![vec![1], vec![2], vec![4], vec![4], vec![4], vec![5]],
            1,
        )
        .unwrap();
        let q = m.behavioral_quotient();
        assert_eq!(q.state_to_block, vec![0, 1, 2, 2, 3, 3]);
        assert_eq!(q.partitions.len(), 3);
        assert!(m.verify_quotient(&q));
        assert!(m.is_report_congruence(&q.state_to_block));
        assert_eq!(q.quotient.behavioral_quotient().quotient, q.quotient);
    }

    #[test]
    fn quotient_universal_factor_and_classification() {
        let m = FiniteMoore::new(vec![0, 0, 1], vec![vec![2], vec![2], vec![2]], 1).unwrap();
        let q = m.behavioral_quotient();
        assert_eq!(
            m.factor_surjective_quotient(&q.quotient, &q.state_to_block)
                .unwrap(),
            vec![0, 1]
        );
        assert_eq!(
            m.factor_surjective_quotient(&m, &[0, 1, 2]).unwrap(),
            q.state_to_block
        );
        assert!(m.same_behavior_set(&q.quotient));
        let renamed = FiniteMoore::new(vec![1, 0], vec![vec![0], vec![0]], 1).unwrap();
        assert!(m.same_behavior_set(&renamed));
        let false_target = FiniteMoore::new(vec![0], vec![vec![0]], 1).unwrap();
        assert!(m
            .factor_surjective_quotient(&false_target, &[0, 0, 0])
            .is_err());
        assert!(!m.same_behavior_set(&false_target));
    }

    #[test]
    fn receipt_rejects_stable_overrefinement_and_forged_reports() {
        let m = FiniteMoore::new(vec![7, 7], vec![vec![0], vec![1]], 1).unwrap();
        let mut q = m.behavioral_quotient();
        q.partitions = vec![vec![0, 1]];
        q.state_to_block = vec![0, 1];
        q.quotient = m.clone();
        assert!(!m.verify_quotient(&q));
        let mut q = m.behavioral_quotient();
        q.quotient = FiniteMoore::new(vec![9], vec![vec![0]], 1).unwrap();
        assert!(!m.verify_quotient(&q));
    }

    #[test]
    fn totality_and_empty_alphabet() {
        assert!(FiniteMoore::new(vec![0, 1], vec![vec![0], vec![]], 1).is_err());
        assert!(FiniteMoore::new(vec![0], vec![vec![1]], 1).is_err());
        let static_reports =
            FiniteMoore::new(vec![0, 1, 0], vec![vec![], vec![], vec![]], 0).unwrap();
        assert_eq!(
            static_reports.behavioral_quotient().state_to_block,
            vec![0, 1, 0]
        );
    }
    #[test]
    fn exhaustive_three_state_greatest_congruence() {
        let partitions = [
            vec![0, 0, 0],
            vec![0, 0, 1],
            vec![0, 1, 0],
            vec![0, 1, 1],
            vec![0, 1, 2],
        ];
        for output_bits in 0..8 {
            for transition_code in 0..27 {
                let reports = (0..3).map(|i| (output_bits >> i) & 1).collect();
                let mut digits = transition_code;
                let transitions = (0..3)
                    .map(|_| {
                        let next = digits % 3;
                        digits /= 3;
                        vec![next]
                    })
                    .collect();
                let machine = FiniteMoore::new(reports, transitions, 1).unwrap();
                let quotient = machine.behavioral_quotient();
                assert!(machine.verify_quotient(&quotient));
                assert!(quotient.partitions.len() <= machine.state_count());
                for candidate in &partitions {
                    if machine.is_report_congruence(candidate) {
                        for s in 0..3 {
                            for t in 0..3 {
                                if candidate[s] == candidate[t] {
                                    assert_eq!(
                                        quotient.state_to_block[s],
                                        quotient.state_to_block[t]
                                    );
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
