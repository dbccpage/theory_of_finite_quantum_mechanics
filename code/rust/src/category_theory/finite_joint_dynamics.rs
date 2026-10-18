use crate::finite_continuation::{ContinuationError, DistinguishingWord, PartialDynamics};
use crate::finite_moore::MooreQuotient;
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JointOperation {
    Left(usize),
    Right(usize),
    Interaction(Vec<Option<usize>>),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JointDynamicsError {
    InvalidRelation,
    InvalidOperation,
    NotClosed {
        row: usize,
        operation: usize,
        target: (usize, usize),
    },
    WorkLimit,
    Dynamics(ContinuationError),
    CertificateMismatch,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointDynamicsAnalysis {
    pub refinement: MooreQuotient,
    pub collision: Option<DistinguishingWord>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointDynamics {
    pairs: Vec<(usize, usize)>,
    local_reports: Vec<(usize, usize)>,
    dynamics: PartialDynamics,
    pair_budget: usize,
}

fn refinement_cost(m: &PartialDynamics) -> Option<usize> {
    let n = m.reports().len().checked_add(1)?;
    n.checked_mul(n)?
        .checked_mul(m.transitions()[0].len().checked_add(1)?)
}

impl JointDynamics {
    pub fn new(
        left: &PartialDynamics,
        right: &PartialDynamics,
        pairs: Vec<(usize, usize)>,
        operations: &[JointOperation],
        max_cells: usize,
    ) -> Result<Self, JointDynamicsError> {
        let size = pairs
            .len()
            .checked_add(1)
            .ok_or(JointDynamicsError::WorkLimit)?;
        let pair_budget = size
            .checked_mul(size)
            .ok_or(JointDynamicsError::WorkLimit)?;
        let cost = pair_budget
            .checked_mul(
                operations
                    .len()
                    .checked_add(1)
                    .ok_or(JointDynamicsError::WorkLimit)?,
            )
            .and_then(|n| refinement_cost(left).and_then(|l| n.checked_add(l)))
            .and_then(|n| refinement_cost(right).and_then(|r| n.checked_add(r)));
        if cost.is_none_or(|n| n > max_cells) {
            return Err(JointDynamicsError::WorkLimit);
        }
        let ids: BTreeMap<_, _> = pairs
            .iter()
            .copied()
            .enumerate()
            .map(|(i, p)| (p, i))
            .collect();
        if pairs.is_empty()
            || ids.len() != pairs.len()
            || pairs
                .iter()
                .any(|&(l, r)| l >= left.reports().len() || r >= right.reports().len())
        {
            return Err(JointDynamicsError::InvalidRelation);
        }
        for op in operations {
            let valid = match op {
                JointOperation::Left(a) => *a < left.transitions()[0].len(),
                JointOperation::Right(a) => *a < right.transitions()[0].len(),
                JointOperation::Interaction(t) => {
                    t.len() == pairs.len() && t.iter().flatten().all(|&s| s < pairs.len())
                }
            };
            if !valid {
                return Err(JointDynamicsError::InvalidOperation);
            }
        }
        let mut transitions = Vec::new();
        for (row, &(l, r)) in pairs.iter().enumerate() {
            let mut next = Vec::new();
            for (operation, op) in operations.iter().enumerate() {
                let target = match op {
                    JointOperation::Left(a) => left.transitions()[l][*a].map(|t| (t, r)),
                    JointOperation::Right(a) => right.transitions()[r][*a].map(|t| (l, t)),
                    JointOperation::Interaction(t) => {
                        next.push(t[row]);
                        continue;
                    }
                };
                next.push(match target {
                    None => None,
                    Some(target) => {
                        Some(*ids.get(&target).ok_or(JointDynamicsError::NotClosed {
                            row,
                            operation,
                            target,
                        })?)
                    }
                });
            }
            transitions.push(next);
        }
        let lc = left.quotient().state_to_block;
        let rc = right.quotient().state_to_block;
        let local_reports: Vec<_> = pairs.iter().map(|&(l, r)| (lc[l], rc[r])).collect();
        let mut labels = BTreeMap::new();
        let reports = local_reports
            .iter()
            .map(|&p| {
                let id = labels.len();
                *labels.entry(p).or_insert(id)
            })
            .collect();
        let dynamics = PartialDynamics::new(reports, transitions, operations.len())
            .map_err(JointDynamicsError::Dynamics)?;
        Ok(Self {
            pairs,
            local_reports,
            dynamics,
            pair_budget,
        })
    }
    pub fn pairs(&self) -> &[(usize, usize)] {
        &self.pairs
    }
    pub fn local_reports(&self) -> &[(usize, usize)] {
        &self.local_reports
    }
    pub fn dynamics(&self) -> &PartialDynamics {
        &self.dynamics
    }

    pub fn analyze(&self) -> Result<JointDynamicsAnalysis, JointDynamicsError> {
        let refinement = self.dynamics.quotient();
        let mut collision = None;
        'outer: for r in 0..self.pairs.len() {
            for l in 0..r {
                if self.local_reports[l] == self.local_reports[r]
                    && refinement.state_to_block[l] != refinement.state_to_block[r]
                {
                    collision = self
                        .dynamics
                        .distinguish(l, r, self.pair_budget)
                        .map_err(JointDynamicsError::Dynamics)?;
                    break 'outer;
                }
            }
        }
        Ok(JointDynamicsAnalysis {
            refinement,
            collision,
        })
    }
    pub fn verify(&self, c: &JointDynamicsAnalysis) -> Result<(), JointDynamicsError> {
        if self.analyze()? == *c {
            Ok(())
        } else {
            Err(JointDynamicsError::CertificateMismatch)
        }
    }
}
