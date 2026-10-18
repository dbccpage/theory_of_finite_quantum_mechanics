
use std::collections::{BTreeMap, BTreeSet};

use crate::finite_moore::FiniteMoore;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ClassificationError {
    InvalidModel,
    ImpossibleSignature,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RetentionSignature {
    pub nontrivial: bool,
    pub reversible: bool,
    pub observable: bool,
    pub tolerance: bool,
    pub minimal: bool,
    pub active: bool,
}

impl RetentionSignature {
    pub fn is_realizable(self) -> bool {
        if !self.nontrivial {
            return self.reversible
                && self.observable
                && !self.tolerance
                && self.minimal
                && !self.active;
        }
        if self.observable && !self.tolerance && !self.minimal {
            return false;
        }
        if !self.active {
            return self.reversible && self.minimal == (self.observable && !self.tolerance);
        }
        true
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteRetentionModel {
    raw_reports: Vec<usize>,
    moore: FiniteMoore,
}

impl FiniteRetentionModel {
    pub fn new(
        raw_reports: Vec<usize>,
        recognized: Vec<usize>,
        transitions: Vec<Vec<usize>>,
        inputs: usize,
    ) -> Result<Self, ClassificationError> {
        if raw_reports.len() != recognized.len() {
            return Err(ClassificationError::InvalidModel);
        }
        let mut factor = BTreeMap::new();
        for (&raw, &report) in raw_reports.iter().zip(&recognized) {
            if let Some(previous) = factor.insert(raw, report) {
                if previous != report {
                    return Err(ClassificationError::InvalidModel);
                }
            }
        }
        let moore = FiniteMoore::new(recognized, transitions, inputs)
            .map_err(|_| ClassificationError::InvalidModel)?;
        Ok(Self { raw_reports, moore })
    }

    pub fn raw_reports(&self) -> &[usize] {
        &self.raw_reports
    }
    pub fn moore(&self) -> &FiniteMoore {
        &self.moore
    }

    pub fn signature(&self) -> RetentionSignature {
        let n = self.moore.state_count();
        let observable = self.raw_reports.iter().collect::<BTreeSet<_>>().len() == n;
        let tolerance = (0..n).any(|x| {
            (0..n).any(|y| {
                self.raw_reports[x] != self.raw_reports[y]
                    && self.moore.reports()[x] == self.moore.reports()[y]
            })
        });
        let reversible = (0..self.moore.input_count()).all(|i| {
            self.moore
                .transitions()
                .iter()
                .map(|row| row[i])
                .collect::<BTreeSet<_>>()
                .len()
                == n
        });
        let active = self
            .moore
            .transitions()
            .iter()
            .enumerate()
            .any(|(x, row)| row.iter().any(|&y| x != y));
        RetentionSignature {
            nontrivial: n > 1,
            reversible,
            observable,
            tolerance,
            minimal: self.moore.behavioral_quotient().quotient.state_count() == n,
            active,
        }
    }
}

pub fn realize_retention(
    signature: RetentionSignature,
) -> Result<FiniteRetentionModel, ClassificationError> {
    if !signature.is_realizable() {
        return Err(ClassificationError::ImpossibleSignature);
    }
    let (raw, recognized) = if !signature.nontrivial {
        (vec![0], vec![0])
    } else if signature.minimal {
        match (signature.observable, signature.tolerance) {
            (true, false) => (vec![0, 1], vec![0, 1]),
            (false, false) => (vec![0, 0, 1], vec![0, 0, 1]),
            (true, true) => (vec![0, 1, 2], vec![0, 0, 1]),
            (false, true) => (vec![0, 0, 1, 2], vec![0, 0, 0, 1]),
        }
    } else {
        match (signature.observable, signature.tolerance) {
            (true, true) => (vec![0, 1], vec![0, 0]),
            (false, false) => (vec![0, 0], vec![0, 0]),
            (false, true) => (vec![0, 0, 1], vec![0, 0, 0]),
            (true, false) => return Err(ClassificationError::ImpossibleSignature),
        }
    };
    let n = raw.len();
    let transitions = (0..n)
        .map(|x| {
            vec![if !signature.active {
                x
            } else if signature.reversible {
                (x + 1) % n
            } else if signature.minimal {
                (x + 1).min(n - 1)
            } else {
                0
            }]
        })
        .collect();
    FiniteRetentionModel::new(raw, recognized, transitions, 1)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FunctionalSignature {
    pub linked: bool,
    pub presentation_stable: bool,
    pub report_stable: bool,
    pub calibrated: bool,
    pub blind_spot: bool,
}

impl FunctionalSignature {
    pub fn is_realizable(self) -> bool {
        (self.blind_spot || self.linked)
            && !(self.linked && self.presentation_stable && !self.report_stable)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteFunctionalModel {
    presentation: Vec<usize>,
    report: Vec<usize>,
    context: Vec<usize>,
    target: Vec<usize>,
}

impl FiniteFunctionalModel {
    pub fn new(
        presentation: Vec<usize>,
        report: Vec<usize>,
        context: Vec<usize>,
        target: Vec<usize>,
    ) -> Result<Self, ClassificationError> {
        let n = presentation.len();
        if n == 0
            || report.len() != n
            || context.len() != n
            || target.len() != n
            || context.iter().any(|&x| x >= n)
        {
            return Err(ClassificationError::InvalidModel);
        }
        Ok(Self {
            presentation,
            report,
            context,
            target,
        })
    }
    pub fn presentation(&self) -> &[usize] {
        &self.presentation
    }
    pub fn report(&self) -> &[usize] {
        &self.report
    }
    pub fn context(&self) -> &[usize] {
        &self.context
    }
    pub fn target(&self) -> &[usize] {
        &self.target
    }

    pub fn report_factor(&self) -> Option<BTreeMap<usize, usize>> {
        let mut factor = BTreeMap::new();
        for (&q, &s) in self.presentation.iter().zip(&self.report) {
            if let Some(old) = factor.insert(q, s) {
                if old != s {
                    return None;
                }
            }
        }
        Some(factor)
    }
    pub fn signature(&self) -> FunctionalSignature {
        FunctionalSignature {
            linked: self.report_factor().is_some(),
            presentation_stable: self
                .context
                .iter()
                .enumerate()
                .all(|(x, &tx)| self.presentation[x] == self.presentation[tx]),
            report_stable: self
                .context
                .iter()
                .enumerate()
                .all(|(x, &tx)| self.report[x] == self.report[tx]),
            calibrated: self.report == self.target,
            blind_spot: self.presentation.iter().collect::<BTreeSet<_>>().len()
                < self.presentation.len(),
        }
    }
}

pub fn realize_functional(
    signature: FunctionalSignature,
) -> Result<FiniteFunctionalModel, ClassificationError> {
    if !signature.is_realizable() {
        return Err(ClassificationError::ImpossibleSignature);
    }
    let (q, s, t) = if !signature.blind_spot {
        let q = vec![0, 1];
        if signature.presentation_stable {
            (q, vec![0, 1], vec![0, 1])
        } else if signature.report_stable {
            (q, vec![0, 0], vec![1, 1])
        } else {
            (q, vec![0, 1], vec![1, 1])
        }
    } else if signature.linked {
        let q = vec![0, 0, 1];
        if signature.presentation_stable {
            (q, vec![0, 0, 1], vec![0, 1, 2])
        } else if signature.report_stable {
            (q, vec![0, 0, 0], vec![2, 1, 2])
        } else {
            (q, vec![0, 0, 1], vec![2, 1, 2])
        }
    } else {
        let q = vec![0, 0, 1];
        if signature.presentation_stable {
            if signature.report_stable {
                (q, vec![0, 1, 0], vec![0, 1, 2])
            } else {
                (q, vec![0, 1, 0], vec![1, 1, 2])
            }
        } else if signature.report_stable {
            (q, vec![0, 1, 0], vec![2, 1, 2])
        } else {
            (q, vec![0, 1, 2], vec![2, 1, 2])
        }
    };
    let mut target = s.clone();
    if !signature.calibrated {
        target[0] += 1;
    }
    FiniteFunctionalModel::new(q, s, t, target)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PropertyLiteral {
    pub index: usize,
    pub value: bool,
}

pub fn retention_implication_countermodel(
    premises: &[PropertyLiteral],
    conclusion: PropertyLiteral,
) -> Result<Option<FiniteRetentionModel>, ClassificationError> {
    if conclusion.index >= 6 || premises.iter().any(|literal| literal.index >= 6) {
        return Err(ClassificationError::InvalidModel);
    }
    for bits in 0_usize..64 {
        let flags: [bool; 6] = std::array::from_fn(|i| bits & (1 << i) != 0);
        if flags[conclusion.index] == conclusion.value
            || premises
                .iter()
                .any(|literal| flags[literal.index] != literal.value)
        {
            continue;
        }
        let signature = RetentionSignature {
            nontrivial: flags[0],
            reversible: flags[1],
            observable: flags[2],
            tolerance: flags[3],
            minimal: flags[4],
            active: flags[5],
        };
        if signature.is_realizable() {
            return realize_retention(signature).map(Some);
        }
    }
    Ok(None)
}

pub fn functional_implication_countermodel(
    premises: &[PropertyLiteral],
    conclusion: PropertyLiteral,
) -> Result<Option<FiniteFunctionalModel>, ClassificationError> {
    if conclusion.index >= 5 || premises.iter().any(|literal| literal.index >= 5) {
        return Err(ClassificationError::InvalidModel);
    }
    for bits in 0_usize..32 {
        let flags: [bool; 5] = std::array::from_fn(|i| bits & (1 << i) != 0);
        if flags[conclusion.index] == conclusion.value
            || premises
                .iter()
                .any(|literal| flags[literal.index] != literal.value)
        {
            continue;
        }
        let signature = FunctionalSignature {
            linked: flags[0],
            presentation_stable: flags[1],
            report_stable: flags[2],
            calibrated: flags[3],
            blind_spot: flags[4],
        };
        if signature.is_realizable() {
            return realize_functional(signature).map(Some);
        }
    }
    Ok(None)
}
