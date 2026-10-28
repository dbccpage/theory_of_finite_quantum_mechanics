
use std::collections::{BTreeMap, BTreeSet};

use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use engine_quantum_physics::finite_chsh_correlations::PairwiseBox;
use thiserror::Error;

use crate::error::WdpError;
use crate::stochastic_package::bounded_power;
use crate::types::AuthorityEffect;

pub type Section = Vec<usize>;

pub type SectionDistribution = BTreeMap<Section, BigRational>;

pub type PairDefects = Vec<((usize, usize), BigRational)>;

pub const MAX_ASSIGNMENTS: usize = 1_000_000;

pub const MAX_MEASUREMENTS: usize = 1_000_000;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
#[error(
    "contexts {i} and {j} disagree on overlap section {overlap_section:?}: {weight_i} against {weight_j}"
)]
pub struct SignallingWitness {
    pub i: usize,
    pub j: usize,
    pub overlap_section: Section,
    pub weight_i: BigRational,
    pub weight_j: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
#[error(
    "contexts {i} and {j} have marginal defect {defect} above tolerance {eps} on overlap {overlap:?}"
)]
pub struct ToleranceWitness {
    pub i: usize,
    pub j: usize,
    pub defect: BigRational,
    pub eps: BigRational,
    pub overlap: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum AdapterRefusal {
    #[error("context {0} has no runs")]
    EmptyContext(usize),
    #[error(transparent)]
    Signalling(Box<SignallingWitness>),
    #[error(transparent)]
    ToleranceExceeded(Box<ToleranceWitness>),
    #[error("invalid input: {detail}")]
    InvalidInput { detail: String },
    #[error("crate refusal: {0}")]
    Wdp(#[source] Box<WdpError>),
}

impl From<WdpError> for AdapterRefusal {
    fn from(error: WdpError) -> Self {
        match error {
            WdpError::InvalidInput { detail } => AdapterRefusal::InvalidInput { detail },
            WdpError::Adapter(refusal) => *refusal,
            other => AdapterRefusal::Wdp(Box::new(other)),
        }
    }
}

fn invalid(detail: String) -> AdapterRefusal {
    AdapterRefusal::InvalidInput { detail }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MeasurementCover {
    measurements: usize,
    outcomes: usize,
    contexts: Vec<Vec<usize>>,
}

impl MeasurementCover {
    pub fn new(
        measurements: usize,
        outcomes: usize,
        contexts: Vec<Vec<usize>>,
    ) -> Result<Self, WdpError> {
        let bad = |detail: String| WdpError::InvalidInput { detail };
        if measurements == 0 || outcomes == 0 {
            return Err(bad(
                "a cover needs at least one measurement and one outcome".to_string(),
            ));
        }
        if measurements > MAX_MEASUREMENTS {
            return Err(bad(format!(
                "{measurements} measurements exceed the cap {MAX_MEASUREMENTS}"
            )));
        }
        if contexts.is_empty() {
            return Err(bad("a cover needs at least one context".to_string()));
        }
        for (i, context) in contexts.iter().enumerate() {
            if context.is_empty() {
                return Err(bad(format!("context {i} has no measurements")));
            }
            if context.windows(2).any(|w| w[0] >= w[1]) {
                return Err(bad(format!("context {i} is not strictly increasing")));
            }
            if let Some(&id) = context.iter().find(|&&id| id >= measurements) {
                return Err(bad(format!(
                    "context {i} names measurement {id} outside 0..{measurements}"
                )));
            }
        }
        Ok(Self {
            measurements,
            outcomes,
            contexts,
        })
    }

    pub fn measurements(&self) -> usize {
        self.measurements
    }

    pub fn outcomes(&self) -> usize {
        self.outcomes
    }

    pub fn contexts(&self) -> &[Vec<usize>] {
        &self.contexts
    }

    pub fn overlap(&self, i: usize, j: usize) -> Option<Vec<usize>> {
        (i < self.contexts.len() && j < self.contexts.len()).then(|| self.overlap_unchecked(i, j))
    }

    fn overlap_unchecked(&self, i: usize, j: usize) -> Vec<usize> {
        let cj = &self.contexts[j];
        self.contexts[i]
            .iter()
            .copied()
            .filter(|id| cj.contains(id))
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RunTable {
    runs: Vec<Vec<Section>>,
}

impl RunTable {
    pub fn new(cover: &MeasurementCover, runs: Vec<Vec<Section>>) -> Result<Self, WdpError> {
        check_runs(cover, &runs)?;
        Ok(Self { runs })
    }

    pub fn runs(&self) -> &[Vec<Section>] {
        &self.runs
    }
}

fn check_runs(cover: &MeasurementCover, runs: &[Vec<Section>]) -> Result<(), WdpError> {
    let bad = |detail: String| WdpError::InvalidInput { detail };
    if runs.len() != cover.contexts.len() {
        return Err(bad(format!(
            "{} run lists for {} contexts",
            runs.len(),
            cover.contexts.len()
        )));
    }
    for (i, (context, context_runs)) in cover.contexts.iter().zip(runs).enumerate() {
        for (r, run) in context_runs.iter().enumerate() {
            if run.len() != context.len() {
                return Err(bad(format!(
                    "run {r} of context {i} has {} outcomes, expected {}",
                    run.len(),
                    context.len()
                )));
            }
            if let Some(&o) = run.iter().find(|&&o| o >= cover.outcomes) {
                return Err(bad(format!(
                    "run {r} of context {i} has outcome {o} outside 0..{}",
                    cover.outcomes
                )));
            }
        }
    }
    Ok(())
}

fn restrict(context: &[usize], section: &[usize], onto: &[usize]) -> Section {
    onto.iter()
        .filter_map(|id| context.iter().position(|c| c == id).map(|p| section[p]))
        .collect()
}

fn marginal(context: &[usize], dist: &SectionDistribution, onto: &[usize]) -> SectionDistribution {
    let mut out = SectionDistribution::new();
    for (section, weight) in dist {
        *out.entry(restrict(context, section, onto))
            .or_insert_with(BigRational::zero) += weight;
    }
    out
}

pub fn l1_distance(a: &SectionDistribution, b: &SectionDistribution) -> BigRational {
    let keys: BTreeSet<&Section> = a.keys().chain(b.keys()).collect();
    let zero = BigRational::zero();
    let difference: Vec<_> = keys
        .into_iter()
        .map(|key| a.get(key).unwrap_or(&zero) - b.get(key).unwrap_or(&zero))
        .collect();
    engine_functional::Phi1Functional::unweighted_l1_rational(&difference)
        .expect("exact section frequencies")
}

fn check_table_shape(cover: &MeasurementCover, table: &RunTable) -> Result<(), AdapterRefusal> {
    Ok(check_runs(cover, &table.runs)?)
}

pub fn frequencies(
    cover: &MeasurementCover,
    table: &RunTable,
) -> Result<Vec<SectionDistribution>, AdapterRefusal> {
    check_table_shape(cover, table)?;
    let mut all = Vec::with_capacity(table.runs.len());
    for (i, runs) in table.runs.iter().enumerate() {
        if runs.is_empty() {
            return Err(AdapterRefusal::EmptyContext(i));
        }
        let total = BigRational::from_integer(runs.len().into());
        let mut dist = SectionDistribution::new();
        for run in runs {
            *dist.entry(run.clone()).or_insert_with(BigRational::zero) += BigRational::one();
        }
        for weight in dist.values_mut() {
            *weight = &*weight / &total;
        }
        all.push(dist);
    }
    Ok(all)
}

fn pairs(count: usize) -> impl Iterator<Item = (usize, usize)> {
    (0..count).flat_map(move |i| ((i + 1)..count).map(move |j| (i, j)))
}

fn pair_marginals(
    cover: &MeasurementCover,
    dists: &[SectionDistribution],
    i: usize,
    j: usize,
) -> (Vec<usize>, SectionDistribution, SectionDistribution) {
    let overlap = cover.overlap_unchecked(i, j);
    let mu_i = marginal(&cover.contexts[i], &dists[i], &overlap);
    let mu_j = marginal(&cover.contexts[j], &dists[j], &overlap);
    (overlap, mu_i, mu_j)
}

fn check_compatible(
    cover: &MeasurementCover,
    dists: &[SectionDistribution],
) -> Result<(), AdapterRefusal> {
    for (i, j) in pairs(dists.len()) {
        let (_, mu_i, mu_j) = pair_marginals(cover, dists, i, j);
        let keys: BTreeSet<&Section> = mu_i.keys().chain(mu_j.keys()).collect();
        let zero = BigRational::zero();
        for key in keys {
            let (weight_i, weight_j) = (
                mu_i.get(key).unwrap_or(&zero),
                mu_j.get(key).unwrap_or(&zero),
            );
            if weight_i != weight_j {
                return Err(AdapterRefusal::Signalling(Box::new(SignallingWitness {
                    i,
                    j,
                    overlap_section: key.clone(),
                    weight_i: weight_i.clone(),
                    weight_j: weight_j.clone(),
                })));
            }
        }
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EmpiricalModel {
    cover: MeasurementCover,
    distributions: Vec<SectionDistribution>,
    authority_effect: AuthorityEffect,
}

impl EmpiricalModel {
    pub fn new(
        cover: MeasurementCover,
        distributions: Vec<SectionDistribution>,
    ) -> Result<Self, AdapterRefusal> {
        if distributions.len() != cover.contexts.len() {
            return Err(invalid(format!(
                "{} distributions for {} contexts",
                distributions.len(),
                cover.contexts.len()
            )));
        }
        let mut canonical = Vec::with_capacity(distributions.len());
        for (i, (context, dist)) in cover.contexts.iter().zip(&distributions).enumerate() {
            let mut total = BigRational::zero();
            let mut kept = SectionDistribution::new();
            for (section, weight) in dist {
                if section.len() != context.len() || section.iter().any(|&o| o >= cover.outcomes) {
                    return Err(invalid(format!(
                        "context {i} has a malformed section {section:?}"
                    )));
                }
                if weight.is_negative() {
                    return Err(invalid(format!(
                        "context {i} has negative weight {weight} on {section:?}"
                    )));
                }
                total += weight;
                if !weight.is_zero() {
                    kept.insert(section.clone(), weight.clone());
                }
            }
            if !total.is_one() {
                return Err(invalid(format!(
                    "context {i} has total weight {total}, not 1"
                )));
            }
            canonical.push(kept);
        }
        check_compatible(&cover, &canonical)?;
        Ok(Self {
            cover,
            distributions: canonical,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn cover(&self) -> &MeasurementCover {
        &self.cover
    }

    pub fn distributions(&self) -> &[SectionDistribution] {
        &self.distributions
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        self.authority_effect
    }

    pub fn positive_global_assignments(&self) -> Result<Vec<Section>, WdpError> {
        self.positive_global_assignments_with_limit(MAX_ASSIGNMENTS)
    }

    pub fn positive_global_assignments_with_limit(
        &self,
        limit: usize,
    ) -> Result<Vec<Section>, WdpError> {
        let (m, k) = (self.cover.measurements, self.cover.outcomes);
        if m > limit {
            return Err(WdpError::InvalidInput {
                detail: format!("{m} measurements exceed the enumeration cap {limit}"),
            });
        }
        bounded_power(k, m, limit).ok_or_else(|| WdpError::InvalidInput {
            detail: format!("more than {limit} global assignments; enumeration refused"),
        })?;
        let mut positive = Vec::new();
        let mut assignment = vec![0usize; m];
        loop {
            let supported =
                self.cover
                    .contexts
                    .iter()
                    .zip(&self.distributions)
                    .all(|(context, dist)| {
                        let section: Section = context.iter().map(|&id| assignment[id]).collect();
                        dist.contains_key(&section)
                    });
            if supported {
                positive.push(assignment.clone());
            }
            let mut position = m;
            loop {
                if position == 0 {
                    return Ok(positive);
                }
                position -= 1;
                assignment[position] += 1;
                if assignment[position] < k {
                    break;
                }
                assignment[position] = 0;
            }
        }
    }

    pub fn has_positive_global_assignment(&self) -> Result<bool, WdpError> {
        Ok(!self.positive_global_assignments()?.is_empty())
    }
}

pub fn adapt_exact(
    cover: &MeasurementCover,
    table: &RunTable,
) -> Result<EmpiricalModel, AdapterRefusal> {
    let freqs = frequencies(cover, table)?;
    EmpiricalModel::new(cover.clone(), freqs)
}

fn defects_of(cover: &MeasurementCover, freqs: &[SectionDistribution]) -> PairDefects {
    pairs(freqs.len())
        .map(|(i, j)| {
            let (_, mu_i, mu_j) = pair_marginals(cover, freqs, i, j);
            ((i, j), l1_distance(&mu_i, &mu_j))
        })
        .collect()
}

pub fn signalling_defect(
    cover: &MeasurementCover,
    table: &RunTable,
) -> Result<PairDefects, AdapterRefusal> {
    Ok(defects_of(cover, &frequencies(cover, table)?))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TolerantModel {
    pub frequencies: Vec<SectionDistribution>,
    pub defects: PairDefects,
    pub max_defect: BigRational,
    pub eps: BigRational,
    pub authority_effect: AuthorityEffect,
}

pub fn adapt_tolerant(
    cover: &MeasurementCover,
    table: &RunTable,
    eps: &BigRational,
) -> Result<TolerantModel, AdapterRefusal> {
    if eps.is_negative() {
        return Err(invalid(format!("tolerance {eps} is negative")));
    }
    let freqs = frequencies(cover, table)?;
    let defects = defects_of(cover, &freqs);
    if let Some(((i, j), defect)) = defects.iter().find(|(_, d)| d > eps) {
        let overlap = cover.overlap(*i, *j).unwrap_or_default();
        return Err(AdapterRefusal::ToleranceExceeded(Box::new(
            ToleranceWitness {
                i: *i,
                j: *j,
                defect: defect.clone(),
                eps: eps.clone(),
                overlap,
            },
        )));
    }
    let max_defect =
        defects.iter().fold(
            BigRational::zero(),
            |acc, (_, d)| if d > &acc { d.clone() } else { acc },
        );
    Ok(TolerantModel {
        frequencies: freqs,
        defects,
        max_defect,
        eps: eps.clone(),
        authority_effect: AuthorityEffect::None,
    })
}

pub fn l1_distance_to_model(
    frequencies: &[SectionDistribution],
    model: &EmpiricalModel,
) -> Result<Vec<BigRational>, AdapterRefusal> {
    if frequencies.len() != model.distributions.len() {
        return Err(invalid(format!(
            "{} frequency vectors for {} contexts",
            frequencies.len(),
            model.distributions.len()
        )));
    }
    Ok(frequencies
        .iter()
        .zip(&model.distributions)
        .map(|(f, m)| l1_distance(f, m))
        .collect())
}

fn canonical_extension(context: &[usize], overlap: &[usize], t: &[usize]) -> Section {
    context
        .iter()
        .map(|id| overlap.iter().position(|o| o == id).map_or(0, |q| t[q]))
        .collect()
}

pub fn two_context_repair(
    cover: &MeasurementCover,
    table: &RunTable,
) -> Result<EmpiricalModel, AdapterRefusal> {
    if cover.contexts.len() != 2 {
        return Err(invalid(format!(
            "two-context repair needs exactly 2 contexts, found {}",
            cover.contexts.len()
        )));
    }
    let freqs = frequencies(cover, table)?;
    let (overlap, mu_0, mu_1) = pair_marginals(cover, &freqs, 0, 1);
    let two = BigRational::from_integer(2.into());
    let mut nu = SectionDistribution::new();
    for key in mu_0.keys().chain(mu_1.keys()) {
        let zero = BigRational::zero();
        let average = (mu_0.get(key).unwrap_or(&zero) + mu_1.get(key).unwrap_or(&zero)) / &two;
        nu.insert(key.clone(), average);
    }
    let mut repaired = Vec::with_capacity(2);
    for (context, (freq, mu)) in cover.contexts.iter().zip(freqs.iter().zip([&mu_0, &mu_1])) {
        let mut dist = SectionDistribution::new();
        for (section, weight) in freq {
            let t = restrict(context, section, &overlap);
            let (Some(mu_t), Some(nu_t)) = (mu.get(&t), nu.get(&t)) else {
                return Err(invalid(format!(
                    "overlap section {t:?} has no marginal weight"
                )));
            };
            *dist
                .entry(section.clone())
                .or_insert_with(BigRational::zero) += weight * nu_t / mu_t;
        }
        for (t, nu_t) in &nu {
            if !mu.contains_key(t) {
                *dist
                    .entry(canonical_extension(context, &overlap, t))
                    .or_insert_with(BigRational::zero) += nu_t;
            }
        }
        repaired.push(dist);
    }
    EmpiricalModel::new(cover.clone(), repaired)
}

pub fn chsh_cover() -> Result<MeasurementCover, WdpError> {
    MeasurementCover::new(4, 2, vec![vec![0, 2], vec![0, 3], vec![1, 2], vec![1, 3]])
}

pub fn pr_box_run_table() -> Result<RunTable, WdpError> {
    let cover = chsh_cover()?;
    let runs = (0..2usize)
        .flat_map(|x| (0..2usize).map(move |y| (x, y)))
        .map(|(x, y)| {
            [0usize, 1]
                .iter()
                .map(|&a| vec![a, a ^ (x * y)])
                .collect::<Vec<Section>>()
        })
        .collect();
    RunTable::new(&cover, runs)
}

pub fn global_run_table(
    cover: &MeasurementCover,
    assignments: &[Section],
) -> Result<RunTable, WdpError> {
    if let Some(bad) = assignments.iter().find(|a| a.len() != cover.measurements) {
        return Err(WdpError::InvalidInput {
            detail: format!(
                "global run assigns {} measurements, expected {}",
                bad.len(),
                cover.measurements
            ),
        });
    }
    let runs = cover
        .contexts
        .iter()
        .map(|context| {
            assignments
                .iter()
                .map(|a| context.iter().map(|&id| a[id]).collect())
                .collect()
        })
        .collect();
    RunTable::new(cover, runs)
}

fn require_chsh_model(model: &EmpiricalModel) -> Result<(), AdapterRefusal> {
    if model.cover == chsh_cover()? {
        Ok(())
    } else {
        Err(invalid("the model is not on the CHSH cover".to_string()))
    }
}

pub fn chsh_pairwise_box(model: &EmpiricalModel) -> Result<PairwiseBox, AdapterRefusal> {
    require_chsh_model(model)?;
    let mut coordinates = vec![BigRational::zero(); 16];
    for (context, dist) in model.distributions.iter().enumerate() {
        for (section, weight) in dist {
            coordinates[4 * context + 2 * section[0] + section[1]] = weight.clone();
        }
    }
    PairwiseBox::new(coordinates).map_err(|e| AdapterRefusal::from(WdpError::from(e)))
}

pub fn chsh_correlator(
    model: &EmpiricalModel,
    x: usize,
    y: usize,
) -> Result<BigRational, AdapterRefusal> {
    chsh_pairwise_box(model)?
        .correlator(x, y)
        .map_err(|e| AdapterRefusal::from(WdpError::from(e)))
}

pub fn chsh_value(model: &EmpiricalModel) -> Result<BigRational, AdapterRefusal> {
    Ok(chsh_pairwise_box(model)?.chsh())
}
