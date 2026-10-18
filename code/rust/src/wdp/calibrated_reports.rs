use crate::observation_cost::{Instrument, ObservationCostError, ObservationInstance, MAX_STATES};
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use std::collections::{BTreeMap, BTreeSet};

pub const COST_DOMAIN: &str = "ideal_calibrated_interval_product";
pub const MAX_CANDIDATES: usize = 10;
pub const MAX_CHANNELS: usize = 12;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CalibratedError {
    #[error("candidate count must be between 1 and {MAX_CANDIDATES}")]
    CandidateCount,
    #[error("at most {MAX_CHANNELS} channels")]
    ChannelCount,
    #[error("aligned candidate tables required")]
    Misaligned,
    #[error("duplicate candidate or channel label")]
    Duplicate,
    #[error("nonempty channel and unit labels required")]
    EmptyLabel,
    #[error("nonzero gain and positive price required")]
    GainOrPrice,
    #[error("reversed interval")]
    ReversedInterval,
    #[error("raw and calibration bounds must be nonnegative and the gain nonzero")]
    BadBound,
    #[error("finite lift exceeds the reference solver state cap")]
    LiftCap,
    #[error("finite instance refused: {0}")]
    Instance(#[from] ObservationCostError),
}

pub fn transported_radius(
    gain: &BigRational,
    raw_bound: &BigRational,
    calibration_bound: &BigRational,
) -> Result<BigRational, CalibratedError> {
    if gain.is_zero() || raw_bound.is_negative() || calibration_bound.is_negative() {
        return Err(CalibratedError::BadBound);
    }
    Ok(gain.abs() * raw_bound + calibration_bound)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Channel {
    pub name: String,
    pub raw_unit: String,
    pub unit: String,
    pub gain: BigRational,
    pub offset: BigRational,
    pub intervals: Vec<(BigRational, BigRational)>,
    pub price: BigRational,
}

impl Channel {
    fn support(&self, value: &BigRational) -> BTreeSet<usize> {
        self.intervals
            .iter()
            .enumerate()
            .filter(|(_, (lo, hi))| lo <= value && value <= hi)
            .map(|(x, _)| x)
            .collect()
    }

    pub fn separates(&self, x: usize, y: usize) -> bool {
        let (a, b) = (&self.intervals[x], &self.intervals[y]);
        a.1 < b.0 || b.1 < a.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawReading {
    pub channel: String,
    pub raw_unit: String,
    pub value: BigRational,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RecoveryStatus {
    Verified,
    Abstain,
    Inconsistent,
    InvalidReport,
    InvalidProposal,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RecoveryEvaluation {
    pub status: RecoveryStatus,
    pub compatible: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CalibratedModel {
    states: Vec<String>,
    visible: Vec<String>,
    answers: Vec<String>,
    channels: Vec<Channel>,
}

impl CalibratedModel {
    pub fn new(
        states: Vec<String>,
        visible: Vec<String>,
        answers: Vec<String>,
        channels: Vec<Channel>,
    ) -> Result<Self, CalibratedError> {
        let n = states.len();
        if n == 0 || n > MAX_CANDIDATES {
            return Err(CalibratedError::CandidateCount);
        }
        if channels.len() > MAX_CHANNELS {
            return Err(CalibratedError::ChannelCount);
        }
        if visible.len() != n || answers.len() != n {
            return Err(CalibratedError::Misaligned);
        }
        if states.iter().collect::<BTreeSet<_>>().len() != n
            || channels.iter().map(|c| &c.name).collect::<BTreeSet<_>>().len() != channels.len()
        {
            return Err(CalibratedError::Duplicate);
        }
        for channel in &channels {
            if channel.name.is_empty() || channel.raw_unit.is_empty() || channel.unit.is_empty() {
                return Err(CalibratedError::EmptyLabel);
            }
            if channel.gain.is_zero() || !channel.price.is_positive() {
                return Err(CalibratedError::GainOrPrice);
            }
            if channel.intervals.len() != n {
                return Err(CalibratedError::Misaligned);
            }
            if channel.intervals.iter().any(|(lo, hi)| lo > hi) {
                return Err(CalibratedError::ReversedInterval);
            }
        }
        Ok(Self {
            states,
            visible,
            answers,
            channels,
        })
    }

    pub fn channels(&self) -> &[Channel] {
        &self.channels
    }

    pub fn evaluate(
        &self,
        visible: &str,
        readings: &[RawReading],
        proposed_answer: &str,
    ) -> RecoveryEvaluation {
        let mut candidates: BTreeSet<usize> = self
            .visible
            .iter()
            .enumerate()
            .filter(|(_, p)| p.as_str() == visible)
            .map(|(x, _)| x)
            .collect();
        let mut seen = BTreeSet::new();
        for reading in readings {
            let Some(channel) = self.channels.iter().find(|c| c.name == reading.channel) else {
                return self.status(RecoveryStatus::InvalidReport, &BTreeSet::new());
            };
            if !seen.insert(&reading.channel) || reading.raw_unit != channel.raw_unit {
                return self.status(RecoveryStatus::InvalidReport, &BTreeSet::new());
            }
            let calibrated = &channel.gain * &reading.value + &channel.offset;
            let support = channel.support(&calibrated);
            candidates.retain(|x| support.contains(x));
        }
        if candidates.is_empty() {
            return self.status(RecoveryStatus::Inconsistent, &candidates);
        }
        let answers: BTreeSet<&String> = candidates.iter().map(|&x| &self.answers[x]).collect();
        if answers.len() != 1 {
            return self.status(RecoveryStatus::Abstain, &candidates);
        }
        if !answers.contains(&proposed_answer.to_string()) {
            return self.status(RecoveryStatus::InvalidProposal, &candidates);
        }
        self.status(RecoveryStatus::Verified, &candidates)
    }

    fn status(&self, status: RecoveryStatus, set: &BTreeSet<usize>) -> RecoveryEvaluation {
        RecoveryEvaluation {
            status,
            compatible: set.iter().map(|&x| self.states[x].clone()).collect(),
        }
    }

    pub fn alphabet(&self, channel: usize) -> Vec<BTreeSet<usize>> {
        let c = &self.channels[channel];
        let endpoints: BTreeSet<BigRational> = c
            .intervals
            .iter()
            .flat_map(|(lo, hi)| [lo.clone(), hi.clone()])
            .collect();
        let endpoints: Vec<BigRational> = endpoints.into_iter().collect();
        let two = BigRational::from_integer(2.into());
        let representatives = endpoints.iter().cloned().chain(
            endpoints
                .windows(2)
                .map(|w| (&w[0] + &w[1]) / &two),
        );
        let signatures: BTreeSet<BTreeSet<usize>> = representatives
            .map(|value| c.support(&value))
            .filter(|s| !s.is_empty())
            .collect();
        signatures.into_iter().collect()
    }

    pub fn finite_lift(&self) -> Result<ObservationInstance, CalibratedError> {
        let alphabets: Vec<Vec<BTreeSet<usize>>> =
            (0..self.channels.len()).map(|i| self.alphabet(i)).collect();
        let mut worlds: Vec<(usize, Vec<usize>)> = Vec::new();
        for x in 0..self.states.len() {
            let options: Vec<Vec<usize>> = alphabets
                .iter()
                .map(|symbols| {
                    symbols
                        .iter()
                        .enumerate()
                        .filter(|(_, s)| s.contains(&x))
                        .map(|(k, _)| k)
                        .collect()
                })
                .collect();
            let count = options.iter().try_fold(1usize, |acc, o| acc.checked_mul(o.len()));
            match count {
                Some(c) if worlds.len() + c <= MAX_STATES => {}
                _ => return Err(CalibratedError::LiftCap),
            }
            let mut partial: Vec<Vec<usize>> = vec![Vec::new()];
            for choice in &options {
                partial = partial
                    .into_iter()
                    .flat_map(|prefix| {
                        choice.iter().map(move |&k| {
                            let mut next = prefix.clone();
                            next.push(k);
                            next
                        })
                    })
                    .collect();
            }
            worlds.extend(partial.into_iter().map(|reports| (x, reports)));
        }
        let instruments = self
            .channels
            .iter()
            .enumerate()
            .map(|(i, channel)| Instrument {
                name: channel.name.clone(),
                outcomes: worlds.iter().map(|(_, r)| r[i].to_string()).collect(),
                cost: channel.price.clone(),
            })
            .collect();
        Ok(ObservationInstance::new(
            (0..worlds.len()).map(|j| j.to_string()).collect(),
            worlds.iter().map(|(x, _)| self.visible[*x].clone()).collect(),
            worlds.iter().map(|(x, _)| self.answers[*x].clone()).collect(),
            instruments,
        )?)
    }

    fn unresolved_pairs(&self) -> Vec<(usize, usize)> {
        let n = self.states.len();
        (0..n)
            .flat_map(|x| ((x + 1)..n).map(move |y| (x, y)))
            .filter(|&(x, y)| self.visible[x] == self.visible[y] && self.answers[x] != self.answers[y])
            .collect()
    }

    pub fn fixed_robust_cost(&self) -> Option<(BigRational, u32)> {
        let pairs = self.unresolved_pairs();
        (0..(1u32 << self.channels.len()))
            .filter(|&mask| {
                pairs.iter().all(|&(x, y)| {
                    self.channels
                        .iter()
                        .enumerate()
                        .any(|(i, c)| mask & (1 << i) != 0 && c.separates(x, y))
                })
            })
            .map(|mask| {
                let cost = self
                    .channels
                    .iter()
                    .enumerate()
                    .filter(|(i, _)| mask & (1 << i) != 0)
                    .fold(BigRational::zero(), |acc, (_, c)| acc + &c.price);
                (cost, mask)
            })
            .min()
    }

    pub fn adaptive_robust_cost(&self) -> Option<BigRational> {
        let alphabets: Vec<Vec<BTreeSet<usize>>> =
            (0..self.channels.len()).map(|i| self.alphabet(i)).collect();
        let mut fibers: BTreeMap<&String, BTreeSet<usize>> = BTreeMap::new();
        for (x, p) in self.visible.iter().enumerate() {
            fibers.entry(p).or_default().insert(x);
        }
        let all: u32 = (1u32 << self.channels.len()) - 1;
        let mut memo = BTreeMap::new();
        let mut worst = BigRational::zero();
        for fiber in fibers.into_values() {
            let value = self.recursion(&alphabets, fiber, all, &mut memo)?;
            if value > worst {
                worst = value;
            }
        }
        Some(worst)
    }

    fn recursion(
        &self,
        alphabets: &[Vec<BTreeSet<usize>>],
        candidates: BTreeSet<usize>,
        remaining: u32,
        memo: &mut BTreeMap<(BTreeSet<usize>, u32), Option<BigRational>>,
    ) -> Option<BigRational> {
        let answers: BTreeSet<&String> = candidates.iter().map(|&x| &self.answers[x]).collect();
        if answers.len() <= 1 {
            return Some(BigRational::zero());
        }
        let key = (candidates.clone(), remaining);
        if let Some(value) = memo.get(&key) {
            return value.clone();
        }
        let mut best: Option<BigRational> = None;
        for (i, channel) in self.channels.iter().enumerate() {
            if remaining & (1 << i) == 0 {
                continue;
            }
            let mut worst_branch = Some(BigRational::zero());
            for signature in &alphabets[i] {
                let child: BTreeSet<usize> = candidates.intersection(signature).copied().collect();
                if child.is_empty() {
                    continue;
                }
                let value = self.recursion(alphabets, child, remaining & !(1 << i), memo);
                worst_branch = match (worst_branch, value) {
                    (Some(w), Some(v)) => Some(if v > w { v } else { w }),
                    _ => None,
                };
                if worst_branch.is_none() {
                    break;
                }
            }
            if let Some(w) = worst_branch {
                let total = &channel.price + w;
                if best.as_ref().map_or(true, |b| &total < b) {
                    best = Some(total);
                }
            }
        }
        memo.insert(key, best.clone());
        best
    }
}
