
use std::collections::{BTreeMap, BTreeSet};

use omega_category_theory::finite_report_descent::{CoverClassification, FiniteReportPresheaf};

use super::model::Scenario;
use super::{positions, EmpiricalError};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AssignmentPresheaf {
    arities: Vec<usize>,
    sections: BTreeMap<u64, Vec<Vec<usize>>>,
}

impl AssignmentPresheaf {
    pub fn from_rule(
        arities: Vec<usize>,
        keys: &BTreeSet<u64>,
        admissible: impl Fn(&[usize], &[usize]) -> bool,
    ) -> Result<Self, EmpiricalError> {
        let n = arities.len();
        if n == 0 || n > 64 {
            return Err(EmpiricalError::CarrierSize);
        }
        let full = Scenario::full_of(n);
        let mut closed: BTreeSet<u64> = keys.iter().map(|k| k & full).collect();
        closed.insert(0);
        closed.insert(full);
        loop {
            let before = closed.len();
            let items: Vec<u64> = closed.iter().copied().collect();
            for &a in &items {
                for &b in &items {
                    closed.insert(a & b);
                }
            }
            if closed.len() == before {
                break;
            }
        }
        let scenario_like = Scenario {
            arities: arities.clone(),
            contexts: vec![(0..n).collect()],
        };
        let mut sections = BTreeMap::new();
        for &key in &closed {
            let window = positions(key);
            let count = scenario_like.section_count(&window)?;
            let admitted: Vec<Vec<usize>> = (0..count)
                .map(|k| scenario_like.assignment_of(&window, k))
                .filter(|assignment| admissible(&window, assignment))
                .collect();
            sections.insert(key, admitted);
        }
        Ok(Self { arities, sections })
    }

    pub fn arities(&self) -> &[usize] {
        &self.arities
    }

    pub fn sections(&self) -> &BTreeMap<u64, Vec<Vec<usize>>> {
        &self.sections
    }

    pub fn section_index(&self, key: u64, assignment: &[usize]) -> Option<usize> {
        self.sections
            .get(&key)?
            .iter()
            .position(|s| s.as_slice() == assignment)
    }

    pub fn to_finite_report_presheaf(&self) -> Result<FiniteReportPresheaf, EmpiricalError> {
        let report_counts: BTreeMap<u64, usize> =
            self.sections.iter().map(|(&k, s)| (k, s.len())).collect();
        let mut restrictions = BTreeMap::new();
        for (&source, sections) in &self.sections {
            for &target in self.sections.keys().filter(|&&t| t & source == t) {
                let (from, to) = (positions(source), positions(target));
                let table = sections
                    .iter()
                    .map(|s| {
                        Scenario::restrict(&from, s, &to)
                            .and_then(|r| self.section_index(target, &r))
                            .ok_or(EmpiricalError::NotClosedUnderRestriction {
                                from: source,
                                into: target,
                            })
                    })
                    .collect::<Result<Vec<usize>, EmpiricalError>>()?;
                restrictions.insert((source, target), table);
            }
        }
        Ok(FiniteReportPresheaf::new(
            self.arities.len(),
            report_counts,
            restrictions,
        )?)
    }

    pub fn classify_cover(
        &self,
        target: u64,
        cover: &[u64],
        limit: usize,
    ) -> Result<CoverClassification, EmpiricalError> {
        Ok(self
            .to_finite_report_presheaf()?
            .classify_cover(target, cover, limit)?)
    }
}
