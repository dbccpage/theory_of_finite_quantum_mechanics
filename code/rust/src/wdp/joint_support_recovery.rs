use crate::observation_cost::{
    rational_text, Instrument, ObservationCostError, ObservationInstance, MAX_INSTRUMENTS,
    MAX_STATES,
};
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use std::collections::{BTreeMap, BTreeSet};

pub const MAX_INPUT_BITS: u64 = 256;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum JointSupportError {
    #[error("joint model exceeds the finite reference caps")]
    CapExceeded,
    #[error("channel names must be nonempty and unique, with nonzero gain and positive price")]
    BadChannel,
    #[error("segments need nonempty state labels and one free report and answer per state")]
    BadSegment,
    #[error("reversed parameter interval")]
    ReversedInterval,
    #[error("affine rows must match the channel count")]
    ShapeMismatch,
    #[error("finite reduction requires every segment slope to be nonzero")]
    ZeroSlope,
    #[error("joint witness exceeds the existing finite solver state cap")]
    WitnessExceedsSolverCap,
    #[error("inconsistent history")]
    InconsistentHistory,
    #[error("invalid channel index")]
    BadChannelIndex,
    #[error("finite instance rejected: {0}")]
    Instance(#[from] ObservationCostError),
    #[error("no-signalling violation detected: marginal depends on remote setting")]
    SignallingDetected,
    #[error("unnormalized bipartite behavior: probabilities do not sum to 1")]
    UnnormalizedBehavior,
    #[error("negative probability in bipartite behavior")]
    NegativeProbability,
    #[error("empty settings or outcomes in bipartite behavior")]
    EmptyBehavior,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Channel {
    pub name: String,
    pub raw_gain: BigRational,
    pub raw_offset: BigRational,
    pub price: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Segment {
    pub state: String,
    pub visible: String,
    pub answer: String,
    pub lower: BigRational,
    pub upper: BigRational,
    pub slopes: Vec<BigRational>,
    pub offsets: Vec<BigRational>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct JointModel {
    channels: Vec<Channel>,
    segments: Vec<Segment>,
}

pub type World = (String, Vec<BigRational>);

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum JointStatus {
    Verified(Vec<String>),
    Abstain(Vec<String>),
    InvalidProposal(Vec<String>),
    Inconsistent,
    InvalidReport,
}

fn bounded(value: &BigRational) -> bool {
    value.numer().magnitude().bits() <= MAX_INPUT_BITS
        && value.denom().magnitude().bits() <= MAX_INPUT_BITS
}

impl JointModel {
    pub fn new(channels: Vec<Channel>, segments: Vec<Segment>) -> Result<Self, JointSupportError> {
        if channels.len() > MAX_INSTRUMENTS || segments.is_empty() || segments.len() > MAX_STATES {
            return Err(JointSupportError::CapExceeded);
        }
        let mut names = BTreeSet::new();
        for channel in &channels {
            if channel.name.is_empty()
                || !names.insert(channel.name.clone())
                || channel.raw_gain.is_zero()
                || !channel.price.is_positive()
                || ![&channel.raw_gain, &channel.raw_offset, &channel.price]
                    .into_iter()
                    .all(bounded)
            {
                return Err(JointSupportError::BadChannel);
            }
        }
        let mut metadata: BTreeMap<&str, (&str, &str)> = BTreeMap::new();
        for segment in &segments {
            if segment.state.is_empty() {
                return Err(JointSupportError::BadSegment);
            }
            let entry = (segment.visible.as_str(), segment.answer.as_str());
            if *metadata.entry(segment.state.as_str()).or_insert(entry) != entry {
                return Err(JointSupportError::BadSegment);
            }
            if segment.slopes.len() != channels.len() || segment.offsets.len() != channels.len() {
                return Err(JointSupportError::ShapeMismatch);
            }
            let mut values = [&segment.lower, &segment.upper]
                .into_iter()
                .chain(&segment.slopes)
                .chain(&segment.offsets);
            if !values.all(bounded) {
                return Err(JointSupportError::CapExceeded);
            }
            if segment.lower > segment.upper {
                return Err(JointSupportError::ReversedInterval);
            }
            if segment.slopes.iter().any(Zero::is_zero) {
                return Err(JointSupportError::ZeroSlope);
            }
        }
        Ok(Self { channels, segments })
    }

    pub fn channels(&self) -> &[Channel] {
        &self.channels
    }

    pub fn segments(&self) -> &[Segment] {
        &self.segments
    }

    fn metadata(&self, state: &str) -> (&str, &str) {
        self.segments
            .iter()
            .find(|s| s.state == state)
            .map(|s| (s.visible.as_str(), s.answer.as_str()))
            .unwrap_or_default()
    }
}

fn world(segment: &Segment, parameter: &BigRational) -> World {
    let values = segment
        .slopes
        .iter()
        .zip(&segment.offsets)
        .map(|(a, b)| a * parameter + b)
        .collect();
    (segment.state.clone(), values)
}

fn parameter_at(segment: &Segment, i: usize, value: &BigRational) -> BigRational {
    (value - &segment.offsets[i]) / &segment.slopes[i]
}

fn fiber(segments: &[&Segment], i: usize, value: &BigRational) -> Vec<World> {
    let mut worlds: Vec<World> = Vec::new();
    for segment in segments {
        let parameter = parameter_at(segment, i, value);
        if segment.lower <= parameter && parameter <= segment.upper {
            let candidate = world(segment, &parameter);
            if !worlds.contains(&candidate) {
                worlds.push(candidate);
            }
        }
    }
    worlds
}

fn image(segment: &Segment, i: usize) -> (BigRational, BigRational) {
    let a = &segment.slopes[i] * &segment.lower + &segment.offsets[i];
    let b = &segment.slopes[i] * &segment.upper + &segment.offsets[i];
    if a <= b {
        (a, b)
    } else {
        (b, a)
    }
}

fn prediction(segment: &Segment, i: usize, j: usize) -> (BigRational, BigRational) {
    let slope = &segment.slopes[j] / &segment.slopes[i];
    let intercept = &segment.offsets[j] - &slope * &segment.offsets[i];
    (slope, intercept)
}

fn overlap(left: &Segment, right: &Segment, i: usize) -> Option<(BigRational, BigRational)> {
    let (l0, l1) = image(left, i);
    let (r0, r1) = image(right, i);
    let low = l0.max(r0);
    let high = l1.min(r1);
    (low <= high).then_some((low, high))
}

pub fn collision(model: &JointModel) -> Option<(World, World)> {
    let segments = &model.segments;
    for (index, left) in segments.iter().enumerate() {
        for right in &segments[index + 1..] {
            if left.visible != right.visible || left.answer == right.answer {
                continue;
            }
            if model.channels.is_empty() {
                return Some((world(left, &left.lower), world(right, &right.lower)));
            }
            let Some((low, high)) = overlap(left, right, 0) else {
                continue;
            };
            let mut root: Option<BigRational> = None;
            let mut compatible = true;
            for j in 0..model.channels.len() {
                let (a, b) = prediction(left, 0, j);
                let (c, d) = prediction(right, 0, j);
                if a == c {
                    if b != d {
                        compatible = false;
                        break;
                    }
                } else {
                    let value = (&d - &b) / (&a - &c);
                    if root.as_ref().is_some_and(|r| *r != value) {
                        compatible = false;
                        break;
                    }
                    root = Some(value);
                }
            }
            let value = root.unwrap_or_else(|| low.clone());
            if compatible && low <= value && value <= high {
                let worlds = fiber(&[left, right], 0, &value);
                if worlds.len() == 2 && worlds[0].1 == worlds[1].1 {
                    let mut it = worlds.into_iter();
                    return Some((it.next()?, it.next()?));
                }
            }
        }
    }
    None
}

fn critical_values(segments: &[&Segment], i: usize, width: usize) -> Vec<BigRational> {
    let mut points: BTreeSet<BigRational> = BTreeSet::new();
    for segment in segments {
        let (a, b) = image(segment, i);
        points.insert(a);
        points.insert(b);
    }
    for (index, left) in segments.iter().enumerate() {
        for right in &segments[index + 1..] {
            let Some((low, high)) = overlap(left, right, i) else {
                continue;
            };
            for j in 0..width {
                let (a, b) = prediction(left, i, j);
                let (c, d) = prediction(right, i, j);
                if a != c {
                    let root = (&d - &b) / (&a - &c);
                    if low <= root && root <= high {
                        points.insert(root);
                    }
                }
            }
        }
    }
    points.into_iter().collect()
}

pub fn sample_worlds(model: &JointModel) -> Result<Vec<World>, JointSupportError> {
    if let Some((left, right)) = collision(model) {
        return Ok(vec![left, right]);
    }
    let mut worlds: Vec<World> = Vec::new();
    let mut admit = |candidate: World| -> Result<(), JointSupportError> {
        if !worlds.contains(&candidate) {
            if worlds.len() == MAX_STATES {
                return Err(JointSupportError::WitnessExceedsSolverCap);
            }
            worlds.push(candidate);
        }
        Ok(())
    };
    for segment in &model.segments {
        admit(world(segment, &segment.lower))?;
    }
    let reports: BTreeSet<&str> = model.segments.iter().map(|s| s.visible.as_str()).collect();
    let two = BigRational::from_integer(2.into());
    for visible in reports {
        let segments: Vec<&Segment> =
            model.segments.iter().filter(|s| s.visible == visible).collect();
        let answers: BTreeSet<&str> = segments.iter().map(|s| s.answer.as_str()).collect();
        if answers.len() == 1 {
            continue;
        }
        for i in 0..model.channels.len() {
            let endpoints = critical_values(&segments, i, model.channels.len());
            let mut representatives: BTreeSet<BigRational> = endpoints.iter().cloned().collect();
            for pair in endpoints.windows(2) {
                representatives.insert((&pair[0] + &pair[1]) / &two);
            }
            for value in &representatives {
                let found = fiber(&segments, i, value);
                let labels: BTreeSet<&str> =
                    found.iter().map(|(state, _)| model.metadata(state).1).collect();
                if labels.len() > 1 {
                    for candidate in found {
                        admit(candidate)?;
                    }
                }
            }
        }
    }
    Ok(worlds)
}

fn instance(
    model: &JointModel,
    worlds: &[World],
    remaining: &[usize],
) -> Result<ObservationInstance, JointSupportError> {
    let states = (0..worlds.len()).map(|i| i.to_string()).collect();
    let visible = worlds.iter().map(|(s, _)| model.metadata(s).0.to_string()).collect();
    let query = worlds.iter().map(|(s, _)| model.metadata(s).1.to_string()).collect();
    let instruments = remaining
        .iter()
        .map(|&j| Instrument {
            name: model.channels[j].name.clone(),
            outcomes: worlds.iter().map(|(_, v)| rational_text(&v[j])).collect(),
            cost: model.channels[j].price.clone(),
        })
        .collect();
    Ok(ObservationInstance::new(states, visible, query, instruments)?)
}

pub fn finite_instance(model: &JointModel) -> Result<ObservationInstance, JointSupportError> {
    let worlds = sample_worlds(model)?;
    let all: Vec<usize> = (0..model.channels.len()).collect();
    instance(model, &worlds, &all)
}

pub fn conditional_instance(
    model: &JointModel,
    i: usize,
    value: &BigRational,
    visible: &str,
) -> Result<ObservationInstance, JointSupportError> {
    if i >= model.channels.len() {
        return Err(JointSupportError::BadChannelIndex);
    }
    let segments: Vec<&Segment> = model.segments.iter().filter(|s| s.visible == visible).collect();
    let worlds = fiber(&segments, i, value);
    if worlds.is_empty() {
        return Err(JointSupportError::InconsistentHistory);
    }
    let remaining: Vec<usize> = (0..model.channels.len()).filter(|&j| j != i).collect();
    instance(model, &worlds, &remaining)
}

pub fn calibrate(channel: &Channel, raw: &BigRational) -> BigRational {
    &channel.raw_gain * raw + &channel.raw_offset
}

fn matches(segment: &Segment, readings: &[(usize, BigRational)]) -> bool {
    let Some((i, value)) = readings.first() else {
        return true;
    };
    let parameter = parameter_at(segment, *i, value);
    segment.lower <= parameter
        && parameter <= segment.upper
        && readings
            .iter()
            .all(|(j, observed)| &segment.slopes[*j] * &parameter + &segment.offsets[*j] == *observed)
}

pub fn evaluate(
    model: &JointModel,
    visible: &str,
    readings: &[(usize, BigRational)],
    proposed_answer: &str,
) -> JointStatus {
    let mut seen = BTreeSet::new();
    if readings.len() > model.channels.len()
        || readings.iter().any(|(i, _)| *i >= model.channels.len() || !seen.insert(*i))
    {
        return JointStatus::InvalidReport;
    }
    let mut labels: Vec<String> = Vec::new();
    let mut answers: BTreeSet<&str> = BTreeSet::new();
    for segment in &model.segments {
        if segment.visible == visible && matches(segment, readings) {
            if !labels.contains(&segment.state) {
                labels.push(segment.state.clone());
            }
            answers.insert(segment.answer.as_str());
        }
    }
    if labels.is_empty() {
        return JointStatus::Inconsistent;
    }
    if answers.len() != 1 {
        return JointStatus::Abstain(labels);
    }
    if !answers.contains(proposed_answer) {
        return JointStatus::InvalidProposal(labels);
    }
    JointStatus::Verified(labels)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BipartiteBehavior {
    pub num_alice_settings: usize,
    pub num_bob_settings: usize,
    pub num_alice_outcomes: usize,
    pub num_bob_outcomes: usize,
    pub table: Vec<Vec<Vec<Vec<BigRational>>>>,
}

impl BipartiteBehavior {
    pub fn new(table: Vec<Vec<Vec<Vec<BigRational>>>>) -> Result<Self, JointSupportError> {
        let num_alice_settings = table.len();
        if num_alice_settings == 0 {
            return Err(JointSupportError::EmptyBehavior);
        }
        let num_bob_settings = table[0].len();
        if num_bob_settings == 0 {
            return Err(JointSupportError::EmptyBehavior);
        }
        let num_alice_outcomes = table[0][0].len();
        if num_alice_outcomes == 0 {
            return Err(JointSupportError::EmptyBehavior);
        }
        let num_bob_outcomes = table[0][0][0].len();
        if num_bob_outcomes == 0 {
            return Err(JointSupportError::EmptyBehavior);
        }

        let one = BigRational::from_integer(1.into());
        for x in 0..num_alice_settings {
            if table[x].len() != num_bob_settings {
                return Err(JointSupportError::ShapeMismatch);
            }
            for y in 0..num_bob_settings {
                if table[x][y].len() != num_alice_outcomes {
                    return Err(JointSupportError::ShapeMismatch);
                }
                let mut sum = BigRational::zero();
                for a in 0..num_alice_outcomes {
                    if table[x][y][a].len() != num_bob_outcomes {
                        return Err(JointSupportError::ShapeMismatch);
                    }
                    for b in 0..num_bob_outcomes {
                        let p = &table[x][y][a][b];
                        if p.is_negative() {
                            return Err(JointSupportError::NegativeProbability);
                        }
                        sum += p;
                    }
                }
                if sum != one {
                    return Err(JointSupportError::UnnormalizedBehavior);
                }
            }
        }

        Ok(Self {
            num_alice_settings,
            num_bob_settings,
            num_alice_outcomes,
            num_bob_outcomes,
            table,
        })
    }

    pub fn from_product(
        pa: &[Vec<BigRational>],
        pb: &[Vec<BigRational>],
    ) -> Result<Self, JointSupportError> {
        let num_alice_settings = pa.len();
        let num_bob_settings = pb.len();
        if num_alice_settings == 0 || num_bob_settings == 0 {
            return Err(JointSupportError::EmptyBehavior);
        }
        let num_alice_outcomes = pa[0].len();
        let num_bob_outcomes = pb[0].len();
        if num_alice_outcomes == 0 || num_bob_outcomes == 0 {
            return Err(JointSupportError::EmptyBehavior);
        }

        let one = BigRational::from_integer(1.into());
        for row in pa {
            if row.len() != num_alice_outcomes {
                return Err(JointSupportError::ShapeMismatch);
            }
            let mut sum = BigRational::zero();
            for p in row {
                if p.is_negative() {
                    return Err(JointSupportError::NegativeProbability);
                }
                sum += p;
            }
            if sum != one {
                return Err(JointSupportError::UnnormalizedBehavior);
            }
        }
        for row in pb {
            if row.len() != num_bob_outcomes {
                return Err(JointSupportError::ShapeMismatch);
            }
            let mut sum = BigRational::zero();
            for p in row {
                if p.is_negative() {
                    return Err(JointSupportError::NegativeProbability);
                }
                sum += p;
            }
            if sum != one {
                return Err(JointSupportError::UnnormalizedBehavior);
            }
        }

        let mut table = Vec::with_capacity(num_alice_settings);
        for x in 0..num_alice_settings {
            let mut row_y = Vec::with_capacity(num_bob_settings);
            for y in 0..num_bob_settings {
                let mut row_a = Vec::with_capacity(num_alice_outcomes);
                for a in 0..num_alice_outcomes {
                    let mut row_b = Vec::with_capacity(num_bob_outcomes);
                    for b in 0..num_bob_outcomes {
                        row_b.push(&pa[x][a] * &pb[y][b]);
                    }
                    row_a.push(row_b);
                }
                row_y.push(row_a);
            }
            table.push(row_y);
        }

        Ok(Self {
            num_alice_settings,
            num_bob_settings,
            num_alice_outcomes,
            num_bob_outcomes,
            table,
        })
    }

    pub fn alice_marginal(&self, x: usize, y: usize, a: usize) -> BigRational {
        let mut sum = BigRational::zero();
        for b in 0..self.num_bob_outcomes {
            sum += &self.table[x][y][a][b];
        }
        sum
    }

    pub fn bob_marginal(&self, x: usize, y: usize, b: usize) -> BigRational {
        let mut sum = BigRational::zero();
        for a in 0..self.num_alice_outcomes {
            sum += &self.table[x][y][a][b];
        }
        sum
    }

    pub fn verify_no_signalling(&self) -> Result<(), JointSupportError> {
        for x in 0..self.num_alice_settings {
            for a in 0..self.num_alice_outcomes {
                let baseline = self.alice_marginal(x, 0, a);
                for y in 1..self.num_bob_settings {
                    if self.alice_marginal(x, y, a) != baseline {
                        return Err(JointSupportError::SignallingDetected);
                    }
                }
            }
        }
        for y in 0..self.num_bob_settings {
            for b in 0..self.num_bob_outcomes {
                let baseline = self.bob_marginal(0, y, b);
                for x in 1..self.num_alice_settings {
                    if self.bob_marginal(x, y, b) != baseline {
                        return Err(JointSupportError::SignallingDetected);
                    }
                }
            }
        }
        Ok(())
    }
}

