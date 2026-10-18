
use num_traits::Zero;

use super::descent::{summarize_descent, DescentSummary};
use super::model::{EmpiricalModel, Scenario};
use super::{qr, EmpiricalError, MAX_GLOBAL_ASSIGNMENTS, Q};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParityCycle {
    targets: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParityCycleReport {
    pub holonomy: u8,
    pub global_support: usize,
    pub arc_cover: [u64; 2],
    pub descent: DescentSummary,
    pub strongly_contextual: bool,
}

impl ParityCycle {
    pub fn new(targets: Vec<u8>) -> Result<Self, EmpiricalError> {
        if targets.len() < 3 {
            return Err(EmpiricalError::CycleTooShort);
        }
        if targets.len() > 64 {
            return Err(EmpiricalError::CarrierSize);
        }
        if let Some(index) = targets.iter().position(|&target| target > 1) {
            return Err(EmpiricalError::ParityTarget { index });
        }
        Ok(Self { targets })
    }

    pub fn targets(&self) -> &[u8] {
        &self.targets
    }

    pub fn holonomy(&self) -> u8 {
        self.targets.iter().fold(0, |acc, t| acc ^ t)
    }

    pub fn scenario(&self) -> Result<Scenario, EmpiricalError> {
        let n = self.targets.len();
        let contexts = (0..n)
            .map(|i| {
                let mut c = vec![i, (i + 1) % n];
                c.sort_unstable();
                c
            })
            .collect();
        Scenario::binary(n, contexts)
    }

    pub fn model(&self) -> Result<EmpiricalModel, EmpiricalError> {
        let scenario = self.scenario()?;
        let distributions = self
            .targets
            .iter()
            .map(|&t| {
                (0..4usize)
                    .map(|k| {
                        let (x, y) = (k >> 1, k & 1);
                        if (x ^ y) as u8 == t {
                            qr(1, 2)
                        } else {
                            Q::zero()
                        }
                    })
                    .collect()
            })
            .collect();
        EmpiricalModel::new(scenario, distributions)
    }

    pub fn arc_cover(&self) -> [u64; 2] {
        let n = self.targets.len();
        let left = (0..n - 1).fold(0, |m, i| m | 1 << i);
        let right = (1..n).fold(0, |m, i| m | 1 << i);
        [left, right]
    }

    pub fn report(&self) -> Result<ParityCycleReport, EmpiricalError> {
        let model = self.model()?;
        let arc_cover = self.arc_cover();
        let presheaf = model.admissible_presheaf(&arc_cover)?;
        let classification = presheaf.classify_cover(
            model.scenario().full_mask(),
            &arc_cover,
            MAX_GLOBAL_ASSIGNMENTS,
        )?;
        let global_support = model.global_support()?.len();
        Ok(ParityCycleReport {
            holonomy: self.holonomy(),
            global_support,
            arc_cover,
            descent: summarize_descent(&classification),
            strongly_contextual: global_support == 0,
        })
    }
}
